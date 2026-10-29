#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 laksanakan_perintah, kegagalan_VALUE/sumber_VALUE 경계 ujian."""
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
from ujian_pengguna_rangkaian import mesin_maya, Kedudukan


def edit_VALUE(mesin, Nama, Kandungan_VALUE, stor_VALUE=True):
    Jalan = len(mesin.LOG_baris)
    mesin.직렬.sendall(('edit ' + Nama + '\n').encode())
    mesin.keadaan_tunggu('...> ', Jalan)
    for baris in Kandungan_VALUE.splitlines():
        assert len(baris) <= 128
        Jalan = len(mesin.LOG_baris)
        mesin.직렬.sendall((baris + '\n').encode())
        mesin.keadaan_tunggu('...> ', Jalan)
    Jalan = len(mesin.LOG_baris)
    mesin.직렬.sendall(b'.save\n' if stor_VALUE else b'.cancel\n')
    ukuran = mesin.keadaan_tunggu('jkoros> ', Jalan)
    assert ('Saved:' if stor_VALUE else 'Cancelled; original preserved') in ukuran, ukuran


def fail_e_mel():
    ukuran = subprocess.check_output(['nm', '-n', str(Kedudukan / 'build/kernel.elf')], universal_newlines=True)
    for baris in ukuran.splitlines():
        if baris.endswith(' ram_files'):
            return int(baris.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def tetamu_fail(mesin, 슬롯, Saiz, LALUAN):
    # ujian VM의 메모리에서 sebenar_data 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    e_mel = fail_e_mel() + 슬롯 * 16384
    mesin.pantau_VALUE.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(e_mel, Saiz, LALUAN)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if LALUAN.exists() and LALUAN.stat().st_size == Saiz:
            return LALUAN.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def jalanan_ujian(종류):
    mesin = mesin_maya(Kedudukan / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, rangkaian_VALUE=False)
    ukuran = {}
    try:
        mesin.Perintah('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        mesin.Perintah('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        mesin.Perintah('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        mesin.Perintah('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        mesin.Perintah('java Missing', ['cannot read class: -2', 'Exit: 1'])
        mesin.Perintah('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        mesin.Perintah('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        Kandungan_VALUE = '''public class Calc {
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
        edit_VALUE(mesin, 'Calc.java', Kandungan_VALUE)
        mesin.Perintah('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        출력 = mesin.Perintah('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ukuran['guest_output'] = 출력
        pemasukan_Senarai = mesin.Perintah('ls', ['Calc.class'])
        Saiz = int(re.search(r'Calc\.class\s+(\d+) bytes', pemasukan_Senarai).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as direktori_VALUE:
            LALUAN = Path(direktori_VALUE) / 'Calc.class'
            data = tetamu_fail(mesin, 3, Saiz, LALUAN)
            sebenar_data = subprocess.check_output(['java', '-Xverify:all', '-cp', direktori_VALUE, 'Calc', '6', 'guest'], universal_newlines=True)
            assert sebenar_data.splitlines() == 기대, sebenar_data
            ukuran['class_sha256'] = hashlib.sha256(data).hexdigest()
            ukuran['openjdk_output'] = sebenar_data
        # 실패한 edit_VALUE/컴파일은 기존 class를 보존한다.
        edit_VALUE(mesin, 'Calc.java', 'not Java at all', stor_VALUE=False)
        mesin.Perintah('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for tak_sah_ukuran in [
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
            edit_VALUE(mesin, 'Calc.java', tak_sah_ukuran)
            mesin.Perintah('javac Calc.java', ['javac error:', 'Exit: 1'])
            mesin.Perintah('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # lelaran_VALUE 실행은 ruang_pengguna timbunan_VALUE/프레임을 매번 초기화한다.
        for 수 in range(12):
            mesin.Perintah('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        mesin.Perintah('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        mesin.Perintah('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        edit_VALUE(mesin, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        mesin.Perintah('javac Calc.java', ['Compiled:', 'Exit: 0'])
        mesin.Perintah('java Calc', ['instruction limit', 'Exit: 1'])
        mesin.Perintah('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        edit_VALUE(mesin, 'Bad.class', 'garbage')
        mesin.Perintah('java Bad', ['JVM error:', 'Exit: 1'])
        mesin.Perintah('rm Bad.class', ['Removed'])
        mesin.Perintah('java Bad', ['cannot read class: -2'])
        # edit_VALUE 입력의 넘친 부분을 잘라서 저장하지 않는다.
        Jalan = len(mesin.LOG_baris)
        mesin.직렬.sendall(b'edit Hello.java\n')
        mesin.keadaan_tunggu('...> ', Jalan)
        Jalan = len(mesin.LOG_baris)
        mesin.직렬.sendall(b'x' * 129 + b'\n')
        mesin.keadaan_tunggu('...> ', Jalan)
        mesin.Perintah('.save', ['Too much input; original preserved'])
        mesin.Perintah('javac Hello.java', ['Compiled:', 'Exit: 0'])
        edit_VALUE(mesin, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            edit_VALUE(mesin, 'f' + str(수), 'occupied')
        mesin.Perintah('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        mesin.Perintah('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in mesin.LOG_baris.decode('utf-8', 'replace')
        ukuran['serial'] = mesin.LOG_baris.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ukuran
    finally:
        mesin.Tutup()


def 주코드(data):
    """손상 시험용 main Code의 sebenar_data Fail 오프셋/길이만 읽는다."""
    jawatan_VALUE = 8
    def 짧():
        nonlocal jawatan_VALUE
        VALUE = struct.unpack_from('>H', data, jawatan_VALUE)[0]
        jawatan_VALUE += 2
        return VALUE
    def 정():
        nonlocal jawatan_VALUE
        VALUE = struct.unpack_from('>I', data, jawatan_VALUE)[0]
        jawatan_VALUE += 4
        return VALUE
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = data[jawatan_VALUE]
        jawatan_VALUE += 1
        if 종류 == 1:
            kepanjangan_VALUE = 짧()
            문자들[수] = data[jawatan_VALUE:jawatan_VALUE + kepanjangan_VALUE]
            jawatan_VALUE += kepanjangan_VALUE
        elif 종류 in (7, 8): jawatan_VALUE += 2
        elif 종류 in (3, 9, 10, 12): jawatan_VALUE += 4
        else: raise AssertionError(종류)
    jawatan_VALUE += 6
    item_COUNT = 짧()
    jawatan_VALUE += item_COUNT * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        Nama = 짧()
        짧()
        for 수 in range(짧()):
            atribut_VALUE = 짧()
            Saiz = 정()
            if 문자들[Nama] == b'main' and 문자들[atribut_VALUE] == b'Code':
                return jawatan_VALUE + 8, struct.unpack_from('>I', data, jawatan_VALUE + 4)[0]
            jawatan_VALUE += Saiz
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        direktori_VALUE = Path(임시)
        (direktori_VALUE / 'build').mkdir()
        SUMBER = direktori_VALUE / 'Imported.java'
        SUMBER.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(SUMBER)], check=True)
        원본 = (direktori_VALUE / 'Imported.class').read_bytes()
        kod_VALUE, kepanjangan_VALUE = 주코드(원본)
        변형 = {}
        data = bytearray(원본); data[0] = 0; 변형['BadMagic'] = data
        data = bytearray(원본); data[7] = 61; 변형['BadVer'] = data
        data = bytearray(원본); data[8:10] = b'\xff\xff'; 변형['BadPool'] = data
        data = bytearray(원본); data[kod_VALUE:kod_VALUE + kepanjangan_VALUE] = bytes(kepanjangan_VALUE)
        data[kod_VALUE:kod_VALUE + 3] = b'\xa7\x00\x01'; data[kod_VALUE + kepanjangan_VALUE - 1] = 177; 변형['BadJump'] = data
        data = bytearray(원본); data[kod_VALUE:kod_VALUE + kepanjangan_VALUE] = bytes(kepanjangan_VALUE)
        data[kod_VALUE] = 87; data[kod_VALUE + kepanjangan_VALUE - 1] = 177; 변형['BadStack'] = data
        # Nama 검사를 통과시켜 sebenar_data laksanakan_perintah 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        pemasukan_VALUE = ['Imported.class=' + str(direktori_VALUE / 'Imported.class'), 'Imported.java=' + str(SUMBER)]
        for Nama, data in 변형.items():
            LALUAN = direktori_VALUE / (Nama + '.class'); LALUAN.write_bytes(data)
            pemasukan_VALUE.append(Nama + '.class=' + str(LALUAN))
        Kumpulan_VALUE = direktori_VALUE / 'build/java-files.bin'
        subprocess.run([sys.executable, str(Kedudukan / 'alat/자바파일묶기.py'), '-o', str(Kumpulan_VALUE)] + pemasukan_VALUE, check=True)
        subprocess.run(['as', '--32', '-o', str(direktori_VALUE / 'user.o'), str(Kedudukan / 'permulaan_mesin/ruang_pengguna.s')], cwd=str(direktori_VALUE), check=True)
        kernel_VALUE = direktori_VALUE / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Kedudukan / 'permulaan_mesin/susun_atur_pautan.ld'), '-o', str(kernel_VALUE),
                        str(Kedudukan / 'build/boot.o'), str(Kedudukan / 'build/java.o'), str(direktori_VALUE / 'user.o'), str(Kedudukan / 'build/apps.o')], check=True)
        mesin = mesin_maya(kernel_VALUE, rangkaian_VALUE=False)
        try:
            mesin.Perintah('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            mesin.Perintah('cat Imported.java', ['int[] values = new int[3]'])
            for Nama, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                mesin.Perintah('java ' + Nama, [문구, 'Exit: 1'])
                mesin.Perintah('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return mesin.LOG_baris.decode('utf-8', 'replace')
        finally:
            mesin.Tutup()


if __name__ == '__main__':
    hurai_VALUE = argparse.ArgumentParser()
    hurai_VALUE.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = hurai_VALUE.parse_args()
    ukuran = {종류: jalanan_ujian(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    ukuran['import'] = 적재시험()
    (Kedudukan / 'build/자바시험.json').write_text(json.dumps(ukuran, ensure_ascii=False, indent=2) + '\n')
