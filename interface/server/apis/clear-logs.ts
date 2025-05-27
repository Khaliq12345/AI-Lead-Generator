import axios from 'axios'


export const clearLogs = async () => {
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string
  console.log(baseUrl)
  return axios.post(`${baseUrl}/clear-logs`, null, {
    params: {},
    headers: {},
  })
}