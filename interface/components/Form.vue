<template>
  <div class="min-h-screen bg-black py-10 px-4">
    <div class="max-w-5xl mx-auto bg-[#1c1c1e] rounded-md shadow-lg p-10">
      <h1 class="text-3xl font-semibold text-center text-black bg-white bg-opacity-10 py-4 rounded-md mb-10">
        AI Lead Generator
      </h1>

      <form class="space-y-6">
        <TextArea
          label="Property Details"
          placeholder="Enter property details..."
          :rows="5"
          @on-update-text="(newValue) => propertyDetails = newValue"
        ></TextArea>

        <TextArea
            label="Compose Email Prompt"
            placeholder="Enter email prompt..."
            :rows="5"
            @on-update-text="(newValue) => composeEmailPrompt = newValue"
        ></TextArea>

        <div class="flex flex-col sm:flex-row gap-4 pt-6">
          <Button @click="submitForm">SUBMIT</Button>
        </div>
      </form>
    </div>
    <UDrawer
        title=""
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
    const propertyDetails= ref('')
    const composeEmailPrompt = ref('')
    const drawerOpen = ref(false)

    const submitForm = () => {
        console.log('Starting process:', {
            propertyDetails: propertyDetails.value,
            composeEmailPrompt: composeEmailPrompt.value
        })
        drawerOpen.value = true
    }

    const refreshLog= () => {
        console.log("Refresh Logs...")
    }

    const clearLog = () => {
        console.log("Clear Logs...")
    }

    /* const { data } = await useFetch('/api/hello')
    console.log(data.value) */

    /* const { data } = await useFetch('/clear-log/test', {
        params: {
            'name': "Khaliq"
        },
        headers: {

        }
    }) */
</script>


<style>
</style>