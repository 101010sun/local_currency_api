from flask import Flask, json, request , jsonify
from flask_cors import CORS
import Wallet, insertData, getData

app = Flask(__name__)
CORS(app)

# 使用者登入路由
# [user_account, user_password, user_id]
@app.route('/login', methods=['POST'])
def login():
    insertValues = request.get_json()
    user_account = insertValues['user_account']
    user_password = insertValues['user_password']
    user_id = insertValues['user_id']
    verify_epass = Wallet.encryption_password(user_password, user_id)
    user_epass = getData.Taken_password(user_account)
    if verify_epass == user_epass:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'reason': '帳號密碼錯誤'})

# 使用者註冊
# [user_name, user_id, user_sex, user_birth, user_email, user_phone, user_address, user_account, user_password]
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
    check_id = getData.Check_id(e_id)
    if check_id:
        user_account = insertValues['user_account']
        user_password = insertValues['user_password']
        check_account = getData.Check_account(user_account)
        if check_account:
            walletaddress, private_key = Wallet.generate_address()
            public_key = walletaddress
            e_password = Wallet.encryption_password(user_password, user_id) # 加密密碼 (明文身分證)
            e_private_key = Wallet.encryption_privatekey(private_key, user_password) # 加密私鑰 (明文密碼)
            insertData.insert_Information_user(user_name, user_sex, e_id, user_birth, user_email, user_phone, user_address, user_account, user_photo, walletaddress, public_key, e_private_key, e_password)
            return jsonify({'result': 'success'})
        else:
            return jsonify({'result': 'fail', 'reason': '帳號已註冊過'})
    else:
        return jsonify({'result': 'fail', 'reason': '身分證號碼已註冊過'})

# 使用者註冊、驗證身分證
# [user_id]
@app.route('/signup/verify_id', methods=['POST'])
def verifyid():
    insertValues = request.get_json()
    user_id = insertValues['user_id']
    e_id = Wallet.encryption_id_card(user_id)
    check_id = getData.Check_account(e_id)
    if check_id:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'reason': '身分證號碼已註冊過'})

# 新增社區公告
# [communityname, bulletin_title, bulletin_context]
@app.route('/create-new/community', methods=['POST'])
def createComNew():
    insertValues = request.get_json()
    com_name = insertValues['communityname']
    bul_title = insertValues['bulletin_title']
    bul_context = insertValues['bulletin_context']
    insertData.insert_Community_bulletin(com_name, bul_title, bul_context)
    return jsonify({'result': 'success'})

# 新增系統公告
# [bulletin_title, bulletin_context]
@app.route('/create-new/system', methods=['POST'])
def createSysNew():
    insertValues = request.get_json()
    bul_title = insertValues['bulletin_title']
    bul_context = insertValues['bulletin_context']
    insertData.insert_System_bulletin(bul_title, bul_context)
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)