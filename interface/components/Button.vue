<template>
    <UButton
        @click="$emit('click')"
        :type="type"
        :class="computedClass"
        :disabled="disabled"
    >
        <slot>SUBMIT</slot>
    </UButton>
</template>

<script setup lang="ts">
    import { computed } from 'vue'

    const props = defineProps<{
        type?: 'button' | 'submit' | 'reset',
        customClass?: string,
        disabled?: boolean
    }>()

    const defaultClass = "bg-white text-black px-6 py-2 rounded hover:bg-black hover:text-white border border-white transition cursor-pointer"

    const computedClass = computed(() => {
        return props.customClass ?? defaultClass
    })
</script>

<style></style>