export default defineEventHandler(async (event) => {
  const body = await readFormData(event);
  const query = getQuery(event);
  const property_details = query.property_details;
  const numberOfDomains = query.number_of_domains;
  const leadType = query.lead_type;

  event.path;

  try {
    const baseUrl = useRuntimeConfig().public.API_BASE_URL as string;
    const response = await $fetch(event.path, {
      baseURL: baseUrl,
      method: "POST",
      body: body,
      params: {
        property_details: property_details,
        number_of_domains: numberOfDomains,
        lead_type: leadType,
      },
      headers: {
        accept: "*/*",
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
