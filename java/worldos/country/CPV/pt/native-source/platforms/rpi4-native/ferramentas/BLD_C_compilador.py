"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Criar_C_compilador(raiz_caminho, repositório_caminho, C_compilador, vinculador_ferramenta, Configuração_BITS, Executar_comando):
    RC_dados = raiz_caminho / 'build/ccompiler'; RC_dados.mkdir(exist_ok=True)
    원본자료 = raiz_caminho / 'C_compilador'
    upstream = raiz_caminho / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    kit_de_desenvolvimento = raiz_caminho / 'vendor/sdk'
    if not (kit_de_desenvolvimento/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((kit_de_desenvolvimento/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    Configuração_BITS = [Configurações_VALOR for Configurações_VALOR in Configuração_BITS if Configurações_VALOR != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstream, '-I', raiz_caminho/'espaço_do_utilizador', '-I', RC_dados, '-isystem', kit_de_desenvolvimento/'usr/include']
    Executar_comando([C_compilador]+Configuração_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'inicialização_Suporte.c','-o',RC_dados/'crt.o'])
    Executar_comando([C_compilador]+Configuração_BITS+['-I',repositório_caminho/'posix-kor/arm64-native/declarações']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',RC_dados/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+dados_cargo.name,dados_cargo) for dados_cargo in sorted((repositório_caminho/'posix-kor/arm64-native/declarações').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dados_cargo.name,dados_cargo) for dados_cargo in sorted((upstream/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dados_cargo.name,dados_cargo) for dados_cargo in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',raiz_caminho/'build/user/start.o'),('/sdk/lib/crt.o',RC_dados/'crt.o'),('/sdk/lib/aot-runtime.o',RC_dados/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',raiz_caminho/'build/libposix-kor-user.a')]
    Cabeçalho_VALOR=['typedef struct { const char *Nome; const unsigned char *dados; unsigned Tamanho; } compilador_recurso;']
    for 순번,(_,caminho) in enumerate(탑재자료):
        Cabeçalho_VALOR.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in caminho.read_bytes())))
    Cabeçalho_VALOR.append('static const compilador_recurso compilador_Recursos[] = {')
    for 순번,(Nome,caminho) in enumerate(탑재자료): Cabeçalho_VALOR.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nome,ensure_ascii=False),순번,caminho.stat().st_size))
    Cabeçalho_VALOR.append('};');(RC_dados/'resources.h').write_text('\n'.join(Cabeçalho_VALOR)+'\n',encoding='utf-8')
    destino_Arquivos=[]
    for Nome in ('compilador_ferramenta.c','SuporteExecução.c','iniciar.c','미리번역.c','devolver_ponte.S'):
        arquivo_de_destino=RC_dados/(Path(Nome).stem+'.o');destino_Arquivos.append(arquivo_de_destino)
        Executar_comando([C_compilador]+Configuração_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nome,'-o',arquivo_de_destino])
    executável=raiz_caminho/'build/user/cc.elf'
    Executar_comando([vinculador_ferramenta,'--gc-sections','-T',raiz_caminho/'espaço_do_utilizador/disposição_de_ligação.ld','-z','max-page-size=4096','-o',executável,
         raiz_caminho/'build/user/start.o',raiz_caminho/'build/user/runtime.o']+destino_Arquivos+
         [raiz_caminho/'build/user'/Nome for Nome in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
