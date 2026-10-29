#!/usr/bin/env python3
"""dữLiệuThựcTế QEMU/VNC에서 MànHình cỡ·giáTrịRanhGiới·cửaSổ giáTrịDiChuyển·Swing·언어별 그리기를 검사한다."""
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
from khungNhìnMànLàmViệc import giáTrịChínhXác
from thựcThiLệnh import gốcCâyDựÁn


def ThửĐộPhânGiải(giáTrịRộng, giáTrịCao, đườngDẫnKếtQuả):
    with socket.socket() as giáTrịTạm:
        giáTrịTạm.bind(('127.0.0.1', 0)); sốCổng = giáTrịTạm.getsockname()[1]
    vănBảnCỡ = '{}x{}'.format(giáTrịRộng, giáTrịCao)
    giáTrịTiếnTrình = subprocess.Popen(['python3', str(gốcCâyDựÁn/'CôngCụ/thựcThiLệnh.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(sốCổng), '--resolution', vănBảnCỡ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    BộChọn = selectors.DefaultSelector(); BộChọn.register(giáTrịTiếnTrình.stdout, selectors.EVENT_READ)
    bảnGhiNhậtKý = bytearray(); giáTrịTừXa = None; giáTrịChuyểnGiao = None

    def đợi(hiệnGiáTrị, chạy=0):
        giáTrịHạnChót = time.monotonic() + 60
        while hiệnGiáTrị not in bảnGhiNhậtKý[chạy:]:
            if time.monotonic() > giáTrịHạnChót or giáTrịTiếnTrình.poll() is not None or b'HALTED' in bảnGhiNhậtKý or b'PANIC:' in bảnGhiNhậtKý:
                raise AssertionError(bảnGhiNhậtKý[chạy:].decode('utf-8', 'replace'))
            for sựKiện, _ in BộChọn.select(.1):
                DữLiệu = sựKiện.fileobj.read(65536)
                if DữLiệu: bảnGhiNhậtKý.extend(DữLiệu)
        return bảnGhiNhậtKý[chạy:].decode('utf-8', 'replace')

    def nútNhấnChuột(kýHiệu, làĐãNhấn=True): giáTrịTừXa.sendall(struct.pack('>BBHI', 4, int(làĐãNhấn), 0, kýHiệu))

    def gửiVănBản(vănBản):
        chạy = len(bảnGhiNhậtKý)
        for giáTrịKýTự in vănBản:
            kýHiệu = 0xff0d if giáTrịKýTự == '\n' else ord(giáTrịKýTự) if ord(giáTrịKýTự) < 256 else 0x1000000 | ord(giáTrịKýTự)
            nútNhấnChuột(kýHiệu); nútNhấnChuột(kýHiệu, False)
        return chạy

    def vỏLệnh(vănBản): return đợi(b'\r\n__RESOLUTION_DONE__\r\n', gửiVănBản(vănBản+'; echo __RESOLUTION_DONE__\n'))

    def tạiĐiểm(vịTríNgang, vịTríDọc, làĐãNhấn): giáTrịTừXa.sendall(struct.pack('>BBHH', 5, làĐãNhấn, vịTríNgang, vịTríDọc))

    def giáTrịNhấnChuột(vịTríNgang, vịTríDọc): tạiĐiểm(vịTríNgang, vịTríDọc, 1); tạiĐiểm(vịTríNgang, vịTríDọc, 0)

    def ảnhBảnĐồBit():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 dữLiệuThựcTế 너비를 쓴다.
        giáTrịTừXa.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, giáTrịRộng, giáTrịCao))
        HìnhVẽ = Image.new('RGB', (giáTrịRộng, giáTrịCao)); giáTrịVùng = 0
        while True:
            giáTrịLoại = giáTrịChínhXác(giáTrịTừXa, 1)[0]
            if giáTrịLoại == 2: continue
            if giáTrịLoại == 3:
                độDài = struct.unpack('>I', giáTrịChínhXác(giáTrịTừXa, 7)[3:])[0]; giáTrịChínhXác(giáTrịTừXa, độDài); continue
            assert giáTrịLoại == 0, giáTrịLoại
            sốLượngPhầnMục = struct.unpack('>H', giáTrịChínhXác(giáTrịTừXa, 3)[1:])[0]
            for _ in range(sốLượngPhầnMục):
                vịTríNgang, vịTríDọc, khoảngTrảiRộng, độDài, giáTrịBảngMã = struct.unpack('>HHHHi', giáTrịChínhXác(giáTrịTừXa, 12))
                assert giáTrịBảngMã == 0 and vịTríNgang+khoảngTrảiRộng <= giáTrịRộng and vịTríDọc+độDài <= giáTrịCao
                HìnhVẽ.paste(Image.frombytes('RGB', (khoảngTrảiRộng, độDài), giáTrịChínhXác(giáTrịTừXa, khoảngTrảiRộng*độDài*4), 'raw', 'BGRX'), (vịTríNgang, vịTríDọc))
                giáTrịVùng += khoảngTrảiRộng*độDài
            if giáTrịVùng:
                assert giáTrịVùng == giáTrịRộng*giáTrịCao, giáTrịVùng
                return HìnhVẽ

    def kiểmTraĐiểmẢnh(giáTrịTọaĐộ, giáTrịMàu):
        giáTrịHạnChót = time.monotonic()+10
        while True:
            HìnhVẽ = ảnhBảnĐồBit()
            if HìnhVẽ.getpixel(giáTrịTọaĐộ) == giáTrịMàu: return HìnhVẽ
            if time.monotonic() > giáTrịHạnChót: raise AssertionError((giáTrịTọaĐộ, HìnhVẽ.getpixel(giáTrịTọaĐộ), giáTrịMàu))

    def cácTệpTảiLên(tên, DữLiệu): giáTrịChuyểnGiao.storbinary('STOR '+tên, io.BytesIO(DữLiệu))

    try:
        đợi(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+vănBảnCỡ+' RGB32').encode() in bảnGhiNhậtKý
        print('BOOT:', vănBảnCỡ, flush=True)
        sốTừXa = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', bảnGhiNhậtKý).group(1))
        giáTrịTừXa = socket.create_connection(('127.0.0.1', sốTừXa), timeout=20)
        assert giáTrịChínhXác(giáTrịTừXa, 12) == b'RFB 003.008\n'; giáTrịTừXa.sendall(b'RFB 003.008\n')
        assert 1 in giáTrịChínhXác(giáTrịTừXa, giáTrịChínhXác(giáTrịTừXa, 1)[0]); giáTrịTừXa.sendall(b'\x01')
        assert giáTrịChínhXác(giáTrịTừXa, 4) == b'\0'*4; giáTrịTừXa.sendall(b'\x01')
        trạngTháiBanĐầu = giáTrịChínhXác(giáTrịTừXa, 24); assert struct.unpack('>HH', trạngTháiBanĐầu[:4]) == (giáTrịRộng, giáTrịCao)
        giáTrịChínhXác(giáTrịTừXa, struct.unpack('>I', trạngTháiBanĐầu[20:])[0])
        giáTrịTừXa.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        giáTrịTừXa.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        kiểmTraĐiểmẢnh((giáTrịRộng-1, giáTrịCao-1), (24, 32, 48))
        # MànHình phải 아래까지 이동한다. phầnMụcTrướcĐó 640×480 giáTrịRanhGiới 밖에서 X를 누른다.
        tạiĐiểm(40, 60, 1); tạiĐiểm(giáTrịRộng-568+28, giáTrịCao-360+12, 1); tạiĐiểm(giáTrịRộng-568+28, giáTrịCao-360+12, 0)
        kiểmTraĐiểmẢnh((giáTrịRộng-568, giáTrịCao-360), (32, 80, 144))
        chạy = len(bảnGhiNhậtKý); giáTrịNhấnChuột(giáTrịRộng-20, giáTrịCao-345); đợi(b'TERMINAL FOCUS 1', chạy)
        kiểmTraĐiểmẢnh((giáTrịRộng-568, giáTrịCao-360), (24, 32, 48))
        chạy = len(bảnGhiNhậtKý); giáTrịNhấnChuột(80, 16); đợi(b'TERMINAL FOCUS 1', chạy)
        vỏLệnh('ftpd start')
        giáTrịChuyểnGiao = ftplib.FTP(); giáTrịChuyểnGiao.encoding = 'utf-8'; giáTrịChuyểnGiao.connect('127.0.0.1', sốCổng, timeout=20); giáTrịChuyểnGiao.login()
        # C giáTrịRanhGiới 검사는 32비트 unsigned giáTrịÂm chuyểnĐổiGiáTrị·cắtXén 밖·빈 사각형을 포함한다.
        mãNguồn = '''#include <ABIMànHình.h>
#include <ABITệp.h>
int main(void) {
    unsigned giáTrịRộng=rộngMànHình(), giáTrịCao=caoMànHình();
    if(giáTrịRộng!=WIDTH || giáTrịCao!=HEIGHT) return 1;
    if(vẽHìnhChữNhật(giáTrịRộng,giáTrịCao,0,0,0)) return 2;
    if(vẽHìnhChữNhật(giáTrịRộng,giáTrịCao-1,1,1,0)!=-22) return 3;
    if(vẽHìnhChữNhật(giáTrịRộng-1,giáTrịCao,1,1,0)!=-22) return 4;
    if(vẽHìnhChữNhật(-1,0,1,1,0)!=-22) return 5;
    if(vẽHìnhChữNhật(0,0,-1,1,0)!=-22) return 6;
    if(vẽHìnhChữNhật(giáTrịRộng-1,giáTrịCao-1,1,1,0x332211)) return 7;
    ghiDữLiệuTệp(1,"C RESOLUTION PASS\\n",18);
    chờBảnVẽCho(); return 0;
}
'''.replace('WIDTH', str(giáTrịRộng)).replace('HEIGHT', str(giáTrịCao))
        cácTệpTảiLên('thửMànHình.c', mãNguồn.encode())
        assert 'exit 0' in vỏLệnh('cc /thửMànHình.c -o /thửMànHình')
        đợi(b'C RESOLUTION PASS', gửiVănBản('run /thửMànHình\n'))
        kiểmTraĐiểmẢnh((giáTrịRộng-1, giáTrịCao-1), (17, 34, 51))
        đợi(b'jkoros-native> ', gửiVănBản('q'))
        mãNguồn = '''from tiếngViệt import cỡMànHình, vẽHìnhChữNhật, chờBảnVẽCho, ĐầuRa, LỗiHệThống
giáTrịRộng, giáTrịCao = cỡMànHình()
assert (giáTrịRộng, giáTrịCao) == (WIDTH, HEIGHT)
try:
    vẽHìnhChữNhật(giáTrịRộng, giáTrịCao-1, 1, 1, 0)
    raise AssertionError("boundary")
except LỗiHệThống as lỗi:
    assert lỗi.sốHiệu == 22
vẽHìnhChữNhật(giáTrịRộng-1, giáTrịCao-1, 1, 1, 0x665544)
ĐầuRa("PYTHON RESOLUTION PASS")
chờBảnVẽCho()
'''.replace('WIDTH', str(giáTrịRộng)).replace('HEIGHT', str(giáTrịCao))
        cácTệpTảiLên('thửMànHình.py', mãNguồn.encode())
        đợi(b'PYTHON RESOLUTION PASS', gửiVănBản('python /thửMànHình.py\n'))
        kiểmTraĐiểmẢnh((giáTrịRộng-1, giáTrịCao-1), (68, 85, 102))
        đợi(b'jkoros-native> ', gửiVănBản('q'))
        mãNguồn = '''import tiếngViệt.tựThân.*;
public class ThửĐộPhânGiải {
    public static void main(String[] cácĐốiSố) {
        int giáTrịRộng=MànHình.giáTrịRộng(), giáTrịCao=MànHình.giáTrịCao();
        if (giáTrịRộng!=WIDTH || giáTrịCao!=HEIGHT) throw new NgoạiLệTrạngThái("cỡ");
        try { MànHình.hìnhChữNhật(giáTrịRộng,giáTrịCao-1,1,1,0); throw new NgoạiLệTrạngThái("cắtXén"); }
        catch (NgoạiLệĐốiSốKhôngHợpLệ lỗi) { }
        MànHình.xóaMục(0x302018);
        MànHình.hìnhChữNhật(giáTrịRộng-1,giáTrịCao-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        MànHình.đợi();
    }
}
'''.replace('WIDTH', str(giáTrịRộng)).replace('HEIGHT', str(giáTrịCao))
        # ngoạiLệ 처리는 Chủ javac 결과를 tựThân JVM에 올려 검사한다.
        nguồnRanhGiới = đườngDẫnKếtQuả/'해상도경계시험.java'
        nguồnRanhGiới.write_text(mãNguồn.replace('class ThửĐộPhânGiải', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(gốcCâyDựÁn/'dist/jkoros-native-korean.jar'), '-d', str(đườngDẫnKếtQuả), str(nguồnRanhGiới)])
        cácTệpTảiLên('해상도경계시험.class', (đườngDẫnKếtQuả/'해상도경계시험.class').read_bytes())
        đợi(b'JAVA RESOLUTION PASS', gửiVănBản('java 해상도경계시험\n'))
        kiểmTraĐiểmẢnh((giáTrịRộng-1, giáTrịCao-1), (119, 136, 153))
        đợi(b'jkoros-native> ', gửiVănBản('q'))
        # 게스트 javac의 giáTrịHỗTrợ 문법으로 cỡ giáTrịTruyVấn·xóaMục·다섯 cácĐốiSố 그리기를 컴파일한다.
        mãNguồn = '''public class ThửĐộPhânGiải {
    public static void main(String[] cácĐốiSố) {
        int giáTrịRộng=tiếngViệt.tựThân.MànHình.giáTrịRộng();
        int giáTrịCao=tiếngViệt.tựThân.MànHình.giáTrịCao();
        if (giáTrịRộng!=WIDTH || giáTrịCao!=HEIGHT) return;
        tiếngViệt.tựThân.MànHình.xóaMục(3153944);
        tiếngViệt.tựThân.MànHình.hìnhChữNhật(giáTrịRộng-1,giáTrịCao-1,1,1,10061943);
        tiếngViệt.tựThân.ĐầuRa.ghiDòng("JAVA RESOLUTION PASS");
        tiếngViệt.tựThân.MànHình.đợi();
    }
}
'''.replace('WIDTH', str(giáTrịRộng)).replace('HEIGHT', str(giáTrịCao))
        cácTệpTảiLên('ThửĐộPhânGiải.java', mãNguồn.encode())
        kếtQuả = vỏLệnh('javac ThửĐộPhânGiải.java'); assert 'exit 0' in kếtQuả, kếtQuả
        đợi(b'JAVA RESOLUTION PASS', gửiVănBản('java ThửĐộPhânGiải\n'))
        kiểmTraĐiểmẢnh((giáTrịRộng-1, giáTrịCao-1), (119, 136, 153))
        đợi(b'jkoros-native> ', gửiVănBản('q'))
        cácTệpTảiLên('ThửSwing.class', (đườngDẫnKếtQuả/'ThửSwing.class').read_bytes())
        đợi(b'SWING READY', gửiVănBản('java ThửSwing\n'))
        vịTríNgang, vịTríDọc = (giáTrịRộng-400)//2, (giáTrịCao-280)//2
        HìnhVẽ = kiểmTraĐiểmẢnh((vịTríNgang, vịTríDọc), (32, 80, 144))
        HìnhVẽ.save(str(đườngDẫnKếtQuả/(vănBảnCỡ+'.png')))
        chạy = len(bảnGhiNhậtKý); giáTrịNhấnChuột(vịTríNgang+80, vịTríDọc+155)
        đợi('SWING CLICK tên'.encode(), chạy)
        chạy = len(bảnGhiNhậtKý); giáTrịNhấnChuột(vịTríNgang+385, vịTríDọc+15); đợi(b'jkoros-native> ', chạy)
        assert 'AFTER_RESOLUTION' in vỏLệnh('echo AFTER_RESOLUTION')
        print('PASS:', vănBảnCỡ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if giáTrịChuyểnGiao: giáTrịChuyểnGiao.close()
        if giáTrịTừXa: giáTrịTừXa.close()
        if giáTrịTiếnTrình.poll() is None:
            giáTrịTiếnTrình.terminate()
            try: giáTrịTiếnTrình.wait(timeout=8)
            except subprocess.TimeoutExpired: giáTrịTiếnTrình.kill(); giáTrịTiếnTrình.wait()
        BộChọn.close(); giáTrịTiếnTrình.stdout.close()
        (đườngDẫnKếtQuả/(vănBảnCỡ+'.log')).write_bytes(bảnGhiNhậtKý)


def chạy():
    đườngDẫnKếtQuả = gốcCâyDựÁn/'build/verification/resolution'; đườngDẫnKếtQuả.mkdir(parents=True, exist_ok=True)
    bảnGhiNhậtKý = {'passed': False, 'kernel_sha256': hashlib.sha256((gốcCâyDựÁn/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for giáTrịKhôngHợpLệ in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            kếtQuả = subprocess.run(['python3', str(gốcCâyDựÁn/'CôngCụ/thựcThiLệnh.py'), '--resolution', giáTrịKhôngHợpLệ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert kếtQuả.returncode == 2 and b'--resolution' in kếtQuả.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(đườngDẫnKếtQuả), str(gốcCâyDựÁn/'KiểmThử/Java/ThửSwing.java')])
        for giáTrịRộng, giáTrịCao in ((1920,1080), (1280,720), (640,480)):
            ThửĐộPhânGiải(giáTrịRộng, giáTrịCao, đườngDẫnKếtQuả); bảnGhiNhậtKý['resolutions'].append([giáTrịRộng, giáTrịCao])
        bảnGhiNhậtKý.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (đườngDẫnKếtQuả/'report.json').write_text(json.dumps(bảnGhiNhậtKý, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': chạy()
