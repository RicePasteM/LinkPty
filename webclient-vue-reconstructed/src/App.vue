<template>
   <n-modal-provider>
      <n-message-provider>
         <div class="appOuter">
         <router-view/>
         </div>
      </n-message-provider>
   </n-modal-provider>
</template>


<script setup>
import { NMessageProvider, NModalProvider } from "naive-ui";
</script>

<style lang="scss">

</style>
