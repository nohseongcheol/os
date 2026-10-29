#!/usr/bin/env python3
"""libclang dichiarazione·fonti 위치를 수집한다. esterno_VALORE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_fonte
import hashlib
import json
from pathlib import Path

azione_radice = Path(__file__).resolve().parents[1]
implementazione = C_fonte.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class stringa_VALORE(C_fonte.Structure): _fields_ = [('dati',C_fonte.c_void_p),('mostrare_VALORE',C_fonte.c_uint)]
class cursore_VALORE(C_fonte.Structure): _fields_ = [('Kind_VALORE',C_fonte.c_uint),('보조',C_fonte.c_int),('dati',C_fonte.c_void_p*3)]
class posizione(C_fonte.Structure): _fields_ = [('dati',C_fonte.c_void_p*2),('SCARTO_VALORE',C_fonte.c_uint)]
def FUNZIONE_VALORE(Nome, Reso_KR, *argomenti):
    voce_VALORE = getattr(implementazione, Nome); voce_VALORE.restype = Reso_KR; voce_VALORE.argtypes = list(argomenti); return voce_VALORE
get_SMS = FUNZIONE_VALORE('clang_getCString',C_fonte.c_char_p,stringa_VALORE)
release_SMS = FUNZIONE_VALORE('clang_disposeString',None,stringa_VALORE)
def testo(VALORE):
    risultato = (get_SMS(VALORE) or b'').decode('utf-8'); release_SMS(VALORE); return risultato
get_nome = FUNZIONE_VALORE('clang_getCursorSpelling',stringa_VALORE,cursore_VALORE)
get_fonti = FUNZIONE_VALORE('clang_getCursorReferenced',cursore_VALORE,cursore_VALORE)
get_funzione = FUNZIONE_VALORE('clang_getCursorLocation',posizione,cursore_VALORE)
File_funzione = FUNZIONE_VALORE('clang_getFileLocation',None,posizione,C_fonte.POINTER(C_fonte.c_void_p),C_fonte.POINTER(C_fonte.c_uint),C_fonte.POINTER(C_fonte.c_uint),C_fonte.POINTER(C_fonte.c_uint))
File_voce_nome = FUNZIONE_VALORE('clang_getFileName',stringa_VALORE,C_fonte.c_void_p)
UNICI_nome = FUNZIONE_VALORE('clang_getCursorUSR',stringa_VALORE,cursore_VALORE)
connessione_Kind = FUNZIONE_VALORE('clang_getCursorLinkage',C_fonte.c_uint,cursore_VALORE)
방문형 = C_fonte.CFUNCTYPE(C_fonte.c_uint,cursore_VALORE,cursore_VALORE,C_fonte.c_void_p)
방문 = FUNZIONE_VALORE('clang_visitChildren',C_fonte.c_uint,cursore_VALORE,방문형,C_fonte.c_void_p)
generare = FUNZIONE_VALORE('clang_createIndex',C_fonte.c_void_p,C_fonte.c_int,C_fonte.c_int)
Analizza_VALORE = FUNZIONE_VALORE('clang_parseTranslationUnit',C_fonte.c_void_p,C_fonte.c_void_p,C_fonte.c_char_p,C_fonte.POINTER(C_fonte.c_char_p),C_fonte.c_int,C_fonte.c_void_p,C_fonte.c_uint,C_fonte.c_uint)
radice_VALORE = FUNZIONE_VALORE('clang_getTranslationUnitCursor',cursore_VALORE,C_fonte.c_void_p)
esci_app = FUNZIONE_VALORE('clang_disposeTranslationUnit',None,C_fonte.c_void_p)
진단수 = FUNZIONE_VALORE('clang_getNumDiagnostics',C_fonte.c_uint,C_fonte.c_void_p)
진단얻기 = FUNZIONE_VALORE('clang_getDiagnostic',C_fonte.c_void_p,C_fonte.c_void_p,C_fonte.c_uint)
gravità_VALORE = FUNZIONE_VALORE('clang_getDiagnosticSeverity',C_fonte.c_uint,C_fonte.c_void_p)
진단문 = FUNZIONE_VALORE('clang_getDiagnosticSpelling',stringa_VALORE,C_fonte.c_void_p)
진단해제 = FUNZIONE_VALORE('clang_disposeDiagnostic',None,C_fonte.c_void_p)

def funzione_INDICE(voce_VALORE):
    file = C_fonte.c_void_p(); riga_di_ingresso = C_fonte.c_uint(); slot_voce = C_fonte.c_uint(); SCARTO_VALORE = C_fonte.c_uint()
    File_funzione(get_funzione(voce_VALORE),C_fonte.byref(file),C_fonte.byref(riga_di_ingresso),C_fonte.byref(slot_voce),C_fonte.byref(SCARTO_VALORE))
    return (testo(File_voce_nome(file)) if file else '', SCARTO_VALORE.value, riga_di_ingresso.value)

def Esegui_comando():
    CERCA_INDICE = generare(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # compilatore_strumento.c는 nativo dichiarazione 없이 TinyCC esterno_VALORE 단일 TRADUCI_fonte 단위만 포함한다.
    # esterno_VALORE 선언을 nativo 이름으로 세지 않으며, effettivo_dati 빌드에서는 계속 컴파일한다.
    소유파일 = {str(percorso.resolve()) for percorso in azione_radice.rglob('*') if percorso.suffix in ('.c','.h','.cpp','.inc')
              and not set(percorso.relative_to(azione_radice).parts)&{'build','dist','vendor','__pycache__'}
              and percorso.relative_to(azione_radice).as_posix() != 'C_compilatore/compilatore_strumento.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(azione_radice/'spazio_utente'),
          '-I'+str(azione_radice.parents[1]/'posix-kor/arm64-native/dichiarazioni'),'-I'+str(azione_radice/'build'),'-I'+str(azione_radice/'build/user'),
          '-I'+str(azione_radice/'build/remote'),'-I'+str(azione_radice/'vendor/bearssl/inc'),
          '-I'+str(azione_radice/'vendor/bearssl/src'),'-I'+str(azione_radice/'vendor/libassh/src'),
          '-I'+str(azione_radice/'vendor/lwip/src/include'),'-I'+str(azione_radice/'rete_Pila'),
          '-I'+str(azione_radice/'remoto_VALORE'),'-I'+str(azione_radice/'C_compilatore')]
    for percorso in sorted(Path(Nome) for Nome in 소유파일 if Nome.endswith(('.c','.cpp'))):
        argomenti = 공통 + ['-std=c++11' if percorso.suffix=='.cpp' else '-std=c11']
        if 'rete_Pila' in percorso.parts: argomenti += ['-I'+str(azione_radice/'rete_Pila'),'-I'+str(azione_radice/'vendor/lwip/src/include')]
        if 'C_compilatore' in percorso.parts:
            argomenti += ['-I'+str(azione_radice/'C_compilatore'),'-I'+str(azione_radice/'vendor/tinycc'),'-I'+str(azione_radice/'build/ccompiler'),
                    '-isystem',str(azione_radice.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_bridge' in percorso.parts:
            argomenti += ['-I'+str(azione_radice/'PYTHON_bridge'),'-I'+str(azione_radice/'build/micropython-1.24.1'),'-I'+str(azione_radice/'build/python'),'-isystem','/usr/include/newlib']
        if 'remoto_VALORE' in percorso.parts:
            argomenti += ['-isystem', '/usr/include/newlib']
        if 'distribuzione_VALORE' in percorso.parts: argomenti += ['-D__JKOROS__=1']
        if percorso.name=='aggregare.c': argomenti += ['-I'+str(azione_radice/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        gruppo_VALORE = (C_fonte.c_char_p*len(argomenti))(*[voce_VALORE.encode() for voce_VALORE in argomenti])
        unità_di_conversione = Analizza_VALORE(CERCA_INDICE,str(percorso).encode(),gruppo_VALORE,len(argomenti),None,0,1)
        for INDICE in range(진단수(unità_di_conversione)):
            진단 = 진단얻기(unità_di_conversione,INDICE)
            if gravità_VALORE(진단)>=3: 오류들.append((str(percorso.relative_to(azione_radice)),testo(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(voce_VALORE,padre_VALORE,dati):
            file,SCARTO_VALORE,riga_di_ingresso = funzione_INDICE(voce_VALORE)
            if file not in 소유파일: return 2 if voce_VALORE.Kind_VALORE==300 else 1
            낱말 = testo(get_nome(voce_VALORE))
            if not 낱말 or any(ord(carattere_VALORE)>127 for carattere_VALORE in 낱말): return 2
            if voce_VALORE.Kind_VALORE in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNICI_VALORE = testo(UNICI_nome(voce_VALORE)) or file+':'+str(SCARTO_VALORE)
                선언들[UNICI_VALORE] = {'file':file,'SCARTO_VALORE':SCARTO_VALORE,'riga_di_ingresso':riga_di_ingresso,'Kind_VALORE':voce_VALORE.Kind_VALORE,'Nome':낱말,'Connetti':connessione_Kind(voce_VALORE)}
                참조들.append((file,SCARTO_VALORE,낱말,UNICI_VALORE))
            else:
                fonti = get_fonti(voce_VALORE)
                fonti_File,_,_ = funzione_INDICE(fonti)
                if fonti_File in 소유파일:
                    UNICI_VALORE = testo(UNICI_nome(fonti)); 참조들.append((file,SCARTO_VALORE,testo(get_nome(fonti)),UNICI_VALORE))
            return 2
        방문(radice_VALORE(unità_di_conversione),살피기,None)
        esci_app(unità_di_conversione)
    meta_VALORE = azione_radice/'build/한국어화/시언어분석.json'
    meta_VALORE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {file:hashlib.sha256(Path(file).read_bytes()).hexdigest() for file in sorted(소유파일)}
    meta_VALORE.write_text(json.dumps({'dichiarazione':선언들,'fonti':참조들,'errore':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('dichiarazione',len(선언들),'fonti',len(참조들),'errore',len(오류들))
    for errore in 오류들: print(*errore)

if __name__=='__main__': Esegui_comando()
