export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string
  const url = `${baseUrl}/api/start-processing`
  const data = await $fetch(url, {
    method: 'GET',
    params: query,
  })

  return data
})