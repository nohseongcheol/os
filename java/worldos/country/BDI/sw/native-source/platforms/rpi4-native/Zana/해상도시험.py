#!/usr/bin/env python3
"""halisi_data QEMU/VNC에서 화면 panga_ukubwa·경계·dirisha hamisha_thamani·Swing·언어별 그리기를 검사한다."""
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
from Eneo_kazi_Onesha import 정확한값
from tekeleza_amri import 기준


def 해상도시험(너비, 높이, 결과경로):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); namba_ya_kituo = 임시.getsockname()[1]
    panga_ukubwa_SMS = '{}x{}'.format(너비, 높이)
    Mchakato_thamani = subprocess.Popen(['python3', str(기준/'Zana/tekeleza_amri.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(namba_ya_kituo), '--resolution', panga_ukubwa_SMS], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    kiteuzi_a916db4e = selectors.DefaultSelector(); kiteuzi_a916db4e.register(Mchakato_thamani.stdout, selectors.EVENT_READ)
    batli_REKODI = bytearray(); kwa_mbali_thamani = None; hamisha_thamani_630ba093 = None

    def 기다리기(onyesha_thamani, endesha=0):
        마감 = time.monotonic() + 60
        while onyesha_thamani not in batli_REKODI[endesha:]:
            if time.monotonic() > 마감 or Mchakato_thamani.poll() is not None or b'HALTED' in batli_REKODI or b'PANIC:' in batli_REKODI:
                raise AssertionError(batli_REKODI[endesha:].decode('utf-8', 'replace'))
            for tukio, _ in kiteuzi_a916db4e.select(.1):
                data = tukio.fileobj.read(65536)
                if data: batli_REKODI.extend(data)
        return batli_REKODI[endesha:].decode('utf-8', 'replace')

    def bofya_kitufe(ishara, 눌림=True): kwa_mbali_thamani.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ishara))

    def tuma_SMS(SMS):
        endesha = len(batli_REKODI)
        for kibambo_thamani in SMS:
            ishara = 0xff0d if kibambo_thamani == '\n' else ord(kibambo_thamani) if ord(kibambo_thamani) < 256 else 0x1000000 | ord(kibambo_thamani)
            bofya_kitufe(ishara); bofya_kitufe(ishara, False)
        return endesha

    def sheli(SMS): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', tuma_SMS(SMS+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, 세로, 눌림): kwa_mbali_thamani.sendall(struct.pack('>BBHH', 5, 눌림, 가로, 세로))

    def bofya_thamani(가로, 세로): 가리키기(가로, 세로, 1); 가리키기(가로, 세로, 0)

    def taswidoti_picha():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 halisi_data 너비를 쓴다.
        kwa_mbali_thamani.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        mchoro_thamani = Image.new('RGB', (너비, 높이)); eneo_thamani = 0
        while True:
            종류 = 정확한값(kwa_mbali_thamani, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                urefu_thamani = struct.unpack('>I', 정확한값(kwa_mbali_thamani, 7)[3:])[0]; 정확한값(kwa_mbali_thamani, urefu_thamani); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(kwa_mbali_thamani, 3)[1:])[0]
            for _ in range(개수):
                가로, 세로, 폭, urefu_thamani, usimbaji_thamani = struct.unpack('>HHHHi', 정확한값(kwa_mbali_thamani, 12))
                assert usimbaji_thamani == 0 and 가로+폭 <= 너비 and 세로+urefu_thamani <= 높이
                mchoro_thamani.paste(Image.frombytes('RGB', (폭, urefu_thamani), 정확한값(kwa_mbali_thamani, 폭*urefu_thamani*4), 'raw', 'BGRX'), (가로, 세로))
                eneo_thamani += 폭*urefu_thamani
            if eneo_thamani:
                assert eneo_thamani == 너비*높이, eneo_thamani
                return mchoro_thamani

    def hundi_elepi(kiratibu_thamani, 색):
        마감 = time.monotonic()+10
        while True:
            mchoro_thamani = taswidoti_picha()
            if mchoro_thamani.getpixel(kiratibu_thamani) == 색: return mchoro_thamani
            if time.monotonic() > 마감: raise AssertionError((kiratibu_thamani, mchoro_thamani.getpixel(kiratibu_thamani), 색))

    def pakia_Faili(Jina, data): hamisha_thamani_630ba093.storbinary('STOR '+Jina, io.BytesIO(data))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+panga_ukubwa_SMS+' RGB32').encode() in batli_REKODI
        print('BOOT:', panga_ukubwa_SMS, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', batli_REKODI).group(1))
        kwa_mbali_thamani = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(kwa_mbali_thamani, 12) == b'RFB 003.008\n'; kwa_mbali_thamani.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(kwa_mbali_thamani, 정확한값(kwa_mbali_thamani, 1)[0]); kwa_mbali_thamani.sendall(b'\x01')
        assert 정확한값(kwa_mbali_thamani, 4) == b'\0'*4; kwa_mbali_thamani.sendall(b'\x01')
        초기 = 정확한값(kwa_mbali_thamani, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(kwa_mbali_thamani, struct.unpack('>I', 초기[20:])[0])
        kwa_mbali_thamani.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        kwa_mbali_thamani.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        hundi_elepi((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        hundi_elepi((너비-568, 높이-360), (32, 80, 144))
        endesha = len(batli_REKODI); bofya_thamani(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', endesha)
        hundi_elepi((너비-568, 높이-360), (24, 32, 48))
        endesha = len(batli_REKODI); bofya_thamani(80, 16); 기다리기(b'TERMINAL FOCUS 1', endesha)
        sheli('ftpd start')
        hamisha_thamani_630ba093 = ftplib.FTP(); hamisha_thamani_630ba093.encoding = 'utf-8'; hamisha_thamani_630ba093.connect('127.0.0.1', namba_ya_kituo, timeout=20); hamisha_thamani_630ba093.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·dondoo 밖·빈 사각형을 포함한다.
        chanzo = '''#include <화면규약.h>
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
    andika_faili_data(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        pakia_Faili('화면시험.c', chanzo.encode())
        assert 'exit 0' in sheli('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', tuma_SMS('run /화면시험\n'))
        hundi_elepi((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', tuma_SMS('q'))
        chanzo = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, mfumo_kosa
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except mfumo_kosa as kosa:
    assert kosa.kielezo == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        pakia_Faili('화면시험.py', chanzo.encode())
        기다리기(b'PYTHON RESOLUTION PASS', tuma_SMS('python /화면시험.py\n'))
        hundi_elepi((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', tuma_SMS('q'))
        chanzo = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new hali_vighairi("panga_ukubwa");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new hali_vighairi("dondoo"); }
        catch (batili_hoja_vighairi kosa) { }
        화면.futa_ingizo(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # vighairi 처리는 mwenyeji javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = 결과경로/'해상도경계시험.java'
        경계원문.write_text(chanzo.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'dist/jkoros-native-korean.jar'), '-d', str(결과경로), str(경계원문)])
        pakia_Faili('해상도경계시험.class', (결과경로/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', tuma_SMS('java 해상도경계시험\n'))
        hundi_elepi((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', tuma_SMS('q'))
        # 게스트 javac의 Auni_thamani 문법으로 panga_ukubwa uliza_thamani·futa_ingizo·다섯 인수 그리기를 컴파일한다.
        chanzo = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.futa_ingizo(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.andika_laini("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        pakia_Faili('해상도시험.java', chanzo.encode())
        결과 = sheli('javac 해상도시험.java'); assert 'exit 0' in 결과, 결과
        기다리기(b'JAVA RESOLUTION PASS', tuma_SMS('java 해상도시험\n'))
        hundi_elepi((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', tuma_SMS('q'))
        pakia_Faili('스윙시험.class', (결과경로/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', tuma_SMS('java 스윙시험\n'))
        가로, 세로 = (너비-400)//2, (높이-280)//2
        mchoro_thamani = hundi_elepi((가로, 세로), (32, 80, 144))
        mchoro_thamani.save(str(결과경로/(panga_ukubwa_SMS+'.png')))
        endesha = len(batli_REKODI); bofya_thamani(가로+80, 세로+155)
        기다리기('SWING CLICK Jina'.encode(), endesha)
        endesha = len(batli_REKODI); bofya_thamani(가로+385, 세로+15); 기다리기(b'jkoros-native> ', endesha)
        assert 'AFTER_RESOLUTION' in sheli('echo AFTER_RESOLUTION')
        print('PASS:', panga_ukubwa_SMS, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if hamisha_thamani_630ba093: hamisha_thamani_630ba093.close()
        if kwa_mbali_thamani: kwa_mbali_thamani.close()
        if Mchakato_thamani.poll() is None:
            Mchakato_thamani.terminate()
            try: Mchakato_thamani.wait(timeout=8)
            except subprocess.TimeoutExpired: Mchakato_thamani.kill(); Mchakato_thamani.wait()
        kiteuzi_a916db4e.close(); Mchakato_thamani.stdout.close()
        (결과경로/(panga_ukubwa_SMS+'.log')).write_bytes(batli_REKODI)


def endesha():
    결과경로 = 기준/'build/verification/resolution'; 결과경로.mkdir(parents=True, exist_ok=True)
    batli_REKODI = {'passed': False, 'kernel_sha256': hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for batili_thamani in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            결과 = subprocess.run(['python3', str(기준/'Zana/tekeleza_amri.py'), '--resolution', batili_thamani], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 결과.returncode == 2 and b'--resolution' in 결과.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(결과경로), str(기준/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, 결과경로); batli_REKODI['resolutions'].append([너비, 높이])
        batli_REKODI.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (결과경로/'report.json').write_text(json.dumps(batli_REKODI, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': endesha()
