<template>
    <div class="terminal-container" :ref="`terminal${terminal.tabIndex}`">
        <!-- 终端内容 -->
    </div>
</template>

<script>
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

export default {
    name: 'TerminalComponent',
    props: {
        terminal: Object
    },
    mounted() {
        const term = new Terminal({
            scrollback: 2147483647,
            fontFamily: 'consolas, monospace'
        });
        const fitAddon = new FitAddon.FitAddon();
        term.loadAddon(fitAddon);
        term.open(this.$refs.terminal);
        fitAddon.fit();
        // 其他初始化逻辑...
    },
    methods: {
        resizeTerminal() {
            const fitAddon = this.terminal.fitAddon;
            if (fitAddon) {
                fitAddon.fit();
            }
        }
    }
};
</script>