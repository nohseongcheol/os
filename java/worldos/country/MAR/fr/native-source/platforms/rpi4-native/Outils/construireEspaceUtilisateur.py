"""독립된 interne ABI ELF64와 로더 rejeterValeur Tests 자료를 만든다."""
import struct
import tempfile
from pathlib import Path
from construirePython import créerPython
from construireBibliothèqueJava import créerBibliothèqueJava
from construireCompilateurC import créerCompilateurC


def créerEspaceUtilisateur(cheminRacine, cheminDépôt, CompilateurC, compilateurCpp, outilÉditeurLiens, outilArchive, bitsConfiguration, exécuterCommande):
    bitsConfiguration = [valeurRéglages for valeurRéglages in bitsConfiguration if valeurRéglages != '-mgeneral-regs-only']
    construireChemin = cheminRacine / 'build'
    sortie = construireChemin / 'user'
    sortie.mkdir(exist_ok=True)
    donnéesOriginal = cheminRacine / 'Utilisateur'
    pOSIX = cheminDépôt / 'posix-kor/arm64-native'
    cheminInclure = ['-I', donnéesOriginal, '-I', pOSIX / 'Entêtes', '-I', sortie]
    for outilCompilateur, régionSupplémentaire, chemin, nom in [
            (CompilateurC, [], donnéesOriginal / 'lancer.S', 'start.o'),
            (CompilateurC, ['-std=c11'], donnéesOriginal / 'exécuterCommande.c', 'runtime.o'),
            (CompilateurC, ['-std=c11'], pOSIX / 'pontUtilisateur.c', 'posix.o'),
            (compilateurCpp, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], donnéesOriginal / 'ExempleFichier.cpp', 'demo.o'),
            (compilateurCpp, ['-std=c++11', '-fno-exceptions', '-fno-rtti'], donnéesOriginal / 'ExempleCommunication.cpp', 'network.o'),
            (CompilateurC, ['-std=c11'], donnéesOriginal / 'TestProtection.c', 'fault.o'),
            (CompilateurC, ['-std=c11'], donnéesOriginal / 'Éditeur.c', 'vi.o')]:
        exécuterCommande([outilCompilateur] + bitsConfiguration + régionSupplémentaire + cheminInclure + ['-Wall', '-Wextra', '-Werror', '-c', chemin, '-o', sortie / nom])
    exécuterCommande([outilArchive, 'rcs', construireChemin / 'libposix-kor-user.a', sortie / 'posix.o'])
    for nom in ('demo', 'fault', 'network', 'vi'):
        exécuterCommande([outilÉditeurLiens, '-T', donnéesOriginal / 'DispositionLiens.ld', '-z', 'max-page-size=4096', '-o', sortie / (nom + '.elf'),
             sortie / 'start.o', sortie / 'runtime.o', sortie / (nom + '.o'), construireChemin / 'libposix-kor-user.a'])
    créerBibliothèqueJava(cheminRacine, exécuterCommande)
    # 기존 interne Java Compilateur/JVM을 별도의 EL0 ELF로 재사용한다.
    with tempfile.TemporaryDirectory(prefix='java-tools-', dir=str(construireChemin)) as cheminTravailEnCours:
        cheminClasse = Path(cheminTravailEnCours)
        exécuterCommande(['javac', '--release', '8', '-encoding', 'UTF-8', '-proc:none',
             '-classpath', cheminClasse, '-sourcepath', cheminClasse, '-d', cheminClasse] +
            [positionDonnées for positionDonnées in sorted((cheminDépôt / 'os/Utilisateur/Java').glob('*.java')) if positionDonnées.name != 'MachineVirtuelleJava.java'] + sorted((donnéesOriginal / 'Java').glob('*.java')))
        exécuterCommande(['sh', cheminDépôt / 'compiler/tempsDeAnticipé.sh', '--entry', 'EntréeÉlémentOutil.lancer',
             '--profile', 'user', '--heap-words', '1048576', '-o', sortie / 'java-tools.c'] + sorted(cheminClasse.glob('*.class')))
    bibliothèqueDécompression = cheminRacine / 'vendor/uzlib'
    for chemin, nom in [(sortie / 'java-tools.c', 'java-tools.o'), (donnéesOriginal / 'pontJava.c', 'java-link.o'),
                       (donnéesOriginal / 'Paquet.c', 'jar.o')] + [(bibliothèqueDécompression / (nom + '.c'), nom + '.o') for nom in ('tinflate', 'crc32', 'adler32')]:
        exécuterCommande([CompilateurC] + bitsConfiguration + ['-std=c11', '-DUZLIB_CONF_PARANOID_CHECKS=1', '-I', bibliothèqueDécompression] + cheminInclure + ['-c', chemin, '-o', sortie / nom])
    exécuterCommande([outilÉditeurLiens, '-T', donnéesOriginal / 'DispositionLiens.ld', '-z', 'max-page-size=4096', '-o', sortie / 'java-tools.elf'] +
        [sortie / nom for nom in ('start.o', 'runtime.o', 'java-tools.o', 'java-link.o', 'jar.o', 'tinflate.o', 'crc32.o', 'adler32.o')])
    créerPython(cheminRacine, CompilateurC, outilÉditeurLiens)
    créerCompilateurC(cheminRacine, cheminDépôt, CompilateurC, outilÉditeurLiens, bitsConfiguration, exécuterCommande)
    valide = (sortie / 'demo.elf').read_bytes()
    décalageEntêteProgramme = struct.unpack_from('<Q', valide, 32)[0]
    listeEntête = [décalageEntêteProgramme + nombreÉlémentsÉlémentListe * 56 for nombreÉlémentsÉlémentListe in range(struct.unpack_from('<H', valide, 56)[0])]
    chargements = [positionDonnées for positionDonnées in listeEntête if struct.unpack_from('<I', valide, positionDonnées)[0] == 1]
    texte, Données = chargements[:2]
    adresseCommande = struct.unpack_from('<Q', valide, texte + 16)[0]
    adresseDonnées = struct.unpack_from('<Q', valide, Données + 16)[0]
    ABIAppel = valide.index(b'JKOROS\0')
    testCas = [('empty', b''), ('short', valide[:63])]
    modifications = [('magic', 0, 'B', 0), ('elf32', 4, 'B', 1), ('endian', 5, 'B', 2),
               ('machine', 18, 'H', 62), ('shared', 16, 'H', 3),
               ('phoff-overflow', 32, 'Q', 2**64 - 8), ('phnum', 56, 'H', 17), ('phsize', 54, 'H', 57),
               ('unaligned-entry', 24, 'Q', adresseCommande + 1), ('data-entry', 24, 'Q', adresseDonnées),
               ('outside-file', texte + 32, 'Q', len(valide) + 1), ('short-memory', texte + 40, 'Q', 1),
               ('kernel-address', texte + 16, 'Q', 0x80000), ('memory-overflow', texte + 40, 'Q', 2**64 - 1),
               ('writable-code', texte + 4, 'I', 7), ('missing-abi', ABIAppel, 'B', ord('X')),
               ('wrong-abi', ABIAppel + 8, 'I', 2), ('dynamic', texte, 'I', 2),
               ('unaligned-load', texte + 16, 'Q', adresseCommande + 8),
               ('overlap', Données + 16, 'Q', adresseCommande)]
    for nom, valeurDécalage, formatDonnées, valeur in modifications:
        changé = bytearray(valide); struct.pack_into('<' + formatDonnées, changé, valeurDécalage, valeur)
        testCas.append((nom, bytes(changé)))
    blocsBinaires = [(nom.replace('-', '_'), sortie / (nom + '.elf')) for nom in ('demo', 'fault', 'network', 'java-tools', 'python', 'vi', 'cc')]
    for indiceRechercher, (nom, donnéesChargeUtile) in enumerate(testCas):
        chemin = sortie / ('invalid-{}.elf'.format(nom)); chemin.write_bytes(donnéesChargeUtile)
        blocsBinaires.append(('invalid_{}'.format(indiceRechercher), chemin))
    assembleur, valeurEntête = ['.section .rodata.user,"a"'], []
    tailles = {}
    for nom, chemin in blocsBinaires:
        valeurSymbole = 'user_blob_' + nom
        tailles[nom] = chemin.stat().st_size
        # 생성한 valeurPairRéseau 경로만 넣어 프로젝트 경로의 공백/guillemet 영향을 피한다.
        assembleur += ['.balign 16', '.global ' + valeurSymbole, valeurSymbole + ':', '.incbin "{}"'.format(chemin.relative_to(cheminRacine))]
        valeurEntête.append('extern const unsigned char {}[];'.format(valeurSymbole))
    assembleur.append('.section .note.GNU-stack,"",%progbits')
    valeurEntête += ['static const programme entréesListeCodeExécutable[] = {', '{user_blob_demo, %d, 0},' % tailles['demo']]
    valeurEntête += ['{user_blob_fault, %d, %d},' % (tailles['fault'], valeurTransféré) for valeurTransféré in range(8)]
    valeurEntête += ['{user_blob_network, %d, 0},' % tailles['network']]
    valeurEntête += ['{user_blob_java_tools, %d, %d},' % (tailles['java_tools'], modeMéthode) for modeMéthode in (0, 1)]
    valeurEntête += ['{user_blob_python, %d, 0},' % tailles['python'], '{user_blob_vi, %d, 0},' % tailles['vi']]
    valeurEntête += ['{user_blob_java_tools, %d, 2},' % tailles['java_tools']]
    valeurEntête += ['{user_blob_cc, %d, 0},' % tailles['cc']]
    valeurEntête += ['{user_blob_cc, %d, 1},' % tailles['cc']]
    valeurEntête += ['};', 'static const programme exécutablesInvalide[] = {']
    valeurEntête += ['{user_blob_invalid_%d, %d, 0},' % (indiceOrdinal, len(donnéesChargeUtile)) for indiceOrdinal, (_, donnéesChargeUtile) in enumerate(testCas)]
    valeurEntête += ['};']
    (construireChemin / 'programs.S').write_text('\n'.join(assembleur) + '\n')
    (construireChemin / 'programs.h').write_text('\n'.join(valeurEntête) + '\n')
    (sortie / 'invalid-cases.txt').write_text('\n'.join(nom for nom, _ in testCas) + '\n')
    exécuterCommande([CompilateurC] + bitsConfiguration + ['-c', construireChemin / 'programs.S', '-o', construireChemin / 'programs.o'])
