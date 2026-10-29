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
from 통신다리 import 통신다리
from 실행 import 기준, команда
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def 시작():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    провјера_извјештај = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.писати_редак("JAR 실행: " + 인수[0]); 한국어.자체.фајл.писати("jar.txt", "자체 језгро_вриједност фајл"); 한국어.자체.출력.писати_редак(한국어.자체.фајл.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    архива = io.BytesIO()
    with zipfile.ZipFile(архива, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); сервер_ток_порт = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(сервер_ток_порт), 'udp:{}:9301'.format(서버전문접속번호)], 포착여부=True) as 연결다리:
        процес = subprocess.Popen(команда() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(процес.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            подаци = bytearray(); 끝위치 = time.monotonic() + 시간제한
            while 확인표시 not in подаци:
                if time.monotonic() > 끝위치 or процес.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + подаци.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: подаци.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in подаци or b'FAIL ' in подаци: raise AssertionError(подаци)
            return подаци.decode('utf-8', 'replace').replace('\r\n', '\n')
        def љуска(редак):
            процес.stdin.write(редак.encode() + b'\n'); процес.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in љуска('ftpd start')
            фајл_пријенос_веза = ftplib.FTP(); фајл_пријенос_веза.encoding = 'utf-8'; фајл_пријенос_веза.connect('127.0.0.1', 접속번호, timeout=20); фајл_пријенос_веза.login()
            корисни_садржај_подаци = bytes(range(256)) * 32
            фајл_пријенос_веза.storbinary('STOR binary.dat', io.BytesIO(корисни_садржај_подаци))
            결과 = bytearray(); фајл_пријенос_веза.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == корисни_садржај_подаци; assert фајл_пријенос_веза.size('binary.dat') == len(корисни_садржај_подаци)
            провјера_извјештај['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            фајл_пријенос_веза.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in љуска('cat 한글.txt')
            assert '한글.txt' in фајл_пријенос_веза.nlst()
            assert dict(фајл_пријенос_веза.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            провјера_извјештај['checks'].append('UTF-8 filename and content visible in guest shell')
            try: фајл_пријенос_веза.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); фајл_пријенос_веза.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == корисни_садржај_подаци
            провјера_извјештај['checks'].append('oversized replacement rejected; previous file preserved')
            with фајл_пријенос_веза.transfercmd('STOR pending.txt') as 올리기:
                # A control command must not change the active upload's destination.
                assert фајл_пријенос_веза.size('binary.dat') == len(корисни_садржај_подаци)
                올리기.sendall(b'UPLOAD TARGET PRESERVED')
            assert фајл_пријенос_веза.voidresp().startswith('226')
            결과 = bytearray(); фајл_пријенос_веза.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); фајл_пријенос_веза.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == корисни_садржај_подаци
            фајл_пријенос_веза.delete('pending.txt')
            провјера_извјештај['checks'].append('interleaved SIZE cannot change the active STOR destination')
            фајл_пријенос_веза.storbinary('STOR 인사.jar', io.BytesIO(архива.getvalue()))
            текст = љуска('java -jar 인사.jar 누리')
            assert 'JAR 실행: 누리' in текст and '자체 језгро_вриједност фајл' in текст and 'exit 0' in текст, текст
            текст = љуска('./인사.jar 세상')
            assert 'JAR 실행: 세상' in текст and 'exit 0' in текст, текст
            провјера_извјештај['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct подаци { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct подаци вриједност = {합(10), 1.25}; if (вриједност.수 != 55 || вриједност.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = отворити_фајл("cc.txt", и_за_читање_и_за_писање | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; писати_фајл_подаци(문서, 인사, sizeof(인사)-1); затворити_фајл(문서); писати_фајл_подаци(1, 인사, sizeof(인사)-1); return 0; }\n'
            фајл_пријенос_веза.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            текст = љуска('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = љуска('run 한글.elf'); assert 'CC NATIVE PASS' in текст and 'exit 0' in текст, текст
            assert 'CC NATIVE PASS' in љуска('cat cc.txt')
            실행파일 = bytearray(); фајл_пријенос_веза.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            фајл_пријенос_веза.storbinary('STOR инстанца_вриједност.elf', io.BytesIO(실행파일)); текст = љуска('run инстанца_вриједност.elf'); assert 'CC NATIVE PASS' in текст and 'exit 0' in текст, текст
            фајл_пријенос_веза.storbinary('STOR 실행', io.BytesIO(실행파일)); текст=љуска('./실행');assert 'CC NATIVE PASS' in текст and 'exit 0' in текст,текст
            фајл_пријенос_веза.storbinary('STOR назив.txt', io.BytesIO(실행파일)); текст=љуска('./назив.txt');assert 'CC NATIVE PASS' in текст and 'exit 0' in текст,текст
            љуска('rm 실행 назив.txt')
            провјера_извјештај['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            љуска('rm binary.dat 한글.txt 한글.c 한글.elf инстанца_вриједност.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            фајл_пријенос_веза.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            текст=љуска('./리눅스인사');assert 'exit -8' in текст,текст
            текст=љуска('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in текст,текст
            assert 'LINUX ELF FILE IO' in љуска('cat linux.txt')
            фајл_пријенос_веза.delete('리눅스인사');фајл_пријенос_веза.delete('linux.txt')
            фајл_пријенос_веза.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in љуска('./거짓.elf');фајл_пријенос_веза.delete('거짓.elf')
            провјера_извјештај['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket повезати = 한국어.자체.연결통신.повезати("10.0.2.2", Integer.parseInt(args[0]));
 повезати.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] извор = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<извор.length;i++) if (повезати.getInputStream().read() != (извор[i]&255)) throw new RuntimeException("TCP mismatch");
 повезати.close();
 DatagramSocket крајња_тачка = 한국어.자체.통신.отворити(0); 한국어.자체.통신.대기시간(крајња_тачка, 500);
 한국어.자체.통신.послати(крајња_тачка, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(крајња_тачка).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 крајња_тачка.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                фајл_пријенос_веза.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                текст = љуска('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_порт, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in текст and '10.0.2.2' in текст and 'exit 0' in текст, текст
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            провјера_извјештај['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            фајл_пријенос_веза.delete('바깥통신.class')
            сервер_извор=결과자료/'서버시험.java'
            сервер_извор.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket сервер_вриједност = new ServerSocket(9300); DatagramSocket крајња_тачка = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = сервер_вриједност.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); сервер_вриједност.close();
  byte[] Садржај_вриједност = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Садржај_вриједност, Садржај_вриједност.length); крајња_тачка.receive(전문);
  крајња_тачка.send(전문); крајња_тачка.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(сервер_извор)])
            фајл_пријенос_веза.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            процес.stdin.write('java 서버시험\n'.encode());процес.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',сервер_ток_порт),timeout=5) as peer_вриједност:
                peer_вриједност.sendall(b'A');assert peer_вриједност.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peer_вриједност:
                peer_вриједност.settimeout(5);peer_вриједност.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert peer_вриједност.recvfrom(512)[0]==b'UDP-IN'
            текст=수신하기();assert 'INBOUND TCP UDP PASS' in текст and 'exit 0' in текст,текст
            провјера_извјештај['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            фајл_пријенос_веза.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.фајл.писати("aot.txt", "한글 AOT фајл 😀"); 한국어.자체.출력.писати_редак(한국어.자체.фајл.읽기("aot.txt")); } }'
            фајл_пријенос_веза.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            текст = љуска('javac 빛.java'); assert 'exit 0' in текст and 'Compiled:' in текст, текст
            текст = љуска('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = љуска('run 빛.elf'); assert '\n55\n' in текст and '한글 AOT фајл 😀' in текст and 'exit 0' in текст, текст
            자체실행파일 = bytearray(); фајл_пријенос_веза.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            текст = љуска('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in текст and 'unsupported' in текст, текст
            보존자료 = bytearray(); фајл_пријенос_веза.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); фајл_пријенос_веза.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            фајл_пријенос_веза.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            текст = љуска('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in текст and 'exit 0' in текст, текст
            текст = љуска('run 빛.elf'); assert '\n55\n' in текст and '한글 AOT фајл 😀' in текст and 'exit 0' in текст, текст
            провјера_извјештај['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            провјера_извјештај['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            статични_извор=결과자료/'정적시험.java'
            статични_извор.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] вриједност = new int[] {기준, 합(10)};
  System.out.println(вриједност[0] + вриједност[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(статични_извор)])
            фајл_пријенос_веза.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            текст=љуска('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in текст,текст
            текст=љуска('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in текст,текст
            фајл_пријенос_веза.delete('정적시험.class');фајл_пријенос_веза.delete('정적시험.elf')
            провјера_извјештај['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(архива.getvalue());손상자료[14]^=1
            фајл_пријенос_веза.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            текст=љуска('java -jar 인사.jar');assert 'Main-Class\nexit 1' in текст,текст
            провјера_извјештај['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            фајл_пријенос_веза.quit(); assert 'FTP stopped' in љуска('ftpd stop')
            assert not 연결다리.грешка, 연결다리.грешка
            провјера_извјештај.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.пауза_догађај.set()
            процес.terminate()
            try: процес.wait(timeout=5)
            except subprocess.TimeoutExpired: процес.kill(); процес.wait()
            준비선택기.close(); процес.stdin.close(); процес.stdout.close()
            провјера_извјештај['bridge_error'] = 연결다리.грешка
            провјера_извјештај['frames_to_guest'] = 연결다리.커널수신틀수; провјера_извјештај['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(провјера_извјештај, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': 시작()
