export default defineEventHandler(async (event) => {
  const body = await readFormData(event)
  const query = getQuery(event);
  const property_details = query.property_details;
  const email_prompt = query.compose_email_prompt;
  const numberOfDomains = query.number_of_domains;

  event.path

  try {
    const baseUrl = useRuntimeConfig().public.API_BASE_URL as string;
    const response = await $fetch(event.path, {
      baseURL: baseUrl,
      method: "POST",
      body: body,
      params: {
        property_details: property_details,
        compose_email_prompt: email_prompt,
        number_of_domains: numberOfDomains,
      },
      headers: {
        'accept': '*/*',
      },
    });

    return response; //
  } catch (err: any) {
    console.error("Erreur lors de l'appel à l'API distante :", err?.message);
    return createError({
      statusCode: err?.response?.status || 500,
      statusMessage: err?.response?.data?.message || "Erreur serveur",
    });
  }
});
