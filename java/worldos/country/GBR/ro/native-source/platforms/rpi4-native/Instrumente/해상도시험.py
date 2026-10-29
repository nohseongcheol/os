#!/usr/bin/env python3
"""real_date QEMU/VNC에서 화면 Mărime·경계·Fereastră muta_VALUE_83b651b8·Swing·언어별 그리기를 검사한다."""
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
from desktop_vizualiza import EXACT_VALUE
from executa_comandă import Project_rădăcină


def 해상도시험(너비, 높이, KR_cale):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); număr_port = 임시.getsockname()[1]
    dimensiona_SMS = '{}x{}'.format(너비, 높이)
    Proces_VALUE = subprocess.Popen(['python3', str(Project_rădăcină/'Instrumente/executa_comandă.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(număr_port), '--resolution', dimensiona_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    selector_a916db4e = selectors.DefaultSelector(); selector_a916db4e.register(Proces_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); la_distanță_VALUE = None; Transfer_VALUE = None

    def 기다리기(afișa_VALUE, Pornește=0):
        dată_limită_VALUE = time.monotonic() + 60
        while afișa_VALUE not in LOG_RECORD[Pornește:]:
            if time.monotonic() > dată_limită_VALUE or Proces_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Pornește:].decode('utf-8', 'replace'))
            for Eveniment, _ in selector_a916db4e.select(.1):
                date = Eveniment.fileobj.read(65536)
                if date: LOG_RECORD.extend(date)
        return LOG_RECORD[Pornește:].decode('utf-8', 'replace')

    def clic_buton(simbol, 눌림=True): la_distanță_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbol))

    def trimitere_SMS(SMS):
        Pornește = len(LOG_RECORD)
        for caracter_VALUE in SMS:
            simbol = 0xff0d if caracter_VALUE == '\n' else ord(caracter_VALUE) if ord(caracter_VALUE) < 256 else 0x1000000 | ord(caracter_VALUE)
            clic_buton(simbol); clic_buton(simbol, False)
        return Pornește

    def shell(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', trimitere_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Verticală_poziție, 눌림): la_distanță_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Verticală_poziție))

    def clic_VALUE(가로, Verticală_poziție): 가리키기(가로, Verticală_poziție, 1); 가리키기(가로, Verticală_poziție, 0)

    def bitmap_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 real_date 너비를 쓴다.
        la_distanță_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        desen_VALUE = Image.new('RGB', (너비, 높이)); zonă_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(la_distanță_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                lungime_VALUE = struct.unpack('>I', EXACT_VALUE(la_distanță_VALUE, 7)[3:])[0]; EXACT_VALUE(la_distanță_VALUE, lungime_VALUE); continue
            assert 종류 == 0, 종류
            element_COUNT = struct.unpack('>H', EXACT_VALUE(la_distanță_VALUE, 3)[1:])[0]
            for _ in range(element_COUNT):
                가로, Verticală_poziție, 폭, lungime_VALUE, codificare_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(la_distanță_VALUE, 12))
                assert codificare_VALUE == 0 and 가로+폭 <= 너비 and Verticală_poziție+lungime_VALUE <= 높이
                desen_VALUE.paste(Image.frombytes('RGB', (폭, lungime_VALUE), EXACT_VALUE(la_distanță_VALUE, 폭*lungime_VALUE*4), 'raw', 'BGRX'), (가로, Verticală_poziție))
                zonă_VALUE_9285603e += 폭*lungime_VALUE
            if zonă_VALUE_9285603e:
                assert zonă_VALUE_9285603e == 너비*높이, zonă_VALUE_9285603e
                return desen_VALUE

    def verifica_element_imagine(좌표, 색):
        dată_limită_VALUE = time.monotonic()+10
        while True:
            desen_VALUE = bitmap_IMAGE()
            if desen_VALUE.getpixel(좌표) == 색: return desen_VALUE
            if time.monotonic() > dată_limită_VALUE: raise AssertionError((좌표, desen_VALUE.getpixel(좌표), 색))

    def Upload_Fișiere(Nume, date): Transfer_VALUE.storbinary('STOR '+Nume, io.BytesIO(date))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+dimensiona_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', dimensiona_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        la_distanță_VALUE = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_VALUE(la_distanță_VALUE, 12) == b'RFB 003.008\n'; la_distanță_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(la_distanță_VALUE, EXACT_VALUE(la_distanță_VALUE, 1)[0]); la_distanță_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(la_distanță_VALUE, 4) == b'\0'*4; la_distanță_VALUE.sendall(b'\x01')
        stare_inițială = EXACT_VALUE(la_distanță_VALUE, 24); assert struct.unpack('>HH', stare_inițială[:4]) == (너비, 높이)
        EXACT_VALUE(la_distanță_VALUE, struct.unpack('>I', stare_inițială[20:])[0])
        la_distanță_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        la_distanță_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        verifica_element_imagine((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. Anteriorul_element 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        verifica_element_imagine((너비-568, 높이-360), (32, 80, 144))
        Pornește = len(LOG_RECORD); clic_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Pornește)
        verifica_element_imagine((너비-568, 높이-360), (24, 32, 48))
        Pornește = len(LOG_RECORD); clic_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Pornește)
        shell('ftpd start')
        Transfer_VALUE = ftplib.FTP(); Transfer_VALUE.encoding = 'utf-8'; Transfer_VALUE.connect('127.0.0.1', număr_port, timeout=20); Transfer_VALUE.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·clip 밖·빈 사각형을 포함한다.
        SURSĂ = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Desen_dreptunghi(너비,높이,0,0,0)) return 2;
    if(Desen_dreptunghi(너비,높이-1,1,1,0)!=-22) return 3;
    if(Desen_dreptunghi(너비-1,높이,1,1,0)!=-22) return 4;
    if(Desen_dreptunghi(-1,0,1,1,0)!=-22) return 5;
    if(Desen_dreptunghi(0,0,-1,1,0)!=-22) return 6;
    if(Desen_dreptunghi(너비-1,높이-1,1,1,0x332211)) return 7;
    scriere_Fișier_date(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fișiere('화면시험.c', SURSĂ.encode())
        assert 'exit 0' in shell('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', trimitere_SMS('run /화면시험\n'))
        verifica_element_imagine((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', trimitere_SMS('q'))
        SURSĂ = '''from Română import 화면크기, Desen_dreptunghi, 그림기다리기, Rezultat, sistem_eroare
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Desen_dreptunghi(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistem_eroare as eroare:
    assert eroare.INDEX == 22
Desen_dreptunghi(너비-1, 높이-1, 1, 1, 0x665544)
Rezultat("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fișiere('화면시험.py', SURSĂ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', trimitere_SMS('python /화면시험.py\n'))
        verifica_element_imagine((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', trimitere_SMS('q'))
        SURSĂ = '''import Română.propriu.*;
public class 해상도시험 {
    public static void main(String[] Argumente) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Stare_excepție("Mărime");
        try { 화면.dreptunghi(너비,높이-1,1,1,0); throw new Stare_excepție("clip"); }
        catch (nul_argument_excepție eroare) { }
        화면.șterge_intrare(0x302018);
        화면.dreptunghi(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # excepție 처리는 gazdă javac 결과를 propriu JVM에 올려 검사한다.
        경계원문 = KR_cale/'해상도경계시험.java'
        경계원문.write_text(SURSĂ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_rădăcină/'dist/jkoros-native-korean.jar'), '-d', str(KR_cale), str(경계원문)])
        Upload_Fișiere('해상도경계시험.class', (KR_cale/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', trimitere_SMS('java 해상도경계시험\n'))
        verifica_element_imagine((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', trimitere_SMS('q'))
        # 게스트 javac의 suport_VALUE 문법으로 Mărime interoga_VALUE·șterge_intrare·다섯 Argumente 그리기를 컴파일한다.
        SURSĂ = '''public class 해상도시험 {
    public static void main(String[] Argumente) {
        int 너비=Română.propriu.화면.너비();
        int 높이=Română.propriu.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Română.propriu.화면.șterge_intrare(3153944);
        Română.propriu.화면.dreptunghi(너비-1,높이-1,1,1,10061943);
        Română.propriu.Rezultat.scriere_linie("JAVA RESOLUTION PASS");
        Română.propriu.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Fișiere('해상도시험.java', SURSĂ.encode())
        KR = shell('javac 해상도시험.java'); assert 'exit 0' in KR, KR
        기다리기(b'JAVA RESOLUTION PASS', trimitere_SMS('java 해상도시험\n'))
        verifica_element_imagine((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', trimitere_SMS('q'))
        Upload_Fișiere('스윙시험.class', (KR_cale/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', trimitere_SMS('java 스윙시험\n'))
        가로, Verticală_poziție = (너비-400)//2, (높이-280)//2
        desen_VALUE = verifica_element_imagine((가로, Verticală_poziție), (32, 80, 144))
        desen_VALUE.save(str(KR_cale/(dimensiona_SMS+'.png')))
        Pornește = len(LOG_RECORD); clic_VALUE(가로+80, Verticală_poziție+155)
        기다리기('SWING CLICK Nume'.encode(), Pornește)
        Pornește = len(LOG_RECORD); clic_VALUE(가로+385, Verticală_poziție+15); 기다리기(b'jkoros-native> ', Pornește)
        assert 'AFTER_RESOLUTION' in shell('echo AFTER_RESOLUTION')
        print('PASS:', dimensiona_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Transfer_VALUE: Transfer_VALUE.close()
        if la_distanță_VALUE: la_distanță_VALUE.close()
        if Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try: Proces_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces_VALUE.kill(); Proces_VALUE.wait()
        selector_a916db4e.close(); Proces_VALUE.stdout.close()
        (KR_cale/(dimensiona_SMS+'.log')).write_bytes(LOG_RECORD)


def Pornește():
    KR_cale = Project_rădăcină/'build/verification/resolution'; KR_cale.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_rădăcină/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for nul_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            KR = subprocess.run(['python3', str(Project_rădăcină/'Instrumente/executa_comandă.py'), '--resolution', nul_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert KR.returncode == 2 and b'--resolution' in KR.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_cale), str(Project_rădăcină/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, KR_cale); LOG_RECORD['resolutions'].append([너비, 높이])
        LOG_RECORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_cale/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Pornește()
