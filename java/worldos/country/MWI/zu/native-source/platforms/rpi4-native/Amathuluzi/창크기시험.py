#!/usr/bin/env python3
"""ulwazi_ngokwenzekile_imininingwane QEMU/VNC에서 터미널 모서리 donsa_inani·isikhombi·동적 uhlamvusimo_inani isikhala_okufakwayo·hlela_inani Okuqukethwe_inani 보존를 검사한다."""
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
from ideskithophu_buka import 정확한값
from yenza_umyalo import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    linganisa_I_SMS = '{}x{}'.format(너비, 높이)
    Inqubo_inani = subprocess.Popen(['python3', str(기준/'Amathuluzi/yenza_umyalo.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', linganisa_I_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    isiqoki_a916db4e = selectors.DefaultSelector(); isiqoki_a916db4e.register(Inqubo_inani.stdout, selectors.EVENT_READ)
    loga_umugqa = bytearray(); kude_inani = None; dlulisa_inani_630ba093 = None; isikhombi_kufihliwe=[False]

    def 기다리기(khombisa_inani, Sebenzisa=0):
        마감 = time.monotonic() + 60
        while khombisa_inani not in loga_umugqa[Sebenzisa:]:
            if time.monotonic() > 마감 or Inqubo_inani.poll() is not None or b'HALTED' in loga_umugqa or b'PANIC:' in loga_umugqa:
                raise AssertionError(loga_umugqa[Sebenzisa:].decode('utf-8', 'replace'))
            for isigameko, _ in isiqoki_a916db4e.select(.1):
                imininingwane = isigameko.fileobj.read(65536)
                if imininingwane: loga_umugqa.extend(imininingwane)
        return loga_umugqa[Sebenzisa:].decode('utf-8', 'replace')

    def qhafaza_inkinobho(uphawu_ad6f1a96, 눌림=True): kude_inani.sendall(struct.pack('>BBHI', 4, int(눌림), 0, uphawu_ad6f1a96))

    def thumela_i_SMS(Itekisi):
        Sebenzisa = len(loga_umugqa)
        for uhlamvusimo_inani in Itekisi:
            uphawu_ad6f1a96 = 0xff0d if uhlamvusimo_inani == '\n' else ord(uhlamvusimo_inani) if ord(uhlamvusimo_inani) < 256 else 0x1000000 | ord(uhlamvusimo_inani)
            qhafaza_inkinobho(uphawu_ad6f1a96); qhafaza_inkinobho(uphawu_ad6f1a96, False)
        return Sebenzisa

    def isihumushi_miyalelo(Itekisi): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', thumela_i_SMS(Itekisi+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kude_inani.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def qhafaza_inani(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def isithombe_samabhithi_isithombe():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ulwazi_ngokwenzekile_imininingwane 너비를 쓴다.
        kude_inani.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        umdwebo_inani = Image.new('RGB', (너비, 높이)); indawo_inani = 0
        while True:
            종류 = 정확한값(kude_inani, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ubude_inani = struct.unpack('>I', 정확한값(kude_inani, 7)[3:])[0]; 정확한값(kude_inani, ubude_inani); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kude_inani, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ubude_inani, ukubhala_ngokufihla_inani = struct.unpack('>HHHHi', 정확한값(kude_inani, 12))
                if ukubhala_ngokufihla_inani == -239:
                    assert 폭==0 and ubude_inani==0, 'remote cursor must be hidden'
                    isikhombi_kufihliwe[0]=True
                    continue
                assert ukubhala_ngokufihla_inani == 0 and 가로+폭 <= 너비 and 세로+ubude_inani <= 높이
                umdwebo_inani.paste(Image.frombytes('RGB', (폭, ubude_inani), 정확한값(kude_inani, 폭*ubude_inani*4), 'raw', 'BGRX'), (가로, 세로))
                indawo_inani += 폭*ubude_inani
            if indawo_inani:
                assert indawo_inani == 너비*높이, indawo_inani
                return umdwebo_inani

    def hlola_i_pel(iphuzumkhathi_inani, 색):
        마감 = time.monotonic()+10
        while True:
            umdwebo_inani = isithombe_samabhithi_isithombe()
            if umdwebo_inani.getpixel(iphuzumkhathi_inani) == 색: return umdwebo_inani
            if time.monotonic() > 마감: raise AssertionError((iphuzumkhathi_inani, umdwebo_inani.getpixel(iphuzumkhathi_inani), 색))

    def layisha_Amafayela(Igama, imininingwane): dlulisa_inani_630ba093.storbinary('STOR '+Igama, io.BytesIO(imininingwane))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+linganisa_I_SMS+' RGB32').encode() in loga_umugqa
        print('BOOT:', linganisa_I_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', loga_umugqa).group(1))
        kude_inani = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kude_inani, 12) == b'RFB 003.008\n'; kude_inani.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kude_inani, 정확한값(kude_inani, 1)[0]); kude_inani.sendall(b'\x01')
        assert 정확한값(kude_inani, 4) == b'\0'*4; kude_inani.sendall(b'\x01')
        초기 = 정확한값(kude_inani, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kude_inani, struct.unpack('>I', 초기[20:])[0])
        kude_inani.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kude_inani.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        hlola_i_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for isigameko,_ in isiqoki_a916db4e.select(.02):
                    imininingwane=isigameko.fileobj.read(65536)
                    if imininingwane:loga_umugqa.extend(imininingwane)
        ifasitela=[12,48,568,360]
        def qiniseka_linganisa():
            ikholomu_inani,umugqa_inani=(ifasitela[2]-24)//8,(ifasitela[3]-56)//16
            Itekisi=isihumushi_miyalelo('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ikholomu_inani,umugqa_inani) in Itekisi,Itekisi
            # ulwazi_ngokwenzekile_imininingwane ifasitela 테두리: 단지 Ubungako umbuzo_inani 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            hlola_i_pel((ifasitela[0],ifasitela[1]),(32,80,144))
            umdwebo_inani=hlola_i_pel((ifasitela[0]+ifasitela[2]-1,ifasitela[1]+ifasitela[3]-1),(39,49,64))
            return umdwebo_inani
        def 모서리(방향):
            return (ifasitela[0]+(3 if 방향 in (1,3) else ifasitela[2]-4),ifasitela[1]+(3 if 방향<=2 else ifasitela[3]-4))
        def ukulinganisa_kabusha_donsa(방향,차이,inkinobho=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            hlola_i_pel(흰점,(255,255,255))
            가리키기(가,세,inkinobho)
            끝가=max(0,min(너비-1,가+차이[0]));yekisa_Okuqondile=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,yekisa_Okuqondile,inkinobho);가리키기(끝가,yekisa_Okuqondile,0);숨고르기()
            if inkinobho==1:
                왼,위,폭,ubude_inani=ifasitela;오른,아래=왼+폭,위+ubude_inani
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+yekisa_Okuqondile-세))
                else:아래=max(위+216,min(높이,아래+yekisa_Okuqondile-세))
                ifasitela[:]=[왼,위,오른-왼,아래-위]
        qiniseka_linganisa();assert isikhombi_kufihliwe[0]
        ukulinganisa_kabusha_donsa(4,(-100,-60),4);qiniseka_linganisa() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ukulinganisa_kabusha_donsa(방향,차이);qiniseka_linganisa()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        thumela_i_SMS("echo '"+긴글+"'");숨고르기()
        ukulinganisa_kabusha_donsa(4,(-1000,-1000));assert ifasitela[2:]==[360,216]
        ukulinganisa_kabusha_donsa(4,(너비,높이))
        Sebenzisa=thumela_i_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Sebenzisa);qiniseka_linganisa()
        # vi가 hlela_inani 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        isihumushi_miyalelo('ftpd start')
        dlulisa_inani_630ba093=ftplib.FTP();dlulisa_inani_630ba093.encoding='utf-8';dlulisa_inani_630ba093.connect('127.0.0.1',접속번호,timeout=20);dlulisa_inani_630ba093.login()
        기다리기(b'NORMAL',thumela_i_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',thumela_i_SMS('i미저장 한글 imininingwane\n'));숨고르기()
        ukulinganisa_kabusha_donsa(4,(-너비,-높이))
        # ANSI umugqa_inani 이동에 새 umugqa_inani 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((ifasitela[3]-56)//16)).encode() in loga_umugqa[-4096:]
        thumela_i_SMS('작은 창에서도 이어 Bhala\n');숨고르기()
        ukulinganisa_kabusha_donsa(4,(너비,높이))
        thumela_i_SMS('큰 창에서도 이어 Bhala\n');숨고르기()
        qhafaza_inkinobho(0xff1b);qhafaza_inkinobho(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',thumela_i_SMS(':wq\n'))
        Okuqukethwe_inani=bytearray();dlulisa_inani_630ba093.retrbinary('RETR 크기자료.txt',Okuqukethwe_inani.extend)
        assert Okuqukethwe_inani=='미저장 한글 imininingwane\n작은 창에서도 이어 Bhala\n큰 창에서도 이어 Bhala\n'.encode(),Okuqukethwe_inani
        qiniseka_linganisa().save(str(결과경로/(linganisa_I_SMS+'-large.png')))
        # 두 번째 창은 inani_elimisiwe Ubungako, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Sebenzisa=len(loga_umugqa);qhafaza_inani(70,16);기다리기(b'TERMINAL FOCUS 2',Sebenzisa)
        assert 'TERMINAL SIZE 68x19' in isihumushi_miyalelo('terminal size')
        Sebenzisa=len(loga_umugqa);qhafaza_inani(180,16);기다리기(b'TERMINAL FOCUS 1',Sebenzisa);qiniseka_linganisa()
        ukulinganisa_kabusha_donsa(4,(-너비,-높이));qiniseka_linganisa().save(str(결과경로/(linganisa_I_SMS+'-small.png')))
        # Ubungako guqula_inani Impindamuva_inani X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Sebenzisa=len(loga_umugqa);qhafaza_inani(ifasitela[0]+ifasitela[2]-20,ifasitela[1]+15);기다리기(b'TERMINAL FOCUS 2',Sebenzisa)
        assert 'RESIZE CLOSED' in isihumushi_miyalelo('echo RESIZE CLOSED')
        print('PASS:',linganisa_I_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if dlulisa_inani_630ba093:dlulisa_inani_630ba093.close()
        if kude_inani:kude_inani.close()
        if Inqubo_inani.poll() is None:
            Inqubo_inani.terminate()
            try:Inqubo_inani.wait(timeout=8)
            except subprocess.TimeoutExpired:Inqubo_inani.kill();Inqubo_inani.wait()
        isiqoki_a916db4e.close();Inqubo_inani.stdout.close();(결과경로/(linganisa_I_SMS+'.log')).write_bytes(loga_umugqa)


def Sebenzisa():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    loga_umugqa={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);loga_umugqa['resolutions'].append([너비,높이])
        loga_umugqa.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(loga_umugqa,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Sebenzisa()
