# pixiv ETuSoTo Telegram bot
方便大家找p站圖片的機器人，請低調使用。  
感謝 https://saucenao.com/ ，歡迎大家[斗內💰支持他們](https://saucenao.com/donate.php)或我🙇。

## 使用方法
直接傳送圖片給機器人，機器人會去以圖搜圖。請注意以下幾點：  

1. 一則訊息只傳送一張（Forward 亦可）
2. 請使用**圖片**🖼而非檔案❌的方式傳送

## 需求
1. Python 3.7 或以上
2. 必須要有以下套件（可直接用 pip 安裝或使用 pipenv）
	1. python telegram bot
	2. requests
	3. Beautiful Soup

## 部屬
請先複製 `config.ini.example` 出來成 `config.ini` 並填入相關的設定檔內容，之後安裝套件（下面兩種方式二選一）：
### 一般方法
	pip3 install python-telegram-bot==12.4.2
	pip3 install requests
	pip3 install beautifulsoup4
### pipenv
	pipenv install

## 聲明
本人撰寫程式僅用於學術研究及學習，請勿用於非法用途。使用者一切行為所致皆由使用者自行承擔，與作者無任何關聯，亦不負任何責任。

## LICENSE
See [LICENSE](https://gitlab.com/hms5232/pixiv-etusoto-telegram-bot/-/blob/master/LICENSE) file.
