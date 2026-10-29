"""독립된 savas ABI ELF64와 로더 atmesti_VALUE 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from kompiliuoti_PYTHON import kurti_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from kompiliuoti_C_kompiliatorius import kurti_C_kompiliatorius


def kurti_naudotojas_erdvė(šaknis_kelias, saugykla_kelias, C_kompiliatorius, 시플플번역기, 연결편집기, Archyvas_įrankis, konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba, Vykdyti_komanda):
    konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba = [Parametrai_VALUE for Parametrai_VALUE in konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba if Parametrai_VALUE != '-mgeneral-regs-only']
    kompiliuoti_kelias = šaknis_kelias / 'build'
    išeiga = kompiliuoti_kelias / 'user'
    išeiga.mkdir(exist_ok=True)
    원본자료 = šaknis_kelias / 'naudotojas'
    포직스경로 = saugykla_kelias / 'posix-kor/arm64-native'
    apimti_kelias = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', išeiga]
    for kompiliatorius_įrankis, 추가영역, KELIAS, Pavadinimas_2 in [
            (C_kompiliatorius, [], 원본자료 / 'Paleisti.S', 'start.o'),
            (C_kompiliatorius, ['-std=c11'], 원본자료 / 'Vykdyti_komanda.c', 'runtime.o'),
            (C_kompiliatorius, ['-std=c11'], 포직스경로 / 'naudotojas_tiltas.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'FailoPavyzdys.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_kompiliatorius, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (C_kompiliatorius, ['-std=c11'], 원본자료 / 'Redaktorius.c', 'vi.o')]:
        Vykdyti_komanda([kompiliatorius_įrankis] + konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba + 추가영역 + apimti_kelias + ['-Wall', '-Wextra', '-Werror', '-c', KELIAS, '-o', išeiga / Pavadinimas_2])
    Vykdyti_komanda([Archyvas_įrankis, 'rcs', kompiliuoti_kelias / 'libposix-kor-user.a', išeiga / 'posix.o'])
    for Pavadinimas_2 in ('demo', 'fault', 'network', 'vi'):
        Vykdyti_komanda([연결편집기, '-T', 원본자료 / 'sieti_schema.ld', '-z', 'max-page-size=4096', '-o', išeiga / (Pavadinimas_2 + '.elf'),
             išeiga / 'start.o', išeiga / 'runtime.o', išeiga / (Pavadinimas_2 + '.o'), kompiliuoti_kelias / 'libposix-kor-user.a'])
    자바라이브러리만들기(šaknis_kelias, Vykdyti_komanda)
    # 기존 savas Java kompiliatorius/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(kompiliuoti_kelias)) as 작업경로:
        klasė_kelias = Path(작업경로)
        Vykdyti_komanda(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klasė_kelias, '-sourcepath', klasė_kelias, '-d', klasė_kelias] +
            [duomenys_padėtis for duomenys_padėtis in sorted((saugykla_kelias / 'os/naudotojas/자바').glob('*.java')) if duomenys_padėtis.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Vykdyti_komanda(['sh', saugykla_kelias / 'compiler/미리번역.sh', '--entry', 'įrankis_įrašas.Paleisti',
             '--profile', 'user', '--heap-words', '1048576', '-o', išeiga / 'java-tools.c'] + sorted(klasė_kelias.glob('*.class')))
    압축해제경로 = šaknis_kelias / 'vendor/uzlib'
    for KELIAS, Pavadinimas_2 in [(išeiga / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'paketas.c', 'jar.o')] + [(압축해제경로 / (Pavadinimas_2 + '.c'), Pavadinimas_2 + '.o') for Pavadinimas_2 in ('tinflate', 'crc32', 'adler32')]:
        Vykdyti_komanda([C_kompiliatorius] + konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + apimti_kelias + ['-c', KELIAS, '-o', išeiga / Pavadinimas_2])
    Vykdyti_komanda([연결편집기, '-T', 원본자료 / 'sieti_schema.ld', '-z', 'max-page-size=4096', '-o', išeiga / 'java-tools.elf'] +
        [išeiga / Pavadinimas_2 for Pavadinimas_2 in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    kurti_PYTHON(šaknis_kelias, C_kompiliatorius, 연결편집기)
    kurti_C_kompiliatorius(šaknis_kelias, saugykla_kelias, C_kompiliatorius, 연결편집기, konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba, Vykdyti_komanda)
    유효함 = (išeiga / 'demo.elf').read_bytes()
    programa_Antraštė_OFFSET = struct.unpack_from('<Q', 유효함, 32)[0]
    Antraštė_Sąrašas = [programa_Antraštė_OFFSET + prekė_COUNT * 56 for prekė_COUNT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [duomenys_padėtis for duomenys_padėtis in Antraštė_Sąrašas if struct.unpack_from('<I', 유효함, duomenys_padėtis)[0] == 1]
    Tekstas, duomenys = 적재구획[:2]
    komanda_ADDRESS = struct.unpack_from('<Q', 유효함, Tekstas + 16)[0]
    duomenys_ADDRESS = struct.unpack_from('<Q', 유효함, duomenys + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', komanda_ADDRESS + 1), ('data-entry', 24, 'Q', duomenys_ADDRESS),
               ('outside-file', Tekstas + 32, 'Q', len(유효함) + 1), ('short-memory', Tekstas + 40, 'Q', 1),
               ('kernel-address', Tekstas + 16, 'Q', 0x80000), ('memory-overflow', Tekstas + 40, 'Q', 2**64 - 1),
               ('writable-code', Tekstas + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Tekstas, 'I', 2),
               ('unaligned-load', Tekstas + 16, 'Q', komanda_ADDRESS + 8),
               ('overlap', duomenys + 16, 'Q', komanda_ADDRESS)]
    for Pavadinimas_2, OFFSET_VALUE, formatas_932e03c8, VALUE in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + formatas_932e03c8, 바뀐자료, OFFSET_VALUE, VALUE)
        시험사례.append((Pavadinimas_2, bytes(바뀐자료)))
    탑재덩이들 = [(Pavadinimas_2.replace('-', '_'), išeiga / (Pavadinimas_2 + '.elf')) for Pavadinimas_2 in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for LOOKUP_INDEX, (Pavadinimas_2, mokamoji_krova_duomenys) in enumerate(시험사례):
        KELIAS = išeiga / ('invalid-{}.elf'.format(Pavadinimas_2)); KELIAS.write_bytes(mokamoji_krova_duomenys)
        탑재덩이들.append(('invalid_{}'.format(LOOKUP_INDEX), KELIAS))
    rinkinys, Antraštė_VALUE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Pavadinimas_2, KELIAS in 탑재덩이들:
        simbolis_VALUE = 'user_blob_' + Pavadinimas_2
        크기목록[Pavadinimas_2] = KELIAS.stat().st_size
        # 생성한 lygiavertis_mazgas_VALUE 경로만 넣어 프로젝트 경로의 공백/Citavimas 영향을 피한다.
        rinkinys += ['.balign 16', '.global ' + simbolis_VALUE, simbolis_VALUE + ':', '.incbin "{}"'.format(KELIAS.relative_to(šaknis_kelias))]
        Antraštė_VALUE.append('extern const unsigned char {}[];'.format(simbolis_VALUE))
    rinkinys.append('.section .note.GNU-stack,"",%progbits')
    Antraštė_VALUE += ['static const programa 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Antraštė_VALUE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Antraštė_VALUE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Antraštė_VALUE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metodas_MODE) for metodas_MODE in (0, 1)]
    Antraštė_VALUE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Antraštė_VALUE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Antraštė_VALUE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Antraštė_VALUE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Antraštė_VALUE += ['};', 'static const programa 잘못된실행항목들[] = {']
    Antraštė_VALUE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(mokamoji_krova_duomenys)) for 순번, (_, mokamoji_krova_duomenys) in enumerate(시험사례)]
    Antraštė_VALUE += ['};']
    (kompiliuoti_kelias / 'programs.S').write_text('\n'.join(rinkinys) + '\n')
    (kompiliuoti_kelias / 'programs.h').write_text('\n'.join(Antraštė_VALUE) + '\n')
    (išeiga / 'invalid-cases.txt').write_text('\n'.join(Pavadinimas_2 for Pavadinimas_2, _ in 시험사례) + '\n')
    Vykdyti_komanda([C_kompiliatorius] + konfigūracija_foninio_intelektualiojo_perdavimo_tarnyba + ['-c', kompiliuoti_kelias / 'programs.S', '-o', kompiliuoti_kelias / 'programs.o'])
