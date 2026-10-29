#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 ดําเนินการ_คําสั่ง, ความล้มเหลว_ค่า/ทรัพยากร_ค่า 경계 시험."""
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
from การทดสอบ_ผู้ใช้_เครือข่าย import เครื่องเสมือน, ตําแหน่ง


def แก้ไข_ค่า(เครื่อง, ชื่อ, เนื้อหา_ค่า, เก็บ_ค่า=True):
    เรียกใช้งาน = len(เครื่อง.บันทึก_สถิติ)
    เครื่อง.직렬.sendall(('edit ' + ชื่อ + '\n').encode())
    เครื่อง.ภาวะรอ('...> ', เรียกใช้งาน)
    for บรรทัด in เนื้อหา_ค่า.splitlines():
        assert len(บรรทัด) <= 128
        เรียกใช้งาน = len(เครื่อง.บันทึก_สถิติ)
        เครื่อง.직렬.sendall((บรรทัด + '\n').encode())
        เครื่อง.ภาวะรอ('...> ', เรียกใช้งาน)
    เรียกใช้งาน = len(เครื่อง.บันทึก_สถิติ)
    เครื่อง.직렬.sendall(b'.save\n' if เก็บ_ค่า else b'.cancel\n')
    ผลลัพธ์ = เครื่อง.ภาวะรอ('jkoros> ', เรียกใช้งาน)
    assert ('Saved:' if เก็บ_ค่า else 'Cancelled; original preserved') in ผลลัพธ์, ผลลัพธ์


def แฟ้ม_อีเมล():
    ผลลัพธ์ = subprocess.check_output(['nm', '-n', str(ตําแหน่ง / 'build/kernel.elf')], universal_newlines=True)
    for บรรทัด in ผลลัพธ์.splitlines():
        if บรรทัด.endswith(' ram_files'):
            return int(บรรทัด.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def ผู้เยี่ยมชม_แฟ้ม(เครื่อง, 슬롯, ขนาด, เส้นทาง):
    # 시험 VM의 메모리에서 ค่าจริง_ข้อมูล 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    อีเมล = แฟ้ม_อีเมล() + 슬롯 * 16384
    เครื่อง.จอภาพ_ค่า.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(อีเมล, ขนาด, เส้นทาง)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if เส้นทาง.exists() and เส้นทาง.stat().st_size == ขนาด:
            return เส้นทาง.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def การทดสอบการใช้งาน(종류):
    เครื่อง = เครื่องเสมือน(ตําแหน่ง / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, เครือข่าย_ค่า=False)
    ผลลัพธ์ = {}
    try:
        เครื่อง.คําสั่ง('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        เครื่อง.คําสั่ง('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        เครื่อง.คําสั่ง('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        เครื่อง.คําสั่ง('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        เครื่อง.คําสั่ง('java Missing', ['cannot read class: -2', 'Exit: 1'])
        เครื่อง.คําสั่ง('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        เครื่อง.คําสั่ง('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        เนื้อหา_ค่า = '''public class Calc {
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
        แก้ไข_ค่า(เครื่อง, 'Calc.java', เนื้อหา_ค่า)
        เครื่อง.คําสั่ง('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        ข้อความออก = เครื่อง.คําสั่ง('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ผลลัพธ์['guest_output'] = ข้อความออก
        รายการ_รายการ = เครื่อง.คําสั่ง('ls', ['Calc.class'])
        ขนาด = int(re.search(r'Calc\.class\s+(\d+) bytes', รายการ_รายการ).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as ไดเรกทอรี_ค่า:
            เส้นทาง = Path(ไดเรกทอรี_ค่า) / 'Calc.class'
            ข้อมูล = ผู้เยี่ยมชม_แฟ้ม(เครื่อง, 3, ขนาด, เส้นทาง)
            ค่าจริง_ข้อมูล = subprocess.check_output(['java', '-Xverify:all', '-cp', ไดเรกทอรี_ค่า, 'Calc', '6', 'guest'], universal_newlines=True)
            assert ค่าจริง_ข้อมูล.splitlines() == 기대, ค่าจริง_ข้อมูล
            ผลลัพธ์['class_sha256'] = hashlib.sha256(ข้อมูล).hexdigest()
            ผลลัพธ์['openjdk_output'] = ค่าจริง_ข้อมูล
        # 실패한 แก้ไข_ค่า/컴파일은 기존 class를 보존한다.
        แก้ไข_ค่า(เครื่อง, 'Calc.java', 'not Java at all', เก็บ_ค่า=False)
        เครื่อง.คําสั่ง('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for ไม่ถูกต้อง_เมตริก in [
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
            แก้ไข_ค่า(เครื่อง, 'Calc.java', ไม่ถูกต้อง_เมตริก)
            เครื่อง.คําสั่ง('javac Calc.java', ['javac error:', 'Exit: 1'])
            เครื่อง.คําสั่ง('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # สปรินต์_ค่า 실행은 ผู้ใช้ ฮีป_ค่า/프레임을 매번 초기화한다.
        for หมายเลข in range(12):
            เครื่อง.คําสั่ง('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        เครื่อง.คําสั่ง('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        เครื่อง.คําสั่ง('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        แก้ไข_ค่า(เครื่อง, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        เครื่อง.คําสั่ง('javac Calc.java', ['Compiled:', 'Exit: 0'])
        เครื่อง.คําสั่ง('java Calc', ['instruction limit', 'Exit: 1'])
        เครื่อง.คําสั่ง('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        แก้ไข_ค่า(เครื่อง, 'Bad.class', 'garbage')
        เครื่อง.คําสั่ง('java Bad', ['JVM error:', 'Exit: 1'])
        เครื่อง.คําสั่ง('rm Bad.class', ['Removed'])
        เครื่อง.คําสั่ง('java Bad', ['cannot read class: -2'])
        # แก้ไข_ค่า 입력의 넘친 부분을 잘라서 저장하지 않는다.
        เรียกใช้งาน = len(เครื่อง.บันทึก_สถิติ)
        เครื่อง.직렬.sendall(b'edit Hello.java\n')
        เครื่อง.ภาวะรอ('...> ', เรียกใช้งาน)
        เรียกใช้งาน = len(เครื่อง.บันทึก_สถิติ)
        เครื่อง.직렬.sendall(b'x' * 129 + b'\n')
        เครื่อง.ภาวะรอ('...> ', เรียกใช้งาน)
        เครื่อง.คําสั่ง('.save', ['Too much input; original preserved'])
        เครื่อง.คําสั่ง('javac Hello.java', ['Compiled:', 'Exit: 0'])
        แก้ไข_ค่า(เครื่อง, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for หมายเลข in range(3):
            แก้ไข_ค่า(เครื่อง, 'f' + str(หมายเลข), 'occupied')
        เครื่อง.คําสั่ง('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        เครื่อง.คําสั่ง('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
        ผลลัพธ์['serial'] = เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ผลลัพธ์
    finally:
        เครื่อง.ปิด()


def 주코드(ข้อมูล):
    """손상 시험용 main Code의 ค่าจริง_ข้อมูล แฟ้ม 오프셋/길이만 읽는다."""
    ตําแหน่ง_ค่า = 8
    def 짧():
        nonlocal ตําแหน่ง_ค่า
        ค่า = struct.unpack_from('>H', ข้อมูล, ตําแหน่ง_ค่า)[0]
        ตําแหน่ง_ค่า += 2
        return ค่า
    def 정():
        nonlocal ตําแหน่ง_ค่า
        ค่า = struct.unpack_from('>I', ข้อมูล, ตําแหน่ง_ค่า)[0]
        ตําแหน่ง_ค่า += 4
        return ค่า
    문자들 = {}
    for หมายเลข in range(1, 짧()):
        종류 = ข้อมูล[ตําแหน่ง_ค่า]
        ตําแหน่ง_ค่า += 1
        if 종류 == 1:
            길이 = 짧()
            문자들[หมายเลข] = ข้อมูล[ตําแหน่ง_ค่า:ตําแหน่ง_ค่า + 길이]
            ตําแหน่ง_ค่า += 길이
        elif 종류 in (7, 8): ตําแหน่ง_ค่า += 2
        elif 종류 in (3, 9, 10, 12): ตําแหน่ง_ค่า += 4
        else: raise AssertionError(종류)
    ตําแหน่ง_ค่า += 6
    개수 = 짧()
    ตําแหน่ง_ค่า += 개수 * 2
    assert 짧() == 0
    for หมายเลข in range(짧()):
        짧()
        ชื่อ = 짧()
        짧()
        for หมายเลข in range(짧()):
            แอตทริบิวต์_ค่า = 짧()
            ขนาด = 정()
            if 문자들[ชื่อ] == b'main' and 문자들[แอตทริบิวต์_ค่า] == b'Code':
                return ตําแหน่ง_ค่า + 8, struct.unpack_from('>I', ข้อมูล, ตําแหน่ง_ค่า + 4)[0]
            ตําแหน่ง_ค่า += ขนาด
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        ไดเรกทอรี_ค่า = Path(임시)
        (ไดเรกทอรี_ค่า / 'build').mkdir()
        รหัสต้นฉบับ = ไดเรกทอรี_ค่า / 'Imported.java'
        รหัสต้นฉบับ.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(รหัสต้นฉบับ)], check=True)
        원본 = (ไดเรกทอรี_ค่า / 'Imported.class').read_bytes()
        รหัส_ค่า, 길이 = 주코드(원본)
        ตัวแปร_ค่า = {}
        ข้อมูล = bytearray(원본); ข้อมูล[0] = 0; ตัวแปร_ค่า['BadMagic'] = ข้อมูล
        ข้อมูล = bytearray(원본); ข้อมูล[7] = 61; ตัวแปร_ค่า['BadVer'] = ข้อมูล
        ข้อมูล = bytearray(원본); ข้อมูล[8:10] = b'\xff\xff'; ตัวแปร_ค่า['BadPool'] = ข้อมูล
        ข้อมูล = bytearray(원본); ข้อมูล[รหัส_ค่า:รหัส_ค่า + 길이] = bytes(길이)
        ข้อมูล[รหัส_ค่า:รหัส_ค่า + 3] = b'\xa7\x00\x01'; ข้อมูล[รหัส_ค่า + 길이 - 1] = 177; ตัวแปร_ค่า['BadJump'] = ข้อมูล
        ข้อมูล = bytearray(원본); ข้อมูล[รหัส_ค่า:รหัส_ค่า + 길이] = bytes(길이)
        ข้อมูล[รหัส_ค่า] = 87; ข้อมูล[รหัส_ค่า + 길이 - 1] = 177; ตัวแปร_ค่า['BadStack'] = ข้อมูล
        # ชื่อ 검사를 통과시켜 ค่าจริง_ข้อมูล ดําเนินการ_คําสั่ง 중의 ตัวถูกดําเนินการ_สแตก 오류까지 검사한다.
        ตัวแปร_ค่า['BadStack'] = ตัวแปร_ค่า['BadStack'].replace(b'Imported', b'BadStack')
        รายการ_ค่า = ['Imported.class=' + str(ไดเรกทอรี_ค่า / 'Imported.class'), 'Imported.java=' + str(รหัสต้นฉบับ)]
        for ชื่อ, ข้อมูล in ตัวแปร_ค่า.items():
            เส้นทาง = ไดเรกทอรี_ค่า / (ชื่อ + '.class'); เส้นทาง.write_bytes(ข้อมูล)
            รายการ_ค่า.append(ชื่อ + '.class=' + str(เส้นทาง))
        กลุ่ม_ค่า = ไดเรกทอรี_ค่า / 'build/java-files.bin'
        subprocess.run([sys.executable, str(ตําแหน่ง / 'เครื่องมือ/자바파일묶기.py'), '-o', str(กลุ่ม_ค่า)] + รายการ_ค่า, check=True)
        subprocess.run(['as', '--32', '-o', str(ไดเรกทอรี_ค่า / 'user.o'), str(ตําแหน่ง / '부팅/ผู้ใช้.s')], cwd=str(ไดเรกทอรี_ค่า), check=True)
        เคอร์เนล_ค่า = ไดเรกทอรี_ค่า / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ตําแหน่ง / '부팅/ลิงก์_การนําทาง.ld'), '-o', str(เคอร์เนล_ค่า),
                        str(ตําแหน่ง / 'build/boot.o'), str(ตําแหน่ง / 'build/java.o'), str(ไดเรกทอรี_ค่า / 'user.o'), str(ตําแหน่ง / 'build/apps.o')], check=True)
        เครื่อง = เครื่องเสมือน(เคอร์เนล_ค่า, เครือข่าย_ค่า=False)
        try:
            เครื่อง.คําสั่ง('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            เครื่อง.คําสั่ง('cat Imported.java', ['int[] values = new int[3]'])
            for ชื่อ, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                เครื่อง.คําสั่ง('java ' + ชื่อ, [문구, 'Exit: 1'])
                เครื่อง.คําสั่ง('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
        finally:
            เครื่อง.ปิด()


if __name__ == '__main__':
    แยกวิเคราะห์_ค่า = argparse.ArgumentParser()
    แยกวิเคราะห์_ค่า.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    อาร์กิวเมนต์ = แยกวิเคราะห์_ค่า.parse_args()
    ผลลัพธ์ = {종류: การทดสอบการใช้งาน(종류) for 종류 in (('elf', 'iso') if อาร์กิวเมนต์.boot == 'both' else (อาร์กิวเมนต์.boot,))}
    ผลลัพธ์['import'] = 적재시험()
    (ตําแหน่ง / 'build/자바시험.json').write_text(json.dumps(ผลลัพธ์, ensure_ascii=False, indent=2) + '\n')
