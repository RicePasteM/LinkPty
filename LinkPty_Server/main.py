from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import random
import json
import string
import os
from datetime import datetime
import re
from fastapi.staticfiles import StaticFiles
import asyncio

os.environ["LANG"] = "en_US.UTF-8"
os.environ["LC_ALL"] = "en_US.UTF-8"
os.environ["TERM"] = "xterm-256color"

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

servers = dict()


class Server:
    def __init__(self, websocket: WebSocket):
        self.terminals = []
        self.websocket = websocket
        self.client = None

class Terminal:
    def __init__(self, key : str, terminal_index : int, is_online : bool = True):
        self.terminal_index = terminal_index
        self.is_online = is_online
        self.key = key
        # 为每个终端创建对应的日志文件
        self.log_file = f"./data/terminal_{key}_{terminal_index}.txt"
        if is_online:
            if not os.path.exists('./data'):
                os.makedirs('./data')

    # 记录 SERVEROUTPUT
    def log_server_output(self, output):
        with open(self.log_file, 'a', encoding="utf8") as f:
            f.write(output)

def generate_key(key_length=8):
    key = ''.join(random.choices(string.ascii_letters + string.digits, k=key_length))
    return key

app.mount("/static", StaticFiles(directory="static"), name="static")

# 服务端连接
@app.websocket("/dockerserver")
async def dockerserver(websocket: WebSocket):
    global servers
    # 检查客户端是否给了key
    key = websocket.query_params.get("key")
    
    if key is None:
        key = generate_key()
        servers[key] = Server(websocket)
    else:
        # 从服务端提供的信息中恢复
        servers[key] = Server(websocket)
        # 恢复所有的terminal
        terminals = websocket.query_params.get("histories")
        if terminals is None:
            terminals = []
        for index, is_online in enumerate(terminals):
            # print(is_online)
            servers[key].terminals.append(Terminal(key, index, True if is_online == "1" else False))

    await websocket.accept()
    await websocket.send_text(json.dumps({"operation": "ASSIGN_KEY", "key": key}))
    
    while True:
        try:
            data = await websocket.receive_text()
            print(data)
            data_json = json.loads(data)
            operation = data_json["operation"]
            if operation == "RECEIVE_SERVEROUTPUT":
                terminal_index = data_json["terminal_index"]
                server: Server = servers[key]
                terminal: Terminal = server.terminals[terminal_index]
                terminal.log_server_output(data_json["data"])  # 记录SERVEROUTPUT
                client: WebSocket = server.client
                if client is not None:
                    await client.send_text(json.dumps(data_json))
            elif operation == "PING":
                server: Server = servers[key]
                await server.websocket.send_text(json.dumps({"operation": "PONG"}))
        except WebSocketDisconnect:
            print(f"服务端 {key} 断开连接")
            await websocket.close()
            servers.pop(key)
            break
        except Exception as e:
            print(e)
            await websocket.close()
            servers.pop(key)
            break

# 客户端连接
@app.websocket("/dockerclient")
async def dockerclient(websocket: WebSocket):
    global servers
    key = websocket.query_params.get('key')
    if servers.get(key) is not None:
        server: Server = servers[key]
        server.client = websocket
        await websocket.accept()
        while True:
            try:
                data = await websocket.receive_text()
                data_json = json.loads(data)
                operation = data_json["operation"]
                if operation == "RECEIVE_USERINPUT":
                    print("RECEIVE_USERINPUT")
                    terminal: Terminal = server.terminals[data_json["terminal_index"]]
                    if terminal.is_online:
                        await server.websocket.send_text(json.dumps(data_json))
                    else:
                        pass
                elif operation == "PING":
                    server: Server = servers[key]
                    client: WebSocket = server.client
                    await client.send_text(json.dumps({"operation": "PONG"}))
            except WebSocketDisconnect:
                print(f"客户端 {key} 断开连接")
                server: Server = servers[key]
                server.client = None
                break
            except Exception as e:
                await websocket.close()
                server: Server = servers[key]
                server.client = None
                break
    else:
        await websocket.close(reason="主机不存在")

@app.get("/create_terminal")
async def create_terminal(key: str):
    if servers.get(key) is not None:
        server: Server = servers[key]
        await server.websocket.send_text(json.dumps({"operation": "CREATE_TERMINAL"}))
        return {"result": "success"}
    else:
        return {"result": "fail", "msg": "主机不存在"}

@app.get("/create_terminal_done")
async def create_terminal_done(key: str, terminal_index: int):
    if servers.get(key) is not None:
        server: Server = servers[key]
        for terminal in server.terminals:
            terminal: Terminal = terminal
            if terminal.terminal_index == terminal_index:
                client: WebSocket = server.client
                await client.send_text(json.dumps({"operation": "RESET_TERMINAL_DONE", "terminal_index": terminal_index}))
                return {"result": "reset", "msg": "已重置终端"}
        server.terminals.append(Terminal(key, terminal_index))
        client: WebSocket = server.client
        await client.send_text(json.dumps({"operation": "CREATE_TERMINAL_DONE", "terminal_index": terminal_index}))
        return {"result": "success"}
    else:
        return {"result": "fail", "msg": "主机不存在"}

@app.get("/terminate_terminal")
async def terminate_terminal(key: str, terminal_index: int):
    if servers.get(key) is not None:
        server: Server = servers[key]
        await server.websocket.send_text(json.dumps({"operation": "TERMINATE_TERMINAL", "terminal_index": terminal_index}))
        terminal: Terminal = server.terminals[terminal_index]
        terminal.is_online = False
        return {"result": "success"}
    else:
        return {"result": "fail", "msg": "主机不存在"}

# 获取某个 Terminal 的历史记录
@app.get("/get_history")
async def get_history(key: str, terminal_index: int):
    try:
        log_file = f"./data/terminal_{key}_{terminal_index}.txt"
        if not os.path.exists(log_file):
            with open(log_file, 'a', encoding="utf8") as f:
                f.write("\n")
        with open(log_file, 'r', encoding="utf8") as file:
            content = file.readlines()
            content = [line.strip() for line in content[-2000:]]
            return {"result": "success", "history": content}
    except Exception as e:
        return {"result": "fail", "msg": str(e)}
    
# 获取某个 Key 对应的服务状态
@app.get("/get_status")
async def get_status(key: str):
    if servers.get(key) is not None:
        try:
            server: Server = servers[key]
            terminals = []
            for terminal in server.terminals:
                terminal : Terminal = terminal
                terminals.append(
                    {
                        "terminal_index": terminal.terminal_index,
                        "is_online": terminal.is_online
                    }
                )
            return {"result": "success", "terminals": terminals}
        except Exception as e:
            return {"result": "fail", "msg": str(e)}
    else:
        # 用于存储匹配到的 index
        terminals = []

        # 定义文件名的正则表达式模式，匹配 terminal_{key}_{index}.txt
        pattern = re.compile(r'terminal_.+_(\d+)\.txt')

        # 遍历文件夹中的所有文件
        for file_name in os.listdir("./data/"):
            match = pattern.match(file_name)
            if match:
                # 提取 index 并添加到列表中
                index = int(match.group(1))
                if key in file_name:
                    terminals.append({
                        "terminal_index": index,
                        "is_online": False
                    })
        return {"result": "offline", "terminals": terminals}

@app.get("/reset_terminal")
async def reset_terminal(key: str, terminal_index: int):
    if servers.get(key) is not None:
        server: Server = servers[key]
        await server.websocket.send_text(json.dumps({
            "operation": "RESET_TERMINAL", 
            "terminal_index": terminal_index
        }))
        return {"result": "success"}
    else:
        return {"result": "fail", "msg": "主机不存在"}
