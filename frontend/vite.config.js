import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0", // allow access from outside the container
    port: 5173,
    // Proxy API calls to the FastAPI container so we avoid CORS issues during dev
    proxy: {
      "/api": {
        target: "http://api:8000",
        changeOrigin: true,
      },
    },
  },
});
