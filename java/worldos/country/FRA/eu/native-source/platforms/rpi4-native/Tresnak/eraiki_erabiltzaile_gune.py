"""독립된 자체 ABI ELF64와 로더 baztertu_balio 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from eraiki_PYTHON import sortu_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def sortu_erabiltzaile_gune(erro_bide_izen, biltegi_bide_izen, 시언어번역기, 시플플번역기, 연결편집기, artxibo_tresna, konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna, exekutatu_komando):
    konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna = [Ezarpenak_balio for Ezarpenak_balio in konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna if Ezarpenak_balio != '-mgeneral-regs-only']
    eraiki_bide_izen = erro_bide_izen / 'build'
    출력결과 = eraiki_bide_izen / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = erro_bide_izen / 'erabiltzaile'
    포직스경로 = biltegi_bide_izen / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Bide_izena, Izena in [
            (시언어번역기, [], 원본자료 / 'Exekutatu_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'exekutatu_komando.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'erabiltzaile_zubi.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'editore.c', 'vi.o')]:
        exekutatu_komando([번역기] + konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', Bide_izena, '-o', 출력결과 / Izena])
    exekutatu_komando([artxibo_tresna, 'rcs', eraiki_bide_izen / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Izena in ('demo', 'fault', 'network', 'vi'):
        exekutatu_komando([연결편집기, '-T', 원본자료 / 'lotu_diseinu.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Izena + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Izena + '.o'), eraiki_bide_izen / 'libposix-kor-user.a'])
    자바라이브러리만들기(erro_bide_izen, exekutatu_komando)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(eraiki_bide_izen)) as 작업경로:
        Gela_bide_izen = Path(작업경로)
        exekutatu_komando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Gela_bide_izen, '-sourcepath', Gela_bide_izen, '-d', Gela_bide_izen] +
            [datuak_kargu for datuak_kargu in sorted((biltegi_bide_izen / 'os/erabiltzaile/자바').glob('*.java')) if datuak_kargu.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        exekutatu_komando(['sh', biltegi_bide_izen / 'compiler/미리번역.sh', '--entry', 'tresna_sarrera.Exekutatu_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Gela_bide_izen.glob('*.class')))
    압축해제경로 = erro_bide_izen / 'vendor/uzlib'
    for Bide_izena, Izena in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'multzo.c', 'jar.o')] + [(압축해제경로 / (Izena + '.c'), Izena + '.o') for Izena in ('tinflate', 'crc32', 'adler32')]:
        exekutatu_komando([시언어번역기] + konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', Bide_izena, '-o', 출력결과 / Izena])
    exekutatu_komando([연결편집기, '-T', 원본자료 / 'lotu_diseinu.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Izena for Izena in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    sortu_PYTHON(erro_bide_izen, 시언어번역기, 연결편집기)
    시언어번역기만들기(erro_bide_izen, biltegi_bide_izen, 시언어번역기, 연결편집기, konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna, exekutatu_komando)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    aplik_goiburu_Geruzak = struct.unpack_from('<Q', 유효함, 32)[0]
    goiburu_Zerrenda = [aplik_goiburu_Geruzak + elementu_ZENBATU * 56 for elementu_ZENBATU in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [datuak_kargu for datuak_kargu in goiburu_Zerrenda if struct.unpack_from('<I', 유효함, datuak_kargu)[0] == 1]
    Testua, datuak = 적재구획[:2]
    komando_helbide = struct.unpack_from('<Q', 유효함, Testua + 16)[0]
    datuak_helbide = struct.unpack_from('<Q', 유효함, datuak + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', komando_helbide + 1), ('data-entry', 24, 'Q', datuak_helbide),
               ('outside-file', Testua + 32, 'Q', len(유효함) + 1), ('short-memory', Testua + 40, 'Q', 1),
               ('kernel-address', Testua + 16, 'Q', 0x80000), ('memory-overflow', Testua + 40, 'Q', 2**64 - 1),
               ('writable-code', Testua + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Testua, 'I', 2),
               ('unaligned-load', Testua + 16, 'Q', komando_helbide + 8),
               ('overlap', datuak + 16, 'Q', komando_helbide)]
    for Izena, Geruzak_balio, formatu_932e03c8, balio in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + formatu_932e03c8, 바뀐자료, Geruzak_balio, balio)
        시험사례.append((Izena, bytes(바뀐자료)))
    탑재덩이들 = [(Izena.replace('-', '_'), 출력결과 / (Izena + '.elf')) for Izena in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for BEGIRATU_INDIZE, (Izena, karga_datuak) in enumerate(시험사례):
        Bide_izena = 출력결과 / ('invalid-{}.elf'.format(Izena)); Bide_izena.write_bytes(karga_datuak)
        탑재덩이들.append(('invalid_{}'.format(BEGIRATU_INDIZE), Bide_izena))
    mihiztatze, goiburu_balio = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Izena, Bide_izena in 탑재덩이들:
        ikur_balio = 'user_blob_' + Izena
        크기목록[Izena] = Bide_izena.stat().st_size
        # 생성한 pareko_balio 경로만 넣어 프로젝트 경로의 공백/Aipua 영향을 피한다.
        mihiztatze += ['.balign 16', '.global ' + ikur_balio, ikur_balio + ':', '.incbin "{}"'.format(Bide_izena.relative_to(erro_bide_izen))]
        goiburu_balio.append('extern const unsigned char {}[];'.format(ikur_balio))
    mihiztatze.append('.section .note.GNU-stack,"",%progbits')
    goiburu_balio += ['static const aplik 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    goiburu_balio += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    goiburu_balio += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    goiburu_balio += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], 방식) for 방식 in (0, 1)]
    goiburu_balio += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    goiburu_balio += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    goiburu_balio += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    goiburu_balio += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    goiburu_balio += ['};', 'static const aplik 잘못된실행항목들[] = {']
    goiburu_balio += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(karga_datuak)) for 순번, (_, karga_datuak) in enumerate(시험사례)]
    goiburu_balio += ['};']
    (eraiki_bide_izen / 'programs.S').write_text('\n'.join(mihiztatze) + '\n')
    (eraiki_bide_izen / 'programs.h').write_text('\n'.join(goiburu_balio) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Izena for Izena, _ in 시험사례) + '\n')
    exekutatu_komando([시언어번역기] + konfigurazio_Atzeko_planoko_transferentzia_zerbitzu_adimenduna + ['-c', eraiki_bide_izen / 'programs.S', '-o', eraiki_bide_izen / 'programs.o'])
