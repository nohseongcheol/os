"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from bena_PYTHON import ħalaq_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def ħalaq_utent_SPACE(għerq_mogħdija, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Arkivju_għodda, 설정비트, eżegwixxa_kmand):
    설정비트 = [Settings_VALUE for Settings_VALUE in 설정비트 if Settings_VALUE != '-mgeneral-regs-only']
    bena_mogħdija = għerq_mogħdija / 'build'
    출력결과 = bena_mogħdija / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = għerq_mogħdija / 'utent'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, mogħdija, isem in [
            (시언어번역기, [], 원본자료 / 'serje.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'eżegwixxa_kmand.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'utent_pont.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Editur.c', 'vi.o')]:
        eżegwixxa_kmand([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', mogħdija, '-o', 출력결과 / isem])
    eżegwixxa_kmand([Arkivju_għodda, 'rcs', bena_mogħdija / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for isem in ('demo', 'fault', 'network', 'vi'):
        eżegwixxa_kmand([연결편집기, '-T', 원본자료 / 'Link_Tqassim.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (isem + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (isem + '.o'), bena_mogħdija / 'libposix-kor-user.a'])
    자바라이브러리만들기(għerq_mogħdija, eżegwixxa_kmand)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(bena_mogħdija)) as 작업경로:
        klassi_mogħdija = Path(작업경로)
        eżegwixxa_kmand(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klassi_mogħdija, '-sourcepath', klassi_mogħdija, '-d', klassi_mogħdija] +
            [data_pożizzjoni for data_pożizzjoni in sorted((저장소경로 / 'os/utent/자바').glob('*.java')) if data_pożizzjoni.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        eżegwixxa_kmand(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'għodda_entrata.serje',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(klassi_mogħdija.glob('*.class')))
    압축해제경로 = għerq_mogħdija / 'vendor/uzlib'
    for mogħdija, isem in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'lott.c', 'jar.o')] + [(압축해제경로 / (isem + '.c'), isem + '.o') for isem in ('tinflate', 'crc32', 'adler32')]:
        eżegwixxa_kmand([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', mogħdija, '-o', 출력결과 / isem])
    eżegwixxa_kmand([연결편집기, '-T', 원본자료 / 'Link_Tqassim.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / isem for isem in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    ħalaq_PYTHON(għerq_mogħdija, 시언어번역기, 연결편집기)
    시언어번역기만들기(għerq_mogħdija, 저장소경로, 시언어번역기, 연결편집기, 설정비트, eżegwixxa_kmand)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    programm_Intestazzjoni_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Intestazzjoni_Lista = [programm_Intestazzjoni_OFFSET + element_COUNT * 56 for element_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [data_pożizzjoni for data_pożizzjoni in Intestazzjoni_Lista if struct.unpack_from('<I', 유효함, data_pożizzjoni)[0] == 1]
    SMS, data = 적재구획[:2]
    kmand_ADDRESS = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    data_ADDRESS = struct.unpack_from('<Q', 유효함, data + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', kmand_ADDRESS + 1), ('data-entry', 24, 'Q', data_ADDRESS),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', kmand_ADDRESS + 8),
               ('overlap', data + 16, 'Q', kmand_ADDRESS)]
    for isem, OFFSET_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((isem, bytes(바뀐자료)))
    탑재덩이들 = [(isem.replace('-', '_'), 출력결과 / (isem + '.elf')) for isem in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (isem, payload_data) in enumerate(시험사례):
        mogħdija = 출력결과 / ('invalid-{}.elf'.format(isem)); mogħdija.write_bytes(payload_data)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), mogħdija))
    어셈블리자료, Intestazzjoni_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for isem, mogħdija in 탑재덩이들:
        simbolu_VALUE = 'user_blob_' + isem
        크기목록[isem] = mogħdija.stat().st_size
        # 생성한 peer_VALUE 경로만 넣어 프로젝트 경로의 공백/Kwotazzjoni 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + simbolu_VALUE, simbolu_VALUE + ':', '.incbin "{}"'.format(mogħdija.relative_to(għerq_mogħdija))]
        Intestazzjoni_VALUE.append('extern const unsigned char {}[];'.format(simbolu_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Intestazzjoni_VALUE += ['static const programm 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Intestazzjoni_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Intestazzjoni_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Intestazzjoni_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metodu_MODE) for metodu_MODE in (0, 1)]
    Intestazzjoni_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Intestazzjoni_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Intestazzjoni_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Intestazzjoni_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Intestazzjoni_VALUE += ['};', 'static const programm 잘못된실행항목들[] = {']
    Intestazzjoni_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(payload_data)) for 순번, (_, payload_data) in enumerate(시험사례)]
    Intestazzjoni_VALUE += ['};']
    (bena_mogħdija / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (bena_mogħdija / 'programs.h').write_text('\n'.join(Intestazzjoni_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(isem for isem, _ in 시험사례) + '\n')
    eżegwixxa_kmand([시언어번역기] + 설정비트 + ['-c', bena_mogħdija / 'programs.S', '-o', bena_mogħdija / 'programs.o'])
