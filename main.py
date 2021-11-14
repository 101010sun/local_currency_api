from flask import Flask, json, request , jsonify
from flask_cors import CORS
import Wallet, Database

app = Flask(__name__)
CORS(app)

# 使用者登入路由
@app.route('/login', methods=['POST'])
def login():
    insertValues = request.get_json()
    user_account = insertValues['user_account']
    user_password = insertValues['user_password']
    user_id = insertValues['user_id']
    verify_epass = Wallet.encryption_password(user_password, user_id)
    user_epass = Database.Taken_password(user_account)
    if verify_epass == user_epass:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'reason': '帳號密碼錯誤'})

# 使用者註冊
@app.route('/signup', methods=['POST'])
def signup():
    insertValues = request.get_json()
    user_name = insertValues['user_name']
    user_id = insertValues['user_id']
    user_sex = insertValues['user_sex']
    user_birth = insertValues['user_birth']
    user_email = insertValues['user_email']
    user_phone = insertValues['user_phone']
    user_address = insertValues['user_address']
    user_photo = '' #--?
    e_id = Wallet.encryption_id_card(user_id)
    check_id = Database.Check_account(e_id)
    if check_id:
        user_account = insertValues['user_account']
        user_password = insertValues['user_password']
        walletaddress, private_key = Wallet.generate_address()
        public_key = walletaddress
        e_password = Wallet.encryption_password(user_password, user_id) # 加密密碼 (明文身分證)
        e_private_key = Wallet.encryption_privatekey(private_key, user_password) # 加密私鑰 (明文密碼)
        Database.insert_Information_user(user_name, user_sex, e_id, user_birth, user_email, user_phone, user_address, user_account, user_photo, walletaddress, public_key, e_private_key, e_password)
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'reason': '身分證號碼已註冊過'})

# 使用者註冊 驗證身分證
@app.route('/signup/verify_id', methods=['POST'])
def verifyid():
    insertValues = request.get_json()
    user_id = insertValues['user_id']
    e_id = Wallet.encryption_id_card(user_id)
    check_id = Database.Check_account(e_id)
    if check_id:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'reason': '身分證號碼已註冊過'})

# 取社區公告
@app.route('/get-new', methods=['POST'])
def getnew():
    insertValues = request.get_json()
    user_account = insertValues['user_account']
    #- 去資料庫取這個使用者所在的所有社區
    #- 取所有社區的公告
    #- 取系統公告

if __name__ == '__main__':
    app.run(host='192.168.0.108', port='5000', debug=True)