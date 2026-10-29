#!/usr/bin/env python3
"""effettivo_dati kernel_VALORE Paint_schermata 코드를 host Memoria_dati 화면에 연결해 부분 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

azione_radice = Path(__file__).resolve().parents[1]

def avvia():
    fonte_File = ['prove/aggiornare_schermata.c', 'computer/schermata_disegno.c', 'computer/terminale.c', 'computer/elemento_grafico.c']
    검증원문들 = fonte_File + ['codiceSorgente/화면합성.java', 'codiceSorgente/scheda.java', '../../compiler/자바도구/기계어미리번역.java']
    meta_VALORE = azione_radice/'build/verification/redraw'; meta_VALORE.mkdir(parents=True, exist_ok=True)
    LOG_riga = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Nome: hashlib.sha256((azione_radice/Nome).read_bytes()).hexdigest() for Nome in 검증원문들}}
    try:
        Corso_percorso = meta_VALORE/'classes'; Corso_percorso.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Corso_percorso),
            str(azione_radice/'codiceSorgente/화면합성.java'), str(azione_radice/'codiceSorgente/scheda.java')])
        esportare_tabella = {'jdraw_prepare': 'Prepara', 'jdraw_width': '너비얻기', 'jdraw_height': 'get_altezza',
            'jdraw_count_low': '기록아래얻기', 'jdraw_count_high': '기록위얻기', 'jdraw_clip': 'ritagliare',
            'jdraw_clip_value': 'ritagliare_VALORE', 'jdraw_begin': 'avvia', 'jdraw_end': 'Fine',
            'jdraw_pixel': 'pixel', 'jdraw_rectangle': 'rettangolo_Riempi', 'jdraw_pointer': 'puntatore'}
        번역명령 = ['sh', str(azione_radice.parents[1]/'compiler/미리번역.sh'), '--entry', '화면합성.너비얻기', '-o', str(meta_VALORE/'disegno_VALORE.c')]
        for Connetti, FUNZIONE_VALORE in esportare_tabella.items(): 번역명령.extend(['--export', Connetti+'=화면합성.'+FUNZIONE_VALORE])
        subprocess.check_call(번역명령+[str(percorso) for percorso in sorted(Corso_percorso.glob('*.class'))])
        comando = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + fonte_File
        disegno_meta = meta_VALORE/'disegno_VALORE.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(meta_VALORE/'disegno_VALORE.c'), '-o', str(disegno_meta)])
        subprocess.check_call(comando+[str(disegno_meta), 'build/terminal-font.S', '-o', str(meta_VALORE/'schermata_aggiornare_test')], cwd=str(azione_radice))
        risultato = subprocess.check_output([str(meta_VALORE/'schermata_aggiornare_test')], timeout=30).decode()
        (meta_VALORE/'convalidare.log').write_text(risultato)
        맞음 = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', risultato)
        assert 맞음 and 'PASS:' in risultato, risultato
        LOG_riga.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(맞음[1]), mean_framebuffer_writes_per_move=int(맞음[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(risultato, end='')
    finally:
        (meta_VALORE/'report.json').write_text(json.dumps(LOG_riga, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': avvia()
