#include "../nommage/nomsLierMachine.h"
/* Passive FTP service in EL1. Uploads commit to the Java RAM VFS only after EOF. */
#include "PileRéseau.h"
#include "string.h"
#include "ABIFichier.h"
extern uintptr_t millisecondesÉcouléesCarteMatérielle(void);
extern int32_t longueurEntréeÉlémentSystèmeFichiersJava(int32_t), octetEntréeÉlémentSystèmeFichiersJava(int32_t,int32_t), tailleEntréeÉlémentSystèmeFichiersJava(int32_t);
extern int32_t nombreÉlémentsEntréeÉlémentSystèmeFichiersJava(void);
static int recevoirPort = -1, contrôle = -1, connexionManuel = -1, Données = -1;
static unsigned estEntrantJournalisé, correctÉtatUtilisateur, tailleLigne, incorrectLigne, programmeTerminerSession, tâcheExécutionEnCours, capacitéUtilisé, nombreÉlémentsEnvoyé, possèdeÉchoué;
static unsigned tailleRéponse, envoyéRéponse, numéroPortSuivant;
static uint32_t activité;
static char ligne[256], réponses[2048], nomEntréeÉlémentFichier[64], nomTransfert[64];
static unsigned char étatValeurTransfert[16384];
static int égal(const char *valeurPremier, const char *valeurDeuxième) { while (*valeurPremier && *valeurPremier == *valeurDeuxième) { valeurPremier++; valeurDeuxième++; } return *valeurPremier == *valeurDeuxième; }
static void réponse(const char *donnéesChaîne) {
    size_t nombreÉlémentsÉlémentListe = strlen(donnéesChaîne);
    if (envoyéRéponse) { memmove(réponses, réponses + envoyéRéponse, tailleRéponse - envoyéRéponse); tailleRéponse -= envoyéRéponse; envoyéRéponse = 0; }
    if (nombreÉlémentsÉlémentListe > sizeof(réponses) - tailleRéponse) { programmeTerminerSession = 1; return; }
    memcpy(réponses + tailleRéponse, donnéesChaîne, nombreÉlémentsÉlémentListe); tailleRéponse += nombreÉlémentsÉlémentListe;
}
static void valeurNumérique(unsigned valeur, char *donnéesRésultat, unsigned *nombreÉlémentsÉlémentListe) {
    char nombreÉlémentsChiffre[10]; unsigned nombreÉlémentsEntréeÉlément = 0;
    do { nombreÉlémentsChiffre[nombreÉlémentsEntréeÉlément++] = '0' + valeur % 10; valeur /= 10; } while (valeur);
    while (nombreÉlémentsEntréeÉlément) donnéesRésultat[(*nombreÉlémentsÉlémentListe)++] = nombreÉlémentsChiffre[--nombreÉlémentsEntréeÉlément];
}
static void arrêterTransfert(void) {
    if (Données >= 0) fermerRéseau(Données); if (connexionManuel >= 0) fermerRéseau(connexionManuel);
    Données = connexionManuel = -1; tâcheExécutionEnCours = capacitéUtilisé = nombreÉlémentsEnvoyé = possèdeÉchoué = 0;
}
static void déconnecter(void) {
    arrêterTransfert(); if (contrôle >= 0) fermerRéseau(contrôle); contrôle = -1;
    estEntrantJournalisé = correctÉtatUtilisateur = tailleLigne = incorrectLigne = tailleRéponse = envoyéRéponse = programmeTerminerSession = 0;
}
int contrôleTransfertFichier(int action) {
    if (action == 2) return recevoirPort >= 0;
    if (action == 0) { déconnecter(); if (recevoirPort >= 0) fermerRéseau(recevoirPort); recevoirPort = -1; return 0; }
    if (action != 1) return -22; if (recevoirPort >= 0) return 0;
    recevoirPort = créerExtrémitéPriseRéseau(1); if (recevoirPort < 0) return recevoirPort;
    int valeurRetourné = associerRéseauCourt(recevoirPort, lireÉtatRéseau(0,0), 21); if (!valeurRetourné) valeurRetourné = écouterRéseauCourt(recevoirPort);
    if (valeurRetourné < 0) { fermerRéseau(recevoirPort); recevoirPort = -1; } return valeurRetourné;
}
static int chemin(const char *nom) {
    unsigned nombreÉlémentsÉlémentListe = 0; if (*nom == '/') nom++;
    if (!*nom || égal(nom, ".") || égal(nom, "..")) return 0;
    nomEntréeÉlémentFichier[nombreÉlémentsÉlémentListe++] = '/';
    while (*nom) {
        unsigned char codeCaractère = *nom++;
        if (nombreÉlémentsÉlémentListe >= 63 || codeCaractère < 32 || codeCaractère == 127 || codeCaractère == '/' || codeCaractère == '\\') return 0;
        nomEntréeÉlémentFichier[nombreÉlémentsÉlémentListe++] = codeCaractère;
    }
    nomEntréeÉlémentFichier[nombreÉlémentsÉlémentListe] = 0; return 1;
}
static void envoyerListe(int détail) {
    capacitéUtilisé = nombreÉlémentsEnvoyé = 0;
    for (int indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsEntréeÉlémentSystèmeFichiersJava(); indiceOrdinal++) {
        int nombreÉlémentsÉlémentListe = longueurEntréeÉlémentSystèmeFichiersJava(indiceOrdinal); if (nombreÉlémentsÉlémentListe <= 0) continue;
        const char *partiePréalable = détail == 2 ? "type=file;size=" : détail == 1 ? "-rw-rw-rw- 1 user user " : "";
        unsigned nombreÉlémentsEntréeÉlément = strlen(partiePréalable); memcpy(étatValeurTransfert + capacitéUtilisé, partiePréalable, nombreÉlémentsEntréeÉlément); capacitéUtilisé += nombreÉlémentsEntréeÉlément;
        if (détail) valeurNumérique(tailleEntréeÉlémentSystèmeFichiersJava(indiceOrdinal), (char *)étatValeurTransfert, &capacitéUtilisé);
        const char *valeurSuffixe = détail == 2 ? "; " : détail == 1 ? " Jan 01 00:00 " : "";
        nombreÉlémentsEntréeÉlément = strlen(valeurSuffixe); memcpy(étatValeurTransfert + capacitéUtilisé, valeurSuffixe, nombreÉlémentsEntréeÉlément); capacitéUtilisé += nombreÉlémentsEntréeÉlément;
        for (int ordinalInterne = 0; ordinalInterne < nombreÉlémentsÉlémentListe; ordinalInterne++) étatValeurTransfert[capacitéUtilisé++] = octetEntréeÉlémentSystèmeFichiersJava(indiceOrdinal,ordinalInterne);
        étatValeurTransfert[capacitéUtilisé++] = '\r'; étatValeurTransfert[capacitéUtilisé++] = '\n';
    }
}
static void préparerConnexionManuel(int étendu) {
    if (tâcheExécutionEnCours) { réponse("450 Transfer in progress\r\n"); return; }
    arrêterTransfert(); connexionManuel = créerExtrémitéPriseRéseau(1);
    if (connexionManuel >= 0) adressePriseRéseauRéutiliser(connexionManuel);
    unsigned numéroPort = 50000 + numéroPortSuivant++ % 8;
    if (connexionManuel < 0 || associerRéseauCourt(connexionManuel, lireÉtatRéseau(0,0), numéroPort) || écouterRéseauCourt(connexionManuel)) {
        arrêterTransfert(); réponse("425 Cannot open passive listener\r\n"); return;
    }
    char réponseRetour[96]; const char *partiePréalable = étendu ? "229 Entering Extended Passive Mode (|||" : "227 Entering Passive Mode (";
    unsigned nombreÉlémentsÉlémentListe = strlen(partiePréalable); memcpy(réponseRetour, partiePréalable, nombreÉlémentsÉlémentListe);
    if (étendu) { valeurNumérique(numéroPort, réponseRetour, &nombreÉlémentsÉlémentListe); réponseRetour[nombreÉlémentsÉlémentListe++] = '|'; }
    else {
        uint32_t adresse=lireÉtatRéseau(0,0);
        for (int indicePosition=24;indicePosition>=0;indicePosition-=8) { valeurNumérique((adresse>>indicePosition)&255,réponseRetour,&nombreÉlémentsÉlémentListe);réponseRetour[nombreÉlémentsÉlémentListe++]=','; }
        valeurNumérique(numéroPort / 256, réponseRetour, &nombreÉlémentsÉlémentListe); réponseRetour[nombreÉlémentsÉlémentListe++] = ','; valeurNumérique(numéroPort % 256, réponseRetour, &nombreÉlémentsÉlémentListe);
    }
    réponseRetour[nombreÉlémentsÉlémentListe++] = ')'; réponseRetour[nombreÉlémentsÉlémentListe++] = '\r'; réponseRetour[nombreÉlémentsÉlémentListe++] = '\n'; réponseRetour[nombreÉlémentsÉlémentListe] = 0; réponse(réponseRetour);
}
static void commande(void) {
    ligne[tailleLigne] = 0;
    char *argumentsSupplémentaire = ligne; while (*argumentsSupplémentaire && *argumentsSupplémentaire != ' ') { if (*argumentsSupplémentaire >= 'a' && *argumentsSupplémentaire <= 'z') *argumentsSupplémentaire -= 32; argumentsSupplémentaire++; }
    if (*argumentsSupplémentaire) *argumentsSupplémentaire++ = 0; while (*argumentsSupplémentaire == ' ') argumentsSupplémentaire++;
    if (égal(ligne, "QUIT")) { arrêterTransfert(); réponse("221 Goodbye\r\n"); programmeTerminerSession = 1; return; }
    if (égal(ligne, "NOOP")) { réponse("200 OK\r\n"); return; }
    if (égal(ligne, "SYST")) { réponse("215 UNIX Type: L8\r\n"); return; }
    if (égal(ligne, "FEAT")) { réponse("211-Features\r\n UTF8\r\n EPSV\r\n SIZE\r\n MLST type*;size*;\r\n211 End\r\n"); return; }
    if (égal(ligne, "USER")) { estEntrantJournalisé = 0; correctÉtatUtilisateur = égal(argumentsSupplémentaire, "anonymous") || égal(argumentsSupplémentaire, "jkoros"); réponse(correctÉtatUtilisateur ? "331 Password required\r\n" : "530 Unknown user\r\n"); return; }
    if (égal(ligne, "PASS")) { estEntrantJournalisé = correctÉtatUtilisateur; réponse(estEntrantJournalisé ? "230 Anonymous RAM workspace\r\n" : "530 Send USER first\r\n"); return; }
    if (!estEntrantJournalisé) { réponse("530 Login first\r\n"); return; }
    if (égal(ligne, "PWD")) réponse("257 \"/\"\r\n");
    else if (égal(ligne, "CWD")) réponse(égal(argumentsSupplémentaire, "/") || égal(argumentsSupplémentaire, ".") ? "250 Root directory\r\n" : "550 Root files only\r\n");
    else if (égal(ligne, "TYPE")) réponse(égal(argumentsSupplémentaire, "I") || égal(argumentsSupplémentaire, "A") ? "200 Type set\r\n" : "504 Unsupported type\r\n");
    else if (égal(ligne, "OPTS")) réponse(égal(argumentsSupplémentaire, "UTF8 ON") ? "200 UTF8 enabled\r\n" : "501 Unsupported option\r\n");
    else if (égal(ligne, "PASV")) préparerConnexionManuel(0);
    else if (égal(ligne, "EPSV")) { if (*argumentsSupplémentaire && !égal(argumentsSupplémentaire, "1")) réponse("522 IPv4 only\r\n"); else préparerConnexionManuel(1); }
    else if (égal(ligne, "ABOR")) { arrêterTransfert(); réponse("226 Transfer aborted\r\n"); }
    else if (égal(ligne, "DELE")) { réponse(chemin(argumentsSupplémentaire) && pk_unlink(nomEntréeÉlémentFichier) == 0 ? "250 Deleted\r\n" : "550 Cannot delete file\r\n"); }
    else if (égal(ligne, "LIST") || égal(ligne, "NLST") || égal(ligne, "MLSD")) {
        if (tâcheExécutionEnCours) { réponse("450 Transfer in progress\r\n"); return; }
        if (connexionManuel < 0 && Données < 0) { réponse("425 Use PASV or EPSV\r\n"); return; }
        if (*argumentsSupplémentaire && !égal(argumentsSupplémentaire,"/") && !égal(argumentsSupplémentaire,".") && !égal(argumentsSupplémentaire,"-a") && !égal(argumentsSupplémentaire,"-l") && !égal(argumentsSupplémentaire,"-la")) { réponse("550 Root listing only\r\n"); return; }
        envoyerListe(égal(ligne,"MLSD") ? 2 : égal(ligne,"LIST") ? 1 : 0); tâcheExécutionEnCours = 2;
        réponse("150 Opening directory listing\r\n");
    }
    else if (égal(ligne, "SIZE")) {
        if (!chemin(argumentsSupplémentaire)) { réponse("550 Invalid filename\r\n"); return; }
        int poignéeFichier = pk_open(nomEntréeÉlémentFichier, lireValeurSeulement, 0); if (poignéeFichier < 0) { réponse("550 File unavailable\r\n"); return; }
        int taille = pk_size(poignéeFichier); pk_close(poignéeFichier); char réponseRetour[32] = "213 "; unsigned nombreÉlémentsÉlémentListe = 4;
        valeurNumérique(taille, réponseRetour, &nombreÉlémentsÉlémentListe); réponseRetour[nombreÉlémentsÉlémentListe++] = '\r'; réponseRetour[nombreÉlémentsÉlémentListe++] = '\n'; réponseRetour[nombreÉlémentsÉlémentListe] = 0; réponse(réponseRetour);
    } else if (égal(ligne, "STOR") || égal(ligne, "RETR")) {
        if (tâcheExécutionEnCours) { réponse("450 Transfer in progress\r\n"); return; }
        if (connexionManuel < 0 && Données < 0) { réponse("425 Use PASV or EPSV\r\n"); return; }
        if (!chemin(argumentsSupplémentaire)) { réponse("550 Invalid filename\r\n"); return; }
        tâcheExécutionEnCours = égal(ligne, "STOR") ? 1 : 2; capacitéUtilisé = nombreÉlémentsEnvoyé = possèdeÉchoué = 0;
        memcpy(nomTransfert, nomEntréeÉlémentFichier, strlen(nomEntréeÉlémentFichier) + 1);
        if (tâcheExécutionEnCours == 2) {
            int poignéeFichier = pk_open(nomEntréeÉlémentFichier, lireValeurSeulement, 0);
            if (poignéeFichier < 0) { tâcheExécutionEnCours = 0; réponse("550 File unavailable\r\n"); return; }
            int nombreÉlémentsÉlémentListe = pk_read(poignéeFichier, étatValeurTransfert, sizeof(étatValeurTransfert)); pk_close(poignéeFichier);
            if (nombreÉlémentsÉlémentListe < 0) { tâcheExécutionEnCours = 0; réponse("451 Read failed\r\n"); return; } capacitéUtilisé = nombreÉlémentsÉlémentListe;
        }
        réponse("150 Opening binary data connection\r\n");
    } else réponse("502 Command not implemented\r\n");
}
void inspecterTransfertFichier(void) {
    if (recevoirPort < 0) return;
    int connexionArrivant = accepterRéseauCourt(recevoirPort);
    if (connexionArrivant >= 0) {
        if (contrôle >= 0) { écrireRéseauCourt(connexionArrivant, "421 One session at a time\r\n", 27); fermerRéseau(connexionArrivant); }
        else { contrôle = connexionArrivant; activité = millisecondesÉcouléesCarteMatérielle(); réponse("220 jkoros native ARM64 FTP ready\r\n"); }
    }
    if (contrôle < 0) return;
    if ((uint32_t)(millisecondesÉcouléesCarteMatérielle() - activité) > 60000) { déconnecter(); return; }
    if (!programmeTerminerSession) for (unsigned budget = 0; budget < 256; budget++) {
        unsigned char codeCaractère; int valeurRetourné = lireRéseauCourt(contrôle, &codeCaractère, 1);
        if (valeurRetourné == -11) break; if (valeurRetourné <= 0) { déconnecter(); return; } activité = millisecondesÉcouléesCarteMatérielle();
        if (codeCaractère == '\n') { if (incorrectLigne) réponse("500 Command too long or invalid\r\n"); else commande(); tailleLigne = incorrectLigne = 0; if (programmeTerminerSession) break; }
        else if (codeCaractère != '\r') { if (!codeCaractère || tailleLigne >= sizeof(ligne) - 1) incorrectLigne = 1; else ligne[tailleLigne++] = codeCaractère; }
    }
    if (connexionManuel >= 0 && Données < 0) {
        int valeurRetourné = accepterRéseauCourt(connexionManuel);
        if (valeurRetourné >= 0) {
            if (adressePairRéseauRéseauCourt(valeurRetourné) != adressePairRéseauRéseauCourt(contrôle)) fermerRéseau(valeurRetourné);
            else { Données = valeurRetourné; fermerRéseau(connexionManuel); connexionManuel = -1; activité = millisecondesÉcouléesCarteMatérielle(); }
        }
    }
    if (tâcheExécutionEnCours == 1 && Données >= 0) for (unsigned budget = 0; budget < 8; budget++) {
        unsigned char blocDonnées[512]; int nombreÉlémentsÉlémentListe = lireRéseauCourt(Données, blocDonnées, sizeof(blocDonnées));
        if (nombreÉlémentsÉlémentListe == -11) break;
        if (nombreÉlémentsÉlémentListe < 0) { arrêterTransfert(); réponse("426 Data connection failed\r\n"); break; }
        activité = millisecondesÉcouléesCarteMatérielle();
        if (nombreÉlémentsÉlémentListe == 0) {
            int résultat = -1;
            if (!possèdeÉchoué) {
                int poignéeFichier = pk_open(nomTransfert, écrireValeurSeulement | ManquantSiCréer | ContenuTronquer, 0600);
                if (poignéeFichier >= 0) { résultat = pk_write(poignéeFichier, étatValeurTransfert, capacitéUtilisé); pk_close(poignéeFichier); }
            }
            int estRéussi = !possèdeÉchoué && résultat == (int)capacitéUtilisé; arrêterTransfert(); réponse(estRéussi ? "226 Upload committed to RAM\r\n" : "552 File exceeds RAM limit or storage full\r\n"); break;
        }
        if ((unsigned)nombreÉlémentsÉlémentListe > sizeof(étatValeurTransfert) - capacitéUtilisé) possèdeÉchoué = 1;
        if (!possèdeÉchoué) { memcpy(étatValeurTransfert + capacitéUtilisé, blocDonnées, nombreÉlémentsÉlémentListe); capacitéUtilisé += nombreÉlémentsÉlémentListe; }
    }
    if (tâcheExécutionEnCours == 2 && Données >= 0) {
        int nombreÉlémentsÉlémentListe = écrireRéseauCourt(Données, étatValeurTransfert + nombreÉlémentsEnvoyé, capacitéUtilisé - nombreÉlémentsEnvoyé);
        if (nombreÉlémentsÉlémentListe >= 0) { nombreÉlémentsEnvoyé += nombreÉlémentsÉlémentListe; activité = millisecondesÉcouléesCarteMatérielle(); if (nombreÉlémentsEnvoyé == capacitéUtilisé) { arrêterTransfert(); réponse("226 Transfer complete\r\n"); } }
        else if (nombreÉlémentsÉlémentListe != -11) { arrêterTransfert(); réponse("426 Data connection failed\r\n"); }
    }
    if (envoyéRéponse < tailleRéponse) {
        int nombreÉlémentsÉlémentListe = écrireRéseauCourt(contrôle, réponses + envoyéRéponse, tailleRéponse - envoyéRéponse);
        if (nombreÉlémentsÉlémentListe > 0) envoyéRéponse += nombreÉlémentsÉlémentListe; else if (nombreÉlémentsÉlémentListe != -11) { déconnecter(); return; }
    }
    if (envoyéRéponse == tailleRéponse) { tailleRéponse = envoyéRéponse = 0; if (programmeTerminerSession) déconnecter(); }
}
