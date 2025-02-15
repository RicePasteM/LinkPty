<template>
    <div class="terminal-container" ref="terminal">
    </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

const terminal = ref(null);
const term = new Terminal();
const fitAddon = new FitAddon();

const emit = defineEmits(['data']);

onMounted(() => {
    term.loadAddon(fitAddon);
    term.open(terminal.value);
    fitAddon.fit();

    term.onData(function (input) {
        emit('data', input);
    });
});

const write = (data) => {
  term.write(data);
}

const setOption = (key, value) => {
  term.options[key] = value;
}

defineExpose({ write, setOption });

</script>

<style scoped lang="scss">
.terminal-container{
    width: 100%;
    height: 100%;
}
</style>