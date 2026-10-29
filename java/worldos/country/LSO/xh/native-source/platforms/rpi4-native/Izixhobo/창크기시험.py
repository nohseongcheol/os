#!/usr/bin/env python3
"""eyona_yenzekileyo_iingcombolo QEMU/VNC에서 i_Terminal 모서리 tsala_ixabiso·isalathisi·동적 ikharakhtha_ixabiso isithuba_ufako_nkcukacha·hlela_ixabiso Isiqulatho_ixabiso 보존를 검사한다."""
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
from idesktophu_bona import 정확한값
from ukwenza_umyalelo import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    isayizi_I_SMS = '{}x{}'.format(너비, 높이)
    Inkqubo_ixabiso = subprocess.Popen(['python3', str(기준/'Izixhobo/ukwenza_umyalelo.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', isayizi_I_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    umkhethi_a916db4e = selectors.DefaultSelector(); umkhethi_a916db4e.register(Inkqubo_ixabiso.stdout, selectors.EVENT_READ)
    ilog_umqolo = bytearray(); kude_ixabiso = None; gqithisela_ixabiso = None; isalathisi_efihliweyo=[False]

    def 기다리기(bonisa_ixabiso, Phumeza=0):
        마감 = time.monotonic() + 60
        while bonisa_ixabiso not in ilog_umqolo[Phumeza:]:
            if time.monotonic() > 마감 or Inkqubo_ixabiso.poll() is not None or b'HALTED' in ilog_umqolo or b'PANIC:' in ilog_umqolo:
                raise AssertionError(ilog_umqolo[Phumeza:].decode('utf-8', 'replace'))
            for umcimbi, _ in umkhethi_a916db4e.select(.1):
                iingcombolo = umcimbi.fileobj.read(65536)
                if iingcombolo: ilog_umqolo.extend(iingcombolo)
        return ilog_umqolo[Phumeza:].decode('utf-8', 'replace')

    def cofa_iqhosha(isimboli, 눌림=True): kude_ixabiso.sendall(struct.pack('>BBHI', 4, int(눌림), 0, isimboli))

    def thumela_i_SMS(Umbhalo):
        Phumeza = len(ilog_umqolo)
        for ikharakhtha_ixabiso in Umbhalo:
            isimboli = 0xff0d if ikharakhtha_ixabiso == '\n' else ord(ikharakhtha_ixabiso) if ord(ikharakhtha_ixabiso) < 256 else 0x1000000 | ord(ikharakhtha_ixabiso)
            cofa_iqhosha(isimboli); cofa_iqhosha(isimboli, False)
        return Phumeza

    def isiniki_myalelo(Umbhalo): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', thumela_i_SMS(Umbhalo+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kude_ixabiso.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def cofa_ixabiso(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def ibhitmephu_umfanekiso():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 eyona_yenzekileyo_iingcombolo 너비를 쓴다.
        kude_ixabiso.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        umzobo_ixabiso = Image.new('RGB', (너비, 높이)); ingingqi_ixabiso = 0
        while True:
            종류 = 정확한값(kude_ixabiso, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ubude_ixabiso = struct.unpack('>I', 정확한값(kude_ixabiso, 7)[3:])[0]; 정확한값(kude_ixabiso, ubude_ixabiso); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kude_ixabiso, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, ubude_ixabiso, ujiko_nkcukacha_zibe_ziikhowudi_ixabiso = struct.unpack('>HHHHi', 정확한값(kude_ixabiso, 12))
                if ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == -239:
                    assert 폭==0 and ubude_ixabiso==0, 'remote cursor must be hidden'
                    isalathisi_efihliweyo[0]=True
                    continue
                assert ujiko_nkcukacha_zibe_ziikhowudi_ixabiso == 0 and 가로+폭 <= 너비 and 세로+ubude_ixabiso <= 높이
                umzobo_ixabiso.paste(Image.frombytes('RGB', (폭, ubude_ixabiso), 정확한값(kude_ixabiso, 폭*ubude_ixabiso*4), 'raw', 'BGRX'), (가로, 세로))
                ingingqi_ixabiso += 폭*ubude_ixabiso
            if ingingqi_ixabiso:
                assert ingingqi_ixabiso == 너비*높이, ingingqi_ixabiso
                return umzobo_ixabiso

    def jonga_i_pel(isilungiselelanisi_ixabiso, 색):
        마감 = time.monotonic()+10
        while True:
            umzobo_ixabiso = ibhitmephu_umfanekiso()
            if umzobo_ixabiso.getpixel(isilungiselelanisi_ixabiso) == 색: return umzobo_ixabiso
            if time.monotonic() > 마감: raise AssertionError((isilungiselelanisi_ixabiso, umzobo_ixabiso.getpixel(isilungiselelanisi_ixabiso), 색))

    def layisha_Iifayile(Igama, iingcombolo): gqithisela_ixabiso.storbinary('STOR '+Igama, io.BytesIO(iingcombolo))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+isayizi_I_SMS+' RGB32').encode() in ilog_umqolo
        print('BOOT:', isayizi_I_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ilog_umqolo).group(1))
        kude_ixabiso = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kude_ixabiso, 12) == b'RFB 003.008\n'; kude_ixabiso.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kude_ixabiso, 정확한값(kude_ixabiso, 1)[0]); kude_ixabiso.sendall(b'\x01')
        assert 정확한값(kude_ixabiso, 4) == b'\0'*4; kude_ixabiso.sendall(b'\x01')
        초기 = 정확한값(kude_ixabiso, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kude_ixabiso, struct.unpack('>I', 초기[20:])[0])
        kude_ixabiso.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kude_ixabiso.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        jonga_i_pel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for umcimbi,_ in umkhethi_a916db4e.select(.02):
                    iingcombolo=umcimbi.fileobj.read(65536)
                    if iingcombolo:ilog_umqolo.extend(iingcombolo)
        i_window=[12,48,568,360]
        def ngqinisisa_isayizi():
            ikholam_ixabiso,umqolo_ixabiso=(i_window[2]-24)//8,(i_window[3]-56)//16
            Umbhalo=isiniki_myalelo('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(ikholam_ixabiso,umqolo_ixabiso) in Umbhalo,Umbhalo
            # eyona_yenzekileyo_iingcombolo i_window 테두리: 단지 Ubukhulu umbuzo_ixabiso 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            jonga_i_pel((i_window[0],i_window[1]),(32,80,144))
            umzobo_ixabiso=jonga_i_pel((i_window[0]+i_window[2]-1,i_window[1]+i_window[3]-1),(39,49,64))
            return umzobo_ixabiso
        def 모서리(방향):
            return (i_window[0]+(3 if 방향 in (1,3) else i_window[2]-4),i_window[1]+(3 if 방향<=2 else i_window[3]-4))
        def khangela_kwakhona_ubungakanani_tsala(방향,차이,iqhosha=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            jonga_i_pel(흰점,(255,255,255))
            가리키기(가,세,iqhosha)
            끝가=max(0,min(너비-1,가+차이[0]));phela_Ethe_nkqo=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,phela_Ethe_nkqo,iqhosha);가리키기(끝가,phela_Ethe_nkqo,0);숨고르기()
            if iqhosha==1:
                왼,위,폭,ubude_ixabiso=i_window;오른,아래=왼+폭,위+ubude_ixabiso
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+phela_Ethe_nkqo-세))
                else:아래=max(위+216,min(높이,아래+phela_Ethe_nkqo-세))
                i_window[:]=[왼,위,오른-왼,아래-위]
        ngqinisisa_isayizi();assert isalathisi_efihliweyo[0]
        khangela_kwakhona_ubungakanani_tsala(4,(-100,-60),4);ngqinisisa_isayizi() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            khangela_kwakhona_ubungakanani_tsala(방향,차이);ngqinisisa_isayizi()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        thumela_i_SMS("echo '"+긴글+"'");숨고르기()
        khangela_kwakhona_ubungakanani_tsala(4,(-1000,-1000));assert i_window[2:]==[360,216]
        khangela_kwakhona_ubungakanani_tsala(4,(너비,높이))
        Phumeza=thumela_i_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),Phumeza);ngqinisisa_isayizi()
        # vi가 hlela_ixabiso 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        isiniki_myalelo('ftpd start')
        gqithisela_ixabiso=ftplib.FTP();gqithisela_ixabiso.encoding='utf-8';gqithisela_ixabiso.connect('127.0.0.1',접속번호,timeout=20);gqithisela_ixabiso.login()
        기다리기(b'NORMAL',thumela_i_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',thumela_i_SMS('i미저장 한글 iingcombolo\n'));숨고르기()
        khangela_kwakhona_ubungakanani_tsala(4,(-너비,-높이))
        # ANSI umqolo_ixabiso 이동에 새 umqolo_ixabiso 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((i_window[3]-56)//16)).encode() in ilog_umqolo[-4096:]
        thumela_i_SMS('작은 창에서도 이어 Bhala\n');숨고르기()
        khangela_kwakhona_ubungakanani_tsala(4,(너비,높이))
        thumela_i_SMS('큰 창에서도 이어 Bhala\n');숨고르기()
        cofa_iqhosha(0xff1b);cofa_iqhosha(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',thumela_i_SMS(':wq\n'))
        Isiqulatho_ixabiso=bytearray();gqithisela_ixabiso.retrbinary('RETR 크기자료.txt',Isiqulatho_ixabiso.extend)
        assert Isiqulatho_ixabiso=='미저장 한글 iingcombolo\n작은 창에서도 이어 Bhala\n큰 창에서도 이어 Bhala\n'.encode(),Isiqulatho_ixabiso
        ngqinisisa_isayizi().save(str(결과경로/(isayizi_I_SMS+'-large.png')))
        # 두 번째 창은 ixabiso_elisisiseko Ubukhulu, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        Phumeza=len(ilog_umqolo);cofa_ixabiso(70,16);기다리기(b'TERMINAL FOCUS 2',Phumeza)
        assert 'TERMINAL SIZE 68x19' in isiniki_myalelo('terminal size')
        Phumeza=len(ilog_umqolo);cofa_ixabiso(180,16);기다리기(b'TERMINAL FOCUS 1',Phumeza);ngqinisisa_isayizi()
        khangela_kwakhona_ubungakanani_tsala(4,(-너비,-높이));ngqinisisa_isayizi().save(str(결과경로/(isayizi_I_SMS+'-small.png')))
        # Ubukhulu tshintsha_ixabiso Emva_ixabiso X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        Phumeza=len(ilog_umqolo);cofa_ixabiso(i_window[0]+i_window[2]-20,i_window[1]+15);기다리기(b'TERMINAL FOCUS 2',Phumeza)
        assert 'RESIZE CLOSED' in isiniki_myalelo('echo RESIZE CLOSED')
        print('PASS:',isayizi_I_SMS,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if gqithisela_ixabiso:gqithisela_ixabiso.close()
        if kude_ixabiso:kude_ixabiso.close()
        if Inkqubo_ixabiso.poll() is None:
            Inkqubo_ixabiso.terminate()
            try:Inkqubo_ixabiso.wait(timeout=8)
            except subprocess.TimeoutExpired:Inkqubo_ixabiso.kill();Inkqubo_ixabiso.wait()
        umkhethi_a916db4e.close();Inkqubo_ixabiso.stdout.close();(결과경로/(isayizi_I_SMS+'.log')).write_bytes(ilog_umqolo)


def Phumeza():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    ilog_umqolo={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);ilog_umqolo['resolutions'].append([너비,높이])
        ilog_umqolo.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(ilog_umqolo,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':Phumeza()
