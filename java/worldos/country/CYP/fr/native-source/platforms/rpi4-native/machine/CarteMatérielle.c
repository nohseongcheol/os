#include "../nommage/nomsLierMachine.h"
#include "informationÉcran.h"
#include <stdint.h>
#include <stddef.h>
#include "Utilisateur.h"
#include "../PileRéseau/PileRéseau.h"
typedef uintptr_t motMachine;
#define registreMachine(valeurPremier) (*(volatile uint32_t *)(uintptr_t)(valeurPremier))
#define périphériqueSériel 0xfe201000u
#define entréeSortieUsageButGénéral 0xfe200000u
#define adresseBoîteMessages 0xfe00b880u
static inline void barrièreMémoire(void) { __asm__ volatile("dsb sy" ::: "memory"); }
static uint64_t nombreÉlémentsHorloge(void) { uint64_t donnéesTemporaire; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(donnéesTemporaire)); return donnéesTemporaire; }
static uint64_t fréquence;
static volatile uint32_t donnéesBoîteMessages[64] __attribute__((aligned(16)));
static unsigned prêtÉcran;
static uint32_t unitéOctetKibiMémoireARM;

void *memset(void *positionDonnées, int codeCaractère, size_t nombreÉlémentsÉlémentListe) { unsigned char *décalageSuivant = positionDonnées; while (nombreÉlémentsÉlémentListe--) *décalageSuivant++ = codeCaractère; return positionDonnées; }
void *memcpy(void *donnéesDestination, const void *donnéesChaîne, size_t nombreÉlémentsÉlémentListe) { unsigned char *valeurPremier = donnéesDestination; const unsigned char *valeurDeuxième = donnéesChaîne; while (nombreÉlémentsÉlémentListe--) *valeurPremier++ = *valeurDeuxième++; return donnéesDestination; }

static int boîteMessages(void) {
    uint32_t requête = (uint32_t)(uintptr_t)donnéesBoîteMessages | 8;
    uint64_t lancer = nombreÉlémentsHorloge();
    barrièreMémoire();
    while (registreMachine(adresseBoîteMessages + 0x38) & 0x80000000u)
        if (nombreÉlémentsHorloge() - lancer > fréquence) return 0;
    registreMachine(adresseBoîteMessages + 0x20) = requête;
    for (;;) {
        if (!(registreMachine(adresseBoîteMessages + 0x18) & 0x40000000u)) {
            uint32_t réponse = registreMachine(adresseBoîteMessages);
            if (réponse == requête) { barrièreMémoire(); return donnéesBoîteMessages[1] == 0x80000000u; }
        }
        if (nombreÉlémentsHorloge() - lancer > fréquence) return 0;
    }
}

extern int32_t sortieConsoleJava(int32_t, int32_t), entréeConsoleJava(void);
extern void octetTerminal(unsigned);
extern int enAttenteTerminal(void);
extern void pointeurTerminal(unsigned,int,int),raccourciClavierTerminal(unsigned);
extern void modeEntréeTerminal(unsigned);
#include "../valeurDistant/valeurDistant.h"
static int fluxListe;
static unsigned précédentÉlémentUART;
motMachine fluxListeCarteMatérielle(motMachine estUtilisé) { fluxListe=estUtilisé!=0; return 0; }
motMachine canalCarteMatérielle(motMachine canal, motMachine codeCaractère) {
    if(fluxListe && sortieConsoleJava((int32_t)canal,(int32_t)(codeCaractère&255))) return 0;
    octetTerminal(codeCaractère&255);
    sortieDistant(codeCaractère&255);
    if ((codeCaractère&255)==10 && précédentÉlémentUART!=13) {
        while (registreMachine(périphériqueSériel + 0x18) & 0x20) __asm__ volatile("yield");
        registreMachine(périphériqueSériel)=13;
    }
    précédentÉlémentUART=codeCaractère&255;
    while (registreMachine(périphériqueSériel + 0x18) & 0x20) __asm__ volatile("yield");
    registreMachine(périphériqueSériel) = (uint32_t)codeCaractère & 255;
    return 0;
}
motMachine écrireCaractèreCarteMatérielle(motMachine codeCaractère) { return canalCarteMatérielle(1,codeCaractère); }
motMachine obtenirCaractèreBrutCarteMatérielle(void) {
    int caractèreDistant=entréeDistant();if(caractèreDistant>=0)return caractèreDistant;
    if (registreMachine(périphériqueSériel + 0x18) & 0x10) return (uint32_t)-1;
    uint32_t valeur = registreMachine(périphériqueSériel);
    if (valeur & 0xf00) { registreMachine(périphériqueSériel + 4) = 0; return (uint32_t)-1; }
    return valeur & 255;
}
motMachine obtenirCaractèreCarteMatérielle(void) {
    network_poll();
    static unsigned paquetEntrant,capacitéUtilisé; static unsigned char donnéesPaquet[6];
    if(enAttenteTerminal())return (uint32_t)-4096;
    if(fluxListe){int32_t codeCaractère=entréeConsoleJava();if(codeCaractère!=-3)return (uint32_t)codeCaractère;}
    for(;;){
        int codeCaractère=(int32_t)obtenirCaractèreBrutCarteMatérielle();if(codeCaractère<0)return (uint32_t)codeCaractère;
        if(!paquetEntrant){if(codeCaractère!=30)return codeCaractère;paquetEntrant=1;capacitéUtilisé=0;continue;}
        donnéesPaquet[capacitéUtilisé++]=codeCaractère;if(capacitéUtilisé<6)continue;paquetEntrant=0;
        if(donnéesPaquet[0]==1)pointeurTerminal(donnéesPaquet[1],donnéesPaquet[2]+donnéesPaquet[3]*256,donnéesPaquet[4]+donnéesPaquet[5]*256);
        if(donnéesPaquet[0]==2)raccourciClavierTerminal(donnéesPaquet[1]);
        if(donnéesPaquet[0]==3)modeEntréeTerminal(donnéesPaquet[1]);
        if(enAttenteTerminal())return (uint32_t)-4096;
    }
}
motMachine millisecondesÉcouléesCarteMatérielle(void) { return (uint32_t)(nombreÉlémentsHorloge() / (fréquence / 1000)); }
motMachine niveauExceptionCarteMatérielle(void) { uint64_t donnéesTemporaire; __asm__ volatile("mrs %0, CurrentEL" : "=r"(donnéesTemporaire)); return donnéesTemporaire >> 2; }
static void uARTAfficherLigne(const char *donnéesChaîne) { while (*donnéesChaîne) écrireCaractèreCarteMatérielle((unsigned char)*donnéesChaîne++); }
static void uARTHexadécimalCourt(motMachine nombreÉlémentsÉlémentListe) { const char *chiffresHexadécimal = "0123456789abcdef"; for (int donnéesChaîne = 60; donnéesChaîne >= 0; donnéesChaîne -= 4) écrireCaractèreCarteMatérielle(chiffresHexadécimal[(nombreÉlémentsÉlémentListe >> donnéesChaîne) & 15]); }
motMachine arrêterCarteMatérielle(motMachine valeurÉtatValeur) {
    uARTAfficherLigne("\r\nHALTED "); uARTHexadécimalCourt(valeurÉtatValeur); uARTAfficherLigne("\r\n");
    for (;;) __asm__ volatile("wfe");
}
void arrêtFatalNoyau(const char *valeurCause) __attribute__((noreturn));
void arrêtFatalNoyau(const char *valeurCause) { uARTAfficherLigne("\r\nPANIC: "); uARTAfficherLigne(valeurCause); arrêterCarteMatérielle(1); __builtin_unreachable(); }
void exceptionCarteMatérielle(motMachine étatValeurException, motMachine positionCommande, motMachine adresseInvalide) {
    uARTAfficherLigne("\r\nEXCEPTION ESR="); uARTHexadécimalCourt(étatValeurException);
    uARTAfficherLigne(" PC="); uARTHexadécimalCourt(positionCommande); uARTAfficherLigne(" FAR="); uARTHexadécimalCourt(adresseInvalide);
    arrêterCarteMatérielle(2);
}
int matérielPhysiqueCarteMatérielle(void) {
    /* QEMU의 GET_BOARD_SERIAL은 미구현(0). 존재하지 않는 GENET MMIO를 읽지 않는다. */
    donnéesBoîteMessages[0]=32;donnéesBoîteMessages[1]=0;donnéesBoîteMessages[2]=0x10004;donnéesBoîteMessages[3]=8;donnéesBoîteMessages[4]=0;
    donnéesBoîteMessages[5]=donnéesBoîteMessages[6]=donnéesBoîteMessages[7]=0;
    return boîteMessages()&&donnéesBoîteMessages[4]==0x80000008u&&(donnéesBoîteMessages[5]||donnéesBoîteMessages[6]);
}
int adresseMachineCarteMatérielle(unsigned char *adresse) {
    donnéesBoîteMessages[0]=32;donnéesBoîteMessages[1]=0;donnéesBoîteMessages[2]=0x10003;donnéesBoîteMessages[3]=8;donnéesBoîteMessages[4]=0;
    donnéesBoîteMessages[5]=donnéesBoîteMessages[6]=donnéesBoîteMessages[7]=0;
    if(!boîteMessages()||(donnéesBoîteMessages[4]&0x80000000u)==0||(donnéesBoîteMessages[4]&0xffff)!=6)return 0;
    const unsigned char *Données=(const unsigned char*)&donnéesBoîteMessages[5];unsigned valeurSomme=0;
    for(unsigned indiceOrdinal=0;indiceOrdinal<6;indiceOrdinal++){adresse[indiceOrdinal]=Données[indiceOrdinal];valeurSomme|=Données[indiceOrdinal];}return valeurSomme&&!(adresse[0]&1);
}
void opérationInitialisationCarteMatérielle(void) {
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(fréquence));
    registreMachine(périphériqueSériel + 0x30) = 0;
    // GPIO14/15 ALT0: PL011 UART0, Pi4 전용 pull 레지스터.
    registreMachine(entréeSortieUsageButGénéral + 4) = (registreMachine(entréeSortieUsageButGénéral + 4) & ~((7u << 12) | (7u << 15))) | (4u << 12) | (4u << 15);
    registreMachine(entréeSortieUsageButGénéral + 0xe4) &= ~((3u << 28) | (3u << 30));
    // 펌웨어의 UART 시계를 고정한다. valeurÉchec 시 config.txt의 48MHz를 사용한다.
    donnéesBoîteMessages[0] = 36; donnéesBoîteMessages[1] = 0; donnéesBoîteMessages[2] = 0x38002; donnéesBoîteMessages[3] = 12;
    donnéesBoîteMessages[4] = 0; donnéesBoîteMessages[5] = 2; donnéesBoîteMessages[6] = 48000000; donnéesBoîteMessages[7] = 0; donnéesBoîteMessages[8] = 0;
    int sainHorloge = boîteMessages();
    uint32_t valeurVitesse = sainHorloge && donnéesBoîteMessages[6] >= 1843200 ? donnéesBoîteMessages[6] : 48000000;
    donnéesBoîteMessages[0]=32; donnéesBoîteMessages[1]=0; donnéesBoîteMessages[2]=0x10005; donnéesBoîteMessages[3]=8; donnéesBoîteMessages[4]=0;
    donnéesBoîteMessages[5]=donnéesBoîteMessages[6]=donnéesBoîteMessages[7]=0;
    if (boîteMessages() && donnéesBoîteMessages[4]==0x80000008u) unitéOctetKibiMémoireARM=donnéesBoîteMessages[6]/1024;
    uint32_t diviseur64 = (uint32_t)(((uint64_t)valeurVitesse * 4 + 57600) / 115200);
    registreMachine(périphériqueSériel + 0x44) = 0x7ff;
    registreMachine(périphériqueSériel + 0x24) = diviseur64 / 64;
    registreMachine(périphériqueSériel + 0x28) = diviseur64 % 64;
    registreMachine(périphériqueSériel + 0x2c) = (3u << 5) | (1u << 4);
    registreMachine(périphériqueSériel + 0x38) = 0;
    registreMachine(périphériqueSériel + 0x30) = 0x301;
    barrièreMémoire();
    uARTAfficherLigne("JKOROS AARCH64 BARE METAL\r\n");
    opérationInitialisationSystèmeUtilisateur();
    network_init();
}
motMachine fTPCarteMatérielle(motMachine action) { return (uint32_t)ftp_control((int)action); }
motMachine étatRéseauCarteMatérielle(motMachine valeurEntréeÉlément, motMachine numéro) { return lireÉtatRéseau(valeurEntréeÉlément, numéro); }
motMachine réglagesRéseauCarteMatérielle(motMachine action, motMachine adresse, motMachine valeurMasque, motMachine valeurPasserelle) { return (uint32_t)configurerRéseau(action, adresse, valeurMasque, valeurPasserelle); }
motMachine réponseRetourEnvoyerCarteMatérielle(motMachine adresse, motMachine valeurOrdre) { return (uint32_t)démarrerTestRéponseRetour(adresse, valeurOrdre); }
motMachine réponseRetourLireCarteMatérielle(motMachine valeurEntréeÉlément) { return (uint32_t)lireTestRéponseRetour(valeurEntréeÉlément); }
motMachine désactivéAlimentationCarteMatérielle(void) {
    ftp_control(0);
    for (unsigned numéro=0; numéro<32; numéro++) fermerRéseau(numéro);
    for (unsigned numéro=0; numéro<4; numéro++) contrôleUtilisateurCarteMatérielle(32+numéro);
    __asm__ volatile("msr daifset, #15; dsb sy" ::: "memory");
    uARTAfficherLigne("\r\nPOWER OFF\r\n");
    while (registreMachine(périphériqueSériel+0x18)&8) __asm__ volatile("yield");
    /* BCM power manager: firmware halt partition, then watchdog reset. */
    registreMachine(0xfe100020ul)=0x5a000000u | (registreMachine(0xfe100020ul)&~0xfffu) | 0x555;
    registreMachine(0xfe100024ul)=0x5a000000u | 10;
    registreMachine(0xfe10001cul)=0x5a000000u | (registreMachine(0xfe10001cul)&~0x30u) | 0x20;
    barrièreMémoire();
    for (;;) __asm__ volatile("wfe");
}

motMachine tamponImageCarteMatérielle(void) {
    if (prêtÉcran) return 1;
    /* QEMU xres/yres 또는 Pi 펌웨어의 HDMI 설정에서 élémentListeActuel 크기를 읽는다. */
    const uint32_t valeurInterroger[] = {8 * 4, 0, 0x40003, 8, 0, 0, 0, 0};
    uint32_t largeurDemandé = 640, hauteurDemandé = 480;
    for (size_t indiceOrdinal = 0; indiceOrdinal < sizeof(valeurInterroger)/4; indiceOrdinal++) donnéesBoîteMessages[indiceOrdinal] = valeurInterroger[indiceOrdinal];
    if (boîteMessages() && donnéesBoîteMessages[4] == 0x80000008u &&
        donnéesBoîteMessages[5] >= 640 && donnéesBoîteMessages[5] <= 1920 &&
        donnéesBoîteMessages[6] >= 480 && donnéesBoîteMessages[6] <= 1080) {
        largeurDemandé = donnéesBoîteMessages[5]; hauteurDemandé = donnéesBoîteMessages[6];
    }
    const uint32_t requête[] = {
        35 * 4, 0,
        0x48003, 8, 0, largeurDemandé, hauteurDemandé,
        0x48004, 8, 0, largeurDemandé, hauteurDemandé,
        0x48005, 4, 0, 32,
        0x48006, 4, 0, 1,
        0x48009, 8, 0, 0, 0,
        0x40001, 8, 0, 4096, 0,
        0x40008, 4, 0, 0,
        0
    };
    for (size_t indiceOrdinal = 0; indiceOrdinal < sizeof(requête)/4; indiceOrdinal++) donnéesBoîteMessages[indiceOrdinal] = requête[indiceOrdinal];
    // valeurSommet 메시지의 donnéesEffectif 길이를 valeurUtiliser: 태그 ajouterFinEntréeÉlément 시 longueur 불일치를 방지한다.
    donnéesBoîteMessages[0] = sizeof(requête);
    if (!boîteMessages()) return 0;
    const unsigned réponsesListe[] = {4, 9, 14, 18, 22, 27, 32};
    const unsigned longueurRéponseRetour[] = {8, 8, 4, 4, 8, 8, 4};
    for (unsigned indiceOrdinal = 0; indiceOrdinal < sizeof(réponsesListe)/sizeof(réponsesListe[0]); indiceOrdinal++)
        if (donnéesBoîteMessages[réponsesListe[indiceOrdinal]] != (0x80000000u | longueurRéponseRetour[indiceOrdinal])) return 0;
    uint32_t valeurArrièrePlan = donnéesBoîteMessages[28] & 0x3fffffffu;
    uint32_t taille = donnéesBoîteMessages[29];
    uint32_t largeurReçu = donnéesBoîteMessages[5], hauteurReçu = donnéesBoîteMessages[6], espacementLigneReçu = donnéesBoîteMessages[33];
    if (donnéesBoîteMessages[15] != 32 || donnéesBoîteMessages[19] != 1 ||
        largeurReçu < 640 || largeurReçu > 1920 || hauteurReçu < 480 || hauteurReçu > 1080 ||
        donnéesBoîteMessages[10] < largeurReçu || donnéesBoîteMessages[11] < hauteurReçu || donnéesBoîteMessages[23] || donnéesBoîteMessages[24] ||
        !valeurArrièrePlan || valeurArrièrePlan < 0x1000000 || (valeurArrièrePlan & 3) || espacementLigneReçu < largeurReçu * 4 || (espacementLigneReçu & 3) ||
        (uint64_t)espacementLigneReçu * hauteurReçu > taille || (uint64_t)valeurArrièrePlan + taille > 0x40000000u)
        return 0;
    dessinPréparerCarteMatérielle((volatile uint32_t *)(uintptr_t)valeurArrièrePlan, largeurReçu, hauteurReçu, espacementLigneReçu);
    prêtÉcran = 1;
    return 1;
}

// 단일 코어의 협력식 valeurFilExécution. MMU 격리, 선점, pthread ABI는 아직 없다.
typedef struct { uint64_t enregistré[13]; } contexte;
static contexte contextes[3];
static unsigned char piles[2][65536] __attribute__((aligned(16)));
static int estEnExécution[3] = {1, 0, 0};
static int tâcheActuel;
extern void commuterContexte(contexte *, contexte *);
extern void tâcheJava(int32_t);
motMachine céderCarteMatérielle(void) {
    network_poll();
    int élémentListePrécédentÉlément = tâcheActuel, élémentListeSuivant = (élémentListePrécédentÉlément + 1) % 3;
    while (élémentListeSuivant != élémentListePrécédentÉlément && !estEnExécution[élémentListeSuivant]) élémentListeSuivant = (élémentListeSuivant + 1) % 3;
    if (élémentListeSuivant != élémentListePrécédentÉlément) {
        for (unsigned indiceOrdinal = 0; indiceOrdinal < 2; indiceOrdinal++)
            if (estEnExécution[indiceOrdinal + 1] && *(uint64_t *)piles[indiceOrdinal] != 0x6b6f726f7373746bull)
                arrêtFatalNoyau("task stack guard");
        tâcheActuel = élémentListeSuivant;
        commuterContexte(&contextes[élémentListePrécédentÉlément], &contextes[élémentListeSuivant]);
    }
    return 0;
}
static void amorçageInitialTâche(void) {
    tâcheJava(tâcheActuel);
    estEnExécution[tâcheActuel] = 0;
    céderCarteMatérielle();
    arrêtFatalNoyau("finished task resumed");
}
motMachine créerTâcheCarteMatérielle(motMachine valeurIdentificateur) {
    if (valeurIdentificateur < 1 || valeurIdentificateur > 2 || estEnExécution[valeurIdentificateur]) return (uint32_t)-1;
    memset(&contextes[valeurIdentificateur], 0, sizeof(contexte));
    *(uint64_t *)piles[valeurIdentificateur - 1] = 0x6b6f726f7373746bull;
    contextes[valeurIdentificateur].enregistré[11] = (uintptr_t)amorçageInitialTâche;
    contextes[valeurIdentificateur].enregistré[12] = (uintptr_t)(piles[valeurIdentificateur - 1] + sizeof(piles[0]));
    estEnExécution[valeurIdentificateur] = 1;
    return 0;
}
motMachine étatValeurTâcheCarteMatérielle(motMachine valeurIdentificateur) { return valeurIdentificateur < 3 ? estEnExécution[valeurIdentificateur] : (uint32_t)-1; }
extern motMachine rechercherMémoireCompilationAnticipée(motMachine);
extern uint32_t lireÉtatValeurUtilisateur(unsigned, unsigned);
extern unsigned char SommetPile[];
motMachine systèmeInterrogerCarteMatérielle(motMachine valeurEntréeÉlément, motMachine numéro) {
    if (valeurEntréeÉlément==0) return unitéOctetKibiMémoireARM;
    if (valeurEntréeÉlément==1) return ((uintptr_t)SommetPile-0x80000+1023)/1024;
    if (valeurEntréeÉlément==2 || valeurEntréeÉlément==3) return rechercherMémoireCompilationAnticipée(valeurEntréeÉlément==3);
    if (valeurEntréeÉlément==4) return prêtÉcran ? (largeurÉcranCarteMatérielle()*hauteurÉcranCarteMatérielle()*4+1023)/1024 : 0;
    if (valeurEntréeÉlément==5) return 80*1024; /* exécuterCommande régionAdresse 16 MiB + 네 세션 préserverValeur régionAdresse. */
    if (valeurEntréeÉlément>=20) return lireÉtatValeurUtilisateur(valeurEntréeÉlément-20, numéro);
    return 0;
}
int *pk_errno_location(void) { static int erreurs[3]; return &erreurs[tâcheActuel]; }
