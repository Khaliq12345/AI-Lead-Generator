export default defineEventHandler(async (event) => {
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string;
  const url = `${baseUrl}/api/clear-log`;
  const data = await $fetch(url, {
    method: "GET",
  });

  return data;
});

 