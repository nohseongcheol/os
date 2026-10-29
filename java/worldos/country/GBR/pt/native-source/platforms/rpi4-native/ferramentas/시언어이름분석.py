#!/usr/bin/env python3
"""libclang declaração·Referência 위치를 수집한다. externo_VALOR 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_fonte
import hashlib
import json
from pathlib import Path

ação_raiz = Path(__file__).resolve().parents[1]
implementação = C_fonte.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class cadeia_VALOR(C_fonte.Structure): _fields_ = [('dados',C_fonte.c_void_p),('mostrar_VALOR',C_fonte.c_uint)]
class cursor_VALOR(C_fonte.Structure): _fields_ = [('Tipo_VALOR',C_fonte.c_uint),('보조',C_fonte.c_int),('dados',C_fonte.c_void_p*3)]
class posição(C_fonte.Structure): _fields_ = [('dados',C_fonte.c_void_p*2),('DESLOC_VALOR',C_fonte.c_uint)]
def FUNÇÃO_VALOR(Nome, devolver_RC, *argumentos):
    entrada_VALOR_962f286b = getattr(implementação, Nome); entrada_VALOR_962f286b.restype = devolver_RC; entrada_VALOR_962f286b.argtypes = list(argumentos); return entrada_VALOR_962f286b
get_SMS = FUNÇÃO_VALOR('clang_getCString',C_fonte.c_char_p,cadeia_VALOR)
lançar_SMS = FUNÇÃO_VALOR('clang_disposeString',None,cadeia_VALOR)
def texto(VALOR):
    resultado = (get_SMS(VALOR) or b'').decode('utf-8'); lançar_SMS(VALOR); return resultado
get_nome = FUNÇÃO_VALOR('clang_getCursorSpelling',cadeia_VALOR,cursor_VALOR)
get_Referência = FUNÇÃO_VALOR('clang_getCursorReferenced',cursor_VALOR,cursor_VALOR)
get_cargo = FUNÇÃO_VALOR('clang_getCursorLocation',posição,cursor_VALOR)
Arquivo_cargo_2aa21a9a = FUNÇÃO_VALOR('clang_getFileLocation',None,posição,C_fonte.POINTER(C_fonte.c_void_p),C_fonte.POINTER(C_fonte.c_uint),C_fonte.POINTER(C_fonte.c_uint),C_fonte.POINTER(C_fonte.c_uint))
Arquivo_entrada_nome = FUNÇÃO_VALOR('clang_getFileName',cadeia_VALOR,C_fonte.c_void_p)
ÚNICO_nome = FUNÇÃO_VALOR('clang_getCursorUSR',cadeia_VALOR,cursor_VALOR)
conexão_Tipo = FUNÇÃO_VALOR('clang_getCursorLinkage',C_fonte.c_uint,cursor_VALOR)
방문형 = C_fonte.CFUNCTYPE(C_fonte.c_uint,cursor_VALOR,cursor_VALOR,C_fonte.c_void_p)
방문 = FUNÇÃO_VALOR('clang_visitChildren',C_fonte.c_uint,cursor_VALOR,방문형,C_fonte.c_void_p)
gerar = FUNÇÃO_VALOR('clang_createIndex',C_fonte.c_void_p,C_fonte.c_int,C_fonte.c_int)
Analisar_VALOR = FUNÇÃO_VALOR('clang_parseTranslationUnit',C_fonte.c_void_p,C_fonte.c_void_p,C_fonte.c_char_p,C_fonte.POINTER(C_fonte.c_char_p),C_fonte.c_int,C_fonte.c_void_p,C_fonte.c_uint,C_fonte.c_uint)
raiz_VALOR = FUNÇÃO_VALOR('clang_getTranslationUnitCursor',cursor_VALOR,C_fonte.c_void_p)
encerrar_app = FUNÇÃO_VALOR('clang_disposeTranslationUnit',None,C_fonte.c_void_p)
진단수 = FUNÇÃO_VALOR('clang_getNumDiagnostics',C_fonte.c_uint,C_fonte.c_void_p)
진단얻기 = FUNÇÃO_VALOR('clang_getDiagnostic',C_fonte.c_void_p,C_fonte.c_void_p,C_fonte.c_uint)
gravidade_VALOR = FUNÇÃO_VALOR('clang_getDiagnosticSeverity',C_fonte.c_uint,C_fonte.c_void_p)
진단문 = FUNÇÃO_VALOR('clang_getDiagnosticSpelling',cadeia_VALOR,C_fonte.c_void_p)
진단해제 = FUNÇÃO_VALOR('clang_disposeDiagnostic',None,C_fonte.c_void_p)

def cargo_ÍNDICE(entrada_VALOR_962f286b):
    ficheiro = C_fonte.c_void_p(); linha_de_entrada = C_fonte.c_uint(); slot_entrada = C_fonte.c_uint(); DESLOC_VALOR = C_fonte.c_uint()
    Arquivo_cargo_2aa21a9a(get_cargo(entrada_VALOR_962f286b),C_fonte.byref(ficheiro),C_fonte.byref(linha_de_entrada),C_fonte.byref(slot_entrada),C_fonte.byref(DESLOC_VALOR))
    return (texto(Arquivo_entrada_nome(ficheiro)) if ficheiro else '', DESLOC_VALOR.value, linha_de_entrada.value)

def Executar_comando():
    PROC_ÍNDICE = gerar(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # compilador_ferramenta.c는 nativo declaração 없이 TinyCC externo_VALOR 단일 mover_fonte 단위만 포함한다.
    # externo_VALOR 선언을 nativo 이름으로 세지 않으며, real_dados 빌드에서는 계속 컴파일한다.
    소유파일 = {str(caminho.resolve()) for caminho in ação_raiz.rglob('*') if caminho.suffix in ('.c','.h','.cpp','.inc')
              and not set(caminho.relative_to(ação_raiz).parts)&{'build','dist','vendor','__pycache__'}
              and caminho.relative_to(ação_raiz).as_posix() != 'C_compilador/compilador_ferramenta.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(ação_raiz/'espaço_do_utilizador'),
          '-I'+str(ação_raiz.parents[1]/'posix-kor/arm64-native/declarações'),'-I'+str(ação_raiz/'build'),'-I'+str(ação_raiz/'build/user'),
          '-I'+str(ação_raiz/'build/remote'),'-I'+str(ação_raiz/'vendor/bearssl/inc'),
          '-I'+str(ação_raiz/'vendor/bearssl/src'),'-I'+str(ação_raiz/'vendor/libassh/src'),
          '-I'+str(ação_raiz/'vendor/lwip/src/include'),'-I'+str(ação_raiz/'rede_pilha'),
          '-I'+str(ação_raiz/'remoto_VALOR'),'-I'+str(ação_raiz/'C_compilador')]
    for caminho in sorted(Path(Nome) for Nome in 소유파일 if Nome.endswith(('.c','.cpp'))):
        argumentos = 공통 + ['-std=c++11' if caminho.suffix=='.cpp' else '-std=c11']
        if 'rede_pilha' in caminho.parts: argumentos += ['-I'+str(ação_raiz/'rede_pilha'),'-I'+str(ação_raiz/'vendor/lwip/src/include')]
        if 'C_compilador' in caminho.parts:
            argumentos += ['-I'+str(ação_raiz/'C_compilador'),'-I'+str(ação_raiz/'vendor/tinycc'),'-I'+str(ação_raiz/'build/ccompiler'),
                    '-isystem',str(ação_raiz.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_ponte' in caminho.parts:
            argumentos += ['-I'+str(ação_raiz/'PYTHON_ponte'),'-I'+str(ação_raiz/'build/micropython-1.24.1'),'-I'+str(ação_raiz/'build/python'),'-isystem','/usr/include/newlib']
        if 'remoto_VALOR' in caminho.parts:
            argumentos += ['-isystem', '/usr/include/newlib']
        if 'distribuição_VALOR' in caminho.parts: argumentos += ['-D__JKOROS__=1']
        if caminho.name=='grupo.c': argumentos += ['-I'+str(ação_raiz/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupo_VALOR = (C_fonte.c_char_p*len(argumentos))(*[entrada_VALOR_962f286b.encode() for entrada_VALOR_962f286b in argumentos])
        unidade_de_tradução = Analisar_VALOR(PROC_ÍNDICE,str(caminho).encode(),Grupo_VALOR,len(argumentos),None,0,1)
        for ÍNDICE in range(진단수(unidade_de_tradução)):
            진단 = 진단얻기(unidade_de_tradução,ÍNDICE)
            if gravidade_VALOR(진단)>=3: 오류들.append((str(caminho.relative_to(ação_raiz)),texto(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(entrada_VALOR_962f286b,pai_VALOR,dados):
            ficheiro,DESLOC_VALOR,linha_de_entrada = cargo_ÍNDICE(entrada_VALOR_962f286b)
            if ficheiro not in 소유파일: return 2 if entrada_VALOR_962f286b.Tipo_VALOR==300 else 1
            낱말 = texto(get_nome(entrada_VALOR_962f286b))
            if not 낱말 or any(ord(caractere_VALOR)>127 for caractere_VALOR in 낱말): return 2
            if entrada_VALOR_962f286b.Tipo_VALOR in (2,3,4,5,6,7,8,9,10,20,21,501):
                ÚNICO_VALOR = texto(ÚNICO_nome(entrada_VALOR_962f286b)) or ficheiro+':'+str(DESLOC_VALOR)
                선언들[ÚNICO_VALOR] = {'ficheiro':ficheiro,'DESLOC_VALOR':DESLOC_VALOR,'linha_de_entrada':linha_de_entrada,'Tipo_VALOR':entrada_VALOR_962f286b.Tipo_VALOR,'Nome':낱말,'Ligar':conexão_Tipo(entrada_VALOR_962f286b)}
                참조들.append((ficheiro,DESLOC_VALOR,낱말,ÚNICO_VALOR))
            else:
                Referência = get_Referência(entrada_VALOR_962f286b)
                Referência_Arquivo,_,_ = cargo_ÍNDICE(Referência)
                if Referência_Arquivo in 소유파일:
                    ÚNICO_VALOR = texto(ÚNICO_nome(Referência)); 참조들.append((ficheiro,DESLOC_VALOR,texto(get_nome(Referência)),ÚNICO_VALOR))
            return 2
        방문(raiz_VALOR(unidade_de_tradução),살피기,None)
        encerrar_app(unidade_de_tradução)
    destino_VALOR = ação_raiz/'build/한국어화/시언어분석.json'
    destino_VALOR.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ficheiro:hashlib.sha256(Path(ficheiro).read_bytes()).hexdigest() for ficheiro in sorted(소유파일)}
    destino_VALOR.write_text(json.dumps({'declaração':선언들,'Referência':참조들,'erro':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('declaração',len(선언들),'Referência',len(참조들),'erro',len(오류들))
    for erro in 오류들: print(*erro)

if __name__=='__main__': Executar_comando()
