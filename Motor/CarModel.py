# !/usr/bin/env python
# -*- coding: utf-8 -*


# section 1

import json

import csv, time
import random
import requests

from conf import *

cars = []
cars.append(["make", "model", "body", "year", "variant", "engine", "price", "img"])

url = "https://api.yourcar.co.nz/graphql"

payload = "{\n    \"operationName\": \"fetchCmakes\",\n    \"variables\": {\n        \"withModels\": false\n    },\n    \"query\": \"query fetchCmakes($withModels: Boolean = false) {\\n  cmakes(where: {is_disabled: false}, limit: 99999, sort: \\\"name:asc\\\") {\\n    id\\n    name\\n    slug\\n    cmodels(where: {is_disabled: false}, limit: 99999) @include(if: $withModels) {\\n      id\\n      name\\n      cgenerations(where: {name: \\\"Latest\\\"}) {\\n        id\\n        cmodelvariants(limit: 99999) {\\n          id\\n          name\\n          cbodytype_id {\\n            id\\n            name\\n            __typename\\n          }\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"\n}"
headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'User-Agent': "PostmanRuntime/7.19.0",
    'Accept': "*/*",
    'Postman-Token': "c6ba88f7-92d8-4281-9c45-11a7d2877b9a,db5e2d65-7898-4d0e-8966-bb222a55506b",
    'Host': "api.yourcar.co.nz",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "708",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
}

response = requests.request("POST", url, data=payload, headers=headers, proxies=random.choice(proxies))

# print(response.text)
data_make = json.loads(response.text)

for make in data_make["data"]["cmakes"]:
    make_id = make["id"]
    make_name = make["name"]

    # section 2
    payload = "{\"operationName\":\"findCmake\",\"variables\":{\"cmakeId\":%s},\"query\":\"query findCmake($cmakeId: ID = 25) {\\n  cmake(id: $cmakeId) {\\n    id\\n    name\\n    cmodels(sort: \\\"name:asc\\\", where: {is_disabled: false}) {\\n      id\\n      name\\n      cmodelvariants(limit: 99999) {\\n        id\\n        name\\n        cbodytype_id {\\n          id\\n          name\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}" % make_id
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "484d58b0-be1b-48f8-b042-138c8959c66b,f9121801-34eb-46e9-a7f5-242ac1795a5d",
        'Host': "api.yourcar.co.nz",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "462",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload, headers=headers, proxies=random.choice(proxies))

    # print(response.text)
    data_model = json.loads(response.text)

    for model in data_model["data"]["cmake"]["cmodels"]:
        model_id = model["id"]
        model_name = model["name"]

        for variant in model["cmodelvariants"]:
            variant_id = variant["id"]
            variant_name = variant["cbodytype_id"]["name"]


            # section 3

            payload = "{\"operationName\":\"findCmodelvariant\",\"variables\":{\"cmodelvariantId\":\"%s\"},\"query\":\"query findCmodelvariant($cmodelvariantId: ID!) {\\n  cmodelvariant(id: $cmodelvariantId) {\\n    id\\n    description\\n    cbodytype_id {\\n      id\\n      name\\n      slug\\n      __typename\\n    }\\n    cmodel_id {\\n      id\\n      name\\n      description\\n      cmake_id {\\n        id\\n        name\\n        slug\\n        __typename\\n      }\\n      image {\\n        id\\n        name\\n        url\\n        __typename\\n      }\\n      __typename\\n    }\\n    image {\\n      id\\n      name\\n      url\\n      __typename\\n    }\\n    cgeneration_id {\\n      id\\n      year_begin\\n      __typename\\n    }\\n    cspecs {\\n      id\\n      name\\n      description\\n      cspecengines(sort: \\\"price_mrp:asc\\\") {\\n        id\\n        price_mrp\\n        cengine_id {\\n          id\\n          name\\n          cspecificationvalues(where: {cspecification_id: {slug_in: [\\\"fuel_type\\\", \\\"transmission\\\"]}}) {\\n            id\\n            value\\n            cspecification_id {\\n              id\\n              name\\n              slug\\n              __typename\\n            }\\n            __typename\\n          }\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}" % variant_id
            headers = {
                'Content-Type': "application/json",
                'User-Agent': "PostmanRuntime/7.19.0",
                'Accept': "*/*",
                'Cache-Control': "no-cache",
                'Postman-Token': "e848bcc1-7c1a-4076-8309-605b070083d6,3a0d756a-a66c-46bb-903c-1313c61fc333",
                'Host': "api.yourcar.co.nz",
                'Accept-Encoding': "gzip, deflate",
                'Content-Length': "1287",
                'Connection': "keep-alive",
                'cache-control': "no-cache"
            }

            response = requests.request("POST", url, data=payload, headers=headers, proxies=random.choice(proxies))
            data_spec = json.loads(response.text)
            # print(response.text)
            time.sleep(5)
            for spec in data_spec["data"]["cmodelvariant"]["cspecs"]:
                spec_id = spec["id"]
                spec_name = spec["name"]
                variant_year = data_spec["data"]["cmodelvariant"]["cgeneration_id"]["year_begin"]
                if data_spec["data"]["cmodelvariant"]["image"] != None:
                    variant_img = data_spec["data"]["cmodelvariant"]["image"]["url"]
                else:
                    variant_img = ""

                # section 4
                #                 payload = "{\"operationName\":\"findCspec\",\"variables\":{\"cspecId\":\"%s\"},\"query\":\"query findCspec($cspecId: ID!) {\\n  cspec(id: $cspecId) {\\n    id\\n    name\\n    cspecengines {\\n      id\\n      price_mrp\\n      cengine_id {\\n        id\\n        name\\n        cspecificationvalues(where: {cspecification_id: {slug_in: [\\\"transmission\\\", \\\"fuel_type\\\"]}}) {\\n          id\\n          value\\n          cspecification_id {\\n            id\\n            name\\n            slug\\n            __typename\\n          }\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"%spec_id
                #                 headers = {
                #                     'Content-Type': "application/json",
                #                     'User-Agent': "PostmanRuntime/7.19.0",
                #                     'Accept': "*/*",
                #                     'Cache-Control': "no-cache",
                #                     'Postman-Token': "08395a0d-5592-451f-930e-ba41830b3404,79b31667-0d8c-4e54-bf7e-33863a5fa206",
                #                     'Host': "api.yourcar.co.nz",
                #                     'Accept-Encoding': "gzip, deflate",
                #                     'Content-Length': "607",
                #                     'Connection': "keep-alive",
                #                     'cache-control': "no-cache"
                #                 }
                #
                #                 response = requests.request("POST", url, data=payload, headers=headers, proxies=random.choice(proxies))
                #                 data_spec_detail = json.loads(response.text)

                for engine in spec["cspecengines"]:
                    engine_price = engine["price_mrp"]
                    engine_name = engine["cengine_id"]["name"]
                    car = [make_name, model_name, variant_name, variant_year, spec_name, engine_name, engine_price, variant_img]
                    print(car)
                    cars.append(car)

    #         break
    #     break
    # break

with open("yourcar.csv", 'w+') as fp:
    csvwriter = csv.writer(fp)
    csvwriter.writerows(cars)
