// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Wallis_et_Futuna.JWlfOS.Tests;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Wallis_et_Futuna.JWlfOS.EspaceMémoire.GestionnaireMémoire;
import Wallis_et_Futuna.JWlfOS.EspaceMémoire.GestionnairePage;
import Wallis_et_Futuna.JWlfOS.valeurEntrée.évènementEntrée;
import Wallis_et_Futuna.JWlfOS.Tâche.valeurProcessus;
import Wallis_et_Futuna.JWlfOS.AppelSystème.AppelSystème;
import Wallis_et_Futuna.JWlfOS.SystèmeFichier.ChargeurCodeExécutable;
import Wallis_et_Futuna.JWlfOS.Noyau.Noyau;
import Wallis_et_Futuna.JWlfOS.Hôte.MatérielHôte;
import Wallis_et_Futuna.JWlfOS.interrompre.GestionnaireInterrompre;
import Wallis_et_Futuna.JWlfOS.entréeÉlémentDescripteur.TableDescripteurGlobal;
import Wallis_et_Futuna.JWlfOS.périphériqueStockage.PièceJointeTechnologieAvancé;
import Wallis_et_Futuna.JWlfOS.Périphérique.GestionnaireBusPériphériqueMatériel;
import Wallis_et_Futuna.JWlfOS.PileRéseau.OutilsRéseau;
import Wallis_et_Futuna.JWlfOS.PileRéseau.CoucheRéseau;
import Wallis_et_Futuna.JWlfOS.Périphérique.Horloge;
import Wallis_et_Futuna.JWlfOS.entréeÉlémentDescripteur.SegmentÉtatValeurTâche;
import Wallis_et_Futuna.JWlfOS.Écran.présenterCaractère;
import Wallis_et_Futuna.JWlfOS.SystèmeFichier.tablePartitionPrimaire;

public final class testTous {
    private static int nombreÉlémentsPassage;

    private testTous() {
    }

    public static void main(String[] argumentParamètre) {
        MatérielHôte Périphérique = new MatérielHôte();
        Noyau valeurNoyau = new Noyau(Périphérique);
        valeurNoyau.lancer();

        testMémoire(valeurNoyau);
        testGestionPage(valeurNoyau);
        testProcessusListeEtFichiers(valeurNoyau);
        testELF(valeurNoyau);
        testEntrée(valeurNoyau);
        testMatériel(Périphérique);
        testDescripteursEtInterruptions();
        testMiseEnRéseauEtStockage();
        testHorlogeEtÉcran();

        System.out.println("JWlfOS Tests valeurPassage: " + nombreÉlémentsPassage);
    }

    private static void testMémoire(Noyau valeurNoyau) {
        GestionnaireMémoire valeurGestionnaire = valeurNoyau.EspaceMémoire();
        int adressePremier = valeurGestionnaire.allouerAligné(100, 64);
        vérifier((adressePremier & 63) == 0, "valeurAligner allouerStockage");
        valeurGestionnaire.écrireValeurOctet(adressePremier, (byte) 0x5a);
        vérifier(valeurGestionnaire.lireValeurOctet(adressePremier) == (byte) 0x5a, "물리 EspaceMémoire 읽고 écrire");
        int utiliserAvant = valeurGestionnaire.tailleUtilisé();
        valeurGestionnaire.libérerStockage(adressePremier);
        vérifier(valeurGestionnaire.tailleUtilisé() < utiliserAvant, "EspaceMémoire libérerStockage");
    }

    private static void testGestionPage(Noyau valeurNoyau) {
        GestionnairePage valeurGestionnaire = valeurNoyau.gestionPage();
        GestionnairePage.EspaceAdresse espaceParent = valeurGestionnaire.espaceAdresseNouveau();
        valeurGestionnaire.pageTableCorrespondance(espaceParent, 0x1000, true);
        valeurGestionnaire.écrireValeurOctet(espaceParent, 0x1010, (byte) 7);
        GestionnairePage.EspaceAdresse espaceEnfant = valeurGestionnaire.écrireActivéCopierCloner(espaceParent);
        valeurGestionnaire.écrireValeurOctet(espaceEnfant, 0x1010, (byte) 9);
        vérifier(valeurGestionnaire.lireValeurOctet(espaceParent, 0x1010) == 7, "écrire 시 copierValeur valeurParent 격리");
        vérifier(valeurGestionnaire.lireValeurOctet(espaceEnfant, 0x1010) == 9, "écrire 시 copierValeur valeurEnfant écrire");
    }

    private static void testProcessusListeEtFichiers(Noyau valeurNoyau) {
        byte[] valeurContenuValeur = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        valeurNoyau.SystèmeFichier().ajouterFinFichier("Tests", valeurContenuValeur);
        valeurProcessus valeurParent = valeurNoyau.processusPremier();
        AppelSystème invoquer = valeurNoyau.AppelSystème();
        int entréeÉlémentDescripteur = invoquer.ouvrir(valeurParent, "/Tests", AppelSystème.lireDrapeauSeulement);
        vérifier(entréeÉlémentDescripteur >= 3, "Fichier ouvrir");

        byte[] recevoirDestination = new byte[valeurContenuValeur.length];
        vérifier(invoquer.lire(valeurParent, entréeÉlémentDescripteur, recevoirDestination, recevoirDestination.length) == valeurContenuValeur.length, "Fichier lire");
        vérifier(Arrays.equals(valeurContenuValeur, recevoirDestination), "Fichier valeurContenuValeur");
        vérifier(invoquer.positionDéplacer(valeurParent, entréeÉlémentDescripteur, 0, AppelSystème.chercherDémarrer) == 0, "Fichier position valeurDéplacer");

        int descripteurCloné = invoquer.descripteurDuplicata(valeurParent, entréeÉlémentDescripteur);
        vérifier(descripteurCloné >= 0, "entréeÉlémentDescripteur valeurCloner");
        valeurProcessus valeurEnfant = invoquer.processusCloner(valeurParent);
        vérifier(valeurEnfant.valeurIdentificateur() != valeurParent.valeurIdentificateur(), "valeurProcessus valeurIdentificateur 분리");
        vérifier(valeurEnfant.identificateurParent() == valeurParent.valeurIdentificateur(), "valeurParent valeurProcessus valeurIdentificateur");
        vérifier(invoquer.fermer(valeurEnfant, entréeÉlémentDescripteur) == 0 && valeurParent.descripteurFichier().estOuvrir(entréeÉlémentDescripteur), "valeurEnfant fermer 격리");

        int finPrécédentÉlément = invoquer.augmenterRompreProgramme(valeurParent, 8192);
        vérifier(finPrécédentÉlément == 0x06000000, "Programme terminaison 늘리기");
        vérifier(valeurParent.rompreProgramme() == 0x06002000, "Programme terminaison 반영");
        vérifier(valeurEnfant.rompreProgramme() == 0x06000000, "과정별 Programme terminaison 격리");

        valeurEnfant.programmeQuitter(7);
        vérifier(invoquer.attendreEnfantPour(valeurParent, valeurEnfant.valeurIdentificateur(), false) == (7 << 8), "valeurEnfant programmeQuitter attendreFin");
        vérifier(invoquer.estAccessible("Tests", 1) == -13, "exécuterCommande valeurPermission rejeterValeur");
        vérifier(invoquer.identificateurUtilisateur() == 0 && invoquer.identificateurGroupe() == 0, "사용자와 무리 valeurIdentificateur");
        vérifier("/".equals(invoquer.listeTâcheActuel(2)) && invoquer.listeTâcheCommuter("/") == 0, "élémentListeActuel Tâche listeEntréeÉlément");
        vérifier(invoquer.estTerminal(valeurParent, 1), "표준 Sortie EntréeSortieTerminal");
        vérifier("JWlfOS".equals(invoquer.détailsSystème().nomSystème()), "valeurSystèmeExploitation informationSystème");
    }

    private static void testELF(Noyau valeurNoyau) {
        byte[] Données = new byte[92];
        Données[0] = 0x7f;
        Données[1] = 'E';
        Données[2] = 'L';
        Données[3] = 'F';
        Données[4] = 1;
        Données[5] = 1;
        écrireValeurEntier(Données, 24, 0x04001000);
        écrireValeurEntier(Données, 32, 52);
        écrireEntierCourt(Données, 46, 40);
        écrireEntierCourt(Données, 48, 1);
        écrireValeurEntier(Données, 56, 8);
        écrireValeurEntier(Données, 60, 2);
        écrireValeurEntier(Données, 64, 0x04002000);
        écrireValeurEntier(Données, 72, 64);

        ChargeurCodeExécutable.image valeurImage = new ChargeurCodeExécutable().Contrôles(Données);
        vérifier(valeurImage.démarrerAdresse() == 0x04001000, "ELF lancer adresse");
        vérifier(valeurImage.listeSections().size() == 1 && valeurImage.listeSections().get(0).valeurGenre() == 8, "ELF 빈 Données valeurSection");
        int entréeÉlémentDescripteur = valeurNoyau.AppelSystème().ouvrir(valeurNoyau.processusPremier(), "Tests", AppelSystème.lireDrapeauSeulement);
        vérifier(valeurNoyau.AppelSystème().contrôleFichier(valeurNoyau.processusPremier(), entréeÉlémentDescripteur, 2, 1) == 0, "exécuterCommande 시 fermer réglages");
        vérifier(valeurNoyau.AppelSystème().exécuterCommande(valeurNoyau.processusPremier(), Données, new String[] {"Tests", "값"}, new String[] {"Langue=français"}) == 0, "ELF exécuterCommande valeurImage 적재");
        vérifier(valeurNoyau.processusPremier().adresseDémarrerExécution() == 0x04001000, "exécuterCommande lancer adresse 반영");
        vérifier(valeurNoyau.processusPremier().argumentExécution().length == 2 && valeurNoyau.processusPremier().valeurEnvironnement().length == 1, "exécuterCommande 인자와 environnement");
        vérifier(!valeurNoyau.processusPremier().descripteurFichier().estOuvrir(entréeÉlémentDescripteur), "exécuterCommande 시 entréeÉlémentDescripteur fermer");
        vérifier(valeurNoyau.gestionPage().lireValeurOctet(valeurNoyau.processusPremier().EspaceAdresse(), 0x04002000) == 0, "빈 Données valeurSection opérandeZéro initialiser");
    }

    private static void testEntrée(Noyau valeurNoyau) {
        valeurNoyau.GestionEntrée().basDirectionTouche('가');
        valeurNoyau.GestionEntrée().mouvementSouris(3, -2);
        évènementEntrée évènementPremier = valeurNoyau.GestionEntrée().évènementSuivant();
        évènementEntrée évènementDeuxième = valeurNoyau.GestionEntrée().évènementSuivant();
        vérifier(évènementPremier.genreÉvènement() == évènementEntrée.valeurGenre.basDirectionTouche, "자판 évènement");
        vérifier(évènementDeuxième.valeurPremier() == 3 && évènementDeuxième.valeurDeuxième() == -2, "쥐 valeurDéplacer évènement");
    }

    private static void testMatériel(MatérielHôte Périphérique) {
        Périphérique.écrireOctetPort(0x3f8, 0xab);
        vérifier(Périphérique.lireOctetPort(0x3f8) == 0xab, "portMatériel sortieEntrée valeurFrontière");
        vérifier(Périphérique.journalSériel().contains("JWlfOS"), "valeurSériel enregistrementJournal");
    }

    private static void testDescripteursEtInterruptions() {
        GestionnaireInterrompre valeurGestionnaire = new GestionnaireInterrompre();
        valeurGestionnaire.registreEntréeÉlément(0x21, adresseStockage -> adresseStockage + 4);
        valeurGestionnaire.activer();
        vérifier(valeurGestionnaire.distribuerValeur(0x21, 100) == 104, "interrompre distribuerValeur");
        valeurGestionnaire.désactiver();
        vérifier(valeurGestionnaire.distribuerValeur(0x21, 100) == 100, "interrompre désactiver");

        TableDescripteurGlobal tableDescripteur = new TableDescripteurGlobal();
        tableDescripteur.définirValeurDéfaut();
        vérifier(tableDescripteur.listeFragments().size() == 5, "전역 tableDescripteur");
        SegmentÉtatValeurTâche étatValeurTâche = new SegmentÉtatValeurTâche();
        étatValeurTâche.définirPilePrivilégié(0x10, 0x800000);
        vérifier(étatValeurTâche.blocZéroPile() == 0x10 && étatValeurTâche.adresseZéroPile() == 0x800000, "Tâche valeurÉtatValeur valeurSection");
    }

    private static void testMiseEnRéseauEtStockage() {
        PièceJointeTechnologieAvancé périphériqueStockage = new PièceJointeTechnologieAvancé(4, false);
        byte[] écrireVersDonnées = new byte[PièceJointeTechnologieAvancé.tailleSection];
        byte[] lireValeurDonnées = new byte[PièceJointeTechnologieAvancé.tailleSection];
        écrireVersDonnées[17] = 42;
        périphériqueStockage.écrire(2, écrireVersDonnées);
        périphériqueStockage.lire(2, lireValeurDonnées);
        vérifier(lireValeurDonnées[17] == 42, "ATA valeurSection 읽고 écrire");

        GestionnaireBusPériphériqueMatériel périphériqueMatériel = new GestionnaireBusPériphériqueMatériel();
        périphériqueMatériel.valeurDécouvert(new GestionnaireBusPériphériqueMatériel.Périphérique(0x1022, 0x2000, 0xc000, 11));
        vérifier(périphériqueMatériel.trouverEntréeÉlément(0x1022, 0x2000) != null, "주변 Périphérique trouverEntréeÉlément");

        byte[] cadreEthernet = new byte[34];
        cadreEthernet[12] = 0x08;
        cadreEthernet[13] = 0x00;
        cadreEthernet[14] = 0x45;
        vérifier(OutilsRéseau.protocoleSupérieurEthernet(cadreEthernet) == 0x0800, "이더넷 상위 valeurContrat");
        vérifier(OutilsRéseau.estProtocole4VersionIP(cadreEthernet, 14), "상호통신망규약 4판");
        vérifier(OutilsRéseau.sommeContrôleInternet(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 sommeContrôle");

        byte[] sectionPremier = new byte[512];
        sectionPremier[510] = 0x55;
        sectionPremier[511] = (byte) 0xaa;
        sectionPremier[450] = 0x0b;
        écrireValeurEntier(sectionPremier, 454, 63);
        écrireValeurEntier(sectionPremier, 458, 1024);
        vérifier(new tablePartitionPrimaire().lire(sectionPremier).size() == 1, "valeurDéfaut 분할 영역표");

        CoucheRéseau valeurCouche = new CoucheRéseau();
        int[] nombreÉlémentsReçu = new int[1];
        valeurCouche.registreUnitéDonnéesUtilisateur(7, (Données, lancer, longueur) -> nombreÉlémentsReçu[0]++);
        byte[] indiceCadre = new byte[14 + 20 + 8];
        indiceCadre[12] = 0x08;
        indiceCadre[13] = 0x00;
        indiceCadre[14] = 0x45;
        indiceCadre[16] = 0;
        indiceCadre[17] = 28;
        indiceCadre[23] = 17;
        indiceCadre[36] = 0;
        indiceCadre[37] = 7;
        vérifier(valeurCouche.recevoirEthernet(indiceCadre) && nombreÉlémentsReçu[0] == 1, "Utilisateur Données valeurUnité distribuerValeur");
    }

    private static void testHorlogeEtÉcran() {
        présenterCaractère Écran = new présenterCaractère();
        Écran.Sortie("가나\n다");
        vérifier(Écran.Caractères(0, 0) == '가' && Écran.Caractères(0, 1) == '다', "Caractères Écran Sortie");
        Horloge Horloge = new Horloge(100);
        for (int numéro = 0; numéro < 10; numéro++) {
            Horloge.valeurBattement();
        }
        vérifier(Horloge.millisecondesÉcoulé() == 100, "Horloge valeurBattement convertirValeur");
    }

    private static void écrireValeurEntier(byte[] Données, int position, int valeur) {
        Données[position] = (byte) valeur;
        Données[position + 1] = (byte) (valeur >>> 8);
        Données[position + 2] = (byte) (valeur >>> 16);
        Données[position + 3] = (byte) (valeur >>> 24);
    }

    private static void écrireEntierCourt(byte[] Données, int position, int valeur) {
        Données[position] = (byte) valeur;
        Données[position + 1] = (byte) (valeur >>> 8);
    }

    private static void vérifier(boolean condition, String nom) {
        if (!condition) {
            throw new AssertionError("valeurÉchec: " + nom);
        }
        nombreÉlémentsPassage++;
        System.out.println("valeurPassage: " + nom);
    }
}
