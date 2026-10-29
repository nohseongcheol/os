"""독립된 nativo ABI ELF64와 로더 rejeitar_VALOR testes 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from BLD_PYTHON import Criar_PYTHON
from 자바라이브러리빌드 import 자바라이브러리만들기
from BLD_C_compilador import Criar_C_compilador


def Criar_usuário_ESPAÇO(raiz_caminho, repositório_caminho, C_compilador, 시플플번역기, vinculador_ferramenta, arquivo_ferramenta, Configuração_BITS, Executar_comando):
    Configuração_BITS = [Configurações_VALOR for Configurações_VALOR in Configuração_BITS if Configurações_VALOR != '-mgeneral-regs-only']
    BLD_caminho = raiz_caminho / 'build'
    saída = BLD_caminho / 'user'
    saída.mkdir(exist_ok=True)
    원본자료 = raiz_caminho / 'espaço_do_utilizador'
    포직스경로 = repositório_caminho / 'posix-kor/arm64-native'
    incluir_caminho = ['-I', 원본자료, '-I', 포직스경로 / 'declarações', '-I', saída]
    for compilador_ferramenta, 추가영역, caminho, Nome in [
            (C_compilador, [], 원본자료 / 'iniciar.S', 'start.o'),
            (C_compilador, ['-std=c11'], 원본자료 / 'Executar_comando.c', 'runtime.o'),
            (C_compilador, ['-std=c11'], 포직스경로 / 'usuário_ponte.c', 'posix.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / 'ExemploFicheiro.cpp', 'demo.o'),
            (시플플번역기, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], 원본자료 / '통신예제.cpp', 'network.o'),
            (C_compilador, ['-std=c11'], 원본자료 / 'Proteção_teste.c', 'fault.o'),
            (C_compilador, ['-std=c11'], 원본자료 / 'Editor.c', 'vi.o')]:
        Executar_comando([compilador_ferramenta] + Configuração_BITS + 추가영역 + incluir_caminho + ['-Wall', '-Wextra', '-Werror', '-c', caminho, '-o', saída / Nome])
    Executar_comando([arquivo_ferramenta, 'rcs', BLD_caminho / 'libposix-kor-user.a', saída / 'posix.o'])
    for Nome in ('demo', 'fault', 'network', 'vi'):
        Executar_comando([vinculador_ferramenta, '-T', 원본자료 / 'disposição_de_ligação.ld', '-z', 'max-page-size=4096', '-o', saída / (Nome + '.elf'),
             saída / 'start.o', saída / 'runtime.o', saída / (Nome + '.o'), BLD_caminho / 'libposix-kor-user.a'])
    자바라이브러리만들기(raiz_caminho, Executar_comando)
    # 기존 nativo Java compilador/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(BLD_caminho)) as 작업경로:
        aula_caminho = Path(작업경로)
        Executar_comando(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', aula_caminho, '-sourcepath', aula_caminho, '-d', aula_caminho] +
            [dados_cargo for dados_cargo in sorted((repositório_caminho / 'os/espaço_do_utilizador/자바').glob('*.java')) if dados_cargo.name != '자바가상기계.java'] + sorted((원본자료 / '자바').glob('*.java')))
        Executar_comando(['sh', repositório_caminho / 'compiler/미리번역.sh', '--entry', 'ferramenta_entrada.iniciar',
             '--profile', 'user', '--heap-words', '1048576', '-o', saída / 'java-tools.c'] + sorted(aula_caminho.glob('*.class')))
    압축해제경로 = raiz_caminho / 'vendor/uzlib'
    for caminho, Nome in [(saída / 'java-tools.c', 'java-tools.o'), (원본자료 / '자바연결.c', 'java-link.o'),
                       (원본자료 / 'grupo.c', 'jar.o')] + [(압축해제경로 / (Nome + '.c'), Nome + '.o') for Nome in ('tinflate', 'crc32', 'adler32')]:
        Executar_comando([C_compilador] + Configuração_BITS + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', 압축해제경로] + incluir_caminho + ['-c', caminho, '-o', saída / Nome])
    Executar_comando([vinculador_ferramenta, '-T', 원본자료 / 'disposição_de_ligação.ld', '-z', 'max-page-size=4096', '-o', saída / 'java-tools.elf'] +
        [saída / Nome for Nome in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    Criar_PYTHON(raiz_caminho, C_compilador, vinculador_ferramenta)
    Criar_C_compilador(raiz_caminho, repositório_caminho, C_compilador, vinculador_ferramenta, Configuração_BITS, Executar_comando)
    válido = (saída / 'demo.elf').read_bytes()
    app_Cabeçalho_DESLOC = struct.unpack_from('<Q', válido, 32)[0]
    Cabeçalho_Lista = [app_Cabeçalho_DESLOC + item_CONT_NÚM * 56 for item_CONT_NÚM in range(struct.unpack_from('<H', válido, 56)[0])]
    적재구획 = [dados_cargo for dados_cargo in Cabeçalho_Lista if struct.unpack_from('<I', válido, dados_cargo)[0] == 1]
    texto, dados = 적재구획[:2]
    comando_email = struct.unpack_from('<Q', válido, texto + 16)[0]
    dados_email = struct.unpack_from('<Q', válido, dados + 16)[0]
    Ligar_ABI = válido.index(b'JKOROS\0')
    caso_de_teste = [('empty', b''), ('short', válido[:63])]
    수정사항 = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', comando_email + 1), ('data-entry', 24, 'Q', dados_email),
               ('outside-file', texto + 32, 'Q', len(válido) + 1), ('short-memory', texto + 40, 'Q', 1),
               ('kernel-address', texto + 16, 'Q', 0x80000), ('memory-overflow', texto + 40, 'Q', 2**64 - 1),
               ('writable-code', texto + 4, 'I', 7), ('missing-abi', Ligar_ABI, 'B', ord('X')),
               ('wrong-abi', Ligar_ABI + 8, 'I', 2), ('dynamic', texto, 'I', 2),
               ('unaligned-load', texto + 16, 'Q', comando_email + 8),
               ('overlap', dados + 16, 'Q', comando_email)]
    for Nome, DESLOC_VALOR, formato_932e03c8, VALOR in 수정사항:
        바뀐자료 = bytearray(válido); struct.pack_into('<' + formato_932e03c8, 바뀐자료, DESLOC_VALOR, VALOR)
        caso_de_teste.append((Nome, bytes(바뀐자료)))
    탑재덩이들 = [(Nome.replace('-', '_'), saída / (Nome + '.elf')) for Nome in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for PROC_ÍNDICE, (Nome, carga_dados) in enumerate(caso_de_teste):
        caminho = saída / ('invalid-{}.elf'.format(Nome)); caminho.write_bytes(carga_dados)
        탑재덩이들.append(('invalid_{}'.format(PROC_ÍNDICE), caminho))
    assembly, Cabeçalho_VALOR = ['.section .rodata.user,"a"'], []
    크기목록 = {}
    for Nome, caminho in 탑재덩이들:
        símbolo_VALOR = 'user_blob_' + Nome
        크기목록[Nome] = caminho.stat().st_size
        # 생성한 par_VALOR 경로만 넣어 프로젝트 경로의 공백/Citação 영향을 피한다.
        assembly += ['.balign 16', '.global ' + símbolo_VALOR, símbolo_VALOR + ':', '.incbin "{}"'.format(caminho.relative_to(raiz_caminho))]
        Cabeçalho_VALOR.append('extern const unsigned char {}[];'.format(símbolo_VALOR))
    assembly.append('.section .note.GNU-stack,"",%progbits')
    Cabeçalho_VALOR += ['static const app 실행항목들[] = {', '{user_blob_demo, %d, 0},' % 크기목록['demo']]
    Cabeçalho_VALOR += ['{user_blob_fault, %d, %d},' % (크기목록['fault'], 전달값) for 전달값 in range(8)]
    Cabeçalho_VALOR += ['{user_blob_network, %d, 0},' % 크기목록['network']]
    Cabeçalho_VALOR += ['{user_blob_java_tools, %d, %d},' % (크기목록['java_tools'], método_MODO) for método_MODO in (0, 1)]
    Cabeçalho_VALOR += ['{user_blob_python, %d, 0},' % 크기목록['python'], '{user_blob_vi, %d, 0},' % 크기목록['vi']]
    Cabeçalho_VALOR += ['{user_blob_java_tools, %d, 2},' % 크기목록['java_tools']]
    Cabeçalho_VALOR += ['{user_blob_cc, %d, 0},' % 크기목록['cc']]
    Cabeçalho_VALOR += ['{user_blob_cc, %d, 1},' % 크기목록['cc']]
    Cabeçalho_VALOR += ['};', 'static const app 잘못된실행항목들[] = {']
    Cabeçalho_VALOR += ['{user_blob_invalid_%d, %d, 0},' % (순번, len(carga_dados)) for 순번, (_, carga_dados) in enumerate(caso_de_teste)]
    Cabeçalho_VALOR += ['};']
    (BLD_caminho / 'programs.S').write_text('\n'.join(assembly) + '\n')
    (BLD_caminho / 'programs.h').write_text('\n'.join(Cabeçalho_VALOR) + '\n')
    (saída / 'invalid-cases.txt').write_text('\n'.join(Nome for Nome, _ in caso_de_teste) + '\n')
    Executar_comando([C_compilador] + Configuração_BITS + ['-c', BLD_caminho / 'programs.S', '-o', BLD_caminho / 'programs.o'])
