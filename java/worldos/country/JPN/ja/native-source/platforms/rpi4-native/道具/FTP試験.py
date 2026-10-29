#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from 通信網橋渡し import 通信網橋渡し
from 命令実行 import 計画根, 命令
from 復唱試験資料 import 復唱試験資料
from ELF試験 import Linux例


def 起動処理():
    結果データ = 計画根 / 'build/verification/ftp'; 結果データ.mkdir(parents=True, exist_ok=True)
    妥当性報告 = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((計画根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    実行記録 = bytearray()
    Javaソース = 結果データ / '束試験.java'
    Javaソース.write_text('public class 束試験 { public static void main(String[] 引数) throws Exception { 日本語.内蔵.出力.行書込("JAR 命令実行: " + 引数[0]); 日本語.内蔵.ファイル.書込("jar.txt", "内蔵 中核値 ファイル"); 日本語.内蔵.出力.行書込(日本語.内蔵.ファイル.読取("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(計画根/'build/java-library/classes'), '-d', str(結果データ), str(Javaソース)])
    書庫 = io.BytesIO()
    with zipfile.ZipFile(書庫, 'w', zipfile.ZIP_DEFLATED) as Java束:
        Java束.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 束試験\r\n\r\n')
        Java束.write(str(結果データ/'束試験.class'), '束試験.class')
    with socket.socket() as 一時:
        一時.bind(('127.0.0.1', 0)); ポート番号 = 一時.getsockname()[1]
    with socket.socket() as 一時:
        一時.bind(('127.0.0.1', 0)); サーバーストリームポート = 一時.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 一時:
        一時.bind(('127.0.0.1', 0)); サーバーデータグラムポート = 一時.getsockname()[1]
    with 通信網橋渡し(ポート番号, ['tcp:{}:9300'.format(サーバーストリームポート), 'udp:{}:9301'.format(サーバーデータグラムポート)], 捕獲=True) as 橋渡し:
        プロセス = subprocess.Popen(命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 橋渡し.転送済み引数(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        準備監視器 = selectors.DefaultSelector(); 準備監視器.register(プロセス.stdout, selectors.EVENT_READ)
        def メッセージ受取(標識=b'jkoros-native> ', 実行状態待機期限=60):
            データ = bytearray(); 終端位置変位量 = time.monotonic() + 実行状態待機期限
            while 標識 not in データ:
                if time.monotonic() > 終端位置変位量 or プロセス.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + データ.decode('utf-8', 'replace'))
                for 押下済み値, _ in 準備監視器.select(.1):
                    断片値 = 押下済み値.fileobj.read(4096)
                    if 断片値: データ.extend(断片値); 実行記録.extend(断片値)
                if b'PANIC:' in データ or b'FAIL ' in データ: raise AssertionError(データ)
            return データ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def シェル(行):
            プロセス.stdin.write(行.encode() + b'\n'); プロセス.stdin.flush(); return メッセージ受取()
        try:
            メッセージ受取(); assert 'FTP listening' in シェル('ftpd start')
            ファイル転送接続状態 = ftplib.FTP(); ファイル転送接続状態.encoding = 'utf-8'; ファイル転送接続状態.connect('127.0.0.1', ポート番号, timeout=20); ファイル転送接続状態.login()
            本文データデータ = bytes(range(256)) * 32
            ファイル転送接続状態.storbinary('STOR binary.dat', io.BytesIO(本文データデータ))
            結果 = bytearray(); ファイル転送接続状態.retrbinary('RETR binary.dat', 結果.extend)
            assert 結果 == 本文データデータ; assert ファイル転送接続状態.size('binary.dat') == len(本文データデータ)
            妥当性報告['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ファイル転送接続状態.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in シェル('cat 한글.txt')
            assert '한글.txt' in ファイル転送接続状態.nlst()
            assert dict(ファイル転送接続状態.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            妥当性報告['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ファイル転送接続状態.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 補助入口: assert str(補助入口).startswith('552'), str(補助入口)
            else: raise AssertionError('oversized upload accepted')
            結果 = bytearray(); ファイル転送接続状態.retrbinary('RETR binary.dat', 結果.extend); assert 結果 == 本文データデータ
            妥当性報告['checks'].append('oversized replacement rejected; previous file preserved')
            with ファイル転送接続状態.transfercmd('STOR pending.txt') as 送出転送ファイル群:
                # A control command must not change the active upload's destination.
                assert ファイル転送接続状態.size('binary.dat') == len(本文データデータ)
                送出転送ファイル群.sendall(b'UPLOAD TARGET PRESERVED')
            assert ファイル転送接続状態.voidresp().startswith('226')
            結果 = bytearray(); ファイル転送接続状態.retrbinary('RETR pending.txt', 結果.extend)
            assert 結果 == b'UPLOAD TARGET PRESERVED'
            結果 = bytearray(); ファイル転送接続状態.retrbinary('RETR binary.dat', 結果.extend)
            assert 結果 == 本文データデータ
            ファイル転送接続状態.delete('pending.txt')
            妥当性報告['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ファイル転送接続状態.storbinary('STOR 挨拶例.jar', io.BytesIO(書庫.getvalue()))
            文 = シェル('java -jar 挨拶例.jar 누리')
            assert 'JAR 命令実行: 누리' in 文 and '内蔵 中核値 ファイル' in 文 and 'exit 0' in 文, 文
            文 = シェル('./挨拶例.jar 세상')
            assert 'JAR 命令実行: 세상' in 文 and 'exit 0' in 文, 文
            妥当性報告['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            原本データ = '#include <ファイルABI.h>\nstruct データ { int 数; double 비율; };\nint 総和値(int n) { return n ? n + 総和値(n-1) : 0; }\nint main(void) { struct データ 値 = {総和値(10), 1.25}; if (値.数 != 55 || 値.비율 * 2 != 2.5) return 3; const char 挨拶例[] = "CC NATIVE PASS\\n"; int 文書 = ファイル開放("cc.txt", 読取書込 | 作成条件未存在 | 切詰め内容, 0600); if (文書 < 0) return 1; ファイルデータ書込(文書, 挨拶例, sizeof(挨拶例)-1); ファイル閉鎖(文書); ファイルデータ書込(1, 挨拶例, sizeof(挨拶例)-1); return 0; }\n'
            ファイル転送接続状態.storbinary('STOR ハングル文字列.c', io.BytesIO(原本データ.encode()))
            文 = シェル('cc ハングル文字列.c -o ハングル文字列.elf'); assert 'Compiled native ARM64 ELF:' in 文 and 'exit 0' in 文, 文
            文 = シェル('run ハングル文字列.elf'); assert 'CC NATIVE PASS' in 文 and 'exit 0' in 文, 文
            assert 'CC NATIVE PASS' in シェル('cat cc.txt')
            実行形式ファイル = bytearray(); ファイル転送接続状態.retrbinary('RETR ハングル文字列.elf', 実行形式ファイル.extend)
            assert 実行形式ファイル[:4] == b'\x7fELF' and 実行形式ファイル[18:20] == b'\xb7\x00'
            ファイル転送接続状態.storbinary('STOR 値複写.elf', io.BytesIO(実行形式ファイル)); 文 = シェル('run 値複写.elf'); assert 'CC NATIVE PASS' in 文 and 'exit 0' in 文, 文
            ファイル転送接続状態.storbinary('STOR 命令実行', io.BytesIO(実行形式ファイル)); 文=シェル('./命令実行');assert 'CC NATIVE PASS' in 文 and 'exit 0' in 文,文
            ファイル転送接続状態.storbinary('STOR 名前.txt', io.BytesIO(実行形式ファイル)); 文=シェル('./名前.txt');assert 'CC NATIVE PASS' in 文 and 'exit 0' in 文,文
            シェル('rm 命令実行 名前.txt')
            妥当性報告['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            シェル('rm binary.dat ハングル文字列.txt ハングル文字列.c ハングル文字列.elf 値複写.elf cc.txt jar.txt')
            Linuxファイル,期待=Linux例(結果データ/'linux-reference')
            ファイル転送接続状態.storbinary('STOR 리눅스인사',io.BytesIO(Linuxファイル.read_bytes()))
            文=シェル('./리눅스인사');assert 'exit -8' in 文,文
            文=シェル('run --linux 리눅스인사 한글인수');assert 期待+'exit 0' in 文,文
            assert 'LINUX ELF FILE IO' in シェル('cat linux.txt')
            ファイル転送接続状態.delete('리눅스인사');ファイル転送接続状態.delete('linux.txt')
            ファイル転送接続状態.storbinary('STOR 偽値.elf',io.BytesIO(b'plain text'))
            assert '실행할 数 없습니다:' in シェル('./偽値.elf');ファイル転送接続状態.delete('偽値.elf')
            妥当性報告['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 復唱試験資料() as 復唱サーバー入口:
                網ソース = 結果データ/'外部通信.java'
                網ソース.write_text('''import java.net.*; import java.io.*;
public class 外部通信 { public static void main(String[] args) throws Exception {
 Socket 接続 = 日本語.内蔵.接続状態輸送.接続("10.0.2.2", Integer.parseInt(args[0]));
 接続.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ソース = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ソース.length;i++) if (接続.getInputStream().read() != (ソース[i]&255)) throw new RuntimeException("TCP mismatch");
 接続.close();
 DatagramSocket 通信端点 = 日本語.内蔵.通信.開放(0); 日本語.内蔵.通信.待機期限(通信端点, 500);
 日本語.内蔵.通信.送信(通信端点, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!日本語.内蔵.通信.受取(通信端点).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 通信端点.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(計画根/'build/java-library/classes'),'-d',str(結果データ),str(網ソース)])
                ファイル転送接続状態.storbinary('STOR 外部通信.class', io.BytesIO((結果データ/'外部通信.class').read_bytes()))
                文 = シェル('java 外部通信 {} {}'.format(復唱サーバー入口.TCPポート, 復唱サーバー入口.UDPポート))
                assert 'EXTERNAL TCP UDP PASS' in 文 and '10.0.2.2' in 文 and 'exit 0' in 文, 文
                assert 復唱サーバー入口.保有受信済み == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 復唱サーバー入口.保有受信済み
                assert not 復唱サーバー入口.エラー一覧, 復唱サーバー入口.エラー一覧
            妥当性報告['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ファイル転送接続状態.delete('外部通信.class')
            サーバーソース=結果データ/'サーバー試験.java'
            サーバーソース.write_text('''import java.net.*; public class サーバー試験 {
 public static void main(String[] args) throws Exception {
  ServerSocket サーバー値 = new ServerSocket(9300); DatagramSocket 通信端点 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ゲスト値 = サーバー値.accept();
  ゲスト値.getOutputStream().write(ゲスト値.getInputStream().read()+1); ゲスト値.close(); サーバー値.close();
  byte[] 内容物値 = new byte[8]; DatagramPacket データグラム = new DatagramPacket(内容物値, 内容物値.length); 通信端点.receive(データグラム);
  通信端点.send(データグラム); 通信端点.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(結果データ),str(サーバーソース)])
            ファイル転送接続状態.storbinary('STOR サーバー試験.class',io.BytesIO((結果データ/'サーバー試験.class').read_bytes()))
            プロセス.stdin.write('java サーバー試験\n'.encode());プロセス.stdin.flush();メッセージ受取(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',サーバーストリームポート),timeout=5) as 通信相手値:
                通信相手値.sendall(b'A');assert 通信相手値.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as 通信相手値:
                通信相手値.settimeout(5);通信相手値.sendto(b'UDP-IN',('127.0.0.1',サーバーデータグラムポート));assert 通信相手値.recvfrom(512)[0]==b'UDP-IN'
            文=メッセージ受取();assert 'INBOUND TCP UDP PASS' in 文 and 'exit 0' in 文,文
            妥当性報告['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ファイル転送接続状態.delete('サーバー試験.class')
            命令語列順 = 'public class 色 { public static void main(String[] 引数) throws Exception { int 総和値 = 0; int 数 = 1; while (数 <= 10) { 総和値 = 総和値 + 数; 数 = 数 + 1; } 日本語.内蔵.出力.番号書込(総和値); 日本語.内蔵.ファイル.書込("aot.txt", "한글 AOT ファイル 😀"); 日本語.内蔵.出力.行書込(日本語.内蔵.ファイル.読取("aot.txt")); } }'
            ファイル転送接続状態.storbinary('STOR 色.java', io.BytesIO(命令語列順.encode()))
            文 = シェル('javac 色.java'); assert 'exit 0' in 文 and 'Compiled:' in 文, 文
            文 = シェル('jaot 色.class -o 色.elf'); assert 'AOT compiled native ARM64 ELF:' in 文 and 'exit 0' in 文, 文
            文 = シェル('run 色.elf'); assert '\n55\n' in 文 and '한글 AOT ファイル 😀' in 文 and 'exit 0' in 文, 文
            自前 = bytearray(); ファイル転送接続状態.retrbinary('RETR 色.elf', 自前.extend)
            文 = シェル('jaot 挨拶例.jar -o 色.elf'); assert 'exit 1' in 文 and 'unsupported' in 文, 文
            保持済みデータ = bytearray(); ファイル転送接続状態.retrbinary('RETR 色.elf', 保持済みデータ.extend); assert 自前 == 保持済みデータ
            バイトコード = bytearray(); ファイル転送接続状態.retrbinary('RETR 色.class', バイトコード.extend)
            梱包済み = io.BytesIO()
            with zipfile.ZipFile(梱包済み, 'w', zipfile.ZIP_DEFLATED) as Java束:
                Java束.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 色\r\n\r\n')
                Java束.writestr('色.class', バイトコード)
            ファイル転送接続状態.storbinary('STOR 色.jar', io.BytesIO(梱包済み.getvalue()))
            文 = シェル('jaot 色.jar -o 色.elf'); assert 'AOT compiled native ARM64 ELF:' in 文 and 'exit 0' in 文, 文
            文 = シェル('run 色.elf'); assert '\n55\n' in 文 and '한글 AOT ファイル 😀' in 文 and 'exit 0' in 文, 文
            妥当性報告['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            妥当性報告['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            静的ソース=結果データ/'静的試験.java'
            静的ソース.write_text('''public class 静的試験 {
 static int 計画根 = 3;
 static int 総和値(int n) { return n == 0 ? 0 : n + 総和値(n-1); }
 public static void main(String[] 引数) {
  int[] 値 = new int[] {計画根, 総和値(10)};
  System.out.println(値[0] + 値[1]); System.out.println(引数[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(結果データ),str(静的ソース)])
            ファイル転送接続状態.storbinary('STOR 静的試験.class',io.BytesIO((結果データ/'静的試験.class').read_bytes()))
            文=シェル('jaot 静的試験.class -o 静的試験.elf');assert 'exit 0' in 文,文
            文=シェル('run 静的試験.elf 한글인수');assert '\n58\n한글인수\nexit 0' in 文,文
            ファイル転送接続状態.delete('静的試験.class');ファイル転送接続状態.delete('静的試験.elf')
            妥当性報告['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            破損=bytearray(書庫.getvalue());破損[14]^=1
            ファイル転送接続状態.storbinary('STOR 挨拶例.jar',io.BytesIO(破損))
            文=シェル('java -jar 挨拶例.jar');assert 'Main-Class\nexit 1' in 文,文
            妥当性報告['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ファイル転送接続状態.quit(); assert 'FTP stopped' in シェル('ftpd stop')
            assert not 橋渡し.エラー, 橋渡し.エラー
            妥当性報告.update(passed=True, frames_to_guest=橋渡し.枠一覧到達先ゲスト, frames_from_guest=橋渡し.枠一覧起点ゲスト)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 押下済み値,_ in 準備監視器.select(0):
                断片値=押下済み値.fileobj.read(65536)
                if 断片値: 実行記録.extend(断片値)
            橋渡し.一時停止イベント.set()
            プロセス.terminate()
            try: プロセス.wait(timeout=5)
            except subprocess.TimeoutExpired: プロセス.kill(); プロセス.wait()
            準備監視器.close(); プロセス.stdin.close(); プロセス.stdout.close()
            妥当性報告['bridge_error'] = 橋渡し.エラー
            妥当性報告['frames_to_guest'] = 橋渡し.枠一覧到達先ゲスト; 妥当性報告['frames_from_guest'] = 橋渡し.枠一覧起点ゲスト
            (結果データ/'packets.json').write_text(json.dumps(橋渡し.追跡履歴記録,indent=2)+'\n')
            (結果データ / 'serial.log').write_bytes(実行記録)
            (結果データ / 'report.json').write_text(json.dumps(妥当性報告, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': 起動処理()
