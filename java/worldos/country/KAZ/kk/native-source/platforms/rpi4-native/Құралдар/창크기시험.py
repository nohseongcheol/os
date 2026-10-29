#!/usr/bin/env python3
"""нақты_деректер QEMU/VNC에서 Терминал 모서리 апару_мән·меңзер·동적 таңба_мән 칸·өңдеу_мән мазмұн_мән 보존를 검사한다."""
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
from үстелдік_Көрініс import 정확한값
from орындау_пәрмен import жоба_түбір


def 창크기시험(너비, 높이, өлшем_жол):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); порт_нөмірі = 임시.getsockname()[1]
    өлшемді_өзгерту_Мәтін = '{}x{}'.format(너비, 높이)
    Процесс_мән = subprocess.Popen(['python3', str(жоба_түбір/'Құралдар/орындау_пәрмен.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(порт_нөмірі), '--resolution', өлшемді_өзгерту_Мәтін], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    селектор_a916db4e = selectors.DefaultSelector(); селектор_a916db4e.register(Процесс_мән.stdout, selectors.EVENT_READ)
    журнал_жол = bytearray(); 원격 = None; аудару_мән = None; меңзер_Жасырын=[False]

    def 기다리기(көрсету_мән, Орындау_2=0):
        ең_соңғы_мерзім_мән = time.monotonic() + 60
        while көрсету_мән not in журнал_жол[Орындау_2:]:
            if time.monotonic() > ең_соңғы_мерзім_мән or Процесс_мән.poll() is not None or b'HALTED' in журнал_жол or b'PANIC:' in журнал_жол:
                raise AssertionError(журнал_жол[Орындау_2:].decode('utf-8', 'replace'))
            for Оқиға, _ in селектор_a916db4e.select(.1):
                деректер = Оқиға.fileobj.read(65536)
                if деректер: журнал_жол.extend(деректер)
        return журнал_жол[Орындау_2:].decode('utf-8', 'replace')

    def басу_түйме(символ, 눌림=True): 원격.sendall(struct.pack('>BBHI', 4, int(눌림), 0, символ))

    def SMS_жіберу(Мәтін):
        Орындау_2 = len(журнал_жол)
        for таңба_мән in Мәтін:
            символ = 0xff0d if таңба_мән == '\n' else ord(таңба_мән) if ord(таңба_мән) < 256 else 0x1000000 | ord(таңба_мән)
            басу_түйме(символ); басу_түйме(символ, False)
        return Орындау_2

    def қоршам(Мәтін): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_жіберу(Мәтін+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Тік_лауазым, 눌림): 원격.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Тік_лауазым))

    def басу_мән(가로, Тік_лауазым): 가리키기(가로, Тік_лауазым, 1); 가리키기(가로, Тік_лауазым, 0)

    def нүктелік_кескін_сурет():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 нақты_деректер 너비를 쓴다.
        원격.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        сызба_мән = Image.new('RGB', (너비, 높이)); аймақ_мән = 0
        while True:
            종류 = 정확한값(원격, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ұзындық_мән = struct.unpack('>I', 정확한값(원격, 7)[3:])[0]; 정확한값(원격, ұзындық_мән); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(원격, 3)[1:])[0]
            for _ in range(개수):
                가로, Тік_лауазым, 폭, ұзындық_мән, кодтау_мән = struct.unpack('>HHHHi', 정확한값(원격, 12))
                if кодтау_мән == -239:
                    assert 폭==0 and ұзындық_мән==0, 'remote cursor must be hidden'
                    меңзер_Жасырын[0]=True
                    continue
                assert кодтау_мән == 0 and 가로+폭 <= 너비 and Тік_лауазым+ұзындық_мән <= 높이
                сызба_мән.paste(Image.frombytes('RGB', (폭, ұзындық_мән), 정확한값(원격, 폭*ұзындық_мән*4), 'raw', 'BGRX'), (가로, Тік_лауазым))
                аймақ_мән += 폭*ұзындық_мән
            if аймақ_мән:
                assert аймақ_мән == 너비*높이, аймақ_мән
                return сызба_мән

    def чек_нүкте(координата_мән, 색):
        ең_соңғы_мерзім_мән = time.monotonic()+10
        while True:
            сызба_мән = нүктелік_кескін_сурет()
            if сызба_мән.getpixel(координата_мән) == 색: return сызба_мән
            if time.monotonic() > ең_соңғы_мерзім_мән: raise AssertionError((координата_мән, сызба_мән.getpixel(координата_мән), 색))

    def Жүктеп_салу_Файлдар(Аты, деректер): аудару_мән.storbinary('STOR '+Аты, io.BytesIO(деректер))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+өлшемді_өзгерту_Мәтін+' RGB32').encode() in журнал_жол
        print('BOOT:', өлшемді_өзгерту_Мәтін, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', журнал_жол).group(1))
        원격 = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(원격, 12) == b'RFB 003.008\n'; 원격.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(원격, 정확한값(원격, 1)[0]); 원격.sendall(b'\x01')
        assert 정확한값(원격, 4) == b'\0'*4; 원격.sendall(b'\x01')
        бастапқы_күй = 정확한값(원격, 24); assert struct.unpack('>HH', бастапқы_күй[:4]) == (너비, 높이)
        정확한값(원격, struct.unpack('>I', бастапқы_күй[20:])[0])
        원격.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        원격.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        чек_нүкте((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Оқиға,_ in селектор_a916db4e.select(.02):
                    деректер=Оқиға.fileobj.read(65536)
                    if деректер:журнал_жол.extend(деректер)
        Терезе=[12,48,568,360]
        def тексеру_өлшемді_өзгерту():
            баған_мән,жол_мән_fc48bc81=(Терезе[2]-24)//8,(Терезе[3]-56)//16
            Мәтін=қоршам('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(баған_мән,жол_мән_fc48bc81) in Мәтін,Мәтін
            # нақты_деректер Терезе 테두리: 단지 Өлшемі сұрау_мән 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            чек_нүкте((Терезе[0],Терезе[1]),(32,80,144))
            сызба_мән=чек_нүкте((Терезе[0]+Терезе[2]-1,Терезе[1]+Терезе[3]-1),(39,49,64))
            return сызба_мән
        def 모서리(방향):
            return (Терезе[0]+(3 if 방향 in (1,3) else Терезе[2]-4),Терезе[1]+(3 if 방향<=2 else Терезе[3]-4))
        def өлшемді_өзгерту_апару(방향,차이,батырма=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            чек_нүкте(흰점,(255,255,255))
            가리키기(가,세,батырма)
            끝가=max(0,min(너비-1,가+차이[0]));тоқтату_Тік=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,тоқтату_Тік,батырма);가리키기(끝가,тоқтату_Тік,0);숨고르기()
            if батырма==1:
                왼,위,폭,ұзындық_мән=Терезе;오른,아래=왼+폭,위+ұзындық_мән
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+тоқтату_Тік-세))
                else:아래=max(위+216,min(높이,아래+тоқтату_Тік-세))
                Терезе[:]=[왼,위,오른-왼,아래-위]
        тексеру_өлшемді_өзгерту();assert меңзер_Жасырын[0]
        өлшемді_өзгерту_апару(4,(-100,-60),4);тексеру_өлшемді_өзгерту() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            өлшемді_өзгерту_апару(방향,차이);тексеру_өлшемді_өзгерту()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_жіберу("echo '"+긴글+"'");숨고르기()
        өлшемді_өзгерту_апару(4,(-1000,-1000));assert Терезе[2:]==[360,216]
        өлшемді_өзгерту_апару(4,(너비,높이))
        Орындау_2=SMS_жіберу('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Орындау_2);тексеру_өлшемді_өзгерту()
        # vi가 өңдеу_мән 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        қоршам('ftpd start')
        аудару_мән=ftplib.FTP();аудару_мән.encoding='utf-8';аудару_мән.connect('127.0.0.1',порт_нөмірі,timeout=20);аудару_мән.login()
        기다리기(b'NORMAL',SMS_жіберу('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_жіберу('i미저장 한글 деректер\n'));숨고르기()
        өлшемді_өзгерту_апару(4,(-너비,-높이))
        # ANSI жол_мән_fc48bc81 이동에 새 жол_мән_fc48bc81 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Терезе[3]-56)//16)).encode() in журнал_жол[-4096:]
        SMS_жіберу('작은 창에서도 이어 Жазу\n');숨고르기()
        өлшемді_өзгерту_апару(4,(너비,높이))
        SMS_жіберу('큰 창에서도 이어 Жазу\n');숨고르기()
        басу_түйме(0xff1b);басу_түйме(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_жіберу(':wq\n'))
        мазмұн_мән=bytearray();аудару_мән.retrbinary('RETR 크기자료.txt',мазмұн_мән.extend)
        assert мазмұн_мән=='미저장 한글 деректер\n작은 창에서도 이어 Жазу\n큰 창에서도 이어 Жазу\n'.encode(),мазмұн_мән
        тексеру_өлшемді_өзгерту().save(str(өлшем_жол/(өлшемді_өзгерту_Мәтін+'-large.png')))
        # 두 번째 창은 әдепкі_мән Өлшемі, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Орындау_2=len(журнал_жол);басу_мән(70,16);기다리기(b'TERMINAL FOCUS 2',Орындау_2)
        assert 'TERMINAL SIZE 68x19' in қоршам('terminal size')
        Орындау_2=len(журнал_жол);басу_мән(180,16);기다리기(b'TERMINAL FOCUS 1',Орындау_2);тексеру_өлшемді_өзгерту()
        өлшемді_өзгерту_апару(4,(-너비,-높이));тексеру_өлшемді_өзгерту().save(str(өлшем_жол/(өлшемді_өзгерту_Мәтін+'-small.png')))
        # Өлшемі өзгерту_мән АРТҚА_мән X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Орындау_2=len(журнал_жол);басу_мән(Терезе[0]+Терезе[2]-20,Терезе[1]+15);기다리기(b'TERMINAL FOCUS 2',Орындау_2)
        assert 'RESIZE CLOSED' in қоршам('echo RESIZE CLOSED')
        print('PASS:',өлшемді_өзгерту_Мәтін,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if аудару_мән:аудару_мән.close()
        if 원격:원격.close()
        if Процесс_мән.poll() is None:
            Процесс_мән.terminate()
            try:Процесс_мән.wait(timeout=8)
            except subprocess.TimeoutExpired:Процесс_мән.kill();Процесс_мән.wait()
        селектор_a916db4e.close();Процесс_мән.stdout.close();(өлшем_жол/(өлшемді_өзгерту_Мәтін+'.log')).write_bytes(журнал_жол)


def Орындау_2():
    өлшем_жол=жоба_түбір/'build/verification/resize';өлшем_жол.mkdir(parents=True,exist_ok=True)
    журнал_жол={'passed':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,өлшем_жол);журнал_жол['resolutions'].append([너비,높이])
        журнал_жол.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(өлшем_жол/'report.json').write_text(json.dumps(журнал_жол,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Орындау_2()
