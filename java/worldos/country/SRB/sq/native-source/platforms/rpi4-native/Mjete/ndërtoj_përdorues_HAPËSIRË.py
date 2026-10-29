"""독립된 자체 ABI ELF64와 로더 refuzo_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from ndërtoj_PYTHON import Krijo_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Krijo_përdorues_HAPËSIRË(rrënjë_shteg, depo_shteg, 시언어번역기, 시플플번역기, 연결편집기, arkiv_vegël, konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond, zbatoj_komandë):
    konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond = [cilësimet_VALUE for cilësimet_VALUE in konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond if cilësimet_VALUE != '-mgeneral-regs-only']
    ndërtoj_shteg = rrënjë_shteg / 'build'
    출력결과 = ndërtoj_shteg / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = rrënjë_shteg / 'përdorues'
    포직스경로 = depo_shteg / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, POZICIONI, Emër in [
            (시언어번역기, [], 원본자료 / 'Ekzekuto.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'zbatoj_komandë.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'përdorues_urë.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Redaktori.c', 'vi.o')]:
        zbatoj_komandë([번역기] + konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', POZICIONI, '-o', 출력결과 / Emër])
    zbatoj_komandë([arkiv_vegël, 'rcs', ndërtoj_shteg / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Emër in ('demo', 'fault', 'network', 'vi'):
        zbatoj_komandë([연결편집기, '-T', 원본자료 / 'lidh_Navigimi.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Emër + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Emër + '.o'), ndërtoj_shteg / 'libposix-kor-user.a'])
    자바라이브러리만들기(rrënjë_shteg, zbatoj_komandë)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(ndërtoj_shteg)) as 작업경로:
        klasë_shteg = Path(작업경로)
        zbatoj_komandë(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klasë_shteg, '-sourcepath', klasë_shteg, '-d', klasë_shteg] +
            [të_dhëna_pozicioni for të_dhëna_pozicioni in sorted((depo_shteg / 'os/përdorues/자바').glob('*.java')) if të_dhëna_pozicioni.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        zbatoj_komandë(['sh', depo_shteg / 'compiler/미리번역.sh', '--entry', 'vegël_futje.Ekzekuto',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(klasë_shteg.glob('*.class')))
    압축해제경로 = rrënjë_shteg / 'vendor/uzlib'
    for POZICIONI, Emër in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'grupoj.c', 'jar.o')] + [(압축해제경로 / (Emër + '.c'), Emër + '.o') for Emër in ('tinflate', 'crc32', 'adler32')]:
        zbatoj_komandë([시언어번역기] + konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', POZICIONI, '-o', 출력결과 / Emër])
    zbatoj_komandë([연결편집기, '-T', 원본자료 / 'lidh_Navigimi.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Emër for Emër in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Krijo_PYTHON(rrënjë_shteg, 시언어번역기, 연결편집기)
    시언어번역기만들기(rrënjë_shteg, depo_shteg, 시언어번역기, 연결편집기, konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond, zbatoj_komandë)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    program_Kreu_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Kreu_Listë = [program_Kreu_OFFSET + njësi_COUNT * 56 for njësi_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [të_dhëna_pozicioni for të_dhëna_pozicioni in Kreu_Listë if struct.unpack_from('<I', 유효함, të_dhëna_pozicioni)[0] == 1]
    Teksti, të_dhëna = 적재구획[:2]
    komandë_email = struct.unpack_from('<Q', 유효함, Teksti + 16)[0]
    të_dhëna_email = struct.unpack_from('<Q', 유효함, të_dhëna + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', komandë_email + 1), ('data-entry', 24, 'Q', të_dhëna_email),
               ('outside-file', Teksti + 32, 'Q', len(유효함) + 1), ('short-memory', Teksti + 40, 'Q', 1),
               ('kernel-address', Teksti + 16, 'Q', 0x80000), ('memory-overflow', Teksti + 40, 'Q', 2**64 - 1),
               ('writable-code', Teksti + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Teksti, 'I', 2),
               ('unaligned-load', Teksti + 16, 'Q', komandë_email + 8),
               ('overlap', të_dhëna + 16, 'Q', komandë_email)]
    for Emër, OFFSET_VALUE, format_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Emër, bytes(바뀐자료)))
    탑재덩이들 = [(Emër.replace('-', '_'), 출력결과 / (Emër + '.elf')) for Emër in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Emër, ngarkesë_e_dobishme_të_dhëna) in enumerate(시험사례):
        POZICIONI = 출력결과 / ('invalid-{}.elf'.format(Emër)); POZICIONI.write_bytes(ngarkesë_e_dobishme_të_dhëna)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), POZICIONI))
    어셈블리자료, Kreu_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Emër, POZICIONI in 탑재덩이들:
        simbol_VALUE = 'user_blob_' + Emër
        크기목록[Emër] = POZICIONI.stat().st_size
        # 생성한 homolog_VALUE 경로만 넣어 프로젝트 경로의 공백/Citim 영향을 피한다.
        어셈블리자료 += ['.balign 16', '.global ' + simbol_VALUE, simbol_VALUE + ':', '.incbin "{}"'.format(POZICIONI.relative_to(rrënjë_shteg))]
        Kreu_VALUE.append('extern const unsigned char {}[];'.format(simbol_VALUE))
    어셈블리자료.append('.section .note.GNU-stack,"",%progbits')
    Kreu_VALUE += ['static const program 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Kreu_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Kreu_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Kreu_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metoda_MODE) for metoda_MODE in (0, 1)]
    Kreu_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Kreu_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Kreu_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Kreu_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Kreu_VALUE += ['};', 'static const program 잘못된실행항목들[] = {']
    Kreu_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(ngarkesë_e_dobishme_të_dhëna)) for 순번, (_, ngarkesë_e_dobishme_të_dhëna) in enumerate(시험사례)]
    Kreu_VALUE += ['};']
    (ndërtoj_shteg / 'programs.S').write_text('\n'.join(어셈블리자료) + '\n')
    (ndërtoj_shteg / 'programs.h').write_text('\n'.join(Kreu_VALUE) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Emër for Emër, _ in 시험사례) + '\n')
    zbatoj_komandë([시언어번역기] + konfigurim_Shërbimi_i_transferimit_inteligjent_në_sfond + ['-c', ndërtoj_shteg / 'programs.S', '-o', ndërtoj_shteg / 'programs.o'])
