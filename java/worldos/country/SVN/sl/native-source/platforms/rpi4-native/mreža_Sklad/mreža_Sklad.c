#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "mreža_Sklad.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../oddaljen_VALUE/oddaljen_VALUE.h"
#include "žičen_mreža.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define računalnik_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif povezava_naprava;
static int 준비됨, 살피는중;
static int uporaba_žičen_mreža;
static unsigned sprejeti_sprejemati_prejeti_prejemati_uporaba, 수신탈출, 수신오류;
static unsigned char sprejeti_sprejemati_prejeti_prejemati_podatkovni_medpomnilnik[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_datagram_COUNT, 보낸전문수, RECEIVED_bajt_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int Tip_območje, sprejeti_sprejemati_prejeti_prejemati_vrata, informacijska_tehnologija_čakajoče, 연결됨, Datoteka_končati_klic, NAPAKA;
    struct tcp_pcb *povezava_nadzor;
    struct udp_pcb *datagram_nadzor;
    unsigned sprednja_vnos, vnos_COUNT;
    unsigned char podatki[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], enakovreden_naslov;
} vtičnica_končna_točka_3db661a2;
static vtičnica_končna_točka_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int številka_napake(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static vtičnica_končna_točka_3db661a2 *dobiti_VALUE(int Datoteka_ročica) { return Datoteka_ročica >= 0 && Datoteka_ročica < 32 && 통신끝점들[Datoteka_ročica].Tip_območje ? &통신끝점들[Datoteka_ročica] : 0; }
static int 예약하기(int Tip_območje) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].Tip_območje) {
        memset(&통신끝점들[순번], 0, sizeof(vtičnica_končna_točka_3db661a2)); 통신끝점들[순번].Tip_območje = Tip_območje; 통신끝점들[순번].informacijska_tehnologija_čakajoče = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned koda_znaka) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = koda_znaka; }
static err_t 출력결과(struct netif *element_COUNT, struct pbuf *podatki_položaj, const ip4_addr_t *naslov) {
    (void)element_COUNT; (void)naslov;
    if (podatki_položaj->tot_len > 1500 || 송신개수 + 2 * podatki_položaj->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Naprej_odmik = podatki_položaj; Naprej_odmik; Naprej_odmik = Naprej_odmik->next) for (unsigned 순번 = 0; 순번 < Naprej_odmik->len; 순번++) {
        unsigned koda_znaka = ((unsigned char *)Naprej_odmik->payload)[순번];
        if (koda_znaka == 192 || koda_znaka == 219) { 내보내기(219); 내보내기(koda_znaka == 192 ? 220 : 221); } else 내보내기(koda_znaka);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += podatki_položaj->tot_len; return ERR_OK;
}
static err_t Pripravi_skupni_jezikovni_izvajalnik(struct netif *element_COUNT) { element_COUNT->name[0] = 's'; element_COUNT->name[1] = 'l'; element_COUNT->mtu = 1500; element_COUNT->output = 출력결과; return ERR_OK; }
void Pripravi_mreža(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    računalnik_register(보조장치 + 4) |= 1; računalnik_register(보조장치 + 0x60) = 0; računalnik_register(보조장치 + 0x44) = 0;
    računalnik_register(보조장치 + 0x48) = 0xc6; računalnik_register(보조장치 + 0x4c) = 3; računalnik_register(보조장치 + 0x68) = 270; računalnik_register(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetni_račun, bitna_maska, naslov_prehoda;
    uporaba_žičen_mreža=유선장치있음();
    ip4_addr_set_u32(&internetni_račun, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitna_maska, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&naslov_prehoda, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&povezava_naprava, &internetni_račun, &bitna_maska, &naslov_prehoda, 0, uporaba_žičen_mreža?Pripravi_žičen_mreža:Pripravi_skupni_jezikovni_izvajalnik, uporaba_žičen_mreža?ethernet_input:ip4_input))return;
    netif_set_default(&povezava_naprava); netif_set_up(&povezava_naprava);if(!uporaba_žičen_mreža)netif_set_link_up(&povezava_naprava); 준비됨 = 1;
    Pripravi_oddaljen();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *podatki_položaj, err_t NAPAKA) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = 부가인수; (void)통신제어블록; (void)NAPAKA;
    if (!podatki_položaj) { niz_podatki->Datoteka_končati_klic = 1; return ERR_OK; }
    if (podatki_položaj->tot_len > sizeof(niz_podatki->podatki) - niz_podatki->vnos_COUNT) return ERR_MEM;
    unsigned sprotno_položaj = (niz_podatki->sprednja_vnos + niz_podatki->vnos_COUNT) % sizeof(niz_podatki->podatki);
    for (struct pbuf *Naprej_odmik = podatki_položaj; Naprej_odmik; Naprej_odmik = Naprej_odmik->next) for (unsigned 순번 = 0; 순번 < Naprej_odmik->len; 순번++) {
        niz_podatki->podatki[sprotno_položaj] = ((unsigned char *)Naprej_odmik->payload)[순번]; sprotno_položaj = (sprotno_položaj + 1) % sizeof(niz_podatki->podatki);
    }
    niz_podatki->vnos_COUNT += podatki_položaj->tot_len; pbuf_free(podatki_položaj); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t NAPAKA) { vtičnica_končna_točka_3db661a2 *niz_podatki = 부가인수; niz_podatki->povezava_nadzor = 0; niz_podatki->NAPAKA = številka_napake(NAPAKA); }
static void 되부름목록(vtičnica_končna_točka_3db661a2 *niz_podatki) { tcp_arg(niz_podatki->povezava_nadzor, niz_podatki); tcp_recv(niz_podatki->povezava_nadzor, 수신됨); tcp_err(niz_podatki->povezava_nadzor, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t NAPAKA) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = 부가인수; (void)통신제어블록; if (NAPAKA) niz_podatki->NAPAKA = številka_napake(NAPAKA); else niz_podatki->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t NAPAKA) {
    vtičnica_končna_točka_3db661a2 *nadrejen = 부가인수; if (NAPAKA) return NAPAKA;
    int Datoteka_ročica = 예약하기(1); if (Datoteka_ročica < 0) return ERR_MEM;
    vtičnica_končna_točka_3db661a2 *niz_podatki = &통신끝점들[Datoteka_ročica]; niz_podatki->povezava_nadzor = 통신제어블록; niz_podatki->연결됨 = 1; niz_podatki->informacijska_tehnologija_čakajoče = (int)(nadrejen - 통신끝점들);
    niz_podatki->enakovreden_naslov = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); niz_podatki->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(niz_podatki); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *podatki_položaj, const ip_addr_t *naslov, u16_t številka_vrat) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = 부가인수; (void)통신제어블록;
    if (niz_podatki->vnos_COUNT < 4 && podatki_položaj->tot_len <= 512) {
        unsigned kazalec_mesta = (niz_podatki->sprednja_vnos + niz_podatki->vnos_COUNT) % 4;
        pbuf_copy_partial(podatki_položaj, niz_podatki->podatki + kazalec_mesta * 512, podatki_položaj->tot_len, 0);
        niz_podatki->길이목록[kazalec_mesta] = podatki_položaj->tot_len; niz_podatki->접속번호들[kazalec_mesta] = številka_vrat;
        niz_podatki->주소목록[kazalec_mesta] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(naslov))); niz_podatki->vnos_COUNT++;
    }
    pbuf_free(podatki_položaj);
}
int Ustvari_vtičnica_končna_točka(int Tip_območje) {
    if (!준비됨) return -100;
    if (Tip_območje != 1 && Tip_območje != 2) return -93;
    int Datoteka_ročica = 예약하기(Tip_območje); if (Datoteka_ročica < 0) return Datoteka_ročica;
    vtičnica_končna_točka_3db661a2 *niz_podatki = &통신끝점들[Datoteka_ročica];
    if (Tip_območje == 1) { niz_podatki->povezava_nadzor = tcp_new(); if (niz_podatki->povezava_nadzor) 되부름목록(niz_podatki); }
    else { niz_podatki->datagram_nadzor = udp_new(); if (niz_podatki->datagram_nadzor) udp_recv(niz_podatki->datagram_nadzor, datagram, niz_podatki); }
    if (!niz_podatki->povezava_nadzor && !niz_podatki->datagram_nadzor) { niz_podatki->Tip_območje = 0; return -12; } return Datoteka_ročica;
}
int NET_BIND(int Datoteka_ročica, uint32_t naslov, unsigned številka_vrat) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki) return -9;
    if (številka_vrat > 65535 || (naslov && naslov != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&povezava_naprava))) && naslov != 0x7f000001)) return -99;
    ip_addr_t internetni_račun; ip_addr_set_ip4_u32(&internetni_račun, lwip_htonl(naslov));
    err_t 보조항목 = niz_podatki->Tip_območje == 1 ? tcp_bind(niz_podatki->povezava_nadzor, &internetni_račun, številka_vrat) : udp_bind(niz_podatki->datagram_nadzor, &internetni_račun, številka_vrat); return 보조항목 ? številka_napake(보조항목) : 0;
}
void 통신주소재사용(int Datoteka_ročica) { vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (niz_podatki && niz_podatki->povezava_nadzor) ip_set_option(niz_podatki->povezava_nadzor, SOF_REUSEADDR); }
int NET_poslušati(int Datoteka_ročica) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki || niz_podatki->Tip_območje != 1) return -9;
    if (niz_podatki->sprejeti_sprejemati_prejeti_prejemati_vrata) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(niz_podatki->povezava_nadzor, 4, &보조항목);
    if (!통신제어블록) return številka_napake(보조항목); niz_podatki->povezava_nadzor = 통신제어블록; niz_podatki->sprejeti_sprejemati_prejeti_prejemati_vrata = 1; tcp_arg(통신제어블록, niz_podatki); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_POVEŽI(int Datoteka_ročica, uint32_t naslov, unsigned številka_vrat) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki || niz_podatki->Tip_območje != 1) return -9;
    if (niz_podatki->NAPAKA) return niz_podatki->NAPAKA;
    if (niz_podatki->연결됨) return 0;
    if (niz_podatki->상대창구번호) return -115;
    if (!številka_vrat || številka_vrat > 65535 || !naslov) return -22;
    ip_addr_t internetni_račun; ip_addr_set_ip4_u32(&internetni_račun, lwip_htonl(naslov));
    niz_podatki->enakovreden_naslov = naslov; niz_podatki->상대창구번호 = številka_vrat;
    err_t 보조항목 = tcp_connect(niz_podatki->povezava_nadzor, &internetni_račun, številka_vrat, 연결됨); return 보조항목 ? številka_napake(보조항목) : -115;
}
int NET_sprejeti(int Datoteka_ročica) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki || !niz_podatki->sprejeti_sprejemati_prejeti_prejemati_vrata) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].Tip_območje == 1 && 통신끝점들[순번].informacijska_tehnologija_čakajoče == Datoteka_ročica) { 통신끝점들[순번].informacijska_tehnologija_čakajoče = -1; return 순번; }
    return -11;
}
int 통신읽기(int Datoteka_ročica, void *podatki, unsigned element_COUNT) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki || niz_podatki->Tip_območje != 1) return -9;
    if (!element_COUNT) return 0; if (!niz_podatki->vnos_COUNT) return niz_podatki->NAPAKA ? niz_podatki->NAPAKA : niz_podatki->Datoteka_končati_klic ? 0 : -11;
    if (element_COUNT > niz_podatki->vnos_COUNT) element_COUNT = niz_podatki->vnos_COUNT;
    for (unsigned 순번 = 0; 순번 < element_COUNT; 순번++) { ((unsigned char *)podatki)[순번] = niz_podatki->podatki[niz_podatki->sprednja_vnos]; niz_podatki->sprednja_vnos = (niz_podatki->sprednja_vnos + 1) % sizeof(niz_podatki->podatki); }
    niz_podatki->vnos_COUNT -= element_COUNT; if (niz_podatki->povezava_nadzor) tcp_recved(niz_podatki->povezava_nadzor, element_COUNT); return element_COUNT;
}
int NET_pisati(int Datoteka_ročica, const void *podatki, unsigned element_COUNT) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki || niz_podatki->Tip_območje != 1) return -9;
    if (niz_podatki->NAPAKA) return niz_podatki->NAPAKA; if (!niz_podatki->povezava_nadzor || !niz_podatki->연결됨) return -107;
    if (!element_COUNT) return 0; if (element_COUNT > tcp_sndbuf(niz_podatki->povezava_nadzor)) element_COUNT = tcp_sndbuf(niz_podatki->povezava_nadzor);
    if (!element_COUNT) return -11; if (element_COUNT > 1024) element_COUNT = 1024;
    err_t 보조항목 = tcp_write(niz_podatki->povezava_nadzor, podatki, element_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return številka_napake(보조항목);
    tcp_output(niz_podatki->povezava_nadzor); return element_COUNT;
}
int poslati_datagram(int Datoteka_ročica, const void *podatki, unsigned element_COUNT, uint32_t naslov, unsigned številka_vrat) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki || niz_podatki->Tip_območje != 2) return -9;
    if (element_COUNT > 512) return -90; if (!številka_vrat || številka_vrat > 65535) return -22;
    struct pbuf *podatki_položaj = pbuf_alloc(PBUF_TRANSPORT, element_COUNT, PBUF_RAM); if (!podatki_položaj) return -11;
    pbuf_take(podatki_položaj, podatki, element_COUNT); ip_addr_t internetni_račun; ip_addr_set_ip4_u32(&internetni_račun, lwip_htonl(naslov));
    err_t 보조항목 = udp_sendto(niz_podatki->datagram_nadzor, podatki_položaj, &internetni_račun, številka_vrat); pbuf_free(podatki_položaj); return 보조항목 ? številka_napake(보조항목) : (int)element_COUNT;
}
int sprejeti_sprejemati_prejeti_prejemati_datagram(int Datoteka_ročica, void *podatki, unsigned element_COUNT) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki || niz_podatki->Tip_območje != 2) return -9;
    if (!niz_podatki->vnos_COUNT) return -11; unsigned sprotno_položaj = niz_podatki->sprednja_vnos;
    if (element_COUNT > niz_podatki->길이목록[sprotno_položaj]) element_COUNT = niz_podatki->길이목록[sprotno_položaj]; memcpy(podatki, niz_podatki->podatki + sprotno_položaj * 512, element_COUNT);
    niz_podatki->상대창구번호 = niz_podatki->접속번호들[sprotno_položaj]; niz_podatki->enakovreden_naslov = niz_podatki->주소목록[sprotno_položaj]; niz_podatki->sprednja_vnos = (sprotno_položaj + 1) % 4; niz_podatki->vnos_COUNT--; return element_COUNT;
}
unsigned mreža_številka_vrat(int Datoteka_ročica) { vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); return !niz_podatki ? 0 : niz_podatki->povezava_nadzor ? niz_podatki->povezava_nadzor->local_port : niz_podatki->datagram_nadzor ? niz_podatki->datagram_nadzor->local_port : 0; }
unsigned enakovreden_številka_vrat(int Datoteka_ročica) { vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); return niz_podatki ? niz_podatki->상대창구번호 : 0; }
uint32_t NET_enakovreden_naslov(int Datoteka_ročica) { vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); return niz_podatki ? niz_podatki->enakovreden_naslov : 0; }
void Zapri_mreža(int Datoteka_ročica) {
    vtičnica_končna_točka_3db661a2 *niz_podatki = dobiti_VALUE(Datoteka_ročica); if (!niz_podatki) return;
    if (niz_podatki->sprejeti_sprejemati_prejeti_prejemati_vrata) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].Tip_območje && 통신끝점들[순번].informacijska_tehnologija_čakajoče == Datoteka_ročica) Zapri_mreža(순번);
    if (niz_podatki->povezava_nadzor) {
        tcp_arg(niz_podatki->povezava_nadzor, 0); if (niz_podatki->sprejeti_sprejemati_prejeti_prejemati_vrata) tcp_accept(niz_podatki->povezava_nadzor, 0); else { tcp_recv(niz_podatki->povezava_nadzor, 0); tcp_err(niz_podatki->povezava_nadzor, 0); }
        if (tcp_close(niz_podatki->povezava_nadzor) != ERR_OK) tcp_abort(niz_podatki->povezava_nadzor);
    }
    if (niz_podatki->datagram_nadzor) udp_remove(niz_podatki->datagram_nadzor); niz_podatki->Tip_območje = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(uporaba_žičen_mreža)유선망살피기(&povezava_naprava);
    for (unsigned proračun = 0; !uporaba_žičen_mreža && proračun < 4096 && (računalnik_register(보조장치 + 0x54) & 1); proračun++) {
        unsigned koda_znaka = računalnik_register(보조장치 + 0x40) & 255;
        if (koda_znaka == 192) {
            if (sprejeti_sprejemati_prejeti_prejemati_uporaba && !수신오류 && !수신탈출) {
                struct pbuf *podatki_položaj = pbuf_alloc(PBUF_RAW, sprejeti_sprejemati_prejeti_prejemati_uporaba, PBUF_POOL);
                if (podatki_položaj) { RECEIVED_datagram_COUNT++; RECEIVED_bajt_COUNT += sprejeti_sprejemati_prejeti_prejemati_uporaba; pbuf_take(podatki_položaj, sprejeti_sprejemati_prejeti_prejemati_podatkovni_medpomnilnik, sprejeti_sprejemati_prejeti_prejemati_uporaba); if (povezava_naprava.input(podatki_položaj, &povezava_naprava) != ERR_OK) { 버린전문수++; pbuf_free(podatki_položaj); } }
                else 버린전문수++;
            }
            else if (sprejeti_sprejemati_prejeti_prejemati_uporaba) 버린전문수++;
            sprejeti_sprejemati_prejeti_prejemati_uporaba = 수신오류 = 수신탈출 = 0;
        } else if (koda_znaka == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (koda_znaka != 220 && koda_znaka != 221) 수신오류 = 1; koda_znaka = koda_znaka == 220 ? 192 : 219; 수신탈출 = 0; }
            if (sprejeti_sprejemati_prejeti_prejemati_uporaba < sizeof(sprejeti_sprejemati_prejeti_prejemati_podatkovni_medpomnilnik)) sprejeti_sprejemati_prejeti_prejemati_podatkovni_medpomnilnik[sprejeti_sprejemati_prejeti_prejemati_uporaba++] = koda_znaka; else 수신오류 = 1;
        }
    }
    netif_poll(&povezava_naprava); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned proračun = 0; proračun < 4096 && 송신개수 && (računalnik_register(보조장치 + 0x54) & 0x20); proračun++) {
        računalnik_register(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Nastavitve·조회는 lwIP의 dejanski_podatki 인터페이스와 končati_klic_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned vnos_VALUE, unsigned INDEX) {
    if(vnos_VALUE==20)return uporaba_žičen_mreža;
    if(vnos_VALUE==21)return 준비됨&&netif_is_link_up(&povezava_naprava);
    if(vnos_VALUE==22)return uporaba_žičen_mreža?유선망집계(5):0;
    if (!준비됨) return 0;
    if(uporaba_žičen_mreža&&vnos_VALUE>=4&&vnos_VALUE<=8)return 유선망집계(vnos_VALUE-4);
    if (vnos_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&povezava_naprava)));
    if (vnos_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&povezava_naprava)));
    if (vnos_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&povezava_naprava)));
    if (vnos_VALUE == 3) return netif_is_up(&povezava_naprava) != 0;
    if (vnos_VALUE == 4) return RECEIVED_datagram_COUNT;
    if (vnos_VALUE == 5) return 보낸전문수;
    if (vnos_VALUE == 6) return RECEIVED_bajt_COUNT;
    if (vnos_VALUE == 7) return 보낸바이트수;
    if (vnos_VALUE == 8) return 버린전문수;
    if (vnos_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    vtičnica_končna_točka_3db661a2 *končati_klic_p = &통신끝점들[INDEX];
    if (vnos_VALUE == 10) return končati_klic_p->Tip_območje;
    if (!končati_klic_p->Tip_območje) return 0;
    if (vnos_VALUE == 11) return mreža_številka_vrat(INDEX);
    if (vnos_VALUE == 12) return končati_klic_p->enakovreden_naslov;
    if (vnos_VALUE == 13) return končati_klic_p->상대창구번호;
    if (vnos_VALUE == 14) return končati_klic_p->sprejeti_sprejemati_prejeti_prejemati_vrata ? 1 : končati_klic_p->Datoteka_končati_klic ? 3 : končati_klic_p->NAPAKA ? 4 : končati_klic_p->연결됨 ? 2 : 0;
    if (vnos_VALUE == 15) return končati_klic_p->vnos_COUNT;
    if (vnos_VALUE == 16) {
        const ip_addr_t *naslov = končati_klic_p->Tip_območje == 1 && končati_klic_p->povezava_nadzor ? &končati_klic_p->povezava_nadzor->local_ip :
            končati_klic_p->Tip_območje == 2 && končati_klic_p->datagram_nadzor ? &končati_klic_p->datagram_nadzor->local_ip : 0;
        return naslov ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(naslov))) : 0;
    }
    return 0;
}

int konfigurirati_mreža(unsigned Dejanje, uint32_t naslov, uint32_t maska_VALUE, uint32_t prehod_VALUE) {
    if (!준비됨) return -100;
    if (Dejanje == 1) { netif_set_up(&povezava_naprava); return 0; }
    if (Dejanje == 2) { netif_set_down(&povezava_naprava); return 0; }
    if (Dejanje != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_VALUE, 같은 망의 선택적 privzeta_vrednost prehod_VALUE. */
    uint32_t 뒤집은가림 = ~maska_VALUE;
    if (!maska_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !naslov || (naslov >> 24) == 127 ||
        (naslov >> 24) == 0 || (naslov >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(naslov & 뒤집은가림) || (naslov & 뒤집은가림) == 뒤집은가림)) ||
        (prehod_VALUE && ((prehod_VALUE & maska_VALUE) != (naslov & maska_VALUE) || prehod_VALUE == naslov || (prehod_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(prehod_VALUE & 뒤집은가림) || (prehod_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 naslov 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].Tip_območje &&
        !(통신끝점들[INDEX].sprejeti_sprejemati_prejeti_prejemati_vrata && 통신끝점들[INDEX].povezava_nadzor && ip_addr_isany(&통신끝점들[INDEX].povezava_nadzor->local_ip))) return -16;
    if(uporaba_žičen_mreža)dhcp_stop(&povezava_naprava);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(naslov)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(prehod_VALUE));
    netif_set_addr(&povezava_naprava, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *odziv_končna_točka;
static uint32_t preskusiti_naslov, preskusiti_čas, odzivni_čas;
static unsigned preskusiti_SEQUENCE, preskusiti_identifikator, odziv_SEQUENCE;
static int odziv_stanje;
static u8_t 응답받음(void *Argumenti, struct raw_pcb *končati_klic_p, struct pbuf *podatki, const ip_addr_t *naslov) {
    (void)Argumenti; (void)končati_klic_p;
    unsigned char 머리[20], odgovor[16];
    if (odziv_stanje != -11 || podatki->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(naslov))) != preskusiti_naslov || pbuf_copy_partial(podatki, 머리, 20, 0) != 20) return 0;
    unsigned Glava_spremeniti_velikost = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Glava_spremeniti_velikost < 20 || podatki->tot_len < Glava_spremeniti_velikost + 16 ||
        pbuf_copy_partial(podatki, odgovor, 16, Glava_spremeniti_velikost) != 16 || odgovor[0] || odgovor[1] ||
        (((unsigned)odgovor[4] << 8) | odgovor[5]) != preskusiti_identifikator ||
        (((unsigned)odgovor[6] << 8) | odgovor[7]) != preskusiti_SEQUENCE ||
        odgovor[8] != 'J' || odgovor[9] != 'K' || odgovor[10] != 'O' || odgovor[11] != 'S' ||
        (((uint32_t)odgovor[12] << 24) | ((uint32_t)odgovor[13] << 16) | ((uint32_t)odgovor[14] << 8) | odgovor[15]) != preskusiti_čas) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(podatki, Glava_spremeniti_velikost)) return 0;
    if (inet_chksum_pbuf(podatki)) { pbuf_add_header(podatki, Glava_spremeniti_velikost); return 0; }
    odzivni_čas = (uint32_t)보드밀리초() - preskusiti_čas; odziv_SEQUENCE = 머리[8]; odziv_stanje = 0;
    pbuf_free(podatki); return 1;
}
int Start_odziv_preskusiti(uint32_t naslov, unsigned naročilo_VALUE) {
    if (!준비됨 || !netif_is_up(&povezava_naprava)) return -100;
    if (!naslov || (naslov >> 28) >= 14 || naslov == 0xffffffffu) return -22;
    if (!odziv_končna_točka) { odziv_končna_točka = raw_new(IP_PROTO_ICMP); if (!odziv_končna_točka) return -12; raw_recv(odziv_končna_točka, 응답받음, 0); }
    preskusiti_naslov = naslov; preskusiti_SEQUENCE = naročilo_VALUE & 65535; preskusiti_identifikator = (preskusiti_identifikator + 1) & 65535;
    preskusiti_čas = 보드밀리초(); odziv_stanje = -11; odzivni_čas = odziv_SEQUENCE = 0;
    unsigned char podatki[32] = {8,0,0,0};
    podatki[4] = preskusiti_identifikator >> 8; podatki[5] = preskusiti_identifikator; podatki[6] = preskusiti_SEQUENCE >> 8; podatki[7] = preskusiti_SEQUENCE;
    podatki[8]='J'; podatki[9]='K'; podatki[10]='O'; podatki[11]='S';
    podatki[12]=preskusiti_čas >> 24; podatki[13]=preskusiti_čas >> 16; podatki[14]=preskusiti_čas >> 8; podatki[15]=preskusiti_čas;
    for (unsigned kazalec_mesta = 16; kazalec_mesta < sizeof(podatki); kazalec_mesta++) podatki[kazalec_mesta] = kazalec_mesta;
    uint16_t preverjanje_kontrolna_vsota = inet_chksum(podatki, sizeof(podatki)); memcpy(podatki + 2, &preverjanje_kontrolna_vsota, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(podatki), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, podatki, sizeof(podatki)); ip_addr_t cilj_končna_točka; ip_addr_set_ip4_u32(&cilj_končna_točka, lwip_htonl(naslov));
    err_t 처리값 = raw_sendto(odziv_končna_točka, datagram, &cilj_končna_točka); pbuf_free(datagram);
    if (처리값) odziv_stanje = številka_napake(처리값);
    return 처리값 ? odziv_stanje : 0;
}
int 응답시험읽기(unsigned vnos_VALUE) {
    통신망살피기();
    return vnos_VALUE == 0 ? odziv_stanje : vnos_VALUE == 1 ? (int)odzivni_čas : vnos_VALUE == 2 ? (int)odziv_SEQUENCE : -22;
}
