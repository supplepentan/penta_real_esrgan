<script setup lang="ts"></script>

<template>
  <div>
    <nav class="flex flex-wrap items-center justify-between p-6 bg-blue-300">
      <div class="flex items-center flex-shrink-0 mr-6 text-white">
        <span>🐧</span>
        <span class="text-xl font-semibold tracking-tight"
          >Penta Real-ESRGAN</span
        >
      </div>
      <div class="block lg:hidden">
        <button
          class="flex items-center px-3 py-2 text-teal-200 border border-teal-400 rounded hover:text-white hover:border-white"
        >
          <svg
            class="w-3 h-3 fill-current"
            viewBox="0 0 20 20"
            xmlns="http://www.w3.org/2000/svg"
          >
            <title>Menu</title>
            <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z" />
          </svg>
        </button>
      </div>
      <div class="flex-grow block w-full lg:flex lg:items-center lg:w-auto">
        <div class="text-sm lg:flex-grow">
          <a
            href="https://vuejs.org/index.html"
            class="block mt-4 mr-4 text-teal-200 lg:inline-block lg:mt-0 hover:text-white"
            target="blank"
          >
            Vue.js
          </a>
          <a
            href="https://vitejs.dev/"
            class="block mt-4 mr-4 text-teal-200 lg:inline-block lg:mt-0 hover:text-white"
            target="blank"
          >
            Vite
          </a>
          <a
            href="https://flowbite.com/tools/tailwind-cheat-sheet/"
            class="block mt-4 mr-4 text-teal-200 lg:inline-block lg:mt-0 hover:text-white"
            target="blank"
          >
            Tailwind cheat sheet
          </a>
          <a
            href="https://www.typescriptlang.org/"
            class="block mt-4 mr-4 text-teal-200 lg:inline-block lg:mt-0 hover:text-white"
            target="blank"
          >
            TypeScript
          </a>
          <a
            href="https://supplepentan.com/"
            class="block mt-4 text-teal-200 lg:inline-block lg:mt-0 hover:text-white"
            target="blank"
          >
            Blog
          </a>
        </div>
      </div>
    </nav>
  </div>
</template>

<style scoped></style>
