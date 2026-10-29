#!/usr/bin/env python3
"""faktisks_dati QEMU/VNC에서 화면 Izmērs·경계·Logs pārvietot_VALUE·Swing·언어별 그리기를 검사한다."""
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
from dators_Skats import EXACT_VALUE
from Izpildīt_komanda import Project_sakne


def 해상도시험(너비, 높이, mērs_ceļš):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); porta_numurs = 임시.getsockname()[1]
    mainīt_izmērus_SMS = '{}x{}'.format(너비, 높이)
    Process_VALUE = subprocess.Popen(['python3', str(Project_sakne/'Rīki/Izpildīt_komanda.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(porta_numurs), '--resolution', mainīt_izmērus_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    atlasītājs_a916db4e = selectors.DefaultSelector(); atlasītājs_a916db4e.register(Process_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); attāls_VALUE = None; nodot_VALUE_630ba093 = None

    def 기다리기(rādīt_VALUE, Palaist=0):
        izpildes_termiņš_VALUE = time.monotonic() + 60
        while rādīt_VALUE not in LOG_RECORD[Palaist:]:
            if time.monotonic() > izpildes_termiņš_VALUE or Process_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Palaist:].decode('utf-8', 'replace'))
            for Notikums, _ in atlasītājs_a916db4e.select(.1):
                dati = Notikums.fileobj.read(65536)
                if dati: LOG_RECORD.extend(dati)
        return LOG_RECORD[Palaist:].decode('utf-8', 'replace')

    def klikšķis_poga(simbols, 눌림=True): attāls_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbols))

    def sūtīt_īsziņu(Teksts):
        Palaist = len(LOG_RECORD)
        for rakstzīme_VALUE in Teksts:
            simbols = 0xff0d if rakstzīme_VALUE == '\n' else ord(rakstzīme_VALUE) if ord(rakstzīme_VALUE) < 256 else 0x1000000 | ord(rakstzīme_VALUE)
            klikšķis_poga(simbols); klikšķis_poga(simbols, False)
        return Palaist

    def čaula(Teksts): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', sūtīt_īsziņu(Teksts+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, vertikāle_amats, 눌림): attāls_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, vertikāle_amats))

    def klikšķis_VALUE(가로, vertikāle_amats): 가리키기(가로, vertikāle_amats, 1); 가리키기(가로, vertikāle_amats, 0)

    def bitkarte_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktisks_dati 너비를 쓴다.
        attāls_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        zīmējums_VALUE = Image.new('RGB', (너비, 높이)); joma_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(attāls_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(attāls_VALUE, 7)[3:])[0]; EXACT_VALUE(attāls_VALUE, 길이); continue
            assert 종류 == 0, 종류
            krājums_COUNT = struct.unpack('>H', EXACT_VALUE(attāls_VALUE, 3)[1:])[0]
            for _ in range(krājums_COUNT):
                가로, vertikāle_amats, 폭, 길이, kodēšana_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(attāls_VALUE, 12))
                assert kodēšana_VALUE == 0 and 가로+폭 <= 너비 and vertikāle_amats+길이 <= 높이
                zīmējums_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(attāls_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, vertikāle_amats))
                joma_VALUE_9285603e += 폭*길이
            if joma_VALUE_9285603e:
                assert joma_VALUE_9285603e == 너비*높이, joma_VALUE_9285603e
                return zīmējums_VALUE

    def čeks_attēla_elements(좌표, 색):
        izpildes_termiņš_VALUE = time.monotonic()+10
        while True:
            zīmējums_VALUE = bitkarte_IMAGE()
            if zīmējums_VALUE.getpixel(좌표) == 색: return zīmējums_VALUE
            if time.monotonic() > izpildes_termiņš_VALUE: raise AssertionError((좌표, zīmējums_VALUE.getpixel(좌표), 색))

    def Upload_Faili(Nosaukums, dati): nodot_VALUE_630ba093.storbinary('STOR '+Nosaukums, io.BytesIO(dati))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+mainīt_izmērus_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', mainīt_izmērus_SMS, flush=True)
        attāls_numurs = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        attāls_VALUE = socket.create_connection(('127.0.0.1', attāls_numurs), timeout=20)
        assert EXACT_VALUE(attāls_VALUE, 12) == b'RFB 003.008\n'; attāls_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(attāls_VALUE, EXACT_VALUE(attāls_VALUE, 1)[0]); attāls_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(attāls_VALUE, 4) == b'\0'*4; attāls_VALUE.sendall(b'\x01')
        sākumstāvoklis = EXACT_VALUE(attāls_VALUE, 24); assert struct.unpack('>HH', sākumstāvoklis[:4]) == (너비, 높이)
        EXACT_VALUE(attāls_VALUE, struct.unpack('>I', sākumstāvoklis[20:])[0])
        attāls_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        attāls_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        čeks_attēla_elements((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        čeks_attēla_elements((너비-568, 높이-360), (32, 80, 144))
        Palaist = len(LOG_RECORD); klikšķis_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Palaist)
        čeks_attēla_elements((너비-568, 높이-360), (24, 32, 48))
        Palaist = len(LOG_RECORD); klikšķis_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Palaist)
        čaula('ftpd start')
        nodot_VALUE_630ba093 = ftplib.FTP(); nodot_VALUE_630ba093.encoding = 'utf-8'; nodot_VALUE_630ba093.connect('127.0.0.1', porta_numurs, timeout=20); nodot_VALUE_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klips 밖·빈 사각형을 포함한다.
        AVOTS = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(zīmēt_taisnstūris(너비,높이,0,0,0)) return 2;
    if(zīmēt_taisnstūris(너비,높이-1,1,1,0)!=-22) return 3;
    if(zīmēt_taisnstūris(너비-1,높이,1,1,0)!=-22) return 4;
    if(zīmēt_taisnstūris(-1,0,1,1,0)!=-22) return 5;
    if(zīmēt_taisnstūris(0,0,-1,1,0)!=-22) return 6;
    if(zīmēt_taisnstūris(너비-1,높이-1,1,1,0x332211)) return 7;
    rakstīšana_Fails_dati(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Faili('화면시험.c', AVOTS.encode())
        assert 'exit 0' in čaula('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', sūtīt_īsziņu('run /화면시험\n'))
        čeks_attēla_elements((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', sūtīt_īsziņu('q'))
        AVOTS = '''from Latviešu import 화면크기, zīmēt_taisnstūris, 그림기다리기, Izvade, sistēma_kļūda
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    zīmēt_taisnstūris(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except sistēma_kļūda as Kļūda:
    assert Kļūda.INDEX == 22
zīmēt_taisnstūris(너비-1, 높이-1, 1, 1, 0x665544)
Izvade("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Faili('화면시험.py', AVOTS.encode())
        기다리기(b'PYTHON RESOLUTION PASS', sūtīt_īsziņu('python /화면시험.py\n'))
        čeks_attēla_elements((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', sūtīt_īsziņu('q'))
        AVOTS = '''import Latviešu.savs.*;
public class 해상도시험 {
    public static void main(String[] Parametri) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Statuss_izņēmums("Izmērs");
        try { 화면.taisnstūris(너비,높이-1,1,1,0); throw new Statuss_izņēmums("klips"); }
        catch (nederīgs_arg_izņēmums Kļūda) { }
        화면.dzēst_ievade(0x302018);
        화면.taisnstūris(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # izņēmums 처리는 viesot javac 결과를 savs JVM에 올려 검사한다.
        경계원문 = mērs_ceļš/'해상도경계시험.java'
        경계원문.write_text(AVOTS.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_sakne/'dist/jkoros-native-korean.jar'), '-d', str(mērs_ceļš), str(경계원문)])
        Upload_Faili('해상도경계시험.class', (mērs_ceļš/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', sūtīt_īsziņu('java 해상도경계시험\n'))
        čeks_attēla_elements((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', sūtīt_īsziņu('q'))
        # 게스트 javac의 Atbalsts_VALUE 문법으로 Izmērs vaicāt_VALUE·dzēst_ievade·다섯 Parametri 그리기를 컴파일한다.
        AVOTS = '''public class 해상도시험 {
    public static void main(String[] Parametri) {
        int 너비=Latviešu.savs.화면.너비();
        int 높이=Latviešu.savs.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Latviešu.savs.화면.dzēst_ievade(3153944);
        Latviešu.savs.화면.taisnstūris(너비-1,높이-1,1,1,10061943);
        Latviešu.savs.Izvade.rakstīšana_līnija("JAVA RESOLUTION PASS");
        Latviešu.savs.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Faili('해상도시험.java', AVOTS.encode())
        mērs = čaula('javac 해상도시험.java'); assert 'exit 0' in mērs, mērs
        기다리기(b'JAVA RESOLUTION PASS', sūtīt_īsziņu('java 해상도시험\n'))
        čeks_attēla_elements((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', sūtīt_īsziņu('q'))
        Upload_Faili('스윙시험.class', (mērs_ceļš/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', sūtīt_īsziņu('java 스윙시험\n'))
        가로, vertikāle_amats = (너비-400)//2, (높이-280)//2
        zīmējums_VALUE = čeks_attēla_elements((가로, vertikāle_amats), (32, 80, 144))
        zīmējums_VALUE.save(str(mērs_ceļš/(mainīt_izmērus_SMS+'.png')))
        Palaist = len(LOG_RECORD); klikšķis_VALUE(가로+80, vertikāle_amats+155)
        기다리기('SWING CLICK Nosaukums'.encode(), Palaist)
        Palaist = len(LOG_RECORD); klikšķis_VALUE(가로+385, vertikāle_amats+15); 기다리기(b'jkoros-native> ', Palaist)
        assert 'AFTER_RESOLUTION' in čaula('echo AFTER_RESOLUTION')
        print('PASS:', mainīt_izmērus_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if nodot_VALUE_630ba093: nodot_VALUE_630ba093.close()
        if attāls_VALUE: attāls_VALUE.close()
        if Process_VALUE.poll() is None:
            Process_VALUE.terminate()
            try: Process_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Process_VALUE.kill(); Process_VALUE.wait()
        atlasītājs_a916db4e.close(); Process_VALUE.stdout.close()
        (mērs_ceļš/(mainīt_izmērus_SMS+'.log')).write_bytes(LOG_RECORD)


def Palaist():
    mērs_ceļš = Project_sakne/'build/verification/resolution'; mērs_ceļš.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for nederīgs_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            mērs = subprocess.run(['python3', str(Project_sakne/'Rīki/Izpildīt_komanda.py'), '--resolution', nederīgs_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert mērs.returncode == 2 and b'--resolution' in mērs.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(mērs_ceļš), str(Project_sakne/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, mērs_ceļš); LOG_RECORD['resolutions'].append([너비, 높이])
        LOG_RECORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (mērs_ceļš/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Palaist()
