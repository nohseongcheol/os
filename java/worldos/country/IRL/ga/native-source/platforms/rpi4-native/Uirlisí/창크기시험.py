#!/usr/bin/env python3
"""iarbhír_sonraí QEMU/VNC에서 Teirminéal 모서리 tarraing_VALUE·pointeoir·동적 carachtar_VALUE spás_iontráil·cuir_in_eagar_VALUE Inneachar_VALUE 보존를 검사한다."""
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
from deasc_Amharc import EXACT_VALUE
from Rith_ordú import teilgean_fréamh


def 창크기시험(너비, 높이, tomhas_cosán):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); uimhir_phoirt = 임시.getsockname()[1]
    socraigh_méid_SMS = '{}x{}'.format(너비, 높이)
    Próiseas_VALUE = subprocess.Popen(['python3', str(teilgean_fréamh/'Uirlisí/Rith_ordú.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(uimhir_phoirt), '--resolution', socraigh_méid_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    roghnóir_a916db4e = selectors.DefaultSelector(); roghnóir_a916db4e.register(Próiseas_VALUE.stdout, selectors.EVENT_READ)
    LOG_ró = bytearray(); cianda_VALUE = None; traschur_VALUE = None; pointeoir_folaithe=[False]

    def 기다리기(seó_VALUE, Rith_2=0):
        마감 = time.monotonic() + 60
        while seó_VALUE not in LOG_ró[Rith_2:]:
            if time.monotonic() > 마감 or Próiseas_VALUE.poll() is not None or b'HALTED' in LOG_ró or b'PANIC:' in LOG_ró:
                raise AssertionError(LOG_ró[Rith_2:].decode('utf-8', 'replace'))
            for ócáid, _ in roghnóir_a916db4e.select(.1):
                sonraí = ócáid.fileobj.read(65536)
                if sonraí: LOG_ró.extend(sonraí)
        return LOG_ró[Rith_2:].decode('utf-8', 'replace')

    def cliceáil_cnaipe(siombail, 눌림=True): cianda_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, siombail))

    def SMS_a_sheoladh(Téacs):
        Rith_2 = len(LOG_ró)
        for carachtar_VALUE in Téacs:
            siombail = 0xff0d if carachtar_VALUE == '\n' else ord(carachtar_VALUE) if ord(carachtar_VALUE) < 256 else 0x1000000 | ord(carachtar_VALUE)
            cliceáil_cnaipe(siombail); cliceáil_cnaipe(siombail, False)
        return Rith_2

    def blaosc(Téacs): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_a_sheoladh(Téacs+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, Ingearach_suíomh, 눌림): cianda_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Ingearach_suíomh))

    def cliceáil_VALUE(가로, Ingearach_suíomh): 가리키기(가로, Ingearach_suíomh, 1); 가리키기(가로, Ingearach_suíomh, 0)

    def mapa_giotán_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 iarbhír_sonraí 너비를 쓴다.
        cianda_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        líníocht_VALUE = Image.new('RGB', (너비, 높이)); catagóir_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(cianda_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                fad_VALUE = struct.unpack('>I', EXACT_VALUE(cianda_VALUE, 7)[3:])[0]; EXACT_VALUE(cianda_VALUE, fad_VALUE); continue
            assert 종류 == 0, 종류
            mír_COUNT = struct.unpack('>H', EXACT_VALUE(cianda_VALUE, 3)[1:])[0]
            for _ in range(mír_COUNT):
                가로, Ingearach_suíomh, 폭, fad_VALUE, ionchódú_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(cianda_VALUE, 12))
                if ionchódú_VALUE == -239:
                    assert 폭==0 and fad_VALUE==0, 'remote cursor must be hidden'
                    pointeoir_folaithe[0]=True
                    continue
                assert ionchódú_VALUE == 0 and 가로+폭 <= 너비 and Ingearach_suíomh+fad_VALUE <= 높이
                líníocht_VALUE.paste(Image.frombytes('RGB', (폭, fad_VALUE), EXACT_VALUE(cianda_VALUE, 폭*fad_VALUE*4), 'raw', 'BGRX'), (가로, Ingearach_suíomh))
                catagóir_VALUE_9285603e += 폭*fad_VALUE
            if catagóir_VALUE_9285603e:
                assert catagóir_VALUE_9285603e == 너비*높이, catagóir_VALUE_9285603e
                return líníocht_VALUE

    def seic_picteilín(comhordanáid_VALUE, 색):
        마감 = time.monotonic()+10
        while True:
            líníocht_VALUE = mapa_giotán_IMAGE()
            if líníocht_VALUE.getpixel(comhordanáid_VALUE) == 색: return líníocht_VALUE
            if time.monotonic() > 마감: raise AssertionError((comhordanáid_VALUE, líníocht_VALUE.getpixel(comhordanáid_VALUE), 색))

    def uaslódáil_Comhaid(Ainm, sonraí): traschur_VALUE.storbinary('STOR '+Ainm, io.BytesIO(sonraí))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+socraigh_méid_SMS+' RGB32').encode() in LOG_ró
        print('BOOT:', socraigh_méid_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_ró).group(1))
        cianda_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(cianda_VALUE, 12) == b'RFB 003.008\n'; cianda_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(cianda_VALUE, EXACT_VALUE(cianda_VALUE, 1)[0]); cianda_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(cianda_VALUE, 4) == b'\0'*4; cianda_VALUE.sendall(b'\x01')
        초기 = EXACT_VALUE(cianda_VALUE, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_VALUE(cianda_VALUE, struct.unpack('>I', 초기[20:])[0])
        cianda_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        cianda_VALUE.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        seic_picteilín((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ócáid,_ in roghnóir_a916db4e.select(.02):
                    sonraí=ócáid.fileobj.read(65536)
                    if sonraí:LOG_ró.extend(sonraí)
        fuinneog=[12,48,568,360]
        def fíoraigh_socraigh_méid():
            colún_VALUE,ró_VALUE=(fuinneog[2]-24)//8,(fuinneog[3]-56)//16
            Téacs=blaosc('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(colún_VALUE,ró_VALUE) in Téacs,Téacs
            # iarbhír_sonraí fuinneog 테두리: 단지 Méid iarratas_VALUE 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            seic_picteilín((fuinneog[0],fuinneog[1]),(32,80,144))
            líníocht_VALUE=seic_picteilín((fuinneog[0]+fuinneog[2]-1,fuinneog[1]+fuinneog[3]-1),(39,49,64))
            return líníocht_VALUE
        def 모서리(방향):
            return (fuinneog[0]+(3 if 방향 in (1,3) else fuinneog[2]-4),fuinneog[1]+(3 if 방향<=2 else fuinneog[3]-4))
        def athraigh_méid_tarraing(방향,차이,cnaipe=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            seic_picteilín(흰점,(255,255,255))
            가리키기(가,세,cnaipe)
            끝가=max(0,min(너비-1,가+차이[0]));cuir_deireadh_le_Ingearach=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,cuir_deireadh_le_Ingearach,cnaipe);가리키기(끝가,cuir_deireadh_le_Ingearach,0);숨고르기()
            if cnaipe==1:
                LEFT_VALUE,위,폭,fad_VALUE=fuinneog;RIGHT_VALUE,아래=LEFT_VALUE+폭,위+fad_VALUE
                if 방향 in (1,3):LEFT_VALUE=max(0,min(RIGHT_VALUE-360,LEFT_VALUE+끝가-가))
                else:RIGHT_VALUE=max(LEFT_VALUE+360,min(너비,RIGHT_VALUE+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+cuir_deireadh_le_Ingearach-세))
                else:아래=max(위+216,min(높이,아래+cuir_deireadh_le_Ingearach-세))
                fuinneog[:]=[LEFT_VALUE,위,RIGHT_VALUE-LEFT_VALUE,아래-위]
        fíoraigh_socraigh_méid();assert pointeoir_folaithe[0]
        athraigh_méid_tarraing(4,(-100,-60),4);fíoraigh_socraigh_méid() # RIGHT 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            athraigh_méid_tarraing(방향,차이);fíoraigh_socraigh_méid()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_a_sheoladh("echo '"+긴글+"'");숨고르기()
        athraigh_méid_tarraing(4,(-1000,-1000));assert fuinneog[2:]==[360,216]
        athraigh_méid_tarraing(4,(너비,높이))
        Rith_2=SMS_a_sheoladh('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Rith_2);fíoraigh_socraigh_méid()
        # vi가 cuir_in_eagar_VALUE 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        blaosc('ftpd start')
        traschur_VALUE=ftplib.FTP();traschur_VALUE.encoding='utf-8';traschur_VALUE.connect('127.0.0.1',uimhir_phoirt,timeout=20);traschur_VALUE.login()
        기다리기(b'NORMAL',SMS_a_sheoladh('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_a_sheoladh('i미저장 한글 sonraí\n'));숨고르기()
        athraigh_méid_tarraing(4,(-너비,-높이))
        # ANSI ró_VALUE 이동에 새 ró_VALUE 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((fuinneog[3]-56)//16)).encode() in LOG_ró[-4096:]
        SMS_a_sheoladh('작은 창에서도 이어 Scríobh\n');숨고르기()
        athraigh_méid_tarraing(4,(너비,높이))
        SMS_a_sheoladh('큰 창에서도 이어 Scríobh\n');숨고르기()
        cliceáil_cnaipe(0xff1b);cliceáil_cnaipe(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_a_sheoladh(':wq\n'))
        Inneachar_VALUE=bytearray();traschur_VALUE.retrbinary('RETR 크기자료.txt',Inneachar_VALUE.extend)
        assert Inneachar_VALUE=='미저장 한글 sonraí\n작은 창에서도 이어 Scríobh\n큰 창에서도 이어 Scríobh\n'.encode(),Inneachar_VALUE
        fíoraigh_socraigh_méid().save(str(tomhas_cosán/(socraigh_méid_SMS+'-large.png')))
        # 두 번째 창은 luach_réamhshocraithe Méid, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Rith_2=len(LOG_ró);cliceáil_VALUE(70,16);기다리기(b'TERMINAL FOCUS 2',Rith_2)
        assert 'TERMINAL SIZE 68x19' in blaosc('terminal size')
        Rith_2=len(LOG_ró);cliceáil_VALUE(180,16);기다리기(b'TERMINAL FOCUS 1',Rith_2);fíoraigh_socraigh_méid()
        athraigh_méid_tarraing(4,(-너비,-높이));fíoraigh_socraigh_méid().save(str(tomhas_cosán/(socraigh_méid_SMS+'-small.png')))
        # Méid athraigh_VALUE Siar_VALUE X 닫기도 새로운 RIGHT 가장자리를 사용한다.
        Rith_2=len(LOG_ró);cliceáil_VALUE(fuinneog[0]+fuinneog[2]-20,fuinneog[1]+15);기다리기(b'TERMINAL FOCUS 2',Rith_2)
        assert 'RESIZE CLOSED' in blaosc('echo RESIZE CLOSED')
        print('PASS:',socraigh_méid_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if traschur_VALUE:traschur_VALUE.close()
        if cianda_VALUE:cianda_VALUE.close()
        if Próiseas_VALUE.poll() is None:
            Próiseas_VALUE.terminate()
            try:Próiseas_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired:Próiseas_VALUE.kill();Próiseas_VALUE.wait()
        roghnóir_a916db4e.close();Próiseas_VALUE.stdout.close();(tomhas_cosán/(socraigh_méid_SMS+'.log')).write_bytes(LOG_ró)


def Rith_2():
    tomhas_cosán=teilgean_fréamh/'build/verification/resize';tomhas_cosán.mkdir(parents=True,exist_ok=True)
    LOG_ró={'passed':False,'kernel_sha256':hashlib.sha256((teilgean_fréamh/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,tomhas_cosán);LOG_ró['resolutions'].append([너비,높이])
        LOG_ró.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(tomhas_cosán/'report.json').write_text(json.dumps(LOG_ró,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Rith_2()
