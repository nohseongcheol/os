"""독립된 자체 ABI ELF64와 로더 gwrthod_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from llunio_PYTHON import Creu_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Creu_defnyddiwr_lle(gwraidd_llwybr, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Archif_offeryn, 설정비트, Gweithredu_gorchymyn):
    설정비트 = [Gosodiadau_VALUE for Gosodiadau_VALUE in 설정비트 if Gosodiadau_VALUE != '-mgeneral-regs-only']
    llunio_llwybr = gwraidd_llwybr / 'build'
    출력결과 = llunio_llwybr / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = gwraidd_llwybr / 'defnyddiwr'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, LLWYBR, Enw in [
            (시언어번역기, [], 원본자료 / 'Gweithredu_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Gweithredu_gorchymyn.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'defnyddiwr_pont.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Gweithredu_gorchymyn([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', LLWYBR, '-o', 출력결과 / Enw])
    Gweithredu_gorchymyn([Archif_offeryn, 'rcs', llunio_llwybr / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Enw in ('demo', 'fault', 'network', 'vi'):
        Gweithredu_gorchymyn([연결편집기, '-T', 원본자료 / 'Dolen_Llywio.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Enw + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Enw + '.o'), llunio_llwybr / 'libposix-kor-user.a'])
    자바라이브러리만들기(gwraidd_llwybr, Gweithredu_gorchymyn)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(llunio_llwybr)) as 작업경로:
        Dosbarth_llwybr = Path(작업경로)
        Gweithredu_gorchymyn(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Dosbarth_llwybr, '-sourcepath', Dosbarth_llwybr, '-d', Dosbarth_llwybr] +
            [data_safle for data_safle in sorted((저장소경로 / 'os/defnyddiwr/자바').glob('*.java')) if data_safle.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Gweithredu_gorchymyn(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'offeryn_cofnod.Gweithredu_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Dosbarth_llwybr.glob('*.class')))
    압축해제경로 = gwraidd_llwybr / 'vendor/uzlib'
    for LLWYBR, Enw in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'bwndel.c', 'jar.o')] + [(압축해제경로 / (Enw + '.c'), Enw + '.o') for Enw in ('tinflate', 'crc32', 'adler32')]:
        Gweithredu_gorchymyn([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', LLWYBR, '-o', 출력결과 / Enw])
    Gweithredu_gorchymyn([연결편집기, '-T', 원본자료 / 'Dolen_Llywio.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Enw for Enw in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Creu_PYTHON(gwraidd_llwybr, 시언어번역기, 연결편집기)
    시언어번역기만들기(gwraidd_llwybr, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Gweithredu_gorchymyn)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    Rhaglen_Pennyn_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Pennyn_Rhestr = [Rhaglen_Pennyn_OFFSET + eitem_COUNT * 56 for eitem_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [data_safle for data_safle in Pennyn_Rhestr if struct.unpack_from('<I', 유효함, data_safle)[0] == 1]
    Testun, data = 적재구획[:2]
    gorchymyn_ADDRESS = struct.unpack_from('<Q', 유효함, Testun + 16)[0]
    data_ADDRESS = struct.unpack_from('<Q', 유효함, data + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', gorchymyn_ADDRESS + 1), ('data-entry', 24, 'Q', data_ADDRESS),
               ('outside-file', Testun + 32, 'Q', len(유효함) + 1), ('short-memory', Testun + 40, 'Q', 1),
               ('kernel-address', Testun + 16, 'Q', 0x80000), ('memory-overflow', Testun + 40, 'Q', 2**64 - 1),
               ('writable-code', Testun + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Testun, 'I', 2),
               ('unaligned-load', Testun + 16, 'Q', gorchymyn_ADDRESS + 8),
               ('overlap', data + 16, 'Q', gorchymyn_ADDRESS)]
    for Enw, OFFSET_VALUE, fformat_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + fformat_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Enw, bytes(바뀐자료)))
    탑재덩이들 = [(Enw.replace('-', '_'), 출력결과 / (Enw + '.elf')) for Enw in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Enw, llwyth_uchaf_data) in enumerate(시험사례):
        LLWYBR = 출력결과 / ('invalid-{}.elf'.format(Enw)); LLWYBR.write_bytes(llwyth_uchaf_data)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), LLWYBR))
    어셈블리자료, Pennyn_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Enw, LLWYBR in 탑재덩이들:
        symbol_VALUE = 'user_blob_' + Enw
        크기목록[Enw] = LLWYBR.stat().st_size
        # 생성한 cymar_VALUE 경로만 넣어 프로젝트 경로의 공백/Dyfyniad 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + symbol_VALUE, symbol_VALUE + ':', '.incbin "{}"'.format(LLWYBR.relative_to(gwraidd_llwybr))]
        Pennyn_VALUE.append('extern const unsigned char {}[];'.format(symbol_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Pennyn_VALUE += ['static const Rhaglen 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Pennyn_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Pennyn_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Pennyn_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], dull_MODE) for dull_MODE in (0, 1)]
    Pennyn_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Pennyn_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Pennyn_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Pennyn_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Pennyn_VALUE += ['};', 'static const Rhaglen 잘못된실행항목들[] = {']
    Pennyn_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(llwyth_uchaf_data)) for 순번, (_, llwyth_uchaf_data) in enumerate(시험사례)]
    Pennyn_VALUE += ['};']
    (llunio_llwybr / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (llunio_llwybr / 'programs.h').write_text('\n'.join(Pennyn_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Enw for Enw, _ in 시험사례) + '\n')
    Gweithredu_gorchymyn([시언어번역기] + 설정비트 + ['-c', llunio_llwybr / 'programs.S', '-o', llunio_llwybr / 'programs.o'])
