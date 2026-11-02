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
        "pop-scale": {
          "0%": { opacity: "0", transform: "scale(0.68) translateY(32px)" },
          "65%": { opacity: "1", transform: "scale(1.06) translateY(-5px)" },
          "84%": { opacity: "1", transform: "scale(0.98) translateY(1px)" },
          "100%": { opacity: "1", transform: "scale(1) translateY(0)" },
        },
        "pop-up": {
          "0%": { opacity: "0", transform: "translateY(44px) scale(0.88)" },
          "65%": { opacity: "1", transform: "translateY(-7px) scale(1.035)" },
          "84%": { opacity: "1", transform: "translateY(2px) scale(0.99)" },
          "100%": { opacity: "1", transform: "translateY(0) scale(1)" },
        },
        "pop-left": {
          "0%": { opacity: "0", transform: "translateX(-64px) rotate(-6deg) scale(0.84)" },
          "65%": { opacity: "1", transform: "translateX(7px) rotate(1.5deg) scale(1.04)" },
          "84%": { opacity: "1", transform: "translateX(-2px) rotate(-0.4deg) scale(0.99)" },
          "100%": { opacity: "1", transform: "translateX(0) rotate(0deg) scale(1)" },
        },
        "pop-right": {
          "0%": { opacity: "0", transform: "translateX(64px) rotate(6deg) scale(0.84)" },
          "65%": { opacity: "1", transform: "translateX(-7px) rotate(-1.5deg) scale(1.04)" },
          "84%": { opacity: "1", transform: "translateX(2px) rotate(0.4deg) scale(0.99)" },
          "100%": { opacity: "1", transform: "translateX(0) rotate(0deg) scale(1)" },
        },
        "pop-stamp": {
          "0%": { opacity: "0", transform: "scale(0.48) rotate(-8deg)" },
          "60%": { opacity: "1", transform: "scale(1.12) rotate(2.5deg)" },
          "80%": { opacity: "1", transform: "scale(0.96) rotate(-0.8deg)" },
          "100%": { opacity: "1", transform: "scale(1) rotate(0deg)" },
        },
        "pop-paw": {
          "0%": { opacity: "0", transform: "scale(0.25) rotate(-28deg)" },
          "60%": { opacity: "1", transform: "scale(1.24) rotate(10deg)" },
          "80%": { opacity: "1", transform: "scale(0.93) rotate(-3deg)" },
          "100%": { opacity: "1", transform: "scale(1) rotate(0deg)" },
        },
        "pop-cat-ragdoll": {
          "0%": {
            opacity: "0",
            transform: "translateX(-72px) translateY(42px) rotate(-28deg) scale(0.74)",
          },
          "65%": {
            opacity: "1",
            transform: "translateX(7px) translateY(-6px) rotate(-13.5deg) scale(1.05)",
          },
          "84%": {
            opacity: "1",
            transform: "translateX(-2px) translateY(1px) rotate(-17.2deg) scale(0.99)",
          },
          "100%": {
            opacity: "1",
            transform: "translateX(0) translateY(0) rotate(-16.504deg) scale(1)",
          },
        },
        "pop-cat-flip": {
          "0%": {
            opacity: "0",
            transform: "scaleX(-1) translateX(-72px) translateY(38px) rotate(-10deg) scale(0.74)",
          },
          "65%": {
            opacity: "1",
            transform: "scaleX(-1) translateX(7px) translateY(-6px) rotate(2.5deg) scale(1.05)",
          },
          "84%": {
            opacity: "1",
            transform: "scaleX(-1) translateX(-2px) translateY(1px) rotate(-0.6deg) scale(0.99)",
          },
          "100%": {
            opacity: "1",
            transform: "scaleX(-1) translateX(0) translateY(0) rotate(0deg) scale(1)",
          },
        },
      },
      animation: {
        "pop-scale": "pop-scale 680ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "pop-up": "pop-up 640ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "pop-left": "pop-left 680ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "pop-right": "pop-right 680ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "pop-stamp": "pop-stamp 620ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "pop-paw": "pop-paw 560ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "pop-cat-ragdoll": "pop-cat-ragdoll 760ms cubic-bezier(0.22, 1, 0.36, 1) both",
        "pop-cat-flip": "pop-cat-flip 760ms cubic-bezier(0.22, 1, 0.36, 1) both",
      },
    },
  },
  plugins: [],
};
