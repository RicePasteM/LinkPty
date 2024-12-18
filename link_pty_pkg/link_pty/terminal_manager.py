import asyncio
import json
import os
import pty
import select
import subprocess
import websockets
import requests
import argparse
import signal
import psutil  # 需要安装此库

os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"
os.environ["TERM"] = "xterm-256color"

class TerminalManager:
    current_key = None  # 类变量，用于保存 key
    terminals = []
    ws = None
    buf = []

    def __init__(self, base_url):
        self.BASE_SERVER_URL = base_url
        if TerminalManager.current_key is not None:
            self.key = TerminalManager.current_key
        else:
            self.key = None  # 初次连接时 key 为 None

    def is_ws_connected(self):
        """检查 WebSocket 连接状态"""
        try:
            return self.ws.open if hasattr(self.ws, 'open') else True
        except:
            return False

    async def read_and_save_buf(self, master_fd: int, terminal_index: int):
        """持续读取伪终端的输出并通过 WebSocket 转发给客户端"""
        try:
            while True:
                await asyncio.sleep(0.1)  # 非阻塞等待
                rlist, _, _ = select.select([master_fd], [], [], 0.1)
                if master_fd in rlist:
                    output = os.read(master_fd, 2048).decode("utf-8", errors="ignore")
                    print(output)
                    self.buf.append((terminal_index, output))
        except Exception as e:
            print(f"Error while reading pty output: {e}")
    
    async def forward_output(self):
        while True:
            try:
                await asyncio.sleep(0.1)  # 非阻塞等待
                if len(self.buf) > 0 and self.is_ws_connected():
                    terminal_index : int = self.buf[0][0]
                    outputs = list([item[1] for item in self.buf if item[0] == terminal_index])
                    self.buf = list(filter(lambda item: item[0] != terminal_index, self.buf))
                    await self.ws.send(json.dumps({"operation": "RECEIVE_SERVEROUTPUT", "terminal_index": terminal_index, "data": ''.join(outputs)}))
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                print(f"Error while reading pty output: {e}")
    
    async def ping(self):
        while True:
            try:
                await asyncio.sleep(60)  # 非阻塞等待
                if self.is_ws_connected():
                    await self.ws.send(json.dumps({"operation": "PING"}))
            except websockets.exceptions.ConnectionClosed:
                break
            except Exception as e:
                print(f"Ping error: {e}")

    async def on_message(self, ws):
        try:
            async for message in ws:
                data_json = json.loads(message)
                operation = data_json["operation"]
                if operation == "ASSIGN_KEY":
                    TerminalManager.current_key = data_json["key"]
                    self.key = data_json['key']
                    print(f"Please use this code to connect to the pseudo terminal: {data_json['key']}")
                elif operation == "CREATE_TERMINAL":
                    # 创建伪终端
                    master_fd, slave_fd = pty.openpty()
                    process = subprocess.Popen(
                        ["/bin/bash"],
                        stdin=slave_fd, stdout=slave_fd, stderr=slave_fd, close_fds=True
                    )
                    TerminalManager.terminals.append((process, master_fd, slave_fd))
                    requests.get(f"http://{self.BASE_SERVER_URL}/create_terminal_done?key={self.key}&terminal_index={len(TerminalManager.terminals) - 1}")

                    # 使用 asyncio 创建任务
                    asyncio.ensure_future(self.read_and_save_buf(master_fd, len(TerminalManager.terminals) - 1))
                    print(f"Created new pseudo terminal #{len(TerminalManager.terminals) - 1}")
                elif operation == "TERMINATE_TERMINAL":
                    terminal = TerminalManager.terminals[data_json["terminal_index"]]
                    terminal[0].terminate()  # 终止子进程
                    os.close(terminal[1])
                    os.close(terminal[2])
                elif operation == "RECEIVE_USERINPUT":
                    terminal = TerminalManager.terminals[data_json["terminal_index"]]
                    user_input = data_json["data"]
                    
                    # 检查是否是 Ctrl+C (ASCII 3 对应 Ctrl+C)
                    if user_input == '\x03':
                        # 获取伪终端的子进程
                        process = psutil.Process(terminal[0].pid)
                        children = process.children(recursive=True)  # 获取所有子进程
                        
                        if children:
                            # 发送 SIGINT 给第一个子进程
                            os.kill(children[0].pid, signal.SIGINT)
                        else:
                            print("No child processes to terminate.")
                    else:
                        os.write(terminal[1], user_input.encode('utf-8'))
        except Exception as e:
            print(f"Error handling message: {e}")

    async def main(self):
        asyncio.ensure_future(self.forward_output())
        asyncio.ensure_future(self.ping())
        while True:
            await asyncio.sleep(1)
            try:
                websocket_url = f"ws://{self.BASE_SERVER_URL}/dockerserver" + (f"?key={TerminalManager.current_key}" if TerminalManager.current_key is not None else "")
                if TerminalManager.current_key is not None:
                    websocket_url += "&histories="
                    for index, terminal in enumerate(TerminalManager.terminals):
                        if terminal[0].poll() is None: # 说明进程还在执行中
                            websocket_url += "1"
                        else:
                            websocket_url += "0"
                print(f"Connecting to {websocket_url} ...")
                async with websockets.connect(websocket_url) as ws:
                    self.ws = ws
                    await self.on_message(ws)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed: {e}. Reconnecting in 5 seconds...")
            except Exception as e:
                print(f"Unexpected error: {e}. Reconnecting in 5 seconds...")

def run_terminal_manager():
    parser = argparse.ArgumentParser(description='Run the terminal manager.')
    parser.add_argument('--base-url', type=str, required=False, default="linkpty.codesocean.top:43143", help='Base URL for the WebSocket server.')
    args = parser.parse_args()
    manager = TerminalManager(args.base_url)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(manager.main())

if __name__ == "__main__":
    try:
        run_terminal_manager()
    except Exception as e:
        print(e)
