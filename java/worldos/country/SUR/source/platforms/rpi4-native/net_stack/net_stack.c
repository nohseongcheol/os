#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "net_stack.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../extern_WAARDE_28edcfa1/extern_WAARDE_28edcfa1.h"
#include "bekabeld_net.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define machine_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif verbinding_mobiel;
static int 준비됨, navragen;
static int gebruik_bekabeld_net;
static unsigned ontvangen_gebruik, 수신탈출, ontvangen_fout;
static unsigned char ontvangen_gegevensbuffer[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t OPBRENGST_datagram_AANTAL, 보낸전문수, OPBRENGST_byte_AANTAL, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_gebied, ontvangen_poort, informatie_In_behandeling, 연결됨, Bestand_beëindigen, fout;
    struct tcp_pcb *verbinding_controle;
    struct udp_pcb *datagram_controle;
    unsigned voorkant_invoer, invoer_AANTAL_8f7753a1;
    unsigned char gegevens[4096];
    unsigned 길이목록[4], 접속번호들[4], peer_eindpunt_nummer;
    uint32_t 주소목록[4], peer_ADRES;
} socket_eindpunt_3db661a2;
static socket_eindpunt_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int foutnummer(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static socket_eindpunt_3db661a2 *ophalen_WAARDE(int bestandsingang) { return bestandsingang >= 0 && bestandsingang < 32 && 통신끝점들[bestandsingang].TYPE_gebied ? &통신끝점들[bestandsingang] : 0; }
static int 예약하기(int TYPE_gebied) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_gebied) {
        memset(&통신끝점들[순번], 0, sizeof(socket_eindpunt_3db661a2)); 통신끝점들[순번].TYPE_gebied = TYPE_gebied; 통신끝점들[순번].informatie_In_behandeling = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned codepoint) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = codepoint; }
static err_t uitvoer(struct netif *item_AANTAL, struct pbuf *gegevens_functie, const ip4_addr_t *ADRES) {
    (void)item_AANTAL; (void)ADRES;
    if (gegevens_functie->tot_len > 1500 || 송신개수 + 2 * gegevens_functie->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Volgende_VERSCHUIVING = gegevens_functie; Volgende_VERSCHUIVING; Volgende_VERSCHUIVING = Volgende_VERSCHUIVING->next) for (unsigned 순번 = 0; 순번 < Volgende_VERSCHUIVING->len; 순번++) {
        unsigned codepoint = ((unsigned char *)Volgende_VERSCHUIVING->payload)[순번];
        if (codepoint == 192 || codepoint == 219) { 내보내기(219); 내보내기(codepoint == 192 ? 220 : 221); } else 내보내기(codepoint);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += gegevens_functie->tot_len; return ERR_OK;
}
static err_t Bereid_voor_CLR(struct netif *item_AANTAL) { item_AANTAL->name[0] = 's'; item_AANTAL->name[1] = 'l'; item_AANTAL->mtu = 1500; item_AANTAL->output = uitvoer; return ERR_OK; }
void Bereid_voor_net(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    machine_register(보조장치 + 4) |= 1; machine_register(보조장치 + 0x60) = 0; machine_register(보조장치 + 0x44) = 0;
    machine_register(보조장치 + 0x48) = 0xc6; machine_register(보조장치 + 0x4c) = 3; machine_register(보조장치 + 0x68) = 270; machine_register(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetadres, bitmasker, gatewayadres;
    gebruik_bekabeld_net=유선장치있음();
    ip4_addr_set_u32(&internetadres, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmasker, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gatewayadres, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&verbinding_mobiel, &internetadres, &bitmasker, &gatewayadres, 0, gebruik_bekabeld_net?Bereid_voor_bekabeld_net:Bereid_voor_CLR, gebruik_bekabeld_net?ethernet_input:ip4_input))return;
    netif_set_default(&verbinding_mobiel); netif_set_up(&verbinding_mobiel);if(!gebruik_bekabeld_net)netif_set_link_up(&verbinding_mobiel); 준비됨 = 1;
    Bereid_voor_extern();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *gegevens_functie, err_t fout) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = 부가인수; (void)통신제어블록; (void)fout;
    if (!gegevens_functie) { tekenreeks_gegevens->Bestand_beëindigen = 1; return ERR_OK; }
    if (gegevens_functie->tot_len > sizeof(tekenreeks_gegevens->gegevens) - tekenreeks_gegevens->invoer_AANTAL_8f7753a1) return ERR_MEM;
    unsigned actueel_functie = (tekenreeks_gegevens->voorkant_invoer + tekenreeks_gegevens->invoer_AANTAL_8f7753a1) % sizeof(tekenreeks_gegevens->gegevens);
    for (struct pbuf *Volgende_VERSCHUIVING = gegevens_functie; Volgende_VERSCHUIVING; Volgende_VERSCHUIVING = Volgende_VERSCHUIVING->next) for (unsigned 순번 = 0; 순번 < Volgende_VERSCHUIVING->len; 순번++) {
        tekenreeks_gegevens->gegevens[actueel_functie] = ((unsigned char *)Volgende_VERSCHUIVING->payload)[순번]; actueel_functie = (actueel_functie + 1) % sizeof(tekenreeks_gegevens->gegevens);
    }
    tekenreeks_gegevens->invoer_AANTAL_8f7753a1 += gegevens_functie->tot_len; pbuf_free(gegevens_functie); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t fout) { socket_eindpunt_3db661a2 *tekenreeks_gegevens = 부가인수; tekenreeks_gegevens->verbinding_controle = 0; tekenreeks_gegevens->fout = foutnummer(fout); }
static void 되부름목록(socket_eindpunt_3db661a2 *tekenreeks_gegevens) { tcp_arg(tekenreeks_gegevens->verbinding_controle, tekenreeks_gegevens); tcp_recv(tekenreeks_gegevens->verbinding_controle, 수신됨); tcp_err(tekenreeks_gegevens->verbinding_controle, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t fout) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = 부가인수; (void)통신제어블록; if (fout) tekenreeks_gegevens->fout = foutnummer(fout); else tekenreeks_gegevens->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t fout) {
    socket_eindpunt_3db661a2 *bovenliggend = 부가인수; if (fout) return fout;
    int bestandsingang = 예약하기(1); if (bestandsingang < 0) return ERR_MEM;
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = &통신끝점들[bestandsingang]; tekenreeks_gegevens->verbinding_controle = 통신제어블록; tekenreeks_gegevens->연결됨 = 1; tekenreeks_gegevens->informatie_In_behandeling = (int)(bovenliggend - 통신끝점들);
    tekenreeks_gegevens->peer_ADRES = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); tekenreeks_gegevens->peer_eindpunt_nummer = 통신제어블록->remote_port;
    되부름목록(tekenreeks_gegevens); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *gegevens_functie, const ip_addr_t *ADRES, u16_t poortnummer) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = 부가인수; (void)통신제어블록;
    if (tekenreeks_gegevens->invoer_AANTAL_8f7753a1 < 4 && gegevens_functie->tot_len <= 512) {
        unsigned plaatsingsindex = (tekenreeks_gegevens->voorkant_invoer + tekenreeks_gegevens->invoer_AANTAL_8f7753a1) % 4;
        pbuf_copy_partial(gegevens_functie, tekenreeks_gegevens->gegevens + plaatsingsindex * 512, gegevens_functie->tot_len, 0);
        tekenreeks_gegevens->길이목록[plaatsingsindex] = gegevens_functie->tot_len; tekenreeks_gegevens->접속번호들[plaatsingsindex] = poortnummer;
        tekenreeks_gegevens->주소목록[plaatsingsindex] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADRES))); tekenreeks_gegevens->invoer_AANTAL_8f7753a1++;
    }
    pbuf_free(gegevens_functie);
}
int maken_socket_eindpunt(int TYPE_gebied) {
    if (!준비됨) return -100;
    if (TYPE_gebied != 1 && TYPE_gebied != 2) return -93;
    int bestandsingang = 예약하기(TYPE_gebied); if (bestandsingang < 0) return bestandsingang;
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = &통신끝점들[bestandsingang];
    if (TYPE_gebied == 1) { tekenreeks_gegevens->verbinding_controle = tcp_new(); if (tekenreeks_gegevens->verbinding_controle) 되부름목록(tekenreeks_gegevens); }
    else { tekenreeks_gegevens->datagram_controle = udp_new(); if (tekenreeks_gegevens->datagram_controle) udp_recv(tekenreeks_gegevens->datagram_controle, datagram, tekenreeks_gegevens); }
    if (!tekenreeks_gegevens->verbinding_controle && !tekenreeks_gegevens->datagram_controle) { tekenreeks_gegevens->TYPE_gebied = 0; return -12; } return bestandsingang;
}
int NET_BIND(int bestandsingang, uint32_t ADRES, unsigned poortnummer) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens) return -9;
    if (poortnummer > 65535 || (ADRES && ADRES != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&verbinding_mobiel))) && ADRES != 0x7f000001)) return -99;
    ip_addr_t internetadres; ip_addr_set_ip4_u32(&internetadres, lwip_htonl(ADRES));
    err_t 보조항목 = tekenreeks_gegevens->TYPE_gebied == 1 ? tcp_bind(tekenreeks_gegevens->verbinding_controle, &internetadres, poortnummer) : udp_bind(tekenreeks_gegevens->datagram_controle, &internetadres, poortnummer); return 보조항목 ? foutnummer(보조항목) : 0;
}
void 통신주소재사용(int bestandsingang) { socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (tekenreeks_gegevens && tekenreeks_gegevens->verbinding_controle) ip_set_option(tekenreeks_gegevens->verbinding_controle, SOF_REUSEADDR); }
int 연결기다리기(int bestandsingang) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens || tekenreeks_gegevens->TYPE_gebied != 1) return -9;
    if (tekenreeks_gegevens->ontvangen_poort) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(tekenreeks_gegevens->verbinding_controle, 4, &보조항목);
    if (!통신제어블록) return foutnummer(보조항목); tekenreeks_gegevens->verbinding_controle = 통신제어블록; tekenreeks_gegevens->ontvangen_poort = 1; tcp_arg(통신제어블록, tekenreeks_gegevens); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_VERBINDEN(int bestandsingang, uint32_t ADRES, unsigned poortnummer) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens || tekenreeks_gegevens->TYPE_gebied != 1) return -9;
    if (tekenreeks_gegevens->fout) return tekenreeks_gegevens->fout;
    if (tekenreeks_gegevens->연결됨) return 0;
    if (tekenreeks_gegevens->peer_eindpunt_nummer) return -115;
    if (!poortnummer || poortnummer > 65535 || !ADRES) return -22;
    ip_addr_t internetadres; ip_addr_set_ip4_u32(&internetadres, lwip_htonl(ADRES));
    tekenreeks_gegevens->peer_ADRES = ADRES; tekenreeks_gegevens->peer_eindpunt_nummer = poortnummer;
    err_t 보조항목 = tcp_connect(tekenreeks_gegevens->verbinding_controle, &internetadres, poortnummer, 연결됨); return 보조항목 ? foutnummer(보조항목) : -115;
}
int NET_accepteren(int bestandsingang) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens || !tekenreeks_gegevens->ontvangen_poort) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_gebied == 1 && 통신끝점들[순번].informatie_In_behandeling == bestandsingang) { 통신끝점들[순번].informatie_In_behandeling = -1; return 순번; }
    return -11;
}
int 통신읽기(int bestandsingang, void *gegevens, unsigned item_AANTAL) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens || tekenreeks_gegevens->TYPE_gebied != 1) return -9;
    if (!item_AANTAL) return 0; if (!tekenreeks_gegevens->invoer_AANTAL_8f7753a1) return tekenreeks_gegevens->fout ? tekenreeks_gegevens->fout : tekenreeks_gegevens->Bestand_beëindigen ? 0 : -11;
    if (item_AANTAL > tekenreeks_gegevens->invoer_AANTAL_8f7753a1) item_AANTAL = tekenreeks_gegevens->invoer_AANTAL_8f7753a1;
    for (unsigned 순번 = 0; 순번 < item_AANTAL; 순번++) { ((unsigned char *)gegevens)[순번] = tekenreeks_gegevens->gegevens[tekenreeks_gegevens->voorkant_invoer]; tekenreeks_gegevens->voorkant_invoer = (tekenreeks_gegevens->voorkant_invoer + 1) % sizeof(tekenreeks_gegevens->gegevens); }
    tekenreeks_gegevens->invoer_AANTAL_8f7753a1 -= item_AANTAL; if (tekenreeks_gegevens->verbinding_controle) tcp_recved(tekenreeks_gegevens->verbinding_controle, item_AANTAL); return item_AANTAL;
}
int NET_schrijven(int bestandsingang, const void *gegevens, unsigned item_AANTAL) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens || tekenreeks_gegevens->TYPE_gebied != 1) return -9;
    if (tekenreeks_gegevens->fout) return tekenreeks_gegevens->fout; if (!tekenreeks_gegevens->verbinding_controle || !tekenreeks_gegevens->연결됨) return -107;
    if (!item_AANTAL) return 0; if (item_AANTAL > tcp_sndbuf(tekenreeks_gegevens->verbinding_controle)) item_AANTAL = tcp_sndbuf(tekenreeks_gegevens->verbinding_controle);
    if (!item_AANTAL) return -11; if (item_AANTAL > 1024) item_AANTAL = 1024;
    err_t 보조항목 = tcp_write(tekenreeks_gegevens->verbinding_controle, gegevens, item_AANTAL, TCP_WRITE_FLAG_COPY); if (보조항목) return foutnummer(보조항목);
    tcp_output(tekenreeks_gegevens->verbinding_controle); return item_AANTAL;
}
int e_mailen_datagram(int bestandsingang, const void *gegevens, unsigned item_AANTAL, uint32_t ADRES, unsigned poortnummer) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens || tekenreeks_gegevens->TYPE_gebied != 2) return -9;
    if (item_AANTAL > 512) return -90; if (!poortnummer || poortnummer > 65535) return -22;
    struct pbuf *gegevens_functie = pbuf_alloc(PBUF_TRANSPORT, item_AANTAL, PBUF_RAM); if (!gegevens_functie) return -11;
    pbuf_take(gegevens_functie, gegevens, item_AANTAL); ip_addr_t internetadres; ip_addr_set_ip4_u32(&internetadres, lwip_htonl(ADRES));
    err_t 보조항목 = udp_sendto(tekenreeks_gegevens->datagram_controle, gegevens_functie, &internetadres, poortnummer); pbuf_free(gegevens_functie); return 보조항목 ? foutnummer(보조항목) : (int)item_AANTAL;
}
int ontvangen_datagram(int bestandsingang, void *gegevens, unsigned item_AANTAL) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens || tekenreeks_gegevens->TYPE_gebied != 2) return -9;
    if (!tekenreeks_gegevens->invoer_AANTAL_8f7753a1) return -11; unsigned actueel_functie = tekenreeks_gegevens->voorkant_invoer;
    if (item_AANTAL > tekenreeks_gegevens->길이목록[actueel_functie]) item_AANTAL = tekenreeks_gegevens->길이목록[actueel_functie]; memcpy(gegevens, tekenreeks_gegevens->gegevens + actueel_functie * 512, item_AANTAL);
    tekenreeks_gegevens->peer_eindpunt_nummer = tekenreeks_gegevens->접속번호들[actueel_functie]; tekenreeks_gegevens->peer_ADRES = tekenreeks_gegevens->주소목록[actueel_functie]; tekenreeks_gegevens->voorkant_invoer = (actueel_functie + 1) % 4; tekenreeks_gegevens->invoer_AANTAL_8f7753a1--; return item_AANTAL;
}
unsigned net_poortnummer(int bestandsingang) { socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); return !tekenreeks_gegevens ? 0 : tekenreeks_gegevens->verbinding_controle ? tekenreeks_gegevens->verbinding_controle->local_port : tekenreeks_gegevens->datagram_controle ? tekenreeks_gegevens->datagram_controle->local_port : 0; }
unsigned peer_poortnummer(int bestandsingang) { socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); return tekenreeks_gegevens ? tekenreeks_gegevens->peer_eindpunt_nummer : 0; }
uint32_t NET_peer_ADRES(int bestandsingang) { socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); return tekenreeks_gegevens ? tekenreeks_gegevens->peer_ADRES : 0; }
void Sluiten_net(int bestandsingang) {
    socket_eindpunt_3db661a2 *tekenreeks_gegevens = ophalen_WAARDE(bestandsingang); if (!tekenreeks_gegevens) return;
    if (tekenreeks_gegevens->ontvangen_poort) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_gebied && 통신끝점들[순번].informatie_In_behandeling == bestandsingang) Sluiten_net(순번);
    if (tekenreeks_gegevens->verbinding_controle) {
        tcp_arg(tekenreeks_gegevens->verbinding_controle, 0); if (tekenreeks_gegevens->ontvangen_poort) tcp_accept(tekenreeks_gegevens->verbinding_controle, 0); else { tcp_recv(tekenreeks_gegevens->verbinding_controle, 0); tcp_err(tekenreeks_gegevens->verbinding_controle, 0); }
        if (tcp_close(tekenreeks_gegevens->verbinding_controle) != ERR_OK) tcp_abort(tekenreeks_gegevens->verbinding_controle);
    }
    if (tekenreeks_gegevens->datagram_controle) udp_remove(tekenreeks_gegevens->datagram_controle); tekenreeks_gegevens->TYPE_gebied = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || navragen) return; navragen = 1;
    if(gebruik_bekabeld_net)유선망살피기(&verbinding_mobiel);
    for (unsigned budget = 0; !gebruik_bekabeld_net && budget < 4096 && (machine_register(보조장치 + 0x54) & 1); budget++) {
        unsigned codepoint = machine_register(보조장치 + 0x40) & 255;
        if (codepoint == 192) {
            if (ontvangen_gebruik && !ontvangen_fout && !수신탈출) {
                struct pbuf *gegevens_functie = pbuf_alloc(PBUF_RAW, ontvangen_gebruik, PBUF_POOL);
                if (gegevens_functie) { OPBRENGST_datagram_AANTAL++; OPBRENGST_byte_AANTAL += ontvangen_gebruik; pbuf_take(gegevens_functie, ontvangen_gegevensbuffer, ontvangen_gebruik); if (verbinding_mobiel.input(gegevens_functie, &verbinding_mobiel) != ERR_OK) { 버린전문수++; pbuf_free(gegevens_functie); } }
                else 버린전문수++;
            }
            else if (ontvangen_gebruik) 버린전문수++;
            ontvangen_gebruik = ontvangen_fout = 수신탈출 = 0;
        } else if (codepoint == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (codepoint != 220 && codepoint != 221) ontvangen_fout = 1; codepoint = codepoint == 220 ? 192 : 219; 수신탈출 = 0; }
            if (ontvangen_gebruik < sizeof(ontvangen_gegevensbuffer)) ontvangen_gegevensbuffer[ontvangen_gebruik++] = codepoint; else ontvangen_fout = 1;
        }
    }
    netif_poll(&verbinding_mobiel); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budget = 0; budget < 4096 && 송신개수 && (machine_register(보조장치 + 0x54) & 0x20); budget++) {
        machine_register(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    navragen = 0;
}

/* Instellingen·조회는 lwIP의 werkelijk_gegevens 인터페이스와 beëindigen_punt 표를 사용한다. */
uint32_t 망상태읽기(unsigned invoer_WAARDE_962f286b, unsigned INDEX) {
    if(invoer_WAARDE_962f286b==20)return gebruik_bekabeld_net;
    if(invoer_WAARDE_962f286b==21)return 준비됨&&netif_is_link_up(&verbinding_mobiel);
    if(invoer_WAARDE_962f286b==22)return gebruik_bekabeld_net?bekabeld_net_Statistieken(5):0;
    if (!준비됨) return 0;
    if(gebruik_bekabeld_net&&invoer_WAARDE_962f286b>=4&&invoer_WAARDE_962f286b<=8)return bekabeld_net_Statistieken(invoer_WAARDE_962f286b-4);
    if (invoer_WAARDE_962f286b == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&verbinding_mobiel)));
    if (invoer_WAARDE_962f286b == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&verbinding_mobiel)));
    if (invoer_WAARDE_962f286b == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&verbinding_mobiel)));
    if (invoer_WAARDE_962f286b == 3) return netif_is_up(&verbinding_mobiel) != 0;
    if (invoer_WAARDE_962f286b == 4) return OPBRENGST_datagram_AANTAL;
    if (invoer_WAARDE_962f286b == 5) return 보낸전문수;
    if (invoer_WAARDE_962f286b == 6) return OPBRENGST_byte_AANTAL;
    if (invoer_WAARDE_962f286b == 7) return 보낸바이트수;
    if (invoer_WAARDE_962f286b == 8) return 버린전문수;
    if (invoer_WAARDE_962f286b == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    socket_eindpunt_3db661a2 *beëindigen_punt = &통신끝점들[INDEX];
    if (invoer_WAARDE_962f286b == 10) return beëindigen_punt->TYPE_gebied;
    if (!beëindigen_punt->TYPE_gebied) return 0;
    if (invoer_WAARDE_962f286b == 11) return net_poortnummer(INDEX);
    if (invoer_WAARDE_962f286b == 12) return beëindigen_punt->peer_ADRES;
    if (invoer_WAARDE_962f286b == 13) return beëindigen_punt->peer_eindpunt_nummer;
    if (invoer_WAARDE_962f286b == 14) return beëindigen_punt->ontvangen_poort ? 1 : beëindigen_punt->Bestand_beëindigen ? 3 : beëindigen_punt->fout ? 4 : beëindigen_punt->연결됨 ? 2 : 0;
    if (invoer_WAARDE_962f286b == 15) return beëindigen_punt->invoer_AANTAL_8f7753a1;
    if (invoer_WAARDE_962f286b == 16) {
        const ip_addr_t *ADRES = beëindigen_punt->TYPE_gebied == 1 && beëindigen_punt->verbinding_controle ? &beëindigen_punt->verbinding_controle->local_ip :
            beëindigen_punt->TYPE_gebied == 2 && beëindigen_punt->datagram_controle ? &beëindigen_punt->datagram_controle->local_ip : 0;
        return ADRES ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADRES))) : 0;
    }
    return 0;
}

int configureren_net(unsigned Actie, uint32_t ADRES, uint32_t masker_WAARDE, uint32_t gateway_WAARDE) {
    if (!준비됨) return -100;
    if (Actie == 1) { netif_set_up(&verbinding_mobiel); return 0; }
    if (Actie == 2) { netif_set_down(&verbinding_mobiel); return 0; }
    if (Actie != 0) return -22;
    /* 유니캐스트 IPv4, 연속 masker_WAARDE, 같은 망의 선택적 standaardwaarde gateway_WAARDE. */
    uint32_t 뒤집은가림 = ~masker_WAARDE;
    if (!masker_WAARDE || (뒤집은가림 & (뒤집은가림 + 1)) || !ADRES || (ADRES >> 24) == 127 ||
        (ADRES >> 24) == 0 || (ADRES >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADRES & 뒤집은가림) || (ADRES & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_WAARDE && ((gateway_WAARDE & masker_WAARDE) != (ADRES & masker_WAARDE) || gateway_WAARDE == ADRES || (gateway_WAARDE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_WAARDE & 뒤집은가림) || (gateway_WAARDE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADRES 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_gebied &&
        !(통신끝점들[INDEX].ontvangen_poort && 통신끝점들[INDEX].verbinding_controle && ip_addr_isany(&통신끝점들[INDEX].verbinding_controle->local_ip))) return -16;
    if(gebruik_bekabeld_net)dhcp_stop(&verbinding_mobiel);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADRES)); ip4_addr_set_u32(&새가림, lwip_htonl(masker_WAARDE)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_WAARDE));
    netif_set_addr(&verbinding_mobiel, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *reactie_eindpunt;
static uint32_t test_ADRES, test_TIJD, reactietijd;
static unsigned test_REEKS, test_id, reactie_REEKS;
static int reactie_Status;
static u8_t 응답받음(void *argumenten, struct raw_pcb *beëindigen_punt, struct pbuf *gegevens, const ip_addr_t *ADRES) {
    (void)argumenten; (void)beëindigen_punt;
    unsigned char kop_WAARDE[20], reactie[16];
    if (reactie_Status != -11 || gegevens->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADRES))) != test_ADRES || pbuf_copy_partial(gegevens, kop_WAARDE, 20, 0) != 20) return 0;
    unsigned header_formaat_wijzigen = (kop_WAARDE[0] & 15) * 4;
    if ((kop_WAARDE[0] >> 4) != 4 || header_formaat_wijzigen < 20 || gegevens->tot_len < header_formaat_wijzigen + 16 ||
        pbuf_copy_partial(gegevens, reactie, 16, header_formaat_wijzigen) != 16 || reactie[0] || reactie[1] ||
        (((unsigned)reactie[4] << 8) | reactie[5]) != test_id ||
        (((unsigned)reactie[6] << 8) | reactie[7]) != test_REEKS ||
        reactie[8] != 'J' || reactie[9] != 'K' || reactie[10] != 'O' || reactie[11] != 'S' ||
        (((uint32_t)reactie[12] << 24) | ((uint32_t)reactie[13] << 16) | ((uint32_t)reactie[14] << 8) | reactie[15]) != test_TIJD) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(gegevens, header_formaat_wijzigen)) return 0;
    if (inet_chksum_pbuf(gegevens)) { pbuf_add_header(gegevens, header_formaat_wijzigen); return 0; }
    reactietijd = (uint32_t)보드밀리초() - test_TIJD; reactie_REEKS = kop_WAARDE[8]; reactie_Status = 0;
    pbuf_free(gegevens); return 1;
}
int START_reactie_test(uint32_t ADRES, unsigned order_WAARDE) {
    if (!준비됨 || !netif_is_up(&verbinding_mobiel)) return -100;
    if (!ADRES || (ADRES >> 28) >= 14 || ADRES == 0xffffffffu) return -22;
    if (!reactie_eindpunt) { reactie_eindpunt = raw_new(IP_PROTO_ICMP); if (!reactie_eindpunt) return -12; raw_recv(reactie_eindpunt, 응답받음, 0); }
    test_ADRES = ADRES; test_REEKS = order_WAARDE & 65535; test_id = (test_id + 1) & 65535;
    test_TIJD = 보드밀리초(); reactie_Status = -11; reactietijd = reactie_REEKS = 0;
    unsigned char gegevens[32] = {8,0,0,0};
    gegevens[4] = test_id >> 8; gegevens[5] = test_id; gegevens[6] = test_REEKS >> 8; gegevens[7] = test_REEKS;
    gegevens[8]='J'; gegevens[9]='K'; gegevens[10]='O'; gegevens[11]='S';
    gegevens[12]=test_TIJD >> 24; gegevens[13]=test_TIJD >> 16; gegevens[14]=test_TIJD >> 8; gegevens[15]=test_TIJD;
    for (unsigned plaatsingsindex = 16; plaatsingsindex < sizeof(gegevens); plaatsingsindex++) gegevens[plaatsingsindex] = plaatsingsindex;
    uint16_t verificatie_controlesom = inet_chksum(gegevens, sizeof(gegevens)); memcpy(gegevens + 2, &verificatie_controlesom, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(gegevens), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, gegevens, sizeof(gegevens)); ip_addr_t doel_eindpunt; ip_addr_set_ip4_u32(&doel_eindpunt, lwip_htonl(ADRES));
    err_t 처리값 = raw_sendto(reactie_eindpunt, datagram, &doel_eindpunt); pbuf_free(datagram);
    if (처리값) reactie_Status = foutnummer(처리값);
    return 처리값 ? reactie_Status : 0;
}
int 응답시험읽기(unsigned invoer_WAARDE_962f286b) {
    통신망살피기();
    return invoer_WAARDE_962f286b == 0 ? reactie_Status : invoer_WAARDE_962f286b == 1 ? (int)reactietijd : invoer_WAARDE_962f286b == 2 ? (int)reactie_REEKS : -22;
}
