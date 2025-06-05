// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    "@nuxt/scripts"
  ],
  css: ['~/assets/css/main.css'],
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      API_BASE_URL: process.env.NUXT_API_BASE_URL
    },
  },
  // scripts: {
  //   globals: {
  //       "src": "http://localhost:3000/script.js",
  //       "data-website-id": "065f1435-d200-4e9a-9cf4-a728b4c54131"
  //     }
  // }
})