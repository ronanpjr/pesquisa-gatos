/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html"],
  blocklist: ["filter", "transition", "sr-only"],
  corePlugins: {
    preflight: false,
  },
  theme: {
    extend: {
      keyframes: {
        "cat-breathe": {
          "0%, 100%": { transform: "scale(1)" },
          "50%": { transform: "scale(1.016, 1.024)" },
        },
        "cat-ragdoll": {
          "0%, 100%": { transform: "rotate(-16.504deg) translateY(0)" },
          "50%": { transform: "rotate(-14.8deg) translateY(-5px)" },
        },
        "cat-tabby": {
          "0%, 100%": { transform: "scaleX(-1) translateY(0) rotate(0deg)" },
          "50%": { transform: "scaleX(-1) translateY(-5px) rotate(1.2deg)" },
        },
        "cat-team": {
          "0%, 100%": { transform: "scaleX(-1) translateY(0) rotate(0deg)" },
          "50%": { transform: "scaleX(-1) translateY(-5px) rotate(-1deg)" },
        },
        "cat-float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-6px)" },
        },
        "flask-swirl": {
          "0%, 100%": { transform: "rotate(0deg)" },
          "25%": { transform: "rotate(-7deg) translateY(-2px)" },
          "75%": { transform: "rotate(6deg) translateY(-1px)" },
        },
        "tube-bob": {
          "0%, 100%": { transform: "translateY(0) rotate(0deg)" },
          "50%": { transform: "translateY(-4px) rotate(3deg)" },
        },
        "rays-pulse": {
          "0%, 100%": { opacity: "1", transform: "scale(1)" },
          "50%": { opacity: "0.4", transform: "scale(1.03)" },
        },
        "sunburst-pulse": {
          "0%, 100%": { opacity: "1", transform: "scale(1)" },
          "50%": { opacity: "0.72", transform: "scale(1.022)" },
        },
        "paw-wiggle": {
          "0%, 100%": { transform: "rotate(0deg) scale(1)" },
          "30%": { transform: "rotate(-12deg) scale(1.1)" },
          "60%": { transform: "rotate(10deg) scale(1.06)" },
        },
        "phone-ring": {
          "0%, 70%, 100%": { transform: "rotate(0deg) scale(1)" },
          "75%": { transform: "rotate(-12deg) scale(1.08)" },
          "80%": { transform: "rotate(12deg) scale(1.08)" },
          "85%": { transform: "rotate(-10deg) scale(1.06)" },
          "90%": { transform: "rotate(10deg) scale(1.06)" },
          "95%": { transform: "rotate(0deg) scale(1)" },
        },
        "badge-float": {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-3px)" },
        },
      },
      animation: {
        "cat-breathe": "cat-breathe 4.5s ease-in-out infinite",
        "cat-ragdoll": "cat-ragdoll 5.5s ease-in-out infinite",
        "cat-tabby": "cat-tabby 5s ease-in-out infinite",
        "cat-team": "cat-team 5.5s ease-in-out infinite",
        "cat-float": "cat-float 4.8s ease-in-out infinite",
        "flask-swirl": "flask-swirl 3.6s ease-in-out infinite",
        "tube-bob": "tube-bob 3.8s ease-in-out infinite",
        "rays-pulse": "rays-pulse 2.4s ease-in-out infinite",
        "sunburst-pulse": "sunburst-pulse 4s ease-in-out infinite",
        "paw-wiggle": "paw-wiggle 3.2s ease-in-out infinite",
        "phone-ring": "phone-ring 3s ease-in-out infinite",
        "badge-float": "badge-float 3.5s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
