#include "ABIRéseau.h"
static AdressePriseRéseauInternet adresse(unsigned valeurPort) {
    AdressePriseRéseauInternet valeur = {}; valeur.familleAdresse = FamilleInternet;
    valeur.numéroPort = courtRéseau(valeurPort); valeur.AdresseInternet.valeurAdresse = entierRéseau(adresseBoucleRetour); return valeur;
}
extern "C" int démarrerProgrammeUtilisateur(int) {
    int extrémitéÉmissionEnCours = créerExtrémité(FamilleInternet, PriseRéseauDatagramme, 0);
    int extrémitéRécepteur = créerExtrémité(FamilleInternet, PriseRéseauDatagramme, ProtocoleDatagramme);
    if (extrémitéÉmissionEnCours < 0 || extrémitéRécepteur < 0) return 1;
    AdressePriseRéseauInternet valeurArrivée = adresse(7777), valeurDépart = adresse(7778), adresseEnvoyé = {};
    typeLongueurAdressePriseRéseau longueurAdresse = sizeof(adresseEnvoyé);
    if (associerAdresse(extrémitéRécepteur, (AdressePriseRéseau *)&valeurArrivée, sizeof(valeurArrivée))) return 2;
    if (associerAdresse(extrémitéÉmissionEnCours, (AdressePriseRéseau *)&valeurArrivée, sizeof(valeurArrivée)) != -1 || numéroErreur != 98) return 3;
    if (associerAdresse(extrémitéÉmissionEnCours, (AdressePriseRéseau *)&valeurDépart, sizeof(valeurDépart))) return 4;
    static const char valeurContenuValeur[] = "한글 UDP loopback 😀";
    char valeurReçu[64] = {};
    if (envoyerDonnéesDatagramme(extrémitéÉmissionEnCours, valeurContenuValeur, sizeof(valeurContenuValeur), 0, (AdressePriseRéseau *)&valeurArrivée, sizeof(valeurArrivée)) != sizeof(valeurContenuValeur)) return 5;
    if (recevoirDonnéesDatagramme(extrémitéRécepteur, (void *)valeurContenuValeur, sizeof(valeurContenuValeur), 0, 0, 0) != -1 || numéroErreur != 14) return 6;
    if (recevoirDonnéesDatagramme(extrémitéRécepteur, valeurReçu, sizeof(valeurReçu), 0, (AdressePriseRéseau *)&adresseEnvoyé, &longueurAdresse) != sizeof(valeurContenuValeur)) return 7;
    if (longueurAdresse != sizeof(adresseEnvoyé) || courtOrdrePériphérique(adresseEnvoyé.numéroPort) != 7778 || entierOrdrePériphérique(adresseEnvoyé.AdresseInternet.valeurAdresse) != adresseBoucleRetour) return 8;
    for (unsigned indiceOrdinal = 0; indiceOrdinal < sizeof(valeurContenuValeur); indiceOrdinal++) if (valeurReçu[indiceOrdinal] != valeurContenuValeur[indiceOrdinal]) return 9;
    if (recevoirDonnéesDatagramme(extrémitéRécepteur, valeurReçu, sizeof(valeurReçu), 0, 0, 0) != -1 || numéroErreur != 11) return 10;
    if (envoyerDonnéesDatagramme(extrémitéRécepteur, valeurReçu, sizeof(valeurContenuValeur), 0, (AdressePriseRéseau *)&adresseEnvoyé, sizeof(adresseEnvoyé)) != sizeof(valeurContenuValeur)) return 11;
    if (recevoirDonnéesDatagramme(extrémitéÉmissionEnCours, valeurReçu, 4, 0, 0, 0) != 4) return 12;
    if (recevoirDonnéesDatagramme(extrémitéÉmissionEnCours, valeurReçu, 4, 0, 0, 0) != -1 || numéroErreur != 11) return 13;
    for (int indiceOrdinal = 0; indiceOrdinal < 4; indiceOrdinal++) if (envoyerDonnéesDatagramme(extrémitéÉmissionEnCours, valeurContenuValeur, sizeof(valeurContenuValeur), 0, (AdressePriseRéseau *)&valeurArrivée, sizeof(valeurArrivée)) != sizeof(valeurContenuValeur)) return 14;
    if (envoyerDonnéesDatagramme(extrémitéÉmissionEnCours, valeurContenuValeur, sizeof(valeurContenuValeur), 0, (AdressePriseRéseau *)&valeurArrivée, sizeof(valeurArrivée)) != -1 || numéroErreur != 11) return 15;
    for (int indiceOrdinal = 0; indiceOrdinal < 4; indiceOrdinal++) if (recevoirDonnéesDatagramme(extrémitéRécepteur, valeurReçu, sizeof(valeurReçu), 0, 0, 0) != sizeof(valeurContenuValeur)) return 16;
    if (envoyerDonnéesDatagramme(extrémitéÉmissionEnCours, 0, 0, 0, (AdressePriseRéseau *)&valeurArrivée, sizeof(valeurArrivée)) != 0 ||
        recevoirDonnéesDatagramme(extrémitéRécepteur, 0, 0, 0, 0, 0) != 0) return 21;
    valeurArrivée.AdresseInternet.valeurAdresse = entierRéseau(0x08080808);
    if (envoyerDonnéesDatagramme(extrémitéÉmissionEnCours, valeurContenuValeur, sizeof(valeurContenuValeur), 0, (AdressePriseRéseau *)&valeurArrivée, sizeof(valeurArrivée)) != -1 || numéroErreur != 101) return 17;
    if (créerExtrémité(FamilleInternet, RéseauFlux, ProtocoleDatagramme) != -1 || numéroErreur != 93) return 18;
    longueurAdresse = sizeof(adresseEnvoyé);
    if (lireAdressePriseRéseau(extrémitéRécepteur, (AdressePriseRéseau *)&adresseEnvoyé, &longueurAdresse) || courtOrdrePériphérique(adresseEnvoyé.numéroPort) != 7777) return 19;
    if (fermerFichier(extrémitéRécepteur) || fermerFichier(extrémitéRécepteur) != -1 || numéroErreur != 9) return 20;
    // 보내는곳은 열어 둔다: programmeQuitter 시 프로세스별 socket 정리를 검사한다.
    static const char estTerminé[] = "EL0 UDP LOOPBACK PASS (external network unavailable)\n";
    écrireDonnéesFichier(1, estTerminé, sizeof(estTerminé) - 1);
    return 0;
}
