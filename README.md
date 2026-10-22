# NV Green Dark

NV Green Dark 是一款供本機安裝的 VS Code 深色主題擴充套件。視覺基準取自 `20261020_Task_Progress_Reports` 的深綠黑底、亮綠色強調與分層面板。

## 內容

- 色彩主題：工作台、編輯器、終端機、語法與語意標記。
- 檔案圖示主題：常見程式碼、設定、文件、韌體映像與日誌；其他格式使用通用圖示。
- 介面圖示主題：常用工作台操作圖示。未覆寫的圖示沿用 VS Code 預設圖示。
- `NV Green Dark: Apply Complete Theme` 指令：將三種主題寫入使用者層級設定。

## 本機使用

1. 執行 `npm.cmd install`、`npm.cmd test` 與 `npm.cmd run package:verify`。
2. 執行 `code.cmd --install-extension release/nv-green-dark-0.1.0.vsix`。
3. 在 VS Code 命令面板執行 `NV Green Dark: Apply Complete Theme`。

本指令只在使用者主動執行時變更主題設定。其他擴充套件自行固定樣式的 Webview 不一定會隨色彩主題改變。

## 圖示來源與維護

SVG 檔案與介面圖示字型均為此專案繪製。介面字型由 `tool/build_product_font.py` 產生；重新產生時需要 `fonttools==4.60.1`。`tool/render_preview.py` 可產生視覺檢查圖，另需 Pillow。

本專案是獨立 Git 儲存庫，目前僅規劃本機 VSIX 驗收，沒有公開發佈流程。
