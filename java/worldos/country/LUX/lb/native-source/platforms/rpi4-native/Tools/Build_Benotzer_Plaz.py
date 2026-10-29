"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from Build_PYTHON import Create_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Create_Benotzer_Plaz(Racinn_Wee, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Archiv_Tool, 설정비트, ausféieren_Befeel):
    설정비트 = [Astellungen_VALUE for Astellungen_VALUE in 설정비트 if Astellungen_VALUE != '-mgeneral-regs-only']
    Build_Wee = Racinn_Wee / 'build'
    출력결과 = Build_Wee / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = Racinn_Wee / 'Benotzer'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Wee, Numm in [
            (시언어번역기, [], 원본자료 / 'Laf.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ausféieren_Befeel.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'Benotzer_Bréck.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Editeur.c', 'vi.o')]:
        ausféieren_Befeel([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Wee, '-o', 출력결과 / Numm])
    ausféieren_Befeel([Archiv_Tool, 'rcs', Build_Wee / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Numm in ('demo', 'fault', 'network', 'vi'):
        ausféieren_Befeel([연결편집기, '-T', 원본자료 / 'Link_Layout.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Numm + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Numm + '.o'), Build_Wee / 'libposix-kor-user.a'])
    자바라이브러리만들기(Racinn_Wee, ausféieren_Befeel)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(Build_Wee)) as 작업경로:
        Klass_Wee = Path(작업경로)
        ausféieren_Befeel(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Klass_Wee, '-sourcepath', Klass_Wee, '-d', Klass_Wee] +
            [Daten_positionéieren for Daten_positionéieren in sorted((저장소경로 / 'os/Benotzer/자바').glob('*.java')) if Daten_positionéieren.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ausféieren_Befeel(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'Tool_Agab.Laf',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Klass_Wee.glob('*.class')))
    압축해제경로 = Racinn_Wee / 'vendor/uzlib'
    for Wee, Numm in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'Bëndel.c', 'jar.o')] + [(압축해제경로 / (Numm + '.c'), Numm + '.o') for Numm in ('tinflate', 'crc32', 'adler32')]:
        ausféieren_Befeel([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Wee, '-o', 출력결과 / Numm])
    ausféieren_Befeel([연결편집기, '-T', 원본자료 / 'Link_Layout.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Numm for Numm in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Create_PYTHON(Racinn_Wee, 시언어번역기, 연결편집기)
    시언어번역기만들기(Racinn_Wee, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ausféieren_Befeel)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    App_En_tête_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    En_tête_Lëscht = [App_En_tête_OFFSET + Element_COUNT * 56 for Element_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [Daten_positionéieren for Daten_positionéieren in En_tête_Lëscht if struct.unpack_from('<I', 유효함, Daten_positionéieren)[0] == 1]
    SMS, Daten = 적재구획[:2]
    Befeel_Adress = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    Daten_Adress = struct.unpack_from('<Q', 유효함, Daten + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', Befeel_Adress + 1), ('data-entry', 24, 'Q', Daten_Adress),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', Befeel_Adress + 8),
               ('overlap', Daten + 16, 'Q', Befeel_Adress)]
    for Numm, OFFSET_VALUE, Format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + Format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Numm, bytes(바뀐자료)))
    탑재덩이들 = [(Numm.replace('-', '_'), 출력결과 / (Numm + '.elf')) for Numm in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Numm, nëtzlech_Charge_Daten) in enumerate(시험사례):
        Wee = 출력결과 / ('invalid-{}.elf'.format(Numm)); Wee.write_bytes(nëtzlech_Charge_Daten)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), Wee))
    어셈블리자료, En_tête_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Numm, Wee in 탑재덩이들:
        Symbol_VALUE = 'user_blob_' + Numm
        크기목록[Numm] = Wee.stat().st_size
        # 생성한 Peer_VALUE 경로만 넣어 프로젝트 경로의 공백/Zitat 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + Symbol_VALUE, Symbol_VALUE + ':', '.incbin "{}"'.format(Wee.relative_to(Racinn_Wee))]
        En_tête_VALUE.append('extern const unsigned char {}[];'.format(Symbol_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    En_tête_VALUE += ['static const App 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    En_tête_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    En_tête_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    En_tête_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], Method_MODE) for Method_MODE in (0, 1)]
    En_tête_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    En_tête_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    En_tête_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    En_tête_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    En_tête_VALUE += ['};', 'static const App 잘못된실행항목들[] = {']
    En_tête_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(nëtzlech_Charge_Daten)) for 순번, (_, nëtzlech_Charge_Daten) in enumerate(시험사례)]
    En_tête_VALUE += ['};']
    (Build_Wee / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (Build_Wee / 'programs.h').write_text('\n'.join(En_tête_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Numm for Numm, _ in 시험사례) + '\n')
    ausféieren_Befeel([시언어번역기] + 설정비트 + ['-c', Build_Wee / 'programs.S', '-o', Build_Wee / 'programs.o'])
