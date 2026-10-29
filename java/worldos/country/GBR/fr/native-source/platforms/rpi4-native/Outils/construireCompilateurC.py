"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def créerCompilateurC(cheminRacine, cheminDépôt, CompilateurC, outilÉditeurLiens, bitsConfiguration, exécuterCommande):
    donnéesRésultat = cheminRacine / 'build/ccompiler'; donnéesRésultat.mkdir(exist_ok=True)
    donnéesOriginal = cheminRacine / 'CompilateurC'
    amont = cheminRacine / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    trousseDéveloppement = cheminRacine / 'vendor/sdk'
    if not (trousseDéveloppement/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    élémentsIntégrés = sorted((trousseDéveloppement/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not élémentsIntégrés: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    bitsConfiguration = [valeurRéglages for valeurRéglages in bitsConfiguration if valeurRéglages != '-mgeneral-regs-only']
    inclusions = ['-I', donnéesOriginal, '-I', amont, '-I', cheminRacine/'Utilisateur', '-I', donnéesRésultat, '-isystem', trousseDéveloppement/'usr/include']
    exécuterCommande([CompilateurC]+bitsConfiguration+['-ffunction-sections','-fdata-sections']+inclusions+['-c',donnéesOriginal/'priseEnChargeDémarrage.c','-o',donnéesRésultat/'crt.o'])
    exécuterCommande([CompilateurC]+bitsConfiguration+['-I',cheminDépôt/'posix-kor/arm64-native/Entêtes']+inclusions+['-c',donnéesOriginal/'environnementExécutionCompilationAnticipée.c','-o',donnéesRésultat/'aot-runtime.o'])
    ressourcesVisuelles = [('/sdk/include/'+positionDonnées.name,positionDonnées) for positionDonnées in sorted((cheminDépôt/'posix-kor/arm64-native/Entêtes').glob('*.h'))]
    ressourcesVisuelles += [('/sdk/include/'+positionDonnées.name,positionDonnées) for positionDonnées in sorted((amont/'include').glob('*.h'))]
    ressourcesVisuelles += [('/sdk/include/'+positionDonnées.name,positionDonnées) for positionDonnées in sorted((donnéesOriginal/'entêtesDéveloppement').glob('*.h'))]
    ressourcesVisuelles += [('/sdk/lib/start.o',cheminRacine/'build/user/start.o'),('/sdk/lib/crt.o',donnéesRésultat/'crt.o'),('/sdk/lib/aot-runtime.o',donnéesRésultat/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',cheminRacine/'build/libposix-kor-user.a')]
    valeurEntête=['typedef struct { const char *nom; const unsigned char *Données; unsigned taille; } ressourceCompilateur;']
    for indiceOrdinal,(_,chemin) in enumerate(ressourcesVisuelles):
        valeurEntête.append('static const unsigned char 탑재자원_%d[] = {%s};'%(indiceOrdinal,','.join(str(donnéesTemporaire) for donnéesTemporaire in chemin.read_bytes())))
    valeurEntête.append('static const ressourceCompilateur ressourcesCompilateur[] = {')
    for indiceOrdinal,(nom,chemin) in enumerate(ressourcesVisuelles): valeurEntête.append('{%s, 탑재자원_%d, %d},'%(json.dumps(nom,ensure_ascii=False),indiceOrdinal,chemin.stat().st_size))
    valeurEntête.append('};');(donnéesRésultat/'resources.h').write_text('\n'.join(valeurEntête)+'\n',encoding='utf-8')
    fichiersDestination=[]
    for nom in ('outilCompilateur.c','PriseEnChargeEnvironnementExécution.c','lancer.c','tempsDeAnticipé.c','pontRetourner.S'):
        fichierDestination=donnéesRésultat/(Path(nom).stem+'.o');fichiersDestination.append(fichierDestination)
        exécuterCommande([CompilateurC]+bitsConfiguration+['-ffunction-sections','-fdata-sections']+inclusions+['-c',donnéesOriginal/nom,'-o',fichierDestination])
    fichierCodeExécutable=cheminRacine/'build/user/cc.elf'
    exécuterCommande([outilÉditeurLiens,'--gc-sections','-T',cheminRacine/'Utilisateur/DispositionLiens.ld','-z','max-page-size=4096','-o',fichierCodeExécutable,
         cheminRacine/'build/user/start.o',cheminRacine/'build/user/runtime.o']+fichiersDestination+
         [cheminRacine/'build/user'/nom for nom in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[élémentsIntégrés[-1]])
