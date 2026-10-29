"""독립된 oma ABI ELF64와 로더 keelduma_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from järk_PYTHON import avama_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from järk_15_kompilaator import avama_15_kompilaator


def avama_kasutaja_ruum(juur_tee, hoidla_tee, _15_kompilaator, 시플플번역기, 연결편집기, Arhiiv_tööriist, konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus, Täida_käsk):
    konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus = [Sätted_VALUE for Sätted_VALUE in konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus if Sätted_VALUE != '-mgeneral-regs-only']
    järk_tee = juur_tee / 'build'
    toodang = järk_tee / 'user'
    toodang.mkdir(exist_ok=True)
    원본자료 = juur_tee / 'kasutaja'
    포직스경로 = hoidla_tee / 'posix-kor/arm64-native'
    hõlmama_tee = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', toodang]
    for kompilaator_tööriist, 추가영역, RADA, Nimi_2 in [
            (_15_kompilaator, [], 원본자료 / 'Käivita_2.S', 'start.o'),
            (_15_kompilaator, ['-std=c11'], 원본자료 / 'Täida_käsk.c', 'runtime.o'),
            (_15_kompilaator, ['-std=c11'], 포직스경로 / 'kasutaja_sild.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'FailiNäide.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (_15_kompilaator, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (_15_kompilaator, ['-std=c11'], 원본자료 / 'korrektor.c', 'vi.o')]:
        Täida_käsk([kompilaator_tööriist] + konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus + 추가영역 + hõlmama_tee + ['-Wall', '-Wextra', '-Werror', '-c', RADA, '-o', toodang / Nimi_2])
    Täida_käsk([Arhiiv_tööriist, 'rcs', järk_tee / 'libposix-kor-user.a', toodang / 'posix.o'])
    for Nimi_2 in ('demo', 'fault', 'network', 'vi'):
        Täida_käsk([연결편집기, '-T', 원본자료 / 'Link_küljend.ld', '-z', 'max-page-size=4096', '-o', toodang / (Nimi_2 + '.elf'),
             toodang / 'start.o', toodang / 'runtime.o', toodang / (Nimi_2 + '.o'), järk_tee / 'libposix-kor-user.a'])
    자바라이브러리만들기(juur_tee, Täida_käsk)
    # 기존 oma Java kompilaator/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(järk_tee)) as 작업경로:
        tund_tee = Path(작업경로)
        Täida_käsk(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', tund_tee, '-sourcepath', tund_tee, '-d', tund_tee] +
            [andmed_ametikoht for andmed_ametikoht in sorted((hoidla_tee / 'os/kasutaja/자바').glob('*.java')) if andmed_ametikoht.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Täida_käsk(['sh', hoidla_tee / 'compiler/미리번역.sh', '--entry', 'tööriist_kirje.Käivita_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', toodang / 'java-tools.c'] + sorted(tund_tee.glob('*.class')))
    압축해제경로 = juur_tee / 'vendor/uzlib'
    for RADA, Nimi_2 in [(toodang / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'kogum.c', 'jar.o')] + [(압축해제경로 / (Nimi_2 + '.c'), Nimi_2 + '.o') for Nimi_2 in ('tinflate', 'crc32', 'adler32')]:
        Täida_käsk([_15_kompilaator] + konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + hõlmama_tee + ['-c', RADA, '-o', toodang / Nimi_2])
    Täida_käsk([연결편집기, '-T', 원본자료 / 'Link_küljend.ld', '-z', 'max-page-size=4096', '-o', toodang / 'java-tools.elf'] +
        [toodang / Nimi_2 for Nimi_2 in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    avama_PYTHON(juur_tee, _15_kompilaator, 연결편집기)
    avama_15_kompilaator(juur_tee, hoidla_tee, _15_kompilaator, 연결편집기, konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus, Täida_käsk)
    유효함 = (toodang / 'demo.elf').read_bytes()
    programm_Päis_nihe = struct.unpack_from('<Q', 유효함, 32)[0]
    Päis_Loend = [programm_Päis_nihe + kaup_COUNT * 56 for kaup_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [andmed_ametikoht for andmed_ametikoht in Päis_Loend if struct.unpack_from('<I', 유효함, andmed_ametikoht)[0] == 1]
    Tekst, andmed = 적재구획[:2]
    käsk_ADDRESS = struct.unpack_from('<Q', 유효함, Tekst + 16)[0]
    andmed_ADDRESS = struct.unpack_from('<Q', 유효함, andmed + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', käsk_ADDRESS + 1), ('data-entry', 24, 'Q', andmed_ADDRESS),
               ('outside-file', Tekst + 32, 'Q', len(유효함) + 1), ('short-memory', Tekst + 40, 'Q', 1),
               ('kernel-address', Tekst + 16, 'Q', 0x80000), ('memory-overflow', Tekst + 40, 'Q', 2**64 - 1),
               ('writable-code', Tekst + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Tekst, 'I', 2),
               ('unaligned-load', Tekst + 16, 'Q', käsk_ADDRESS + 8),
               ('overlap', andmed + 16, 'Q', käsk_ADDRESS)]
    for Nimi_2, nihe_VALUE, vorming_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + vorming_932e03c8, 바뀐자료, nihe_VALUE, VALUE)
        시험사례.append((Nimi_2, bytes(바뀐자료)))
    탑재덩이들 = [(Nimi_2.replace('-', '_'), toodang / (Nimi_2 + '.elf')) for Nimi_2 in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Nimi_2, last_andmed) in enumerate(시험사례):
        RADA = toodang / ('invalid-{}.elf'.format(Nimi_2)); RADA.write_bytes(last_andmed)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), RADA))
    komplekt, Päis_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nimi_2, RADA in 탑재덩이들:
        sümbol_VALUE = 'user_blob_' + Nimi_2
        크기목록[Nimi_2] = RADA.stat().st_size
        # 생성한 partner_VALUE 경로만 넣어 프로젝트 경로의 공백/Tsitaat 영향을 피한다.
        komplekt += ['.balign 16', '.global ' + sümbol_VALUE, sümbol_VALUE + ':', '.incbin "{}"'.format(RADA.relative_to(juur_tee))]
        Päis_VALUE.append('extern const unsigned char {}[];'.format(sümbol_VALUE))
    komplekt.append('.section .note.GNU-stack,"",%progbits')
    Päis_VALUE += ['static const programm 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Päis_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Päis_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Päis_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], meetod_MODE) for meetod_MODE in (0, 1)]
    Päis_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Päis_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Päis_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Päis_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Päis_VALUE += ['};', 'static const programm 잘못된실행항목들[] = {']
    Päis_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(last_andmed)) for 순번, (_, last_andmed) in enumerate(시험사례)]
    Päis_VALUE += ['};']
    (järk_tee / 'programs.S').write_text('\n'.join(komplekt) + '\n')
    (järk_tee / 'programs.h').write_text('\n'.join(Päis_VALUE) + '\n')
    (toodang / 'invalid-cases.txt').write_text('\n'.join(Nimi_2 for Nimi_2, _ in 시험사례) + '\n')
    Täida_käsk([_15_kompilaator] + konfiguratsioon_Taustal_töötav_intelligentne_edastusteenus + ['-c', järk_tee / 'programs.S', '-o', järk_tee / 'programs.o'])
