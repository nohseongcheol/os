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
from Ցանց_կամուրջ import Ցանց_կամուրջ
from կատարել_հրաման import արձակել_արմատ, Հրահանգ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Գործարկել():
    չափ_տվյալ = արձակել_արմատ / 'build/verification/ftp'; չափ_տվյալ.mkdir(parents=True, exist_ok=True)
    վավերացում_զեկույց = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((արձակել_արմատ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = չափ_տվյալ / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.Ելք.գրել_կապ("JAR կատարել_հրաման: " + 인수[0]); 한국어.자체.Ֆայլ.Գրել("jar.txt", "자체 միջուկ_արժեք Ֆայլ"); 한국어.자체.Ելք.գրել_կապ(한국어.자체.Ֆայլ.Ընթերցում("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(արձակել_արմատ/'build/java-library/classes'), '-d', str(չափ_տվյալ), str(자바원문)])
    Պահոց = io.BytesIO()
    with zipfile.ZipFile(Պահոց, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(չափ_տվյալ/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); սպասարկիչ_հոսք_միացք = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Ցանց_կամուրջ(접속번호, ['tcp:{}:9300'.format(սպասարկիչ_հոսք_միացք), 'udp:{}:9301'.format(서버전문접속번호)], նկարահանել=True) as կամուրջ:
        Գործընթաց = subprocess.Popen(Հրահանգ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + կամուրջ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ընտրիչ = selectors.DefaultSelector(); ընտրիչ.register(Գործընթաց.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            տվյալ = bytearray(); վերջացնել_Տեղաշարժում = time.monotonic() + 시간제한
            while 확인표시 not in տվյալ:
                if time.monotonic() > վերջացնել_Տեղաշարժում or Գործընթաց.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + տվյալ.decode('utf-8', 'replace'))
                for 누름값, _ in ընտրիչ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: տվյալ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in տվյալ or b'FAIL ' in տվյալ: raise AssertionError(տվյալ)
            return տվյալ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def խեցի(կապ):
            Գործընթաց.stdin.write(կապ.encode() + b'\n'); Գործընթաց.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in խեցի('ftpd start')
            նիշք_փոխանցել_կապ = ftplib.FTP(); նիշք_փոխանցել_կապ.encoding = 'utf-8'; նիշք_փոխանցել_կապ.connect('127.0.0.1', 접속번호, timeout=20); նիշք_փոխանցել_կապ.login()
            օգտակար_բեռնվածք_տվյալ = bytes(range(256)) * 32
            նիշք_փոխանցել_կապ.storbinary('STOR binary.dat', io.BytesIO(օգտակար_բեռնվածք_տվյալ))
            չափ = bytearray(); նիշք_փոխանցել_կապ.retrbinary('RETR binary.dat', չափ.extend)
            assert չափ == օգտակար_բեռնվածք_տվյալ; assert նիշք_փոխանցել_կապ.size('binary.dat') == len(օգտակար_բեռնվածք_տվյալ)
            վավերացում_զեկույց['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            նիշք_փոխանցել_կապ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in խեցի('cat 한글.txt')
            assert '한글.txt' in նիշք_փոխանցել_կապ.nlst()
            assert dict(նիշք_փոխանցել_կապ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            վավերացում_զեկույց['checks'].append('UTF-8 filename and content visible in guest shell')
            try: նիշք_փոխանցել_կապ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            չափ = bytearray(); նիշք_փոխանցել_կապ.retrbinary('RETR binary.dat', չափ.extend); assert չափ == օգտակար_բեռնվածք_տվյալ
            վավերացում_զեկույց['checks'].append('oversized replacement rejected; previous file preserved')
            with նիշք_փոխանցել_կապ.transfercmd('STOR pending.txt') as վերբեռնել_Նիշքեր:
                # A control command must not change the active upload's destination.
                assert նիշք_փոխանցել_կապ.size('binary.dat') == len(օգտակար_բեռնվածք_տվյալ)
                վերբեռնել_Նիշքեր.sendall(b'UPLOAD TARGET PRESERVED')
            assert նիշք_փոխանցել_կապ.voidresp().startswith('226')
            չափ = bytearray(); նիշք_փոխանցել_կապ.retrbinary('RETR pending.txt', չափ.extend)
            assert չափ == b'UPLOAD TARGET PRESERVED'
            չափ = bytearray(); նիշք_փոխանցել_կապ.retrbinary('RETR binary.dat', չափ.extend)
            assert չափ == օգտակար_բեռնվածք_տվյալ
            նիշք_փոխանցել_կապ.delete('pending.txt')
            վավերացում_զեկույց['checks'].append('interleaved SIZE cannot change the active STOR destination')
            նիշք_փոխանցել_կապ.storbinary('STOR 인사.jar', io.BytesIO(Պահոց.getvalue()))
            Տեքստ = խեցի('java -jar 인사.jar 누리')
            assert 'JAR կատարել_հրաման: 누리' in Տեքստ and '자체 միջուկ_արժեք Ֆայլ' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            Տեքստ = խեցի('./인사.jar 세상')
            assert 'JAR կատարել_հրաման: 세상' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            վավերացում_զեկույց['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct տվյալ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct տվյալ արժեք = {합(10), 1.25}; if (արժեք.수 != 55 || արժեք.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = բացել_նիշք("cc.txt", կարդալ_գրել | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; գրել_նիշք_տվյալ(문서, 인사, sizeof(인사)-1); փակել_նիշք(문서); գրել_նիշք_տվյալ(1, 인사, sizeof(인사)-1); return 0; }\n'
            նիշք_փոխանցել_կապ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Տեքստ = խեցի('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            Տեքստ = խեցի('run 한글.elf'); assert 'CC NATIVE PASS' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            assert 'CC NATIVE PASS' in խեցի('cat cc.txt')
            실행파일 = bytearray(); նիշք_փոխանցել_կապ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            նիշք_փոխանցել_կապ.storbinary('STOR պատճեն_արժեք.elf', io.BytesIO(실행파일)); Տեքստ = խեցի('run պատճեն_արժեք.elf'); assert 'CC NATIVE PASS' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            նիշք_փոխանցել_կապ.storbinary('STOR կատարել_հրաման', io.BytesIO(실행파일)); Տեքստ=խեցի('./կատարել_հրաման');assert 'CC NATIVE PASS' in Տեքստ and 'exit 0' in Տեքստ,Տեքստ
            նիշք_փոխանցել_կապ.storbinary('STOR Անուն.txt', io.BytesIO(실행파일)); Տեքստ=խեցի('./Անուն.txt');assert 'CC NATIVE PASS' in Տեքստ and 'exit 0' in Տեքստ,Տեքստ
            խեցի('rm կատարել_հրաման Անուն.txt')
            վավերացում_զեկույց['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            խեցի('rm binary.dat 한글.txt 한글.c 한글.elf պատճեն_արժեք.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(չափ_տվյալ/'linux-reference')
            նիշք_փոխանցել_կապ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Տեքստ=խեցի('./리눅스인사');assert 'exit -8' in Տեքստ,Տեքստ
            Տեքստ=խեցի('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Տեքստ,Տեքստ
            assert 'LINUX ELF FILE IO' in խեցի('cat linux.txt')
            նիշք_փոխանցել_կապ.delete('리눅스인사');նիշք_փոխանցել_կապ.delete('linux.txt')
            նիշք_փոխանցել_կապ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in խեցի('./거짓.elf');նիշք_փոխանցել_կապ.delete('거짓.elf')
            վավերացում_զեկույց['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = չափ_տվյալ/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Միացնել = 한국어.자체.연결통신.Միացնել("10.0.2.2", Integer.parseInt(args[0]));
 Միացնել.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ԱՂԲՅՈՒՐ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ԱՂԲՅՈՒՐ.length;i++) if (Միացնել.getInputStream().read() != (ԱՂԲՅՈՒՐ[i]&255)) throw new RuntimeException("TCP mismatch");
 Միացնել.close();
 DatagramSocket 종단 = 한국어.자체.통신.Բաց(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.ուղարկել(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(արձակել_արմատ/'build/java-library/classes'),'-d',str(չափ_տվյալ),str(통신원문)])
                նիշք_փոխանցել_կապ.storbinary('STOR 바깥통신.class', io.BytesIO((չափ_տվյալ/'바깥통신.class').read_bytes()))
                Տեքստ = խեցի('java 바깥통신 {} {}'.format(되돌림서버항목.Փոխանցման_կառավարման_հաղորդակարգ_միացք, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Տեքստ and '10.0.2.2' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            վավերացում_զեկույց['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            նիշք_փոխանցել_կապ.delete('바깥통신.class')
            սպասարկիչ_աղբյուր=չափ_տվյալ/'서버시험.java'
            սպասարկիչ_աղբյուր.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket սպասարկիչ_արժեք = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket հյուր_արժեք = սպասարկիչ_արժեք.accept();
  հյուր_արժեք.getOutputStream().write(հյուր_արժեք.getInputStream().read()+1); հյուր_արժեք.close(); սպասարկիչ_արժեք.close();
  byte[] Բովանդակություն_արժեք = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Բովանդակություն_արժեք, Բովանդակություն_արժեք.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(չափ_տվյալ),str(սպասարկիչ_աղբյուր)])
            նիշք_փոխանցել_կապ.storbinary('STOR 서버시험.class',io.BytesIO((չափ_տվյալ/'서버시험.class').read_bytes()))
            Գործընթաց.stdin.write('java 서버시험\n'.encode());Գործընթաց.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',սպասարկիչ_հոսք_միացք),timeout=5) as հավասարազոր_սարք_արժեք:
                հավասարազոր_սարք_արժեք.sendall(b'A');assert հավասարազոր_սարք_արժեք.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as հավասարազոր_սարք_արժեք:
                հավասարազոր_սարք_արժեք.settimeout(5);հավասարազոր_սարք_արժեք.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert հավասարազոր_սարք_արժեք.recvfrom(512)[0]==b'UDP-IN'
            Տեքստ=수신하기();assert 'INBOUND TCP UDP PASS' in Տեքստ and 'exit 0' in Տեքստ,Տեքստ
            վավերացում_զեկույց['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            նիշք_փոխանցել_կապ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.Ելք.수쓰기(합); 한국어.자체.Ֆայլ.Գրել("aot.txt", "한글 AOT Ֆայլ 😀"); 한국어.자체.Ելք.գրել_կապ(한국어.자체.Ֆայլ.Ընթերցում("aot.txt")); } }'
            նիշք_փոխանցել_կապ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Տեքստ = խեցի('javac 빛.java'); assert 'exit 0' in Տեքստ and 'Compiled:' in Տեքստ, Տեքստ
            Տեքստ = խեցի('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            Տեքստ = խեցի('run 빛.elf'); assert '\n55\n' in Տեքստ and '한글 AOT Ֆայլ 😀' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            자체실행파일 = bytearray(); նիշք_փոխանցել_կապ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Տեքստ = խեցի('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Տեքստ and 'unsupported' in Տեքստ, Տեքստ
            보존자료 = bytearray(); նիշք_փոխանցել_կապ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); նիշք_փոխանցել_կապ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            նիշք_փոխանցել_կապ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Տեքստ = խեցի('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            Տեքստ = խեցի('run 빛.elf'); assert '\n55\n' in Տեքստ and '한글 AOT Ֆայլ 😀' in Տեքստ and 'exit 0' in Տեքստ, Տեքստ
            վավերացում_զեկույց['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            վավերացում_զեկույց['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            հաստատուն_աղբյուր=չափ_տվյալ/'정적시험.java'
            հաստատուն_աղբյուր.write_text('''public class 정적시험 {
 static int արձակել_արմատ = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] արժեք = new int[] {արձակել_արմատ, 합(10)};
  System.out.println(արժեք[0] + արժեք[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(չափ_տվյալ),str(հաստատուն_աղբյուր)])
            նիշք_փոխանցել_կապ.storbinary('STOR 정적시험.class',io.BytesIO((չափ_տվյալ/'정적시험.class').read_bytes()))
            Տեքստ=խեցի('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Տեքստ,Տեքստ
            Տեքստ=խեցի('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Տեքստ,Տեքստ
            նիշք_փոխանցել_կապ.delete('정적시험.class');նիշք_փոխանցել_կապ.delete('정적시험.elf')
            վավերացում_զեկույց['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Պահոց.getvalue());손상자료[14]^=1
            նիշք_փոխանցել_կապ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Տեքստ=խեցի('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Տեքստ,Տեքստ
            վավերացում_զեկույց['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            նիշք_փոխանցել_կապ.quit(); assert 'FTP stopped' in խեցի('ftpd stop')
            assert not կամուրջ.Սխալ, կամուրջ.Սխալ
            վավերացում_զեկույց.update(passed=True, frames_to_guest=կամուրջ.커널수신틀수, frames_from_guest=կամուրջ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in ընտրիչ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            կամուրջ.դադար_միջոցառում.set()
            Գործընթաց.terminate()
            try: Գործընթաց.wait(timeout=5)
            except subprocess.TimeoutExpired: Գործընթաց.kill(); Գործընթաց.wait()
            ընտրիչ.close(); Գործընթաց.stdin.close(); Գործընթաց.stdout.close()
            վավերացում_զեկույց['bridge_error'] = կամուրջ.Սխալ
            վավերացում_զեկույց['frames_to_guest'] = կամուրջ.커널수신틀수; վավերացում_զեկույց['frames_from_guest'] = կամուրջ.커널발신틀수
            (չափ_տվյալ/'packets.json').write_text(json.dumps(կամուրջ.추적기록,indent=2)+'\n')
            (չափ_տվյալ / 'serial.log').write_bytes(대화기록)
            (չափ_տվյալ / 'report.json').write_text(json.dumps(վավերացում_զեկույց, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Գործարկել()
