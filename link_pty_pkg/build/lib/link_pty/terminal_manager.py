import asyncio
import json
import os
import pty
import select
import subprocess
import websockets
import requests
import argparse

class TerminalManager:
    current_key = None  # 类变量，用于保存 key
    terminals = []

    def __init__(self, base_url):
        self.BASE_SERVER_URL = base_url
        if TerminalManager.current_key is not None:
            self.key = TerminalManager.current_key
        else:
            self.key = None  # 初次连接时 key 为 None

    async def read_and_forward_output(self, ws, master_fd: int, terminal_index: int):
        """持续读取伪终端的输出并通过 WebSocket 转发给客户端"""
        try:
            while ws.open:
                await asyncio.sleep(0.1)  # 非阻塞等待
                rlist, _, _ = select.select([master_fd], [], [], 0.1)
                if master_fd in rlist:
                    output = os.read(master_fd, 2048).decode("utf-8", errors="ignore")
                    await ws.send(json.dumps({"operation": "RECEIVE_SERVEROUTPUT", "terminal_index": terminal_index, "data": output}))
        except Exception as e:
            print(f"Error while reading pty output: {e}")
    
    async def ping(self, ws):
        try:
            while ws.open:
                await asyncio.sleep(60)  # 非阻塞等待
                await ws.send(json.dumps({"operation": "PING"}))
        except websockets.exceptions.ConnectionClosed:
            print("WebSocket connection closed. Stopping ping.")
        except Exception as e:
            print(f"Ping error: {e}")

    async def on_message(self, ws):
        async for message in ws:
            try:
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
                    asyncio.create_task(self.read_and_forward_output(ws, master_fd, len(TerminalManager.terminals) - 1))
                    print(f"Created new pseudo terminal #{len(TerminalManager.terminals) - 1}")
                elif operation == "TERMINATE_TERMINAL":
                    terminal = TerminalManager.terminals[data_json["terminal_index"]]
                    terminal[0].terminate()  # 终止子进程
                    os.close(terminal[1])
                    os.close(terminal[2])
                elif operation == "RECEIVE_USERINPUT":
                    print(data_json)
                    terminal = TerminalManager.terminals[data_json["terminal_index"]]
                    os.write(terminal[1], data_json["data"].encode('utf-8'))
            except Exception as e:
                print(f"Error handling message: {e}")

    async def main(self):
        for i in range(0, 10):
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
                    for index, terminal in enumerate(TerminalManager.terminals):
                        if terminal[0].poll() is None: # 说明进程还在执行中
                            asyncio.create_task(self.read_and_forward_output(ws, terminal[1], index))
                            print(f"Relinked pseudo terminal #{index}")
                        else:
                            websocket_url += "0"
                    asyncio.create_task(self.ping(ws))
                    await self.on_message(ws)
            except websockets.exceptions.ConnectionClosedError as e:
                print(f"Connection closed: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)  # 等待 5 秒后重新连接
            except Exception as e:
                print(f"Unexpected error: {e}. Reconnecting in 5 seconds...")
                await asyncio.sleep(5)

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
