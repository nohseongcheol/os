#include "../nommage/nomsLierMachine.h"
// AOT 슬롯은 uintptr_t. Java 도구의 Fichier/Sortie/인수는 construireTous EL0 SVC를 거친다.
#include "invoquer.h"
#include "java-resources.h"
#include "Paquet.h"
typedef uintptr_t motMachine;
static int valeurCatégorie;
static int actifJAR, décalerJAR;
static motMachine argumentTransféré[8][257];
static unsigned substitutUnicodeEnAttente;
extern int32_t entréeÉlémentJava(void);
static intptr_t invoquer(unsigned nombreÉlémentsÉlémentListe, motMachine valeurPremier, motMachine valeurDeuxième, motMachine codeCaractère) {
    return invoquerUtilisateur(nombreÉlémentsÉlémentListe, valeurPremier, valeurDeuxième, codeCaractère, 0, 0, 0);
}
static void valeursOctet(const char *positionDonnées, size_t nombreÉlémentsÉlémentListe) { invoquer(1, 1, (motMachine)positionDonnées, nombreÉlémentsÉlémentListe); }
static void caractère(unsigned codeCaractère) {
    unsigned char Données[4]; unsigned nombreÉlémentsÉlémentListe = 0;
    if (codeCaractère < 128) Données[nombreÉlémentsÉlémentListe++] = codeCaractère;
    else if (codeCaractère < 2048) { Données[nombreÉlémentsÉlémentListe++] = 0xc0 | (codeCaractère >> 6); Données[nombreÉlémentsÉlémentListe++] = 0x80 | (codeCaractère & 63); }
    else if (codeCaractère < 65536) { Données[nombreÉlémentsÉlémentListe++] = 0xe0 | (codeCaractère >> 12); Données[nombreÉlémentsÉlémentListe++] = 0x80 | ((codeCaractère >> 6) & 63); Données[nombreÉlémentsÉlémentListe++] = 0x80 | (codeCaractère & 63); }
    else { Données[nombreÉlémentsÉlémentListe++] = 0xf0 | (codeCaractère >> 18); Données[nombreÉlémentsÉlémentListe++] = 0x80 | ((codeCaractère >> 12) & 63); Données[nombreÉlémentsÉlémentListe++] = 0x80 | ((codeCaractère >> 6) & 63); Données[nombreÉlémentsÉlémentListe++] = 0x80 | (codeCaractère & 63); }
    valeursOctet((const char *)Données, nombreÉlémentsÉlémentListe);
}
motMachine caractèreOutil(motMachine valeur) {
    unsigned codeCaractère = valeur;
    if (substitutUnicodeEnAttente) {
        unsigned partieHaut = substitutUnicodeEnAttente; substitutUnicodeEnAttente = 0;
        if (codeCaractère >= 0xdc00 && codeCaractère <= 0xdfff) { caractère(0x10000 + ((partieHaut - 0xd800) << 10) + codeCaractère - 0xdc00); return 1; }
        caractère(0xfffd);
    }
    if (codeCaractère >= 0xd800 && codeCaractère <= 0xdbff) substitutUnicodeEnAttente = codeCaractère;
    else caractère(codeCaractère > 0x10ffff || (codeCaractère >= 0xdc00 && codeCaractère <= 0xdfff) ? 0xfffd : codeCaractère);
    return 1;
}
motMachine imprimerOutil(motMachine valeur) {
    const motMachine *donnéesChaîne = (const motMachine *)valeur;
    for (motMachine indiceOrdinal = 0; indiceOrdinal < donnéesChaîne[0]; indiceOrdinal++) caractèreOutil(donnéesChaîne[indiceOrdinal + 1]);
    return donnéesChaîne[0];
}
static int chemin(motMachine référenceObjet, char donnéesRésultat[512]) {
    const motMachine *valeurPremier = (const motMachine *)référenceObjet;
    unsigned capacitéUtilisé = 0;
    for (motMachine indiceOrdinal = 1; indiceOrdinal <= valeurPremier[0] && valeurPremier[indiceOrdinal]; indiceOrdinal++) {
        unsigned codeCaractère = valeurPremier[indiceOrdinal];
        // UTF-16 -> UTF-8. 기존 도구의 char[] modeMéthode 경로와 호환한다.
        if (codeCaractère >= 0xd800 && codeCaractère <= 0xdbff && indiceOrdinal < valeurPremier[0] && valeurPremier[indiceOrdinal + 1] >= 0xdc00 && valeurPremier[indiceOrdinal + 1] <= 0xdfff)
            { unsigned valeurBas = valeurPremier[++indiceOrdinal]; codeCaractère = 0x10000 + ((codeCaractère - 0xd800) << 10) + valeurBas - 0xdc00; }
        else if (codeCaractère >= 0xd800 && codeCaractère <= 0xdfff) return -22;
        unsigned nombreÉlémentsÉlémentListe = codeCaractère < 128 ? 1 : codeCaractère < 2048 ? 2 : codeCaractère < 65536 ? 3 : 4;
        if (capacitéUtilisé + nombreÉlémentsÉlémentListe > 511) return -36;
        if (nombreÉlémentsÉlémentListe == 1) donnéesRésultat[capacitéUtilisé++] = codeCaractère;
        else {
            donnéesRésultat[capacitéUtilisé++] = (nombreÉlémentsÉlémentListe == 2 ? 0xc0 : nombreÉlémentsÉlémentListe == 3 ? 0xe0 : 0xf0) | (codeCaractère >> (6 * (nombreÉlémentsÉlémentListe - 1)));
            for (unsigned ordinalInterne = nombreÉlémentsÉlémentListe - 1; ordinalInterne; ordinalInterne--) donnéesRésultat[capacitéUtilisé++] = 0x80 | ((codeCaractère >> (6 * (ordinalInterne - 1))) & 63);
        }
    }
    donnéesRésultat[capacitéUtilisé] = 0; return capacitéUtilisé ? 0 : -22;
}
motMachine ouvrirOutil(motMachine nom, motMachine bitsConfiguration) {
    char positionDonnées[512]; int erreur = chemin(nom, positionDonnées);
    return (uint32_t)(erreur ? erreur : invoquer(3, (motMachine)positionDonnées, bitsConfiguration, 0));
}
motMachine fermerOutil(motMachine poignéeFichier) { return (uint32_t)invoquer(4, poignéeFichier, 0, 0); }
motMachine octetLireOutil(motMachine poignéeFichier) {
    unsigned char valeurDeuxième; intptr_t nombreÉlémentsÉlémentListe = invoquer(2, poignéeFichier, (motMachine)&valeurDeuxième, 1);
    return (uint32_t)(nombreÉlémentsÉlémentListe == 1 ? valeurDeuxième : nombreÉlémentsÉlémentListe == 0 ? 256 : nombreÉlémentsÉlémentListe);
}
motMachine octetÉcrireOutil(motMachine poignéeFichier, motMachine valeur) {
    unsigned char valeurDeuxième = valeur; return (uint32_t)invoquer(1, poignéeFichier, (motMachine)&valeurDeuxième, 1);
}
motMachine lireOutil(motMachine nom, motMachine adresseDonnéesDestination) {
    if (actifJAR) {
        char positionDonnées[512]; int erreur = chemin(nom, positionDonnées); if (erreur) return (uint32_t)erreur;
        unsigned nombreÉlémentsÉlémentListe = 0; while (positionDonnées[nombreÉlémentsÉlémentListe]) nombreÉlémentsÉlémentListe++;
        if (nombreÉlémentsÉlémentListe >= 6) for (unsigned indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe - 6; indiceOrdinal++) if (positionDonnées[indiceOrdinal] == '.') positionDonnées[indiceOrdinal] = '/';
        unsigned char valeursOctet[16384]; motMachine *positionValeurDestination = (motMachine *)adresseDonnéesDestination;
        int nombreÉlémentsReçu = lireJAR(positionDonnées, valeursOctet, positionValeurDestination[0] < sizeof(valeursOctet) ? positionValeurDestination[0] : sizeof(valeursOctet));
        if (nombreÉlémentsReçu >= 0) { for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsReçu; indiceOrdinal++) positionValeurDestination[indiceOrdinal + 1] = valeursOctet[indiceOrdinal]; return nombreÉlémentsReçu; }
        if (nombreÉlémentsReçu != -2) return (uint32_t)nombreÉlémentsReçu;
    }
    int poignéeFichier = actifJAR ? -2 : (int32_t)ouvrirOutil(nom, 0);
    if (poignéeFichier < 0) {
        char positionDonnées[512]; int erreur = chemin(nom, positionDonnées); if (erreur) return (uint32_t)erreur;
        for (unsigned indiceOrdinal = 0; indiceOrdinal < sizeof(listeClasseJava) / sizeof(listeClasseJava[0]); indiceOrdinal++) {
            const char *décalageSuivant = listeClasseJava[indiceOrdinal].nom; unsigned ordinalInterne = 0;
            while (positionDonnées[ordinalInterne] && positionDonnées[ordinalInterne] == décalageSuivant[ordinalInterne]) ordinalInterne++;
            if (positionDonnées[ordinalInterne] || décalageSuivant[ordinalInterne]) continue;
            motMachine *positionValeurDestination = (motMachine *)adresseDonnéesDestination;
            if (positionValeurDestination[0] < listeClasseJava[indiceOrdinal].taille) return (uint32_t)-27;
            for (ordinalInterne = 0; ordinalInterne < listeClasseJava[indiceOrdinal].taille; ordinalInterne++) positionValeurDestination[ordinalInterne + 1] = listeClasseJava[indiceOrdinal].Données[ordinalInterne];
            return listeClasseJava[indiceOrdinal].taille;
        }
        return (uint32_t)poignéeFichier;
    }
    motMachine *valeurPremier = (motMachine *)adresseDonnéesDestination;
    intptr_t taille = invoquer(9, poignéeFichier, 0, 0), montantAchevé = 0;
    if (taille < 0 || (motMachine)taille > valeurPremier[0]) { fermerOutil(poignéeFichier); return (uint32_t)(taille < 0 ? taille : -27); }
    unsigned char blocDonnées[256];
    while (montantAchevé < taille) {
        intptr_t nombreÉlémentsÉlémentListe = invoquer(2, poignéeFichier, (motMachine)blocDonnées, taille - montantAchevé < 256 ? taille - montantAchevé : 256);
        if (nombreÉlémentsÉlémentListe <= 0) { fermerOutil(poignéeFichier); return (uint32_t)(nombreÉlémentsÉlémentListe ? nombreÉlémentsÉlémentListe : -5); }
        for (intptr_t indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) valeurPremier[1 + montantAchevé + indiceOrdinal] = blocDonnées[indiceOrdinal];
        montantAchevé += nombreÉlémentsÉlémentListe;
    }
    fermerOutil(poignéeFichier); return montantAchevé;
}
motMachine écrireOutil(motMachine nom, motMachine donnéesOriginal, motMachine nombreÉlémentsEntréeÉlément) {
    const motMachine *valeurPremier = (const motMachine *)donnéesOriginal;
    if (nombreÉlémentsEntréeÉlément > valeurPremier[0] || nombreÉlémentsEntréeÉlément > 16384) return (uint32_t)-27;
    int poignéeFichier = (int32_t)ouvrirOutil(nom, 577); if (poignéeFichier < 0) return (uint32_t)poignéeFichier;
    unsigned char blocDonnées[256]; motMachine montantAchevé = 0;
    while (montantAchevé < nombreÉlémentsEntréeÉlément) {
        motMachine nombreÉlémentsÉlémentListe = nombreÉlémentsEntréeÉlément - montantAchevé < 256 ? nombreÉlémentsEntréeÉlément - montantAchevé : 256;
        for (motMachine indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) blocDonnées[indiceOrdinal] = valeurPremier[1 + montantAchevé + indiceOrdinal];
        intptr_t résultat = invoquer(1, poignéeFichier, (motMachine)blocDonnées, nombreÉlémentsÉlémentListe);
        if (résultat <= 0) { fermerOutil(poignéeFichier); return (uint32_t)(résultat ? résultat : -5); }
        montantAchevé += résultat;
    }
    fermerOutil(poignéeFichier); return nombreÉlémentsEntréeÉlément;
}
motMachine nombreArgumentsOutil(void) { return invoquer(15, UINTPTR_MAX, 0, 0) - (actifJAR ? décalerJAR : 0); }
motMachine argumentOutil(motMachine indiceRechercher) {
    static const motMachine valeurVide[1] = {0};
    if (indiceRechercher >= 8) return (motMachine)valeurVide;
    unsigned char entrée[256]; intptr_t nombreÉlémentsÉlémentListe;
    if (actifJAR && indiceRechercher == 0) { const char *positionDonnées = principalJAR(); nombreÉlémentsÉlémentListe = 0; while (positionDonnées[nombreÉlémentsÉlémentListe] && nombreÉlémentsÉlémentListe < 255) { entrée[nombreÉlémentsÉlémentListe] = positionDonnées[nombreÉlémentsÉlémentListe]; nombreÉlémentsÉlémentListe++; } }
    else nombreÉlémentsÉlémentListe = invoquer(15, indiceRechercher + (actifJAR ? décalerJAR : 0), (motMachine)entrée, sizeof(entrée));
    if (nombreÉlémentsÉlémentListe < 0) return (motMachine)valeurVide;
    motMachine *donnéesRésultat = argumentTransféré[indiceRechercher]; unsigned nombreÉlémentsEntréeÉlément = 0;
    for (intptr_t indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe;) {
        unsigned codeCaractère = entrée[indiceOrdinal++], possèdeDavantage = codeCaractère < 128 ? 0 : codeCaractère >= 0xc2 && codeCaractère < 0xe0 ? 1 : codeCaractère < 0xf0 && codeCaractère >= 0xe0 ? 2 : codeCaractère >= 0xf0 && codeCaractère <= 0xf4 ? 3 : 4;
        if (possèdeDavantage == 4 || indiceOrdinal + possèdeDavantage > nombreÉlémentsÉlémentListe) { donnéesRésultat[++nombreÉlémentsEntréeÉlément] = 0xfffd; continue; }
        unsigned donnéesMinimal = possèdeDavantage == 1 ? 128 : possèdeDavantage == 2 ? 2048 : possèdeDavantage == 3 ? 65536 : 0;
        if (possèdeDavantage) codeCaractère &= (1u << (6 - possèdeDavantage)) - 1;
        unsigned ordinalInterne = 0;
        while (ordinalInterne < possèdeDavantage && (entrée[indiceOrdinal] & 0xc0) == 0x80) { codeCaractère = (codeCaractère << 6) | (entrée[indiceOrdinal++] & 63); ordinalInterne++; }
        if (ordinalInterne != possèdeDavantage || codeCaractère < donnéesMinimal || codeCaractère > 0x10ffff || (codeCaractère >= 0xd800 && codeCaractère <= 0xdfff)) codeCaractère = 0xfffd;
        if (codeCaractère >= 65536) { codeCaractère -= 65536; donnéesRésultat[++nombreÉlémentsEntréeÉlément] = 0xd800 | (codeCaractère >> 10); donnéesRésultat[++nombreÉlémentsEntréeÉlément] = 0xdc00 | (codeCaractère & 1023); }
        else donnéesRésultat[++nombreÉlémentsEntréeÉlément] = codeCaractère;
    }
    donnéesRésultat[0] = nombreÉlémentsEntréeÉlément; return (motMachine)donnéesRésultat;
}
motMachine genreOutil(void) { return valeurCatégorie; }
void arrêtFatalNoyau(const char *texteNotification) {
    const char *positionDonnées = texteNotification; while (*positionDonnées) positionDonnées++;
    valeursOctet("Java tool runtime error: ", 25); valeursOctet(texteNotification, positionDonnées - texteNotification); caractère(10);
    invoquer(6, 1, 0, 0); for (;;) {}
}
int démarrerProgrammeUtilisateur(int modeMéthode) {
    valeurCatégorie = modeMéthode;
    unsigned char entréeÉlémentPremier[256]; intptr_t nombreÉlémentsÉlémentListe = invoquer(15, 0, (motMachine)entréeÉlémentPremier, sizeof(entréeÉlémentPremier));
    if (modeMéthode == 2 || (modeMéthode == 1 && nombreÉlémentsÉlémentListe == 4 && entréeÉlémentPremier[0] == '-' && entréeÉlémentPremier[1] == 'j' && entréeÉlémentPremier[2] == 'a' && entréeÉlémentPremier[3] == 'r')) {
        décalerJAR = modeMéthode == 2 ? 0 : 1;
        char nomEntréeÉlémentFichier[256]; intptr_t donnéesLongueur = invoquer(15, décalerJAR, (motMachine)nomEntréeÉlémentFichier, sizeof(nomEntréeÉlémentFichier));
        if (donnéesLongueur <= 0 || ouvrirJAR(nomEntréeÉlémentFichier) < 0) {
            static const char erreur[] = "JAR error: invalid/unsupported archive or Main-Class\n";
            valeursOctet(erreur, sizeof(erreur) - 1); return 1;
        }
        actifJAR = 1;
    }
    int résultat = entréeÉlémentJava();
    if (substitutUnicodeEnAttente) caractère(0xfffd);
    return résultat;
}

// UDP는 interne 커널의 SVC를 통과하며 élémentListeActuel 127.0.0.1만 제공한다.
struct adresseJava { uint16_t famille, numéroPort; uint32_t adresse; unsigned char valeurZéro[8]; };
static struct adresseJava adresseUDP(unsigned numéroPort) {
    struct adresseJava valeurPremier = {2, (uint16_t)((numéroPort << 8) | (numéroPort >> 8)), 0x0100007f, {0}}; return valeurPremier;
}
motMachine ouvrirUDPOutil(motMachine numéroPort) {
    intptr_t poignéeFichier = invoquer(32, 2, 2, 17); if (poignéeFichier < 0) return (uint32_t)poignéeFichier;
    struct adresseJava valeurPremier = adresseUDP(numéroPort);
    valeurPremier.adresse = 0;
    intptr_t valeurÉtatValeur = invoquer(33, poignéeFichier, (motMachine)&valeurPremier, sizeof(valeurPremier));
    if (valeurÉtatValeur < 0) { fermerOutil(poignéeFichier); return (uint32_t)valeurÉtatValeur; }
    return poignéeFichier;
}
motMachine envoyerUDPOutil(motMachine poignéeFichier, motMachine numéroPort, motMachine valeurTableau, motMachine longueur) {
    const motMachine *adresseOriginal = (const motMachine *)valeurTableau; unsigned char Données[512];
    if (longueur > 512 || longueur > adresseOriginal[0]) return (uint32_t)-90;
    for (motMachine indiceOrdinal = 0; indiceOrdinal < longueur; indiceOrdinal++) Données[indiceOrdinal] = adresseOriginal[indiceOrdinal + 1];
    struct adresseJava valeurPremier = adresseUDP(numéroPort);
    return (uint32_t)invoquerUtilisateur(34, poignéeFichier, (motMachine)Données, longueur, 0, (motMachine)&valeurPremier, sizeof(valeurPremier));
}
static uint32_t ordreOctetInverse(uint32_t nombreÉlémentsÉlémentListe) { return (nombreÉlémentsÉlémentListe>>24)|((nombreÉlémentsÉlémentListe>>8)&0xff00)|((nombreÉlémentsÉlémentListe<<8)&0xff0000)|(nombreÉlémentsÉlémentListe<<24); }
motMachine adresseEnvoyerUDPOutil(motMachine poignéeFichier, motMachine adresse, motMachine numéroPort, motMachine valeurTableau, motMachine longueur) {
    const motMachine *adresseOriginal = (const motMachine *)valeurTableau; unsigned char Données[512];
    if (longueur > 512 || longueur > adresseOriginal[0]) return (uint32_t)-90;
    for (motMachine indiceOrdinal = 0; indiceOrdinal < longueur; indiceOrdinal++) Données[indiceOrdinal] = adresseOriginal[indiceOrdinal + 1];
    struct adresseJava valeurPremier = adresseUDP(numéroPort); valeurPremier.adresse = ordreOctetInverse(adresse);
    return (uint32_t)invoquerUtilisateur(34, poignéeFichier, (motMachine)Données, longueur, 0, (motMachine)&valeurPremier, sizeof(valeurPremier));
}
motMachine connecterOutil(motMachine poignéeFichier, motMachine adresse, motMachine numéroPort) {
    struct adresseJava valeurPremier = adresseUDP(numéroPort); valeurPremier.adresse = ordreOctetInverse(adresse);
    uint32_t lancer = invoquer(7, 0, 0, 0);
    for (;;) {
        intptr_t résultat = invoquer(37, poignéeFichier, (motMachine)&valeurPremier, sizeof(valeurPremier));
        if (résultat != -115) return (uint32_t)résultat;
        if ((uint32_t)(invoquer(7, 0, 0, 0) - lancer) >= 1000) return (uint32_t)-110;
    }
}
motMachine opérationRéceptionUDPOutil(motMachine poignéeFichier, motMachine valeurTableau, motMachine capacitéTampon) {
    motMachine *adresseDestination = (motMachine *)valeurTableau; unsigned char Données[512];
    if (capacitéTampon > 512 || adresseDestination[0] < 514) return (uint32_t)-90;
    struct adresseJava valeurPremier; unsigned donnéesLongueur = sizeof(valeurPremier);
    intptr_t nombreÉlémentsÉlémentListe = invoquerUtilisateur(35, poignéeFichier, (motMachine)Données, capacitéTampon, 0, (motMachine)&valeurPremier, (motMachine)&donnéesLongueur);
    if (nombreÉlémentsÉlémentListe >= 0) { for (intptr_t indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) adresseDestination[indiceOrdinal + 1] = Données[indiceOrdinal]; adresseDestination[513] = (valeurPremier.numéroPort << 8 | valeurPremier.numéroPort >> 8) & 65535; adresseDestination[514] = ordreOctetInverse(valeurPremier.adresse); }
    return (uint32_t)nombreÉlémentsÉlémentListe;
}
motMachine portUDPOutil(motMachine poignéeFichier) {
    struct adresseJava valeurPremier; unsigned donnéesLongueur = sizeof(valeurPremier);
    intptr_t valeurRetourné = invoquer(36, poignéeFichier, (motMachine)&valeurPremier, (motMachine)&donnéesLongueur);
    return (uint32_t)(valeurRetourné < 0 ? valeurRetourné : (valeurPremier.numéroPort << 8 | valeurPremier.numéroPort >> 8) & 65535);
}
motMachine millisecondesÉcouléesOutil(void) { return (uint32_t)invoquer(7, 0, 0, 0); }
motMachine largeurÉcranOutil(void) { return (uint32_t)lireLargeurÉcran(); }
motMachine hauteurÉcranOutil(void) { return (uint32_t)lireHauteurÉcran(); }
motMachine attendreGraphismeOutil(void) { return (uint32_t)attendreToucheÉcranPour(); }
motMachine rectangleOutil(motMachine coordonnéeCoordonnéeHorizontale, motMachine coordonnéeCoordonnéeVerticale, motMachine valeurLargeurDemandé, motMachine valeurHauteurDemandé, motMachine couleurPixel) {
    return (uint32_t)invoquerUtilisateur(13, coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale, couleurPixel, valeurLargeurDemandé, valeurHauteurDemandé, 0);
}

motMachine fluxOutil(motMachine action,motMachine poignéeFichier,motMachine valeur){
    if(action==0)return (uint32_t)invoquer(32,2,1,6);
    struct adresseJava valeurPremier=adresseUDP(valeur);
    if(action==1){valeurPremier.adresse=0;intptr_t valeurRetourné=invoquer(33,poignéeFichier,(motMachine)&valeurPremier,sizeof(valeurPremier));return (uint32_t)(valeurRetourné<0?valeurRetourné:invoquer(38,poignéeFichier,4,0));}
    if(action==2)return (uint32_t)invoquer(37,poignéeFichier,(motMachine)&valeurPremier,sizeof(valeurPremier));
    if(action==3)return (uint32_t)invoquer(39,poignéeFichier,0,0);
    if(action==4)return portUDPOutil(poignéeFichier);
    if(action==5)return (uint32_t)invoquer(40,poignéeFichier,0,0);
    return (uint32_t)-22;
}
motMachine gUIOutil(motMachine action,motMachine valeurIdentificateur,motMachine valeurPremier,motMachine valeurDeuxième,motMachine codeCaractère,motMachine donnéesDestination){return (uint32_t)invoquerUtilisateur(20,action,valeurIdentificateur,valeurPremier,valeurDeuxième,codeCaractère,donnéesDestination);}
motMachine texteGUIOutil(motMachine valeurIdentificateur,motMachine valeurTableau,motMachine nombreÉlémentsÉlémentListe){
    const motMachine *adresseOriginal=(const motMachine *)valeurTableau;uint32_t Données[127];unsigned nombreÉlémentsEntréeÉlément=0;
    if(nombreÉlémentsÉlémentListe>adresseOriginal[0])return (uint32_t)-22;
    for(motMachine indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++){unsigned encodageCaractère=adresseOriginal[indiceOrdinal+1];if(encodageCaractère>=0xd800&&encodageCaractère<=0xdbff&&indiceOrdinal+1<nombreÉlémentsÉlémentListe){unsigned valeurBas=adresseOriginal[++indiceOrdinal+1];if(valeurBas<0xdc00||valeurBas>0xdfff)return (uint32_t)-22;encodageCaractère=0x10000+((encodageCaractère-0xd800)<<10)+valeurBas-0xdc00;}if(nombreÉlémentsEntréeÉlément==127)return (uint32_t)-22;Données[nombreÉlémentsEntréeÉlément++]=encodageCaractère;}
    return (uint32_t)invoquerUtilisateur(21,valeurIdentificateur,(motMachine)Données,nombreÉlémentsEntréeÉlément,0,0,0);
}
