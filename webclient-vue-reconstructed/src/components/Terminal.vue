<template>
    <div class="terminal-container" ref="terminal">
    </div>
</template>

<script setup>
import { ref, onMounted, defineEmits, defineProps, onBeforeMount } from 'vue';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { SearchAddon } from '@xterm/addon-search';
import 'xterm/css/xterm.css';

const terminal = ref(null);
const term = new Terminal({allowProposedApi: true});
const fitAddon = new FitAddon();
const searchAddon = new SearchAddon();

const props = defineProps(['terminalStyle']);
const emit = defineEmits(['data']);

function fitWindow() {
  fitAddon.fit();
}

function updateTerminalStyle() {
  term.options['fontFamily'] = props.terminalStyle.fontFamily;
  term.options['fontSize'] = props.terminalStyle.fontSize;
  term.write(`\x1b[10;${props.terminalStyle.fontSize}m`);
  fitWindow();
}

onMounted(() => {
    term.loadAddon(fitAddon);
    term.open(terminal.value);
    fitAddon.fit();
    term.loadAddon(searchAddon);
    updateTerminalStyle();

    window.addEventListener("resize", fitWindow);

    term.onData(function (input) {
        emit('data', input);
    });
});

onBeforeMount(() => {
  window.removeEventListener("resize", fitWindow);
})

const write = (data) => {
  term.write(data);
}

const setOption = (key, value) => {
  term.options[key] = value;
}

const getContent = () => {
  return terminal.value.innerText;
}

defineExpose({ write, setOption, updateTerminalStyle, searchAddon, getContent, term });

</script>

<style scoped lang="scss">
.terminal-container{
    width: 100%;
    height: 100%;
}
</style>