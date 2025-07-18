export default defineEventHandler(async (event) => {
  const body = await readFormData(event);
  const {
    property_details,
    client_name,
    lead_mail,
    lead_name,
    lead_position,
    additional_prompt,
  } = getQuery(event);

  try {
    const baseUrl = useRuntimeConfig().public.API_BASE_URL as string;
    const response = await $fetch(event.path, {
      baseURL: baseUrl,
      method: "POST",
      body: body,
      params: {
        property_details: property_details,
        client_name: client_name,
        lead_mail: lead_mail,
        lead_name: lead_name,
        lead_position: lead_position,
        additional_prompt: additional_prompt,
      },
      headers: {
        accept: "*/*",
      },
      timeout: 60000,
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
