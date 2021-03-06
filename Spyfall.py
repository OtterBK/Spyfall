# -*- coding: utf-8 -*-


#### 스카이폴
#### 작성: OtterBK

#### 필요 라이브러리 로드
import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import CommandNotFound
import logging
import asyncio
import os
import math
import random
import sys, traceback
import json
import operator

class Config(enumerate):
    BOT_PREFIX = "~"
    TOKEN = "" # 여기에 봇 토큰 입력
    VERSION = "1.0.0"
    LAST_PATCH = "21/05/14"
    EMAIL_ADDRESS = "otter6975@gmail.com"
    BOT_LINK = ""

    BGM_PATH = os.getcwd() + "/bgm/"

class EMOJI_ICON(enumerate):
    JOIN = "✋"
    START = "🕹"

    ICON_VERSION = "📌"
    ICON_FOLDER = "📁"
    ICON_PAGE = "🅿️"
    ICON_GAME ="🎮"
    ICON_LIST = "📄"
    ICON_CARD = "🃏"
    ICON_QUESTION = "❓"
    ICON_WARN = "⚠"
    ICON_NOTE = "📖"
    ICON_DOWN = "👇"
    ICON_MAP = "🗺"
    ICON_ROLE = "🏷"
    ICON_VOTE = "📩"
    ICON_TIP = "🔖"
    ICON_ANSWER = "🖲"
    ICON_PHONE = "📱"
    ICON_MAIL = "📧"
    ICON_GIT = "🌐"
    ICON_FIX = "🛠️"
    ICON_BOOK_RED = "📕"

    CLOCK_0 = "🕛"
    CLOCK_1 = "🕐"
    CLOCK_2 = "🕑"
    CLOCK_3 = "🕒"
    CLOCK_4 = "🕓"
    CLOCK_5 = "🕔"
    CLOCK_6 = "🕕"
    CLOCK_7 = "🕖"   
    CLOCK_8 = "🕗"
    CLOCK_9 = "🕘"
    CLOCK_10 = "🕙"
    CLOCK_11 = "🕚"
    CLOCK_12 = "🕛"

    ALPHABET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"
        , "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    NUMBER = [ "0️⃣", "1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    ICON_HUMAN = ["👮‍♀️","🕵️‍♀️","🕵️‍♂️","💂‍♂️","💂‍♀️","👷‍♀️","👷‍♂️","👩‍⚕️","👨‍⚕️","👩‍🎓","👨‍🎓","👩‍🏫","👨‍🏫","👩‍⚖️","👨‍⚖️","👩‍🌾","👨‍🌾","👩‍🍳","👨‍🍳","👩‍🔧","👩‍🏭","👨‍🔧","👨‍🏭","👩‍💼","👨‍💼","👩‍🔬","👨‍🔬","👩‍💻","👨‍💻","👩‍🎤","👨‍🎤","👩‍🎨","👨‍🎨","👩‍✈️","👨‍✈️","👩‍🚀","👨‍🚀","👩‍🚒","👨‍🚒","🧕","👰","🤵","🤱","🤰","🦸‍♀️","🦸‍♂️","🦹‍♀️","🦹‍♂️","🧙‍♀️","🧙‍♂️","🧚‍♀️","🧚‍♂️","🧛‍♀️","🧛‍♂️","🧜‍♀️","🧝‍♀️","🧝‍♂️","🧟‍♀️","🧟‍♂️"]


class BGM_TYPE(enumerate):
    PLING = 1
    ROUND_ALARM = 2
    SCORE_ALARM = 3
    ENDING = 4
    FAIL = 5
    countdown10 = 6
    SUCCESS = 7
    BELL = 8
    LONGTIMER = 9
    CARD_DRAW = 10
    CHANGE_BADGE = 11
    VOTE_TIME = 12


def getAlphabetFromIndex(index):
    return EMOJI_ICON.ALPHABET[index]


def getEmojiFromNumber(index): #정수값에 알맞은 이모지 반환
    return EMOJI_ICON.NUMBER[index]

def getNumberFromEmoji(emoji): #이모지가 숫자 이모지인지 확인
    index = 0
    while index < len(EMOJI_ICON.NUMBER): #이모지에 맞는 번호 반환
        if EMOJI_ICON.NUMBER[index] == emoji:
            return index
        index += 1

def getRandomHumanIcon():
    return random.choice(EMOJI_ICON.ICON_HUMAN)

def getClockIcon(leftTime, maxTime): #시계 아이콘 반환
    if maxTime == 0:
        return EMOJI_ICON._CLOCK_0
    clockType = int((maxTime-leftTime)/maxTime * 12)
    if clockType == 0:
        return EMOJI_ICON.CLOCK_0
    elif clockType == 1:
        return EMOJI_ICON.CLOCK_1
    elif clockType == 2:
        return EMOJI_ICON.CLOCK_2
    elif clockType == 3:
        return EMOJI_ICON.CLOCK_3
    elif clockType == 4:
        return EMOJI_ICON.CLOCK_4
    elif clockType == 5:
        return EMOJI_ICON.CLOCK_5
    elif clockType == 6:
        return EMOJI_ICON.CLOCK_6
    elif clockType == 7:
        return EMOJI_ICON.CLOCK_7
    elif clockType == 8:
        return EMOJI_ICON.CLOCK_8
    elif clockType == 9:
        return EMOJI_ICON.CLOCK_9
    elif clockType == 10:
        return EMOJI_ICON.CLOCK_10
    elif clockType == 11:
        return EMOJI_ICON.CLOCK_11
    elif clockType == 12:
        return EMOJI_ICON.CLOCK_12

    return EMOJI_ICON.CLOCK_0


#### 기본 설정
bot = commands.Bot(command_prefix=Config.BOT_PREFIX)  # 봇 커맨드 설정
random.seed() #시드 설정

if Config.TOKEN == "":
    try:
        path = os.getcwd() + "/token.txt"
        f = open(path, 'r', encoding="utf-8" )
        Config.TOKEN = f.readline().strip()
        f.close()
    except:
        print(path)
        print("토큰 로드 에러")

def __get_logger():
    """로거 인스턴스 반환
    """

    __logger = logging.getLogger('logger')

    # 로그 포멧 정의
    # formatter = logging.Formatter(
    #     '%(levelname)s##%(asctime)s##%(message)s >> @@file::%(filename)s@@line::%(lineno)s')

    formatter = logging.Formatter("<보드게임봇>"+" [%(levelname)s] %(asctime)s   >>   %(message)s")

    # 스트림 핸들러 정의
    stream_handler = logging.StreamHandler()
    # 각 핸들러에 포멧 지정
    stream_handler.setFormatter(formatter)
    # 로거 인스턴스에 핸들러 삽입
    __logger.addHandler(stream_handler)
    # 로그 레벨 정의
    __logger.setLevel(logging.INFO)

    return __logger

Logger = __get_logger()


#### 유틸
class Frame:
    def __init__(self):

        self._LIST_PER_PAGE = 5 #페이지 마다 표시할 메인 메시지 라인수

        self._title_visible = True #타이틀 표시 여부
        self._title_text = "Title"  #타이틀 메시지

        self._sub_visible = True #서브 타이틀 표시 여부
        self._sub_text = "Sub Title"  # 서브 타이틀 메시지

        self._main_visible = True #메인 메시지 표시 여부
        self._main_text = [] #메인, list 형태로하여 _LIST_PER_PAGE 만큼 표시

        self._notice_visible = True #알림 표시 여부
        self._notice_text = "Notice" #알림

        self._field_visible = True #Field 표시 여부
        self._field_text = dict() #맵에 있는 값을 차례로 표시할 거임

        self._page_visible = True #페이지 표시 옵션
        self._page_nowPage = 0 #현재 페이지 번호

        self._path_visible = True #경로 표시 옵션
        self._path_text = "Path" #경로 메시지

        self._customFooter_visible = False
        self._customFooter_text = ""

        self._image_visible = False #이미지 표시 여부
        self._image_local = False #로컬 이미지 여부
        self._image_url = "" #이미지 url

        self._embedColor = discord.Color.magenta() #색상

        self._author = None #작성자 여부 None이면 기본값

        self._myMessage = None

    def addMain(self, singleMsg):
        self._main_text.append(singleMsg)


    def addField(self, fKey, fValue):
        self._field_text[fKey] = fValue

    def paint(self, message): #해당 프레임이 표시될 때 이벤트
        self._myMessage = message

    def destructor(self, message): #해당 프레임이 메시지에서 사라질 때 이벤트
        self._myMessage = message

    async def update(self): #프레임 새로고침
        try:
            setFrame(self._myMessage, self)
        except:
            print("frame update failed")

    async def on_reaction_add(self, message, emoji, user):
        print("이모지 추가")

    async def on_reaction_remove(self, message, emoji, user):
        print("이모지 삭제")


class LobbyFrame(Frame):
    def __init__(self):
        super().__init__() #frame 초기화

        self._title_text = chr(173)+"[　　　　"+ EMOJI_ICON.ICON_GAME +" 스파이폴　　　　]"

        self._sub_visible = True
        self._sub_text = EMOJI_ICON.JOIN + "　**게임 참가**\n"
        self._sub_text += EMOJI_ICON.START + "　**게임 시작**\n"

        self._main_visible = False

        self._notice_visible = True
        self._notice_text = EMOJI_ICON.ICON_LIST+" 참여 인원 목록\n"

        self._field_visible = False

        self._customFooter_visible = True
        self._customFooter_text = EMOJI_ICON.ICON_VERSION + " 버전: " + Config.VERSION

        self._page_visible = False

        self._path_visible = False

        self._image_visible = True
        self._image_url = "https://www.popcone.co.kr/shop/data/goods/1550212054751l0.jpg"

        self._embedColor = discord.Color.blue()


    async def update(self):
        guildID = self._myMessage.guild.id

        gameData = getGamedata(guildID)

        if gameData != None:
            self._notice_text = EMOJI_ICON.ICON_LIST+" 참여 인원 목록 ( "+str(len(gameData._ingamePlayer.keys())) + " / " + str(gameData._maxPlayer) +"명 )\n" + chr(173) + "\n"
            for player in gameData._ingamePlayer.keys():
                self._notice_text += getRandomHumanIcon() +" "+ gameData._ingamePlayer[player]._user.display_name + "\n"
        try:
            await setFrame(self._myMessage, self)
        except:
            print("frame update failed")


    async def on_reaction_add(self, message, emoji, user):
        guild = message.guild # 반응한 서버
        channel = message.channel  # 반응 추가한 채널
        gameData = getGamedata(guild.id)

        if str(emoji) == str(EMOJI_ICON.JOIN): # 참가 이모지 누른거라면
            if not user.id in gameData._ingamePlayer.keys():
                playBGM(gameData._voice, BGM_TYPE.PLING)
                gameData._ingamePlayer[user.id] = Playerdata(user) # 플레이어 데이터 생성
                await self.update() # 프레임 업데이트
        elif str(emoji) == str(EMOJI_ICON.START): # 시작 이모지 누른거라면
            asyncio.ensure_future(message.remove_reaction(emoji, user))  # 이모지 삭제, 버튼 반응 속도 개선
            if gameData._owner == user: # 주최자가 누른거라면
                await gameData.startGame() # 게임 시작
            else:
                asyncio.ensure_future(channel.send("```" + EMOJI_ICON.ICON_TIP + " " + "게임 주최자 [ "+gameData._owner.display_name + " ] 님만이 시작이 가능합니다.```")) #이벤트 동작


    async def on_reaction_remove(self, message, emoji, user):
        guild = message.guild # 반응한 서버
        channel = message.channel  # 반응 추가한 채널
        gameData = getGamedata(guild.id)

        if str(emoji) == str(EMOJI_ICON.JOIN): # 참가 이모지 삭제한거라면
            if user.id in gameData._ingamePlayer.keys():
                del gameData._ingamePlayer[user.id] # 참가 취소
                await self.update() # 프레임 업데이트
        elif emoji == EMOJI_ICON.START: # 시작 이모지 삭제한거라면
            asyncio.ensure_future(message.add_reaction(emoji=emoji))  # 이모지 다시 추가, 버튼 반응 속도 개선


class GameFrame(Frame): # 게임 진행 프레임
    def __init__(self):
        super().__init__() #frame 초기화

        self._title_text = chr(173)+"[　　　　"+ EMOJI_ICON.ICON_GAME +" 스파이폴　　　　]"

        self._sub_visible = True
        self._sub_text = EMOJI_ICON.ICON_CARD + "　**역할 설정 중입니다...**\n"

        self._main_visible = False

        self._notice_visible = True
        self._notice_text = EMOJI_ICON.ICON_NOTE + " **[ @닉네임 ]** 으로 맨션 기능을 \n사용해 질문이 가능합니다.\n" + chr(173) + "\n"
        self._notice_text += EMOJI_ICON.ICON_ANSWER + " 스파이는 [ "+Config.BOT_PREFIX+"정답 ] 명령어로 \n정답을 맞출 수 있습니다.\n" + chr(173) + "\n"
        self._notice_text += EMOJI_ICON.ICON_DOWN + " **맵 목록.**\n" + chr(173) + "\n"

        self._field_visible = True

        self._customFooter_visible = True
        self._customFooter_text = ""

        self._page_visible = False

        self._path_visible = False

        self._image_visible = False
        self._image_url = "https://www.popcone.co.kr/shop/data/goods/1550212054751l0.jpg"

        self._embedColor = discord.Color.green()


    async def update(self):
        try:
            await setFrame(self._myMessage, self)
        except:
            print("frame update failed")


class CardFrame(Frame):
    def __init__(self, map="", role="", url="", guildName="", isShowcard=False, user=None):
        super().__init__() #frame 초기화
        if isShowcard:
            self._title_text = chr(173)+"[　　　　"+ EMOJI_ICON.ICON_GAME +" 역할 공개　　　　]"
        else:
            self._title_text = chr(173)+"[　　　　"+ EMOJI_ICON.ICON_GAME +" 역할　　　　]"

        self._sub_visible = True
        self._sub_text = ""

        if map != "":
            self._sub_text += EMOJI_ICON.ICON_MAP + " 장소: **" + map + "**\n"

        if role != "":
            self._sub_text += EMOJI_ICON.ICON_ROLE + " 역할: **" + role + "**\n"

        self._main_visible = False

        if map != "" and role != "" and not isShowcard:
            self._notice_visible = True
            self._notice_text = "당신은 **"+map+"**에 있는 **" + role+"**입니다! \n역할에 몰입하세요!"
        else:
            self._notice_visible = False

        self._field_visible = False

        if guildName != "":
            self._customFooter_visible = True
            self._customFooter_text = "서버: " + guildName
        else:
            self._customFooter_visible = False


        self._page_visible = False

        self._path_visible = False

        if url != "":
            self._image_visible = True
            self._image_url = url
        else:
            self._image_visible = False

        self._embedColor = discord.Color.gold()
        if isShowcard:
            self._author = user


class ResultFrame(Frame):
    def __init__(self, gameData, winText):
        super().__init__() #frame 초기화

        self._title_text = chr(173)+"[　　　　"+ EMOJI_ICON.ICON_GAME +" 결과 공개　　　　]"

        self._sub_visible = True
        self._sub_text = winText

        self._main_visible = False

        self._notice_visible = True
        self._notice_text = EMOJI_ICON.ICON_MAP+" 장소: **" + gameData._nowMap + "**"

        self._field_visible = True
        for player in gameData._ingamePlayer.values():
            self.addField(player._user.display_name, "[ "+player._role + " ]")

        self._customFooter_visible = True
        self._customFooter_text = ""

        self._page_visible = False

        self._path_visible = False

        self._image_visible = True
        data = gameData._mapAndRole
        map = gameData._nowMap
        mapUrl = data[map]['이미지_주소']
        self._image_url = mapUrl

        self._embedColor = discord.Color.green()

def getEmbedFromFrame(frame): #frame으로 embed 생성

    title = frame._title_text
    mainList = frame._main_text
    nowPage = int(frame._page_nowPage) #현재 페이지 가져옴
    maxPage = math.ceil(len(mainList) / frame._LIST_PER_PAGE)  #최대 페이지 설정
    if nowPage > maxPage - 1: #페이지 초과시 max로
        frame._page_nowPage = maxPage - 1
        nowPage = maxPage - 1
    if nowPage < 0: #음수 방지
        frame._page_nowPage = 0
        nowPage = 0


    desc = chr(173)+"\n"

    if frame._sub_visible: #서브 타이틀
        desc += chr(173)+"\n"+frame._sub_text + "\n"
        desc += chr(173)+"\n" + chr(173) + "\n"


    if frame._main_visible: #메인 메시지, 스크롤 방식
        pageIndex = nowPage * frame._LIST_PER_PAGE #표시 시작할 인덱스

        i = 0
        while i < frame._LIST_PER_PAGE: #LIST_PER_PAGE 만큼 목록 표시
            fileIndex = pageIndex + i
            if fileIndex >= len(mainList): #마지막 텍스트 도달하면 바로 break
                break
            #print(fileIndex)
            #print(str(mainList))
            text = mainList[fileIndex]
            i += 1
            desc += getEmojiFromNumber(i) + ")　" + str(text) + "\n" + chr(173) + "\n"

        desc += chr(173) + "\n"

    if frame._notice_visible: #알림 같은것(에러 메시지 등)
        desc += chr(173) + "\n"
        desc += frame._notice_text
        desc += chr(173)+"\n" + chr(173) + "\n"

    color = frame._embedColor
    selectorEmbed = discord.Embed(title=title, url="", description=desc, color=color) #embed 설정

    if frame._field_visible: #필드부
        for field in frame._field_text.keys():
            fieldValue = frame._field_text[field]
            selectorEmbed.add_field(name=field, value=fieldValue, inline=True)

    text_footer = ""

    if frame._customFooter_visible: #footer를 특정 문자열로 지정하기
        text_footer = frame._customFooter_text
    else:
        if frame._page_visible: # 페이지 표시
            text_footer += EMOJI_ICON.ICON_PAGE + " "
            text_footer += str(nowPage + 1) + " / " + str(maxPage)

        if frame._path_visible: #패스 표시
            if frame._page_visible:
                text_footer += "　　|　　"
            text_footer += EMOJI_ICON.ICON_FOLDER + " " + str(frame._path_text)

    # embed 추가 설정
    if frame._author == None:
        selectorEmbed.set_author(name=bot.user.name, url="",
                                 icon_url=bot.user.avatar_url)
        selectorEmbed.remove_author()
    else:
        author = frame._author
        selectorEmbed.set_author(name=author.display_name, url="",
                                 icon_url=author.avatar_url)

    if frame._image_visible: #이미지
        if not frame._image_local: #로컬 이미지 사용이 아니면
            selectorEmbed.set_image(url=frame._image_url)

    selectorEmbed.set_footer(text=text_footer) #footer 설정

    return selectorEmbed


async def showFrame(message, frame, isPopUp=True): #프레임 표시, isPopUp 가 True면 프레임을 추가로 띄우는 방식으로

    guildID = message.guild.id

    gameData = getGamedata(guildID)
    frameStack = gameData._frameStack

    if gameData != None: # 게임 데이터가 있을 때만
        await setFrame(message, frame)

        if not isPopUp and len(frameStack) > 0: # 팝업 방식이 아니고 프레임 스택에 뭐 있다면
            del frameStack[len(frameStack) - 1] # 마지막 프레임 교체를 위한 삭제

        frameStack.append(frame)




async def setFrame(message, frame): #메시지에 해당 프레임을 설정
    if message == None or frame == None:
        return False

    frame.paint(message) #프레임 표시 이벤트
    selectorEmbed = getEmbedFromFrame(frame)

    try:
        await message.edit(embed=selectorEmbed) # 메시지 객체 업데이트
        return True
    except:
        Logger.error(traceback.format_exc())
        return False


#### 필요 클래스
class GAME_STEP(enumerate):
    LOBBY = 0 # 시작 대기중, 참가자 받기
    SEND_RULE = 1 # 룰 설명 중
    PREPARE = 2 # 게임 준비, 카드 나눠주기 등등
    INGAME = 3 # 게임 진행 중
    TOTALIZE = 4 # 투표 등등 진행
    RESULT = 5 # 게임 결과 발표
    STOP = 6 # 게임 중지
    FINISH = 7 # 게임 끝
    
    

class Gamedata:
    def __init__(self, guild, message, owner, voice):
        self._maxPlayer = 12

        self._voice = voice

        self._guild = guild
        self._frameStack = []
        self._chatChannel = message.channel
        self._owner = owner # 주최자

        self._ingamePlayer = dict() # 게임 참여중인 플레이어, (각 플레이어 데이터가 키 값)

        self._gameStep = GAME_STEP.LOBBY
        self._maxTime = 600
        self._leftTime = self._maxTime

        self._vote_maxTime = 100
        self._vote_leftTime = self._vote_maxTime

        self._answer_maxTime = 100
        self._answer_leftTime = self._answer_maxTime
        self._isAnswering = False

        self._nowMap = "" # 현재 맵
        self._question_from = None # 현재 질문자 ID
        self._question_target = None # 현재 답변자 id

        self._gameFrame = None
        self._mapAndRole = None

        self._votedPlayer = []

        self._spyName = "스파이"
        self._spyMap = "정체불명"
        self._spyUrl = "https://user-images.githubusercontent.com/28488288/118138876-c96a6880-b441-11eb-8356-61322b1ca97e.png"

    async def startGame(self):
        self._gameFrame = GameFrame()
        for player in self._ingamePlayer.values():
            self._gameFrame.addField(player._user.display_name, EMOJI_ICON.ICON_CARD)

        playBGM(self._voice, BGM_TYPE.ROUND_ALARM)

        tmpEmbed = discord.Embed(
            title="초기화중... 잠시만 기다려주세요.", url="", description="\n▽", color=discord.Color.dark_magenta())

        message = await self._chatChannel.send(embed=tmpEmbed)

        await clearChat([message,],self._chatChannel)
    
        await showFrame(message, self._gameFrame, isPopUp=False)
        #asyncio.ensure_future(message.add_reaction(EMOJI_ICON.ICON_ANSWER)) # 스파이 정답 맞추기

        self._gameStep = GAME_STEP.PREPARE

        self.loadMapAndRole()

        self.setMap()

        await asyncio.sleep(3)

        for player in self._ingamePlayer.keys(): # 역할 배포 효과음
            await asyncio.sleep(0.3)
            playBGM(self._voice, BGM_TYPE.CARD_DRAW)

        self.setRole()

        rdID = random.choice(list(self._ingamePlayer.keys()))
        self.setQuestionTarget(None,rdID)

        for player in self._ingamePlayer.values():
            await self.sendCard(player, isShowcard=False)

        self._gameStep = GAME_STEP.INGAME
        await self.timer()

        self._gameStep = GAME_STEP.TOTALIZE
        
        if self._leftTime <= 0: # 타이머 초과로 끝난거면
            # 투표 진행
            asyncio.ensure_future(self._chatChannel.send("```" + EMOJI_ICON.ICON_TIP + " " + "스파이에게 투표하세요.```"))
            await self.vote()

            if len(self._ingamePlayer.keys()) > 8: # 스파이 2명이면
                asyncio.ensure_future(self._chatChannel.send("```" + EMOJI_ICON.ICON_TIP + " " + "두 번째 스파이에게 투표하세요.```"))
                await self.vote()

        else: # 스파이 정답 도전시
            print("스파이가 정답 도전함")

        if self._isAnswering: #스파이가 직업 공개한 상태면
            return

        self._gameStep = GAME_STEP.RESULT

        # await self.showCard() # 직업 공개

        await asyncio.sleep(2)

        asyncio.ensure_future(self._chatChannel.send("```"+EMOJI_ICON.ICON_TIP+"지목된 플레이어의 정체는...?```"))

        await asyncio.sleep(3)


        isCollect = True
        for user in self._votedPlayer:
            player = self._ingamePlayer[user.id]
            await self.sendCard(player, isShowcard=True)
            if player._role != self._spyName:
                isCollect = False

        await asyncio.sleep(3)

        if isCollect:
            await self.civilWin()
        else:
            await self.spyWin()

    async def updateUI(self):
        gameData = self
        gameFrame = self._gameFrame

        await gameFrame.update()


    def loadMapAndRole(self):
        dataFile = os.getcwd() + "/MapAndRole" + ".json"
        gameFrame = self._gameFrame

        if os.path.isfile(dataFile):
            with open(dataFile, "r", encoding="utf-8") as json_file:
                self._mapAndRole = json.load(json_file)['data']
                for map in list(self._mapAndRole.keys()):
                    gameFrame._notice_text += "✔ + " + map + "\n"



    def setMap(self): # 장소 설정
        data = self._mapAndRole
        self._nowMap = random.choice(list(data.keys()))


    def setRole(self): # 역할 설정

        data = self._mapAndRole

        spys = []

        playerList = list(self._ingamePlayer.keys())

        rd = random.randint(0, len(playerList) - 1)
        spys.append(self._ingamePlayer[playerList[rd]])
        del playerList[rd]

        if len(playerList) >= 8: # 아직도 8명 이상 남았다면
            rd = random.randint(0, len(playerList) - 1)
            spys.append(playerList[rd])
            del playerList[rd] # 1명 더 뽑기

        for spy in spys:
            spy._role = self._spyName

        roleList = data[self._nowMap]['역할']

        for player in self._ingamePlayer.values():
            if player._role == "None":
                rd = random.randint(0, len(roleList) - 1)
                role = roleList[rd]
                player._role = role
                del roleList[rd]

    def setQuestionTarget(self, fromID, targetID):
        self._question_from = fromID
        self._question_target = targetID
        playBGM(self._voice, BGM_TYPE.CHANGE_BADGE)

    async def sendCard(self, player, isShowcard=False):
        data = self._mapAndRole
        map = self._nowMap
        mapUrl = data[map]['이미지_주소']

        if player._role == self._spyName:
            card = CardFrame(self._spyMap, player._role, self._spyUrl, self._guild.name, isShowcard, user=player._user)
        else:
            card = CardFrame(map, player._role, mapUrl, self._guild.name, isShowcard, user=player._user)
        embed = getEmbedFromFrame(card)
        if isShowcard:
            asyncio.ensure_future(self._chatChannel.send(embed=embed))
        else:
            asyncio.ensure_future(player._user.send(embed=embed))


    async def timer(self): # 타이머 카운트다운
        gameData = self
        gameFrame = self._gameFrame

        while True:

            if gameData._question_from == None:
                question_fromName = ""
            else:
                question_fromName = gameData._ingamePlayer[gameData._question_from]._user.display_name

            question_targetName = gameData._ingamePlayer[gameData._question_target]._user.display_name

            gameFrame._sub_text = "```"
            gameFrame._sub_text += EMOJI_ICON.ICON_QUESTION + "현재 질문자: **[ " + question_fromName + " ]**\n"
            gameFrame._sub_text += EMOJI_ICON.ICON_ANSWER + "현재 답변자: **[ " + question_targetName + " ]**\n"
            gameFrame._sub_text += "```"
            gameFrame._customFooter_text = getClockIcon(gameData._leftTime, gameData._maxTime) + " 투표까지 " + str(gameData._leftTime)+"초" # 남은 시간 표시

            gameFrame._field_text.clear()
            for player in gameData._ingamePlayer.values():
                if gameData._question_from == player._user.id:
                    gameData._gameFrame.addField(player._user.display_name, EMOJI_ICON.ICON_QUESTION)
                elif gameData._question_target == player._user.id:
                    gameData._gameFrame.addField(player._user.display_name, EMOJI_ICON.ICON_ANSWER)
                else:
                    gameData._gameFrame.addField(player._user.display_name, EMOJI_ICON.ICON_CARD)

            await self.updateUI()
            if self._leftTime <= 0 or self._gameStep != GAME_STEP.INGAME:
                break
            await asyncio.sleep(1)
            self._leftTime -= 1


    async def answerSpy(self, user, place):

        gameData = self
        print(gameData._nowMap)

        if user.id in self._ingamePlayer: # 게임 참가중이라면
            player = self._ingamePlayer[user.id]
            if player._role == self._spyName: #스파이라면
                if gameData._gameStep == GAME_STEP.INGAME: # 게임 진행 중 상태면
                    if not self._isAnswering:
                        gameData._gameStep = GAME_STEP.TOTALIZE
                        playBGM(self._voice, BGM_TYPE.SCORE_ALARM)
                        for player in self._ingamePlayer.values():
                            if player._role == self._spyName: # 스파이들 정체 공개
                                await self.sendCard(player, isShowcard=True)
                        asyncio.ensure_future(self._chatChannel.send("```" + EMOJI_ICON.ICON_TIP + " " +"스파이가 자신의 정체를 공개하였습니다.\n" + "스파이는 모두가 있는 장소를 맞춰주세요.\n["+Config.BOT_PREFIX+"정답 <장소이름>] 명령어를 사용해 입력하세요.```"))
                        await self.answerTimer()
                        if self._answer_leftTime <= 0: # 시간 초과면
                            await self.civilWin()
                elif gameData._gameStep == GAME_STEP.TOTALIZE:
                    if self._isAnswering:
                        asyncio.ensure_future(self._chatChannel.send("```제출한 답: "+place+"```"))
                        asyncio.ensure_future(self._chatChannel.send("```"+EMOJI_ICON.ICON_TIP+"정답은 과연...?```"))
                        await asyncio.sleep(3)

                        if place == self._nowMap: #정답 맞췄다면
                            await self.spyWin() # 스파이 승리
                        else: # 틀렸다면
                            await self.civilWin() # 시민 승리



    async def answerTimer(self):

        gameData = self
        gameFrame = self._gameFrame

        self._isAnswering = True

        self._answer_leftTime = self._answer_maxTime

        gameFrame._gameStep = GAME_STEP.TOTALIZE

        gameFrame._title_text = chr(173)+"[　　　　"+ EMOJI_ICON.ICON_GAME +" 스파이 공개　　　　]"

        gameFrame._sub_visible = True
        gameFrame._sub_text = EMOJI_ICON.ICON_VOTE + "　**스파이의 정답을 기다리는 중**\n" + chr(173) + "\n"

        gameFrame._main_visible = False

        gameFrame._notice_visible = True
        gameFrame._notice_text = EMOJI_ICON.ICON_NOTE + " **["+Config.BOT_PREFIX+"정답 장소이름] 명령어를 사용해\n정답 제출 가능\n" + chr(173) + "\n"
        for map in list(self._mapAndRole.keys()):
            gameFrame._notice_text += "✔ + " + map + "\n"

        gameFrame._field_visible = False

        gameFrame._customFooter_visible = True
        gameFrame._customFooter_text = ""

        gameFrame._page_visible = False

        gameFrame._path_visible = False

        gameFrame._image_visible = False
        gameFrame._image_url = self._spyUrl

        gameFrame._embedColor = discord.Color.dark_purple()

        while True:

            gameFrame._customFooter_text = getClockIcon(gameData._answer_leftTime, gameData._answer_maxTime) + " 제한시간 " + str(gameData._answer_leftTime) +"초"# 남은 시간 표시

            await self.updateUI()

            if self._answer_leftTime <= 0 or self._gameStep != GAME_STEP.TOTALIZE:
                break
            await asyncio.sleep(1)
            self._answer_leftTime -= 1


    async def voteTimer(self): # 타이머 카운트다운

        gameData = self
        gameFrame = self._gameFrame

        while True:

            gameFrame._sub_text = EMOJI_ICON.ICON_VOTE + "　**투표 현황**\n" + chr(173) + "\n"
            for player in self._ingamePlayer.values():
                if player._vote_target != None:
                    gameFrame._sub_text += getRandomHumanIcon() + "　**"+player._user.display_name + " -> "+player._vote_target.display_name+"**\n"

            gameFrame._customFooter_text = getClockIcon(gameData._vote_leftTime, gameData._vote_maxTime) + " 투표 종료까지 " + str(gameData._vote_leftTime) +"초"# 남은 시간 표시

            await self.updateUI()

            isAllVote = True
            for player in self._ingamePlayer.values():
                if player._vote_target == None:
                    isAllVote = False
                    break

            if isAllVote: # 모두 투표하면 바로 다음으로
                self._gameStep = GAME_STEP.RESULT

            if self._vote_leftTime <= 0 or self._gameStep != GAME_STEP.TOTALIZE:
                break
            await asyncio.sleep(1)
            self._vote_leftTime -= 1


    async def vote(self):

        gameFrame = self._gameFrame

        while True:

            playBGM(self._voice, BGM_TYPE.VOTE_TIME)

            self._vote_leftTime = self._vote_maxTime

            for player in self._ingamePlayer.values():
                player._vote_target = None

            gameFrame._gameStep = GAME_STEP.TOTALIZE

            gameFrame._title_text = chr(173)+"[　　　　"+ EMOJI_ICON.ICON_GAME +" 투표　　　　]"

            gameFrame._sub_visible = True
            gameFrame._sub_text = EMOJI_ICON.ICON_VOTE + "　**투표 현황**\n" + chr(173) + "\n"

            gameFrame._main_visible = False

            gameFrame._notice_visible = True
            gameFrame._notice_text = EMOJI_ICON.ICON_NOTE + " **[ @닉네임 ]** 으로 맨션 기능을 사용해\n투표가 가능합니다.\n" + chr(173) + "\n"

            gameFrame._field_visible = False

            gameFrame._customFooter_visible = True
            gameFrame._customFooter_text = ""

            gameFrame._page_visible = False

            gameFrame._path_visible = False

            gameFrame._image_visible = False
            gameFrame._image_url = ""

            gameFrame._embedColor = discord.Color.light_gray()

            await self.voteTimer()

            topPlayer = self.totalizeVote()
            playBGM(self._voice, BGM_TYPE.SCORE_ALARM)
            if topPlayer != None:

                if topPlayer in self._votedPlayer: # 이미 투표된 플레이어면
                    asyncio.ensure_future(self._chatChannel.send("```" + EMOJI_ICON.ICON_TIP + " " + ""+str(topPlayer.display_name)+" 님은 이미 스파이로 지목됐습니다. 재투표를 진행합니다.```"))
                    continue
                else:
                    asyncio.ensure_future(self._chatChannel.send("```" + EMOJI_ICON.ICON_TIP + " " + ""+str(topPlayer.display_name)+" 님이 스파이로 지목됐습니다.```"))
                    self._votedPlayer.append(topPlayer)
                break
            else:
                asyncio.ensure_future(self._chatChannel.send("```" + EMOJI_ICON.ICON_TIP + " " + "최다 득표를 받은 플레이어가 없습니다. 재투표를 진행합니다.```"))
                continue



    def totalizeVote(self):
        voteMap = dict()

        for player in self._ingamePlayer.values():
            target = player._vote_target
            if target == None:
                continue
            if target in voteMap:
                voteMap[target] += 1
            else:
                voteMap[target] = 1

        sortList = sorted(voteMap.items(), key=operator.itemgetter(1))

        topPlayer = None
        if len(sortList) > 0: #
            topPlayer = sortList[0][0]
            if len(sortList) > 1:
                if sortList[0][1] == sortList[1][1]: # 1등, 2등 동표면
                    topPlayer = None

        return topPlayer



    async def spyWin(self):
        playBGM(self._voice, BGM_TYPE.SUCCESS)
        asyncio.ensure_future(self._chatChannel.send("```멋쟁이 스파이 팀이 승리하였습니다.```"))
        winText = "```"+EMOJI_ICON.ICON_TIP+" [ 스파이팀 승리! ]```"

        resultFrame = ResultFrame(self, winText)
        embed = getEmbedFromFrame(resultFrame)

        asyncio.ensure_future(self._chatChannel.send(embed=embed))

        await self.endGame() # 게임 종료

    async def civilWin(self):
        playBGM(self._voice, BGM_TYPE.SUCCESS)
        asyncio.ensure_future(self._chatChannel.send("```멋쟁이 시민 팀이 승리하였습니다.```"))
        winText = "```"+EMOJI_ICON.ICON_TIP+" [ 시민팀 승리! ]```"

        resultFrame = ResultFrame(self, winText)
        embed = getEmbedFromFrame(resultFrame)

        asyncio.ensure_future(self._chatChannel.send(embed=embed))

        await self.endGame() # 게임 종료


    async def endGame(self):
        self._gameStep = GAME_STEP.FINISH
        del gameData[self._guild.id] # 게임 데이터 삭제
        asyncio.ensure_future(self._chatChannel.send("```게임이 종료되었습니다.```"))
        await self._voice.disconnect()


    async def on_message(self, message):
        mentions = message.mentions
        if len(mentions) == 0: return
        target = mentions[0]
        user = message.author

        isRemoveMsg = False
        if not user.id in self._ingamePlayer or not target.id in self._ingamePlayer: # 게임 참가중이 아닌 사람이 했다면
            isRemoveMsg = True
        else:
            if self._gameStep == GAME_STEP.INGAME: # 게임 진행중이면
                isRemoveMsg = True
                if user.id == self._question_target: # 질문 뱃지 가지고 있다면
                    if self._question_from == None or self._question_from != target.id: # 이전 질문자가 아니라면
                        if target.id == user.id: # 자신에게 한 거라면
                            asyncio.ensure_future(user.send("```스스로에게 질문할 수 없습니다.```"))
                        else:
                            self.setQuestionTarget(user.id, target.id) # 뱃지 변경
                    else:
                        asyncio.ensure_future(user.send("```당신에게 질문한 사람에게는 바로 다시 질문할 수 없습니다.```"))


            elif self._gameStep == GAME_STEP.TOTALIZE: # 투표 등등 진행중이면
                isRemoveMsg = True
                if self._leftTime <= 0: # 투표 진행중이면
                    player = self._ingamePlayer[user.id]
                    player._vote_target = target # 투표 타겟 설정

        if isRemoveMsg:
            asyncio.ensure_future(message.delete()) # 쓸모없는 메시지는 삭제
            

class Playerdata:
    def __init__(self, user):
        self._user = user # 유저 객체
        self._role = "None" # 직업
        self._vote_target = None # 투표 대상


#### 전역 변수
gameData = dict()


#### 함수
async def helpMessage(ctx): #도움말
    sendStr = EMOJI_ICON.ICON_TIP + "[ 도움말 ]\n" + chr(173) + "\n"
    sendStr += EMOJI_ICON.ICON_BOOK_RED + " ~스파이폴 - 게임을 시작합니다.\n"
    sendStr += EMOJI_ICON.ICON_BOOK_RED + " ~중지 - 게임을 강제로 중지합니다.\n"

    sendStr += chr(173) + "\n"

    sendStr += "봇 이름:　" + "스파이폴\n"
    sendStr += "봇 버전:　" + Config.VERSION + "\n"
    sendStr += "제작 　:　제육보끔#1916\n"
    sendStr += "패치일 :　" + Config.LAST_PATCH + "\n"

    sendStr += chr(173) + "\n"

    sendStr += EMOJI_ICON.ICON_PHONE + " Contact\n" +chr(173) + "\n"
    sendStr += EMOJI_ICON.ICON_MAIL + " 이메일:　" + Config.EMAIL_ADDRESS + "\n"
    sendStr += EMOJI_ICON.ICON_BOOK_RED + " 봇 공유링크:　"+Config.BOT_LINK + "\n"
    sendStr += EMOJI_ICON.ICON_GIT + " 깃허브:　"+"https://github.com/OtterBK/Spyfall" + "\n"
    sendStr += chr(173) + "\n" + EMOJI_ICON.ICON_FIX + "버그 제보, 개선점, 건의사항이 있다면 상단 이메일 주소로 알려주세요!\n" + chr(173) + "\n"

    asyncio.ensure_future(ctx.send("```" + chr(173) +"\n" + str(sendStr) + "\n```"))


async def clearChat(exclude, chatChannel): #메시지 삭제
    def check(msg):
        return not msg in exclude

    try:
        asyncio.ensure_future(chatChannel.purge(check=check, limit=100))
    except:
        Logger.error("clearchat error")
        Logger.error(traceback.format_exc())


def getGamedata(guildID):
    if guildID in gameData:
        return gameData[guildID]
    else:
        return None


async def sendLobbyMessage(ctx):

    guild = ctx.guild
    chattingChannel = ctx.message.channel  # 퀴즈할 채팅 채널 얻기
    owner = ctx.message.author

    if owner.voice == None:
        await ctx.send("```"+EMOJI_ICON.ICON_WARN + " 먼저 음성 채널에 참가해주세요.```")
        return

    voiceChannel = owner.voice.channel  # 호출자의 음성 채널 얻기

    isSuccess = False
    voice = get(bot.voice_clients, guild=guild)
    if voice == None or not voice.is_connected():  # 음성 연결 안됐다면
        try:
            voice = await voiceChannel.connect()  # 음성 채널 연결후 해당 객체 반환
            isSuccess = True
        except: #보통 Already voice connected 문제 발생시
            isSuccess = False
            Logger.error(traceback.format_exc())
            asyncio.ensure_future(chattingChannel.send("❗ 예기치 못한 문제가 발생하였습니다. 재시도해주세요. \n해당 문제가 지속적으로 발생할 시 \n💌 [ "+Config.EMAIL_ADDRESS+" ] 으로 문의바랍니다.\n"))
            if voice == None:
                asyncio.ensure_future(chattingChannel.send("voice == None"))
            elif voice.is_connected():
                asyncio.ensure_future(chattingChannel.send("voice is connected"))
            await voice.move_to(voiceChannel)
            await asyncio.sleep(1)
            await voice.disconnect() #보이스 강제로 연결끊기

    if not isSuccess:
        tmpVoice = get(bot.voice_clients, channel=voiceChannel)
        tmpVoice.disconnect()

    frame = LobbyFrame()

    tmpEmbed = discord.Embed(
        title="초기화중... 잠시만 기다려주세요.", url="", description="\n▽", color=discord.Color.dark_magenta())

    message = await ctx.send(embed=tmpEmbed)

    gameData[ctx.guild.id] = Gamedata(ctx.guild, message, ctx.message.author, voice) # 게임 데이터 등록

    playBGM(voice, BGM_TYPE.BELL)

    asyncio.ensure_future(message.add_reaction(EMOJI_ICON.JOIN)) # 참여
    asyncio.ensure_future(message.add_reaction(EMOJI_ICON.START)) # 시작

    await showFrame(message, frame, isPopUp=False)

    return message


def playBGM(voice, bgmType): #BGM 틀기
    try:
        if(bgmType == BGM_TYPE.PLING):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "pling.mp3")
        elif(bgmType == BGM_TYPE.ROUND_ALARM):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "ROUND_ALARM.mp3")
        elif(bgmType == BGM_TYPE.SCORE_ALARM):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "SCORE_ALARM.mp3")
        elif(bgmType == BGM_TYPE.ENDING):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "ENDING.mp3")
        elif(bgmType == BGM_TYPE.FAIL):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "FAIL.mp3")
        elif(bgmType == BGM_TYPE.countdown10):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "countdown10.wav")
        elif(bgmType == BGM_TYPE.SUCCESS):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "SUCCESS.mp3")
        elif(bgmType == BGM_TYPE.BELL):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "bell.mp3")
        elif(bgmType == BGM_TYPE.CARD_DRAW):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "CARD_DRAW.mp3")
        elif(bgmType == BGM_TYPE.CHANGE_BADGE):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "CHANGE_BADGE.mp3")
        elif(bgmType == BGM_TYPE.VOTE_TIME):
            source = discord.FFmpegPCMAudio(Config.BGM_PATH + "VOTE_TIME.mp3")

        voice.play(source)
    except:
        Logger.error("error01 - voice is not connect error")
        Logger.error(traceback.format_exc())


#### 이벤트
@bot.event
async def on_ready():
    Logger.info(f'{bot.user} 활성화됨')
    await bot.change_presence(status=discord.Status.online) #온라인
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="~도움말"))

    Logger.info("봇 이름:" + str(bot.user.name) + ", 봇 아이디:" + str(bot.user.name) + ", 봇 버전:" + discord.__version__)
    for guild in bot.guilds:
        print(guild.name)
    Logger.info(str(len(bot.guilds)) + "개의 서버 연결됨")

@bot.command(pass_context=False, aliases=["ping"])  # ping 명령어 입력시
async def pingCommand(ctx):  # ping 테스트
    asyncio.ensure_future(ctx.send(f"핑 : {round(bot.latency * 1000)}ms"))

@bot.command(pass_context=False, aliases=["도움", "도움말","명령어", "commands"])  # 도움말 명령어 입력시
async def helpCommand(ctx):  # 도움말
    asyncio.ensure_future(helpMessage(ctx))

@bot.command(pass_context=False, aliases=["규칙"])  # 규칙 명령어 입력시
async def ruleCommand(ctx):  # 도움말
    asyncio.ensure_future(ctx.send("https://youtu.be/c_MXwC4tdg8"))

@bot.command(pass_context=False, aliases=["스파이폴"])  # 스파이폴 명령어 입력시
async def spyfallCommand(ctx, gamesrc=None):  # 보드게임 선택 UI 생성
    if gamesrc == None:
        guild = ctx.guild #서버
        if guild == None:
            return
        gameData = getGamedata(guild.id)
        
        if gameData != None: # 게임 진행중이면
            if gameData._gameStep != GAME_STEP.LOBBY: # 게임 진행 중 상태면
                asyncio.ensure_future(ctx.send("```" + EMOJI_ICON.ICON_TIP + " " + "먼저 진행중인 스파이폴 게임을 중지해주세요.\n[ ~중지 ]```"))
                return
                
        await sendLobbyMessage(ctx)


@bot.command(pass_context=False, aliases=["정답"])  # 정답 명령어 입력시
async def answerCommand(ctx, gamesrc=None):  # 보드게임 선택 UI 생성
    guild = ctx.guild #서버
    gameData = getGamedata(guild.id)

    if gameData != None: # 게임 진행중이면
        await gameData.answerSpy(ctx.message.author, gamesrc)

@bot.command(pass_context=False, aliases=["중지"])  # 정답 명령어 입력시
async def stopCommand(ctx, gamesrc=None):  # 보드게임 선택 UI 생성
    guild = ctx.guild #서버
    gameData = getGamedata(guild.id)
    user = ctx.message.author

    if gameData != None: # 게임 진행중이면
        if gameData._owner.id == user.id: 
            await gameData.endGame()
        else:
            asyncio.ensure_future(ctx.send("```" + EMOJI_ICON.ICON_TIP + " " + "게임 주최자 [ "+gameData._owner.display_name + " ] 님만이 중지할 수 있습니다.```")) #이벤트 동작
    else:
        asyncio.ensure_future(ctx.send("```" + EMOJI_ICON.ICON_TIP + " " + "진행 중인 게임이 없습니다.```"))


@bot.event
async def on_message(message):
    # 봇이 입력한 메시지라면 무시하고 넘어간다.
    if message.author == bot.user:
        return
    elif message.content.startswith(Config.BOT_PREFIX):  # 명령어면 return
        asyncio.ensure_future(bot.process_commands(message))
        return
    else:
        gameData = getGamedata(message.guild.id)
        if gameData == None:  # 게임데이터가 없으면 return
            return
        if message.channel != gameData._chatChannel: #채팅 채널이 게임데이터에 저장된 채팅채널과 일치하지 않으면
            return

        asyncio.ensure_future(gameData.on_message(message)) #메세지 이벤트 동작



@bot.event
async def on_raw_reaction_add(payload):
    try:
        guild = bot.get_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        gameData = getGamedata(guild.id)
        emoji = payload.emoji

        if user == bot.user:  # 봇이 입력  한거면
            return  # 건너뛰어

        if gameData != None: # 게임 진행중이라면
            if gameData._chatChannel.id == payload.channel_id: # 게임 진행중인 채널이면
                await gameData._frameStack[len(gameData._frameStack)-1].on_reaction_add(message, emoji, user) # 각 프레임에 맞는 이벤트 작동
    except:
        Logger.error(traceback.format_exc())


@bot.event
async def on_raw_reaction_remove(payload):
    try:
        guild = bot.get_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        gameData = getGamedata(guild.id)
        emoji = payload.emoji

        if user == bot.user:  # 봇이 삭제한거면
            return  # 건너뛰어

        if gameData != None: # 게임 진행중이라면
            if gameData._chatChannel.id == payload.channel_id: # 게임 진행중인 채널이면
                await gameData._frameStack[len(gameData._frameStack)-1].on_reaction_remove(message, emoji, user) # 각 프레임에 맞는 이벤트 작동
    except:
        Logger.error(traceback.format_exc())




#커맨드 에러 핸들링
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error



#### 봇 실행
bot.run(Config.TOKEN)