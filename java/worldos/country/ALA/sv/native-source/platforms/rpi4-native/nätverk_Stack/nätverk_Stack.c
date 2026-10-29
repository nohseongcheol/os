#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "nätverk_Stack.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../fjärr_värde/fjärr_värde.h"
#include "kabelansluten_nätverk.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define dator_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif kontakt_enhet;
static int 준비됨, avsökning;
static int använda_kabelansluten_nätverk;
static unsigned få_användning, 수신탈출, få_fel;
static unsigned char få_databuffert[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t BELOPP_datagram_ANTAL, 보낸전문수, BELOPP_byte_ANTAL, 보낸바이트수, 버린전문수;
typedef struct {
    int Typ_område, få_port, informationsteknik_väntar, 연결됨, fil_avsluta, fel;
    struct tcp_pcb *kontakt_kontroll;
    struct udp_pcb *datagram_kontroll;
    unsigned framåtvänd_post, post_ANTAL;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], peer_deltagare_nummer;
    uint32_t 주소목록[4], peer_ADRESS;
} socket_deltagare_3db661a2;
static socket_deltagare_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int felnummer(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static socket_deltagare_3db661a2 *hämta_värde(int filreferens) { return filreferens >= 0 && filreferens < 32 && 통신끝점들[filreferens].Typ_område ? &통신끝점들[filreferens] : 0; }
static int 예약하기(int Typ_område) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].Typ_område) {
        memset(&통신끝점들[순번], 0, sizeof(socket_deltagare_3db661a2)); 통신끝점들[순번].Typ_område = Typ_område; 통신끝점들[순번].informationsteknik_väntar = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kodpunkt) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kodpunkt; }
static err_t utleverans(struct netif *objekt_ANTAL, struct pbuf *data_placera, const ip4_addr_t *Adress) {
    (void)objekt_ANTAL; (void)Adress;
    if (data_placera->tot_len > 1500 || 송신개수 + 2 * data_placera->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Nästa_FÖRSKJUTNING = data_placera; Nästa_FÖRSKJUTNING; Nästa_FÖRSKJUTNING = Nästa_FÖRSKJUTNING->next) for (unsigned 순번 = 0; 순번 < Nästa_FÖRSKJUTNING->len; 순번++) {
        unsigned kodpunkt = ((unsigned char *)Nästa_FÖRSKJUTNING->payload)[순번];
        if (kodpunkt == 192 || kodpunkt == 219) { 내보내기(219); 내보내기(kodpunkt == 192 ? 220 : 221); } else 내보내기(kodpunkt);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_placera->tot_len; return ERR_OK;
}
static err_t Förbereda_CLR(struct netif *objekt_ANTAL) { objekt_ANTAL->name[0] = 's'; objekt_ANTAL->name[1] = 'l'; objekt_ANTAL->mtu = 1500; objekt_ANTAL->output = utleverans; return ERR_OK; }
void Förbereda_nätverk(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    dator_register(보조장치 + 4) |= 1; dator_register(보조장치 + 0x60) = 0; dator_register(보조장치 + 0x44) = 0;
    dator_register(보조장치 + 0x48) = 0xc6; dator_register(보조장치 + 0x4c) = 3; dator_register(보조장치 + 0x68) = 270; dator_register(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internetadress, bitmask, gateway_adress;
    använda_kabelansluten_nätverk=유선장치있음();
    ip4_addr_set_u32(&Internetadress, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmask, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gateway_adress, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&kontakt_enhet, &Internetadress, &bitmask, &gateway_adress, 0, använda_kabelansluten_nätverk?Förbereda_kabelansluten_nätverk:Förbereda_CLR, använda_kabelansluten_nätverk?ethernet_input:ip4_input))return;
    netif_set_default(&kontakt_enhet); netif_set_up(&kontakt_enhet);if(!använda_kabelansluten_nätverk)netif_set_link_up(&kontakt_enhet); 준비됨 = 1;
    Förbereda_fjärr();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *data_placera, err_t fel) {
    socket_deltagare_3db661a2 *sträng_data = 부가인수; (void)통신제어블록; (void)fel;
    if (!data_placera) { sträng_data->fil_avsluta = 1; return ERR_OK; }
    if (data_placera->tot_len > sizeof(sträng_data->data) - sträng_data->post_ANTAL) return ERR_MEM;
    unsigned aktuellt_placera = (sträng_data->framåtvänd_post + sträng_data->post_ANTAL) % sizeof(sträng_data->data);
    for (struct pbuf *Nästa_FÖRSKJUTNING = data_placera; Nästa_FÖRSKJUTNING; Nästa_FÖRSKJUTNING = Nästa_FÖRSKJUTNING->next) for (unsigned 순번 = 0; 순번 < Nästa_FÖRSKJUTNING->len; 순번++) {
        sträng_data->data[aktuellt_placera] = ((unsigned char *)Nästa_FÖRSKJUTNING->payload)[순번]; aktuellt_placera = (aktuellt_placera + 1) % sizeof(sträng_data->data);
    }
    sträng_data->post_ANTAL += data_placera->tot_len; pbuf_free(data_placera); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t fel) { socket_deltagare_3db661a2 *sträng_data = 부가인수; sträng_data->kontakt_kontroll = 0; sträng_data->fel = felnummer(fel); }
static void 되부름목록(socket_deltagare_3db661a2 *sträng_data) { tcp_arg(sträng_data->kontakt_kontroll, sträng_data); tcp_recv(sträng_data->kontakt_kontroll, 수신됨); tcp_err(sträng_data->kontakt_kontroll, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t fel) {
    socket_deltagare_3db661a2 *sträng_data = 부가인수; (void)통신제어블록; if (fel) sträng_data->fel = felnummer(fel); else sträng_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t fel) {
    socket_deltagare_3db661a2 *överordnad = 부가인수; if (fel) return fel;
    int filreferens = 예약하기(1); if (filreferens < 0) return ERR_MEM;
    socket_deltagare_3db661a2 *sträng_data = &통신끝점들[filreferens]; sträng_data->kontakt_kontroll = 통신제어블록; sträng_data->연결됨 = 1; sträng_data->informationsteknik_väntar = (int)(överordnad - 통신끝점들);
    sträng_data->peer_ADRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); sträng_data->peer_deltagare_nummer = 통신제어블록->remote_port;
    되부름목록(sträng_data); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *data_placera, const ip_addr_t *Adress, u16_t portnummer) {
    socket_deltagare_3db661a2 *sträng_data = 부가인수; (void)통신제어블록;
    if (sträng_data->post_ANTAL < 4 && data_placera->tot_len <= 512) {
        unsigned positionsindex = (sträng_data->framåtvänd_post + sträng_data->post_ANTAL) % 4;
        pbuf_copy_partial(data_placera, sträng_data->data + positionsindex * 512, data_placera->tot_len, 0);
        sträng_data->길이목록[positionsindex] = data_placera->tot_len; sträng_data->접속번호들[positionsindex] = portnummer;
        sträng_data->주소목록[positionsindex] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adress))); sträng_data->post_ANTAL++;
    }
    pbuf_free(data_placera);
}
int Skapa_socket_deltagare(int Typ_område) {
    if (!준비됨) return -100;
    if (Typ_område != 1 && Typ_område != 2) return -93;
    int filreferens = 예약하기(Typ_område); if (filreferens < 0) return filreferens;
    socket_deltagare_3db661a2 *sträng_data = &통신끝점들[filreferens];
    if (Typ_område == 1) { sträng_data->kontakt_kontroll = tcp_new(); if (sträng_data->kontakt_kontroll) 되부름목록(sträng_data); }
    else { sträng_data->datagram_kontroll = udp_new(); if (sträng_data->datagram_kontroll) udp_recv(sträng_data->datagram_kontroll, datagram, sträng_data); }
    if (!sträng_data->kontakt_kontroll && !sträng_data->datagram_kontroll) { sträng_data->Typ_område = 0; return -12; } return filreferens;
}
int NET_BIND(int filreferens, uint32_t Adress, unsigned portnummer) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data) return -9;
    if (portnummer > 65535 || (Adress && Adress != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_enhet))) && Adress != 0x7f000001)) return -99;
    ip_addr_t Internetadress; ip_addr_set_ip4_u32(&Internetadress, lwip_htonl(Adress));
    err_t 보조항목 = sträng_data->Typ_område == 1 ? tcp_bind(sträng_data->kontakt_kontroll, &Internetadress, portnummer) : udp_bind(sträng_data->datagram_kontroll, &Internetadress, portnummer); return 보조항목 ? felnummer(보조항목) : 0;
}
void 통신주소재사용(int filreferens) { socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (sträng_data && sträng_data->kontakt_kontroll) ip_set_option(sträng_data->kontakt_kontroll, SOF_REUSEADDR); }
int NET_lyssna(int filreferens) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data || sträng_data->Typ_område != 1) return -9;
    if (sträng_data->få_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(sträng_data->kontakt_kontroll, 4, &보조항목);
    if (!통신제어블록) return felnummer(보조항목); sträng_data->kontakt_kontroll = 통신제어블록; sträng_data->få_port = 1; tcp_arg(통신제어블록, sträng_data); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_ANSLUT(int filreferens, uint32_t Adress, unsigned portnummer) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data || sträng_data->Typ_område != 1) return -9;
    if (sträng_data->fel) return sträng_data->fel;
    if (sträng_data->연결됨) return 0;
    if (sträng_data->peer_deltagare_nummer) return -115;
    if (!portnummer || portnummer > 65535 || !Adress) return -22;
    ip_addr_t Internetadress; ip_addr_set_ip4_u32(&Internetadress, lwip_htonl(Adress));
    sträng_data->peer_ADRESS = Adress; sträng_data->peer_deltagare_nummer = portnummer;
    err_t 보조항목 = tcp_connect(sträng_data->kontakt_kontroll, &Internetadress, portnummer, 연결됨); return 보조항목 ? felnummer(보조항목) : -115;
}
int NET_acceptera(int filreferens) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data || !sträng_data->få_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].Typ_område == 1 && 통신끝점들[순번].informationsteknik_väntar == filreferens) { 통신끝점들[순번].informationsteknik_väntar = -1; return 순번; }
    return -11;
}
int NET_läsa(int filreferens, void *data, unsigned objekt_ANTAL) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data || sträng_data->Typ_område != 1) return -9;
    if (!objekt_ANTAL) return 0; if (!sträng_data->post_ANTAL) return sträng_data->fel ? sträng_data->fel : sträng_data->fil_avsluta ? 0 : -11;
    if (objekt_ANTAL > sträng_data->post_ANTAL) objekt_ANTAL = sträng_data->post_ANTAL;
    for (unsigned 순번 = 0; 순번 < objekt_ANTAL; 순번++) { ((unsigned char *)data)[순번] = sträng_data->data[sträng_data->framåtvänd_post]; sträng_data->framåtvänd_post = (sträng_data->framåtvänd_post + 1) % sizeof(sträng_data->data); }
    sträng_data->post_ANTAL -= objekt_ANTAL; if (sträng_data->kontakt_kontroll) tcp_recved(sträng_data->kontakt_kontroll, objekt_ANTAL); return objekt_ANTAL;
}
int NET_skriva(int filreferens, const void *data, unsigned objekt_ANTAL) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data || sträng_data->Typ_område != 1) return -9;
    if (sträng_data->fel) return sträng_data->fel; if (!sträng_data->kontakt_kontroll || !sträng_data->연결됨) return -107;
    if (!objekt_ANTAL) return 0; if (objekt_ANTAL > tcp_sndbuf(sträng_data->kontakt_kontroll)) objekt_ANTAL = tcp_sndbuf(sträng_data->kontakt_kontroll);
    if (!objekt_ANTAL) return -11; if (objekt_ANTAL > 1024) objekt_ANTAL = 1024;
    err_t 보조항목 = tcp_write(sträng_data->kontakt_kontroll, data, objekt_ANTAL, TCP_WRITE_FLAG_COPY); if (보조항목) return felnummer(보조항목);
    tcp_output(sträng_data->kontakt_kontroll); return objekt_ANTAL;
}
int skicka_datagram(int filreferens, const void *data, unsigned objekt_ANTAL, uint32_t Adress, unsigned portnummer) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data || sträng_data->Typ_område != 2) return -9;
    if (objekt_ANTAL > 512) return -90; if (!portnummer || portnummer > 65535) return -22;
    struct pbuf *data_placera = pbuf_alloc(PBUF_TRANSPORT, objekt_ANTAL, PBUF_RAM); if (!data_placera) return -11;
    pbuf_take(data_placera, data, objekt_ANTAL); ip_addr_t Internetadress; ip_addr_set_ip4_u32(&Internetadress, lwip_htonl(Adress));
    err_t 보조항목 = udp_sendto(sträng_data->datagram_kontroll, data_placera, &Internetadress, portnummer); pbuf_free(data_placera); return 보조항목 ? felnummer(보조항목) : (int)objekt_ANTAL;
}
int få_datagram(int filreferens, void *data, unsigned objekt_ANTAL) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data || sträng_data->Typ_område != 2) return -9;
    if (!sträng_data->post_ANTAL) return -11; unsigned aktuellt_placera = sträng_data->framåtvänd_post;
    if (objekt_ANTAL > sträng_data->길이목록[aktuellt_placera]) objekt_ANTAL = sträng_data->길이목록[aktuellt_placera]; memcpy(data, sträng_data->data + aktuellt_placera * 512, objekt_ANTAL);
    sträng_data->peer_deltagare_nummer = sträng_data->접속번호들[aktuellt_placera]; sträng_data->peer_ADRESS = sträng_data->주소목록[aktuellt_placera]; sträng_data->framåtvänd_post = (aktuellt_placera + 1) % 4; sträng_data->post_ANTAL--; return objekt_ANTAL;
}
unsigned nätverk_portnummer(int filreferens) { socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); return !sträng_data ? 0 : sträng_data->kontakt_kontroll ? sträng_data->kontakt_kontroll->local_port : sträng_data->datagram_kontroll ? sträng_data->datagram_kontroll->local_port : 0; }
unsigned peer_portnummer(int filreferens) { socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); return sträng_data ? sträng_data->peer_deltagare_nummer : 0; }
uint32_t NET_peer_ADRESS(int filreferens) { socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); return sträng_data ? sträng_data->peer_ADRESS : 0; }
void Stäng_nätverk(int filreferens) {
    socket_deltagare_3db661a2 *sträng_data = hämta_värde(filreferens); if (!sträng_data) return;
    if (sträng_data->få_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].Typ_område && 통신끝점들[순번].informationsteknik_väntar == filreferens) Stäng_nätverk(순번);
    if (sträng_data->kontakt_kontroll) {
        tcp_arg(sträng_data->kontakt_kontroll, 0); if (sträng_data->få_port) tcp_accept(sträng_data->kontakt_kontroll, 0); else { tcp_recv(sträng_data->kontakt_kontroll, 0); tcp_err(sträng_data->kontakt_kontroll, 0); }
        if (tcp_close(sträng_data->kontakt_kontroll) != ERR_OK) tcp_abort(sträng_data->kontakt_kontroll);
    }
    if (sträng_data->datagram_kontroll) udp_remove(sträng_data->datagram_kontroll); sträng_data->Typ_område = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || avsökning) return; avsökning = 1;
    if(använda_kabelansluten_nätverk)유선망살피기(&kontakt_enhet);
    for (unsigned budget = 0; !använda_kabelansluten_nätverk && budget < 4096 && (dator_register(보조장치 + 0x54) & 1); budget++) {
        unsigned kodpunkt = dator_register(보조장치 + 0x40) & 255;
        if (kodpunkt == 192) {
            if (få_användning && !få_fel && !수신탈출) {
                struct pbuf *data_placera = pbuf_alloc(PBUF_RAW, få_användning, PBUF_POOL);
                if (data_placera) { BELOPP_datagram_ANTAL++; BELOPP_byte_ANTAL += få_användning; pbuf_take(data_placera, få_databuffert, få_användning); if (kontakt_enhet.input(data_placera, &kontakt_enhet) != ERR_OK) { 버린전문수++; pbuf_free(data_placera); } }
                else 버린전문수++;
            }
            else if (få_användning) 버린전문수++;
            få_användning = få_fel = 수신탈출 = 0;
        } else if (kodpunkt == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kodpunkt != 220 && kodpunkt != 221) få_fel = 1; kodpunkt = kodpunkt == 220 ? 192 : 219; 수신탈출 = 0; }
            if (få_användning < sizeof(få_databuffert)) få_databuffert[få_användning++] = kodpunkt; else få_fel = 1;
        }
    }
    netif_poll(&kontakt_enhet); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budget = 0; budget < 4096 && 송신개수 && (dator_register(보조장치 + 0x54) & 0x20); budget++) {
        dator_register(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    avsökning = 0;
}

/* Inställningar·조회는 lwIP의 verklig_data 인터페이스와 avsluta_peka 표를 사용한다. */
uint32_t läsa_nätverk_status(unsigned post_värde, unsigned INDEX) {
    if(post_värde==20)return använda_kabelansluten_nätverk;
    if(post_värde==21)return 준비됨&&netif_is_link_up(&kontakt_enhet);
    if(post_värde==22)return använda_kabelansluten_nätverk?kabelansluten_nätverk_Statistik(5):0;
    if (!준비됨) return 0;
    if(använda_kabelansluten_nätverk&&post_värde>=4&&post_värde<=8)return kabelansluten_nätverk_Statistik(post_värde-4);
    if (post_värde == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_enhet)));
    if (post_värde == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&kontakt_enhet)));
    if (post_värde == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&kontakt_enhet)));
    if (post_värde == 3) return netif_is_up(&kontakt_enhet) != 0;
    if (post_värde == 4) return BELOPP_datagram_ANTAL;
    if (post_värde == 5) return 보낸전문수;
    if (post_värde == 6) return BELOPP_byte_ANTAL;
    if (post_värde == 7) return 보낸바이트수;
    if (post_värde == 8) return 버린전문수;
    if (post_värde == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    socket_deltagare_3db661a2 *avsluta_peka = &통신끝점들[INDEX];
    if (post_värde == 10) return avsluta_peka->Typ_område;
    if (!avsluta_peka->Typ_område) return 0;
    if (post_värde == 11) return nätverk_portnummer(INDEX);
    if (post_värde == 12) return avsluta_peka->peer_ADRESS;
    if (post_värde == 13) return avsluta_peka->peer_deltagare_nummer;
    if (post_värde == 14) return avsluta_peka->få_port ? 1 : avsluta_peka->fil_avsluta ? 3 : avsluta_peka->fel ? 4 : avsluta_peka->연결됨 ? 2 : 0;
    if (post_värde == 15) return avsluta_peka->post_ANTAL;
    if (post_värde == 16) {
        const ip_addr_t *Adress = avsluta_peka->Typ_område == 1 && avsluta_peka->kontakt_kontroll ? &avsluta_peka->kontakt_kontroll->local_ip :
            avsluta_peka->Typ_område == 2 && avsluta_peka->datagram_kontroll ? &avsluta_peka->datagram_kontroll->local_ip : 0;
        return Adress ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adress))) : 0;
    }
    return 0;
}

int konfigurera_nätverk(unsigned Åtgärd, uint32_t Adress, uint32_t mask_värde, uint32_t gateway_värde) {
    if (!준비됨) return -100;
    if (Åtgärd == 1) { netif_set_up(&kontakt_enhet); return 0; }
    if (Åtgärd == 2) { netif_set_down(&kontakt_enhet); return 0; }
    if (Åtgärd != 0) return -22;
    /* 유니캐스트 IPv4, 연속 mask_värde, 같은 망의 선택적 standardvärde gateway_värde. */
    uint32_t 뒤집은가림 = ~mask_värde;
    if (!mask_värde || (뒤집은가림 & (뒤집은가림 + 1)) || !Adress || (Adress >> 24) == 127 ||
        (Adress >> 24) == 0 || (Adress >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(Adress & 뒤집은가림) || (Adress & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_värde && ((gateway_värde & mask_värde) != (Adress & mask_värde) || gateway_värde == Adress || (gateway_värde >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_värde & 뒤집은가림) || (gateway_värde & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 Adress 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].Typ_område &&
        !(통신끝점들[INDEX].få_port && 통신끝점들[INDEX].kontakt_kontroll && ip_addr_isany(&통신끝점들[INDEX].kontakt_kontroll->local_ip))) return -16;
    if(använda_kabelansluten_nätverk)dhcp_stop(&kontakt_enhet);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(Adress)); ip4_addr_set_u32(&새가림, lwip_htonl(mask_värde)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_värde));
    netif_set_addr(&kontakt_enhet, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *svar_deltagare;
static uint32_t test_ADRESS, test_tid, svarstid;
static unsigned test_SEKVENS, test_identifierare, svar_SEKVENS;
static int svar_status;
static u8_t 응답받음(void *argument, struct raw_pcb *avsluta_peka, struct pbuf *data, const ip_addr_t *Adress) {
    (void)argument; (void)avsluta_peka;
    unsigned char 머리[20], svara[16];
    if (svar_status != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adress))) != test_ADRESS || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned huvud_storlek = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || huvud_storlek < 20 || data->tot_len < huvud_storlek + 16 ||
        pbuf_copy_partial(data, svara, 16, huvud_storlek) != 16 || svara[0] || svara[1] ||
        (((unsigned)svara[4] << 8) | svara[5]) != test_identifierare ||
        (((unsigned)svara[6] << 8) | svara[7]) != test_SEKVENS ||
        svara[8] != 'J' || svara[9] != 'K' || svara[10] != 'O' || svara[11] != 'S' ||
        (((uint32_t)svara[12] << 24) | ((uint32_t)svara[13] << 16) | ((uint32_t)svara[14] << 8) | svara[15]) != test_tid) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, huvud_storlek)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, huvud_storlek); return 0; }
    svarstid = (uint32_t)보드밀리초() - test_tid; svar_SEKVENS = 머리[8]; svar_status = 0;
    pbuf_free(data); return 1;
}
int START_svar_test(uint32_t Adress, unsigned order_värde) {
    if (!준비됨 || !netif_is_up(&kontakt_enhet)) return -100;
    if (!Adress || (Adress >> 28) >= 14 || Adress == 0xffffffffu) return -22;
    if (!svar_deltagare) { svar_deltagare = raw_new(IP_PROTO_ICMP); if (!svar_deltagare) return -12; raw_recv(svar_deltagare, 응답받음, 0); }
    test_ADRESS = Adress; test_SEKVENS = order_värde & 65535; test_identifierare = (test_identifierare + 1) & 65535;
    test_tid = 보드밀리초(); svar_status = -11; svarstid = svar_SEKVENS = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = test_identifierare >> 8; data[5] = test_identifierare; data[6] = test_SEKVENS >> 8; data[7] = test_SEKVENS;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=test_tid >> 24; data[13]=test_tid >> 16; data[14]=test_tid >> 8; data[15]=test_tid;
    for (unsigned positionsindex = 16; positionsindex < sizeof(data); positionsindex++) data[positionsindex] = positionsindex;
    uint16_t verifiering_kontrollsumma = inet_chksum(data, sizeof(data)); memcpy(data + 2, &verifiering_kontrollsumma, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, data, sizeof(data)); ip_addr_t mål_deltagare; ip_addr_set_ip4_u32(&mål_deltagare, lwip_htonl(Adress));
    err_t 처리값 = raw_sendto(svar_deltagare, datagram, &mål_deltagare); pbuf_free(datagram);
    if (처리값) svar_status = felnummer(처리값);
    return 처리값 ? svar_status : 0;
}
int läsa_svar_test(unsigned post_värde) {
    통신망살피기();
    return post_värde == 0 ? svar_status : post_värde == 1 ? (int)svarstid : post_värde == 2 ? (int)svar_SEKVENS : -22;
}
