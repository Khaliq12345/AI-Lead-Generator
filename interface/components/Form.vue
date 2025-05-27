<template>
  <div class="min-h-screen bg-black py-10 px-4">
    <div class="max-w-5xl mx-auto bg-[#1c1c1e] rounded-md shadow-lg p-10">
      <h1 class="text-3xl font-semibold text-center text-black bg-white bg-opacity-10 py-4 rounded-md mb-10">
        AI Lead Generator
      </h1>

      <form class="space-y-6">
        <div>
          <label class="block text-base text-gray-300 mb-1 font-semibold">Property Details</label>
          <textarea
            rows="5"
            v-model="propertyDetails"
            class="w-full px-4 py-2 border border-gray-700 bg-[#2c2c2e] rounded text-white placeholder-gray-400 focus:outline-none focus:border-white"
          />
        </div>

        <div>
          <label class="block text-base text-gray-300 mb-1 font-semibold">Compose Email Prompt</label>
          <textarea
            rows="5"
            v-model="composeEmailPrompt"
            class="w-full px-4 py-2 border border-gray-700 bg-[#2c2c2e] rounded text-white placeholder-gray-400 focus:outline-none focus:border-white"
          />
        </div>

        <div class="flex flex-col sm:flex-row gap-4 pt-6">
          <button
            @click="submitForm"
            type="button"
            class="bg-white text-black px-6 py-2 rounded hover:bg-black hover:text-white border border-white transition cursor-pointer"
          >
            SUBMIT
          </button>
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
                <button
                    @click="refreshLog"
                    type="button"
                    class="text-white mr-2 px-6 py-2 rounded hover:bg-black hover:text-white border border-white transition cursor-pointer"
                >
                    Refresh Log
                </button>
                <button
                    @click="clearLog"
                    type="button"
                    class="bg-white text-black px-6 py-2 rounded hover:bg-black hover:text-white border border-white transition cursor-pointer"
                >
                    Clear Log
                </button>
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
      console.log('Starting bot with configuration:', {
        propertyDetails: propertyDetails.value,
        composeEmailPrompt: composeEmailPrompt.value
      })
      drawerOpen.value = true
    }

    const clearLog = () => {}
    const refreshLog= () => {}
</script>


<style>
</style>