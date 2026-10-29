#!/usr/bin/env python3
"""eyona_yenzekileyo_iingcombolo QEMU/VNC에서 화면 Ubukhulu·경계·i_window fudusa_ixabiso·Swing·언어별 그리기를 검사한다."""
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


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    isayizi_I_SMS = '{}x{}'.format(너비, 높이)
    Inkqubo_ixabiso = subprocess.Popen(['python3', str(기준/'Izixhobo/ukwenza_umyalelo.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', isayizi_I_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    umkhethi_a916db4e = selectors.DefaultSelector(); umkhethi_a916db4e.register(Inkqubo_ixabiso.stdout, selectors.EVENT_READ)
    ilog_umqolo = bytearray(); kude_ixabiso = None; gqithisela_ixabiso = None

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

    def isiniki_myalelo(Umbhalo): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', thumela_i_SMS(Umbhalo+'; echo __RESOLUTION_DONE__\n'))

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
        kude_ixabiso.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        jonga_i_pel((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        jonga_i_pel((너비-568, 높이-360), (32, 80, 144))
        Phumeza = len(ilog_umqolo); cofa_ixabiso(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Phumeza)
        jonga_i_pel((너비-568, 높이-360), (24, 32, 48))
        Phumeza = len(ilog_umqolo); cofa_ixabiso(80, 16); 기다리기(b'TERMINAL FOCUS 1', Phumeza)
        isiniki_myalelo('ftpd start')
        gqithisela_ixabiso = ftplib.FTP(); gqithisela_ixabiso.encoding = 'utf-8'; gqithisela_ixabiso.connect('127.0.0.1', 접속번호, timeout=20); gqithisela_ixabiso.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ikliphu 밖·빈 사각형을 포함한다.
        UMTHOMBO = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(네모그리기(너비,높이,0,0,0)) return 2;
    if(네모그리기(너비,높이-1,1,1,0)!=-22) return 3;
    if(네모그리기(너비-1,높이,1,1,0)!=-22) return 4;
    if(네모그리기(-1,0,1,1,0)!=-22) return 5;
    if(네모그리기(0,0,-1,1,0)!=-22) return 6;
    if(네모그리기(너비-1,높이-1,1,1,0x332211)) return 7;
    bhala_ifayile_iingcombolo(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        layisha_Iifayile('화면시험.c', UMTHOMBO.encode())
        assert 'exit 0' in isiniki_myalelo('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', thumela_i_SMS('run /화면시험\n'))
        jonga_i_pel((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', thumela_i_SMS('q'))
        UMTHOMBO = '''from isiXhosa import 화면크기, 네모그리기, 그림기다리기, 출력, inkqubo_impazamo
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except inkqubo_impazamo as Impazamo:
    assert Impazamo.indeksa == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        layisha_Iifayile('화면시험.py', UMTHOMBO.encode())
        기다리기(b'PYTHON RESOLUTION PASS', thumela_i_SMS('python /화면시험.py\n'))
        jonga_i_pel((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', thumela_i_SMS('q'))
        UMTHOMBO = '''import isiXhosa.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Ubukhulu");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ikliphu"); }
        catch (잘못된인수예외 Impazamo) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 umsingathi javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(UMTHOMBO.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        layisha_Iifayile('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', thumela_i_SMS('java 해상도경계시험\n'))
        jonga_i_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', thumela_i_SMS('q'))
        # 게스트 javac의 inkxaso_ixabiso 문법으로 Ubukhulu umbuzo_ixabiso·지우기·다섯 인수 그리기를 컴파일한다.
        UMTHOMBO = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=isiXhosa.자체.화면.너비();
        int 높이=isiXhosa.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        isiXhosa.자체.화면.지우기(3153944);
        isiXhosa.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        isiXhosa.자체.출력.bhala_umgca("JAVA RESOLUTION PASS");
        isiXhosa.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        layisha_Iifayile('해상도시험.java', UMTHOMBO.encode())
        결과 = isiniki_myalelo('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', thumela_i_SMS('java 해상도시험\n'))
        jonga_i_pel((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', thumela_i_SMS('q'))
        layisha_Iifayile('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', thumela_i_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        umzobo_ixabiso = jonga_i_pel((가로, 세로), (32, 80, 144))
        umzobo_ixabiso.save(str(결과경로/(isayizi_I_SMS+'.png')))
        Phumeza = len(ilog_umqolo); cofa_ixabiso(가로+80, 세로+155)
        기다리기('SWING CLICK Igama'.encode(), Phumeza)
        Phumeza = len(ilog_umqolo); cofa_ixabiso(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Phumeza)
        assert 'AFTER_RESOLUTION' in isiniki_myalelo('echo AFTER_RESOLUTION')
        print('PASS:', isayizi_I_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if gqithisela_ixabiso: gqithisela_ixabiso.close()
        if kude_ixabiso: kude_ixabiso.close()
        if Inkqubo_ixabiso.poll() is None:
            Inkqubo_ixabiso.terminate()
            try: Inkqubo_ixabiso.wait(timeout=8)
            except subprocess.TimeoutExpired: Inkqubo_ixabiso.kill(); Inkqubo_ixabiso.wait()
        umkhethi_a916db4e.close(); Inkqubo_ixabiso.stdout.close()
        (결과경로/(isayizi_I_SMS+'.log')).write_bytes(ilog_umqolo)


def Phumeza():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    ilog_umqolo = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ayisebenzi_ixabiso in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Izixhobo/ukwenza_umyalelo.py'), '--resolution', ayisebenzi_ixabiso], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); ilog_umqolo['resolutions'].append([너비, 높이])
        ilog_umqolo.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(ilog_umqolo, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Phumeza()
