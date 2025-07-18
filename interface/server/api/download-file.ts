import fs from "fs/promises"


export default defineEventHandler(async (event) => {
    const query = getQuery(event)
    const filename = query.filename as string

    const content = await fs.readFile(filename)
    const bytes = new Uint8Array(content)

    const blob = new Blob([bytes], {
        "type": "application/zip"
    })

    return blob
})