#!/usr/bin/env python3
"""వాస్తవ_డేటా QEMU/VNC에서 టెర్మినల్ 모서리 లాగు_మూల్యం·పాయింటర్·동적 అక్షరం_మూల్యం స్లాట్_ప్రవేశం·సంకలనంచేయు_మూల్యం విషయం_మూల్యం 보존를 검사한다."""
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
from డెస్క్_టాప్_వీక్షణ import 정확한값
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def 창크기시험(너비, 높이, ప్రమాణం_పథం):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); పోర్ట్_సంఖ్య = 임시.getsockname()[1]
    పరిమాణం_మార్చు_పాఠం = '{}x{}'.format(너비, 높이)
    విధానం_మూల్యం = subprocess.Popen(['python3', str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/అమలు_చేయి_ఆదేశం.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(పోర్ట్_సంఖ్య), '--resolution', పరిమాణం_మార్చు_పాఠం], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    సెలక్టర్_a916db4e = selectors.DefaultSelector(); సెలక్టర్_a916db4e.register(విధానం_మూల్యం.stdout, selectors.EVENT_READ)
    లాగ్_వరుస = bytearray(); రిమోట్_మూల్యం = None; బదిలీ_మూల్యం = None; పాయింటర్_అదృశ్య=[False]

    def 기다리기(చూపించు_మూల్యం, నడుపుము=0):
        마감 = time.monotonic() + 60
        while చూపించు_మూల్యం not in లాగ్_వరుస[నడుపుము:]:
            if time.monotonic() > 마감 or విధానం_మూల్యం.poll() is not None or b'HALTED' in లాగ్_వరుస or b'PANIC:' in లాగ్_వరుస:
                raise AssertionError(లాగ్_వరుస[నడుపుము:].decode('utf-8', 'replace'))
            for ఈవెంట్, _ in సెలక్టర్_a916db4e.select(.1):
                డేటా = ఈవెంట్.fileobj.read(65536)
                if డేటా: లాగ్_వరుస.extend(డేటా)
        return లాగ్_వరుస[నడుపుము:].decode('utf-8', 'replace')

    def క్లిక్_చెయండి_బటన్(చిహ్నం, 눌림=True): రిమోట్_మూల్యం.sendall(struct.pack('>BBHI', 4, int(눌림), 0, చిహ్నం))

    def SMS_పంపు(పాఠ్యము):
        నడుపుము = len(లాగ్_వరుస)
        for అక్షరం_మూల్యం in పాఠ్యము:
            చిహ్నం = 0xff0d if అక్షరం_మూల్యం == '\n' else ord(అక్షరం_మూల్యం) if ord(అక్షరం_మూల్యం) < 256 else 0x1000000 | ord(అక్షరం_మూల్యం)
            క్లిక్_చెయండి_బటన్(చిహ్నం); క్లిక్_చెయండి_బటన్(చిహ్నం, False)
        return నడుపుము

    def షెల్(పాఠ్యము): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_పంపు(పాఠ్యము+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, నిలువు_స్థాయి, 눌림): రిమోట్_మూల్యం.sendall(struct.pack('>BBHH', 5, 눌림, 가로, నిలువు_స్థాయి))

    def క్లిక్_చెయండి_మూల్యం(가로, నిలువు_స్థాయి): 가리키기(가로, నిలువు_స్థాయి, 1); 가리키기(가로, నిలువు_స్థాయి, 0)

    def బిట్_మ్యాప్_చిత్రం():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 వాస్తవ_డేటా 너비를 쓴다.
        రిమోట్_మూల్యం.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        రేఖాచిత్రణ_మూల్యం = Image.new('RGB', (너비, 높이)); ప్రదేశం_మూల్యం = 0
        while True:
            종류 = 정확한값(రిమోట్_మూల్యం, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                పొడవు_మూల్యం = struct.unpack('>I', 정확한값(రిమోట్_మూల్యం, 7)[3:])[0]; 정확한값(రిమోట్_మూల్యం, పొడవు_మూల్యం); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(రిమోట్_మూల్యం, 3)[1:])[0]
            for _ in range(개수):
                가로, నిలువు_స్థాయి, 폭, పొడవు_మూల్యం, సంకేతీకరణం_మూల్యం = struct.unpack('>HHHHi', 정확한값(రిమోట్_మూల్యం, 12))
                if సంకేతీకరణం_మూల్యం == -239:
                    assert 폭==0 and పొడవు_మూల్యం==0, 'remote cursor must be hidden'
                    పాయింటర్_అదృశ్య[0]=True
                    continue
                assert సంకేతీకరణం_మూల్యం == 0 and 가로+폭 <= 너비 and నిలువు_స్థాయి+పొడవు_మూల్యం <= 높이
                రేఖాచిత్రణ_మూల్యం.paste(Image.frombytes('RGB', (폭, పొడవు_మూల్యం), 정확한값(రిమోట్_మూల్యం, 폭*పొడవు_మూల్యం*4), 'raw', 'BGRX'), (가로, నిలువు_స్థాయి))
                ప్రదేశం_మూల్యం += 폭*పొడవు_మూల్యం
            if ప్రదేశం_మూల్యం:
                assert ప్రదేశం_మూల్యం == 너비*높이, ప్రదేశం_మూల్యం
                return రేఖాచిత్రణ_మూల్యం

    def తనిఖీ_పెల్(సమన్వయపరుచు_మూల్యం, 색):
        마감 = time.monotonic()+10
        while True:
            రేఖాచిత్రణ_మూల్యం = బిట్_మ్యాప్_చిత్రం()
            if రేఖాచిత్రణ_మూల్యం.getpixel(సమన్వయపరుచు_మూల్యం) == 색: return రేఖాచిత్రణ_మూల్యం
            if time.monotonic() > 마감: raise AssertionError((సమన్వయపరుచు_మూల్యం, రేఖాచిత్రణ_మూల్యం.getpixel(సమన్వయపరుచు_మూల్యం), 색))

    def అప్_లోడ్_ఫైల్_లు(పేరు, డేటా): బదిలీ_మూల్యం.storbinary('STOR '+పేరు, io.BytesIO(డేటా))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+పరిమాణం_మార్చు_పాఠం+' RGB32').encode() in లాగ్_వరుస
        print('BOOT:', పరిమాణం_మార్చు_పాఠం, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', లాగ్_వరుస).group(1))
        రిమోట్_మూల్యం = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(రిమోట్_మూల్యం, 12) == b'RFB 003.008\n'; రిమోట్_మూల్యం.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(రిమోట్_మూల్యం, 정확한값(రిమోట్_మూల్యం, 1)[0]); రిమోట్_మూల్యం.sendall(b'\x01')
        assert 정확한값(రిమోట్_మూల్యం, 4) == b'\0'*4; రిమోట్_మూల్యం.sendall(b'\x01')
        초기 = 정확한값(రిమోట్_మూల్యం, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(రిమోట్_మూల్యం, struct.unpack('>I', 초기[20:])[0])
        రిమోట్_మూల్యం.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        రిమోట్_మూల్యం.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        తనిఖీ_పెల్((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for ఈవెంట్,_ in సెలక్టర్_a916db4e.select(.02):
                    డేటా=ఈవెంట్.fileobj.read(65536)
                    if డేటా:లాగ్_వరుస.extend(డేటా)
        విండో=[12,48,568,360]
        def సరిచూడు_పరిమాణం_మార్చు():
            కాలమ్_మూల్యం,వరుస_మూల్యం=(విండో[2]-24)//8,(విండో[3]-56)//16
            పాఠ్యము=షెల్('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(కాలమ్_మూల్యం,వరుస_మూల్యం) in పాఠ్యము,పాఠ్యము
            # వాస్తవ_డేటా విండో 테두리: 단지 పరిమాణం ప్రశ్న_మూల్యం 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            తనిఖీ_పెల్((విండో[0],విండో[1]),(32,80,144))
            రేఖాచిత్రణ_మూల్యం=తనిఖీ_పెల్((విండో[0]+విండో[2]-1,విండో[1]+విండో[3]-1),(39,49,64))
            return రేఖాచిత్రణ_మూల్యం
        def 모서리(방향):
            return (విండో[0]+(3 if 방향 in (1,3) else విండో[2]-4),విండో[1]+(3 if 방향<=2 else విండో[3]-4))
        def పరిమాణం_మార్చు_లాగు(방향,차이,బటన్=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            తనిఖీ_పెల్(흰점,(255,255,255))
            가리키기(가,세,బటన్)
            끝가=max(0,min(너비-1,가+차이[0]));ముగించు_నిలువు=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,ముగించు_నిలువు,బటన్);가리키기(끝가,ముగించు_నిలువు,0);숨고르기()
            if బటన్==1:
                왼,위,폭,పొడవు_మూల్యం=విండో;오른,아래=왼+폭,위+పొడవు_మూల్యం
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+ముగించు_నిలువు-세))
                else:아래=max(위+216,min(높이,아래+ముగించు_నిలువు-세))
                విండో[:]=[왼,위,오른-왼,아래-위]
        సరిచూడు_పరిమాణం_మార్చు();assert పాయింటర్_అదృశ్య[0]
        పరిమాణం_మార్చు_లాగు(4,(-100,-60),4);సరిచూడు_పరిమాణం_మార్చు() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            పరిమాణం_మార్చు_లాగు(방향,차이);సరిచూడు_పరిమాణం_మార్చు()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_పంపు("echo '"+긴글+"'");숨고르기()
        పరిమాణం_మార్చు_లాగు(4,(-1000,-1000));assert విండో[2:]==[360,216]
        పరిమాణం_మార్చు_లాగు(4,(너비,높이))
        నడుపుము=SMS_పంపు('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),నడుపుము);సరిచూడు_పరిమాణం_మార్చు()
        # vi가 సంకలనంచేయు_మూల్యం 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        షెల్('ftpd start')
        బదిలీ_మూల్యం=ftplib.FTP();బదిలీ_మూల్యం.encoding='utf-8';బదిలీ_మూల్యం.connect('127.0.0.1',పోర్ట్_సంఖ్య,timeout=20);బదిలీ_మూల్యం.login()
        기다리기(b'NORMAL',SMS_పంపు('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_పంపు('i미저장 한글 డేటా\n'));숨고르기()
        పరిమాణం_మార్చు_లాగు(4,(-너비,-높이))
        # ANSI వరుస_మూల్యం 이동에 새 వరుస_మూల్యం 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((విండో[3]-56)//16)).encode() in లాగ్_వరుస[-4096:]
        SMS_పంపు('작은 창에서도 이어 వ్రాయుము\n');숨고르기()
        పరిమాణం_మార్చు_లాగు(4,(너비,높이))
        SMS_పంపు('큰 창에서도 이어 వ్రాయుము\n');숨고르기()
        క్లిక్_చెయండి_బటన్(0xff1b);క్లిక్_చెయండి_బటన్(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_పంపు(':wq\n'))
        విషయం_మూల్యం=bytearray();బదిలీ_మూల్యం.retrbinary('RETR 크기자료.txt',విషయం_మూల్యం.extend)
        assert విషయం_మూల్యం=='미저장 한글 డేటా\n작은 창에서도 이어 వ్రాయుము\n큰 창에서도 이어 వ్రాయుము\n'.encode(),విషయం_మూల్యం
        సరిచూడు_పరిమాణం_మార్చు().save(str(ప్రమాణం_పథం/(పరిమాణం_మార్చు_పాఠం+'-large.png')))
        # 두 번째 창은 స్వయంసిద్ధ_విలువ పరిమాణం, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        నడుపుము=len(లాగ్_వరుస);క్లిక్_చెయండి_మూల్యం(70,16);기다리기(b'TERMINAL FOCUS 2',నడుపుము)
        assert 'TERMINAL SIZE 68x19' in షెల్('terminal size')
        నడుపుము=len(లాగ్_వరుస);క్లిక్_చెయండి_మూల్యం(180,16);기다리기(b'TERMINAL FOCUS 1',నడుపుము);సరిచూడు_పరిమాణం_మార్చు()
        పరిమాణం_మార్చు_లాగు(4,(-너비,-높이));సరిచూడు_పరిమాణం_మార్చు().save(str(ప్రమాణం_పథం/(పరిమాణం_మార్చు_పాఠం+'-small.png')))
        # పరిమాణం మార్చు_మూల్యం వెనుకకు_మూల్యం X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        నడుపుము=len(లాగ్_వరుస);క్లిక్_చెయండి_మూల్యం(విండో[0]+విండో[2]-20,విండో[1]+15);기다리기(b'TERMINAL FOCUS 2',నడుపుము)
        assert 'RESIZE CLOSED' in షెల్('echo RESIZE CLOSED')
        print('PASS:',పరిమాణం_మార్చు_పాఠం,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if బదిలీ_మూల్యం:బదిలీ_మూల్యం.close()
        if రిమోట్_మూల్యం:రిమోట్_మూల్యం.close()
        if విధానం_మూల్యం.poll() is None:
            విధానం_మూల్యం.terminate()
            try:విధానం_మూల్యం.wait(timeout=8)
            except subprocess.TimeoutExpired:విధానం_మూల్యం.kill();విధానం_మూల్యం.wait()
        సెలక్టర్_a916db4e.close();విధానం_మూల్యం.stdout.close();(ప్రమాణం_పథం/(పరిమాణం_మార్చు_పాఠం+'.log')).write_bytes(లాగ్_వరుస)


def నడుపుము():
    ప్రమాణం_పథం=ప్రొజెక్ట్_మూలం/'build/verification/resize';ప్రమాణం_పథం.mkdir(parents=True,exist_ok=True)
    లాగ్_వరుస={'passed':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,ప్రమాణం_పథం);లాగ్_వరుస['resolutions'].append([너비,높이])
        లాగ్_వరుస.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(ప్రమాణం_పథం/'report.json').write_text(json.dumps(లాగ్_వరుస,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':నడుపుము()
