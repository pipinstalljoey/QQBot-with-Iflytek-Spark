import SparkApi
import yaml
import sys
with open('config.yaml', 'r') as yaml_file:
    config = yaml.safe_load(yaml_file)
print("[INFO] 获取config.yaml成功！", config)
# 以下密钥信息从控制台获取
for i in config:
    if config[i] == "":
        print("[ERROR] config.yaml中填写有遗漏！停止运行")
        sys.exit()
    print("[INFO]", i, ":", config[i])
appid = config["ai-AppId"]
api_secret = config["ai-ApiSecret"]
api_key = config["ai-ApiKey"]
version = config["version"]
if version == "v1.5":
    domain = "general"  # v1.5版本
    Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"
elif version == "v2.0":
    domain = "generalv2"
    Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"
else:
    print("[WARNING] config.yaml中version一项填写错误，默认使用v1.5!")
    domain = "general"  # v1.5版本
    Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"

text = []

length = 0


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


def question(Input):
    text.clear
    print("[INPUT] ", Input)
    question = checklen(getText("user", Input))
    SparkApi.answer = ""
    print("[OUTPUT] ", end="")
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    answer = getText("assistant", SparkApi.answer)
    res = answer[length - 1]["content"]
    return res
