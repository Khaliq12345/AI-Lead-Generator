<template>
  <div class="min-h-screen bg-black py-10 px-4">
    <div class="max-w-5xl mx-auto bg-[#1c1c1e] rounded-md shadow-lg p-10">
      <h1 class="text-3xl font-semibold text-center text-black bg-white bg-opacity-10 py-4 rounded-md mb-10">
        AI Lead Generator
      </h1>

      <form class="space-y-6">
        <div v-if="errorMsg" class="errorMsg"><strong>{{ errorMsg }}</strong></div>
        <div v-if="successMsg" class="successMsg"><strong>{{ successMsg }}</strong></div>
        <ClientOnly>
            <TextArea
                label="Property Details"
                placeholder="Enter property details..."
                :rows="5"
                @on-update-text="(newValue) => propertyDetails = newValue"
            ></TextArea>
        </ClientOnly>

        <ClientOnly>
            <TextArea
                label="Compose Email Prompt"
                placeholder="Enter email prompt..."
                :rows="5"
                @on-update-text="(newValue) => composeEmailPrompt = newValue"
            ></TextArea>
        </ClientOnly>

        <div
            v-if="isLoading"
            class="flex justify-center"
        >
            <div class="loader"></div>
        </div>
        <div v-else class="flex flex-col sm:flex-row gap-4 pt-6 justify-center">
            <ClientOnly>
                <Button
                    v-bind:disabled="isLoading || !canSubmitForm"
                    @click="submitForm"
                >
                    SUBMIT
                </Button>
            </ClientOnly>
        </div>
      </form>
    </div>
    <UDrawer
        title="Submitted Data Details"
        description="View and manage submitted property data and email prompts"
        v-model:open="drawerOpen"
        :ui="{ header: 'flex items-center justify-between' }"
    >
        <template #header>
            <h2 class="text-highlighted font-semibold"></h2>
            <div>
                <Button
                    @click="refreshLog"
                    customClass="bg-[0] text-white mr-2 px-6 py-2 rounded hover:bg-black hover:text-white border border-white transition cursor-pointer"
                >
                    Refresh Log
                </Button>
                <Button @click="clearLog">Clear Log</Button>
            </div>
        </template>
        <template #body>
            <div class="p-6 text-white">
                <h2 class="text-2xl font-bold mb-4">Submitted Data</h2>
                <p class="mb-2"><strong>Property Details :</strong></p>
                <p class="mb-4 whitespace-pre-line text-sm text-gray-300">{{ propertyDetails }}</p>
                <p class="mb-2"><strong>Email Prompt :</strong></p>
                <p class="whitespace-pre-line text-sm text-gray-300">{{ composeEmailPrompt }}</p>
            </div>
        </template>
    </UDrawer>
  </div>
</template>


<script setup lang="ts">
    import type { StartProcessing } from '~/interfaces/StartProcessing'

    const propertyDetails= ref('')
    const composeEmailPrompt = ref('')
    const errorMsg = ref('')
    const successMsg= ref('')
    const isLoading = ref(false)
    const drawerOpen = ref(false)
    const canSubmitForm = computed(() => !!propertyDetails.value && !!composeEmailPrompt.value)

    const submitForm = async () => {
        if (!propertyDetails.value || !composeEmailPrompt.value) {
            errorMsg.value = "Veuillez remplir tous les champs"
            return
        }
        try {
            isLoading.value = true
            const { data, error } = await useFetch<StartProcessing>('api/start-processing', {
                params: {
                    property_details: propertyDetails.value,
                    compose_email_prompt: composeEmailPrompt.value,
                }
            })
            if (error.value) {
                console.error("Erreur lors du démarrage du processus:", error.value)
                errorMsg.value = "Erreur lors du démarrage du processus"
            }
            else if(data.value) {
                console.log("Processus démarré :", data.value)
                successMsg.value = data.value.message || ''
            }
        }
        catch (e) {
            console.error("Une erreur inattendue s'est produite :", e)
            errorMsg.value = "Une erreur inattendue s'est produite"
        }
        finally {
            isLoading.value = false
            // drawerOpen.value = true
        }

        /* console.log('Starting process:', {
            propertyDetails: propertyDetails.value,
            composeEmailPrompt: composeEmailPrompt.value
        }) */
    }

    const refreshLog= async () => {
        console.log("Refresh Logs...")
        try {
            const { data, error } = await useFetch('api/refresh-logs')
            if (error.value) {
                console.error("Erreur lors du refresh:", error.value)
            } else {
                console.log("Logs rafraîchis :", data.value)
            }
        }
        catch (e) {
            console.error("Une erreur inattendue s'est produite :", e)
        }
    }

    const clearLog = async () => {
        console.log("Clear Logs...")
        try {
            const { data, error } = await useFetch('api/clear-logs')
            if (error.value) {
                console.error("Erreur lors du clear:", error.value)
            } else {
                console.log("Logs supprimés :", data.value)
            }
        }
        catch (e) {
            console.error("Une erreur inattendue s'est produite :", e)
        }
    }
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
        border: solid 4px #FFF;
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