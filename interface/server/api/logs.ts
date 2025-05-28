export default defineEventHandler(async (event) => {
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string
  const url = `${baseUrl}/api/get-log`
  const data = await $fetch(url)

  return data
})