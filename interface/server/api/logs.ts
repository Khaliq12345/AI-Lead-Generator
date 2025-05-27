import axios from 'axios'


export const getLogs = async () => {
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string
  console.log(baseUrl)
  return axios.get(`${baseUrl}/get-logs`)
}