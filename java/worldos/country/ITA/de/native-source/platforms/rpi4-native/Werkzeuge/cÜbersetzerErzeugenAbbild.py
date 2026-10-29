"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def cÜbersetzerErstellen(wurzelPfad, ablagePfad, CÜbersetzer, binderWerkzeug, konfigurationBitliste, befehlAusführen):
    ergebnisDaten = wurzelPfad / 'build/ccompiler'; ergebnisDaten.mkdir(exist_ok=True)
    ursprünglichDaten = wurzelPfad / 'CÜbersetzer'
    vorgelagert = wurzelPfad / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    entwicklungWerkzeugsatz = wurzelPfad / 'vendor/sdk'
    if not (entwicklungWerkzeugsatz/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    einbauten = sorted((entwicklungWerkzeugsatz/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not einbauten: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurationBitliste = [einstellungenWert for einstellungenWert in konfigurationBitliste if einstellungenWert != '-mgeneral-regs-only']
    einschlüsse = ['-I', ursprünglichDaten, '-I', vorgelagert, '-I', wurzelPfad/'Benutzer', '-I', ergebnisDaten, '-isystem', entwicklungWerkzeugsatz/'usr/include']
    befehlAusführen([CÜbersetzer]+konfigurationBitliste+['-ffunction-sections','-fdata-sections']+einschlüsse+['-c',ursprünglichDaten/'anlaufUnterstützung.c','-o',ergebnisDaten/'crt.o'])
    befehlAusführen([CÜbersetzer]+konfigurationBitliste+['-I',ablagePfad/'posix-kor/arm64-native/Kopfdateien']+einschlüsse+['-c',ursprünglichDaten/'vorabübersetzungLaufzeit.c','-o',ergebnisDaten/'aot-runtime.o'])
    bestandteile = [('/sdk/include/'+datenPosition.name,datenPosition) for datenPosition in sorted((ablagePfad/'posix-kor/arm64-native/Kopfdateien').glob('*.h'))]
    bestandteile += [('/sdk/include/'+datenPosition.name,datenPosition) for datenPosition in sorted((vorgelagert/'include').glob('*.h'))]
    bestandteile += [('/sdk/include/'+datenPosition.name,datenPosition) for datenPosition in sorted((ursprünglichDaten/'entwicklungKopfdateien').glob('*.h'))]
    bestandteile += [('/sdk/lib/start.o',wurzelPfad/'build/user/start.o'),('/sdk/lib/crt.o',ergebnisDaten/'crt.o'),('/sdk/lib/aot-runtime.o',ergebnisDaten/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',wurzelPfad/'build/libposix-kor-user.a')]
    kopfbereichWert=['typedef struct { const char *Name; const unsigned char *Daten; unsigned größe; } übersetzerBetriebsmittelEintrag;']
    for ordnungszahlIndex,(_,pfad) in enumerate(bestandteile):
        kopfbereichWert.append('static const unsigned char 탑재자원_%d[] = {%s};'%(ordnungszahlIndex,','.join(str(vorläufigDaten) for vorläufigDaten in pfad.read_bytes())))
    kopfbereichWert.append('static const übersetzerBetriebsmittelEintrag übersetzerBetriebsmittel[] = {')
    for ordnungszahlIndex,(Name,pfad) in enumerate(bestandteile): kopfbereichWert.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Name,ensure_ascii=False),ordnungszahlIndex,pfad.stat().st_size))
    kopfbereichWert.append('};');(ergebnisDaten/'resources.h').write_text('\n'.join(kopfbereichWert)+'\n',encoding='utf-8')
    zielDateien=[]
    for Name in ('übersetzerWerkzeug.c','LaufzeitUnterstützung.c','ausführenVorgang.c','vorabVonElementZeit.c','zurückkehrenBrücke.S'):
        zielDatei=ergebnisDaten/(Path(Name).stem+'.o');zielDateien.append(zielDatei)
        befehlAusführen([CÜbersetzer]+konfigurationBitliste+['-ffunction-sections','-fdata-sections']+einschlüsse+['-c',ursprünglichDaten/Name,'-o',zielDatei])
    ausführdateiDatei=wurzelPfad/'build/user/cc.elf'
    befehlAusführen([binderWerkzeug,'--gc-sections','-T',wurzelPfad/'Benutzer/Bindungsanordnung.ld','-z','max-page-size=4096','-o',ausführdateiDatei,
         wurzelPfad/'build/user/start.o',wurzelPfad/'build/user/runtime.o']+zielDateien+
         [wurzelPfad/'build/user'/Name for Name in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[einbauten[-1]])
