import discord
import random
import webbrowser
from bs4 import BeautifulSoup
import requests as r
import pandas as pd
p = ("Арктические льды стремительно тают. К 2040 году ожидается полное отсутствие льда в летний период.",
     "В национальном парк Глейшер, США на сегодняшний день осталось лишь 25 ледников вместо 150, которые были там в 1\
910 году.", "В связи с потеплением и загрязнением океанов, массово начали гибнуть коралловые рифы.",
     "Глобальное потепление вызывает резкие изменения погодных условий, что в последствии приводит к лесным пожарам, ан\
омальной жаре и сильным тропическим штормам по всему миру.", " В результате деятельности человека производится бо\
льшее количество углекислого газа, чем могут поглотить растения и океаны.", "Уровень моря поднялся на 17-18 см за \
последние 100 лет, эти данные превышают показатели за предыдущие 2000 лет. Повышение уровня моря несет угрозу для \
людей, живущих в прибрежных районах")
intents = discord.Intents.default()

intents.message_content = True

client = discord.Client(command_prefix='$', intents=discord.Intents.default())
response = r.get('https://news.un.org/ru/tags/globalnoe-poteplenie')
print(response)
bs = BeautifulSoup(response.text, "lxml")


def parser():
    temp = bs.find_all('h2', 'node__title')
    print(temp)
    print(f"""h2 содержит внутри себя тег <a> c ссылкой и сам текст \n
          текст самого первого заголовка: {temp[0].text}. \n
          Ссылка, которая хранится внутри: {temp[0].find('a').get('href')}""")
    dict_news = {"news": [], "links": []}

    for i in temp:
        dict_news["news"].append(i.text)
        dict_news["links"].append('https://news.un.org' + (i.find('a').get('href')))
    print(dict_news)
    df_news = pd.DataFrame(dict_news, columns=["news", "links"])
    print(df_news)
    return df_news


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.startswith('Факты о глобальном потеплении'):
        img = random.choice(p)
        await message.channel.send(img)
    elif message.content.startswith('Статья о глобальном потеплении'):
        rf = random.randint(0, 1)
        if rf:
            webbrowser.open_new('https://www.un.org/ru/climatechange/science/causes-effects-climate-change')
        elif not rf:
            webbrowser.open_new('https://ria.ru/keyword_globalnoe_poteplenie/')
    elif message.content.startswith('Насколько опасна глобальное потепление'):
        await message.channel.send(file=discord.File('мцпмц/qGuns8v-WhwP8GnUQjPLggba1c9nzsnEX0aPM-iL4I4.gif'))
    elif message.content.startswith('Новости о глобальном потеплении'):
        t = parser()
        await message.channel.send(t)
    elif message.content.startswith('Что такое глобальное потепление'):
        await message.channel.send("Глоба́льное потепле́ние — долгосрочное повышение средней температуры климатической\
        cистемы Земли, происходящее уже более века, основной причиной чего, по мнению подавляющего большинства\
        учёных, является человеческая деятельность (антропогенный фактор).")
    else:
        pass

client.run('Token')

if __name__ == '__main__':
    pass
