#!/usr/bin/env python3
"""tūturu_raraunga QEMU/VNC에서 화면 rahi·경계·matapihi nuku_uara·Swing·언어별 그리기를 검사한다."""
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
from papamahi_tiro import EXACT_uara
from kawe_tono import whakaatu_pūtake


def 해상도시험(너비, 높이, mēhua_ara):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); 접속번호 = 임시.getsockname()[1]
    rahi_TEXT = '{}x{}'.format(너비, 높이)
    Hātepe_uara = subprocess.Popen(['python3', str(whakaatu_pūtake/'Ngā_Utauta/kawe_tono.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(접속번호), '--resolution', rahi_TEXT], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    pūtīpako_a916db4e = selectors.DefaultSelector(); pūtīpako_a916db4e.register(Hātepe_uara.stdout, selectors.EVENT_READ)
    LOG_RECORD = bytearray(); mamao_uara = None; whakawhiti_uara_630ba093 = None

    def 기다리기(whakaatu_uara, whakahaere=0):
        마감 = time.monotonic() + 60
        while whakaatu_uara not in LOG_RECORD[whakahaere:]:
            if time.monotonic() > 마감 or Hātepe_uara.poll() is not None or b'HALTED' in LOG_RECORD or b'PANIC:' in LOG_RECORD:
                raise AssertionError(LOG_RECORD[whakahaere:].decode('utf-8', 'replace'))
            for hui, _ in pūtīpako_a916db4e.select(.1):
                raraunga = hui.fileobj.read(65536)
                if raraunga: LOG_RECORD.extend(raraunga)
        return LOG_RECORD[whakahaere:].decode('utf-8', 'replace')

    def pāwhiri_pātene(tohu, 눌림=True): mamao_uara.sendall(struct.pack('>BBHI', 4, int(눌림), 0, tohu))

    def tuku_kuputuhi(Ngā_kupu):
        whakahaere = len(LOG_RECORD)
        for pūāhua_uara in Ngā_kupu:
            tohu = 0xff0d if pūāhua_uara == '\n' else ord(pūāhua_uara) if ord(pūāhua_uara) < 256 else 0x1000000 | ord(pūāhua_uara)
            pāwhiri_pātene(tohu); pāwhiri_pātene(tohu, False)
        return whakahaere

    def anga(Ngā_kupu): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', tuku_kuputuhi(Ngā_kupu+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, Poutū_tūranga, 눌림): mamao_uara.sendall(struct.pack('>BBHH', 5, 눌림, 가로, Poutū_tūranga))

    def pāwhiri_uara(가로, Poutū_tūranga): 가리키기(가로, Poutū_tūranga, 1); 가리키기(가로, Poutū_tūranga, 0)

    def maheremoka_IMAGE():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 tūturu_raraunga 너비를 쓴다.
        mamao_uara.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        tātuhi_uara = Image.new('RGB', (너비, 높이)); kāwai_uara_9285603e = 0
        while True:
            종류 = EXACT_uara(mamao_uara, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                roa_uara = struct.unpack('>I', EXACT_uara(mamao_uara, 7)[3:])[0]; EXACT_uara(mamao_uara, roa_uara); continue
            assert 종류 == 0, 종류
            tuemi_COUNT = struct.unpack('>H', EXACT_uara(mamao_uara, 3)[1:])[0]
            for _ in range(tuemi_COUNT):
                가로, Poutū_tūranga, 폭, roa_uara, whakawaehere_uara = struct.unpack('>HHHHi', EXACT_uara(mamao_uara, 12))
                assert whakawaehere_uara == 0 and 가로+폭 <= 너비 and Poutū_tūranga+roa_uara <= 높이
                tātuhi_uara.paste(Image.frombytes('RGB', (폭, roa_uara), EXACT_uara(mamao_uara, 폭*roa_uara*4), 'raw', 'BGRX'), (가로, Poutū_tūranga))
                kāwai_uara_9285603e += 폭*roa_uara
            if kāwai_uara_9285603e:
                assert kāwai_uara_9285603e == 너비*높이, kāwai_uara_9285603e
                return tātuhi_uara

    def taki_pika(ruruku_uara, 색):
        마감 = time.monotonic()+10
        while True:
            tātuhi_uara = maheremoka_IMAGE()
            if tātuhi_uara.getpixel(ruruku_uara) == 색: return tātuhi_uara
            if time.monotonic() > 마감: raise AssertionError((ruruku_uara, tātuhi_uara.getpixel(ruruku_uara), 색))

    def tukuatu_Ngā_Kōnae(Ingoa, raraunga): whakawhiti_uara_630ba093.storbinary('STOR '+Ingoa, io.BytesIO(raraunga))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+rahi_TEXT+' RGB32').encode() in LOG_RECORD
        print('BOOT:', rahi_TEXT, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', LOG_RECORD).group(1))
        mamao_uara = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert EXACT_uara(mamao_uara, 12) == b'RFB 003.008\n'; mamao_uara.sendall(b'RFB 003.008\n')
        assert 1 in EXACT_uara(mamao_uara, EXACT_uara(mamao_uara, 1)[0]); mamao_uara.sendall(b'\x01')
        assert EXACT_uara(mamao_uara, 4) == b'\0'*4; mamao_uara.sendall(b'\x01')
        초기 = EXACT_uara(mamao_uara, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        EXACT_uara(mamao_uara, struct.unpack('>I', 초기[20:])[0])
        mamao_uara.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        mamao_uara.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        taki_pika((너비-1, 높이-1), (24, 32, 48))
        # 화면 RIGHT 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        taki_pika((너비-568, 높이-360), (32, 80, 144))
        whakahaere = len(LOG_RECORD); pāwhiri_uara(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', whakahaere)
        taki_pika((너비-568, 높이-360), (24, 32, 48))
        whakahaere = len(LOG_RECORD); pāwhiri_uara(80, 16); 기다리기(b'TERMINAL FOCUS 1', whakahaere)
        anga('ftpd start')
        whakawhiti_uara_630ba093 = ftplib.FTP(); whakawhiti_uara_630ba093.encoding = 'utf-8'; whakawhiti_uara_630ba093.connect('127.0.0.1', 접속번호, timeout=20); whakawhiti_uara_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 CONVERT_uara·topenga 밖·빈 사각형을 포함한다.
        pūtake = '''#include <화면규약.h>
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
    tuhi_kōnae_raraunga(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        tukuatu_Ngā_Kōnae('화면시험.c', pūtake.encode())
        assert 'exit 0' in anga('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', tuku_kuputuhi('run /화면시험\n'))
        taki_pika((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', tuku_kuputuhi('q'))
        pūtake = '''from Reo_Māori import 화면크기, 네모그리기, 그림기다리기, 출력, pūnaha_hapa
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except pūnaha_hapa as Pōhēhē:
    assert Pōhēhē.INDEX == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        tukuatu_Ngā_Kōnae('화면시험.py', pūtake.encode())
        기다리기(b'PYTHON RESOLUTION PASS', tuku_kuputuhi('python /화면시험.py\n'))
        taki_pika((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', tuku_kuputuhi('q'))
        pūtake = '''import Reo_Māori.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new 상태예외("rahi");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new 상태예외("topenga"); }
        catch (잘못된인수예외 Pōhēhē) { }
        화면.지우기(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # 예외 처리는 taurima javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = mēhua_ara/'해상도경계시험.java'
        경계원문.write_text(pūtake.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(whakaatu_pūtake/'dist/jkoros-native-korean.jar'), '-d', str(mēhua_ara), str(경계원문)])
        tukuatu_Ngā_Kōnae('해상도경계시험.class', (mēhua_ara/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', tuku_kuputuhi('java 해상도경계시험\n'))
        taki_pika((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', tuku_kuputuhi('q'))
        # 게스트 javac의 Tautoko_uara 문법으로 rahi uiui_uara·지우기·다섯 인수 그리기를 컴파일한다.
        pūtake = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=Reo_Māori.자체.화면.너비();
        int 높이=Reo_Māori.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        Reo_Māori.자체.화면.지우기(3153944);
        Reo_Māori.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        Reo_Māori.자체.출력.tuhi_hononga("JAVA RESOLUTION PASS");
        Reo_Māori.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        tukuatu_Ngā_Kōnae('해상도시험.java', pūtake.encode())
        mēhua = anga('javac 해상도시험.java'); assert 'exit 0' in mēhua, mēhua
        기다리기(b'JAVA RESOLUTION PASS', tuku_kuputuhi('java 해상도시험\n'))
        taki_pika((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', tuku_kuputuhi('q'))
        tukuatu_Ngā_Kōnae('스윙시험.class', (mēhua_ara/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', tuku_kuputuhi('java 스윙시험\n'))
        가로, Poutū_tūranga = (너비-400)//2, (높이-280)//2
        tātuhi_uara = taki_pika((가로, Poutū_tūranga), (32, 80, 144))
        tātuhi_uara.save(str(mēhua_ara/(rahi_TEXT+'.png')))
        whakahaere = len(LOG_RECORD); pāwhiri_uara(가로+80, Poutū_tūranga+155)
        기다리기('SWING CLICK Ingoa'.encode(), whakahaere)
        whakahaere = len(LOG_RECORD); pāwhiri_uara(가로+385, Poutū_tūranga+15); 기다리기(b'jkoros-native> ', whakahaere)
        assert 'AFTER_RESOLUTION' in anga('echo AFTER_RESOLUTION')
        print('PASS:', rahi_TEXT, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if whakawhiti_uara_630ba093: whakawhiti_uara_630ba093.close()
        if mamao_uara: mamao_uara.close()
        if Hātepe_uara.poll() is None:
            Hātepe_uara.terminate()
            try: Hātepe_uara.wait(timeout=8)
            except subprocess.TimeoutExpired: Hātepe_uara.kill(); Hātepe_uara.wait()
        pūtīpako_a916db4e.close(); Hātepe_uara.stdout.close()
        (mēhua_ara/(rahi_TEXT+'.log')).write_bytes(LOG_RECORD)


def whakahaere():
    mēhua_ara = whakaatu_pūtake/'build/verification/resolution'; mēhua_ara.mkdir(parents=True, exist_ok=True)
    LOG_RECORD = {'passed': False, 'kernel_sha256': hashlib.sha256((whakaatu_pūtake/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for muhu_uara in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            mēhua = subprocess.run(['python3', str(whakaatu_pūtake/'Ngā_Utauta/kawe_tono.py'), '--resolution', muhu_uara], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert mēhua.returncode == 2 and b'--resolution' in mēhua.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(mēhua_ara), str(whakaatu_pūtake/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, mēhua_ara); LOG_RECORD['resolutions'].append([너비, 높이])
        LOG_RECORD.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (mēhua_ara/'report.json').write_text(json.dumps(LOG_RECORD, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': whakahaere()
