#!/usr/bin/env python3
"""faktinis_duomenys QEMU/VNC에서 Terminalas 모서리 vilkti_VALUE·rodyklė·동적 simbolis_VALUE_068c2631 칸·redaguoti_VALUE Turinys_VALUE 보존를 검사한다."""
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
from darbalaukis_rodyti import EXACT_VALUE
from Vykdyti_komanda import Project_šaknis


def 창크기시험(너비, 높이, KR_kelias):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); prievado_numeris = 임시.getsockname()[1]
    dydis_SMS = '{}x{}'.format(너비, 높이)
    Procesas_VALUE = subprocess.Popen(['python3', str(Project_šaknis/'Įrankiai/Vykdyti_komanda.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(prievado_numeris), '--resolution', dydis_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    išrinkiklis_a916db4e = selectors.DefaultSelector(); išrinkiklis_a916db4e.register(Procesas_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); nuotolinis_VALUE = None; perduoti_VALUE_630ba093 = None; rodyklė_Paslėptas=[False]

    def 기다리기(laida_VALUE, Paleisti=0):
        terminas_VALUE = time.monotonic() + 60
        while laida_VALUE not in LOG_RECORD[Paleisti:]:
            if time.monotonic() > terminas_VALUE or Procesas_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Paleisti:].decode('utf-8', 'replace'))
            for Įvykis, _ in išrinkiklis_a916db4e.select(.1):
                duomenys = Įvykis.fileobj.read(65536)
                if duomenys: LOG_RECORD.extend(duomenys)
        return LOG_RECORD[Paleisti:].decode('utf-8', 'replace')

    def spustelėti_mygtukas(simbolis, 눌림=True): nuotolinis_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbolis))

    def siųsti_SMS_žinutę(Tekstas):
        Paleisti = len(LOG_RECORD)
        for simbolis_VALUE_068c2631 in Tekstas:
            simbolis = 0xff0d if simbolis_VALUE_068c2631 == '\n' else ord(simbolis_VALUE_068c2631) if ord(simbolis_VALUE_068c2631) < 256 else 0x1000000 | ord(simbolis_VALUE_068c2631)
            spustelėti_mygtukas(simbolis); spustelėti_mygtukas(simbolis, False)
        return Paleisti

    def apvalkalas(Tekstas): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', siųsti_SMS_žinutę(Tekstas+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, segmentas_padėtis, 눌림): nuotolinis_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, segmentas_padėtis))

    def spustelėti_VALUE(가로, segmentas_padėtis): 가리키기(가로, segmentas_padėtis, 1); 가리키기(가로, segmentas_padėtis, 0)

    def rastras_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktinis_duomenys 너비를 쓴다.
        nuotolinis_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        piešinys_VALUE = Image.new('RGB', (너비, 높이)); sritis_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(nuotolinis_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(nuotolinis_VALUE, 7)[3:])[0]; EXACT_VALUE(nuotolinis_VALUE, 길이); continue
            assert 종류 == 0, 종류
            prekė_COUNT = struct.unpack('>H', EXACT_VALUE(nuotolinis_VALUE, 3)[1:])[0]
            for _ in range(prekė_COUNT):
                가로, segmentas_padėtis, 폭, 길이, kodavimas_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(nuotolinis_VALUE, 12))
                if kodavimas_VALUE == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    rodyklė_Paslėptas[0]=True
                    continue
                assert kodavimas_VALUE == 0 and 가로+폭 <= 너비 and segmentas_padėtis+길이 <= 높이
                piešinys_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(nuotolinis_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, segmentas_padėtis))
                sritis_VALUE_9285603e += 폭*길이
            if sritis_VALUE_9285603e:
                assert sritis_VALUE_9285603e == 너비*높이, sritis_VALUE_9285603e
                return piešinys_VALUE

    def čekis_pikselis(좌표, 색):
        terminas_VALUE = time.monotonic()+10
        while True:
            piešinys_VALUE = rastras_IMAGE()
            if piešinys_VALUE.getpixel(좌표) == 색: return piešinys_VALUE
            if time.monotonic() > terminas_VALUE: raise AssertionError((좌표, piešinys_VALUE.getpixel(좌표), 색))

    def Upload_Failai(Pavadinimas_2, duomenys): perduoti_VALUE_630ba093.storbinary('STOR '+Pavadinimas_2, io.BytesIO(duomenys))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+dydis_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', dydis_SMS, flush=True)
        nuotolinis_numeris = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        nuotolinis_VALUE = socket.create_connection(('127.0.0.1', nuotolinis_numeris), timeout=20)
        assert EXACT_VALUE(nuotolinis_VALUE, 12) == b'RFB 003.008\n'; nuotolinis_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(nuotolinis_VALUE, EXACT_VALUE(nuotolinis_VALUE, 1)[0]); nuotolinis_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(nuotolinis_VALUE, 4) == b'\0'*4; nuotolinis_VALUE.sendall(b'\x01')
        pradinė_būsena = EXACT_VALUE(nuotolinis_VALUE, 24); assert struct.unpack('>HH', pradinė_būsena[:4]) == (너비, 높이)
        EXACT_VALUE(nuotolinis_VALUE, struct.unpack('>I', pradinė_būsena[20:])[0])
        nuotolinis_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        nuotolinis_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        čekis_pikselis((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Įvykis,_ in išrinkiklis_a916db4e.select(.02):
                    duomenys=Įvykis.fileobj.read(65536)
                    if duomenys:LOG_RECORD.extend(duomenys)
        Langas=[12,48,568,360]
        def patvirtinti_dydis():
            COLUMN_VALUE,ROW_VALUE=(Langas[2]-24)//8,(Langas[3]-56)//16
            Tekstas=apvalkalas('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Tekstas,Tekstas
            # faktinis_duomenys Langas 테두리: 단지 Dydis užklausa_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            čekis_pikselis((Langas[0],Langas[1]),(32,80,144))
            piešinys_VALUE=čekis_pikselis((Langas[0]+Langas[2]-1,Langas[1]+Langas[3]-1),(39,49,64))
            return piešinys_VALUE
        def 모서리(방향):
            return (Langas[0]+(3 if 방향 in (1,3) else Langas[2]-4),Langas[1]+(3 if 방향<=2 else Langas[3]-4))
        def keisti_dydį_vilkti(방향,차이,mygtukas=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            čekis_pikselis(흰점,(255,255,255))
            가리키기(가,세,mygtukas)
            끝가=max(0,min(너비-1,가+차이[0]));baigti_pokalbį_segmentas=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,baigti_pokalbį_segmentas,mygtukas);가리키기(끝가,baigti_pokalbį_segmentas,0);숨고르기()
            if mygtukas==1:
                LEFT_VALUE,위,폭,길이=Langas;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+길이
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+baigti_pokalbį_segmentas-세))
                else:아래=max(위+216,min(높이,아래+baigti_pokalbį_segmentas-세))
                Langas[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        patvirtinti_dydis();assert rodyklė_Paslėptas[0]
        keisti_dydį_vilkti(4,(-100,-60),4);patvirtinti_dydis() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            keisti_dydį_vilkti(방향,차이);patvirtinti_dydis()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        siųsti_SMS_žinutę("echo '"+긴글+"'");숨고르기()
        keisti_dydį_vilkti(4,(-1000,-1000));assert Langas[2:]==[360,216]
        keisti_dydį_vilkti(4,(너비,높이))
        Paleisti=siųsti_SMS_žinutę('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Paleisti);patvirtinti_dydis()
        # vi가 redaguoti_VALUE 중에 화면 크기를 kartoti_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        apvalkalas('ftpd start')
        perduoti_VALUE_630ba093=ftplib.FTP();perduoti_VALUE_630ba093.encoding='utf-8';perduoti_VALUE_630ba093.connect('127.0.0.1',prievado_numeris,timeout=20);perduoti_VALUE_630ba093.login()
        기다리기(b'NORMAL',siųsti_SMS_žinutę('vi /크기자료.txt\n'))
        기다리기(b'INSERT',siųsti_SMS_žinutę('i미저장 한글 duomenys\n'));숨고르기()
        keisti_dydį_vilkti(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Langas[3]-56)//16)).encode() in LOG_RECORD[-4096:]
        siųsti_SMS_žinutę('작은 창에서도 이어 Rašymas\n');숨고르기()
        keisti_dydį_vilkti(4,(너비,높이))
        siųsti_SMS_žinutę('큰 창에서도 이어 Rašymas\n');숨고르기()
        spustelėti_mygtukas(0xff1b);spustelėti_mygtukas(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',siųsti_SMS_žinutę(':wq\n'))
        Turinys_VALUE=bytearray();perduoti_VALUE_630ba093.retrbinary('RETR 크기자료.txt',Turinys_VALUE.extend)
        assert Turinys_VALUE=='미저장 한글 duomenys\n작은 창에서도 이어 Rašymas\n큰 창에서도 이어 Rašymas\n'.encode(),Turinys_VALUE
        patvirtinti_dydis().save(str(KR_kelias/(dydis_SMS+'-large.png')))
        # 두 번째 창은 numatytoji_reikšmė Dydis, kartoti_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Paleisti=len(LOG_RECORD);spustelėti_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Paleisti)
        assert 'TERMINAL SIZE 68x19' in apvalkalas('terminal size')
        Paleisti=len(LOG_RECORD);spustelėti_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Paleisti);patvirtinti_dydis()
        keisti_dydį_vilkti(4,(-너비,-높이));patvirtinti_dydis().save(str(KR_kelias/(dydis_SMS+'-small.png')))
        # Dydis keisti_VALUE ATGAL_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Paleisti=len(LOG_RECORD);spustelėti_VALUE(Langas[0]+Langas[2]-20,Langas[1]+15);기다리기(b'TERMINAL FOCUS 2',Paleisti)
        assert 'RESIZE CLOSED' in apvalkalas('echo RESIZE CLOSED')
        print('PASS:',dydis_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if perduoti_VALUE_630ba093:perduoti_VALUE_630ba093.close()
        if nuotolinis_VALUE:nuotolinis_VALUE.close()
        if Procesas_VALUE.poll() is None:
            Procesas_VALUE.terminate()
            try:Procesas_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Procesas_VALUE.kill();Procesas_VALUE.wait()
        išrinkiklis_a916db4e.close();Procesas_VALUE.stdout.close();(KR_kelias/(dydis_SMS+'.log')).write_bytes(LOG_RECORD)


def Paleisti():
    KR_kelias=Project_šaknis/'build/verification/resize';KR_kelias.mkdir(parents=True,exist_ok=True)
    LOG_RECORD={'passed':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,KR_kelias);LOG_RECORD['resolutions'].append([너비,높이])
        LOG_RECORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(KR_kelias/'report.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Paleisti()
