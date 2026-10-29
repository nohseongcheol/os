// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import français.interne.*;

/** Test du contrat de communication exécutant le même bytecode sur OpenJDK et sur la JVM du projet. */
public class testMiseEnRéseauCoréen {
    public static void main(String[] arguments) throws ExceptionSortieEntrée {
        recevoirPort valeurPort = transportConnexion.ouvrirRécepteur(0);
        Connexion valeurInvité = transportConnexion.ouvrir("127.0.0.1", valeurPort.numéroPort());
        Connexion identificateurPropriétaire = valeurPort.recevoir();
        valeurInvité.délaiExpiration(200); identificateurPropriétaire.délaiExpiration(200);
        Contrôles.exiger(valeurInvité.connecté() && !valeurInvité.estFermé(), "connecter valeurÉtatValeur");
        Contrôles.exiger(identificateurPropriétaire.numéroPort() == valeurInvité.numéroPortLocal(), "valeurPairRéseau numéroPort");
        Contrôles.exiger(valeurInvité.numéroPort() == identificateurPropriétaire.numéroPortLocal(), "portéeLocal numéroPort");
        FluxEntrée valeurEntrée = identificateurPropriétaire.valeurEntrée(); FluxSortie pageSortie = valeurInvité.Sortie();
        byte[] message = Caractères.encoder("한글 valeurFlux");
        pageSortie.écrire(message, 0, message.length); pageSortie.émettreValeur();
        byte[] texteReçu = new byte[message.length];
        int lireNombreÉléments = 0;
        while (lireNombreÉléments < texteReçu.length) {
            int lireSupplémentaire = valeurEntrée.lire(texteReçu, lireNombreÉléments, texteReçu.length - lireNombreÉléments);
            Contrôles.exiger(lireSupplémentaire > 0, "예상하지 않은 Fichier terminaison"); lireNombreÉléments += lireSupplémentaire;
        }
        Contrôles.exiger(Caractères.texteÉgal(Caractères.déchiffrerDonnées(texteReçu), "한글 valeurFlux"), "valeurSousPartie 읽기와 écrire");
        pageSortie.écrire(new byte[] {17, 18});
        byte[] lireCourt = new byte[2];
        int lirePremier = valeurEntrée.lire(lireCourt);
        Contrôles.exiger(lirePremier > 0 && lireCourt[0] == 17, "valeurTableau lire");
        if (lirePremier == 1) lireCourt[1] = (byte)valeurEntrée.lire();
        Contrôles.exiger(lireCourt[1] == 18, "valeurResteDivision lire");
        identificateurPropriétaire.Sortie().écrire(255);
        Contrôles.exiger(valeurInvité.valeurEntrée().lire() == 255, "valeurEncodage 없는 한 valeurOctet");
        pageSortie.fermer();
        Contrôles.exiger(valeurInvité.estFermé() && valeurEntrée.lire() == -1, "닫기와 Fichier terminaison");
        valeurEntrée.fermer(); Contrôles.exiger(identificateurPropriétaire.estFermé(), "valeurEntrée valeurFlux fermer");
        valeurInvité.fermer(); identificateurPropriétaire.fermer();
        valeurPort.délaiExpiration(15);
        boolean délaiExpirationExécution = false;
        try { valeurPort.recevoir(); } catch (ExceptionDélaiExpirationAttendre erreurAttendu) { délaiExpirationExécution = true; }
        Contrôles.exiger(délaiExpirationExécution, "recevoirValeur délaiExpiration");
        valeurPort.fermer(); Contrôles.exiger(valeurPort.estFermé(), "recevoirPort fermer");
        CanalDatagramme extrémitéRécepteur = CanalDatagramme.ouvrir(0), extrémitéÉmissionEnCours = CanalDatagramme.ouvrir(0);
        extrémitéRécepteur.délaiExpiration(200);
        extrémitéÉmissionEnCours.envoyer("127.0.0.1", extrémitéRécepteur.numéroPort(), "datagramme 한글");
        Contrôles.exiger(Caractères.texteÉgal(extrémitéRécepteur.recevoir(), "datagramme 한글"), "datagramme 송수신");
        extrémitéÉmissionEnCours.fermer(); extrémitéRécepteur.fermer();
        Contrôles.exiger(extrémitéÉmissionEnCours.estFermé() && extrémitéRécepteur.estFermé(), "datagramme fermer");
        Sortie.écrireLigne("français Communication vérifier: connecter datagramme valeurFlux délaiExpirationExécution fermer");
    }
}
