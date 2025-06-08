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

      <!-- Logs Drawer Button -->
      <div class="flex justify-center p-5">
        <a :href="outputFile" download>Download</a>
      </div>
    </div>

    <!-- Logging -->
    <UDrawer
      title="Submitted Data Details"
      description="View and manage submitted property data and email prompts"
      v-model:open="drawerOpen"
      :dismissible="false"
      :handle="false"
      :ui="{ header: 'flex items-center justify-between' }"
    >
      <template #dialogtitle></template>
      <template #description></template>
      <template #header>
        <h2 class="text-highlighted font-semibold"></h2>
        <div>
          <Button
            @click="getLogs"
            customClass="bg-[0] text-white px-6 py-2 mr-3 rounded hover:bg-black hover:text-white border border-white transition cursor-pointer"
          >
            Refresh Logs
          </Button>
          <Button @click="clearLogs">Clear Logs</Button>
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-lucide-x"
            class="py-2 mt-[-15px] cursor-pointer"
            @click="drawerOpen = false"
          />
        </div>
      </template>
      <template #body>
        <div v-if="isLoading" class="flex justify-center">
          <div class="loader"></div>
        </div>
        <div
          v-else
          class="p-6 text-white font-mono break-words whitespace-pre-wrap"
        >
          {{ logs.length == 0 ? "Nothing to show !" : logs }}
        </div>
      </template>
    </UDrawer>
  </div>
</template>

<script setup lang="ts">
const propertyDetails = ref("");
const composeEmailPrompt = ref("");
const logs = ref("");
const errorMsg = ref("");
const successMsg = ref("");
const isLoading = ref(false);
const drawerOpen = ref(false);
const canSubmitForm = computed(() => !!propertyDetails.value);
const numberOfDomains = ref(10);

const toast = useToast();

const outputFile = ref("");

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

async function submitForm() {
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
      params: {
        property_details: propertyDetails.value,
        compose_email_prompt: composeEmailPrompt.value,
        test: dev.value,
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
    const response = (await $fetch("/api/get-logs", {
      method: "GET",
    })) as any;
    console.log("status : ", response);

    logs.value = response as any;
    showSuccessToast("Success", "Logs Refreshed");
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

onMounted(() => {
  setInterval(checkStatus, 5000);
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
</style>
