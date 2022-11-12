<script setup lang="ts">
import { ref } from "vue";
import PostBackendImage from "../Parts/PostBackendImage.vue";
import PostBackendVideo from "../Parts/PostBackendVideo.vue";

const isActive = ref("");
const isSelect = function (seen: string) {
  isActive.value = seen;
};
</script>
<template>
  <div class="bg-sky-100">
    <div>
      <div class="flex justify-center py-1">
        <button
          @click="isSelect('seenImage')"
          class="px-2 border-2 border-blue-600 rounded"
        >
          Image
        </button>
        <button
          @click="isSelect('seenVideo')"
          class="px-2 border-2 border-blue-600 rounded"
        >
          Video
        </button>
      </div>
      <div class="tabContents">
        <div v-if="isActive === 'seenImage'">
          <PostBackendImage
            backendUrl="http://127.0.0.1:8000/upload"
            class="bg-black"
          />
        </div>
        <div v-else-if="isActive === 'seenVideo'">
          <PostBackendVideo
            backendUrl="http://127.0.0.1:8000/upload_video"
            class="bg-black"
          />
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped></style>
