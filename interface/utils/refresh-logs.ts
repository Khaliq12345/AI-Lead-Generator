import axios from 'axios'


export const refreshLogs = async () => {
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string
  console.log(baseUrl)
  return axios.post(`${baseUrl}/refresh-logs`, null, {
    params: {},
    headers: {},
  })
}