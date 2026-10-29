#!/usr/bin/env python3
"""libclang Deklarationen·verweis 위치를 수집한다. externWert 헤더의 멤버는 변환하지 않는다."""
import ctypes as cQuelltext
import hashlib
import json
from pathlib import Path

projektWurzel = Path(__file__).resolve().parents[1]
umsetzung = cQuelltext.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class Zeichenkette(cQuelltext.Structure): _fields_ = [('Daten',cQuelltext.c_void_p),('wertAnzeigen',cQuelltext.c_uint)]
class mauszeigerWert(cQuelltext.Structure): _fields_ = [('artWert',cQuelltext.c_uint),('hilfsWert',cQuelltext.c_int),('Daten',cQuelltext.c_void_p*3)]
class position(cQuelltext.Structure): _fields_ = [('Daten',cQuelltext.c_void_p*2),('versatzwertWert',cQuelltext.c_uint)]
def Funktion(Name, zurückkehrenErgebnis, *argumente):
    eintragWert = getattr(umsetzung, Name); eintragWert.restype = zurückkehrenErgebnis; eintragWert.argtypes = list(argumente); return eintragWert
textHolen = Funktion('clang_getCString',cQuelltext.c_char_p,Zeichenkette)
textFreigeben = Funktion('clang_disposeString',None,Zeichenkette)
def Text(Wert):
    ergebnis = (textHolen(Wert) or b'').decode('utf-8'); textFreigeben(Wert); return ergebnis
nameHolen = Funktion('clang_getCursorSpelling',Zeichenkette,mauszeigerWert)
verweisHolen = Funktion('clang_getCursorReferenced',mauszeigerWert,mauszeigerWert)
positionHolen = Funktion('clang_getCursorLocation',position,mauszeigerWert)
dateiPosition = Funktion('clang_getFileLocation',None,position,cQuelltext.POINTER(cQuelltext.c_void_p),cQuelltext.POINTER(cQuelltext.c_uint),cQuelltext.POINTER(cQuelltext.c_uint),cQuelltext.POINTER(cQuelltext.c_uint))
dateiEintragName = Funktion('clang_getFileName',Zeichenkette,cQuelltext.c_void_p)
eindeutigName = Funktion('clang_getCursorUSR',Zeichenkette,mauszeigerWert)
verbindungArt = Funktion('clang_getCursorLinkage',cQuelltext.c_uint,mauszeigerWert)
besuchtTyp = cQuelltext.CFUNCTYPE(cQuelltext.c_uint,mauszeigerWert,mauszeigerWert,cQuelltext.c_void_p)
wertBesuchen = Funktion('clang_visitChildren',cQuelltext.c_uint,mauszeigerWert,besuchtTyp,cQuelltext.c_void_p)
generieren = Funktion('clang_createIndex',cQuelltext.c_void_p,cQuelltext.c_int,cQuelltext.c_int)
wertUntersuchenWert = Funktion('clang_parseTranslationUnit',cQuelltext.c_void_p,cQuelltext.c_void_p,cQuelltext.c_char_p,cQuelltext.POINTER(cQuelltext.c_char_p),cQuelltext.c_int,cQuelltext.c_void_p,cQuelltext.c_uint,cQuelltext.c_uint)
wurzelWert = Funktion('clang_getTranslationUnitCursor',mauszeigerWert,cQuelltext.c_void_p)
aufhörenProgramm = Funktion('clang_disposeTranslationUnit',None,cQuelltext.c_void_p)
diagnoseAnzahl = Funktion('clang_getNumDiagnostics',cQuelltext.c_uint,cQuelltext.c_void_p)
diagnoseHolen = Funktion('clang_getDiagnostic',cQuelltext.c_void_p,cQuelltext.c_void_p,cQuelltext.c_uint)
schweregradWert = Funktion('clang_getDiagnosticSeverity',cQuelltext.c_uint,cQuelltext.c_void_p)
diagnoseNachricht = Funktion('clang_getDiagnosticSpelling',Zeichenkette,cQuelltext.c_void_p)
diagnoseFreigeben = Funktion('clang_disposeDiagnostic',None,cQuelltext.c_void_p)

def positionIndex(eintragWert):
    Datei = cQuelltext.c_void_p(); zeile = cQuelltext.c_uint(); platzEintrag = cQuelltext.c_uint(); versatzwertWert = cQuelltext.c_uint()
    dateiPosition(positionHolen(eintragWert),cQuelltext.byref(Datei),cQuelltext.byref(zeile),cQuelltext.byref(platzEintrag),cQuelltext.byref(versatzwertWert))
    return (Text(dateiEintragName(Datei)) if Datei else '', versatzwertWert.value, zeile.value)

def befehlAusführen():
    nachschlagenIndex = generieren(0,0); deklarationenListe = {}; verweiseListe = []; fehlerliste = []
    # übersetzerWerkzeug.c는 eigen Deklarationen 없이 TinyCC externWert 단일 quelltextÜbersetzenText 단위만 포함한다.
    # externWert 선언을 eigen 이름으로 세지 않으며, tatsächlichDaten 빌드에서는 fortsetzenVerarbeitung 컴파일한다.
    eigenständigDatei = {str(pfad.resolve()) for pfad in projektWurzel.rglob('*') if pfad.suffix in ('.c','.h','.cpp','.inc')
              and not set(pfad.relative_to(projektWurzel).parts)&{'build','dist','vendor','__pycache__'}
              and pfad.relative_to(projektWurzel).as_posix() != 'CÜbersetzer/übersetzerWerkzeug.c'}
    gemeinsamWert = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(projektWurzel/'Benutzer'),
          '-I'+str(projektWurzel.parents[1]/'posix-kor/arm64-native/Kopfdateien'),'-I'+str(projektWurzel/'build'),'-I'+str(projektWurzel/'build/user'),
          '-I'+str(projektWurzel/'build/remote'),'-I'+str(projektWurzel/'vendor/bearssl/inc'),
          '-I'+str(projektWurzel/'vendor/bearssl/src'),'-I'+str(projektWurzel/'vendor/libassh/src'),
          '-I'+str(projektWurzel/'vendor/lwip/src/include'),'-I'+str(projektWurzel/'Netzwerkstapel'),
          '-I'+str(projektWurzel/'entferntWert'),'-I'+str(projektWurzel/'CÜbersetzer')]
    for pfad in sorted(Path(Name) for Name in eigenständigDatei if Name.endswith(('.c','.cpp'))):
        argumente = gemeinsamWert + ['-std=c++11' if pfad.suffix=='.cpp' else '-std=c11']
        if 'Netzwerkstapel' in pfad.parts: argumente += ['-I'+str(projektWurzel/'Netzwerkstapel'),'-I'+str(projektWurzel/'vendor/lwip/src/include')]
        if 'CÜbersetzer' in pfad.parts:
            argumente += ['-I'+str(projektWurzel/'CÜbersetzer'),'-I'+str(projektWurzel/'vendor/tinycc'),'-I'+str(projektWurzel/'build/ccompiler'),
                    '-isystem',str(projektWurzel.parent/'rpi4/build/rootfs/usr/include')]
        if 'pythonBrücke' in pfad.parts:
            argumente += ['-I'+str(projektWurzel/'pythonBrücke'),'-I'+str(projektWurzel/'build/micropython-1.24.1'),'-I'+str(projektWurzel/'build/python'),'-isystem','/usr/include/newlib']
        if 'entferntWert' in pfad.parts:
            argumente += ['-isystem', '/usr/include/newlib']
        if 'verteilungWert' in pfad.parts: argumente += ['-D__JKOROS__=1']
        if pfad.name=='Paket.c': argumente += ['-I'+str(projektWurzel/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        gruppeWert = (cQuelltext.c_char_p*len(argumente))(*[eintragWert.encode() for eintragWert in argumente])
        übersetzungEinheit = wertUntersuchenWert(nachschlagenIndex,str(pfad).encode(),gruppeWert,len(argumente),None,0,1)
        for Nummer in range(diagnoseAnzahl(übersetzungEinheit)):
            diagnoseWert = diagnoseHolen(übersetzungEinheit,Nummer)
            if schweregradWert(diagnoseWert)>=3: fehlerliste.append((str(pfad.relative_to(projektWurzel)),Text(diagnoseNachricht(diagnoseWert))))
            diagnoseFreigeben(diagnoseWert)
        @besuchtTyp
        def wertUntersuchen(eintragWert,elternknotenWert,Daten):
            Datei,versatzwertWert,zeile = positionIndex(eintragWert)
            if Datei not in eigenständigDatei: return 2 if eintragWert.artWert==300 else 1
            lexikalischMaschinenwort = Text(nameHolen(eintragWert))
            if not lexikalischMaschinenwort or any(ord(zeichenWert)>127 for zeichenWert in lexikalischMaschinenwort): return 2
            if eintragWert.artWert in (2,3,4,5,6,7,8,9,10,20,21,501):
                eindeutigWert = Text(eindeutigName(eintragWert)) or Datei+':'+str(versatzwertWert)
                deklarationenListe[eindeutigWert] = {'Datei':Datei,'versatzwertWert':versatzwertWert,'zeile':zeile,'artWert':eintragWert.artWert,'Name':lexikalischMaschinenwort,'verbinden':verbindungArt(eintragWert)}
                verweiseListe.append((Datei,versatzwertWert,lexikalischMaschinenwort,eindeutigWert))
            else:
                verweis = verweisHolen(eintragWert)
                verweisDatei,_,_ = positionIndex(verweis)
                if verweisDatei in eigenständigDatei:
                    eindeutigWert = Text(eindeutigName(verweis)); verweiseListe.append((Datei,versatzwertWert,Text(nameHolen(verweis)),eindeutigWert))
            return 2
        wertBesuchen(wurzelWert(übersetzungEinheit),wertUntersuchen,None)
        aufhörenProgramm(übersetzungEinheit)
    zielWert = projektWurzel/'build/한국어화/시언어분석.json'
    zielWert.parent.mkdir(parents=True, exist_ok=True)
    prüfsummenListeListe = {Datei:hashlib.sha256(Path(Datei).read_bytes()).hexdigest() for Datei in sorted(eigenständigDatei)}
    zielWert.write_text(json.dumps({'Deklarationen':deklarationenListe,'verweis':verweiseListe,'fehler':fehlerliste,'원문해시':prüfsummenListeListe},ensure_ascii=False,indent=2)+'\n')
    print('Deklarationen',len(deklarationenListe),'verweis',len(verweiseListe),'fehler',len(fehlerliste))
    for fehler in fehlerliste: print(*fehler)

if __name__=='__main__': befehlAusführen()
