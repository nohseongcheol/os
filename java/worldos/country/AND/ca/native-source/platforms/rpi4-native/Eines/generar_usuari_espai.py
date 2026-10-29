"""독립된 propi ABI ELF64와 로더 rebutjar_VALOR 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from generar_PYTHON import Crear_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def Crear_usuari_espai(rel_camí, dipòsit_camí, 시언어번역기, 시플플번역기, 연결편집기, Arxiu_eina, configuració_Servei_de_transferència_intel_ligent_en_segon_terme, Executa_ordre):
    configuració_Servei_de_transferència_intel_ligent_en_segon_terme = [Configuració_VALOR for Configuració_VALOR in configuració_Servei_de_transferència_intel_ligent_en_segon_terme if Configuració_VALOR != '-mgeneral-regs-only']
    generar_camí = rel_camí / 'build'
    출력결과 = generar_camí / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = rel_camí / 'usuari'
    포직스경로 = dipòsit_camí / 'posix-kor/arm64-native'
    incloure_camí = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, Camí, Nom in [
            (시언어번역기, [], 원본자료 / 'Executa_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Executa_ordre.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'usuari_pont.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'ExempleFitxer.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Executa_ordre([번역기] + configuració_Servei_de_transferència_intel_ligent_en_segon_terme + 추가영역 + incloure_camí + ['-Wall', '-Wextra', '-Werror', '-c', Camí, '-o', 출력결과 / Nom])
    Executa_ordre([Arxiu_eina, 'rcs', generar_camí / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Nom in ('demo', 'fault', 'network', 'vi'):
        Executa_ordre([연결편집기, '-T', 원본자료 / 'enllaç_disseny.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Nom + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Nom + '.o'), generar_camí / 'libposix-kor-user.a'])
    자바라이브러리만들기(rel_camí, Executa_ordre)
    # 기존 propi Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(generar_camí)) as 작업경로:
        Classe_camí = Path(작업경로)
        Executa_ordre(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Classe_camí, '-sourcepath', Classe_camí, '-d', Classe_camí] +
            [dades_càrrec for dades_càrrec in sorted((dipòsit_camí / 'os/usuari/자바').glob('*.java')) if dades_càrrec.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Executa_ordre(['sh', dipòsit_camí / 'compiler/미리번역.sh', '--entry', 'eina_introducció.Executa_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Classe_camí.glob('*.class')))
    압축해제경로 = rel_camí / 'vendor/uzlib'
    for Camí, Nom in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'paquet.c', 'jar.o')] + [(압축해제경로 / (Nom + '.c'), Nom + '.o') for Nom in ('tinflate', 'crc32', 'adler32')]:
        Executa_ordre([시언어번역기] + configuració_Servei_de_transferència_intel_ligent_en_segon_terme + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + incloure_camí + ['-c', Camí, '-o', 출력결과 / Nom])
    Executa_ordre([연결편집기, '-T', 원본자료 / 'enllaç_disseny.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Nom for Nom in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Crear_PYTHON(rel_camí, 시언어번역기, 연결편집기)
    시언어번역기만들기(rel_camí, dipòsit_camí, 시언어번역기, 연결편집기, configuració_Servei_de_transferència_intel_ligent_en_segon_terme, Executa_ordre)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    programa_Capçalera_DESPLAÇAMENT = struct.unpack_from('<Q', 유효함, 32)[0]
    Capçalera_Llista = [programa_Capçalera_DESPLAÇAMENT + element_COMPT * 56 for element_COMPT in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [dades_càrrec for dades_càrrec in Capçalera_Llista if struct.unpack_from('<I', 유효함, dades_càrrec)[0] == 1]
    SMS, dades = 적재구획[:2]
    ordre_ADREÇA = struct.unpack_from('<Q', 유효함, SMS + 16)[0]
    dades_ADREÇA = struct.unpack_from('<Q', 유효함, dades + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', ordre_ADREÇA + 1), ('data-entry', 24, 'Q', dades_ADREÇA),
               ('outside-file', SMS + 32, 'Q', len(유효함) + 1), ('short-memory', SMS + 40, 'Q', 1),
               ('kernel-address', SMS + 16, 'Q', 0x80000), ('memory-overflow', SMS + 40, 'Q', 2**64 - 1),
               ('writable-code', SMS + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', SMS, 'I', 2),
               ('unaligned-load', SMS + 16, 'Q', ordre_ADREÇA + 8),
               ('overlap', dades + 16, 'Q', ordre_ADREÇA)]
    for Nom, DESPLAÇAMENT_VALOR, format_932e03c8, VALOR in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + format_932e03c8, 바뀐자료, DESPLAÇAMENT_VALOR, VALOR)
        시험사례.append((Nom, bytes(바뀐자료)))
    탑재덩이들 = [(Nom.replace('-', '_'), 출력결과 / (Nom + '.elf')) for Nom in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for Cerca_INDEX, (Nom, càrrega_dades) in enumerate(시험사례):
        Camí = 출력결과 / ('invalid-{}.elf'.format(Nom)); Camí.write_bytes(càrrega_dades)
        탑재덩이들.append(('invalid_{}'.format(Cerca_INDEX), Camí))
    assemblatge, Capçalera_VALOR = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nom, Camí in 탑재덩이들:
        símbol_VALOR = 'user_blob_' + Nom
        크기목록[Nom] = Camí.stat().st_size
        # 생성한 homòleg_VALOR 경로만 넣어 프로젝트 경로의 공백/oferta 영향을 피한다.
        assemblatge += ['.balign 16', '.global ' + símbol_VALOR, símbol_VALOR + ':', '.incbin "{}"'.format(Camí.relative_to(rel_camí))]
        Capçalera_VALOR.append('extern const unsigned char {}[];'.format(símbol_VALOR))
    assemblatge.append('.section .note.GNU-stack,"",%progbits')
    Capçalera_VALOR += ['static const programa 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Capçalera_VALOR += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Capçalera_VALOR += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Capçalera_VALOR += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], 방식) for 방식 in (0, 1)]
    Capçalera_VALOR += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Capçalera_VALOR += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Capçalera_VALOR += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Capçalera_VALOR += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Capçalera_VALOR += ['};', 'static const programa 잘못된실행항목들[] = {']
    Capçalera_VALOR += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(càrrega_dades)) for 순번, (_, càrrega_dades) in enumerate(시험사례)]
    Capçalera_VALOR += ['};']
    (generar_camí / 'programs.S').write_text('\n'.join(assemblatge) + '\n')
    (generar_camí / 'programs.h').write_text('\n'.join(Capçalera_VALOR) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Nom for Nom, _ in 시험사례) + '\n')
    Executa_ordre([시언어번역기] + configuració_Servei_de_transferència_intel_ligent_en_segon_terme + ['-c', generar_camí / 'programs.S', '-o', generar_camí / 'programs.o'])
