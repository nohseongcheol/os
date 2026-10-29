#!/usr/bin/env python3
"""актуалдуу_берилмелер QEMU/VNC에서 Терминал 모서리 суйрөө_маани·көрсөткүч·동적 символ_маани_068c2631 оюкча_киргизме_жазуу·түзөтүү_маани Мазмун_маани 보존를 검사한다."""
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
from иш_такта_көрүү import 정확한값
from аткаруу_буйрук import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    көлөм_СМС = '{}x{}'.format(너비, 높이)
    Процесс_маани = subprocess.Popen(['python3', str(기준/'Куралдар/аткаруу_буйрук.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', көлөм_СМС], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector(); селектор_a916db4e.register(Процесс_маани.stdout, selectors.EVENT_READ)
    жазуу_катар = bytearray(); алыскы_маани = None; ташүү_маани = None; көрсөткүч_жашырылган=[False]

    def 기다리기(көрсөтүү_маани, Жүргүзүү=0):
        마감 = time.monotonic() + 60
        while көрсөтүү_маани not in жазуу_катар[Жүргүзүү:]:
            if time.monotonic() > 마감 or Процесс_маани.poll() is not None or b'HALTED' in жазуу_катар or b'PANIC:' in жазуу_катар:
                raise AssertionError(жазуу_катар[Жүргүзүү:].decode('utf-8', 'replace'))
            for окуя, _ in селектор_a916db4e.select(.1):
                берилмелер = окуя.fileobj.read(65536)
                if берилмелер: жазуу_катар.extend(берилмелер)
        return жазуу_катар[Жүргүзүү:].decode('utf-8', 'replace')

    def баскылоо_баскыч(символ, 눌림=True): алыскы_маани.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def СМС_жөнөтүү(Текст):
        Жүргүзүү = len(жазуу_катар)
        for символ_маани_068c2631 in Текст:
            символ = 0xff0d if символ_маани_068c2631 == '\n' else ord(символ_маани_068c2631) if ord(символ_маани_068c2631) < 256 else 0x1000000 | ord(символ_маани_068c2631)
            баскылоо_баскыч(символ); баскылоо_баскыч(символ, False)
        return Жүргүзүү

    def сырты(Текст): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', СМС_жөнөтүү(Текст+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): алыскы_маани.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def баскылоо_маани(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def битмап_сүрөт():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 актуалдуу_берилмелер 너비를 쓴다.
        алыскы_маани.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        чийүү_маани = Image.new('RGB', (너비, 높이)); аймак_маани = 0
        while True:
            종류 = 정확한값(алыскы_маани, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                узундук_маани = struct.unpack('>I', 정확한값(алыскы_маани, 7)[3:])[0]; 정확한값(алыскы_маани, узундук_маани); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(алыскы_маани, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, узундук_маани, коддоо_маани = struct.unpack('>HHHHi', 정확한값(алыскы_маани, 12))
                if коддоо_маани == -239:
                    assert 폭==0 and узундук_маани==0, 'remote cursor must be hidden'
                    көрсөткүч_жашырылган[0]=True
                    continue
                assert коддоо_маани == 0 and 가로+폭 <= 너비 and 세로+узундук_маани <= 높이
                чийүү_маани.paste(Image.frombytes('RGB', (폭, узундук_маани), 정확한값(алыскы_маани, 폭*узундук_маани*4), 'raw', 'BGRX'), (가로, 세로))
                аймак_маани += 폭*узундук_маани
            if аймак_маани:
                assert аймак_маани == 너비*높이, аймак_маани
                return чийүү_маани

    def чек_пиксел(координат_маани, 색):
        마감 = time.monotonic()+10
        while True:
            чийүү_маани = битмап_сүрөт()
            if чийүү_маани.getpixel(координат_маани) == 색: return чийүү_маани
            if time.monotonic() > 마감: raise AssertionError((координат_маани, чийүү_маани.getpixel(координат_маани), 색))

    def жүктөп_жөнөтүү_Файлдар(Аты, берилмелер): ташүү_маани.storbinary('STOR '+Аты, io.BytesIO(берилмелер))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+көлөм_СМС+' RGB32').encode() in жазуу_катар
        print('BOOT:', көлөм_СМС, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', жазуу_катар).group(1))
        алыскы_маани = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(алыскы_маани, 12) == b'RFB 003.008\n'; алыскы_маани.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(алыскы_маани, 정확한값(алыскы_маани, 1)[0]); алыскы_маани.sendall(b'\x01')
        assert 정확한값(алыскы_маани, 4) == b'\0'*4; алыскы_маани.sendall(b'\x01')
        초기 = 정확한값(алыскы_маани, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(алыскы_маани, struct.unpack('>I', 초기[20:])[0])
        алыскы_маани.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        алыскы_маани.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        чек_пиксел((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for окуя,_ in селектор_a916db4e.select(.02):
                    берилмелер=окуя.fileobj.read(65536)
                    if берилмелер:жазуу_катар.extend(берилмелер)
        терезе=[12,48,568,360]
        def тууралыгын_аныктоо_көлөм():
            тилке_маани,катар_маани=(терезе[2]-24)//8,(терезе[3]-56)//16
            Текст=сырты('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(тилке_маани,катар_маани) in Текст,Текст
            # актуалдуу_берилмелер терезе 테두리: 단지 Өлчөмү сурам_маани 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            чек_пиксел((терезе[0],терезе[1]),(32,80,144))
            чийүү_маани=чек_пиксел((терезе[0]+терезе[2]-1,терезе[1]+терезе[3]-1),(39,49,64))
            return чийүү_маани
        def 모서리(방향):
            return (терезе[0]+(3 if 방향 in (1,3) else терезе[2]-4),терезе[1]+(3 if 방향<=2 else терезе[3]-4))
        def өлчөмдү_өзгөртүү_суйрөө(방향,차이,баскыч=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            чек_пиксел(흰점,(255,255,255))
            가리키기(가,세,баскыч)
            끝가=max(0,min(너비-1,가+차이[0]));аяктоо_Архив=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,аяктоо_Архив,баскыч);가리키기(끝가,аяктоо_Архив,0);숨고르기()
            if баскыч==1:
                왼,위,폭,узундук_маани=терезе;오른,아래=왼+폭,위+узундук_маани
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+аяктоо_Архив-세))
                else:아래=max(위+216,min(높이,아래+аяктоо_Архив-세))
                терезе[:]=[왼,위,오른-왼,아래-위]
        тууралыгын_аныктоо_көлөм();assert көрсөткүч_жашырылган[0]
        өлчөмдү_өзгөртүү_суйрөө(4,(-100,-60),4);тууралыгын_аныктоо_көлөм() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            өлчөмдү_өзгөртүү_суйрөө(방향,차이);тууралыгын_аныктоо_көлөм()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        СМС_жөнөтүү("echo '"+긴글+"'");숨고르기()
        өлчөмдү_өзгөртүү_суйрөө(4,(-1000,-1000));assert терезе[2:]==[360,216]
        өлчөмдү_өзгөртүү_суйрөө(4,(너비,높이))
        Жүргүзүү=СМС_жөнөтүү('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Жүргүзүү);тууралыгын_аныктоо_көлөм()
        # vi가 түзөтүү_маани 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        сырты('ftpd start')
        ташүү_маани=ftplib.FTP();ташүү_маани.encoding='utf-8';ташүү_маани.connect('127.0.0.1',접속번호,timeout=20);ташүү_маани.login()
        기다리기(b'NORMAL',СМС_жөнөтүү('vi /크기자료.txt\n'))
        기다리기(b'INSERT',СМС_жөнөтүү('i미저장 한글 берилмелер\n'));숨고르기()
        өлчөмдү_өзгөртүү_суйрөө(4,(-너비,-높이))
        # ANSI катар_маани 이동에 새 катар_маани 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((терезе[3]-56)//16)).encode() in жазуу_катар[-4096:]
        СМС_жөнөтүү('작은 창에서도 이어 Жазуу\n');숨고르기()
        өлчөмдү_өзгөртүү_суйрөө(4,(너비,높이))
        СМС_жөнөтүү('큰 창에서도 이어 Жазуу\n');숨고르기()
        баскылоо_баскыч(0xff1b);баскылоо_баскыч(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',СМС_жөнөтүү(':wq\n'))
        Мазмун_маани=bytearray();ташүү_маани.retrbinary('RETR 크기자료.txt',Мазмун_маани.extend)
        assert Мазмун_маани=='미저장 한글 берилмелер\n작은 창에서도 이어 Жазуу\n큰 창에서도 이어 Жазуу\n'.encode(),Мазмун_маани
        тууралыгын_аныктоо_көлөм().save(str(결과경로/(көлөм_СМС+'-large.png')))
        # 두 번째 창은 жарыяланбаган_маани Өлчөмү, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Жүргүзүү=len(жазуу_катар);баскылоо_маани(70,16);기다리기(b'TERMINAL FOCUS 2',Жүргүзүү)
        assert 'TERMINAL SIZE 68x19' in сырты('terminal size')
        Жүргүзүү=len(жазуу_катар);баскылоо_маани(180,16);기다리기(b'TERMINAL FOCUS 1',Жүргүзүү);тууралыгын_аныктоо_көлөм()
        өлчөмдү_өзгөртүү_суйрөө(4,(-너비,-높이));тууралыгын_аныктоо_көлөм().save(str(결과경로/(көлөм_СМС+'-small.png')))
        # Өлчөмү өзгөртүү_маани Артка_маани X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Жүргүзүү=len(жазуу_катар);баскылоо_маани(терезе[0]+терезе[2]-20,терезе[1]+15);기다리기(b'TERMINAL FOCUS 2',Жүргүзүү)
        assert 'RESIZE CLOSED' in сырты('echo RESIZE CLOSED')
        print('PASS:',көлөм_СМС,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if ташүү_маани:ташүү_маани.close()
        if алыскы_маани:алыскы_маани.close()
        if Процесс_маани.poll() is None:
            Процесс_маани.terminate()
            try:Процесс_маани.wait(timeout=8)
            except subprocess.TimeoutExpired:Процесс_маани.kill();Процесс_маани.wait()
        селектор_a916db4e.close();Процесс_маани.stdout.close();(결과경로/(көлөм_СМС+'.log')).write_bytes(жазуу_катар)


def Жүргүзүү():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    жазуу_катар={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);жазуу_катар['resolutions'].append([너비,높이])
        жазуу_катар.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(жазуу_катар,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Жүргүзүү()
