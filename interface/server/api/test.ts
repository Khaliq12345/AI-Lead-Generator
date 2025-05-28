export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const name = query.name

  const url = "https://httpbin.org/get"

  const data = await $fetch(url)

  return data

})