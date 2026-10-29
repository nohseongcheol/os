"""독립된 eigen ABI ELF64와 로더 wertZurückweisen Prüfungen 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from pythonErzeugenAbbild import pythonErstellen
from javaBibliothekErzeugenAbbild import javaBibliothekErstellen
from cÜbersetzerErzeugenAbbild import cÜbersetzerErstellen


def benutzerRaumErstellen(wurzelPfad, ablagePfad, CÜbersetzer, cppÜbersetzer, binderWerkzeug, archivWerkzeug, konfigurationBitliste, befehlAusführen):
    konfigurationBitliste = [einstellungenWert for einstellungenWert in konfigurationBitliste if einstellungenWert != '-mgeneral-regs-only']
    pfadErzeugenAbbild = wurzelPfad / 'build'
    ausgabe = pfadErzeugenAbbild / 'user'
    ausgabe.mkdir(exist_ok=True)
    ursprünglichDaten = wurzelPfad / 'Benutzer'
    pOSIX = ablagePfad / 'posix-kor/arm64-native'
    einbindenPfad = ['-I', ursprünglichDaten, '-I', pOSIX / 'Kopfdateien', '-I', ausgabe]
    for übersetzerWerkzeug, zusätzlichGebiet, pfad, Name in [
            (CÜbersetzer, [], ursprünglichDaten / 'ausführenVorgang.S', 'start.o'),
            (CÜbersetzer, ['-std=c11'], ursprünglichDaten / 'befehlAusführen.c', 'runtime.o'),
            (CÜbersetzer, ['-std=c11'], pOSIX / 'benutzerBrücke.c', 'posix.o'),
            (cppÜbersetzer, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], ursprünglichDaten / 'Dateibeispiel.cpp', 'demo.o'),
            (cppÜbersetzer, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], ursprünglichDaten / 'KommunikationBeispiel.cpp', 'network.o'),
            (CÜbersetzer, ['-std=c11'], ursprünglichDaten / 'SchutzPrüfung.c', 'fault.o'),
            (CÜbersetzer, ['-std=c11'], ursprünglichDaten / 'Editor.c', 'vi.o')]:
        befehlAusführen([übersetzerWerkzeug] + konfigurationBitliste + zusätzlichGebiet + einbindenPfad + ['-Wall', '-Wextra', '-Werror', '-c', pfad, '-o', ausgabe / Name])
    befehlAusführen([archivWerkzeug, 'rcs', pfadErzeugenAbbild / 'libposix-kor-user.a', ausgabe / 'posix.o'])
    for Name in ('demo', 'fault', 'network', 'vi'):
        befehlAusführen([binderWerkzeug, '-T', ursprünglichDaten / 'Bindungsanordnung.ld', '-z', 'max-page-size=4096', '-o', ausgabe / (Name + '.elf'),
             ausgabe / 'start.o', ausgabe / 'runtime.o', ausgabe / (Name + '.o'), pfadErzeugenAbbild / 'libposix-kor-user.a'])
    javaBibliothekErstellen(wurzelPfad, befehlAusführen)
    # 기존 eigen Java Übersetzer/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(pfadErzeugenAbbild)) as arbeitendPfad:
        klassePfad = Path(arbeitendPfad)
        befehlAusführen(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', klassePfad, '-sourcepath', klassePfad, '-d', klassePfad] +
            [datenPosition for datenPosition in sorted((ablagePfad / 'os/Benutzer/Java').glob('*.java')) if datenPosition.name != 'VirtuelleJavaMaschine.java'] + sorted((ursprünglichDaten / 'Java').glob('*.java')))
        befehlAusführen(['sh', ablagePfad / 'compiler/vorabVonElementZeit.sh', '--entry', 'WerkzeugEintrag.ausführenVorgang',
             '--profile', 'user', '--heap-words', '1048576', '-o', ausgabe / 'java-tools.c'] + sorted(klassePfad.glob('*.class')))
    entpackbibliothek = wurzelPfad / 'vendor/uzlib'
    for pfad, Name in [(ausgabe / 'java-tools.c', 'java-tools.o'), (ursprünglichDaten / 'javaBrücke.c', 'java-link.o'),
                       (ursprünglichDaten / 'Paket.c', 'jar.o')] + [(entpackbibliothek / (Name + '.c'), Name + '.o') for Name in ('tinflate', 'crc32', 'adler32')]:
        befehlAusführen([CÜbersetzer] + konfigurationBitliste + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', entpackbibliothek] + einbindenPfad + ['-c', pfad, '-o', ausgabe / Name])
    befehlAusführen([binderWerkzeug, '-T', ursprünglichDaten / 'Bindungsanordnung.ld', '-z', 'max-page-size=4096', '-o', ausgabe / 'java-tools.elf'] +
        [ausgabe / Name for Name in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    pythonErstellen(wurzelPfad, CÜbersetzer, binderWerkzeug)
    cÜbersetzerErstellen(wurzelPfad, ablagePfad, CÜbersetzer, binderWerkzeug, konfigurationBitliste, befehlAusführen)
    gültig = (ausgabe / 'demo.elf').read_bytes()
    programmKopfVersatzwert = struct.unpack_from('<Q', gültig, 32)[0]
    kopfListe = [programmKopfVersatzwert + elementeintragAnzahl * 56 for elementeintragAnzahl in range(struct.unpack_from('<H', gültig, 56)[0])]
    ladeeinträge = [datenPosition for datenPosition in kopfListe if struct.unpack_from('<I', gültig, datenPosition)[0] == 1]
    Text, Daten = ladeeinträge[:2]
    befehlAdresse = struct.unpack_from('<Q', gültig, Text + 16)[0]
    datenAdresse = struct.unpack_from('<Q', gültig, Daten + 16)[0]
    AufrufVorgangABI = gültig.index(b'JKOROS\0')
    fallPrüfung = [('empty', b''), ('short', gültig[:63])]
    änderungen = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', befehlAdresse + 1), ('data-entry', 24, 'Q', datenAdresse),
               ('outside-file', Text + 32, 'Q', len(gültig) + 1), ('short-memory', Text + 40, 'Q', 1),
               ('kernel-address', Text + 16, 'Q', 0x80000), ('memory-overflow', Text + 40, 'Q', 2**64 - 1),
               ('writable-code', Text + 4, 'I', 7), ('missing-abi', AufrufVorgangABI, 'B', ord('X')),
               ('wrong-abi', AufrufVorgangABI + 8, 'I', 2), ('dynamic', Text, 'I', 2),
               ('unaligned-load', Text + 16, 'Q', befehlAdresse + 8),
               ('overlap', Daten + 16, 'Q', befehlAdresse)]
    for Name, versatzwertWert, datenFormat, Wert in änderungen:
        geändert = bytearray(gültig); struct.pack_into('<' + datenFormat, geändert, versatzwertWert, Wert)
        fallPrüfung.append((Name, bytes(geändert)))
    binärblöcke = [(Name.replace('-', '_'), ausgabe / (Name + '.elf')) for Name in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for nachschlagenIndex, (Name, nutzdatenDaten) in enumerate(fallPrüfung):
        pfad = ausgabe / ('invalid-{}.elf'.format(Name)); pfad.write_bytes(nutzdatenDaten)
        binärblöcke.append(('invalid_{}'.format(nachschlagenIndex), pfad))
    assemblersprache, kopfbereichWert = ['.section .rodata.user,"a"'], []
    größen = {}
    for Name, pfad in binärblöcke:
        symbolWert = 'user_blob_' + Name
        größen[Name] = pfad.stat().st_size
        # 생성한 gegenstelleWert 경로만 넣어 프로젝트 경로의 공백/anführungszeichen 영향을 피한다.
        assemblersprache += ['.balign 16', '.global ' + symbolWert, symbolWert + ':', '.incbin "{}"'.format(pfad.relative_to(wurzelPfad))]
        kopfbereichWert.append('extern const unsigned char {}[];'.format(symbolWert))
    assemblersprache.append('.section .note.GNU-stack,"",%progbits')
    kopfbereichWert += ['static const programm ausführdateiEinträge[] = {', '{user_blob_demo, %d, 0},' % größen['demo']]
    kopfbereichWert += ['{user_blob_fault, %d, %d},' % (größen['fault'], weitergeleitetWert) for weitergeleitetWert in range(8)]
    kopfbereichWert += ['{user_blob_network, %d, 0},' % größen['network']]
    kopfbereichWert += ['{user_blob_java_tools, %d, %d},' % (größen['java_tools'], methodeBetriebsart) for methodeBetriebsart in (0, 1)]
    kopfbereichWert += ['{user_blob_python, %d, 0},' % größen['python'], '{user_blob_vi, %d, 0},' % größen['vi']]
    kopfbereichWert += ['{user_blob_java_tools, %d, 2},' % größen['java_tools']]
    kopfbereichWert += ['{user_blob_cc, %d, 0},' % größen['cc']]
    kopfbereichWert += ['{user_blob_cc, %d, 1},' % größen['cc']]
    kopfbereichWert += ['};', 'static const programm ungültigAusführdateien[] = {']
    kopfbereichWert += ['{user_blob_invalid_%d, %d, 0},' % (ordnungszahlIndex, len(nutzdatenDaten)) for ordnungszahlIndex, (_, nutzdatenDaten) in enumerate(fallPrüfung)]
    kopfbereichWert += ['};']
    (pfadErzeugenAbbild / 'programs.S').write_text('\n'.join(assemblersprache) + '\n')
    (pfadErzeugenAbbild / 'programs.h').write_text('\n'.join(kopfbereichWert) + '\n')
    (ausgabe / 'invalid-cases.txt').write_text('\n'.join(Name for Name, _ in fallPrüfung) + '\n')
    befehlAusführen([CÜbersetzer] + konfigurationBitliste + ['-c', pfadErzeugenAbbild / 'programs.S', '-o', pfadErzeugenAbbild / 'programs.o'])
