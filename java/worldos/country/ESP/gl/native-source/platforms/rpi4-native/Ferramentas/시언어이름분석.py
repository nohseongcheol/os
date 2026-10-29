#!/usr/bin/env python3
"""libclang declaración·Material_de_referencia 위치를 수집한다. externo_VALOR 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_raíz = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class cadea_VALOR(씨.Structure): _fields_ = [('datos',씨.c_void_p),('mostrar_VALOR',씨.c_uint)]
class cursor_VALOR(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('datos',씨.c_void_p*3)]
class Posición(씨.Structure): _fields_ = [('datos',씨.c_void_p*2),('DESPRAZAMENTO_VALOR',씨.c_uint)]
def FUNCIÓN_VALOR(Nome, devolver_medida, *Argumentos):
    introdución_VALOR = getattr(구현, Nome); introdución_VALOR.restype = devolver_medida; introdución_VALOR.argtypes = list(Argumentos); return introdución_VALOR
obter_SMS = FUNCIÓN_VALOR('clang_getCString',씨.c_char_p,cadea_VALOR)
liberar_SMS = FUNCIÓN_VALOR('clang_disposeString',None,cadea_VALOR)
def Texto(VALOR):
    RESULTANTE = (obter_SMS(VALOR) or b'').decode('utf-8'); liberar_SMS(VALOR); return RESULTANTE
obter_nome = FUNCIÓN_VALOR('clang_getCursorSpelling',cadea_VALOR,cursor_VALOR)
obter_Material_de_referencia = FUNCIÓN_VALOR('clang_getCursorReferenced',cursor_VALOR,cursor_VALOR)
obter_cargo = FUNCIÓN_VALOR('clang_getCursorLocation',Posición,cursor_VALOR)
Ficheiro_cargo = FUNCIÓN_VALOR('clang_getFileLocation',None,Posición,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
Ficheiro_introdución_nome = FUNCIÓN_VALOR('clang_getFileName',cadea_VALOR,씨.c_void_p)
ÚNICO_nome = FUNCIÓN_VALOR('clang_getCursorUSR',cadea_VALOR,cursor_VALOR)
연결종류 = FUNCIÓN_VALOR('clang_getCursorLinkage',씨.c_uint,cursor_VALOR)
방문형 = 씨.CFUNCTYPE(씨.c_uint,cursor_VALOR,cursor_VALOR,씨.c_void_p)
방문 = FUNCIÓN_VALOR('clang_visitChildren',씨.c_uint,cursor_VALOR,방문형,씨.c_void_p)
xerar = FUNCIÓN_VALOR('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
Análise_VALOR = FUNCIÓN_VALOR('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
raíz_VALOR = FUNCIÓN_VALOR('clang_getTranslationUnitCursor',cursor_VALOR,씨.c_void_p)
saír_apl_55b3a1cd = FUNCIÓN_VALOR('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCIÓN_VALOR('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCIÓN_VALOR('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
gravidade_VALOR = FUNCIÓN_VALOR('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCIÓN_VALOR('clang_getDiagnosticSpelling',cadea_VALOR,씨.c_void_p)
진단해제 = FUNCIÓN_VALOR('clang_disposeDiagnostic',None,씨.c_void_p)

def cargo_ÍNDICE(introdución_VALOR):
    Ficheiro = 씨.c_void_p(); Liña = 씨.c_uint(); 칸 = 씨.c_uint(); DESPRAZAMENTO_VALOR = 씨.c_uint()
    Ficheiro_cargo(obter_cargo(introdución_VALOR),씨.byref(Ficheiro),씨.byref(Liña),씨.byref(칸),씨.byref(DESPRAZAMENTO_VALOR))
    return (Texto(Ficheiro_introdución_nome(Ficheiro)) if Ficheiro else '', DESPRAZAMENTO_VALOR.value, Liña.value)

def executar_comando():
    Busca_ÍNDICE = xerar(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 declaración 없이 TinyCC externo_VALOR 단일 TRADUCIR_fonte 단위만 포함한다.
    # externo_VALOR 선언을 자체 이름으로 세지 않으며, real_datos 빌드에서는 계속 컴파일한다.
    소유파일 = {str(CAMIÑO.resolve()) for CAMIÑO in Project_raíz.rglob('*') if CAMIÑO.suffix in ('.c','.h','.cpp','.inc')
              and not set(CAMIÑO.relative_to(Project_raíz).parts)&{'build','dist','vendor','__pycache__'}
              and CAMIÑO.relative_to(Project_raíz).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_raíz/'usuario'),
          '-I'+str(Project_raíz.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_raíz/'build'),'-I'+str(Project_raíz/'build/user'),
          '-I'+str(Project_raíz/'build/remote'),'-I'+str(Project_raíz/'vendor/bearssl/inc'),
          '-I'+str(Project_raíz/'vendor/bearssl/src'),'-I'+str(Project_raíz/'vendor/libassh/src'),
          '-I'+str(Project_raíz/'vendor/lwip/src/include'),'-I'+str(Project_raíz/'Rede_Montón'),
          '-I'+str(Project_raíz/'remoto_VALOR'),'-I'+str(Project_raíz/'시언어번역기')]
    for CAMIÑO in sorted(Path(Nome) for Nome in 소유파일 if Nome.endswith(('.c','.cpp'))):
        Argumentos = 공통 + ['-std=c++11' if CAMIÑO.suffix=='.cpp' else '-std=c11']
        if 'Rede_Montón' in CAMIÑO.parts: Argumentos += ['-I'+str(Project_raíz/'Rede_Montón'),'-I'+str(Project_raíz/'vendor/lwip/src/include')]
        if '시언어번역기' in CAMIÑO.parts:
            Argumentos += ['-I'+str(Project_raíz/'시언어번역기'),'-I'+str(Project_raíz/'vendor/tinycc'),'-I'+str(Project_raíz/'build/ccompiler'),
                    '-isystem',str(Project_raíz.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_ponte' in CAMIÑO.parts:
            Argumentos += ['-I'+str(Project_raíz/'PYTHON_ponte'),'-I'+str(Project_raíz/'build/micropython-1.24.1'),'-I'+str(Project_raíz/'build/python'),'-isystem','/usr/include/newlib']
        if 'remoto_VALOR' in CAMIÑO.parts:
            Argumentos += ['-isystem', '/usr/include/newlib']
        if '배포' in CAMIÑO.parts: Argumentos += ['-D__JKOROS__=1']
        if CAMIÑO.name=='paquete.c': Argumentos += ['-I'+str(Project_raíz/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupo_VALOR = (씨.c_char_p*len(Argumentos))(*[introdución_VALOR.encode() for introdución_VALOR in Argumentos])
        Tradución_lección = Análise_VALOR(Busca_ÍNDICE,str(CAMIÑO).encode(),Grupo_VALOR,len(Argumentos),None,0,1)
        for ÍNDICE in range(진단수(Tradución_lección)):
            진단 = 진단얻기(Tradución_lección,ÍNDICE)
            if gravidade_VALOR(진단)>=3: 오류들.append((str(CAMIÑO.relative_to(Project_raíz)),Texto(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(introdución_VALOR,부모,datos):
            Ficheiro,DESPRAZAMENTO_VALOR,Liña = cargo_ÍNDICE(introdución_VALOR)
            if Ficheiro not in 소유파일: return 2 if introdución_VALOR.종류==300 else 1
            낱말 = Texto(obter_nome(introdución_VALOR))
            if not 낱말 or any(ord(carácter_VALOR)>127 for carácter_VALOR in 낱말): return 2
            if introdución_VALOR.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                ÚNICO_VALOR = Texto(ÚNICO_nome(introdución_VALOR)) or Ficheiro+':'+str(DESPRAZAMENTO_VALOR)
                선언들[ÚNICO_VALOR] = {'Ficheiro':Ficheiro,'DESPRAZAMENTO_VALOR':DESPRAZAMENTO_VALOR,'Liña':Liña,'종류':introdución_VALOR.종류,'Nome':낱말,'Conectar':연결종류(introdución_VALOR)}
                참조들.append((Ficheiro,DESPRAZAMENTO_VALOR,낱말,ÚNICO_VALOR))
            else:
                Material_de_referencia = obter_Material_de_referencia(introdución_VALOR)
                Material_de_referencia_Ficheiro,_,_ = cargo_ÍNDICE(Material_de_referencia)
                if Material_de_referencia_Ficheiro in 소유파일:
                    ÚNICO_VALOR = Texto(ÚNICO_nome(Material_de_referencia)); 참조들.append((Ficheiro,DESPRAZAMENTO_VALOR,Texto(obter_nome(Material_de_referencia)),ÚNICO_VALOR))
            return 2
        방문(raíz_VALOR(Tradución_lección),살피기,None)
        saír_apl_55b3a1cd(Tradución_lección)
    destino_VALOR = Project_raíz/'build/한국어화/시언어분석.json'
    destino_VALOR.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Ficheiro:hashlib.sha256(Path(Ficheiro).read_bytes()).hexdigest() for Ficheiro in sorted(소유파일)}
    destino_VALOR.write_text(json.dumps({'declaración':선언들,'Material_de_referencia':참조들,'ERRO':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('declaración',len(선언들),'Material_de_referencia',len(참조들),'ERRO',len(오류들))
    for ERRO in 오류들: print(*ERRO)

if __name__=='__main__': executar_comando()
