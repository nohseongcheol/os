"""독립된 자체 ABI ELF64와 로더 거부 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from 파이썬빌드 import 파이썬만들기
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def döretmek_ulanyjy_ýer(기준경로, 저장소경로, 시언어번역기, 시플플번역기, 연결편집기, Arhiw_gural, 설정비트, ýerine_ýetir_buýruk):
    설정비트 = [Sazlamalar_baha for Sazlamalar_baha in 설정비트 if Sazlamalar_baha != '-mgeneral-regs-only']
    düz_ýol = 기준경로 / 'build'
    출력결과 = düz_ýol / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = 기준경로 / 'ulanyjy'
    포직스경로 = 저장소경로 / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Ýol, Ad in [
            (시언어번역기, [], 원본자료 / 'Bitir.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'ýerine_ýetir_buýruk.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / '사용자연결.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Redaktor.c', 'vi.o')]:
        ýerine_ýetir_buýruk([번역기] + 설정비트 + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Ýol, '-o', 출력결과 / Ad])
    ýerine_ýetir_buýruk([Arhiw_gural, 'rcs', düz_ýol / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Ad in ('demo', 'fault', 'network', 'vi'):
        ýerine_ýetir_buýruk([연결편집기, '-T', 원본자료 / 'Bag_Ýerleşiş.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Ad + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Ad + '.o'), düz_ýol / 'libposix-kor-user.a'])
    자바라이브러리만들기(기준경로, ýerine_ýetir_buýruk)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(düz_ýol)) as 작업경로:
        klas_ýol = Path(작업경로)
        ýerine_ýetir_buýruk(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klas_ýol, '-sourcepath', klas_ýol, '-d', klas_ýol] +
            [자료위치 for 자료위치 in sorted((저장소경로 / 'os/ulanyjy/자바').glob('*.java')) if 자료위치.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        ýerine_ýetir_buýruk(['sh', 저장소경로 / 'compiler/미리번역.sh', '--entry', 'gural_girizmeklik.Bitir',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(klas_ýol.glob('*.class')))
    압축해제경로 = 기준경로 / 'vendor/uzlib'
    for Ýol, Ad in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'toplum.c', 'jar.o')] + [(압축해제경로 / (Ad + '.c'), Ad + '.o') for Ad in ('tinflate', 'crc32', 'adler32')]:
        ýerine_ýetir_buýruk([시언어번역기] + 설정비트 + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Ýol, '-o', 출력결과 / Ad])
    ýerine_ýetir_buýruk([연결편집기, '-T', 원본자료 / 'Bag_Ýerleşiş.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Ad for Ad in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    파이썬만들기(기준경로, 시언어번역기, 연결편집기)
    시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ýerine_ýetir_buýruk)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    programma_At_Süýşüriş = struct.unpack_from('<Q', 유효함, 32)[0]
    At_Sanaw = [programma_At_Süýşüriş + 개수 * 56 for 개수 in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [자료위치 for 자료위치 in At_Sanaw if struct.unpack_from('<I', 유효함, 자료위치)[0] == 1]
    Metin, maglumat = 적재구획[:2]
    buýruk_salgy = struct.unpack_from('<Q', 유효함, Metin + 16)[0]
    maglumat_salgy = struct.unpack_from('<Q', 유효함, maglumat + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', buýruk_salgy + 1), ('data-entry', 24, 'Q', maglumat_salgy),
               ('outside-file', Metin + 32, 'Q', len(유효함) + 1), ('short-memory', Metin + 40, 'Q', 1),
               ('kernel-address', Metin + 16, 'Q', 0x80000), ('memory-overflow', Metin + 40, 'Q', 2**64 - 1),
               ('writable-code', Metin + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Metin, 'I', 2),
               ('unaligned-load', Metin + 16, 'Q', buýruk_salgy + 8),
               ('overlap', maglumat + 16, 'Q', buýruk_salgy)]
    for Ad, Süýşüriş_baha, format_932e03c8, baha in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, Süýşüriş_baha, baha)
        시험사례.append((Ad, bytes(바뀐자료)))
    탑재덩이들 = [(Ad.replace('-', '_'), 출력결과 / (Ad + '.elf')) for Ad in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for 색인, (Ad, ýük_gutujygy_maglumat) in enumerate(시험사례):
        Ýol = 출력결과 / ('invalid-{}.elf'.format(Ad)); Ýol.write_bytes(ýük_gutujygy_maglumat)
        탑재덩이들.append(('invalid_{}'.format(색인), Ýol))
    어셈블리자료, At_baha = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Ad, Ýol in 탑재덩이들:
        nyşan_baha = 'user_blob_' + Ad
        크기목록[Ad] = Ýol.stat().st_size
        # 생성한 deň_derejeli_düwün_baha 경로만 넣어 프로젝트 경로의 공백/따옴표 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + nyşan_baha, nyşan_baha + ':', '.incbin "{}"'.format(Ýol.relative_to(기준경로))]
        At_baha.append('extern const unsigned char {}[];'.format(nyşan_baha))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    At_baha += ['static const programma 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    At_baha += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    At_baha += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    At_baha += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], usul_reje) for usul_reje in (0, 1)]
    At_baha += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    At_baha += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    At_baha += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    At_baha += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    At_baha += ['};', 'static const programma 잘못된실행항목들[] = {']
    At_baha += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ýük_gutujygy_maglumat)) for 순번, (_, ýük_gutujygy_maglumat) in enumerate(시험사례)]
    At_baha += ['};']
    (düz_ýol / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (düz_ýol / 'programs.h').write_text('\n'.join(At_baha) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Ad for Ad, _ in 시험사례) + '\n')
    ýerine_ýetir_buýruk([시언어번역기] + 설정비트 + ['-c', düz_ýol / 'programs.S', '-o', düz_ýol / 'programs.o'])
