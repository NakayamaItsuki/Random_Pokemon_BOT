import discord
import random
import requests
from PIL import Image
from io import BytesIO

# Discordボットのトークン
TOKEN = "YOUR TOKEN HERE"

# Discordクライアントを作成します。
intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

# ログインした時にコマンドラインに通知する
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

# メインの処理
@client.event
async def on_message(message):
    
    # メッセージの送信者がボット自体の場合は無視
    if message.author == client.user:
        return

    # botがメンションされた場合
    if client.user in message.mentions:
        
        # ポケモンの総数，新たにポケモンが追加された場合はここを変更
        total_pokemon = 1010

        # ランダムなポケモンの番号を生成
        random_pokemon_id = random.randint(1, total_pokemon)

        # Pokemon APIを使用して，番号に対応するポケモンのデータを取得
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{random_pokemon_id}"
        pokemon_response = requests.get(pokemon_url)
        pokemon_data = pokemon_response.json()
        
        # ポケモンの名前（英語名と日本語名）を取得
        english_name = pokemon_data["name"]

        species_url = pokemon_data["species"]["url"]
        species_response = requests.get(species_url)
        species_data = species_response.json()
        
        japanese_name = "不明"  # 日本語名が見つからない場合のデフォルト値
        for name_info in species_data["names"]:
            if name_info["language"]["name"] == "ja":
                japanese_name = name_info["name"]
                break
            
        # ポケモンの画像URLを取得
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{random_pokemon_id}.png"

        # 画像をダウンロードしてDiscordに送信
        sprite_response = requests.get(sprite_url)
        image_data = BytesIO(sprite_response.content)
        image = Image.open(image_data)
        image = image.resize((image.width * 3, image.height * 3))
        
        image_path = "random_pokemon.png" # 画像を一時的に保存する場所
        image.save(image_path)

        await message.channel.send(f"日本語名: {japanese_name}")
        await message.channel.send(f"英語名: {english_name}")
        await message.channel.send(file=discord.File(image_path))

if __name__ == "__main__":
    client.run(TOKEN)
