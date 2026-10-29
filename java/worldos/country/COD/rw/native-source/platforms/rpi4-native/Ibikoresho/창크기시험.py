#!/usr/bin/env python3
"""nyakuri_amakurushingiro QEMU/VNC에서 터미널 모서리 kunyereza_agaciro·mwerekana·동적 inyuguti_agaciro umwanya_icyinjizwa·guhindura_agaciro Ibirimo_agaciro 보존를 검사한다."""
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
from biro_igaragaza import 정확한값
from gukora_ibwiriza import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ingano_SMS = '{}x{}'.format(너비, 높이)
    Inzira_agaciro = subprocess.Popen(['python3', str(기준/'Ibikoresho/gukora_ibwiriza.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ingano_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    muhitamo_a916db4e = selectors.DefaultSelector(); muhitamo_a916db4e.register(Inzira_agaciro.stdout, selectors.EVENT_READ)
    kubika_umurongo = bytearray(); kure_agaciro = None; iyimura_agaciro = None; mwerekana_cyahishwe=[False]

    def 기다리기(kugaragaza_agaciro, ihuriro=0):
        마감 = time.monotonic() + 60
        while kugaragaza_agaciro not in kubika_umurongo[ihuriro:]:
            if time.monotonic() > 마감 or Inzira_agaciro.poll() is not None or b'HALTED' in kubika_umurongo or b'PANIC:' in kubika_umurongo:
                raise AssertionError(kubika_umurongo[ihuriro:].decode('utf-8', 'replace'))
            for icyabaye, _ in muhitamo_a916db4e.select(.1):
                amakurushingiro = icyabaye.fileobj.read(65536)
                if amakurushingiro: kubika_umurongo.extend(amakurushingiro)
        return kubika_umurongo[ihuriro:].decode('utf-8', 'replace')

    def gukanda_buto(ikimenyetso, 눌림=True): kure_agaciro.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ikimenyetso))

    def ohereza_SMS(Umwandiko):
        ihuriro = len(kubika_umurongo)
        for inyuguti_agaciro in Umwandiko:
            ikimenyetso = 0xff0d if inyuguti_agaciro == '\n' else ord(inyuguti_agaciro) if ord(inyuguti_agaciro) < 256 else 0x1000000 | ord(inyuguti_agaciro)
            gukanda_buto(ikimenyetso); gukanda_buto(ikimenyetso, False)
        return ihuriro

    def insomamabwiriza(Umwandiko): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', ohereza_SMS(Umwandiko+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kure_agaciro.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def gukanda_agaciro(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitimapu_ishusho():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 nyakuri_amakurushingiro 너비를 쓴다.
        kure_agaciro.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        igishushanyo_agaciro = Image.new('RGB', (너비, 높이)); akanya_agaciro = 0
        while True:
            종류 = 정확한값(kure_agaciro, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                uburebure_agaciro = struct.unpack('>I', 정확한값(kure_agaciro, 7)[3:])[0]; 정확한값(kure_agaciro, uburebure_agaciro); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kure_agaciro, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, uburebure_agaciro, gusobeka_agaciro = struct.unpack('>HHHHi', 정확한값(kure_agaciro, 12))
                if gusobeka_agaciro == -239:
                    assert 폭==0 and uburebure_agaciro==0, 'remote cursor must be hidden'
                    mwerekana_cyahishwe[0]=True
                    continue
                assert gusobeka_agaciro == 0 and 가로+폭 <= 너비 and 세로+uburebure_agaciro <= 높이
                igishushanyo_agaciro.paste(Image.frombytes('RGB', (폭, uburebure_agaciro), 정확한값(kure_agaciro, 폭*uburebure_agaciro*4), 'raw', 'BGRX'), (가로, 세로))
                akanya_agaciro += 폭*uburebure_agaciro
            if akanya_agaciro:
                assert akanya_agaciro == 너비*높이, akanya_agaciro
                return igishushanyo_agaciro

    def sheki_pel(guhuza_agaciro, 색):
        마감 = time.monotonic()+10
        while True:
            igishushanyo_agaciro = bitimapu_ishusho()
            if igishushanyo_agaciro.getpixel(guhuza_agaciro) == 색: return igishushanyo_agaciro
            if time.monotonic() > 마감: raise AssertionError((guhuza_agaciro, igishushanyo_agaciro.getpixel(guhuza_agaciro), 색))

    def gukurura_Dosiye(Izina, amakurushingiro): iyimura_agaciro.storbinary('STOR '+Izina, io.BytesIO(amakurushingiro))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ingano_SMS+' RGB32').encode() in kubika_umurongo
        print('BOOT:', ingano_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', kubika_umurongo).group(1))
        kure_agaciro = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kure_agaciro, 12) == b'RFB 003.008\n'; kure_agaciro.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kure_agaciro, 정확한값(kure_agaciro, 1)[0]); kure_agaciro.sendall(b'\x01')
        assert 정확한값(kure_agaciro, 4) == b'\0'*4; kure_agaciro.sendall(b'\x01')
        초기 = 정확한값(kure_agaciro, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kure_agaciro, struct.unpack('>I', 초기[20:])[0])
        kure_agaciro.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kure_agaciro.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        sheki_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for icyabaye,_ in muhitamo_a916db4e.select(.02):
                    amakurushingiro=icyabaye.fileobj.read(65536)
                    if amakurushingiro:kubika_umurongo.extend(amakurushingiro)
        idirishya=[12,48,568,360]
        def gusuzuma_ingano():
            inkingi_agaciro,umurongo_agaciro_fc48bc81=(idirishya[2]-24)//8,(idirishya[3]-56)//16
            Umwandiko=insomamabwiriza('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(inkingi_agaciro,umurongo_agaciro_fc48bc81) in Umwandiko,Umwandiko
            # nyakuri_amakurushingiro idirishya 테두리: 단지 Ingano isaba_agaciro 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            sheki_pel((idirishya[0],idirishya[1]),(32,80,144))
            igishushanyo_agaciro=sheki_pel((idirishya[0]+idirishya[2]-1,idirishya[1]+idirishya[3]-1),(39,49,64))
            return igishushanyo_agaciro
        def 모서리(방향):
            return (idirishya[0]+(3 if 방향 in (1,3) else idirishya[2]-4),idirishya[1]+(3 if 방향<=2 else idirishya[3]-4))
        def guhindura_ingano_kunyereza(방향,차이,buto=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            sheki_pel(흰점,(255,255,255))
            가리키기(가,세,buto)
            끝가=max(0,min(너비-1,가+차이[0]));kurangiza_Impagarike=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,kurangiza_Impagarike,buto);가리키기(끝가,kurangiza_Impagarike,0);숨고르기()
            if buto==1:
                왼,위,폭,uburebure_agaciro=idirishya;오른,아래=왼+폭,위+uburebure_agaciro
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+kurangiza_Impagarike-세))
                else:아래=max(위+216,min(높이,아래+kurangiza_Impagarike-세))
                idirishya[:]=[왼,위,오른-왼,아래-위]
        gusuzuma_ingano();assert mwerekana_cyahishwe[0]
        guhindura_ingano_kunyereza(4,(-100,-60),4);gusuzuma_ingano() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            guhindura_ingano_kunyereza(방향,차이);gusuzuma_ingano()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        ohereza_SMS("echo '"+긴글+"'");숨고르기()
        guhindura_ingano_kunyereza(4,(-1000,-1000));assert idirishya[2:]==[360,216]
        guhindura_ingano_kunyereza(4,(너비,높이))
        ihuriro=ohereza_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ihuriro);gusuzuma_ingano()
        # vi가 guhindura_agaciro 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        insomamabwiriza('ftpd start')
        iyimura_agaciro=ftplib.FTP();iyimura_agaciro.encoding='utf-8';iyimura_agaciro.connect('127.0.0.1',접속번호,timeout=20);iyimura_agaciro.login()
        기다리기(b'NORMAL',ohereza_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',ohereza_SMS('i미저장 한글 amakurushingiro\n'));숨고르기()
        guhindura_ingano_kunyereza(4,(-너비,-높이))
        # ANSI umurongo_agaciro_fc48bc81 이동에 새 umurongo_agaciro_fc48bc81 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((idirishya[3]-56)//16)).encode() in kubika_umurongo[-4096:]
        ohereza_SMS('작은 창에서도 이어 kwandika\n');숨고르기()
        guhindura_ingano_kunyereza(4,(너비,높이))
        ohereza_SMS('큰 창에서도 이어 kwandika\n');숨고르기()
        gukanda_buto(0xff1b);gukanda_buto(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',ohereza_SMS(':wq\n'))
        Ibirimo_agaciro=bytearray();iyimura_agaciro.retrbinary('RETR 크기자료.txt',Ibirimo_agaciro.extend)
        assert Ibirimo_agaciro=='미저장 한글 amakurushingiro\n작은 창에서도 이어 kwandika\n큰 창에서도 이어 kwandika\n'.encode(),Ibirimo_agaciro
        gusuzuma_ingano().save(str(결과경로/(ingano_SMS+'-large.png')))
        # 두 번째 창은 agaciro_gasanzweho Ingano, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ihuriro=len(kubika_umurongo);gukanda_agaciro(70,16);기다리기(b'TERMINAL FOCUS 2',ihuriro)
        assert 'TERMINAL SIZE 68x19' in insomamabwiriza('terminal size')
        ihuriro=len(kubika_umurongo);gukanda_agaciro(180,16);기다리기(b'TERMINAL FOCUS 1',ihuriro);gusuzuma_ingano()
        guhindura_ingano_kunyereza(4,(-너비,-높이));gusuzuma_ingano().save(str(결과경로/(ingano_SMS+'-small.png')))
        # Ingano guhindura_agaciro_16f64fe4 Ikibanza_agaciro X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ihuriro=len(kubika_umurongo);gukanda_agaciro(idirishya[0]+idirishya[2]-20,idirishya[1]+15);기다리기(b'TERMINAL FOCUS 2',ihuriro)
        assert 'RESIZE CLOSED' in insomamabwiriza('echo RESIZE CLOSED')
        print('PASS:',ingano_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if iyimura_agaciro:iyimura_agaciro.close()
        if kure_agaciro:kure_agaciro.close()
        if Inzira_agaciro.poll() is None:
            Inzira_agaciro.terminate()
            try:Inzira_agaciro.wait(timeout=8)
            except subprocess.TimeoutExpired:Inzira_agaciro.kill();Inzira_agaciro.wait()
        muhitamo_a916db4e.close();Inzira_agaciro.stdout.close();(결과경로/(ingano_SMS+'.log')).write_bytes(kubika_umurongo)


def ihuriro():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    kubika_umurongo={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);kubika_umurongo['resolutions'].append([너비,높이])
        kubika_umurongo.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(kubika_umurongo,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ihuriro()
