# Penta Real-ESRGAN

The origin is https://github.com/xinntao/Real-ESRGAN

This is Browser-App makeing from Real-ESRGAN.
Using tools are FastAPI, Poetry of Python to backend-side,
and Vue.js, Vite, Typescript, TailwindCSS of Javascript to frontend-side.

# Usage

## Clone from github.

```
gh repo clone xinntao/Real-ESRGAN
```

## Install FastAPI of Backend (including front-template) by using Poetry.

```
cd penta_real_esrgan
poetry install
```

### Initialize (Only once)

This root-directory is penta_real_esrgan (Not "penta_real_esrgan/penta_real_esrgan").

```
poetry shell
python setup.py develop
```

## Install Vue.js3 of Frontend (using Vite, Typescript, TailwindCSS)

This is used only development environment. Without installing, able to play Super-Resolution. Root-directory is penta_real_esrgan (Not "penta_real_esrgan/penta_real_esrgan")

```
cd front
npm install
```
