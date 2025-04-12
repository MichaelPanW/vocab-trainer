# Vocabulary Test

這是一個學習英文單字的模擬測驗程式。

## 功能特點

- 支援多題庫
- 提供提示功能（單字長度、首字母等）
- 錯誤次數統計
- 繁體中文介面
- 智能出題系統（根據歷史表現調整難度）
- 測驗結果記錄與分析
- 每次測驗 5 題，專注學習

## 使用說明

### 使用 Docker 運行（推薦）

1. 確保已安裝 Docker 和 Docker Compose
2. 克隆此專案：
   ```bash
   git clone https://github.com/dsm-helper/dictest.git
   cd dictest
   ```
3. 使用 Docker Compose 啟動：
   ```bash
   docker-compose up --build
   ```
4. 進入容器進行互動：
   ```bash
   docker-compose exec dictest bash
   ```

### 直接運行

1. 確保已安裝 Python 3.9 或更高版本
2. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```
3. 運行程式：
   ```bash
   python dictest/main.py
   ```

### 使用方式

1. 啟動程式後，選擇要測驗的題庫編號

2. 測驗開始後：
   - 程式會顯示單字的中文解釋
   - 同時顯示單字的首尾字母，中間用底線表示長度
   - 請輸入對應的英文單字

3. 答題提示：
   - 答錯 5 次後會提示首字母
   - 答錯 7 次後會提示單字長度
   - 答錯 10 次後會顯示正確答案

4. 特殊指令：
   - 輸入 "exit" 可退出程式
   - 輸入 "next" 可跳過當前題目

5. 測驗結束後：
   - 顯示本次測驗結果
   - 列出放棄的題目
   - 自動記錄測驗結果

6. 智能出題：
   - 系統會根據歷史表現選擇較難的單字
   - 優先出之前答錯或跳過的題目
   - 新單字會以中等難度出題

## 檔案結構

```
dictest/
├── data/               # 題庫資料夾
├── dictest/
│   ├── main.py        # 主程式
│   ├── config.py      # 設定檔
│   └── quiz_history.py # 測驗歷史記錄
├── quiz_history.json  # 測驗結果記錄
├── Dockerfile
└── docker-compose.yml
```

## 參考資料

 - [dictest](https://github.com/dsm-helper/dictest)