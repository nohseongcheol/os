#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 Jalankan_perintah, kegagalan_VALUE/sumber_daya_VALUE 경계 pengujian."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import time
from 사용자통신시험 import mesin_virtual, posisi


def Edit_VALUE(mesin, Nama_2, Isi_VALUE, Store_VALUE=True):
    jalankan = len(mesin.LOG_baris)
    mesin.직렬.sendall(('edit ' + Nama_2 + '\n').encode())
    mesin.tunggu_Status('...> ', jalankan)
    for baris_masukan in Isi_VALUE.splitlines():
        assert len(baris_masukan) <= 128
        jalankan = len(mesin.LOG_baris)
        mesin.직렬.sendall((baris_masukan + '\n').encode())
        mesin.tunggu_Status('...> ', jalankan)
    jalankan = len(mesin.LOG_baris)
    mesin.직렬.sendall(b'.save\n' if Store_VALUE else b'.cancel\n')
    hasil = mesin.tunggu_Status('jkoros> ', jalankan)
    assert ('Saved:' if Store_VALUE else 'Cancelled; original preserved') in hasil, hasil


def file_surel():
    hasil = subprocess.check_output(['nm', '-n', str(posisi / 'build/kernel.elf')], universal_newlines=True)
    for baris_masukan in hasil.splitlines():
        if baris_masukan.endswith(' ram_files'):
            return int(baris_masukan.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def tamu_file(mesin, slot_VALUE, Ukuran, jalur):
    # pengujian VM의 메모리에서 aktual_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    surel = file_surel() + slot_VALUE * 16384
    mesin.pantau_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(surel, Ukuran, jalur)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if jalur.exists() and jalur.stat().st_size == Ukuran:
            return jalur.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    mesin = mesin_virtual(posisi / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, jaringan_VALUE=False)
    hasil = {}
    try:
        mesin.perintah('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        mesin.perintah('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        mesin.perintah('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        mesin.perintah('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        mesin.perintah('java Missing', ['cannot read class: -2', 'Exit: 1'])
        mesin.perintah('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        mesin.perintah('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Isi_VALUE = '''public class Calc {
 public static int fact(int n) {
  if (n <= 1) { return 1; } else { return n * fact(n - 1); }
 }
 public static boolean check(int n) { return n == 7; }
 public static void main(String[] args) {
  int n = Integer.parseInt(args[0]);
  System.out.println(fact(n));
  int sum = 0;
  for (int i = 1; i <= n; i++) { sum = sum + i; }
  while (n > 0) { n--; }
  System.out.println(sum);
  System.out.println(n);
  System.out.println(check(7) && false || true);
  System.out.println(false && 1 / 0 == 0);
  System.out.println(true || 1 / 0 == 0);
  System.out.println(-2147483648 / -1);
  System.out.println(args[1]);
  System.out.println(args[1].length());
  System.out.println(args.length);
  String label = "sum=";
  label += sum;
  System.out.println(label);
  System.out.println(12 + "x" + false);
  System.out.println("logic=" + (true && check(7)));
  char letter = 'a';
  letter++;
  System.out.println(letter);
  System.out.println("letter=" + letter);
  int extra = 7;
  extra *= 3;
  extra -= 1;
  System.out.println(extra);
 }
}'''
        Edit_VALUE(mesin, 'Calc.java', Isi_VALUE)
        mesin.perintah('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        keluaranTeks = mesin.perintah('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        hasil['guest_output'] = keluaranTeks
        entri_Daftar = mesin.perintah('ls', ['Calc.class'])
        Ukuran = int(re.search(r'Calc\.class\s+(\d+) bytes', entri_Daftar).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as Direktori_VALUE:
            jalur = Path(Direktori_VALUE) / 'Calc.class'
            data = tamu_file(mesin, 3, Ukuran, jalur)
            aktual_data = subprocess.check_output(['java', '-Xverify:all', '-cp', Direktori_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert aktual_data.splitlines() == 기대, aktual_data
            hasil['class_sha256'] = hashlib.sha256(data).hexdigest()
            hasil['openjdk_output'] = aktual_data
        # 실패한 Edit_VALUE/컴파일은 기존 class를 보존한다.
        Edit_VALUE(mesin, 'Calc.java', 'not Java at all', Store_VALUE=False)
        mesin.perintah('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for tidak_sahih_KR in [
            'public class Calc { public static void main(String[] args) { int x = ; } }',
            'public class Calc { public static void main(String[] args) { int x = true; } }',
            'public class Calc { public static void main(String[] args) { int x = 2147483648; } }',
            'public class Calc { public static int f() { int x = 1; } }',
            'public class Calc { public static void main(String[] args) { Object x = new Object(); } }',
            'public class Other { public static void main(String[] args) {} }',
            'public class Calc { public static void main(String[] args) { int while = 3; } }',
            'public class Calc { public static void main(String[] args) { if (true) int x = 3; } }',
            'public class Calc { public static void main(String[] args) { int x = 010; } }',
        ]:
            Edit_VALUE(mesin, 'Calc.java', tidak_sahih_KR)
            mesin.perintah('javac Calc.java', ['javac error:', 'Exit: 1'])
            mesin.perintah('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # sprint_VALUE 실행은 ruang_pengguna 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            mesin.perintah('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        mesin.perintah('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        mesin.perintah('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        Edit_VALUE(mesin, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        mesin.perintah('javac Calc.java', ['Compiled:', 'Exit: 0'])
        mesin.perintah('java Calc', ['instruction limit', 'Exit: 1'])
        mesin.perintah('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        Edit_VALUE(mesin, 'Bad.class', 'garbage')
        mesin.perintah('java Bad', ['JVM error:', 'Exit: 1'])
        mesin.perintah('rm Bad.class', ['Removed'])
        mesin.perintah('java Bad', ['cannot read class: -2'])
        # Edit_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        jalankan = len(mesin.LOG_baris)
        mesin.직렬.sendall(b'edit Hello.java\n')
        mesin.tunggu_Status('...> ', jalankan)
        jalankan = len(mesin.LOG_baris)
        mesin.직렬.sendall(b'x' * 129 + b'\n')
        mesin.tunggu_Status('...> ', jalankan)
        mesin.perintah('.save', ['Too much input; original preserved'])
        mesin.perintah('javac Hello.java', ['Compiled:', 'Exit: 0'])
        Edit_VALUE(mesin, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            Edit_VALUE(mesin, 'f' + str(수), 'occupied')
        mesin.perintah('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        mesin.perintah('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in mesin.LOG_baris.decode('utf-8', 'replace')
        hasil['serial'] = mesin.LOG_baris.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return hasil
    finally:
        mesin.Tutup()


def 주코드(data):
    """손상 시험용 main Code의 aktual_data berkas 오프셋/길이만 읽는다."""
    posisi_VALUE = 8
    def 짧():
        nonlocal posisi_VALUE
        VALUE = struct.unpack_from('>H', data, posisi_VALUE)[0]
        posisi_VALUE += 2
        return VALUE
    def 정():
        nonlocal posisi_VALUE
        VALUE = struct.unpack_from('>I', data, posisi_VALUE)[0]
        posisi_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = data[posisi_VALUE]
        posisi_VALUE += 1
        if 종류 == 1:
            panjang_VALUE = 짧()
            문자들[수] = data[posisi_VALUE:posisi_VALUE + panjang_VALUE]
            posisi_VALUE += panjang_VALUE
        elif 종류 in (7, 8): posisi_VALUE += 2
        elif 종류 in (3, 9, 10, 12): posisi_VALUE += 4
        else: raise AssertionError(종류)
    posisi_VALUE += 6
    item_COUNT = 짧()
    posisi_VALUE += item_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Nama_2 = 짧()
        짧()
        for 수 in range(짧()):
            nilai_atribut = 짧()
            Ukuran = 정()
            if 문자들[Nama_2] == b'main' and 문자들[nilai_atribut] == b'Code':
                return posisi_VALUE + 8, struct.unpack_from('>I', data, posisi_VALUE + 4)[0]
            posisi_VALUE += Ukuran
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        Direktori_VALUE = Path(임시)
        (Direktori_VALUE / 'build').mkdir()
        kodeSumber = Direktori_VALUE / 'Imported.java'
        kodeSumber.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(kodeSumber)], check=True)
        원본 = (Direktori_VALUE / 'Imported.class').read_bytes()
        CODE_VALUE, panjang_VALUE = 주코드(원본)
        변형 = {}
        data = bytearray(원본); data[0] = 0; 변형['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; 변형['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; 변형['BadPool'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + panjang_VALUE] = bytes(panjang_VALUE)
        data[CODE_VALUE:CODE_VALUE + 3] = b'\xa7\x00\x01'; data[CODE_VALUE + panjang_VALUE - 1] = 177; 변형['BadJump'] = data
        data = bytearray(원본); data[CODE_VALUE:CODE_VALUE + panjang_VALUE] = bytes(panjang_VALUE)
        data[CODE_VALUE] = 87; data[CODE_VALUE + panjang_VALUE - 1] = 177; 변형['BadStack'] = data
        # Nama_2 검사를 통과시켜 aktual_data Jalankan_perintah 중의 operand_tumpuk 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        entri_VALUE = ['Imported.class=' + str(Direktori_VALUE / 'Imported.class'), 'Imported.java=' + str(kodeSumber)]
        for Nama_2, data in 변형.items():
            jalur = Direktori_VALUE / (Nama_2 + '.class'); jalur.write_bytes(data)
            entri_VALUE.append(Nama_2 + '.class=' + str(jalur))
        grup_VALUE = Direktori_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(posisi / 'alat/자바파일묶기.py'), '-o', str(grup_VALUE)] + entri_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(Direktori_VALUE / 'user.o'), str(posisi / 'awal_mesin/ruang_pengguna.s')], cwd=str(Direktori_VALUE), check=True)
        kernel_VALUE = Direktori_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(posisi / 'awal_mesin/tata_letak_penautan.ld'), '-o', str(kernel_VALUE),
                        str(posisi / 'build/boot.o'), str(posisi / 'build/java.o'), str(Direktori_VALUE / 'user.o'), str(posisi / 'build/apps.o')], check=True)
        mesin = mesin_virtual(kernel_VALUE, jaringan_VALUE=False)
        try:
            mesin.perintah('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            mesin.perintah('cat Imported.java', ['int[] values = new int[3]'])
            for Nama_2, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                mesin.perintah('java ' + Nama_2, [문구, 'Exit: 1'])
                mesin.perintah('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()


if __name__ == '__main__':
    urai_VALUE = argparse.ArgumentParser()
    urai_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    argumen = urai_VALUE.parse_args()
    hasil = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if argumen.boot == 'both' else (argumen.boot,))}
    hasil['import'] = 적재시험()
    (posisi / 'build/자바시험.json').write_text(json.dumps(hasil, ensure_ascii=False, indent=2) + '\n')
