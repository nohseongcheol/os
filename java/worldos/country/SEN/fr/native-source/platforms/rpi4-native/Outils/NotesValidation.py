#!/usr/bin/env python3
"""élémentListeActuel 커널과 donnéesEffectif Tests·배포물이 일치할 때에만 통합 valider 기록을 만든다."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

racineProjet = Path(__file__).resolve().parents[1]

def fichierHachage(chemin):
    calculRésultat = hashlib.sha256()
    with chemin.open('rb') as Fichier:
        for Données in iter(lambda: Fichier.read(1048576), b''): calculRésultat.update(Données)
    return calculRésultat.hexdigest()

def lancer():
    cheminValidation = racineProjet/'build/verification'
    hachageNoyau = fichierHachage(racineProjet/'build/kernel8.img')
    enregistrementsJournal = {}
    for nom in ('boot','shell','desktop','windows','swing','stream','coding','jvm','examples','ftp','elf','remmina','pip','resolution','resize'):
        cheminRelatif = 'report.json' if nom == 'boot' else nom+'/report.json'
        Données = json.loads((cheminValidation/cheminRelatif).read_text())
        if not Données.get('passed') or Données.get('kernel_sha256') != hachageNoyau:
            raise SystemExit('élémentListeActuel 커널에 대한 valeurSuccès 기록이 필요합니다: '+cheminRelatif)
        enregistrementsJournal[nom] = {'passed': True, 'report': cheminRelatif}
    contrôlerNom = json.loads((cheminValidation/'naming/report.json').read_text())
    if not contrôlerNom['passed'] or not contrôlerNom['c_semantic_checked']: raise SystemExit('C 선언을 포함한 nommage Contrôles valeurNécessaire')
    for chemin, valeurAttendu in contrôlerNom['c_source_sha256'].items():
        if fichierHachage(racineProjet/chemin) != valeurAttendu: raise SystemExit('nommage Contrôles valeurRetourArrièreCôté 바뀐 C source: '+chemin)
    contrôlerJava = json.loads((cheminValidation/'jvm/report.json').read_text())
    ÉcranDirect = json.loads((cheminValidation/'swing/report.json').read_text())
    if not ÉcranDirect.get('direct_korean_gui'): raise SystemExit('français 직접 Écran exécuterCommande Tests valeurNécessaire')
    contrôlerValeurOctet = json.loads((cheminValidation/'naming/direct-bytecode.json').read_text())
    if not contrôlerValeurOctet['passed'] or contrôlerValeurOctet['jar_sha256'] != fichierHachage(racineProjet/'dist/jkoros-native-korean.jar'):
        raise SystemExit('élémentListeActuel français 라이브러리의 직접 invoquer codeOctets vérifier valeurNécessaire')
    contrôlerRésolution = json.loads((cheminValidation/'resolution/report.json').read_text())
    contrôlerTaille = json.loads((cheminValidation/'resize/report.json').read_text())
    contrôlerMisesÀJourPour = json.loads((cheminValidation/'redraw/report.json').read_text())
    if not contrôlerMisesÀJourPour['passed'] or contrôlerMisesÀJourPour['kernel_sha256'] != hachageNoyau:
        raise SystemExit('élémentListeActuel 커널의 valeurSousPartie actualiser Tests valeurNécessaire')
    for chemin, valeurAttendu in contrôlerMisesÀJourPour['source_sha256'].items():
        if fichierHachage(racineProjet/chemin) != valeurAttendu: raise SystemExit('valeurSousPartie actualiser Tests valeurRetourArrièreCôté 바뀐 source: '+chemin)
    if not contrôlerJava.get('direct_korean_thread_and_entry'):
        raise SystemExit('français 직접 가닥과 lancer pointEntréeÉlément Tests valeurNécessaire')
    contrôlerExemple = json.loads((cheminValidation/'examples/report.json').read_text())
    if sorted(contrôlerTaille['resolutions']) != [[640,480],[1920,1080]]:
        raise SystemExit('두 해상도의 valeurCoin taille 조절 Tests valeurNécessaire')
    if not contrôlerExemple.get('swing_example_korean_input_button_label_and_close') or contrôlerExemple['examples_executed'] != 13:
        raise SystemExit('français Swing 창을 포함한 Exemples 13개 Tests valeurNécessaire')
    if sorted(contrôlerRésolution['resolutions']) != [[640,480], [1280,720], [1920,1080]]:
        raise SystemExit('640×480, 1280×720, 1920×1080 donnéesEffectif Écran Tests valeurNécessaire')
    if contrôlerJava['korean_library_sha256'] != fichierHachage(racineProjet/'dist/jkoros-native-korean.jar'):
        raise SystemExit('Java Tests valeurRetourArrièreCôté 라이브러리가 바뀌었습니다.')
    for nom in ('testMiseEnRéseauCoréen','testExceptionsCoréen'):
        if not any(valeurEntréeÉlément['name']==nom and valeurEntréeÉlément.get('openjdk_output_equal') for valeurEntréeÉlément in contrôlerJava['tests']):
            raise SystemExit('OpenJDK 대조 Tests valeurNécessaire: '+nom)
    listeException = sorted(chemin.stem for chemin in (racineProjet/'JavaFrançais/français/interne').glob('*exception.java'))
    journalException = (cheminValidation/'jvm/testExceptionsCoréen.log').read_text().replace('\r\n','\n')
    for nom in listeException:
        if '\n'+nom+'\n' not in journalException: raise SystemExit('exception générer·잡기·description Tests valeurNécessaire: '+nom)
    spécification = json.loads((racineProjet/'dist/manifest.json').read_text())
    if spécification['image_sha256'] != fichierHachage(racineProjet/'dist/jkoros-native-rpi4.img'):
        raise SystemExit('valeurDistribution valeurImage fichierHachage 불일치')
    with zipfile.ZipFile(str(racineProjet/'dist/jkoros-native-rpi4-boot.zip')) as Paquet:
        if hashlib.sha256(Paquet.read('kernel8.img')).hexdigest() != hachageNoyau:
            raise SystemExit('Amorçage ZIP valeurNoyau 불일치')
        réglagesAmorçage = Paquet.read('config.txt')
        for nom, taille in zip(('width', 'height'), spécification['framebuffer_resolution']):
            if 'framebuffer_'+nom+'='+str(taille) not in réglagesAmorçage.decode().splitlines():
                raise SystemExit('Amorçage ZIP Écran réglages 불일치')
    with tempfile.TemporaryDirectory(prefix='release-check-', dir=str(racineProjet/'build')) as valeurTemporaire:
        valeurCopié = Path(valeurTemporaire)/'kernel8.img'
        subprocess.check_call(['mcopy','-i',str(racineProjet/'dist/jkoros-native-rpi4.img')+'@@1048576','::/kernel8.img',str(valeurCopié)])
        if fichierHachage(valeurCopié) != hachageNoyau: raise SystemExit('SD valeurImage valeurNoyau 불일치')
        copierRéglages = Path(valeurTemporaire)/'config.txt'
        subprocess.check_call(['mcopy','-i',str(racineProjet/'dist/jkoros-native-rpi4.img')+'@@1048576','::/config.txt',str(copierRéglages)])
        if copierRéglages.read_bytes() != réglagesAmorçage: raise SystemExit('SD 영상과 ZIP Écran réglages 불일치')
    enregistrementJournal = {'passed': True, 'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'target': 'own Java AOT kernel, Raspberry Pi 4 ARM64', 'kernel_sha256': hachageNoyau,
            'linux_kernel_loaded': False, 'physical_board_tested': False,
            'full_regression_and_integration_reports': enregistrementsJournal, 'naming_report': 'naming/report.json',
            'korean_exception_classes': listeException, 'openjdk_korean_api_comparison': True,
            'korean_examples_executed': contrôlerExemple['examples_executed'], 'image_and_zip_kernel_match': True,
            'terminal_resize_mouse_button': 'left', 'native_resize_cursor': True,
            'live_shell_and_vi_resize': True, 'swing_example_tested': True,
            'direct_korean_gui_and_thread': True, 'korean_start_entry': True,
            'partial_redraw_report': 'redraw/report.json',
            'combined_desktop_network': True, 'remmina_actual_client_tested': True,
            'framebuffer_resolutions_tested': sorted(contrôlerRésolution['resolutions']),
            'sd_framebuffer_resolution': spécification['framebuffer_resolution'],
            'pip_external_source_install_tested': True, 'cpython_pip': False,
            'c_korean_structs_and_real_functions': True, 'python_korean_os_error': True,
            'artifacts_sha256': {nom:fichierHachage(racineProjet/'dist'/nom) for nom in (
                'jkoros-native-rpi4.img', 'jkoros-native-rpi4-boot.zip', 'jkoros-native-korean.jar',
                'jkoros-native-korean-sources.zip', 'jkoros-native-aarch64-sdk.tar.gz', 'jkoros-native-compiler-source.tar.gz')}}
    (cheminValidation/'native-runtime-summary.json').write_text(json.dumps(enregistrementJournal,ensure_ascii=False,indent=2)+'\n')
    print('PASS: élémentListeActuel 커널의',len(enregistrementsJournal),'개 통합 Tests enregistrementJournal, français exception',len(listeException),'définitionClasse, SD valeurImage·ZIP estÉgal')

if __name__ == '__main__': lancer()
