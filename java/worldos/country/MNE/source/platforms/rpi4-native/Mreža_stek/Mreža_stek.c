#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Mreža_stek.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../udaljen_VALUE/udaljen_VALUE.h"
#include "žični_Mreža.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define računar_registar(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif veza_uređaj;
static int 준비됨, prozivanje;
static int koristiti_žični_Mreža;
static unsigned primiti_upotreba, 수신탈출, primiti_greška;
static unsigned char primiti_bafer_za_podatke[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_datagram_COUNT, 보낸전문수, RECEIVED_bajt_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int tip_oblast, primiti_port, informatičko_odeljenje_na_čekanju, 연결됨, Datoteka_završiti_razgovor, greška;
    struct tcp_pcb *veza_kontrola;
    struct udp_pcb *datagram_kontrola;
    unsigned čeona_kamera_stavka, stavka_COUNT_8f7753a1;
    unsigned char podaci[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], ravnopravni_uređaj_adresa;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int broj_greške(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *preuzeti_VALUE(int Datoteka_pokazivač) { return Datoteka_pokazivač >= 0 && Datoteka_pokazivač < 32 && 통신끝점들[Datoteka_pokazivač].tip_oblast ? &통신끝점들[Datoteka_pokazivač] : 0; }
static int 예약하기(int tip_oblast) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].tip_oblast) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].tip_oblast = tip_oblast; 통신끝점들[순번].informatičko_odeljenje_na_čekanju = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kôd_znaka) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kôd_znaka; }
static err_t 출력결과(struct netif *stavka_COUNT, struct pbuf *podaci_pozicija, const ip4_addr_t *adresa) {
    (void)stavka_COUNT; (void)adresa;
    if (podaci_pozicija->tot_len > 1500 || 송신개수 + 2 * podaci_pozicija->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Dalje_Pomak = podaci_pozicija; Dalje_Pomak; Dalje_Pomak = Dalje_Pomak->next) for (unsigned 순번 = 0; 순번 < Dalje_Pomak->len; 순번++) {
        unsigned kôd_znaka = ((unsigned char *)Dalje_Pomak->payload)[순번];
        if (kôd_znaka == 192 || kôd_znaka == 219) { 내보내기(219); 내보내기(kôd_znaka == 192 ? 220 : 221); } else 내보내기(kôd_znaka);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += podaci_pozicija->tot_len; return ERR_OK;
}
static err_t Pripremi_CLR_komponenta(struct netif *stavka_COUNT) { stavka_COUNT->name[0] = 's'; stavka_COUNT->name[1] = 'l'; stavka_COUNT->mtu = 1500; stavka_COUNT->output = 출력결과; return ERR_OK; }
void Pripremi_Mreža(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    računar_registar(보조장치 + 4) |= 1; računar_registar(보조장치 + 0x60) = 0; računar_registar(보조장치 + 0x44) = 0;
    računar_registar(보조장치 + 0x48) = 0xc6; računar_registar(보조장치 + 0x4c) = 3; računar_registar(보조장치 + 0x68) = 270; računar_registar(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internet_adresa, maska_bitova, adresa_mrežnog_prolaza;
    koristiti_žični_Mreža=유선장치있음();
    ip4_addr_set_u32(&Internet_adresa, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&maska_bitova, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&adresa_mrežnog_prolaza, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&veza_uređaj, &Internet_adresa, &maska_bitova, &adresa_mrežnog_prolaza, 0, koristiti_žični_Mreža?Pripremi_žični_Mreža:Pripremi_CLR_komponenta, koristiti_žični_Mreža?ethernet_input:ip4_input))return;
    netif_set_default(&veza_uređaj); netif_set_up(&veza_uređaj);if(!koristiti_žični_Mreža)netif_set_link_up(&veza_uređaj); 준비됨 = 1;
    Pripremi_udaljen();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *podaci_pozicija, err_t greška) {
    통신끝점 *niska_podaci = 부가인수; (void)통신제어블록; (void)greška;
    if (!podaci_pozicija) { niska_podaci->Datoteka_završiti_razgovor = 1; return ERR_OK; }
    if (podaci_pozicija->tot_len > sizeof(niska_podaci->podaci) - niska_podaci->stavka_COUNT_8f7753a1) return ERR_MEM;
    unsigned aktuelno_pozicija = (niska_podaci->čeona_kamera_stavka + niska_podaci->stavka_COUNT_8f7753a1) % sizeof(niska_podaci->podaci);
    for (struct pbuf *Dalje_Pomak = podaci_pozicija; Dalje_Pomak; Dalje_Pomak = Dalje_Pomak->next) for (unsigned 순번 = 0; 순번 < Dalje_Pomak->len; 순번++) {
        niska_podaci->podaci[aktuelno_pozicija] = ((unsigned char *)Dalje_Pomak->payload)[순번]; aktuelno_pozicija = (aktuelno_pozicija + 1) % sizeof(niska_podaci->podaci);
    }
    niska_podaci->stavka_COUNT_8f7753a1 += podaci_pozicija->tot_len; pbuf_free(podaci_pozicija); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t greška) { 통신끝점 *niska_podaci = 부가인수; niska_podaci->veza_kontrola = 0; niska_podaci->greška = broj_greške(greška); }
static void 되부름목록(통신끝점 *niska_podaci) { tcp_arg(niska_podaci->veza_kontrola, niska_podaci); tcp_recv(niska_podaci->veza_kontrola, 수신됨); tcp_err(niska_podaci->veza_kontrola, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t greška) {
    통신끝점 *niska_podaci = 부가인수; (void)통신제어블록; if (greška) niska_podaci->greška = broj_greške(greška); else niska_podaci->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t greška) {
    통신끝점 *nadređen = 부가인수; if (greška) return greška;
    int Datoteka_pokazivač = 예약하기(1); if (Datoteka_pokazivač < 0) return ERR_MEM;
    통신끝점 *niska_podaci = &통신끝점들[Datoteka_pokazivač]; niska_podaci->veza_kontrola = 통신제어블록; niska_podaci->연결됨 = 1; niska_podaci->informatičko_odeljenje_na_čekanju = (int)(nadređen - 통신끝점들);
    niska_podaci->ravnopravni_uređaj_adresa = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); niska_podaci->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(niska_podaci); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *podaci_pozicija, const ip_addr_t *adresa, u16_t broj_porta) {
    통신끝점 *niska_podaci = 부가인수; (void)통신제어블록;
    if (niska_podaci->stavka_COUNT_8f7753a1 < 4 && podaci_pozicija->tot_len <= 512) {
        unsigned indeks_pozicije = (niska_podaci->čeona_kamera_stavka + niska_podaci->stavka_COUNT_8f7753a1) % 4;
        pbuf_copy_partial(podaci_pozicija, niska_podaci->podaci + indeks_pozicije * 512, podaci_pozicija->tot_len, 0);
        niska_podaci->길이목록[indeks_pozicije] = podaci_pozicija->tot_len; niska_podaci->접속번호들[indeks_pozicije] = broj_porta;
        niska_podaci->주소목록[indeks_pozicije] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))); niska_podaci->stavka_COUNT_8f7753a1++;
    }
    pbuf_free(podaci_pozicija);
}
int 통신끝점만들기(int tip_oblast) {
    if (!준비됨) return -100;
    if (tip_oblast != 1 && tip_oblast != 2) return -93;
    int Datoteka_pokazivač = 예약하기(tip_oblast); if (Datoteka_pokazivač < 0) return Datoteka_pokazivač;
    통신끝점 *niska_podaci = &통신끝점들[Datoteka_pokazivač];
    if (tip_oblast == 1) { niska_podaci->veza_kontrola = tcp_new(); if (niska_podaci->veza_kontrola) 되부름목록(niska_podaci); }
    else { niska_podaci->datagram_kontrola = udp_new(); if (niska_podaci->datagram_kontrola) udp_recv(niska_podaci->datagram_kontrola, datagram, niska_podaci); }
    if (!niska_podaci->veza_kontrola && !niska_podaci->datagram_kontrola) { niska_podaci->tip_oblast = 0; return -12; } return Datoteka_pokazivač;
}
int NET_povezati(int Datoteka_pokazivač, uint32_t adresa, unsigned broj_porta) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci) return -9;
    if (broj_porta > 65535 || (adresa && adresa != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&veza_uređaj))) && adresa != 0x7f000001)) return -99;
    ip_addr_t Internet_adresa; ip_addr_set_ip4_u32(&Internet_adresa, lwip_htonl(adresa));
    err_t 보조항목 = niska_podaci->tip_oblast == 1 ? tcp_bind(niska_podaci->veza_kontrola, &Internet_adresa, broj_porta) : udp_bind(niska_podaci->datagram_kontrola, &Internet_adresa, broj_porta); return 보조항목 ? broj_greške(보조항목) : 0;
}
void 통신주소재사용(int Datoteka_pokazivač) { 통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (niska_podaci && niska_podaci->veza_kontrola) ip_set_option(niska_podaci->veza_kontrola, SOF_REUSEADDR); }
int NET_slušati(int Datoteka_pokazivač) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci || niska_podaci->tip_oblast != 1) return -9;
    if (niska_podaci->primiti_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(niska_podaci->veza_kontrola, 4, &보조항목);
    if (!통신제어블록) return broj_greške(보조항목); niska_podaci->veza_kontrola = 통신제어블록; niska_podaci->primiti_port = 1; tcp_arg(통신제어블록, niska_podaci); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_veze(int Datoteka_pokazivač, uint32_t adresa, unsigned broj_porta) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci || niska_podaci->tip_oblast != 1) return -9;
    if (niska_podaci->greška) return niska_podaci->greška;
    if (niska_podaci->연결됨) return 0;
    if (niska_podaci->상대창구번호) return -115;
    if (!broj_porta || broj_porta > 65535 || !adresa) return -22;
    ip_addr_t Internet_adresa; ip_addr_set_ip4_u32(&Internet_adresa, lwip_htonl(adresa));
    niska_podaci->ravnopravni_uređaj_adresa = adresa; niska_podaci->상대창구번호 = broj_porta;
    err_t 보조항목 = tcp_connect(niska_podaci->veza_kontrola, &Internet_adresa, broj_porta, 연결됨); return 보조항목 ? broj_greške(보조항목) : -115;
}
int NET_prihvatiti(int Datoteka_pokazivač) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci || !niska_podaci->primiti_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].tip_oblast == 1 && 통신끝점들[순번].informatičko_odeljenje_na_čekanju == Datoteka_pokazivač) { 통신끝점들[순번].informatičko_odeljenje_na_čekanju = -1; return 순번; }
    return -11;
}
int 통신읽기(int Datoteka_pokazivač, void *podaci, unsigned stavka_COUNT) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci || niska_podaci->tip_oblast != 1) return -9;
    if (!stavka_COUNT) return 0; if (!niska_podaci->stavka_COUNT_8f7753a1) return niska_podaci->greška ? niska_podaci->greška : niska_podaci->Datoteka_završiti_razgovor ? 0 : -11;
    if (stavka_COUNT > niska_podaci->stavka_COUNT_8f7753a1) stavka_COUNT = niska_podaci->stavka_COUNT_8f7753a1;
    for (unsigned 순번 = 0; 순번 < stavka_COUNT; 순번++) { ((unsigned char *)podaci)[순번] = niska_podaci->podaci[niska_podaci->čeona_kamera_stavka]; niska_podaci->čeona_kamera_stavka = (niska_podaci->čeona_kamera_stavka + 1) % sizeof(niska_podaci->podaci); }
    niska_podaci->stavka_COUNT_8f7753a1 -= stavka_COUNT; if (niska_podaci->veza_kontrola) tcp_recved(niska_podaci->veza_kontrola, stavka_COUNT); return stavka_COUNT;
}
int 통신쓰기(int Datoteka_pokazivač, const void *podaci, unsigned stavka_COUNT) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci || niska_podaci->tip_oblast != 1) return -9;
    if (niska_podaci->greška) return niska_podaci->greška; if (!niska_podaci->veza_kontrola || !niska_podaci->연결됨) return -107;
    if (!stavka_COUNT) return 0; if (stavka_COUNT > tcp_sndbuf(niska_podaci->veza_kontrola)) stavka_COUNT = tcp_sndbuf(niska_podaci->veza_kontrola);
    if (!stavka_COUNT) return -11; if (stavka_COUNT > 1024) stavka_COUNT = 1024;
    err_t 보조항목 = tcp_write(niska_podaci->veza_kontrola, podaci, stavka_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return broj_greške(보조항목);
    tcp_output(niska_podaci->veza_kontrola); return stavka_COUNT;
}
int poslati_datagram(int Datoteka_pokazivač, const void *podaci, unsigned stavka_COUNT, uint32_t adresa, unsigned broj_porta) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci || niska_podaci->tip_oblast != 2) return -9;
    if (stavka_COUNT > 512) return -90; if (!broj_porta || broj_porta > 65535) return -22;
    struct pbuf *podaci_pozicija = pbuf_alloc(PBUF_TRANSPORT, stavka_COUNT, PBUF_RAM); if (!podaci_pozicija) return -11;
    pbuf_take(podaci_pozicija, podaci, stavka_COUNT); ip_addr_t Internet_adresa; ip_addr_set_ip4_u32(&Internet_adresa, lwip_htonl(adresa));
    err_t 보조항목 = udp_sendto(niska_podaci->datagram_kontrola, podaci_pozicija, &Internet_adresa, broj_porta); pbuf_free(podaci_pozicija); return 보조항목 ? broj_greške(보조항목) : (int)stavka_COUNT;
}
int primiti_datagram(int Datoteka_pokazivač, void *podaci, unsigned stavka_COUNT) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci || niska_podaci->tip_oblast != 2) return -9;
    if (!niska_podaci->stavka_COUNT_8f7753a1) return -11; unsigned aktuelno_pozicija = niska_podaci->čeona_kamera_stavka;
    if (stavka_COUNT > niska_podaci->길이목록[aktuelno_pozicija]) stavka_COUNT = niska_podaci->길이목록[aktuelno_pozicija]; memcpy(podaci, niska_podaci->podaci + aktuelno_pozicija * 512, stavka_COUNT);
    niska_podaci->상대창구번호 = niska_podaci->접속번호들[aktuelno_pozicija]; niska_podaci->ravnopravni_uređaj_adresa = niska_podaci->주소목록[aktuelno_pozicija]; niska_podaci->čeona_kamera_stavka = (aktuelno_pozicija + 1) % 4; niska_podaci->stavka_COUNT_8f7753a1--; return stavka_COUNT;
}
unsigned Mreža_broj_porta(int Datoteka_pokazivač) { 통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); return !niska_podaci ? 0 : niska_podaci->veza_kontrola ? niska_podaci->veza_kontrola->local_port : niska_podaci->datagram_kontrola ? niska_podaci->datagram_kontrola->local_port : 0; }
unsigned ravnopravni_uređaj_broj_porta(int Datoteka_pokazivač) { 통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); return niska_podaci ? niska_podaci->상대창구번호 : 0; }
uint32_t NET_ravnopravni_uređaj_adresa(int Datoteka_pokazivač) { 통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); return niska_podaci ? niska_podaci->ravnopravni_uređaj_adresa : 0; }
void Zatvori_Mreža(int Datoteka_pokazivač) {
    통신끝점 *niska_podaci = preuzeti_VALUE(Datoteka_pokazivač); if (!niska_podaci) return;
    if (niska_podaci->primiti_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].tip_oblast && 통신끝점들[순번].informatičko_odeljenje_na_čekanju == Datoteka_pokazivač) Zatvori_Mreža(순번);
    if (niska_podaci->veza_kontrola) {
        tcp_arg(niska_podaci->veza_kontrola, 0); if (niska_podaci->primiti_port) tcp_accept(niska_podaci->veza_kontrola, 0); else { tcp_recv(niska_podaci->veza_kontrola, 0); tcp_err(niska_podaci->veza_kontrola, 0); }
        if (tcp_close(niska_podaci->veza_kontrola) != ERR_OK) tcp_abort(niska_podaci->veza_kontrola);
    }
    if (niska_podaci->datagram_kontrola) udp_remove(niska_podaci->datagram_kontrola); niska_podaci->tip_oblast = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || prozivanje) return; prozivanje = 1;
    if(koristiti_žični_Mreža)유선망살피기(&veza_uređaj);
    for (unsigned budžet = 0; !koristiti_žični_Mreža && budžet < 4096 && (računar_registar(보조장치 + 0x54) & 1); budžet++) {
        unsigned kôd_znaka = računar_registar(보조장치 + 0x40) & 255;
        if (kôd_znaka == 192) {
            if (primiti_upotreba && !primiti_greška && !수신탈출) {
                struct pbuf *podaci_pozicija = pbuf_alloc(PBUF_RAW, primiti_upotreba, PBUF_POOL);
                if (podaci_pozicija) { RECEIVED_datagram_COUNT++; RECEIVED_bajt_COUNT += primiti_upotreba; pbuf_take(podaci_pozicija, primiti_bafer_za_podatke, primiti_upotreba); if (veza_uređaj.input(podaci_pozicija, &veza_uređaj) != ERR_OK) { 버린전문수++; pbuf_free(podaci_pozicija); } }
                else 버린전문수++;
            }
            else if (primiti_upotreba) 버린전문수++;
            primiti_upotreba = primiti_greška = 수신탈출 = 0;
        } else if (kôd_znaka == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kôd_znaka != 220 && kôd_znaka != 221) primiti_greška = 1; kôd_znaka = kôd_znaka == 220 ? 192 : 219; 수신탈출 = 0; }
            if (primiti_upotreba < sizeof(primiti_bafer_za_podatke)) primiti_bafer_za_podatke[primiti_upotreba++] = kôd_znaka; else primiti_greška = 1;
        }
    }
    netif_poll(&veza_uređaj); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budžet = 0; budžet < 4096 && 송신개수 && (računar_registar(보조장치 + 0x54) & 0x20); budžet++) {
        računar_registar(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    prozivanje = 0;
}

/* Postavke·조회는 lwIP의 stvarni_podaci 인터페이스와 završiti_razgovor_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned stavka_VALUE, unsigned INDEX) {
    if(stavka_VALUE==20)return koristiti_žični_Mreža;
    if(stavka_VALUE==21)return 준비됨&&netif_is_link_up(&veza_uređaj);
    if(stavka_VALUE==22)return koristiti_žični_Mreža?유선망집계(5):0;
    if (!준비됨) return 0;
    if(koristiti_žični_Mreža&&stavka_VALUE>=4&&stavka_VALUE<=8)return 유선망집계(stavka_VALUE-4);
    if (stavka_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&veza_uređaj)));
    if (stavka_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&veza_uređaj)));
    if (stavka_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&veza_uređaj)));
    if (stavka_VALUE == 3) return netif_is_up(&veza_uređaj) != 0;
    if (stavka_VALUE == 4) return RECEIVED_datagram_COUNT;
    if (stavka_VALUE == 5) return 보낸전문수;
    if (stavka_VALUE == 6) return RECEIVED_bajt_COUNT;
    if (stavka_VALUE == 7) return 보낸바이트수;
    if (stavka_VALUE == 8) return 버린전문수;
    if (stavka_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *završiti_razgovor_p = &통신끝점들[INDEX];
    if (stavka_VALUE == 10) return završiti_razgovor_p->tip_oblast;
    if (!završiti_razgovor_p->tip_oblast) return 0;
    if (stavka_VALUE == 11) return Mreža_broj_porta(INDEX);
    if (stavka_VALUE == 12) return završiti_razgovor_p->ravnopravni_uređaj_adresa;
    if (stavka_VALUE == 13) return završiti_razgovor_p->상대창구번호;
    if (stavka_VALUE == 14) return završiti_razgovor_p->primiti_port ? 1 : završiti_razgovor_p->Datoteka_završiti_razgovor ? 3 : završiti_razgovor_p->greška ? 4 : završiti_razgovor_p->연결됨 ? 2 : 0;
    if (stavka_VALUE == 15) return završiti_razgovor_p->stavka_COUNT_8f7753a1;
    if (stavka_VALUE == 16) {
        const ip_addr_t *adresa = završiti_razgovor_p->tip_oblast == 1 && završiti_razgovor_p->veza_kontrola ? &završiti_razgovor_p->veza_kontrola->local_ip :
            završiti_razgovor_p->tip_oblast == 2 && završiti_razgovor_p->datagram_kontrola ? &završiti_razgovor_p->datagram_kontrola->local_ip : 0;
        return adresa ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) : 0;
    }
    return 0;
}

int konfigurisati_Mreža(unsigned radnja, uint32_t adresa, uint32_t maska_VALUE, uint32_t mrežni_prolaz_VALUE) {
    if (!준비됨) return -100;
    if (radnja == 1) { netif_set_up(&veza_uređaj); return 0; }
    if (radnja == 2) { netif_set_down(&veza_uređaj); return 0; }
    if (radnja != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_VALUE, 같은 망의 선택적 podrazumevana_vrednost mrežni_prolaz_VALUE. */
    uint32_t 뒤집은가림 = ~maska_VALUE;
    if (!maska_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !adresa || (adresa >> 24) == 127 ||
        (adresa >> 24) == 0 || (adresa >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(adresa & 뒤집은가림) || (adresa & 뒤집은가림) == 뒤집은가림)) ||
        (mrežni_prolaz_VALUE && ((mrežni_prolaz_VALUE & maska_VALUE) != (adresa & maska_VALUE) || mrežni_prolaz_VALUE == adresa || (mrežni_prolaz_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(mrežni_prolaz_VALUE & 뒤집은가림) || (mrežni_prolaz_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 adresa 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].tip_oblast &&
        !(통신끝점들[INDEX].primiti_port && 통신끝점들[INDEX].veza_kontrola && ip_addr_isany(&통신끝점들[INDEX].veza_kontrola->local_ip))) return -16;
    if(koristiti_žični_Mreža)dhcp_stop(&veza_uređaj);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(adresa)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(mrežni_prolaz_VALUE));
    netif_set_addr(&veza_uređaj, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *odgovor_učesnik;
static uint32_t 시험주소, 시험시각, vreme_odziva;
static unsigned 시험순서, 시험식별자, odgovor_SEQUENCE;
static int odgovor_Status;
static u8_t 응답받음(void *인수, struct raw_pcb *završiti_razgovor_p, struct pbuf *podaci, const ip_addr_t *adresa) {
    (void)인수; (void)završiti_razgovor_p;
    unsigned char 머리[20], odgovor[16];
    if (odgovor_Status != -11 || podaci->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) != 시험주소 || pbuf_copy_partial(podaci, 머리, 20, 0) != 20) return 0;
    unsigned Zaglavlje_promeniti_veličinu = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Zaglavlje_promeniti_veličinu < 20 || podaci->tot_len < Zaglavlje_promeniti_veličinu + 16 ||
        pbuf_copy_partial(podaci, odgovor, 16, Zaglavlje_promeniti_veličinu) != 16 || odgovor[0] || odgovor[1] ||
        (((unsigned)odgovor[4] << 8) | odgovor[5]) != 시험식별자 ||
        (((unsigned)odgovor[6] << 8) | odgovor[7]) != 시험순서 ||
        odgovor[8] != 'J' || odgovor[9] != 'K' || odgovor[10] != 'O' || odgovor[11] != 'S' ||
        (((uint32_t)odgovor[12] << 24) | ((uint32_t)odgovor[13] << 16) | ((uint32_t)odgovor[14] << 8) | odgovor[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(podaci, Zaglavlje_promeniti_veličinu)) return 0;
    if (inet_chksum_pbuf(podaci)) { pbuf_add_header(podaci, Zaglavlje_promeniti_veličinu); return 0; }
    vreme_odziva = (uint32_t)보드밀리초() - 시험시각; odgovor_SEQUENCE = 머리[8]; odgovor_Status = 0;
    pbuf_free(podaci); return 1;
}
int 응답시험시작(uint32_t adresa, unsigned poručiti_VALUE) {
    if (!준비됨 || !netif_is_up(&veza_uređaj)) return -100;
    if (!adresa || (adresa >> 28) >= 14 || adresa == 0xffffffffu) return -22;
    if (!odgovor_učesnik) { odgovor_učesnik = raw_new(IP_PROTO_ICMP); if (!odgovor_učesnik) return -12; raw_recv(odgovor_učesnik, 응답받음, 0); }
    시험주소 = adresa; 시험순서 = poručiti_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); odgovor_Status = -11; vreme_odziva = odgovor_SEQUENCE = 0;
    unsigned char podaci[32] = {8,0,0,0};
    podaci[4] = 시험식별자 >> 8; podaci[5] = 시험식별자; podaci[6] = 시험순서 >> 8; podaci[7] = 시험순서;
    podaci[8]='J'; podaci[9]='K'; podaci[10]='O'; podaci[11]='S';
    podaci[12]=시험시각 >> 24; podaci[13]=시험시각 >> 16; podaci[14]=시험시각 >> 8; podaci[15]=시험시각;
    for (unsigned indeks_pozicije = 16; indeks_pozicije < sizeof(podaci); indeks_pozicije++) podaci[indeks_pozicije] = indeks_pozicije;
    uint16_t verifikacija_kontrolni_zbir = inet_chksum(podaci, sizeof(podaci)); memcpy(podaci + 2, &verifikacija_kontrolni_zbir, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(podaci), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, podaci, sizeof(podaci)); ip_addr_t odredište_učesnik; ip_addr_set_ip4_u32(&odredište_učesnik, lwip_htonl(adresa));
    err_t 처리값 = raw_sendto(odgovor_učesnik, datagram, &odredište_učesnik); pbuf_free(datagram);
    if (처리값) odgovor_Status = broj_greške(처리값);
    return 처리값 ? odgovor_Status : 0;
}
int 응답시험읽기(unsigned stavka_VALUE) {
    통신망살피기();
    return stavka_VALUE == 0 ? odgovor_Status : stavka_VALUE == 1 ? (int)vreme_odziva : stavka_VALUE == 2 ? (int)odgovor_SEQUENCE : -22;
}
