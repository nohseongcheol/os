#!/usr/bin/env python3
"""ELF/ISO 게스트 javac->class->java, OpenJDK 교차 అమలు_చేయి_ఆదేశం, వైఫల్యం_మూల్యం/వనరు_మూల్యం 경계 시험."""
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
from 사용자통신시험 import వర్చువల్_యంత్రం, స్థానము


def సంకలనంచేయు_మూల్యం(యంత్రం, పేరు, విషయం_మూల్యం, నిల్వ_మూల్యం=True):
    నడుపుము = len(యంత్రం.లాగ్_వరుస)
    యంత్రం.직렬.sendall(('edit ' + పేరు + '\n').encode())
    యంత్రం.వేచియుండు_స్థితి('...> ', నడుపుము)
    for పంక్తి in విషయం_మూల్యం.splitlines():
        assert len(పంక్తి) <= 128
        నడుపుము = len(యంత్రం.లాగ్_వరుస)
        యంత్రం.직렬.sendall((పంక్తి + '\n').encode())
        యంత్రం.వేచియుండు_స్థితి('...> ', నడుపుము)
    నడుపుము = len(యంత్రం.లాగ్_వరుస)
    యంత్రం.직렬.sendall(b'.save\n' if నిల్వ_మూల్యం else b'.cancel\n')
    ప్రమాణం = యంత్రం.వేచియుండు_స్థితి('jkoros> ', నడుపుము)
    assert ('Saved:' if నిల్వ_మూల్యం else 'Cancelled; original preserved') in ప్రమాణం, ప్రమాణం


def ఫైలు_ఇమెయిల్():
    ప్రమాణం = subprocess.check_output(['nm', '-n', str(స్థానము / 'build/kernel.elf')], universal_newlines=True)
    for పంక్తి in ప్రమాణం.splitlines():
        if పంక్తి.endswith(' ram_files'):
            return int(పంక్తి.split()[0], 16)
    raise AssertionError('ram_files symbol missing')


def అతిథి_ఫైలు(యంత్రం, స్లాట్_మూల్యం, పరిమాణం, పాత్):
    # 시험 VM의 메모리에서 వాస్తవ_డేటా 생성한 파일을 읽어 독립 OpenJDK로 검증한다.
    ఇమెయిల్ = ఫైలు_ఇమెయిల్() + స్లాట్_మూల్యం * 16384
    యంత్రం.మానిటర్_మూల్యం.sendall(('pmemsave 0x{:x} {} "{}"\n'.format(ఇమెయిల్, పరిమాణం, పాత్)).encode())
    끝 = time.monotonic() + 5
    while time.monotonic() < 끝:
        if పాత్.exists() and పాత్.stat().st_size == పరిమాణం:
            return పాత్.read_bytes()
        time.sleep(0.03)
    raise AssertionError('guest file export failed')


def 실행시험(종류):
    యంత్రం = వర్చువల్_యంత్రం(స్థానము / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류, నెట్_వర్క్_మూల్యం=False)
    ప్రమాణం = {}
    try:
        యంత్రం.ఆదేశము('javac -version', ['subset compiler; not OpenJDK', 'Exit: 0'])
        యంత్రం.ఆదేశము('java -version', ['class 45..52 subset; not OpenJDK', 'Exit: 0'])
        యంత్రం.ఆదేశము('javac Hello.java', ['Compiled: Hello.class', 'Exit: 0'])
        యంత్రం.ఆదేశము('java Hello', ['Hello from jkoros JVM!', '\r\n55\r\n', 'Exit: 0'])
        యంత్రం.ఆదేశము('java Missing', ['cannot read class: -2', 'Exit: 1'])
        యంత్రం.ఆదేశము('javac Missing.java', ['cannot read source: -2', 'Exit: 1'])
        యంత్రం.ఆదేశము('javac Hello.class', ['expected FILE.java', 'Exit: 2'])
        విషయం_మూల్యం = '''public class Calc {
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
        సంకలనంచేయు_మూల్యం(యంత్రం, 'Calc.java', విషయం_మూల్యం)
        యంత్రం.ఆదేశము('javac Calc.java', ['Compiled: Calc.class', 'Exit: 0'])
        기대 = ['720', '21', '0', 'true', 'false', 'true', '-2147483648', 'guest', '5', '2',
                'sum=21', '12xfalse', 'logic=true', 'b', 'letter=b', '20']
        అవుట్పుట్ = యంత్రం.ఆదేశము('java Calc 6 guest', ['\r\n' + '\r\n'.join(기대) + '\r\n', 'Exit: 0'])
        ప్రమాణం['guest_output'] = అవుట్పుట్
        ప్రవేశం_జాబితా = యంత్రం.ఆదేశము('ls', ['Calc.class'])
        పరిమాణం = int(re.search(r'Calc\.class\s+(\d+) bytes', ప్రవేశం_జాబితా).group(1))
        with tempfile.TemporaryDirectory(prefix='jkoros-java-cross-') as సంచయని_మూల్యం:
            పాత్ = Path(సంచయని_మూల్యం) / 'Calc.class'
            డేటా = అతిథి_ఫైలు(యంత్రం, 3, పరిమాణం, పాత్)
            వాస్తవ_డేటా = subprocess.check_output(['java', '-Xverify:all', '-cp', సంచయని_మూల్యం, 'Calc', '6', 'guest'], universal_newlines=True)
            assert వాస్తవ_డేటా.splitlines() == 기대, వాస్తవ_డేటా
            ప్రమాణం['class_sha256'] = hashlib.sha256(డేటా).hexdigest()
            ప్రమాణం['openjdk_output'] = వాస్తవ_డేటా
        # 실패한 సంకలనంచేయు_మూల్యం/컴파일은 기존 class를 보존한다.
        సంకలనంచేయు_మూల్యం(యంత్రం, 'Calc.java', 'not Java at all', నిల్వ_మూల్యం=False)
        యంత్రం.ఆదేశము('javac Calc.java', ['Compiled:', 'Exit: 0'])
        for చెల్లని_ప్రమాణం in [
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
            సంకలనంచేయు_మూల్యం(యంత్రం, 'Calc.java', చెల్లని_ప్రమాణం)
            యంత్రం.ఆదేశము('javac Calc.java', ['javac error:', 'Exit: 1'])
            యంత్రం.ఆదేశము('java Calc 6 guest', ['\r\n720\r\n', 'Exit: 0'])
        # పునరావృతం_మూల్యం 실행은 వినియోగదారు 힙/프레임을 매번 초기화한다.
        for 수 in range(12):
            యంత్రం.ఆదేశము('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        యంత్రం.ఆదేశము('java Calc nope guest', ['NumberFormatException', 'Exit: 1'])
        యంత్రం.ఆదేశము('java Calc 6', ['ArrayIndexOutOfBoundsException', 'Exit: 1'])
        సంకలనంచేయు_మూల్యం(యంత్రం, 'Calc.java', '''public class Calc {
 public static void main(String[] args) { while (true) { } }
}''')
        యంత్రం.ఆదేశము('javac Calc.java', ['Compiled:', 'Exit: 0'])
        యంత్రం.ఆదేశము('java Calc', ['instruction limit', 'Exit: 1'])
        యంత్రం.ఆదేశము('run hello after-java', ['USER MODE ring 3', 'after-java', 'Exit: 0'])
        సంకలనంచేయు_మూల్యం(యంత్రం, 'Bad.class', 'garbage')
        యంత్రం.ఆదేశము('java Bad', ['JVM error:', 'Exit: 1'])
        యంత్రం.ఆదేశము('rm Bad.class', ['Removed'])
        యంత్రం.ఆదేశము('java Bad', ['cannot read class: -2'])
        # సంకలనంచేయు_మూల్యం 입력의 넘친 부분을 잘라서 저장하지 않는다.
        నడుపుము = len(యంత్రం.లాగ్_వరుస)
        యంత్రం.직렬.sendall(b'edit Hello.java\n')
        యంత్రం.వేచియుండు_స్థితి('...> ', నడుపుము)
        నడుపుము = len(యంత్రం.లాగ్_వరుస)
        యంత్రం.직렬.sendall(b'x' * 129 + b'\n')
        యంత్రం.వేచియుండు_స్థితి('...> ', నడుపుము)
        యంత్రం.ఆదేశము('.save', ['Too much input; original preserved'])
        యంత్రం.ఆదేశము('javac Hello.java', ['Compiled:', 'Exit: 0'])
        సంకలనంచేయు_మూల్యం(యంత్రం, 'Full.java', 'public class Full { public static void main(String[] args) {} }')
        for 수 in range(3):
            సంకలనంచేయు_మూల్యం(యంత్రం, 'f' + str(수), 'occupied')
        యంత్రం.ఆదేశము('javac Full.java', ['cannot save class: -28', 'Exit: 1'])
        యంత్రం.ఆదేశము('java Hello', ['\r\n55\r\n', 'Exit: 0'])
        assert 'PANIC' not in యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
        ప్రమాణం['serial'] = యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
        print('PASS: {} guest compile/run, OpenJDK class verification, errors, repeat, limits'.format(종류))
        return ప్రమాణం
    finally:
        యంత్రం.మూసివేయి()


def 주코드(డేటా):
    """손상 시험용 main Code의 వాస్తవ_డేటా దస్త్రం 오프셋/길이만 읽는다."""
    స్థాయి_మూల్యం = 8
    def 짧():
        nonlocal స్థాయి_మూల్యం
        మూల్యం = struct.unpack_from('>H', డేటా, స్థాయి_మూల్యం)[0]
        స్థాయి_మూల్యం += 2
        return మూల్యం
    def 정():
        nonlocal స్థాయి_మూల్యం
        మూల్యం = struct.unpack_from('>I', డేటా, స్థాయి_మూల్యం)[0]
        స్థాయి_మూల్యం += 4
        return మూల్యం
    문자들 = {}
    for 수 in range(1, 짧()):
        종류 = డేటా[స్థాయి_మూల్యం]
        స్థాయి_మూల్యం += 1
        if 종류 == 1:
            పొడవు_మూల్యం = 짧()
            문자들[수] = డేటా[స్థాయి_మూల్యం:స్థాయి_మూల్యం + పొడవు_మూల్యం]
            స్థాయి_మూల్యం += పొడవు_మూల్యం
        elif 종류 in (7, 8): స్థాయి_మూల్యం += 2
        elif 종류 in (3, 9, 10, 12): స్థాయి_మూల్యం += 4
        else: raise AssertionError(종류)
    స్థాయి_మూల్యం += 6
    개수 = 짧()
    స్థాయి_మూల్యం += 개수 * 2
    assert 짧() == 0
    for 수 in range(짧()):
        짧()
        పేరు = 짧()
        짧()
        for 수 in range(짧()):
            లక్షణం_మూల్యం = 짧()
            పరిమాణం = 정()
            if 문자들[పేరు] == b'main' and 문자들[లక్షణం_మూల్యం] == b'Code':
                return స్థాయి_మూల్యం + 8, struct.unpack_from('>I', డేటా, స్థాయి_మూల్యం + 4)[0]
            స్థాయి_మూల్యం += పరిమాణం
    raise AssertionError('main Code missing')


def 적재시험():
    with tempfile.TemporaryDirectory(prefix='jkoros-java-import-') as 임시:
        సంచయని_మూల్యం = Path(임시)
        (సంచయని_మూల్యం / 'build').mkdir()
        వనరు = సంచయని_మూల్యం / 'Imported.java'
        వనరు.write_text('''public class Imported {
 public static void main(String[] args) {
  int[] values = new int[3];
  values[0] = 9; values[1] = -4; values[2] = 7;
  System.out.println("from OpenJDK: " + (values[0] + values[1] + values[2]));
  System.out.println(args[0].charAt(1));
  System.out.println("한글");
 }
}''')
        subprocess.run(['javac', '--release', '8', '-encoding', 'UTF-8', str(వనరు)], check=True)
        원본 = (సంచయని_మూల్యం / 'Imported.class').read_bytes()
        కోడ్_మూల్యం, పొడవు_మూల్యం = 주코드(원본)
        변형 = {}
        డేటా = bytearray(원본); డేటా[0] = 0; 변형['BadMagic'] = డేటా
        డేటా = bytearray(원본); డేటా[7] = 61; 변형['BadVer'] = డేటా
        డేటా = bytearray(원본); డేటా[8:10] = b'\xff\xff'; 변형['BadPool'] = డేటా
        డేటా = bytearray(원본); డేటా[కోడ్_మూల్యం:కోడ్_మూల్యం + పొడవు_మూల్యం] = bytes(పొడవు_మూల్యం)
        డేటా[కోడ్_మూల్యం:కోడ్_మూల్యం + 3] = b'\xa7\x00\x01'; డేటా[కోడ్_మూల్యం + పొడవు_మూల్యం - 1] = 177; 변형['BadJump'] = డేటా
        డేటా = bytearray(원본); డేటా[కోడ్_మూల్యం:కోడ్_మూల్యం + పొడవు_మూల్యం] = bytes(పొడవు_మూల్యం)
        డేటా[కోడ్_మూల్యం] = 87; డేటా[కోడ్_మూల్యం + పొడవు_మూల్యం - 1] = 177; 변형['BadStack'] = డేటా
        # పేరు 검사를 통과시켜 వాస్తవ_డేటా అమలు_చేయి_ఆదేశం 중의 스택 오류까지 검사한다.
        변형['BadStack'] = 변형['BadStack'].replace(b'Imported', b'BadStack')
        ప్రవేశం_మూల్యం = ['Imported.class=' + str(సంచయని_మూల్యం / 'Imported.class'), 'Imported.java=' + str(వనరు)]
        for పేరు, డేటా in 변형.items():
            పాత్ = సంచయని_మూల్యం / (పేరు + '.class'); పాత్.write_bytes(డేటా)
            ప్రవేశం_మూల్యం.append(పేరు + '.class=' + str(పాత్))
        సమూహం_మూల్యం = సంచయని_మూల్యం / 'build/java-files.bin'
        subprocess.run([sys.executable, str(స్థానము / 'ఉపకరణాలు/자바파일묶기.py'), '-o', str(సమూహం_మూల్యం)] + ప్రవేశం_మూల్యం, check=True)
        subprocess.run(['as', '--32', '-o', str(సంచయని_మూల్యం / 'user.o'), str(స్థానము / '부팅/వినియోగదారు.s')], cwd=str(సంచయని_మూల్యం), check=True)
        కెర్నల్_మూల్యం = సంచయని_మూల్యం / 'kernel.elf'
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(స్థానము / '부팅/బంధం_లేవుట్.ld'), '-o', str(కెర్నల్_మూల్యం),
                        str(స్థానము / 'build/boot.o'), str(స్థానము / 'build/java.o'), str(సంచయని_మూల్యం / 'user.o'), str(స్థానము / 'build/apps.o')], check=True)
        యంత్రం = వర్చువల్_యంత్రం(కెర్నల్_మూల్యం, నెట్_వర్క్_మూల్యం=False)
        try:
            యంత్రం.ఆదేశము('java Imported guest', ['from OpenJDK: 12', '\r\nu\r\n', '한글', 'Exit: 0'])
            యంత్రం.ఆదేశము('cat Imported.java', ['int[] values = new int[3]'])
            for పేరు, 문구 in [('BadMagic', 'not a class file'), ('BadVer', 'supported class versions'),
                                 ('BadPool', 'constant pool limit'), ('BadJump', 'invalid branch target'), ('BadStack', 'operand stack underflow')]:
                యంత్రం.ఆదేశము('java ' + పేరు, [문구, 'Exit: 1'])
                యంత్రం.ఆదేశము('java Imported again', ['from OpenJDK: 12', 'Exit: 0'])
            print('PASS: OpenJDK -> guest class loading, int arrays, UTF-8, malformed classes')
            return యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
        finally:
            యంత్రం.మూసివేయి()


if __name__ == '__main__':
    పార్స్_మూల్యం = argparse.ArgumentParser()
    పార్స్_మూల్యం.add_argument('--boot', choices=('elf', 'iso', 'both'), default='both')
    인수 = పార్స్_మూల్యం.parse_args()
    ప్రమాణం = {종류: 실행시험(종류) for 종류 in (('elf', 'iso') if 인수.boot == 'both' else (인수.boot,))}
    ప్రమాణం['import'] = 적재시험()
    (స్థానము / 'build/자바시험.json').write_text(json.dumps(ప్రమాణం, ensure_ascii=False, indent=2) + '\n')
