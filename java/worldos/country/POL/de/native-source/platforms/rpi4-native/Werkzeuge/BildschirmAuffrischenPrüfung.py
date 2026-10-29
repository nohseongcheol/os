#!/usr/bin/env python3
"""tatsächlichDaten betriebskernWert malenBildschirm 코드를 Wirtssystem speicherDaten 화면에 연결해 unterteilWert 갱신을 검증한다."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

projektWurzel = Path(__file__).resolve().parents[1]

def ausführenVorgang():
    quelltextDateien = ['Prüfungen/bildschirmAuffrischen.c', 'maschine/bildschirmZeichnung.c', 'maschine/terminal.c', 'maschine/Bedienelement.c']
    validierungQuelltexte = quelltextDateien + ['Quelltext/BildpufferZusammensetzer.java', 'Quelltext/Platine.java', '../../compiler/JavaWerkzeug/Vorabübersetzung.java']
    zielWert = projektWurzel/'build/verification/redraw'; zielWert.mkdir(parents=True, exist_ok=True)
    protokolldateiAufzeichnung = {'passed': False, 'test_environment': 'host CPU, Java AOT framebuffer composition and native terminal/widgets with memory framebuffer',
          'kernel_sha256': hashlib.sha256((projektWurzel/'build/kernel8.img').read_bytes()).hexdigest(),
          'source_sha256': {Name: hashlib.sha256((projektWurzel/Name).read_bytes()).hexdigest() for Name in validierungQuelltexte}}
    try:
        klassePfad = zielWert/'classes'; klassePfad.mkdir(exist_ok=True)
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(klassePfad),
            str(projektWurzel/'Quelltext/BildpufferZusammensetzer.java'), str(projektWurzel/'Quelltext/Platine.java')])
        exportierenTabelle = {'jdraw_prepare': 'vorbereiten', 'jdraw_width': 'breiteHolen', 'jdraw_height': 'höheHolen',
            'jdraw_count_low': 'zählerNiedrigHolen', 'jdraw_count_high': 'zählerHochHolen', 'jdraw_clip': 'beschneiden',
            'jdraw_clip_value': 'beschneidenWert', 'jdraw_begin': 'ausführenVorgang', 'jdraw_end': 'beenden',
            'jdraw_pixel': 'bildpunkt', 'jdraw_rectangle': 'rechteckFüllen', 'jdraw_pointer': 'zeiger'}
        übersetzungsvorgangBefehl = ['sh', str(projektWurzel.parents[1]/'compiler/vorabVonElementZeit.sh'), '--entry', 'BildpufferZusammensetzer.breiteHolen', '-o', str(zielWert/'Zeichnung.c')]
        for verbinden, Funktion in exportierenTabelle.items(): übersetzungsvorgangBefehl.extend(['--export', verbinden+'=BildpufferZusammensetzer.'+Funktion])
        subprocess.check_call(übersetzungsvorgangBefehl+[str(pfad) for pfad in sorted(klassePfad.glob('*.class'))])
        befehl = ['clang', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror'] + quelltextDateien
        zeichnungZiel = zielWert/'Zeichnung.o'
        subprocess.check_call(['clang', '-std=c11', '-O2', '-c', str(zielWert/'Zeichnung.c'), '-o', str(zeichnungZiel)])
        subprocess.check_call(befehl+[str(zeichnungZiel), 'build/terminal-font.S', '-o', str(zielWert/'BildschirmAuffrischenPrüfung')], cwd=str(projektWurzel))
        ergebnis = subprocess.check_output([str(zielWert/'BildschirmAuffrischenPrüfung')], timeout=30).decode()
        (zielWert/'validieren.log').write_text(ergebnis)
        istÜbereinstimmend = re.search(r'([\d.]+) ms/move; (\d+) framebuffer writes/move', ergebnis)
        assert istÜbereinstimmend and 'PASS:' in ergebnis, ergebnis
        protokolldateiAufzeichnung.update(passed=True, move_count=80, resize_count=40, window_count=4,
                   host_cpu_ms_per_move=float(istÜbereinstimmend[1]), mean_framebuffer_writes_per_move=int(istÜbereinstimmend[2]),
                   full_redraw_reference_equal=True, untouched_outside_damage=True,
                   unchanged_pixels_not_written=True, repeated_position_not_repainted=True,
                   padded_stride_preserved=True)
        print(ergebnis, end='')
    finally:
        (zielWert/'report.json').write_text(json.dumps(protokolldateiAufzeichnung, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__': ausführenVorgang()
