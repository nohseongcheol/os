#!/usr/bin/env python3
"""halisi_data QEMU/VNC에서 터미널 모서리 kokota_thamani·kielekezi·동적 kibambo_thamani Sloti_ingizo·hariri_thamani maudhui_thamani 보존를 검사한다."""
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
from Eneo_kazi_Onesha import 정확한값
from tekeleza_amri import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); namba_ya_kituo = 임시.getsockname()[1]
    panga_ukubwa_SMS = '{}x{}'.format(너비, 높이)
    Mchakato_thamani = subprocess.Popen(['python3', str(기준/'Zana/tekeleza_amri.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(namba_ya_kituo), '--resolution', panga_ukubwa_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    kiteuzi_a916db4e = selectors.DefaultSelector(); kiteuzi_a916db4e.register(Mchakato_thamani.stdout, selectors.EVENT_READ)
    batli_REKODI = bytearray(); kwa_mbali_thamani = None; hamisha_thamani_630ba093 = None; kielekezi_fiche=[False]

    def 기다리기(onyesha_thamani, endesha=0):
        마감 = time.monotonic() + 60
        while onyesha_thamani not in batli_REKODI[endesha:]:
            if time.monotonic() > 마감 or Mchakato_thamani.poll() is not None or b'HALTED' in batli_REKODI or b'PANIC:' in batli_REKODI:
                raise AssertionError(batli_REKODI[endesha:].decode('utf-8', 'replace'))
            for tukio, _ in kiteuzi_a916db4e.select(.1):
                data = tukio.fileobj.read(65536)
                if data: batli_REKODI.extend(data)
        return batli_REKODI[endesha:].decode('utf-8', 'replace')

    def bofya_kitufe(ishara, 눌림=True): kwa_mbali_thamani.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ishara))

    def tuma_SMS(SMS):
        endesha = len(batli_REKODI)
        for kibambo_thamani in SMS:
            ishara = 0xff0d if kibambo_thamani == '\n' else ord(kibambo_thamani) if ord(kibambo_thamani) < 256 else 0x1000000 | ord(kibambo_thamani)
            bofya_kitufe(ishara); bofya_kitufe(ishara, False)
        return endesha

    def sheli(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', tuma_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kwa_mbali_thamani.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def bofya_thamani(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def taswidoti_picha():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 halisi_data 너비를 쓴다.
        kwa_mbali_thamani.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        mchoro_thamani = Image.new('RGB', (너비, 높이)); eneo_thamani = 0
        while True:
            종류 = 정확한값(kwa_mbali_thamani, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                urefu_thamani = struct.unpack('>I', 정확한값(kwa_mbali_thamani, 7)[3:])[0]; 정확한값(kwa_mbali_thamani, urefu_thamani); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kwa_mbali_thamani, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, urefu_thamani, usimbaji_thamani = struct.unpack('>HHHHi', 정확한값(kwa_mbali_thamani, 12))
                if usimbaji_thamani == -239:
                    assert 폭==0 and urefu_thamani==0, 'remote cursor must be hidden'
                    kielekezi_fiche[0]=True
                    continue
                assert usimbaji_thamani == 0 and 가로+폭 <= 너비 and 세로+urefu_thamani <= 높이
                mchoro_thamani.paste(Image.frombytes('RGB', (폭, urefu_thamani), 정확한값(kwa_mbali_thamani, 폭*urefu_thamani*4), 'raw', 'BGRX'), (가로, 세로))
                eneo_thamani += 폭*urefu_thamani
            if eneo_thamani:
                assert eneo_thamani == 너비*높이, eneo_thamani
                return mchoro_thamani

    def hundi_elepi(kiratibu_thamani, 색):
        마감 = time.monotonic()+10
        while True:
            mchoro_thamani = taswidoti_picha()
            if mchoro_thamani.getpixel(kiratibu_thamani) == 색: return mchoro_thamani
            if time.monotonic() > 마감: raise AssertionError((kiratibu_thamani, mchoro_thamani.getpixel(kiratibu_thamani), 색))

    def pakia_Faili(Jina, data): hamisha_thamani_630ba093.storbinary('STOR '+Jina, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+panga_ukubwa_SMS+' RGB32').encode() in batli_REKODI
        print('BOOT:', panga_ukubwa_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', batli_REKODI).group(1))
        kwa_mbali_thamani = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kwa_mbali_thamani, 12) == b'RFB 003.008\n'; kwa_mbali_thamani.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kwa_mbali_thamani, 정확한값(kwa_mbali_thamani, 1)[0]); kwa_mbali_thamani.sendall(b'\x01')
        assert 정확한값(kwa_mbali_thamani, 4) == b'\0'*4; kwa_mbali_thamani.sendall(b'\x01')
        초기 = 정확한값(kwa_mbali_thamani, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kwa_mbali_thamani, struct.unpack('>I', 초기[20:])[0])
        kwa_mbali_thamani.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kwa_mbali_thamani.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        hundi_elepi((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for tukio,_ in kiteuzi_a916db4e.select(.02):
                    data=tukio.fileobj.read(65536)
                    if data:batli_REKODI.extend(data)
        dirisha=[12,48,568,360]
        def thibitisha_panga_ukubwa():
            safuwima_thamani,kumbukumbu_thamani=(dirisha[2]-24)//8,(dirisha[3]-56)//16
            SMS=sheli('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(safuwima_thamani,kumbukumbu_thamani) in SMS,SMS
            # halisi_data dirisha 테두리: 단지 panga_ukubwa uliza_thamani 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            hundi_elepi((dirisha[0],dirisha[1]),(32,80,144))
            mchoro_thamani=hundi_elepi((dirisha[0]+dirisha[2]-1,dirisha[1]+dirisha[3]-1),(39,49,64))
            return mchoro_thamani
        def 모서리(방향):
            return (dirisha[0]+(3 if 방향 in (1,3) else dirisha[2]-4),dirisha[1]+(3 if 방향<=2 else dirisha[3]-4))
        def badilisha_ukubwa_kokota(방향,차이,kitufe=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            hundi_elepi(흰점,(255,255,255))
            가리키기(가,세,kitufe)
            끝가=max(0,min(너비-1,가+차이[0]));tamatia_Wima=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,tamatia_Wima,kitufe);가리키기(끝가,tamatia_Wima,0);숨고르기()
            if kitufe==1:
                왼,위,폭,urefu_thamani=dirisha;오른,아래=왼+폭,위+urefu_thamani
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+tamatia_Wima-세))
                else:아래=max(위+216,min(높이,아래+tamatia_Wima-세))
                dirisha[:]=[왼,위,오른-왼,아래-위]
        thibitisha_panga_ukubwa();assert kielekezi_fiche[0]
        badilisha_ukubwa_kokota(4,(-100,-60),4);thibitisha_panga_ukubwa() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            badilisha_ukubwa_kokota(방향,차이);thibitisha_panga_ukubwa()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        tuma_SMS("echo '"+긴글+"'");숨고르기()
        badilisha_ukubwa_kokota(4,(-1000,-1000));assert dirisha[2:]==[360,216]
        badilisha_ukubwa_kokota(4,(너비,높이))
        endesha=tuma_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),endesha);thibitisha_panga_ukubwa()
        # vi가 hariri_thamani 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        sheli('ftpd start')
        hamisha_thamani_630ba093=ftplib.FTP();hamisha_thamani_630ba093.encoding='utf-8';hamisha_thamani_630ba093.connect('127.0.0.1',namba_ya_kituo,timeout=20);hamisha_thamani_630ba093.login()
        기다리기(b'NORMAL',tuma_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',tuma_SMS('i미저장 한글 data\n'));숨고르기()
        badilisha_ukubwa_kokota(4,(-너비,-높이))
        # ANSI kumbukumbu_thamani 이동에 새 kumbukumbu_thamani 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((dirisha[3]-56)//16)).encode() in batli_REKODI[-4096:]
        tuma_SMS('작은 창에서도 이어 andika\n');숨고르기()
        badilisha_ukubwa_kokota(4,(너비,높이))
        tuma_SMS('큰 창에서도 이어 andika\n');숨고르기()
        bofya_kitufe(0xff1b);bofya_kitufe(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',tuma_SMS(':wq\n'))
        maudhui_thamani=bytearray();hamisha_thamani_630ba093.retrbinary('RETR 크기자료.txt',maudhui_thamani.extend)
        assert maudhui_thamani=='미저장 한글 data\n작은 창에서도 이어 andika\n큰 창에서도 이어 andika\n'.encode(),maudhui_thamani
        thibitisha_panga_ukubwa().save(str(결과경로/(panga_ukubwa_SMS+'-large.png')))
        # 두 번째 창은 hali_ya_chaguo_msingi panga_ukubwa, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        endesha=len(batli_REKODI);bofya_thamani(70,16);기다리기(b'TERMINAL FOCUS 2',endesha)
        assert 'TERMINAL SIZE 68x19' in sheli('terminal size')
        endesha=len(batli_REKODI);bofya_thamani(180,16);기다리기(b'TERMINAL FOCUS 1',endesha);thibitisha_panga_ukubwa()
        badilisha_ukubwa_kokota(4,(-너비,-높이));thibitisha_panga_ukubwa().save(str(결과경로/(panga_ukubwa_SMS+'-small.png')))
        # panga_ukubwa badilisha_thamani_16f64fe4 Nyuma_thamani X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        endesha=len(batli_REKODI);bofya_thamani(dirisha[0]+dirisha[2]-20,dirisha[1]+15);기다리기(b'TERMINAL FOCUS 2',endesha)
        assert 'RESIZE CLOSED' in sheli('echo RESIZE CLOSED')
        print('PASS:',panga_ukubwa_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if hamisha_thamani_630ba093:hamisha_thamani_630ba093.close()
        if kwa_mbali_thamani:kwa_mbali_thamani.close()
        if Mchakato_thamani.poll() is None:
            Mchakato_thamani.terminate()
            try:Mchakato_thamani.wait(timeout=8)
            except subprocess.TimeoutExpired:Mchakato_thamani.kill();Mchakato_thamani.wait()
        kiteuzi_a916db4e.close();Mchakato_thamani.stdout.close();(결과경로/(panga_ukubwa_SMS+'.log')).write_bytes(batli_REKODI)


def endesha():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    batli_REKODI={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);batli_REKODI['resolutions'].append([너비,높이])
        batli_REKODI.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(batli_REKODI,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':endesha()
