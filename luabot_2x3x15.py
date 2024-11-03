import discord
import random
import uuid
import requests
from discord import Guild, app_commands
from discord.utils import get
from datetime import datetime
from datetime import date, timedelta
from discord.ui import Button, View
from discord import ui
from discord.ext import commands
import json
import tempfile

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f'{self.user}이 시작되었습니다') #  봇이 시작하였을때 터미널에 뜨는 말
        game = discord.Game('LUABOT Ver.ㅣ2.4.15') # 'LUABOT Ver.ㅣNone'
        await self.change_presence(status=discord.Status.online, activity=game)

client = aclient()
tree = app_commands.CommandTree(client)
punishment_path = 'punishment.json'
account_path = 'account.json'
license_path = 'license.json'
purchase_path = 'purchase.json'

#unishment_path = r'C:\Users\helloworld\Desktop\Discord_Work\LUA_Studio\LUABOT\Data\punishment.json'
#account_path = r'C:\Users\helloworld\Desktop\Discord_Work\LUA_Studio\LUABOT\Data\account.json'
#license_path = r'C:\Users\helloworld\Desktop\Discord_Work\LUA_Studio\LUABOT\Data\license.json'
#purchase_path = r'C:\Users\helloworld\Desktop\Discord_Work\LUA_Studio\LUABOT\Data\purchase.json'

errorembed = discord.Embed(title="ERROR", description="해당 명령어를 사용할 수 있는 권한이 없습니다ㅣYou don't have permission to use that command", color=0xeb9534)
errorembed.set_footer(text="made by BINI in FICES™")

bot_token = 'MTI0NTI3NDM0NzE4NzQ3NDUxNQ.GkBqMh.XifIebPaGKBzrRfD1NjuD3aLBzgDqEPwyMYXEc'

def get_invite_expiration(invite_code, bot_token):
    url = f"https://discord.com/api/v10/invites/{invite_code}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        invite_info = response.json()
        expires_at = invite_info.get('expires_at')
        if expires_at is None:
            return 'Unlimited'
        return expires_at
    else:
        return "Error fetching expiration"

def get_server_name_from_id(server_id, bot_token):
    url = f"https://discord.com/api/v10/guilds/{server_id}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        guild_info = response.json()
        server_name = guild_info['name']
        return server_name
    else:
        return None

def get_server_name_from_invite(invite_code, bot_token):
    url = f"https://discord.com/api/v10/invites/{invite_code}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        invite_info = response.json()
        server_name = invite_info['guild']['name']
        return server_name
    else:
        return None

def get_group_name(group_id):
    group_url = f"https://groups.roblox.com/v1/groups/{group_id}"
    response = requests.get(group_url)
    
    if response.status_code != 200:
        return None

    data = response.json()
    
    if 'errors' in data:
        return None

    return data['name']

def get_roblox_group_owner_id(group_id):
    url = f"https://groups.roblox.com/v1/groups/{group_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        group_data = response.json()
        owner = group_data.get("owner")
        if owner:
            return owner.get("userId", "Owner ID not available")
        else:
            return "Owner information not available"
    else:
        return f"Failed to get group information. Status code: {response.status_code}"

def get_roblox_user_id(username):
    url = f"https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username]}
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    
    if 'data' in data and len(data['data']) > 0:
        return data['data'][0]['id']
    else:
        return None

def get_user_description(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('description', 'No description available.')
    else:
        return f"Failed to retrieve information for user ID {user_id}. Status code: {response.status_code}"
        
def get_username_from_user_id(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('name', 'No name available.')
    else:
        return f"Failed to retrieve information for user ID {user_id}. Status code: {response.status_code}"

def get_server_id_from_invite(invite_code, bot_token):
    url = f"https://discord.com/api/v10/invites/{invite_code}"
    headers = {
        "Authorization": f"Bot {bot_token}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        invite_info = response.json()
        server_id = invite_info['guild']['id']
        return server_id
    else:
        return None

class license_modal(ui.Modal, title = "라이센스 등록"):
    serverinvite = ui.TextInput(label = "서버 초대코드", style = discord.TextStyle.short, required = True, max_length = 18)
    groupid = ui.TextInput(label = "그룹 아이디", style = discord.TextStyle.short, placeholder='EX) 0000000', required = True, max_length = 18)
    async def on_submit(self, interaction: discord.Interaction):
        with open(account_path, 'r', encoding='utf-8') as file:
            accountdata = json.load(file)
        with open(license_path, 'r', encoding='utf-8') as file:
            licensedata = json.load(file)
        groupname = get_group_name(self.groupid)
        if groupname:
            expiration = get_invite_expiration(self.serverinvite, bot_token)
            serverid = get_server_id_from_invite(self.serverinvite, bot_token)
            servername = get_server_name_from_invite(str(self.serverinvite), bot_token)
            groupownerid = get_roblox_group_owner_id(self.groupid)
            role = get(interaction.guild.roles, id=1248085227553685526)
            if not serverid or expiration == "Error fetching max uses" or not servername:
                embed = discord.Embed(title="ERROR", description="서버 정보를 가져오는 도중 오류가 발생했습니다. \n루아봇오피스에 문의하세요.", color=0xeb9534)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if expiration != 'Unlimited':
                embed = discord.Embed(title="ERROR", description="만료기간과 제한인원이 모두 무제한인 초대코드를 입력해주세요.", color=0xeb9534)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if not str(interaction.user.id) in accountdata:
                embed = discord.Embed(title="ERROR", description="서버장의 회원가입이 필요합니다.", color=0xeb9534)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if str(interaction.user.id) in licensedata:
                embed = discord.Embed(title="ERROR", description="유저는 두개 이상의 라이센스 서버를 소유할 수 없습니다.", color=0xeb9534)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            if not int(groupownerid) == int(accountdata[str(interaction.user.id)][2]):
                embed = discord.Embed(title="ERROR", description="그룹장이 아닙니다.", color=0xeb9534)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            now = datetime.now()
            adminlog = client.get_channel(1243139947624529961)
            date = '{}-{}-{}'.format(now.year, f'{now.month:02d}', f'{now.day:02d}')
            num = '{}{}-{}-{}-{}'.format(f'{now.month:02d}', f'{now.day:02d}', now.year, f'{len(licensedata)+1:02d}', f'{random.randint(0, 999999999999):012}')
            logembed = discord.Embed(title="ADD LICENSE", description="라이센스가 등록되었습니다.", color=0xeb9534)
            logembed.add_field(name="서버명(서버 직행)", value="[{}](https://discord.gg/{})".format(servername, self.serverinvite))
            logembed.add_field(name="서버장", value="{}".format(interaction.user.mention))
            logembed.add_field(name="서버 아이디", value="{}".format(serverid))
            logembed.add_field(name="그룹명(그룹 직행)", value="[{}](https://www.roblox.com/groups/{})".format(groupname, self.groupid), inline=False)
            logembed.add_field(name="그룹오너", value="{}".format(get_username_from_user_id(groupownerid)))
            logembed.add_field(name="그룹 아이디", value="{}".format(self.groupid))
            logembed.add_field(name="서버 초대코드", value="{}".format(self.serverinvite), inline=False)
            logembed.add_field(name="가입날짜", value="{}".format(date))
            logembed.add_field(name="고유번호", value="**`{}`**".format(num))
            logembed.set_footer(text="made by BINI in FICES™")
            embed = discord.Embed(title="COMPLETE", description="이제부터 아래 서버는 루아스튜디오 라이센스 소유 서버입니다.", color=0xeb9534)
            embed.add_field(name="서버명", value="{}".format(servername), inline=False)
            embed.add_field(name="서버장", value="{} ({})".format(interaction.user.mention, interaction.user.id), inline=False)
            embed.add_field(name="서버 아이디", value="{}".format(serverid), inline=False)
            embed.add_field(name="서버 초대코드", value="{}".format(self.serverinvite), inline=False)
            embed.add_field(name="그룹명", value="{}".format(groupname), inline=False)
            embed.add_field(name="라이센스 고유번호", value="**`{}`**".format(num), inline=False)
            embed.set_footer(text="made by BINI in FICES™")
            licensedata[str(interaction.user.id)] = [str(serverid), str(self.groupid), str(self.serverinvite), date, num]
            with open(license_path, 'w', encoding='utf-8') as file:
                json.dump(licensedata, file, ensure_ascii=False, indent=4)
            await interaction.user.add_roles(roles=role)
            await adminlog.send(embed=logembed)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="ERROR", description="그룹이 존재하지 않습니다.", color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
            await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name = 'ban', description = '유저를 서버에서 차단합니다.')
@app_commands.describe(대상='차단할 유저를 선택하세요', 사유='차단 사유를 입력하세요')
async def slash2(interaction: discord.Interaction, 대상: discord.Member, 사유:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    with open(account_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if data[str(interaction.user.id)][2]:
        대상로블닉 = data[str(interaction.user.id)][2]
    else:
        대상로블닉 = '정보를 가져올수 없음.(비회원)'
    if interaction.user.guild_permissions.administrator:
        log = client.get_channel(1205218949759893626)
        blacklist = client.get_channel(1205237194009092126)
        logembed = discord.Embed(title="BAN", description="{}님이 {}님을 서버에서 차단하였습니다.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        dmembed = discord.Embed(title="LUA BOT MESSAGE", description="[Web 발신][LUA BOT]\n귀하께서는 **`{}`**로 인하여 서버에서 차단당하셨습니다. 이의제기는 DVNC™입장 후에 가능합니다.".format(사유), color=0xeb9534)
        dmembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="COMPLETE", description="{}님이 서버에서 차단되었습니다. \n증거물을 게시해야할 경우 <#1205237194009092126> 로 이동해주세요.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        banembed = discord.Embed(title="BLACKLIST", description="아래 인원이 블랙리스트로 배정되었습니다.", color=0xeb9534)
        banembed.add_field(name="멤버", value="**`{}`**".format(대상.mention), inline=False)
        banembed.add_field(name="로블록스 닉네임", value="**`{}`**".format(대상로블닉), inline=False)
        banembed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
        banembed.set_footer(text="made by BINI in FICES™")
        await 대상.send()
        await 대상.ban(reason=사유)
        await log.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await blacklist.send(embed=banembed)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'kick', description = '유저를 서버에서 추방합니다.')
@app_commands.describe(대상='추방할 유저를 선택하세요', 사유='추방 사유를 입력하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member, 사유:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    with open(account_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if data[str(interaction.user.id)][2]:
        대상로블닉 = data[str(interaction.user.id)][2]
    else:
        대상로블닉 = '정보를 가져올수 없음.(비회원)'
    if interaction.user.guild_permissions.administrator:
        log = client.get_channel(1205218949759893626)
        banlist = client.get_channel(1205237261218750505)
        logembed = discord.Embed(title="KICK", description="{}님이 {}님을 서버에서 추방하였습니다.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="COMPLETE", description="{}님이 서버에서 추방되었습니다. \n증거물을 게시해야할 경우 <#1205237261218750505> 으로 이동해주세요.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        banembed = discord.Embed(title="KICK", description="아래 인원이 추방되었습니다.", color=0xeb9534)
        banembed.add_field(name="멤버", value="**`{}`**".format(대상.mention), inline=False)
        banembed.add_field(name="로블록스 닉네임", value="**`{}`**".format(대상로블닉), inline=False)
        banembed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
        banembed.set_footer(text="made by BINI in FICES™")
        dmembed = discord.Embed(title="LUA BOT MESSAGE", description="[Web 발신][LUA BOT]\n귀하께서는 아래 사유로 인하여 루아스튜디오 서버에서 추방당하셨습니다. 이의제기는 DVNC™ 입장 후 부탁드립니다.", color=0xeb9534)
        dmembed.add_field(name="멤버", value="**`{}`**".format(대상.mention), inline=False)
        dmembed.set_footer(text='LuaStudio CO. 드림.ㅣmade by BINI in FICES™')
        await 대상.send(embed=dmembed)
        await 대상.kick(reason=사유)
        await log.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await banlist.send(embed=banembed)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'message', description = '사용자 설정 메시지를 보냅니다.')
@app_commands.describe(대상='메시지를 받을 유저를 선택하세요', 메시지='대상에게 보낼 메시지를 입력하세요', 파일='대상에게 보낼 파일을 업로드하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member, 메시지:str, 파일: discord.Attachment = None):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="ADMIN MESSAGE", description="{}님이 {}님에게 메시지를 보냈습니다.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        logembed.add_field(name="내용", value="**`{}`**".format(메시지), inline=False)
        if 파일:
            logembed.add_field(name="파일", value="**`{}`**".format(파일.filename), inline=False)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="COMPLETE", description="{}님에게 메시지를 보냈습니다.".format(대상), color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        msgembed = discord.Embed(title="LUA MANAGER MESSAGE", description="{}".format(메시지), color=0xeb9534)
        msgembed.set_footer(text="LuaStudio CO. 드림.ㅣmade by BINI in FICES™")
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        if 파일:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                await 파일.save(temp_file.name)  # 파일을 임시 경로에 저장
                file = discord.File(temp_file.name, filename=파일.filename)
                await 대상.send(embed=msgembed, file=file)
        else:
            await 대상.send(embed=msgembed)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = '본인경고조회', description = '본인의 경고 횟수를 조회합니다.')
async def slash2(interaction: discord.Interaction):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    with open(punishment_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    adminlog = client.get_channel(1243139947624529961)
    logembed = discord.Embed(title="WARNING VIEW", description="{}님이 본인의 경고를 조회했습니다.".format(interaction.user.mention), color=0xeb9534)
    logembed.set_footer(text="made by BINI in FICES™")
    memberid = '{}'.format(interaction.user.id)
    if memberid in data:
        embed = discord.Embed(title="경고 {}회".format(data[memberid]), description="당신 ( {} ) 은 {}회의 경고를 소유하고 있습니다.".format(interaction.user.mention, data[memberid]), color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
    else:
        embed = discord.Embed(title="경고 없음", description="당신( {} ) 은 경고를 소유하고 있지 않습니다.".format(interaction.user.mention), color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
    await adminlog.send(embed=logembed)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name = 'warnview', description = '특정 멤버의 경고 횟수를 조회합니다.')
@app_commands.describe(대상='조회할 유저를 선택하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        with open(punishment_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="MEMBER WARNING VIEW", description="{}님이 {}의 경고를 조회했습니다.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        memberid = '{}'.format(대상.id)
        if memberid in data:
            embed = discord.Embed(title="경고 {}회".format(data[memberid]), description="해당 멤버 ( {} ) 는 {}회의 경고를 소유하고 있습니다.".format(대상.mention, data[memberid]), color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
        else:
            embed = discord.Embed(title="경고 없음", description="해당 멤버( {} ) 는 경고를 소유하고 있지 않습니다.".format(대상.mention), color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'addwarns', description = '특정 멤버에게 경고를 부여합니다.')
@app_commands.describe(대상='경고를 부여할 유저를 선택하세요', 횟수 = '부여할 경고의 횟수를 입력하세요', 사유='경고부여 사유를 입력하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member, 횟수: int, 사유:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        with open(punishment_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="MEMBER WARNING GIVE", description="{}님이 {}에게 경고를 {}회 부여했습니다.".format(interaction.user.mention, 대상.mention, 횟수), color=0xeb9534)
        logembed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
        logembed.set_footer(text="made by BINI in FICES™")
        memberid = '{}'.format(대상.id)
        if memberid in data:
            data[memberid] += 횟수
            embed = discord.Embed(title="COMPLETE".format(data[memberid]), description="해당 멤버 ( {} ) 는 {}회의 경고를 소유하고 있습니다.({} -> {})".format(대상.mention, data[memberid], data[memberid] - 횟수, data[memberid]), color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
        else:
            data[memberid] = 횟수
            embed = discord.Embed(title="COMPLETE".format(data[memberid]), description="해당 멤버 ( {} ) 는 {}회의 경고를 소유하고 있습니다.({} -> {})".format(대상.mention, data[memberid], data[memberid] - 횟수, data[memberid]), color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
        if data[memberid] >= 5:
            embed = discord.Embed(title="COMPLETE".format(data[memberid]), description="해당 멤버 ( {} ) 는 {}회(5회 이상)의 경고를 소유하게 되었으므로 자동 추방됩니다.({} -> {})".format(대상.mention, data[memberid], data[memberid] - 횟수, data[memberid]), color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
            data[memberid] = 0
            대상.kick(reason='경고 누적ㅣ마지막 경고 사유: {}'.format(사유))
        with open(punishment_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        dmembed = discord.Embed(title="LUA BOT MESSAGE", description="[Web 발신][LUA BOT]\n귀하께서는 **`{}`**로 인하여 경고 {}회를 부여받으셨습니다.\n이로써 총 경고 수는 {}개 입니다.({}->{})\n안전한 쇼핑 되시기 바랍니다. 감사합니다.".format(사유, 횟수, data[memberid], data[memberid] - 횟수, data[memberid]), color=0xeb9534)
        dmembed.set_footer(text="LuaStudio CO. 드림.ㅣmade by BINI in FICES™")
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await 대상.send(embed=dmembed)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'editwarns', description = '특정 멤버의 경고를 수정합니다.')
@app_commands.describe(대상='경고를 수정할 유저를 선택하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member, 횟수: int, 사유:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        with open(punishment_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="MEMBER WARNING EDIT", description="{}님이 {}의 경고를 {}회로 수정하였습니다.".format(interaction.user.mention, 대상.mention, 횟수), color=0xeb9534)
        logembed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
        logembed.set_footer(text="made by BINI in FICES™")
        memberid = '{}'.format(대상.id)
        data[memberid] = 횟수
        embed = discord.Embed(title="COMPLETE".format(data[memberid]), description="해당 멤버 ( {} ) 는 {}회의 경고를 소유하고 있습니다.({} -> {})".format(대상.mention, data[memberid], data[memberid] - 횟수, data[memberid]), color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        if data[memberid] >= 5:
            embed = discord.Embed(title="COMPLETE".format(data[memberid]), description="해당 멤버 ( {} ) 는 {}회(5회 이상)의 경고를 소유하게 되었으므로 자동 추방됩니다.({} -> {})".format(대상.mention, data[memberid], data[memberid] - 횟수, data[memberid]), color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
            data[memberid] = 0
        with open(punishment_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        dmembed = discord.Embed(title="LUA BOT MESSAGE", description="[Web 발신][LUA BOT]\n귀하께서는 `**{}**`로 인하여 경고 {}회를 수정받으셨습니다.\n이로써 현재 경고 수는 {}개 입니다.({}->{})\n안전한 쇼핑 되시기 바랍니다. 감사합니다.".format(사유, 횟수, data[memberid], data[memberid] - 횟수, data[memberid]), color=0xeb9534)
        dmembed.set_footer(text="LuaStudio CO. 드림.ㅣmade by BINI in FICES™")
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await 대상.send(embed=dmembed)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = '회원가입', description = '루아스튜디오 회원이 되어보세요.')
@app_commands.describe(로블록스닉네임='당신의 로블록스 닉네임을 입력해주세요')
async def slash2(interaction: discord.Interaction, 로블록스닉네임:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    with open(account_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    log = client.get_channel(1205218949759893626)
    verifycode = f"{random.randint(0, 999999):06d}"
    if __name__ == "__main__":
        username = 로블록스닉네임
        user_id = get_roblox_user_id(username)
        roof = True
        memberid = '{}'.format(interaction.user.id)
        if user_id:
            if memberid in data:
                rbxname = get_username_from_user_id(int(data[memberid][2]))
                embed = discord.Embed(title="ERROR", description="이미 회원으로 등록되어 있습니다. 복귀자인 경우 자동 회원 처리되었습니다.", color=0xeb9534)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                mbr = get(interaction.guild.roles, id=1205244518082027581)
                line1 = get(interaction.guild.roles, id=1205197875399753738)
                line2 = get(interaction.guild.roles, id=1205244496216850503)
                line3 = get(interaction.guild.roles, id=1227435991673995264)
                line4 = get(interaction.guild.roles, id=1205244659815813120)
                nmbr = get(interaction.guild.roles, id=1212716579746488391)
                await interaction.user.add_roles(mbr, line1, line2, line3, line4)
                await interaction.user.remove_roles(nmbr)
                await interaction.user.edit(nick='MBR : {}'.format(rbxname))
                return
            while roof:
                reqembed = discord.Embed(title="REQUEST", description="로블록스 계정({})의 소개란에 **`{}`**를 포함시켜주세요.\n인증이 완료된 뒤에는 지우셔도 됩니다.".format(로블록스닉네임, verifycode), color=0xeb9534)
                reqembed.set_footer(text="made by BINI in FICES™")
                button1 = Button(label="완료했습니다", style = discord.ButtonStyle.green)
                async def button_callback1(binteraction: discord.Interaction):
                    description = get_user_description(user_id)
                    if str(verifycode) in description:
                        await interaction.delete_original_response()
                        memberid = '{}'.format(binteraction.user.id)
                        now = datetime.now()
                        signupday = '{}-{}-{}'.format(now.year, f'{now.month:02d}', f'{now.day:02d}')
                        uuidcode = str(uuid.uuid4())
                        rbxid = get_roblox_user_id(로블록스닉네임)
                        mbr = get(binteraction.guild.roles, id=1205244518082027581)
                        line1 = get(binteraction.guild.roles, id=1205197875399753738)
                        line2 = get(binteraction.guild.roles, id=1205244496216850503)
                        line3 = get(binteraction.guild.roles, id=1227435991673995264)
                        line4 = get(binteraction.guild.roles, id=1205244659815813120)
                        nmbr = get(interaction.guild.roles, id=1212716579746488391)
                        logembed = discord.Embed(title="SIGNUP", description="{}님이 루아스튜디오 회원이 되셨습니다.".format(interaction.user.mention), color=0xeb9534)
                        logembed.set_footer(text="made by BINI in FICES™")
                        embed = discord.Embed(title="COMPLETE", description="축하합니다! 지금부터 당신은 루아스튜디오를 자유롭게 이용하실 수 있습니다.", color=0xeb9534)
                        embed.set_footer(text="made by BINI in FICES™")
                        data[memberid] = [0, signupday, str(rbxid), uuidcode]
                        with open(account_path, 'w', encoding='utf-8') as file:
                            json.dump(data, file, ensure_ascii=False, indent=4)
                        await binteraction.user.add_roles(mbr, line1, line2, line3, line4)
                        await interaction.user.remove_roles(nmbr)
                        await binteraction.user.edit(nick='MBR : {}'.format(로블록스닉네임))
                        await log.send(embed=logembed)
                        await binteraction.response.send_message(embed=embed, ephemeral=True)
                    else:
                        reqembed = discord.Embed(title="REQUEST", description="로블록스 계정({})의 소개란에 **`{}`**를 포함시켜주세요.\n인증이 완료된 뒤에는 지우셔도 됩니다.".format(로블록스닉네임, verifycode), color=0xeb9534)
                        reqembed.add_field(name="현재 소개란", value="**`{}`**".format(description), inline=False)
                        reqembed.set_footer(text="made by BINI in FICES™")
                        await interaction.response.send_message(embed=reqembed, ephemeral=True)
                button1.callback = button_callback1
                view = View()
                view.add_item(button1)
                await interaction.response.send_message(embed=reqembed, ephemeral=True, view=view)
        else:
            errembed = discord.Embed(title="ERROR", description="존재하지 않는 유저입니다.", color=0xeb9534)
            errembed.set_footer(text="made by BINI in FICES™")
            await interaction.response.send_message(embed=errembed, ephemeral=True)
            return

@tree.command(name = '회원정보조회', description = '본인의 회원정보를 조회합니다.')
async def slash2(interaction: discord.Interaction):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    memberid = '{}'.format(interaction.user.id)
    with open(account_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    if not memberid in data:
        embed = discord.Embed(title="ERROR", description="회원정보를 찾을 수 없습니다. 회원가입이 되어있지 않은 것으로 보입니다.", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    log = client.get_channel(1205218949759893626)
    logembed = discord.Embed(title="INFO VIEW", description="{}님이 본인의 회원정보를 조회했습니다.".format(interaction.user.mention), color=0xeb9534)
    logembed.set_footer(text="made by BINI in FICES™")
    buyer = get(interaction.guild.roles, id=1205251441707458653)
    bronze = get(interaction.guild.roles, id=1205251551065677855)
    silver = get(interaction.guild.roles, id=1205251736671879259)
    gold = get(interaction.guild.roles, id=1205251805064335392)
    platinum = get(interaction.guild.roles, id=1205251958206889984)
    diamond = get(interaction.guild.roles, id=1205252070618300498)
    red_diamond = get(interaction.guild.roles, id=1205252209688973323)
    buypoint = data[memberid][0] / 5000
    buyrank = None
    if data[memberid][0] <= 0:
        buyrank = 'None'
    elif 60 <= buypoint:
        buyrank = red_diamond
    elif 30 <= buypoint >= 2:
        buyrank = diamond
    elif 18 <= buypoint >= 2:
        buyrank = platinum
    elif 12 <= buypoint >= 2:
        buyrank = gold
    elif 6 <= buypoint >= 2:
        buyrank = silver
    elif 3 <= buypoint >= 2:
        buyrank = bronze
    elif 0 <= buypoint >= 2:
        buyrank = buyer
    if not memberid in data:
        embed = discord.Embed(title="ERROR", description="회원정보를 찾을 수 없습니다. 회원가입이 되어있지 않은 것으로 보입니다.", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    user_id = data[memberid][2]
    if __name__ == "__main__":
        user_id = int(user_id)
        username = get_username_from_user_id(user_id)
    embed = discord.Embed(title="INFO".format(data[memberid]), description="{} 님의 회원 정보입니다.".format(interaction.user.mention), color=0xeb9534)
    embed.add_field(name="가입날짜", value="**`{}`**".format(data[memberid][1]), inline=False)
    try:
        embed.add_field(name="구매등급", value="{}(**`{}원`**)".format(buyrank.mention, data[memberid][0]), inline=False)
    except AttributeError:
        embed.add_field(name="구매등급", value="{}(**`{}`**)".format(buyrank, data[memberid][0]), inline=False)
    embed.add_field(name="회원고유번호", value="**`{}`**".format(data[memberid][3]), inline=False)
    embed.add_field(name="로블록스 닉네임", value="**`{}`**".format(username), inline=False)
    embed.set_footer(text="made by BINI in FICES™")
    await log.send(embed=logembed)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    if not buyrank in interaction.user.roles:
        await interaction.user.remove_roles(bronze,silver,gold,platinum,diamond,red_diamond)
        await interaction.user.add_roles(buyrank)
        changeembed = discord.Embed(title="LUA BOT MESSAGE".format(data[memberid]), description="소유하고 계신 구매등급 역할이 입력된 정보와 일치하지 않아 회원님의 역할을 업데이트하였습니다.".format(interaction.user.mention), color=0xeb9534)
        changeembed.add_field(name="업데이트 사항", value="구매등급이 {} 역할로 변경됨".format(buyrank.mention), inline=False)
        await interaction.followup.send(embed=changeembed, ephemeral=True)

@tree.command(name = 'infoview', description = '특정 멤버의 회원정보를 조회합니다.')
@app_commands.describe(대상='조회할 유저를 선택하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        memberid = '{}'.format(대상.id)
        with open(account_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if not memberid in data:
            embed = discord.Embed(title="ERROR", description="회원정보를 찾을 수 없습니다. 회원가입이 되어있지 않은 것으로 보입니다.", color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="ADMIN INFO VIEW", description="{}님이 {}님의 회원정보를 조회했습니다.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        buyer = get(interaction.guild.roles, id=1205251441707458653)
        bronze = get(interaction.guild.roles, id=1205251551065677855)
        silver = get(interaction.guild.roles, id=1205251736671879259)
        gold = get(interaction.guild.roles, id=1205251805064335392)
        platinum = get(interaction.guild.roles, id=1205251958206889984)
        diamond = get(interaction.guild.roles, id=1205252070618300498)
        red_diamond = get(interaction.guild.roles, id=1205252209688973323)
        buypoint = data[memberid][0] / 5000
        buyrank = None
        if data[memberid][0] <= 0:
            buyrank = 'None'
        elif 60 <= buypoint:
            buyrank = red_diamond
        elif 30 <= buypoint >= 2:
            buyrank = diamond
        elif 18 <= buypoint >= 2:
            buyrank = platinum
        elif 12 <= buypoint >= 2:
            buyrank = gold
        elif 6 <= buypoint >= 2:
            buyrank = silver
        elif 3 <= buypoint >= 2:
            buyrank = bronze
        elif 0 <= buypoint >= 2:
            buyrank = buyer
        user_id = data[memberid][2]
        if __name__ == "__main__":
            user_id = int(user_id)
            username = get_username_from_user_id(user_id)
        embed = discord.Embed(title="INFO".format(data[memberid]), description="{} 님의 회원 정보입니다.".format(대상.mention), color=0xeb9534)
        embed.add_field(name="가입날짜", value="**`{}`**".format(data[memberid][1]), inline=False)
        try:
            embed.add_field(name="구매등급", value="{}(**`{}원`**)".format(buyrank.mention, data[memberid][0]), inline=False)
        except AttributeError:
            embed.add_field(name="구매등급", value="{}(**`{}`**)".format(buyrank, data[memberid][0]), inline=False)
        embed.add_field(name="회원고유번호", value="**`{}`**".format(data[memberid][3]), inline=False)
        embed.add_field(name="로블록스 닉네임", value="**`{}`**".format(username), inline=False)
        embed.set_footer(text="made by BINI in FICES™")
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = '회원탈퇴', description = '루아스튜디오 회원자격을 포기합니다.')
async def slash2(interaction: discord.Interaction):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    log = client.get_channel(1205218949759893626)
    logembed = discord.Embed(title="SECESSION", description="{}님이 회원에서 탈퇴하였습니다.".format(interaction.user.mention), color=0xeb9534)
    logembed.set_footer(text="made by BINI in FICES™")
    with open(account_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    key_to_delete = str(interaction.user.id)
    if data[key_to_delete]:
        del data[key_to_delete]
        roles = interaction.user.roles[1:]
        nmbr = get(interaction.guild.roles, id=1212716579746488391)
        await interaction.user.remove_roles(*roles)
        await interaction.user.add_roles(nmbr)
        embed = discord.Embed(title="COMPLETE", description="회원탈퇴가 완료되었습니다. 회원정보가 삭제처리되었습니다.", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
    else:
        embed = discord.Embed(title="ERROR", description="회원정보를 찾을 수 없습니다. 회원가입이 되어있지 않은 것으로 보입니다.", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        return
    with open(account_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    await log.send(embed=logembed)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name = 'secession', description = '루아스튜디오 회원자격을 포기합니다.')
@app_commands.describe(대상='대상을 선택하세요', 사유='사유를 입력하세요')
async def slash2(interaction: discord.Interaction, 대상: discord.Member, 사유:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    log = client.get_channel(1205218949759893626)
    logembed = discord.Embed(title="SECESSIONED", description="{}님이 {}에 의해 회원정보가 삭제제되었습니다.\n다시 등록할 수 있습니다.".format(대상.mention, 대상.mention), color=0xeb9534)
    logembed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
    logembed.set_footer(text="made by BINI in FICES™")
    with open(account_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    key_to_delete = str(대상.id)
    if data[key_to_delete]:
        del data[key_to_delete]
        roles = 대상.roles[1:]
        nmbr = get(interaction.guild.roles, id=1212716579746488391)
        await 대상.remove_roles(*roles)
        await 대상.add_roles(nmbr)
        embed = discord.Embed(title="COMPLETE", description="회원탈퇴가 완료되었습니다. 회원정보가 삭제처리되었습니다.", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
    else:
        embed = discord.Embed(title="ERROR", description="회원정보를 찾을 수 없습니다. 회원가입이 되어있지 않은 것으로 보입니다.", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        return
    with open(account_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    dmembed = discord.Embed(title="COMPLETE", description="[Web 발신][LUA BOT]\n귀하께서는 **`{}`**로 인하여 회원정보가 삭제조치되셨습니다. 이의제기가 가능하며, 다시 등록할 수 있습니다.".format(사유), color=0xeb9534)
    dmembed.set_footer(text="made by BINI in FICES™")
    await log.send(embed=logembed)
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name = 'testing', description = 'test cmd')
async def slash2(interaction: discord.Interaction, arg:discord.Member):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    await interaction.response.send_message('테스트중인 명령어가 없습니다', ephemeral=True)

@tree.command(name = 'addlicense', description = '새로운 라이센스를 등록합니다.')
async def slash2(interaction: discord.Interaction):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    button = Button(label="준비됐습니다", style = discord.ButtonStyle.green)
    mainembed = discord.Embed(title="TIP!", description="라이센스 등록 전 아래 정보를 준비하시기 바랍니다", color=0xeb9534)
    mainembed.add_field(name="그룹 아이디", value="로블록스 그룹 메인페이지 - 위 링크 내 숫자 7자리", inline=False)
    mainembed.add_field(name="디스코드 초대코드(영구)", value="본인 서버 프로필 우클릭 - 초대하기 - 초대 링크 편집하기 - 잔혀 유효기간, 최대 사용횟수 제한없음 - 새 링크 만들기 - 세번째 \'/\'기호 후부터 복사", inline=False)
    mainembed.set_footer(text="made by BINI in FICES™")
    async def button_callback(binteraction: discord.Interaction):
        await binteraction.response.send_modal(license_modal())
        await interaction.delete_original_response()
    button.callback = button_callback
    view = View()
    view.add_item(button)
    await interaction.response.send_message(embed=mainembed, view=view, ephemeral=True)
    

@tree.command(name = '라이센스조회', description = '본인 서버의 라이센스를 조회합니다.')
async def slash2(interaction: discord.Interaction):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    with open(license_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    log = client.get_channel(1205218949759893626)
    logembed = discord.Embed(title="LICENSE VIEW", description="{}님이 본인 서버의 라이센스를 조회했습니다.".format(interaction.user.mention), color=0xeb9534)
    logembed.set_footer(text="made by BINI in FICES™")
    licenseid = '{}'.format(interaction.user.id)
    if not licenseid in data:
        embed = discord.Embed(title="ERROR", description="라이센스 정보를 찾을 수 없습니다. 라이센스 등록이 되어있지 않은 것으로 보입니다.\n++ 서버장만 서버 라이센스 조회를 신청할 수 있습니다.", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    embed = discord.Embed(title="INFO", description="라이센스 정보입니다.", color=0xeb9534)
    embed.add_field(name="서버명(서버 직행)", value="[{}](https://discord.gg/{})".format(get_server_name_from_invite(str(data[licenseid][2]), bot_token), data[licenseid][2]))
    embed.add_field(name="서버장", value="{}".format(interaction.user.mention))
    embed.add_field(name="서버 아이디", value="{}".format(data[licenseid][0]))
    embed.add_field(name="그룹명(그룹 직행)", value="[{}](https://www.roblox.com/groups/{})".format(get_group_name(data[licenseid][1]), data[licenseid][1]), inline=False)
    embed.add_field(name="그룹오너", value="{}".format(get_username_from_user_id(get_roblox_group_owner_id(data[licenseid][1]))))
    embed.add_field(name="그룹 아이디", value="{}".format(data[licenseid][1]))
    embed.add_field(name="서버 초대코드", value="{}".format(data[licenseid][2]), inline=False)
    embed.add_field(name="가입날짜", value="{}".format(data[licenseid][3]))
    embed.add_field(name="고유번호", value="**`{}`**".format(data[licenseid][4]))
    embed.set_footer(text="made by BINI in FICES™")
    await log.send(embed=logembed) 
    await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name = 'licenseview', description = '특정 라이센스 서버를 조회합니다.')
@app_commands.describe(서버장='조회할 서버의 서버장을 선택하세요')
async def slash2(interaction: discord.Interaction, 서버장:discord.Member):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        with open(license_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="ADMIN LICENSE VIEW", description="{}님이 **``**({}님의 서버) 라이센스를 조회했습니다.".format(interaction.user.mention, 서버장.mention), color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        licenseid = '{}'.format(서버장.id)
        if not licenseid in data:
            embed = discord.Embed(title="ERROR", description="라이센스 정보를 찾을 수 없습니다. 라이센스 등록이 되어있지 않은 것으로 보입니다.\n++ 서버장만 서버 라이센스 조회를 신청할 수 있습니다.", color=0xeb9534)
            embed.set_footer(text="made by BINI in FICES™")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        embed = discord.Embed(title="INFO", description="라이센스 정보입니다.", color=0xeb9534)
        embed.add_field(name="서버명(서버 직행)", value="[{}](https://discord.gg/{})".format(get_server_name_from_invite(str(data[licenseid][2]), bot_token), data[licenseid][2]))
        embed.add_field(name="서버장", value="{}".format(서버장.mention))
        embed.add_field(name="서버 아이디", value="{}".format(data[licenseid][0]))
        embed.add_field(name="그룹명(그룹 직행)", value="[{}](https://www.roblox.com/groups/{})".format(get_group_name(data[licenseid][1]), data[licenseid][1]), inline=False)
        embed.add_field(name="그룹오너", value="{}".format(get_username_from_user_id(get_roblox_group_owner_id(data[licenseid][1]))))
        embed.add_field(name="그룹 아이디", value="{}".format(data[licenseid][1]))
        embed.add_field(name="서버 초대코드", value="{}".format(data[licenseid][2]), inline=False)
        embed.add_field(name="가입날짜", value="{}".format(data[licenseid][3]))
        embed.add_field(name="고유번호", value="**`{}`**".format(data[licenseid][4]))
        embed.set_footer(text="made by BINI in FICES™")
        await adminlog.send(embed=logembed) 
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = '라이센스탈퇴', description = '본인에게 등록된 라이센스 서버를 연결 해지합니다.')
@app_commands.describe(사유='탈퇴하시는 사유를 작성해주세요')
async def slash2(interaction: discord.Interaction, 사유: str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    with open(license_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    adminlog = client.get_channel(1243139947624529961)
    licenseid = '{}'.format(interaction.user.id)
    if licenseid in data:
        logembed = discord.Embed(title="LICENSE SECESION", description="아래 서버의 서버장이신 {}님께서 `'{}'`로 인하여 라이센스를 해지했습니다.".format(interaction.user.mention, 사유), color=0xeb9534)
        logembed.add_field(name="서버명(서버 직행)", value="[{}](https://discord.gg/{})".format(get_server_name_from_invite(str(data[licenseid][2]), bot_token), data[licenseid][2]))
        logembed.add_field(name="서버장", value="{}".format(interaction.user.mention))
        logembed.add_field(name="서버 아이디", value="{}".format(data[licenseid][0]))
        logembed.add_field(name="그룹명(그룹 직행)", value="[{}](https://www.roblox.com/groups/{})".format(get_group_name(data[licenseid][1]), data[licenseid][1]), inline=False)
        logembed.add_field(name="그룹오너", value="{}".format(get_username_from_user_id(get_roblox_group_owner_id(data[licenseid][1]))))
        logembed.add_field(name="그룹 아이디", value="{}".format(data[licenseid][1]))
        logembed.add_field(name="서버 초대코드", value="{}".format(data[licenseid][2]), inline=False)
        logembed.add_field(name="가입날짜", value="{}".format(data[licenseid][3]))
        logembed.add_field(name="고유번호", value="**`{}`**".format(data[licenseid][4]))
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="INFO", description="루아스튜디오와의 라이센스가 연결 해지되었습니다. \'{}\'서버는 이제 라이센스 등록서버가 아닙니다.".format(get_server_name_from_invite(str(data[licenseid][2]), bot_token)), color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
    else:
        embed = discord.Embed(title="ERROR", description="라이센스 정보를 찾을 수 없습니다. 라이센스 등록이 되어있지 않은 것으로 보입니다.\n++ 서버장만 서버 라이센스 탈퇴를 신청할 수 있습니다.", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    role = get(interaction.guild.roles, id=1205244518082027581)
    await interaction.user.remove_roles(role)
    await interaction.response.send_message(embed=embed, ephemeral=True)
    del data[licenseid]
    with open(license_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    await adminlog.send(embed=logembed)

@tree.command(name = 'timeout', description = '특정 멤버에게 타임아웃을 부여합니다.')
@app_commands.describe(대상 = '타임아웃을 부여할 유저를 선택하세요', 시간='타임아웃 시간을 설정하세요(시간 기준)', 사유='타임아웃 부여 사유를 입력하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member, 시간:int, 사유:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        adminlog = client.get_channel(1243139947624529961)
        duration = timedelta(hours=시간)
        logembed = discord.Embed(title="TIME OUT", description="{}님이 {}님에게 타임아웃 {}시간을 부여했습니다.".format(interaction.user.mention, 대상.mention, 시간), color=0xeb9534)
        logembed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="TIME OUT", description="{}님에게 타임아웃 {}시간을 부여했습니다.".format(대상.mention, 시간), color=0xeb9534)
        embed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
        embed.set_footer(text="made by BINI in FICES™")
        dmembed = discord.Embed(title="LUA BOT MESSAGE", description="[WEB 발신][LUA BOT]\n귀하께서는 **`{}`**로 인하여 타임아웃 {}시간을 부여받으셨습니다.\n안전한 쇼핑 되시기 바랍니다. 감사합니다.".format(대상.mention, 시간), color=0xeb9534)
        dmembed.set_footer(text="LuaStudio CO. 드림.ㅣmade by BINI in FICES™")
        await 대상.timeout(duration, reason=사유)
        await 대상.send(embed=dmembed)
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'timeoutclear', description = '특정 멤버의 타임아웃을 해제합니다.')
@app_commands.describe(대상='해제할 유저를 선택하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member, 사유:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        if not 대상.is_timed_out():
            embed = discord.Embed(title="ERROR", description="해당 멤버는 타임아웃 상태가 아닙니다.", color=0xeb9534)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="TIME OUT CLEAR", description="{}님이 {}님의 타임아웃을 해제했습니다.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        logembed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="TIME OUT", description="{}님의 타임아웃을 해제했습니다".format(대상.mention), color=0xeb9534)
        embed.add_field(name="사유", value="**`{}`**".format(사유), inline=False)
        embed.set_footer(text="made by BINI in FICES™")
        dmembed = discord.Embed(title="LUA BOT MESSAGE", description="[WEB 발신][LUA BOT]\n귀하께서는 **`{}`**로 인하여 귀하의 타임아웃이 해제되었습니다.\n안전한 쇼핑 되시기 바랍니다. 감사합니다.".format(사유), color=0xeb9534)
        dmembed.set_footer(text="LuaStudio CO. 드림.ㅣmade by BINI in FICES™")
        await 대상.timeout(None)
        await 대상.send(embed=dmembed)
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'addgoods', description = '상품코드를 등록합니다.')
@app_commands.describe(코드번호='상품을 식별할 때 사용할 코드를 입력하세요', 상품이름='상품의 이름을 입력하세요', 가격='가격을 입력하세요')
async def slash2(interaction: discord.Interaction, 코드번호:str, 상품이름:str, 가격:int):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.id == 944555542855163905:
        with open(purchase_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if 코드번호 in data:
            embed = discord.Embed(title="ERROR", description="해당 코드번호를 가진 상품이 이미 있습니다.", color=0xeb9534)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        now = datetime.now()
        adminlog = client.get_channel(1243139947624529961)
        num = '{}-{}-{}'.format(now.year, f'{now.month:02d}', f'{now.day:02d}')
        logembed = discord.Embed(title="PURCHASE CODE", description="새로운 상품코드가 등록되었습니다.", color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="COMPLETE", description="새로운 상품코드가 등록되었습니다.", color=0xeb9534)
        embed.add_field(name="상품이름", value="**`{}`**".format(상품이름), inline=False)
        embed.add_field(name="상품코드", value="**`{}`**".format(코드번호), inline=False)
        embed.add_field(name="등록날짜", value="**`{}원`**".format(num), inline=False)
        embed.add_field(name="상품가격", value="**`{}원`**".format(가격), inline=False)
        embed.set_footer(text="made by BINI in FICES™")
        data[코드번호] = [상품이름, 가격, num]
        with open(purchase_path, 'w', encoding='utf-8') as file:
           json.dump(data, file, ensure_ascii=False, indent=4)
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'deletegoods', description = '상품코드를 삭제합니다.')
@app_commands.describe(코드번호='삭제할 상품의 코드번호를 입력하세요')
async def slash2(interaction: discord.Interaction, 코드번호:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.id == 944555542855163905:
        with open(purchase_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if not 코드번호 in data:
            embed = discord.Embed(title="ERROR", description="해당 코드번호를 가진 상품이 없습니다.", color=0xeb9534)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="PURCHASE CODE DELETE", description="상품코드가 삭제되었습니다.", color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="COMPLETE", description="상품코드가 삭제되었습니다.", color=0xeb9534)
        embed.add_field(name="상품이름", value="**`{}`**".format(data[코드번호][0]), inline=False)
        embed.add_field(name="상품코드", value="**`{}`**".format(코드번호), inline=False)
        embed.add_field(name="등록날짜", value="**`{}`**".format(data[코드번호][2]), inline=False)   
        embed.add_field(name="상품가격", value="**`{}원`**".format(data[코드번호][1]), inline=False)
        embed.set_footer(text="made by BINI in FICES™")
        with open(purchase_path, 'w', encoding='utf-8') as file:
           json.dump(data, file, ensure_ascii=False, indent=4)
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'goodsview', description = '상품을 조회합니다.')
@app_commands.describe(코드번호='조회할 상품의 코드번호를 입력하세요')
async def slash2(interaction: discord.Interaction, 코드번호:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.administrator:
        with open(purchase_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if not 코드번호 in data:
            embed = discord.Embed(title="ERROR", description="해당 코드번호를 가진 상품이 없습니다.", color=0xeb9534)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="PURCHASE CODE View", description="{}님이 상품코드를 조회했습니다.".format(interaction.user.mention), color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="INFO", description="상품 정보입니다.", color=0xeb9534)
        embed.add_field(name="상품이름", value="**`{}`**".format(data[코드번호][0]))
        embed.add_field(name="상품코드", value="**`{}`**".format(코드번호))
        embed.add_field(name="등록날짜", value="**`{}`**".format(data[코드번호][2]))   
        embed.add_field(name="상품가격", value="**`{}원`**".format(data[코드번호][1]))
        embed.set_footer(text="made by BINI in FICES™")
        del data[코드번호]
        with open(purchase_path, 'w', encoding='utf-8') as file:
           json.dump(data, file, ensure_ascii=False, indent=4)
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'benefit', description = '유저에게 구매한 상품에 대한 일부 혜택을 지급합니다.')
@app_commands.describe(대상='혜택을 지급할 유저를 선택하세요', 코드번호='상품의 코드번호를 입력하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member, 코드번호:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        with open(purchase_path, 'r', encoding='utf-8') as file:
            purchasedata = json.load(file)
        with open(account_path, 'r', encoding='utf-8') as file:
            accountdata = json.load(file)
        if not 코드번호 in purchasedata:
            embed = discord.Embed(title="ERROR", description="해당 코드번호를 가진 상품이 없습니다.", color=0xeb9534)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        log = client.get_channel(1205218949759893626)
        logembed = discord.Embed(title="PURCHASED", description="{}에게 구매 혜택이 지급되었습니다.".format(대상.mention), color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="COMPLETE", description="새로운 일부 구매 혜택을 지급했습니다.", color=0xeb9534)
        embed.add_field(name="상품이름", value="**`{}`**".format(purchasedata[코드번호][0]), inline=False)
        embed.add_field(name="상품코드", value="**`{}`**".format(코드번호), inline=False)
        embed.set_footer(text="made by BINI in FICES™")
        accountdata[str(대상.id)][0] += purchasedata[코드번호][1]
        with open(account_path, 'w', encoding='utf-8') as file:
           json.dump(accountdata, file, ensure_ascii=False, indent=4)
        await log.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)

@tree.command(name = 'removebnft', description = '대상에게서 특정 상품의 포인트 적립을 철회합니다')
@app_commands.describe(대상='혜택을 취소할 유저를 선택하세요', 코드번호='상품의 코드번호를 입력하세요')
async def slash2(interaction: discord.Interaction, 대상:discord.Member, 코드번호:str):
    if not interaction.guild.id == 1205153551366627379:
        embed = discord.Embed(title="ERROR", description="이 봇은 해당 서버에서 사용하실 수 없습니다.\n 이런 본인의 서버만을 위한 커스텀 봇을 만들고 싶으신가요? 에서 시작하세요!", color=0xeb9534)
        embed.set_footer(text="made by BINI in FICES™")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    if interaction.user.guild_permissions.moderate_members:
        with open(purchase_path, 'r', encoding='utf-8') as file:
            purchasedata = json.load(file)
        with open(account_path, 'r', encoding='utf-8') as file:
            accountdata = json.load(file)
        if not 코드번호 in purchasedata:
            embed = discord.Embed(title="ERROR", description="해당 코드번호를 가진 상품이 없습니다.", color=0xeb9534)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        adminlog = client.get_channel(1243139947624529961)
        logembed = discord.Embed(title="PURCHASED", description="{}님이 {}님에게서 구매 혜택을 철회했습니다.".format(interaction.user.mention, 대상.mention), color=0xeb9534)
        logembed.set_footer(text="made by BINI in FICES™")
        embed = discord.Embed(title="COMPLETE", description="구매 혜택을 철회했습니다.", color=0xeb9534)
        embed.add_field(name="상품이름", value="**`{}`**".format(purchasedata[코드번호][0]), inline=False)
        embed.add_field(name="상품코드", value="**`{}`**".format(코드번호), inline=False)
        embed.set_footer(text="made by BINI in FICES™")
        if accountdata[str(대상.id)][0] < purchasedata[코드번호][1]:
            embed = discord.Embed(title="COMPLETE", description="혜택 철회 시 포인트가 음수가 되므로 포인트를 0으로 변경했습니다.", color=0xeb9534)
            accountdata[str(대상.id)][0] = 0
        else:
            accountdata[str(대상.id)][0] -= purchasedata[코드번호][1]
        with open(account_path, 'w', encoding='utf-8') as file:
           json.dump(accountdata, file, ensure_ascii=False, indent=4)
        await adminlog.send(embed=logembed)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=errorembed)
client.run(bot_token)
