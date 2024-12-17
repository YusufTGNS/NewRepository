import discord
import random
from discord.ext import commands
from config import token  # Botun tokenini config dosyasından içe aktarma

intents = discord.Intents.default()
intents.members = True  # Botun kullanıcılarla çalışmasına ve onları banlamasına izin verir
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı:  {bot.user.name}')

@bot.command()
async def start(ctx):
    await ctx.send("Merhaba! Ben bir sohbet yöneticisi botuyum!")

@bot.command(name="yazitura")
async def yazitura(ctx, tahmin: str):
    # Geçerli giriş kontrolü
    if tahmin.lower() not in ["yazı", "tura"]:
        await ctx.send("Lütfen 'yazı' veya 'tura' seç!")
        return

    # Yazı-Tura sonucu
    sonuc = random.choice(["yazı", "tura"])

    # Kazanıp kazanmadığını kontrol et
    if tahmin.lower() == sonuc:
        await ctx.send(f"Tebrikler! **{sonuc}** geldi. Kazandın! 🎉")
    else:
        await ctx.send(f"Maalesef, **{sonuc}** geldi. Kaybettin. 😢")


#git reset --hard origin/main
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı banlamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanızı {member.name} banlandı")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `!ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")

bot.run(token)