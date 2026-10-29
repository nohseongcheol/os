#!/usr/bin/env python3
"""実際データ QEMU/VNC에서 画面 容量·境界位置値·窓 移動値·Swing·언어별 그리기를 검사한다."""
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
from デスクトップ表示像 import 厳密値
from 命令実行 import 計画根


def 解像度試験(幅値, 高さ値, 結果経路):
    with socket.socket() as 一時値:
        一時値.bind(('127.0.0.1', 0)); ポート番号 = 一時値.getsockname()[1]
    容量本文 = '{}x{}'.format(幅値, 高さ値)
    プロセス値 = subprocess.Popen(['python3', str(計画根/'道具/命令実行.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(ポート番号), '--resolution', 容量本文], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    選択器 = selectors.DefaultSelector(); 選択器.register(プロセス値.stdout, selectors.EVENT_READ)
    履歴記録記録 = bytearray(); 遠隔値 = None; 転送値 = None

    def 待機(値表示, 起動処理=0):
        期限値 = time.monotonic() + 60
        while 値表示 not in 履歴記録記録[起動処理:]:
            if time.monotonic() > 期限値 or プロセス値.poll() is not None or b'HALTED' in 履歴記録記録 or b'PANIC:' in 履歴記録記録:
                raise AssertionError(履歴記録記録[起動処理:].decode('utf-8', 'replace'))
            for イベント, _ in 選択器.select(.1):
                データ = イベント.fileobj.read(65536)
                if データ: 履歴記録記録.extend(データ)
        return 履歴記録記録[起動処理:].decode('utf-8', 'replace')

    def クリックボタン(記号, 判定押下済み=True): 遠隔値.sendall(struct.pack('>BBHI', 4, int(判定押下済み), 0, 記号))

    def 本文送信(文):
        起動処理 = len(履歴記録記録)
        for 文字値 in 文:
            記号 = 0xff0d if 文字値 == '\n' else ord(文字値) if ord(文字値) < 256 else 0x1000000 | ord(文字値)
            クリックボタン(記号); クリックボタン(記号, False)
        return 起動処理

    def シェル(文): return 待機(b'\r\n__RESOLUTION_DONE__\r\n', 本文送信(文+'; echo __RESOLUTION_DONE__\n'))

    def 点位置(水平位置, 垂直位置, 判定押下済み): 遠隔値.sendall(struct.pack('>BBHH', 5, 判定押下済み, 水平位置, 垂直位置))

    def クリック値(水平位置, 垂直位置): 点位置(水平位置, 垂直位置, 1); 点位置(水平位置, 垂直位置, 0)

    def ビットマップイメージ():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 実際データ 너비를 쓴다.
        遠隔値.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 幅値, 高さ値))
        描画 = Image.new('RGB', (幅値, 高さ値)); 面積値 = 0
        while True:
            種別値 = 厳密値(遠隔値, 1)[0]
            if 種別値 == 2: continue
            if 種別値 == 3:
                長さ = struct.unpack('>I', 厳密値(遠隔値, 7)[3:])[0]; 厳密値(遠隔値, 長さ); continue
            assert 種別値 == 0, 種別値
            項目個数 = struct.unpack('>H', 厳密値(遠隔値, 3)[1:])[0]
            for _ in range(項目個数):
                水平位置, 垂直位置, 幅跨域, 長さ, 符号化状態値 = struct.unpack('>HHHHi', 厳密値(遠隔値, 12))
                assert 符号化状態値 == 0 and 水平位置+幅跨域 <= 幅値 and 垂直位置+長さ <= 高さ値
                描画.paste(Image.frombytes('RGB', (幅跨域, 長さ), 厳密値(遠隔値, 幅跨域*長さ*4), 'raw', 'BGRX'), (水平位置, 垂直位置))
                面積値 += 幅跨域*長さ
            if 面積値:
                assert 面積値 == 幅値*高さ値, 面積値
                return 描画

    def 画素検査(座標値, 色値):
        期限値 = time.monotonic()+10
        while True:
            描画 = ビットマップイメージ()
            if 描画.getpixel(座標値) == 色値: return 描画
            if time.monotonic() > 期限値: raise AssertionError((座標値, 描画.getpixel(座標値), 色値))

    def 送出転送ファイル群(名前, データ): 転送値.storbinary('STOR '+名前, io.BytesIO(データ))

    try:
        待機(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+容量本文+' RGB32').encode() in 履歴記録記録
        print('BOOT:', 容量本文, flush=True)
        遠隔番号 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', 履歴記録記録).group(1))
        遠隔値 = socket.create_connection(('127.0.0.1', 遠隔番号), timeout=20)
        assert 厳密値(遠隔値, 12) == b'RFB 003.008\n'; 遠隔値.sendall(b'RFB 003.008\n')
        assert 1 in 厳密値(遠隔値, 厳密値(遠隔値, 1)[0]); 遠隔値.sendall(b'\x01')
        assert 厳密値(遠隔値, 4) == b'\0'*4; 遠隔値.sendall(b'\x01')
        初期状況 = 厳密値(遠隔値, 24); assert struct.unpack('>HH', 初期状況[:4]) == (幅値, 高さ値)
        厳密値(遠隔値, struct.unpack('>I', 初期状況[20:])[0])
        遠隔値.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        遠隔値.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        画素検査((幅値-1, 高さ値-1), (24, 32, 48))
        # 画面 右 아래까지 이동한다. 前回項目 640×480 境界位置値 밖에서 X를 누른다.
        点位置(40, 60, 1); 点位置(幅値-568+28, 高さ値-360+12, 1); 点位置(幅値-568+28, 高さ値-360+12, 0)
        画素検査((幅値-568, 高さ値-360), (32, 80, 144))
        起動処理 = len(履歴記録記録); クリック値(幅値-20, 高さ値-345); 待機(b'TERMINAL FOCUS 1', 起動処理)
        画素検査((幅値-568, 高さ値-360), (24, 32, 48))
        起動処理 = len(履歴記録記録); クリック値(80, 16); 待機(b'TERMINAL FOCUS 1', 起動処理)
        シェル('ftpd start')
        転送値 = ftplib.FTP(); 転送値.encoding = 'utf-8'; 転送値.connect('127.0.0.1', ポート番号, timeout=20); 転送値.login()
        # C 境界位置値 검사는 32비트 unsigned 負数値 値変換·切抜き 밖·빈 사각형을 포함한다.
        ソース = '''#include <画面ABI.h>
#include <ファイルABI.h>
int main(void) {
    unsigned 幅値=画面幅(), 高さ値=画面高さ();
    if(幅値!=WIDTH || 高さ値!=HEIGHT) return 1;
    if(矩形描画処理(幅値,高さ値,0,0,0)) return 2;
    if(矩形描画処理(幅値,高さ値-1,1,1,0)!=-22) return 3;
    if(矩形描画処理(幅値-1,高さ値,1,1,0)!=-22) return 4;
    if(矩形描画処理(-1,0,1,1,0)!=-22) return 5;
    if(矩形描画処理(0,0,-1,1,0)!=-22) return 6;
    if(矩形描画処理(幅値-1,高さ値-1,1,1,0x332211)) return 7;
    ファイルデータ書込(1,"C RESOLUTION PASS\\n",18);
    対象描画中待合(); return 0;
}
'''.replace('WIDTH', str(幅値)).replace('HEIGHT', str(高さ値))
        送出転送ファイル群('画面試験.c', ソース.encode())
        assert 'exit 0' in シェル('cc /画面試験.c -o /画面試験')
        待機(b'C RESOLUTION PASS', 本文送信('run /画面試験\n'))
        画素検査((幅値-1, 高さ値-1), (17, 34, 51))
        待機(b'jkoros-native> ', 本文送信('q'))
        ソース = '''from 日本語 import 画面容量, 矩形描画処理, 対象描画中待合, 出力, システムエラー
幅値, 高さ値 = 画面容量()
assert (幅値, 高さ値) == (WIDTH, HEIGHT)
try:
    矩形描画処理(幅値, 高さ値-1, 1, 1, 0)
    raise AssertionError("boundary")
except システムエラー as エラー:
    assert エラー.番号 == 22
矩形描画処理(幅値-1, 高さ値-1, 1, 1, 0x665544)
出力("PYTHON RESOLUTION PASS")
対象描画中待合()
'''.replace('WIDTH', str(幅値)).replace('HEIGHT', str(高さ値))
        送出転送ファイル群('画面試験.py', ソース.encode())
        待機(b'PYTHON RESOLUTION PASS', 本文送信('python /画面試験.py\n'))
        画素検査((幅値-1, 高さ値-1), (68, 85, 102))
        待機(b'jkoros-native> ', 本文送信('q'))
        ソース = '''import 日本語.内蔵.*;
public class 解像度試験 {
    public static void main(String[] 引数) {
        int 幅値=画面.幅値(), 高さ値=画面.高さ値();
        if (幅値!=WIDTH || 高さ値!=HEIGHT) throw new 状況例外("容量");
        try { 画面.矩形(幅値,高さ値-1,1,1,0); throw new 状況例外("切抜き"); }
        catch (無効引数例外 エラー) { }
        画面.入口消去処理(0x302018);
        画面.矩形(幅値-1,高さ値-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        画面.待機();
    }
}
'''.replace('WIDTH', str(幅値)).replace('HEIGHT', str(高さ値))
        # 例外 처리는 ホスト javac 결과를 内蔵 JVM에 올려 검사한다.
        境界位置ソース = 結果経路/'해상도경계시험.java'
        境界位置ソース.write_text(ソース.replace('class 解像度試験', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(計画根/'dist/jkoros-native-korean.jar'), '-d', str(結果経路), str(境界位置ソース)])
        送出転送ファイル群('해상도경계시험.class', (結果経路/'해상도경계시험.class').read_bytes())
        待機(b'JAVA RESOLUTION PASS', 本文送信('java 해상도경계시험\n'))
        画素検査((幅値-1, 高さ値-1), (119, 136, 153))
        待機(b'jkoros-native> ', 本文送信('q'))
        # 게스트 javac의 支援値 문법으로 容量 照会値·入口消去処理·다섯 引数 그리기를 컴파일한다.
        ソース = '''public class 解像度試験 {
    public static void main(String[] 引数) {
        int 幅値=日本語.内蔵.画面.幅値();
        int 高さ値=日本語.内蔵.画面.高さ値();
        if (幅値!=WIDTH || 高さ値!=HEIGHT) return;
        日本語.内蔵.画面.入口消去処理(3153944);
        日本語.内蔵.画面.矩形(幅値-1,高さ値-1,1,1,10061943);
        日本語.内蔵.出力.行書込("JAVA RESOLUTION PASS");
        日本語.内蔵.画面.待機();
    }
}
'''.replace('WIDTH', str(幅値)).replace('HEIGHT', str(高さ値))
        送出転送ファイル群('解像度試験.java', ソース.encode())
        結果 = シェル('javac 解像度試験.java'); assert 'exit 0' in 結果, 結果
        待機(b'JAVA RESOLUTION PASS', 本文送信('java 解像度試験\n'))
        画素検査((幅値-1, 高さ値-1), (119, 136, 153))
        待機(b'jkoros-native> ', 本文送信('q'))
        送出転送ファイル群('Swing試験.class', (結果経路/'Swing試験.class').read_bytes())
        待機(b'SWING READY', 本文送信('java Swing試験\n'))
        水平位置, 垂直位置 = (幅値-400)//2, (高さ値-280)//2
        描画 = 画素検査((水平位置, 垂直位置), (32, 80, 144))
        描画.save(str(結果経路/(容量本文+'.png')))
        起動処理 = len(履歴記録記録); クリック値(水平位置+80, 垂直位置+155)
        待機('SWING CLICK 名前'.encode(), 起動処理)
        起動処理 = len(履歴記録記録); クリック値(水平位置+385, 垂直位置+15); 待機(b'jkoros-native> ', 起動処理)
        assert 'AFTER_RESOLUTION' in シェル('echo AFTER_RESOLUTION')
        print('PASS:', 容量本文, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if 転送値: 転送値.close()
        if 遠隔値: 遠隔値.close()
        if プロセス値.poll() is None:
            プロセス値.terminate()
            try: プロセス値.wait(timeout=8)
            except subprocess.TimeoutExpired: プロセス値.kill(); プロセス値.wait()
        選択器.close(); プロセス値.stdout.close()
        (結果経路/(容量本文+'.log')).write_bytes(履歴記録記録)


def 起動処理():
    結果経路 = 計画根/'build/verification/resolution'; 結果経路.mkdir(parents=True, exist_ok=True)
    履歴記録記録 = {'passed': False, 'kernel_sha256': hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for 無効値 in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            結果 = subprocess.run(['python3', str(計画根/'道具/命令実行.py'), '--resolution', 無効値], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert 結果.returncode == 2 and b'--resolution' in 結果.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(結果経路), str(計画根/'試験/Java/Swing試験.java')])
        for 幅値, 高さ値 in ((1920,1080), (1280,720), (640,480)):
            解像度試験(幅値, 高さ値, 結果経路); 履歴記録記録['resolutions'].append([幅値, 高さ値])
        履歴記録記録.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (結果経路/'report.json').write_text(json.dumps(履歴記録記録, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': 起動処理()
