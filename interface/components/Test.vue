<template>
  <div class="min-h-screen bg-[#f5f5f5] py-10 px-4">
    <div class="max-w-5xl mx-auto bg-[#eeeeee] rounded-md shadow p-10">
      <h1 class="text-3xl font-semibold text-center text-white bg-[#5397d6] py-4 rounded-md mb-10">AI Lead Generator</h1>

      <form class="space-y-6">
        <div>
          <label class="block text-base text-gray-800 mb-1"><strong>Property Details</strong></label>
          <textarea type="text" rows="5" v-model="propertyDetails" class="w-full px-4 py-2 border border-gray-400 rounded text-black" />
        </div>
        <div>
          <label class="block text-base text-gray-800 mb-1"><strong>Compose Email Prompt</strong></label>
          <textarea type="text" rows="5" v-model="composeEmailPrompt" class="w-full px-4 py-2 border border-gray-400 rounded text-black" />
        </div>
        <div class="flex flex-col sm:flex-row gap-4 pt-6">
          <button
            @click="startBot"
            type="button" class="bg-[#4ba3e3] text-white px-6 py-2 rounded hover:bg-[#368acc] transition cursor-pointer"
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