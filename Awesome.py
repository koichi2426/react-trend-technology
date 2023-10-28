#1.GitHubAPIを活用したデータ取得
import json
import requests
import openai
import git
import os

query = "React"#検索キーワードの設定
params = {"q": query, "sort": "stars", "order": "desc","per_page": 20}#人気順トップ20のリポジトリを取得
URL = "https://api.github.com/search/repositories"
response = requests.get(URL, params=params)
data = json.loads(response.text)



#2.必要な情報を見つけ出すテキスト分類
openai.api_key = "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"
model = "gpt-3.5-turbo"

def related_decisions(word):
    prompt = """
    Question:\nIs this description relevant to f{target_word}? Please answer Yes or No.\n\n###
    Description:\nf{word}\n\n### Answer:\n"""

    messages = [{"role": "system", "content": prompt}]
    completion = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    )
    return completion["choices"][0]["message"]["content"]

#3.情報をわかりやすく伝える多言語機械翻訳
def translate(input_text):
    target_lang = "Japanese"
    prompt = (
    "Please translate the following input text into"
    f" {target_lang}.\n\nInput text: {input_text}"
    )
    messages = [{"role": "system", "content": prompt}]
    completion = openai.ChatCompletion.create(model=model,messages=messages)
    return completion["choices"][0]["message"]["content"]


# dataからitemsリストを取得
items = data["items"]

# 書き込み用にファイルを開く（ファイルが存在しない場合は作成します）
with open("./AwesomeRepositories/README.md", "w", encoding="utf-8") as readme_file:
    # ヘッダーを書き込む
    readme_file.write("# react trend news\n\n今日のreactトレンドトップ20\n\nこのランキングは毎日5時に更新されます。トレンドトップ20をお届けします。\n\n")
    top = 1
    # リポジトリのアイテムをループ処理
    for item in items:
        description = translate(item["description"])
        html_url = item["html_url"]

        # 翻訳された説明とHTML URLをファイルに書き込む
        print("processing...top" + str(top))
        readme_file.write(f"## TOP"+str(top)+f"リポジトリ: {html_url}\n\n")
        readme_file.write(f"説明: {description}\n\n")
        top += 1
print("finished!!")
