import discord
from discord.ext import commands	#Библиотеки для написания Discord-Бота
from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio
token = "yourtoken"
bot = commands.Bot(command_prefix = "!") #Префикс
ban_words = ['окрошка', 'пицца', 'борщ', 'бутерброд', 'сало', 'макароны', 'суши', 'роллы'] #Бан ворды
#Статус и включение бота
@bot.event #Новая команда
async def on_ready(): #Бот готов
	print("Бот включён!")
	await bot.change_presence(status=discord.Status.online, activity=discord.Game('!хелп')) #Статус бота
#Команда !привет
@bot.command(pass_context=True)
async def привет(ctx):
	await ctx.author.send("Привет, {}".format(ctx.message.author.mention)) #Отправит в ЛС
#Команда !хелп и её содержание
@bot.command(pass_context=True) #Новая команда
async def хелп(ctx,*args): #"Распаковка" аргументов
	helpcom = discord.Embed(title = "Навигация по командам", colour = discord.Color.green()) #Цвет
	helpcom.add_field(name = "!привет", value = "Получение привета✋") #Мини-Отступ и надпись в нем
	helpcom.add_field(name = "!бан", value = "Ограничение доступа к серверу🚫")
	helpcom.add_field(name = "!кик", value = "Удаление участника с сервера🚷")
	helpcom.add_field(name = "!очистка", value = "Очистка выбранного чата📦")
	helpcom.add_field(name = "!мут", value = "Ограничение на общение🔈")
	helpcom.add_field(name = "!всеовшп", value = "Соц. сети ВШП💻")
	helpcom.set_footer(text = "Все команды сделаны для администратора вашего сервера")
	await ctx.send(embed = helpcom)  #Отправит то что мы написали выше
#Команда !кик
@bot.command(pass_context=True) #Новая команда
@commands.has_permissions(administrator=True)  #Этой командой может пользоваться только админ
async def кик(ctx, member:discord.Member,*,reason=None):	#Кик без причины
	kickemb = discord.Embed(title = "Кик", colour = discord.Color.blue()) #Цвет
	await ctx.channel.purge(limit = 1) #Команда удалится после написания
	await member.kick(reason=reason) #Осуществление кика
	kickemb.set_author(name = member.name, icon_url = member.avatar_url) #Никнейм и аватарка кикнутого
	kickemb.add_field(name = "Кикнут за нарушение прав сервера", value = "Кикнутый участник : {}".format(member.mention)) #Тег кикнутого
	await ctx.send(embed = kickemb) #Отправит то что мы написали выше
#Команда !бан
@bot.command(pass_context=True) #Новая команда
@commands.has_permissions(administrator=True) #Этой командой может пользоваться только админ
async def бан(ctx, member:discord.Member,*,reason=None):	#Бан без причины
	emb = discord.Embed(title = "Бан", colour = discord.Color.red()) #Цвет
	await ctx.channel.purge(limit = 1) #Команда удалится после написания
	await member.ban(reason=reason) #Осуществление бана
	emb.set_author(name = member.name, icon_url = member.avatar_url) #Никнейм и аватарка забаненного
	emb.add_field(name = "Бан был получен за нарушение правил сервера", value = "Забаненный участник : {}".format(member.mention)) #Тег забаненного
	await ctx.send(embed = emb) #Отправит то что мы написали выше
#Команда !очистка 
@bot.command(pass_context = True) #Новая команда
@commands.has_permissions( administrator = True)  #Этой командой может пользоваться только админ
async def очистка(ctx,amount = 100): #Удалится 100 сообщений
    await ctx.channel.purge(limit = amount)
#Команда !мут (на 1 час) / присутствует настройка времени на мут в секундах
@bot.command(pass_context=True) #Новая команда
@commands.has_permissions(administrator=True) #Этой командой может пользоваться только админ
async def мут(ctx,member:discord.Member):	#Взаимодействие с пользователем
	await ctx.channel.purge(limit = 1) #Команда удалится после написания
	mute = discord.utils.get(ctx.message.guild.roles,name="mute") #Взаимодействие с командой мута
	await member.add_roles(mute) #Даст роль мута
	await ctx.send(f'{member.mention} был замучен на 1 час') #Тег замученного участника 
	await asyncio.sleep(3600) #Пройдёт час - участник размутится
	await member.remove_roles(mute) #Снять роль когда пройдет час
#Фильтр чата (бан ворды в ban_words) / присутствует настройка запрещенных на сервере слов
@bot.event #Новая команда
async def on_message(message): #Читает сообщения
	await bot.process_commands(message) #Всегда проверяет сообщения
	msg = message.content.lower() #Превращение слов в нижний регистр 
	if msg in ban_words: #Если слово есть в бан ворде, то:
		await message.delete() #Удалит бан ворд
		await message.author.send( f'{message.author.name}, такие слова на данном сервере запрещены!') #Напишет в ЛС о предупреждении
#Команда !всеовшп / соц. сети ВШП / использование новой функцией Discord - Кнопки
@bot.command() #Новая команда
async def всеовшп(ctx):
	await ctx.send(
		embed=discord.Embed(title="🔴📣**Всё о ВШП**📣🔴"), #Надпись
		components=[
			Button(style=ButtonStyle.URL, label="🖥️Оффициальный сайт", url="https://it-proger.com"), #Стиль кнопок
			Button(style=ButtonStyle.URL, label="🌍ВКонтакте", url="https://vk.com/school_programmistov"),
			Button(style=ButtonStyle.URL, label="✈️ Телеграм", url="https://t.me/it_proger_com")
		]
	)
bot.run(token) #Включение бота
