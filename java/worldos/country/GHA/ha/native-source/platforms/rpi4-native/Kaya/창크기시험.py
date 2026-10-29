#!/usr/bin/env python3
"""Na_hakika_Tarin_bayani QEMU/VNC에서 터미널 모서리 Jawo_abu_Daraja·manuni·동적 Harafi_Daraja rami_Mashigar_bayanai·gyaran_Daraja kunshiya_Daraja 보존를 검사한다."""
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
from destof_s import 정확한값
from gudanar_Umarni import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); lambar_kafa = 임시.getsockname()[1]
    girma_SMS = '{}x{}'.format(너비, 높이)
    haryar_aikin_na_ura_Daraja = subprocess.Popen(['python3', str(기준/'Kaya/gudanar_Umarni.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(lambar_kafa), '--resolution', girma_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    mai_zabe_a916db4e = selectors.DefaultSelector(); mai_zabe_a916db4e.register(haryar_aikin_na_ura_Daraja.stdout, selectors.EVENT_READ)
    logu_naɗa = bytearray(); na_nesa_Daraja = None; Gusar_da_Daraja = None; manuni_ɓoyayye=[False]

    def 기다리기(Nuna_Daraja, Tafiyar_da=0):
        마감 = time.monotonic() + 60
        while Nuna_Daraja not in logu_naɗa[Tafiyar_da:]:
            if time.monotonic() > 마감 or haryar_aikin_na_ura_Daraja.poll() is not None or b'HALTED' in logu_naɗa or b'PANIC:' in logu_naɗa:
                raise AssertionError(logu_naɗa[Tafiyar_da:].decode('utf-8', 'replace'))
            for Faruwa, _ in mai_zabe_a916db4e.select(.1):
                Tarin_bayani = Faruwa.fileobj.read(65536)
                if Tarin_bayani: logu_naɗa.extend(Tarin_bayani)
        return logu_naɗa[Tafiyar_da:].decode('utf-8', 'replace')

    def Danna_maɓali(alama_ad6f1a96, 눌림=True): na_nesa_Daraja.sendall(struct.pack('>BBHI', 4, int(눌림), 0, alama_ad6f1a96))

    def aika_SMS(SMS):
        Tafiyar_da = len(logu_naɗa)
        for Harafi_Daraja in SMS:
            alama_ad6f1a96 = 0xff0d if Harafi_Daraja == '\n' else ord(Harafi_Daraja) if ord(Harafi_Daraja) < 256 else 0x1000000 | ord(Harafi_Daraja)
            Danna_maɓali(alama_ad6f1a96); Danna_maɓali(alama_ad6f1a96, False)
        return Tafiyar_da

    def Mai_fayyace_umani(SMS): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', aika_SMS(SMS+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): na_nesa_Daraja.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def Danna_Daraja(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def Hoton_digo_digo_Hoto():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 Na_hakika_Tarin_bayani 너비를 쓴다.
        na_nesa_Daraja.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        zane_Daraja = Image.new('RGB', (너비, 높이)); Wuri_Daraja = 0
        while True:
            종류 = 정확한값(na_nesa_Daraja, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                Tsawo_Daraja = struct.unpack('>I', 정확한값(na_nesa_Daraja, 7)[3:])[0]; 정확한값(na_nesa_Daraja, Tsawo_Daraja); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(na_nesa_Daraja, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, Tsawo_Daraja, Juyar_da_bayanai_zuwa_lamba_Daraja = struct.unpack('>HHHHi', 정확한값(na_nesa_Daraja, 12))
                if Juyar_da_bayanai_zuwa_lamba_Daraja == -239:
                    assert 폭==0 and Tsawo_Daraja==0, 'remote cursor must be hidden'
                    manuni_ɓoyayye[0]=True
                    continue
                assert Juyar_da_bayanai_zuwa_lamba_Daraja == 0 and 가로+폭 <= 너비 and 세로+Tsawo_Daraja <= 높이
                zane_Daraja.paste(Image.frombytes('RGB', (폭, Tsawo_Daraja), 정확한값(na_nesa_Daraja, 폭*Tsawo_Daraja*4), 'raw', 'BGRX'), (가로, 세로))
                Wuri_Daraja += 폭*Tsawo_Daraja
            if Wuri_Daraja:
                assert Wuri_Daraja == 너비*높이, Wuri_Daraja
                return zane_Daraja

    def Bincika_pel(Mai_tsarawa_Daraja, 색):
        마감 = time.monotonic()+10
        while True:
            zane_Daraja = Hoton_digo_digo_Hoto()
            if zane_Daraja.getpixel(Mai_tsarawa_Daraja) == 색: return zane_Daraja
            if time.monotonic() > 마감: raise AssertionError((Mai_tsarawa_Daraja, zane_Daraja.getpixel(Mai_tsarawa_Daraja), 색))

    def lodawa_Fayiloli(Suna, Tarin_bayani): Gusar_da_Daraja.storbinary('STOR '+Suna, io.BytesIO(Tarin_bayani))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+girma_SMS+' RGB32').encode() in logu_naɗa
        print('BOOT:', girma_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', logu_naɗa).group(1))
        na_nesa_Daraja = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(na_nesa_Daraja, 12) == b'RFB 003.008\n'; na_nesa_Daraja.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(na_nesa_Daraja, 정확한값(na_nesa_Daraja, 1)[0]); na_nesa_Daraja.sendall(b'\x01')
        assert 정확한값(na_nesa_Daraja, 4) == b'\0'*4; na_nesa_Daraja.sendall(b'\x01')
        초기 = 정확한값(na_nesa_Daraja, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(na_nesa_Daraja, struct.unpack('>I', 초기[20:])[0])
        na_nesa_Daraja.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        na_nesa_Daraja.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        Bincika_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Faruwa,_ in mai_zabe_a916db4e.select(.02):
                    Tarin_bayani=Faruwa.fileobj.read(65536)
                    if Tarin_bayani:logu_naɗa.extend(Tarin_bayani)
        taga=[12,48,568,360]
        def Tabbatar_da_girma():
            ginshiƙi_Daraja,layin_kwance_Daraja=(taga[2]-24)//8,(taga[3]-56)//16
            SMS=Mai_fayyace_umani('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ginshiƙi_Daraja,layin_kwance_Daraja) in SMS,SMS
            # Na_hakika_Tarin_bayani taga 테두리: 단지 Girma Matantanci_Daraja 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            Bincika_pel((taga[0],taga[1]),(32,80,144))
            zane_Daraja=Bincika_pel((taga[0]+taga[2]-1,taga[1]+taga[3]-1),(39,49,64))
            return zane_Daraja
        def 모서리(방향):
            return (taga[0]+(3 if 방향 in (1,3) else taga[2]-4),taga[1]+(3 if 방향<=2 else taga[3]-4))
        def sakegirma_Jawo_abu(방향,차이,maɓali=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            Bincika_pel(흰점,(255,255,255))
            가리키기(가,세,maɓali)
            끝가=max(0,min(너비-1,가+차이[0]));Ƙarshe_Tsaye=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,Ƙarshe_Tsaye,maɓali);가리키기(끝가,Ƙarshe_Tsaye,0);숨고르기()
            if maɓali==1:
                왼,위,폭,Tsawo_Daraja=taga;오른,아래=왼+폭,위+Tsawo_Daraja
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+Ƙarshe_Tsaye-세))
                else:아래=max(위+216,min(높이,아래+Ƙarshe_Tsaye-세))
                taga[:]=[왼,위,오른-왼,아래-위]
        Tabbatar_da_girma();assert manuni_ɓoyayye[0]
        sakegirma_Jawo_abu(4,(-100,-60),4);Tabbatar_da_girma() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            sakegirma_Jawo_abu(방향,차이);Tabbatar_da_girma()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        aika_SMS("echo '"+긴글+"'");숨고르기()
        sakegirma_Jawo_abu(4,(-1000,-1000));assert taga[2:]==[360,216]
        sakegirma_Jawo_abu(4,(너비,높이))
        Tafiyar_da=aika_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Tafiyar_da);Tabbatar_da_girma()
        # vi가 gyaran_Daraja 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        Mai_fayyace_umani('ftpd start')
        Gusar_da_Daraja=ftplib.FTP();Gusar_da_Daraja.encoding='utf-8';Gusar_da_Daraja.connect('127.0.0.1',lambar_kafa,timeout=20);Gusar_da_Daraja.login()
        기다리기(b'NORMAL',aika_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',aika_SMS('i미저장 한글 Tarin_bayani\n'));숨고르기()
        sakegirma_Jawo_abu(4,(-너비,-높이))
        # ANSI layin_kwance_Daraja 이동에 새 layin_kwance_Daraja 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((taga[3]-56)//16)).encode() in logu_naɗa[-4096:]
        aika_SMS('작은 창에서도 이어 Yi_Rubutu\n');숨고르기()
        sakegirma_Jawo_abu(4,(너비,높이))
        aika_SMS('큰 창에서도 이어 Yi_Rubutu\n');숨고르기()
        Danna_maɓali(0xff1b);Danna_maɓali(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',aika_SMS(':wq\n'))
        kunshiya_Daraja=bytearray();Gusar_da_Daraja.retrbinary('RETR 크기자료.txt',kunshiya_Daraja.extend)
        assert kunshiya_Daraja=='미저장 한글 Tarin_bayani\n작은 창에서도 이어 Yi_Rubutu\n큰 창에서도 이어 Yi_Rubutu\n'.encode(),kunshiya_Daraja
        Tabbatar_da_girma().save(str(결과경로/(girma_SMS+'-large.png')))
        # 두 번째 창은 Tanadaddiyar_daraja Girma, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Tafiyar_da=len(logu_naɗa);Danna_Daraja(70,16);기다리기(b'TERMINAL FOCUS 2',Tafiyar_da)
        assert 'TERMINAL SIZE 68x19' in Mai_fayyace_umani('terminal size')
        Tafiyar_da=len(logu_naɗa);Danna_Daraja(180,16);기다리기(b'TERMINAL FOCUS 1',Tafiyar_da);Tabbatar_da_girma()
        sakegirma_Jawo_abu(4,(-너비,-높이));Tabbatar_da_girma().save(str(결과경로/(girma_SMS+'-small.png')))
        # Girma Canza_Daraja Baya_Daraja X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Tafiyar_da=len(logu_naɗa);Danna_Daraja(taga[0]+taga[2]-20,taga[1]+15);기다리기(b'TERMINAL FOCUS 2',Tafiyar_da)
        assert 'RESIZE CLOSED' in Mai_fayyace_umani('echo RESIZE CLOSED')
        print('PASS:',girma_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if Gusar_da_Daraja:Gusar_da_Daraja.close()
        if na_nesa_Daraja:na_nesa_Daraja.close()
        if haryar_aikin_na_ura_Daraja.poll() is None:
            haryar_aikin_na_ura_Daraja.terminate()
            try:haryar_aikin_na_ura_Daraja.wait(timeout=8)
            except subprocess.TimeoutExpired:haryar_aikin_na_ura_Daraja.kill();haryar_aikin_na_ura_Daraja.wait()
        mai_zabe_a916db4e.close();haryar_aikin_na_ura_Daraja.stdout.close();(결과경로/(girma_SMS+'.log')).write_bytes(logu_naɗa)


def Tafiyar_da():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    logu_naɗa={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);logu_naɗa['resolutions'].append([너비,높이])
        logu_naɗa.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(logu_naɗa,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Tafiyar_da()
