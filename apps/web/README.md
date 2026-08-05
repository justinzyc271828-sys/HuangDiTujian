# 皇帝图鉴 Web · MVP

## 启动

在仓库根目录或本目录：

```bash
# 1) 生成数据
python tools/build_site_data.py

# 2) 安装并开发
cd apps/web
npm install
npm run dev
```

浏览器打开终端提示的本地地址（默认 `http://localhost:5173`）。

## 闭环能力

- 图鉴总览（首批三人 / 全部 / 已读）
- 人物页：事迹（可跳转）、年表、关联表
- 侧栏示意地图：弧线路径 + 事件列表
- 本地收集进度（localStorage 已读 / 收藏）
- 准帝王入口占位

## 数据

来源：`data/emperors`、`data/places`、`content/bios`  
构建：`tools/build_site_data.py` → `public/data/site.json`
