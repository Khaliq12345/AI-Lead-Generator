export default defineEventHandler(async (event) => {
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string
  const data = await $fetch(event.path, {
    baseURL: baseUrl,
    method: 'GET'
  })

  return data as String
})