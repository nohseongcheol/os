#!/usr/bin/env python3
"""donnéesEffectif valeurNoyau écranPeindre 코드를 Hôte donnéesMémoire 화면에 연결해 valeurSousPartie 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

racineProjet = Path(__file__).resolve().parents[1]

def lancer():
    fichiersSource = ['Tests/actualiserÉcran.c', 'machine/dessinÉcran.c', 'machine/terminal.c', 'machine/ComposantVisuel.c']
    sourcesValidation = fichiersSource + ['source/ComposeurTamponImage.java', 'source/CarteMatérielle.java', '../../compiler/OutilJava/CompilationAnticipée.java']
    valeurDestination = racineProjet/'build/verification/redraw'; valeurDestination.mkdir(parents=True, exist_ok=True)
    enregistrementJournal = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((racineProjet/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {nom: hashlib.sha256((racineProjet/nom).read_bytes()).hexdigest() for nom in sourcesValidation}}
    try:
        cheminClasse = valeurDestination/'classes'; cheminClasse.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(cheminClasse),
            str(racineProjet/'source/ComposeurTamponImage.java'), str(racineProjet/'source/CarteMatérielle.java')])
        tableExporter = {'jdraw_prepare': 'préparer', 'jdraw_width': 'obtenirLargeur', 'jdraw_height': 'obtenirHauteur',
            'jdraw_count_low': 'obtenirBasCompteur', 'jdraw_count_high': 'obtenirHautCompteur', 'jdraw_clip': 'rogner',
            'jdraw_clip_value': 'valeurRogner', 'jdraw_begin': 'lancer', 'jdraw_end': 'terminer',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': 'remplirRectangle', 'jdraw_pointer': 'pointeur'}
        commandeCompilation = ['sh', str(racineProjet.parents[1]/'compiler/tempsDeAnticipé.sh'), '--entry', 'ComposeurTamponImage.obtenirLargeur', '-o', str(valeurDestination/'Dessin.c')]
        for connecter, Fonction in tableExporter.items(): commandeCompilation.extend(['--export', connecter+'=ComposeurTamponImage.'+Fonction])
        subprocess.check_call(commandeCompilation+[str(chemin) for chemin in sorted(cheminClasse.glob('*.class'))])
        commande = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + fichiersSource
        destinationDessin = valeurDestination/'Dessin.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(valeurDestination/'Dessin.c'), '-o', str(destinationDessin)])
        subprocess.check_call(commande+[str(destinationDessin), 'build/terminal-font.S', '-o', str(valeurDestination/'TestActualiserÉcran')], cwd=str(racineProjet))
        résultat = subprocess.check_output([str(valeurDestination/'TestActualiserÉcran')], timeout=30).decode()
        (valeurDestination/'valider.log').write_text(résultat)
        estCorrespondant = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', résultat)
        assert estCorrespondant and 'PASS:' in résultat, résultat
        enregistrementJournal.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(estCorrespondant[1]), mean_framebuffer_writes_per_move=int(estCorrespondant[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(résultat, end='')
    finally:
        (valeurDestination/'report.json').write_text(json.dumps(enregistrementJournal, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': lancer()
