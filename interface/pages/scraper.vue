<template>
  <div class="min-h-screen bg-black py-10 px-4">
    <div class="max-w-5xl mx-auto bg-[#1c1c1e] rounded-md shadow-lg p-10">
      <div class="flex justify-end my-3 p-5">
        <!-- Download Button -->
        <UButton to="/">Home</UButton>
      </div>
      <h1
        class="text-3xl font-semibold text-center text-black bg-white bg-opacity-10 py-4 rounded-md mb-10"
      >
        Scraper Section
      </h1>

      <form @submit.prevent class="space-y-6 flex flex-col">
        <div v-if="errorMsg" class="errorMsg">
          <strong>{{ errorMsg }}</strong>
        </div>
        <div v-if="successMsg" class="successMsg">
          <strong>{{ successMsg }}</strong>
        </div>

        <UInput placeholder="Site URL" v-model="site_url"></UInput>

        <div v-if="isLoading" class="flex justify-center">
          <div class="loader"></div>
        </div>
        <div v-else class="flex flex-col sm:flex-row gap-4 pt-6 justify-center">
          <Button @click="submitForm"> SUBMIT </Button>
        </div>
      </form>

      <div class="flex justify-start p-5">
        <!-- Download Button -->
        <UButton @click="downloadOutput()" :disabled="!outputs"
          >Download</UButton
        >
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import * as XLSX from "xlsx";

const site_url: Ref<string> = ref("");
const errorMsg = ref("");
const successMsg = ref("");
const isLoading = ref(false);
const toast = useToast();
const outputs = ref();

function showToast(title: any, desc: any, color: any) {
  toast.add({
    title: title,
    description: desc,
    color: color,
  });
}

async function submitForm() {
  if (!site_url.value) {
    errorMsg.value = "Veuillez remplir tous les champs";
    return;
  }
  if (isLoading.value == true) {
    return;
  }
  try {
    errorMsg.value = "";
    successMsg.value = "";
    isLoading.value = true;
    const response = (await $fetch("/api/scrape-link", {
      method: "GET",
      params: {
        url: site_url.value,
      },
    })) as any;
    console.log("Result - ", response);
    if (
      !Array.isArray(response) ||
      (Array.isArray(response) && response.length === 0)
    ) {
      console.error("No Data to Doownload");
      showToast("Error", "No Data returned !", "error");
      isLoading.value = false;
      return;
    }
    outputs.value = await response;
    showToast("Success", "Scraping Successfully done !", "success");
    isLoading.value = false;
  } catch (e) {
    console.error("Une erreur inattendue s'est produite :", e);
    showToast("Error", `Scraping Error ${e}`, "error");
    isLoading.value = false;
  }
}
const downloadOutput = async () => {
  try {
    // Convertir la liste de JSON en format XLSX
    const jsonToXlsx = (jsonData: any[]) => {
      // Créer un classeur Excel à partir des données JSON
      const ws = XLSX.utils.json_to_sheet(jsonData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Sheet1");
      return wb;
    };
    // Convertir la donnée JSON en format XLSX
    const wb = jsonToXlsx(outputs.value);
    // Créer un Blob pour le fichier .xlsx
    const filename = "result.xlsx";
    const xlsxBlob = XLSX.write(wb, {
      bookType: "xlsx",
      type: "array",
    });
    // Créer un URL pour télécharger le fichier
    const fileURL = window.URL.createObjectURL(
      new Blob([xlsxBlob], { type: "application/octet-stream" })
    );
    // Créer un lien de téléchargement et simuler un clic pour lancer le téléchargement
    const a = document.createElement("a");
    a.href = fileURL;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(fileURL);
  } catch (error) {
    console.error("Download failed:", error);
  }
};
</script>

<style>
.successMsg {
  text-align: center;
  color: green;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.errorMsg {
  text-align: center;
  color: red;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.loader {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: solid 4px #fff;
  border-top: 5px solid transparent;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
