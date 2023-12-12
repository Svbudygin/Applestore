import requests
import json
import os
from config import headers, cookies
from math import ceil


def id_parsing(offset='0'):
    params = {
        'categoryId': '205',
        'offset': offset,
        'limit': '24',
        'filterParams': [
            'WyJjYXRlZ29yeSIsIiIsImlwaG9uZS05MTQiXQ==',
            'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
        ],
        'doTranslit': 'true',
    }
    return params


def descripion_parsing(product_ids):
    json_data = {
        'productIds': product_ids,
        'mediaTypes': [
            'images',
        ],
        'category': True,
        'status': True,
        'brand': True,
        'propertyTypes': [
            'KEY',
        ],
        'propertiesConfig': {
            'propertiesPortionSize': 5,
        },
        'multioffer': False,
    }
    return json_data


def prices_parsing(product_ids_str):
    params = {
        'productIds': product_ids_str,
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }
    headers1 = {
        'Accept': 'application/json',
        'Sec-Fetch-Site': 'same-origin',
        'Accept-Language': 'ru',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
        'Referer': 'https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205/f/category=iphone-914?reff=menu_main',
        'Connection': 'keep-alive',
        'Host': 'www.mvideo.ru',
        'Sec-Fetch-Dest': 'empty',
        # 'Cookie': 'MVID_ENVCLOUD=prod1; _ga_BNX5WPP3YK=GS1.1.1702363817.7.1.1702366155.53.0.0; _ga_CFMZTSS5FM=GS1.1.1702363817.7.1.1702366155.0.0.0; MVID_CITY_ID=CityCZ_975; MVID_KLADR_ID=7700000000000; MVID_REGION_ID=1; MVID_REGION_SHOP=S002; MVID_TIMEZONE_OFFSET=3; fgsscgib-w-mvideo=faM867b6410982aed5dc67b6c84a47731ed87062; gsscgib-w-mvideo=OB89rGdiUJL07f7hS0RwsP8GiLGTtSdOVzF2jdFT3iiEzSOazPlEsnMj/lF2lSHHUMv59DWY+ivbAnTk7J3jE1dhZVbrc700ESSxZVvIUDRVZJ4zkHPyApVQA1lsBuE9/MglOWpXfeMKSIW7IkjrX+ZkKinTce/wtGXkrW/W76KTJ/gNcmYj3rijVFcpL9BYVjlHVfSaguqyrW+2roCYfR5ziQsxChpFxsiU9k3m4fRqprrFrkV8JIFapkCLhA2dbw==; fgsscgib-w-mvideo=faM867b6410982aed5dc67b6c84a47731ed87062; gsscgib-w-mvideo=OB89rGdiUJL07f7hS0RwsP8GiLGTtSdOVzF2jdFT3iiEzSOazPlEsnMj/lF2lSHHUMv59DWY+ivbAnTk7J3jE1dhZVbrc700ESSxZVvIUDRVZJ4zkHPyApVQA1lsBuE9/MglOWpXfeMKSIW7IkjrX+ZkKinTce/wtGXkrW/W76KTJ/gNcmYj3rijVFcpL9BYVjlHVfSaguqyrW+2roCYfR5ziQsxChpFxsiU9k3m4fRqprrFrkV8JIFapkCLhA2dbw==; cfidsgib-w-mvideo=N/hia2VPf+IpSDJZxhU7sdsX/0p+pSujEfrsE6/GHdU/LdpI/O4TL8OsANNQPBxZPFNpg12olTwDEgkgGrH5QvASOZxu4RmO/Ls6yYvjx9JEEb1YcTrnCnIFpj3651qQOmErIN6D2tm9k8uA2R54oQGP/nPAIf6XcK3xu8Q=; gsscgib-w-mvideo=Zm7wqKQ9cZxPQtQlJ9zC5y3IY+U5kUrRwGlcIUm3+v5DSd6zd8irC/ZfcQW2a6FZqcnjEKd2HarVMTHlAnrkNo3eWJgXTb9YKvJ3mQS2EBzoB38IGycYNu/PNoqluT/0QrtCRAppOIgRZ2VGUW2whaHXIM9WHutOrfQ7WRYt5I/D1o0mTZXEMIY4IRttidWBNh2gSZ8whNYpSh1edrEzxrE4kc+yJDykUssNAwU4Dt3gLUDw1H2znITtKvyqP+znyw==; __hash_=f54ecfc38059edd6e76485ce1c3317b9; _sp_id.d61c=f13a452c-fa99-4f8e-810b-0f3ce268c406.1702312209.7.1702366148.1702336060.7c16aac6-e18a-47ce-86a7-5f2faa67f6ba.f4dce330-3f6a-4995-ba9a-acfade84389f.534a09f4-f5f4-4b2f-8b2c-af0c9e4b0874.1702363812255.28; _sp_ses.d61c=*; __rhash_=044ec4411309add6e7675c9cc946aa96; tmr_detect=0%7C1702364982018; _gp100025D5={"hits":16,"vc":1,"ac":1,"a6":1}; afUserId=8d94f3ec-9f52-485c-9c59-dcaadd064e10-p; tmr_lvid=d91abb7bc3161e63b455e58bc5bbaebb; tmr_lvidTS=1702312212779; _ga=GA1.1.430761083.1702312210; directCrm-session=%7B%22deviceGuid%22%3A%2229d9e523-f6a9-467c-939c-c22b074b3b81%22%7D; mindboxDeviceUUID=29d9e523-f6a9-467c-939c-c22b074b3b81; __lhash_=80288e1deeae0e7dfc97da81f4539058; cookie_ip_add=46.138.199.251; __SourceTracker=google__organic; admitad_deduplication_cookie=google__organic; SMSError=; authError=; CACHE_INDICATOR=true; COMPARISON_INDICATOR=false; MVID_NEW_OLD=eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9; MVID_VIEWED_PRODUCTS=; bIPs=-826759811; flacktory=no; BIGipServeratg-ps-prod_tcp80=1141169162.20480.0000; BIGipServeratg-ps-prod_tcp80_clone=1141169162.20480.0000; deviceType=desktop; HINTS_FIO_COOKIE_NAME=2; JSESSIONID=215yl3nB78QJXJ9DysvS3mv1htl5MhC4s7n6m1hyJGmHX7DgJqGT!-925465543; MVID_CALC_BONUS_RUBLES_PROFIT=false; MVID_CART_MULTI_DELETE=false; MVID_GET_LOCATION_BY_DADATA=DaData; MVID_GUEST_ID=23315655657; MVID_OLD_NEW=eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==; MVID_YANDEX_WIDGET=true; NEED_REQUIRE_APPLY_DISCOUNT=true; PRESELECT_COURIER_DELIVERY_FOR_KBT=true; PROMOLISTING_WITHOUT_STOCK_AB_TEST=2; searchType2=2; wurfl_device_id=generic_web_browser; MVID_GTM_BROWSER_THEME=1; adid=170232234840327; AF_SYNC=1702312213507; _gpVisits={"isFirstVisitDomain":true,"idContainer":"100025D5"}; adrcid=AzlTqR41p215i47pts5eAsw; advcake_session_id=8a957788-78b8-42cd-103b-45217dc0bfb0; advcake_track_id=9537b346-ac88-1f21-d1e3-bd9288102da0; gdeslon.ru.__arc_domain=gdeslon.ru; gdeslon.ru.user_id=a7dd74a3-3a9a-4082-9038-c5d694fd2be8; uxs_uid=8eda03a0-9842-11ee-8e74-37fbf3d4856e; flocktory-uuid=497d72f0-7dd0-4bef-93b6-0b823c107e75-3; _ym_d=1702312210; _ym_isad=2; _ym_uid=1702312210977470640; st_uid=c5a099678d0a2bc4a82b4b6d899386ad; MVID_AB_PERSONAL_RECOMMENDS=true; MVID_AB_UPSALE=true; MVID_ALFA_PODELI_NEW=true; MVID_CHAT_VERSION=4.16.4; MVID_CREDIT_DIGITAL=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_CROSS_POLLINATION=true; MVID_DISPLAY_ACCRUED_BR=true; MVID_EMPLOYEE_DISCOUNT=true; MVID_FILTER_TOOLTIP=1; MVID_GTM_ENABLED=011; MVID_INTERVAL_DELIVERY=true; MVID_IS_NEW_BR_WIDGET=true; MVID_LAYOUT_TYPE=1; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_NEW_MBONUS_BLOCK=true; MVID_PODELI_PDP=true; MVID_SERVICE_AVLB=true; MVID_SINGLE_CHECKOUT=true; SENTRY_ERRORS_RATE=0.1; SENTRY_TRANSACTIONS_RATE=0.5; MVID_CASCADE_CMN=true; MVID_CREDIT_SERVICES=true; MVID_FILTER_CODES=true; MVID_FLOCKTORY_ON=true; MVID_NEW_LK_OTP_TIMER=true; MVID_SERVICES=111; MVID_SP=true; MVID_TYP_CHAT=true; MVID_WEB_SBP=true; MVID_GEOLOCATION_NEEDED=true',
        'baggage': 'sentry-environment=production,sentry-public_key=1e9efdeb57cf4127af3f903ec9db1466,sentry-trace_id=c933095468d642659bd08837ca1931eb,sentry-sample_rate=0.5,sentry-transaction=%2F**%2F,sentry-sampled=true',
        'sentry-trace': 'c933095468d642659bd08837ca1931eb-883d42e3d729b0d1-1',
        'x-set-application-id': '308f7a15-86bf-4493-ad96-5b3e0a70c120',
    }
    return params, headers1


def get_data():
    if not os.path.exists('data'):
        os.mkdir('data')

    params = id_parsing()
    # echo -n 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==' | base64 -d
    sess = requests.Session()
    response = sess.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                        headers=headers).json()
    total_number_of_items = response.get('body').get('total')
    if total_number_of_items is None:
        return 'Товары не найдены!'
    pages = ceil(total_number_of_items / 24)

    description = {}
    ids = {}
    prices = {}
    for page in range(pages):
        offset = str(page * 24)
        params = id_parsing(offset=offset)
        response = sess.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                            headers=headers).json()
        product_ids = response.get('body').get('products')
        ids[page] = product_ids
        # ------ next block: prices
        product_ids_str = ','.join(product_ids)
        params, headers1 = prices_parsing(product_ids_str)
        try:
            response_price = sess.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                      headers=headers1).json()
        except requests.exceptions.JSONDecodeError:
            continue
        # ------ next block: description
        json_data = descripion_parsing(product_ids)

        response = sess.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers,
                             json=json_data).json()
        description[page] = response
        # ------ back to block: prices
        material_prices = response_price.get('body').get('materialPrices')

        for product in material_prices:
            product_id = product.get('price').get('productId')
            product_base_price = product.get('price').get('basePrice')
            product_sale_price = product.get('price').get('salePrice')
            product_bonus = product.get('bonusRubles').get('total')
            prices[product_id] = {
                "basePrice": product_base_price,
                "salePrice": product_sale_price,
                "bonus": product_bonus
            }
        print(f'[+] Page {page} from {pages}')
    with open(f'data/description.json', 'w') as file:
        json.dump(description, file, indent=4, ensure_ascii=True)
    for items in description.values():
        items = items.get('body').get('products')
        if items:
            for product in items:
                product_id = product.get('productId')
                if product_id in prices:
                    price = prices[product_id]
                    product["basePrice"] = price.get('basePrice')
                    product["salePrice"] = price.get('salePrice')
                    product["bonus"] = price.get('bonus')
                    product["link"] = f"https://www.mvideo.ru/products/{product.get('nameTranslit')}-{product_id}"

    with open(f'data/result.json', 'w') as file:
        json.dump(description, file, indent=4, ensure_ascii=True)


def main():
    # get_data()
    pass
if __name__ == '__main__':
    main()
