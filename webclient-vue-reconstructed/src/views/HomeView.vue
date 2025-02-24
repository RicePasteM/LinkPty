<template>
  <div class="tabWrapper">
    <div class="tabs">
      <div class="tab" style="width: auto" onclick="window.open('https:\/\/github.com/RicePasteM/LinkPty')">
        <span class="name" style="display: flex; align-items:center; font-family: DatCub;">
          <img src="@/assets/logo.png" alt="" style="height: 18px; margin: 0 8px; "> LinkPty </span>
      </div>
      <VueDraggable style="display: flex" v-model="tabs" target=".sort-target" :animation="150" filter=".undraggable" @change="handleChangeTerminalSort">
        <TransitionGroup
            type="transition"
            tag="div"
            name="fade"
            class="sort-target"
            style="display: flex;"
          >
          <div class="tab" v-for="tab in tabs" :class="{ 'selected': tab == selectedTab, 'undraggable': tab != selectedTab }" @click="selectedTab = tab" :key="tab.tabIndex">
            <span class="name">
              <div :class="`status ${tab.isOnline ? 'online' : 'offline'}`"></div> #{{ tab.tabIndex }}
            </span>
            <button @click="handleCloseTerminal(tab.tabIndex)">
              <n-icon size="14">
                <Close />
              </n-icon>
            </button>
          </div>
          <div class="newtab" style="display: flex; justify-content: center; align-items: center;" @click="handleCreateNewTab">
            <n-icon size="16" v-show="!isNewTabLoading">
              <Add />
            </n-icon>
            <n-spin size="small" style="transform: scale(.5);" v-show="isNewTabLoading"/>
          </div>
        </TransitionGroup>
      </VueDraggable>
    </div>
    <div class="btn" style="width: 40px; display: flex; justify-content: center; align-items: center;"
      @click="showSearchBar">
      <n-icon size="16">
        <SearchOutline />
      </n-icon>
    </div>
    <div class="btn" style="width: 40px; display: flex; justify-content: center; align-items: center;"
      @click="openSettings">
      <n-icon size="16">
        <SettingsOutline />
      </n-icon>
    </div>
  </div>
  <div class="terminals">
    <TerminalVue class="terminal" v-for="(tab, index) in tabs" :key="tab.tabIndex"
      :ref="el => termRefs[tab.tabIndex] = el" :style="{ 'zIndex': selectedTab == tab ? 1 : 0 }"
      @data="handleTermUserInput(tab, $event)" :terminalStyle="terminalStyle" :searchText="searchText" />
  </div>

  <n-modal v-model:show="showStartupModal" transform-origin="center" :mask-closable="false">
    <StartupModalVue v-model:startConnectionForm="startConnectionForm" @startConnection="handleStartConnection">
    </StartupModalVue>
  </n-modal>

  <!-- Settings Modal -->
  <n-modal v-model:show="showSettingsModal" preset="card" title="终端设置" style="width: 500px;" :bordered="false">
    <n-form-item label="终端字体" path="font">
      <n-select v-model:value="settingsForm.font" :options="fontOptions" placeholder="选择字体" filterable tag />
    </n-form-item>

    <n-form-item label="终端字号" path="fontSize">
      <n-input-number v-model:value="settingsForm.fontSize" :min="8" :max="72" placeholder="输入字号" />
    </n-form-item>
    <n-space vertical :size="10">

      <n-space justify="space-between" :size="16">
        <n-text depth="3" style="font-size: 14px;">强制重置当前终端（仅当出现问题时使用）</n-text>
        <n-button type="warning" tertiary @click="forceReconnect">
          立即重置
        </n-button>
      </n-space>

      <n-space justify="space-between" :size="16">
        <n-text depth="3" style="font-size: 14px;">下载当前终端日志</n-text>
        <n-button type="info" tertiary @click="downloadTerminalLog">
          下载日志
        </n-button>
      </n-space>

      <div style="display: flex; justify-content: center; margin-top: 15px;">
        <n-button type="primary" @click="applySettings">
          应用设置
        </n-button>
      </div>
    </n-space>
  </n-modal>

  <div class="search-container" v-show="showSearch" ref="searchContainer">
    <div class="search-box">
      <n-input v-model:value="searchText" placeholder="输入搜索内容" @keyup.enter="searchNext" ref="searchInput"
        class="search-input" />
      <div class="search-controls">
        <n-button size="small" @click="searchPrev">
          <template #icon>
            <n-icon>
              <ChevronUp />
            </n-icon>
          </template>
        </n-button>
        <n-button size="small" @click="searchNext">
          <template #icon>
            <n-icon>
              <ChevronDown />
            </n-icon>
          </template>
        </n-button>
        <n-button size="small" @click="closeSearch">
          <template #icon>
            <n-icon>
              <Close />
            </n-icon>
          </template>
        </n-button>
      </div>
    </div>
    <!-- <div class="search-status" v-if="currentMatch.length > 0">
      找到 {{ currentMatch.length }} 个匹配项
    </div> -->
  </div>

  <n-modal v-model:show="showLogDownloadModal" transform-origin="center" :mask-closable="false" display-directive="show" preset="card" 
           :style="{'width': '500px'}" title="日志下载" @after-leave="handleCloseDownloadModal">
    <DownloadLogVue ref="logDownloader" @close="showLogDownloadModal = false">
    </DownloadLogVue>
  </n-modal>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick, computed, watch } from 'vue'
import { useMessage, useModal } from 'naive-ui'
import { SearchOutline, SettingsOutline, ChevronUp, ChevronDown, Close, Add } from "@vicons/ionicons5"
import { VueDraggable } from 'vue-draggable-plus'
import TerminalVue from '@/components/Terminal.vue'
import StartupModalVue from "@/components/StartupModal.vue";
import DownloadLogVue from "@/components/DownloadLog.vue"

const documentTitle = ref("LinkPty - 跨网伪终端穿透工具")

let SERVER_URL = "linkpty.codesocean.top:43143";

const savedFont = localStorage.getItem('terminalFont') || 'Consolas';
const savedFontSize = localStorage.getItem('terminalFontSize') || '16';
const terminalStyle = reactive({
  fontFamily: savedFont, fontSize: savedFontSize
})

const message = useMessage()

let tabs = ref([]);
let selectedTab = ref(undefined);
let termRefs = ref({});
const isNewTabLoading = ref(false);

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

const showStartupModal = ref(true);

const startConnectionForm = reactive({
  key: undefined,
  serverUrl: localStorage.getItem('serverUrl') || 'linkpty.codesocean.top:43143'
})

let key = "";

const handleStartConnection = () => {
  // 保存到历史中
  SERVER_URL = startConnectionForm.serverUrl;
  key = startConnectionForm.key;
  documentTitle.value = key + " - " + documentTitle.value;
  showStartupModal.value = false;
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
        message.success("已成功重置终端")
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



function handleCreateNewTab() {
  if(isNewTabLoading.value) return;
  fetch(`http://${SERVER_URL}/create_terminal?key=${key}`, {
    method: 'GET',
    headers: new Headers(),
    redirect: 'follow'
  })
    .then(response => response.text())
    .then(result => {
      isNewTabLoading.value = true;
      result = JSON.parse(result);
      if (result.result != "success") {
        message.info(result.msg)
      }
    })
    .catch(error => message.error("创建新标签时出错"));
}

function handleCreateNewTabDone(terminalIndex, isOnline = true) {
  isNewTabLoading.value = false;
  tabs.value.push(
    {
      name: "新标签",
      tabIndex: terminalIndex,
      isOnline
    }
  )
  selectedTab.value = tabs.value[tabs.value.length - 1];
  nextTick(() => {
    if (isOnline) {
      socket.send(JSON.stringify({
        "operation": "RECEIVE_USERINPUT",
        "data": `\r\nstty cols ${termRefs.value[terminalIndex].term.cols} rows ${termRefs.value[terminalIndex].term.rows}\r\n`,
        "terminal_index": terminalIndex
      }));
    } else {
      termRefs.value[terminalIndex].write("\r\nThis terminal is offline, below are histories.\r\n")
    }
  })
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
      }
    })
    .catch(error => message.error("连接失败"));
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


// Settings Modal 相关逻辑
const showSettingsModal = ref(false)
const settingsForm = reactive({
  font: localStorage.getItem('terminalFont') || 'Consolas',
  fontSize: parseInt(localStorage.getItem('terminalFontSize')) || 16
})

const fontOptions = [
  { label: 'Monospace', value: 'monospace' },
  { label: 'Consolas', value: 'Consolas' },
  { label: 'Courier New', value: 'Courier New' }
]


const applySettings = () => {
  localStorage.setItem('terminalFont', settingsForm.font)
  localStorage.setItem('terminalFontSize', settingsForm.fontSize)
  terminalStyle.fontFamily = settingsForm.font
  terminalStyle.fontSize = settingsForm.fontSize

  for (let key in termRefs.value) {
    termRefs.value[key].updateTerminalStyle();
  }
  message.success('设置已应用')
  showSettingsModal.value = false;
}

const stopTask = () => {
  // 在此处添加停止任务的逻辑
  message.info('任务已停止！');
}

const forceReconnect = async () => {
  if (!selectedTab.value) return;

  console.log(selectedTab.value)

  try {
    const response = await fetch(`http://${SERVER_URL}/reset_terminal?key=${key}&terminal_index=${selectedTab.value.tabIndex}`);
    const result = await response.json();

    if (result.result === "success") {
      console.log("Terminal reset successfully");
    } else {
      message.error(result.msg || '重置终端时出错')
    }
  } catch (error) {
    message.error(error.msg || '无法连接到服务器')
  }
}

const openSettings = () => {
  showSettingsModal.value = true
}

const handleChangeTerminalSort = (event) => {
  console.log(event)
}



// 搜索相关功能

const showSearch = ref(false)
const searchText = ref('')
const currentMatch = ref([])
const searchInput = ref(null)

const showSearchBar = () => {
  showSearch.value = !showSearch.value
  if (showSearch.value) {
    nextTick(() => {
      searchInput.value?.focus()
    })
  }
}

const closeSearch = () => {
  showSearch.value = false
  clearSearch()
}

const performSearch = (before, after) => {
  if (!selectedTab.value) return;

  const terminal = termRefs.value[selectedTab.value.tabIndex];
  const content = terminal.getContent();
  let matches;
  if (searchText.value.trim() == "") {
    matches = []
  } else {
    const regex = new RegExp(searchText.value, 'gi');
    matches = [...content.matchAll(regex)]
  }

  currentMatch.value = matches.length > 0 ? matches : [];

  if (matches.length > 0) {
    if (before != after) {
      terminal.searchAddon.clearDecorations();
      terminal.searchAddon.clearActiveDecoration();
      searchNext()
    }
  }
}


const searchOptions = {
  decorations: {
    matchBackground: "#666666",
    activeMatchBackground: "#FF8000",
    activeMatchBorder: "#FF0000"
  }
}

// 导航功能
const searchNext = () => {
  const terminal = termRefs.value[selectedTab.value.tabIndex];
  terminal.searchAddon.findNext(searchText.value, searchOptions)
}

const searchPrev = () => {
  const terminal = termRefs.value[selectedTab.value.tabIndex];
  terminal.searchAddon.findPrevious(searchText.value, searchOptions)
}


// 清理搜索
const clearSearch = () => {
  searchText.value = ''
  currentMatch.value = []
  if (selectedTab.value) {
    const terminal = termRefs.value[selectedTab.value.tabIndex];
    terminal.searchAddon.clearDecorations();
    terminal.searchAddon.clearActiveDecoration();
  }
}

watch(searchText, performSearch)
watch(documentTitle, () => {
  document.title = documentTitle.value;
}, {
  immediate: true
})

// 日志下载相关功能
const showLogDownloadModal = ref(false);
const logDownloader = ref();

const downloadTerminalLog = async () => {
  if (!selectedTab.value) return;

  showLogDownloadModal.value = true;

  nextTick(() => {
    logDownloader.value.downloadLog(SERVER_URL, key, selectedTab.value.tabIndex);
  })
};

const handleCloseDownloadModal = async () => {
  logDownloader.value.stopDownload();
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
  user-select: none;

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
    border: 1px;
    border-radius: 5px 5px 0 0;
    border-color: transparent;

    .name {
      display: flex;
      align-items: center;
      font-size: 15px;

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
      transform: translateX(5px);
    }

    button:hover {
      background-color: #ccccccff;
    }

    button:active {
      background-color: rgb(150, 150, 150);
    }

    button:focus {
      outline: 0;
    }
  }

  .newtab{
    width: 40px;
    justify-content: center;
    cursor: pointer;
    transition: all .3s;
  }

  .tab:hover, .newtab:hover {
    background-color: #EAEAEA;
  }

  .tab:active, .newtab:active {
    transform: scale(0.96);
  }

  .tab.selected {
    background-color: white;
    border-left: 1px solid #D2D2D2;
    border-right: 1px solid #D2D2D2;
    border-top: 1px solid #D2D2D2;
    box-shadow:
      0px 0.7px 2.2px rgba(0, 0, 0, 0.02),
      0px 1.7px 5.3px rgba(0, 0, 0, 0.028),
      0px 3.3px 10px rgba(0, 0, 0, 0.035),
      0px 5.8px 17.9px rgba(0, 0, 0, 0.042),
      0px 10.9px 33.4px rgba(0, 0, 0, 0.05),
      0px 26px 80px rgba(0, 0, 0, 0.07);
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

.search-container {
  position: absolute;
  right: 40px;
  top: 40px;
  z-index: 1000;
  background: white;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  padding: 8px;
  min-width: 300px;

  .search-box {
    display: flex;
    gap: 8px;
    align-items: center;

    .search-input {
      flex: 1;
    }

    .search-controls {
      display: flex;
      gap: 4px;
    }
  }

  .search-status {
    font-size: 12px;
    color: #666;
    margin-top: 4px;
    padding-left: 4px;
  }
}

.fade-move,
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scaleY(0.01) translate(30px, 0);
}

.fade-leave-active {
  position: absolute;
}
</style>