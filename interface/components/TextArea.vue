<template>
  <div>
    <label class="block text-base text-gray-300 mb-1 font-semibold">{{ label }}</label>
    <UTextarea
        v-model="value"
        :rows="rows"
        :placeholder="placeholder"
        class="w-full bg-[#2c2c2e] rounded text-white placeholder-gray-400 focus:outline-none focus:border-white"
        @update:modelValue="$emit('OnUpdateText', value)"
    ></UTextarea>
  </div>
</template>

<script setup lang="ts">
    defineProps<{
        label: string;
        placeholder?: string;
        rows?: number;
    }>();

    const value = ref("")

    defineEmits(["OnUpdateText"]);
</script>

<style></style>

