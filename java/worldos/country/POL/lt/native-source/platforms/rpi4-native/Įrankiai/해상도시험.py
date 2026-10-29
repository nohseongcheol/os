#!/usr/bin/env python3
"""faktinis_duomenys QEMU/VNC에서 화면 Dydis·경계·Langas judėti_VALUE·Swing·언어별 그리기를 검사한다."""
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
from darbalaukis_rodyti import EXACT_VALUE
from Vykdyti_komanda import Project_šaknis


def 해상도시험(너비, 높이, KR_kelias):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); prievado_numeris = 임시.getsockname()[1]
    dydis_SMS = '{}x{}'.format(너비, 높이)
    Procesas_VALUE = subprocess.Popen(['python3', str(Project_šaknis/'Įrankiai/Vykdyti_komanda.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(prievado_numeris), '--resolution', dydis_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    išrinkiklis_a916db4e = selectors.DefaultSelector(); išrinkiklis_a916db4e.register(Procesas_VALUE.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); nuotolinis_VALUE = None; perduoti_VALUE_630ba093 = None

    def 기다리기(laida_VALUE, Paleisti=0):
        terminas_VALUE = time.monotonic() + 60
        while laida_VALUE not in LOG_RECORD[Paleisti:]:
            if time.monotonic() > terminas_VALUE or Procesas_VALUE.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[Paleisti:].decode('utf-8', 'replace'))
            for Įvykis, _ in išrinkiklis_a916db4e.select(.1):
                duomenys = Įvykis.fileobj.read(65536)
                if duomenys: LOG_RECORD.extend(duomenys)
        return LOG_RECORD[Paleisti:].decode('utf-8', 'replace')

    def spustelėti_mygtukas(simbolis, 눌림=True): nuotolinis_VALUE.sendall(struct.pack('>BBHI', 4, int(눌림), 0, simbolis))

    def siųsti_SMS_žinutę(Tekstas):
        Paleisti = len(LOG_RECORD)
        for simbolis_VALUE_068c2631 in Tekstas:
            simbolis = 0xff0d if simbolis_VALUE_068c2631 == '\n' else ord(simbolis_VALUE_068c2631) if ord(simbolis_VALUE_068c2631) < 256 else 0x1000000 | ord(simbolis_VALUE_068c2631)
            spustelėti_mygtukas(simbolis); spustelėti_mygtukas(simbolis, False)
        return Paleisti

    def apvalkalas(Tekstas): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', siųsti_SMS_žinutę(Tekstas+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, segmentas_padėtis, 눌림): nuotolinis_VALUE.sendall(struct.pack('>BBHH', 5, 눌림, 가로, segmentas_padėtis))

    def spustelėti_VALUE(가로, segmentas_padėtis): 가리키기(가로, segmentas_padėtis, 1); 가리키기(가로, segmentas_padėtis, 0)

    def rastras_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 faktinis_duomenys 너비를 쓴다.
        nuotolinis_VALUE.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        piešinys_VALUE = Image.new('RGB', (너비, 높이)); sritis_VALUE_9285603e = 0
        while True:
            종류 = EXACT_VALUE(nuotolinis_VALUE, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', EXACT_VALUE(nuotolinis_VALUE, 7)[3:])[0]; EXACT_VALUE(nuotolinis_VALUE, 길이); continue
            assert 종류 == 0, 종류
            prekė_COUNT = struct.unpack('>H', EXACT_VALUE(nuotolinis_VALUE, 3)[1:])[0]
            for _ in range(prekė_COUNT):
                가로, segmentas_padėtis, 폭, 길이, kodavimas_VALUE = struct.unpack('>HHHHi', EXACT_VALUE(nuotolinis_VALUE, 12))
                assert kodavimas_VALUE == 0 and 가로+폭 <= 너비 and segmentas_padėtis+길이 <= 높이
                piešinys_VALUE.paste(Image.frombytes('RGB', (폭, 길이), EXACT_VALUE(nuotolinis_VALUE, 폭*길이*4), 'raw', 'BGRX'), (가로, segmentas_padėtis))
                sritis_VALUE_9285603e += 폭*길이
            if sritis_VALUE_9285603e:
                assert sritis_VALUE_9285603e == 너비*높이, sritis_VALUE_9285603e
                return piešinys_VALUE

    def čekis_pikselis(좌표, 색):
        terminas_VALUE = time.monotonic()+10
        while True:
            piešinys_VALUE = rastras_IMAGE()
            if piešinys_VALUE.getpixel(좌표) == 색: return piešinys_VALUE
            if time.monotonic() > terminas_VALUE: raise AssertionError((좌표, piešinys_VALUE.getpixel(좌표), 색))

    def Upload_Failai(Pavadinimas_2, duomenys): perduoti_VALUE_630ba093.storbinary('STOR '+Pavadinimas_2, io.BytesIO(duomenys))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+dydis_SMS+' RGB32').encode() in LOG_RECORD
        print('BOOT:', dydis_SMS, flush=True)
        nuotolinis_numeris = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        nuotolinis_VALUE = socket.create_connection(('127.0.0.1', nuotolinis_numeris), timeout=20)
        assert EXACT_VALUE(nuotolinis_VALUE, 12) == b'RFB 003.008\n'; nuotolinis_VALUE.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_VALUE(nuotolinis_VALUE, EXACT_VALUE(nuotolinis_VALUE, 1)[0]); nuotolinis_VALUE.sendall(b'\x01')
        assert EXACT_VALUE(nuotolinis_VALUE, 4) == b'\0'*4; nuotolinis_VALUE.sendall(b'\x01')
        pradinė_būsena = EXACT_VALUE(nuotolinis_VALUE, 24); assert struct.unpack('>HH', pradinė_būsena[:4]) == (너비, 높이)
        EXACT_VALUE(nuotolinis_VALUE, struct.unpack('>I', pradinė_būsena[20:])[0])
        nuotolinis_VALUE.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        nuotolinis_VALUE.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        čekis_pikselis((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        čekis_pikselis((너비-568, 높이-360), (32, 80, 144))
        Paleisti = len(LOG_RECORD); spustelėti_VALUE(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Paleisti)
        čekis_pikselis((너비-568, 높이-360), (24, 32, 48))
        Paleisti = len(LOG_RECORD); spustelėti_VALUE(80, 16); 기다리기(b'TERMINAL FOCUS 1', Paleisti)
        apvalkalas('ftpd start')
        perduoti_VALUE_630ba093 = ftplib.FTP(); perduoti_VALUE_630ba093.encoding = 'utf-8'; perduoti_VALUE_630ba093.connect('127.0.0.1', prievado_numeris, timeout=20); perduoti_VALUE_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_VALUE·klipas 밖·빈 사각형을 포함한다.
        ŠALTINIS = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(piešti_stačiakampis(너비,높이,0,0,0)) return 2;
    if(piešti_stačiakampis(너비,높이-1,1,1,0)!=-22) return 3;
    if(piešti_stačiakampis(너비-1,높이,1,1,0)!=-22) return 4;
    if(piešti_stačiakampis(-1,0,1,1,0)!=-22) return 5;
    if(piešti_stačiakampis(0,0,-1,1,0)!=-22) return 6;
    if(piešti_stačiakampis(너비-1,높이-1,1,1,0x332211)) return 7;
    rašymas_Failas_duomenys(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Failai('화면시험.c', ŠALTINIS.encode())
        assert 'exit 0' in apvalkalas('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', siųsti_SMS_žinutę('run /화면시험\n'))
        čekis_pikselis((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', siųsti_SMS_žinutę('q'))
        ŠALTINIS = '''from Lietuvių import 화면크기, piešti_stačiakampis, 그림기다리기, Išvestis, 운영체제오류
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    piešti_stačiakampis(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except 운영체제오류 as KLAIDA:
    assert KLAIDA.INDEX == 22
piešti_stačiakampis(너비-1, 높이-1, 1, 1, 0x665544)
Išvestis("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Failai('화면시험.py', ŠALTINIS.encode())
        기다리기(b'PYTHON RESOLUTION PASS', siųsti_SMS_žinutę('python /화면시험.py\n'))
        čekis_pikselis((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', siųsti_SMS_žinutę('q'))
        ŠALTINIS = '''import Lietuvių.savas.*;
public class 해상도시험 {
    public static void main(String[] Argumentai) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Būsena_išimtis("Dydis");
        try { 화면.stačiakampis(너비,높이-1,1,1,0); throw new Būsena_išimtis("klipas"); }
        catch (neleistinas_argumentas_išimtis KLAIDA) { }
        화면.ištrinti_įrašas(0x302018);
        화면.stačiakampis(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # išimtis 처리는 organizuoti javac 결과를 savas JVM에 올려 검사한다.
        경계원문 = KR_kelias/'해상도경계시험.java'
        경계원문.write_text(ŠALTINIS.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_šaknis/'dist/jkoros-native-korean.jar'), '-d', str(KR_kelias), str(경계원문)])
        Upload_Failai('해상도경계시험.class', (KR_kelias/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', siųsti_SMS_žinutę('java 해상도경계시험\n'))
        čekis_pikselis((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', siųsti_SMS_žinutę('q'))
        # 게스트 javac의 pagalba_VALUE 문법으로 Dydis užklausa_VALUE·ištrinti_įrašas·다섯 Argumentai 그리기를 컴파일한다.
        ŠALTINIS = '''public class 해상도시험 {
    public static void main(String[] Argumentai) {
        int 너비=Lietuvių.savas.화면.너비();
        int 높이=Lietuvių.savas.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Lietuvių.savas.화면.ištrinti_įrašas(3153944);
        Lietuvių.savas.화면.stačiakampis(너비-1,높이-1,1,1,10061943);
        Lietuvių.savas.Išvestis.rašymas_eilutė("JAVA RESOLUTION PASS");
        Lietuvių.savas.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        Upload_Failai('해상도시험.java', ŠALTINIS.encode())
        REZULTATAS = apvalkalas('javac 해상도시험.java'); assert 'exit 0' in REZULTATAS, REZULTATAS
        기다리기(b'JAVA RESOLUTION PASS', siųsti_SMS_žinutę('java 해상도시험\n'))
        čekis_pikselis((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', siųsti_SMS_žinutę('q'))
        Upload_Failai('스윙시험.class', (KR_kelias/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', siųsti_SMS_žinutę('java 스윙시험\n'))
        가로, segmentas_padėtis = (너비-400)//2, (높이-280)//2
        piešinys_VALUE = čekis_pikselis((가로, segmentas_padėtis), (32, 80, 144))
        piešinys_VALUE.save(str(KR_kelias/(dydis_SMS+'.png')))
        Paleisti = len(LOG_RECORD); spustelėti_VALUE(가로+80, segmentas_padėtis+155)
        기다리기('SWING CLICK Pavadinimas_2'.encode(), Paleisti)
        Paleisti = len(LOG_RECORD); spustelėti_VALUE(가로+385, segmentas_padėtis+15); 기다리기(b'jkoros-native> ', Paleisti)
        assert 'AFTER_RESOLUTION' in apvalkalas('echo AFTER_RESOLUTION')
        print('PASS:', dydis_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if perduoti_VALUE_630ba093: perduoti_VALUE_630ba093.close()
        if nuotolinis_VALUE: nuotolinis_VALUE.close()
        if Procesas_VALUE.poll() is None:
            Procesas_VALUE.terminate()
            try: Procesas_VALUE.wait(timeout=8)
            except subprocess.TimeoutExpired: Procesas_VALUE.kill(); Procesas_VALUE.wait()
        išrinkiklis_a916db4e.close(); Procesas_VALUE.stdout.close()
        (KR_kelias/(dydis_SMS+'.log')).write_bytes(LOG_RECORD)


def Paleisti():
    KR_kelias = Project_šaknis/'build/verification/resolution'; KR_kelias.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'kernel_sha256': hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for neleistinas_VALUE in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            REZULTATAS = subprocess.run(['python3', str(Project_šaknis/'Įrankiai/Vykdyti_komanda.py'), '--resolution', neleistinas_VALUE], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert REZULTATAS.returncode == 2 and b'--resolution' in REZULTATAS.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_kelias), str(Project_šaknis/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, KR_kelias); LOG_RECORD['resolutions'].append([너비, 높이])
        LOG_RECORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_kelias/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Paleisti()
