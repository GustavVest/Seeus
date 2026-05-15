<template>
  <section id="label-renderer" class="py-24 lg:py-32 bg-ice-white border-y border-black/[0.06]">
    <div class="max-w-7xl mx-auto px-6 lg:px-10">
      <div class="max-w-3xl mb-10 lg:mb-14">
        <span class="font-mono text-xs tracking-widest text-signal-purple">RENDER ENGINE</span>
        <h2 class="mt-4 font-display text-4xl lg:text-5xl text-primary-black tracking-tight font-medium leading-tight">
          Premium private label rendering.
        </h2>
        <p class="mt-4 text-lg text-graphite/75 max-w-2xl leading-relaxed">
          Generate clean label concepts from real product information — not broken AI text. Deterministic SVG rendering, browser-native, downloadable as PNG or SVG.
        </p>
      </div>

      <div class="grid lg:grid-cols-[440px_1fr] gap-8 items-start">
        <!-- ===== FORM ===== -->
        <div class="rounded-2xl border border-black/[0.08] bg-white p-6 lg:p-7 space-y-5">
          <label class="block">
            <span class="text-xs font-mono tracking-widest text-graphite/55">PRODUCT NAME</span>
            <input
              v-model="productName"
              type="text"
              class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-primary-black focus:outline-none focus:border-signal-purple"
            />
          </label>

          <label class="block">
            <span class="text-xs font-mono tracking-widest text-graphite/55">BRAND NAME</span>
            <input
              v-model="brandName"
              type="text"
              class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-primary-black focus:outline-none focus:border-signal-purple"
            />
          </label>

          <label class="block">
            <span class="text-xs font-mono tracking-widest text-graphite/55">SUBTITLE</span>
            <input
              v-model="subtitle"
              type="text"
              class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-primary-black focus:outline-none focus:border-signal-purple"
            />
          </label>

          <div class="grid grid-cols-2 gap-3">
            <label class="block">
              <span class="text-xs font-mono tracking-widest text-graphite/55">CATEGORY</span>
              <select v-model="productCategory" class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                <option value="food">Food</option>
                <option value="beverage">Beverage</option>
                <option value="supplement">Supplement</option>
                <option value="cosmetic">Cosmetic</option>
                <option value="private_label">Private label</option>
                <option value="other">Other</option>
              </select>
            </label>
            <label class="block">
              <span class="text-xs font-mono tracking-widest text-graphite/55">PACKAGE</span>
              <select v-model="packageType" class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                <option value="box">Box</option>
                <option value="bottle">Bottle</option>
                <option value="jar">Jar</option>
                <option value="pouch">Pouch</option>
                <option value="can">Can</option>
                <option value="sachet">Sachet</option>
                <option value="tube">Tube</option>
              </select>
            </label>
          </div>

          <label class="block">
            <span class="text-xs font-mono tracking-widest text-graphite/55">TARGET COUNTRY</span>
            <input
              v-model="targetCountry"
              type="text"
              class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-primary-black focus:outline-none focus:border-signal-purple"
            />
          </label>

          <label class="block">
            <span class="text-xs font-mono tracking-widest text-graphite/55">LABEL STYLE</span>
            <select v-model="labelStyle" class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
              <option value="clean_premium">Clean premium</option>
              <option value="nordic_minimal">Nordic minimal</option>
              <option value="modern_retail">Modern retail</option>
              <option value="natural_organic">Natural / organic</option>
              <option value="scientific_supplement">Scientific supplement</option>
              <option value="bold_commercial">Bold commercial</option>
            </select>
          </label>

          <div class="grid grid-cols-2 gap-3">
            <label class="block">
              <span class="text-xs font-mono tracking-widest text-graphite/55">NET CONTENT</span>
              <input
                v-model="netContent"
                type="text"
                class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-primary-black focus:outline-none focus:border-signal-purple"
              />
            </label>
            <label class="block">
              <span class="text-xs font-mono tracking-widest text-graphite/55">ORIGIN</span>
              <input
                v-model="origin"
                type="text"
                class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-primary-black focus:outline-none focus:border-signal-purple"
              />
            </label>
          </div>

          <label class="block">
            <span class="text-xs font-mono tracking-widest text-graphite/55">BENEFITS (COMMA-SEPARATED)</span>
            <input
              v-model="benefitText"
              type="text"
              class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-primary-black focus:outline-none focus:border-signal-purple"
            />
          </label>

          <label class="block">
            <span class="text-xs font-mono tracking-widest text-graphite/55">CLAIMS / BADGES (COMMA-SEPARATED)</span>
            <input
              v-model="claimsText"
              type="text"
              class="mt-1.5 w-full px-3 py-2.5 bg-ice-white border border-black/10 rounded-md text-sm text-primary-black focus:outline-none focus:border-signal-purple"
            />
          </label>
        </div>

        <!-- ===== PREVIEW ===== -->
        <div class="rounded-2xl border border-black/[0.08] bg-white p-6 lg:p-7">
          <div class="flex flex-wrap items-center justify-between gap-3 mb-5">
            <div>
              <div class="font-mono text-[10px] tracking-widest text-graphite/55">LIVE PREVIEW</div>
              <p class="text-sm text-graphite/75">Updates as you type. No round-trip to a model.</p>
            </div>
            <div class="flex gap-2">
              <button
                type="button"
                @click="downloadPng"
                :disabled="busy"
                class="px-4 py-2 text-sm font-semibold rounded-md bg-primary-black text-ice-white hover:bg-signal-purple disabled:opacity-60 disabled:cursor-not-allowed transition-colors"
              >
                {{ busy ? 'Rendering…' : 'Download PNG' }}
              </button>
              <button
                type="button"
                @click="downloadSvg"
                class="px-4 py-2 text-sm font-semibold rounded-md border border-black/15 text-graphite hover:bg-ice-white transition-colors"
              >
                Download SVG
              </button>
            </div>
          </div>

          <div class="rounded-xl bg-ice-white p-4 lg:p-6 shadow-inner border border-black/[0.04] flex justify-center">
            <svg
              ref="svgEl"
              :viewBox="`0 0 ${SVG_W} ${SVG_H}`"
              :width="SVG_W"
              :height="SVG_H"
              xmlns="http://www.w3.org/2000/svg"
              class="w-full max-w-[460px] h-auto rounded-md"
              :style="{ background: theme.background }"
            >
              <!-- Inner frame -->
              <rect
                :x="36" :y="36"
                :width="SVG_W - 72" :height="SVG_H - 72"
                :rx="32"
                fill="none"
                :stroke="theme.border"
                stroke-width="1"
              />

              <!-- Top row: brand + country -->
              <text
                :x="100" :y="135"
                :fill="theme.secondary"
                font-family="Inter, Helvetica, Arial, sans-serif"
                font-size="26"
                letter-spacing="3"
              >{{ (brandName || 'PRIVATE LABEL').toUpperCase() }}</text>
              <text
                :x="SVG_W - 100" :y="135"
                text-anchor="end"
                :fill="theme.secondary"
                font-family="Inter, Helvetica, Arial, sans-serif"
                font-size="26"
                letter-spacing="3"
              >{{ targetCountry.toUpperCase() }}</text>

              <!-- Category chip -->
              <g>
                <rect
                  :x="SVG_W / 2 - 110" :y="245"
                  width="220" height="48"
                  rx="24"
                  fill="none"
                  :stroke="theme.border"
                />
                <text
                  :x="SVG_W / 2" :y="277"
                  text-anchor="middle"
                  :fill="theme.secondary"
                  font-family="Inter, Helvetica, Arial, sans-serif"
                  font-size="20"
                >{{ getCategoryLabel(productCategory) }}</text>
              </g>

              <!-- Product name (hero) -->
              <text
                :x="SVG_W / 2" :y="430"
                text-anchor="middle"
                :fill="theme.primary"
                font-family="Inter, Helvetica, Arial, sans-serif"
                font-size="84"
                font-weight="700"
                letter-spacing="-2"
              >{{ productName || 'Product Name' }}</text>

              <!-- Subtitle -->
              <text
                :x="SVG_W / 2" :y="495"
                text-anchor="middle"
                :fill="theme.secondary"
                font-family="Inter, Helvetica, Arial, sans-serif"
                font-size="32"
              >{{ subtitle || 'Premium market-adapted product concept' }}</text>

              <!-- Concept ring -->
              <g :transform="`translate(${SVG_W / 2}, 720)`">
                <circle cx="0" cy="0" r="120" fill="none" :stroke="theme.accent" stroke-width="2.5" />
                <text
                  x="0" y="8"
                  text-anchor="middle"
                  :fill="theme.accent"
                  font-family="Inter, Helvetica, Arial, sans-serif"
                  font-size="22"
                  letter-spacing="2"
                >CONCEPT</text>
              </g>

              <!-- Benefit chips (up to 3) -->
              <g v-if="benefits.length">
                <g v-for="(b, i) in benefits.slice(0, 3)" :key="i">
                  <rect
                    :x="benefitX(i)" :y="990"
                    :width="benefitW" height="100"
                    rx="20"
                    fill="none"
                    :stroke="theme.border"
                  />
                  <text
                    :x="benefitX(i) + benefitW / 2" :y="1050"
                    text-anchor="middle"
                    :fill="theme.primary"
                    font-family="Inter, Helvetica, Arial, sans-serif"
                    font-size="22"
                  >{{ b }}</text>
                </g>
              </g>

              <!-- Claim chips at the bottom -->
              <g v-if="claims.length">
                <g v-for="(c, i) in claims.slice(0, 4)" :key="i">
                  <rect
                    :x="claimX(i)" :y="1240"
                    :width="claimW(c)" height="44"
                    rx="22"
                    fill="none"
                    :stroke="theme.border"
                  />
                  <text
                    :x="claimX(i) + claimW(c) / 2" :y="1270"
                    text-anchor="middle"
                    :fill="theme.secondary"
                    font-family="Inter, Helvetica, Arial, sans-serif"
                    font-size="20"
                  >{{ c }}</text>
                </g>
              </g>

              <!-- Footer: net content / origin / disclaimer -->
              <text
                :x="100" :y="1360"
                :fill="theme.secondary"
                font-family="Inter, Helvetica, Arial, sans-serif"
                font-size="24"
              >{{ netContent || 'Net content' }}</text>
              <text
                :x="SVG_W - 100" :y="1360"
                text-anchor="end"
                :fill="theme.secondary"
                font-family="Inter, Helvetica, Arial, sans-serif"
                font-size="24"
              >{{ origin || 'Origin / producer' }}</text>

              <text
                :x="SVG_W / 2" :y="1420"
                text-anchor="middle"
                :fill="theme.secondary"
                font-family="Inter, Helvetica, Arial, sans-serif"
                font-size="16"
                opacity="0.7"
              >Concept mockup only — final claims and declarations require review.</text>
            </svg>
          </div>

          <p class="mt-4 text-xs text-graphite/55 leading-relaxed">
            Generated labels are concept mockups only. Final label text, claims, nutrition information, ingredients, and regulatory wording must be reviewed before commercial use.
          </p>
        </div>
      </div>

      <!-- TODO future extensions:
           - Multiple templates per category (back label / nutrition table)
           - Real GLB 3D mockup with Three.js
           - Ingredient declaration + claims-risk auto-checker
           - Before/after comparison renderer
           - Persistent storage of generated PNGs (S3 / Supabase)
           - Paid unlock for higher resolution / vector export -->
    </div>
  </section>
</template>

<script setup>
import { ref, computed, useTemplateRef } from 'vue'

const SVG_W = 1200
const SVG_H = 1600

// Form state (defaults match the spec's React reference)
const productName = ref('Premium Calcium')
const brandName = ref('Private Label')
const subtitle = ref('Market-adapted premium supplement')
const productCategory = ref('supplement')
const packageType = ref('bottle')
const targetCountry = ref('Lithuania')
const labelStyle = ref('clean_premium')
const netContent = ref('60 capsules')
const origin = ref('Produced in Europe')
const benefitText = ref('Premium positioning, Market adapted, Shelf ready')
const claimsText = ref('Clean label direction, Premium format')

const busy = ref(false)
const svgEl = useTemplateRef('svgEl')

// 6 themes per the spec
const STYLE_THEMES = {
  clean_premium:         { background: '#F8FAFC', primary: '#0F172A', secondary: '#475569', accent: '#0EA5E9', border: '#CBD5E1' },
  nordic_minimal:        { background: '#F8FAFC', primary: '#111827', secondary: '#6B7280', accent: '#38BDF8', border: '#D1D5DB' },
  modern_retail:         { background: '#FFFFFF', primary: '#020617', secondary: '#64748B', accent: '#2563EB', border: '#E2E8F0' },
  natural_organic:       { background: '#FAFAF5', primary: '#1F2933', secondary: '#5F6F52', accent: '#7A9E65', border: '#D8D6C3' },
  scientific_supplement: { background: '#F8FAFC', primary: '#0B1120', secondary: '#475569', accent: '#0369A1', border: '#CBD5E1' },
  bold_commercial:       { background: '#0F172A', primary: '#FFFFFF', secondary: '#CBD5E1', accent: '#FACC15', border: '#334155' },
}

const theme = computed(() => STYLE_THEMES[labelStyle.value] || STYLE_THEMES.clean_premium)

const benefits = computed(() =>
  benefitText.value.split(',').map(s => s.trim()).filter(Boolean)
)
const claims = computed(() =>
  claimsText.value.split(',').map(s => s.trim()).filter(Boolean)
)

function getCategoryLabel(cat) {
  return {
    food: 'Food Product',
    beverage: 'Beverage',
    supplement: 'Supplement',
    cosmetic: 'Cosmetic',
    private_label: 'Private Label',
    other: 'Product',
  }[cat] || 'Product'
}

// Benefit positioning (up to 3 across)
const benefitW = 320
function benefitX(i) {
  const total = 3 * benefitW + 2 * 30
  const startX = (SVG_W - total) / 2
  return startX + i * (benefitW + 30)
}

// Claim chip positioning (up to 4 across)
function claimW(c) { return Math.max(140, c.length * 12 + 36) }
function claimX(i) {
  const widths = claims.value.slice(0, 4).map(claimW)
  const totalWithGaps = widths.reduce((a, b) => a + b, 0) + (widths.length - 1) * 16
  const startX = (SVG_W - totalWithGaps) / 2
  let x = startX
  for (let k = 0; k < i; k++) x += widths[k] + 16
  return x
}

function _slug(s) {
  return (s || 'label').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')
}

function downloadSvg() {
  if (!svgEl.value) return
  // Clone + serialize so we can attach xmlns explicitly, ensuring the file
  // opens correctly outside the browser.
  const clone = svgEl.value.cloneNode(true)
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
  const serialized = new XMLSerializer().serializeToString(clone)
  const blob = new Blob([
    '<?xml version="1.0" encoding="UTF-8"?>\n',
    serialized,
  ], { type: 'image/svg+xml' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${_slug(productName.value)}-label-concept.svg`
  a.click()
  URL.revokeObjectURL(url)
}

async function downloadPng() {
  if (!svgEl.value) return
  busy.value = true
  try {
    // Serialize the live SVG, draw it on a canvas, export to PNG.
    const clone = svgEl.value.cloneNode(true)
    clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg')
    const serialized = new XMLSerializer().serializeToString(clone)
    const blob = new Blob([serialized], { type: 'image/svg+xml;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    await new Promise((resolve, reject) => {
      const img = new Image()
      img.onload = () => {
        const canvas = document.createElement('canvas')
        canvas.width = SVG_W
        canvas.height = SVG_H
        const ctx = canvas.getContext('2d')
        ctx.fillStyle = theme.value.background
        ctx.fillRect(0, 0, SVG_W, SVG_H)
        ctx.drawImage(img, 0, 0, SVG_W, SVG_H)
        canvas.toBlob((pngBlob) => {
          const dlUrl = URL.createObjectURL(pngBlob)
          const a = document.createElement('a')
          a.href = dlUrl
          a.download = `${_slug(productName.value)}-label-concept.png`
          a.click()
          URL.revokeObjectURL(dlUrl)
          URL.revokeObjectURL(url)
          resolve()
        }, 'image/png')
      }
      img.onerror = reject
      img.src = url
    })
  } finally {
    busy.value = false
  }
}
</script>
