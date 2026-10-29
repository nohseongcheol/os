#!/usr/bin/env python3
"""стваран_подаци QEMU/VNC에서 화면 подесити_величину·경계·прозор помаћи_вриједност·Swing·언어별 그리기를 검사한다."""
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
from радна_површина_поглед import 정확한값
from 실행 import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    подесити_величину_текст = '{}x{}'.format(너비, 높이)
    процес_вриједност = subprocess.Popen(['python3', str(기준/'도구/실행.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', подесити_величину_текст], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    선택기 = selectors.DefaultSelector(); 선택기.register(процес_вриједност.stdout, selectors.EVENT_READ)
    дневник_рада_ред = bytearray(); удаљено_вриједност = None; пријенос_вриједност = None

    def 기다리기(приказати_вриједност, 시작=0):
        마감 = time.monotonic() + 60
        while приказати_вриједност not in дневник_рада_ред[시작:]:
            if time.monotonic() > 마감 or процес_вриједност.poll() is not None or b'HALTED' in дневник_рада_ред or b'PANIC:' in дневник_рада_ред:
                raise AssertionError(дневник_рада_ред[시작:].decode('utf-8', 'replace'))
            for догађај, _ in 선택기.select(.1):
                подаци = догађај.fileobj.read(65536)
                if подаци: дневник_рада_ред.extend(подаци)
        return дневник_рада_ред[시작:].decode('utf-8', 'replace')

    def кликнути_дугме(기호, 눌림=True): удаљено_вриједност.sendall(struct.pack('>BBHI', 4, int(눌림), 0, 기호))

    def послати_текст(текст):
        시작 = len(дневник_рада_ред)
        for знак_вриједност in текст:
            기호 = 0xff0d if знак_вриједност == '\n' else ord(знак_вриједност) if ord(знак_вриједност) < 256 else 0x1000000 | ord(знак_вриједност)
            кликнути_дугме(기호); кликнути_дугме(기호, False)
        return 시작

    def љуска(текст): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', послати_текст(текст+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): удаљено_вриједност.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def кликнути_вриједност(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def растерска_слика_слика():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 стваран_подаци 너비를 쓴다.
        удаљено_вриједност.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        уцртавање_вриједност = Image.new('RGB', (너비, 높이)); подручје_вриједност = 0
        while True:
            종류 = 정확한값(удаљено_вриједност, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                дужина_вриједност = struct.unpack('>I', 정확한값(удаљено_вриједност, 7)[3:])[0]; 정확한값(удаљено_вриједност, дужина_вриједност); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(удаљено_вриједност, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, дужина_вриједност, кодирање_вриједност = struct.unpack('>HHHHi', 정확한값(удаљено_вриједност, 12))
                assert кодирање_вриједност == 0 and 가로+폭 <= 너비 and 세로+дужина_вриједност <= 높이
                уцртавање_вриједност.paste(Image.frombytes('RGB', (폭, дужина_вриједност), 정확한값(удаљено_вриједност, 폭*дужина_вриједност*4), 'raw', 'BGRX'), (가로, 세로))
                подручје_вриједност += 폭*дужина_вриједност
            if подручје_вриједност:
                assert подручје_вриједност == 너비*높이, подручје_вриједност
                return уцртавање_вриједност

    def чек_Пел(координата_вриједност, 색):
        마감 = time.monotonic()+10
        while True:
            уцртавање_вриједност = растерска_слика_слика()
            if уцртавање_вриједност.getpixel(координата_вриједност) == 색: return уцртавање_вриједност
            if time.monotonic() > 마감: raise AssertionError((координата_вриједност, уцртавање_вриједност.getpixel(координата_вриједност), 색))

    def 올리기(назив, подаци): пријенос_вриједност.storbinary('STOR '+назив, io.BytesIO(подаци))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+подесити_величину_текст+' RGB32').encode() in дневник_рада_ред
        print('BOOT:', подесити_величину_текст, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', дневник_рада_ред).group(1))
        удаљено_вриједност = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(удаљено_вриједност, 12) == b'RFB 003.008\n'; удаљено_вриједност.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(удаљено_вриједност, 정확한값(удаљено_вриједност, 1)[0]); удаљено_вриједност.sendall(b'\x01')
        assert 정확한값(удаљено_вриједност, 4) == b'\0'*4; удаљено_вриједност.sendall(b'\x01')
        초기 = 정확한값(удаљено_вриједност, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(удаљено_вриједност, struct.unpack('>I', 초기[20:])[0])
        удаљено_вриједност.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        удаљено_вриједност.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        чек_Пел((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        чек_Пел((너비-568, 높이-360), (32, 80, 144))
        시작 = len(дневник_рада_ред); кликнути_вриједност(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', 시작)
        чек_Пел((너비-568, 높이-360), (24, 32, 48))
        시작 = len(дневник_рада_ред); кликнути_вриједност(80, 16); 기다리기(b'TERMINAL FOCUS 1', 시작)
        љуска('ftpd start')
        пријенос_вриједност = ftplib.FTP(); пријенос_вриједност.encoding = 'utf-8'; пријенос_вриједност.connect('127.0.0.1', 접속번호, timeout=20); пријенос_вриједност.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·исјечак 밖·빈 사각형을 포함한다.
        извор = '''#include <화면규약.h>
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
    писати_фајл_подаци(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.c', извор.encode())
        assert 'exit 0' in љуска('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', послати_текст('run /화면시험\n'))
        чек_Пел((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', послати_текст('q'))
        извор = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, систем_грешка
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except систем_грешка as грешка:
    assert грешка.индекс == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('화면시험.py', извор.encode())
        기다리기(b'PYTHON RESOLUTION PASS', послати_текст('python /화면시험.py\n'))
        чек_Пел((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', послати_текст('q'))
        извор = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("подесити_величину");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("исјечак"); }
        catch (잘못된인수예외 грешка) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 хост_рачунар javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(извор.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        올리기('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', послати_текст('java 해상도경계시험\n'))
        чек_Пел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', послати_текст('q'))
        # 게스트 javac의 подршка_вриједност 문법으로 подесити_величину упит_вриједност·지우기·다섯 인수 그리기를 컴파일한다.
        извор = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.писати_редак("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        올리기('해상도시험.java', извор.encode())
        결과 = љуска('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', послати_текст('java 해상도시험\n'))
        чек_Пел((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', послати_текст('q'))
        올리기('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', послати_текст('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        уцртавање_вриједност = чек_Пел((가로, 세로), (32, 80, 144))
        уцртавање_вриједност.save(str(결과경로/(подесити_величину_текст+'.png')))
        시작 = len(дневник_рада_ред); кликнути_вриједност(가로+80, 세로+155)
        기다리기('SWING CLICK назив'.encode(), 시작)
        시작 = len(дневник_рада_ред); кликнути_вриједност(가로+385, 세로+15); 기다리기(b'jkoros-native> ', 시작)
        assert 'AFTER_RESOLUTION' in љуска('echo AFTER_RESOLUTION')
        print('PASS:', подесити_величину_текст, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if пријенос_вриједност: пријенос_вриједност.close()
        if удаљено_вриједност: удаљено_вриједност.close()
        if процес_вриједност.poll() is None:
            процес_вриједност.terminate()
            try: процес_вриједност.wait(timeout=8)
            except subprocess.TimeoutExpired: процес_вриједност.kill(); процес_вриједност.wait()
        선택기.close(); процес_вриједност.stdout.close()
        (결과경로/(подесити_величину_текст+'.log')).write_bytes(дневник_рада_ред)


def 시작():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    дневник_рада_ред = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for Неважећи_вриједност in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'도구/실행.py'), '--resolution', Неважећи_вриједност], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); дневник_рада_ред['resolutions'].append([너비, 높이])
        дневник_рада_ред.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(дневник_рада_ред, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': 시작()
