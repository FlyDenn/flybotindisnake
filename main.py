# coding=utf-8
import disnake
from disnake.ext import commands
from disnake.utils import *
from disnake.ui import *
from disnake.ui import Button, View, Modal, Select
import datetime
import os
from dotenv import load_dotenv


client = commands.Bot(command_prefix = '.', intents = disnake.Intents.all(), help_command = None)

@client.event
async def on_ready():
	print(f'{client.user.name}#{client.user.discriminator} готов к работе!')
	await client.change_presence(status = disnake.Status.idle, activity = disnake.Game('v23.9.22'))

# class modalHelper(Modal):
# 	def __init__(self):
# 		components = [
# 			disnake.ui.TextInput(
# 				label = 'Вашe имя', 
# 				placeholder = 'Введите ваше имя',
# 				custom_id = 'Имя',
# 				max_length = 25
# 			),
# 			disnake.ui.TextInput(
# 				label = 'Ваш возраст', 
# 				placeholder = 'Введите ваш возраст',
# 				custom_id = 'Возраст',
# 				max_length = 3
# 			),
# 			disnake.ui.TextInput(
# 				label = 'Был ли у вас опыт работы?', 
# 				placeholder = 'Введите ответ на вопрос',
# 				custom_id = 'Опыт работы',
# 				max_length = 250,
# 				style = disnake.TextInputStyle.paragraph
# 			),
# 			disnake.ui.TextInput(
# 				label = 'Расскажите немного о себе', 
# 				placeholder = 'Введите ответ на вопрос',
# 				custom_id = 'О себе',
# 				max_length = 500,
# 				style = disnake.TextInputStyle.paragraph
# 			)
# 		]

# 		super().__init__(title = 'Подача заявки на пост "Helper"', components = components)

# 	async def callback(self, inter: disnake.ModalInteraction):
# 		time = datetime.datetime.utcnow()
# 		embed = disnake.Embed(
# 			title = 'Заявка на пост "Helper"',
# 			description = f'Подал: {inter.author.mention}',
# 			color = 0x2f3136,
# 			timestamp = time
# 		)
# 		for key, value in inter.text_values.items():
# 			embed.add_field(name = key, value = f'```{value}```', inline = False)

# 		embed.set_footer(
# 			text = 'Все команды бота: /help'
# 		)

# 		await inter.response.send_message(embed=embed)
	
@client.event
async def on_button_click(inter):
	if inter.component.custom_id == 'lox':
		await inter.response.send_modal(modal=modalHelper())
	if inter.component.custom_id == 'verifButton':
		role = inter.guild.get_role(1067559841930956884)
		if role in inter.author.roles:
			await inter.response.send_message('Вы уже верифицированы!', ephemeral = True)
		else:
			await inter.author.add_roles(role)
			await inter.response.send_message('Вы успешно верифицированы!', ephemeral = True)
	if inter.component.custom_id == 'profile':
		pink = inter.guild.get_role(1068157298448547941)
		yellow = inter.guild.get_role(1068156923179962369)
		lime = inter.guild.get_role(1068157559237787739)
		green = inter.guild.get_role(1068157087416336404)
		blue = inter.guild.get_role(1068157741799059476)
		
		embed = disnake.Embed(
			color = 0x2f3136,
			title = 'Ваш профиль',
			description = '> Здесь Вы можете увидеть информацию о Ваших оповещениях и цвете никнейма.'
		)
		if pink in inter.author.roles:
			embed.add_field(name = 'Цвет никнейма', value = pink.mention)
		elif yellow in inter.author.roles:
			embed.add_field(name = 'Цвет никнейма', value = yellow.mention)
		elif lime in inter.author.roles:
			embed.add_field(name = 'Цвет никнейма', value = lime.mention)
		elif green in inter.author.roles:
			embed.add_field(name = 'Цвет никнейма', value = green.mention)
		elif blue in inter.author.roles:
			embed.add_field(name = 'Цвет никнейма', value = blue.mention)
		else:
			embed.add_field(name = 'Цвет никнейма', value = '``Отсутствует``')

		news = inter.guild.get_role(1068156281887658024)
		videos = inter.guild.get_role(1068156170570833921)
		joinUser = f'{disnake.utils.format_dt(inter.author.joined_at)}'

		if (news in inter.author.roles) and (videos in inter.author.roles):
			embed.add_field(name = 'Оповещения', value = f'{news.mention} / {videos.mention}')
		elif news in inter.author.roles:
			embed.add_field(name = 'Оповещения', value = f'{news.mention}')
		elif videos in inter.author.roles:
			embed.add_field(name = 'Оповещения', value = f'{videos.mention}')
		else:
			embed.add_field(name = 'Оповещения', value = '``Отсутствуют``')

		embed.add_field(name = 'Вы присоединились', value = joinUser )
		embed.set_thumbnail(
			url = inter.author.display_avatar.url
		)

		clearColor = Button(
			label = 'Убрать цвет',
			style = disnake.ButtonStyle.red
		)
		clearBroadcast = Button(
			label = 'Убрать оповещения',
			style = disnake.ButtonStyle.red
		)

		view = View()
		view.add_item(clearColor)
		view.add_item(clearBroadcast)

		async def color_callback(inter):
			await inter.author.remove_roles(pink, yellow, lime, green, blue)
			await inter.response.send_message('Цвет никнейма успешно убран!', ephemeral = True)

		async def broadcast_callback(inter):
			await inter.author.remove_roles(news, videos)
			await inter.response.send_message('Оповещения успешно убраны!', ephemeral = True)

		clearColor.callback = color_callback
		clearBroadcast.callback = broadcast_callback

		await inter.response.send_message(embed = embed, view = view, ephemeral = True)

@client.event
async def on_dropdown(inter):
	if inter.component.custom_id == 'rolesGiver':
		pink = inter.guild.get_role(1068157298448547941)
		yellow = inter.guild.get_role(1068156923179962369)
		lime = inter.guild.get_role(1068157559237787739)
		green = inter.guild.get_role(1068157087416336404)
		blue = inter.guild.get_role(1068157741799059476)
		if inter.values[0] == 'Розовый':
			await inter.response.defer()
			await inter.author.remove_roles(pink, yellow, lime, green, blue)
			await inter.author.add_roles(pink)
		elif inter.values[0] == 'Жёлтый':
			await inter.response.defer()
			await inter.author.remove_roles(pink, yellow, lime, green, blue)
			await inter.author.add_roles(yellow)
		elif inter.values[0] == 'Лаймовый':
			await inter.response.defer()
			await inter.author.remove_roles(pink, yellow, lime, green, blue)
			await inter.author.add_roles(lime)
		elif inter.values[0] == 'Зелёный':
			await inter.response.defer()
			await inter.author.remove_roles(pink, yellow, lime, green, blue)
			await inter.author.add_roles(green)
		elif inter.values[0] == 'Голубой':
			await inter.response.defer()
			await inter.author.remove_roles(pink, yellow, lime, green, blue)
			await inter.author.add_roles(blue)
	if inter.component.custom_id == 'broadcastRoles':
		news = inter.guild.get_role(1068156281887658024)
		videos = inter.guild.get_role(1068156170570833921)
		if inter.values[0] == 'Новости':
			if news in inter.author.roles:
				await inter.response.send_message(f'У Вас уже установлено это оповещение!', ephemeral = True)
			else:
				await inter.response.send_message(f'<:point:1068220992746430534> **Вы выбрали:** {news.mention}\n> Теперь мимо Вас не проскочит ни одна важная новость! Отключить оповещение можно через свой профиль.', ephemeral = True)
				await inter.author.add_roles(news)
		elif inter.values[0] == 'Видео':
			if videos in inter.author.roles:
				await inter.response.send_message(f'У Вас уже установлено это оповещение!', ephemeral = True)
			else:
				await inter.response.send_message(f'<:point:1068220992746430534> **Вы выбрали:** {videos.mention}\n> Теперь Вы не пропустите ни одного видео от наших ютуберов! Отключить оповещение можно через свой профиль.', ephemeral = True)
				await inter.author.add_roles(videos)

@client.slash_command(name = 'roles', description = 'Установить роли')
async def roles(inter, channel: disnake.TextChannel = commands.Param(description = 'Укажите канал')):
	if inter.author.id != 760739749009948682:
		return await inter.response.send_message('Вы не можете использовать это!', ephemeral = True)
	# role0 = inter.guild.get_role(1067872197613465681)
	# role1 = inter.guild.get_role(1067557922525171773)

	# if (role0 in inter.author.roles) and (role1 in inter.author.roles):
	# 	await inter.send(f'{role0.mention} / {role1.mention}')
	# elif role0 in inter.author.roles:
	# 	await inter.send(f'{role0.mention}')
	# elif role1 in inter.author.roles:
	# 	await inter.send(f'{role1.mention}')
	# else:
	# 	await inter.send('**отсутствуют**')

	colors = Select(
		placeholder = 'Выберите цвет',
		custom_id = 'rolesGiver',
		options = [
			disnake.SelectOption(
				label = 'Розовый',
				emoji = '<:pink:1068229849795285053>'
			),
			disnake.SelectOption(
				label = 'Жёлтый',
				emoji = '<:yellow:1068229852118913034>'
			),
			disnake.SelectOption(
				label = 'Лаймовый',
				emoji = '<:lime:1068229847261904966>'
			),
			disnake.SelectOption(
				label = 'Зелёный',
				emoji = '<:green:1068229845550641244>'
			),
			disnake.SelectOption(
				label = 'Голубой',
				emoji = '<:blue:1068229842442653869>'
			)
		]
	)

	broadcast = Select(
		placeholder = 'Выберите оповещение',
		custom_id = 'broadcastRoles',
		options = [
			disnake.SelectOption(
				label = 'Новости',
				emoji = '📝'
			),
			disnake.SelectOption(
				label = 'Видео',
				emoji = '📷'
			)
		]
	)

	profile = Button(
		style = disnake.ButtonStyle.gray,
		label = 'Открыть профиль',
		custom_id = 'profile'
	)

	view = View()
	view.add_item(colors)

	broad = View()
	broad.add_item(broadcast)

	prof = View()
	prof.add_item(profile)

	await channel.send(file = disnake.File('./assets/roles.png'))
	await channel.send(
		content = '> В этом канале **Вы** сможете ознакомиться со всеми ролями на сервере, настроить свой **профиль** чтобы выделятся среди других. Изменить **цвет** никнейма и выбрать желаемые **оповещения**, чтобы ничего не пропускать.\n\n<:point3:1068220992746430534> **Цвета**\n> На нашем сервере есть возможно изменить **цвет** Вашего никнейма. Если Вы устали от однотипного цвета, который уже вам надоел, то смените его скорей! Здесь есть выбор из **целых пяти** видов цветов. Станьте **особенным** :3 ',
		view = view
	)
	await channel.send(
		content = '<:point3:1068220992746430534> **Оповещения**\n> В списке ниже Вы можете выбрать, какие оповещения хотите получать. Вы можете выбрать несколько оповещений. В зависимости от Вашего выбора, Вам будут приходить уведомления о новостях, новых роликах и т.п. Всё решаете именно Вы.',
		view = broad
	)
	await channel.send(
		content = '> Вы можете посмотреть свой профиль, нажав на кнопку под сообщением :3',
		view = prof
	)

@client.slash_command(name = 'verif', description = 'Установить верификацию')
async def verif(inter, channel: disnake.TextChannel = commands.Param(description = 'Укажите канал')):
	if inter.author.id != 760739749009948682:
		return await inter.response.send_message('Вы не можете использовать это!', ephemeral = True)

	embed = disnake.Embed(
		title = 'Верификация',
		description = 'Нажми на кнопку',
		color = 0x2f3136
	)
	button = Button(
		label = 'Верифицироваться',
		emoji = '<:active:1067879501494755428>',
		style = disnake.ButtonStyle.gray,
		custom_id = 'verifButton'
	)

	view = View()
	view.add_item(button)

	await channel.send(
		file = disnake.File('./assets/verif.png')
	)
	await channel.send(
		content = '<:point:1068220992746430534> Приветствуем **Вас** на сервере **FB community**!\n\n> На нашем сервере **Вы** найдете много позитивных и добродушных участников, с которыми **Вы** можете подружиться.\n\n> Здесь рады **Всем**! Но перед началом общения **Вам** нужно пройти верификацию. В этом нет ничего сложно, просто нажмите на кнопку под сообщением.\n\n> Нажимая на кнопку, **Вы** также соглашаетесь с правилами нашего сервера и обязуетесь их выполнять, в ином случае последуют наказания.\n\n__С уважением, Администрация сервера FB community__\n', 
		view = view
	)
	await inter.response.send_message('тест', ephemeral = True)

@client.slash_command(name = 'anument', description = 'Установить анументы')
async def anument(inter, channel: disnake.TextChannel = commands.Param(description = 'Укажите канал')):
	if inter.author.id != 760739749009948682:
		return await inter.response.send_message('Вы не можете использовать это!', ephemeral = True)

	await channel.send(
		file = disnake.File('./assets/anuments.png')
	)
	await channel.send(
		content = '\n> **Анументы** - это событие, которое проходит **1 раз в месяц**. Во время него **Вы** сможете оценить работу наших сотрудников как с **хорошей **стороны, так и с **плохой**.\n\n<:point:1068220992746430534> Во время оценки будьте **внимательны** и **честны**!\n\n> Сотрудник, набравший больше всего **положительных оценок**, будет автоматически **повышен.**\n\n> Сотруднику, набравшему больше всего **отрицательных оценок**, будет выдано **2 выговора**.\n\n<:point:1068220992746430534> Как и другие события, **анументы** имеют свои правила:\n\n`1.` Запрещено голосовать за самого себя.\n__Наказание:__ `1 выговор`\n\n`2.` Запрещено сговариваться / подкупать участников против другого сотрудника.\n__Наказание:__ `Снятие`\n\n__С уважением, Администрация сервера FB community__\n',
	)

#load_dotenv()
#TOKEN = os.getenv('TOKEN')
client.run('MTAyMDMyNTA2OTMwMzU4Mjc5NQ.GNg0Zr.Ev7qGkwH7w7YoDlb7AKAruDbZuyslx2XR2CgyU')