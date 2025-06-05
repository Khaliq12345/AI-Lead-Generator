export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string
  const url = `${baseUrl}/api/get-log`
  const data = await $fetch(url, {
    method: 'GET'
  })

  return data as String
})