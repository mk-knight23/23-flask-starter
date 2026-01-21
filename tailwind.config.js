/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                flask: "#0891b2", // Premium teal/cyan for FlaskHub
                dark: "#020617",
            },
            fontFamily: {
                mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
            },
            boxShadow: {
                'neon': '0 0 15px rgba(0, 180, 216, 0.2)',
                'neon-strong': '0 0 20px rgba(0, 180, 216, 0.3)',
            },
        },
    },
    plugins: [],
}
