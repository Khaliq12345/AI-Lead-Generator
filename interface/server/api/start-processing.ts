export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const property_details = query.property_details;
  const email_prompt = query.compose_email_prompt;
  const numberOfDomains = query.number_of_domains;
  const test = query.test;
  console.log(property_details, email_prompt, numberOfDomains, test)
  const baseUrl = useRuntimeConfig().public.API_BASE_URL as string;
  const url = `${baseUrl}/api/start-processing`;
  // const data = await $fetch(url, {
  //   method: "GET",
  //   params: {
  //     property_details: property_details,
  //     compose_email_prompt: email_prompt,
  //     number_of_domains: numberOfDomains,
  //     test: test
  //   },
  // });

  const data = await $fetch("https://jsonplaceholder.typicode.com/todos/1")
  return data;
});
