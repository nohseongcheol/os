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
from 網路橋接 import 網路橋接
from 執行命令 import 項目根, 命令
from 回顯測試夾具 import 回顯測試夾具
from 測試ELF import Linux範例


def 運行():
    結果資料 = 項目根 / 'build/verification/ftp'; 結果資料.mkdir(parents=True, exist_ok=True)
    有效性驗證報告 = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((項目根 / 'build/kernel8.img').read_bytes()).hexdigest()}
    執行記錄 = bytearray()
    Java原始碼 = 結果資料 / '測試捆綁.java'
    Java原始碼.write_text('public class 測試捆綁 { public static void main(String[] 實參) throws Exception { 中文.內建.輸出.寫入行("JAR 執行命令: " + 實參[0]); 中文.內建.檔案.寫入("jar.txt", "內建 內核值 檔案"); 中文.內建.輸出.寫入行(中文.內建.檔案.讀取("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(項目根/'build/java-library/classes'), '-d', str(結果資料), str(Java原始碼)])
    存檔 = io.BytesIO()
    with zipfile.ZipFile(存檔, 'w', zipfile.ZIP_DEFLATED) as Java捆綁:
        Java捆綁.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 測試捆綁\r\n\r\n')
        Java捆綁.write(str(結果資料/'測試捆綁.class'), '測試捆綁.class')
    with socket.socket() as 臨時:
        臨時.bind(('127.0.0.1', 0)); 埠編號 = 臨時.getsockname()[1]
    with socket.socket() as 臨時:
        臨時.bind(('127.0.0.1', 0)); 服務器流埠 = 臨時.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 臨時:
        臨時.bind(('127.0.0.1', 0)); 服務器數據報埠 = 臨時.getsockname()[1]
    with 網路橋接(埠編號, ['tcp:{}:9300'.format(服務器流埠), 'udp:{}:9301'.format(服務器數據報埠)], 捕獲=True) as 橋接:
        程序 = subprocess.Popen(命令() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 橋接.已轉發實際參數(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        就緒選擇器 = selectors.DefaultSelector(); 就緒選擇器.register(程序.stdout, selectors.EVENT_READ)
        def 接收消息(標記=b'jkoros-native> ', 執行狀態超時=60):
            資料 = bytearray(); 結束偏移 = time.monotonic() + 執行狀態超時
            while 標記 not in 資料:
                if time.monotonic() > 結束偏移 or 程序.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + 資料.decode('utf-8', 'replace'))
                for 已按下值, _ in 就緒選擇器.select(.1):
                    片段值 = 已按下值.fileobj.read(4096)
                    if 片段值: 資料.extend(片段值); 執行記錄.extend(片段值)
                if b'PANIC:' in 資料 or b'FAIL ' in 資料: raise AssertionError(資料)
            return 資料.decode('utf-8', 'replace').replace('\r\n', '\n')
        def 命令殼(行):
            程序.stdin.write(行.encode() + b'\n'); 程序.stdin.flush(); return 接收消息()
        try:
            接收消息(); assert 'FTP listening' in 命令殼('ftpd start')
            檔案傳送連接狀態 = ftplib.FTP(); 檔案傳送連接狀態.encoding = 'utf-8'; 檔案傳送連接狀態.connect('127.0.0.1', 埠編號, timeout=20); 檔案傳送連接狀態.login()
            載荷數據資料 = bytes(range(256)) * 32
            檔案傳送連接狀態.storbinary('STOR binary.dat', io.BytesIO(載荷數據資料))
            結果 = bytearray(); 檔案傳送連接狀態.retrbinary('RETR binary.dat', 結果.extend)
            assert 結果 == 載荷數據資料; assert 檔案傳送連接狀態.size('binary.dat') == len(載荷數據資料)
            有效性驗證報告['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            檔案傳送連接狀態.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in 命令殼('cat 한글.txt')
            assert '한글.txt' in 檔案傳送連接狀態.nlst()
            assert dict(檔案傳送連接狀態.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            有效性驗證報告['checks'].append('UTF-8 filename and content visible in guest shell')
            try: 檔案傳送連接狀態.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 輔助條目: assert str(輔助條目).startswith('552'), str(輔助條目)
            else: raise AssertionError('oversized upload accepted')
            結果 = bytearray(); 檔案傳送連接狀態.retrbinary('RETR binary.dat', 結果.extend); assert 結果 == 載荷數據資料
            有效性驗證報告['checks'].append('oversized replacement rejected; previous file preserved')
            with 檔案傳送連接狀態.transfercmd('STOR pending.txt') as 上傳檔案集:
                # A control command must not change the active upload's destination.
                assert 檔案傳送連接狀態.size('binary.dat') == len(載荷數據資料)
                上傳檔案集.sendall(b'UPLOAD TARGET PRESERVED')
            assert 檔案傳送連接狀態.voidresp().startswith('226')
            結果 = bytearray(); 檔案傳送連接狀態.retrbinary('RETR pending.txt', 結果.extend)
            assert 結果 == b'UPLOAD TARGET PRESERVED'
            結果 = bytearray(); 檔案傳送連接狀態.retrbinary('RETR binary.dat', 結果.extend)
            assert 結果 == 載荷數據資料
            檔案傳送連接狀態.delete('pending.txt')
            有效性驗證報告['checks'].append('interleaved SIZE cannot change the active STOR destination')
            檔案傳送連接狀態.storbinary('STOR 問候例.jar', io.BytesIO(存檔.getvalue()))
            文本 = 命令殼('java -jar 問候例.jar 누리')
            assert 'JAR 執行命令: 누리' in 文本 and '內建 內核值 檔案' in 文本 and 'exit 0' in 文本, 文本
            文本 = 命令殼('./問候例.jar 세상')
            assert 'JAR 執行命令: 세상' in 文本 and 'exit 0' in 文本, 文本
            有效性驗證報告['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            原始資料 = '#include <檔案ABI.h>\nstruct 資料 { int 數; double 비율; };\nint 總和值(int n) { return n ? n + 總和值(n-1) : 0; }\nint main(void) { struct 資料 值 = {總和值(10), 1.25}; if (值.數 != 55 || 值.비율 * 2 != 2.5) return 3; const char 問候例[] = "CC NATIVE PASS\\n"; int 文檔集 = 打開檔案("cc.txt", 讀取寫入 | 創建條件缺失 | 截斷內容, 0600); if (文檔集 < 0) return 1; 寫入檔案資料(文檔集, 問候例, sizeof(問候例)-1); 關閉檔案(文檔集); 寫入檔案資料(1, 問候例, sizeof(問候例)-1); return 0; }\n'
            檔案傳送連接狀態.storbinary('STOR 韓文文本.c', io.BytesIO(原始資料.encode()))
            文本 = 命令殼('cc 韓文文本.c -o 韓文文本.elf'); assert 'Compiled native ARM64 ELF:' in 文本 and 'exit 0' in 文本, 文本
            文本 = 命令殼('run 韓文文本.elf'); assert 'CC NATIVE PASS' in 文本 and 'exit 0' in 文本, 文本
            assert 'CC NATIVE PASS' in 命令殼('cat cc.txt')
            可執行文件檔案 = bytearray(); 檔案傳送連接狀態.retrbinary('RETR 韓文文本.elf', 可執行文件檔案.extend)
            assert 可執行文件檔案[:4] == b'\x7fELF' and 可執行文件檔案[18:20] == b'\xb7\x00'
            檔案傳送連接狀態.storbinary('STOR 複製值.elf', io.BytesIO(可執行文件檔案)); 文本 = 命令殼('run 複製值.elf'); assert 'CC NATIVE PASS' in 文本 and 'exit 0' in 文本, 文本
            檔案傳送連接狀態.storbinary('STOR 執行命令', io.BytesIO(可執行文件檔案)); 文本=命令殼('./執行命令');assert 'CC NATIVE PASS' in 文本 and 'exit 0' in 文本,文本
            檔案傳送連接狀態.storbinary('STOR 名稱.txt', io.BytesIO(可執行文件檔案)); 文本=命令殼('./名稱.txt');assert 'CC NATIVE PASS' in 文本 and 'exit 0' in 文本,文本
            命令殼('rm 執行命令 名稱.txt')
            有效性驗證報告['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            命令殼('rm binary.dat 韓文文本.txt 韓文文本.c 韓文文本.elf 複製值.elf cc.txt jar.txt')
            Linux檔案,預期=Linux範例(結果資料/'linux-reference')
            檔案傳送連接狀態.storbinary('STOR 리눅스인사',io.BytesIO(Linux檔案.read_bytes()))
            文本=命令殼('./리눅스인사');assert 'exit -8' in 文本,文本
            文本=命令殼('run --linux 리눅스인사 한글인수');assert 預期+'exit 0' in 文本,文本
            assert 'LINUX ELF FILE IO' in 命令殼('cat linux.txt')
            檔案傳送連接狀態.delete('리눅스인사');檔案傳送連接狀態.delete('linux.txt')
            檔案傳送連接狀態.storbinary('STOR 假值.elf',io.BytesIO(b'plain text'))
            assert '실행할 數 없습니다:' in 命令殼('./假值.elf');檔案傳送連接狀態.delete('假值.elf')
            有效性驗證報告['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 回顯測試夾具() as 回顯服務器條目:
                網路層原始碼 = 結果資料/'外部通信.java'
                網路層原始碼.write_text('''import java.net.*; import java.io.*;
public class 外部通信 { public static void main(String[] args) throws Exception {
 Socket 連接 = 中文.內建.連接狀態傳輸.連接("10.0.2.2", Integer.parseInt(args[0]));
 連接.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] 原始碼 = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<原始碼.length;i++) if (連接.getInputStream().read() != (原始碼[i]&255)) throw new RuntimeException("TCP mismatch");
 連接.close();
 DatagramSocket 端點 = 中文.內建.通信.打開(0); 中文.內建.通信.超時(端點, 500);
 中文.內建.通信.發送(端點, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!中文.內建.通信.接收(端點).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 端點.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(項目根/'build/java-library/classes'),'-d',str(結果資料),str(網路層原始碼)])
                檔案傳送連接狀態.storbinary('STOR 外部通信.class', io.BytesIO((結果資料/'外部通信.class').read_bytes()))
                文本 = 命令殼('java 外部通信 {} {}'.format(回顯服務器條目.TCP埠, 回顯服務器條目.UDP埠))
                assert 'EXTERNAL TCP UDP PASS' in 文本 and '10.0.2.2' in 文本 and 'exit 0' in 文本, 文本
                assert 回顯服務器條目.擁有已接收 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 回顯服務器條目.擁有已接收
                assert not 回顯服務器條目.錯誤列, 回顯服務器條目.錯誤列
            有效性驗證報告['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            檔案傳送連接狀態.delete('外部通信.class')
            服務器原始碼=結果資料/'服務器測試.java'
            服務器原始碼.write_text('''import java.net.*; public class 服務器測試 {
 public static void main(String[] args) throws Exception {
  ServerSocket 服務器值 = new ServerSocket(9300); DatagramSocket 端點 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 客戶機值 = 服務器值.accept();
  客戶機值.getOutputStream().write(客戶機值.getInputStream().read()+1); 客戶機值.close(); 服務器值.close();
  byte[] 內容值 = new byte[8]; DatagramPacket 數據報 = new DatagramPacket(內容值, 內容值.length); 端點.receive(數據報);
  端點.send(數據報); 端點.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(結果資料),str(服務器原始碼)])
            檔案傳送連接狀態.storbinary('STOR 服務器測試.class',io.BytesIO((結果資料/'服務器測試.class').read_bytes()))
            程序.stdin.write('java 服務器測試\n'.encode());程序.stdin.flush();接收消息(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',服務器流埠),timeout=5) as 對端值:
                對端值.sendall(b'A');assert 對端值.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as 對端值:
                對端值.settimeout(5);對端值.sendto(b'UDP-IN',('127.0.0.1',服務器數據報埠));assert 對端值.recvfrom(512)[0]==b'UDP-IN'
            文本=接收消息();assert 'INBOUND TCP UDP PASS' in 文本 and 'exit 0' in 文本,文本
            有效性驗證報告['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            檔案傳送連接狀態.delete('服務器測試.class')
            指令序列 = 'public class 顏色 { public static void main(String[] 實參) throws Exception { int 總和值 = 0; int 數 = 1; while (數 <= 10) { 總和值 = 總和值 + 數; 數 = 數 + 1; } 中文.內建.輸出.寫入編號(總和值); 中文.內建.檔案.寫入("aot.txt", "한글 AOT 檔案 😀"); 中文.內建.輸出.寫入行(中文.內建.檔案.讀取("aot.txt")); } }'
            檔案傳送連接狀態.storbinary('STOR 顏色.java', io.BytesIO(指令序列.encode()))
            文本 = 命令殼('javac 顏色.java'); assert 'exit 0' in 文本 and 'Compiled:' in 文本, 文本
            文本 = 命令殼('jaot 顏色.class -o 顏色.elf'); assert 'AOT compiled native ARM64 ELF:' in 文本 and 'exit 0' in 文本, 文本
            文本 = 命令殼('run 顏色.elf'); assert '\n55\n' in 文本 and '한글 AOT 檔案 😀' in 文本 and 'exit 0' in 文本, 文本
            原生 = bytearray(); 檔案傳送連接狀態.retrbinary('RETR 顏色.elf', 原生.extend)
            文本 = 命令殼('jaot 問候例.jar -o 顏色.elf'); assert 'exit 1' in 文本 and 'unsupported' in 文本, 文本
            已保留資料 = bytearray(); 檔案傳送連接狀態.retrbinary('RETR 顏色.elf', 已保留資料.extend); assert 原生 == 已保留資料
            字節碼 = bytearray(); 檔案傳送連接狀態.retrbinary('RETR 顏色.class', 字節碼.extend)
            已打包 = io.BytesIO()
            with zipfile.ZipFile(已打包, 'w', zipfile.ZIP_DEFLATED) as Java捆綁:
                Java捆綁.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 顏色\r\n\r\n')
                Java捆綁.writestr('顏色.class', 字節碼)
            檔案傳送連接狀態.storbinary('STOR 顏色.jar', io.BytesIO(已打包.getvalue()))
            文本 = 命令殼('jaot 顏色.jar -o 顏色.elf'); assert 'AOT compiled native ARM64 ELF:' in 文本 and 'exit 0' in 文本, 文本
            文本 = 命令殼('run 顏色.elf'); assert '\n55\n' in 文本 and '한글 AOT 檔案 😀' in 文本 and 'exit 0' in 文本, 文本
            有效性驗證報告['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            有效性驗證報告['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            靜態原始碼=結果資料/'靜態測試.java'
            靜態原始碼.write_text('''public class 靜態測試 {
 static int 項目根 = 3;
 static int 總和值(int n) { return n == 0 ? 0 : n + 總和值(n-1); }
 public static void main(String[] 實參) {
  int[] 值 = new int[] {項目根, 總和值(10)};
  System.out.println(值[0] + 值[1]); System.out.println(實參[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(結果資料),str(靜態原始碼)])
            檔案傳送連接狀態.storbinary('STOR 靜態測試.class',io.BytesIO((結果資料/'靜態測試.class').read_bytes()))
            文本=命令殼('jaot 靜態測試.class -o 靜態測試.elf');assert 'exit 0' in 文本,文本
            文本=命令殼('run 靜態測試.elf 한글인수');assert '\n58\n한글인수\nexit 0' in 文本,文本
            檔案傳送連接狀態.delete('靜態測試.class');檔案傳送連接狀態.delete('靜態測試.elf')
            有效性驗證報告['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            已損壞=bytearray(存檔.getvalue());已損壞[14]^=1
            檔案傳送連接狀態.storbinary('STOR 問候例.jar',io.BytesIO(已損壞))
            文本=命令殼('java -jar 問候例.jar');assert 'Main-Class\nexit 1' in 文本,文本
            有效性驗證報告['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            檔案傳送連接狀態.quit(); assert 'FTP stopped' in 命令殼('ftpd stop')
            assert not 橋接.錯誤, 橋接.錯誤
            有效性驗證報告.update(passed=True, frames_to_guest=橋接.幀列目標側客戶機, frames_from_guest=橋接.幀列起點客戶機)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 已按下值,_ in 就緒選擇器.select(0):
                片段值=已按下值.fileobj.read(65536)
                if 片段值: 執行記錄.extend(片段值)
            橋接.暫停事件.set()
            程序.terminate()
            try: 程序.wait(timeout=5)
            except subprocess.TimeoutExpired: 程序.kill(); 程序.wait()
            就緒選擇器.close(); 程序.stdin.close(); 程序.stdout.close()
            有效性驗證報告['bridge_error'] = 橋接.錯誤
            有效性驗證報告['frames_to_guest'] = 橋接.幀列目標側客戶機; 有效性驗證報告['frames_from_guest'] = 橋接.幀列起點客戶機
            (結果資料/'packets.json').write_text(json.dumps(橋接.追蹤日誌,indent=2)+'\n')
            (結果資料 / 'serial.log').write_bytes(執行記錄)
            (結果資料 / 'report.json').write_text(json.dumps(有效性驗證報告, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': 運行()
