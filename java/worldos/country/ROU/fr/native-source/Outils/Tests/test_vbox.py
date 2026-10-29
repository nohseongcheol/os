import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import uuid

valeurDéfinition = importlib.util.spec_from_file_location('jkoros_vbox', str(Path(__file__).resolve().parents[1] / 'VirtualBox.py'))
valeurModule = importlib.util.module_from_spec(valeurDéfinition)
valeurDéfinition.loader.exec_module(valeurModule)


class BoîteFactice:
    def __init__(self, valeurRacine):
        self.valeurRacine = valeurRacine
        self.listeCommandes = []
        self.machinesVirtuel = {}
        self.valeurÉchec = None

    def __call__(self, arguments):
        arguments = list(map(str, arguments))
        self.listeCommandes.append(arguments)
        if self.valeurÉchec == arguments[1] or (arguments[0] == 'make' and self.valeurÉchec == 'make'):
            self.valeurÉchec = None
            raise valeurModule.erreurExécution('시험용 valeurÉchec')
        if arguments[0] == 'make':
            chemin = self.valeurRacine / 'os/build/kernel.iso'
            chemin.parent.mkdir(parents=True, exist_ok=True)
            chemin.write_bytes(b'fake-iso-for-launcher-test')
            return 'build complete\n'
        action = arguments[1]
        if action == 'list':
            return '\n'.join('"{}" {{{}}}'.format(valeur['name'], numéro) for numéro, valeur in self.machinesVirtuel.items())
        if action == 'createvm':
            numéro, nom = arguments[arguments.index('--uuid') + 1], arguments[arguments.index('--name') + 1]
            self.machinesVirtuel[numéro] = {'UUID': numéro, 'name': nom, 'VMState': 'poweroff',
                'CfgFile': str(self.valeurRacine / '.vbox/machines' / nom / (nom + '.vbox')), 'owner': None}
            return ''
        machine = self.machinesVirtuel[arguments[2]]
        if action == 'showvminfo':
            return '\n'.join('{}={}'.format(json.dumps(nom), json.dumps(valeur)) for nom, valeur in machine.items() if nom != 'owner')
        if action == 'getextradata': return 'Value: ' + machine['owner'] if machine['owner'] else 'No value set!'
        if action == 'setextradata': machine['owner'] = arguments[4]
        elif action == 'storagectl': machine['storagecontrollername0'] = 'JKOROS IDE'
        elif action == 'storageattach': machine['JKOROS IDE-0-0'] = arguments[arguments.index('--medium') + 1]
        elif action == 'startvm': machine['VMState'] = 'running'
        elif action == 'controlvm':
            assert arguments[3] == 'resume'
            machine['VMState'] = 'running'
        elif action != 'modifyvm': raise AssertionError(arguments)
        return ''


class testLancer(unittest.TestCase):
    def setUp(self):
        self.valeurTemporaire = tempfile.TemporaryDirectory(prefix='jkoros-vbox-test-')
        self.addCleanup(self.valeurTemporaire.cleanup)
        self.valeurRacine = Path(self.valeurTemporaire.name)
        (self.valeurRacine / '.vbox').mkdir()
        self.valeurBoîte = BoîteFactice(self.valeurRacine)
        self.exécuterCommande = valeurModule.LanceurProgramme(self.valeurRacine, 'jkoros operating system', commande=self.valeurBoîte)

    def créerEntréeÉlément(self):
        résultat = self.exécuterCommande.exécuterCommande()
        self.valeurBoîte.listeCommandes.clear()
        return self.valeurBoîte.machinesVirtuel[résultat['uuid']]

    def estInchangé(self):
        self.assertTrue(all(commande[0] == 'VBoxManage' and commande[1] in ('list', 'showvminfo', 'getextradata') for commande in self.valeurBoîte.listeCommandes))

    def testAmorçageOptiqueEtCréationInitialValeur(self):
        résultat = self.exécuterCommande.exécuterCommande()
        self.assertEqual(résultat['state'], 'running')
        self.assertTrue(Path(résultat['iso']).is_file())
        self.assertTrue(any('--nic1' in commande and 'none' in commande for commande in self.valeurBoîte.listeCommandes))
        self.assertFalse(any('hdd' in commande or 'discardstate' in commande or 'createmedium' in commande for commande in self.valeurBoîte.listeCommandes))

    def testPréservéMachineVirtuelleEnExécution(self):
        self.créerEntréeÉlément()
        self.assertEqual(self.exécuterCommande.exécuterCommande()['state'], 'running')
        self.estInchangé()

    def testPréservationJournalEtReprendreÉtatValeurEnregistré(self):
        machine = self.créerEntréeÉlément()
        machine['VMState'] = 'saved'
        valeurJournal = self.exécuterCommande.chemin(self.exécuterCommande.lire()['serial_log'])
        valeurJournal.write_text('saved log')
        self.exécuterCommande.exécuterCommande()
        self.assertFalse(any(commande[0] == 'make' or commande[1] == 'modifyvm' for commande in self.valeurBoîte.listeCommandes))
        self.assertEqual([chemin.read_text() for chemin in valeurJournal.parent.glob('before-resume-*.log')], ['saved log'])

    def testReprendreEtMettreEnPause(self):
        self.créerEntréeÉlément()['VMState'] = 'paused'
        self.exécuterCommande.exécuterCommande()
        self.assertTrue(any(commande[1] == 'controlvm' and commande[3] == 'resume' for commande in self.valeurBoîte.listeCommandes))
        self.assertFalse(any(commande[0] == 'make' for commande in self.valeurBoîte.listeCommandes))

    def testCollisionNomMachineVirtuelleAutre(self):
        self.valeurBoîte.machinesVirtuel[str(uuid.uuid4())] = {'name': 'jkoros operating system'}
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()
        self.estInchangé()

    def testRejetéMarqueurPropriété(self):
        self.créerEntréeÉlément()['owner'] = 'someone-else'
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()
        self.estInchangé()

    def testRejetéCheminRéglagesAutre(self):
        self.créerEntréeÉlément()['CfgFile'] = '/tmp/someone-else.vbox'
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()
        self.estInchangé()

    def testPréservéDisqueUtilisateurSupplémentaire(self):
        machine = self.créerEntréeÉlément()
        machine['VMState'] = 'poweroff'
        machine['JKOROS IDE-0-1'] = '/external/user.vdi'
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()
        self.estInchangé()

    def testRejetéTransition(self):
        self.créerEntréeÉlément()['VMState'] = 'saving'
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()
        self.estInchangé()

    def testRejetéDésinscrire(self):
        self.créerEntréeÉlément()
        self.valeurBoîte.machinesVirtuel.clear()
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()
        self.estInchangé()

    def testÉchecConstruireActivéPréservéMachineVirtuelle(self):
        machine = self.créerEntréeÉlément()
        machine['VMState'] = 'poweroff'
        élémentListePrécédentÉlément = dict(machine)
        self.valeurBoîte.valeurÉchec = 'make'
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()
        self.assertEqual(machine, élémentListePrécédentÉlément)

    def testRécupérationMarqueurPropriétéInterrompu(self):
        self.valeurBoîte.valeurÉchec = 'setextradata'
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()
        self.valeurBoîte.listeCommandes.clear()
        self.assertEqual(self.exécuterCommande.exécuterCommande()['state'], 'running')
        self.assertFalse(any(commande[1] == 'createvm' for commande in self.valeurBoîte.listeCommandes))

    def testRejetéAltérationISOPréservé(self):
        machine = self.créerEntréeÉlément()
        machine['VMState'] = 'poweroff'
        Path(machine['JKOROS IDE-0-0']).write_bytes(b'changed')
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.exécuterCommande()

    def testCrééÉtatValeurAucun(self):
        self.assertEqual(self.exécuterCommande.afficherÉtatValeur()['state'], 'not-created')
        self.assertFalse(self.valeurBoîte.listeCommandes)

    def testRejetéÉchapperChemin(self):
        for chemin in ('../outside', '/tmp/outside'):
            with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.chemin(chemin)
        (self.valeurRacine / '.vbox/media').symlink_to('/tmp')
        with self.assertRaises(valeurModule.erreurExécution): self.exécuterCommande.chemin('media/kernel.iso')

    def testPropriétésComposite52VirtualBox(self):
        résultat = valeurModule.valeurAttribut('VMState="running"\nVideoMode="720,400,0"@0,0 1\n"IDE-0-0"="/a b.iso"')
        self.assertEqual(résultat['VMState'], 'running')
        self.assertEqual(résultat['IDE-0-0'], '/a b.iso')


if __name__ == '__main__': unittest.main()
