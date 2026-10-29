#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "nettverk_stakk.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../ekstern_VERDI_28edcfa1/ekstern_VERDI_28edcfa1.h"
#include "kabelbasert_nettverk.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define maskin_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif kontakt_enhet;
static int 준비됨, avspørring;
static int bruk_kabelbasert_nettverk;
static unsigned motta_bruk, 수신탈출, motta_feil;
static unsigned char motta_databuffer[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t MOTTATT_AVKAST_datagram_ANTALL, 보낸전문수, MOTTATT_AVKAST_byte_ANTALL, 보낸바이트수, 버린전문수;
typedef struct {
    int Type_område, motta_port, informasjonssystemer_Venter, 연결됨, Fil_avslutte_en_samtale, feil;
    struct tcp_pcb *kontakt_kontroll;
    struct udp_pcb *datagram_kontroll;
    unsigned frontkamera_oppføring, oppføring_ANTALL;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], node_deltaker_nummer;
    uint32_t 주소목록[4], node_e_post;
} socket_deltaker_3db661a2;
static socket_deltaker_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int feilnummer(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static socket_deltaker_3db661a2 *hente_VERDI(int Fil_håndtak) { return Fil_håndtak >= 0 && Fil_håndtak < 32 && 통신끝점들[Fil_håndtak].Type_område ? &통신끝점들[Fil_håndtak] : 0; }
static int 예약하기(int Type_område) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].Type_område) {
        memset(&통신끝점들[순번], 0, sizeof(socket_deltaker_3db661a2)); 통신끝점들[순번].Type_område = Type_område; 통신끝점들[순번].informasjonssystemer_Venter = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned tegnkode) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = tegnkode; }
static err_t produksjon(struct netif *vare_ANTALL, struct pbuf *data_plassere, const ip4_addr_t *e_post) {
    (void)vare_ANTALL; (void)e_post;
    if (data_plassere->tot_len > 1500 || 송신개수 + 2 * data_plassere->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Neste_FORSKYVNING = data_plassere; Neste_FORSKYVNING; Neste_FORSKYVNING = Neste_FORSKYVNING->next) for (unsigned 순번 = 0; 순번 < Neste_FORSKYVNING->len; 순번++) {
        unsigned tegnkode = ((unsigned char *)Neste_FORSKYVNING->payload)[순번];
        if (tegnkode == 192 || tegnkode == 219) { 내보내기(219); 내보내기(tegnkode == 192 ? 220 : 221); } else 내보내기(tegnkode);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_plassere->tot_len; return ERR_OK;
}
static err_t Forbered_CLR(struct netif *vare_ANTALL) { vare_ANTALL->name[0] = 's'; vare_ANTALL->name[1] = 'l'; vare_ANTALL->mtu = 1500; vare_ANTALL->output = produksjon; return ERR_OK; }
void Forbered_nettverk(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    maskin_register(보조장치 + 4) |= 1; maskin_register(보조장치 + 0x60) = 0; maskin_register(보조장치 + 0x44) = 0;
    maskin_register(보조장치 + 0x48) = 0xc6; maskin_register(보조장치 + 0x4c) = 3; maskin_register(보조장치 + 0x68) = 270; maskin_register(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internett_adresse, bitmaske, gateway_adresse;
    bruk_kabelbasert_nettverk=유선장치있음();
    ip4_addr_set_u32(&Internett_adresse, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmaske, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gateway_adresse, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&kontakt_enhet, &Internett_adresse, &bitmaske, &gateway_adresse, 0, bruk_kabelbasert_nettverk?Forbered_kabelbasert_nettverk:Forbered_CLR, bruk_kabelbasert_nettverk?ethernet_input:ip4_input))return;
    netif_set_default(&kontakt_enhet); netif_set_up(&kontakt_enhet);if(!bruk_kabelbasert_nettverk)netif_set_link_up(&kontakt_enhet); 준비됨 = 1;
    Forbered_ekstern();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *data_plassere, err_t feil) {
    socket_deltaker_3db661a2 *streng_data = 부가인수; (void)통신제어블록; (void)feil;
    if (!data_plassere) { streng_data->Fil_avslutte_en_samtale = 1; return ERR_OK; }
    if (data_plassere->tot_len > sizeof(streng_data->data) - streng_data->oppføring_ANTALL) return ERR_MEM;
    unsigned betalt_plassere = (streng_data->frontkamera_oppføring + streng_data->oppføring_ANTALL) % sizeof(streng_data->data);
    for (struct pbuf *Neste_FORSKYVNING = data_plassere; Neste_FORSKYVNING; Neste_FORSKYVNING = Neste_FORSKYVNING->next) for (unsigned 순번 = 0; 순번 < Neste_FORSKYVNING->len; 순번++) {
        streng_data->data[betalt_plassere] = ((unsigned char *)Neste_FORSKYVNING->payload)[순번]; betalt_plassere = (betalt_plassere + 1) % sizeof(streng_data->data);
    }
    streng_data->oppføring_ANTALL += data_plassere->tot_len; pbuf_free(data_plassere); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t feil) { socket_deltaker_3db661a2 *streng_data = 부가인수; streng_data->kontakt_kontroll = 0; streng_data->feil = feilnummer(feil); }
static void 되부름목록(socket_deltaker_3db661a2 *streng_data) { tcp_arg(streng_data->kontakt_kontroll, streng_data); tcp_recv(streng_data->kontakt_kontroll, 수신됨); tcp_err(streng_data->kontakt_kontroll, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t feil) {
    socket_deltaker_3db661a2 *streng_data = 부가인수; (void)통신제어블록; if (feil) streng_data->feil = feilnummer(feil); else streng_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t feil) {
    socket_deltaker_3db661a2 *overordnet = 부가인수; if (feil) return feil;
    int Fil_håndtak = 예약하기(1); if (Fil_håndtak < 0) return ERR_MEM;
    socket_deltaker_3db661a2 *streng_data = &통신끝점들[Fil_håndtak]; streng_data->kontakt_kontroll = 통신제어블록; streng_data->연결됨 = 1; streng_data->informasjonssystemer_Venter = (int)(overordnet - 통신끝점들);
    streng_data->node_e_post = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); streng_data->node_deltaker_nummer = 통신제어블록->remote_port;
    되부름목록(streng_data); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *data_plassere, const ip_addr_t *e_post, u16_t portnummer) {
    socket_deltaker_3db661a2 *streng_data = 부가인수; (void)통신제어블록;
    if (streng_data->oppføring_ANTALL < 4 && data_plassere->tot_len <= 512) {
        unsigned posisjonsindeks = (streng_data->frontkamera_oppføring + streng_data->oppføring_ANTALL) % 4;
        pbuf_copy_partial(data_plassere, streng_data->data + posisjonsindeks * 512, data_plassere->tot_len, 0);
        streng_data->길이목록[posisjonsindeks] = data_plassere->tot_len; streng_data->접속번호들[posisjonsindeks] = portnummer;
        streng_data->주소목록[posisjonsindeks] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_post))); streng_data->oppføring_ANTALL++;
    }
    pbuf_free(data_plassere);
}
int åpne_socket_deltaker(int Type_område) {
    if (!준비됨) return -100;
    if (Type_område != 1 && Type_område != 2) return -93;
    int Fil_håndtak = 예약하기(Type_område); if (Fil_håndtak < 0) return Fil_håndtak;
    socket_deltaker_3db661a2 *streng_data = &통신끝점들[Fil_håndtak];
    if (Type_område == 1) { streng_data->kontakt_kontroll = tcp_new(); if (streng_data->kontakt_kontroll) 되부름목록(streng_data); }
    else { streng_data->datagram_kontroll = udp_new(); if (streng_data->datagram_kontroll) udp_recv(streng_data->datagram_kontroll, datagram, streng_data); }
    if (!streng_data->kontakt_kontroll && !streng_data->datagram_kontroll) { streng_data->Type_område = 0; return -12; } return Fil_håndtak;
}
int netto_BIND(int Fil_håndtak, uint32_t e_post, unsigned portnummer) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data) return -9;
    if (portnummer > 65535 || (e_post && e_post != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_enhet))) && e_post != 0x7f000001)) return -99;
    ip_addr_t Internett_adresse; ip_addr_set_ip4_u32(&Internett_adresse, lwip_htonl(e_post));
    err_t 보조항목 = streng_data->Type_område == 1 ? tcp_bind(streng_data->kontakt_kontroll, &Internett_adresse, portnummer) : udp_bind(streng_data->datagram_kontroll, &Internett_adresse, portnummer); return 보조항목 ? feilnummer(보조항목) : 0;
}
void 통신주소재사용(int Fil_håndtak) { socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (streng_data && streng_data->kontakt_kontroll) ip_set_option(streng_data->kontakt_kontroll, SOF_REUSEADDR); }
int 연결기다리기(int Fil_håndtak) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data || streng_data->Type_område != 1) return -9;
    if (streng_data->motta_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(streng_data->kontakt_kontroll, 4, &보조항목);
    if (!통신제어블록) return feilnummer(보조항목); streng_data->kontakt_kontroll = 통신제어블록; streng_data->motta_port = 1; tcp_arg(통신제어블록, streng_data); tcp_accept(통신제어블록, 연결받음); return 0;
}
int netto_KOBLE_TIL(int Fil_håndtak, uint32_t e_post, unsigned portnummer) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data || streng_data->Type_område != 1) return -9;
    if (streng_data->feil) return streng_data->feil;
    if (streng_data->연결됨) return 0;
    if (streng_data->node_deltaker_nummer) return -115;
    if (!portnummer || portnummer > 65535 || !e_post) return -22;
    ip_addr_t Internett_adresse; ip_addr_set_ip4_u32(&Internett_adresse, lwip_htonl(e_post));
    streng_data->node_e_post = e_post; streng_data->node_deltaker_nummer = portnummer;
    err_t 보조항목 = tcp_connect(streng_data->kontakt_kontroll, &Internett_adresse, portnummer, 연결됨); return 보조항목 ? feilnummer(보조항목) : -115;
}
int netto_godta(int Fil_håndtak) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data || !streng_data->motta_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].Type_område == 1 && 통신끝점들[순번].informasjonssystemer_Venter == Fil_håndtak) { 통신끝점들[순번].informasjonssystemer_Venter = -1; return 순번; }
    return -11;
}
int 통신읽기(int Fil_håndtak, void *data, unsigned vare_ANTALL) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data || streng_data->Type_område != 1) return -9;
    if (!vare_ANTALL) return 0; if (!streng_data->oppføring_ANTALL) return streng_data->feil ? streng_data->feil : streng_data->Fil_avslutte_en_samtale ? 0 : -11;
    if (vare_ANTALL > streng_data->oppføring_ANTALL) vare_ANTALL = streng_data->oppføring_ANTALL;
    for (unsigned 순번 = 0; 순번 < vare_ANTALL; 순번++) { ((unsigned char *)data)[순번] = streng_data->data[streng_data->frontkamera_oppføring]; streng_data->frontkamera_oppføring = (streng_data->frontkamera_oppføring + 1) % sizeof(streng_data->data); }
    streng_data->oppføring_ANTALL -= vare_ANTALL; if (streng_data->kontakt_kontroll) tcp_recved(streng_data->kontakt_kontroll, vare_ANTALL); return vare_ANTALL;
}
int netto_skrive(int Fil_håndtak, const void *data, unsigned vare_ANTALL) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data || streng_data->Type_område != 1) return -9;
    if (streng_data->feil) return streng_data->feil; if (!streng_data->kontakt_kontroll || !streng_data->연결됨) return -107;
    if (!vare_ANTALL) return 0; if (vare_ANTALL > tcp_sndbuf(streng_data->kontakt_kontroll)) vare_ANTALL = tcp_sndbuf(streng_data->kontakt_kontroll);
    if (!vare_ANTALL) return -11; if (vare_ANTALL > 1024) vare_ANTALL = 1024;
    err_t 보조항목 = tcp_write(streng_data->kontakt_kontroll, data, vare_ANTALL, TCP_WRITE_FLAG_COPY); if (보조항목) return feilnummer(보조항목);
    tcp_output(streng_data->kontakt_kontroll); return vare_ANTALL;
}
int sende_datagram(int Fil_håndtak, const void *data, unsigned vare_ANTALL, uint32_t e_post, unsigned portnummer) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data || streng_data->Type_område != 2) return -9;
    if (vare_ANTALL > 512) return -90; if (!portnummer || portnummer > 65535) return -22;
    struct pbuf *data_plassere = pbuf_alloc(PBUF_TRANSPORT, vare_ANTALL, PBUF_RAM); if (!data_plassere) return -11;
    pbuf_take(data_plassere, data, vare_ANTALL); ip_addr_t Internett_adresse; ip_addr_set_ip4_u32(&Internett_adresse, lwip_htonl(e_post));
    err_t 보조항목 = udp_sendto(streng_data->datagram_kontroll, data_plassere, &Internett_adresse, portnummer); pbuf_free(data_plassere); return 보조항목 ? feilnummer(보조항목) : (int)vare_ANTALL;
}
int motta_datagram(int Fil_håndtak, void *data, unsigned vare_ANTALL) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data || streng_data->Type_område != 2) return -9;
    if (!streng_data->oppføring_ANTALL) return -11; unsigned betalt_plassere = streng_data->frontkamera_oppføring;
    if (vare_ANTALL > streng_data->길이목록[betalt_plassere]) vare_ANTALL = streng_data->길이목록[betalt_plassere]; memcpy(data, streng_data->data + betalt_plassere * 512, vare_ANTALL);
    streng_data->node_deltaker_nummer = streng_data->접속번호들[betalt_plassere]; streng_data->node_e_post = streng_data->주소목록[betalt_plassere]; streng_data->frontkamera_oppføring = (betalt_plassere + 1) % 4; streng_data->oppføring_ANTALL--; return vare_ANTALL;
}
unsigned nettverk_portnummer(int Fil_håndtak) { socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); return !streng_data ? 0 : streng_data->kontakt_kontroll ? streng_data->kontakt_kontroll->local_port : streng_data->datagram_kontroll ? streng_data->datagram_kontroll->local_port : 0; }
unsigned node_portnummer(int Fil_håndtak) { socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); return streng_data ? streng_data->node_deltaker_nummer : 0; }
uint32_t netto_node_e_post(int Fil_håndtak) { socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); return streng_data ? streng_data->node_e_post : 0; }
void Lukk_nettverk(int Fil_håndtak) {
    socket_deltaker_3db661a2 *streng_data = hente_VERDI(Fil_håndtak); if (!streng_data) return;
    if (streng_data->motta_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].Type_område && 통신끝점들[순번].informasjonssystemer_Venter == Fil_håndtak) Lukk_nettverk(순번);
    if (streng_data->kontakt_kontroll) {
        tcp_arg(streng_data->kontakt_kontroll, 0); if (streng_data->motta_port) tcp_accept(streng_data->kontakt_kontroll, 0); else { tcp_recv(streng_data->kontakt_kontroll, 0); tcp_err(streng_data->kontakt_kontroll, 0); }
        if (tcp_close(streng_data->kontakt_kontroll) != ERR_OK) tcp_abort(streng_data->kontakt_kontroll);
    }
    if (streng_data->datagram_kontroll) udp_remove(streng_data->datagram_kontroll); streng_data->Type_område = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || avspørring) return; avspørring = 1;
    if(bruk_kabelbasert_nettverk)유선망살피기(&kontakt_enhet);
    for (unsigned budsjett = 0; !bruk_kabelbasert_nettverk && budsjett < 4096 && (maskin_register(보조장치 + 0x54) & 1); budsjett++) {
        unsigned tegnkode = maskin_register(보조장치 + 0x40) & 255;
        if (tegnkode == 192) {
            if (motta_bruk && !motta_feil && !수신탈출) {
                struct pbuf *data_plassere = pbuf_alloc(PBUF_RAW, motta_bruk, PBUF_POOL);
                if (data_plassere) { MOTTATT_AVKAST_datagram_ANTALL++; MOTTATT_AVKAST_byte_ANTALL += motta_bruk; pbuf_take(data_plassere, motta_databuffer, motta_bruk); if (kontakt_enhet.input(data_plassere, &kontakt_enhet) != ERR_OK) { 버린전문수++; pbuf_free(data_plassere); } }
                else 버린전문수++;
            }
            else if (motta_bruk) 버린전문수++;
            motta_bruk = motta_feil = 수신탈출 = 0;
        } else if (tegnkode == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (tegnkode != 220 && tegnkode != 221) motta_feil = 1; tegnkode = tegnkode == 220 ? 192 : 219; 수신탈출 = 0; }
            if (motta_bruk < sizeof(motta_databuffer)) motta_databuffer[motta_bruk++] = tegnkode; else motta_feil = 1;
        }
    }
    netif_poll(&kontakt_enhet); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budsjett = 0; budsjett < 4096 && 송신개수 && (maskin_register(보조장치 + 0x54) & 0x20); budsjett++) {
        maskin_register(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    avspørring = 0;
}

/* Innstillinger·조회는 lwIP의 faktisk_data 인터페이스와 avslutte_en_samtale_peke 표를 사용한다. */
uint32_t 망상태읽기(unsigned oppføring_VERDI, unsigned INDEKS) {
    if(oppføring_VERDI==20)return bruk_kabelbasert_nettverk;
    if(oppføring_VERDI==21)return 준비됨&&netif_is_link_up(&kontakt_enhet);
    if(oppføring_VERDI==22)return bruk_kabelbasert_nettverk?kabelbasert_nettverk_statistikk(5):0;
    if (!준비됨) return 0;
    if(bruk_kabelbasert_nettverk&&oppføring_VERDI>=4&&oppføring_VERDI<=8)return kabelbasert_nettverk_statistikk(oppføring_VERDI-4);
    if (oppføring_VERDI == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_enhet)));
    if (oppføring_VERDI == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&kontakt_enhet)));
    if (oppføring_VERDI == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&kontakt_enhet)));
    if (oppføring_VERDI == 3) return netif_is_up(&kontakt_enhet) != 0;
    if (oppføring_VERDI == 4) return MOTTATT_AVKAST_datagram_ANTALL;
    if (oppføring_VERDI == 5) return 보낸전문수;
    if (oppføring_VERDI == 6) return MOTTATT_AVKAST_byte_ANTALL;
    if (oppføring_VERDI == 7) return 보낸바이트수;
    if (oppføring_VERDI == 8) return 버린전문수;
    if (oppføring_VERDI == 9) return 송신개수;
    if (INDEKS >= 32) return 0;
    socket_deltaker_3db661a2 *avslutte_en_samtale_peke = &통신끝점들[INDEKS];
    if (oppføring_VERDI == 10) return avslutte_en_samtale_peke->Type_område;
    if (!avslutte_en_samtale_peke->Type_område) return 0;
    if (oppføring_VERDI == 11) return nettverk_portnummer(INDEKS);
    if (oppføring_VERDI == 12) return avslutte_en_samtale_peke->node_e_post;
    if (oppføring_VERDI == 13) return avslutte_en_samtale_peke->node_deltaker_nummer;
    if (oppføring_VERDI == 14) return avslutte_en_samtale_peke->motta_port ? 1 : avslutte_en_samtale_peke->Fil_avslutte_en_samtale ? 3 : avslutte_en_samtale_peke->feil ? 4 : avslutte_en_samtale_peke->연결됨 ? 2 : 0;
    if (oppføring_VERDI == 15) return avslutte_en_samtale_peke->oppføring_ANTALL;
    if (oppføring_VERDI == 16) {
        const ip_addr_t *e_post = avslutte_en_samtale_peke->Type_område == 1 && avslutte_en_samtale_peke->kontakt_kontroll ? &avslutte_en_samtale_peke->kontakt_kontroll->local_ip :
            avslutte_en_samtale_peke->Type_område == 2 && avslutte_en_samtale_peke->datagram_kontroll ? &avslutte_en_samtale_peke->datagram_kontroll->local_ip : 0;
        return e_post ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_post))) : 0;
    }
    return 0;
}

int konfigurere_nettverk(unsigned Handling, uint32_t e_post, uint32_t maske_VERDI, uint32_t gateway_VERDI) {
    if (!준비됨) return -100;
    if (Handling == 1) { netif_set_up(&kontakt_enhet); return 0; }
    if (Handling == 2) { netif_set_down(&kontakt_enhet); return 0; }
    if (Handling != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maske_VERDI, 같은 망의 선택적 standardverdi gateway_VERDI. */
    uint32_t 뒤집은가림 = ~maske_VERDI;
    if (!maske_VERDI || (뒤집은가림 & (뒤집은가림 + 1)) || !e_post || (e_post >> 24) == 127 ||
        (e_post >> 24) == 0 || (e_post >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(e_post & 뒤집은가림) || (e_post & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_VERDI && ((gateway_VERDI & maske_VERDI) != (e_post & maske_VERDI) || gateway_VERDI == e_post || (gateway_VERDI >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_VERDI & 뒤집은가림) || (gateway_VERDI & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 e_post 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEKS = 0; INDEKS < 32; INDEKS++) if (통신끝점들[INDEKS].Type_område &&
        !(통신끝점들[INDEKS].motta_port && 통신끝점들[INDEKS].kontakt_kontroll && ip_addr_isany(&통신끝점들[INDEKS].kontakt_kontroll->local_ip))) return -16;
    if(bruk_kabelbasert_nettverk)dhcp_stop(&kontakt_enhet);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(e_post)); ip4_addr_set_u32(&새가림, lwip_htonl(maske_VERDI)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_VERDI));
    netif_set_addr(&kontakt_enhet, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *svar_deltaker;
static uint32_t test_e_post, test_TID, svartid;
static unsigned test_SEKVENS, test_identifikator, svar_SEKVENS;
static int svar_status;
static u8_t 응답받음(void *Argumenter, struct raw_pcb *avslutte_en_samtale_peke, struct pbuf *data, const ip_addr_t *e_post) {
    (void)Argumenter; (void)avslutte_en_samtale_peke;
    unsigned char 머리[20], svar[16];
    if (svar_status != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(e_post))) != test_e_post || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Topptekst_skalere = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Topptekst_skalere < 20 || data->tot_len < Topptekst_skalere + 16 ||
        pbuf_copy_partial(data, svar, 16, Topptekst_skalere) != 16 || svar[0] || svar[1] ||
        (((unsigned)svar[4] << 8) | svar[5]) != test_identifikator ||
        (((unsigned)svar[6] << 8) | svar[7]) != test_SEKVENS ||
        svar[8] != 'J' || svar[9] != 'K' || svar[10] != 'O' || svar[11] != 'S' ||
        (((uint32_t)svar[12] << 24) | ((uint32_t)svar[13] << 16) | ((uint32_t)svar[14] << 8) | svar[15]) != test_TID) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Topptekst_skalere)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Topptekst_skalere); return 0; }
    svartid = (uint32_t)보드밀리초() - test_TID; svar_SEKVENS = 머리[8]; svar_status = 0;
    pbuf_free(data); return 1;
}
int START_svar_test(uint32_t e_post, unsigned ordre_VERDI) {
    if (!준비됨 || !netif_is_up(&kontakt_enhet)) return -100;
    if (!e_post || (e_post >> 28) >= 14 || e_post == 0xffffffffu) return -22;
    if (!svar_deltaker) { svar_deltaker = raw_new(IP_PROTO_ICMP); if (!svar_deltaker) return -12; raw_recv(svar_deltaker, 응답받음, 0); }
    test_e_post = e_post; test_SEKVENS = ordre_VERDI & 65535; test_identifikator = (test_identifikator + 1) & 65535;
    test_TID = 보드밀리초(); svar_status = -11; svartid = svar_SEKVENS = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = test_identifikator >> 8; data[5] = test_identifikator; data[6] = test_SEKVENS >> 8; data[7] = test_SEKVENS;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=test_TID >> 24; data[13]=test_TID >> 16; data[14]=test_TID >> 8; data[15]=test_TID;
    for (unsigned posisjonsindeks = 16; posisjonsindeks < sizeof(data); posisjonsindeks++) data[posisjonsindeks] = posisjonsindeks;
    uint16_t kontroll_kontrollsum = inet_chksum(data, sizeof(data)); memcpy(data + 2, &kontroll_kontrollsum, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, data, sizeof(data)); ip_addr_t mål_deltaker; ip_addr_set_ip4_u32(&mål_deltaker, lwip_htonl(e_post));
    err_t 처리값 = raw_sendto(svar_deltaker, datagram, &mål_deltaker); pbuf_free(datagram);
    if (처리값) svar_status = feilnummer(처리값);
    return 처리값 ? svar_status : 0;
}
int 응답시험읽기(unsigned oppføring_VERDI) {
    통신망살피기();
    return oppføring_VERDI == 0 ? svar_status : oppføring_VERDI == 1 ? (int)svartid : oppføring_VERDI == 2 ? (int)svar_SEKVENS : -22;
}
