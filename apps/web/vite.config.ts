import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// 部署到 GitHub Pages 项目页(子路径 /HuangDiTujian/);本地 dev 保持根路径。
export default defineConfig(({ command }) => ({
  base: command === "build" ? "/HuangDiTujian/" : "/",
  plugins: [react()],
  server: {
    port: 5173,
    open: false,
  },
}));
