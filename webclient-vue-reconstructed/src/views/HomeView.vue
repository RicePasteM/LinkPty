<template>
    <div class="tabWrapper">
      <div class="tabs">
        <div class="tab" style="width: auto" onclick="window.open('https:\/\/github.com/RicePasteM/LinkPty')">
          <span class="name" style="display: flex; align-items:center; font-family: DatCub;">
            <img src="@/assets/favicon.png" alt="" style="height: 20px; margin: 0 5px; "> LinkPty </span>
        </div>
      </div>
      <div class="btn" style="width: 40px; display: flex; justify-content: center; align-items: center;"
        onclick="window.showSearchBar()">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search"
          viewBox="0 0 16 16" style="transform: scale(1)">
          <path
            d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0" />
        </svg>
      </div>
      <div class="btn" style="width: 40px; display: flex; justify-content: center; align-items: center;"
        onclick="window.settingsModal.show()">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear"
          viewBox="0 0 16 16">
          <path
            d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0" />
          <path
            d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z" />
        </svg>
      </div>
    </div>
    <div class="terminals">
      <TerminalVue class="terminal" v-for="(tab, index) in tabs" :key="tab.tabIndex" :ref="el => termRefs[tab.tabIndex] = el"
        :style="{'zIndex': selectedTab == tab ? 1 : 0}" @data="handleTermUserInput(tab, $event)" />
    </div>

    <!-- Modal -->
    <div class="modal fade" id="settingsModal" tabindex="-1" aria-labelledby="settingsModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="modal-title fs-5" id="settingsModalLabel">Settings</h3>
            <button type="button" class="btn btn-close" data-bs-dismiss="modal" aria-label="Close">×</button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label for="fontSelect">终端字体</label>
              <select id="fontSelect" class="form-control">
                <option value="monospace">Monospace</option>
                <option value="Consolas">Consolas</option>
                <option value="Courier New">Courier New</option>
              </select>
            </div>
            <div class="form-group">
              <label for="fontSizeSelect">终端字号</label>
              <input type="number" id="fontSizeSelect" class="form-control" value="14" min="8" max="72" />
            </div>
            <!-- <div class="form-group">
                        <div>结束任务 </div>
                        <button type="button" id="stopTask" class="btn btn-danger" onclick="stopTask()">停止任务</button>
                    </div> -->
            <div class="form-group">
              <div>强制重置当前终端（仅当出现问题时使用）</div>
              <button type="button" id="forceReconnect" class="btn btn-warning" onclick="forceReconnect()">立即重置</button>
            </div>
            <div class="form-group">
              <div>下载当前终端日志</div>
              <button type="button" id="downloadLog" class="btn btn-info" onclick="downloadTerminalLog()">下载日志</button>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" onclick="applySettings()">应用设置</button>
          </div>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useMessage} from 'naive-ui'
import TerminalVue from '@/components/Terminal.vue'

const SERVER_URL = "linkpty.codesocean.top:43143";

// 读取设置并应用
const savedFont = localStorage.getItem('terminalFont') || 'consolas';
const savedFontSize = localStorage.getItem('terminalFontSize') || '16';

const message = useMessage()

let tabs = ref([]);
let selectedTab = ref(undefined);
let termRefs = ref({});

let socket = undefined;

const handleTermUserInput = (tab, input) => {
  if (tab.isOnline) {
    socket.send(JSON.stringify({
      "operation": "RECEIVE_USERINPUT",
      "data": input,
      "terminal_index": tab.tabIndex
    }));
  }
}

window.onload = async function () {
  // 设置下拉框和输入框的初始值
  document.getElementById('fontSelect').value = savedFont;
  document.getElementById('fontSizeSelect').value = savedFontSize;

  // Modal
  window.settingsModal = new bootstrap.Modal(document.getElementById('settingsModal'));



  // 历史连接码，最多保存5个
  const historyKeys = JSON.parse(localStorage.getItem('historyKeys')) || [];

  const { value: key } = await Swal.fire({
    title: "Please input code to link",
    html: `
                    <input style="width: 80%;" type="text" id="keyInput" class="swal2-input" placeholder="Please input key">
                    <div class="history" style="margin-top: 10px;">
                        <div class="d-flex justify-content-center align-items-center mb-1">
                            <span style="margin-right: 10px;">Histories </span>
                            ${historyKeys.map((k, index) => `
                                    <button style="margin-right: 5px;" class="btn btn-secondary btn-sm history-key" onclick="document.getElementById('keyInput').value = '${k}';">${k}</button>
                            `).join('')}
                        </div>
                    </div>
                `,
    focusConfirm: false,
    preConfirm: () => {
      const keyValue = document.getElementById('keyInput').value;
      if (!keyValue) {
        Swal.showValidationMessage('Please input key');
      }
      return keyValue;
    }
  });

  if (key) {
    // 如果输入的连接码有效，保存到历史中
    if (!historyKeys.includes(key)) {
      historyKeys.unshift(key);
      if (historyKeys.length > 5) historyKeys.pop(); // 保持最多5个历史记录
      localStorage.setItem('historyKeys', JSON.stringify(historyKeys));
    }
    document.title = key + " - " + document.title;
  } else {
    location.reload();
  }

  function createWebsocket() {
    return new Promise((resolve, reject) => {
      let socket = new WebSocket(`ws://${SERVER_URL}/dockerclient?key=${key}`);

      // 显示终端输出
      socket.onmessage = function (event) {
        let jsonData = JSON.parse(event.data);
        if (jsonData.operation == "CREATE_TERMINAL_DONE") {
          handleCreateNewTabDone(jsonData.terminal_index)
        } else if (jsonData.operation == "RECEIVE_SERVEROUTPUT") {
          for (let item of tabs.value) {
            if (item.tabIndex == jsonData.terminal_index) {
              termRefs.value[item.tabIndex].write(jsonData.data);
            }
          }
        } else if (jsonData.operation == "RESET_TERMINAL_DONE") {
          Swal.fire({
            icon: 'success',
            title: 'Reset Successfully'
          });
        }
      };

      socket.onopen = function (event) {
        setInterval(() => {
          socket.send(JSON.stringify({
            "operation": "PING"
          }))
        }, 60000)
        resolve(socket);
      }
    });
  }

  // 首先检查状态
  setTimeout(() => {
    fetch(`http://${SERVER_URL}/get_status?key=${key}`, {
      method: 'GET',
      headers: new Headers(),
      redirect: 'follow'
    })
      .then(response => response.text())
      .then(async function (result) {
        result = JSON.parse(result);
        if (result.result == "offline") {
          message.warning("该主机已经离线，将加载历史记录。")
          for (let terminal of result.terminals) {
            handleCreateNewTabDone(terminal.terminal_index, false)
            nextTick(() => handleGetTerminalHistory(terminal.terminal_index))
          }
        } else if (result.result == "success") {
          socket = await createWebsocket();
          if (result.terminals.length == 0) {
            handleCreateNewTab();
          } else {
            for (let terminal of result.terminals) {
              handleCreateNewTabDone(terminal.terminal_index, terminal.is_online)
              nextTick(() => handleGetTerminalHistory(terminal.terminal_index))
            }
          }
        } else {
          message.warning(result.msg);
        }
      })
      .catch(error => { console.log(error); message.error("检查状态时出错") });
  }, 500);




  function handleCreateNewTab() {
    fetch(`http://${SERVER_URL}/create_terminal?key=${key}`, {
      method: 'GET',
      headers: new Headers(),
      redirect: 'follow'
    })
      .then(response => response.text())
      .then(result => {
        result = JSON.parse(result);
        if (result.result != "success") {
          message.info(result.msg)
        }
      })
      .catch(error => message.error("创建新标签时出错"));
  }

  function handleCreateNewTabDone(terminalIndex, isOnline = true) {
    tabs.value.push(
      {
        name: "新标签",
        tabIndex: terminalIndex,
        isOnline
      }
    )
    if (isOnline) {
      // socket.send(JSON.stringify({
      //   "operation": "RECEIVE_USERINPUT",
      //   "data": `stty cols ${term.cols} rows ${term.rows}\r\n`,
      //   "terminal_index": terminalIndex
      // }));
    } else {
      termRefs.value[terminalIndex].write("\r\nThis terminal is offline, below are histories.\r\n")
    }
    selectedTab.value = tabs.value[tabs.value.length - 1];
    drawTabs();
  }

  function handleCloseTerminal(terminalIndex) {
    fetch(`http://${SERVER_URL}/terminate_terminal?key=${key}&terminal_index=${terminalIndex}`, {
      method: 'GET',
      headers: new Headers(),
      redirect: 'follow'
    })
      .then(response => response.text())
      .then(result => {
        result = JSON.parse(result);
        if (result.result != "success") {
          message.info(result.msg)
        } else {
          for (let i = 0; i <= tabs.value.length; i++) {
            let item = tabs.value[i];
            if (item.tabIndex == terminalIndex) {
              tabs.value.splice(i, 1);
              if (item == selectedTab.value) {
                if (tabs.value.length == 0) handleCreateNewTab(); else selectedTab.value = tabs.value[0];
              }
              break;
            }
          }
          drawTabs();
        }
      })
      .catch(error => message.error("连接失败"));
  }

  function drawTabs() {
    let tabsDom = document.querySelector(".tabs");
    tabsDom.innerHTML = `<div class="tab" style="width: auto" onclick="window.open('https:\/\/github.com/RicePasteM/LinkPty')">
                    <span class="name" style="display: flex; align-items:center; font-family: DatCub;">
                        <img src="./favicon.ico" alt="" style="height: 20px; margin: 0 5px; "> LinkPty </span>
                </div>`;
    for (let item of tabs.value) {
      let tabDom = document.createElement("div");
      tabDom.classList.add("tab");
      if (item == selectedTab.value) tabDom.classList.add("selected");
      tabDom.innerHTML = `
                        <span class="name"> <div class="status ${item.isOnline ? 'online' : 'offline'}"></div> #${item.tabIndex} </span> <button>×</button>
                    `
      tabsDom.appendChild(tabDom);
      let closeBtnDom = tabDom.querySelector("button");
      tabDom.onclick = function (event) {
        selectedTab.value = item;
        drawTabs();
      }
      closeBtnDom.onclick = function (event) {
        handleCloseTerminal(item.tabIndex);
        event.stopPropagation();
      }
    }
    let newTabButtonDom = document.createElement("div")
    newTabButtonDom.onclick = handleCreateNewTab;
    newTabButtonDom.innerHTML = `<span>+</span>`
    newTabButtonDom.classList.add("tab")
    newTabButtonDom.classList.add("new")
    tabsDom.appendChild(newTabButtonDom);
  }

  function handleGetTerminalHistory(terminalIndex) {
    termRefs.value[terminalIndex].write("\r\nHistory records are stilling being loaded(and may take several minutes when large), please wait...\r\n")
    fetch(`http://${SERVER_URL}/get_history?key=${key}&terminal_index=${terminalIndex}`, {
      method: 'GET',
      headers: new Headers(),
      redirect: 'follow'
    })
      .then(response => response.text())
      .then(result => {
        result = JSON.parse(result);
        if (result.result != "success") {
          message.info(result.msg)
        } else {
          for (let item of tabs.value) {
            for (let line of result.history) {
              if (line != "") {
                termRefs.value[terminalIndex].write(line + '\r\n');
              }
            }
          }
        }
      })
      .catch(error => { console.log(error); message.error("获取历史数据时出错") });
  }


  window.applySettings = () => {
    const font = document.getElementById('fontSelect').value;
    const fontSize = document.getElementById('fontSizeSelect').value;

    // 保存设置到 localStorage
    localStorage.setItem('terminalFont', font);
    localStorage.setItem('terminalFontSize', fontSize);

    for (let tab of tabs.value) {
      termRefs.value[tab.terminalIndex].setOption('fontFamily', font);
      termRefs.value[tab.terminalIndex].setOption('fontSize', parseInt(fontSize, 10));
      termRefs.value[tab.terminalIndex].write(`\x1b[10;${fontSize}m`);
      // tab.fitAddon.fit();
    }
    window.settingsModal.hide();
  }

  window.stopTask = () => {
    // 在此处添加停止任务的逻辑
    message.info('任务已停止！');
  }

  window.forceReconnect = async () => {
    if (!selectedTab.value) return;

    console.log(selectedTab.value)

    try {
      const response = await fetch(`http://${SERVER_URL}/reset_terminal?key=${key}&terminal_index=${selectedTab.value.tabIndex}`);
      const result = await response.json();

      if (result.result === "success") {
        console.log("Terminal reset successfully");
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Reset Failed',
          text: result.msg || 'Failed to reset terminal'
        });
      }
    } catch (error) {
      console.error('Error resetting terminal:', error);
      Swal.fire({
        icon: 'error',
        title: 'Reset Failed',
        text: 'Failed to connect to server'
      });
    }
  }

  window.downloadTerminalLog = async () => {
    if (!selectedTab.value) return;

    try {
      message.loading("已经开始下载（速度较慢）请耐心等待。");
      const response = await fetch(`http://${SERVER_URL}/download_terminal_log?key=${key}&terminal_index=${selectedTab.value.tabIndex}`);
      const result = await response.json();

      if (result.result === "success") {
        // 创建当前时间戳
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = `terminal_${key}_${selectedTab.value.tabIndex}_${timestamp}.log`;

        // 创建 Blob 对象
        const blob = new Blob([result.content], { type: 'text/plain' });

        // 创建下载链接并触发下载
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();

        // 清理
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        Swal.fire({
          icon: 'success',
          title: 'Download Success',
          text: 'Terminal log has been downloaded'
        });
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Download Failed',
          text: result.msg || 'Failed to download terminal log'
        });
      }
    } catch (error) {
      console.error('Error downloading terminal log:', error);
      Swal.fire({
        icon: 'error',
        title: 'Download Failed',
        text: 'Failed to connect to server'
      });
    }
  };

}
</script>

<style lang="scss">
.tabWrapper {
  width: 100%;
  height: 35px;
  display: flex;
  background-color: #F7F7F7;
  border-bottom: 2px solid #E6E6E6;
  box-sizing: border-box;

  .btn {
    cursor: pointer;
    transition: all .3s;
  }

  .btn:hover {
    filter: brightness(0.9);
    background-color: #e2e2e2;
  }
}

.tabs {
  display: flex;
  width: 100%;
  height: 35px;

  .tab {
    height: 100%;
    display: flex;
    width: 150px;
    padding: 0 20px;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    box-sizing: border-box;
    transition: all .3s;

    .name {
      display: flex;
      align-items: center;
      font-size: 18px;

      .status {
        width: 10px;
        height: 10px;
        border-radius: 100%;
        margin-right: 5px;
      }

      .status.online {
        background-color: #B5CEA8;
      }

      .status.offline {
        background-color: #F88069;
      }
    }

    button {
      border-radius: 5px;
      border: 0;
      width: 20px;
      height: 20px;
      margin: 0;
      padding: 0;
      line-height: 20px;
      font-size: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all .3s;
      background-color: #cccccc00;
    }

    button:hover {
      background-color: #ccccccff;
    }
  }

  .tab.new {
    width: 20px;
    justify-content: center;
  }

  .tab:hover {
    background-color: #EAEAEA;
  }

  .tab.selected {
    background-color: white;
    border-left: 1px solid #D2D2D2;
    border-right: 1px solid #D2D2D2;
    border-top: 1px solid #D2D2D2;
    border-radius: 5px 5px 0 0;
  }
}

.terminals {
  position: relative;
  height: calc(100vh - 40px);

  .terminal {
    position: absolute;
    width: 100vw;
    height: calc(100vh - 40px);
  }
}
</style>