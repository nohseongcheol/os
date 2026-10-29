#include "../benennung/maschineBindenNamen.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Netzwerkstapel.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../entferntWert/entferntWert.h"
#include "verdrahtetNetzwerk.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define maschineRegister(ersterWert) (*(volatile uint32_t *)(uintptr_t)(ersterWert))
#define hilfsGerät 0xfe215000ul
extern uintptr_t platineVergangeneMillisekunden(void);
static struct netif verbindungGerät;
static int istVorbereitet, abfragezyklus;
static int benutzenVerdrahtetNetzwerk;
static unsigned nutzungEmpfangen, maskierenEmpfangen, fehlerEmpfangen;
static unsigned char datenPufferEmpfangen[1600];
static unsigned char übertragenDaten[32768];
static unsigned sendeseiteKopf, sendeseiteAnzahl;
static uint32_t empfangenWertDatagrammAnzahl, gesendetDatagrammAnzahl, empfangenWertByteAnzahl, gesendetByteAnzahl, verworfenAnzahlDatagrammAnzahl;
typedef struct {
    int typKategorie, portEmpfangen, istAusstehend, verbunden, dateiEnde, fehler;
    struct tcp_pcb *verbindungSteuerung;
    struct udp_pcb *datagrammSteuerung;
    unsigned vorderseiteEintrag, eintragAnzahl;
    unsigned char Daten[4096];
    unsigned längen[4], ports[4], gegenstelleEndpunktNummer;
    uint32_t adressen[4], gegenstelleAdresse;
} netzbuchseEndpunkt;
static netzbuchseEndpunkt netzbuchseEndpunkte[32];
u32_t sys_now(void) { return (u32_t)platineVergangeneMillisekunden(); }
static int fehlerNummer(err_t hilfsEintrag) {
    return hilfsEintrag == ERR_MEM || hilfsEintrag == ERR_BUF || hilfsEintrag == ERR_WOULDBLOCK ? -11 : hilfsEintrag == ERR_USE ? -98 :
        hilfsEintrag == ERR_RTE ? -101 : hilfsEintrag == ERR_RST ? -104 : hilfsEintrag == ERR_CONN ? -107 : hilfsEintrag == ERR_TIMEOUT ? -110 : -5;
}
static netzbuchseEndpunkt *wertHolen(int dateiKennwert) { return dateiKennwert >= 0 && dateiKennwert < 32 && netzbuchseEndpunkte[dateiKennwert].typKategorie ? &netzbuchseEndpunkte[dateiKennwert] : 0; }
static int reservieren(int typKategorie) {
    for (int ordnungszahlIndex = 0; ordnungszahlIndex < 32; ++ordnungszahlIndex) if (!netzbuchseEndpunkte[ordnungszahlIndex].typKategorie) {
        memset(&netzbuchseEndpunkte[ordnungszahlIndex], 0, sizeof(netzbuchseEndpunkt)); netzbuchseEndpunkte[ordnungszahlIndex].typKategorie = typKategorie; netzbuchseEndpunkte[ordnungszahlIndex].istAusstehend = -1; return ordnungszahlIndex;
    }
    return -24;
}
static void wertAusgeben(unsigned zeichenKode) { übertragenDaten[(sendeseiteKopf + sendeseiteAnzahl++) % sizeof(übertragenDaten)] = zeichenKode; }
static err_t ausgabe(struct netif *elementeintragAnzahl, struct pbuf *datenPosition, const ip4_addr_t *adresse) {
    (void)elementeintragAnzahl; (void)adresse;
    if (datenPosition->tot_len > 1500 || sendeseiteAnzahl + 2 * datenPosition->tot_len + 2 > sizeof(übertragenDaten)) return ERR_MEM;
    wertAusgeben(192);
    for (struct pbuf *nächsterVersatzwert = datenPosition; nächsterVersatzwert; nächsterVersatzwert = nächsterVersatzwert->next) for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < nächsterVersatzwert->len; ordnungszahlIndex++) {
        unsigned zeichenKode = ((unsigned char *)nächsterVersatzwert->payload)[ordnungszahlIndex];
        if (zeichenKode == 192 || zeichenKode == 219) { wertAusgeben(219); wertAusgeben(zeichenKode == 192 ? 220 : 221); } else wertAusgeben(zeichenKode);
    }
    wertAusgeben(192); gesendetDatagrammAnzahl++; gesendetByteAnzahl += datenPosition->tot_len; return ERR_OK;
}
static err_t laufzeitVorbereiten(struct netif *elementeintragAnzahl) { elementeintragAnzahl->name[0] = 's'; elementeintragAnzahl->name[1] = 'l'; elementeintragAnzahl->mtu = 1500; elementeintragAnzahl->output = ausgabe; return ERR_OK; }
void netzwerkVorbereiten(void) {
    if (istVorbereitet) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    maschineRegister(hilfsGerät + 4) |= 1; maschineRegister(hilfsGerät + 0x60) = 0; maschineRegister(hilfsGerät + 0x44) = 0;
    maschineRegister(hilfsGerät + 0x48) = 0xc6; maschineRegister(hilfsGerät + 0x4c) = 3; maschineRegister(hilfsGerät + 0x68) = 270; maschineRegister(hilfsGerät + 0x60) = 3;
    lwip_init();
    ip4_addr_t InternetAdresse, bitMaske, netzübergangAdresse;
    benutzenVerdrahtetNetzwerk=hatVerdrahtetGerät();
    ip4_addr_set_u32(&InternetAdresse, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitMaske, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&netzübergangAdresse, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&verbindungGerät, &InternetAdresse, &bitMaske, &netzübergangAdresse, 0, benutzenVerdrahtetNetzwerk?verdrahtetNetzwerkVorbereiten:laufzeitVorbereiten, benutzenVerdrahtetNetzwerk?ethernet_input:ip4_input))return;
    netif_set_default(&verbindungGerät); netif_set_up(&verbindungGerät);if(!benutzenVerdrahtetNetzwerk)netif_set_link_up(&verbindungGerät); istVorbereitet = 1;
    entferntVorbereiten();
}
static err_t hatEmpfangenWert(void *zusätzlichArgumente, struct tcp_pcb *datenübermittlungSteuerungBlock, struct pbuf *datenPosition, err_t fehler) {
    netzbuchseEndpunkt *zeichenketteDaten = zusätzlichArgumente; (void)datenübermittlungSteuerungBlock; (void)fehler;
    if (!datenPosition) { zeichenketteDaten->dateiEnde = 1; return ERR_OK; }
    if (datenPosition->tot_len > sizeof(zeichenketteDaten->Daten) - zeichenketteDaten->eintragAnzahl) return ERR_MEM;
    unsigned aktuellPosition = (zeichenketteDaten->vorderseiteEintrag + zeichenketteDaten->eintragAnzahl) % sizeof(zeichenketteDaten->Daten);
    for (struct pbuf *nächsterVersatzwert = datenPosition; nächsterVersatzwert; nächsterVersatzwert = nächsterVersatzwert->next) for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < nächsterVersatzwert->len; ordnungszahlIndex++) {
        zeichenketteDaten->Daten[aktuellPosition] = ((unsigned char *)nächsterVersatzwert->payload)[ordnungszahlIndex]; aktuellPosition = (aktuellPosition + 1) % sizeof(zeichenketteDaten->Daten);
    }
    zeichenketteDaten->eintragAnzahl += datenPosition->tot_len; pbuf_free(datenPosition); return ERR_OK;
}
static void hatFehlgeschlagen(void *zusätzlichArgumente, err_t fehler) { netzbuchseEndpunkt *zeichenketteDaten = zusätzlichArgumente; zeichenketteDaten->verbindungSteuerung = 0; zeichenketteDaten->fehler = fehlerNummer(fehler); }
static void rückrufe(netzbuchseEndpunkt *zeichenketteDaten) { tcp_arg(zeichenketteDaten->verbindungSteuerung, zeichenketteDaten); tcp_recv(zeichenketteDaten->verbindungSteuerung, hatEmpfangenWert); tcp_err(zeichenketteDaten->verbindungSteuerung, hatFehlgeschlagen); }
static err_t verbunden(void *zusätzlichArgumente, struct tcp_pcb *datenübermittlungSteuerungBlock, err_t fehler) {
    netzbuchseEndpunkt *zeichenketteDaten = zusätzlichArgumente; (void)datenübermittlungSteuerungBlock; if (fehler) zeichenketteDaten->fehler = fehlerNummer(fehler); else zeichenketteDaten->verbunden = 1; return ERR_OK;
}
static err_t angenommen(void *zusätzlichArgumente, struct tcp_pcb *datenübermittlungSteuerungBlock, err_t fehler) {
    netzbuchseEndpunkt *elternknoten = zusätzlichArgumente; if (fehler) return fehler;
    int dateiKennwert = reservieren(1); if (dateiKennwert < 0) return ERR_MEM;
    netzbuchseEndpunkt *zeichenketteDaten = &netzbuchseEndpunkte[dateiKennwert]; zeichenketteDaten->verbindungSteuerung = datenübermittlungSteuerungBlock; zeichenketteDaten->verbunden = 1; zeichenketteDaten->istAusstehend = (int)(elternknoten - netzbuchseEndpunkte);
    zeichenketteDaten->gegenstelleAdresse = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&datenübermittlungSteuerungBlock->remote_ip))); zeichenketteDaten->gegenstelleEndpunktNummer = datenübermittlungSteuerungBlock->remote_port;
    rückrufe(zeichenketteDaten); return ERR_OK;
}
static void datagramm(void *zusätzlichArgumente, struct udp_pcb *datenübermittlungSteuerungBlock, struct pbuf *datenPosition, const ip_addr_t *adresse, u16_t portNummer) {
    netzbuchseEndpunkt *zeichenketteDaten = zusätzlichArgumente; (void)datenübermittlungSteuerungBlock;
    if (zeichenketteDaten->eintragAnzahl < 4 && datenPosition->tot_len <= 512) {
        unsigned positionIndex = (zeichenketteDaten->vorderseiteEintrag + zeichenketteDaten->eintragAnzahl) % 4;
        pbuf_copy_partial(datenPosition, zeichenketteDaten->Daten + positionIndex * 512, datenPosition->tot_len, 0);
        zeichenketteDaten->längen[positionIndex] = datenPosition->tot_len; zeichenketteDaten->ports[positionIndex] = portNummer;
        zeichenketteDaten->adressen[positionIndex] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresse))); zeichenketteDaten->eintragAnzahl++;
    }
    pbuf_free(datenPosition);
}
int netzbuchseEndpunktErstellen(int typKategorie) {
    if (!istVorbereitet) return -100;
    if (typKategorie != 1 && typKategorie != 2) return -93;
    int dateiKennwert = reservieren(typKategorie); if (dateiKennwert < 0) return dateiKennwert;
    netzbuchseEndpunkt *zeichenketteDaten = &netzbuchseEndpunkte[dateiKennwert];
    if (typKategorie == 1) { zeichenketteDaten->verbindungSteuerung = tcp_new(); if (zeichenketteDaten->verbindungSteuerung) rückrufe(zeichenketteDaten); }
    else { zeichenketteDaten->datagrammSteuerung = udp_new(); if (zeichenketteDaten->datagrammSteuerung) udp_recv(zeichenketteDaten->datagrammSteuerung, datagramm, zeichenketteDaten); }
    if (!zeichenketteDaten->verbindungSteuerung && !zeichenketteDaten->datagrammSteuerung) { zeichenketteDaten->typKategorie = 0; return -12; } return dateiKennwert;
}
int netzZuordnen(int dateiKennwert, uint32_t adresse, unsigned portNummer) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten) return -9;
    if (portNummer > 65535 || (adresse && adresse != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&verbindungGerät))) && adresse != 0x7f000001)) return -99;
    ip_addr_t InternetAdresse; ip_addr_set_ip4_u32(&InternetAdresse, lwip_htonl(adresse));
    err_t hilfsEintrag = zeichenketteDaten->typKategorie == 1 ? tcp_bind(zeichenketteDaten->verbindungSteuerung, &InternetAdresse, portNummer) : udp_bind(zeichenketteDaten->datagrammSteuerung, &InternetAdresse, portNummer); return hilfsEintrag ? fehlerNummer(hilfsEintrag) : 0;
}
void wiederverwendenNetzbuchseAdresse(int dateiKennwert) { netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (zeichenketteDaten && zeichenketteDaten->verbindungSteuerung) ip_set_option(zeichenketteDaten->verbindungSteuerung, SOF_REUSEADDR); }
int netzLauschen(int dateiKennwert) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten || zeichenketteDaten->typKategorie != 1) return -9;
    if (zeichenketteDaten->portEmpfangen) return 0;
    err_t hilfsEintrag; struct tcp_pcb *datenübermittlungSteuerungBlock = tcp_listen_with_backlog_and_err(zeichenketteDaten->verbindungSteuerung, 4, &hilfsEintrag);
    if (!datenübermittlungSteuerungBlock) return fehlerNummer(hilfsEintrag); zeichenketteDaten->verbindungSteuerung = datenübermittlungSteuerungBlock; zeichenketteDaten->portEmpfangen = 1; tcp_arg(datenübermittlungSteuerungBlock, zeichenketteDaten); tcp_accept(datenübermittlungSteuerungBlock, angenommen); return 0;
}
int netzVerbinden(int dateiKennwert, uint32_t adresse, unsigned portNummer) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten || zeichenketteDaten->typKategorie != 1) return -9;
    if (zeichenketteDaten->fehler) return zeichenketteDaten->fehler;
    if (zeichenketteDaten->verbunden) return 0;
    if (zeichenketteDaten->gegenstelleEndpunktNummer) return -115;
    if (!portNummer || portNummer > 65535 || !adresse) return -22;
    ip_addr_t InternetAdresse; ip_addr_set_ip4_u32(&InternetAdresse, lwip_htonl(adresse));
    zeichenketteDaten->gegenstelleAdresse = adresse; zeichenketteDaten->gegenstelleEndpunktNummer = portNummer;
    err_t hilfsEintrag = tcp_connect(zeichenketteDaten->verbindungSteuerung, &InternetAdresse, portNummer, verbunden); return hilfsEintrag ? fehlerNummer(hilfsEintrag) : -115;
}
int netzAnnehmen(int dateiKennwert) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten || !zeichenketteDaten->portEmpfangen) return -22;
    for (int ordnungszahlIndex = 0; ordnungszahlIndex < 32; ordnungszahlIndex++) if (netzbuchseEndpunkte[ordnungszahlIndex].typKategorie == 1 && netzbuchseEndpunkte[ordnungszahlIndex].istAusstehend == dateiKennwert) { netzbuchseEndpunkte[ordnungszahlIndex].istAusstehend = -1; return ordnungszahlIndex; }
    return -11;
}
int netzLesen(int dateiKennwert, void *Daten, unsigned elementeintragAnzahl) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten || zeichenketteDaten->typKategorie != 1) return -9;
    if (!elementeintragAnzahl) return 0; if (!zeichenketteDaten->eintragAnzahl) return zeichenketteDaten->fehler ? zeichenketteDaten->fehler : zeichenketteDaten->dateiEnde ? 0 : -11;
    if (elementeintragAnzahl > zeichenketteDaten->eintragAnzahl) elementeintragAnzahl = zeichenketteDaten->eintragAnzahl;
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < elementeintragAnzahl; ordnungszahlIndex++) { ((unsigned char *)Daten)[ordnungszahlIndex] = zeichenketteDaten->Daten[zeichenketteDaten->vorderseiteEintrag]; zeichenketteDaten->vorderseiteEintrag = (zeichenketteDaten->vorderseiteEintrag + 1) % sizeof(zeichenketteDaten->Daten); }
    zeichenketteDaten->eintragAnzahl -= elementeintragAnzahl; if (zeichenketteDaten->verbindungSteuerung) tcp_recved(zeichenketteDaten->verbindungSteuerung, elementeintragAnzahl); return elementeintragAnzahl;
}
int netzSchreiben(int dateiKennwert, const void *Daten, unsigned elementeintragAnzahl) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten || zeichenketteDaten->typKategorie != 1) return -9;
    if (zeichenketteDaten->fehler) return zeichenketteDaten->fehler; if (!zeichenketteDaten->verbindungSteuerung || !zeichenketteDaten->verbunden) return -107;
    if (!elementeintragAnzahl) return 0; if (elementeintragAnzahl > tcp_sndbuf(zeichenketteDaten->verbindungSteuerung)) elementeintragAnzahl = tcp_sndbuf(zeichenketteDaten->verbindungSteuerung);
    if (!elementeintragAnzahl) return -11; if (elementeintragAnzahl > 1024) elementeintragAnzahl = 1024;
    err_t hilfsEintrag = tcp_write(zeichenketteDaten->verbindungSteuerung, Daten, elementeintragAnzahl, TCP_WRITE_FLAG_COPY); if (hilfsEintrag) return fehlerNummer(hilfsEintrag);
    tcp_output(zeichenketteDaten->verbindungSteuerung); return elementeintragAnzahl;
}
int datagrammSenden(int dateiKennwert, const void *Daten, unsigned elementeintragAnzahl, uint32_t adresse, unsigned portNummer) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten || zeichenketteDaten->typKategorie != 2) return -9;
    if (elementeintragAnzahl > 512) return -90; if (!portNummer || portNummer > 65535) return -22;
    struct pbuf *datenPosition = pbuf_alloc(PBUF_TRANSPORT, elementeintragAnzahl, PBUF_RAM); if (!datenPosition) return -11;
    pbuf_take(datenPosition, Daten, elementeintragAnzahl); ip_addr_t InternetAdresse; ip_addr_set_ip4_u32(&InternetAdresse, lwip_htonl(adresse));
    err_t hilfsEintrag = udp_sendto(zeichenketteDaten->datagrammSteuerung, datenPosition, &InternetAdresse, portNummer); pbuf_free(datenPosition); return hilfsEintrag ? fehlerNummer(hilfsEintrag) : (int)elementeintragAnzahl;
}
int datagrammEmpfangen(int dateiKennwert, void *Daten, unsigned elementeintragAnzahl) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten || zeichenketteDaten->typKategorie != 2) return -9;
    if (!zeichenketteDaten->eintragAnzahl) return -11; unsigned aktuellPosition = zeichenketteDaten->vorderseiteEintrag;
    if (elementeintragAnzahl > zeichenketteDaten->längen[aktuellPosition]) elementeintragAnzahl = zeichenketteDaten->längen[aktuellPosition]; memcpy(Daten, zeichenketteDaten->Daten + aktuellPosition * 512, elementeintragAnzahl);
    zeichenketteDaten->gegenstelleEndpunktNummer = zeichenketteDaten->ports[aktuellPosition]; zeichenketteDaten->gegenstelleAdresse = zeichenketteDaten->adressen[aktuellPosition]; zeichenketteDaten->vorderseiteEintrag = (aktuellPosition + 1) % 4; zeichenketteDaten->eintragAnzahl--; return elementeintragAnzahl;
}
unsigned netzwerkPortNummer(int dateiKennwert) { netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); return !zeichenketteDaten ? 0 : zeichenketteDaten->verbindungSteuerung ? zeichenketteDaten->verbindungSteuerung->local_port : zeichenketteDaten->datagrammSteuerung ? zeichenketteDaten->datagrammSteuerung->local_port : 0; }
unsigned gegenstellePortNummer(int dateiKennwert) { netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); return zeichenketteDaten ? zeichenketteDaten->gegenstelleEndpunktNummer : 0; }
uint32_t netzGegenstelleAdresse(int dateiKennwert) { netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); return zeichenketteDaten ? zeichenketteDaten->gegenstelleAdresse : 0; }
void netzwerkSchließen(int dateiKennwert) {
    netzbuchseEndpunkt *zeichenketteDaten = wertHolen(dateiKennwert); if (!zeichenketteDaten) return;
    if (zeichenketteDaten->portEmpfangen) for (int ordnungszahlIndex = 0; ordnungszahlIndex < 32; ++ordnungszahlIndex) if (netzbuchseEndpunkte[ordnungszahlIndex].typKategorie && netzbuchseEndpunkte[ordnungszahlIndex].istAusstehend == dateiKennwert) netzwerkSchließen(ordnungszahlIndex);
    if (zeichenketteDaten->verbindungSteuerung) {
        tcp_arg(zeichenketteDaten->verbindungSteuerung, 0); if (zeichenketteDaten->portEmpfangen) tcp_accept(zeichenketteDaten->verbindungSteuerung, 0); else { tcp_recv(zeichenketteDaten->verbindungSteuerung, 0); tcp_err(zeichenketteDaten->verbindungSteuerung, 0); }
        if (tcp_close(zeichenketteDaten->verbindungSteuerung) != ERR_OK) tcp_abort(zeichenketteDaten->verbindungSteuerung);
    }
    if (zeichenketteDaten->datagrammSteuerung) udp_remove(zeichenketteDaten->datagrammSteuerung); zeichenketteDaten->typKategorie = 0;
}
void netzwerkUntersuchen(void) {
    if (!istVorbereitet || abfragezyklus) return; abfragezyklus = 1;
    if(benutzenVerdrahtetNetzwerk)verdrahtetNetzwerkUntersuchen(&verbindungGerät);
    for (unsigned vorrat = 0; !benutzenVerdrahtetNetzwerk && vorrat < 4096 && (maschineRegister(hilfsGerät + 0x54) & 1); vorrat++) {
        unsigned zeichenKode = maschineRegister(hilfsGerät + 0x40) & 255;
        if (zeichenKode == 192) {
            if (nutzungEmpfangen && !fehlerEmpfangen && !maskierenEmpfangen) {
                struct pbuf *datenPosition = pbuf_alloc(PBUF_RAW, nutzungEmpfangen, PBUF_POOL);
                if (datenPosition) { empfangenWertDatagrammAnzahl++; empfangenWertByteAnzahl += nutzungEmpfangen; pbuf_take(datenPosition, datenPufferEmpfangen, nutzungEmpfangen); if (verbindungGerät.input(datenPosition, &verbindungGerät) != ERR_OK) { verworfenAnzahlDatagrammAnzahl++; pbuf_free(datenPosition); } }
                else verworfenAnzahlDatagrammAnzahl++;
            }
            else if (nutzungEmpfangen) verworfenAnzahlDatagrammAnzahl++;
            nutzungEmpfangen = fehlerEmpfangen = maskierenEmpfangen = 0;
        } else if (zeichenKode == 219 && !maskierenEmpfangen) maskierenEmpfangen = 1;
        else {
            if (maskierenEmpfangen) { if (zeichenKode != 220 && zeichenKode != 221) fehlerEmpfangen = 1; zeichenKode = zeichenKode == 220 ? 192 : 219; maskierenEmpfangen = 0; }
            if (nutzungEmpfangen < sizeof(datenPufferEmpfangen)) datenPufferEmpfangen[nutzungEmpfangen++] = zeichenKode; else fehlerEmpfangen = 1;
        }
    }
    netif_poll(&verbindungGerät); sys_check_timeouts(); dateiÜbertragungUntersuchen(); entferntUntersuchen();
    for (unsigned vorrat = 0; vorrat < 4096 && sendeseiteAnzahl && (maschineRegister(hilfsGerät + 0x54) & 0x20); vorrat++) {
        maschineRegister(hilfsGerät + 0x40) = übertragenDaten[sendeseiteKopf]; sendeseiteKopf = (sendeseiteKopf + 1) % sizeof(übertragenDaten); sendeseiteAnzahl--;
    }
    abfragezyklus = 0;
}

/* einstellungen·조회는 lwIP의 tatsächlichDaten 인터페이스와 endePunkt 표를 사용한다. */
uint32_t netzwerkZustandLesen(unsigned eintragWert, unsigned Nummer) {
    if(eintragWert==20)return benutzenVerdrahtetNetzwerk;
    if(eintragWert==21)return istVorbereitet&&netif_is_link_up(&verbindungGerät);
    if(eintragWert==22)return benutzenVerdrahtetNetzwerk?verdrahtetNetzwerkStatistik(5):0;
    if (!istVorbereitet) return 0;
    if(benutzenVerdrahtetNetzwerk&&eintragWert>=4&&eintragWert<=8)return verdrahtetNetzwerkStatistik(eintragWert-4);
    if (eintragWert == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&verbindungGerät)));
    if (eintragWert == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&verbindungGerät)));
    if (eintragWert == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&verbindungGerät)));
    if (eintragWert == 3) return netif_is_up(&verbindungGerät) != 0;
    if (eintragWert == 4) return empfangenWertDatagrammAnzahl;
    if (eintragWert == 5) return gesendetDatagrammAnzahl;
    if (eintragWert == 6) return empfangenWertByteAnzahl;
    if (eintragWert == 7) return gesendetByteAnzahl;
    if (eintragWert == 8) return verworfenAnzahlDatagrammAnzahl;
    if (eintragWert == 9) return sendeseiteAnzahl;
    if (Nummer >= 32) return 0;
    netzbuchseEndpunkt *endePunkt = &netzbuchseEndpunkte[Nummer];
    if (eintragWert == 10) return endePunkt->typKategorie;
    if (!endePunkt->typKategorie) return 0;
    if (eintragWert == 11) return netzwerkPortNummer(Nummer);
    if (eintragWert == 12) return endePunkt->gegenstelleAdresse;
    if (eintragWert == 13) return endePunkt->gegenstelleEndpunktNummer;
    if (eintragWert == 14) return endePunkt->portEmpfangen ? 1 : endePunkt->dateiEnde ? 3 : endePunkt->fehler ? 4 : endePunkt->verbunden ? 2 : 0;
    if (eintragWert == 15) return endePunkt->eintragAnzahl;
    if (eintragWert == 16) {
        const ip_addr_t *adresse = endePunkt->typKategorie == 1 && endePunkt->verbindungSteuerung ? &endePunkt->verbindungSteuerung->local_ip :
            endePunkt->typKategorie == 2 && endePunkt->datagrammSteuerung ? &endePunkt->datagrammSteuerung->local_ip : 0;
        return adresse ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresse))) : 0;
    }
    return 0;
}

int netzwerkKonfigurieren(unsigned aktion, uint32_t adresse, uint32_t maskeWert, uint32_t netzübergangWert) {
    if (!istVorbereitet) return -100;
    if (aktion == 1) { netif_set_up(&verbindungGerät); return 0; }
    if (aktion == 2) { netif_set_down(&verbindungGerät); return 0; }
    if (aktion != 0) return -22;
    /* 유니캐스트 IPv4, dichtUmschaltenFallliste maskeWert, 같은 망의 선택적 standardwertWert netzübergangWert. */
    uint32_t umgekehrtMaske = ~maskeWert;
    if (!maskeWert || (umgekehrtMaske & (umgekehrtMaske + 1)) || !adresse || (adresse >> 24) == 127 ||
        (adresse >> 24) == 0 || (adresse >> 28) >= 14 ||
        (umgekehrtMaske > 1 && (!(adresse & umgekehrtMaske) || (adresse & umgekehrtMaske) == umgekehrtMaske)) ||
        (netzübergangWert && ((netzübergangWert & maskeWert) != (adresse & maskeWert) || netzübergangWert == adresse || (netzübergangWert >> 28) >= 14 ||
         (umgekehrtMaske > 1 && (!(netzübergangWert & umgekehrtMaske) || (netzübergangWert & umgekehrtMaske) == umgekehrtMaske))))) return -22;
    /* 기존 연결을 adresse 변경으로 몰래 끊지 않는다. */
    for (unsigned Nummer = 0; Nummer < 32; Nummer++) if (netzbuchseEndpunkte[Nummer].typKategorie &&
        !(netzbuchseEndpunkte[Nummer].portEmpfangen && netzbuchseEndpunkte[Nummer].verbindungSteuerung && ip_addr_isany(&netzbuchseEndpunkte[Nummer].verbindungSteuerung->local_ip))) return -16;
    if(benutzenVerdrahtetNetzwerk)dhcp_stop(&verbindungGerät);
    ip4_addr_t neuAdresse, neuMaske, neuNetzübergangWert;
    ip4_addr_set_u32(&neuAdresse, lwip_htonl(adresse)); ip4_addr_set_u32(&neuMaske, lwip_htonl(maskeWert)); ip4_addr_set_u32(&neuNetzübergangWert, lwip_htonl(netzübergangWert));
    netif_set_addr(&verbindungGerät, &neuAdresse, &neuMaske, &neuNetzübergangWert);
    return 0;
}

static struct raw_pcb *rückmeldungEndpunkt;
static uint32_t adressePrüfung, zeitPrüfung, rückmeldungZeit;
static unsigned folgePrüfung, bezeichnerPrüfung, rückmeldungFolge;
static int rückmeldungStatuswert;
static u8_t hatRückmeldung(void *argumente, struct raw_pcb *endePunkt, struct pbuf *Daten, const ip_addr_t *adresse) {
    (void)argumente; (void)endePunkt;
    unsigned char kopfWert[20], antwort[16];
    if (rückmeldungStatuswert != -11 || Daten->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresse))) != adressePrüfung || pbuf_copy_partial(Daten, kopfWert, 20, 0) != 20) return 0;
    unsigned kopfGröße = (kopfWert[0] & 15) * 4;
    if ((kopfWert[0] >> 4) != 4 || kopfGröße < 20 || Daten->tot_len < kopfGröße + 16 ||
        pbuf_copy_partial(Daten, antwort, 16, kopfGröße) != 16 || antwort[0] || antwort[1] ||
        (((unsigned)antwort[4] << 8) | antwort[5]) != bezeichnerPrüfung ||
        (((unsigned)antwort[6] << 8) | antwort[7]) != folgePrüfung ||
        antwort[8] != 'J' || antwort[9] != 'K' || antwort[10] != 'O' || antwort[11] != 'S' ||
        (((uint32_t)antwort[12] << 24) | ((uint32_t)antwort[13] << 16) | ((uint32_t)antwort[14] << 8) | antwort[15]) != zeitPrüfung) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(Daten, kopfGröße)) return 0;
    if (inet_chksum_pbuf(Daten)) { pbuf_add_header(Daten, kopfGröße); return 0; }
    rückmeldungZeit = (uint32_t)platineVergangeneMillisekunden() - zeitPrüfung; rückmeldungFolge = kopfWert[8]; rückmeldungStatuswert = 0;
    pbuf_free(Daten); return 1;
}
int rückmeldungPrüfungStarten(uint32_t adresse, unsigned reihenfolgeWert) {
    if (!istVorbereitet || !netif_is_up(&verbindungGerät)) return -100;
    if (!adresse || (adresse >> 28) >= 14 || adresse == 0xffffffffu) return -22;
    if (!rückmeldungEndpunkt) { rückmeldungEndpunkt = raw_new(IP_PROTO_ICMP); if (!rückmeldungEndpunkt) return -12; raw_recv(rückmeldungEndpunkt, hatRückmeldung, 0); }
    adressePrüfung = adresse; folgePrüfung = reihenfolgeWert & 65535; bezeichnerPrüfung = (bezeichnerPrüfung + 1) & 65535;
    zeitPrüfung = platineVergangeneMillisekunden(); rückmeldungStatuswert = -11; rückmeldungZeit = rückmeldungFolge = 0;
    unsigned char Daten[32] = {8,0,0,0};
    Daten[4] = bezeichnerPrüfung >> 8; Daten[5] = bezeichnerPrüfung; Daten[6] = folgePrüfung >> 8; Daten[7] = folgePrüfung;
    Daten[8]='J'; Daten[9]='K'; Daten[10]='O'; Daten[11]='S';
    Daten[12]=zeitPrüfung >> 24; Daten[13]=zeitPrüfung >> 16; Daten[14]=zeitPrüfung >> 8; Daten[15]=zeitPrüfung;
    for (unsigned positionIndex = 16; positionIndex < sizeof(Daten); positionIndex++) Daten[positionIndex] = positionIndex;
    uint16_t überprüfungKontrollsumme = inet_chksum(Daten, sizeof(Daten)); memcpy(Daten + 2, &überprüfungKontrollsumme, 2);
    struct pbuf *datagramm = pbuf_alloc(PBUF_IP, sizeof(Daten), PBUF_RAM); if (!datagramm) return -12;
    pbuf_take(datagramm, Daten, sizeof(Daten)); ip_addr_t zielEndpunkt; ip_addr_set_ip4_u32(&zielEndpunkt, lwip_htonl(adresse));
    err_t verarbeitetWert = raw_sendto(rückmeldungEndpunkt, datagramm, &zielEndpunkt); pbuf_free(datagramm);
    if (verarbeitetWert) rückmeldungStatuswert = fehlerNummer(verarbeitetWert);
    return verarbeitetWert ? rückmeldungStatuswert : 0;
}
int rückmeldungPrüfungLesen(unsigned eintragWert) {
    netzwerkUntersuchen();
    return eintragWert == 0 ? rückmeldungStatuswert : eintragWert == 1 ? (int)rückmeldungZeit : eintragWert == 2 ? (int)rückmeldungFolge : -22;
}
