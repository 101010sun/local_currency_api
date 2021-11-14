from pymongo import MongoClient
from Model import Wallet
import gridfs
import cv2

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

# 新增_使用者資訊
def insert_Information_user(name,sex,id_card,birth,email,phone,address,account,photo_id,walletaddress,public_key,e_private_key,e_password): #加入帳戶資訊
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
      'walletaddress': walletaddress,
      'public_key': public_key,
      'private_key': e_private_key,
      'e_password': e_password
    }
    info = col_Information_user.insert_one(data)
    return(info)

# 新增_需求資訊
def insert_Information_demand(requester_id,applicant_id,Photo_id,productname,amount,details):
    data = {
      'requester_id': requester_id,
      'applicant_id': applicant_id,
      'demand_imfor':{
        'Photo_id': Photo_id,
        'productname': productname,
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

# 寫入_照片檔案
def store_photo(name):
    file_location =  name
    file_data = open(file_location, "rb")
    data = file_data.read() #data--讀取檔案
    fs = gridfs.GridFS(db) #fs--選取資料庫
    fs.put(data, filename = name) #寫入資料庫
    print("upload complete")

# 新增_社區管理員審核名單
def insert_Check_community_manager(applicant_id,reason):
    data = {
      'applicant_id': applicant_id,
      'reason': reason
    }
    col_Check_community_manager.insert_one(data)

# 新增_社區用戶審核名單
def insert_Check_community_user(applicant_id,applyaddress):
    data = {
      'applicant_id': applicant_id,
      'applyaddress': applyaddress
    }
    col_Check_community_user.insert_one(data)

# 新增_創建社區審核清單
def insert_Check_createcommunity(applicant_id,communityname,communityaddress):
    data = {
      'applicant_id': applicant_id,
      'communityname': communityname,
      'communityaddress': communityaddress
    }
    col_Check_createcommunity.insert_one(data)   

# 新增_平台管理者名單
def insert_System_members(account):
    data = {
      'account': account
    }
    col_System_members.insert_one(data) 

# 新增_社區用戶名單
def insert_Communitymembers(user_id,communityaddress,identity):
    data = {
      'user_id':user_id, ###改Validation 取名
      'communityaddress': communityaddress,
      'identity': identity
    }
    col_Community_members.insert_one(data)   

# 新增_社區名單
def insert_community(community, community_wallet_address, community_private_key):
    data = {
        'community': community,
        'community_wallet_address': community_wallet_address,
        'community_private_key': community_private_key
    }
    col_Community.insert_one(data)

# 新增_社區公告
def insert_Community_bulletin(communityname, bul_title, bul_context):
    data = {
        'communityname': communityname,
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



# --------test--------
# def register():
#   name = "葉清偉"
#   sex = "男"
#   id_card = "F274234929"
#   birth = "1999-08-13"
#   #database-date
#   #birth = datetime.datetime.strptime("2017-10-13T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")
#   email = "fewffw"
#   phone = "0974613264"
#   address = ["桃園"]
#   account = "rgrwgN"
#   e_id_card = Wallet.encryption_id_card(id_card,account)
#   photo_id = "wfwfwfefwr"
#   walletaddress,private_key = Wallet.generate_address() #產生公私鑰地址
#   public_key = walletaddress 
#   #密碼
#   password = "GFGwfwfe3"
#   e_password = Wallet.encryption_password(password,e_id_card) #加密密碼
#   e_private_key = Wallet.encryption_privatekey(private_key,password) #加密私鑰
#   insert_Information_user(name,sex,e_id_card,birth,email,phone,address,account,photo_id,walletaddress,public_key,e_private_key,e_password)

# print(Taken_privatekey('rgrwgN','GFGwfwfe3'))