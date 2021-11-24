from pymongo import MongoClient
from Model import getData, Wallet
import gridfs
import numpy as np
import cryptocode

#local host
conn = MongoClient()
#database
db = conn.localcurrency
#collection
col_Information_user         = db.Information_user
col_Information_demand       = db.Information_demand
col_Photo                    = db.Photo
col_Check_community_manager  = db.Check_community_manager
col_Check_community_user     = db.Check_community_user
col_Check_createcommunity    = db.Check_createcommunity
col_Community_members        = db.Community_members
col_Community_bulletin       = db.Community_bulletin
col_System_bulletin          = db.System_bulletin
col_System_members           = db.System_members
col_Community                = db.Community
#connect error or not
col_Information_user.stats
col_Information_demand.stats
col_Photo.stats
col_Check_community_manager.stats
col_Check_community_user.stats
col_Check_createcommunity.stats
col_Community_members.stats
col_Community_bulletin.stats
col_System_bulletin.stats
col_Community.stats

# 新增使用者資訊
def insert_Information_user(name,sex,id_card,birth,email,phone,address,account,photo_id,wallet_address,public_key,e_private_key,e_password): #加入帳戶資訊
    data = {
      'name': name,
      'sex': sex,
      'id_card': id_card,
      'birth': birth,
      'email': email,
      'phone': phone,
      'address': address,
      'account': account,
      'photo_id': photo_id,
      'wallet_address': wallet_address,
      'public_key': public_key,
      'private_key': e_private_key,
      'e_password': e_password
    }
    info = col_Information_user.insert_one(data)
    return(info)

# 新增_需求資訊
def insert_information_demand(requester_account,applicant_account,Photo_id,product_name,amount,details):
    data = {
      'requester_account': requester_account,
      'applicant_account': applicant_account,
      'demand_info':{
        'photo_id': Photo_id,
        'product_name': product_name,
        'amount': amount,
        'details': details
      }
    }
    col_Information_demand.insert_one(data)

# 新增_圖檔
def insert_Photo(length,chunkSize,uploadDate,filename,metadata):
    data = {
      'length': length,
      'chunkSize': chunkSize,
      'uploadDate': uploadDate,
      'filename': filename,
      'metadata': metadata
    }
    col_Photo.insert_one(data)

# 新增_社區管理員審核名單
def insert_Check_community_manager(applicant_account, apply_community, reason):
    data = {
      'applicant_account': applicant_account,
      'apply_community': apply_community
    }
    col_Check_community_manager.insert_one(data)

# 新增_社區用戶審核名單
def insert_Check_community_user(applicant_account, apply_community, applyaddress):
    data = {
      'applicant_account': applicant_account,
      'apply_community': apply_community,
      'apply_address': applyaddress
    }
    col_Check_community_user.insert_one(data)

# 新增_創建社區審核清單
def insert_Check_createcommunity(applicant_account, community, currency_name, circulation):
    data = {
      'applicant_account': applicant_account,
      'community': community,
      'currency_name': currency_name,
      'circulation': circulation
    }
    col_Check_createcommunity.insert_one(data)   

# 新增_社區用戶名單
def insert_Community_members(account,community,community_address,identity):
    myquery = {'account': account}
    cursor = col_Community_members.find(myquery)
    data = [d for d in cursor]
    if data == list([]):
      data = {
        'account': account,
        'community': [community], 
        'community_address': [community_address],
        'identity': [identity] # ('管理員'、'一般用戶')
      }
      col_Community_members.insert_one(data) 
      return True  
    else:
      col_Community_members.update_many({"account": account}, {'$addToSet': {"community":{"$each" : [community]}, "community_address":{"$each" : [community_address]},"identity":{"$each" : [identity]}}})

# 新增_平台管理者
def insert_System_members(account):
    cursor = col_System_members.find()
    data = [d for d in cursor]
    if data == list([]):
      print('Please create system member first!')
    else:
      system_wallet_address = getData.taken_plat_address()
      col_System_members.update_many({"system_wallet_address": system_wallet_address}, {'$addToSet': {"account" :{"$each" :account}}})

# 新增_平台管理者名單(創建)
def create_system_members(account,platform_password):
  system_wallet_address,system_private_key = Wallet.generate_address()
  e_platform_password = Wallet.encryption_id_card(platform_password)
  e_system_private_key = Wallet.encryption_privatekey(system_private_key, platform_password) #傳入私鑰與明文密碼
  cursor = col_System_members.find()
  data = [d for d in cursor]
  if data == list([]):
    data = {
      'account': [account],
      'platform_password': e_platform_password,
      'system_wallet_address': system_wallet_address,
      'system_private_key': e_system_private_key
    }
    col_System_members.insert_one(data) 


# 新增_照片檔案寫入資料庫
def store_photo(name):
    file_location =  name
    file_data = open(file_location, "rb")
    data = file_data.read() #data--讀取檔案
    fs = gridfs.GridFS(db) #fs--選取資料庫
    fs.put(data, filename = name) #寫入資料庫
    print("upload complete")

# 新增_社區公告
def insert_Community_bulletin(communityname, bul_title, bul_context):
    data = {
        'community_name': communityname,
        'bulletin_title': bul_title,
        'bulletin_context': bul_context
    }
    col_Community_bulletin.insert_one(data)

# 新增_系統公告
def insert_System_bulletin(bul_title, bul_context):
    data = {
        'bulletin_title': bul_title,
        'bulletin_context': bul_context
    }
    col_System_bulletin.insert_one(data)

# 新增_社區名單
def insert_community(community, community_wallet_address, community_private_key):
    data = {
        'community': community,
        'community_wallet_address': community_wallet_address,
        'community_private_key': community_private_key
    }
    col_Community.insert_one(data)

# ----test----
# insert_System_members('10')
# system_members(['53'],'platform_password','system_wallet_address','system_private_key')
# insert_System_members(['10'])
  