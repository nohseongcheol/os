#!/usr/bin/env python3
"""faktisk_data QEMU/VNC에서 Terminal 모서리 trække_VÆRDI·markør·동적 tegn_VÆRDI udvidelsesstik_post·Rediger_VÆRDI Indhold_VÆRDI 보존를 검사한다."""
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
from desktop_Visning import EKSAKT_VÆRDI
from Udfør_kommando import To_do_rod


def 창크기시험(너비, 높이, KR_sti):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portnummer = 임시.getsockname()[1]
    tilpasse_størrelse_sms = '{}x{}'.format(너비, 높이)
    Proces_VÆRDI = subprocess.Popen(['python3', str(To_do_rod/'Værktøjer/Udfør_kommando.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portnummer), '--resolution', tilpasse_størrelse_sms], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selektor_a916db4e = selectors.DefaultSelector(); selektor_a916db4e.register(Proces_VÆRDI.stdout, selectors.EVENT_READ)
    LOG_post = bytearray(); fjern_VÆRDI = None; overføre_VÆRDI = None; markør_Skjult=[False]

    def 기다리기(vise_VÆRDI, Kør_2=0):
        deadline_VÆRDI = time.monotonic() + 60
        while vise_VÆRDI not in LOG_post[Kør_2:]:
            if time.monotonic() > deadline_VÆRDI or Proces_VÆRDI.poll() is not None or b'HALTED' in LOG_post or b'PANIC:' in LOG_post:
                raise AssertionError(LOG_post[Kør_2:].decode('utf-8', 'replace'))
            for hændelse, _ in selektor_a916db4e.select(.1):
                data = hændelse.fileobj.read(65536)
                if data: LOG_post.extend(data)
        return LOG_post[Kør_2:].decode('utf-8', 'replace')

    def klik_knap(symbol, 눌림=True): fjern_VÆRDI.sendall(struct.pack('>BBHI', 4, int(눌림), 0, symbol))

    def send_sms(Tekst):
        Kør_2 = len(LOG_post)
        for tegn_VÆRDI in Tekst:
            symbol = 0xff0d if tegn_VÆRDI == '\n' else ord(tegn_VÆRDI) if ord(tegn_VÆRDI) < 256 else 0x1000000 | ord(tegn_VÆRDI)
            klik_knap(symbol); klik_knap(symbol, False)
        return Kør_2

    def Shell(Tekst): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', send_sms(Tekst+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Lodret_placere, 눌림): fjern_VÆRDI.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Lodret_placere))

    def klik_VÆRDI(가로, Lodret_placere): 가리키기(가로, Lodret_placere, 1); 가리키기(가로, Lodret_placere, 0)

    def bitmap_Image():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktisk_data 너비를 쓴다.
        fjern_VÆRDI.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tegning_VÆRDI = Image.new('RGB', (너비, 높이)); område_VÆRDI_9285603e = 0
        while True:
            종류 = EKSAKT_VÆRDI(fjern_VÆRDI, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                varighed_VÆRDI = struct.unpack('>I', EKSAKT_VÆRDI(fjern_VÆRDI, 7)[3:])[0]; EKSAKT_VÆRDI(fjern_VÆRDI, varighed_VÆRDI); continue
            assert 종류 == 0, 종류
            vare_TÆL = struct.unpack('>H', EKSAKT_VÆRDI(fjern_VÆRDI, 3)[1:])[0]
            for _ in range(vare_TÆL):
                가로, Lodret_placere, 폭, varighed_VÆRDI, kodning_VÆRDI = struct.unpack('>HHHHi', EKSAKT_VÆRDI(fjern_VÆRDI, 12))
                if kodning_VÆRDI == -239:
                    assert 폭==0 and varighed_VÆRDI==0, 'remote cursor must be hidden'
                    markør_Skjult[0]=True
                    continue
                assert kodning_VÆRDI == 0 and 가로+폭 <= 너비 and Lodret_placere+varighed_VÆRDI <= 높이
                tegning_VÆRDI.paste(Image.frombytes('RGB', (폭, varighed_VÆRDI), EKSAKT_VÆRDI(fjern_VÆRDI, 폭*varighed_VÆRDI*4), 'raw', 'BGRX'), (가로, Lodret_placere))
                område_VÆRDI_9285603e += 폭*varighed_VÆRDI
            if område_VÆRDI_9285603e:
                assert område_VÆRDI_9285603e == 너비*높이, område_VÆRDI_9285603e
                return tegning_VÆRDI

    def check_pixel(koordinat_VÆRDI, 색):
        deadline_VÆRDI = time.monotonic()+10
        while True:
            tegning_VÆRDI = bitmap_Image()
            if tegning_VÆRDI.getpixel(koordinat_VÆRDI) == 색: return tegning_VÆRDI
            if time.monotonic() > deadline_VÆRDI: raise AssertionError((koordinat_VÆRDI, tegning_VÆRDI.getpixel(koordinat_VÆRDI), 색))

    def Upload_Filer(Navn, data): overføre_VÆRDI.storbinary('STOR '+Navn, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+tilpasse_størrelse_sms+' RGB32').encode() in LOG_post
        print('BOOT:', tilpasse_størrelse_sms, flush=True)
        fjern_tal = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_post).group(1))
        fjern_VÆRDI = socket.create_connection(('127.0.0.1', fjern_tal), timeout=20)
        assert EKSAKT_VÆRDI(fjern_VÆRDI, 12) == b'RFB 003.008\n'; fjern_VÆRDI.sendall(b'RFB 003.008\n')
        assert 1 in EKSAKT_VÆRDI(fjern_VÆRDI, EKSAKT_VÆRDI(fjern_VÆRDI, 1)[0]); fjern_VÆRDI.sendall(b'\x01')
        assert EKSAKT_VÆRDI(fjern_VÆRDI, 4) == b'\0'*4; fjern_VÆRDI.sendall(b'\x01')
        starttilstand = EKSAKT_VÆRDI(fjern_VÆRDI, 24); assert struct.unpack('>HH', starttilstand[:4]) == (너비, 높이)
        EKSAKT_VÆRDI(fjern_VÆRDI, struct.unpack('>I', starttilstand[20:])[0])
        fjern_VÆRDI.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        fjern_VÆRDI.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        check_pixel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for hændelse,_ in selektor_a916db4e.select(.02):
                    data=hændelse.fileobj.read(65536)
                    if data:LOG_post.extend(data)
        Vindue=[12,48,568,360]
        def bekræfte_tilpasse_størrelse():
            KOLONNE_VÆRDI,post_VÆRDI=(Vindue[2]-24)//8,(Vindue[3]-56)//16
            Tekst=Shell('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(KOLONNE_VÆRDI,post_VÆRDI) in Tekst,Tekst
            # faktisk_data Vindue 테두리: 단지 Størrelse forespørge_VÆRDI 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            check_pixel((Vindue[0],Vindue[1]),(32,80,144))
            tegning_VÆRDI=check_pixel((Vindue[0]+Vindue[2]-1,Vindue[1]+Vindue[3]-1),(39,49,64))
            return tegning_VÆRDI
        def 모서리(방향):
            return (Vindue[0]+(3 if 방향 in (1,3) else Vindue[2]-4),Vindue[1]+(3 if 방향<=2 else Vindue[3]-4))
        def tilpasse_størrelsen_trække(방향,차이,knap=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            check_pixel(흰점,(255,255,255))
            가리키기(가,세,knap)
            끝가=max(0,min(너비-1,가+차이[0]));afslutte_et_opkald_Lodret=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,afslutte_et_opkald_Lodret,knap);가리키기(끝가,afslutte_et_opkald_Lodret,0);숨고르기()
            if knap==1:
                VENSTRE_VÆRDI,위,폭,varighed_VÆRDI=Vindue;HØJRE_VÆRDI,아래=VENSTRE_VÆRDI+폭,위+varighed_VÆRDI
                if 방향 in (1,3):VENSTRE_VÆRDI=max(0,min(HØJRE_VÆRDI-360,VENSTRE_VÆRDI+끝가-가))
                else:HØJRE_VÆRDI=max(VENSTRE_VÆRDI+360,min(너비,HØJRE_VÆRDI+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+afslutte_et_opkald_Lodret-세))
                else:아래=max(위+216,min(높이,아래+afslutte_et_opkald_Lodret-세))
                Vindue[:]=[VENSTRE_VÆRDI,위,HØJRE_VÆRDI-VENSTRE_VÆRDI,아래-위]
        bekræfte_tilpasse_størrelse();assert markør_Skjult[0]
        tilpasse_størrelsen_trække(4,(-100,-60),4);bekræfte_tilpasse_størrelse() # HØJRE 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            tilpasse_størrelsen_trække(방향,차이);bekræfte_tilpasse_størrelse()
        # input_VÆRDI 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        send_sms("echo '"+긴글+"'");숨고르기()
        tilpasse_størrelsen_trække(4,(-1000,-1000));assert Vindue[2:]==[360,216]
        tilpasse_størrelsen_trække(4,(너비,높이))
        Kør_2=send_sms('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Kør_2);bekræfte_tilpasse_størrelse()
        # vi가 Rediger_VÆRDI 중에 skærmbillede 크기를 prøve_igen_VÆRDI 읽고, 저장하지 않은 한글도 유지한다.
        Shell('ftpd start')
        overføre_VÆRDI=ftplib.FTP();overføre_VÆRDI.encoding='utf-8';overføre_VÆRDI.connect('127.0.0.1',portnummer,timeout=20);overføre_VÆRDI.login()
        기다리기(b'NORMAL',send_sms('vi /크기자료.txt\n'))
        기다리기(b'INSERT',send_sms('i미저장 한글 data\n'));숨고르기()
        tilpasse_størrelsen_trække(4,(-너비,-높이))
        # ANSI post_VÆRDI 이동에 새 post_VÆRDI 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Vindue[3]-56)//16)).encode() in LOG_post[-4096:]
        send_sms('작은 창에서도 이어 Skrive\n');숨고르기()
        tilpasse_størrelsen_trække(4,(너비,높이))
        send_sms('큰 창에서도 이어 Skrive\n');숨고르기()
        klik_knap(0xff1b);klik_knap(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',send_sms(':wq\n'))
        Indhold_VÆRDI=bytearray();overføre_VÆRDI.retrbinary('RETR 크기자료.txt',Indhold_VÆRDI.extend)
        assert Indhold_VÆRDI=='미저장 한글 data\n작은 창에서도 이어 Skrive\n큰 창에서도 이어 Skrive\n'.encode(),Indhold_VÆRDI
        bekræfte_tilpasse_størrelse().save(str(KR_sti/(tilpasse_størrelse_sms+'-large.png')))
        # 두 번째 창은 standardværdi Størrelse, prøve_igen_VÆRDI 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Kør_2=len(LOG_post);klik_VÆRDI(70,16);기다리기(b'TERMINAL FOCUS 2',Kør_2)
        assert 'TERMINAL SIZE 68x19' in Shell('terminal size')
        Kør_2=len(LOG_post);klik_VÆRDI(180,16);기다리기(b'TERMINAL FOCUS 1',Kør_2);bekræfte_tilpasse_størrelse()
        tilpasse_størrelsen_trække(4,(-너비,-높이));bekræfte_tilpasse_størrelse().save(str(KR_sti/(tilpasse_størrelse_sms+'-small.png')))
        # Størrelse ændre_VÆRDI BACK_VÆRDI X 닫기도 새로운 HØJRE 가장자리를 사용한다.
        Kør_2=len(LOG_post);klik_VÆRDI(Vindue[0]+Vindue[2]-20,Vindue[1]+15);기다리기(b'TERMINAL FOCUS 2',Kør_2)
        assert 'RESIZE CLOSED' in Shell('echo RESIZE CLOSED')
        print('PASS:',tilpasse_størrelse_sms,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if overføre_VÆRDI:overføre_VÆRDI.close()
        if fjern_VÆRDI:fjern_VÆRDI.close()
        if Proces_VÆRDI.poll() is None:
            Proces_VÆRDI.terminate()
            try:Proces_VÆRDI.wait(timeout=8)
            except subprocess.TimeoutExpired:Proces_VÆRDI.kill();Proces_VÆRDI.wait()
        selektor_a916db4e.close();Proces_VÆRDI.stdout.close();(KR_sti/(tilpasse_størrelse_sms+'.log')).write_bytes(LOG_post)


def Kør_2():
    KR_sti=To_do_rod/'build/verification/resize';KR_sti.mkdir(parents=True,exist_ok=True)
    LOG_post={'passed':False,'kernel_sha256':hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_sti);LOG_post['resolutions'].append([너비,높이])
        LOG_post.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_sti/'report.json').write_text(json.dumps(LOG_post,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Kør_2()
