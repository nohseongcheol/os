#include "../nommage/nomsLierMachine.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "PileRéseau.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../valeurDistant/valeurDistant.h"
#include "réseauCâblé.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define registreMachine(valeurPremier) (*(volatile uint32_t *)(uintptr_t)(valeurPremier))
#define périphériqueAuxiliaire 0xfe215000ul
extern uintptr_t millisecondesÉcouléesCarteMatérielle(void);
static struct netif périphériqueConnexion;
static int estPréparé, scrutation;
static int réseauCâbléUtiliser;
static unsigned recevoirUtilisation, recevoirÉchapper, recevoirErreur;
static unsigned char recevoirTamponDonnées[1600];
static unsigned char donnéesTransmettre[32768];
static unsigned têteCôtéÉmission, nombreÉlémentsCôtéÉmission;
static uint32_t nombreÉlémentsDatagrammeReçu, nombreÉlémentsDatagrammeEnvoyé, nombreÉlémentsOctetReçu, nombreÉlémentsOctetEnvoyé, nombreÉlémentsDatagrammeAbandonnésNombre;
typedef struct {
    int catégorieType, recevoirPort, estEnAttente, connecté, finFichier, erreur;
    struct tcp_pcb *contrôleConnexion;
    struct udp_pcb *contrôleDatagramme;
    unsigned entréeÉlémentAvantCôté, nombreÉlémentsEntréeÉlément;
    unsigned char Données[4096];
    unsigned longueurs[4], ports[4], numéroExtrémitéPairRéseau;
    uint32_t adresses[4], adressePairRéseau;
} extrémitéPriseRéseau;
static extrémitéPriseRéseau extrémitésPriseRéseau[32];
u32_t sys_now(void) { return (u32_t)millisecondesÉcouléesCarteMatérielle(); }
static int numéroErreur(err_t entréeÉlémentAuxiliaire) {
    return entréeÉlémentAuxiliaire == ERR_MEM || entréeÉlémentAuxiliaire == ERR_BUF || entréeÉlémentAuxiliaire == ERR_WOULDBLOCK ? -11 : entréeÉlémentAuxiliaire == ERR_USE ? -98 :
        entréeÉlémentAuxiliaire == ERR_RTE ? -101 : entréeÉlémentAuxiliaire == ERR_RST ? -104 : entréeÉlémentAuxiliaire == ERR_CONN ? -107 : entréeÉlémentAuxiliaire == ERR_TIMEOUT ? -110 : -5;
}
static extrémitéPriseRéseau *obtenirValeur(int poignéeFichier) { return poignéeFichier >= 0 && poignéeFichier < 32 && extrémitésPriseRéseau[poignéeFichier].catégorieType ? &extrémitésPriseRéseau[poignéeFichier] : 0; }
static int réserver(int catégorieType) {
    for (int indiceOrdinal = 0; indiceOrdinal < 32; ++indiceOrdinal) if (!extrémitésPriseRéseau[indiceOrdinal].catégorieType) {
        memset(&extrémitésPriseRéseau[indiceOrdinal], 0, sizeof(extrémitéPriseRéseau)); extrémitésPriseRéseau[indiceOrdinal].catégorieType = catégorieType; extrémitésPriseRéseau[indiceOrdinal].estEnAttente = -1; return indiceOrdinal;
    }
    return -24;
}
static void émettreValeur(unsigned codeCaractère) { donnéesTransmettre[(têteCôtéÉmission + nombreÉlémentsCôtéÉmission++) % sizeof(donnéesTransmettre)] = codeCaractère; }
static err_t sortie(struct netif *nombreÉlémentsÉlémentListe, struct pbuf *positionDonnées, const ip4_addr_t *adresse) {
    (void)nombreÉlémentsÉlémentListe; (void)adresse;
    if (positionDonnées->tot_len > 1500 || nombreÉlémentsCôtéÉmission + 2 * positionDonnées->tot_len + 2 > sizeof(donnéesTransmettre)) return ERR_MEM;
    émettreValeur(192);
    for (struct pbuf *décalageSuivant = positionDonnées; décalageSuivant; décalageSuivant = décalageSuivant->next) for (unsigned indiceOrdinal = 0; indiceOrdinal < décalageSuivant->len; indiceOrdinal++) {
        unsigned codeCaractère = ((unsigned char *)décalageSuivant->payload)[indiceOrdinal];
        if (codeCaractère == 192 || codeCaractère == 219) { émettreValeur(219); émettreValeur(codeCaractère == 192 ? 220 : 221); } else émettreValeur(codeCaractère);
    }
    émettreValeur(192); nombreÉlémentsDatagrammeEnvoyé++; nombreÉlémentsOctetEnvoyé += positionDonnées->tot_len; return ERR_OK;
}
static err_t préparerEnvironnementExécution(struct netif *nombreÉlémentsÉlémentListe) { nombreÉlémentsÉlémentListe->name[0] = 's'; nombreÉlémentsÉlémentListe->name[1] = 'l'; nombreÉlémentsÉlémentListe->mtu = 1500; nombreÉlémentsÉlémentListe->output = sortie; return ERR_OK; }
void préparerRéseau(void) {
    if (estPréparé) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    registreMachine(périphériqueAuxiliaire + 4) |= 1; registreMachine(périphériqueAuxiliaire + 0x60) = 0; registreMachine(périphériqueAuxiliaire + 0x44) = 0;
    registreMachine(périphériqueAuxiliaire + 0x48) = 0xc6; registreMachine(périphériqueAuxiliaire + 0x4c) = 3; registreMachine(périphériqueAuxiliaire + 0x68) = 270; registreMachine(périphériqueAuxiliaire + 0x60) = 3;
    lwip_init();
    ip4_addr_t AdresseInternet, masqueBit, adressePasserelle;
    réseauCâbléUtiliser=possèdePériphériqueCâblé();
    ip4_addr_set_u32(&AdresseInternet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&masqueBit, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&adressePasserelle, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&périphériqueConnexion, &AdresseInternet, &masqueBit, &adressePasserelle, 0, réseauCâbléUtiliser?préparerRéseauCâblé:préparerEnvironnementExécution, réseauCâbléUtiliser?ethernet_input:ip4_input))return;
    netif_set_default(&périphériqueConnexion); netif_set_up(&périphériqueConnexion);if(!réseauCâbléUtiliser)netif_set_link_up(&périphériqueConnexion); estPréparé = 1;
    préparerDistant();
}
static err_t possèdeReçu(void *argumentsSupplémentaire, struct tcp_pcb *blocContrôleTransmission, struct pbuf *positionDonnées, err_t erreur) {
    extrémitéPriseRéseau *donnéesChaîne = argumentsSupplémentaire; (void)blocContrôleTransmission; (void)erreur;
    if (!positionDonnées) { donnéesChaîne->finFichier = 1; return ERR_OK; }
    if (positionDonnées->tot_len > sizeof(donnéesChaîne->Données) - donnéesChaîne->nombreÉlémentsEntréeÉlément) return ERR_MEM;
    unsigned positionActuel = (donnéesChaîne->entréeÉlémentAvantCôté + donnéesChaîne->nombreÉlémentsEntréeÉlément) % sizeof(donnéesChaîne->Données);
    for (struct pbuf *décalageSuivant = positionDonnées; décalageSuivant; décalageSuivant = décalageSuivant->next) for (unsigned indiceOrdinal = 0; indiceOrdinal < décalageSuivant->len; indiceOrdinal++) {
        donnéesChaîne->Données[positionActuel] = ((unsigned char *)décalageSuivant->payload)[indiceOrdinal]; positionActuel = (positionActuel + 1) % sizeof(donnéesChaîne->Données);
    }
    donnéesChaîne->nombreÉlémentsEntréeÉlément += positionDonnées->tot_len; pbuf_free(positionDonnées); return ERR_OK;
}
static void possèdeÉchoué(void *argumentsSupplémentaire, err_t erreur) { extrémitéPriseRéseau *donnéesChaîne = argumentsSupplémentaire; donnéesChaîne->contrôleConnexion = 0; donnéesChaîne->erreur = numéroErreur(erreur); }
static void rappels(extrémitéPriseRéseau *donnéesChaîne) { tcp_arg(donnéesChaîne->contrôleConnexion, donnéesChaîne); tcp_recv(donnéesChaîne->contrôleConnexion, possèdeReçu); tcp_err(donnéesChaîne->contrôleConnexion, possèdeÉchoué); }
static err_t connecté(void *argumentsSupplémentaire, struct tcp_pcb *blocContrôleTransmission, err_t erreur) {
    extrémitéPriseRéseau *donnéesChaîne = argumentsSupplémentaire; (void)blocContrôleTransmission; if (erreur) donnéesChaîne->erreur = numéroErreur(erreur); else donnéesChaîne->connecté = 1; return ERR_OK;
}
static err_t accepté(void *argumentsSupplémentaire, struct tcp_pcb *blocContrôleTransmission, err_t erreur) {
    extrémitéPriseRéseau *parent = argumentsSupplémentaire; if (erreur) return erreur;
    int poignéeFichier = réserver(1); if (poignéeFichier < 0) return ERR_MEM;
    extrémitéPriseRéseau *donnéesChaîne = &extrémitésPriseRéseau[poignéeFichier]; donnéesChaîne->contrôleConnexion = blocContrôleTransmission; donnéesChaîne->connecté = 1; donnéesChaîne->estEnAttente = (int)(parent - extrémitésPriseRéseau);
    donnéesChaîne->adressePairRéseau = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&blocContrôleTransmission->remote_ip))); donnéesChaîne->numéroExtrémitéPairRéseau = blocContrôleTransmission->remote_port;
    rappels(donnéesChaîne); return ERR_OK;
}
static void datagramme(void *argumentsSupplémentaire, struct udp_pcb *blocContrôleTransmission, struct pbuf *positionDonnées, const ip_addr_t *adresse, u16_t numéroPort) {
    extrémitéPriseRéseau *donnéesChaîne = argumentsSupplémentaire; (void)blocContrôleTransmission;
    if (donnéesChaîne->nombreÉlémentsEntréeÉlément < 4 && positionDonnées->tot_len <= 512) {
        unsigned indicePosition = (donnéesChaîne->entréeÉlémentAvantCôté + donnéesChaîne->nombreÉlémentsEntréeÉlément) % 4;
        pbuf_copy_partial(positionDonnées, donnéesChaîne->Données + indicePosition * 512, positionDonnées->tot_len, 0);
        donnéesChaîne->longueurs[indicePosition] = positionDonnées->tot_len; donnéesChaîne->ports[indicePosition] = numéroPort;
        donnéesChaîne->adresses[indicePosition] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresse))); donnéesChaîne->nombreÉlémentsEntréeÉlément++;
    }
    pbuf_free(positionDonnées);
}
int créerExtrémitéPriseRéseau(int catégorieType) {
    if (!estPréparé) return -100;
    if (catégorieType != 1 && catégorieType != 2) return -93;
    int poignéeFichier = réserver(catégorieType); if (poignéeFichier < 0) return poignéeFichier;
    extrémitéPriseRéseau *donnéesChaîne = &extrémitésPriseRéseau[poignéeFichier];
    if (catégorieType == 1) { donnéesChaîne->contrôleConnexion = tcp_new(); if (donnéesChaîne->contrôleConnexion) rappels(donnéesChaîne); }
    else { donnéesChaîne->contrôleDatagramme = udp_new(); if (donnéesChaîne->contrôleDatagramme) udp_recv(donnéesChaîne->contrôleDatagramme, datagramme, donnéesChaîne); }
    if (!donnéesChaîne->contrôleConnexion && !donnéesChaîne->contrôleDatagramme) { donnéesChaîne->catégorieType = 0; return -12; } return poignéeFichier;
}
int associerRéseauCourt(int poignéeFichier, uint32_t adresse, unsigned numéroPort) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne) return -9;
    if (numéroPort > 65535 || (adresse && adresse != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&périphériqueConnexion))) && adresse != 0x7f000001)) return -99;
    ip_addr_t AdresseInternet; ip_addr_set_ip4_u32(&AdresseInternet, lwip_htonl(adresse));
    err_t entréeÉlémentAuxiliaire = donnéesChaîne->catégorieType == 1 ? tcp_bind(donnéesChaîne->contrôleConnexion, &AdresseInternet, numéroPort) : udp_bind(donnéesChaîne->contrôleDatagramme, &AdresseInternet, numéroPort); return entréeÉlémentAuxiliaire ? numéroErreur(entréeÉlémentAuxiliaire) : 0;
}
void adressePriseRéseauRéutiliser(int poignéeFichier) { extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (donnéesChaîne && donnéesChaîne->contrôleConnexion) ip_set_option(donnéesChaîne->contrôleConnexion, SOF_REUSEADDR); }
int écouterRéseauCourt(int poignéeFichier) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne || donnéesChaîne->catégorieType != 1) return -9;
    if (donnéesChaîne->recevoirPort) return 0;
    err_t entréeÉlémentAuxiliaire; struct tcp_pcb *blocContrôleTransmission = tcp_listen_with_backlog_and_err(donnéesChaîne->contrôleConnexion, 4, &entréeÉlémentAuxiliaire);
    if (!blocContrôleTransmission) return numéroErreur(entréeÉlémentAuxiliaire); donnéesChaîne->contrôleConnexion = blocContrôleTransmission; donnéesChaîne->recevoirPort = 1; tcp_arg(blocContrôleTransmission, donnéesChaîne); tcp_accept(blocContrôleTransmission, accepté); return 0;
}
int connecterRéseauCourt(int poignéeFichier, uint32_t adresse, unsigned numéroPort) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne || donnéesChaîne->catégorieType != 1) return -9;
    if (donnéesChaîne->erreur) return donnéesChaîne->erreur;
    if (donnéesChaîne->connecté) return 0;
    if (donnéesChaîne->numéroExtrémitéPairRéseau) return -115;
    if (!numéroPort || numéroPort > 65535 || !adresse) return -22;
    ip_addr_t AdresseInternet; ip_addr_set_ip4_u32(&AdresseInternet, lwip_htonl(adresse));
    donnéesChaîne->adressePairRéseau = adresse; donnéesChaîne->numéroExtrémitéPairRéseau = numéroPort;
    err_t entréeÉlémentAuxiliaire = tcp_connect(donnéesChaîne->contrôleConnexion, &AdresseInternet, numéroPort, connecté); return entréeÉlémentAuxiliaire ? numéroErreur(entréeÉlémentAuxiliaire) : -115;
}
int accepterRéseauCourt(int poignéeFichier) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne || !donnéesChaîne->recevoirPort) return -22;
    for (int indiceOrdinal = 0; indiceOrdinal < 32; indiceOrdinal++) if (extrémitésPriseRéseau[indiceOrdinal].catégorieType == 1 && extrémitésPriseRéseau[indiceOrdinal].estEnAttente == poignéeFichier) { extrémitésPriseRéseau[indiceOrdinal].estEnAttente = -1; return indiceOrdinal; }
    return -11;
}
int lireRéseauCourt(int poignéeFichier, void *Données, unsigned nombreÉlémentsÉlémentListe) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne || donnéesChaîne->catégorieType != 1) return -9;
    if (!nombreÉlémentsÉlémentListe) return 0; if (!donnéesChaîne->nombreÉlémentsEntréeÉlément) return donnéesChaîne->erreur ? donnéesChaîne->erreur : donnéesChaîne->finFichier ? 0 : -11;
    if (nombreÉlémentsÉlémentListe > donnéesChaîne->nombreÉlémentsEntréeÉlément) nombreÉlémentsÉlémentListe = donnéesChaîne->nombreÉlémentsEntréeÉlément;
    for (unsigned indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsÉlémentListe; indiceOrdinal++) { ((unsigned char *)Données)[indiceOrdinal] = donnéesChaîne->Données[donnéesChaîne->entréeÉlémentAvantCôté]; donnéesChaîne->entréeÉlémentAvantCôté = (donnéesChaîne->entréeÉlémentAvantCôté + 1) % sizeof(donnéesChaîne->Données); }
    donnéesChaîne->nombreÉlémentsEntréeÉlément -= nombreÉlémentsÉlémentListe; if (donnéesChaîne->contrôleConnexion) tcp_recved(donnéesChaîne->contrôleConnexion, nombreÉlémentsÉlémentListe); return nombreÉlémentsÉlémentListe;
}
int écrireRéseauCourt(int poignéeFichier, const void *Données, unsigned nombreÉlémentsÉlémentListe) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne || donnéesChaîne->catégorieType != 1) return -9;
    if (donnéesChaîne->erreur) return donnéesChaîne->erreur; if (!donnéesChaîne->contrôleConnexion || !donnéesChaîne->connecté) return -107;
    if (!nombreÉlémentsÉlémentListe) return 0; if (nombreÉlémentsÉlémentListe > tcp_sndbuf(donnéesChaîne->contrôleConnexion)) nombreÉlémentsÉlémentListe = tcp_sndbuf(donnéesChaîne->contrôleConnexion);
    if (!nombreÉlémentsÉlémentListe) return -11; if (nombreÉlémentsÉlémentListe > 1024) nombreÉlémentsÉlémentListe = 1024;
    err_t entréeÉlémentAuxiliaire = tcp_write(donnéesChaîne->contrôleConnexion, Données, nombreÉlémentsÉlémentListe, TCP_WRITE_FLAG_COPY); if (entréeÉlémentAuxiliaire) return numéroErreur(entréeÉlémentAuxiliaire);
    tcp_output(donnéesChaîne->contrôleConnexion); return nombreÉlémentsÉlémentListe;
}
int envoyerDatagramme(int poignéeFichier, const void *Données, unsigned nombreÉlémentsÉlémentListe, uint32_t adresse, unsigned numéroPort) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne || donnéesChaîne->catégorieType != 2) return -9;
    if (nombreÉlémentsÉlémentListe > 512) return -90; if (!numéroPort || numéroPort > 65535) return -22;
    struct pbuf *positionDonnées = pbuf_alloc(PBUF_TRANSPORT, nombreÉlémentsÉlémentListe, PBUF_RAM); if (!positionDonnées) return -11;
    pbuf_take(positionDonnées, Données, nombreÉlémentsÉlémentListe); ip_addr_t AdresseInternet; ip_addr_set_ip4_u32(&AdresseInternet, lwip_htonl(adresse));
    err_t entréeÉlémentAuxiliaire = udp_sendto(donnéesChaîne->contrôleDatagramme, positionDonnées, &AdresseInternet, numéroPort); pbuf_free(positionDonnées); return entréeÉlémentAuxiliaire ? numéroErreur(entréeÉlémentAuxiliaire) : (int)nombreÉlémentsÉlémentListe;
}
int recevoirDatagramme(int poignéeFichier, void *Données, unsigned nombreÉlémentsÉlémentListe) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne || donnéesChaîne->catégorieType != 2) return -9;
    if (!donnéesChaîne->nombreÉlémentsEntréeÉlément) return -11; unsigned positionActuel = donnéesChaîne->entréeÉlémentAvantCôté;
    if (nombreÉlémentsÉlémentListe > donnéesChaîne->longueurs[positionActuel]) nombreÉlémentsÉlémentListe = donnéesChaîne->longueurs[positionActuel]; memcpy(Données, donnéesChaîne->Données + positionActuel * 512, nombreÉlémentsÉlémentListe);
    donnéesChaîne->numéroExtrémitéPairRéseau = donnéesChaîne->ports[positionActuel]; donnéesChaîne->adressePairRéseau = donnéesChaîne->adresses[positionActuel]; donnéesChaîne->entréeÉlémentAvantCôté = (positionActuel + 1) % 4; donnéesChaîne->nombreÉlémentsEntréeÉlément--; return nombreÉlémentsÉlémentListe;
}
unsigned numéroPortRéseau(int poignéeFichier) { extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); return !donnéesChaîne ? 0 : donnéesChaîne->contrôleConnexion ? donnéesChaîne->contrôleConnexion->local_port : donnéesChaîne->contrôleDatagramme ? donnéesChaîne->contrôleDatagramme->local_port : 0; }
unsigned numéroPortPairRéseau(int poignéeFichier) { extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); return donnéesChaîne ? donnéesChaîne->numéroExtrémitéPairRéseau : 0; }
uint32_t adressePairRéseauRéseauCourt(int poignéeFichier) { extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); return donnéesChaîne ? donnéesChaîne->adressePairRéseau : 0; }
void fermerRéseau(int poignéeFichier) {
    extrémitéPriseRéseau *donnéesChaîne = obtenirValeur(poignéeFichier); if (!donnéesChaîne) return;
    if (donnéesChaîne->recevoirPort) for (int indiceOrdinal = 0; indiceOrdinal < 32; ++indiceOrdinal) if (extrémitésPriseRéseau[indiceOrdinal].catégorieType && extrémitésPriseRéseau[indiceOrdinal].estEnAttente == poignéeFichier) fermerRéseau(indiceOrdinal);
    if (donnéesChaîne->contrôleConnexion) {
        tcp_arg(donnéesChaîne->contrôleConnexion, 0); if (donnéesChaîne->recevoirPort) tcp_accept(donnéesChaîne->contrôleConnexion, 0); else { tcp_recv(donnéesChaîne->contrôleConnexion, 0); tcp_err(donnéesChaîne->contrôleConnexion, 0); }
        if (tcp_close(donnéesChaîne->contrôleConnexion) != ERR_OK) tcp_abort(donnéesChaîne->contrôleConnexion);
    }
    if (donnéesChaîne->contrôleDatagramme) udp_remove(donnéesChaîne->contrôleDatagramme); donnéesChaîne->catégorieType = 0;
}
void inspecterRéseau(void) {
    if (!estPréparé || scrutation) return; scrutation = 1;
    if(réseauCâbléUtiliser)inspecterRéseauCâblé(&périphériqueConnexion);
    for (unsigned budget = 0; !réseauCâbléUtiliser && budget < 4096 && (registreMachine(périphériqueAuxiliaire + 0x54) & 1); budget++) {
        unsigned codeCaractère = registreMachine(périphériqueAuxiliaire + 0x40) & 255;
        if (codeCaractère == 192) {
            if (recevoirUtilisation && !recevoirErreur && !recevoirÉchapper) {
                struct pbuf *positionDonnées = pbuf_alloc(PBUF_RAW, recevoirUtilisation, PBUF_POOL);
                if (positionDonnées) { nombreÉlémentsDatagrammeReçu++; nombreÉlémentsOctetReçu += recevoirUtilisation; pbuf_take(positionDonnées, recevoirTamponDonnées, recevoirUtilisation); if (périphériqueConnexion.input(positionDonnées, &périphériqueConnexion) != ERR_OK) { nombreÉlémentsDatagrammeAbandonnésNombre++; pbuf_free(positionDonnées); } }
                else nombreÉlémentsDatagrammeAbandonnésNombre++;
            }
            else if (recevoirUtilisation) nombreÉlémentsDatagrammeAbandonnésNombre++;
            recevoirUtilisation = recevoirErreur = recevoirÉchapper = 0;
        } else if (codeCaractère == 219 && !recevoirÉchapper) recevoirÉchapper = 1;
        else {
            if (recevoirÉchapper) { if (codeCaractère != 220 && codeCaractère != 221) recevoirErreur = 1; codeCaractère = codeCaractère == 220 ? 192 : 219; recevoirÉchapper = 0; }
            if (recevoirUtilisation < sizeof(recevoirTamponDonnées)) recevoirTamponDonnées[recevoirUtilisation++] = codeCaractère; else recevoirErreur = 1;
        }
    }
    netif_poll(&périphériqueConnexion); sys_check_timeouts(); inspecterTransfertFichier(); inspecterDistant();
    for (unsigned budget = 0; budget < 4096 && nombreÉlémentsCôtéÉmission && (registreMachine(périphériqueAuxiliaire + 0x54) & 0x20); budget++) {
        registreMachine(périphériqueAuxiliaire + 0x40) = donnéesTransmettre[têteCôtéÉmission]; têteCôtéÉmission = (têteCôtéÉmission + 1) % sizeof(donnéesTransmettre); nombreÉlémentsCôtéÉmission--;
    }
    scrutation = 0;
}

/* réglages·조회는 lwIP의 donnéesEffectif 인터페이스와 pointFin 표를 사용한다. */
uint32_t lireÉtatRéseau(unsigned valeurEntréeÉlément, unsigned numéro) {
    if(valeurEntréeÉlément==20)return réseauCâbléUtiliser;
    if(valeurEntréeÉlément==21)return estPréparé&&netif_is_link_up(&périphériqueConnexion);
    if(valeurEntréeÉlément==22)return réseauCâbléUtiliser?statistiquesRéseauCâblé(5):0;
    if (!estPréparé) return 0;
    if(réseauCâbléUtiliser&&valeurEntréeÉlément>=4&&valeurEntréeÉlément<=8)return statistiquesRéseauCâblé(valeurEntréeÉlément-4);
    if (valeurEntréeÉlément == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&périphériqueConnexion)));
    if (valeurEntréeÉlément == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&périphériqueConnexion)));
    if (valeurEntréeÉlément == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&périphériqueConnexion)));
    if (valeurEntréeÉlément == 3) return netif_is_up(&périphériqueConnexion) != 0;
    if (valeurEntréeÉlément == 4) return nombreÉlémentsDatagrammeReçu;
    if (valeurEntréeÉlément == 5) return nombreÉlémentsDatagrammeEnvoyé;
    if (valeurEntréeÉlément == 6) return nombreÉlémentsOctetReçu;
    if (valeurEntréeÉlément == 7) return nombreÉlémentsOctetEnvoyé;
    if (valeurEntréeÉlément == 8) return nombreÉlémentsDatagrammeAbandonnésNombre;
    if (valeurEntréeÉlément == 9) return nombreÉlémentsCôtéÉmission;
    if (numéro >= 32) return 0;
    extrémitéPriseRéseau *pointFin = &extrémitésPriseRéseau[numéro];
    if (valeurEntréeÉlément == 10) return pointFin->catégorieType;
    if (!pointFin->catégorieType) return 0;
    if (valeurEntréeÉlément == 11) return numéroPortRéseau(numéro);
    if (valeurEntréeÉlément == 12) return pointFin->adressePairRéseau;
    if (valeurEntréeÉlément == 13) return pointFin->numéroExtrémitéPairRéseau;
    if (valeurEntréeÉlément == 14) return pointFin->recevoirPort ? 1 : pointFin->finFichier ? 3 : pointFin->erreur ? 4 : pointFin->connecté ? 2 : 0;
    if (valeurEntréeÉlément == 15) return pointFin->nombreÉlémentsEntréeÉlément;
    if (valeurEntréeÉlément == 16) {
        const ip_addr_t *adresse = pointFin->catégorieType == 1 && pointFin->contrôleConnexion ? &pointFin->contrôleConnexion->local_ip :
            pointFin->catégorieType == 2 && pointFin->contrôleDatagramme ? &pointFin->contrôleDatagramme->local_ip : 0;
        return adresse ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresse))) : 0;
    }
    return 0;
}

int configurerRéseau(unsigned action, uint32_t adresse, uint32_t valeurMasque, uint32_t valeurPasserelle) {
    if (!estPréparé) return -100;
    if (action == 1) { netif_set_up(&périphériqueConnexion); return 0; }
    if (action == 2) { netif_set_down(&périphériqueConnexion); return 0; }
    if (action != 0) return -22;
    /* 유니캐스트 IPv4, casListeCommuterDense valeurMasque, 같은 망의 선택적 valeurDéfaut valeurPasserelle. */
    uint32_t masqueInversé = ~valeurMasque;
    if (!valeurMasque || (masqueInversé & (masqueInversé + 1)) || !adresse || (adresse >> 24) == 127 ||
        (adresse >> 24) == 0 || (adresse >> 28) >= 14 ||
        (masqueInversé > 1 && (!(adresse & masqueInversé) || (adresse & masqueInversé) == masqueInversé)) ||
        (valeurPasserelle && ((valeurPasserelle & valeurMasque) != (adresse & valeurMasque) || valeurPasserelle == adresse || (valeurPasserelle >> 28) >= 14 ||
         (masqueInversé > 1 && (!(valeurPasserelle & masqueInversé) || (valeurPasserelle & masqueInversé) == masqueInversé))))) return -22;
    /* 기존 연결을 adresse 변경으로 몰래 끊지 않는다. */
    for (unsigned numéro = 0; numéro < 32; numéro++) if (extrémitésPriseRéseau[numéro].catégorieType &&
        !(extrémitésPriseRéseau[numéro].recevoirPort && extrémitésPriseRéseau[numéro].contrôleConnexion && ip_addr_isany(&extrémitésPriseRéseau[numéro].contrôleConnexion->local_ip))) return -16;
    if(réseauCâbléUtiliser)dhcp_stop(&périphériqueConnexion);
    ip4_addr_t adresseNouveau, masqueNouveau, valeurPasserelleNouveau;
    ip4_addr_set_u32(&adresseNouveau, lwip_htonl(adresse)); ip4_addr_set_u32(&masqueNouveau, lwip_htonl(valeurMasque)); ip4_addr_set_u32(&valeurPasserelleNouveau, lwip_htonl(valeurPasserelle));
    netif_set_addr(&périphériqueConnexion, &adresseNouveau, &masqueNouveau, &valeurPasserelleNouveau);
    return 0;
}

static struct raw_pcb *extrémitéRéponseRetour;
static uint32_t testAdresse, testTemps, tempsRéponseRetour;
static unsigned testSéquence, testIdentificateur, séquenceRéponseRetour;
static int étatValeurRéponseRetour;
static u8_t possèdeRéponseRetour(void *arguments, struct raw_pcb *pointFin, struct pbuf *Données, const ip_addr_t *adresse) {
    (void)arguments; (void)pointFin;
    unsigned char valeurTête[20], réponse[16];
    if (étatValeurRéponseRetour != -11 || Données->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresse))) != testAdresse || pbuf_copy_partial(Données, valeurTête, 20, 0) != 20) return 0;
    unsigned tailleEntête = (valeurTête[0] & 15) * 4;
    if ((valeurTête[0] >> 4) != 4 || tailleEntête < 20 || Données->tot_len < tailleEntête + 16 ||
        pbuf_copy_partial(Données, réponse, 16, tailleEntête) != 16 || réponse[0] || réponse[1] ||
        (((unsigned)réponse[4] << 8) | réponse[5]) != testIdentificateur ||
        (((unsigned)réponse[6] << 8) | réponse[7]) != testSéquence ||
        réponse[8] != 'J' || réponse[9] != 'K' || réponse[10] != 'O' || réponse[11] != 'S' ||
        (((uint32_t)réponse[12] << 24) | ((uint32_t)réponse[13] << 16) | ((uint32_t)réponse[14] << 8) | réponse[15]) != testTemps) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(Données, tailleEntête)) return 0;
    if (inet_chksum_pbuf(Données)) { pbuf_add_header(Données, tailleEntête); return 0; }
    tempsRéponseRetour = (uint32_t)millisecondesÉcouléesCarteMatérielle() - testTemps; séquenceRéponseRetour = valeurTête[8]; étatValeurRéponseRetour = 0;
    pbuf_free(Données); return 1;
}
int démarrerTestRéponseRetour(uint32_t adresse, unsigned valeurOrdre) {
    if (!estPréparé || !netif_is_up(&périphériqueConnexion)) return -100;
    if (!adresse || (adresse >> 28) >= 14 || adresse == 0xffffffffu) return -22;
    if (!extrémitéRéponseRetour) { extrémitéRéponseRetour = raw_new(IP_PROTO_ICMP); if (!extrémitéRéponseRetour) return -12; raw_recv(extrémitéRéponseRetour, possèdeRéponseRetour, 0); }
    testAdresse = adresse; testSéquence = valeurOrdre & 65535; testIdentificateur = (testIdentificateur + 1) & 65535;
    testTemps = millisecondesÉcouléesCarteMatérielle(); étatValeurRéponseRetour = -11; tempsRéponseRetour = séquenceRéponseRetour = 0;
    unsigned char Données[32] = {8,0,0,0};
    Données[4] = testIdentificateur >> 8; Données[5] = testIdentificateur; Données[6] = testSéquence >> 8; Données[7] = testSéquence;
    Données[8]='J'; Données[9]='K'; Données[10]='O'; Données[11]='S';
    Données[12]=testTemps >> 24; Données[13]=testTemps >> 16; Données[14]=testTemps >> 8; Données[15]=testTemps;
    for (unsigned indicePosition = 16; indicePosition < sizeof(Données); indicePosition++) Données[indicePosition] = indicePosition;
    uint16_t sommeContrôleVérification = inet_chksum(Données, sizeof(Données)); memcpy(Données + 2, &sommeContrôleVérification, 2);
    struct pbuf *datagramme = pbuf_alloc(PBUF_IP, sizeof(Données), PBUF_RAM); if (!datagramme) return -12;
    pbuf_take(datagramme, Données, sizeof(Données)); ip_addr_t extrémitéDestination; ip_addr_set_ip4_u32(&extrémitéDestination, lwip_htonl(adresse));
    err_t valeurTraité = raw_sendto(extrémitéRéponseRetour, datagramme, &extrémitéDestination); pbuf_free(datagramme);
    if (valeurTraité) étatValeurRéponseRetour = numéroErreur(valeurTraité);
    return valeurTraité ? étatValeurRéponseRetour : 0;
}
int lireTestRéponseRetour(unsigned valeurEntréeÉlément) {
    inspecterRéseau();
    return valeurEntréeÉlément == 0 ? étatValeurRéponseRetour : valeurEntréeÉlément == 1 ? (int)tempsRéponseRetour : valeurEntréeÉlément == 2 ? (int)séquenceRéponseRetour : -22;
}
