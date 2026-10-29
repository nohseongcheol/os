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
from መረብ_ድልድይ import መረብ_ድልድይ
from ፈጽም_ትእዛዝ import አሳይ_ስር, ትእዛዝ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ማስኬጃ():
    ልኬት_ውሂብ = አሳይ_ስር / 'build/verification/ftp'; ልኬት_ውሂብ.mkdir(parents=True, exist_ok=True)
    ማረጋገጥ_ዘገባ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((አሳይ_ስር / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ልኬት_ውሂብ / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { አማርኛ.자체.ውጤት.ጻፍ_መስመር("JAR ፈጽም_ትእዛዝ: " + 인수[0]); አማርኛ.자체.ፋይል.መጻፊያ("jar.txt", "자체 ዓንኳር_እሴት ፋይል"); አማርኛ.자체.ውጤት.ጻፍ_መስመር(አማርኛ.자체.ፋይል.ማንበቢያ("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(አሳይ_ስር/'build/java-library/classes'), '-d', str(ልኬት_ውሂብ), str(자바원문)])
    ከዝን = io.BytesIO()
    with zipfile.ZipFile(ከዝን, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ልኬት_ውሂብ/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); የወደብ_ቁጥር = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); አገልጋይ_ልቀቅ_ወደብ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with መረብ_ድልድይ(የወደብ_ቁጥር, ['tcp:{}:9300'.format(አገልጋይ_ልቀቅ_ወደብ), 'udp:{}:9301'.format(서버전문접속번호)], መያዝ=True) as ድልድይ:
        ሂደቶች = subprocess.Popen(ትእዛዝ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ድልድይ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        መራጭ = selectors.DefaultSelector(); መራጭ.register(ሂደቶች.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ውሂብ = bytearray(); ጨርስ_ዝንፍ = time.monotonic() + 시간제한
            while 확인표시 not in ውሂብ:
                if time.monotonic() > ጨርስ_ዝንፍ or ሂደቶች.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ውሂብ.decode('utf-8', 'replace'))
                for 누름값, _ in መራጭ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ውሂብ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ውሂብ or b'FAIL ' in ውሂብ: raise AssertionError(ውሂብ)
            return ውሂብ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ሼል(መስመር):
            ሂደቶች.stdin.write(መስመር.encode() + b'\n'); ሂደቶች.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ሼል('ftpd start')
            ፋይል_ትልልፍ_ግንኙነት = ftplib.FTP(); ፋይል_ትልልፍ_ግንኙነት.encoding = 'utf-8'; ፋይል_ትልልፍ_ግንኙነት.connect('127.0.0.1', የወደብ_ቁጥር, timeout=20); ፋይል_ትልልፍ_ግንኙነት.login()
            የክፍያ_ጫና_ውሂብ = bytes(range(256)) * 32
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR binary.dat', io.BytesIO(የክፍያ_ጫና_ውሂብ))
            ልኬት = bytearray(); ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR binary.dat', ልኬት.extend)
            assert ልኬት == የክፍያ_ጫና_ውሂብ; assert ፋይል_ትልልፍ_ግንኙነት.size('binary.dat') == len(የክፍያ_ጫና_ውሂብ)
            ማረጋገጥ_ዘገባ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ሼል('cat 한글.txt')
            assert '한글.txt' in ፋይል_ትልልፍ_ግንኙነት.nlst()
            assert dict(ፋይል_ትልልፍ_ግንኙነት.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ማረጋገጥ_ዘገባ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ልኬት = bytearray(); ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR binary.dat', ልኬት.extend); assert ልኬት == የክፍያ_ጫና_ውሂብ
            ማረጋገጥ_ዘገባ['checks'].append('oversized replacement rejected; previous file preserved')
            with ፋይል_ትልልፍ_ግንኙነት.transfercmd('STOR pending.txt') as መጫን_ፋይሎች:
                # A control command must not change the active upload's destination.
                assert ፋይል_ትልልፍ_ግንኙነት.size('binary.dat') == len(የክፍያ_ጫና_ውሂብ)
                መጫን_ፋይሎች.sendall(b'UPLOAD TARGET PRESERVED')
            assert ፋይል_ትልልፍ_ግንኙነት.voidresp().startswith('226')
            ልኬት = bytearray(); ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR pending.txt', ልኬት.extend)
            assert ልኬት == b'UPLOAD TARGET PRESERVED'
            ልኬት = bytearray(); ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR binary.dat', ልኬት.extend)
            assert ልኬት == የክፍያ_ጫና_ውሂብ
            ፋይል_ትልልፍ_ግንኙነት.delete('pending.txt')
            ማረጋገጥ_ዘገባ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 인사.jar', io.BytesIO(ከዝን.getvalue()))
            ጽሁፍ = ሼል('java -jar 인사.jar 누리')
            assert 'JAR ፈጽም_ትእዛዝ: 누리' in ጽሁፍ and '자체 ዓንኳር_እሴት ፋይል' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            ጽሁፍ = ሼል('./인사.jar 세상')
            assert 'JAR ፈጽም_ትእዛዝ: 세상' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            ማረጋገጥ_ዘገባ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ውሂብ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ውሂብ እሴት = {합(10), 1.25}; if (እሴት.수 != 55 || እሴት.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ክፈት_ፋይል("cc.txt", ተነባቢ_የሚጻፍበት | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ጻፍ_ፋይል_ውሂብ(문서, 인사, sizeof(인사)-1); ዝጋ_ፋይል(문서); ጻፍ_ፋይል_ውሂብ(1, 인사, sizeof(인사)-1); return 0; }\n'
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ጽሁፍ = ሼል('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            ጽሁፍ = ሼል('run 한글.elf'); assert 'CC NATIVE PASS' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            assert 'CC NATIVE PASS' in ሼል('cat cc.txt')
            실행파일 = bytearray(); ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR ቅዳ_እሴት.elf', io.BytesIO(실행파일)); ጽሁፍ = ሼል('run ቅዳ_እሴት.elf'); assert 'CC NATIVE PASS' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR ፈጽም_ትእዛዝ', io.BytesIO(실행파일)); ጽሁፍ=ሼል('./ፈጽም_ትእዛዝ');assert 'CC NATIVE PASS' in ጽሁፍ and 'exit 0' in ጽሁፍ,ጽሁፍ
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR ስም.txt', io.BytesIO(실행파일)); ጽሁፍ=ሼል('./ስም.txt');assert 'CC NATIVE PASS' in ጽሁፍ and 'exit 0' in ጽሁፍ,ጽሁፍ
            ሼል('rm ፈጽም_ትእዛዝ ስም.txt')
            ማረጋገጥ_ዘገባ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ሼል('rm binary.dat 한글.txt 한글.c 한글.elf ቅዳ_እሴት.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ልኬት_ውሂብ/'linux-reference')
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ጽሁፍ=ሼል('./리눅스인사');assert 'exit -8' in ጽሁፍ,ጽሁፍ
            ጽሁፍ=ሼል('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ጽሁፍ,ጽሁፍ
            assert 'LINUX ELF FILE IO' in ሼል('cat linux.txt')
            ፋይል_ትልልፍ_ግንኙነት.delete('리눅스인사');ፋይል_ትልልፍ_ግንኙነት.delete('linux.txt')
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ሼል('./거짓.elf');ፋይል_ትልልፍ_ግንኙነት.delete('거짓.elf')
            ማረጋገጥ_ዘገባ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ልኬት_ውሂብ/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket መገናኛ = አማርኛ.자체.연결통신.መገናኛ("10.0.2.2", Integer.parseInt(args[0]));
 መገናኛ.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ምንጭ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ምንጭ.length;i++) if (መገናኛ.getInputStream().read() != (ምንጭ[i]&255)) throw new RuntimeException("TCP mismatch");
 መገናኛ.close();
 DatagramSocket 종단 = አማርኛ.자체.통신.መክፈቻ(0); አማርኛ.자체.통신.대기시간(종단, 500);
 አማርኛ.자체.통신.ላክ(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!አማርኛ.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(አሳይ_ስር/'build/java-library/classes'),'-d',str(ልኬት_ውሂብ),str(통신원문)])
                ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 바깥통신.class', io.BytesIO((ልኬት_ውሂብ/'바깥통신.class').read_bytes()))
                ጽሁፍ = ሼል('java 바깥통신 {} {}'.format(되돌림서버항목.የትልልፍ_ቁጥጥር_ፕሮቶኮል_ወደብ, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ጽሁፍ and '10.0.2.2' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ማረጋገጥ_ዘገባ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ፋይል_ትልልፍ_ግንኙነት.delete('바깥통신.class')
            አገልጋይ_ምንጭ=ልኬት_ውሂብ/'서버시험.java'
            አገልጋይ_ምንጭ.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket አገልጋይ_እሴት = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket እንግዳ_እሴት = አገልጋይ_እሴት.accept();
  እንግዳ_እሴት.getOutputStream().write(እንግዳ_እሴት.getInputStream().read()+1); እንግዳ_እሴት.close(); አገልጋይ_እሴት.close();
  byte[] ይዘት_እሴት = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ይዘት_እሴት, ይዘት_እሴት.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ልኬት_ውሂብ),str(አገልጋይ_ምንጭ)])
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 서버시험.class',io.BytesIO((ልኬት_ውሂብ/'서버시험.class').read_bytes()))
            ሂደቶች.stdin.write('java 서버시험\n'.encode());ሂደቶች.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',አገልጋይ_ልቀቅ_ወደብ),timeout=5) as አቻ_እሴት:
                አቻ_እሴት.sendall(b'A');assert አቻ_እሴት.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as አቻ_እሴት:
                አቻ_እሴት.settimeout(5);አቻ_እሴት.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert አቻ_እሴት.recvfrom(512)[0]==b'UDP-IN'
            ጽሁፍ=수신하기();assert 'INBOUND TCP UDP PASS' in ጽሁፍ and 'exit 0' in ጽሁፍ,ጽሁፍ
            ማረጋገጥ_ዘገባ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ፋይል_ትልልፍ_ግንኙነት.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } አማርኛ.자체.ውጤት.수쓰기(합); አማርኛ.자체.ፋይል.መጻፊያ("aot.txt", "한글 AOT ፋይል 😀"); አማርኛ.자체.ውጤት.ጻፍ_መስመር(አማርኛ.자체.ፋይል.ማንበቢያ("aot.txt")); } }'
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ጽሁፍ = ሼል('javac 빛.java'); assert 'exit 0' in ጽሁፍ and 'Compiled:' in ጽሁፍ, ጽሁፍ
            ጽሁፍ = ሼል('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            ጽሁፍ = ሼል('run 빛.elf'); assert '\n55\n' in ጽሁፍ and '한글 AOT ፋይል 😀' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            자체실행파일 = bytearray(); ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ጽሁፍ = ሼል('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ጽሁፍ and 'unsupported' in ጽሁፍ, ጽሁፍ
            보존자료 = bytearray(); ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ፋይል_ትልልፍ_ግንኙነት.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ጽሁፍ = ሼል('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            ጽሁፍ = ሼል('run 빛.elf'); assert '\n55\n' in ጽሁፍ and '한글 AOT ፋይል 😀' in ጽሁፍ and 'exit 0' in ጽሁፍ, ጽሁፍ
            ማረጋገጥ_ዘገባ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ማረጋገጥ_ዘገባ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            አይንቀሳቀሴ_ምንጭ=ልኬት_ውሂብ/'정적시험.java'
            አይንቀሳቀሴ_ምንጭ.write_text('''public class 정적시험 {
 static int አሳይ_ስር = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] እሴት = new int[] {አሳይ_ስር, 합(10)};
  System.out.println(እሴት[0] + እሴት[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ልኬት_ውሂብ),str(አይንቀሳቀሴ_ምንጭ)])
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 정적시험.class',io.BytesIO((ልኬት_ውሂብ/'정적시험.class').read_bytes()))
            ጽሁፍ=ሼል('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in ጽሁፍ,ጽሁፍ
            ጽሁፍ=ሼል('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ጽሁፍ,ጽሁፍ
            ፋይል_ትልልፍ_ግንኙነት.delete('정적시험.class');ፋይል_ትልልፍ_ግንኙነት.delete('정적시험.elf')
            ማረጋገጥ_ዘገባ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ከዝን.getvalue());손상자료[14]^=1
            ፋይል_ትልልፍ_ግንኙነት.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ጽሁፍ=ሼል('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ጽሁፍ,ጽሁፍ
            ማረጋገጥ_ዘገባ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ፋይል_ትልልፍ_ግንኙነት.quit(); assert 'FTP stopped' in ሼል('ftpd stop')
            assert not ድልድይ.ስህተት, ድልድይ.ስህተት
            ማረጋገጥ_ዘገባ.update(passed=True, frames_to_guest=ድልድይ.커널수신틀수, frames_from_guest=ድልድይ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in መራጭ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ድልድይ.ላፍታ_አቁም_ፍጻሜ.set()
            ሂደቶች.terminate()
            try: ሂደቶች.wait(timeout=5)
            except subprocess.TimeoutExpired: ሂደቶች.kill(); ሂደቶች.wait()
            መራጭ.close(); ሂደቶች.stdin.close(); ሂደቶች.stdout.close()
            ማረጋገጥ_ዘገባ['bridge_error'] = ድልድይ.ስህተት
            ማረጋገጥ_ዘገባ['frames_to_guest'] = ድልድይ.커널수신틀수; ማረጋገጥ_ዘገባ['frames_from_guest'] = ድልድይ.커널발신틀수
            (ልኬት_ውሂብ/'packets.json').write_text(json.dumps(ድልድይ.ዱካ_መዝግብ,indent=2)+'\n')
            (ልኬት_ውሂብ / 'serial.log').write_bytes(대화기록)
            (ልኬት_ውሂብ / 'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ማስኬጃ()
