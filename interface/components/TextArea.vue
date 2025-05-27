<template>
    <div>
        <label class="block text-base text-gray-300 mb-1 font-semibold">{{ label }}</label>
        <textarea
            :rows="rows"
            :placeholder="placeholder"
            :value="modelValue"
            class="w-full px-4 py-2 border border-gray-700 bg-[#2c2c2e] rounded text-white placeholder-gray-400 focus:outline-none focus:border-white"
        />
    </div>
</template>


<script setup lang="ts">
    defineProps<{
        label: string
        modelValue: string
        placeholder?: string
        rows?: number
    }>()
</script>

<style>
</style>