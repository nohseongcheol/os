"""독립된 nativo ABI ELF64와 로더 rifiutare_VALORE prove 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from BLD_PYTHON import Crea_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from BLD_C_compilatore import Crea_C_compilatore


def Crea_USER_Space(radice_percorso, archivio_percorso, C_compilatore, 시플플번역기, linker_strumento, Archivio_strumento, configurazione_BITS, Esegui_comando):
    configurazione_BITS = [Impostazioni_VALORE for Impostazioni_VALORE in configurazione_BITS if Impostazioni_VALORE != '-mgeneral-regs-only']
    BLD_percorso = radice_percorso / 'build'
    output = BLD_percorso / 'user'
    output.mkdir(exist_ok=True)
    원본자료 = radice_percorso / 'spazio_utente'
    포직스경로 = archivio_percorso / 'posix-kor/arm64-native'
    includere_percorso = ['-I', 원본자료, '-I', 포직스경로 / 'dichiarazioni', '-I', output]
    for compilatore_strumento, 추가영역, percorso, Nome in [
            (C_compilatore, [], 원본자료 / 'avvia.S', 'start.o'),
            (C_compilatore, ['-std=c11'], 원본자료 / 'Esegui_comando.c', 'runtime.o'),
            (C_compilatore, ['-std=c11'], 포직스경로 / 'USER_bridge.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'EsempioFile.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_compilatore, ['-std=c11'], 원본자료 / 'Protezione_test.c', 'fault.o'),
            (C_compilatore, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Esegui_comando([compilatore_strumento] + configurazione_BITS + 추가영역 + includere_percorso + ['-Wall', '-Wextra', '-Werror', '-c', percorso, '-o', output / Nome])
    Esegui_comando([Archivio_strumento, 'rcs', BLD_percorso / 'libposix-kor-user.a', output / 'posix.o'])
    for Nome in ('demo', 'fault', 'network', 'vi'):
        Esegui_comando([linker_strumento, '-T', 원본자료 / 'disposizione_di_collegamento.ld', '-z', 'max-page-size=4096', '-o', output / (Nome + '.elf'),
             output / 'start.o', output / 'runtime.o', output / (Nome + '.o'), BLD_percorso / 'libposix-kor-user.a'])
    자바라이브러리만들기(radice_percorso, Esegui_comando)
    # 기존 nativo Java compilatore/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(BLD_percorso)) as 작업경로:
        Corso_percorso = Path(작업경로)
        Esegui_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Corso_percorso, '-sourcepath', Corso_percorso, '-d', Corso_percorso] +
            [dati_funzione for dati_funzione in sorted((archivio_percorso / 'os/spazio_utente/자바').glob('*.java')) if dati_funzione.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Esegui_comando(['sh', archivio_percorso / 'compiler/미리번역.sh', '--entry', 'strumento_voce.avvia',
             '--profile', 'user', '--heap-words', '1048576', '-o', output / 'java-tools.c'] + sorted(Corso_percorso.glob('*.class')))
    압축해제경로 = radice_percorso / 'vendor/uzlib'
    for percorso, Nome in [(output / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'aggregare.c', 'jar.o')] + [(압축해제경로 / (Nome + '.c'), Nome + '.o') for Nome in ('tinflate', 'crc32', 'adler32')]:
        Esegui_comando([C_compilatore] + configurazione_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + includere_percorso + ['-c', percorso, '-o', output / Nome])
    Esegui_comando([linker_strumento, '-T', 원본자료 / 'disposizione_di_collegamento.ld', '-z', 'max-page-size=4096', '-o', output / 'java-tools.elf'] +
        [output / Nome for Nome in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Crea_PYTHON(radice_percorso, C_compilatore, linker_strumento)
    Crea_C_compilatore(radice_percorso, archivio_percorso, C_compilatore, linker_strumento, configurazione_BITS, Esegui_comando)
    valido = (output / 'demo.elf').read_bytes()
    app_Intestazione_SCARTO = struct.unpack_from('<Q', valido, 32)[0]
    Intestazione_elenco = [app_Intestazione_SCARTO + articolo_CONTA_NUMERI * 56 for articolo_CONTA_NUMERI in range(struct.unpack_from('<H', valido, 56)[0])]
    적재구획 = [dati_funzione for dati_funzione in Intestazione_elenco if struct.unpack_from('<I', valido, dati_funzione)[0] == 1]
    testo, dati = 적재구획[:2]
    comando_e_mail = struct.unpack_from('<Q', valido, testo + 16)[0]
    dati_e_mail = struct.unpack_from('<Q', valido, dati + 16)[0]
    Chiama_ABI = valido.index(b'JKOROS\0')
    test_case = [('empty', b''), ('short', valido[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', comando_e_mail + 1), ('data-entry', 24, 'Q', dati_e_mail),
               ('outside-file', testo + 32, 'Q', len(valido) + 1), ('short-memory', testo + 40, 'Q', 1),
               ('kernel-address', testo + 16, 'Q', 0x80000), ('memory-overflow', testo + 40, 'Q', 2**64 - 1),
               ('writable-code', testo + 4, 'I', 7), ('missing-abi', Chiama_ABI, 'B', ord('X')),
               ('wrong-abi', Chiama_ABI + 8, 'I', 2), ('dynamic', testo, 'I', 2),
               ('unaligned-load', testo + 16, 'Q', comando_e_mail + 8),
               ('overlap', dati + 16, 'Q', comando_e_mail)]
    for Nome, SCARTO_VALORE, formato_932e03c8, VALORE in 수정사항:
        바뀐자료 = bytearray(valido); struct.pack_into('<' + formato_932e03c8, 바뀐자료, SCARTO_VALORE, VALORE)
        test_case.append((Nome, bytes(바뀐자료)))
    탑재덩이들 = [(Nome.replace('-', '_'), output / (Nome + '.elf')) for Nome in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for CERCA_INDICE, (Nome, payload_dati) in enumerate(test_case):
        percorso = output / ('invalid-{}.elf'.format(Nome)); percorso.write_bytes(payload_dati)
        탑재덩이들.append(('invalid_{}'.format(CERCA_INDICE), percorso))
    assembly, Intestazione_VALORE = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nome, percorso in 탑재덩이들:
        simbolo_VALORE = 'user_blob_' + Nome
        크기목록[Nome] = percorso.stat().st_size
        # 생성한 peer_VALORE 경로만 넣어 프로젝트 경로의 공백/offerta 영향을 피한다.
        assembly += ['.balign 16', '.global ' + simbolo_VALORE, simbolo_VALORE + ':', '.incbin "{}"'.format(percorso.relative_to(radice_percorso))]
        Intestazione_VALORE.append('extern const unsigned char {}[];'.format(simbolo_VALORE))
    assembly.append('.section .note.GNU-stack,"",%progbits')
    Intestazione_VALORE += ['static const app 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Intestazione_VALORE += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Intestazione_VALORE += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Intestazione_VALORE += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], metodo_MODA) for metodo_MODA in (0, 1)]
    Intestazione_VALORE += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Intestazione_VALORE += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Intestazione_VALORE += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Intestazione_VALORE += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Intestazione_VALORE += ['};', 'static const app 잘못된실행항목들[] = {']
    Intestazione_VALORE += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(payload_dati)) for 순번, (_, payload_dati) in enumerate(test_case)]
    Intestazione_VALORE += ['};']
    (BLD_percorso / 'programs.S').write_text('\n'.join(assembly) + '\n')
    (BLD_percorso / 'programs.h').write_text('\n'.join(Intestazione_VALORE) + '\n')
    (output / 'invalid-cases.txt').write_text('\n'.join(Nome for Nome, _ in test_case) + '\n')
    Esegui_comando([C_compilatore] + configurazione_BITS + ['-c', BLD_percorso / 'programs.S', '-o', BLD_percorso / 'programs.o'])
