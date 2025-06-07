export default defineEventHandler(async (event) => {
    const storage = useStorage()

    console.log(storage.get('1749282152'))
})