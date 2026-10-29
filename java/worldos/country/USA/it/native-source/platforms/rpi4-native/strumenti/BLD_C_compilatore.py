"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Crea_C_compilatore(radice_percorso, archivio_percorso, C_compilatore, linker_strumento, configurazione_BITS, Esegui_comando):
    KR_dati = radice_percorso / 'build/ccompiler'; KR_dati.mkdir(exist_ok=True)
    원본자료 = radice_percorso / 'C_compilatore'
    upstream = radice_percorso / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    kit_di_sviluppo = radice_percorso / 'vendor/sdk'
    if not (kit_di_sviluppo/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((kit_di_sviluppo/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    configurazione_BITS = [Impostazioni_VALORE for Impostazioni_VALORE in configurazione_BITS if Impostazioni_VALORE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', upstream, '-I', radice_percorso/'spazio_utente', '-I', KR_dati, '-isystem', kit_di_sviluppo/'usr/include']
    Esegui_comando([C_compilatore]+configurazione_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'avvio_Supporto.c','-o',KR_dati/'crt.o'])
    Esegui_comando([C_compilatore]+configurazione_BITS+['-I',archivio_percorso/'posix-kor/arm64-native/dichiarazioni']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',KR_dati/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+dati_funzione.name,dati_funzione) for dati_funzione in sorted((archivio_percorso/'posix-kor/arm64-native/dichiarazioni').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dati_funzione.name,dati_funzione) for dati_funzione in sorted((upstream/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dati_funzione.name,dati_funzione) for dati_funzione in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',radice_percorso/'build/user/start.o'),('/sdk/lib/crt.o',KR_dati/'crt.o'),('/sdk/lib/aot-runtime.o',KR_dati/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',radice_percorso/'build/libposix-kor-user.a')]
    Intestazione_VALORE=['typedef struct { const char *Nome; const unsigned char *dati; unsigned Dimensione; } compilatore_risorsa;']
    for 순번,(_,percorso) in enumerate(탑재자료):
        Intestazione_VALORE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in percorso.read_bytes())))
    Intestazione_VALORE.append('static const compilatore_risorsa compilatore_Risorse[] = {')
    for 순번,(Nome,percorso) in enumerate(탑재자료): Intestazione_VALORE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nome,ensure_ascii=False),순번,percorso.stat().st_size))
    Intestazione_VALORE.append('};');(KR_dati/'resources.h').write_text('\n'.join(Intestazione_VALORE)+'\n',encoding='utf-8')
    meta_File=[]
    for Nome in ('compilatore_strumento.c','CLR_Supporto.c','avvia.c','미리번역.c','Reso_bridge.S'):
        file_di_destinazione=KR_dati/(Path(Nome).stem+'.o');meta_File.append(file_di_destinazione)
        Esegui_comando([C_compilatore]+configurazione_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nome,'-o',file_di_destinazione])
    eseguibile=radice_percorso/'build/user/cc.elf'
    Esegui_comando([linker_strumento,'--gc-sections','-T',radice_percorso/'spazio_utente/disposizione_di_collegamento.ld','-z','max-page-size=4096','-o',eseguibile,
         radice_percorso/'build/user/start.o',radice_percorso/'build/user/runtime.o']+meta_File+
         [radice_percorso/'build/user'/Nome for Nome in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
