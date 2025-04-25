import { axios } from "@pipedream/platform"
import xlsx from "xlsx"
import fs from "fs"

export default defineComponent({
  props: {
    excelFileUrl: {
      type: "string",
      label: "https://1drv.ms/x/c/ca832b41b3f96a17/ESAErOktSkpJqYyCB55xorYBPCnsjct9_rGBQBb5gKZbYw?e=VJO53o&nav=MTVfezAwMDAwMDAwLTAwMDEtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMH0",
      description: "URL to the Excel file containing the sawmilling data"
    }
  },
  async run({ steps, $ }) {
    // Download the Excel file
    const response = await axios($, {
      url: this.excelFileUrl,
      responseType: "arraybuffer"
    })
    
    // Write to temp file since we need to process multiple sheets
    const tempFile = "/tmp/sawmill-data.xlsx"
    fs.writeFileSync(tempFile, Buffer.from(response.data))
    
    // Read all sheets
    const workbook = xlsx.readFile(tempFile)
    const dfMain = xlsx.utils.sheet_to_json(workbook.Sheets["Milling"])
    const dfHeritage = xlsx.utils.sheet_to_json(workbook.Sheets["Heritage slabs index"])
    const dfWeights = xlsx.utils.sheet_to_json(workbook.Sheets["Log weight calculation"])
    const dfSheet3 = xlsx.utils.sheet_to_json(workbook.Sheets["Sheet3"])

    // Process data similar to Python script
    const uniqueHSpecies = new Set()
    const uniqueMSpecies = new Set()
    const HSpeciesDct = {}
    
    // Calculate board feet and prices
    const bdftDict = {}
    let bdftCum = 0
    let priceCum = 0
    
    dfSheet3.forEach((row) => {
      if (row.BdFt && !isNaN(row.BdFt)) {
        bdftCum += parseFloat(row.BdFt)
      }
      if (row["Price (15/bf)"] && !isNaN(row["Price (15/bf)"])) {
        priceCum += parseInt(row["Price (15/bf)"])
      }
      bdftDict[bdftCum] = priceCum
    })

    // Process dates and weights
    const dateDict = {}
    const startDate = 9 * 30 + 4

    dfWeights.forEach((row) => {
      if (row["Mill date"] && row.Weight) {
        const date = new Date(row["Mill date"])
        const year = date.getFullYear()
        const month = date.getMonth() + 1
        const day = date.getDate()
        const sumDate = (year - 2020) * 365 + month * 30 + day
        const sinceStart = sumDate - startDate
        
        if (!dateDict[sinceStart]) {
          dateDict[sinceStart] = [parseFloat(row.Weight)]
        } else {
          dateDict[sinceStart].push(parseFloat(row.Weight))
        }
      }
    })

    // Calculate averages
    Object.keys(dateDict).forEach((key) => {
      dateDict[key] = dateDict[key].reduce((a, b) => a + b, 0) / 2
    })

    // Calculate cumulative sums
    const keys = Object.keys(dateDict).sort((a, b) => a - b)
    keys.forEach((key, i) => {
      if (i > 0) {
        dateDict[key] += dateDict[keys[i-1]]
      }
    })

    // Calculate carbon comparison data
    const slope = 4.6 * 2204.623 / 365
    const xValues = [0, 1300]
    const yValues = xValues.map(x => slope * x)

    // Clean up temp file
    fs.unlinkSync(tempFile)

    // Return processed data
    return {
      boardFeetData: bdftDict,
      carbonData: {
        trees: dateDict,
        carComparison: {
          days: xValues,
          carbon: yValues
        }
      },
      uniqueSpecies: {
        heritage: Array.from(uniqueHSpecies),
        milled: Array.from(uniqueMSpecies)
      }
    }
  }
})