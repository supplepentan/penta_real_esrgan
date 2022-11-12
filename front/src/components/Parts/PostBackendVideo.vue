<script setup lang="ts">
import axios, { AxiosResponse } from "axios";
import { ref, onMounted } from "vue";

interface Props {
  backendUrl: string;
}

const props = defineProps<Props>();
const file = ref();
const previewVideo = ref();
const superResolutionVideo = ref();

onMounted(() => {
  previewVideo.value = document.getElementById("videoPreview");
  superResolutionVideo.value = document.getElementById(
    "superResolutionVideoPreview"
  );
});

const fileSelected = (event: any): void => {
  file.value = event.target.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    previewVideo.value.src = reader.result;
    console.log(previewVideo.value);
  };
  reader.readAsDataURL(event.target.files[0]);
};
const fileUpload = (): void => {
  console.log(props.backendUrl);
  const formData = new FormData();
  formData.append("file", file.value);
  axios
    .post(props.backendUrl, formData, {
      responseType: "blob",
    })
    .then((response: AxiosResponse<any, any>) => {
      let mineType: string | undefined = response.headers["content-type"];
      if (mineType) {
        let ext: string;
        if (mineType === "video/mp4") {
          ext = "mp4";
        } else {
          ext = "";
        }
        console.log(response.headers["content-type"]);
        const blob = new Blob([response.data], { type: mineType });
        let url: string = URL.createObjectURL(blob);
        superResolutionVideo.value.src = url;
        const a: HTMLAnchorElement = document.createElement("a");
        document.body.appendChild(a);
        a.download = "returnFile.".concat(ext);
        a.href = url;
        a.click();
      }
    })
    .catch((error) => console.log(error));
};
</script>
<template>
  <div>
    <h1>Super Resolution Video</h1>
    <div class="p-2 flex justify-center">
      <label
        class="px-4 py-2 bg-transparent border-blue-500 rounded cursor-pointer bg-sky-200 ring-2 hover:bg-blue-300 hover:text-white hover:border-transparent"
      >
        Select File !
        <input class="hidden" type="file" v-on:change="fileSelected" />
      </label>
      <button
        v-on:click="fileUpload"
        class="px-4 py-2 font-semibold text-blue-700 bg-transparent bg-blue-100 border-blue-500 rounded ring-2 hover:bg-blue-300 hover:text-white hover:border-transparent"
      >
        Make It !
      </button>
    </div>
    <div class="grid grid-cols-2">
      <div>
        <video autoplay controls id="videoPreview"></video>
        <div v-if="file" class="m-2 p-2 border rounded-lg border-slate-400">
          <p>Name: {{ file.name }}</p>
          <p>Size: {{ file.size }}</p>
          <p>Type: {{ file.type }}</p>
        </div>
      </div>
      <div>
        <video autoplay controls id="superResolutionVideoPreview"></video>
      </div>
    </div>
  </div>
</template>
