#!/usr/bin/env python3
"""ຕົວ_ຈິງ_ຂໍ້ມູນ QEMU/VNC에서 화면 ຂະ_ຫນາດ·경계·ວິນໂດ 이동·Swing·언어별 그리기를 검사한다."""
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
from ເດັສທັອບ_ເບິ່ງ import 정확한값
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def 해상도시험(너비, 높이, ມາດຕະການ_ທາງໂຄຈອນ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); ຫມາຍເລກພອດ = 임시.getsockname()[1]
    ຂະ_ຫນາດ_ຂໍ້ຄວາມ = '{}x{}'.format(너비, 높이)
    ຂະ_ບວນ_ການ_ຄ່າ = subprocess.Popen(['python3', str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ຫມາຍເລກພອດ), '--resolution', ຂະ_ຫນາດ_ຂໍ້ຄວາມ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ຕົວ_ໃຊ້_ເລືອກ_a916db4e = selectors.DefaultSelector(); ຕົວ_ໃຊ້_ເລືອກ_a916db4e.register(ຂະ_ບວນ_ການ_ຄ່າ.stdout, selectors.EVENT_READ)
    ບັນທຶກ_ແຖວ = bytearray(); ທາງ_ໄກ_ຄ່າ = None; ໂອນ_ຄ່າ = None

    def 기다리기(ລາຍການ_ຄ່າ, ແລ່ນ=0):
        마감 = time.monotonic() + 60
        while ລາຍການ_ຄ່າ not in ບັນທຶກ_ແຖວ[ແລ່ນ:]:
            if time.monotonic() > 마감 or ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None or b'HALTED' in ບັນທຶກ_ແຖວ or b'PANIC:' in ບັນທຶກ_ແຖວ:
                raise AssertionError(ບັນທຶກ_ແຖວ[ແລ່ນ:].decode('utf-8', 'replace'))
            for ງານ, _ in ຕົວ_ໃຊ້_ເລືອກ_a916db4e.select(.1):
                ຂໍ້ມູນ = ງານ.fileobj.read(65536)
                if ຂໍ້ມູນ: ບັນທຶກ_ແຖວ.extend(ຂໍ້ມູນ)
        return ບັນທຶກ_ແຖວ[ແລ່ນ:].decode('utf-8', 'replace')

    def ກົດ_ປຸ່ມ(ສັນຍາລັກ, 눌림=True): ທາງ_ໄກ_ຄ່າ.sendall(struct.pack('>BBHI', 4, int(눌림), 0, ສັນຍາລັກ))

    def ສົ່ງ_ຂໍ້ຄວາມ(ຂໍ້ຄວາມ):
        ແລ່ນ = len(ບັນທຶກ_ແຖວ)
        for ຕົວອັກສອນ_ຄ່າ in ຂໍ້ຄວາມ:
            ສັນຍາລັກ = 0xff0d if ຕົວອັກສອນ_ຄ່າ == '\n' else ord(ຕົວອັກສອນ_ຄ່າ) if ord(ຕົວອັກສອນ_ຄ່າ) < 256 else 0x1000000 | ord(ຕົວອັກສອນ_ຄ່າ)
            ກົດ_ປຸ່ມ(ສັນຍາລັກ); ກົດ_ປຸ່ມ(ສັນຍາລັກ, False)
        return ແລ່ນ

    def ເຊລ(ຂໍ້ຄວາມ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ສົ່ງ_ຂໍ້ຄວາມ(ຂໍ້ຄວາມ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, 눌림): ທາງ_ໄກ_ຄ່າ.sendall(struct.pack('>BBHH', 5, 눌림, 가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ))

    def ກົດ_ຄ່າ(가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ): 가리키기(가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, 1); 가리키기(가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, 0)

    def ບິດແມັບ_ຮູບ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ຕົວ_ຈິງ_ຂໍ້ມູນ 너비를 쓴다.
        ທາງ_ໄກ_ຄ່າ.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        ການ_ແຕ້ມ_ຄ່າ = Image.new('RGB', (너비, 높이)); ຫມວດ_ຄ່າ_9285603e = 0
        while True:
            종류 = 정확한값(ທາງ_ໄກ_ຄ່າ, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                ຄວາມຍາວ_ຄ່າ = struct.unpack('>I', 정확한값(ທາງ_ໄກ_ຄ່າ, 7)[3:])[0]; 정확한값(ທາງ_ໄກ_ຄ່າ, ຄວາມຍາວ_ຄ່າ); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ທາງ_ໄກ_ຄ່າ, 3)[1:])[0]
            for _ in range(개수):
                가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ, 폭, ຄວາມຍາວ_ຄ່າ, ເຂົ້າລະຫັດ_ຄ່າ = struct.unpack('>HHHHi', 정확한값(ທາງ_ໄກ_ຄ່າ, 12))
                assert ເຂົ້າລະຫັດ_ຄ່າ == 0 and 가로+폭 <= 너비 and ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ+ຄວາມຍາວ_ຄ່າ <= 높이
                ການ_ແຕ້ມ_ຄ່າ.paste(Image.frombytes('RGB', (폭, ຄວາມຍາວ_ຄ່າ), 정확한값(ທາງ_ໄກ_ຄ່າ, 폭*ຄວາມຍາວ_ຄ່າ*4), 'raw', 'BGRX'), (가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ))
                ຫມວດ_ຄ່າ_9285603e += 폭*ຄວາມຍາວ_ຄ່າ
            if ຫມວດ_ຄ່າ_9285603e:
                assert ຫມວດ_ຄ່າ_9285603e == 너비*높이, ຫມວດ_ຄ່າ_9285603e
                return ການ_ແຕ້ມ_ຄ່າ

    def ເຊັກເງິນ_ເປ_ລ(ຈຸດປະສານ_ຄ່າ, 색):
        마감 = time.monotonic()+10
        while True:
            ການ_ແຕ້ມ_ຄ່າ = ບິດແມັບ_ຮູບ()
            if ການ_ແຕ້ມ_ຄ່າ.getpixel(ຈຸດປະສານ_ຄ່າ) == 색: return ການ_ແຕ້ມ_ຄ່າ
            if time.monotonic() > 마감: raise AssertionError((ຈຸດປະສານ_ຄ່າ, ການ_ແຕ້ມ_ຄ່າ.getpixel(ຈຸດປະສານ_ຄ່າ), 색))

    def ໂອນອອກ_ໄຟລ໌(ຊື່, ຂໍ້ມູນ): ໂອນ_ຄ່າ.storbinary('STOR '+ຊື່, io.BytesIO(ຂໍ້ມູນ))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ຂະ_ຫນາດ_ຂໍ້ຄວາມ+' RGB32').encode() in ບັນທຶກ_ແຖວ
        print('BOOT:', ຂະ_ຫນາດ_ຂໍ້ຄວາມ, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', ບັນທຶກ_ແຖວ).group(1))
        ທາງ_ໄກ_ຄ່າ = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(ທາງ_ໄກ_ຄ່າ, 12) == b'RFB 003.008\n'; ທາງ_ໄກ_ຄ່າ.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ທາງ_ໄກ_ຄ່າ, 정확한값(ທາງ_ໄກ_ຄ່າ, 1)[0]); ທາງ_ໄກ_ຄ່າ.sendall(b'\x01')
        assert 정확한값(ທາງ_ໄກ_ຄ່າ, 4) == b'\0'*4; ທາງ_ໄກ_ຄ່າ.sendall(b'\x01')
        초기 = 정확한값(ທາງ_ໄກ_ຄ່າ, 24); assert struct.unpack('>HH', 초기[:4]) == (너비, 높이)
        정확한값(ທາງ_ໄກ_ຄ່າ, struct.unpack('>I', 초기[20:])[0])
        ທາງ_ໄກ_ຄ່າ.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ທາງ_ໄກ_ຄ່າ.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        ເຊັກເງິນ_ເປ_ລ((너비-1, 높이-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        ເຊັກເງິນ_ເປ_ລ((너비-568, 높이-360), (32, 80, 144))
        ແລ່ນ = len(ບັນທຶກ_ແຖວ); ກົດ_ຄ່າ(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', ແລ່ນ)
        ເຊັກເງິນ_ເປ_ລ((너비-568, 높이-360), (24, 32, 48))
        ແລ່ນ = len(ບັນທຶກ_ແຖວ); ກົດ_ຄ່າ(80, 16); 기다리기(b'TERMINAL FOCUS 1', ແລ່ນ)
        ເຊລ('ftpd start')
        ໂອນ_ຄ່າ = ftplib.FTP(); ໂອນ_ຄ່າ.encoding = 'utf-8'; ໂອນ_ຄ່າ.connect('127.0.0.1', ຫມາຍເລກພອດ, timeout=20); ໂອນ_ຄ່າ.login()
        # C 경계 검사는 32비트 unsigned 음수 변환·ຄ_ລິບ 밖·빈 사각형을 포함한다.
        ແຫຼ່ງທີ່ມາ = '''#include <화면규약.h>
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
    ຂຽນ_ຟາຍ_ຂໍ້ມູນ(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ໂອນອອກ_ໄຟລ໌('화면시험.c', ແຫຼ່ງທີ່ມາ.encode())
        assert 'exit 0' in ເຊລ('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ສົ່ງ_ຂໍ້ຄວາມ('run /화면시험\n'))
        ເຊັກເງິນ_ເປ_ລ((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ສົ່ງ_ຂໍ້ຄວາມ('q'))
        ແຫຼ່ງທີ່ມາ = '''from 한국어 import 화면크기, 네모그리기, 그림기다리기, 출력, ລະບົບ_ຂໍ້ຜິດພາດ
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    네모그리기(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ລະບົບ_ຂໍ້ຜິດພາດ as ຂໍ້ຜິດພາດ:
    assert ຂໍ້ຜິດພາດ.ດັດຊະນີ == 22
네모그리기(너비-1, 높이-1, 1, 1, 0x665544)
출력("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ໂອນອອກ_ໄຟລ໌('화면시험.py', ແຫຼ່ງທີ່ມາ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ສົ່ງ_ຂໍ້ຄວາມ('python /화면시험.py\n'))
        ເຊັກເງິນ_ເປ_ລ((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ສົ່ງ_ຂໍ້ຄວາມ('q'))
        ແຫຼ່ງທີ່ມາ = '''import 한국어.자체.*;
public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new ສະຖານະ_ຂໍ້ຍົກເວັ້ນ("ຂະ_ຫນາດ");
        try { 화면.사각형(너비,높이-1,1,1,0); throw new ສະຖານະ_ຂໍ້ຍົກເວັ້ນ("ຄ_ລິບ"); }
        catch (ໃຊ້ບໍ່ໄດ້_ຂໍ້ພິສູດ_ຂໍ້ຍົກເວັ້ນ ຂໍ້ຜິດພາດ) { }
        화면.ລຶບ_ເຂົ້າໃນ(0x302018);
        화면.사각형(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ຂໍ້ຍົກເວັ້ນ 처리는 ໂຮສ javac 결과를 자체 JVM에 올려 검사한다.
        경계원문 = ມາດຕະການ_ທາງໂຄຈອນ/'해상도경계시험.java'
        경계원문.write_text(ແຫຼ່ງທີ່ມາ.replace('class 해상도시험', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ໂຄງ_ການ_ເລກຮາກ/'dist/jkoros-native-korean.jar'), '-d', str(ມາດຕະການ_ທາງໂຄຈອນ), str(경계원문)])
        ໂອນອອກ_ໄຟລ໌('해상도경계시험.class', (ມາດຕະການ_ທາງໂຄຈອນ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ສົ່ງ_ຂໍ້ຄວາມ('java 해상도경계시험\n'))
        ເຊັກເງິນ_ເປ_ລ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ສົ່ງ_ຂໍ້ຄວາມ('q'))
        # 게스트 javac의 ການຮອງຮັບ_ຄ່າ 문법으로 ຂະ_ຫນາດ ຄິວຣີ_ຄ່າ·ລຶບ_ເຂົ້າໃນ·다섯 인수 그리기를 컴파일한다.
        ແຫຼ່ງທີ່ມາ = '''public class 해상도시험 {
    public static void main(String[] 인수) {
        int 너비=한국어.자체.화면.너비();
        int 높이=한국어.자체.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        한국어.자체.화면.ລຶບ_ເຂົ້າໃນ(3153944);
        한국어.자체.화면.사각형(너비-1,높이-1,1,1,10061943);
        한국어.자체.출력.ຂຽນ_ສາຍ("JAVA RESOLUTION PASS");
        한국어.자체.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        ໂອນອອກ_ໄຟລ໌('해상도시험.java', ແຫຼ່ງທີ່ມາ.encode())
        ມາດຕະການ = ເຊລ('javac 해상도시험.java'); assert 'exit 0' in ມາດຕະການ, ມາດຕະການ
        기다리기(b'JAVA RESOLUTION PASS', ສົ່ງ_ຂໍ້ຄວາມ('java 해상도시험\n'))
        ເຊັກເງິນ_ເປ_ລ((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ສົ່ງ_ຂໍ້ຄວາມ('q'))
        ໂອນອອກ_ໄຟລ໌('스윙시험.class', (ມາດຕະການ_ທາງໂຄຈອນ/'스윙시험.class').read_bytes())
        기다리기(b'SWING READY', ສົ່ງ_ຂໍ້ຄວາມ('java 스윙시험\n'))
        가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ = (너비-400)//2, (높이-280)//2
        ການ_ແຕ້ມ_ຄ່າ = ເຊັກເງິນ_ເປ_ລ((가로, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ), (32, 80, 144))
        ການ_ແຕ້ມ_ຄ່າ.save(str(ມາດຕະການ_ທາງໂຄຈອນ/(ຂະ_ຫນາດ_ຂໍ້ຄວາມ+'.png')))
        ແລ່ນ = len(ບັນທຶກ_ແຖວ); ກົດ_ຄ່າ(가로+80, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ+155)
        기다리기('SWING CLICK ຊື່'.encode(), ແລ່ນ)
        ແລ່ນ = len(ບັນທຶກ_ແຖວ); ກົດ_ຄ່າ(가로+385, ລວງຕັ້ງ_ຈັດຕໍາແຫນ່ງ+15); 기다리기(b'jkoros-native> ', ແລ່ນ)
        assert 'AFTER_RESOLUTION' in ເຊລ('echo AFTER_RESOLUTION')
        print('PASS:', ຂະ_ຫນາດ_ຂໍ້ຄວາມ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if ໂອນ_ຄ່າ: ໂອນ_ຄ່າ.close()
        if ທາງ_ໄກ_ຄ່າ: ທາງ_ໄກ_ຄ່າ.close()
        if ຂະ_ບວນ_ການ_ຄ່າ.poll() is None:
            ຂະ_ບວນ_ການ_ຄ່າ.terminate()
            try: ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=8)
            except subprocess.TimeoutExpired: ຂະ_ບວນ_ການ_ຄ່າ.kill(); ຂະ_ບວນ_ການ_ຄ່າ.wait()
        ຕົວ_ໃຊ້_ເລືອກ_a916db4e.close(); ຂະ_ບວນ_ການ_ຄ່າ.stdout.close()
        (ມາດຕະການ_ທາງໂຄຈອນ/(ຂະ_ຫນາດ_ຂໍ້ຄວາມ+'.log')).write_bytes(ບັນທຶກ_ແຖວ)


def ແລ່ນ():
    ມາດຕະການ_ທາງໂຄຈອນ = ໂຄງ_ການ_ເລກຮາກ/'build/verification/resolution'; ມາດຕະການ_ທາງໂຄຈອນ.mkdir(parents=True, exist_ok=True)
    ບັນທຶກ_ແຖວ = {'passed': False, 'kernel_sha256': hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ໃຊ້ບໍ່ໄດ້_ຄ່າ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ມາດຕະການ = subprocess.run(['python3', str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ.py'), '--resolution', ໃຊ້ບໍ່ໄດ້_ຄ່າ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ມາດຕະການ.returncode == 2 and b'--resolution' in ມາດຕະການ.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ມາດຕະການ_ທາງໂຄຈອນ), str(ໂຄງ_ການ_ເລກຮາກ/'시험/자바/스윙시험.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            해상도시험(너비, 높이, ມາດຕະການ_ທາງໂຄຈອນ); ບັນທຶກ_ແຖວ['resolutions'].append([너비, 높이])
        ບັນທຶກ_ແຖວ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (ມາດຕະການ_ທາງໂຄຈອນ/'report.json').write_text(json.dumps(ບັນທຶກ_ແຖວ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': ແລ່ນ()
