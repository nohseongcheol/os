#!/usr/bin/env python3
"""gangan_détà QEMU/VNC에서 화면 Ìwọ̀n·경계·wínńdò gbé_iye·Swing·언어별 그리기를 검사한다."""
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
from àtẹ_iṣẹ́_wo import 정확한값
from ṣiṣẹ́_àṣẹ import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ìwọn_SMS = '{}x{}'.format(너비, 높이)
    Ìlànà_iye = subprocess.Popen(['python3', str(기준/'Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ìwọn_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    olùyàn_a916db4e = selectors.DefaultSelector(); olùyàn_a916db4e.register(Ìlànà_iye.stdout, selectors.EVENT_READ)
    àkọsílẹ̀_ìṣe_ìlà_ìbú = bytearray(); Ìjìnnà_iye = None; ṣàgbélọ_iye = None

    def 기다리기(ṣàfihàn_iye, Rọ́ọ̀nù=0):
        마감 = time.monotonic() + 60
        while ṣàfihàn_iye not in àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:]:
            if time.monotonic() > 마감 or Ìlànà_iye.poll() is not None or b'HALTED' in àkọsílẹ̀_ìṣe_ìlà_ìbú or b'PANIC:' in àkọsílẹ̀_ìṣe_ìlà_ìbú:
                raise AssertionError(àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:].decode('utf-8', 'replace'))
            for ìgbéṣẹ̀, _ in olùyàn_a916db4e.select(.1):
                détà = ìgbéṣẹ̀.fileobj.read(65536)
                if détà: àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(détà)
        return àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:].decode('utf-8', 'replace')

    def ṣíra_tẹ_bọ́tìnnì(àmì, 눌림=True): Ìjìnnà_iye.sendall(struct.pack('>BBHI', 4, int(눌림), 0, àmì))

    def fi_SMS_ránṣẹ́(SMS):
        Rọ́ọ̀nù = len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
        for ẹyọ_ọ̀rọ̀_iye in SMS:
            àmì = 0xff0d if ẹyọ_ọ̀rọ̀_iye == '\n' else ord(ẹyọ_ọ̀rọ̀_iye) if ord(ẹyọ_ọ̀rọ̀_iye) < 256 else 0x1000000 | ord(ẹyọ_ọ̀rọ̀_iye)
            ṣíra_tẹ_bọ́tìnnì(àmì); ṣíra_tẹ_bọ́tìnnì(àmì, False)
        return Rọ́ọ̀nù

    def ṣẹ́ẹ̀lì(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', fi_SMS_ránṣẹ́(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): Ìjìnnà_iye.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def ṣíra_tẹ_iye(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def bitmap_àwòrán():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 gangan_détà 너비를 쓴다.
        Ìjìnnà_iye.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        íyàwòrán_iye = Image.new('RGB', (너비, 높이)); ìsọ̀rí_iye_9285603e = 0
        while True:
            종류 = 정확한값(Ìjìnnà_iye, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                gígùn_iye = struct.unpack('>I', 정확한값(Ìjìnnà_iye, 7)[3:])[0]; 정확한값(Ìjìnnà_iye, gígùn_iye); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(Ìjìnnà_iye, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, gígùn_iye, pípàrokò_iye = struct.unpack('>HHHHi', 정확한값(Ìjìnnà_iye, 12))
                assert pípàrokò_iye == 0 and 가로+폭 <= 너비 and 세로+gígùn_iye <= 높이
                íyàwòrán_iye.paste(Image.frombytes('RGB', (폭, gígùn_iye), 정확한값(Ìjìnnà_iye, 폭*gígùn_iye*4), 'raw', 'BGRX'), (가로, 세로))
                ìsọ̀rí_iye_9285603e += 폭*gígùn_iye
            if ìsọ̀rí_iye_9285603e:
                assert ìsọ̀rí_iye_9285603e == 너비*높이, ìsọ̀rí_iye_9285603e
                return íyàwòrán_iye

    def ṣàyẹ̀wò_píkísẹ̀(ibi_ìtọ́kasí_iye, 색):
        마감 = time.monotonic()+10
        while True:
            íyàwòrán_iye = bitmap_àwòrán()
            if íyàwòrán_iye.getpixel(ibi_ìtọ́kasí_iye) == 색: return íyàwòrán_iye
            if time.monotonic() > 마감: raise AssertionError((ibi_ìtọ́kasí_iye, íyàwòrán_iye.getpixel(ibi_ìtọ́kasí_iye), 색))

    def fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì(Orúkọ, détà): ṣàgbélọ_iye.storbinary('STOR '+Orúkọ, io.BytesIO(détà))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ìwọn_SMS+' RGB32').encode() in àkọsílẹ̀_ìṣe_ìlà_ìbú
        print('BOOT:', ìwọn_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', àkọsílẹ̀_ìṣe_ìlà_ìbú).group(1))
        Ìjìnnà_iye = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(Ìjìnnà_iye, 12) == b'RFB 003.008\n'; Ìjìnnà_iye.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(Ìjìnnà_iye, 정확한값(Ìjìnnà_iye, 1)[0]); Ìjìnnà_iye.sendall(b'\x01')
        assert 정확한값(Ìjìnnà_iye, 4) == b'\0'*4; Ìjìnnà_iye.sendall(b'\x01')
        초기 = 정확한값(Ìjìnnà_iye, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(Ìjìnnà_iye, struct.unpack('>I', 초기[20:])[0])
        Ìjìnnà_iye.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        Ìjìnnà_iye.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ṣàyẹ̀wò_píkísẹ̀((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ṣàyẹ̀wò_píkísẹ̀((너비-568, 높이-360), (32, 80, 144))
        Rọ́ọ̀nù = len(àkọsílẹ̀_ìṣe_ìlà_ìbú); ṣíra_tẹ_iye(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Rọ́ọ̀nù)
        ṣàyẹ̀wò_píkísẹ̀((너비-568, 높이-360), (24, 32, 48))
        Rọ́ọ̀nù = len(àkọsílẹ̀_ìṣe_ìlà_ìbú); ṣíra_tẹ_iye(80, 16); 기다리기(b'TERMINAL FOCUS 1', Rọ́ọ̀nù)
        ṣẹ́ẹ̀lì('ftpd start')
        ṣàgbélọ_iye = ftplib.FTP(); ṣàgbélọ_iye.encoding = 'utf-8'; ṣàgbélọ_iye.connect('127.0.0.1', 접속번호, timeout=20); ṣàgbélọ_iye.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ní_ṣókí 밖·빈 사각형을 포함한다.
        orísun = '''#include <화면규약.h>
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
    kọ_fáìlì_détà(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('화면시험.c', orísun.encode())
        assert 'exit 0' in ṣẹ́ẹ̀lì('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', fi_SMS_ránṣẹ́('run /화면시험\n'))
        ṣàyẹ̀wò_píkísẹ̀((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', fi_SMS_ránṣẹ́('q'))
        orísun = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, ètò_àṣìṣe
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ètò_àṣìṣe as àṣìṣe:
    assert àṣìṣe.wá_atọ̀ka_àkóónú == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('화면시험.py', orísun.encode())
        기다리기(b'PYTHON RESOLUTION PASS', fi_SMS_ránṣẹ́('python /화면시험.py\n'))
        ṣàyẹ̀wò_píkísẹ̀((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', fi_SMS_ránṣẹ́('q'))
        orísun = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("Ìwọ̀n");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("ní_ṣókí"); }
        catch (잘못된인수예외 àṣìṣe) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 olùpèsè javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(orísun.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', fi_SMS_ránṣẹ́('java 해상도경계시험\n'))
        ṣàyẹ̀wò_píkísẹ̀((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', fi_SMS_ránṣẹ́('q'))
        # 게스트 javac의 àtìlẹ́yìn_iye 문법으로 Ìwọ̀n aṣèbéèré_iye·지우기·다섯 인수 그리기를 컴파일한다.
        orísun = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.kọ_ìlà("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('해상도시험.java', orísun.encode())
        결과 = ṣẹ́ẹ̀lì('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', fi_SMS_ránṣẹ́('java 해상도시험\n'))
        ṣàyẹ̀wò_píkísẹ̀((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', fi_SMS_ránṣẹ́('q'))
        fífi_ẹ̀dà_fáìlì_ṣọwọ́_Àwọn_fáìlì('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', fi_SMS_ránṣẹ́('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        íyàwòrán_iye = ṣàyẹ̀wò_píkísẹ̀((가로, 세로), (32, 80, 144))
        íyàwòrán_iye.save(str(결과경로/(ìwọn_SMS+'.png')))
        Rọ́ọ̀nù = len(àkọsílẹ̀_ìṣe_ìlà_ìbú); ṣíra_tẹ_iye(가로+80, 세로+155)
        기다리기('SWING CLICK Orúkọ'.encode(), Rọ́ọ̀nù)
        Rọ́ọ̀nù = len(àkọsílẹ̀_ìṣe_ìlà_ìbú); ṣíra_tẹ_iye(가로+385, 세로+15); 기다리기(b'jkoros-native> ', Rọ́ọ̀nù)
        assert 'AFTER_RESOLUTION' in ṣẹ́ẹ̀lì('echo AFTER_RESOLUTION')
        print('PASS:', ìwọn_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ṣàgbélọ_iye: ṣàgbélọ_iye.close()
        if Ìjìnnà_iye: Ìjìnnà_iye.close()
        if Ìlànà_iye.poll() is None:
            Ìlànà_iye.terminate()
            try: Ìlànà_iye.wait(timeout=8)
            except subprocess.TimeoutExpired: Ìlànà_iye.kill(); Ìlànà_iye.wait()
        olùyàn_a916db4e.close(); Ìlànà_iye.stdout.close()
        (결과경로/(ìwọn_SMS+'.log')).write_bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú)


def Rọ́ọ̀nù():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    àkọsílẹ̀_ìṣe_ìlà_ìbú = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for aláìbẹgbẹmu_iye in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Àwọn_irinṣẹ́/ṣiṣẹ́_àṣẹ.py'), '--resolution', aláìbẹgbẹmu_iye], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); àkọsílẹ̀_ìṣe_ìlà_ìbú['resolutions'].append([너비, 높이])
        àkọsílẹ̀_ìṣe_ìlà_ìbú.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(àkọsílẹ̀_ìṣe_ìlà_ìbú, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Rọ́ọ̀nù()
