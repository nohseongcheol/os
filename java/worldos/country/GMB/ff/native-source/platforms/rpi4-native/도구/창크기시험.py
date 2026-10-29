#!/usr/bin/env python3
"""laatii_keɓe QEMU/VNC에서 터미널 모서리 daasde_njaru·포인터·동적 alkulal_njaru 칸·feewnditde_njaru loowdi_njaru 보존를 검사한다."""
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
from biro_kollal import 정확한값
from 실행 import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    waylude_etannde_binndi = '{}x{}'.format(너비, 높이)
    Yuɓɓo_golle_njaru = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', waylude_etannde_binndi], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(Yuɓɓo_golle_njaru.stdout, selectors.EVENT_READ)
    suurnal_winndande = bytearray(); 원격 = None; egginde_njaru = None; 포인터숨김=[False]

    def 기다리기(hollirde_njaru, huutoraade=0):
        마감 = time.monotonic() + 60
        while hollirde_njaru not in suurnal_winndande[huutoraade:]:
            if time.monotonic() > 마감 or Yuɓɓo_golle_njaru.poll() is not None or b'HALTED' in suurnal_winndande or b'PANIC:' in suurnal_winndande:
                raise AssertionError(suurnal_winndande[huutoraade:].decode('utf-8', 'replace'))
            for saɗteende, _ in 선택기.select(.1):
                keɓe = saɗteende.fileobj.read(65536)
                if keɓe: suurnal_winndande.extend(keɓe)
        return suurnal_winndande[huutoraade:].decode('utf-8', 'replace')

    def dobaade_feɗoode(기호, 눌림=True): 원격.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def neldude_binndi(binndi):
        huutoraade = len(suurnal_winndande)
        for alkulal_njaru in binndi:
            기호 = 0xff0d if alkulal_njaru == '\n' else ord(alkulal_njaru) if ord(alkulal_njaru) < 256 else 0x1000000 | ord(alkulal_njaru)
            dobaade_feɗoode(기호); dobaade_feɗoode(기호, False)
        return huutoraade

    def laalagal(binndi): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', neldude_binndi(binndi+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): 원격.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def dobaade_njaru(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitmap_natal():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 laatii_keɓe 너비를 쓴다.
        원격.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        natal_njaru_c143fe9e = Image.new('RGB', (너비, 높이)); nokku_njaru = 0
        while True:
            종류 = 정확한값(원격, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                njuuteendi_njaru = struct.unpack('>I', 정확한값(원격, 7)[3:])[0]; 정확한값(원격, njuuteendi_njaru); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(원격, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, njuuteendi_njaru, dokkagol_njaru = struct.unpack('>HHHHi', 정확한값(원격, 12))
                if dokkagol_njaru == -239:
                    assert 폭==0 and njuuteendi_njaru==0, 'remote cursor must be hidden'
                    포인터숨김[0]=True
                    continue
                assert dokkagol_njaru == 0 and 가로+폭 <= 너비 and 세로+njuuteendi_njaru <= 높이
                natal_njaru_c143fe9e.paste(Image.frombytes('RGB', (폭, njuuteendi_njaru), 정확한값(원격, 폭*njuuteendi_njaru*4), 'raw', 'BGRX'), (가로, 세로))
                nokku_njaru += 폭*njuuteendi_njaru
            if nokku_njaru:
                assert nokku_njaru == 너비*높이, nokku_njaru
                return natal_njaru_c143fe9e

    def sek_piksel(좌표, 색):
        마감 = time.monotonic()+10
        while True:
            natal_njaru_c143fe9e = bitmap_natal()
            if natal_njaru_c143fe9e.getpixel(좌표) == 색: return natal_njaru_c143fe9e
            if time.monotonic() > 마감: raise AssertionError((좌표, natal_njaru_c143fe9e.getpixel(좌표), 색))

    def 올리기(innde, keɓe): egginde_njaru.storbinary('STOR '+innde, io.BytesIO(keɓe))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+waylude_etannde_binndi+' RGB32').encode() in suurnal_winndande
        print('BOOT:', waylude_etannde_binndi, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', suurnal_winndande).group(1))
        원격 = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(원격, 12) == b'RFB 003.008\n'; 원격.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(원격, 정확한값(원격, 1)[0]); 원격.sendall(b'\x01')
        assert 정확한값(원격, 4) == b'\0'*4; 원격.sendall(b'\x01')
        초기 = 정확한값(원격, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(원격, struct.unpack('>I', 초기[20:])[0])
        원격.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        원격.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        sek_piksel((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for saɗteende,_ in 선택기.select(.02):
                    keɓe=saɗteende.fileobj.read(65536)
                    if keɓe:suurnal_winndande.extend(keɓe)
        falanteere=[12,48,568,360]
        def ƴeewtaade_waylude_etannde():
            darol_njaru,winndande_njaru=(falanteere[2]-24)//8,(falanteere[3]-56)//16
            binndi=laalagal('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(darol_njaru,winndande_njaru) in binndi,binndi
            # laatii_keɓe falanteere 테두리: 단지 waylude_etannde ɗaɓɓal_njaru 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            sek_piksel((falanteere[0],falanteere[1]),(32,80,144))
            natal_njaru_c143fe9e=sek_piksel((falanteere[0]+falanteere[2]-1,falanteere[1]+falanteere[3]-1),(39,49,64))
            return natal_njaru_c143fe9e
        def 모서리(방향):
            return (falanteere[0]+(3 if 방향 in (1,3) else falanteere[2]-4),falanteere[1]+(3 if 방향<=2 else falanteere[3]-4))
        def fonnditde_daasde(방향,차이,feɗoode=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            sek_piksel(흰점,(255,255,255))
            가리키기(가,세,feɗoode)
            끝가=max(0,min(너비-1,가+차이[0]));끝세=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,끝세,feɗoode);가리키기(끝가,끝세,0);숨고르기()
            if feɗoode==1:
                왼,위,폭,njuuteendi_njaru=falanteere;오른,아래=왼+폭,위+njuuteendi_njaru
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+끝세-세))
                else:아래=max(위+216,min(높이,아래+끝세-세))
                falanteere[:]=[왼,위,오른-왼,아래-위]
        ƴeewtaade_waylude_etannde();assert 포인터숨김[0]
        fonnditde_daasde(4,(-100,-60),4);ƴeewtaade_waylude_etannde() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            fonnditde_daasde(방향,차이);ƴeewtaade_waylude_etannde()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        neldude_binndi("echo '"+긴글+"'");숨고르기()
        fonnditde_daasde(4,(-1000,-1000));assert falanteere[2:]==[360,216]
        fonnditde_daasde(4,(너비,높이))
        huutoraade=neldude_binndi('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),huutoraade);ƴeewtaade_waylude_etannde()
        # vi가 feewnditde_njaru 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        laalagal('ftpd start')
        egginde_njaru=ftplib.FTP();egginde_njaru.encoding='utf-8';egginde_njaru.connect('127.0.0.1',접속번호,timeout=20);egginde_njaru.login()
        기다리기(b'NORMAL',neldude_binndi('vi /크기자료.txt\n'))
        기다리기(b'INSERT',neldude_binndi('i미저장 한글 keɓe\n'));숨고르기()
        fonnditde_daasde(4,(-너비,-높이))
        # ANSI winndande_njaru 이동에 새 winndande_njaru 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((falanteere[3]-56)//16)).encode() in suurnal_winndande[-4096:]
        neldude_binndi('작은 창에서도 이어 winndude\n');숨고르기()
        fonnditde_daasde(4,(너비,높이))
        neldude_binndi('큰 창에서도 이어 winndude\n');숨고르기()
        dobaade_feɗoode(0xff1b);dobaade_feɗoode(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',neldude_binndi(':wq\n'))
        loowdi_njaru=bytearray();egginde_njaru.retrbinary('RETR 크기자료.txt',loowdi_njaru.extend)
        assert loowdi_njaru=='미저장 한글 keɓe\n작은 창에서도 이어 winndude\n큰 창에서도 이어 winndude\n'.encode(),loowdi_njaru
        ƴeewtaade_waylude_etannde().save(str(결과경로/(waylude_etannde_binndi+'-large.png')))
        # 두 번째 창은 lasli_njaru waylude_etannde, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        huutoraade=len(suurnal_winndande);dobaade_njaru(70,16);기다리기(b'TERMINAL FOCUS 2',huutoraade)
        assert 'TERMINAL SIZE 68x19' in laalagal('terminal size')
        huutoraade=len(suurnal_winndande);dobaade_njaru(180,16);기다리기(b'TERMINAL FOCUS 1',huutoraade);ƴeewtaade_waylude_etannde()
        fonnditde_daasde(4,(-너비,-높이));ƴeewtaade_waylude_etannde().save(str(결과경로/(waylude_etannde_binndi+'-small.png')))
        # waylude_etannde waklude_njaru Caggal_njaru X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        huutoraade=len(suurnal_winndande);dobaade_njaru(falanteere[0]+falanteere[2]-20,falanteere[1]+15);기다리기(b'TERMINAL FOCUS 2',huutoraade)
        assert 'RESIZE CLOSED' in laalagal('echo RESIZE CLOSED')
        print('PASS:',waylude_etannde_binndi,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if egginde_njaru:egginde_njaru.close()
        if 원격:원격.close()
        if Yuɓɓo_golle_njaru.poll() is None:
            Yuɓɓo_golle_njaru.terminate()
            try:Yuɓɓo_golle_njaru.wait(timeout=8)
            except subprocess.TimeoutExpired:Yuɓɓo_golle_njaru.kill();Yuɓɓo_golle_njaru.wait()
        선택기.close();Yuɓɓo_golle_njaru.stdout.close();(결과경로/(waylude_etannde_binndi+'.log')).write_bytes(suurnal_winndande)


def huutoraade():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    suurnal_winndande={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);suurnal_winndande['resolutions'].append([너비,높이])
        suurnal_winndande.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(suurnal_winndande,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':huutoraade()
