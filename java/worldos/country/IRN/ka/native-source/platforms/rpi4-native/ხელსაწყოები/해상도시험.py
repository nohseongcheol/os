#!/usr/bin/env python3
"""რეალური_მონაცემები QEMU/VNC에서 화면 ზომა·경계·ფანჯარა გადატანა_მნიშვნელობა·Swing·언어별 그리기를 검사한다."""
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
from სამუშაო_დაფა_ხედი import 정확한값
from შესრულება_ბრძანება import პროეცირება_ფესვი


def 해상도시험(너비, 높이, გაზომვა_მდებარეობა):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    ზომის_შეცვლა_ტექსტი = '{}x{}'.format(너비, 높이)
    პროცესი_მნიშვნელობა = subprocess.Popen(['python3', str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ბრძანება.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', ზომის_შეცვლა_ტექსტი], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    სელექტორი_a916db4e = selectors.DefaultSelector(); სელექტორი_a916db4e.register(პროცესი_მნიშვნელობა.stdout, selectors.EVENT_READ)
    ჟურნალი_ჩაწერა = bytearray(); დისტანციური_მნიშვნელობა = None; გადატანა_მნიშვნელობა_630ba093 = None

    def 기다리기(ჩვენება_მნიშვნელობა, გაშვება=0):
        마감 = time.monotonic() + 60
        while ჩვენება_მნიშვნელობა not in ჟურნალი_ჩაწერა[გაშვება:]:
            if time.monotonic() > 마감 or პროცესი_მნიშვნელობა.poll() is not None or b'HALTED' in ჟურნალი_ჩაწერა or b'PANIC:' in ჟურნალი_ჩაწერა:
                raise AssertionError(ჟურნალი_ჩაწერა[გაშვება:].decode('utf-8', 'replace'))
            for მოვლენა, _ in სელექტორი_a916db4e.select(.1):
                მონაცემები = მოვლენა.fileobj.read(65536)
                if მონაცემები: ჟურნალი_ჩაწერა.extend(მონაცემები)
        return ჟურნალი_ჩაწერა[გაშვება:].decode('utf-8', 'replace')

    def დაწკაპუნება_ღილაკი(სიმბოლო, 눌림=True): დისტანციური_მნიშვნელობა.sendall(struct.pack('>BBHI', 4, int(눌림), 0, სიმბოლო))

    def SMS_ის_გაგზავნა(ტექსტი):
        გაშვება = len(ჟურნალი_ჩაწერა)
        for სიმბოლო_მნიშვნელობა_068c2631 in ტექსტი:
            სიმბოლო = 0xff0d if სიმბოლო_მნიშვნელობა_068c2631 == '\n' else ord(სიმბოლო_მნიშვნელობა_068c2631) if ord(სიმბოლო_მნიშვნელობა_068c2631) < 256 else 0x1000000 | ord(სიმბოლო_მნიშვნელობა_068c2631)
            დაწკაპუნება_ღილაკი(სიმბოლო); დაწკაპუნება_ღილაკი(სიმბოლო, False)
        return გაშვება

    def გარემო(ტექსტი): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_ის_გაგზავნა(ტექსტი+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ვერტიკალური_პოზიცია, 눌림): დისტანციური_მნიშვნელობა.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ვერტიკალური_პოზიცია))

    def დაწკაპუნება_მნიშვნელობა(가로, ვერტიკალური_პოზიცია): 가리키기(가로, ვერტიკალური_პოზიცია, 1); 가리키기(가로, ვერტიკალური_პოზიცია, 0)

    def რასტერული_გრაფიკა_ნახატი():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 რეალური_მონაცემები 너비를 쓴다.
        დისტანციური_მნიშვნელობა.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ნახატი_მნიშვნელობა_c143fe9e = Image.new('RGB', (너비, 높이)); არე_მნიშვნელობა = 0
        while True:
            종류 = 정확한값(დისტანციური_მნიშვნელობა, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                სიგრძე_მნიშვნელობა = struct.unpack('>I', 정확한값(დისტანციური_მნიშვნელობა, 7)[3:])[0]; 정확한값(დისტანციური_მნიშვნელობა, სიგრძე_მნიშვნელობა); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(დისტანციური_მნიშვნელობა, 3)[1:])[0]
            for _ in range(개수):
                가로, ვერტიკალური_პოზიცია, 폭, სიგრძე_მნიშვნელობა, კოდირება_მნიშვნელობა = struct.unpack('>HHHHi', 정확한값(დისტანციური_მნიშვნელობა, 12))
                assert კოდირება_მნიშვნელობა == 0 and 가로+폭 <= 너비 and ვერტიკალური_პოზიცია+სიგრძე_მნიშვნელობა <= 높이
                ნახატი_მნიშვნელობა_c143fe9e.paste(Image.frombytes('RGB', (폭, სიგრძე_მნიშვნელობა), 정확한값(დისტანციური_მნიშვნელობა, 폭*სიგრძე_მნიშვნელობა*4), 'raw', 'BGRX'), (가로, ვერტიკალური_პოზიცია))
                არე_მნიშვნელობა += 폭*სიგრძე_მნიშვნელობა
            if არე_მნიშვნელობა:
                assert არე_მნიშვნელობა == 너비*높이, არე_მნიშვნელობა
                return ნახატი_მნიშვნელობა_c143fe9e

    def შემოწმება_პიქსელი(კოორდინატი_მნიშვნელობა, 색):
        마감 = time.monotonic()+10
        while True:
            ნახატი_მნიშვნელობა_c143fe9e = რასტერული_გრაფიკა_ნახატი()
            if ნახატი_მნიშვნელობა_c143fe9e.getpixel(კოორდინატი_მნიშვნელობა) == 색: return ნახატი_მნიშვნელობა_c143fe9e
            if time.monotonic() > 마감: raise AssertionError((კოორდინატი_მნიშვნელობა, ნახატი_მნიშვნელობა_c143fe9e.getpixel(კოორდინატი_მნიშვნელობა), 색))

    def ატვირთვა_ფაილები(სახელი, მონაცემები): გადატანა_მნიშვნელობა_630ba093.storbinary('STOR '+სახელი, io.BytesIO(მონაცემები))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ზომის_შეცვლა_ტექსტი+' RGB32').encode() in ჟურნალი_ჩაწერა
        print('BOOT:', ზომის_შეცვლა_ტექსტი, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ჟურნალი_ჩაწერა).group(1))
        დისტანციური_მნიშვნელობა = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(დისტანციური_მნიშვნელობა, 12) == b'RFB 003.008\n'; დისტანციური_მნიშვნელობა.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(დისტანციური_მნიშვნელობა, 정확한값(დისტანციური_მნიშვნელობა, 1)[0]); დისტანციური_მნიშვნელობა.sendall(b'\x01')
        assert 정확한값(დისტანციური_მნიშვნელობა, 4) == b'\0'*4; დისტანციური_მნიშვნელობა.sendall(b'\x01')
        초기 = 정확한값(დისტანციური_მნიშვნელობა, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(დისტანციური_მნიშვნელობა, struct.unpack('>I', 초기[20:])[0])
        დისტანციური_მნიშვნელობა.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        დისტანციური_მნიშვნელობა.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        შემოწმება_პიქსელი((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        შემოწმება_პიქსელი((너비-568, 높이-360), (32, 80, 144))
        გაშვება = len(ჟურნალი_ჩაწერა); დაწკაპუნება_მნიშვნელობა(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', გაშვება)
        შემოწმება_პიქსელი((너비-568, 높이-360), (24, 32, 48))
        გაშვება = len(ჟურნალი_ჩაწერა); დაწკაპუნება_მნიშვნელობა(80, 16); 기다리기(b'TERMINAL FOCUS 1', გაშვება)
        გარემო('ftpd start')
        გადატანა_მნიშვნელობა_630ba093 = ftplib.FTP(); გადატანა_მნიშვნელობა_630ba093.encoding = 'utf-8'; გადატანა_მნიშვნელობა_630ba093.connect('127.0.0.1', 접속번호, timeout=20); გადატანა_მნიშვნელობა_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·კლიპი 밖·빈 사각형을 포함한다.
        წყარო = '''#include <화면규약.h>
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
    ჩაწერა_ფაილი_მონაცემები(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ატვირთვა_ფაილები('화면시험.c', წყარო.encode())
        assert 'exit 0' in გარემო('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_ის_გაგზავნა('run /화면시험\n'))
        შემოწმება_პიქსელი((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_ის_გაგზავნა('q'))
        წყარო = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, სისტემა_შეცდომა
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except სისტემა_შეცდომა as შეცდომა:
    assert შეცდომა.ინდექსი == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ატვირთვა_ფაილები('화면시험.py', წყარო.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_ის_გაგზავნა('python /화면시험.py\n'))
        შემოწმება_პიქსელი((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_ის_გაგზავნა('q'))
        წყარო = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("ზომა");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("კლიპი"); }
        catch (잘못된인수예외 შეცდომა) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 მასპინძელი javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = გაზომვა_მდებარეობა/'해상도경계시험.java'
        경계원문.write_text(წყარო.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(პროეცირება_ფესვი/'dist/jkoros-native-korean.jar'), '-d', str(გაზომვა_მდებარეობა), str(경계원문)])
        ატვირთვა_ფაილები('해상도경계시험.class', (გაზომვა_მდებარეობა/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_ის_გაგზავნა('java 해상도경계시험\n'))
        შემოწმება_პიქსელი((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ის_გაგზავნა('q'))
        # 게스트 javac의 მხარდაჭერა_მნიშვნელობა 문법으로 ზომა მოთხოვნა_მნიშვნელობა·지우기·다섯 인수 그리기를 컴파일한다.
        წყარო = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.지우기(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.ჩაწერა_ხაზი("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ატვირთვა_ფაილები('해상도시험.java', წყარო.encode())
        გაზომვა = გარემო('javac 해상도시험.java'); assert 'exit 0' in გაზომვა, გაზომვა
        기다리기(b'JAVA RESOLUTION PASS', SMS_ის_გაგზავნა('java 해상도시험\n'))
        შემოწმება_პიქსელი((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_ის_გაგზავნა('q'))
        ატვირთვა_ფაილები('스윙시험.class', (გაზომვა_მდებარეობა/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', SMS_ის_გაგზავნა('java 스윙시험\n'))
        가로, ვერტიკალური_პოზიცია = (너비-400)//2, (높이-280)//2
        ნახატი_მნიშვნელობა_c143fe9e = შემოწმება_პიქსელი((가로, ვერტიკალური_პოზიცია), (32, 80, 144))
        ნახატი_მნიშვნელობა_c143fe9e.save(str(გაზომვა_მდებარეობა/(ზომის_შეცვლა_ტექსტი+'.png')))
        გაშვება = len(ჟურნალი_ჩაწერა); დაწკაპუნება_მნიშვნელობა(가로+80, ვერტიკალური_პოზიცია+155)
        기다리기('SWING CLICK სახელი'.encode(), გაშვება)
        გაშვება = len(ჟურნალი_ჩაწერა); დაწკაპუნება_მნიშვნელობა(가로+385, ვერტიკალური_პოზიცია+15); 기다리기(b'jkoros-native> ', გაშვება)
        assert 'AFTER_RESOLUTION' in გარემო('echo AFTER_RESOLUTION')
        print('PASS:', ზომის_შეცვლა_ტექსტი, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if გადატანა_მნიშვნელობა_630ba093: გადატანა_მნიშვნელობა_630ba093.close()
        if დისტანციური_მნიშვნელობა: დისტანციური_მნიშვნელობა.close()
        if პროცესი_მნიშვნელობა.poll() is None:
            პროცესი_მნიშვნელობა.terminate()
            try: პროცესი_მნიშვნელობა.wait(timeout=8)
            except subprocess.TimeoutExpired: პროცესი_მნიშვნელობა.kill(); პროცესი_მნიშვნელობა.wait()
        სელექტორი_a916db4e.close(); პროცესი_მნიშვნელობა.stdout.close()
        (გაზომვა_მდებარეობა/(ზომის_შეცვლა_ტექსტი+'.log')).write_bytes(ჟურნალი_ჩაწერა)


def გაშვება():
    გაზომვა_მდებარეობა = პროეცირება_ფესვი/'build/verification/resolution'; გაზომვა_მდებარეობა.mkdir(parents=True, exist_ok=True)
    ჟურნალი_ჩაწერა = {'passed': False, 'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for არასწორი_მნიშვნელობა in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            გაზომვა = subprocess.run(['python3', str(პროეცირება_ფესვი/'ხელსაწყოები/შესრულება_ბრძანება.py'), '--resolution', არასწორი_მნიშვნელობა], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert გაზომვა.returncode == 2 and b'--resolution' in გაზომვა.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(გაზომვა_მდებარეობა), str(პროეცირება_ფესვი/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, გაზომვა_მდებარეობა); ჟურნალი_ჩაწერა['resolutions'].append([너비, 높이])
        ჟურნალი_ჩაწერა.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (გაზომვა_მდებარეობა/'report.json').write_text(json.dumps(ჟურნალი_ჩაწერა, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': გაშვება()
