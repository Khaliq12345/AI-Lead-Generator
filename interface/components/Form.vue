<template>
  <div class="min-h-screen bg-black py-10 px-4">
    <div class="max-w-5xl mx-auto bg-[#1c1c1e] rounded-md shadow-lg p-10">
      <h1
        class="text-3xl font-semibold text-center text-black bg-white bg-opacity-10 py-4 rounded-md mb-10"
      >
        AI Lead Generator
      </h1>

<<<<<<< HEAD
      <form @submit.prevent class="space-y-6">
        <div v-if="errorMsg" class="errorMsg">
          <strong>{{ errorMsg }}</strong>
        </div>
        <div v-if="successMsg" class="successMsg">
          <strong>{{ successMsg }}</strong>
        </div>
        <TextArea label="Property Details" placeholder="Enter property details..." :rows="5"
          @on-update-text="(newValue) => (propertyDetails = newValue)"></TextArea>

        <!-- Files Input -->
        <div class="w-full text-center">
          <UInput class="w-full" type="file" placeholder="Additional Files" accept=".pdf" multiple
            icon="i-heroicons-document-duplicate" @change="handleFileChange" />
          <div class="my-2 font-bold text-white-800" v-if="selectedFiles">
            {{ selectedFiles.length }} File(s) Selected !
          </div>
        </div>

        <TextArea label="Compose Email Prompt" placeholder="Enter email prompt..." :rows="5"
          @on-update-text="(newValue) => (composeEmailPrompt = newValue)"></TextArea>

        <label id="domains-number">Domains: </label>
        <UInputNumber placeholder="Number of companies" id="domains-number" v-model="numberOfDomains" />

        <UCheckbox v-model="dev" label="Test run" />

        <div v-if="isLoading" class="flex justify-center">
          <div class="loader"></div>
        </div>
        <div v-else class="flex flex-col sm:flex-row gap-4 pt-6 justify-center">
          <Button @click="submitForm">
            SUBMIT
          </Button>
        </div>
      </form>

      <!-- Logs Drawer Button -->
      <div class="flex justify-center p-5">
        <a :href="outputFile" download>Download</a>

        <!-- <UButton label="Download" v-if="outputFile" @click="downloadFile()"></UButton> -->

        <!-- <Button @click="drawerOpen = true" :disabled="drawerOpen">
              <UIcon name="i-heroicons-bars-3-bottom-left-20-solid" class="mr-3 text-xl" />
              <span class="ml-3 text-lg font-semibold text-center">Logs</span>
            </Button> -->

      </div>
    </div>


    <!-- Logging -->
    <UDrawer title="Submitted Data Details" description="View and manage submitted property data and email prompts"
      v-model:open="drawerOpen" :dismissible="false" :handle="false"
      :ui="{ header: 'flex items-center justify-between' }">
      <template #dialogtitle></template>
      <template #description></template>
      <template #header>
        <h2 class="text-highlighted font-semibold"></h2>
        <div>
          <Button @click="getLogs"
            customClass="bg-[0] text-white px-6 py-2 mr-3 rounded hover:bg-black hover:text-white border border-white transition cursor-pointer">
            Refresh Logs
          </Button>
          <Button @click="clearLogs">Clear Logs</Button>
          <UButton color="neutral" variant="ghost" icon="i-lucide-x" class="py-2 mt-[-15px] cursor-pointer"
            @click="drawerOpen = false" />
=======
      <!-- Buttons shown only during Lead generation -->
      <UButton
        block
        @click="generateMail = true"
        v-if="!generateMail"
        class="my-5"
        >Generate Mail Instead</UButton
      >

      <!-- Buttons shown only during Mail generation -->
      <UButton
        block
        @click="generateMail = false"
        v-if="generateMail"
        class="my-5"
        >Generate Lead Instead</UButton
      >

      <!-- Form of both generation -->
      <form @submit.prevent class="space-y-6 flex flex-col">
        <div v-if="errorMsg" class="errorMsg">
          <strong>{{ errorMsg }}</strong>
        </div>
        <div v-if="successMsg" class="successMsg">
          <strong>{{ successMsg }}</strong>
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
        </div>

        <URadioGroup v-model="Togglervalue" :items="ToggleItems" />

        <TextArea
          label="Property Details"
          placeholder="Enter property details..."
          :rows="5"
          @on-update-text="(newValue) => (propertyDetails = newValue)"
        ></TextArea>

        <UInput type="file" multiple @change="onFileChange" />

        <!-- Total number to generate from Propert details -->
        <label id="domains-number" v-if="!generateMail">Domains: </label>
        <UInputNumber
          placeholder="Number of companies"
          id="domains-number"
          v-model="numberOfDomains"
          v-if="!generateMail"
        />

        <!-- Input used in generating mails -->
        <div class="flex flex-col gap-4" v-if="generateMail">
          <UInput placeholder="Client Name" v-model="client_name"></UInput>
          <UInput placeholder="Lead Mail" v-model="lead_mail"></UInput>
          <UInput placeholder="Lead Name" v-model="lead_name"></UInput>
          <UInput placeholder="Lead Position" v-model="lead_position"></UInput>
          <UInput
            placeholder="Email Additional Prompt"
            v-model="additional_prompt"
          ></UInput>
        </div>

        <div v-if="isLoading" class="flex justify-center">
          <div class="loader"></div>
        </div>
<<<<<<< HEAD
        <div v-else class="p-6 text-white  font-mono break-words whitespace-pre-wrap">
          {{ logs.length == 0 ? "Nothing to show!" : logs }}</div>
      </template>
    </UDrawer>
=======
        <div v-else class="flex flex-col sm:flex-row gap-4 pt-6 justify-center">
          <Button @click="submitForm"> SUBMIT </Button>
        </div>
      </form>

      <!-- Show the generated mail -->
      <UTextarea
        v-if="outputMail && generateMail"
        v-model="outputMail"
        class="w-full my-5"
      ></UTextarea>

      <div class="flex justify-around p-5">
        <!-- Download Button -->
        <UButton
          @click="downloadOutput()"
          :disabled="!outputs"
          v-if="!generateMail"
          >Download</UButton
        >

        <!-- logging -->
        <UDrawer
          direction="right"
          inset
          title="Loggings"
          description="Showing the logs for the processing"
          v-if="!generateMail"
        >
          <UButton
            label="Show Logs"
            color="neutral"
            variant="subtle"
            trailing-icon="i-lucide-chevron-up"
          />

          <template #content>
            <div class="flex flex-col gap-5 p-5">
              <UButton
                label="Refresh Logs"
                color="neutral"
                variant="subtle"
                @click="getLogs"
              />
              <p
                class="w-full mb-4 whitespace-pre-line font-mono overflow-y-auto"
              >
                {{ logs }}
              </p>
            </div>
          </template>
        </UDrawer>
      </div>
    </div>
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
  </div>
</template>

<script setup lang="ts">
import type { RadioGroupItem, RadioGroupValue } from "@nuxt/ui";

const outputMail = ref();
const client_name: Ref<string> = ref("");
const lead_mail: Ref<string> = ref("");
const lead_name: Ref<string> = ref("");
const lead_position: Ref<string> = ref("");
const additional_prompt: Ref<string> = ref("");
const taskId = ref();
const propertyDetails = ref("");
const logs = ref("");
const errorMsg = ref("");
const successMsg = ref("");
const isLoading = ref(false);
const numberOfDomains = ref(10);
const toast = useToast();
const selectedFiles = ref<[File | null]>();
const outputs = ref();
const generateMail = ref(false);
const ToggleItems: Ref<RadioGroupItem[]> = ref(["buying", "selling"]);
const Togglervalue: Ref<RadioGroupValue> = ref("buying");

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
  selectedFiles.value = e.target.files;
};

async function submitForm() {
  let fileData = new FormData();
  if (selectedFiles.value) {
    for (let file of selectedFiles.value) {
      if (file) {
        const blob = new Blob([await file.arrayBuffer()], {
          type: file.type,
        });
        fileData.append("files", blob, file.name);
      }
    }
  }
  if (!propertyDetails.value) {
    errorMsg.value = "Veuillez remplir tous les champs";
    return;
  }
  if (isLoading.value == true) {
<<<<<<< HEAD
    return
=======
    return;
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
  }
  try {
    isLoading.value = true;
    await clearLogs();
    if (!generateMail.value) {
      const data = await $fetch("api/get-leads", {
        method: "POST",
        body: fileData,
        params: {
          property_details: propertyDetails.value,
<<<<<<< HEAD
          compose_email_prompt: composeEmailPrompt.value,
          test: dev.value,
          number_of_domains: numberOfDomains.value,
          docs: fileByteCodes.value
=======
          number_of_domains: numberOfDomains.value,
          lead_type: Togglervalue.value,
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
        },
      });
      console.log("Response", data);
      showSuccessToast("Success", "AI lead generation done!");
      taskId.value = data;
    } else {
      const data = await $fetch("api/generate-mail", {
        method: "POST",
        body: fileData,
        params: {
          property_details: propertyDetails.value,
          client_name: client_name.value,
          lead_mail: lead_mail.value,
          lead_name: lead_name.value,
          lead_position: lead_position.value,
          additional_prompt: additional_prompt.value,
        },
      });
      showSuccessToast("Success", "AI lead generation done!");
      outputMail.value = data;
      isLoading.value = false;
    }
  } catch (e) {
    console.error("Une erreur inattendue s'est produite :", e);
    showErrorToast();
    isLoading.value = false;
  }
}

const clearLogs = async () => {
  if (isLoading.value == true) {
<<<<<<< HEAD
    return
=======
    return;
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
  }
  try {
    isLoading.value = true;
    const response = (await $fetch("/api/clear-logs", {
      method: "GET",
    })) as any;
    console.log("status : ", response);
  } catch (error) {
<<<<<<< HEAD
    console.error('Erreur de requete:', error);
  } finally {
    isLoading.value = false
    await getLogs()
=======
    console.error("Erreur de requete:", error);
  } finally {
    isLoading.value = false;
    await getLogs();
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
  }
};

const getLogs = async () => {
<<<<<<< HEAD
  if (isLoading.value == true) {
    return
  }
=======
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
  try {
    const response = (await $fetch("/api/get-log", {
      method: "GET",
    })) as any;
    logs.value = response as any;
  } catch (error) {
<<<<<<< HEAD
    console.error('Erreur de requete:', error);
  } finally {
    isLoading.value = false
=======
    console.error("Erreur de requete:", error);
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
  }
};

const checkStatus = async () => {
  if (!taskId.value || generateMail.value) return;
  try {
    const response = (await $fetch("/api/check-status", {
      method: "GET",
      params: {
        taskId: taskId.value,
      },
    })) as any;
    console.log("Status - ", response.status);
    if (response.status === "running") {
      isLoading.value = true;
    } else if (response.status === "success") {
<<<<<<< HEAD
      outputFile.value = response.folder
      isLoading.value = false
    }
    else {
      isLoading.value = false
=======
      isLoading.value = false;
      outputs.value = response.data;
    } else {
      isLoading.value = false;
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1
    }
  } catch (error) {
    console.error("Erreur de requete:", error);
  }
};

<<<<<<< HEAD
// Files
const selectedFiles = ref<FileList | null>(null)
const fileByteCodes = ref<Array<ArrayBuffer>>([])
const handleFileChange = async (event: Event) => {
  const inputElement = event.target as HTMLInputElement;
  if (!inputElement.files) return;
  selectedFiles.value = inputElement.files;
  fileByteCodes.value = []; 
  for (const file of Array.from(inputElement.files)) {
    const byteCode = await readFileAsArrayBuffer(file);
    fileByteCodes.value.push(byteCode);
  }
  console.log('Byte codes:', fileByteCodes.value);
}
// Get ArrayBuffer from file
const readFileAsArrayBuffer = (file: File): Promise<ArrayBuffer> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as ArrayBuffer);
    reader.onerror = reject;
    reader.readAsArrayBuffer(file);
  });
}

=======
const downloadOutput = async () => {
  try {
    if (!outputs.value) {
      console.log("nothing to download");
      return {};
    }
    const jsonBlob = new Blob([outputs.value], { type: "text/plain" });
    const fileURL = window.URL.createObjectURL(jsonBlob);
    const a = document.createElement("a");
    a.href = fileURL;
    a.download = "mails.txt";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(fileURL);
  } catch (error) {
    console.error("Download failed:", error);
  }
};
>>>>>>> d7ac6e1093524b67cbe416f7aee9796dc96f84f1

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
