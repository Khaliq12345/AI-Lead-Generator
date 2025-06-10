<template>
  <div class="min-h-screen bg-black py-10 px-4">
    <div class="max-w-5xl mx-auto bg-[#1c1c1e] rounded-md shadow-lg p-10">
      <h1
        class="text-3xl font-semibold text-center text-black bg-white bg-opacity-10 py-4 rounded-md mb-10"
      >
        AI Lead Generator
      </h1>

      <form @submit.prevent class="space-y-6">
        <div v-if="errorMsg" class="errorMsg">
          <strong>{{ errorMsg }}</strong>
        </div>
        <div v-if="successMsg" class="successMsg">
          <strong>{{ successMsg }}</strong>
        </div>
        <TextArea
          label="Property Details"
          placeholder="Enter property details..."
          :rows="5"
          @on-update-text="(newValue) => (propertyDetails = newValue)"
        ></TextArea>

        <UInput type="file" multiple @change="onFileChange"/>

        <TextArea
          label="Compose Email Prompt"
          placeholder="Enter email prompt..."
          :rows="5"
          @on-update-text="(newValue) => (composeEmailPrompt = newValue)"
        ></TextArea>

        <label id="domains-number">Domains: </label>
        <UInputNumber
          placeholder="Number of companies"
          id="domains-number"
          v-model="numberOfDomains"
        />

        <div v-if="isLoading" class="flex justify-center">
          <div class="loader"></div>
        </div>
        <div v-else class="flex flex-col sm:flex-row gap-4 pt-6 justify-center">
          <Button @click="submitForm"> SUBMIT </Button>
        </div>
      </form>


      <div class="flex justify-around p-5">
        <!-- Download Button -->
        <!-- <a :href="outputFile" download>Download</a> -->
        <UButton @click="downloadOutput">Download</UButton>

        <!-- Logging -->
        <UDrawer 
          direction="right" 
          inset
          title="Loggings"
          description="Showing the logs for the processing"
        >
          <UButton label="Show Logs" color="neutral" variant="subtle" trailing-icon="i-lucide-chevron-up"/>

          <template #content>
            <div class="flex flex-col gap-5 p-5">
              <UButton label="Refresh Logs" color="neutral" variant="subtle" @click="getLogs"/>
              <p class="w-full mb-4 whitespace-pre-line font-mono">{{ logs }}</p>
            </div>
          </template>
        </UDrawer>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const propertyDetails = ref("");
const composeEmailPrompt = ref("");
const logs = ref("")
const errorMsg = ref("");
const successMsg = ref("");
const isLoading = ref(false);
const numberOfDomains = ref(10);

const toast = useToast();

const outputFile = ref("");

const selectedFiles = ref<[File | null]>()

function showSuccessToast(title: any, desc: any) {
  toast.add({
    title: title,
    description: desc,
  });
}

function showErrorToast() {
  toast.add({
    title: "Error",
    description: "AI lead generation failed",
    color: "error",
  });
}

const onFileChange = (e: any) => {
  selectedFiles.value = e.target.files
  console.log(selectedFiles)
}

async function submitForm() {
  let fileData = new FormData()
  if (selectedFiles.value) {
    for (let file of selectedFiles.value) {
      if (file) {
        console.log(await file.arrayBuffer())
        const blob = new Blob([await file.arrayBuffer()], {
          'type': file.type
        })
        fileData.append("files", blob, file.name)
      }
    }
  }
  if (!propertyDetails.value) {
    errorMsg.value = "Veuillez remplir tous les champs";
    return;
  }
  if (isLoading.value == true) {
    return;
  }
  try {
    isLoading.value = true;
    await clearLogs();
    const data = await $fetch("api/start-processing", {
      method: "POST",
      body: fileData,
      params: {
        property_details: propertyDetails.value,
        compose_email_prompt: composeEmailPrompt.value,
        number_of_domains: numberOfDomains.value,
      },
    });
    console.log("Response", data);
    showSuccessToast("Success", "AI lead generation done!");
  } catch (e) {
    console.error("Une erreur inattendue s'est produite :", e);
    showErrorToast();
    isLoading.value = false;
  }
}

const clearLogs = async () => {
  if (isLoading.value == true) {
    return;
  }
  try {
    isLoading.value = true;
    const response = (await $fetch("/api/clear-logs", {
      method: "GET",
    })) as any;
    console.log("status : ", response);
  } catch (error) {
    console.error("Erreur de requete:", error);
  } finally {
    isLoading.value = false;
    await getLogs();
  }
};

const getLogs = async () => {
  if (isLoading.value == true) {
    return;
  }
  try {
    isLoading.value = true;
    const response = (await $fetch("/api/get-log", {
      method: "GET",
    })) as any;
    console.log("status : ", response);

    logs.value = response as any;
  } catch (error) {
    console.error("Erreur de requete:", error);
  } finally {
    isLoading.value = false;
  }
};

const checkStatus = async () => {
  try {
    const response = (await $fetch("/api/check-status", {
      method: "GET",
    })) as any;
    console.log("Status - ", response.status);
    if (response.status === "running") {
      isLoading.value = true;
    } else if (response.status === "success") {
      outputFile.value = response.folder;
      isLoading.value = false;
    } else {
      isLoading.value = false;
    }
  } catch (error) {
    console.error("Erreur de requete:", error);
  }
};

const downloadOutput = async () => {
  try {
    const response = await $fetch(outputFile.value, {
      method: "GET",
      responseType: 'blob',
    });
    console.log(response)

    const fileURL = window.URL.createObjectURL(response as Blob);
    const a = document.createElement('a');
    a.href = fileURL;
    a.download = "mails.zip"
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(fileURL);
  } catch (error) {
    console.error("Download failed:", error);
  } 
}

onMounted(() => {
  setInterval(checkStatus, 10000);
});
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
.log-text {
  white-space: pre-line;
}
</style>
