"""독립된 자체 ABI ELF64와 로더 rexeitar_VALOR_e3ecc00b 시험 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from compilar_PYTHON import crear_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from 시언어번역기빌드 import 시언어번역기만들기


def crear_usuario_espazo(raíz_camiño, repositorio_camiño, 시언어번역기, 시플플번역기, 연결편집기, Arquivo_ferramenta, configuración_Servizo_de_transferencia_intelixente_en_segundo_plano, executar_comando):
    configuración_Servizo_de_transferencia_intelixente_en_segundo_plano = [Configuración_VALOR for Configuración_VALOR in configuración_Servizo_de_transferencia_intelixente_en_segundo_plano if Configuración_VALOR != '-mgeneral-regs-only']
    compilar_camiño = raíz_camiño / 'build'
    출력결과 = compilar_camiño / 'user'
    출력결과.mkdir(exist_ok=True)
    원본자료 = raíz_camiño / 'usuario'
    포직스경로 = repositorio_camiño / 'posix-kor/arm64-native'
    포함경로 = ['-I', 원본자료, '-I', 포직스경로 / '포함', '-I', 출력결과]
    for 번역기, 추가영역, CAMIÑO, Nome in [
            (시언어번역기, [], 원본자료 / 'Executar_2.S', 'start.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'executar_comando.c', 'runtime.o'),
            (시언어번역기, ['-std=c11'], 포직스경로 / 'usuario_ponte.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '파일예제.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / '보호시험.c', 'fault.o'),
            (시언어번역기, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        executar_comando([번역기] + configuración_Servizo_de_transferencia_intelixente_en_segundo_plano + 추가영역 + 포함경로 + ['-Wall', '-Wextra', '-Werror', '-c', CAMIÑO, '-o', 출력결과 / Nome])
    executar_comando([Arquivo_ferramenta, 'rcs', compilar_camiño / 'libposix-kor-user.a', 출력결과 / 'posix.o'])
    for Nome in ('demo', 'fault', 'network', 'vi'):
        executar_comando([연결편집기, '-T', 원본자료 / 'Ligar_deseño.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / (Nome + '.elf'),
             출력결과 / 'start.o', 출력결과 / 'runtime.o', 출력결과 / (Nome + '.o'), compilar_camiño / 'libposix-kor-user.a'])
    자바라이브러리만들기(raíz_camiño, executar_comando)
    # 기존 자체 Java 컴파일러/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(compilar_camiño)) as 작업경로:
        Clase_camiño = Path(작업경로)
        executar_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', Clase_camiño, '-sourcepath', Clase_camiño, '-d', Clase_camiño] +
            [datos_cargo for datos_cargo in sorted((repositorio_camiño / 'os/usuario/자바').glob('*.java')) if datos_cargo.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        executar_comando(['sh', repositorio_camiño / 'compiler/미리번역.sh', '--entry', 'ferramenta_introdución.Executar_2',
             '--profile', 'user', '--heap-words', '1048576', '-o', 출력결과 / 'java-tools.c'] + sorted(Clase_camiño.glob('*.class')))
    압축해제경로 = raíz_camiño / 'vendor/uzlib'
    for CAMIÑO, Nome in [(출력결과 / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'paquete.c', 'jar.o')] + [(압축해제경로 / (Nome + '.c'), Nome + '.o') for Nome in ('tinflate', 'crc32', 'adler32')]:
        executar_comando([시언어번역기] + configuración_Servizo_de_transferencia_intelixente_en_segundo_plano + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + 포함경로 + ['-c', CAMIÑO, '-o', 출력결과 / Nome])
    executar_comando([연결편집기, '-T', 원본자료 / 'Ligar_deseño.ld', '-z', 'max-page-size=4096', '-o', 출력결과 / 'java-tools.elf'] +
        [출력결과 / Nome for Nome in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    crear_PYTHON(raíz_camiño, 시언어번역기, 연결편집기)
    시언어번역기만들기(raíz_camiño, repositorio_camiño, 시언어번역기, 연결편집기, configuración_Servizo_de_transferencia_intelixente_en_segundo_plano, executar_comando)
    유효함 = (출력결과 / 'demo.elf').read_bytes()
    apl_Cabeceira_DESPRAZAMENTO = struct.unpack_from('<Q', 유효함, 32)[0]
    Cabeceira_Lista = [apl_Cabeceira_DESPRAZAMENTO + elemento_CONTAR * 56 for elemento_CONTAR in range(struct.unpack_from('<H', 유효함, 56)[0])]
    적재구획 = [datos_cargo for datos_cargo in Cabeceira_Lista if struct.unpack_from('<I', 유효함, datos_cargo)[0] == 1]
    Texto, datos = 적재구획[:2]
    comando_ENDEREZO = struct.unpack_from('<Q', 유효함, Texto + 16)[0]
    datos_ENDEREZO = struct.unpack_from('<Q', 유효함, datos + 16)[0]
    호출규약 = 유효함.index(b'JKOROS\0')
    시험사례 = [('empty', b''), ('short', 유효함[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', comando_ENDEREZO + 1), ('data-entry', 24, 'Q', datos_ENDEREZO),
               ('outside-file', Texto + 32, 'Q', len(유효함) + 1), ('short-memory', Texto + 40, 'Q', 1),
               ('kernel-address', Texto + 16, 'Q', 0x80000), ('memory-overflow', Texto + 40, 'Q', 2**64 - 1),
               ('writable-code', Texto + 4, 'I', 7), ('missing-abi', 호출규약, 'B', ord('X')),
               ('wrong-abi', 호출규약 + 8, 'I', 2), ('dynamic', Texto, 'I', 2),
               ('unaligned-load', Texto + 16, 'Q', comando_ENDEREZO + 8),
               ('overlap', datos + 16, 'Q', comando_ENDEREZO)]
    for Nome, DESPRAZAMENTO_VALOR, formato_932e03c8, VALOR in 수정사항:
        바뀐자료 = bytearray(유효함); struct.pack_into('<' + formato_932e03c8, 바뀐자료, DESPRAZAMENTO_VALOR, VALOR)
        시험사례.append((Nome, bytes(바뀐자료)))
    탑재덩이들 = [(Nome.replace('-', '_'), 출력결과 / (Nome + '.elf')) for Nome in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for Busca_ÍNDICE, (Nome, carga_datos_60367a51) in enumerate(시험사례):
        CAMIÑO = 출력결과 / ('invalid-{}.elf'.format(Nome)); CAMIÑO.write_bytes(carga_datos_60367a51)
        탑재덩이들.append(('invalid_{}'.format(Busca_ÍNDICE), CAMIÑO))
    ensamblado, Cabeceira_VALOR = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nome, CAMIÑO in 탑재덩이들:
        símbolo_VALOR = 'user_blob_' + Nome
        크기목록[Nome] = CAMIÑO.stat().st_size
        # 생성한 punto_VALOR 경로만 넣어 프로젝트 경로의 공백/Cita 영향을 피한다.
        ensamblado += ['.balign 16', '.global ' + símbolo_VALOR, símbolo_VALOR + ':', '.incbin "{}"'.format(CAMIÑO.relative_to(raíz_camiño))]
        Cabeceira_VALOR.append('extern const unsigned char {}[];'.format(símbolo_VALOR))
    ensamblado.append('.section .note.GNU-stack,"",%progbits')
    Cabeceira_VALOR += ['static const apl 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Cabeceira_VALOR += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Cabeceira_VALOR += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Cabeceira_VALOR += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], 방식) for 방식 in (0, 1)]
    Cabeceira_VALOR += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Cabeceira_VALOR += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Cabeceira_VALOR += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Cabeceira_VALOR += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Cabeceira_VALOR += ['};', 'static const apl 잘못된실행항목들[] = {']
    Cabeceira_VALOR += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(carga_datos_60367a51)) for 순번, (_, carga_datos_60367a51) in enumerate(시험사례)]
    Cabeceira_VALOR += ['};']
    (compilar_camiño / 'programs.S').write_text('\n'.join(ensamblado) + '\n')
    (compilar_camiño / 'programs.h').write_text('\n'.join(Cabeceira_VALOR) + '\n')
    (출력결과 / 'invalid-cases.txt').write_text('\n'.join(Nome for Nome, _ in 시험사례) + '\n')
    executar_comando([시언어번역기] + configuración_Servizo_de_transferencia_intelixente_en_segundo_plano + ['-c', compilar_camiño / 'programs.S', '-o', compilar_camiño / 'programs.o'])
