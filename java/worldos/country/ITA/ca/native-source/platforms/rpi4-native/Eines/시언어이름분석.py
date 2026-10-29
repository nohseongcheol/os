#!/usr/bin/env python3
"""libclang declaració·Referència 위치를 수집한다. extern_VALOR 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_rel = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class cadena_VALOR(씨.Structure): _fields_ = [('dades',씨.c_void_p),('mostrar_VALOR',씨.c_uint)]
class cursor_VALOR(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('dades',씨.c_void_p*3)]
class Posició(씨.Structure): _fields_ = [('dades',씨.c_void_p*2),('DESPLAÇAMENT_VALOR',씨.c_uint)]
def FUNCIÓ_VALOR(Nom, tornar_les_tasques_mesura, *인수):
    introducció_VALOR = getattr(구현, Nom); introducció_VALOR.restype = tornar_les_tasques_mesura; introducció_VALOR.argtypes = list(인수); return introducció_VALOR
obtenir_SMS = FUNCIÓ_VALOR('clang_getCString',씨.c_char_p,cadena_VALOR)
versió_SMS = FUNCIÓ_VALOR('clang_disposeString',None,cadena_VALOR)
def SMS(VALOR):
    RESULTAT = (obtenir_SMS(VALOR) or b'').decode('utf-8'); versió_SMS(VALOR); return RESULTAT
obtenir_nom = FUNCIÓ_VALOR('clang_getCursorSpelling',cadena_VALOR,cursor_VALOR)
obtenir_Referència = FUNCIÓ_VALOR('clang_getCursorReferenced',cursor_VALOR,cursor_VALOR)
obtenir_càrrec = FUNCIÓ_VALOR('clang_getCursorLocation',Posició,cursor_VALOR)
arxiu_càrrec = FUNCIÓ_VALOR('clang_getFileLocation',None,Posició,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
arxiu_introducció_nom = FUNCIÓ_VALOR('clang_getFileName',cadena_VALOR,씨.c_void_p)
ÚNICS_nom = FUNCIÓ_VALOR('clang_getCursorUSR',cadena_VALOR,cursor_VALOR)
연결종류 = FUNCIÓ_VALOR('clang_getCursorLinkage',씨.c_uint,cursor_VALOR)
방문형 = 씨.CFUNCTYPE(씨.c_uint,cursor_VALOR,cursor_VALOR,씨.c_void_p)
방문 = FUNCIÓ_VALOR('clang_visitChildren',씨.c_uint,cursor_VALOR,방문형,씨.c_void_p)
generar = FUNCIÓ_VALOR('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
Anàlisi_VALOR = FUNCIÓ_VALOR('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
rel_VALOR = FUNCIÓ_VALOR('clang_getTranslationUnitCursor',cursor_VALOR,씨.c_void_p)
sortir_programa = FUNCIÓ_VALOR('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCIÓ_VALOR('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCIÓ_VALOR('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
gravetat_VALOR = FUNCIÓ_VALOR('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCIÓ_VALOR('clang_getDiagnosticSpelling',cadena_VALOR,씨.c_void_p)
진단해제 = FUNCIÓ_VALOR('clang_disposeDiagnostic',None,씨.c_void_p)

def càrrec_INDEX(introducció_VALOR):
    Fitxer = 씨.c_void_p(); línia = 씨.c_uint(); 칸 = 씨.c_uint(); DESPLAÇAMENT_VALOR = 씨.c_uint()
    arxiu_càrrec(obtenir_càrrec(introducció_VALOR),씨.byref(Fitxer),씨.byref(línia),씨.byref(칸),씨.byref(DESPLAÇAMENT_VALOR))
    return (SMS(arxiu_introducció_nom(Fitxer)) if Fitxer else '', DESPLAÇAMENT_VALOR.value, línia.value)

def Executa_ordre():
    Cerca_INDEX = generar(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 propi declaració 없이 TinyCC extern_VALOR 단일 TRADUEIX_font 단위만 포함한다.
    # extern_VALOR 선언을 propi 이름으로 세지 않으며, real_dades 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Camí.resolve()) for Camí in Project_rel.rglob('*') if Camí.suffix in ('.c','.h','.cpp','.inc')
              and not set(Camí.relative_to(Project_rel).parts)&{'build','dist','vendor','__pycache__'}
              and Camí.relative_to(Project_rel).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_rel/'usuari'),
          '-I'+str(Project_rel.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_rel/'build'),'-I'+str(Project_rel/'build/user'),
          '-I'+str(Project_rel/'build/remote'),'-I'+str(Project_rel/'vendor/bearssl/inc'),
          '-I'+str(Project_rel/'vendor/bearssl/src'),'-I'+str(Project_rel/'vendor/libassh/src'),
          '-I'+str(Project_rel/'vendor/lwip/src/include'),'-I'+str(Project_rel/'xarxa_Pila'),
          '-I'+str(Project_rel/'remot_VALOR'),'-I'+str(Project_rel/'시언어번역기')]
    for Camí in sorted(Path(Nom) for Nom in 소유파일 if Nom.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Camí.suffix=='.cpp' else '-std=c11']
        if 'xarxa_Pila' in Camí.parts: 인수 += ['-I'+str(Project_rel/'xarxa_Pila'),'-I'+str(Project_rel/'vendor/lwip/src/include')]
        if '시언어번역기' in Camí.parts:
            인수 += ['-I'+str(Project_rel/'시언어번역기'),'-I'+str(Project_rel/'vendor/tinycc'),'-I'+str(Project_rel/'build/ccompiler'),
                    '-isystem',str(Project_rel.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_pont' in Camí.parts:
            인수 += ['-I'+str(Project_rel/'PYTHON_pont'),'-I'+str(Project_rel/'build/micropython-1.24.1'),'-I'+str(Project_rel/'build/python'),'-isystem','/usr/include/newlib']
        if 'remot_VALOR' in Camí.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Camí.parts: 인수 += ['-D__JKOROS__=1']
        if Camí.name=='paquet.c': 인수 += ['-I'+str(Project_rel/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grup_VALOR = (씨.c_char_p*len(인수))(*[introducció_VALOR.encode() for introducció_VALOR in 인수])
        Traducció_lliçó = Anàlisi_VALOR(Cerca_INDEX,str(Camí).encode(),Grup_VALOR,len(인수),None,0,1)
        for INDEX in range(진단수(Traducció_lliçó)):
            진단 = 진단얻기(Traducció_lliçó,INDEX)
            if gravetat_VALOR(진단)>=3: 오류들.append((str(Camí.relative_to(Project_rel)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(introducció_VALOR,부모,dades):
            Fitxer,DESPLAÇAMENT_VALOR,línia = càrrec_INDEX(introducció_VALOR)
            if Fitxer not in 소유파일: return 2 if introducció_VALOR.종류==300 else 1
            낱말 = SMS(obtenir_nom(introducció_VALOR))
            if not 낱말 or any(ord(caràcter_VALOR)>127 for caràcter_VALOR in 낱말): return 2
            if introducció_VALOR.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                ÚNICS_VALOR = SMS(ÚNICS_nom(introducció_VALOR)) or Fitxer+':'+str(DESPLAÇAMENT_VALOR)
                선언들[ÚNICS_VALOR] = {'Fitxer':Fitxer,'DESPLAÇAMENT_VALOR':DESPLAÇAMENT_VALOR,'línia':línia,'종류':introducció_VALOR.종류,'Nom':낱말,'Connecta':연결종류(introducció_VALOR)}
                참조들.append((Fitxer,DESPLAÇAMENT_VALOR,낱말,ÚNICS_VALOR))
            else:
                Referència = obtenir_Referència(introducció_VALOR)
                Referència_arxiu,_,_ = càrrec_INDEX(Referència)
                if Referència_arxiu in 소유파일:
                    ÚNICS_VALOR = SMS(ÚNICS_nom(Referència)); 참조들.append((Fitxer,DESPLAÇAMENT_VALOR,SMS(obtenir_nom(Referència)),ÚNICS_VALOR))
            return 2
        방문(rel_VALOR(Traducció_lliçó),살피기,None)
        sortir_programa(Traducció_lliçó)
    destinació_VALOR = Project_rel/'build/한국어화/시언어분석.json'
    destinació_VALOR.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fitxer:hashlib.sha256(Path(Fitxer).read_bytes()).hexdigest() for Fitxer in sorted(소유파일)}
    destinació_VALOR.write_text(json.dumps({'declaració':선언들,'Referència':참조들,'s_ha_produït_un_error':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('declaració',len(선언들),'Referència',len(참조들),'s_ha_produït_un_error',len(오류들))
    for s_ha_produït_un_error in 오류들: print(*s_ha_produït_un_error)

if __name__=='__main__': Executa_ordre()
