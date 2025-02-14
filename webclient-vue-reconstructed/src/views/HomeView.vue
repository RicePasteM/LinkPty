<template>
  <div class="outer">
    <div class="tabWrapper">
      <div class="tabs">
        <div class="tab" style="width: auto" @click="openGithub">
          <span class="name" style="display: flex; align-items:center; font-family: DatCub;">
            <img src="@/assets/favicon.png" alt="" style="height: 20px; margin: 0 5px;"> LinkPty
          </span>
        </div>
      </div>
      <div class="btn" style="width: 40px; display: flex; justify-content: center; align-items: center;"
        @click="showSearchBar">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-search"
          viewBox="0 0 16 16" style="transform: scale(1)">
          <path
            d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0" />
        </svg>
      </div>
      <div class="btn" style="width: 40px; display: flex; justify-content: center; align-items: center;"
        @click="openSettingsModal">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear"
          viewBox="0 0 16 16">
          <path
            d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492M5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0" />
          <path
            d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115z" />
        </svg>
      </div>
    </div>
    <div class="terminals"></div>

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
              <input type="number" id="fontSizeSelect" class="form-control" v-model="fontSize" />
            </div>
            <div class="form-group">
              <div>强制重置当前终端（仅当出现问题时使用）</div>
              <button type="button" id="forceReconnect" class="btn btn-warning" @click="forceReconnect">立即重置</button>
            </div>
            <div class="form-group">
              <div>下载当前终端日志</div>
              <button type="button" id="downloadLog" class="btn btn-info" @click="downloadTerminalLog">下载日志</button>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="applySettings">应用设置</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';

export default {
  name: 'LinkPty',
  data() {
    return {
      tabs: [],
      selectedTab: undefined,
      fontSize: 14,
      historyKeys: JSON.parse(localStorage.getItem('historyKeys')) || [],
      key: null,
      socket: null,
      SERVER_URL: "linkpty.codesocean.top:43143",
    };
  },
  mounted() {
    this.loadSettings();
    this.showInputKeyDialog();
  },
  methods: {
    openGithub() {
      window.open('https://github.com/RicePasteM/LinkPty');
    },
    showSearchBar() {
      this.selectedTab.searchAddonBar.show();
    },
    openSettingsModal() {
      window.settingsModal.show();
    },
    async loadSettings() {
      const savedFont = localStorage.getItem('terminalFont') || 'consolas';
      this.fontSize = localStorage.getItem('terminalFontSize') || '16';

      document.getElementById('fontSelect').value = savedFont;
      document.getElementById('fontSizeSelect').value = this.fontSize;

      window.settingsModal = new bootstrap.Modal(document.getElementById('settingsModal'));
    },
    async showInputKeyDialog() {
      const { value: key } = await Swal.fire({
        title: "Please input code to link",
        html: `
          <input style="width: 80%;" type="text" id="keyInput" class="swal2-input" placeholder="Please input key">
          <div class="history" style="margin-top: 10px;">
            <div class="d-flex justify-content-center align-items-center mb-1">
              <span style="margin-right: 10px;">Histories </span>
              ${this.historyKeys.map((k, index) => `
                <button style="margin-right: 5px;" class="btn btn-secondary btn-sm history-key" @click="selectHistoryKey('${k}')">${k}</button>
              `).join('')}
            </div>
          </div>
        `,
        focusConfirm: false,
        preConfirm: () => {
          const keyValue = document.getElementById('keyInput').value;
          if (!keyValue) {
            Swal.showValidationMessage('Please input key');
          } else {
            this.key = keyValue;
            this.fetchStatus();
          }
          return keyValue;
        }
      });

      if (key) {
        this.key = key;
        this.saveHistoryKey(key);
        document.title = `${key} - ${document.title}`;
      } else {
        location.reload();
      }
    },
    selectHistoryKey(key) {
      document.getElementById('keyInput').value = key;
    },
    saveHistoryKey(key) {
      if (!this.historyKeys.includes(key)) {
        this.historyKeys.unshift(key);
        if (this.historyKeys.length > 5) this.historyKeys.pop();
        localStorage.setItem('historyKeys', JSON.stringify(this.historyKeys));
      }
    },
    async createWebSocket() {
      this.socket = new WebSocket(`ws://${this.SERVER_URL}/dockerclient?key=${this.key}`);

      this.socket.onmessage = (event) => {
        let jsonData = JSON.parse(event.data);
        if (jsonData.operation === "CREATE_TERMINAL_DONE") {
          this.handleCreateNewTabDone(jsonData.terminal_index);
        } else if (jsonData.operation === "RECEIVE_SERVEROUTPUT") {
          for (let item of this.tabs) {
            if (item.tabIndex === jsonData.terminal_index) {
              item.term.write(jsonData.data);
            }
          }
        } else if (jsonData.operation === "RESET_TERMINAL_DONE") {
          Swal.fire({ icon: 'success', title: 'Reset Successfully' });
        }
      };

      this.socket.onopen = () => {
        setInterval(() => {
          this.socket.send(JSON.stringify({ operation: "PING" }));
        }, 60000);
      };
    },
    async fetchStatus() {
      console.log(this.key)
      try {
        const response = await fetch(`http://${this.SERVER_URL}/get_status?key=${this.key}`);
        const result = await response.json();

        if (result.result === 'offline') {
          Swal.fire({ icon: 'danger', title: 'Host offline' });
          for (let terminal of result.terminals) {
            this.handleCreateNewTabDone(terminal.terminal_index, false);
            this.handleGetTerminalHistory(terminal.terminal_index);
          }
        } else if (result.result === 'success') {
          await this.createWebSocket();
          for (let terminal of result.terminals) {
            this.handleCreateNewTabDone(terminal.terminal_index, terminal.is_online);
            this.handleGetTerminalHistory(terminal.terminal_index);
          }
        }
      } catch (error) {
        Swal.fire({ icon: 'warning', title: 'Error checking status' });
      }
    },
    handleCreateNewTabDone(terminalIndex, isOnline = true) {
      const terminalDom = document.createElement("div");
      terminalDom.classList.add(".terminal");
      let term = new Terminal({
        scrollback: 2147483647,
        fontFamily: 'consolas, monospace'
      });
      const fitAddon = new FitAddon.FitAddon();
      term.loadAddon(fitAddon);
      const searchAddon = new SearchAddon.SearchAddon();
      term.loadAddon(searchAddon);

      this.tabs.push({ name: "新标签", tabIndex: terminalIndex, terminalDom, term, isOnline, searchAddon, fitAddon });
      this.$nextTick(() => {
        term.open(terminalDom);
        fitAddon.fit();
      });
    },
    handleGetTerminalHistory(terminalIndex) {
      const tab = this.tabs.find(tab => tab.tabIndex === terminalIndex);
      tab.term.write("\r\nHistory records are loading... Please wait...\r\n");

      fetch(`http://${this.SERVER_URL}/get_history?key=${this.key}&terminal_index=${terminalIndex}`)
        .then(response => response.json())
        .then(result => {
          if (result.result !== 'success') {
            Swal.fire({ icon: 'error', title: result.msg });
          } else {
            for (let line of result.history) {
              tab.term.write(line + '\r\n');
            }
          }
        })
        .catch(error => Swal.fire({ icon: 'error', title: 'Error fetching history' }));
    },
    applySettings() {
      const font = document.getElementById('fontSelect').value;
      const fontSize = document.getElementById('fontSizeSelect').value;

      localStorage.setItem('terminalFont', font);
      localStorage.setItem('terminalFontSize', fontSize);

      for (let tab of this.tabs) {
        tab.term.options.fontFamily = font;
        tab.term.options.fontSize = parseInt(fontSize, 10);
        tab.term.write(`\x1b[10;${fontSize}m`);
        tab.fitAddon.fit();
      }
      window.settingsModal.hide();
    },
    forceReconnect() {
      if (!this.selectedTab) return;

      const terminalIndex = this.selectedTab.tabIndex;

      fetch(`http://${this.SERVER_URL}/reset_terminal?key=${this.key}&terminal_index=${terminalIndex}`, {
        method: 'GET',
        headers: new Headers(),
        redirect: 'follow'
      })
        .then(response => response.json())
        .then(result => {
          if (result.result === 'success') {
            Swal.fire({
              icon: 'success',
              title: 'Terminal Reset',
              text: 'The terminal has been successfully reset.'
            });

            // Optional: Reset the terminal's state (clear its content, restart connection, etc.)
            this.selectedTab.term.reset();
            this.selectedTab.term.write("Terminal has been reset. Please re-enter commands.\r\n");
          } else {
            Swal.fire({
              icon: 'error',
              title: 'Reset Failed',
              text: result.msg || 'Failed to reset terminal'
            });
          }
        })
        .catch(error => {
          console.error('Error resetting terminal:', error);
          Swal.fire({
            icon: 'error',
            title: 'Reset Failed',
            text: 'Failed to connect to the server'
          });
        });
    },

    downloadTerminalLog() {
      if (!this.selectedTab) return;

      const terminalIndex = this.selectedTab.tabIndex;

      Swal.fire({
        title: 'Downloading log...',
        text: 'This might take a while. Please be patient.',
        showConfirmButton: false,
        didOpen: () => {
          Swal.showLoading();
        }
      });

      fetch(`http://${this.SERVER_URL}/download_terminal_log?key=${this.key}&terminal_index=${terminalIndex}`, {
        method: 'GET',
        headers: new Headers(),
        redirect: 'follow'
      })
        .then(response => response.json())
        .then(result => {
          Swal.close(); // Close the loading dialog

          if (result.result === 'success') {
            // Generate a filename based on the current timestamp
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
            const filename = `terminal_${this.key}_${terminalIndex}_${timestamp}.log`;

            // Create a Blob object for the log content
            const blob = new Blob([result.content], { type: 'text/plain' });

            // Create a download link and trigger the download
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();

            // Clean up
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            Swal.fire({
              icon: 'success',
              title: 'Download Successful',
              text: 'The terminal log has been downloaded successfully.'
            });
          } else {
            Swal.fire({
              icon: 'error',
              title: 'Download Failed',
              text: result.msg || 'Failed to download terminal log'
            });
          }
        })
        .catch(error => {
          Swal.close(); // Close the loading dialog
          console.error('Error downloading terminal log:', error);
          Swal.fire({
            icon: 'error',
            title: 'Download Failed',
            text: 'Failed to connect to the server'
          });
        });
    }
  }
};
</script>

<style scoped lang="scss">
.outer {
  display: flex;
  flex-direction: column;
  margin: 0;

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
      width: 100vw;
      height: calc(100vh - 40px);
    }
  }
}
</style>
