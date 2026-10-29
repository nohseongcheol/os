#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "mreža_hrpa.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../udaljeno_VALUE/udaljeno_VALUE.h"
#include "ožičen_mreža.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define stroj_registar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif veza_uređaj;
static int 준비됨, prozivanje;
static int uporaba_ožičen_mreža;
static unsigned primiti_iskorištenost, 수신탈출, primiti_pogreška;
static unsigned char primiti_međuspremnik_podataka[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_datogram_COUNT, 보낸전문수, RECEIVED_bajt_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_područje, primiti_prebaciti, odjel_informacijske_tehnologije_na_čekanju, 연결됨, Datoteka_završiti_razgovor, GREŠKA;
    struct tcp_pcb *veza_kontrola;
    struct udp_pcb *datogram_kontrola;
    unsigned prednja_unos, unos_COUNT;
    unsigned char podaci[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], ravnopravan_član_adresa;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int broj_pogreške(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *dohvatiti_VALUE(int Datoteka_ustroj) { return Datoteka_ustroj >= 0 && Datoteka_ustroj < 32 && 통신끝점들[Datoteka_ustroj].TYPE_područje ? &통신끝점들[Datoteka_ustroj] : 0; }
static int 예약하기(int TYPE_područje) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_područje) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_područje = TYPE_područje; 통신끝점들[순번].odjel_informacijske_tehnologije_na_čekanju = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kodna_točka) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kodna_točka; }
static err_t 출력결과(struct netif *artikl_COUNT, struct pbuf *podaci_položaj, const ip4_addr_t *adresa) {
    (void)artikl_COUNT; (void)adresa;
    if (podaci_položaj->tot_len > 1500 || 송신개수 + 2 * podaci_položaj->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Dalje_pomak = podaci_položaj; Dalje_pomak; Dalje_pomak = Dalje_pomak->next) for (unsigned 순번 = 0; 순번 < Dalje_pomak->len; 순번++) {
        unsigned kodna_točka = ((unsigned char *)Dalje_pomak->payload)[순번];
        if (kodna_točka == 192 || kodna_točka == 219) { 내보내기(219); 내보내기(kodna_točka == 192 ? 220 : 221); } else 내보내기(kodna_točka);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += podaci_položaj->tot_len; return ERR_OK;
}
static err_t Pripremi_CLR(struct netif *artikl_COUNT) { artikl_COUNT->name[0] = 's'; artikl_COUNT->name[1] = 'l'; artikl_COUNT->mtu = 1500; artikl_COUNT->output = 출력결과; return ERR_OK; }
void Pripremi_mreža(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    stroj_registar(보조장치 + 4) |= 1; stroj_registar(보조장치 + 0x60) = 0; stroj_registar(보조장치 + 0x44) = 0;
    stroj_registar(보조장치 + 0x48) = 0xc6; stroj_registar(보조장치 + 0x4c) = 3; stroj_registar(보조장치 + 0x68) = 270; stroj_registar(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetska_adresa, bit_maska, pristupna_adresa;
    uporaba_ožičen_mreža=유선장치있음();
    ip4_addr_set_u32(&internetska_adresa, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_maska, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&pristupna_adresa, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&veza_uređaj, &internetska_adresa, &bit_maska, &pristupna_adresa, 0, uporaba_ožičen_mreža?Pripremi_ožičen_mreža:Pripremi_CLR, uporaba_ožičen_mreža?ethernet_input:ip4_input))return;
    netif_set_default(&veza_uređaj); netif_set_up(&veza_uređaj);if(!uporaba_ožičen_mreža)netif_set_link_up(&veza_uređaj); 준비됨 = 1;
    Pripremi_udaljeno();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *podaci_položaj, err_t GREŠKA) {
    통신끝점 *niz_podaci = 부가인수; (void)통신제어블록; (void)GREŠKA;
    if (!podaci_položaj) { niz_podaci->Datoteka_završiti_razgovor = 1; return ERR_OK; }
    if (podaci_položaj->tot_len > sizeof(niz_podaci->podaci) - niz_podaci->unos_COUNT) return ERR_MEM;
    unsigned redovno_položaj = (niz_podaci->prednja_unos + niz_podaci->unos_COUNT) % sizeof(niz_podaci->podaci);
    for (struct pbuf *Dalje_pomak = podaci_položaj; Dalje_pomak; Dalje_pomak = Dalje_pomak->next) for (unsigned 순번 = 0; 순번 < Dalje_pomak->len; 순번++) {
        niz_podaci->podaci[redovno_položaj] = ((unsigned char *)Dalje_pomak->payload)[순번]; redovno_položaj = (redovno_položaj + 1) % sizeof(niz_podaci->podaci);
    }
    niz_podaci->unos_COUNT += podaci_položaj->tot_len; pbuf_free(podaci_položaj); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t GREŠKA) { 통신끝점 *niz_podaci = 부가인수; niz_podaci->veza_kontrola = 0; niz_podaci->GREŠKA = broj_pogreške(GREŠKA); }
static void 되부름목록(통신끝점 *niz_podaci) { tcp_arg(niz_podaci->veza_kontrola, niz_podaci); tcp_recv(niz_podaci->veza_kontrola, 수신됨); tcp_err(niz_podaci->veza_kontrola, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t GREŠKA) {
    통신끝점 *niz_podaci = 부가인수; (void)통신제어블록; if (GREŠKA) niz_podaci->GREŠKA = broj_pogreške(GREŠKA); else niz_podaci->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t GREŠKA) {
    통신끝점 *roditeljski = 부가인수; if (GREŠKA) return GREŠKA;
    int Datoteka_ustroj = 예약하기(1); if (Datoteka_ustroj < 0) return ERR_MEM;
    통신끝점 *niz_podaci = &통신끝점들[Datoteka_ustroj]; niz_podaci->veza_kontrola = 통신제어블록; niz_podaci->연결됨 = 1; niz_podaci->odjel_informacijske_tehnologije_na_čekanju = (int)(roditeljski - 통신끝점들);
    niz_podaci->ravnopravan_član_adresa = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); niz_podaci->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(niz_podaci); return ERR_OK;
}
static void datogram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *podaci_položaj, const ip_addr_t *adresa, u16_t broj_priključka) {
    통신끝점 *niz_podaci = 부가인수; (void)통신제어블록;
    if (niz_podaci->unos_COUNT < 4 && podaci_položaj->tot_len <= 512) {
        unsigned indeks_položaja = (niz_podaci->prednja_unos + niz_podaci->unos_COUNT) % 4;
        pbuf_copy_partial(podaci_položaj, niz_podaci->podaci + indeks_položaja * 512, podaci_položaj->tot_len, 0);
        niz_podaci->길이목록[indeks_položaja] = podaci_položaj->tot_len; niz_podaci->접속번호들[indeks_položaja] = broj_priključka;
        niz_podaci->주소목록[indeks_položaja] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))); niz_podaci->unos_COUNT++;
    }
    pbuf_free(podaci_položaj);
}
int 통신끝점만들기(int TYPE_područje) {
    if (!준비됨) return -100;
    if (TYPE_područje != 1 && TYPE_područje != 2) return -93;
    int Datoteka_ustroj = 예약하기(TYPE_područje); if (Datoteka_ustroj < 0) return Datoteka_ustroj;
    통신끝점 *niz_podaci = &통신끝점들[Datoteka_ustroj];
    if (TYPE_područje == 1) { niz_podaci->veza_kontrola = tcp_new(); if (niz_podaci->veza_kontrola) 되부름목록(niz_podaci); }
    else { niz_podaci->datogram_kontrola = udp_new(); if (niz_podaci->datogram_kontrola) udp_recv(niz_podaci->datogram_kontrola, datogram, niz_podaci); }
    if (!niz_podaci->veza_kontrola && !niz_podaci->datogram_kontrola) { niz_podaci->TYPE_područje = 0; return -12; } return Datoteka_ustroj;
}
int NET_BIND(int Datoteka_ustroj, uint32_t adresa, unsigned broj_priključka) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci) return -9;
    if (broj_priključka > 65535 || (adresa && adresa != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&veza_uređaj))) && adresa != 0x7f000001)) return -99;
    ip_addr_t internetska_adresa; ip_addr_set_ip4_u32(&internetska_adresa, lwip_htonl(adresa));
    err_t 보조항목 = niz_podaci->TYPE_područje == 1 ? tcp_bind(niz_podaci->veza_kontrola, &internetska_adresa, broj_priključka) : udp_bind(niz_podaci->datogram_kontrola, &internetska_adresa, broj_priključka); return 보조항목 ? broj_pogreške(보조항목) : 0;
}
void 통신주소재사용(int Datoteka_ustroj) { 통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (niz_podaci && niz_podaci->veza_kontrola) ip_set_option(niz_podaci->veza_kontrola, SOF_REUSEADDR); }
int NET_osluškivati(int Datoteka_ustroj) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci || niz_podaci->TYPE_područje != 1) return -9;
    if (niz_podaci->primiti_prebaciti) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(niz_podaci->veza_kontrola, 4, &보조항목);
    if (!통신제어블록) return broj_pogreške(보조항목); niz_podaci->veza_kontrola = 통신제어블록; niz_podaci->primiti_prebaciti = 1; tcp_arg(통신제어블록, niz_podaci); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_CONNECT(int Datoteka_ustroj, uint32_t adresa, unsigned broj_priključka) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci || niz_podaci->TYPE_područje != 1) return -9;
    if (niz_podaci->GREŠKA) return niz_podaci->GREŠKA;
    if (niz_podaci->연결됨) return 0;
    if (niz_podaci->상대창구번호) return -115;
    if (!broj_priključka || broj_priključka > 65535 || !adresa) return -22;
    ip_addr_t internetska_adresa; ip_addr_set_ip4_u32(&internetska_adresa, lwip_htonl(adresa));
    niz_podaci->ravnopravan_član_adresa = adresa; niz_podaci->상대창구번호 = broj_priključka;
    err_t 보조항목 = tcp_connect(niz_podaci->veza_kontrola, &internetska_adresa, broj_priključka, 연결됨); return 보조항목 ? broj_pogreške(보조항목) : -115;
}
int NET_prihvatiti(int Datoteka_ustroj) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci || !niz_podaci->primiti_prebaciti) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_područje == 1 && 통신끝점들[순번].odjel_informacijske_tehnologije_na_čekanju == Datoteka_ustroj) { 통신끝점들[순번].odjel_informacijske_tehnologije_na_čekanju = -1; return 순번; }
    return -11;
}
int 통신읽기(int Datoteka_ustroj, void *podaci, unsigned artikl_COUNT) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci || niz_podaci->TYPE_područje != 1) return -9;
    if (!artikl_COUNT) return 0; if (!niz_podaci->unos_COUNT) return niz_podaci->GREŠKA ? niz_podaci->GREŠKA : niz_podaci->Datoteka_završiti_razgovor ? 0 : -11;
    if (artikl_COUNT > niz_podaci->unos_COUNT) artikl_COUNT = niz_podaci->unos_COUNT;
    for (unsigned 순번 = 0; 순번 < artikl_COUNT; 순번++) { ((unsigned char *)podaci)[순번] = niz_podaci->podaci[niz_podaci->prednja_unos]; niz_podaci->prednja_unos = (niz_podaci->prednja_unos + 1) % sizeof(niz_podaci->podaci); }
    niz_podaci->unos_COUNT -= artikl_COUNT; if (niz_podaci->veza_kontrola) tcp_recved(niz_podaci->veza_kontrola, artikl_COUNT); return artikl_COUNT;
}
int NET_zapisivanje(int Datoteka_ustroj, const void *podaci, unsigned artikl_COUNT) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci || niz_podaci->TYPE_područje != 1) return -9;
    if (niz_podaci->GREŠKA) return niz_podaci->GREŠKA; if (!niz_podaci->veza_kontrola || !niz_podaci->연결됨) return -107;
    if (!artikl_COUNT) return 0; if (artikl_COUNT > tcp_sndbuf(niz_podaci->veza_kontrola)) artikl_COUNT = tcp_sndbuf(niz_podaci->veza_kontrola);
    if (!artikl_COUNT) return -11; if (artikl_COUNT > 1024) artikl_COUNT = 1024;
    err_t 보조항목 = tcp_write(niz_podaci->veza_kontrola, podaci, artikl_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return broj_pogreške(보조항목);
    tcp_output(niz_podaci->veza_kontrola); return artikl_COUNT;
}
int slati_datogram(int Datoteka_ustroj, const void *podaci, unsigned artikl_COUNT, uint32_t adresa, unsigned broj_priključka) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci || niz_podaci->TYPE_područje != 2) return -9;
    if (artikl_COUNT > 512) return -90; if (!broj_priključka || broj_priključka > 65535) return -22;
    struct pbuf *podaci_položaj = pbuf_alloc(PBUF_TRANSPORT, artikl_COUNT, PBUF_RAM); if (!podaci_položaj) return -11;
    pbuf_take(podaci_položaj, podaci, artikl_COUNT); ip_addr_t internetska_adresa; ip_addr_set_ip4_u32(&internetska_adresa, lwip_htonl(adresa));
    err_t 보조항목 = udp_sendto(niz_podaci->datogram_kontrola, podaci_položaj, &internetska_adresa, broj_priključka); pbuf_free(podaci_položaj); return 보조항목 ? broj_pogreške(보조항목) : (int)artikl_COUNT;
}
int primiti_datogram(int Datoteka_ustroj, void *podaci, unsigned artikl_COUNT) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci || niz_podaci->TYPE_područje != 2) return -9;
    if (!niz_podaci->unos_COUNT) return -11; unsigned redovno_položaj = niz_podaci->prednja_unos;
    if (artikl_COUNT > niz_podaci->길이목록[redovno_položaj]) artikl_COUNT = niz_podaci->길이목록[redovno_položaj]; memcpy(podaci, niz_podaci->podaci + redovno_položaj * 512, artikl_COUNT);
    niz_podaci->상대창구번호 = niz_podaci->접속번호들[redovno_položaj]; niz_podaci->ravnopravan_član_adresa = niz_podaci->주소목록[redovno_položaj]; niz_podaci->prednja_unos = (redovno_položaj + 1) % 4; niz_podaci->unos_COUNT--; return artikl_COUNT;
}
unsigned mreža_broj_priključka(int Datoteka_ustroj) { 통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); return !niz_podaci ? 0 : niz_podaci->veza_kontrola ? niz_podaci->veza_kontrola->local_port : niz_podaci->datogram_kontrola ? niz_podaci->datogram_kontrola->local_port : 0; }
unsigned ravnopravan_član_broj_priključka(int Datoteka_ustroj) { 통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); return niz_podaci ? niz_podaci->상대창구번호 : 0; }
uint32_t NET_ravnopravan_član_adresa(int Datoteka_ustroj) { 통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); return niz_podaci ? niz_podaci->ravnopravan_član_adresa : 0; }
void Zatvori_mreža(int Datoteka_ustroj) {
    통신끝점 *niz_podaci = dohvatiti_VALUE(Datoteka_ustroj); if (!niz_podaci) return;
    if (niz_podaci->primiti_prebaciti) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_područje && 통신끝점들[순번].odjel_informacijske_tehnologije_na_čekanju == Datoteka_ustroj) Zatvori_mreža(순번);
    if (niz_podaci->veza_kontrola) {
        tcp_arg(niz_podaci->veza_kontrola, 0); if (niz_podaci->primiti_prebaciti) tcp_accept(niz_podaci->veza_kontrola, 0); else { tcp_recv(niz_podaci->veza_kontrola, 0); tcp_err(niz_podaci->veza_kontrola, 0); }
        if (tcp_close(niz_podaci->veza_kontrola) != ERR_OK) tcp_abort(niz_podaci->veza_kontrola);
    }
    if (niz_podaci->datogram_kontrola) udp_remove(niz_podaci->datogram_kontrola); niz_podaci->TYPE_područje = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || prozivanje) return; prozivanje = 1;
    if(uporaba_ožičen_mreža)유선망살피기(&veza_uređaj);
    for (unsigned proračun = 0; !uporaba_ožičen_mreža && proračun < 4096 && (stroj_registar(보조장치 + 0x54) & 1); proračun++) {
        unsigned kodna_točka = stroj_registar(보조장치 + 0x40) & 255;
        if (kodna_točka == 192) {
            if (primiti_iskorištenost && !primiti_pogreška && !수신탈출) {
                struct pbuf *podaci_položaj = pbuf_alloc(PBUF_RAW, primiti_iskorištenost, PBUF_POOL);
                if (podaci_položaj) { RECEIVED_datogram_COUNT++; RECEIVED_bajt_COUNT += primiti_iskorištenost; pbuf_take(podaci_položaj, primiti_međuspremnik_podataka, primiti_iskorištenost); if (veza_uređaj.input(podaci_položaj, &veza_uređaj) != ERR_OK) { 버린전문수++; pbuf_free(podaci_položaj); } }
                else 버린전문수++;
            }
            else if (primiti_iskorištenost) 버린전문수++;
            primiti_iskorištenost = primiti_pogreška = 수신탈출 = 0;
        } else if (kodna_točka == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kodna_točka != 220 && kodna_točka != 221) primiti_pogreška = 1; kodna_točka = kodna_točka == 220 ? 192 : 219; 수신탈출 = 0; }
            if (primiti_iskorištenost < sizeof(primiti_međuspremnik_podataka)) primiti_međuspremnik_podataka[primiti_iskorištenost++] = kodna_točka; else primiti_pogreška = 1;
        }
    }
    netif_poll(&veza_uređaj); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned proračun = 0; proračun < 4096 && 송신개수 && (stroj_registar(보조장치 + 0x54) & 0x20); proračun++) {
        stroj_registar(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    prozivanje = 0;
}

/* Postavke·조회는 lwIP의 stvaran_podaci 인터페이스와 završiti_razgovor_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned unos_VALUE, unsigned INDEX) {
    if(unos_VALUE==20)return uporaba_ožičen_mreža;
    if(unos_VALUE==21)return 준비됨&&netif_is_link_up(&veza_uređaj);
    if(unos_VALUE==22)return uporaba_ožičen_mreža?유선망집계(5):0;
    if (!준비됨) return 0;
    if(uporaba_ožičen_mreža&&unos_VALUE>=4&&unos_VALUE<=8)return 유선망집계(unos_VALUE-4);
    if (unos_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&veza_uređaj)));
    if (unos_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&veza_uređaj)));
    if (unos_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&veza_uređaj)));
    if (unos_VALUE == 3) return netif_is_up(&veza_uređaj) != 0;
    if (unos_VALUE == 4) return RECEIVED_datogram_COUNT;
    if (unos_VALUE == 5) return 보낸전문수;
    if (unos_VALUE == 6) return RECEIVED_bajt_COUNT;
    if (unos_VALUE == 7) return 보낸바이트수;
    if (unos_VALUE == 8) return 버린전문수;
    if (unos_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *završiti_razgovor_p = &통신끝점들[INDEX];
    if (unos_VALUE == 10) return završiti_razgovor_p->TYPE_područje;
    if (!završiti_razgovor_p->TYPE_područje) return 0;
    if (unos_VALUE == 11) return mreža_broj_priključka(INDEX);
    if (unos_VALUE == 12) return završiti_razgovor_p->ravnopravan_član_adresa;
    if (unos_VALUE == 13) return završiti_razgovor_p->상대창구번호;
    if (unos_VALUE == 14) return završiti_razgovor_p->primiti_prebaciti ? 1 : završiti_razgovor_p->Datoteka_završiti_razgovor ? 3 : završiti_razgovor_p->GREŠKA ? 4 : završiti_razgovor_p->연결됨 ? 2 : 0;
    if (unos_VALUE == 15) return završiti_razgovor_p->unos_COUNT;
    if (unos_VALUE == 16) {
        const ip_addr_t *adresa = završiti_razgovor_p->TYPE_područje == 1 && završiti_razgovor_p->veza_kontrola ? &završiti_razgovor_p->veza_kontrola->local_ip :
            završiti_razgovor_p->TYPE_područje == 2 && završiti_razgovor_p->datogram_kontrola ? &završiti_razgovor_p->datogram_kontrola->local_ip : 0;
        return adresa ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) : 0;
    }
    return 0;
}

int 망설정하기(unsigned Aktivnost, uint32_t adresa, uint32_t maska_VALUE, uint32_t pristupnik_VALUE) {
    if (!준비됨) return -100;
    if (Aktivnost == 1) { netif_set_up(&veza_uređaj); return 0; }
    if (Aktivnost == 2) { netif_set_down(&veza_uređaj); return 0; }
    if (Aktivnost != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_VALUE, 같은 망의 선택적 zadana_vrijednost pristupnik_VALUE. */
    uint32_t 뒤집은가림 = ~maska_VALUE;
    if (!maska_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !adresa || (adresa >> 24) == 127 ||
        (adresa >> 24) == 0 || (adresa >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(adresa & 뒤집은가림) || (adresa & 뒤집은가림) == 뒤집은가림)) ||
        (pristupnik_VALUE && ((pristupnik_VALUE & maska_VALUE) != (adresa & maska_VALUE) || pristupnik_VALUE == adresa || (pristupnik_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(pristupnik_VALUE & 뒤집은가림) || (pristupnik_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 adresa 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_područje &&
        !(통신끝점들[INDEX].primiti_prebaciti && 통신끝점들[INDEX].veza_kontrola && ip_addr_isany(&통신끝점들[INDEX].veza_kontrola->local_ip))) return -16;
    if(uporaba_ožičen_mreža)dhcp_stop(&veza_uređaj);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(adresa)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(pristupnik_VALUE));
    netif_set_addr(&veza_uređaj, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *odgovor_sudionik;
static uint32_t 시험주소, 시험시각, vrijeme_odgovora;
static unsigned 시험순서, 시험식별자, odgovor_SEQUENCE;
static int odgovor_Stanje;
static u8_t 응답받음(void *Argumenti, struct raw_pcb *završiti_razgovor_p, struct pbuf *podaci, const ip_addr_t *adresa) {
    (void)Argumenti; (void)završiti_razgovor_p;
    unsigned char 머리[20], odgovor[16];
    if (odgovor_Stanje != -11 || podaci->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) != 시험주소 || pbuf_copy_partial(podaci, 머리, 20, 0) != 20) return 0;
    unsigned Zaglavlje_promijeniti_veličinu = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Zaglavlje_promijeniti_veličinu < 20 || podaci->tot_len < Zaglavlje_promijeniti_veličinu + 16 ||
        pbuf_copy_partial(podaci, odgovor, 16, Zaglavlje_promijeniti_veličinu) != 16 || odgovor[0] || odgovor[1] ||
        (((unsigned)odgovor[4] << 8) | odgovor[5]) != 시험식별자 ||
        (((unsigned)odgovor[6] << 8) | odgovor[7]) != 시험순서 ||
        odgovor[8] != 'J' || odgovor[9] != 'K' || odgovor[10] != 'O' || odgovor[11] != 'S' ||
        (((uint32_t)odgovor[12] << 24) | ((uint32_t)odgovor[13] << 16) | ((uint32_t)odgovor[14] << 8) | odgovor[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(podaci, Zaglavlje_promijeniti_veličinu)) return 0;
    if (inet_chksum_pbuf(podaci)) { pbuf_add_header(podaci, Zaglavlje_promijeniti_veličinu); return 0; }
    vrijeme_odgovora = (uint32_t)보드밀리초() - 시험시각; odgovor_SEQUENCE = 머리[8]; odgovor_Stanje = 0;
    pbuf_free(podaci); return 1;
}
int 응답시험시작(uint32_t adresa, unsigned narudžba_VALUE) {
    if (!준비됨 || !netif_is_up(&veza_uređaj)) return -100;
    if (!adresa || (adresa >> 28) >= 14 || adresa == 0xffffffffu) return -22;
    if (!odgovor_sudionik) { odgovor_sudionik = raw_new(IP_PROTO_ICMP); if (!odgovor_sudionik) return -12; raw_recv(odgovor_sudionik, 응답받음, 0); }
    시험주소 = adresa; 시험순서 = narudžba_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); odgovor_Stanje = -11; vrijeme_odgovora = odgovor_SEQUENCE = 0;
    unsigned char podaci[32] = {8,0,0,0};
    podaci[4] = 시험식별자 >> 8; podaci[5] = 시험식별자; podaci[6] = 시험순서 >> 8; podaci[7] = 시험순서;
    podaci[8]='J'; podaci[9]='K'; podaci[10]='O'; podaci[11]='S';
    podaci[12]=시험시각 >> 24; podaci[13]=시험시각 >> 16; podaci[14]=시험시각 >> 8; podaci[15]=시험시각;
    for (unsigned indeks_položaja = 16; indeks_položaja < sizeof(podaci); indeks_položaja++) podaci[indeks_položaja] = indeks_položaja;
    uint16_t programska_provjera_kontrolni_zbroj = inet_chksum(podaci, sizeof(podaci)); memcpy(podaci + 2, &programska_provjera_kontrolni_zbroj, 2);
    struct pbuf *datogram = pbuf_alloc(PBUF_IP, sizeof(podaci), PBUF_RAM); if (!datogram) return -12;
    pbuf_take(datogram, podaci, sizeof(podaci)); ip_addr_t odredište_sudionik; ip_addr_set_ip4_u32(&odredište_sudionik, lwip_htonl(adresa));
    err_t 처리값 = raw_sendto(odgovor_sudionik, datogram, &odredište_sudionik); pbuf_free(datogram);
    if (처리값) odgovor_Stanje = broj_pogreške(처리값);
    return 처리값 ? odgovor_Stanje : 0;
}
int 응답시험읽기(unsigned unos_VALUE) {
    통신망살피기();
    return unos_VALUE == 0 ? odgovor_Stanje : unos_VALUE == 1 ? (int)vrijeme_odgovora : unos_VALUE == 2 ? (int)odgovor_SEQUENCE : -22;
}
