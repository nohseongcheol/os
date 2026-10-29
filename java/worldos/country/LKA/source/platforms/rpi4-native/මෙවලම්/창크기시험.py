#!/usr/bin/env python3
"""තථ්_ය_දත්ත QEMU/VNC에서 අග්_රය 모서리 ඇදගෙන_ඒම_අගය·පොයින්ටරය·동적 අනුලකුණ_අගය විවරය_පිවිසුම·සකසන්න_අගය අන්තර්ගතය_අගය 보존를 검사한다."""
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
from වැඩතලය_දසුන import 정확한값
from ක්_රියාත්මක_කරන්න_විධානය import 기준


def 창크기시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ප්_රමාණනය_පෙළ = '{}x{}'.format(너비, 높이)
    ක්_රියාවලිය_අගය = subprocess.Popen(['python3', str(기준/'මෙවලම්/ක්_රියාත්මක_කරන්න_විධානය.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ප්_රමාණනය_පෙළ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    වරකය_a916db4e = selectors.DefaultSelector(); වරකය_a916db4e.register(ක්_රියාවලිය_අගය.stdout, selectors.EVENT_READ)
    ලොගය_පේළිය = bytearray(); දුරස්ථ_අගය = None; මාරුව_අගය = None; පොයින්ටරය_සැඟවුණු=[False]

    def 기다리기(දර්ශනය_අගය, ක්_රියාත්මක_කරන්න_2=0):
        마감 = time.monotonic() + 60
        while දර්ශනය_අගය not in ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:]:
            if time.monotonic() > 마감 or ක්_රියාවලිය_අගය.poll() is not None or b'HALTED' in ලොගය_පේළිය or b'PANIC:' in ලොගය_පේළිය:
                raise AssertionError(ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:].decode('utf-8', 'replace'))
            for සිදුවීම, _ in වරකය_a916db4e.select(.1):
                දත්ත = සිදුවීම.fileobj.read(65536)
                if දත්ත: ලොගය_පේළිය.extend(දත්ත)
        return ලොගය_පේළිය[ක්_රියාත්මක_කරන්න_2:].decode('utf-8', 'replace')

    def ක්ලික්_කරන්න_බොත්තම(සංකේතය, 눌림=True): දුරස්ථ_අගය.sendall(struct.pack('>BBHI', 4, int(눌림), 0, සංකේතය))

    def SMS_යවන්න(පෙළ):
        ක්_රියාත්මක_කරන්න_2 = len(ලොගය_පේළිය)
        for අනුලකුණ_අගය in පෙළ:
            සංකේතය = 0xff0d if අනුලකුණ_අගය == '\n' else ord(අනුලකුණ_අගය) if ord(අනුලකුණ_අගය) < 256 else 0x1000000 | ord(අනුලකුණ_අගය)
            ක්ලික්_කරන්න_බොත්තම(සංකේතය); ක්ලික්_කරන්න_බොත්තම(සංකේතය, False)
        return ක්_රියාත්මක_කරන්න_2

    def කවචය(පෙළ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', SMS_යවන්න(පෙළ+'; echo __RESIZE_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): දුරස්ථ_අගය.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ක්ලික්_කරන්න_අගය(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def බිටු_සිතියම_අනුරුව():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 තථ්_ය_දත්ත 너비를 쓴다.
        දුරස්ථ_අගය.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        චිත්_රය_අගය = Image.new('RGB', (너비, 높이)); ප්_රදේශය_අගය = 0
        while True:
            종류 = 정확한값(දුරස්ථ_අගය, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                දිග_අගය = struct.unpack('>I', 정확한값(දුරස්ථ_අගය, 7)[3:])[0]; 정확한값(දුරස්ථ_අගය, දිග_අගය); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(දුරස්ථ_අගය, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, දිග_අගය, සංකේතනය_අගය = struct.unpack('>HHHHi', 정확한값(දුරස්ථ_අගය, 12))
                if සංකේතනය_අගය == -239:
                    assert 폭==0 and දිග_අගය==0, 'remote cursor must be hidden'
                    පොයින්ටරය_සැඟවුණු[0]=True
                    continue
                assert සංකේතනය_අගය == 0 and 가로+폭 <= 너비 and 세로+දිග_අගය <= 높이
                චිත්_රය_අගය.paste(Image.frombytes('RGB', (폭, දිග_අගය), 정확한값(දුරස්ථ_අගය, 폭*දිග_අගය*4), 'raw', 'BGRX'), (가로, 세로))
                ප්_රදේශය_අගය += 폭*දිග_අගය
            if ප්_රදේශය_අගය:
                assert ප්_රදේශය_අගය == 너비*높이, ප්_රදේශය_අගය
                return චිත්_රය_අගය

    def චෙක්පත_පික්සලය(ඛණ්ඩාංක_අගය, 색):
        마감 = time.monotonic()+10
        while True:
            චිත්_රය_අගය = බිටු_සිතියම_අනුරුව()
            if චිත්_රය_අගය.getpixel(ඛණ්ඩාංක_අගය) == 색: return චිත්_රය_අගය
            if time.monotonic() > 마감: raise AssertionError((ඛණ්ඩාංක_අගය, චිත්_රය_අගය.getpixel(ඛණ්ඩාංක_අගය), 색))

    def උඩුගත_කරන්න_ගොනු(නම, දත්ත): මාරුව_අගය.storbinary('STOR '+නම, io.BytesIO(දත්ත))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ප්_රමාණනය_පෙළ+' RGB32').encode() in ලොගය_පේළිය
        print('BOOT:', ප්_රමාණනය_පෙළ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ලොගය_පේළිය).group(1))
        දුරස්ථ_අගය = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(දුරස්ථ_අගය, 12) == b'RFB 003.008\n'; දුරස්ථ_අගය.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(දුරස්ථ_අගය, 정확한값(දුරස්ථ_අගය, 1)[0]); දුරස්ථ_අගය.sendall(b'\x01')
        assert 정확한값(දුරස්ථ_අගය, 4) == b'\0'*4; දුරස්ථ_අගය.sendall(b'\x01')
        초기 = 정확한값(දුරස්ථ_අගය, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(දුරස්ථ_අගය, struct.unpack('>I', 초기[20:])[0])
        දුරස්ථ_අගය.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        දුරස්ථ_අගය.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        චෙක්පත_පික්සලය((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for සිදුවීම,_ in වරකය_a916db4e.select(.02):
                    දත්ත=සිදුවීම.fileobj.read(65536)
                    if දත්ත:ලොගය_පේළිය.extend(දත්ත)
        කවුළුව=[12,48,568,360]
        def තහවුරු_කරන්න_ප්_රමාණනය():
            තීරුව_අගය,පේළිය_අගය=(කවුළුව[2]-24)//8,(කවුළුව[3]-56)//16
            පෙළ=කවචය('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(තීරුව_අගය,පේළිය_අගය) in පෙළ,පෙළ
            # තථ්_ය_දත්ත කවුළුව 테두리: 단지 ප්_රමාණය විමසුම_අගය 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            චෙක්පත_පික්සලය((කවුළුව[0],කවුළුව[1]),(32,80,144))
            චිත්_රය_අගය=චෙක්පත_පික්සලය((කවුළුව[0]+කවුළුව[2]-1,කවුළුව[1]+කවුළුව[3]-1),(39,49,64))
            return චිත්_රය_අගය
        def 모서리(방향):
            return (කවුළුව[0]+(3 if 방향 in (1,3) else කවුළුව[2]-4),කවුළුව[1]+(3 if 방향<=2 else කවුළුව[3]-4))
        def ප්_රතිප්_රමාණ_කරන්න_ඇදගෙන_ඒම(방향,차이,බොත්තම=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            චෙක්පත_පික්සලය(흰점,(255,255,255))
            가리키기(가,세,බොත්තම)
            끝가=max(0,min(너비-1,가+차이[0]));නිමා_කරන්න_සිරස්=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,නිමා_කරන්න_සිරස්,බොත්තම);가리키기(끝가,නිමා_කරන්න_සිරස්,0);숨고르기()
            if බොත්තම==1:
                왼,위,폭,දිග_අගය=කවුළුව;오른,아래=왼+폭,위+දිග_අගය
                if 방향 in (1,3):왼=max(0,min(오른-360,왼+끝가-가))
                else:오른=max(왼+360,min(너비,오른+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+නිමා_කරන්න_සිරස්-세))
                else:아래=max(위+216,min(높이,아래+නිමා_කරන්න_සිරස්-세))
                කවුළුව[:]=[왼,위,오른-왼,아래-위]
        තහවුරු_කරන්න_ප්_රමාණනය();assert පොයින්ටරය_සැඟවුණු[0]
        ප්_රතිප්_රමාණ_කරන්න_ඇදගෙන_ඒම(4,(-100,-60),4);තහවුරු_කරන්න_ප්_රමාණනය() # 오른쪽 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ප්_රතිප්_රමාණ_කරන්න_ඇදගෙන_ඒම(방향,차이);තහවුරු_කරන්න_ප්_රමාණනය()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        SMS_යවන්න("echo '"+긴글+"'");숨고르기()
        ප්_රතිප්_රමාණ_කරන්න_ඇදගෙන_ඒම(4,(-1000,-1000));assert කවුළුව[2:]==[360,216]
        ප්_රතිප්_රමාණ_කරන්න_ඇදගෙන_ඒම(4,(너비,높이))
        ක්_රියාත්මක_කරන්න_2=SMS_යවන්න('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),ක්_රියාත්මක_කරන්න_2);තහවුරු_කරන්න_ප්_රමාණනය()
        # vi가 සකසන්න_අගය 중에 화면 크기를 다시 읽고, 저장하지 않은 한글도 유지한다.
        කවචය('ftpd start')
        මාරුව_අගය=ftplib.FTP();මාරුව_අගය.encoding='utf-8';මාරුව_අගය.connect('127.0.0.1',접속번호,timeout=20);මාරුව_අගය.login()
        기다리기(b'NORMAL',SMS_යවන්න('vi /크기자료.txt\n'))
        기다리기(b'INSERT',SMS_යවන්න('i미저장 한글 දත්ත\n'));숨고르기()
        ප්_රතිප්_රමාණ_කරන්න_ඇදගෙන_ඒම(4,(-너비,-높이))
        # ANSI පේළිය_අගය 이동에 새 පේළිය_අගය 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((කවුළුව[3]-56)//16)).encode() in ලොගය_පේළිය[-4096:]
        SMS_යවන්න('작은 창에서도 이어 ලිවීම\n');숨고르기()
        ප්_රතිප්_රමාණ_කරන්න_ඇදගෙන_ඒම(4,(너비,높이))
        SMS_යවන්න('큰 창에서도 이어 ලිවීම\n');숨고르기()
        ක්ලික්_කරන්න_බොත්තම(0xff1b);ක්ලික්_කරන්න_බොත්තම(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',SMS_යවන්න(':wq\n'))
        අන්තර්ගතය_අගය=bytearray();මාරුව_අගය.retrbinary('RETR 크기자료.txt',අන්තර්ගතය_අගය.extend)
        assert අන්තර්ගතය_අගය=='미저장 한글 දත්ත\n작은 창에서도 이어 ලිවීම\n큰 창에서도 이어 ලිවීම\n'.encode(),අන්තර්ගතය_අගය
        තහවුරු_කරන්න_ප්_රමාණනය().save(str(결과경로/(ප්_රමාණනය_පෙළ+'-large.png')))
        # 두 번째 창은 පෙරනිමි_අගය ප්_රමාණය, 다시 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        ක්_රියාත්මක_කරන්න_2=len(ලොගය_පේළිය);ක්ලික්_කරන්න_අගය(70,16);기다리기(b'TERMINAL FOCUS 2',ක්_රියාත්මක_කරන්න_2)
        assert 'TERMINAL SIZE 68x19' in කවචය('terminal size')
        ක්_රියාත්මක_කරන්න_2=len(ලොගය_පේළිය);ක්ලික්_කරන්න_අගය(180,16);기다리기(b'TERMINAL FOCUS 1',ක්_රියාත්මක_කරන්න_2);තහවුරු_කරන්න_ප්_රමාණනය()
        ප්_රතිප්_රමාණ_කරන්න_ඇදගෙන_ඒම(4,(-너비,-높이));තහවුරු_කරන්න_ප්_රමාණනය().save(str(결과경로/(ප්_රමාණනය_පෙළ+'-small.png')))
        # ප්_රමාණය වෙනස්_කරන්න_අගය ආපසු_අගය X 닫기도 새로운 오른쪽 가장자리를 사용한다.
        ක්_රියාත්මක_කරන්න_2=len(ලොගය_පේළිය);ක්ලික්_කරන්න_අගය(කවුළුව[0]+කවුළුව[2]-20,කවුළුව[1]+15);기다리기(b'TERMINAL FOCUS 2',ක්_රියාත්මක_කරන්න_2)
        assert 'RESIZE CLOSED' in කවචය('echo RESIZE CLOSED')
        print('PASS:',ප්_රමාණනය_පෙළ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if මාරුව_අගය:මාරුව_අගය.close()
        if දුරස්ථ_අගය:දුරස්ථ_අගය.close()
        if ක්_රියාවලිය_අගය.poll() is None:
            ක්_රියාවලිය_අගය.terminate()
            try:ක්_රියාවලිය_අගය.wait(timeout=8)
            except subprocess.TimeoutExpired:ක්_රියාවලිය_අගය.kill();ක්_රියාවලිය_අගය.wait()
        වරකය_a916db4e.close();ක්_රියාවලිය_අගය.stdout.close();(결과경로/(ප්_රමාණනය_පෙළ+'.log')).write_bytes(ලොගය_පේළිය)


def ක්_රියාත්මක_කරන්න_2():
    결과경로=기준/'build/verification/resize';결과경로.mkdir(parents=True,exist_ok=True)
    ලොගය_පේළිය={'passed':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,결과경로);ලොගය_පේළිය['resolutions'].append([너비,높이])
        ලොගය_පේළිය.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(결과경로/'report.json').write_text(json.dumps(ලොගය_පේළිය,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':ක්_රියාත්මක_කරන්න_2()
