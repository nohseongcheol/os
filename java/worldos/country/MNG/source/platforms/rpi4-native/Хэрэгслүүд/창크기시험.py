#!/usr/bin/env python3
"""бодит_өгөгдөл QEMU/VNC에서 Терминал 모서리 чирэх_утга·заагч·동적 тэмдэгт_утга зай_оролт·засварлах_утга Агуулга_утга 보존를 검사한다."""
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
from дэлгэц_харах import 정확한값
from Гүйцэтгэх_команд import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    хэмжээ_Бичвэр = '{}x{}'.format(너비, 높이)
    үйл_явц_утга = subprocess.Popen(['python3', str(기준/'Хэрэгслүүд/Гүйцэтгэх_команд.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', хэмжээ_Бичвэр], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    сонгогч_a916db4e = selectors.DefaultSelector(); сонгогч_a916db4e.register(үйл_явц_утга.stdout, selectors.EVENT_READ)
    бичих_мөр_6e8b375a = bytearray(); алсын_утга = None; дамжуулах_утга = None; заагч_нуугдмал=[False]

    def 기다리기(үзүүлэх_утга, Ажиллуулах=0):
        마감 = time.monotonic() + 60
        while үзүүлэх_утга not in бичих_мөр_6e8b375a[Ажиллуулах:]:
            if time.monotonic() > 마감 or үйл_явц_утга.poll() is not None or b'HALTED' in бичих_мөр_6e8b375a or b'PANIC:' in бичих_мөр_6e8b375a:
                raise AssertionError(бичих_мөр_6e8b375a[Ажиллуулах:].decode('utf-8', 'replace'))
            for үйлдэл, _ in сонгогч_a916db4e.select(.1):
                өгөгдөл = үйлдэл.fileobj.read(65536)
                if өгөгдөл: бичих_мөр_6e8b375a.extend(өгөгдөл)
        return бичих_мөр_6e8b375a[Ажиллуулах:].decode('utf-8', 'replace')

    def товших_товч(тэмдэг, 눌림=True): алсын_утга.sendall(struct.pack('>BBHI', 4, int(눌림), 0, тэмдэг))

    def SMS_илгээх(Бичвэр):
        Ажиллуулах = len(бичих_мөр_6e8b375a)
        for тэмдэгт_утга in Бичвэр:
            тэмдэг = 0xff0d if тэмдэгт_утга == '\n' else ord(тэмдэгт_утга) if ord(тэмдэгт_утга) < 256 else 0x1000000 | ord(тэмдэгт_утга)
            товших_товч(тэмдэг); товших_товч(тэмдэг, False)
        return Ажиллуулах

    def бүрхүүл(Бичвэр): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_илгээх(Бичвэр+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): алсын_утга.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def товших_утга(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def цэглэвэр_зураг_зураг():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 бодит_өгөгдөл 너비를 쓴다.
        алсын_утга.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        зураг_утга_c143fe9e = Image.new('RGB', (너비, 높이)); газар_утга = 0
        while True:
            종류 = 정확한값(алсын_утга, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                урт_утга = struct.unpack('>I', 정확한값(алсын_утга, 7)[3:])[0]; 정확한값(алсын_утга, урт_утга); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(алсын_утга, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, урт_утга, кодчлол_утга = struct.unpack('>HHHHi', 정확한값(алсын_утга, 12))
                if кодчлол_утга == -239:
                    assert 폭==0 and урт_утга==0, 'remote cursor must be hidden'
                    заагч_нуугдмал[0]=True
                    continue
                assert кодчлол_утга == 0 and 가로+폭 <= 너비 and 세로+урт_утга <= 높이
                зураг_утга_c143fe9e.paste(Image.frombytes('RGB', (폭, урт_утга), 정확한값(алсын_утга, 폭*урт_утга*4), 'raw', 'BGRX'), (가로, 세로))
                газар_утга += 폭*урт_утга
            if газар_утга:
                assert газар_утга == 너비*높이, газар_утга
                return зураг_утга_c143fe9e

    def чек_нягтрал_186c1328(координат_утга, 색):
        마감 = time.monotonic()+10
        while True:
            зураг_утга_c143fe9e = цэглэвэр_зураг_зураг()
            if зураг_утга_c143fe9e.getpixel(координат_утга) == 색: return зураг_утга_c143fe9e
            if time.monotonic() > 마감: raise AssertionError((координат_утга, зураг_утга_c143fe9e.getpixel(координат_утга), 색))

    def байршуулах_Файлууд(Нэр, өгөгдөл): дамжуулах_утга.storbinary('STOR '+Нэр, io.BytesIO(өгөгдөл))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+хэмжээ_Бичвэр+' RGB32').encode() in бичих_мөр_6e8b375a
        print('BOOT:', хэмжээ_Бичвэр, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', бичих_мөр_6e8b375a).group(1))
        алсын_утга = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(алсын_утга, 12) == b'RFB 003.008\n'; алсын_утга.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(алсын_утга, 정확한값(алсын_утга, 1)[0]); алсын_утга.sendall(b'\x01')
        assert 정확한값(алсын_утга, 4) == b'\0'*4; алсын_утга.sendall(b'\x01')
        초기 = 정확한값(алсын_утга, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(алсын_утга, struct.unpack('>I', 초기[20:])[0])
        алсын_утга.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        алсын_утга.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        чек_нягтрал_186c1328((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for үйлдэл,_ in сонгогч_a916db4e.select(.02):
                    өгөгдөл=үйлдэл.fileobj.read(65536)
                    if өгөгдөл:бичих_мөр_6e8b375a.extend(өгөгдөл)
        цонх=[12,48,568,360]
        def шалгах_хэмжээ():
            багана_утга,мөр_утга=(цонх[2]-24)//8,(цонх[3]-56)//16
            Бичвэр=бүрхүүл('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(багана_утга,мөр_утга) in Бичвэр,Бичвэр
            # бодит_өгөгдөл цонх 테두리: 단지 Хэмжээ асуулга_утга 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            чек_нягтрал_186c1328((цонх[0],цонх[1]),(32,80,144))
            зураг_утга_c143fe9e=чек_нягтрал_186c1328((цонх[0]+цонх[2]-1,цонх[1]+цонх[3]-1),(39,49,64))
            return зураг_утга_c143fe9e
        def 모서리(방향):
            return (цонх[0]+(3 if 방향 in (1,3) else цонх[2]-4),цонх[1]+(3 if 방향<=2 else цонх[3]-4))
        def хэмжээг_өөрчлөх_чирэх(방향,차이,товч=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            чек_нягтрал_186c1328(흰점,(255,255,255))
            가리키기(가,세,товч)
            끝가=max(0,min(너비-1,가+차이[0]));дуусгах_Босоо=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,дуусгах_Босоо,товч);가리키기(끝가,дуусгах_Босоо,0);숨고르기()
            if товч==1:
                왼,위,폭,урт_утга=цонх;오른,아래=왼+폭,위+урт_утга
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+дуусгах_Босоо-세))
                else:아래=max(위+216,min(높이,아래+дуусгах_Босоо-세))
                цонх[:]=[왼,위,오른-왼,아래-위]
        шалгах_хэмжээ();assert заагч_нуугдмал[0]
        хэмжээг_өөрчлөх_чирэх(4,(-100,-60),4);шалгах_хэмжээ() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            хэмжээг_өөрчлөх_чирэх(방향,차이);шалгах_хэмжээ()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_илгээх("echo '"+긴글+"'");숨고르기()
        хэмжээг_өөрчлөх_чирэх(4,(-1000,-1000));assert цонх[2:]==[360,216]
        хэмжээг_өөрчлөх_чирэх(4,(너비,높이))
        Ажиллуулах=SMS_илгээх('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Ажиллуулах);шалгах_хэмжээ()
        # vi가 засварлах_утга 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        бүрхүүл('ftpd start')
        дамжуулах_утга=ftplib.FTP();дамжуулах_утга.encoding='utf-8';дамжуулах_утга.connect('127.0.0.1',접속번호,timeout=20);дамжуулах_утга.login()
        기다리기(b'NORMAL',SMS_илгээх('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_илгээх('i미저장 한글 өгөгдөл\n'));숨고르기()
        хэмжээг_өөрчлөх_чирэх(4,(-너비,-높이))
        # ANSI мөр_утга 이동에 새 мөр_утга 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((цонх[3]-56)//16)).encode() in бичих_мөр_6e8b375a[-4096:]
        SMS_илгээх('작은 창에서도 이어 Бичих\n');숨고르기()
        хэмжээг_өөрчлөх_чирэх(4,(너비,높이))
        SMS_илгээх('큰 창에서도 이어 Бичих\n');숨고르기()
        товших_товч(0xff1b);товших_товч(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_илгээх(':wq\n'))
        Агуулга_утга=bytearray();дамжуулах_утга.retrbinary('RETR 크기자료.txt',Агуулга_утга.extend)
        assert Агуулга_утга=='미저장 한글 өгөгдөл\n작은 창에서도 이어 Бичих\n큰 창에서도 이어 Бичих\n'.encode(),Агуулга_утга
        шалгах_хэмжээ().save(str(결과경로/(хэмжээ_Бичвэр+'-large.png')))
        # 두 번째 창은 өгөгдмөл_утга Хэмжээ, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Ажиллуулах=len(бичих_мөр_6e8b375a);товших_утга(70,16);기다리기(b'TERMINAL FOCUS 2',Ажиллуулах)
        assert 'TERMINAL SIZE 68x19' in бүрхүүл('terminal size')
        Ажиллуулах=len(бичих_мөр_6e8b375a);товших_утга(180,16);기다리기(b'TERMINAL FOCUS 1',Ажиллуулах);шалгах_хэмжээ()
        хэмжээг_өөрчлөх_чирэх(4,(-너비,-높이));шалгах_хэмжээ().save(str(결과경로/(хэмжээ_Бичвэр+'-small.png')))
        # Хэмжээ өөрчлөх_утга Буцах_утга X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Ажиллуулах=len(бичих_мөр_6e8b375a);товших_утга(цонх[0]+цонх[2]-20,цонх[1]+15);기다리기(b'TERMINAL FOCUS 2',Ажиллуулах)
        assert 'RESIZE CLOSED' in бүрхүүл('echo RESIZE CLOSED')
        print('PASS:',хэмжээ_Бичвэр,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if дамжуулах_утга:дамжуулах_утга.close()
        if алсын_утга:алсын_утга.close()
        if үйл_явц_утга.poll() is None:
            үйл_явц_утга.terminate()
            try:үйл_явц_утга.wait(timeout=8)
            except subprocess.TimeoutExpired:үйл_явц_утга.kill();үйл_явц_утга.wait()
        сонгогч_a916db4e.close();үйл_явц_утга.stdout.close();(결과경로/(хэмжээ_Бичвэр+'.log')).write_bytes(бичих_мөр_6e8b375a)


def Ажиллуулах():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    бичих_мөр_6e8b375a={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);бичих_мөр_6e8b375a['resolutions'].append([너비,높이])
        бичих_мөр_6e8b375a.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(бичих_мөр_6e8b375a,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Ажиллуулах()
