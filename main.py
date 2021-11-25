from flask import Flask, json, request , jsonify
from flask_cors import CORS
from Model import Wallet, insertData, getData, checkData

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
    user_epass = getData.taken_password(user_account)
    if verify_epass == user_epass:
        print("success")
        return jsonify({'result': 'success'})
    else:
        print("fail")
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
    check_id = checkData.check_id(e_id)
    if check_id:
        user_account = insertValues['user_account']
        user_password = insertValues['user_password']
        check_account = checkData.check_account(user_account)
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
    check_id = checkData.check_account(e_id)
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

# 取得_此帳號所加入的所有社區的清單
# [user_account]
@app.route('/user-community', methods=['POST'])
def getUserCommunity():
    insertValues = request.get_json()
    user_account = insertValues['user_account']
    isjoincommunity = checkData.check_has_community(user_account)
    issystemmanager = checkData.check_is_system_manage(user_account)
    result = dict({})
    community_list = list([])
    if isjoincommunity: # 有加入社區
        tmp_community = getData.taken_comandid(user_account)
        for i in range(0, len(tmp_community[0]['community'])):
            tmp = {'community': tmp_community[0]['community'][i], 'identity': tmp_community[0]['identity'][i]}
            community_list.append(tmp)
    if issystemmanager: # 是平台管理員
        system_dict = {'community': '平台', 'identity': '平台管理員'}
        community_list.insert(0, system_dict)
    if community_list != []:
        result['all_community'] = community_list
        result['result'] = 'one'
    else:
        result['result'] = 'two'
    return jsonify(result)

# 申請_創建社區
# [user_account, community_name, currency_name, circulation]
@app.route('/apply/create-community', methods=['POST'])
def createCommunity():
    insertValue = request.get_json()
    user_account = insertValue['user_account']
    community_name = insertValue['community_name']
    currency_name = insertValue['currency_name']
    circulation = float(insertValue['circulation'])
    insertData.insert_Check_createcommunity(user_account, community_name, currency_name, circulation)
    return jsonify({'result': 'success'})

# 取得_所有社區清單
@app.route('get-all-community', methods=['POST'])
def getAllCommunity():
    community_list = getData.take_community()
    return jsonify(community_list)

# 申請_加入社區
@app.route('/apply/join-community', methods=['POST'])
def joinCommunity():
    insertValue = request.get_json()
    user_account = insertValue['user_account']
    apply_community = insertValue['apply_community']
    apply_addresss = insertValue['apply_address']
    insertData.insert_Check_community_user(user_account, apply_community, apply_addresss)
    return jsonify({'result': 'success'})

# 驗證_平台管理員密碼
@app.route('/identity/system-password', methods=['POST'])
def identitySysPass():
    insertValue = request.get_json()
    system_password = insertValue['system_password']
    issyspasscurrent = checkData.check_platform_password(system_password)
    if issyspasscurrent:
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'fail', 'reason': '平台密碼錯誤!'})

# 取得_創建社區清單
@app.route('/get-create-community-list', methods=['POST'])
def getCreateComList():
    create_list = getData.take_create_community()
    return jsonify(create_list)

if __name__ == '__main__':
    app.run(host='192.168.0.108', port='5000', debug=True)
    # app.run(debug=True)
