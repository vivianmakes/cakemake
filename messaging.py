import botuser
import discord
import imaging
import prose

async def broadcast_embed(embed, file=None):
	if file is not None:
		embed.set_image(url = 'attachment://image.png')

	await botuser.botuser.broadcast_embed(embed, file = file)


async def send_versus_message(p1, p2):
	im1 = p1.get_portrait_path()
	im2 = p2.get_portrait_path()

	n1 = p1.name
	n2 = p2.name

	d1 = '[' + str(p1.wins) + '-' + str(p1.losses) + ']' + ' - ' + p1.get_vibe_emojis()
	d2 = '[' + str(p2.wins) + '-' + str(p2.losses) + ']' + ' - ' + p2.get_vibe_emojis()

	res = imaging.get_vs_graphic(im1, im2)

	new_embed = discord.Embed(title="UP NEXT...", description="The following contestants will bake next. Use the `!cheer [part of name]` command to cheer for the contestant you want to win.", color=0xffd300)
	new_embed.add_field(name=n1, value=d1, inline=True)
	new_embed.add_field(name=n2, value=d2, inline=True)
	file = imaging.get_image_file(res)

	await broadcast_embed(new_embed, file=file)


async def send_victory_message(result):
	# IN: A result.
	desc = result.p1_details.text_event + "\n" + result.p1_details.text_decision
	desc += "\n\n" + result.p2_details.text_event + "\n" + result.p2_details.text_decision
	winner = result.winner

	graphic = imaging.get_win_graphic(result)
	desc += "\n\n*" + winner.name + "* has swayed the judges with " + winner.get_pronoun(
		'their') + " skill! ***VICTORY! :sparkles:***"

	new_embed = discord.Embed(title = "THE WINNER IS...",
							  description = desc,
							  color = 0x7aa54c)
	file = imaging.get_image_file(graphic)
	await broadcast_embed(new_embed, file=file)


async def send_inspect_message(player):
	desc = ""
	desc += "\n\n**Pronouns:** " + player.get_pronoun('they') + "/" + player.get_pronoun('them')
	desc += "\n**Wins:** " + str(player.wins)
	desc += "\n**Losses:** " + str(player.losses)
	desc += "\n**Talent:** " + player.get_talent_description()
	desc += "\n**Reliability:** " + player.get_reliability_description()
	desc += "\n**Horoscope:** " + player.get_luck_description()
	desc += "\n**Disposition:** " + player.get_disposition_description()

	im = imaging.open_image_path(player.get_portrait_path())
	file = imaging.get_image_file(im)
	new_embed = discord.Embed(title=player.name.upper(),
							  description=desc,
							  color=0x458dd6)
	new_embed.set_image(url='attachment://image.png')
	await broadcast_embed(new_embed)


async def send_error_message(in_desc):
	new_embed = discord.Embed(title = "ERROR!",
							  description = in_desc,
							  color = 0x458dd6)
	await broadcast_embed(new_embed)


async def send_general_message(title, desc, color=0x458dd6):
	new_embed = discord.Embed(title = title,
							  description = desc,
							  color = color)
	await broadcast_embed(new_embed)


async def send_elimination_message(eliminated_player):
	desc = "The judges have decided - ***"
	desc += eliminated_player.name
	desc += "*** shall be **ELIMINATED!** :x:\n"
	desc += eliminated_player.get_pronoun('they')
	desc += " will no longer be able to participate!"
	desc += "\n" + prose.random("elimination.yaml").replace("[Name]", eliminated_player.name)
	new_embed = discord.Embed(title = "ELIMINATED!",
							  description = desc,
							  color = 0x458dd6)
	await broadcast_embed(new_embed)