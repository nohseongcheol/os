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
from ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ import 기준, ᎤᏁᏤᎸᎩ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ᎠᎢᏎᏍᏗ():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / 'ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ.java'
    자바원문.write_text('public class ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.ᎪᏪᎶᏗ_ᏚᏓᏅᏅᎢ("JAR ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ: " + 인수[0]); 한국어.자체.ᎠᏍᏆᏂᎪᏙᏗ.ᎪᏪᎶᏗ("jar.txt", "자체 kernel_ᏧᎬᏩᎶᏗᏯ ᎠᏍᏆᏂᎪᏙᏗ"); 한국어.자체.출력.ᎪᏪᎶᏗ_ᏚᏓᏅᏅᎢ(한국어.자체.ᎠᏍᏆᏂᎪᏙᏗ.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    ᎠᏍᏆᏂᎪᏛᎢ = io.BytesIO()
    with zipfile.ZipFile(ᎠᏍᏆᏂᎪᏛᎢ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ\r\n\r\n')
        자바꾸러미.write(str(결과자료/'ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ.class'), 'ᎠᏓᎪᎵᏰᏍᎩ_ᎦᏇᏅᎯ.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ᏗᏯᏙᎯᎯ_ᎤᏪᎬ_ᎫᏓᎸᏗ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(ᏗᏯᏙᎯᎯ_ᎤᏪᎬ_ᎫᏓᎸᏗ), 'udp:{}:9301'.format(서버전문접속번호)], 포착여부=True) as 연결다리:
        ᎢᏯᏛᏁᎵᏓᏍᏗ = subprocess.Popen(ᎤᏁᏤᎸᎩ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ᎠᏑᏰᏍᎩ = selectors.DefaultSelector(); ᎠᏑᏰᏍᎩ.register(ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ᎦᏟᏌᏅᎯ = bytearray(); 끝위치 = time.monotonic() + 시간제한
            while 확인표시 not in ᎦᏟᏌᏅᎯ:
                if time.monotonic() > 끝위치 or ᎢᏯᏛᏁᎵᏓᏍᏗ.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ᎦᏟᏌᏅᎯ.decode('utf-8', 'replace'))
                for 누름값, _ in ᎠᏑᏰᏍᎩ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ᎦᏟᏌᏅᎯ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ᎦᏟᏌᏅᎯ or b'FAIL ' in ᎦᏟᏌᏅᎯ: raise AssertionError(ᎦᏟᏌᏅᎯ)
            return ᎦᏟᏌᏅᎯ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ᎤᏯᏍᎦ(ᏚᏓᏅᏅᎢ):
            ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write(ᏚᏓᏅᏅᎢ.encode() + b'\n'); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ᎤᏯᏍᎦ('ftpd start')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ = ftplib.FTP(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.encoding = 'utf-8'; ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.connect('127.0.0.1', 접속번호, timeout=20); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.login()
            ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ = bytes(range(256)) * 32
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR binary.dat', io.BytesIO(ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ))
            결과 = bytearray(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ; assert ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.size('binary.dat') == len(ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ)
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ᎤᏯᏍᎦ('cat 한글.txt')
            assert '한글.txt' in ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.nlst()
            assert dict(ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('oversized replacement rejected; previous file preserved')
            with ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.transfercmd('STOR pending.txt') as 올리기:
                # A control command must not change the active upload's destination.
                assert ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.size('binary.dat') == len(ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ)
                올리기.sendall(b'UPLOAD TARGET PRESERVED')
            assert ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.voidresp().startswith('226')
            결과 = bytearray(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ᎠᎫᏴᏗ_ᎠᎧᎵᎢ_ᎦᏟᏌᏅᎯ
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('pending.txt')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 인사.jar', io.BytesIO(ᎠᏍᏆᏂᎪᏛᎢ.getvalue()))
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('java -jar 인사.jar 누리')
            assert 'JAR ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ: 누리' in ᎠᎪᎵᏰᏗ and '자체 kernel_ᏧᎬᏩᎶᏗᏯ ᎠᏍᏆᏂᎪᏙᏗ' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('./인사.jar 세상')
            assert 'JAR ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ: 세상' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ᎦᏟᏌᏅᎯ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ᎦᏟᏌᏅᎯ ᏧᎬᏩᎶᏗᏯ = {합(10), 1.25}; if (ᏧᎬᏩᎶᏗᏯ.수 != 55 || ᏧᎬᏩᎶᏗᏯ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ᎯᏍᏚᎢ_ᎠᏍᏆᏂᎪᏙᏗ("cc.txt", ᎠᎪᎵᏰᏗᏊ_ᎪᏪᎶᏗ | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(문서, 인사, sizeof(인사)-1); ᎯᏍᏚᎲᎦ_ᎠᏍᏆᏂᎪᏙᏗ(문서); ᎪᏪᎶᏗ_ᎠᏍᏆᏂᎪᏙᏗ_ᎦᏟᏌᏅᎯ(1, 인사, sizeof(인사)-1); return 0; }\n'
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('run 한글.elf'); assert 'CC NATIVE PASS' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            assert 'CC NATIVE PASS' in ᎤᏯᏍᎦ('cat cc.txt')
            실행파일 = bytearray(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR ᏗᏟᎶᏍᏔᏅᎯ_ᏧᎬᏩᎶᏗᏯ.elf', io.BytesIO(실행파일)); ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('run ᏗᏟᎶᏍᏔᏅᎯ_ᏧᎬᏩᎶᏗᏯ.elf'); assert 'CC NATIVE PASS' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ', io.BytesIO(실행파일)); ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('./ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ');assert 'CC NATIVE PASS' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR ᏚᏙᎥᎢ.txt', io.BytesIO(실행파일)); ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('./ᏚᏙᎥᎢ.txt');assert 'CC NATIVE PASS' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            ᎤᏯᏍᎦ('rm ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ ᏚᏙᎥᎢ.txt')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ᎤᏯᏍᎦ('rm binary.dat 한글.txt 한글.c 한글.elf ᏗᏟᎶᏍᏔᏅᎯ_ᏧᎬᏩᎶᏗᏯ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('./리눅스인사');assert 'exit -8' in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            assert 'LINUX ELF FILE IO' in ᎤᏯᏍᎦ('cat linux.txt')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('리눅스인사');ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('linux.txt')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ᎤᏯᏍᎦ('./거짓.elf');ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('거짓.elf')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ᎫᏓᎳ = 한국어.자체.연결통신.ᎫᏓᎳ("10.0.2.2", Integer.parseInt(args[0]));
 ᎫᏓᎳ.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ᎦᏟᏌᏅᎯ_0201f362 = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ᎦᏟᏌᏅᎯ_0201f362.length;i++) if (ᎫᏓᎳ.getInputStream().read() != (ᎦᏟᏌᏅᎯ_0201f362[i]&255)) throw new RuntimeException("TCP mismatch");
 ᎫᏓᎳ.close();
 DatagramSocket 종단 = 한국어.자체.통신.ᎯᏍᏚᎢ(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.ᏫᎦᏅᏗ(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_ᎫᏓᎸᏗ, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ᎠᎪᎵᏰᏗ and '10.0.2.2' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('바깥통신.class')
            ᏗᏯᏙᎯᎯ_ᎦᏟᏌᏅᎯ=결과자료/'ᏗᏯᏙᎯᎯ_ᎠᏓᎪᎵᏰᏍᎩ.java'
            ᏗᏯᏙᎯᎯ_ᎦᏟᏌᏅᎯ.write_text('''import java.net.*; public class ᏗᏯᏙᎯᎯ_ᎠᏓᎪᎵᏰᏍᎩ {
 public static void main(String[] args) throws Exception {
  ServerSocket ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ = ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.accept();
  ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ.getOutputStream().write(ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ.getInputStream().read()+1); ᎠᏓᏩᏛᎯᏙᎯ_ᏧᎬᏩᎶᏗᏯ.close(); ᏗᏯᏙᎯᎯ_ᏧᎬᏩᎶᏗᏯ.close();
  byte[] ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ, ᎦᎸᏛᎢ_ᏧᎬᏩᎶᏗᏯ.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ᏗᏯᏙᎯᎯ_ᎦᏟᏌᏅᎯ)])
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR ᏗᏯᏙᎯᎯ_ᎠᏓᎪᎵᏰᏍᎩ.class',io.BytesIO((결과자료/'ᏗᏯᏙᎯᎯ_ᎠᏓᎪᎵᏰᏍᎩ.class').read_bytes()))
            ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.write('java ᏗᏯᏙᎯᎯ_ᎠᏓᎪᎵᏰᏍᎩ\n'.encode());ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ᏗᏯᏙᎯᎯ_ᎤᏪᎬ_ᎫᏓᎸᏗ),timeout=5) as ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ:
                ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sendall(b'A');assert ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ:
                ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.settimeout(5);ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ᏱᎦᏲᎩᎾᏛᏂ_ᏧᎬᏩᎶᏗᏯ.recvfrom(512)[0]==b'UDP-IN'
            ᎠᎪᎵᏰᏗ=수신하기();assert 'INBOUND TCP UDP PASS' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('ᏗᏯᏙᎯᎯ_ᎠᏓᎪᎵᏰᏍᎩ.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.ᎠᏍᏆᏂᎪᏙᏗ.ᎪᏪᎶᏗ("aot.txt", "한글 AOT ᎠᏍᏆᏂᎪᏙᏗ 😀"); 한국어.자체.출력.ᎪᏪᎶᏗ_ᏚᏓᏅᏅᎢ(한국어.자체.ᎠᏍᏆᏂᎪᏙᏗ.읽기("aot.txt")); } }'
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('javac 빛.java'); assert 'exit 0' in ᎠᎪᎵᏰᏗ and 'Compiled:' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('run 빛.elf'); assert '\n55\n' in ᎠᎪᎵᏰᏗ and '한글 AOT ᎠᏍᏆᏂᎪᏙᏗ 😀' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            자체실행파일 = bytearray(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ᎠᎪᎵᏰᏗ and 'unsupported' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            보존자료 = bytearray(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            ᎠᎪᎵᏰᏗ = ᎤᏯᏍᎦ('run 빛.elf'); assert '\n55\n' in ᎠᎪᎵᏰᏗ and '한글 AOT ᎠᏍᏆᏂᎪᏙᏗ 😀' in ᎠᎪᎵᏰᏗ and 'exit 0' in ᎠᎪᎵᏰᏗ, ᎠᎪᎵᏰᏗ
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ᎾᏓᏅᏍᎬᎾ_ᎦᏟᏌᏅᎯ=결과자료/'ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ.java'
            ᎾᏓᏅᏍᎬᎾ_ᎦᏟᏌᏅᎯ.write_text('''public class ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] ᏧᎬᏩᎶᏗᏯ = new int[] {기준, 합(10)};
  System.out.println(ᏧᎬᏩᎶᏗᏯ[0] + ᏧᎬᏩᎶᏗᏯ[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ᎾᏓᏅᏍᎬᎾ_ᎦᏟᏌᏅᎯ)])
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ.class',io.BytesIO((결과자료/'ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ.class').read_bytes()))
            ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('jaot ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ.class -o ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ.elf');assert 'exit 0' in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('run ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ.class');ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.delete('ᎾᏓᏅᏍᎬᎾ_ᎠᏓᎪᎵᏰᏍᎩ.elf')
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ᎠᏍᏆᏂᎪᏛᎢ.getvalue());손상자료[14]^=1
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ᎠᎪᎵᏰᏗ=ᎤᏯᏍᎦ('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ᎠᎪᎵᏰᏗ,ᎠᎪᎵᏰᏗ
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ᎠᏍᏆᏂᎪᏙᏗ_ᎠᎲᏍᏗ_ᎫᏓᎸᎢ.quit(); assert 'FTP stopped' in ᎤᏯᏍᎦ('ftpd stop')
            assert not 연결다리.ᎦᎵᏓᏍᏔᏅ, 연결다리.ᎦᎵᏓᏍᏔᏅ
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in ᎠᏑᏰᏍᎩ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.ᎯᏲᎯᏍᏓ_ᎢᏳᎵᏍᏔᏂᏓᏍᏗᎢ.set()
            ᎢᏯᏛᏁᎵᏓᏍᏗ.terminate()
            try: ᎢᏯᏛᏁᎵᏓᏍᏗ.wait(timeout=5)
            except subprocess.TimeoutExpired: ᎢᏯᏛᏁᎵᏓᏍᏗ.kill(); ᎢᏯᏛᏁᎵᏓᏍᏗ.wait()
            ᎠᏑᏰᏍᎩ.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdin.close(); ᎢᏯᏛᏁᎵᏓᏍᏗ.stdout.close()
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['bridge_error'] = 연결다리.ᎦᎵᏓᏍᏔᏅ
            ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['frames_to_guest'] = 연결다리.커널수신틀수; ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(ᎤᏙᎯᏳᏒᎢ_ᎬᏂᎨᏒᎢᎬᏁᏗ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ᎠᎢᏎᏍᏗ()
