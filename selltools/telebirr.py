import json
import requests
import os
from dotenv import load_dotenv
import uuid
import time
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pss
from base64 import b64decode, b64encode

load_dotenv()

def sign(request):
    privateKey = os.getenv("privatekey")
    exclude_fields = ["sign", "sign_type", "header", "refund_info", "openType", "raw_request"]
    join=[]
    for key in request:
        if key in exclude_fields:
            continue
        if key == "biz_content":
            biz_content = request["biz_content"]
            for k in biz_content:
                join.append(k+"="+biz_content[k])
        else:
            join.append(key+"="+request[key])
    join.sort()
    separator = '&'
    inputString = str(separator.join(join))
    return SignWithRSA(inputString,privateKey,"SHA256withRSA")
# """ Generate signature
#       :param data: the key=value&key2=value2 format signature source string
#       :param key: Sign key
#       :param sign_type: sign type SHA256withRSA or HmacSHA256
#       :return: sign string
# """
def SignWithRSA(data,key, sign_type="SHA256withRSA"):
    if sign_type == "SHA256withRSA":
        key_bytes = b64decode(key.encode("utf-8"))
        key = RSA.importKey(key_bytes)
        digest = SHA256.new()
        digest.update(data.encode("utf-8"))
        signer = pss.new(key)
        signature = signer.sign(digest)
        return b64encode(signature).decode("utf-8")
    else:
        return "Only allowed to the type SHA256withRSA hash"

def createMerchantOrderId():
    return str(time.time())

def createTimeStamp():
    return str(round(time.time()))

def createNonceStr():
    return uuid.uuid1()

def applyFabricToken():
    headers = {
    "Content-Type":"application/json",
    "X-APP-Key":os.getenv('fabricappid')
    }
    payload = {
            "appSecret":os.getenv('secret')
    }
    data=json.dumps(payload)
    authToken = requests.post(url=os.getenv("baseurl") + "/payment/v1/token",headers=headers,data=data,verify=False)
    return authToken.json()['token']

def createRequestObject(notifypath,title,amount,id):
    headers = {
            "Content-Type":"application/json",
            "X-APP-Key":os.getenv('fabricappid'),
            "Authorization":applyFabricToken(),
        }
    req = {
        "nonce_str":"asdscsaxxsdddefgddfdd",
        "method":"payment.preorder",
        "timestamp":createTimeStamp(),
        "version":"1.0",
        "sign_type":"SHA256withRSA",
        "biz_content":{},   
    }
    biz={
        "notify_url":notifypath,
        "business_type":"BuyGoods",
        "trade_type":"Checkout",
        "appid":os.getenv('appid'),
        "merch_code":os.getenv("shortcode"),
        "merch_order_id":id,
        "title":title,
        "total_amount":amount,
        "trans_currency":"ETB",
        "timeout_express":"120m",
        "payee_identifier":os.getenv('shortcode'),
        "payee_identifier_type":"04",
        "payee_type":"5000"
    }
    req["biz_content"] = biz
    req["sign"] =sign(req)
    servert_output = requests.post(url=os.getenv("baseurl") + "/payment/v1/merchant/preOrder",headers=headers,data=json.dumps(req),verify=False)

    print(servert_output.json()) 

def createRawRequest(self,prepayId):
        maps={
            "appid":os.getenv('appid'),
            "merch_code":os.getenv("shortcode"),
            "nonce_str":createNonceStr(),
            "prepay_id":prepayId,
            "timestamp":createTimeStamp(),
            "sign_type":"SHA256WithRSA" 
        }
        rawRequest=""
        for (key,value) in map:
            rawRequest = rawRequest + key + "=" + value + "&"
        sign = tools.sign(maps)
        rawRequest = rawRequest+"sign="+sign
        return rawRequest

createRequestObject("https://www.google.com","test","1200","57")