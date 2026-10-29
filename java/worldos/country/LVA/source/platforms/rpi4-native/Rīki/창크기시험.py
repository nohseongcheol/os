#!/usr/bin/env python3
"""faktisks_dati QEMU/VNC에서 Terminālis 모서리 vilkt_VALUE·rādītājs·동적 rakstzīme_VALUE 칸·Rediģēt_VALUE Saturs_VALUE 보존를 검사한다."""
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
from dators_Skats import EXACT_VALUE
from Izpildīt_komanda import Project_sakne


def 창크기시험(너비, 높이, mērs_ceļš):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); porta_numurs = 임시.getsockname()[1]
    mainīt_izmērus_SMS = '{}x{}'.format(너비, 높이)
    Process_VALUE = subprocess.Popen(['python3', str(Project_sakne/'Rīki/Izpildīt_komanda.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(porta_numurs), '--resolution', mainīt_izmērus_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    atlasītājs_a916db4e = selectors.DefaultSelector(); atlasītājs_a916db4e.register(Process_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); attāls_VALUE = None; nodot_VALUE_630ba093 = None; rādītājs_Slēpts=[False]

    def 기다리기(rādīt_VALUE, Palaist=0):
        izpildes_termiņš_VALUE = time.monotonic() + 60
        while rādīt_VALUE not in LOG_RECORD[Palaist:]:
            if time.monotonic() > izpildes_termiņš_VALUE or Process_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Palaist:].decode('utf-8', 'replace'))
            for Notikums, _ in atlasītājs_a916db4e.select(.1):
                dati = Notikums.fileobj.read(65536)
                if dati: LOG_RECORD.extend(dati)
        return LOG_RECORD[Palaist:].decode('utf-8', 'replace')

    def klikšķis_poga(simbols, 눌림=True): attāls_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbols))

    def sūtīt_īsziņu(Teksts):
        Palaist = len(LOG_RECORD)
        for rakstzīme_VALUE in Teksts:
            simbols = 0xff0d if rakstzīme_VALUE == '\n' else ord(rakstzīme_VALUE) if ord(rakstzīme_VALUE) < 256 else 0x1000000 | ord(rakstzīme_VALUE)
            klikšķis_poga(simbols); klikšķis_poga(simbols, False)
        return Palaist

    def čaula(Teksts): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', sūtīt_īsziņu(Teksts+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, vertikāle_amats, 눌림): attāls_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikāle_amats))

    def klikšķis_VALUE(가로, vertikāle_amats): 가리키기(가로, vertikāle_amats, 1); 가리키기(가로, vertikāle_amats, 0)

    def bitkarte_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktisks_dati 너비를 쓴다.
        attāls_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        zīmējums_VALUE = Image.new('RGB', (너비, 높이)); joma_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(attāls_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(attāls_VALUE, 7)[3:])[0]; EXACT_VALUE(attāls_VALUE, 길이); continue
            assert 종류 == 0, 종류
            krājums_COUNT = struct.unpack('>H', EXACT_VALUE(attāls_VALUE, 3)[1:])[0]
            for _ in range(krājums_COUNT):
                가로, vertikāle_amats, 폭, 길이, kodēšana_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(attāls_VALUE, 12))
                if kodēšana_VALUE == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    rādītājs_Slēpts[0]=True
                    continue
                assert kodēšana_VALUE == 0 and 가로+폭 <= 너비 and vertikāle_amats+길이 <= 높이
                zīmējums_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(attāls_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, vertikāle_amats))
                joma_VALUE_9285603e += 폭*길이
            if joma_VALUE_9285603e:
                assert joma_VALUE_9285603e == 너비*높이, joma_VALUE_9285603e
                return zīmējums_VALUE

    def čeks_attēla_elements(좌표, 색):
        izpildes_termiņš_VALUE = time.monotonic()+10
        while True:
            zīmējums_VALUE = bitkarte_IMAGE()
            if zīmējums_VALUE.getpixel(좌표) == 색: return zīmējums_VALUE
            if time.monotonic() > izpildes_termiņš_VALUE: raise AssertionError((좌표, zīmējums_VALUE.getpixel(좌표), 색))

    def Upload_Faili(Nosaukums, dati): nodot_VALUE_630ba093.storbinary('STOR '+Nosaukums, io.BytesIO(dati))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+mainīt_izmērus_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', mainīt_izmērus_SMS, flush=True)
        attāls_numurs = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        attāls_VALUE = socket.create_connection(('127.0.0.1', attāls_numurs), timeout=20)
        assert EXACT_VALUE(attāls_VALUE, 12) == b'RFB 003.008\n'; attāls_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(attāls_VALUE, EXACT_VALUE(attāls_VALUE, 1)[0]); attāls_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(attāls_VALUE, 4) == b'\0'*4; attāls_VALUE.sendall(b'\x01')
        sākumstāvoklis = EXACT_VALUE(attāls_VALUE, 24); assert struct.unpack('>HH', sākumstāvoklis[:4]) == (너비, 높이)
        EXACT_VALUE(attāls_VALUE, struct.unpack('>I', sākumstāvoklis[20:])[0])
        attāls_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        attāls_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        čeks_attēla_elements((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for Notikums,_ in atlasītājs_a916db4e.select(.02):
                    dati=Notikums.fileobj.read(65536)
                    if dati:LOG_RECORD.extend(dati)
        Logs=[12,48,568,360]
        def verificēt_mainīt_izmērus():
            COLUMN_VALUE,ROW_VALUE=(Logs[2]-24)//8,(Logs[3]-56)//16
            Teksts=čaula('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(COLUMN_VALUE,ROW_VALUE) in Teksts,Teksts
            # faktisks_dati Logs 테두리: 단지 Izmērs vaicāt_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            čeks_attēla_elements((Logs[0],Logs[1]),(32,80,144))
            zīmējums_VALUE=čeks_attēla_elements((Logs[0]+Logs[2]-1,Logs[1]+Logs[3]-1),(39,49,64))
            return zīmējums_VALUE
        def 모서리(방향):
            return (Logs[0]+(3 if 방향 in (1,3) else Logs[2]-4),Logs[1]+(3 if 방향<=2 else Logs[3]-4))
        def mainīt_izmērus_vilkt(방향,차이,Pogas=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            čeks_attēla_elements(흰점,(255,255,255))
            가리키기(가,세,Pogas)
            끝가=max(0,min(너비-1,가+차이[0]));beigt_zvanu_vertikāle=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,beigt_zvanu_vertikāle,Pogas);가리키기(끝가,beigt_zvanu_vertikāle,0);숨고르기()
            if Pogas==1:
                LEFT_VALUE,위,폭,길이=Logs;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+길이
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+beigt_zvanu_vertikāle-세))
                else:아래=max(위+216,min(높이,아래+beigt_zvanu_vertikāle-세))
                Logs[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        verificēt_mainīt_izmērus();assert rādītājs_Slēpts[0]
        mainīt_izmērus_vilkt(4,(-100,-60),4);verificēt_mainīt_izmērus() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            mainīt_izmērus_vilkt(방향,차이);verificēt_mainīt_izmērus()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        sūtīt_īsziņu("echo '"+긴글+"'");숨고르기()
        mainīt_izmērus_vilkt(4,(-1000,-1000));assert Logs[2:]==[360,216]
        mainīt_izmērus_vilkt(4,(너비,높이))
        Palaist=sūtīt_īsziņu('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Palaist);verificēt_mainīt_izmērus()
        # vi가 Rediģēt_VALUE 중에 화면 크기를 mēģināt_vēlreiz_VALUE 읽고, 저장하지 않은 한글도 유지한다.
        čaula('ftpd start')
        nodot_VALUE_630ba093=ftplib.FTP();nodot_VALUE_630ba093.encoding='utf-8';nodot_VALUE_630ba093.connect('127.0.0.1',porta_numurs,timeout=20);nodot_VALUE_630ba093.login()
        기다리기(b'NORMAL',sūtīt_īsziņu('vi /크기자료.txt\n'))
        기다리기(b'INSERT',sūtīt_īsziņu('i미저장 한글 dati\n'));숨고르기()
        mainīt_izmērus_vilkt(4,(-너비,-높이))
        # ANSI ROW_VALUE 이동에 새 ROW_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((Logs[3]-56)//16)).encode() in LOG_RECORD[-4096:]
        sūtīt_īsziņu('작은 창에서도 이어 Rakstīt\n');숨고르기()
        mainīt_izmērus_vilkt(4,(너비,높이))
        sūtīt_īsziņu('큰 창에서도 이어 Rakstīt\n');숨고르기()
        klikšķis_poga(0xff1b);klikšķis_poga(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',sūtīt_īsziņu(':wq\n'))
        Saturs_VALUE=bytearray();nodot_VALUE_630ba093.retrbinary('RETR 크기자료.txt',Saturs_VALUE.extend)
        assert Saturs_VALUE=='미저장 한글 dati\n작은 창에서도 이어 Rakstīt\n큰 창에서도 이어 Rakstīt\n'.encode(),Saturs_VALUE
        verificēt_mainīt_izmērus().save(str(mērs_ceļš/(mainīt_izmērus_SMS+'-large.png')))
        # 두 번째 창은 noklusējuma_vērtība Izmērs, mēģināt_vēlreiz_VALUE 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Palaist=len(LOG_RECORD);klikšķis_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Palaist)
        assert 'TERMINAL SIZE 68x19' in čaula('terminal size')
        Palaist=len(LOG_RECORD);klikšķis_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Palaist);verificēt_mainīt_izmērus()
        mainīt_izmērus_vilkt(4,(-너비,-높이));verificēt_mainīt_izmērus().save(str(mērs_ceļš/(mainīt_izmērus_SMS+'-small.png')))
        # Izmērs mainīt_VALUE ATPAKAĻ_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Palaist=len(LOG_RECORD);klikšķis_VALUE(Logs[0]+Logs[2]-20,Logs[1]+15);기다리기(b'TERMINAL FOCUS 2',Palaist)
        assert 'RESIZE CLOSED' in čaula('echo RESIZE CLOSED')
        print('PASS:',mainīt_izmērus_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if nodot_VALUE_630ba093:nodot_VALUE_630ba093.close()
        if attāls_VALUE:attāls_VALUE.close()
        if Process_VALUE.poll() is None:
            Process_VALUE.terminate()
            try:Process_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Process_VALUE.kill();Process_VALUE.wait()
        atlasītājs_a916db4e.close();Process_VALUE.stdout.close();(mērs_ceļš/(mainīt_izmērus_SMS+'.log')).write_bytes(LOG_RECORD)


def Palaist():
    mērs_ceļš=Project_sakne/'build/verification/resize';mērs_ceļš.mkdir(parents=True,exist_ok=True)
    LOG_RECORD={'passed':False,'kernel_sha256':hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,mērs_ceļš);LOG_RECORD['resolutions'].append([너비,높이])
        LOG_RECORD.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(mērs_ceļš/'report.json').write_text(json.dumps(LOG_RECORD,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Palaist()
