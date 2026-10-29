#!/usr/bin/env python3
"""фактик_мәгълүмат QEMU/VNC에서 Терминал 모서리 сөйрәү_VALUE·күрсәткеч·동적 символ_VALUE_068c2631 оя_кертү·төзәтү_VALUE Эчтәлек_VALUE 보존를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from классик_карау import EXACT_VALUE
from үтәргә_команда import экранга_җибәрү_тамыр


def 창크기시험(너비, 높이, үлчәм_юл):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    үлчәмен_үзгәртү_СМС = '{}x{}'.format(너비, 높이)
    Процесс_VALUE = subprocess.Popen(['python3', str(экранга_җибәрү_тамыр/'Кораллар/үтәргә_команда.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', үлчәмен_үзгәртү_СМС], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    сайлагыч_a916db4e = selectors.DefaultSelector(); сайлагыч_a916db4e.register(Процесс_VALUE.stdout, selectors.EVENT_READ)
    LOG_юл = bytearray(); читтәге_VALUE = None; күчерү_VALUE_630ba093 = None; күрсәткеч_яшерен=[False]

    def 기다리기(күрсәтү_VALUE, эшләтү=0):
        마감 = time.monotonic() + 60
        while күрсәтү_VALUE not in LOG_юл[эшләтү:]:
            if time.monotonic() > 마감 or Процесс_VALUE.poll() is not None or b'HALTED' in LOG_юл or b'PANIC:' in LOG_юл:
                raise AssertionError(LOG_юл[эшләтү:].decode('utf-8', 'replace'))
            for вакыйга, _ in сайлагыч_a916db4e.select(.1):
                мәгълүмат = вакыйга.fileobj.read(65536)
                if мәгълүмат: LOG_юл.extend(мәгълүмат)
        return LOG_юл[эшләтү:].decode('utf-8', 'replace')

    def чирттерү_төймә(символ, 눌림=True): читтәге_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def СМС_җибәрү(Mäten):
        эшләтү = len(LOG_юл)
        for символ_VALUE_068c2631 in Mäten:
            символ = 0xff0d if символ_VALUE_068c2631 == '\n' else ord(символ_VALUE_068c2631) if ord(символ_VALUE_068c2631) < 256 else 0x1000000 | ord(символ_VALUE_068c2631)
            чирттерү_төймә(символ); чирттерү_төймә(символ, False)
        return эшләтү

    def тышча(Mäten): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', СМС_җибәрү(Mäten+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Вертикаль_урнаштыру, 눌림): читтәге_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Вертикаль_урнаштыру))

    def чирттерү_VALUE(가로, Вертикаль_урнаштыру): 가리키기(가로, Вертикаль_урнаштыру, 1); 가리키기(가로, Вертикаль_урнаштыру, 0)

    def нокталы_рәсем_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 фактик_мәгълүмат 너비를 쓴다.
        читтәге_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        сызым_VALUE = Image.new('RGB', (너비, 높이)); өлкә_VALUE = 0
        while True:
            종류 = EXACT_VALUE(читтәге_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                озынлык_VALUE = struct.unpack('>I', EXACT_VALUE(читтәге_VALUE, 7)[3:])[0]; EXACT_VALUE(читтәге_VALUE, озынлык_VALUE); continue
            assert 종류 == 0, 종류
            элемент_COUNT = struct.unpack('>H', EXACT_VALUE(читтәге_VALUE, 3)[1:])[0]
            for _ in range(элемент_COUNT):
                가로, Вертикаль_урнаштыру, 폭, озынлык_VALUE, кодлау_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(читтәге_VALUE, 12))
                if кодлау_VALUE == -239:
                    assert 폭==0 and озынлык_VALUE==0, 'remote cursor must be hidden'
                    күрсәткеч_яшерен[0]=True
                    continue
                assert кодлау_VALUE == 0 and 가로+폭 <= 너비 and Вертикаль_урнаштыру+озынлык_VALUE <= 높이
                сызым_VALUE.paste(Image.frombytes('RGB', (폭, озынлык_VALUE), EXACT_VALUE(читтәге_VALUE, 폭*озынлык_VALUE*4), 'raw', 'BGRX'), (가로, Вертикаль_урнаштыру))
                өлкә_VALUE += 폭*озынлык_VALUE
            if өлкә_VALUE:
                assert өлкә_VALUE == 너비*높이, өлкә_VALUE
                return сызым_VALUE

    def чек_нокта(координат_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            сызым_VALUE = нокталы_рәсем_IMAGE()
            if сызым_VALUE.getpixel(координат_VALUE) == 색: return сызым_VALUE
            if time.monotonic() > 마감: raise AssertionError((координат_VALUE, сызым_VALUE.getpixel(координат_VALUE), 색))

    def йөкләп_җибәрү_Файллар(исем, мәгълүмат): күчерү_VALUE_630ba093.storbinary('STOR '+исем, io.BytesIO(мәгълүмат))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+үлчәмен_үзгәртү_СМС+' RGB32').encode() in LOG_юл
        print('BOOT:', үлчәмен_үзгәртү_СМС, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_юл).group(1))
        читтәге_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(читтәге_VALUE, 12) == b'RFB 003.008\n'; читтәге_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(читтәге_VALUE, EXACT_VALUE(читтәге_VALUE, 1)[0]); читтәге_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(читтәге_VALUE, 4) == b'\0'*4; читтәге_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(читтәге_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(читтәге_VALUE, struct.unpack('>I', 초기[20:])[0])
        читтәге_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        читтәге_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        чек_нокта((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for вакыйга,_ in сайлагыч_a916db4e.select(.02):
                    мәгълүмат=вакыйга.fileobj.read(65536)
                    if мәгълүмат:LOG_юл.extend(мәгълүмат)
        тәрәз=[12,48,568,360]
        def раслау_үлчәмен_үзгәртү():
            COLUMN_VALUE,юл_VALUE_fc48bc81=(тәрәз[2]-24)//8,(тәрәз[3]-56)//16
            Mäten=тышча('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,юл_VALUE_fc48bc81) in Mäten,Mäten
            # фактик_мәгълүмат тәрәз 테두리: 단지 үлчәмен_үзгәртү таләп_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            чек_нокта((тәрәз[0],тәрәз[1]),(32,80,144))
            сызым_VALUE=чек_нокта((тәрәз[0]+тәрәз[2]-1,тәрәз[1]+тәрәз[3]-1),(39,49,64))
            return сызым_VALUE
        def 모서리(방향):
            return (тәрәз[0]+(3 if 방향 in (1,3) else тәрәз[2]-4),тәрәз[1]+(3 if 방향<=2 else тәрәз[3]-4))
        def зурлыкны_үзгәртү_сөйрәү(방향,차이,төймә=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            чек_нокта(흰점,(255,255,255))
            가리키기(가,세,төймә)
            끝가=max(0,min(너비-1,가+차이[0]));тәмамлау_Вертикаль=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,тәмамлау_Вертикаль,төймә);가리키기(끝가,тәмамлау_Вертикаль,0);숨고르기()
            if төймә==1:
                LEFT_VALUE,위,폭,озынлык_VALUE=тәрәз;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+озынлык_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+тәмамлау_Вертикаль-세))
                else:아래=max(위+216,min(높이,아래+тәмамлау_Вертикаль-세))
                тәрәз[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        раслау_үлчәмен_үзгәртү();assert күрсәткеч_яшерен[0]
        зурлыкны_үзгәртү_сөйрәү(4,(-100,-60),4);раслау_үлчәмен_үзгәртү() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            зурлыкны_үзгәртү_сөйрәү(방향,차이);раслау_үлчәмен_үзгәртү()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        СМС_җибәрү("echo '"+긴글+"'");숨고르기()
        зурлыкны_үзгәртү_сөйрәү(4,(-1000,-1000));assert тәрәз[2:]==[360,216]
        зурлыкны_үзгәртү_сөйрәү(4,(너비,높이))
        эшләтү=СМС_җибәрү('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),эшләтү);раслау_үлчәмен_үзгәртү()
        # vi가 төзәтү_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        тышча('ftpd start')
        күчерү_VALUE_630ba093=ftplib.FTP();күчерү_VALUE_630ba093.encoding='utf-8';күчерү_VALUE_630ba093.connect('127.0.0.1',접속번호,timeout=20);күчерү_VALUE_630ba093.login()
        기다리기(b'NORMAL',СМС_җибәрү('vi /크기자료.txt\n'))
        기다리기(b'INSERT',СМС_җибәрү('i미저장 한글 мәгълүмат\n'));숨고르기()
        зурлыкны_үзгәртү_сөйрәү(4,(-너비,-높이))
        # ANSI юл_VALUE_fc48bc81 이동에 새 юл_VALUE_fc48bc81 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((тәрәз[3]-56)//16)).encode() in LOG_юл[-4096:]
        СМС_җибәрү('작은 창에서도 이어 язу\n');숨고르기()
        зурлыкны_үзгәртү_сөйрәү(4,(너비,높이))
        СМС_җибәрү('큰 창에서도 이어 язу\n');숨고르기()
        чирттерү_төймә(0xff1b);чирттерү_төймә(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',СМС_җибәрү(':wq\n'))
        Эчтәлек_VALUE=bytearray();күчерү_VALUE_630ba093.retrbinary('RETR 크기자료.txt',Эчтәлек_VALUE.extend)
        assert Эчтәлек_VALUE=='미저장 한글 мәгълүмат\n작은 창에서도 이어 язу\n큰 창에서도 이어 язу\n'.encode(),Эчтәлек_VALUE
        раслау_үлчәмен_үзгәртү().save(str(үлчәм_юл/(үлчәмен_үзгәртү_СМС+'-large.png')))
        # 두 번째 창은 килешенгәнчә_кыйммәт үлчәмен_үзгәртү, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        эшләтү=len(LOG_юл);чирттерү_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',эшләтү)
        assert 'TERMINAL SIZE 68x19' in тышча('terminal size')
        эшләтү=len(LOG_юл);чирттерү_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',эшләтү);раслау_үлчәмен_үзгәртү()
        зурлыкны_үзгәртү_сөйрәү(4,(-너비,-높이));раслау_үлчәмен_үзгәртү().save(str(үлчәм_юл/(үлчәмен_үзгәртү_СМС+'-small.png')))
        # үлчәмен_үзгәртү үзгәртү_VALUE Артка_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        эшләтү=len(LOG_юл);чирттерү_VALUE(тәрәз[0]+тәрәз[2]-20,тәрәз[1]+15);기다리기(b'TERMINAL FOCUS 2',эшләтү)
        assert 'RESIZE CLOSED' in тышча('echo RESIZE CLOSED')
        print('PASS:',үлчәмен_үзгәртү_СМС,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if күчерү_VALUE_630ba093:күчерү_VALUE_630ba093.close()
        if читтәге_VALUE:читтәге_VALUE.close()
        if Процесс_VALUE.poll() is None:
            Процесс_VALUE.terminate()
            try:Процесс_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Процесс_VALUE.kill();Процесс_VALUE.wait()
        сайлагыч_a916db4e.close();Процесс_VALUE.stdout.close();(үлчәм_юл/(үлчәмен_үзгәртү_СМС+'.log')).write_bytes(LOG_юл)


def эшләтү():
    үлчәм_юл=экранга_җибәрү_тамыр/'build/verification/resize';үлчәм_юл.mkdir(parents=True,exist_ok=True)
    LOG_юл={'passed':False,'kernel_sha256':hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,үлчәм_юл);LOG_юл['resolutions'].append([너비,높이])
        LOG_юл.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(үлчәм_юл/'report.json').write_text(json.dumps(LOG_юл,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':эшләтү()
