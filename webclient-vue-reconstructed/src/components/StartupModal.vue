<template>
    <div class="modalOuter">
        <div class="title">
            <img src="@/assets/logo.png" alt="logo">
            <span>LINKPTY</span>
        </div>
        <div class="form">
            <n-tabs class="card-tabs" default-value="connect" size="large" animated pane-wrapper-style="margin: 0 -4px"
                pane-style="padding-left: 4px; padding-right: 4px; box-sizing: border-box;">
                <n-tab-pane name="connect" tab="连接">
                    <n-form :model="startConnectionForm" :rules="{ key: { required: true, trigger: ['blur', 'input'], message: '请输入 连接码' } }" label-placement="left">
                        <n-form-item label="连接码" path="key">
                            <n-select v-model:value="props.startConnectionForm.key" size="large" filterable tag
                                :options="historyKeyOptions" placeholder="请输入连接码" />
                        </n-form-item>
                    </n-form>
                    <div class="confirm" style="display: flex; justify-content: center; margin-bottom: 5px;">
                        <n-button type="primary" size="large" @click="handleConnectBtnClicked">
                            <template #icon>
                                <n-icon>
                                    <Link />
                                </n-icon>
                            </template>
                            连接到终端
                        </n-button>
                    </div>
                </n-tab-pane>
                <n-tab-pane name="options" tab="选项">
                    <n-form :model="startConnectionForm" :rules="{ serverUrl: { required: true, trigger: ['blur', 'input'], message: '请输入 服务器 URL' } }" label-placement="left">
                        <n-form-item label="服务器 URL" path="serverUrl">
                            <n-input type="text" size="large" placeholder="请输入服务器 URL" v-model:value="startConnectionForm.serverUrl"/>
                        </n-form-item>
                    </n-form>
                </n-tab-pane>
                <n-tab-pane name="about" tab="关于">
                    <p>
                        LinkPty 是一个 <span style="font-weight: bold;">跨网伪终端穿透工具</span>，它允许你通过一个 Python 进程在本无法远程使用终端的设备上构建伪终端，并通过一台预先架设的中转服务器基于 WebSocket 远程创建、管理和操作它们。
                    </p>
                    <p>
                        它被设计为特别适用于以下情况下的终端连接：
                    </p>
                    <ul>
                        <li>被连接方能够运行 Python 程序；</li>
                        <li>由于网络环境或系统限制，无法直接使用 telnet、ssh 等协议与被连接方的终端进行交互；</li>
                        <li>连接方与被连接方均能访问互联网或局域网中的某个中转设备；</li>
                        <li>连接方安装了现代浏览器（如Chrome、Firefox）。</li>
                    </ul>
                    <p>
                        欢迎访问本项目的 Github，提出建议或参与项目贡献。
                    </p>
                    <div class="confirm" style="display: flex; justify-content: center; margin: 5px 0;">
                        <n-button secondary @click="gotoGitHub" style="margin-right: 10px;">
                            <template #icon>
                                <n-icon>
                                    <LogoGithub />
                                </n-icon>
                            </template>
                            GitHub
                        </n-button>
                        <n-button secondary @click="gotoPypi">
                            <template #icon>
                                <n-icon>
                                    <LogoPython />
                                </n-icon>
                            </template>
                            Pypi
                        </n-button>
                    </div>
                </n-tab-pane>
            </n-tabs>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';
import { LogoGithub, LogoPython, Link } from "@vicons/ionicons5"
import { useMessage } from 'naive-ui'

const message = useMessage()


const props = defineProps({
    startConnectionForm: Object
});

const emit = defineEmits(["startConnection"]);

const historyKeys = JSON.parse(localStorage.getItem('historyKeys')) || [];
const historyKeyOptions = ref(historyKeys.map(item => ({label: item, value: item})));

const handleConnectBtnClicked = () => {
    if(props.startConnectionForm.key != undefined) {
        if (!historyKeys.includes(props.startConnectionForm.key)) {
            historyKeys.unshift(props.startConnectionForm.key);
            if (historyKeys.length > 10) historyKeys.pop(); // 保持最多10个历史记录
            localStorage.setItem('historyKeys', JSON.stringify(historyKeys));
        }
        emit("startConnection");
    } else {
        message.error("连接码不能为空");
    }
}

const gotoGitHub = () => {
    window.open('https://github.com/RicePasteM/LinkPty');
}

const gotoPypi = () => {
    window.open('https://pypi.org/project/link-pty/');
}


</script>

<style scoped lang="scss">
.modalOuter {
    width: 500px;
    background-color: white;
    border-radius: 5px;

    .title {
        font-family: DatCub;
        font-size: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 30px 0;
        user-select: none;


        img {
            width: 60px;
            height: 60px;
            margin-right: 20px;
            -webkit-user-drag: none;
        }
    }

    .form {
        margin: 0 40px 40px 40px;
    }
}
</style>