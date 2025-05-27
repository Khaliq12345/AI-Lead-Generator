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
            @click="startBot"
            type="button"
            class="bg-white text-black px-6 py-2 rounded hover:bg-black hover:text-white border border-white transition cursor-pointer"
          >
            SUBMIT
          </button>
        </div>
      </form>
    </div>
  </div>
</template>


<script setup lang="ts">
    const propertyDetails= ref('')
    const composeEmailPrompt = ref('')

    const startBot = () => {
      console.log('Starting bot with configuration:', {
        propertyDetails: propertyDetails.value,
        composeEmailPrompt: composeEmailPrompt.value
      })
    // Appel API pour déclencher une action
    }
</script>


<style>
</style>