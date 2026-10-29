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
from גשר_3de4fe3a import גשר_3de4fe3a
from לבצע_פקודה import לשקף_בסיס, פקודה
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def הפעלה():
    תוצאה_נתונים = לשקף_בסיס / 'build/verification/ftp'; תוצאה_נתונים.mkdir(parents=True, exist_ok=True)
    אימות_דוח = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((לשקף_בסיס / 'build/kernel8.img').read_bytes()).hexdigest()}
    תמליל = bytearray()
    자바원문 = תוצאה_נתונים / 'נסה_חבילה.java'
    자바원문.write_text('public class נסה_חבילה { public static void main(String[] ארגומנטים) throws Exception { עברית.עצמי.פלטטקסט.כתיבה_קו("JAR לבצע_פקודה: " + ארגומנטים[0]); עברית.עצמי.קובץ.כתוב("jar.txt", "עצמי ליבה_ערך קובץ"); עברית.עצמי.פלטטקסט.כתיבה_קו(עברית.עצמי.קובץ.קרא("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(לשקף_בסיס/'build/java-library/classes'), '-d', str(תוצאה_נתונים), str(자바원문)])
    ארכיון = io.BytesIO()
    with zipfile.ZipFile(ארכיון, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: נסה_חבילה\r\n\r\n')
        자바꾸러미.write(str(תוצאה_נתונים/'נסה_חבילה.class'), 'נסה_חבילה.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); מספר_יציאה = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); שרת_זרם_הסב = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); שרת_יחידת_נתונים_הסב = 임시자원.getsockname()[1]
    with גשר_3de4fe3a(מספר_יציאה, ['tcp:{}:9300'.format(שרת_זרם_הסב), 'udp:{}:9301'.format(שרת_יחידת_נתונים_הסב)], לכוד=True) as גשר:
        תהליך = subprocess.Popen(פקודה() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + גשר.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        בורר = selectors.DefaultSelector(); בורר.register(תהליך.stdout, selectors.EVENT_READ)
        def לקבל_דואר(סמן=b'jkoros-native> ', 시간제한=60):
            נתונים = bytearray(); סיים_שיחה_היסט = time.monotonic() + 시간제한
            while סמן not in נתונים:
                if time.monotonic() > סיים_שיחה_היסט or תהליך.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + נתונים.decode('utf-8', 'replace'))
                for 누름값, _ in בורר.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: נתונים.extend(조각); תמליל.extend(조각)
                if b'PANIC:' in נתונים or b'FAIL ' in נתונים: raise AssertionError(נתונים)
            return נתונים.decode('utf-8', 'replace').replace('\r\n', '\n')
        def מעטפת(שורה):
            תהליך.stdin.write(שורה.encode() + b'\n'); תהליך.stdin.flush(); return לקבל_דואר()
        try:
            לקבל_דואר(); assert 'FTP listening' in מעטפת('ftpd start')
            העברת_קבצים_קשר = ftplib.FTP(); העברת_קבצים_קשר.encoding = 'utf-8'; העברת_קבצים_קשר.connect('127.0.0.1', מספר_יציאה, timeout=20); העברת_קבצים_קשר.login()
            מטען_נתונים = bytes(range(256)) * 32
            העברת_קבצים_קשר.storbinary('STOR binary.dat', io.BytesIO(מטען_נתונים))
            תוצאה = bytearray(); העברת_קבצים_קשר.retrbinary('RETR binary.dat', תוצאה.extend)
            assert תוצאה == מטען_נתונים; assert העברת_קבצים_קשר.size('binary.dat') == len(מטען_נתונים)
            אימות_דוח['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            העברת_קבצים_קשר.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in מעטפת('cat 한글.txt')
            assert '한글.txt' in העברת_קבצים_קשר.nlst()
            assert dict(העברת_קבצים_קשר.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            אימות_דוח['checks'].append('UTF-8 filename and content visible in guest shell')
            try: העברת_קבצים_קשר.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            תוצאה = bytearray(); העברת_קבצים_קשר.retrbinary('RETR binary.dat', תוצאה.extend); assert תוצאה == מטען_נתונים
            אימות_דוח['checks'].append('oversized replacement rejected; previous file preserved')
            with העברת_קבצים_קשר.transfercmd('STOR pending.txt') as העלה_קבצים:
                # A control command must not change the active upload's destination.
                assert העברת_קבצים_קשר.size('binary.dat') == len(מטען_נתונים)
                העלה_קבצים.sendall(b'UPLOAD TARGET PRESERVED')
            assert העברת_קבצים_קשר.voidresp().startswith('226')
            תוצאה = bytearray(); העברת_קבצים_קשר.retrbinary('RETR pending.txt', תוצאה.extend)
            assert תוצאה == b'UPLOAD TARGET PRESERVED'
            תוצאה = bytearray(); העברת_קבצים_קשר.retrbinary('RETR binary.dat', תוצאה.extend)
            assert תוצאה == מטען_נתונים
            העברת_קבצים_קשר.delete('pending.txt')
            אימות_דוח['checks'].append('interleaved SIZE cannot change the active STOR destination')
            העברת_קבצים_קשר.storbinary('STOR 인사.jar', io.BytesIO(ארכיון.getvalue()))
            טקסט = מעטפת('java -jar 인사.jar 누리')
            assert 'JAR לבצע_פקודה: 누리' in טקסט and 'עצמי ליבה_ערך קובץ' in טקסט and 'exit 0' in טקסט, טקסט
            טקסט = מעטפת('./인사.jar 세상')
            assert 'JAR לבצע_פקודה: 세상' in טקסט and 'exit 0' in טקסט, טקסט
            אימות_דוח['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct נתונים { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct נתונים ערך = {합(10), 1.25}; if (ערך.수 != 55 || ערך.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = פתח_קובץ("cc.txt", קריאה_כתיבה | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; כתיבה_קובץ_נתונים(문서, 인사, sizeof(인사)-1); סגור_קובץ(문서); כתיבה_קובץ_נתונים(1, 인사, sizeof(인사)-1); return 0; }\n'
            העברת_קבצים_קשר.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            טקסט = מעטפת('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in טקסט and 'exit 0' in טקסט, טקסט
            טקסט = מעטפת('run 한글.elf'); assert 'CC NATIVE PASS' in טקסט and 'exit 0' in טקסט, טקסט
            assert 'CC NATIVE PASS' in מעטפת('cat cc.txt')
            실행파일 = bytearray(); העברת_קבצים_קשר.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            העברת_קבצים_קשר.storbinary('STOR מופע_ערך.elf', io.BytesIO(실행파일)); טקסט = מעטפת('run מופע_ערך.elf'); assert 'CC NATIVE PASS' in טקסט and 'exit 0' in טקסט, טקסט
            העברת_קבצים_קשר.storbinary('STOR לבצע_פקודה', io.BytesIO(실행파일)); טקסט=מעטפת('./לבצע_פקודה');assert 'CC NATIVE PASS' in טקסט and 'exit 0' in טקסט,טקסט
            העברת_קבצים_קשר.storbinary('STOR שם.txt', io.BytesIO(실행파일)); טקסט=מעטפת('./שם.txt');assert 'CC NATIVE PASS' in טקסט and 'exit 0' in טקסט,טקסט
            מעטפת('rm לבצע_פקודה שם.txt')
            אימות_דוח['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            מעטפת('rm binary.dat 한글.txt 한글.c 한글.elf מופע_ערך.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(תוצאה_נתונים/'linux-reference')
            העברת_קבצים_קשר.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            טקסט=מעטפת('./리눅스인사');assert 'exit -8' in טקסט,טקסט
            טקסט=מעטפת('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in טקסט,טקסט
            assert 'LINUX ELF FILE IO' in מעטפת('cat linux.txt')
            העברת_קבצים_קשר.delete('리눅스인사');העברת_קבצים_קשר.delete('linux.txt')
            העברת_קבצים_קשר.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in מעטפת('./거짓.elf');העברת_קבצים_קשר.delete('거짓.elf')
            אימות_דוח['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as הד_שרת_ערך:
                נטו_מקור = תוצאה_נתונים/'바깥통신.java'
                נטו_מקור.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket חיבור = עברית.עצמי.קשר_הובלה.חיבור("10.0.2.2", Integer.parseInt(args[0]));
 חיבור.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] קודמקור = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<קודמקור.length;i++) if (חיבור.getInputStream().read() != (קודמקור[i]&255)) throw new RuntimeException("TCP mismatch");
 חיבור.close();
 DatagramSocket משתתף = עברית.עצמי.통신.פתח(0); עברית.עצמי.통신.פסק_זמן(משתתף, 500);
 עברית.עצמי.통신.שלח(משתתף, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!עברית.עצמי.통신.לקבל(משתתף).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 משתתף.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(לשקף_בסיס/'build/java-library/classes'),'-d',str(תוצאה_נתונים),str(נטו_מקור)])
                העברת_קבצים_קשר.storbinary('STOR 바깥통신.class', io.BytesIO((תוצאה_נתונים/'바깥통신.class').read_bytes()))
                טקסט = מעטפת('java 바깥통신 {} {}'.format(הד_שרת_ערך.יציאת_TCP, הד_שרת_ערך.פרוטוקול_יחידת_נתונים_של_משתמש_הסב))
                assert 'EXTERNAL TCP UDP PASS' in טקסט and '10.0.2.2' in טקסט and 'exit 0' in טקסט, טקסט
                assert הד_שרת_ערך.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, הד_שרת_ערך.수신됨
                assert not הד_שרת_ערך.오류들, הד_שרת_ערך.오류들
            אימות_דוח['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            העברת_קבצים_קשר.delete('바깥통신.class')
            שרת_מקור=תוצאה_נתונים/'שרת_נסה.java'
            שרת_מקור.write_text('''import java.net.*; public class שרת_נסה {
 public static void main(String[] args) throws Exception {
  ServerSocket שרת_ערך = new ServerSocket(9300); DatagramSocket משתתף = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket אורח_ערך = שרת_ערך.accept();
  אורח_ערך.getOutputStream().write(אורח_ערך.getInputStream().read()+1); אורח_ערך.close(); שרת_ערך.close();
  byte[] תוכן_ערך = new byte[8]; DatagramPacket יחידת_נתונים = new DatagramPacket(תוכן_ערך, תוכן_ערך.length); משתתף.receive(יחידת_נתונים);
  משתתף.send(יחידת_נתונים); משתתף.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(תוצאה_נתונים),str(שרת_מקור)])
            העברת_קבצים_קשר.storbinary('STOR שרת_נסה.class',io.BytesIO((תוצאה_נתונים/'שרת_נסה.class').read_bytes()))
            תהליך.stdin.write('java שרת_נסה\n'.encode());תהליך.stdin.flush();לקבל_דואר(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',שרת_זרם_הסב),timeout=5) as עמית_ערך:
                עמית_ערך.sendall(b'A');assert עמית_ערך.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as עמית_ערך:
                עמית_ערך.settimeout(5);עמית_ערך.sendto(b'UDP-IN',('127.0.0.1',שרת_יחידת_נתונים_הסב));assert עמית_ערך.recvfrom(512)[0]==b'UDP-IN'
            טקסט=לקבל_דואר();assert 'INBOUND TCP UDP PASS' in טקסט and 'exit 0' in טקסט,טקסט
            אימות_דוח['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            העברת_קבצים_קשר.delete('שרת_נסה.class')
            הוראה_רצף = 'public class 빛 { public static void main(String[] ארגומנטים) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } עברית.עצמי.פלטטקסט.수쓰기(합); עברית.עצמי.קובץ.כתוב("aot.txt", "한글 AOT קובץ 😀"); עברית.עצמי.פלטטקסט.כתיבה_קו(עברית.עצמי.קובץ.קרא("aot.txt")); } }'
            העברת_קבצים_קשר.storbinary('STOR 빛.java', io.BytesIO(הוראה_רצף.encode()))
            טקסט = מעטפת('javac 빛.java'); assert 'exit 0' in טקסט and 'Compiled:' in טקסט, טקסט
            טקסט = מעטפת('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in טקסט and 'exit 0' in טקסט, טקסט
            טקסט = מעטפת('run 빛.elf'); assert '\n55\n' in טקסט and '한글 AOT קובץ 😀' in טקסט and 'exit 0' in טקסט, טקסט
            מקורי = bytearray(); העברת_קבצים_קשר.retrbinary('RETR 빛.elf', מקורי.extend)
            טקסט = מעטפת('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in טקסט and 'unsupported' in טקסט, טקסט
            보존자료 = bytearray(); העברת_קבצים_קשר.retrbinary('RETR 빛.elf', 보존자료.extend); assert מקורי == 보존자료
            바이트코드 = bytearray(); העברת_קבצים_קשר.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            העברת_קבצים_קשר.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            טקסט = מעטפת('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in טקסט and 'exit 0' in טקסט, טקסט
            טקסט = מעטפת('run 빛.elf'); assert '\n55\n' in טקסט and '한글 AOT קובץ 😀' in טקסט and 'exit 0' in טקסט, טקסט
            אימות_דוח['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            אימות_דוח['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            סטטי_מקור=תוצאה_נתונים/'סטטי_נסה.java'
            סטטי_מקור.write_text('''public class סטטי_נסה {
 static int לשקף_בסיס = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] ארגומנטים) {
  int[] ערך = new int[] {לשקף_בסיס, 합(10)};
  System.out.println(ערך[0] + ערך[1]); System.out.println(ארגומנטים[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(תוצאה_נתונים),str(סטטי_מקור)])
            העברת_קבצים_קשר.storbinary('STOR סטטי_נסה.class',io.BytesIO((תוצאה_נתונים/'סטטי_נסה.class').read_bytes()))
            טקסט=מעטפת('jaot סטטי_נסה.class -o סטטי_נסה.elf');assert 'exit 0' in טקסט,טקסט
            טקסט=מעטפת('run סטטי_נסה.elf 한글인수');assert '\n58\n한글인수\nexit 0' in טקסט,טקסט
            העברת_קבצים_קשר.delete('סטטי_נסה.class');העברת_קבצים_קשר.delete('סטטי_נסה.elf')
            אימות_דוח['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ארכיון.getvalue());손상자료[14]^=1
            העברת_קבצים_קשר.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            טקסט=מעטפת('java -jar 인사.jar');assert 'Main-Class\nexit 1' in טקסט,טקסט
            אימות_דוח['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            העברת_קבצים_קשר.quit(); assert 'FTP stopped' in מעטפת('ftpd stop')
            assert not גשר.שגיאה, גשר.שגיאה
            אימות_דוח.update(passed=True, frames_to_guest=גשר.커널수신틀수, frames_from_guest=גשר.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in בורר.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: תמליל.extend(조각)
            גשר.השהה_אירוע.set()
            תהליך.terminate()
            try: תהליך.wait(timeout=5)
            except subprocess.TimeoutExpired: תהליך.kill(); תהליך.wait()
            בורר.close(); תהליך.stdin.close(); תהליך.stdout.close()
            אימות_דוח['bridge_error'] = גשר.שגיאה
            אימות_דוח['frames_to_guest'] = גשר.커널수신틀수; אימות_דוח['frames_from_guest'] = גשר.커널발신틀수
            (תוצאה_נתונים/'packets.json').write_text(json.dumps(גשר.יומן_מעקב,indent=2)+'\n')
            (תוצאה_נתונים / 'serial.log').write_bytes(תמליל)
            (תוצאה_נתונים / 'report.json').write_text(json.dumps(אימות_דוח, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': הפעלה()
