from pymongo import MongoClient
import Wallet
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

# 檢查_此信箱和電話是否被使用過
def Check_userinfor(email,phone):
  cursor = col_Information_user.find({"email":str(email)})
  data = [d for d in cursor]
  cursor2 = col_Information_user.find({"phone":str(phone)})
  data2 = [d for d in cursor2]
  if data == list([]) and data2 == list([]):
    return True
  else:
    return False

# 檢查_此身分證號碼是否被使用過
def Check_id(id_card):
  cursor = col_Information_user.find({"id_card":str(id_card)})
  data = [d for d in cursor]
  if data == list([]): 
    return True
  else:
    return False

# 檢查_此帳號是否被使用過
def Check_account(account):
  cursor = col_Information_user.find({"account":str(account)})
  data = [d for d in cursor]
  if data == list([]): 
    return True
  else:
    return False

# 檢查此帳號是否已加入社區
def check_has_community(account):
    myquery = {'account': account}
    cursor = col_Community_members.find()
    data = [d for d in cursor]
    if data != list([]):
        return data
    else:
        return None