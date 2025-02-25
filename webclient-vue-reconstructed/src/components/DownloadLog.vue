<template>
    <div class="outer">
        <!-- 下载进度容器 -->
        <div v-if="!downloadComplete" class="progress-container">
            <!-- 进度条 -->
            <div class="progress-bar" :style="{ width: progress + '%' }"></div>
            <!-- 进度文本 -->
            <div class="progress-info">
                <span class="percentage">{{ progress.toFixed(1) }}%</span>
                <span class="size">{{ downloadedSize }} / {{ totalSize }}</span>
            </div>
        </div>

        <!-- 完成提示 -->
        <div v-if="downloadComplete" class="complete-container">
            <n-result status="success" title="下载完成">
                <template #footer>
                <n-button @click="handleClose">关闭窗口</n-button>
                </template>
            </n-result>
        </div>

        <!-- 错误提示 -->
        <div v-if="downloadError" class="error-container">
            <n-result status="500" title="下载失败">
                <template #footer>
                <n-button @click="handleClose">关闭窗口</n-button>
                </template>
            </n-result>
        </div>
    </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import { useMessage } from 'naive-ui'

const emit = defineEmits(['close'])

const message = useMessage()

// 响应式状态
const progress = ref(0)
const totalSize = ref('0 KB')
const downloadedSize = ref('0 KB')
const downloadComplete = ref(false)
const downloadError = ref(false)
const errorMessage = ref('')
let stillDownload = true;

const formatSize = (bytes) => {
    if (bytes >= 1024 * 1024) {
        return (bytes / (1024 * 1024)).toFixed(1) + 'MB'
    }
    return (bytes / 1024).toFixed(1) + 'KB'
}

const handleClose = () => {
    emit('close')
}

const downloadLog = async (serverUrl, key, tabIndex) => {
    try {
        // 重置状态
        progress.value = 0
        downloadComplete.value = false
        downloadError.value = false
        stillDownload = true

        // 获取文件大小
        const startRes = await fetch(`http://${serverUrl}/start_download_terminal_log?key=${key}&terminal_index=${tabIndex}`)
        const startData = await startRes.json()
        
        if (startData.result !== "success") {
            throw new Error('获取文件信息失败')
        }

        // 设置文件大小显示
        totalSize.value = formatSize(startData.size)
        
        // 开始下载
        const downloadRes = await fetch(`http://${serverUrl}/download_terminal_log?key=${key}&terminal_index=${tabIndex}`)
        
        if (!downloadRes.ok) {
            throw new Error('下载请求失败')
        }

        const reader = downloadRes.body.getReader()
        let receivedText = ''

        while (true) {
            const { done, value } = await reader.read()
            if (done) break
            receivedText += new TextDecoder().decode(value)
            if (stillDownload == false) {
                reader.cancel()
                message.info("下载已中断")
                break
            }
        }

        // 解析 JSON 并提取 content
        const jsonData = JSON.parse(receivedText)
        let logContent = jsonData.content || '下载内容为空'

        // 可选：去除 ANSI 颜色转义字符
        logContent = logContent.replace(/\x1B\[[0-9;]*[mK]/g, '')

        // 创建文件下载
        const blob = new Blob([logContent], { type: 'text/plain' })
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `terminal_${key}_${tabIndex}_${new Date().toISOString().replace(/[:.]/g, '-')}.log`
        link.click()
        URL.revokeObjectURL(url)

        // 完成状态
        downloadComplete.value = true
    } catch (error) {
        console.error(error)
        downloadError.value = true
        errorMessage.value = error.message || '下载失败'
    }
}

const stopDownload = () => {
    stillDownload = false;
}

defineExpose({ downloadLog, stopDownload })
</script>

<style scoped lang="scss">
.outer {
    padding: 24px;
    min-width: 300px;
}

.progress-container {
    position: relative;
    background: #f5f5f5;
    border-radius: 8px;
    height: 40px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #409eff, #79bbff);
    transition: width 0.3s ease;
    border-radius: 8px;
}

.progress-info {
    position: absolute;
    top: 0;
    width: calc(100% - 32px);
    height: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 16px;
    font-weight: 500;
    color: #333;

    .percentage {
        font-size: 14px;
    }
    
    .size {
        font-size: 12px;
        opacity: 0.8;
    }
}

.complete-container {
    text-align: center;
    
    .success-text {
        margin: 12px 0;
        color: #67C23A;
        font-weight: 500;
    }

    .close-btn {
        margin-top: 16px;
        transition: all 0.3s;
    }
}

.error-container {
    text-align: center;
    padding: 16px;
    
    .error-text {
        color: #F56C6C;
        margin-top: 8px;
        font-weight: 500;
    }
}
</style>