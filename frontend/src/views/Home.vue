<template>
  <div class="min-h-screen bg-ice-white text-graphite font-sans antialiased">
    <!-- ===== HEADER ===== -->
    <header class="sticky top-0 z-40 bg-ice-white/60 backdrop-blur-xl backdrop-saturate-150 border-b border-black/[0.06]">
      <div class="max-w-7xl mx-auto px-6 lg:px-10 h-16 flex items-center justify-between">
        <a href="#top" class="flex items-center" aria-label="ORAMA INTEL home">
          <img src="../assets/logo/oramaintel-logo.png" alt="ORAMA INTEL" class="h-6 w-auto" />
        </a>

        <nav
          class="relative hidden md:flex items-center gap-0.5 p-1 rounded-full bg-white/40 backdrop-blur-xl border border-black/[0.07] shadow-[0_1px_2px_rgba(0,0,0,0.03)]"
          @mouseleave="indicator.visible = false"
        >
          <span
            class="absolute top-1 bottom-1 rounded-full bg-white shadow-[0_1px_3px_rgba(0,0,0,0.06)] border border-black/[0.05] pointer-events-none transition-[left,width,opacity] duration-300 ease-out"
            :style="{
              left: indicator.left + 'px',
              width: indicator.width + 'px',
              opacity: indicator.visible ? 1 : 0,
            }"
          ></span>
          <a
            v-for="(link, i) in navLinks"
            :key="link.href"
            :href="link.href"
            @mouseenter="updateIndicator"
            class="group relative z-10 flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-graphite/70 hover:text-primary-black transition-colors duration-150"
          >
            <span class="font-mono text-[9px] font-semibold tracking-[0.15em] text-signal-purple/60 group-hover:text-signal-purple tabular-nums transition-colors">
              0{{ i + 1 }}
            </span>
            <span class="text-[13px] font-medium">{{ link.label }}</span>
          </a>
        </nav>

        <button
          @click="openUpload"
          class="group inline-flex items-center gap-2 bg-primary-black text-ice-white px-4 py-2 text-sm font-semibold rounded-md hover:bg-signal-purple transition-colors"
        >
          Create market-ready label
          <span class="text-base leading-none transition-transform group-hover:translate-x-0.5">→</span>
        </button>
      </div>
    </header>

    <!-- ===== HERO ===== -->
    <section id="top" class="relative overflow-hidden">
      <div class="max-w-7xl mx-auto px-6 lg:px-10 pt-16 pb-20 lg:pt-24 lg:pb-28 grid lg:grid-cols-12 gap-12 items-start">
        <div class="lg:col-span-5 lg:sticky lg:top-28">
          <div class="inline-flex items-center gap-2 mb-6 px-3 py-1 rounded-full border border-signal-purple/30 bg-signal-purple/5 text-signal-purple text-xs font-mono tracking-wide">
            <span class="w-1.5 h-1.5 rounded-full bg-signal-purple"></span>
            MARKET-READY LABEL ADAPTATION
          </div>

          <h1 class="font-display text-5xl lg:text-6xl leading-[1.05] tracking-tight text-primary-black font-medium">
            Launch-ready product labels
            <span class="block">for any <span class="text-signal-purple">target market</span>.</span>
          </h1>

          <p class="mt-6 text-lg text-graphite/75 max-w-xl leading-relaxed">
            ORAMA INTEL helps food, beverage, supplement, and private-label companies adapt labels, product messaging, and retail positioning for new countries — with a premium, locally relevant format.
          </p>

          <div class="mt-8 flex flex-wrap items-center gap-4">
            <a
              href="#configurator"
              class="group inline-flex items-center gap-2 bg-primary-black text-ice-white px-6 py-3.5 text-sm font-semibold rounded-md hover:bg-signal-purple transition-colors"
            >
              Create market-ready label
              <span class="text-base leading-none transition-transform group-hover:translate-x-0.5">→</span>
            </a>
            <a href="#how" class="text-sm font-medium text-graphite/70 hover:text-primary-black transition-colors">
              See how it works
            </a>
          </div>

          <p class="mt-6 text-sm text-graphite/60 max-w-md">
            Localized label copy, claims direction, palette, hierarchy, and buyer-facing positioning — generated for the country your product is entering.
          </p>
        </div>

        <!-- 4-field configurator -->
        <div id="configurator" class="lg:col-span-7">
          <div class="relative">
            <div class="absolute -inset-4 bg-gradient-to-tr from-signal-purple/10 via-transparent to-electric-violet/10 blur-2xl rounded-3xl"></div>
            <div class="relative bg-white border border-black/8 rounded-2xl shadow-[0_24px_60px_-20px_rgba(5,5,5,0.18)] overflow-hidden">
              <div class="flex items-center justify-between px-6 py-3 border-b border-black/[0.06] bg-ice-white">
                <span class="font-mono text-[11px] text-graphite/55 tracking-widest">CONFIGURATOR · UPLOAD + 4 STEPS</span>
                <span class="font-mono text-[11px] text-market-green tracking-widest flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-market-green"></span>
                  LIVE
                </span>
              </div>

              <div class="p-6 lg:p-8 space-y-7">

                <!-- Step 0: Upload (file dropzone visible up front) -->
                <div>
                  <label class="font-display text-lg text-primary-black font-semibold">
                    <span class="font-mono text-[10px] text-signal-purple tracking-widest mr-2">00</span>
                    Upload your label or product sheet
                  </label>
                  <label
                    :class="[
                      'mt-3 block border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-colors',
                      heroDragOver
                        ? 'border-signal-purple bg-signal-purple/5'
                        : selectedFile
                          ? 'border-market-green/60 bg-market-green/5'
                          : 'border-black/15 hover:border-signal-purple/50 hover:bg-signal-purple/[0.03]',
                    ]"
                    @dragover.prevent="heroDragOver = true"
                    @dragleave.prevent="heroDragOver = false"
                    @drop.prevent="handleHeroDrop"
                  >
                    <input
                      type="file"
                      accept=".pdf,.png,.jpg,.jpeg,.webp"
                      class="hidden"
                      @change="handleHeroFile"
                    />
                    <div v-if="!selectedFile">
                      <div class="w-9 h-9 mx-auto mb-2 rounded-full border-2 border-graphite/30 flex items-center justify-center text-graphite/55 text-base">↑</div>
                      <p class="text-sm font-medium text-primary-black">Drop your label, packaging photo, or product sheet</p>
                      <p class="text-[11px] text-graphite/55 mt-1">PDF, PNG, JPG, or WEBP · max 15&nbsp;MB</p>
                    </div>
                    <div v-else class="text-left">
                      <div class="flex items-center justify-between gap-3">
                        <div class="min-w-0">
                          <div class="font-mono text-[10px] tracking-widest text-market-green mb-0.5">SELECTED</div>
                          <p class="text-sm font-medium text-primary-black truncate">{{ selectedFile.name }}</p>
                          <p class="text-[11px] text-graphite/55">{{ formatBytes(selectedFile.size) }}</p>
                        </div>
                        <button
                          type="button"
                          @click.prevent.stop="selectedFile = null"
                          class="text-xs font-mono tracking-widest text-graphite/55 hover:text-risk-red transition-colors flex-shrink-0"
                        >
                          ↻ REPLACE
                        </button>
                      </div>
                    </div>
                  </label>
                  <p v-if="heroUploadError" class="mt-2 text-xs text-risk-red flex items-center gap-1.5">
                    <span>⚠</span>{{ heroUploadError }}
                  </p>
                  <p v-else class="mt-2 text-xs text-graphite/60">
                    We use this to adapt the label artwork, wording, and positioning for your target country.
                  </p>
                </div>

                <!-- Step 1: Target Country (most prominent) -->
                <div>
                  <div class="flex items-center justify-between mb-2">
                    <label class="font-display text-lg text-primary-black font-semibold">
                      <span class="font-mono text-[10px] text-signal-purple tracking-widest mr-2">01</span>
                      Target country
                    </label>
                  </div>
                  <select
                    v-model="cfgTargetCountry"
                    class="w-full px-4 py-4 bg-white border-2 border-black/10 rounded-lg text-base text-primary-black font-medium focus:outline-none focus:border-signal-purple transition-colors"
                  >
                    <option value="">Pick a country…</option>
                    <option>Lithuania</option>
                    <option>Norway</option>
                    <option>Sweden</option>
                    <option>Germany</option>
                    <option>Denmark</option>
                    <option>South Korea</option>
                    <option>Japan</option>
                    <option>United Kingdom</option>
                    <option>USA</option>
                    <option>EU</option>
                    <option>Nordics</option>
                  </select>
                  <p class="mt-2 text-xs text-graphite/60">
                    Choose the market you want the product to feel native to.
                  </p>
                </div>

                <!-- Step 2: Product Style -->
                <div>
                  <label class="font-display text-base text-primary-black font-semibold">
                    <span class="font-mono text-[10px] text-signal-purple tracking-widest mr-2">02</span>
                    Product style
                  </label>
                  <select
                    v-model="cfgProductStyle"
                    class="mt-2 w-full px-3 py-3 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple"
                  >
                    <option>Clean premium</option>
                    <option>Nordic minimal</option>
                    <option>Modern retail</option>
                    <option>Natural / organic</option>
                    <option>Scientific supplement</option>
                    <option>Bold commercial</option>
                    <option>Custom style</option>
                  </select>
                  <p class="mt-2 text-xs text-graphite/60">
                    We adapt the label tone, claims style, and visual direction to the market and product category.
                  </p>
                </div>

                <!-- Step 3: Tier (cards) -->
                <div>
                  <label class="font-display text-base text-primary-black font-semibold">
                    <span class="font-mono text-[10px] text-signal-purple tracking-widest mr-2">03</span>
                    Tier
                  </label>
                  <div class="mt-3 grid sm:grid-cols-3 gap-2">
                    <button
                      v-for="t in tierOptions"
                      :key="t.id"
                      type="button"
                      @click="cfgTier = t.id"
                      :class="[
                        'text-left p-3 rounded-lg border-2 transition-colors',
                        cfgTier === t.id
                          ? 'border-signal-purple bg-signal-purple/5'
                          : 'border-black/[0.08] bg-white hover:border-black/30',
                      ]"
                    >
                      <div class="flex items-center justify-between">
                        <span class="font-display text-sm font-semibold text-primary-black">{{ t.name }}</span>
                        <span v-if="cfgTier === t.id" class="text-signal-purple text-xs">✓</span>
                      </div>
                      <p class="mt-1 text-[11px] text-graphite/70 leading-snug">{{ t.tagline }}</p>
                    </button>
                  </div>
                </div>

                <!-- Step 4: Buyer Type -->
                <div>
                  <label class="font-display text-base text-primary-black font-semibold">
                    <span class="font-mono text-[10px] text-signal-purple tracking-widest mr-2">04</span>
                    Buyer type
                  </label>
                  <select
                    v-model="cfgBuyerType"
                    class="mt-2 w-full px-3 py-3 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple"
                  >
                    <option>Food producer</option>
                    <option>Supplement brand</option>
                    <option>Beverage company</option>
                    <option>Private label manufacturer</option>
                    <option>Distributor / importer</option>
                    <option>Other</option>
                  </select>
                  <p class="mt-2 text-xs text-graphite/60">
                    This helps tailor the output to the person who needs to approve, sell, or distribute the product.
                  </p>
                </div>

                <!-- Advanced details accordion -->
                <details class="rounded-lg border border-black/[0.08] group">
                  <summary class="px-4 py-3 text-sm text-graphite/80 cursor-pointer select-none flex items-center justify-between hover:bg-black/[0.02] transition-colors">
                    <span>Advanced details (optional)</span>
                    <span class="text-graphite/40 group-open:rotate-90 transition-transform">›</span>
                  </summary>
                  <div class="px-4 pb-4 pt-1">
                    <textarea
                      v-model="cfgAdvancedDetails"
                      rows="3"
                      placeholder="Anything else we should know — ingredients, claims, certifications, brand notes, regulatory constraints…"
                      class="w-full px-3 py-2 bg-ice-white border border-black/10 rounded-md text-xs text-graphite placeholder:text-graphite/40 focus:outline-none focus:border-signal-purple resize-none"
                    />
                  </div>
                </details>

                <!-- Submit -->
                <button
                  @click="submitConfigurator"
                  :disabled="!cfgTargetCountry"
                  class="w-full inline-flex items-center justify-center gap-2 bg-primary-black text-ice-white px-5 py-4 text-sm font-semibold rounded-md hover:bg-signal-purple disabled:bg-graphite/30 disabled:cursor-not-allowed transition-colors"
                >
                  Create market-ready label
                  <span class="text-base leading-none">→</span>
                </button>
                <p class="text-[11px] text-graphite/55 text-center -mt-3">
                  Next step: upload your existing label so we can adapt it.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== TRUST STRIP ===== -->
    <section class="border-y border-black/5 bg-white">
      <div class="max-w-7xl mx-auto px-6 lg:px-10 py-12">
        <div class="grid lg:grid-cols-2 gap-10 items-center">
          <div>
            <h2 class="font-display text-2xl lg:text-3xl text-primary-black tracking-tight font-medium">
              Built for brands expanding across borders.
            </h2>
            <p class="mt-3 text-sm text-graphite/70 max-w-md">
              Designed around real export-market packaging workflows — not generic AI design.
            </p>
          </div>
          <div class="flex flex-col gap-4">
            <div class="flex flex-wrap gap-2">
              <span v-for="market in markets" :key="market" class="px-3 py-1.5 rounded-full border border-black/10 text-xs font-mono tracking-wider text-graphite/80 bg-white">
                {{ market }}
              </span>
            </div>
            <div class="flex flex-wrap gap-2">
              <span v-for="cat in categories" :key="cat" class="px-3 py-1.5 rounded-full border border-signal-purple/20 bg-signal-purple/5 text-xs font-mono tracking-wider text-signal-purple">
                {{ cat }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== PROBLEM / SOLUTION ===== -->
    <section id="product" class="py-24 lg:py-32">
      <div class="max-w-7xl mx-auto px-6 lg:px-10 grid lg:grid-cols-2 gap-14 items-start">
        <div>
          <span class="font-mono text-xs tracking-widest text-signal-purple">01 / PROBLEM</span>
          <h2 class="mt-4 font-display text-4xl lg:text-5xl text-primary-black tracking-tight font-medium leading-tight">
            Most products do not fail because of the ingredient.
          </h2>
          <p class="mt-5 text-lg text-graphite/75 leading-relaxed">
            They fail because the label, positioning, and product story do not match the market. A product that works in one country can look generic, confusing, or low-trust in another.
          </p>
        </div>
        <div class="p-8 rounded-2xl bg-primary-black text-ice-white">
          <span class="font-mono text-xs tracking-widest text-electric-violet">02 / SOLUTION</span>
          <h2 class="mt-4 font-display text-3xl lg:text-4xl tracking-tight font-medium leading-tight">
            We adapt the product to the market before it reaches the shelf.
          </h2>
          <p class="mt-5 text-base text-ice-white/75 leading-relaxed">
            ORAMA INTEL turns product information into localized, premium, buyer-ready label and marketing material — tailored to the country, channel, and buyer you are targeting.
          </p>
        </div>
      </div>
    </section>

    <!-- ===== HOW IT WORKS · 3 STEPS ===== -->
    <section id="how" class="py-24 lg:py-32 bg-ice-white border-y border-black/[0.06]">
      <div class="max-w-7xl mx-auto px-6 lg:px-10">
        <div class="max-w-3xl">
          <span class="font-mono text-xs tracking-widest text-signal-purple">03 / HOW IT WORKS</span>
          <h2 class="mt-4 font-display text-4xl lg:text-5xl text-primary-black tracking-tight font-medium leading-tight">
            Three steps from product to market-ready package.
          </h2>
        </div>

        <div class="mt-14 grid sm:grid-cols-3 gap-6">
          <div v-for="(step, i) in howItWorks" :key="step.title" class="relative">
            <div class="flex items-center gap-3 mb-5">
              <span class="font-display text-5xl font-medium text-signal-purple tracking-tight">0{{ i + 1 }}</span>
              <span v-if="i < howItWorks.length - 1" class="hidden sm:block flex-1 h-px bg-black/10"></span>
            </div>
            <h3 class="font-display text-xl text-primary-black font-semibold">{{ step.title }}</h3>
            <p class="mt-2 text-sm text-graphite/75 leading-relaxed">{{ step.body }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== WHO IT IS FOR ===== -->
    <section class="py-24 lg:py-32">
      <div class="max-w-7xl mx-auto px-6 lg:px-10">
        <div class="max-w-3xl">
          <span class="font-mono text-xs tracking-widest text-signal-purple">04 / WHO IT IS FOR</span>
          <h2 class="mt-4 font-display text-4xl lg:text-5xl text-primary-black tracking-tight font-medium leading-tight">
            Built for the teams shipping products across borders.
          </h2>
        </div>

        <div class="mt-14 grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <div v-for="aud in audiences" :key="aud.title" class="p-6 bg-white rounded-xl border border-black/[0.08] hover:border-signal-purple/40 transition-colors">
            <h3 class="font-display text-lg text-primary-black font-semibold">{{ aud.title }}</h3>
            <p class="mt-2 text-sm text-graphite/75 leading-relaxed">{{ aud.body }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== ANALYSIS ENGINE ===== -->
    <section class="py-24 lg:py-32">
      <div class="max-w-7xl mx-auto px-6 lg:px-10">
        <div class="max-w-3xl">
          <span class="font-mono text-xs tracking-widest text-signal-purple">03 / ENGINE</span>
          <h2 class="mt-4 font-display text-4xl lg:text-5xl text-primary-black tracking-tight font-medium leading-tight">
            Concrete feedback, not vague design advice.
          </h2>
        </div>

        <div class="mt-14 grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div v-for="card in engineCards" :key="card.title" class="p-5 bg-white border border-black/8 rounded-lg hover:bg-signal-purple/[0.03] hover:border-signal-purple/30 transition-colors">
            <div class="font-mono text-[10px] text-graphite/50 tracking-widest mb-2">{{ card.tag }}</div>
            <h3 class="font-display text-base text-primary-black font-semibold">{{ card.title }}</h3>
          </div>
        </div>

        <!-- Sample insight quote -->
        <div class="mt-14 p-8 lg:p-10 bg-gradient-to-br from-signal-purple/5 to-electric-violet/5 border border-signal-purple/20 rounded-2xl">
          <div class="flex items-start gap-5">
            <div class="hidden sm:flex w-10 h-10 rounded-md bg-signal-purple text-ice-white items-center justify-center flex-shrink-0 font-mono text-lg">"</div>
            <div>
              <span class="font-mono text-xs tracking-widest text-signal-purple">SAMPLE INSIGHT</span>
              <p class="mt-2 font-display text-xl lg:text-2xl text-primary-black leading-snug">
                Your current label may feel too clinical for Korean D2C wellness buyers, but not technical enough for Japanese pharmacy channels.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== BEFORE / AFTER EXAMPLES ===== -->
    <section id="examples" class="py-24 lg:py-32 bg-white border-y border-black/5">
      <div class="max-w-7xl mx-auto px-6 lg:px-10">
        <div class="max-w-3xl">
          <span class="font-mono text-xs tracking-widest text-signal-purple">04 / EXAMPLES</span>
          <h2 class="mt-4 font-display text-4xl lg:text-5xl text-primary-black tracking-tight font-medium leading-tight">
            One product. Different markets. Different buying logic.
          </h2>
        </div>

        <div class="mt-14 grid md:grid-cols-3 gap-5">
          <div v-for="ex in examples" :key="ex.title" class="bg-ice-white border border-black/8 rounded-xl p-6 flex flex-col">
            <div class="flex items-center gap-2 font-mono text-xs tracking-wider text-graphite/60 mb-4">
              <span>{{ ex.from }}</span>
              <span class="text-signal-purple">→</span>
              <span class="text-primary-black font-semibold">{{ ex.to }}</span>
            </div>
            <ul class="space-y-3 flex-1">
              <li v-for="(point, i) in ex.points" :key="i" class="flex gap-2.5 text-sm text-graphite/85">
                <span class="text-signal-purple mt-1">›</span>
                <span>{{ point }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== PRICING ===== -->
    <section id="pricing" class="py-24 lg:py-32">
      <div class="max-w-7xl mx-auto px-6 lg:px-10">
        <div class="max-w-3xl">
          <span class="font-mono text-xs tracking-widest text-signal-purple">05 / PRICING</span>
          <h2 class="mt-4 font-display text-4xl lg:text-5xl text-primary-black tracking-tight font-medium leading-tight">
            Start with a free score. Upgrade when you need the fix.
          </h2>
          <p class="mt-5 text-lg text-graphite/75 max-w-2xl leading-relaxed">
            Get instant market-fit feedback for free. Pay only when you want ORAMA INTEL to generate a market-adapted packaging concept.
          </p>
        </div>

        <div class="mt-14 grid md:grid-cols-3 gap-5">
          <div
            v-for="tier in tiers"
            :key="tier.name"
            :class="[
              'rounded-2xl p-7 flex flex-col border',
              tier.featured
                ? 'bg-primary-black text-ice-white border-primary-black shadow-[0_20px_50px_-20px_rgba(124,58,237,0.45)]'
                : 'bg-white text-graphite border-black/10',
            ]"
          >
            <div v-if="tier.badge" class="mb-4">
              <span class="inline-flex items-center gap-1.5 px-3 py-1 text-[10px] font-mono tracking-widest rounded-full bg-signal-purple text-ice-white">
                <span class="w-1 h-1 rounded-full bg-electric-violet"></span>
                {{ tier.badge.toUpperCase() }}
              </span>
            </div>

            <h3 :class="['font-display text-xl font-semibold', tier.featured ? 'text-ice-white' : 'text-primary-black']">
              {{ tier.name }}
            </h3>

            <div class="mt-5 flex items-end gap-2">
              <span :class="['font-display text-5xl font-medium tracking-tight tabular-nums', tier.featured ? 'text-ice-white' : 'text-primary-black']">
                {{ tier.price }}
              </span>
              <span
                v-if="tier.price !== '€0'"
                :class="['pb-1 text-xs', tier.featured ? 'text-ice-white/60' : 'text-graphite/60']"
              >
                {{ tier.unit || 'per product / market' }}
              </span>
            </div>

            <p :class="['mt-5 text-sm leading-6', tier.featured ? 'text-ice-white/70' : 'text-graphite/70']">
              {{ tier.description }}
            </p>

            <ul class="mt-8 space-y-3 flex-1">
              <li
                v-for="(feat, i) in tier.features"
                :key="i"
                :class="['flex gap-3 text-sm', tier.featured ? 'text-ice-white/90' : 'text-graphite/85']"
              >
                <span
                  :class="[
                    'mt-1.5 h-1.5 w-1.5 rounded-full flex-shrink-0',
                    tier.featured ? 'bg-market-green' : 'bg-signal-purple',
                  ]"
                ></span>
                <span>{{ feat }}</span>
              </li>
            </ul>

            <button
              @click="openUpload"
              :class="[
                'mt-9 w-full inline-flex items-center justify-center gap-2 px-5 py-3 text-sm font-semibold rounded-md transition-colors',
                tier.featured
                  ? 'bg-ice-white text-primary-black hover:bg-electric-violet hover:text-ice-white'
                  : 'bg-primary-black text-ice-white hover:bg-signal-purple',
              ]"
            >
              {{ tier.cta || 'Create market-ready label' }}
              <span class="text-base leading-none">→</span>
            </button>
          </div>
        </div>

        <p class="mt-8 text-xs text-graphite/55 max-w-3xl leading-relaxed">
          Adaptation outputs are AI-generated packaging concepts and market-fit recommendations — not final legal or print-ready compliance documents. Verify with regulatory counsel for your target market before production.
        </p>
      </div>
    </section>

    <!-- ===== FINAL CTA ===== -->
    <section class="py-24 lg:py-32 bg-primary-black text-ice-white">
      <div class="max-w-4xl mx-auto px-6 lg:px-10 text-center">
        <h2 class="font-display text-4xl lg:text-6xl tracking-tight font-medium leading-tight">
          Ready to adapt your product
          <span class="block">for a <span class="text-electric-violet">new market</span>?</span>
        </h2>
        <p class="mt-6 text-lg text-ice-white/70 max-w-2xl mx-auto leading-relaxed">
          Start with the target country, product style, tier, and buyer type. We handle the localization logic from there.
        </p>
        <div class="mt-10">
          <a
            href="#configurator"
            class="group inline-flex items-center gap-2 bg-ice-white text-primary-black px-7 py-4 text-base font-semibold rounded-md hover:bg-electric-violet hover:text-ice-white transition-colors"
          >
            Create market-ready label
            <span class="text-base leading-none transition-transform group-hover:translate-x-0.5">→</span>
          </a>
        </div>
      </div>
    </section>

    <!-- ===== FOOTER ===== -->
    <footer class="bg-primary-black border-t border-ice-white/10">
      <div class="max-w-7xl mx-auto px-6 lg:px-10 py-10 flex flex-col md:flex-row items-center justify-between gap-4">
        <img src="../assets/logo/oramaintel-small.png" alt="ORAMA INTEL" class="h-5 w-auto" style="filter: invert(1)" />
        <p class="text-xs font-mono tracking-wider text-ice-white/50">
          © 2026 ORAMA INTEL · Market-fit intelligence for export brands
        </p>
      </div>
    </footer>

    <!-- ===== UPLOAD MODAL ===== -->
    <Transition name="fade">
      <div v-if="uploadOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4" role="dialog" aria-modal="true">
        <div class="absolute inset-0 bg-primary-black/60 backdrop-blur-sm" @click="closeUpload"></div>

        <div
          :class="[
            'relative bg-white rounded-2xl shadow-2xl w-full p-8 border border-black/8 max-h-[90vh] overflow-y-auto transition-[max-width] duration-300',
            analysisState === 'result' ? 'max-w-2xl' : 'max-w-lg',
          ]"
        >
          <button
            @click="closeUpload"
            class="absolute top-4 right-4 w-8 h-8 rounded-full hover:bg-black/5 flex items-center justify-center text-graphite/60 z-10"
            aria-label="Close"
          >
            ×
          </button>

          <!-- ===== IDLE: UPLOAD FORM ===== -->
          <div v-if="analysisState === 'idle'">
            <div class="font-mono text-[10px] tracking-widest text-signal-purple mb-2">CONFIRM DETAILS</div>
            <h3 class="font-display text-2xl text-primary-black font-medium tracking-tight">
              Add product details
            </h3>
            <p class="mt-2 text-sm text-graphite/70">
              We'll run the 8-agent analysis on the file you uploaded.
            </p>

            <!-- File already attached (typical case — user uploaded from the homepage) -->
            <div
              v-if="selectedFile"
              class="mt-5 flex items-center gap-3 px-4 py-3 rounded-lg border border-market-green/40 bg-market-green/5"
            >
              <span class="flex-shrink-0 w-8 h-8 rounded-md bg-market-green text-ice-white text-sm flex items-center justify-center font-mono">✓</span>
              <div class="min-w-0 flex-1">
                <div class="font-mono text-[10px] tracking-widest text-market-green mb-0.5">ATTACHED</div>
                <p class="text-sm font-medium text-primary-black truncate">{{ selectedFile.name }}</p>
                <p class="text-[11px] text-graphite/55">{{ formatBytes(selectedFile.size) }}</p>
              </div>
              <label class="flex-shrink-0 font-mono text-[10px] tracking-widest text-graphite/55 hover:text-signal-purple cursor-pointer transition-colors">
                <input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg,.webp"
                  class="hidden"
                  @change="handleFile"
                />
                ↻ REPLACE
              </label>
            </div>

            <!-- Fallback dropzone (rare — user opened modal without first uploading on hero) -->
            <label
              v-else
              :class="[
                'mt-5 block border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors',
                dragOver
                  ? 'border-signal-purple bg-signal-purple/5'
                  : 'border-black/15 hover:border-signal-purple/50 hover:bg-signal-purple/[0.03]',
              ]"
              @dragover.prevent="dragOver = true"
              @dragleave.prevent="dragOver = false"
              @drop.prevent="handleDrop"
            >
              <input
                ref="fileInputRef"
                type="file"
                accept=".pdf,.png,.jpg,.jpeg,.webp"
                class="hidden"
                @change="handleFile"
              />
              <div class="w-8 h-8 mx-auto mb-2 rounded-full border-2 border-graphite/30 flex items-center justify-center text-graphite/50 text-sm">↑</div>
              <p class="text-sm font-medium text-primary-black">Drop your label here</p>
              <p class="text-[11px] text-graphite/55 mt-1">PDF, PNG, JPG, or WEBP · max 15&nbsp;MB</p>
            </label>

            <div class="mt-5 space-y-3">
              <input
                v-model="productName"
                type="text"
                placeholder="Product name"
                class="w-full px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite placeholder:text-graphite/40 focus:outline-none focus:border-signal-purple"
              />

              <div class="grid grid-cols-2 gap-3">
                <select v-model="category" class="px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                  <option value="">Product category</option>
                  <option>Supplement</option>
                  <option>Beverage</option>
                  <option>Food</option>
                  <option>Snack</option>
                  <option>Sauce / condiment</option>
                  <option>Functional food</option>
                  <option>Cosmetic / personal care</option>
                  <option>Other</option>
                </select>
                <select v-model="country" class="px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                  <option value="">Target country</option>
                  <option>Japan</option>
                  <option>South Korea</option>
                  <option>EU</option>
                  <option>Germany</option>
                  <option>Nordics</option>
                  <option>USA</option>
                </select>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <select v-model="brandType" class="px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                  <option>Own brand</option>
                  <option>Private label</option>
                  <option>White label</option>
                  <option>Distributor / importer brand</option>
                  <option>Retailer brand</option>
                </select>
                <select v-model="visualStyleMode" class="px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                  <option>Keep current brand style</option>
                  <option>Clean Premium</option>
                  <option>Stylish Premium</option>
                  <option>Bold Retail</option>
                  <option>Clinical / Scientific</option>
                  <option>Natural / Organic</option>
                  <option>Luxury Minimal</option>
                  <option>Trend-led / D2C</option>
                </select>
              </div>
              <p class="text-[11px] text-graphite/55 leading-snug">
                Private label is treated as a <strong class="font-medium">brand type</strong>, not a product category.
                Style mode controls whether the adaptation is clean, bold, clinical, natural, luxury, or visually expressive.
              </p>

              <div class="grid grid-cols-2 gap-3">
                <select v-model="currentMarket" class="px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                  <option value="">Current market</option>
                  <option>Norway</option>
                  <option>Sweden</option>
                  <option>Denmark</option>
                  <option>Germany</option>
                  <option>USA</option>
                  <option>South Korea</option>
                  <option>Japan</option>
                  <option>Other</option>
                </select>
                <select v-model="targetChannel" class="px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                  <option value="supermarket">Channel: Supermarket</option>
                  <option value="pharmacy">Channel: Pharmacy</option>
                  <option value="convenience">Channel: Convenience</option>
                  <option value="amazon">Channel: Amazon / e-com</option>
                  <option value="specialty">Channel: Specialty</option>
                  <option value="b2b">Channel: B2B / distributor</option>
                </select>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <select v-model="targetBuyer" class="px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                  <option value="mass">Buyer: Mass</option>
                  <option value="premium">Buyer: Premium</option>
                  <option value="health-conscious">Buyer: Health-conscious</option>
                  <option value="athletes">Buyer: Athletes</option>
                  <option value="parents">Buyer: Parents</option>
                  <option value="elderly">Buyer: Elderly</option>
                  <option value="gen-z">Buyer: Gen Z</option>
                  <option value="tourists">Buyer: Tourists</option>
                  <option value="business">Buyer: Business / B2B</option>
                </select>
                <select v-model="priceTier" class="px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                  <option value="budget">Tier: Budget</option>
                  <option value="mainstream">Tier: Mainstream</option>
                  <option value="premium">Tier: Premium</option>
                  <option value="luxury">Tier: Luxury</option>
                </select>
              </div>

              <select v-model="brandGoal" class="w-full px-3 py-2.5 bg-white border border-black/10 rounded-md text-sm text-graphite focus:outline-none focus:border-signal-purple">
                <option value="trust">Brand goal: Trust</option>
                <option value="premium">Brand goal: Premium</option>
                <option value="functional">Brand goal: Functional</option>
                <option value="natural">Brand goal: Natural</option>
                <option value="fun">Brand goal: Fun</option>
                <option value="clinical">Brand goal: Clinical</option>
                <option value="local">Brand goal: Local</option>
                <option value="export">Brand goal: Export-ready</option>
              </select>

              <details class="border border-black/[0.08] rounded-md group">
                <summary class="px-3 py-2 text-xs text-graphite/70 cursor-pointer select-none flex items-center justify-between">
                  <span>More details (optional)</span>
                  <span class="text-graphite/40 group-open:rotate-90 transition-transform">›</span>
                </summary>
                <div class="px-3 pb-3 space-y-3">
                  <textarea
                    v-model="claimsOnPack"
                    rows="2"
                    placeholder="Claims on pack — one per line"
                    class="w-full px-3 py-2 bg-ice-white border border-black/10 rounded-md text-xs text-graphite placeholder:text-graphite/40 focus:outline-none focus:border-signal-purple resize-none"
                  />
                  <textarea
                    v-model="ingredientsText"
                    rows="2"
                    placeholder="Ingredient list — comma separated"
                    class="w-full px-3 py-2 bg-ice-white border border-black/10 rounded-md text-xs text-graphite placeholder:text-graphite/40 focus:outline-none focus:border-signal-purple resize-none"
                  />
                  <input
                    v-model="countryOfOrigin"
                    type="text"
                    placeholder="Country of origin"
                    class="w-full px-3 py-2 bg-ice-white border border-black/10 rounded-md text-xs text-graphite placeholder:text-graphite/40 focus:outline-none focus:border-signal-purple"
                  />
                </div>
              </details>
            </div>

            <button
              @click="runAnalysis"
              :disabled="!canSubmitAnalysis"
              class="mt-6 w-full inline-flex items-center justify-center gap-2 bg-primary-black text-ice-white px-5 py-3 text-sm font-semibold rounded-md hover:bg-signal-purple disabled:bg-graphite/30 disabled:cursor-not-allowed transition-colors"
            >
              Run market-fit analysis
              <span class="text-base leading-none">→</span>
            </button>

            <p class="mt-4 text-xs text-graphite/50 text-center">
              Free score · No card required for the first analysis.
            </p>
          </div>

          <!-- ===== ANALYZING ===== -->
          <div v-else-if="analysisState === 'analyzing'" class="py-6">
            <div class="font-mono text-[10px] tracking-widest text-signal-purple mb-2">ANALYZING</div>
            <h3 class="font-display text-2xl text-primary-black font-medium tracking-tight">
              Reading your label
            </h3>
            <p class="mt-2 text-sm text-graphite/70">
              {{ category }} · target market: {{ country }}
            </p>

            <div class="mt-8">
              <div class="h-1 rounded-full bg-graphite/10 overflow-hidden">
                <div class="h-full bg-signal-purple transition-[width] duration-300 ease-linear" :style="{ width: analysisProgress + '%' }"></div>
              </div>
              <div class="mt-2 flex items-center justify-between">
                <span class="font-mono text-[10px] tracking-widest text-graphite/50">{{ analysisStep }}</span>
                <span class="font-mono text-[10px] tracking-widest text-signal-purple tabular-nums">{{ analysisProgress }}%</span>
              </div>
            </div>

            <ul class="mt-8 space-y-2.5">
              <li v-for="(s, i) in analysisSteps" :key="s" class="flex items-center gap-3 text-sm">
                <span
                  :class="[
                    'w-4 h-4 rounded-full flex items-center justify-center flex-shrink-0 transition-colors',
                    i < currentStepIndex ? 'bg-market-green text-ice-white' : i === currentStepIndex ? 'bg-signal-purple text-ice-white' : 'bg-graphite/10 text-graphite/40',
                  ]"
                >
                  <span v-if="i < currentStepIndex" class="text-[10px]">✓</span>
                  <span v-else-if="i === currentStepIndex" class="w-1.5 h-1.5 rounded-full bg-ice-white animate-pulse"></span>
                </span>
                <span :class="i <= currentStepIndex ? 'text-primary-black' : 'text-graphite/50'">{{ s }}</span>
              </li>
            </ul>
          </div>

          <!-- ===== RESULT ===== -->
          <div v-else-if="analysisState === 'result' && result">
            <div class="flex items-center justify-between mb-3">
              <div class="font-mono text-[10px] tracking-widest text-signal-purple">MARKET-FIT REPORT</div>
              <button
                @click="resetAnalysis"
                class="font-mono text-[10px] tracking-widest text-graphite/50 hover:text-primary-black transition-colors"
              >
                ↺ NEW ANALYSIS
              </button>
            </div>

            <h3 class="font-display text-2xl text-primary-black font-medium tracking-tight">
              {{ result.category }} <span class="text-graphite/30">→</span> {{ result.country }}
            </h3>
            <p class="mt-1 text-sm text-graphite/60 break-all">
              {{ result.fileName }}
            </p>

            <div v-if="analysisFallback" class="mt-3 px-3 py-2 rounded-md bg-warning-amber/5 border border-warning-amber/30 text-[11px] text-graphite/80 flex items-start gap-2">
              <span class="text-warning-amber">⚠</span>
              <span>
                <strong class="font-semibold">{{ analysisFallbackReason }}</strong> — showing cached signals instead of live analysis.
              </span>
            </div>

            <p v-if="result.summary" class="mt-3 text-sm text-graphite/80 leading-relaxed">
              {{ result.summary }}
            </p>

            <!-- Score banner -->
            <div class="mt-6 grid grid-cols-12 gap-4 items-center p-5 rounded-xl bg-gradient-to-br from-signal-purple/5 to-electric-violet/5 border border-signal-purple/15">
              <div class="col-span-5">
                <div class="font-mono text-[10px] text-graphite/55 tracking-widest">MARKET FIT SCORE</div>
                <div class="flex items-baseline gap-1 mt-1">
                  <span class="font-display text-5xl font-medium text-primary-black tracking-tight tabular-nums">{{ result.fit }}</span>
                  <span class="font-mono text-sm text-graphite/40">/100</span>
                </div>
                <div :class="[
                  'mt-1 inline-flex items-center gap-1.5 font-mono text-[10px] tracking-widest',
                  result.fit >= 80 ? 'text-market-green' : result.fit >= 65 ? 'text-warning-amber' : 'text-risk-red',
                ]">
                  <span class="w-1.5 h-1.5 rounded-full" :class="result.fit >= 80 ? 'bg-market-green' : result.fit >= 65 ? 'bg-warning-amber' : 'bg-risk-red'"></span>
                  {{ result.fit >= 80 ? 'STRONG FIT' : result.fit >= 65 ? 'NEEDS WORK' : 'HIGH FRICTION' }}
                </div>
              </div>
              <div class="col-span-7 grid grid-cols-2 gap-2">
                <div v-for="sub in result.subScores" :key="sub.label" class="border border-black/[0.06] bg-white rounded-md px-3 py-2">
                  <div class="flex items-center justify-between">
                    <span class="text-[11px] text-graphite/70">{{ sub.label }}</span>
                    <span class="font-mono text-[11px] font-semibold" :class="subColor(sub.value)">
                      {{ typeof sub.value === 'number' ? sub.value : sub.value }}
                    </span>
                  </div>
                  <div class="mt-1.5 h-1 rounded-full bg-graphite/10 overflow-hidden">
                    <div class="h-full" :class="subBarColor(sub.value)" :style="{ width: subBarWidth(sub.value) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Warnings -->
            <div class="mt-5 rounded-lg bg-warning-amber/5 border border-warning-amber/20 p-4">
              <div class="font-mono text-[10px] text-warning-amber tracking-widest mb-2 flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-warning-amber"></span>
                KEY RISKS · {{ result.warnings.length }}
              </div>
              <ul class="space-y-2 text-sm text-graphite/90">
                <li v-for="(w, i) in result.warnings" :key="i" class="flex gap-2.5">
                  <span class="text-warning-amber mt-0.5">›</span>
                  <span>{{ w }}</span>
                </li>
              </ul>
            </div>

            <!-- Improvements -->
            <div class="mt-3 rounded-lg bg-market-green/5 border border-market-green/20 p-4">
              <div class="font-mono text-[10px] text-market-green tracking-widest mb-2 flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 rounded-full bg-market-green"></span>
                RECOMMENDED MOVES · {{ result.improvements.length }}
              </div>
              <ul class="space-y-2 text-sm text-graphite/90">
                <li v-for="(im, i) in result.improvements" :key="i" class="flex gap-2.5">
                  <span class="text-market-green mt-0.5">+</span>
                  <span>{{ im }}</span>
                </li>
              </ul>
            </div>

            <!-- Market reference signals -->
            <div
              v-if="result.marketReferences && (result.marketReferences.referenceProducts.length || result.marketReferences.commonClaims.length)"
              class="mt-5 p-5 rounded-xl border border-signal-purple/20 bg-signal-purple/[0.03]"
            >
              <div class="flex items-center justify-between mb-3">
                <div class="font-mono text-[10px] text-signal-purple tracking-widest">MARKET REFERENCE SIGNALS</div>
                <span class="font-mono text-[9px] tracking-widest text-graphite/45">
                  {{ result.marketReferences.source === 'mock' || result.marketReferences.source === 'mock-fallback'
                    ? 'SAMPLE INTELLIGENCE'
                    : 'LIVE' }}
                </span>
              </div>
              <p class="text-[11px] text-graphite/60 mb-4 italic leading-relaxed">
                Reference-based market analysis using sample market intelligence — not a live scrape of retailer catalogues.
              </p>

              <div class="grid sm:grid-cols-2 gap-4">
                <div v-if="result.marketReferences.commonClaims.length">
                  <div class="font-mono text-[10px] text-graphite/55 tracking-widest mb-2">COMMON CATEGORY PATTERNS</div>
                  <ul class="space-y-1.5 text-sm text-graphite/85">
                    <li v-for="c in result.marketReferences.commonClaims" :key="c" class="flex gap-2">
                      <span class="text-signal-purple">·</span><span>{{ c }}</span>
                    </li>
                  </ul>
                </div>
                <div v-if="result.marketReferences.commonTrustMarkers.length">
                  <div class="font-mono text-[10px] text-graphite/55 tracking-widest mb-2">TRUST MARKERS IN MARKET</div>
                  <ul class="space-y-1.5 text-sm text-graphite/85">
                    <li v-for="t in result.marketReferences.commonTrustMarkers" :key="t" class="flex gap-2">
                      <span class="text-market-green">✓</span><span>{{ t }}</span>
                    </li>
                  </ul>
                </div>
                <div v-if="result.marketReferences.overusedPatterns.length">
                  <div class="font-mono text-[10px] text-warning-amber tracking-widest mb-2">OVERUSED CLICHÉS TO AVOID</div>
                  <ul class="space-y-1.5 text-sm text-graphite/85">
                    <li v-for="o in result.marketReferences.overusedPatterns" :key="o" class="flex gap-2">
                      <span class="text-warning-amber">⚠</span><span>{{ o }}</span>
                    </li>
                  </ul>
                </div>
                <div v-if="result.marketReferences.differentiationOpportunities.length">
                  <div class="font-mono text-[10px] text-market-green tracking-widest mb-2">DIFFERENTIATION OPPORTUNITIES</div>
                  <ul class="space-y-1.5 text-sm text-graphite/85">
                    <li v-for="d in result.marketReferences.differentiationOpportunities" :key="d" class="flex gap-2">
                      <span class="text-market-green">+</span><span>{{ d }}</span>
                    </li>
                  </ul>
                </div>
              </div>

              <div v-if="result.marketReferences.adaptationImplications.length" class="mt-4 pt-4 border-t border-signal-purple/15">
                <div class="font-mono text-[10px] text-signal-purple tracking-widest mb-2">WHAT THIS MEANS FOR YOUR LABEL</div>
                <ul class="space-y-1.5 text-sm text-graphite/90">
                  <li v-for="i in result.marketReferences.adaptationImplications" :key="i" class="flex gap-2">
                    <span class="text-signal-purple">→</span><span>{{ i }}</span>
                  </li>
                </ul>
              </div>

              <details v-if="result.marketReferences.referenceProducts.length" class="mt-4 pt-4 border-t border-signal-purple/15 group">
                <summary class="font-mono text-[10px] text-graphite/55 tracking-widest cursor-pointer flex items-center justify-between select-none">
                  <span>SAMPLE REFERENCE PRODUCTS ({{ result.marketReferences.referenceProducts.length }})</span>
                  <span class="text-graphite/40 group-open:rotate-90 transition-transform">›</span>
                </summary>
                <div class="mt-3 space-y-3">
                  <div v-for="rp in result.marketReferences.referenceProducts" :key="rp.brandName + rp.productName" class="p-3 rounded-md border border-black/[0.06] bg-white">
                    <div class="flex items-center justify-between mb-1">
                      <div class="font-semibold text-sm text-primary-black">{{ rp.brandName }}</div>
                      <span class="font-mono text-[9px] tracking-widest text-graphite/50">{{ (rp.priceTier || '').toUpperCase() }} · {{ (rp.sourceType || '').toUpperCase() }}</span>
                    </div>
                    <div class="text-xs text-graphite/70 mb-2">{{ rp.productName }}</div>
                    <div class="text-[11px] text-graphite/65 leading-relaxed">
                      <strong class="text-graphite/85">Claims:</strong> {{ (rp.visibleClaims || []).slice(0,3).join(' · ') }}
                    </div>
                    <div v-if="rp.colorPalette && rp.colorPalette.length" class="flex items-center gap-1.5 mt-2">
                      <span v-for="hex in rp.colorPalette.slice(0,4)" :key="hex" class="w-4 h-4 rounded border border-black/10" :style="{ backgroundColor: hex }"></span>
                      <span class="font-mono text-[9px] text-graphite/45 ml-1">{{ rp.colorPalette.slice(0,4).join(' · ') }}</span>
                    </div>
                  </div>
                </div>
              </details>
            </div>

            <!-- Recommended copy from the brief (free) -->
            <div v-if="result.copy" class="mt-5 p-5 rounded-xl border border-black/[0.08] bg-white">
              <div class="font-mono text-[10px] text-graphite/55 tracking-widest mb-2">RECOMMENDED COPY</div>
              <div class="font-display text-xl text-primary-black font-semibold leading-snug">{{ result.copy.frontLabelHeadline }}</div>
              <div class="mt-1 text-sm text-graphite/70">{{ result.copy.subheadline }}</div>
              <div v-if="result.copy.trustMarkers && result.copy.trustMarkers.length" class="mt-3 pt-3 border-t border-black/[0.06]">
                <div class="font-mono text-[10px] text-graphite/55 tracking-widest mb-1.5">TRUST MARKERS</div>
                <ul class="text-sm text-graphite/85 space-y-1">
                  <li v-for="t in result.copy.trustMarkers.slice(0,4)" :key="t" class="flex gap-2">
                    <span class="text-signal-purple">›</span><span>{{ t }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Palette (free) -->
            <div v-if="result.palette && result.palette.primary" class="mt-5 p-5 rounded-xl border border-black/[0.08] bg-white">
              <div class="font-mono text-[10px] text-graphite/55 tracking-widest mb-3">PALETTE DIRECTION</div>
              <div class="grid grid-cols-5 gap-2">
                <div v-for="(hex, name) in result.palette" :key="name" class="flex flex-col">
                  <div class="aspect-square rounded-md border border-black/[0.06]" :style="{ backgroundColor: hex }"></div>
                  <div class="mt-1.5 font-mono text-[9px] tracking-widest text-graphite/70 truncate">{{ name }}</div>
                  <div class="font-mono text-[9px] text-graphite/40 tabular-nums">{{ hex }}</div>
                </div>
              </div>
            </div>

            <!-- Hierarchy (free) -->
            <div v-if="result.hierarchy && result.hierarchy.length" class="mt-5 p-5 rounded-xl border border-black/[0.08] bg-white">
              <div class="font-mono text-[10px] text-graphite/55 tracking-widest mb-3">HIERARCHY · TOP TO BOTTOM</div>
              <ol class="space-y-2">
                <li v-for="(h, i) in result.hierarchy" :key="i" class="flex gap-3 text-sm text-graphite/90">
                  <span class="font-mono text-[10px] font-semibold text-signal-purple tabular-nums w-5 pt-0.5 flex-shrink-0">{{ String(i + 1).padStart(2, '0') }}</span>
                  <span>{{ h }}</span>
                </li>
              </ol>
            </div>

            <!-- Mockup generation (paid step) -->
            <div v-if="mockupState === 'idle'" class="mt-6 p-5 rounded-xl bg-primary-black text-ice-white">
              <div class="font-mono text-[10px] tracking-widest text-electric-violet">UNLOCK MOCKUP</div>
              <h4 class="mt-1 font-display text-lg font-semibold">Generate an AI label adaptation concept</h4>
              <p class="mt-1 text-xs text-ice-white/65">AI-generated label adaptation concept · €149 per product/market</p>

              <label class="mt-4 flex items-start gap-3 rounded-lg border border-ice-white/15 bg-ice-white/5 p-3 text-sm cursor-pointer hover:bg-ice-white/[0.07] transition-colors">
                <input
                  type="checkbox"
                  v-model="labelOnlyMode"
                  class="mt-0.5 h-4 w-4 accent-electric-violet cursor-pointer"
                />
                <span class="flex-1">
                  <span class="block font-medium text-ice-white">Preserve package shape — change label only</span>
                  <span class="block mt-1 text-[11px] text-ice-white/55 leading-snug">
                    ORAMA INTEL keeps your existing packaging format and adapts only the label artwork for the target market.
                  </span>
                </span>
              </label>

              <button
                @click="generateMockup"
                class="mt-4 w-full inline-flex items-center justify-center gap-2 bg-ice-white text-primary-black px-5 py-2.5 text-sm font-semibold rounded-md hover:bg-electric-violet hover:text-ice-white transition-colors"
              >
                Generate label adaptation
                <span class="text-base leading-none">→</span>
              </button>
            </div>

            <div v-else-if="mockupState === 'generating'" class="mt-6 p-5 rounded-xl bg-primary-black text-ice-white">
              <div class="font-mono text-[10px] tracking-widest text-electric-violet">GENERATING MOCKUP</div>
              <h4 class="mt-1 font-display text-lg font-semibold">Rendering market-adapted concept</h4>
              <div class="mt-4 h-1 rounded-full bg-ice-white/15 overflow-hidden">
                <div class="h-full bg-electric-violet transition-[width] duration-300 ease-linear" :style="{ width: mockupProgress + '%' }"></div>
              </div>
              <div class="mt-2 flex items-center justify-between text-[10px] font-mono tracking-widest">
                <span class="text-ice-white/55">{{ mockupStep }}</span>
                <span class="text-electric-violet tabular-nums">{{ mockupProgress }}%</span>
              </div>
            </div>

            <div v-else-if="mockupState === 'done'" class="mt-6">
              <div class="flex items-center justify-between mb-3">
                <div class="font-mono text-[10px] tracking-widest text-electric-violet">{{ labelOnlyMode ? 'LABEL ADAPTATION CONCEPT' : 'PACKAGING MOCKUP' }}</div>
                <span v-if="mockupIsMock" class="font-mono text-[10px] tracking-widest text-warning-amber flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-warning-amber"></span>
                  PLACEHOLDER
                </span>
                <span v-else class="font-mono text-[10px] tracking-widest text-market-green flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-market-green"></span>
                  AI-GENERATED
                </span>
              </div>

              <div v-if="mockupError" class="mb-3 px-3 py-2 rounded-md bg-warning-amber/5 border border-warning-amber/30 text-[11px] text-graphite/80 flex items-start gap-2">
                <span class="text-warning-amber">⚠</span>
                <span><strong class="font-semibold">{{ mockupError }}</strong> — showing a placeholder until the real image engine is reachable.</span>
              </div>

              <div v-if="mockupImage" class="relative rounded-xl overflow-hidden border border-black/[0.08] bg-graphite/[0.04]">
                <img
                  :src="`data:image/png;base64,${mockupImage}`"
                  :class="[
                    'w-full h-auto block transition-[filter] duration-300',
                    (devUnlocked || mockupUnlocked) ? 'filter-none' : 'filter blur-md scale-[1.02]',
                  ]"
                  alt="AI-generated label adaptation concept"
                />
                <!-- Locked overlay -->
                <div
                  v-if="!devUnlocked && !mockupUnlocked"
                  class="absolute inset-0 flex flex-col items-center justify-center bg-primary-black/55 backdrop-blur-[2px] text-center p-6"
                >
                  <div class="font-mono text-[10px] tracking-widest text-electric-violet mb-2">PAID UPGRADE</div>
                  <h5 class="font-display text-xl text-ice-white font-semibold leading-snug max-w-xs">
                    Unlock the market-adapted mockup
                  </h5>
                  <p class="mt-2 text-xs text-ice-white/75 max-w-xs">
                    €299 per product / market · Full-resolution export-ready concept image.
                  </p>
                  <button
                    @click="unlockMockup"
                    class="mt-5 inline-flex items-center gap-2 bg-ice-white text-primary-black px-5 py-2.5 text-sm font-semibold rounded-md hover:bg-electric-violet hover:text-ice-white transition-colors"
                  >
                    Unlock for €299
                    <span class="text-base leading-none">→</span>
                  </button>
                  <button
                    @click="unlockMockup"
                    class="mt-3 font-mono text-[10px] tracking-widest text-ice-white/40 hover:text-ice-white/80 transition-colors"
                  >
                    ↺ DEV: PREVIEW
                  </button>
                </div>
              </div>

              <p v-if="(devUnlocked || mockupUnlocked) && mockupImage" class="mt-3 text-[11px] text-graphite/55 leading-relaxed">
                AI-generated label adaptation concept — not a final print-ready file. Verify claims, certifications, and ingredient panel with your regulatory team before production.
              </p>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// In production (Vercel/Railway), VITE_API_BASE points at the backend service
// (e.g. "https://seeus-backend.up.railway.app"). In dev it's empty, so
// relative "/api/..." URLs hit Vite's proxy → localhost:5001.
const API_BASE = import.meta.env.VITE_API_BASE || ''

// ---- 4-step hero configurator (lightweight; pre-fills the upload modal) ----
const cfgTargetCountry = ref('')
const cfgProductStyle = ref('Clean premium')
const cfgTier = ref('premium')
const cfgBuyerType = ref('Food producer')
const cfgAdvancedDetails = ref('')

// Hero dropzone — shares selectedFile state with the modal so the file
// travels through to the analysis flow when the configurator is submitted.
const heroDragOver = ref(false)
const heroUploadError = ref('')
const MAX_HERO_FILE_BYTES = 15 * 1024 * 1024
const HERO_ACCEPTED_EXTS = ['pdf', 'png', 'jpg', 'jpeg', 'webp']

function _validateHeroFile(file) {
  const name = (file?.name || '').toLowerCase()
  const ext = name.includes('.') ? name.split('.').pop() : ''
  if (!HERO_ACCEPTED_EXTS.includes(ext)) {
    heroUploadError.value = 'This file type is not supported. Use PDF, PNG, JPG, or WEBP.'
    return false
  }
  if (file.size > MAX_HERO_FILE_BYTES) {
    heroUploadError.value = 'File is too large. Maximum size is 15 MB.'
    return false
  }
  heroUploadError.value = ''
  return true
}

function handleHeroFile(e) {
  const f = e.target.files?.[0]
  if (f && _validateHeroFile(f)) selectedFile.value = f
}

function handleHeroDrop(e) {
  heroDragOver.value = false
  const f = e.dataTransfer?.files?.[0]
  if (f && _validateHeroFile(f)) selectedFile.value = f
}

const tierOptions = [
  { id: 'starter',     name: 'Starter',     tagline: 'For early validation. Localized label direction + key wording.' },
  { id: 'premium',     name: 'Premium',     tagline: 'For serious launches. Full rewrite + positioning + risk notes.' },
  { id: 'launch_pack', name: 'Launch Pack', tagline: 'For sales / distributor outreach. Label + page copy + pitch.' },
]

// Map the lightweight product-style label to the canonical visual style mode.
const PRODUCT_STYLE_TO_STYLE_MODE = {
  'Clean premium':         'Clean Premium',
  'Nordic minimal':        'Luxury Minimal',
  'Modern retail':         'Bold Retail',
  'Natural / organic':     'Natural / Organic',
  'Scientific supplement': 'Clinical / Scientific',
  'Bold commercial':       'Bold Retail',
  'Custom style':          'Keep current brand style',
}

// Map the lightweight buyer-type label to (brandType, productCategory).
const BUYER_TYPE_TO_FIELDS = {
  'Food producer':                { brandType: 'Own brand',                     category: 'Food' },
  'Supplement brand':             { brandType: 'Own brand',                     category: 'Supplement' },
  'Beverage company':             { brandType: 'Own brand',                     category: 'Beverage' },
  'Private label manufacturer':   { brandType: 'Private label',                 category: '' },
  'Distributor / importer':       { brandType: 'Distributor / importer brand',  category: '' },
  'Other':                        { brandType: 'Own brand',                     category: '' },
}

const TIER_TO_PRICE_TIER = {
  starter: 'mainstream',
  premium: 'premium',
  launch_pack: 'luxury',
}

function submitConfigurator() {
  if (!cfgTargetCountry.value) return
  // Pre-fill the existing upload modal with the configurator selections so
  // the user only has to add a label image + product name from there.
  country.value = cfgTargetCountry.value
  visualStyleMode.value = PRODUCT_STYLE_TO_STYLE_MODE[cfgProductStyle.value] || 'Keep current brand style'
  const buyerFields = BUYER_TYPE_TO_FIELDS[cfgBuyerType.value] || BUYER_TYPE_TO_FIELDS['Other']
  brandType.value = buyerFields.brandType
  if (buyerFields.category) category.value = buyerFields.category
  priceTier.value = TIER_TO_PRICE_TIER[cfgTier.value] || 'premium'
  if (cfgAdvancedDetails.value && !claimsOnPack.value) {
    claimsOnPack.value = cfgAdvancedDetails.value
  }
  openUpload()
}

const uploadOpen = ref(false)
const selectedFile = ref(null)
const productName = ref('')
const category = ref('Supplement')
const brandType = ref('Own brand')
const visualStyleMode = ref('Keep current brand style')
const country = ref('')
const currentMarket = ref('')
const targetChannel = ref('supermarket')
const targetBuyer = ref('mass')
const priceTier = ref('mainstream')
const brandGoal = ref('trust')
const claimsOnPack = ref('')
const ingredientsText = ref('')
const countryOfOrigin = ref('')
const dragOver = ref(false)
const fileInputRef = ref(null)

const canSubmitAnalysis = computed(
  () =>
    !!selectedFile.value &&
    !!productName.value.trim() &&
    !!category.value &&
    !!country.value
)

// Dev toggle: `?unlock=1` in the URL unlocks paid mockup state for demo.
const devUnlocked = ref(
  typeof window !== 'undefined' &&
    new URLSearchParams(window.location.search).get('unlock') === '1'
)
const mockupUnlocked = ref(false)

const indicator = ref({ left: 0, width: 0, visible: false })

const analysisState = ref('idle') // 'idle' | 'analyzing' | 'result'
const analysisProgress = ref(0)
const currentStepIndex = ref(0)
const result = ref(null)
const analysisFallback = ref(false)
const analysisFallbackReason = ref('')

// Mockup generation (paid step). Replaces the old "adaptation" text flow.
const mockupState = ref('idle') // 'idle' | 'generating' | 'done'
const mockupProgress = ref(0)
const mockupStepIndex = ref(0)
const mockupImage = ref(null) // base64 PNG string
const mockupIsMock = ref(false)
const mockupError = ref('')
// Default ON — preserves package shape / casing / cap / perspective and
// only adapts the printed label artwork.
const labelOnlyMode = ref(true)
const exportState = ref('idle') // 'idle' | 'preparing' | 'done'

const analysisSteps = [
  'Reading label · OCR + layout',
  'Mapping claims and benefits',
  'Scoring against market priors',
  'Drafting market-fit report',
]

const mockupSteps = [
  'Loading adaptation brief',
  'Composing visual concept',
  'Rendering packaging mockup',
  'Finalizing concept image',
]

const analysisStep = computed(() => analysisSteps[currentStepIndex.value] || analysisSteps[0])
const mockupStep = computed(() => mockupSteps[mockupStepIndex.value] || mockupSteps[0])

let analysisIntervalId = null
let analysisTimeoutId = null
let mockupIntervalId = null
let mockupTimeoutId = null

function clearAnalysisTimers() {
  if (analysisIntervalId) { clearInterval(analysisIntervalId); analysisIntervalId = null }
  if (analysisTimeoutId) { clearTimeout(analysisTimeoutId); analysisTimeoutId = null }
}

function clearMockupTimers() {
  if (mockupIntervalId) { clearInterval(mockupIntervalId); mockupIntervalId = null }
  if (mockupTimeoutId) { clearTimeout(mockupTimeoutId); mockupTimeoutId = null }
}

function updateIndicator(e) {
  const el = e.currentTarget
  const navEl = el.parentElement
  const rect = el.getBoundingClientRect()
  const navRect = navEl.getBoundingClientRect()
  indicator.value = {
    left: rect.left - navRect.left,
    width: rect.width,
    visible: true,
  }
}

function openUpload() {
  uploadOpen.value = true
}

function closeUpload() {
  uploadOpen.value = false
  clearAnalysisTimers()
  clearMockupTimers()
  setTimeout(() => {
    analysisState.value = 'idle'
    analysisProgress.value = 0
    currentStepIndex.value = 0
    mockupState.value = 'idle'
    mockupProgress.value = 0
    mockupStepIndex.value = 0
    mockupImage.value = null
    mockupUnlocked.value = false
    exportState.value = 'idle'
  }, 200)
}

function resetAnalysis() {
  clearAnalysisTimers()
  clearMockupTimers()
  analysisState.value = 'idle'
  analysisProgress.value = 0
  currentStepIndex.value = 0
  selectedFile.value = null
  result.value = null
  mockupState.value = 'idle'
  mockupProgress.value = 0
  mockupStepIndex.value = 0
  mockupImage.value = null
  mockupIsMock.value = false
  mockupError.value = ''
  mockupUnlocked.value = false
  exportState.value = 'idle'
}

function handleFile(e) {
  const f = e.target.files?.[0]
  if (f) selectedFile.value = f
}

function handleDrop(e) {
  dragOver.value = false
  const f = e.dataTransfer.files?.[0]
  if (f) selectedFile.value = f
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

async function runAnalysis() {
  clearAnalysisTimers()
  analysisState.value = 'analyzing'
  analysisProgress.value = 0
  currentStepIndex.value = 0
  analysisFallback.value = false
  analysisFallbackReason.value = ''

  // Visual progress runs against an expected ceiling; the real call may
  // finish earlier or later. Cap at 95% until the response arrives.
  const expectedDuration = 6000
  const start = performance.now()
  analysisIntervalId = setInterval(() => {
    const elapsed = performance.now() - start
    const pct = Math.min(95, Math.floor((elapsed / expectedDuration) * 100))
    analysisProgress.value = pct
    currentStepIndex.value = Math.min(
      analysisSteps.length - 1,
      Math.floor((elapsed / expectedDuration) * analysisSteps.length)
    )
  }, 50)

  try {
    const form = new FormData()
    if (selectedFile.value) form.append('file', selectedFile.value)
    form.append('product_name', productName.value)
    form.append('product_category', category.value)
    form.append('brand_type', brandType.value)
    form.append('visual_style_mode', visualStyleMode.value)
    form.append('current_market', currentMarket.value)
    form.append('target_market', country.value)
    form.append('target_channel', targetChannel.value)
    form.append('target_buyer', targetBuyer.value)
    form.append('price_tier', priceTier.value)
    form.append('brand_goal', brandGoal.value)
    form.append('claims_on_pack', claimsOnPack.value)
    form.append('ingredients', ingredientsText.value)
    form.append('country_of_origin', countryOfOrigin.value)

    const resp = await fetch(`${API_BASE}/api/label/analyze`, { method: 'POST', body: form })
    if (!resp.ok) {
      const errBody = await resp.json().catch(() => ({}))
      const err = new Error(errBody.error || `HTTP ${resp.status}`)
      err.status = resp.status
      throw err
    }
    const report = await resp.json()

    clearAnalysisTimers()
    analysisProgress.value = 100
    currentStepIndex.value = analysisSteps.length - 1
    result.value = mapReportToResult(report, selectedFile.value)
    analysisState.value = 'result'
  } catch (err) {
    console.warn('Live analysis failed, falling back to client-side mock:', err)
    clearAnalysisTimers()
    analysisProgress.value = 100
    currentStepIndex.value = analysisSteps.length - 1
    result.value = buildResult(category.value, country.value, selectedFile.value)
    analysisFallback.value = true
    analysisFallbackReason.value = err && err.message ? err.message : 'Backend unavailable'
    analysisState.value = 'result'
  }
}

function pickMarketReferenceView(report) {
  const refs = report.marketReferences || {}
  const cp = refs.commonPatterns || {}
  return {
    targetMarket: refs.targetMarket || report.product?.targetMarket || '',
    category: refs.category || report.product?.category || '',
    channel: refs.channel || '',
    source: refs.source || 'mock',
    referenceProducts: (refs.referenceProducts || []).slice(0, 4),
    commonClaims: (cp.claims || []).slice(0, 4),
    commonTrustMarkers: (cp.trustMarkers || []).slice(0, 4),
    overusedPatterns: (refs.overusedPatterns || []).slice(0, 4),
    differentiationOpportunities: (refs.whiteSpaceOpportunities || []).slice(0, 4),
    adaptationImplications: (refs.adaptationImplications || []).slice(0, 4),
  }
}

function mapReportToResult(report, file) {
  // Adapt the FinalReport shape from the backend into the structure our
  // existing result UI already renders (score / sub-scores / warnings /
  // improvements). The richer brief data hangs off result.brief.
  const subScores = [
    { label: 'Culture fit',     value: report.agentScores.cultureFit },
    { label: 'Trend fit',       value: report.agentScores.trendFit },
    { label: 'Claims safety',   value: claimsSafetyDisplay(report.agentScores.claimsSafety) },
    { label: 'Visual hierarchy', value: report.agentScores.visualHierarchy },
    { label: 'Design fit',      value: report.agentScores.designFit },
    { label: 'Competitive fit', value: report.agentScores.competitiveFit },
    { label: 'Buyer motivation', value: report.agentScores.buyerMotivation },
    { label: 'Export readiness', value: report.agentScores.exportReadiness },
  ]
  const warnings = (report.riskFlags || [])
    .filter(f => f.level && f.level !== 'green')
    .map(f => `${(f.phrase || '').trim()}${f.phrase ? ' — ' : ''}${f.issue || ''}`)
  return {
    category: report.product.category,
    country: report.product.targetMarket,
    fileName: file ? file.name : (report.product.name || 'label'),
    fit: report.overallMarketFitScore,
    subScores,
    warnings: warnings.length ? warnings : (report.priorityFixes || []),
    improvements: report.priorityFixes || [],
    summary: report.summary || '',
    positioning: report.recommendedPositioning || '',
    copy: report.recommendedLabelCopy || null,
    palette: report.recommendedPalette || null,
    hierarchy: report.recommendedHierarchy || [],
    brief: report.adaptationBrief || null,
    marketReferences: pickMarketReferenceView(report),
  }
}

function claimsSafetyDisplay(score) {
  if (typeof score !== 'number') return 'Medium'
  if (score >= 80) return 'Low'
  if (score >= 60) return 'Medium'
  return 'High'
}

function buildResult(cat, ctry, file) {
  const warnLib = {
    Japan: {
      Supplement: [
        'Functional ingredient quantification is unclear for pharmacy channel',
        'Trust markers feel too consumer-D2C for conservative Japanese wellness buyers',
        'Claims wording risks regulatory friction with PMDA-style scrutiny',
      ],
      Food: [
        'Allergen visibility doesn\'t meet expected hierarchy on Japanese shelves',
        'Premium cues lean Western — origin story should be more explicit',
        'Ingredient transparency below category norm for premium Japanese retail',
      ],
    },
    'South Korea': {
      Supplement: [
        'Claims aren\'t quantified — Korean D2C wellness buyers expect specific numbers',
        'Hierarchy buries the functional benefit below branding',
        'Visual feels too clinical for Korean lifestyle wellness positioning',
      ],
      Food: [
        'Functional benefit isn\'t front and center for Korean K-Health momentum',
        'Trust signals lean Western — local certifications would lift credibility',
        'Premium cues read flat against current Korean food design language',
      ],
    },
    EU: {
      Supplement: [
        'Claims wording may exceed EFSA-permitted health-claim language',
        'Allergen and ingredient disclosure formatting needs EU-standard layout',
        'Premium positioning relies on hype — clean, restrained tone fits EU better',
      ],
      Food: [
        'Nutrition declaration formatting doesn\'t match FIC Regulation expectations',
        'Origin and sustainability cues are missing — strong drivers in EU buyers',
        'Marketing claims are stronger than EU label-compliance allows',
      ],
    },
    Nordics: {
      Supplement: [
        'Tone reads as US-style hype — Nordic buyers prefer understated claims',
        'Sustainability and origin cues are missing — strong purchase drivers',
        'Functional benefit could be quantified rather than asserted',
      ],
      Food: [
        'Less hype, more provenance — origin story is buried',
        'Sustainability signaling is missing — table-stakes in this market',
        'Cleaner whitespace and restrained palette would lift premium read',
      ],
    },
    USA: {
      Supplement: [
        'FDA-style disclaimer language is missing for supplement claims',
        'Functional benefit hierarchy is buried below branding',
        'Trust markers don\'t match expected US D2C supplement category cues',
      ],
      Food: [
        'Nutrition panel placement doesn\'t hit US shelf-scan patterns',
        'Claims could be sharpened — US buyers respond to specific benefit framing',
        'Premium cues read European; brand could push more category-native signals',
      ],
    },
  }

  const improveLib = {
    Japan: [
      'Quantify the functional benefit with a single hero number',
      'Add a discrete origin / provenance line near the brand mark',
      'Soften superlative claims; lead with technical clarity',
    ],
    'South Korea': [
      'Move the functional benefit above the brand mark',
      'Add a measurable claim ("12g protein", "30-day supply")',
      'Introduce a lifestyle wellness cue — current label reads too clinical',
    ],
    EU: [
      'Adopt EFSA-compliant claim wording (replace assertive verbs)',
      'Restructure allergen list to expected EU layout',
      'Replace hype copy with one restrained credibility line',
    ],
    Nordics: [
      'Lead with origin and sustainability — bury hype claims',
      'Drop one tier of visual noise; whitespace lifts premium read',
      'Quantify benefit instead of asserting it',
    ],
    USA: [
      'Add a "*These statements have not been evaluated..." line',
      'Reorder visual hierarchy: function → brand → tagline',
      'Sharpen benefit copy with one specific, measurable claim',
    ],
  }

  const fallbackWarnings = [
    'Benefit hierarchy is unclear for the target market',
    'Premium cues are weak for the chosen category',
    'Claims should be softened for lower regulatory friction',
  ]

  const fallbackImprovements = [
    'Restructure benefit hierarchy with one hero claim',
    'Tighten claims wording for regulatory headroom',
    'Lift premium read with restraint and origin cues',
  ]

  const baseScore = 60 + ((cat.length * 7 + ctry.length * 11) % 26)
  const warnings = (warnLib[ctry] && warnLib[ctry][cat]) || fallbackWarnings
  const improvements = improveLib[ctry] || fallbackImprovements

  // Minimal brief stub so the mockup endpoint still works offline.
  const palette = {
    primary: '#0A0A0A', secondary: '#F8FAFC',
    accent: '#7C3AED', background: '#FFFFFF', warning: '#EF4444',
  }
  const brief = {
    productName: productName.value || '',
    category: cat,
    targetMarket: ctry,
    packageType: '',
    mustPreserve: [productName.value ? `Product name: ${productName.value}` : 'Product name'],
    claimsToAvoid: [],
    saferClaims: [],
    palette,
    designDirection: 'Single hero benefit, single trust strip, single regulatory line.',
    hierarchy: [
      'Quantified hero benefit', 'Product type', 'Brand mark',
      'Trust signal', 'Compliance line',
    ],
    styleConstraints: ['Restrained typography', 'No decorative pattern overlays'],
    forbiddenChanges: [
      'Do not invent certifications',
      'Do not invent medical claims',
      'Do not add ingredients not in the source label',
    ],
  }

  return {
    category: cat,
    country: ctry,
    fileName: file ? file.name : 'label.pdf',
    fit: baseScore,
    subScores: [
      { label: 'Trust', value: clamp(baseScore + 7) },
      { label: 'Shelf impact', value: clamp(baseScore - 6) },
      { label: 'Claims risk', value: baseScore >= 75 ? 'Low' : baseScore >= 60 ? 'Medium' : 'High' },
      { label: 'Cultural fit', value: clamp(baseScore - 1) },
    ],
    warnings,
    improvements,
    summary: 'Offline fallback — backend analyzer unavailable. Showing cached signals for this market.',
    positioning: '',
    copy: null,
    palette,
    hierarchy: brief.hierarchy,
    brief,
  }
}

function clamp(n) {
  return Math.max(35, Math.min(95, n))
}

async function generateMockup() {
  if (!result.value || !result.value.brief) return
  clearMockupTimers()
  mockupState.value = 'generating'
  mockupProgress.value = 0
  mockupStepIndex.value = 0
  mockupImage.value = null
  mockupIsMock.value = false
  mockupError.value = ''

  const expectedDuration = 10000
  const start = performance.now()
  mockupIntervalId = setInterval(() => {
    const elapsed = performance.now() - start
    const pct = Math.min(95, Math.floor((elapsed / expectedDuration) * 100))
    mockupProgress.value = pct
    mockupStepIndex.value = Math.min(
      mockupSteps.length - 1,
      Math.floor((elapsed / expectedDuration) * mockupSteps.length)
    )
  }, 60)

  try {
    const form = new FormData()
    form.append('brief', JSON.stringify(result.value.brief))
    form.append('label_only_mode', labelOnlyMode.value ? '1' : '0')
    // Send the original label so OpenAI's image-edit endpoint can preserve
    // the physical package shape (cup, bottle, pouch, etc.).
    if (selectedFile.value) {
      form.append('file', selectedFile.value)
    }
    const resp = await fetch(`${API_BASE}/api/label/generate-mockup`, {
      method: 'POST',
      body: form,
    })
    const data = await resp.json().catch(() => ({}))
    if (!resp.ok) {
      throw new Error(data.error || `HTTP ${resp.status}`)
    }
    clearMockupTimers()
    mockupProgress.value = 100
    mockupStepIndex.value = mockupSteps.length - 1
    mockupImage.value = data.image_b64 || null
    mockupIsMock.value = !!data.mock
    mockupError.value = data.error || ''
    mockupState.value = 'done'
  } catch (err) {
    console.warn('Mockup generation failed:', err)
    clearMockupTimers()
    mockupProgress.value = 100
    mockupStepIndex.value = mockupSteps.length - 1
    mockupImage.value = null
    mockupError.value = (err && err.message) || 'Mockup generation failed'
    mockupState.value = 'done'
  }
}

function unlockMockup() {
  mockupUnlocked.value = true
}

function buildAdaptation(cat, ctry) {
  const lib = {
    Nordics: {
      headline: 'Marine Collagen · Wild-caught Atlantic',
      subline: '10g per serving · 30-day supply',
      claim: 'Origin verified. Third-party tested. No added sugar.',
      palette: [
        { name: 'Bone white', hex: '#F5F2EC' },
        { name: 'Slate', hex: '#1F2937' },
        { name: 'Sea grey', hex: '#4A5568' },
        { name: 'Birch', hex: '#C9C2B3' },
      ],
      hierarchy: [
        'Origin / provenance line',
        'Product type · single line',
        'Quantified benefit (single hero number)',
        'Brand mark',
        'Allergen + regulatory line',
      ],
      note: 'Bury hype. Lead with where it\'s from and what\'s in it. Restraint reads premium in this market.',
    },
    USA: {
      headline: '30g Whey Isolate · Per Scoop',
      subline: 'Lab-verified · Third-party tested',
      claim: 'Pre-workout fuel for serious training.',
      palette: [
        { name: 'Stark white', hex: '#FFFFFF' },
        { name: 'Carbon', hex: '#050505' },
        { name: 'Power red', hex: '#DC2626' },
        { name: 'Trust blue', hex: '#1E40AF' },
      ],
      hierarchy: [
        'Quantified hero benefit',
        'Product type + specificity',
        'Brand mark',
        'Third-party / trust badge',
        'FDA disclaimer line',
      ],
      note: 'Lead with measurable benefit. Sharpen claim copy. US D2C rewards specificity over restraint.',
    },
    Japan: {
      headline: 'Pharmacy-Grade Supplement · 1日1粒',
      subline: '30-day supply · Third-party verified',
      claim: 'Quantified wellness. Technical precision.',
      palette: [
        { name: 'Paper white', hex: '#FAFAF7' },
        { name: 'Sumi black', hex: '#1A1A1A' },
        { name: 'Indigo', hex: '#2C3E50' },
        { name: 'Verified', hex: '#2E8B57' },
      ],
      hierarchy: [
        'Pharmacy-grade seal',
        'Quantified ingredient amount',
        'Daily-dose clarity',
        'Brand mark',
        'PMDA-aligned disclaimer',
      ],
      note: 'Technical precision over lifestyle. Quantify everything. Conservative typography signals trust.',
    },
    'South Korea': {
      headline: 'K-Wellness · 10g Functional Collagen',
      subline: 'Daily-use · 30-day supply',
      claim: 'Quantified beauty. Lab-tested.',
      palette: [
        { name: 'Cream', hex: '#FAF7F2' },
        { name: 'Soft black', hex: '#0A0A0A' },
        { name: 'Wellness rose', hex: '#F4C6CB' },
        { name: 'Lab green', hex: '#4ECDC4' },
      ],
      hierarchy: [
        'Lifestyle hero claim',
        'Quantified active ingredient',
        'K-Wellness category cue',
        'Brand mark',
        'Compliance / source line',
      ],
      note: 'Lifestyle wellness, not pharmacy. Specific quantification builds D2C trust in this market.',
    },
    EU: {
      headline: 'Marine Collagen Supplement',
      subline: '10g per serving · 30-day pack',
      claim: 'Source-verified. Third-party tested.',
      palette: [
        { name: 'Off-white', hex: '#F5F5F0' },
        { name: 'Compliance', hex: '#1A1A1A' },
        { name: 'Trust navy', hex: '#1E40AF' },
        { name: 'Verified seal', hex: '#2E8B57' },
      ],
      hierarchy: [
        'Product type · single line',
        'Quantified amount per serving',
        'Brand mark',
        'Full allergen panel',
        'EFSA-compliant claim line',
      ],
      note: 'Replace assertive verbs with EFSA-permitted phrasing. Restraint reads premium in EU retail.',
    },
  }

  return lib[ctry] || {
    headline: `${cat} · Optimized for ${ctry}`,
    subline: 'Quantified · Source-verified',
    claim: 'Functional benefit. Backed by testing.',
    palette: [
      { name: 'Ice white', hex: '#F8FAFC' },
      { name: 'Carbon', hex: '#050505' },
      { name: 'Signal', hex: '#7C3AED' },
      { name: 'Trust', hex: '#1E40AF' },
    ],
    hierarchy: [
      'Hero benefit',
      'Quantified claim',
      'Brand mark',
      'Trust signal',
      'Regulatory line',
    ],
    note: 'Lead with quantified benefit. Tighten claim copy for regulatory headroom.',
  }
}

function downloadReport() {
  exportState.value = 'preparing'
  setTimeout(() => {
    exportState.value = 'done'
  }, 1100)
}

function subColor(v) {
  if (typeof v === 'string') {
    return v === 'Low' ? 'text-market-green' : v === 'Medium' ? 'text-warning-amber' : 'text-risk-red'
  }
  return v >= 80 ? 'text-market-green' : v >= 65 ? 'text-warning-amber' : 'text-risk-red'
}

function subBarColor(v) {
  if (typeof v === 'string') {
    return v === 'Low' ? 'bg-market-green' : v === 'Medium' ? 'bg-warning-amber' : 'bg-risk-red'
  }
  return v >= 80 ? 'bg-market-green' : v >= 65 ? 'bg-warning-amber' : 'bg-risk-red'
}

function subBarWidth(v) {
  if (typeof v === 'string') {
    return v === 'Low' ? 30 : v === 'Medium' ? 55 : 80
  }
  return v
}

const navLinks = [
  { label: 'Product', href: '#product' },
  { label: 'How it works', href: '#how' },
  { label: 'Pricing', href: '#pricing' },
  { label: 'Examples', href: '#examples' },
]

const markets = ['Korea', 'Japan', 'EU', 'Nordics', 'USA']
const categories = ['Food', 'Beverage', 'Supplements', 'Private Label']

const howItWorks = [
  { title: 'Choose the market', body: 'Select the target country and product category.' },
  { title: 'Choose the positioning', body: 'Pick the style and launch tier that fits your product.' },
  { title: 'Receive a market-ready package', body: 'Localized label copy, positioning, and retail-facing messaging adapted for the market.' },
]

const audiences = [
  { title: 'Food producers', body: 'For companies launching new SKUs or adapting existing products to new markets.' },
  { title: 'Supplement companies', body: 'For brands that need clearer label wording, product claims structure, and premium positioning.' },
  { title: 'Beverage brands', body: 'For drinks, functional beverages, and wellness products entering new retail environments.' },
  { title: 'Private label manufacturers', body: 'For companies producing many SKUs where weak labeling reduces sell-through.' },
  { title: 'Distributors and importers', body: 'For teams evaluating whether a product is ready for a local market.' },
  { title: 'Export-ready teams', body: 'For brands moving from one market to several at once.' },
]

const engineCards = [
  { tag: 'A1', title: 'Market Fit Score' },
  { tag: 'A2', title: 'Trust & credibility score' },
  { tag: 'A3', title: 'Shelf impact score' },
  { tag: 'A4', title: 'Claims-risk review' },
  { tag: 'A5', title: 'Cultural fit analysis' },
  { tag: 'A6', title: 'Palette & hierarchy feedback' },
  { tag: 'A7', title: 'Competitor positioning' },
  { tag: 'A8', title: 'Auto-generated adaptation' },
]

const examples = [
  {
    from: 'Norway', to: 'Korea',
    points: ['More quantified benefits', 'Stronger functional hierarchy', 'Cleaner trust markers'],
  },
  {
    from: 'Japan', to: 'EU',
    points: ['Clearer ingredient transparency', 'Stronger allergen visibility', 'More premium whitespace'],
  },
  {
    from: 'USA', to: 'Nordics',
    points: ['Less hype', 'More sustainability and origin cues', 'Cleaner claims language'],
  },
]

const tiers = [
  {
    name: 'Starter',
    price: '€0',
    unit: '',
    description: 'For brands that want a first market-fit check.',
    badge: '',
    features: [
      'Upload one label',
      'Market-fit score',
      'Key risks and improvements',
      'Basic culture and shelf-impact feedback',
    ],
    cta: 'Create market-ready label',
    featured: false,
  },
  {
    name: 'Premium',
    price: '€149',
    unit: 'per product / market',
    description: 'For brands that want the fix, not just the feedback.',
    badge: 'Best for validation',
    features: [
      'Everything in Starter',
      'Improved label copy',
      'Palette and hierarchy direction',
      'AI-generated packaging mockup concept',
      'Market-specific adaptation brief',
    ],
    cta: 'Generate adaptation',
    featured: true,
  },
  {
    name: 'Launch Pack',
    price: '€499',
    unit: 'one target market',
    description: 'For teams testing multiple products or one target market seriously.',
    badge: '',
    features: [
      'Up to 3 products',
      'One target market',
      'Full market-fit report',
      'Mockup concepts for each product',
      'Distributor-ready summary',
    ],
    cta: 'Start pilot',
    featured: false,
  },
]
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
