<script setup lang="ts">
import axios, { AxiosResponse } from "axios";
import { ref } from "vue";

interface Props {
  backendUrl: string;
}

const props = defineProps<Props>();
const file = ref();
const previewImage = ref();
const superResolutionImage = ref();

const fileSelected = (event: any): void => {
  file.value = event.target.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    previewImage.value = reader.result;
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
        if (mineType === "image/jpeg") {
          ext = "jpg";
        } else if (mineType === "image/png") {
          ext = "png";
        } else {
          ext = "";
        }
        console.log(response.headers["content-type"]);
        const blob = new Blob([response.data], { type: mineType });
        let url: string = URL.createObjectURL(blob);
        superResolutionImage.value = url;
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
    <h1>Super Resolution Image</h1>
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
        <img v-bind:src="previewImage" class="img-fluid" alt="" />
        <div v-if="file" class="m-2 p-2 border rounded-lg border-slate-400">
          <p class="text-white">Name: {{ file.name }}</p>
          <p class="text-white">Size: {{ file.size }}</p>
          <p class="text-white">Type: {{ file.type }}</p>
        </div>
      </div>
      <div>
        <img v-bind:src="superResolutionImage" class="img-fluid" alt="" />
      </div>
    </div>
  </div>
</template>
