"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def සාදන්න_පරිශීලක_ස්ථානය(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, සංරක්ෂිතය_මෙවලම, 설정비트, ක්_රියාත්මක_කරන්න_විධානය):
    설정비트 = [පසුතල_අගය for පසුතල_අගය in 설정비트 if පසුතල_අගය != '-mgeneral-regs-only']
    තැනුම_පෙත = 기준경로 / 'build'
    출력결과 = තැනුම_පෙත / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'පරිශීලක'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, මාර්_ගය, නම in [
            (시언어번역기, [], 원본자료 / 'ක්_රියාත්මක_කරන්න_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ක්_රියාත්මක_කරන්න_විධානය.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'පරිශීලක_පාලම.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'සකසනය.c', 'vi.o')]:
        ක්_රියාත්මක_කරන්න_විධානය([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', මාර්_ගය, '-o', 출력결과 / නම])
    ක්_රියාත්මක_කරන්න_විධානය([සංරක්ෂිතය_මෙවලම, 'rcs', තැනුම_පෙත / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for නම in ('demo', 'fault', 'network', 'vi'):
        ක්_රියාත්මක_කරන්න_විධානය([연결편집기, '-T', 원본자료 / 'සබැඳිය_සැකැස්ම.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (නම + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (නම + '.o'), තැනුම_පෙත / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, ක්_රියාත්මක_කරන්න_විධානය)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(තැනුම_පෙත)) as 작업경로:
        පන්තිය_පෙත = Path(작업경로)
        ක්_රියාත්මක_කරන්න_විධානය(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', පන්තිය_පෙත, '-sourcepath', පන්තිය_පෙත, '-d', පන්තිය_පෙත] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/පරිශීලක/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ක්_රියාත්මක_කරන්න_විධානය(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'මෙවලම_පිවිසුම.ක්_රියාත්මක_කරන්න_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(පන්තිය_පෙත.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for මාර්_ගය, නම in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'පොදිය.c', 'jar.o')] + [(압축해제경로 / (නම + '.c'), නම + '.o') for නම in ('tinflate', 'crc32', 'adler32')]:
        ක්_රියාත්මක_කරන්න_විධානය([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', මාර්_ගය, '-o', 출력결과 / නම])
    ක්_රියාත්මක_කරන්න_විධානය([연결편집기, '-T', 원본자료 / 'සබැඳිය_සැකැස්ම.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / නම for නම in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ක්_රියාත්මක_කරන්න_විධානය)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    යෙදු_ශීර්ෂය_ඕෆ්සෙට් = struct.unpack_from('<Q', 유효함, 32)[0]
    ශීර්ෂය_ලැයිස්තුව = [යෙදු_ශීර්ෂය_ඕෆ්සෙට් + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in ශීර්ෂය_ලැයිස්තුව if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    පෙළ, දත්ත = 적재구획[:2]
    විධානය_යොමුව = struct.unpack_from('<Q', 유효함, පෙළ + 16)[0]
    දත්ත_යොමුව = struct.unpack_from('<Q', 유효함, දත්ත + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', විධානය_යොමුව + 1), ('data-entry', 24, 'Q', දත්ත_යොමුව),
               ('outside-file', පෙළ + 32, 'Q', len(유효함) + 1), ('short-memory', පෙළ + 40, 'Q', 1),
               ('kernel-address', පෙළ + 16, 'Q', 0x80000), ('memory-overflow', පෙළ + 40, 'Q', 2**64 - 1),
               ('writable-code', පෙළ + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', පෙළ, 'I', 2),
               ('unaligned-load', පෙළ + 16, 'Q', විධානය_යොමුව + 8),
               ('overlap', දත්ත + 16, 'Q', විධානය_යොමුව)]
    for නම, ඕෆ්සෙට්_අගය, හැඩතලය_932e03c8, අගය in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + හැඩතලය_932e03c8, 바뀐자료, ඕෆ්සෙට්_අගය, අගය)
        시험사례.append((නම, bytes(바뀐자료)))
    탑재덩이들 = [(නම.replace('-', '_'), 출력결과 / (නම + '.elf')) for නම in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (නම, ගෙවීම්_භාරය_දත්ත) in enumerate(시험사례):
        මාර්_ගය = 출력결과 / ('invalid-{}.elf'.format(නම)); මාර්_ගය.write_bytes(ගෙවීම්_භාරය_දත්ත)
        탑재덩이들.append(('invalid_{}'.format(색인), මාර්_ගය))
    어셈블리자료, ශීර්ෂය_අගය = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for නම, මාර්_ගය in 탑재덩이들:
        සංකේතය_අගය = 'user_blob_' + නම
        크기목록[නම] = මාර්_ගය.stat().st_size
        # 생성한 සමානයා_අගය 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + සංකේතය_අගය, සංකේතය_අගය + ':', '.incbin "{}"'.format(මාර්_ගය.relative_to(기준경로))]
        ශීර්ෂය_අගය.append('extern const unsigned char {}[];'.format(සංකේතය_අගය))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    ශීර්ෂය_අගය += ['static const යෙදු 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    ශීර්ෂය_අගය += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    ශීර්ෂය_අගය += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    ශීර්ෂය_අගය += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], ක්_රමය_ප්_රකාරය) for ක්_රමය_ප්_රකාරය in (0, 1)]
    ශීර්ෂය_අගය += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    ශීර්ෂය_අගය += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    ශීර්ෂය_අගය += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    ශීර්ෂය_අගය += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    ශීර්ෂය_අගය += ['};', 'static const යෙදු 잘못된실행항목들[] = {']
    ශීර්ෂය_අගය += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ගෙවීම්_භාරය_දත්ත)) for 순번, (_, ගෙවීම්_භාරය_දත්ත) in enumerate(시험사례)]
    ශීර්ෂය_අගය += ['};']
    (තැනුම_පෙත / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (තැනුම_පෙත / 'programs.h').write_text('\n'.join(ශීර්ෂය_අගය) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(නම for නම, _ in 시험사례) + '\n')
    ක්_රියාත්මක_කරන්න_විධානය([시언어번역기] + 설정비트 + ['-c', තැනුම_පෙත / 'programs.S', '-o', තැනුම_පෙත / 'programs.o'])
