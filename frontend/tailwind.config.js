/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  corePlugins: { preflight: false },
  theme: {
    extend: {
      colors: {
        'primary-black': '#050505',
        'ice-white': '#F8FAFC',
        'warm-cream': '#F1E7D5',
        'warm-tan': '#E5D5BD',
        'warm-brown': '#6B4423',
        'graphite': '#1F2937',
        'signal-purple': '#7C3AED',
        'electric-violet': '#A855F7',
        'market-green': '#22C55E',
        'warning-amber': '#F59E0B',
        'risk-red': '#EF4444',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'system-ui', 'sans-serif'],
        warm: ['Fraunces', 'Georgia', 'serif'],
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'monospace'],
      },
    },
  },
  plugins: [],
}
