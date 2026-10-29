"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def 사용자영역만들기(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Akhaebe_tholosi, 설정비트, phethagatša_taelo):
    설정비트 = [Dipeakanyo_boleng for Dipeakanyo_boleng in 설정비트 if Dipeakanyo_boleng != '-mgeneral-regs-only']
    aga_tsela = 기준경로 / 'build'
    출력결과 = aga_tsela / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'mošomiši'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Tsejana, Leina in [
            (시언어번역기, [], 원본자료 / 'Diriša.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'phethagatša_taelo.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'mošomiši_kgokaganyo.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Morulaganyi.c', 'vi.o')]:
        phethagatša_taelo([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Tsejana, '-o', 출력결과 / Leina])
    phethagatša_taelo([Akhaebe_tholosi, 'rcs', aga_tsela / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Leina in ('demo', 'fault', 'network', 'vi'):
        phethagatša_taelo([연결편집기, '-T', 원본자료 / 'linke_Sebopego.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Leina + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Leina + '.o'), aga_tsela / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, phethagatša_taelo)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(aga_tsela)) as 작업경로:
        legoro_tsela = Path(작업경로)
        phethagatša_taelo(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', legoro_tsela, '-sourcepath', legoro_tsela, '-d', legoro_tsela] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/mošomiši/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        phethagatša_taelo(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'tholosi_go_tsenya_tshedimošo.Diriša',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(legoro_tsela.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for Tsejana, Leina in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'sehlopha.c', 'jar.o')] + [(압축해제경로 / (Leina + '.c'), Leina + '.o') for Leina in ('tinflate', 'crc32', 'adler32')]:
        phethagatša_taelo([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Tsejana, '-o', 출력결과 / Leina])
    phethagatša_taelo([연결편집기, '-T', 원본자료 / 'linke_Sebopego.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Leina for Leina in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, phethagatša_taelo)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    tirišo_Hlogo_E_Šetšego = struct.unpack_from('<Q', 유효함, 32)[0]
    Hlogo_Lenaneo = [tirišo_Hlogo_E_Šetšego + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in Hlogo_Lenaneo if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    Sengwalwa, data = 적재구획[:2]
    taelo_atrese = struct.unpack_from('<Q', 유효함, Sengwalwa + 16)[0]
    data_atrese = struct.unpack_from('<Q', 유효함, data + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', taelo_atrese + 1), ('data-entry', 24, 'Q', data_atrese),
               ('outside-file', Sengwalwa + 32, 'Q', len(유효함) + 1), ('short-memory', Sengwalwa + 40, 'Q', 1),
               ('kernel-address', Sengwalwa + 16, 'Q', 0x80000), ('memory-overflow', Sengwalwa + 40, 'Q', 2**64 - 1),
               ('writable-code', Sengwalwa + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Sengwalwa, 'I', 2),
               ('unaligned-load', Sengwalwa + 16, 'Q', taelo_atrese + 8),
               ('overlap', data + 16, 'Q', taelo_atrese)]
    for Leina, E_Šetšego_boleng, fomete_932e03c8, boleng in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + fomete_932e03c8, 바뀐자료, E_Šetšego_boleng, boleng)
        시험사례.append((Leina, bytes(바뀐자료)))
    탑재덩이들 = [(Leina.replace('-', '_'), 출력결과 / (Leina + '.elf')) for Leina in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Leina, morwalotefelwa_data) in enumerate(시험사례):
        Tsejana = 출력결과 / ('invalid-{}.elf'.format(Leina)); Tsejana.write_bytes(morwalotefelwa_data)
        탑재덩이들.append(('invalid_{}'.format(색인), Tsejana))
    어셈블리자료, Hlogo_boleng = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Leina, Tsejana in 탑재덩이들:
        leswao_boleng = 'user_blob_' + Leina
        크기목록[Leina] = Tsejana.stat().st_size
        # 생성한 sedirišwa_sa_legoro_le_tee_boleng 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + leswao_boleng, leswao_boleng + ':', '.incbin "{}"'.format(Tsejana.relative_to(기준경로))]
        Hlogo_boleng.append('extern const unsigned char {}[];'.format(leswao_boleng))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Hlogo_boleng += ['static const tirišo 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Hlogo_boleng += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Hlogo_boleng += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Hlogo_boleng += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], mokgwa_mokgwa) for mokgwa_mokgwa in (0, 1)]
    Hlogo_boleng += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Hlogo_boleng += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Hlogo_boleng += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Hlogo_boleng += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Hlogo_boleng += ['};', 'static const tirišo 잘못된실행항목들[] = {']
    Hlogo_boleng += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(morwalotefelwa_data)) for 순번, (_, morwalotefelwa_data) in enumerate(시험사례)]
    Hlogo_boleng += ['};']
    (aga_tsela / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (aga_tsela / 'programs.h').write_text('\n'.join(Hlogo_boleng) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Leina for Leina, _ in 시험사례) + '\n')
    phethagatša_taelo([시언어번역기] + 설정비트 + ['-c', aga_tsela / 'programs.S', '-o', aga_tsela / 'programs.o'])
