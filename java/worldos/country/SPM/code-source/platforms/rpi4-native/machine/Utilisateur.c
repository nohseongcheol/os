#include "../nommage/nomsLierMachine.h"
#include "informationÉcran.h"
// EL0 exécuterCommande machine valeurCouche. Fichier Données/정책은 기존 AOT Java 커널에 위임한다.
#include "Utilisateur.h"
#include "ABIFichier.h"
#include "ABIRéseau.h"
#include "../PileRéseau/PileRéseau.h"
extern int32_t distantRéseauJava(int32_t), adresseFluxJava(int32_t);
#define registreMachine(valeurPremier) (*(volatile uint32_t *)(uintptr_t)(valeurPremier))
#define distributeurInterrompre 0xff841000ul
#define interfaceCPUInterrompre 0xff842000ul
#define taillePage 4096ul
#define marqueurAccès (1ul << 10)
#define permissionExécuterAucun (1ul << 53)
#define exécuterAucunUtilisateur (1ul << 54)
#define mémoireNormal ((1ul << 2) | (3ul << 8) | marqueurAccès)
#define pageNoyau (3ul | mémoireNormal | permissionExécuterAucun | exécuterAucunUtilisateur)
#define écrireLireUtilisateur (3ul | mémoireNormal | (1ul << 6) | permissionExécuterAucun | exécuterAucunUtilisateur)
#define seulementLireUtilisateur (3ul | mémoireNormal | (3ul << 6) | permissionExécuterAucun | exécuterAucunUtilisateur)
#define exécuterLireUtilisateur (3ul | mémoireNormal | (3ul << 6) | permissionExécuterAucun)
extern void *memcpy(void *, const void *, size_t);
extern void *memset(void *, int, size_t);
extern uintptr_t écrireCaractèreCarteMatérielle(uintptr_t), obtenirCaractèreCarteMatérielle(void), millisecondesÉcouléesCarteMatérielle(void);
extern uintptr_t pixelCarteMatérielle(uintptr_t, uintptr_t, uintptr_t);
extern uintptr_t tamponImageCarteMatérielle(void);
extern uintptr_t terminalCarteMatérielle(uintptr_t);
extern int enAttenteTerminal(void);
extern int32_t interactifConsoleJava(void);
extern int32_t démarrerCheminJava(int32_t), octetCheminJava(int32_t,int32_t);
extern int32_t répertoireCréerJava(void), répertoireSupprimerJava(void), genreEntréeÉlémentJava(void);
extern int invoquerÉcran(int,unsigned,int,int,int,int,int),texteÉcran(int,int,const uint32_t *,unsigned);
extern void initialiserÉcran(int),enfoncerÉcran(int,unsigned);
extern int reprendreUtilisateur(cadreUtilisateur *,void *);
extern void enregistrerVirguleFlottanteUtilisateur(void *);
extern int entrerUtilisateur(uintptr_t pointEntréeÉlément, uintptr_t stockagePile, uintptr_t valeurTransféré);
extern void retournerUtilisateur(void);
extern void arrêtFatalNoyau(const char *) __attribute__((noreturn));
static uint64_t adresseRacine[512] __attribute__((aligned(4096)));
static uint64_t milieu[4][512] __attribute__((aligned(4096)));
static uint64_t listePage[nombreÉlémentsPageUtilisateur] __attribute__((aligned(4096)));
static uint8_t listePermissions[nombreÉlémentsPageUtilisateur];
static int actif, listeFichier[16], aBILinux;
static unsigned extrémitésPriseRéseau[24];
extern int32_t priseRéseauRéseauJava(int32_t, int32_t, int32_t), associerRéseauJava(int32_t, int32_t, int32_t);
extern int32_t placerRéseauJava(int32_t, int32_t), obtenirRéseauJava(int32_t), envoyerRéseauJava(int32_t, int32_t, int32_t, int32_t);
extern int32_t opérationRéceptionRéseauJava(int32_t, int32_t), portRéseauJava(int32_t), adresseRéseauJava(int32_t), pairRéseauRéseauJava(int32_t), fermerRéseauJava(int32_t);
extern int32_t créerFluxJava(void),associerFluxJava(int32_t,int32_t,int32_t),écouterFluxJava(int32_t,int32_t),connecterFluxJava(int32_t,int32_t,int32_t),accepterFluxJava(int32_t),lireFluxJava(int32_t,int32_t),écrireFluxJava(int32_t,int32_t),portFluxJava(int32_t),pairRéseauFluxJava(int32_t),fermerFluxJava(int32_t);
static int fermerExtrémitéPriseRéseau(unsigned poignéeFichier){return poignéeFichier<40?fermerRéseauJava(poignéeFichier):fermerFluxJava(poignéeFichier);}
static uint64_t fréquence, tempsÉchéance;
static uintptr_t finTas;
// valeurNoyau 셸이 준비한 UTF-8 arguments. EL0에는 copierValeur 호출만 제공한다.
static unsigned nombreÉlémentsArgumentTransféré, longueurArgumentTransféré[8];
static unsigned char argumentTransféré[8][256];
typedef struct {
    int étatValeurEnPause,interactif,aBILinux,listeFichier[16]; unsigned extrémitésPriseRéseau[24],nombreÉlémentsArguments,longueurArgument[8];
    unsigned char tableauArgument[8][256],listePermissions[nombreÉlémentsPageUtilisateur];
    uintptr_t stockageTas; cadreUtilisateur cadreExécution;
    unsigned char étatValeurPointFlottant[528] __attribute__((aligned(16)));
} processusEnregistré;
static processusEnregistré enregistré[4];
static int objetPropriétaire,interactif;
static uint32_t numéroUtilisateur[4], tempsDémarrerUtilisateur[4], tempsAccumuléUtilisateur[4], tempsExécutionUtilisateur[4], numéroUtilisateurSuivant=10;
static unsigned char nomCommandeUtilisateur[4][288];
uint32_t lireÉtatValeurUtilisateur(unsigned valeurEntréeÉlément, unsigned numéro) {
    unsigned indicePosition=numéro&3;
    int valeurÉtatValeur=(actif && objetPropriétaire==(int)indicePosition) ? 1 : enregistré[indicePosition].étatValeurEnPause ? 2 : 0;
    if (valeurEntréeÉlément==0) return valeurÉtatValeur;
    if (!valeurÉtatValeur) return 0;
    if (valeurEntréeÉlément==1) return numéroUtilisateur[indicePosition];
    if (valeurEntréeÉlément==2) {
        unsigned char *listePages=valeurÉtatValeur==1?listePermissions:enregistré[indicePosition].listePermissions;
        unsigned nombreÉlémentsPage=0; for (unsigned indiceOrdinal=0; indiceOrdinal<nombreÉlémentsPageUtilisateur; indiceOrdinal++) if(listePages[indiceOrdinal]) nombreÉlémentsPage++;
        return nombreÉlémentsPage*4;
    }
    if (valeurEntréeÉlément==3) return (uint32_t)millisecondesÉcouléesCarteMatérielle()-tempsDémarrerUtilisateur[indicePosition];
    if (valeurEntréeÉlément==4) return tempsAccumuléUtilisateur[indicePosition]+(valeurÉtatValeur==1?(uint32_t)millisecondesÉcouléesCarteMatérielle()-tempsExécutionUtilisateur[indicePosition]:0);
    if (valeurEntréeÉlément==5) return numéro/4<sizeof(nomCommandeUtilisateur[0])?nomCommandeUtilisateur[indicePosition][numéro/4]:0;
    return 0;
}
uintptr_t débutPositionArgumentsAppelCarteMatérielle(uintptr_t nombreÉlémentsEntréeÉlément) {
    if (actif || nombreÉlémentsEntréeÉlément > 8) return (uint32_t)-22;
    nombreÉlémentsArgumentTransféré = nombreÉlémentsEntréeÉlément;
    memset(longueurArgumentTransféré, 0, sizeof(longueurArgumentTransféré));
    memset(argumentTransféré, 0, sizeof(argumentTransféré));
    return 0;
}
uintptr_t octetArgumentsAppelCarteMatérielle(uintptr_t indiceRechercher, uintptr_t positionActuel, uintptr_t donnéesOctet) {
    if (actif || indiceRechercher >= nombreÉlémentsArgumentTransféré || positionActuel >= 255 || positionActuel != longueurArgumentTransféré[indiceRechercher] || !donnéesOctet || donnéesOctet > 255)
        return (uint32_t)-22;
    argumentTransféré[indiceRechercher][positionActuel] = donnéesOctet;
    longueurArgumentTransféré[indiceRechercher] = positionActuel + 1;
    return 0;
}
static void tablesSynchroniserDonnées(void) {
    __asm__ volatile("dsb sy; tlbi vmalle1; dsb sy; isb" ::: "memory");
}
static uint64_t valeurHorloge(void) { uint64_t donnéesTemporaire; __asm__ volatile("mrs %0, cntpct_el0" : "=r"(donnéesTemporaire)); return donnéesTemporaire; }
static void arrêterDélaiExpiration(void) {
    __asm__ volatile("msr cntp_ctl_el0, xzr; isb; dsb sy" ::: "memory");
    registreMachine(distributeurInterrompre + 0x280) = 1u << 30;
    __asm__ volatile("dsb sy" ::: "memory");
}
static void démarrerDélaiExpiration(void) {
    uint64_t valeurEspacement = fréquence * 2, activer = 1;
    tempsÉchéance = valeurHorloge() + valeurEspacement;
    __asm__ volatile("msr cntp_tval_el0, %0; msr cntp_ctl_el0, %1; isb" :: "r"(valeurEspacement), "r"(activer) : "memory");
}
void opérationInitialisationSystèmeUtilisateur(void) {
    for (unsigned blocDonnées = 0; blocDonnées < 4; blocDonnées++) {
        adresseRacine[blocDonnées] = (uintptr_t)milieu[blocDonnées] | 3;
        for (unsigned indiceOrdinal = 0; indiceOrdinal < 512; indiceOrdinal++) {
            uintptr_t adresse = ((uintptr_t)blocDonnées << 30) | ((uintptr_t)indiceOrdinal << 21);
            milieu[blocDonnées][indiceOrdinal] = adresse | 1 | marqueurAccès | exécuterAucunUtilisateur;
            if (adresse >= 0xfc000000ul) milieu[blocDonnées][indiceOrdinal] |= permissionExécuterAucun; // Device-nGnRnE
            else milieu[blocDonnées][indiceOrdinal] |= mémoireNormal; // Normal, non-cacheable
        }
    }
    for (unsigned valeurDeuxième = 0; valeurDeuxième < nombreÉlémentsPageUtilisateur / 512; valeurDeuxième++)
        milieu[0][(baseUtilisateur >> 21) + valeurDeuxième] = (uintptr_t)(listePage + valeurDeuxième * 512) | 3;
    for (unsigned indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsPageUtilisateur; indiceOrdinal++) listePage[indiceOrdinal] = (baseUtilisateur + indiceOrdinal * taillePage) | pageNoyau;
    uint64_t registreAttributMémoire = 0x4400, contrôleTraductionAdresse = 32 | (3ul << 12) | (1ul << 23), registreContrôleSystème;
    __asm__ volatile("dsb sy; msr mair_el1, %0; msr tcr_el1, %1; msr ttbr0_el1, %2; msr ttbr1_el1, xzr; isb"
        :: "r"(registreAttributMémoire), "r"(contrôleTraductionAdresse), "r"((uintptr_t)adresseRacine) : "memory");
    tablesSynchroniserDonnées();
    __asm__ volatile("mrs %0, sctlr_el1" : "=r"(registreContrôleSystème));
    registreContrôleSystème = (registreContrôleSystème & ~((1ul << 2) | (1ul << 12))) | 1;
    __asm__ volatile("msr sctlr_el1, %0; isb" :: "r"(registreContrôleSystème) : "memory");
    uint64_t étatValeurPointFlottant = 3ul << 20;
    __asm__ volatile("msr cpacr_el1, %0; isb" :: "r"(étatValeurPointFlottant) : "memory");
    __asm__ volatile("mrs %0, cntfrq_el0" : "=r"(fréquence));
    arrêterDélaiExpiration();
    // Pi4 GIC-400, non-secure physical timer PPI 30. IRQ는 EL0 valeurPointEntréeÉlément 때만 autoriserValeur.
    registreMachine(distributeurInterrompre) = 0;
    registreMachine(distributeurInterrompre + 0x180) = 0xffffffff;
    registreMachine(distributeurInterrompre + 0x80) = 0xffffffff;
    registreMachine(distributeurInterrompre + 0x280) = 1u << 30;
    registreMachine(distributeurInterrompre + 0x41c) = 0x80808080;
    registreMachine(distributeurInterrompre + 0x100) = 1u << 30;
    registreMachine(interfaceCPUInterrompre + 4) = 0xff;
    registreMachine(interfaceCPUInterrompre + 8) = 0;
    // Security 확장이 없는 GICv2는 Secure 뷰로 보인다. Group1 enable과
    // AckCtl을 함께 설정해야 IRQ 30을 IAR에서 estNormal 확인할 nombre 있다.
    int sécurité = (registreMachine(distributeurInterrompre + 4) & (1u << 10)) != 0;
    registreMachine(distributeurInterrompre) = sécurité ? 1 : 3;
    registreMachine(interfaceCPUInterrompre) = sécurité ? 1 : 7;
    __asm__ volatile("dsb sy; isb" ::: "memory");
}

typedef struct {
    unsigned char identifiant[16]; uint16_t catégorieType, typeMachine; uint32_t numéroVersion;
    uint64_t pointEntréeÉlément, décalageEntêteProgramme, décalageEntêteSection; uint32_t bitsConfiguration;
    uint16_t tailleEntêteCodeExécutable, tailleEntréeÉlémentEntêteProgramme, nombreÉlémentsEntêteProgramme, tailleEntréeÉlémentEntêteSection, nombreÉlémentsEntêteSection, indiceTableNomSection;
} entêteELF;
typedef struct { uint32_t catégorieType, bitsConfiguration; uint64_t valeurDécalage, adresse, adressePhysique, tailleZoneFichier, tailleZoneMémoire, frontièreAligner; } programmeELF;
_Static_assert(sizeof(entêteELF) == 64 && sizeof(programmeELF) == 56, "ELF layout");
_Static_assert(sizeof(cadreUtilisateur) == 272, "exception assembly layout");
static int contenu(uint64_t valeurDécalage, uint64_t taille, uint64_t décalageFin) {
    return valeurDécalage <= décalageFin && taille <= décalageFin - valeurDécalage;
}
static int contrôlerInformationAuxiliaire(const unsigned char *positionDonnées, size_t taille) {
    size_t positionActuel = 0;
    while (contenu(positionActuel, 12, taille)) {
        uint32_t motsLexical[3]; memcpy(motsLexical, positionDonnées + positionActuel, 12); positionActuel += 12;
        uint64_t tailleZoneNom = ((uint64_t)motsLexical[0] + 3) & ~3ul;
        uint64_t tailleDescription = ((uint64_t)motsLexical[1] + 3) & ~3ul;
        if (!contenu(positionActuel, tailleZoneNom, taille) || !contenu(positionActuel + tailleZoneNom, tailleDescription, taille)) return 0;
        const unsigned char nom[] = {'J','K','O','R','O','S',0};
        int estÉgal = motsLexical[0] == sizeof(nom) && motsLexical[1] == 4 && motsLexical[2] == 1;
        if (estÉgal) for (unsigned indiceOrdinal = 0; indiceOrdinal < sizeof(nom); indiceOrdinal++) if (positionDonnées[positionActuel + indiceOrdinal] != nom[indiceOrdinal]) estÉgal = 0;
        uint32_t numéroVersion = 0;
        if (estÉgal) memcpy(&numéroVersion, positionDonnées + positionActuel + tailleZoneNom, 4);
        if (estÉgal && numéroVersion == 1) return 1;
        positionActuel += tailleZoneNom + tailleDescription;
    }
    return 0;
}
static int validerELF(const unsigned char *Données, size_t taille, int modeLinux) {
    if (taille < sizeof(entêteELF)) return erreurCodeExécutableUtilisateur;
    entêteELF entêteCodeExécutable; memcpy(&entêteCodeExécutable, Données, sizeof(entêteCodeExécutable));
    if (entêteCodeExécutable.identifiant[0] != 127 || entêteCodeExécutable.identifiant[1] != 'E' || entêteCodeExécutable.identifiant[2] != 'L' || entêteCodeExécutable.identifiant[3] != 'F' ||
        entêteCodeExécutable.identifiant[4] != 2 || entêteCodeExécutable.identifiant[5] != 1 || entêteCodeExécutable.identifiant[6] != 1 || (entêteCodeExécutable.identifiant[7] != 0 && (!modeLinux || entêteCodeExécutable.identifiant[7] != 3)) ||
        entêteCodeExécutable.catégorieType != 2 || entêteCodeExécutable.typeMachine != 183 || entêteCodeExécutable.numéroVersion != 1 || entêteCodeExécutable.bitsConfiguration || entêteCodeExécutable.tailleEntêteCodeExécutable != sizeof(entêteCodeExécutable) ||
        entêteCodeExécutable.tailleEntréeÉlémentEntêteProgramme != sizeof(programmeELF) || !entêteCodeExécutable.nombreÉlémentsEntêteProgramme || entêteCodeExécutable.nombreÉlémentsEntêteProgramme > 16 ||
        entêteCodeExécutable.décalageEntêteProgramme < sizeof(entêteCodeExécutable) || !contenu(entêteCodeExécutable.décalageEntêteProgramme, (uint64_t)entêteCodeExécutable.nombreÉlémentsEntêteProgramme * sizeof(programmeELF), taille)) return erreurCodeExécutableUtilisateur;
    uint8_t capacitéUtilisé[(finImageUtilisateur - baseUtilisateur) / taillePage] = {0};
    int pointEntréeÉlémentValide = 0, correctÉtatABI = 0, chargements = 0;
    for (unsigned indiceOrdinal = 0; indiceOrdinal < entêteCodeExécutable.nombreÉlémentsEntêteProgramme; indiceOrdinal++) {
        programmeELF positionDonnées; memcpy(&positionDonnées, Données + entêteCodeExécutable.décalageEntêteProgramme + indiceOrdinal * sizeof(positionDonnées), sizeof(positionDonnées));
        if (positionDonnées.catégorieType == 4) {
            if (!contenu(positionDonnées.valeurDécalage, positionDonnées.tailleZoneFichier, taille)) return erreurCodeExécutableUtilisateur;
            if (contrôlerInformationAuxiliaire(Données + positionDonnées.valeurDécalage, positionDonnées.tailleZoneFichier)) correctÉtatABI = 1;
            continue;
        }
        if (positionDonnées.catégorieType == 0 || positionDonnées.catégorieType == 6 || (positionDonnées.catégorieType == 0x6474e551 && !(positionDonnées.bitsConfiguration & 1))) continue;
        if (positionDonnées.catégorieType != 1) return erreurCodeExécutableUtilisateur; // PT_INTERP, DYNAMIC, TLS estNonPrisEnCharge
        if (!positionDonnées.tailleZoneMémoire) continue;
        if (positionDonnées.bitsConfiguration & ~7u || !(positionDonnées.bitsConfiguration & 4) || (positionDonnées.bitsConfiguration & 3) == 3 || positionDonnées.tailleZoneFichier > positionDonnées.tailleZoneMémoire ||
            (positionDonnées.tailleZoneFichier && !contenu(positionDonnées.valeurDécalage, positionDonnées.tailleZoneFichier, taille)) || positionDonnées.adresse < baseUtilisateur ||
            !contenu(positionDonnées.adresse, positionDonnées.tailleZoneMémoire, finImageUtilisateur) ||
            (!modeLinux && ((positionDonnées.adresse & (taillePage - 1)) || (positionDonnées.valeurDécalage & (taillePage - 1)) || positionDonnées.frontièreAligner != taillePage)) ||
            (modeLinux && (((positionDonnées.adresse ^ positionDonnées.valeurDécalage) & (taillePage - 1)) || !positionDonnées.frontièreAligner ||
                (positionDonnées.frontièreAligner & (positionDonnées.frontièreAligner - 1)) || positionDonnées.frontièreAligner > 0x200000 || ((positionDonnées.adresse ^ positionDonnées.valeurDécalage) & (positionDonnées.frontièreAligner - 1))))) return erreurCodeExécutableUtilisateur;
        unsigned entréeÉlémentPremier = (positionDonnées.adresse - baseUtilisateur) / taillePage;
        unsigned nombreÉlémentsEntréeÉlément = ((positionDonnées.adresse & (taillePage - 1)) + positionDonnées.tailleZoneMémoire + taillePage - 1) / taillePage;
        for (unsigned valeurPage = entréeÉlémentPremier; valeurPage < entréeÉlémentPremier + nombreÉlémentsEntréeÉlément; valeurPage++) {
            if (capacitéUtilisé[valeurPage]) return erreurCodeExécutableUtilisateur;
            capacitéUtilisé[valeurPage] = 1;
        }
        if ((positionDonnées.bitsConfiguration & 1) && entêteCodeExécutable.pointEntréeÉlément >= positionDonnées.adresse && entêteCodeExécutable.pointEntréeÉlément < positionDonnées.adresse + positionDonnées.tailleZoneFichier && !(entêteCodeExécutable.pointEntréeÉlément & 3)) pointEntréeÉlémentValide = 1;
        chargements++;
    }
    return pointEntréeÉlémentValide && (modeLinux ? !correctÉtatABI : correctÉtatABI) && chargements ? 0 : erreurCodeExécutableUtilisateur;
}
int eLFValiderUtilisateur(const unsigned char *Données, size_t taille) { return validerELF(Données, taille, 0); }
static void dispositionPage(uintptr_t adresse, uint64_t bitsConfiguration, unsigned permissionsAccès) {
    unsigned indiceRechercher = (adresse - baseUtilisateur) / taillePage;
    listePage[indiceRechercher] = adresse | bitsConfiguration;
    listePermissions[indiceRechercher] = permissionsAccès;
}
static int plageUtilisateur(uintptr_t adresse, size_t nombreÉlémentsEntréeÉlément, int écritureEnCours) {
    if (adresse < baseUtilisateur || !contenu(adresse, nombreÉlémentsEntréeÉlément, finUtilisateur)) return 0;
    if (!nombreÉlémentsEntréeÉlément) return 1;
    unsigned entréeÉlémentPremier = (adresse - baseUtilisateur) / taillePage, élémentListeDernier = (adresse + nombreÉlémentsEntréeÉlément - 1 - baseUtilisateur) / taillePage;
    for (unsigned indiceOrdinal = entréeÉlémentPremier; indiceOrdinal <= élémentListeDernier; indiceOrdinal++) if (!(listePermissions[indiceOrdinal] & (écritureEnCours ? 2 : 1))) return 0;
    return 1;
}
static int copierChemin(uintptr_t adresse, char *chemin) {
    for (unsigned indiceOrdinal = 0; indiceOrdinal < 65; indiceOrdinal++) {
        if (!plageUtilisateur(adresse, 1, 0)) return -14;
        chemin[indiceOrdinal] = *(const char *)adresse++;
        if (!chemin[indiceOrdinal]) return 0;
    }
    return -36;
}
static intptr_t résultatNoyau(intptr_t résultat) { return résultat < 0 ? -numéroErreur : résultat; }
static int descripteurFichierAssocié(uint64_t poignéeFichier) { return poignéeFichier >= 3 && poignéeFichier < 19 ? listeFichier[poignéeFichier - 3] : -1; }
static int propriétaireExtrémitéPriseRéseau(uint64_t poignéeFichier) { return poignéeFichier >= 32 && poignéeFichier < 56 && extrémitésPriseRéseau[poignéeFichier - 32]; }
static int entréeAdresse(uintptr_t valeurPointageEnCours, size_t longueur, struct pk_sockaddr_in *adresse) {
    if (longueur != sizeof(*adresse)) return -22;
    if (!plageUtilisateur(valeurPointageEnCours, longueur, 0)) return -14;
    memcpy(adresse, (const void *)valeurPointageEnCours, sizeof(*adresse));
    return adresse->sin_family == AF_INET ? 0 : -97;
}
static int contrôlerSortieAdresse(uintptr_t valeurPointageEnCours, uintptr_t pointeurLongueur, pk_socklen_t *capacitéTampon) {
    if (!plageUtilisateur(pointeurLongueur, sizeof(*capacitéTampon), 1)) return -14;
    memcpy(capacitéTampon, (const void *)pointeurLongueur, sizeof(*capacitéTampon));
    if (*capacitéTampon > sizeof(struct pk_sockaddr_in)) *capacitéTampon = sizeof(struct pk_sockaddr_in);
    if (*capacitéTampon && !plageUtilisateur(valeurPointageEnCours, *capacitéTampon, 1)) return -14;
    return 0;
}
static void sortieAdresse(uintptr_t valeurPointageEnCours, uintptr_t pointeurLongueur, pk_socklen_t capacitéTampon, int adresse, int numéroPort) {
    struct pk_sockaddr_in valeur; memset(&valeur, 0, sizeof(valeur));
    valeur.sin_family = AF_INET; valeur.sin_port = pk_htons(numéroPort); valeur.sin_addr.s_addr = pk_htonl(adresse);
    if (capacitéTampon) memcpy((void *)valeurPointageEnCours, &valeur, capacitéTampon);
    pk_socklen_t longueur = sizeof(valeur); memcpy((void *)pointeurLongueur, &longueur, sizeof(longueur));
}
extern uintptr_t canalCarteMatérielle(uintptr_t, uintptr_t);
static intptr_t appelSystèmeNatif(cadreUtilisateur *entréeÉlémentFichier) {
    uintptr_t valeurPremier = entréeÉlémentFichier->registreDonnées[0], valeurDeuxième = entréeÉlémentFichier->registreDonnées[1], codeCaractère = entréeÉlémentFichier->registreDonnées[2];
    char chemin[65];
    int poignéeFichier, résultat;
    switch (entréeÉlémentFichier->registreDonnées[8]) {
    case 0: return 1; // interne ABI 버전
    case 1: // write: pointeur 전체를 검사한 valeurRetourArrièreCôté Sortie/Fichier changerValeur
        if (codeCaractère > 65536) return -22;
        if (!plageUtilisateur(valeurDeuxième, codeCaractère, 0)) return -14;
        if (valeurPremier == 1 || valeurPremier == 2) {
            uint64_t démarrerSortie=valeurHorloge();
            for (size_t indiceOrdinal = 0; indiceOrdinal < codeCaractère; indiceOrdinal++) canalCarteMatérielle(valeurPremier, ((const unsigned char *)valeurDeuxième)[indiceOrdinal]);
            /* 큰 tty를 그린 valeurNoyau 시간만 돌려준다. EL0 calculRésultat 기한은 늘리지 않는다. */
            if(interactif){
                tempsÉchéance+=valeurHorloge()-démarrerSortie;
                __asm__ volatile("msr cntp_cval_el0, %0; isb" :: "r"(tempsÉchéance) : "memory");
            }
            return codeCaractère;
        }
        if(valeurPremier>=40&&propriétaireExtrémitéPriseRéseau(valeurPremier)){
            size_t nombreÉlémentsÉlémentListe=codeCaractère>512?512:codeCaractère;for(size_t indiceOrdinal=0;indiceOrdinal<nombreÉlémentsÉlémentListe;indiceOrdinal++)placerRéseauJava(indiceOrdinal,((const unsigned char *)valeurDeuxième)[indiceOrdinal]);return écrireFluxJava(valeurPremier,nombreÉlémentsÉlémentListe);
        }
        poignéeFichier = descripteurFichierAssocié(valeurPremier); if (poignéeFichier < 0) return -9;
        return résultatNoyau(pk_write(poignéeFichier, (const void *)valeurDeuxième, codeCaractère));
    case 2:
        if (codeCaractère > 65536) return -22;
        if (!plageUtilisateur(valeurDeuxième, codeCaractère, 1)) return -14;
        if (valeurPremier == 0) {
            size_t nombreÉlémentsÉlémentListe = 0;
            while (nombreÉlémentsÉlémentListe < codeCaractère) {
                int valeurCaractère = (int32_t)obtenirCaractèreCarteMatérielle(); if (valeurCaractère == -2) return nombreÉlémentsÉlémentListe; if (valeurCaractère < 0) break;
                ((unsigned char *)valeurDeuxième)[nombreÉlémentsÉlémentListe++] = valeurCaractère;
            }
            return nombreÉlémentsÉlémentListe ? (intptr_t)nombreÉlémentsÉlémentListe : (codeCaractère ? -11 : 0);
        }
        if(valeurPremier>=40&&propriétaireExtrémitéPriseRéseau(valeurPremier)){
            résultat=lireFluxJava(valeurPremier,codeCaractère>512?512:codeCaractère);if(résultat>0)for(int indiceOrdinal=0;indiceOrdinal<résultat;indiceOrdinal++)((unsigned char *)valeurDeuxième)[indiceOrdinal]=obtenirRéseauJava(indiceOrdinal);return résultat;
        }
        poignéeFichier = descripteurFichierAssocié(valeurPremier); if (poignéeFichier < 0) return -9;
        return résultatNoyau(pk_read(poignéeFichier, (void *)valeurDeuxième, codeCaractère));
    case 3:
        résultat = copierChemin(valeurPremier, chemin); if (résultat) return résultat;
        if (valeurDeuxième > 0x7ff) return -22;
        for (unsigned indiceOrdinal = 0; indiceOrdinal < 16; indiceOrdinal++) if (listeFichier[indiceOrdinal] < 0) {
            poignéeFichier = pk_open(chemin, (int)valeurDeuxième, 0600);
            if (poignéeFichier < 0) return -numéroErreur;
            listeFichier[indiceOrdinal] = poignéeFichier; return indiceOrdinal + 3;
        }
        return -24;
    case 4:
        if (propriétaireExtrémitéPriseRéseau(valeurPremier)) { résultat = fermerExtrémitéPriseRéseau(valeurPremier); if (!résultat) extrémitésPriseRéseau[valeurPremier - 32] = 0; return résultat; }
        poignéeFichier = descripteurFichierAssocié(valeurPremier); if (poignéeFichier < 0) return -9;
        résultat = pk_close(poignéeFichier); if (!résultat) listeFichier[valeurPremier - 3] = -1;
        return résultatNoyau(résultat);
    case 5:
        poignéeFichier = descripteurFichierAssocié(valeurPremier); if (poignéeFichier < 0) return -9;
        if (codeCaractère > 2) return -22;
        return résultatNoyau(pk_lseek(poignéeFichier, (int64_t)valeurDeuxième, codeCaractère));
    case 7: return millisecondesÉcouléesCarteMatérielle();
    case 8: { // brk: 별도 Utilisateur RW/NX valeurTas, 새로 노출되는 페이지는 0으로 initialiser
        if (!valeurPremier) return finTas;
        if (valeurPremier < finImageUtilisateur || valeurPremier > finTasUtilisateur) return -12;
        uintptr_t pagesAncien = (finTas + taillePage - 1) & ~(taillePage - 1);
        uintptr_t pagesNouveau = (valeurPremier + taillePage - 1) & ~(taillePage - 1);
        if (pagesNouveau > pagesAncien) {
            for (uintptr_t positionDonnées = pagesAncien; positionDonnées < pagesNouveau; positionDonnées += taillePage) dispositionPage(positionDonnées, pageNoyau, 0);
            tablesSynchroniserDonnées();
            memset((void *)pagesAncien, 0, pagesNouveau - pagesAncien);
            for (uintptr_t positionDonnées = pagesAncien; positionDonnées < pagesNouveau; positionDonnées += taillePage) dispositionPage(positionDonnées, écrireLireUtilisateur, 3);
        } else {
            for (uintptr_t positionDonnées = pagesNouveau; positionDonnées < pagesAncien; positionDonnées += taillePage) {
                listePage[(positionDonnées - baseUtilisateur) / taillePage] = 0; listePermissions[(positionDonnées - baseUtilisateur) / taillePage] = 0;
            }
        }
        finTas = valeurPremier; tablesSynchroniserDonnées(); return valeurPremier;
    }
    case 9:
        poignéeFichier = descripteurFichierAssocié(valeurPremier); return poignéeFichier < 0 ? -9 : résultatNoyau(pk_size(poignéeFichier));
    case 10:
        poignéeFichier = descripteurFichierAssocié(valeurPremier); return poignéeFichier < 0 ? -9 : résultatNoyau(pk_ftruncate(poignéeFichier, (int64_t)valeurDeuxième));
    case 11:
        résultat = copierChemin(valeurPremier, chemin); return résultat ? résultat : résultatNoyau(pk_unlink(chemin));
    case 12:
        poignéeFichier = descripteurFichierAssocié(valeurPremier); return poignéeFichier < 0 ? -9 : résultatNoyau(pk_fsync(poignéeFichier));
    case 13: { // 그래픽 기초 API: Utilisateur 포인터로 MMIO/framebuffer를 직접 노출하지 않음
        uintptr_t valeurLargeurDemandé = entréeÉlémentFichier->registreDonnées[3], valeurHauteurDemandé = entréeÉlémentFichier->registreDonnées[4];
        if (!tamponImageCarteMatérielle()) return -19;
        uintptr_t étendueÉcran = largeurÉcranCarteMatérielle(), longueurÉcran = hauteurÉcranCarteMatérielle();
        if (valeurPremier > étendueÉcran || valeurDeuxième > longueurÉcran || valeurLargeurDemandé > étendueÉcran - valeurPremier || valeurHauteurDemandé > longueurÉcran - valeurDeuxième) return -22;
        for (uintptr_t coordonnéeCoordonnéeVerticale = valeurDeuxième; coordonnéeCoordonnéeVerticale < valeurDeuxième + valeurHauteurDemandé; coordonnéeCoordonnéeVerticale++) for (uintptr_t coordonnéeCoordonnéeHorizontale = valeurPremier; coordonnéeCoordonnéeHorizontale < valeurPremier + valeurLargeurDemandé; coordonnéeCoordonnéeHorizontale++) pixelCarteMatérielle(coordonnéeCoordonnéeHorizontale, coordonnéeCoordonnéeVerticale, codeCaractère);
        return 0;
    }
    case 14: return (int32_t)obtenirCaractèreCarteMatérielle();
    case 15: // args(-1,0,0)=nombreÉlémentsÉlémentListe; args(index,buffer,capacity)=UTF-8 longueur
        if (valeurPremier == UINTPTR_MAX) return nombreÉlémentsArgumentTransféré;
        if (valeurPremier >= nombreÉlémentsArgumentTransféré) return -22;
        if (codeCaractère <= longueurArgumentTransféré[valeurPremier]) return -36;
        if (!plageUtilisateur(valeurDeuxième, longueurArgumentTransféré[valeurPremier] + 1, 1)) return -14;
        memcpy((void *)valeurDeuxième, argumentTransféré[valeurPremier], longueurArgumentTransféré[valeurPremier] + 1);
        return longueurArgumentTransféré[valeurPremier];
    case 16: // Interactive tty: cooperative wait renews the 2-second CPU deadline.
        if(valeurPremier==0){if(!interactifConsoleJava())return -95;interactif=1;return terminalCarteMatérielle(13);}
        if(valeurPremier==2){interactif=0;return 0;}
        if(valeurPremier==3)return terminalCarteMatérielle(13);
        if(valeurPremier!=1||!interactif)return -22;
        résultat=(int32_t)obtenirCaractèreCarteMatérielle();
        if(résultat==-4096)return résultat;
        démarrerDélaiExpiration();return résultat<0?-11:résultat;
    case 17: { // 유한한 협력 attendreValeur: Communication 처리를 계속하며 CPU 독점 제한을 새로 시작한다.
        if (valeurPremier > 100) return -22;
        uint64_t tempsFin = valeurHorloge() + fréquence * valeurPremier / 1000;
        do { inspecterRéseau(); inspecterTransfertFichier(); __asm__ volatile("yield"); } while (valeurHorloge() < tempsFin);
        démarrerDélaiExpiration(); return 0;
    }
    case 18: { // kind(0), mkdir(1), rmdir(2); VFS가 경로와 valeurParent·빈 폴더를 검사한다.
        if (valeurDeuxième > 2) return -22;
        résultat = copierChemin(valeurPremier, chemin); if (résultat) return résultat;
        unsigned longueur = 0; while (chemin[longueur]) longueur++;
        résultat = démarrerCheminJava(longueur); if (résultat < 0) return résultat;
        for (unsigned indiceOrdinal = 0; indiceOrdinal < longueur; indiceOrdinal++) octetCheminJava(indiceOrdinal, (unsigned char)chemin[indiceOrdinal]);
        return valeurDeuxième == 0 ? genreEntréeÉlémentJava() : valeurDeuxième == 1 ? répertoireCréerJava() : répertoireSupprimerJava();
    }
    case 20:
        if(valeurPremier==5){int valeurCaractère=(int32_t)obtenirCaractèreCarteMatérielle();if(valeurCaractère==-4096)return valeurCaractère;if(valeurCaractère>=0)enfoncerÉcran(objetPropriétaire,valeurCaractère);démarrerDélaiExpiration();}
        if(valeurPremier==3&&codeCaractère){if(!interactifConsoleJava())return -95;interactif=1;terminalCarteMatérielle(300);}
        return invoquerÉcran(objetPropriétaire,valeurPremier,valeurDeuxième,codeCaractère,entréeÉlémentFichier->registreDonnées[3],entréeÉlémentFichier->registreDonnées[4],entréeÉlémentFichier->registreDonnées[5]);
    case 21:
        if(codeCaractère>127)return -22;if(!plageUtilisateur(valeurDeuxième,codeCaractère*sizeof(uint32_t),0))return -14;
        return texteÉcran(objetPropriétaire,valeurPremier,(const uint32_t *)valeurDeuxième,codeCaractère);
    case 22: // Écran taille valeurInterroger: 0=valeurLargeur, 1=valeurHauteur. 사용자에게 주소를 노출하지 않는다.
        if (valeurPremier > 1) return -22;
        if (!tamponImageCarteMatérielle()) return -19;
        return valeurPremier == 0 ? largeurÉcranCarteMatérielle() : hauteurÉcranCarteMatérielle();
    case 32:
        if (valeurPremier != AF_INET) return -97;
        if(valeurDeuxième==SOCK_STREAM&&(codeCaractère==0||codeCaractère==6))résultat=créerFluxJava();
        else if(valeurDeuxième==SOCK_DGRAM&&(codeCaractère==0||codeCaractère==IPPROTO_UDP))résultat=priseRéseauRéseauJava(valeurPremier,valeurDeuxième,codeCaractère);
        else return -93;
        if (résultat >= 32 && résultat < 56) extrémitésPriseRéseau[résultat - 32] = 1;
        return résultat;
    case 33: {
        if (!propriétaireExtrémitéPriseRéseau(valeurPremier)) return -9;
        struct pk_sockaddr_in adresse;
        résultat = entréeAdresse(valeurDeuxième, codeCaractère, &adresse); if (résultat) return résultat;
        return valeurPremier>=40?associerFluxJava(valeurPremier,pk_htonl(adresse.sin_addr.s_addr),pk_htons(adresse.sin_port)):associerRéseauJava(valeurPremier, pk_htonl(adresse.sin_addr.s_addr), pk_htons(adresse.sin_port));
    }
    case 34: {
        if (!propriétaireExtrémitéPriseRéseau(valeurPremier)) return -9;
        if(valeurPremier>=40)return -95;
        if (entréeÉlémentFichier->registreDonnées[3]) return -95;
        if (codeCaractère > 512) return -90;
        if (codeCaractère && !plageUtilisateur(valeurDeuxième, codeCaractère, 0)) return -14;
        struct pk_sockaddr_in adresse;
        résultat = entréeAdresse(entréeÉlémentFichier->registreDonnées[4], entréeÉlémentFichier->registreDonnées[5], &adresse); if (résultat) return résultat;
        for (unsigned indiceOrdinal = 0; indiceOrdinal < codeCaractère; indiceOrdinal++) placerRéseauJava(indiceOrdinal, ((const unsigned char *)valeurDeuxième)[indiceOrdinal]);
        return envoyerRéseauJava(valeurPremier, pk_htonl(adresse.sin_addr.s_addr), pk_htons(adresse.sin_port), codeCaractère);
    }
    case 35: {
        if (!propriétaireExtrémitéPriseRéseau(valeurPremier)) return -9;
        if(valeurPremier>=40)return -95;
        if (entréeÉlémentFichier->registreDonnées[3]) return -95;
        if (codeCaractère > 512) return -90;
        if (codeCaractère && !plageUtilisateur(valeurDeuxième, codeCaractère, 1)) return -14;
        pk_socklen_t capacitéTampon = 0;
        if (entréeÉlémentFichier->registreDonnées[4]) { résultat = contrôlerSortieAdresse(entréeÉlémentFichier->registreDonnées[4], entréeÉlémentFichier->registreDonnées[5], &capacitéTampon); if (résultat) return résultat; }
        résultat = opérationRéceptionRéseauJava(valeurPremier, codeCaractère); if (résultat < 0) return résultat;
        for (int indiceOrdinal = 0; indiceOrdinal < résultat; indiceOrdinal++) ((unsigned char *)valeurDeuxième)[indiceOrdinal] = obtenirRéseauJava(indiceOrdinal);
        if (entréeÉlémentFichier->registreDonnées[4]) sortieAdresse(entréeÉlémentFichier->registreDonnées[4], entréeÉlémentFichier->registreDonnées[5], capacitéTampon, distantRéseauJava(valeurPremier), pairRéseauRéseauJava(valeurPremier));
        return résultat;
    }
    case 36: {
        if (!propriétaireExtrémitéPriseRéseau(valeurPremier)) return -9;
        pk_socklen_t capacitéTampon;
        résultat = contrôlerSortieAdresse(valeurDeuxième, codeCaractère, &capacitéTampon); if (résultat) return résultat;
        sortieAdresse(valeurDeuxième,codeCaractère,capacitéTampon,valeurPremier>=40?adresseFluxJava(valeurPremier):adresseRéseauJava(valeurPremier),valeurPremier>=40?portFluxJava(valeurPremier):portRéseauJava(valeurPremier)); return 0;
    }
    case 37: {
        if(valeurPremier<40||!propriétaireExtrémitéPriseRéseau(valeurPremier))return -9;struct pk_sockaddr_in adresse;
        résultat=entréeAdresse(valeurDeuxième,codeCaractère,&adresse);if(résultat)return résultat;
        return connecterFluxJava(valeurPremier,pk_htonl(adresse.sin_addr.s_addr),pk_htons(adresse.sin_port));
    }
    case 38: return valeurPremier>=40&&propriétaireExtrémitéPriseRéseau(valeurPremier)?écouterFluxJava(valeurPremier,valeurDeuxième):-9;
    case 39:
        if(valeurPremier<40||!propriétaireExtrémitéPriseRéseau(valeurPremier))return -9;
        if(valeurDeuxième||codeCaractère)return -95;résultat=accepterFluxJava(valeurPremier);if(résultat>=40&&résultat<56)extrémitésPriseRéseau[résultat-32]=1;return résultat;
    case 40: return valeurPremier>=40&&propriétaireExtrémitéPriseRéseau(valeurPremier)?pairRéseauFluxJava(valeurPremier):-9;
    default: return -38; // estNonPrisEnCharge 기능을 성공으로 가장하지 않음
    }
}
#include "compatibilitéLinux.inc"
static intptr_t AppelSystème(cadreUtilisateur *entréeÉlémentFichier) {
    network_poll();
    return aBILinux ? appelSystèmeLinux(entréeÉlémentFichier) : appelSystèmeNatif(entréeÉlémentFichier);
}
static void noyauRetourner(cadreUtilisateur *entréeÉlémentFichier, int résultat) {
    arrêterDélaiExpiration();
    entréeÉlémentFichier->registreDonnées[0] = (uint64_t)(int64_t)résultat;
    entréeÉlémentFichier->positionCommande = (uintptr_t)retournerUtilisateur;
    entréeÉlémentFichier->codeÉtatValeur = 0x3c5; // EL1h, DAIF masked
}
int exceptionUtilisateur(cadreUtilisateur *entréeÉlémentFichier, unsigned intercepterSignal) {
    if (!actif || (entréeÉlémentFichier->codeÉtatValeur & 15) != 0) return 0;
    if (intercepterSignal) {
        uint32_t valeurAccuséRéception = registreMachine(interfaceCPUInterrompre + 0xc), valeurIdentificateur = valeurAccuséRéception & 1023;
        if (valeurIdentificateur == 30) { noyauRetourner(entréeÉlémentFichier, délaiExpirationUtilisateur); registreMachine(interfaceCPUInterrompre + 0x10) = valeurAccuséRéception; return 1; }
        if (valeurIdentificateur < 1020) registreMachine(interfaceCPUInterrompre + 0x10) = valeurAccuséRéception;
        return 1;
    }
    uint64_t étatValeurException; __asm__ volatile("mrs %0, esr_el1" : "=r"(étatValeurException));
    if (valeurHorloge() >= tempsÉchéance) { noyauRetourner(entréeÉlémentFichier, délaiExpirationUtilisateur); return 1; }
    unsigned catégorieException = étatValeurException >> 26;
    if (catégorieException == 0x15 && (étatValeurException & 0xffff) == 0) {
        if (aBILinux ? entréeÉlémentFichier->registreDonnées[8] == 93 || entréeÉlémentFichier->registreDonnées[8] == 94 : entréeÉlémentFichier->registreDonnées[8] == 6) noyauRetourner(entréeÉlémentFichier, (int)(entréeÉlémentFichier->registreDonnées[0] & 255));
        else {
            intptr_t résultat=AppelSystème(entréeÉlémentFichier);
            if(résultat==-4096&&interactif){
                enregistré[objetPropriétaire].cadreExécution=*entréeÉlémentFichier;enregistré[objetPropriétaire].cadreExécution.positionCommande-=4;
                enregistrerVirguleFlottanteUtilisateur(enregistré[objetPropriétaire].étatValeurPointFlottant);noyauRetourner(entréeÉlémentFichier,interrompuUtilisateur);
            }else entréeÉlémentFichier->registreDonnées[0]=(uint64_t)résultat;
        }
    } else noyauRetourner(entréeÉlémentFichier, catégorieException == 0x24 ? erreurDonnéesUtilisateur : catégorieException == 0x20 ? erreurExécutionUtilisateur : instructionMachineInvalideUtilisateur);
    return 1;
}

// 생성된 const ELF valeurGroupe: 실행은 반드시 Programme 헤더 검증을 통과해야 한다.
typedef struct { const unsigned char *Données; size_t taille; unsigned valeurTransféré; } programme;
#include "programs.h"
static void *instantané(unsigned indicePosition){return (void *)(0x04000000ul+indicePosition*(finUtilisateur-baseUtilisateur));}
static int terminerProgramme(int résultat){
    tempsAccumuléUtilisateur[objetPropriétaire]+=(uint32_t)millisecondesÉcouléesCarteMatérielle()-tempsExécutionUtilisateur[objetPropriétaire];
    arrêterDélaiExpiration();actif=0;
    if(résultat==interrompuUtilisateur){
        processusEnregistré *donnéesChaîne=&enregistré[objetPropriétaire];donnéesChaîne->étatValeurEnPause=1;donnéesChaîne->interactif=interactif;donnéesChaîne->aBILinux=aBILinux;donnéesChaîne->stockageTas=finTas;donnéesChaîne->nombreÉlémentsArguments=nombreÉlémentsArgumentTransféré;
        memcpy(donnéesChaîne->listePermissions,listePermissions,sizeof(listePermissions));memcpy(donnéesChaîne->listeFichier,listeFichier,sizeof(listeFichier));memcpy(donnéesChaîne->extrémitésPriseRéseau,extrémitésPriseRéseau,sizeof(extrémitésPriseRéseau));
        memcpy(donnéesChaîne->tableauArgument,argumentTransféré,sizeof(argumentTransféré));memcpy(donnéesChaîne->longueurArgument,longueurArgumentTransféré,sizeof(longueurArgumentTransféré));
        for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsPageUtilisateur;indiceOrdinal++)if(listePermissions[indiceOrdinal])memcpy((unsigned char *)instantané(objetPropriétaire)+indiceOrdinal*taillePage,(void *)(baseUtilisateur+indiceOrdinal*taillePage),taillePage);
    }else{
        enregistré[objetPropriétaire].étatValeurEnPause=0;initialiserÉcran(objetPropriétaire);
        for(unsigned indiceOrdinal=0;indiceOrdinal<16;indiceOrdinal++)if(listeFichier[indiceOrdinal]>=0)pk_close(listeFichier[indiceOrdinal]);
        for(unsigned indiceOrdinal=0;indiceOrdinal<24;indiceOrdinal++)if(extrémitésPriseRéseau[indiceOrdinal])fermerExtrémitéPriseRéseau(indiceOrdinal+32);
    }
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsPageUtilisateur;indiceOrdinal++){listePage[indiceOrdinal]=0;listePermissions[indiceOrdinal]=0;}tablesSynchroniserDonnées();return résultat;
}
uintptr_t contrôleUtilisateurCarteMatérielle(uintptr_t action){
    unsigned indicePosition=action&15;if(indicePosition>=4||actif)return (uint32_t)-22;
    processusEnregistré *donnéesChaîne=&enregistré[indicePosition];
    if(action>=32){if(donnéesChaîne->étatValeurEnPause){for(unsigned indiceOrdinal=0;indiceOrdinal<16;indiceOrdinal++)if(donnéesChaîne->listeFichier[indiceOrdinal]>=0)pk_close(donnéesChaîne->listeFichier[indiceOrdinal]);for(unsigned indiceOrdinal=0;indiceOrdinal<24;indiceOrdinal++)if(donnéesChaîne->extrémitésPriseRéseau[indiceOrdinal])fermerExtrémitéPriseRéseau(indiceOrdinal+32);}donnéesChaîne->étatValeurEnPause=0;initialiserÉcran(indicePosition);return 0;}
    if(action>=16)return donnéesChaîne->étatValeurEnPause;
    if(!donnéesChaîne->étatValeurEnPause)return (uint32_t)-22;
    objetPropriétaire=indicePosition;interactif=donnéesChaîne->interactif;aBILinux=donnéesChaîne->aBILinux;finTas=donnéesChaîne->stockageTas;nombreÉlémentsArgumentTransféré=donnéesChaîne->nombreÉlémentsArguments;
    memcpy(listeFichier,donnéesChaîne->listeFichier,sizeof(listeFichier));memcpy(extrémitésPriseRéseau,donnéesChaîne->extrémitésPriseRéseau,sizeof(extrémitésPriseRéseau));memcpy(argumentTransféré,donnéesChaîne->tableauArgument,sizeof(argumentTransféré));memcpy(longueurArgumentTransféré,donnéesChaîne->longueurArgument,sizeof(longueurArgumentTransféré));
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsPageUtilisateur;indiceOrdinal++)listePage[indiceOrdinal]=(baseUtilisateur+indiceOrdinal*taillePage)|pageNoyau;tablesSynchroniserDonnées();
    memset((void *)baseUtilisateur,0,finUtilisateur-baseUtilisateur);
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsPageUtilisateur;indiceOrdinal++)if(donnéesChaîne->listePermissions[indiceOrdinal])memcpy((void *)(baseUtilisateur+indiceOrdinal*taillePage),(unsigned char *)instantané(indicePosition)+indiceOrdinal*taillePage,taillePage);
    memcpy(listePermissions,donnéesChaîne->listePermissions,sizeof(listePermissions));
    for(unsigned indiceOrdinal=0;indiceOrdinal<nombreÉlémentsPageUtilisateur;indiceOrdinal++){unsigned positionDonnées=listePermissions[indiceOrdinal];listePage[indiceOrdinal]=positionDonnées?(baseUtilisateur+indiceOrdinal*taillePage)|(positionDonnées==3?écrireLireUtilisateur:positionDonnées==5?exécuterLireUtilisateur:seulementLireUtilisateur):0;}
    tablesSynchroniserDonnées();__asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");actif=1;donnéesChaîne->étatValeurEnPause=0;démarrerDélaiExpiration();
    tempsExécutionUtilisateur[objetPropriétaire]=millisecondesÉcouléesCarteMatérielle();
    return (uint32_t)terminerProgramme(reprendreUtilisateur(&donnéesChaîne->cadreExécution,donnéesChaîne->étatValeurPointFlottant));
}
static int lancerProgramme(const unsigned char *Données, size_t taille, unsigned valeurTransféré, int modeLinux, const char *nom) {
    if (actif) return -16;
    objetPropriétaire=terminalCarteMatérielle(11);if(objetPropriétaire<0||objetPropriétaire>3||enregistré[objetPropriétaire].étatValeurEnPause)return -16;interactif=0;
    int valide = validerELF(Données, taille, modeLinux); if (valide) return valide;
    aBILinux = modeLinux;
    unsigned indiceNom=0;
    while (*nom && indiceNom<31) nomCommandeUtilisateur[objetPropriétaire][indiceNom++]=(unsigned char)*nom++;
    if (nombreÉlémentsArgumentTransféré && longueurArgumentTransféré[0]) {
        if (indiceNom) nomCommandeUtilisateur[objetPropriétaire][indiceNom++]=' ';
        for (unsigned indicePosition=0; indicePosition<longueurArgumentTransféré[0]; indicePosition++) nomCommandeUtilisateur[objetPropriétaire][indiceNom++]=argumentTransféré[0][indicePosition];
    }
    nomCommandeUtilisateur[objetPropriétaire][indiceNom]=0; numéroUtilisateur[objetPropriétaire]=numéroUtilisateurSuivant++;
    if (numéroUtilisateurSuivant>0x7fffffffu) numéroUtilisateurSuivant=10;
    tempsDémarrerUtilisateur[objetPropriétaire]=millisecondesÉcouléesCarteMatérielle(); tempsAccumuléUtilisateur[objetPropriétaire]=0;
    for (unsigned indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsPageUtilisateur; indiceOrdinal++) listePage[indiceOrdinal] = (baseUtilisateur + indiceOrdinal * taillePage) | pageNoyau;
    tablesSynchroniserDonnées();
    memset((void *)baseUtilisateur, 0, finUtilisateur - baseUtilisateur);
    memset(listePermissions, 0, sizeof(listePermissions));
    entêteELF entêteCodeExécutable; memcpy(&entêteCodeExécutable, Données, sizeof(entêteCodeExécutable));
    for (unsigned indiceOrdinal = 0; indiceOrdinal < entêteCodeExécutable.nombreÉlémentsEntêteProgramme; indiceOrdinal++) {
        programmeELF positionDonnées; memcpy(&positionDonnées, Données + entêteCodeExécutable.décalageEntêteProgramme + indiceOrdinal * sizeof(positionDonnées), sizeof(positionDonnées));
        if (positionDonnées.catégorieType != 1 || !positionDonnées.tailleZoneMémoire) continue;
        if (positionDonnées.tailleZoneFichier) memcpy((void *)(uintptr_t)positionDonnées.adresse, Données + positionDonnées.valeurDécalage, positionDonnées.tailleZoneFichier);
        for (uintptr_t positionActuel = positionDonnées.adresse & ~(taillePage - 1); positionActuel < positionDonnées.adresse + positionDonnées.tailleZoneMémoire; positionActuel += taillePage) {
            listePermissions[(positionActuel - baseUtilisateur) / taillePage] = (positionDonnées.bitsConfiguration & 2) ? 3 : ((positionDonnées.bitsConfiguration & 1) ? 5 : 1);
        }
    }
    for (uintptr_t positionActuel = adressePileUtilisateur; positionActuel < finUtilisateur; positionActuel += taillePage) listePermissions[(positionActuel - baseUtilisateur) / taillePage] = 3;
    uintptr_t pileInitialValeur = modeLinux ? pileDémarrerLinux(entêteCodeExécutable.pointEntréeÉlément) : finUtilisateur;
    for (unsigned indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsPageUtilisateur; indiceOrdinal++) {
        unsigned permissionsAccès = listePermissions[indiceOrdinal];
        listePage[indiceOrdinal] = permissionsAccès ? (baseUtilisateur + indiceOrdinal * taillePage) | (permissionsAccès == 3 ? écrireLireUtilisateur : permissionsAccès == 5 ? exécuterLireUtilisateur : seulementLireUtilisateur) : 0;
    }
    tablesSynchroniserDonnées();
    __asm__ volatile("ic iallu; dsb sy; isb" ::: "memory");
    for (unsigned indiceOrdinal = 0; indiceOrdinal < 16; indiceOrdinal++) listeFichier[indiceOrdinal] = -1;
    memset(extrémitésPriseRéseau, 0, sizeof(extrémitésPriseRéseau));
    finTas = finImageUtilisateur;
    actif = 1; démarrerDélaiExpiration();
    tempsExécutionUtilisateur[objetPropriétaire]=millisecondesÉcouléesCarteMatérielle();
    int résultat = entrerUtilisateur(entêteCodeExécutable.pointEntréeÉlément, pileInitialValeur, valeurTransféré);
    return terminerProgramme(résultat);
}
uintptr_t lancerUtilisateurCarteMatérielle(uintptr_t indiceRechercher) {
    if (indiceRechercher >= sizeof(entréesListeCodeExécutable) / sizeof(entréesListeCodeExécutable[0])) return (uint32_t)-22;
    const char *nom=indiceRechercher==10?"javac":indiceRechercher==11?"java":indiceRechercher==12?"python":indiceRechercher==13?"vi":indiceRechercher==14?"jar":indiceRechercher==15?"cc":indiceRechercher==16?"jaot":"ELF";
    return (uint32_t)lancerProgramme(entréesListeCodeExécutable[indiceRechercher].Données, entréesListeCodeExécutable[indiceRechercher].taille, entréesListeCodeExécutable[indiceRechercher].valeurTransféré, 0, nom);
}
static uintptr_t exécuterFichier(int modeLinux) {
    static unsigned char image[16384];
    if (actif || !nombreÉlémentsArgumentTransféré) return (uint32_t)-22;
    int poignéeFichier = pk_open((const char *)argumentTransféré[0], lireValeurSeulement, 0);
    if (poignéeFichier < 0) return (uint32_t)-numéroErreur;
    int taille = pk_size(poignéeFichier);
    if (taille < 0 || (unsigned)taille > sizeof(image)) { pk_close(poignéeFichier); return (uint32_t)-27; }
    int nombreÉlémentsReçu = pk_read(poignéeFichier, image, taille); pk_close(poignéeFichier);
    if (nombreÉlémentsReçu != taille) return (uint32_t)-5;
    return (uint32_t)lancerProgramme(image, taille, 0, modeLinux, "");
}
uintptr_t fichierUtilisateurCarteMatérielle(void) { return exécuterFichier(0); }
uintptr_t fichierLinuxUtilisateurCarteMatérielle(void) { return exécuterFichier(1); }
uintptr_t validerUtilisateurCarteMatérielle(void) {
    for (unsigned indiceOrdinal = 0; indiceOrdinal < sizeof(exécutablesInvalide) / sizeof(exécutablesInvalide[0]); indiceOrdinal++)
        if (eLFValiderUtilisateur(exécutablesInvalide[indiceOrdinal].Données, exécutablesInvalide[indiceOrdinal].taille) != erreurCodeExécutableUtilisateur) return indiceOrdinal + 1;
    return 0;
}
