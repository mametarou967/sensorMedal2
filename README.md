# sensorMedal2
センサメダル2のデータを取得する

# 実行方法
- config.jsonに適切な値を設定します
	- ["SensorMedal2"]["Address"]:センサメダルのアドレス
	- ["AWS"]["Endpoint"]:AWSのエンドポイント
- certフォルダを作成し、AWSに必要なファイル3つを以下の名前で配置します
	- certificate.pem.crt
	- private.pem.key
	- root_ca.pem
- sensorMedal2にボタン電池を入れます（勝手に電源がONになります)
- コンソールより以下のコマンドを実行します
 sudo python3 sensorMedal2.py
