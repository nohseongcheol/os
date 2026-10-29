#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "sieť_Vrstvy.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../vzdialený_VALUE/vzdialený_VALUE.h"
#include "drôtový_sieť.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define počítač_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif kontakt_telefón;
static int 준비됨, vzorkovanie;
static int používať_drôtový_sieť;
static unsigned dostať_použitie, 수신탈출, dostať_Chyba;
static unsigned char dostať_dátová_medzipamäť[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_datagram_COUNT, 보낸전문수, RECEIVED_Byte_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int Typ_oblasť, dostať_port, Informačné_systémy_čakajúci, 연결됨, Súbor_ukončiť_hovor, chyba;
    struct tcp_pcb *kontakt_riadenie;
    struct udp_pcb *datagram_riadenie;
    unsigned predný_položka, položka_COUNT_8f7753a1;
    unsigned char údaje[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], partnerský_uzol_adresa;
} soket_účastník_3db661a2;
static soket_účastník_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int chybové_číslo(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static soket_účastník_3db661a2 *načítať_VALUE(int Súbor_rukoväť) { return Súbor_rukoväť >= 0 && Súbor_rukoväť < 32 && 통신끝점들[Súbor_rukoväť].Typ_oblasť ? &통신끝점들[Súbor_rukoväť] : 0; }
static int 예약하기(int Typ_oblasť) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].Typ_oblasť) {
        memset(&통신끝점들[순번], 0, sizeof(soket_účastník_3db661a2)); 통신끝점들[순번].Typ_oblasť = Typ_oblasť; 통신끝점들[순번].Informačné_systémy_čakajúci = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned bod_kódu) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = bod_kódu; }
static err_t 출력결과(struct netif *položka_COUNT, struct pbuf *údaje_pozícia, const ip4_addr_t *adresa) {
    (void)položka_COUNT; (void)adresa;
    if (údaje_pozícia->tot_len > 1500 || 송신개수 + 2 * údaje_pozícia->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Ďalej_Posun = údaje_pozícia; Ďalej_Posun; Ďalej_Posun = Ďalej_Posun->next) for (unsigned 순번 = 0; 순번 < Ďalej_Posun->len; 순번++) {
        unsigned bod_kódu = ((unsigned char *)Ďalej_Posun->payload)[순번];
        if (bod_kódu == 192 || bod_kódu == 219) { 내보내기(219); 내보내기(bod_kódu == 192 ? 220 : 221); } else 내보내기(bod_kódu);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += údaje_pozícia->tot_len; return ERR_OK;
}
static err_t Pripraviť_CLR(struct netif *položka_COUNT) { položka_COUNT->name[0] = 's'; položka_COUNT->name[1] = 'l'; položka_COUNT->mtu = 1500; položka_COUNT->output = 출력결과; return ERR_OK; }
void Pripraviť_sieť(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    počítač_register(보조장치 + 4) |= 1; počítač_register(보조장치 + 0x60) = 0; počítač_register(보조장치 + 0x44) = 0;
    počítač_register(보조장치 + 0x48) = 0xc6; počítač_register(보조장치 + 0x4c) = 3; počítač_register(보조장치 + 0x68) = 270; počítač_register(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetová_adresa, bitová_maska, adresa_brány;
    používať_drôtový_sieť=유선장치있음();
    ip4_addr_set_u32(&internetová_adresa, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitová_maska, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&adresa_brány, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&kontakt_telefón, &internetová_adresa, &bitová_maska, &adresa_brány, 0, používať_drôtový_sieť?Pripraviť_drôtový_sieť:Pripraviť_CLR, používať_drôtový_sieť?ethernet_input:ip4_input))return;
    netif_set_default(&kontakt_telefón); netif_set_up(&kontakt_telefón);if(!používať_drôtový_sieť)netif_set_link_up(&kontakt_telefón); 준비됨 = 1;
    Pripraviť_vzdialený();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *údaje_pozícia, err_t chyba) {
    soket_účastník_3db661a2 *reťazec_údaje = 부가인수; (void)통신제어블록; (void)chyba;
    if (!údaje_pozícia) { reťazec_údaje->Súbor_ukončiť_hovor = 1; return ERR_OK; }
    if (údaje_pozícia->tot_len > sizeof(reťazec_údaje->údaje) - reťazec_údaje->položka_COUNT_8f7753a1) return ERR_MEM;
    unsigned v_termíne_splatnosti_pozícia = (reťazec_údaje->predný_položka + reťazec_údaje->položka_COUNT_8f7753a1) % sizeof(reťazec_údaje->údaje);
    for (struct pbuf *Ďalej_Posun = údaje_pozícia; Ďalej_Posun; Ďalej_Posun = Ďalej_Posun->next) for (unsigned 순번 = 0; 순번 < Ďalej_Posun->len; 순번++) {
        reťazec_údaje->údaje[v_termíne_splatnosti_pozícia] = ((unsigned char *)Ďalej_Posun->payload)[순번]; v_termíne_splatnosti_pozícia = (v_termíne_splatnosti_pozícia + 1) % sizeof(reťazec_údaje->údaje);
    }
    reťazec_údaje->položka_COUNT_8f7753a1 += údaje_pozícia->tot_len; pbuf_free(údaje_pozícia); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t chyba) { soket_účastník_3db661a2 *reťazec_údaje = 부가인수; reťazec_údaje->kontakt_riadenie = 0; reťazec_údaje->chyba = chybové_číslo(chyba); }
static void 되부름목록(soket_účastník_3db661a2 *reťazec_údaje) { tcp_arg(reťazec_údaje->kontakt_riadenie, reťazec_údaje); tcp_recv(reťazec_údaje->kontakt_riadenie, 수신됨); tcp_err(reťazec_údaje->kontakt_riadenie, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t chyba) {
    soket_účastník_3db661a2 *reťazec_údaje = 부가인수; (void)통신제어블록; if (chyba) reťazec_údaje->chyba = chybové_číslo(chyba); else reťazec_údaje->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t chyba) {
    soket_účastník_3db661a2 *nadradený = 부가인수; if (chyba) return chyba;
    int Súbor_rukoväť = 예약하기(1); if (Súbor_rukoväť < 0) return ERR_MEM;
    soket_účastník_3db661a2 *reťazec_údaje = &통신끝점들[Súbor_rukoväť]; reťazec_údaje->kontakt_riadenie = 통신제어블록; reťazec_údaje->연결됨 = 1; reťazec_údaje->Informačné_systémy_čakajúci = (int)(nadradený - 통신끝점들);
    reťazec_údaje->partnerský_uzol_adresa = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); reťazec_údaje->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(reťazec_údaje); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *údaje_pozícia, const ip_addr_t *adresa, u16_t číslo_portu) {
    soket_účastník_3db661a2 *reťazec_údaje = 부가인수; (void)통신제어블록;
    if (reťazec_údaje->položka_COUNT_8f7753a1 < 4 && údaje_pozícia->tot_len <= 512) {
        unsigned pozičný_index = (reťazec_údaje->predný_položka + reťazec_údaje->položka_COUNT_8f7753a1) % 4;
        pbuf_copy_partial(údaje_pozícia, reťazec_údaje->údaje + pozičný_index * 512, údaje_pozícia->tot_len, 0);
        reťazec_údaje->길이목록[pozičný_index] = údaje_pozícia->tot_len; reťazec_údaje->접속번호들[pozičný_index] = číslo_portu;
        reťazec_údaje->주소목록[pozičný_index] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))); reťazec_údaje->položka_COUNT_8f7753a1++;
    }
    pbuf_free(údaje_pozícia);
}
int Create_soket_účastník(int Typ_oblasť) {
    if (!준비됨) return -100;
    if (Typ_oblasť != 1 && Typ_oblasť != 2) return -93;
    int Súbor_rukoväť = 예약하기(Typ_oblasť); if (Súbor_rukoväť < 0) return Súbor_rukoväť;
    soket_účastník_3db661a2 *reťazec_údaje = &통신끝점들[Súbor_rukoväť];
    if (Typ_oblasť == 1) { reťazec_údaje->kontakt_riadenie = tcp_new(); if (reťazec_údaje->kontakt_riadenie) 되부름목록(reťazec_údaje); }
    else { reťazec_údaje->datagram_riadenie = udp_new(); if (reťazec_údaje->datagram_riadenie) udp_recv(reťazec_údaje->datagram_riadenie, datagram, reťazec_údaje); }
    if (!reťazec_údaje->kontakt_riadenie && !reťazec_údaje->datagram_riadenie) { reťazec_údaje->Typ_oblasť = 0; return -12; } return Súbor_rukoväť;
}
int NET_BIND(int Súbor_rukoväť, uint32_t adresa, unsigned číslo_portu) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje) return -9;
    if (číslo_portu > 65535 || (adresa && adresa != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_telefón))) && adresa != 0x7f000001)) return -99;
    ip_addr_t internetová_adresa; ip_addr_set_ip4_u32(&internetová_adresa, lwip_htonl(adresa));
    err_t 보조항목 = reťazec_údaje->Typ_oblasť == 1 ? tcp_bind(reťazec_údaje->kontakt_riadenie, &internetová_adresa, číslo_portu) : udp_bind(reťazec_údaje->datagram_riadenie, &internetová_adresa, číslo_portu); return 보조항목 ? chybové_číslo(보조항목) : 0;
}
void 통신주소재사용(int Súbor_rukoväť) { soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (reťazec_údaje && reťazec_údaje->kontakt_riadenie) ip_set_option(reťazec_údaje->kontakt_riadenie, SOF_REUSEADDR); }
int NET_načúvať(int Súbor_rukoväť) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje || reťazec_údaje->Typ_oblasť != 1) return -9;
    if (reťazec_údaje->dostať_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(reťazec_údaje->kontakt_riadenie, 4, &보조항목);
    if (!통신제어블록) return chybové_číslo(보조항목); reťazec_údaje->kontakt_riadenie = 통신제어블록; reťazec_údaje->dostať_port = 1; tcp_arg(통신제어블록, reťazec_údaje); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_spojiť(int Súbor_rukoväť, uint32_t adresa, unsigned číslo_portu) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje || reťazec_údaje->Typ_oblasť != 1) return -9;
    if (reťazec_údaje->chyba) return reťazec_údaje->chyba;
    if (reťazec_údaje->연결됨) return 0;
    if (reťazec_údaje->상대창구번호) return -115;
    if (!číslo_portu || číslo_portu > 65535 || !adresa) return -22;
    ip_addr_t internetová_adresa; ip_addr_set_ip4_u32(&internetová_adresa, lwip_htonl(adresa));
    reťazec_údaje->partnerský_uzol_adresa = adresa; reťazec_údaje->상대창구번호 = číslo_portu;
    err_t 보조항목 = tcp_connect(reťazec_údaje->kontakt_riadenie, &internetová_adresa, číslo_portu, 연결됨); return 보조항목 ? chybové_číslo(보조항목) : -115;
}
int NET_prijať(int Súbor_rukoväť) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje || !reťazec_údaje->dostať_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].Typ_oblasť == 1 && 통신끝점들[순번].Informačné_systémy_čakajúci == Súbor_rukoväť) { 통신끝점들[순번].Informačné_systémy_čakajúci = -1; return 순번; }
    return -11;
}
int 통신읽기(int Súbor_rukoväť, void *údaje, unsigned položka_COUNT) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje || reťazec_údaje->Typ_oblasť != 1) return -9;
    if (!položka_COUNT) return 0; if (!reťazec_údaje->položka_COUNT_8f7753a1) return reťazec_údaje->chyba ? reťazec_údaje->chyba : reťazec_údaje->Súbor_ukončiť_hovor ? 0 : -11;
    if (položka_COUNT > reťazec_údaje->položka_COUNT_8f7753a1) položka_COUNT = reťazec_údaje->položka_COUNT_8f7753a1;
    for (unsigned 순번 = 0; 순번 < položka_COUNT; 순번++) { ((unsigned char *)údaje)[순번] = reťazec_údaje->údaje[reťazec_údaje->predný_položka]; reťazec_údaje->predný_položka = (reťazec_údaje->predný_položka + 1) % sizeof(reťazec_údaje->údaje); }
    reťazec_údaje->položka_COUNT_8f7753a1 -= položka_COUNT; if (reťazec_údaje->kontakt_riadenie) tcp_recved(reťazec_údaje->kontakt_riadenie, položka_COUNT); return položka_COUNT;
}
int NET_zapísať(int Súbor_rukoväť, const void *údaje, unsigned položka_COUNT) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje || reťazec_údaje->Typ_oblasť != 1) return -9;
    if (reťazec_údaje->chyba) return reťazec_údaje->chyba; if (!reťazec_údaje->kontakt_riadenie || !reťazec_údaje->연결됨) return -107;
    if (!položka_COUNT) return 0; if (položka_COUNT > tcp_sndbuf(reťazec_údaje->kontakt_riadenie)) položka_COUNT = tcp_sndbuf(reťazec_údaje->kontakt_riadenie);
    if (!položka_COUNT) return -11; if (položka_COUNT > 1024) položka_COUNT = 1024;
    err_t 보조항목 = tcp_write(reťazec_údaje->kontakt_riadenie, údaje, položka_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return chybové_číslo(보조항목);
    tcp_output(reťazec_údaje->kontakt_riadenie); return položka_COUNT;
}
int odoslať_datagram(int Súbor_rukoväť, const void *údaje, unsigned položka_COUNT, uint32_t adresa, unsigned číslo_portu) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje || reťazec_údaje->Typ_oblasť != 2) return -9;
    if (položka_COUNT > 512) return -90; if (!číslo_portu || číslo_portu > 65535) return -22;
    struct pbuf *údaje_pozícia = pbuf_alloc(PBUF_TRANSPORT, položka_COUNT, PBUF_RAM); if (!údaje_pozícia) return -11;
    pbuf_take(údaje_pozícia, údaje, položka_COUNT); ip_addr_t internetová_adresa; ip_addr_set_ip4_u32(&internetová_adresa, lwip_htonl(adresa));
    err_t 보조항목 = udp_sendto(reťazec_údaje->datagram_riadenie, údaje_pozícia, &internetová_adresa, číslo_portu); pbuf_free(údaje_pozícia); return 보조항목 ? chybové_číslo(보조항목) : (int)položka_COUNT;
}
int dostať_datagram(int Súbor_rukoväť, void *údaje, unsigned položka_COUNT) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje || reťazec_údaje->Typ_oblasť != 2) return -9;
    if (!reťazec_údaje->položka_COUNT_8f7753a1) return -11; unsigned v_termíne_splatnosti_pozícia = reťazec_údaje->predný_položka;
    if (položka_COUNT > reťazec_údaje->길이목록[v_termíne_splatnosti_pozícia]) položka_COUNT = reťazec_údaje->길이목록[v_termíne_splatnosti_pozícia]; memcpy(údaje, reťazec_údaje->údaje + v_termíne_splatnosti_pozícia * 512, položka_COUNT);
    reťazec_údaje->상대창구번호 = reťazec_údaje->접속번호들[v_termíne_splatnosti_pozícia]; reťazec_údaje->partnerský_uzol_adresa = reťazec_údaje->주소목록[v_termíne_splatnosti_pozícia]; reťazec_údaje->predný_položka = (v_termíne_splatnosti_pozícia + 1) % 4; reťazec_údaje->položka_COUNT_8f7753a1--; return položka_COUNT;
}
unsigned sieť_číslo_portu(int Súbor_rukoväť) { soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); return !reťazec_údaje ? 0 : reťazec_údaje->kontakt_riadenie ? reťazec_údaje->kontakt_riadenie->local_port : reťazec_údaje->datagram_riadenie ? reťazec_údaje->datagram_riadenie->local_port : 0; }
unsigned partnerský_uzol_číslo_portu(int Súbor_rukoväť) { soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); return reťazec_údaje ? reťazec_údaje->상대창구번호 : 0; }
uint32_t NET_partnerský_uzol_adresa(int Súbor_rukoväť) { soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); return reťazec_údaje ? reťazec_údaje->partnerský_uzol_adresa : 0; }
void Zavrieť_sieť(int Súbor_rukoväť) {
    soket_účastník_3db661a2 *reťazec_údaje = načítať_VALUE(Súbor_rukoväť); if (!reťazec_údaje) return;
    if (reťazec_údaje->dostať_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].Typ_oblasť && 통신끝점들[순번].Informačné_systémy_čakajúci == Súbor_rukoväť) Zavrieť_sieť(순번);
    if (reťazec_údaje->kontakt_riadenie) {
        tcp_arg(reťazec_údaje->kontakt_riadenie, 0); if (reťazec_údaje->dostať_port) tcp_accept(reťazec_údaje->kontakt_riadenie, 0); else { tcp_recv(reťazec_údaje->kontakt_riadenie, 0); tcp_err(reťazec_údaje->kontakt_riadenie, 0); }
        if (tcp_close(reťazec_údaje->kontakt_riadenie) != ERR_OK) tcp_abort(reťazec_údaje->kontakt_riadenie);
    }
    if (reťazec_údaje->datagram_riadenie) udp_remove(reťazec_údaje->datagram_riadenie); reťazec_údaje->Typ_oblasť = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || vzorkovanie) return; vzorkovanie = 1;
    if(používať_drôtový_sieť)유선망살피기(&kontakt_telefón);
    for (unsigned rozpočet = 0; !používať_drôtový_sieť && rozpočet < 4096 && (počítač_register(보조장치 + 0x54) & 1); rozpočet++) {
        unsigned bod_kódu = počítač_register(보조장치 + 0x40) & 255;
        if (bod_kódu == 192) {
            if (dostať_použitie && !dostať_Chyba && !수신탈출) {
                struct pbuf *údaje_pozícia = pbuf_alloc(PBUF_RAW, dostať_použitie, PBUF_POOL);
                if (údaje_pozícia) { RECEIVED_datagram_COUNT++; RECEIVED_Byte_COUNT += dostať_použitie; pbuf_take(údaje_pozícia, dostať_dátová_medzipamäť, dostať_použitie); if (kontakt_telefón.input(údaje_pozícia, &kontakt_telefón) != ERR_OK) { 버린전문수++; pbuf_free(údaje_pozícia); } }
                else 버린전문수++;
            }
            else if (dostať_použitie) 버린전문수++;
            dostať_použitie = dostať_Chyba = 수신탈출 = 0;
        } else if (bod_kódu == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (bod_kódu != 220 && bod_kódu != 221) dostať_Chyba = 1; bod_kódu = bod_kódu == 220 ? 192 : 219; 수신탈출 = 0; }
            if (dostať_použitie < sizeof(dostať_dátová_medzipamäť)) dostať_dátová_medzipamäť[dostať_použitie++] = bod_kódu; else dostať_Chyba = 1;
        }
    }
    netif_poll(&kontakt_telefón); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned rozpočet = 0; rozpočet < 4096 && 송신개수 && (počítač_register(보조장치 + 0x54) & 0x20); rozpočet++) {
        počítač_register(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    vzorkovanie = 0;
}

/* Nastavenia·조회는 lwIP의 skutočný_údaje 인터페이스와 ukončiť_hovor_bod 표를 사용한다. */
uint32_t 망상태읽기(unsigned položka_VALUE, unsigned INDEX) {
    if(položka_VALUE==20)return používať_drôtový_sieť;
    if(položka_VALUE==21)return 준비됨&&netif_is_link_up(&kontakt_telefón);
    if(položka_VALUE==22)return používať_drôtový_sieť?유선망집계(5):0;
    if (!준비됨) return 0;
    if(používať_drôtový_sieť&&položka_VALUE>=4&&položka_VALUE<=8)return 유선망집계(položka_VALUE-4);
    if (položka_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_telefón)));
    if (položka_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&kontakt_telefón)));
    if (položka_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&kontakt_telefón)));
    if (položka_VALUE == 3) return netif_is_up(&kontakt_telefón) != 0;
    if (položka_VALUE == 4) return RECEIVED_datagram_COUNT;
    if (položka_VALUE == 5) return 보낸전문수;
    if (položka_VALUE == 6) return RECEIVED_Byte_COUNT;
    if (položka_VALUE == 7) return 보낸바이트수;
    if (položka_VALUE == 8) return 버린전문수;
    if (položka_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    soket_účastník_3db661a2 *ukončiť_hovor_bod = &통신끝점들[INDEX];
    if (položka_VALUE == 10) return ukončiť_hovor_bod->Typ_oblasť;
    if (!ukončiť_hovor_bod->Typ_oblasť) return 0;
    if (položka_VALUE == 11) return sieť_číslo_portu(INDEX);
    if (položka_VALUE == 12) return ukončiť_hovor_bod->partnerský_uzol_adresa;
    if (položka_VALUE == 13) return ukončiť_hovor_bod->상대창구번호;
    if (položka_VALUE == 14) return ukončiť_hovor_bod->dostať_port ? 1 : ukončiť_hovor_bod->Súbor_ukončiť_hovor ? 3 : ukončiť_hovor_bod->chyba ? 4 : ukončiť_hovor_bod->연결됨 ? 2 : 0;
    if (položka_VALUE == 15) return ukončiť_hovor_bod->položka_COUNT_8f7753a1;
    if (položka_VALUE == 16) {
        const ip_addr_t *adresa = ukončiť_hovor_bod->Typ_oblasť == 1 && ukončiť_hovor_bod->kontakt_riadenie ? &ukončiť_hovor_bod->kontakt_riadenie->local_ip :
            ukončiť_hovor_bod->Typ_oblasť == 2 && ukončiť_hovor_bod->datagram_riadenie ? &ukončiť_hovor_bod->datagram_riadenie->local_ip : 0;
        return adresa ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) : 0;
    }
    return 0;
}

int konfigurovať_sieť(unsigned Akcia, uint32_t adresa, uint32_t maska_VALUE, uint32_t brána_VALUE) {
    if (!준비됨) return -100;
    if (Akcia == 1) { netif_set_up(&kontakt_telefón); return 0; }
    if (Akcia == 2) { netif_set_down(&kontakt_telefón); return 0; }
    if (Akcia != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_VALUE, 같은 망의 선택적 predvolená_hodnota brána_VALUE. */
    uint32_t 뒤집은가림 = ~maska_VALUE;
    if (!maska_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !adresa || (adresa >> 24) == 127 ||
        (adresa >> 24) == 0 || (adresa >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(adresa & 뒤집은가림) || (adresa & 뒤집은가림) == 뒤집은가림)) ||
        (brána_VALUE && ((brána_VALUE & maska_VALUE) != (adresa & maska_VALUE) || brána_VALUE == adresa || (brána_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(brána_VALUE & 뒤집은가림) || (brána_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 adresa 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].Typ_oblasť &&
        !(통신끝점들[INDEX].dostať_port && 통신끝점들[INDEX].kontakt_riadenie && ip_addr_isany(&통신끝점들[INDEX].kontakt_riadenie->local_ip))) return -16;
    if(používať_drôtový_sieť)dhcp_stop(&kontakt_telefón);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(adresa)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(brána_VALUE));
    netif_set_addr(&kontakt_telefón, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *odpoveď_účastník;
static uint32_t test_adresa, test_čas, odpoveď_čas;
static unsigned test_SEQUENCE, test_identifikátor, odpoveď_SEQUENCE;
static int odpoveď_Stav;
static u8_t 응답받음(void *Argumenty, struct raw_pcb *ukončiť_hovor_bod, struct pbuf *údaje, const ip_addr_t *adresa) {
    (void)Argumenty; (void)ukončiť_hovor_bod;
    unsigned char 머리[20], odozva[16];
    if (odpoveď_Stav != -11 || údaje->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) != test_adresa || pbuf_copy_partial(údaje, 머리, 20, 0) != 20) return 0;
    unsigned Nadpis_zmeniť_veľkosť = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Nadpis_zmeniť_veľkosť < 20 || údaje->tot_len < Nadpis_zmeniť_veľkosť + 16 ||
        pbuf_copy_partial(údaje, odozva, 16, Nadpis_zmeniť_veľkosť) != 16 || odozva[0] || odozva[1] ||
        (((unsigned)odozva[4] << 8) | odozva[5]) != test_identifikátor ||
        (((unsigned)odozva[6] << 8) | odozva[7]) != test_SEQUENCE ||
        odozva[8] != 'J' || odozva[9] != 'K' || odozva[10] != 'O' || odozva[11] != 'S' ||
        (((uint32_t)odozva[12] << 24) | ((uint32_t)odozva[13] << 16) | ((uint32_t)odozva[14] << 8) | odozva[15]) != test_čas) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(údaje, Nadpis_zmeniť_veľkosť)) return 0;
    if (inet_chksum_pbuf(údaje)) { pbuf_add_header(údaje, Nadpis_zmeniť_veľkosť); return 0; }
    odpoveď_čas = (uint32_t)보드밀리초() - test_čas; odpoveď_SEQUENCE = 머리[8]; odpoveď_Stav = 0;
    pbuf_free(údaje); return 1;
}
int START_odpoveď_test(uint32_t adresa, unsigned poradie_VALUE) {
    if (!준비됨 || !netif_is_up(&kontakt_telefón)) return -100;
    if (!adresa || (adresa >> 28) >= 14 || adresa == 0xffffffffu) return -22;
    if (!odpoveď_účastník) { odpoveď_účastník = raw_new(IP_PROTO_ICMP); if (!odpoveď_účastník) return -12; raw_recv(odpoveď_účastník, 응답받음, 0); }
    test_adresa = adresa; test_SEQUENCE = poradie_VALUE & 65535; test_identifikátor = (test_identifikátor + 1) & 65535;
    test_čas = 보드밀리초(); odpoveď_Stav = -11; odpoveď_čas = odpoveď_SEQUENCE = 0;
    unsigned char údaje[32] = {8,0,0,0};
    údaje[4] = test_identifikátor >> 8; údaje[5] = test_identifikátor; údaje[6] = test_SEQUENCE >> 8; údaje[7] = test_SEQUENCE;
    údaje[8]='J'; údaje[9]='K'; údaje[10]='O'; údaje[11]='S';
    údaje[12]=test_čas >> 24; údaje[13]=test_čas >> 16; údaje[14]=test_čas >> 8; údaje[15]=test_čas;
    for (unsigned pozičný_index = 16; pozičný_index < sizeof(údaje); pozičný_index++) údaje[pozičný_index] = pozičný_index;
    uint16_t preverenie_kontrolný_súčet = inet_chksum(údaje, sizeof(údaje)); memcpy(údaje + 2, &preverenie_kontrolný_súčet, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(údaje), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, údaje, sizeof(údaje)); ip_addr_t cieľ_účastník; ip_addr_set_ip4_u32(&cieľ_účastník, lwip_htonl(adresa));
    err_t 처리값 = raw_sendto(odpoveď_účastník, datagram, &cieľ_účastník); pbuf_free(datagram);
    if (처리값) odpoveď_Stav = chybové_číslo(처리값);
    return 처리값 ? odpoveď_Stav : 0;
}
int 응답시험읽기(unsigned položka_VALUE) {
    통신망살피기();
    return položka_VALUE == 0 ? odpoveď_Stav : položka_VALUE == 1 ? (int)odpoveď_čas : položka_VALUE == 2 ? (int)odpoveď_SEQUENCE : -22;
}
