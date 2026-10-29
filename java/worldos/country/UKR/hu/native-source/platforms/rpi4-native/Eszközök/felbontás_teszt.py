#!/usr/bin/env python3
"""tényleges_adat QEMU/VNC에서 화면 Méret·határ_ÉRTÉK·Ablak áthelyez_ÉRTÉK·Swing·언어별 그리기를 검사한다."""
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
from Asztal_Nézet import AZONOS_ÉRTÉK
from végrehajt_parancs import teendő_gyök


def felbontás_teszt(너비, 높이, KR_útvonal):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); portszám = 임시.getsockname()[1]
    méretez_SMS = '{}x{}'.format(너비, 높이)
    folyamat_ÉRTÉK = subprocess.Popen(['python3', str(teendő_gyök/'Eszközök/végrehajt_parancs.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(portszám), '--resolution', méretez_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    szelektor_a916db4e = selectors.DefaultSelector(); szelektor_a916db4e.register(folyamat_ÉRTÉK.stdout, selectors.EVENT_READ)
    LOG_REKORD = bytearray(); távoli_ÉRTÉK = None; átvisz_ÉRTÉK = None

    def 기다리기(bemutató_ÉRTÉK, Futtatás=0):
        határidő_ÉRTÉK = time.monotonic() + 60
        while bemutató_ÉRTÉK not in LOG_REKORD[Futtatás:]:
            if time.monotonic() > határidő_ÉRTÉK or folyamat_ÉRTÉK.poll() is not None or b'HALTED' in LOG_REKORD or b'PANIC:' in LOG_REKORD:
                raise AssertionError(LOG_REKORD[Futtatás:].decode('utf-8', 'replace'))
            for Esemény, _ in szelektor_a916db4e.select(.1):
                adat = Esemény.fileobj.read(65536)
                if adat: LOG_REKORD.extend(adat)
        return LOG_REKORD[Futtatás:].decode('utf-8', 'replace')

    def kattint_gomb(szimbólum, 눌림=True): távoli_ÉRTÉK.sendall(struct.pack('>BBHI', 4, int(눌림), 0, szimbólum))

    def SMS_küldése(Szöveg):
        Futtatás = len(LOG_REKORD)
        for karakter_ÉRTÉK in Szöveg:
            szimbólum = 0xff0d if karakter_ÉRTÉK == '\n' else ord(karakter_ÉRTÉK) if ord(karakter_ÉRTÉK) < 256 else 0x1000000 | ord(karakter_ÉRTÉK)
            kattint_gomb(szimbólum); kattint_gomb(szimbólum, False)
        return Futtatás

    def felület(Szöveg): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', SMS_küldése(Szöveg+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, szektor_pozíció, 눌림): távoli_ÉRTÉK.sendall(struct.pack('>BBHH', 5, 눌림, 가로, szektor_pozíció))

    def kattint_ÉRTÉK(가로, szektor_pozíció): 가리키기(가로, szektor_pozíció, 1); 가리키기(가로, szektor_pozíció, 0)

    def bitkép_KÉP():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tényleges_adat 너비를 쓴다.
        távoli_ÉRTÉK.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        rajz_ÉRTÉK = Image.new('RGB', (너비, 높이)); terület_ÉRTÉK_9285603e = 0
        while True:
            Altípus_ÉRTÉK = AZONOS_ÉRTÉK(távoli_ÉRTÉK, 1)[0]
            if Altípus_ÉRTÉK == 2: continue
            if Altípus_ÉRTÉK == 3:
                hossz_ÉRTÉK = struct.unpack('>I', AZONOS_ÉRTÉK(távoli_ÉRTÉK, 7)[3:])[0]; AZONOS_ÉRTÉK(távoli_ÉRTÉK, hossz_ÉRTÉK); continue
            assert Altípus_ÉRTÉK == 0, Altípus_ÉRTÉK
            cikk_DARAB = struct.unpack('>H', AZONOS_ÉRTÉK(távoli_ÉRTÉK, 3)[1:])[0]
            for _ in range(cikk_DARAB):
                가로, szektor_pozíció, 폭, hossz_ÉRTÉK, kódolás_ÉRTÉK = struct.unpack('>HHHHi', AZONOS_ÉRTÉK(távoli_ÉRTÉK, 12))
                assert kódolás_ÉRTÉK == 0 and 가로+폭 <= 너비 and szektor_pozíció+hossz_ÉRTÉK <= 높이
                rajz_ÉRTÉK.paste(Image.frombytes('RGB', (폭, hossz_ÉRTÉK), AZONOS_ÉRTÉK(távoli_ÉRTÉK, 폭*hossz_ÉRTÉK*4), 'raw', 'BGRX'), (가로, szektor_pozíció))
                terület_ÉRTÉK_9285603e += 폭*hossz_ÉRTÉK
            if terület_ÉRTÉK_9285603e:
                assert terület_ÉRTÉK_9285603e == 너비*높이, terület_ÉRTÉK_9285603e
                return rajz_ÉRTÉK

    def csekk_képpont(koordináta_ÉRTÉK, 색):
        határidő_ÉRTÉK = time.monotonic()+10
        while True:
            rajz_ÉRTÉK = bitkép_KÉP()
            if rajz_ÉRTÉK.getpixel(koordináta_ÉRTÉK) == 색: return rajz_ÉRTÉK
            if time.monotonic() > határidő_ÉRTÉK: raise AssertionError((koordináta_ÉRTÉK, rajz_ÉRTÉK.getpixel(koordináta_ÉRTÉK), 색))

    def feltölt_Files(Név, adat): átvisz_ÉRTÉK.storbinary('STOR '+Név, io.BytesIO(adat))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+méretez_SMS+' RGB32').encode() in LOG_REKORD
        print('BOOT:', méretez_SMS, flush=True)
        távoli_szám = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_REKORD).group(1))
        távoli_ÉRTÉK = socket.create_connection(('127.0.0.1', távoli_szám), timeout=20)
        assert AZONOS_ÉRTÉK(távoli_ÉRTÉK, 12) == b'RFB 003.008\n'; távoli_ÉRTÉK.sendall(b'RFB 003.008\n')
        assert 1 in AZONOS_ÉRTÉK(távoli_ÉRTÉK, AZONOS_ÉRTÉK(távoli_ÉRTÉK, 1)[0]); távoli_ÉRTÉK.sendall(b'\x01')
        assert AZONOS_ÉRTÉK(távoli_ÉRTÉK, 4) == b'\0'*4; távoli_ÉRTÉK.sendall(b'\x01')
        kiinduló_állapot = AZONOS_ÉRTÉK(távoli_ÉRTÉK, 24); assert struct.unpack('>HH', kiinduló_állapot[:4]) == (너비, 높이)
        AZONOS_ÉRTÉK(távoli_ÉRTÉK, struct.unpack('>I', kiinduló_állapot[20:])[0])
        távoli_ÉRTÉK.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        távoli_ÉRTÉK.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        csekk_képpont((너비-1, 높이-1), (24, 32, 48))
        # 화면 jog 아래까지 이동한다. Előző_cikk 640×480 határ_ÉRTÉK 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        csekk_képpont((너비-568, 높이-360), (32, 80, 144))
        Futtatás = len(LOG_REKORD); kattint_ÉRTÉK(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', Futtatás)
        csekk_képpont((너비-568, 높이-360), (24, 32, 48))
        Futtatás = len(LOG_REKORD); kattint_ÉRTÉK(80, 16); 기다리기(b'TERMINAL FOCUS 1', Futtatás)
        felület('ftpd start')
        átvisz_ÉRTÉK = ftplib.FTP(); átvisz_ÉRTÉK.encoding = 'utf-8'; átvisz_ÉRTÉK.connect('127.0.0.1', portszám, timeout=20); átvisz_ÉRTÉK.login()
        # C határ_ÉRTÉK 검사는 32비트 unsigned 음수 konvertál_ÉRTÉK·klip 밖·빈 사각형을 포함한다.
        FORRÁS = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(Rajz_téglalap(너비,높이,0,0,0)) return 2;
    if(Rajz_téglalap(너비,높이-1,1,1,0)!=-22) return 3;
    if(Rajz_téglalap(너비-1,높이,1,1,0)!=-22) return 4;
    if(Rajz_téglalap(-1,0,1,1,0)!=-22) return 5;
    if(Rajz_téglalap(0,0,-1,1,0)!=-22) return 6;
    if(Rajz_téglalap(너비-1,높이-1,1,1,0x332211)) return 7;
    ír_Fájl_adat(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        feltölt_Files('화면시험.c', FORRÁS.encode())
        assert 'exit 0' in felület('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', SMS_küldése('run /화면시험\n'))
        csekk_képpont((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', SMS_küldése('q'))
        FORRÁS = '''from magyar import 화면크기, Rajz_téglalap, 그림기다리기, Kimenet, rendszerhiba
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    Rajz_téglalap(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except rendszerhiba as HIBA:
    assert HIBA.INDEX == 22
Rajz_téglalap(너비-1, 높이-1, 1, 1, 0x665544)
Kimenet("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        feltölt_Files('화면시험.py', FORRÁS.encode())
        기다리기(b'PYTHON RESOLUTION PASS', SMS_küldése('python /화면시험.py\n'))
        csekk_képpont((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', SMS_küldése('q'))
        FORRÁS = '''import magyar.saját.*;
public class felbontás_teszt {
    public static void main(String[] Argumentumok) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new Állapot_kivétel("Méret");
        try { 화면.téglalap(너비,높이-1,1,1,0); throw new Állapot_kivétel("klip"); }
        catch (alaptalan_argumentum_kivétel HIBA) { }
        화면.töröl_bejegyzés(0x302018);
        화면.téglalap(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # kivétel 처리는 gazda javac 결과를 saját JVM에 올려 검사한다.
        határ_forrás = KR_útvonal/'해상도경계시험.java'
        határ_forrás.write_text(FORRÁS.replace('class felbontás_teszt', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(teendő_gyök/'dist/jkoros-native-korean.jar'), '-d', str(KR_útvonal), str(határ_forrás)])
        feltölt_Files('해상도경계시험.class', (KR_útvonal/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', SMS_küldése('java 해상도경계시험\n'))
        csekk_képpont((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_küldése('q'))
        # 게스트 javac의 támogat_ÉRTÉK 문법으로 Méret lekérdez_ÉRTÉK·töröl_bejegyzés·다섯 Argumentumok 그리기를 컴파일한다.
        FORRÁS = '''public class felbontás_teszt {
    public static void main(String[] Argumentumok) {
        int 너비=magyar.saját.화면.너비();
        int 높이=magyar.saját.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        magyar.saját.화면.töröl_bejegyzés(3153944);
        magyar.saját.화면.téglalap(너비-1,높이-1,1,1,10061943);
        magyar.saját.Kimenet.ír_sor("JAVA RESOLUTION PASS");
        magyar.saját.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        feltölt_Files('felbontás_teszt.java', FORRÁS.encode())
        KR = felület('javac felbontás_teszt.java'); assert 'exit 0' in KR, KR
        기다리기(b'JAVA RESOLUTION PASS', SMS_küldése('java felbontás_teszt\n'))
        csekk_képpont((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', SMS_küldése('q'))
        feltölt_Files('Szving_teszt.class', (KR_útvonal/'Szving_teszt.class').read_bytes())
        기다리기(b'SWING READY', SMS_küldése('java Szving_teszt\n'))
        가로, szektor_pozíció = (너비-400)//2, (높이-280)//2
        rajz_ÉRTÉK = csekk_képpont((가로, szektor_pozíció), (32, 80, 144))
        rajz_ÉRTÉK.save(str(KR_útvonal/(méretez_SMS+'.png')))
        Futtatás = len(LOG_REKORD); kattint_ÉRTÉK(가로+80, szektor_pozíció+155)
        기다리기('SWING CLICK Név'.encode(), Futtatás)
        Futtatás = len(LOG_REKORD); kattint_ÉRTÉK(가로+385, szektor_pozíció+15); 기다리기(b'jkoros-native> ', Futtatás)
        assert 'AFTER_RESOLUTION' in felület('echo AFTER_RESOLUTION')
        print('PASS:', méretez_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if átvisz_ÉRTÉK: átvisz_ÉRTÉK.close()
        if távoli_ÉRTÉK: távoli_ÉRTÉK.close()
        if folyamat_ÉRTÉK.poll() is None:
            folyamat_ÉRTÉK.terminate()
            try: folyamat_ÉRTÉK.wait(timeout=8)
            except subprocess.TimeoutExpired: folyamat_ÉRTÉK.kill(); folyamat_ÉRTÉK.wait()
        szelektor_a916db4e.close(); folyamat_ÉRTÉK.stdout.close()
        (KR_útvonal/(méretez_SMS+'.log')).write_bytes(LOG_REKORD)


def Futtatás():
    KR_útvonal = teendő_gyök/'build/verification/resolution'; KR_útvonal.mkdir(parents=True, exist_ok=True)
    LOG_REKORD = {'passed': False, 'kernel_sha256': hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for alaptalan_ÉRTÉK in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            KR = subprocess.run(['python3', str(teendő_gyök/'Eszközök/végrehajt_parancs.py'), '--resolution', alaptalan_ÉRTÉK], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert KR.returncode == 2 and b'--resolution' in KR.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(KR_útvonal), str(teendő_gyök/'시험/자바/Szving_teszt.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            felbontás_teszt(너비, 높이, KR_útvonal); LOG_REKORD['resolutions'].append([너비, 높이])
        LOG_REKORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (KR_útvonal/'report.json').write_text(json.dumps(LOG_REKORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Futtatás()
