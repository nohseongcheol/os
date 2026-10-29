#include "ABIRéseau.h"

int démarrerProgrammeUtilisateur(int arguments) {
    (void)arguments;
    struct AdressePriseRéseauInternet adresse = {0};
    adresse.familleAdresse = FamilleInternet;
    adresse.numéroPort = courtRéseau(9260);
    adresse.AdresseInternet.valeurAdresse = entierRéseau(adresseBoucleRetour);
    int valeurServeur = créerExtrémité(FamilleInternet, RéseauFlux, protocoleTransportFlux);
    if (valeurServeur < 0 || associerAdresse(valeurServeur, (struct AdressePriseRéseau *)&adresse, sizeof(adresse)) < 0 ||
        attendreConnexionRéseauPour(valeurServeur, 4) < 0) return 1;
    if (accepterConnexionRéseau(valeurServeur, 0, 0) != -1 || numéroErreur != 11) return 2;
    int valeurInvité = créerExtrémité(FamilleInternet, RéseauFlux, protocoleTransportFlux);
    if (valeurInvité < 0 || connecterRéseau(valeurInvité, (struct AdressePriseRéseau *)&adresse, sizeof(adresse)) < 0) return 3;
    int connecter = accepterConnexionRéseau(valeurServeur, 0, 0);
    if (connecter < 0) return 4;
    unsigned char envoyerVersÉlémentListe[1500], élémentListeReçu[1500];
    for (int nombre = 0; nombre < 1500; nombre++) envoyerVersÉlémentListe[nombre] = (unsigned char)nombre;
    int nombreÉlémentsEnvoyé = 0;
    while (nombreÉlémentsEnvoyé < 1024) {
        int longueur = écrireDonnéesFichier(valeurInvité, envoyerVersÉlémentListe + nombreÉlémentsEnvoyé, sizeof(envoyerVersÉlémentListe) - nombreÉlémentsEnvoyé);
        if (longueur <= 0) return 5;
        nombreÉlémentsEnvoyé += longueur;
    }
    if (écrireDonnéesFichier(valeurInvité, envoyerVersÉlémentListe, 1) != -1 || numéroErreur != 11) return 6;
    /* 상대가 닫아도 이미 도착한 자료를 construireTous 읽은 valeurRetourArrièreCôté EOF가 된다. */
    fermerFichier(valeurInvité);
    int nombreÉlémentsReçu = 0;
    while (nombreÉlémentsReçu < nombreÉlémentsEnvoyé) {
        int longueur = lireDonnéesFichier(connecter, élémentListeReçu + nombreÉlémentsReçu, sizeof(élémentListeReçu) - nombreÉlémentsReçu);
        if (longueur <= 0) return 7;
        nombreÉlémentsReçu += longueur;
    }
    for (int nombre = 0; nombre < nombreÉlémentsReçu; nombre++) if (élémentListeReçu[nombre] != envoyerVersÉlémentListe[nombre]) return 8;
    if (lireDonnéesFichier(connecter, élémentListeReçu, 1) != 0) return 9;
    if (écrireDonnéesFichier(connecter, envoyerVersÉlémentListe, 1) != -1 || numéroErreur != 32) return 10;
    fermerFichier(connecter); fermerFichier(valeurServeur);
    const char résultat[] = "C posix-kor 연결형 Communication PASS\n";
    écrireDonnéesFichier(1, résultat, sizeof(résultat) - 1);
    return 0;
}
