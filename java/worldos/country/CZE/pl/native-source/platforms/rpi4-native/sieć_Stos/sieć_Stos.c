#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "sieć_Stos.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../zdalny_WARTOŚĆ/zdalny_WARTOŚĆ.h"
#include "przewodowy_sieć.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define maszyna_rejestr(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif połączenie_urządzenie;
static int 준비됨, sondowanie;
static int używać_przewodowy_sieć;
static unsigned odbierać_użycie, 수신탈출, odbierać_błąd;
static unsigned char odbierać_bufor_danych[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t KWOTA_WYKUP_datagram_ILE_LICZB, 보낸전문수, KWOTA_WYKUP_bajt_ILE_LICZB, 보낸바이트수, 버린전문수;
typedef struct {
    int TYP_obszar, odbierać_port, systemy_informacyjne_oczekujący, 연결됨, Plik_Koniec, błąd;
    struct tcp_pcb *połączenie_kontrola;
    struct udp_pcb *datagram_kontrola;
    unsigned przód_wpis, wpis_ILE_LICZB;
    unsigned char dane[4096];
    unsigned 길이목록[4], 접속번호들[4], węzeł_równorzędny_uczestnik_identyfikator;
    uint32_t 주소목록[4], węzeł_równorzędny_ADRES;
} gniazdo_uczestnik_3db661a2;
static gniazdo_uczestnik_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int numer_błędu(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static gniazdo_uczestnik_3db661a2 *pobrać_WARTOŚĆ(int dojście_do_pliku) { return dojście_do_pliku >= 0 && dojście_do_pliku < 32 && 통신끝점들[dojście_do_pliku].TYP_obszar ? &통신끝점들[dojście_do_pliku] : 0; }
static int 예약하기(int TYP_obszar) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYP_obszar) {
        memset(&통신끝점들[순번], 0, sizeof(gniazdo_uczestnik_3db661a2)); 통신끝점들[순번].TYP_obszar = TYP_obszar; 통신끝점들[순번].systemy_informacyjne_oczekujący = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kod_znaku) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kod_znaku; }
static err_t produkt_wyjściowy(struct netif *towar_ILE_LICZB, struct pbuf *dane_stanowisko, const ip4_addr_t *Adres) {
    (void)towar_ILE_LICZB; (void)Adres;
    if (dane_stanowisko->tot_len > 1500 || 송신개수 + 2 * dane_stanowisko->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Dalej_przesunąć = dane_stanowisko; Dalej_przesunąć; Dalej_przesunąć = Dalej_przesunąć->next) for (unsigned 순번 = 0; 순번 < Dalej_przesunąć->len; 순번++) {
        unsigned kod_znaku = ((unsigned char *)Dalej_przesunąć->payload)[순번];
        if (kod_znaku == 192 || kod_znaku == 219) { 내보내기(219); 내보내기(kod_znaku == 192 ? 220 : 221); } else 내보내기(kod_znaku);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += dane_stanowisko->tot_len; return ERR_OK;
}
static err_t Przygotuj_CLR(struct netif *towar_ILE_LICZB) { towar_ILE_LICZB->name[0] = 's'; towar_ILE_LICZB->name[1] = 'l'; towar_ILE_LICZB->mtu = 1500; towar_ILE_LICZB->output = produkt_wyjściowy; return ERR_OK; }
void Przygotuj_sieć(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    maszyna_rejestr(보조장치 + 4) |= 1; maszyna_rejestr(보조장치 + 0x60) = 0; maszyna_rejestr(보조장치 + 0x44) = 0;
    maszyna_rejestr(보조장치 + 0x48) = 0xc6; maszyna_rejestr(보조장치 + 0x4c) = 3; maszyna_rejestr(보조장치 + 0x68) = 270; maszyna_rejestr(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t adres_internetowy, maska_bitów, adres_bramy;
    używać_przewodowy_sieć=유선장치있음();
    ip4_addr_set_u32(&adres_internetowy, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&maska_bitów, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&adres_bramy, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&połączenie_urządzenie, &adres_internetowy, &maska_bitów, &adres_bramy, 0, używać_przewodowy_sieć?Przygotuj_przewodowy_sieć:Przygotuj_CLR, używać_przewodowy_sieć?ethernet_input:ip4_input))return;
    netif_set_default(&połączenie_urządzenie); netif_set_up(&połączenie_urządzenie);if(!używać_przewodowy_sieć)netif_set_link_up(&połączenie_urządzenie); 준비됨 = 1;
    Przygotuj_zdalny();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *dane_stanowisko, err_t błąd) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = 부가인수; (void)통신제어블록; (void)błąd;
    if (!dane_stanowisko) { ciąg_dane->Plik_Koniec = 1; return ERR_OK; }
    if (dane_stanowisko->tot_len > sizeof(ciąg_dane->dane) - ciąg_dane->wpis_ILE_LICZB) return ERR_MEM;
    unsigned bieżący_stanowisko = (ciąg_dane->przód_wpis + ciąg_dane->wpis_ILE_LICZB) % sizeof(ciąg_dane->dane);
    for (struct pbuf *Dalej_przesunąć = dane_stanowisko; Dalej_przesunąć; Dalej_przesunąć = Dalej_przesunąć->next) for (unsigned 순번 = 0; 순번 < Dalej_przesunąć->len; 순번++) {
        ciąg_dane->dane[bieżący_stanowisko] = ((unsigned char *)Dalej_przesunąć->payload)[순번]; bieżący_stanowisko = (bieżący_stanowisko + 1) % sizeof(ciąg_dane->dane);
    }
    ciąg_dane->wpis_ILE_LICZB += dane_stanowisko->tot_len; pbuf_free(dane_stanowisko); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t błąd) { gniazdo_uczestnik_3db661a2 *ciąg_dane = 부가인수; ciąg_dane->połączenie_kontrola = 0; ciąg_dane->błąd = numer_błędu(błąd); }
static void 되부름목록(gniazdo_uczestnik_3db661a2 *ciąg_dane) { tcp_arg(ciąg_dane->połączenie_kontrola, ciąg_dane); tcp_recv(ciąg_dane->połączenie_kontrola, 수신됨); tcp_err(ciąg_dane->połączenie_kontrola, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t błąd) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = 부가인수; (void)통신제어블록; if (błąd) ciąg_dane->błąd = numer_błędu(błąd); else ciąg_dane->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t błąd) {
    gniazdo_uczestnik_3db661a2 *nadrzędny = 부가인수; if (błąd) return błąd;
    int dojście_do_pliku = 예약하기(1); if (dojście_do_pliku < 0) return ERR_MEM;
    gniazdo_uczestnik_3db661a2 *ciąg_dane = &통신끝점들[dojście_do_pliku]; ciąg_dane->połączenie_kontrola = 통신제어블록; ciąg_dane->연결됨 = 1; ciąg_dane->systemy_informacyjne_oczekujący = (int)(nadrzędny - 통신끝점들);
    ciąg_dane->węzeł_równorzędny_ADRES = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); ciąg_dane->węzeł_równorzędny_uczestnik_identyfikator = 통신제어블록->remote_port;
    되부름목록(ciąg_dane); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *dane_stanowisko, const ip_addr_t *Adres, u16_t numer_portu) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = 부가인수; (void)통신제어블록;
    if (ciąg_dane->wpis_ILE_LICZB < 4 && dane_stanowisko->tot_len <= 512) {
        unsigned indeks_pozycji = (ciąg_dane->przód_wpis + ciąg_dane->wpis_ILE_LICZB) % 4;
        pbuf_copy_partial(dane_stanowisko, ciąg_dane->dane + indeks_pozycji * 512, dane_stanowisko->tot_len, 0);
        ciąg_dane->길이목록[indeks_pozycji] = dane_stanowisko->tot_len; ciąg_dane->접속번호들[indeks_pozycji] = numer_portu;
        ciąg_dane->주소목록[indeks_pozycji] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adres))); ciąg_dane->wpis_ILE_LICZB++;
    }
    pbuf_free(dane_stanowisko);
}
int Twórca_gniazdo_uczestnik(int TYP_obszar) {
    if (!준비됨) return -100;
    if (TYP_obszar != 1 && TYP_obszar != 2) return -93;
    int dojście_do_pliku = 예약하기(TYP_obszar); if (dojście_do_pliku < 0) return dojście_do_pliku;
    gniazdo_uczestnik_3db661a2 *ciąg_dane = &통신끝점들[dojście_do_pliku];
    if (TYP_obszar == 1) { ciąg_dane->połączenie_kontrola = tcp_new(); if (ciąg_dane->połączenie_kontrola) 되부름목록(ciąg_dane); }
    else { ciąg_dane->datagram_kontrola = udp_new(); if (ciąg_dane->datagram_kontrola) udp_recv(ciąg_dane->datagram_kontrola, datagram, ciąg_dane); }
    if (!ciąg_dane->połączenie_kontrola && !ciąg_dane->datagram_kontrola) { ciąg_dane->TYP_obszar = 0; return -12; } return dojście_do_pliku;
}
int NET_BIND(int dojście_do_pliku, uint32_t Adres, unsigned numer_portu) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane) return -9;
    if (numer_portu > 65535 || (Adres && Adres != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&połączenie_urządzenie))) && Adres != 0x7f000001)) return -99;
    ip_addr_t adres_internetowy; ip_addr_set_ip4_u32(&adres_internetowy, lwip_htonl(Adres));
    err_t 보조항목 = ciąg_dane->TYP_obszar == 1 ? tcp_bind(ciąg_dane->połączenie_kontrola, &adres_internetowy, numer_portu) : udp_bind(ciąg_dane->datagram_kontrola, &adres_internetowy, numer_portu); return 보조항목 ? numer_błędu(보조항목) : 0;
}
void 통신주소재사용(int dojście_do_pliku) { gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (ciąg_dane && ciąg_dane->połączenie_kontrola) ip_set_option(ciąg_dane->połączenie_kontrola, SOF_REUSEADDR); }
int NET_nasłuchiwać(int dojście_do_pliku) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane || ciąg_dane->TYP_obszar != 1) return -9;
    if (ciąg_dane->odbierać_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(ciąg_dane->połączenie_kontrola, 4, &보조항목);
    if (!통신제어블록) return numer_błędu(보조항목); ciąg_dane->połączenie_kontrola = 통신제어블록; ciąg_dane->odbierać_port = 1; tcp_arg(통신제어블록, ciąg_dane); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_POŁĄCZ(int dojście_do_pliku, uint32_t Adres, unsigned numer_portu) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane || ciąg_dane->TYP_obszar != 1) return -9;
    if (ciąg_dane->błąd) return ciąg_dane->błąd;
    if (ciąg_dane->연결됨) return 0;
    if (ciąg_dane->węzeł_równorzędny_uczestnik_identyfikator) return -115;
    if (!numer_portu || numer_portu > 65535 || !Adres) return -22;
    ip_addr_t adres_internetowy; ip_addr_set_ip4_u32(&adres_internetowy, lwip_htonl(Adres));
    ciąg_dane->węzeł_równorzędny_ADRES = Adres; ciąg_dane->węzeł_równorzędny_uczestnik_identyfikator = numer_portu;
    err_t 보조항목 = tcp_connect(ciąg_dane->połączenie_kontrola, &adres_internetowy, numer_portu, 연결됨); return 보조항목 ? numer_błędu(보조항목) : -115;
}
int NET_akceptować(int dojście_do_pliku) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane || !ciąg_dane->odbierać_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYP_obszar == 1 && 통신끝점들[순번].systemy_informacyjne_oczekujący == dojście_do_pliku) { 통신끝점들[순번].systemy_informacyjne_oczekujący = -1; return 순번; }
    return -11;
}
int 통신읽기(int dojście_do_pliku, void *dane, unsigned towar_ILE_LICZB) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane || ciąg_dane->TYP_obszar != 1) return -9;
    if (!towar_ILE_LICZB) return 0; if (!ciąg_dane->wpis_ILE_LICZB) return ciąg_dane->błąd ? ciąg_dane->błąd : ciąg_dane->Plik_Koniec ? 0 : -11;
    if (towar_ILE_LICZB > ciąg_dane->wpis_ILE_LICZB) towar_ILE_LICZB = ciąg_dane->wpis_ILE_LICZB;
    for (unsigned 순번 = 0; 순번 < towar_ILE_LICZB; 순번++) { ((unsigned char *)dane)[순번] = ciąg_dane->dane[ciąg_dane->przód_wpis]; ciąg_dane->przód_wpis = (ciąg_dane->przód_wpis + 1) % sizeof(ciąg_dane->dane); }
    ciąg_dane->wpis_ILE_LICZB -= towar_ILE_LICZB; if (ciąg_dane->połączenie_kontrola) tcp_recved(ciąg_dane->połączenie_kontrola, towar_ILE_LICZB); return towar_ILE_LICZB;
}
int NET_zapis(int dojście_do_pliku, const void *dane, unsigned towar_ILE_LICZB) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane || ciąg_dane->TYP_obszar != 1) return -9;
    if (ciąg_dane->błąd) return ciąg_dane->błąd; if (!ciąg_dane->połączenie_kontrola || !ciąg_dane->연결됨) return -107;
    if (!towar_ILE_LICZB) return 0; if (towar_ILE_LICZB > tcp_sndbuf(ciąg_dane->połączenie_kontrola)) towar_ILE_LICZB = tcp_sndbuf(ciąg_dane->połączenie_kontrola);
    if (!towar_ILE_LICZB) return -11; if (towar_ILE_LICZB > 1024) towar_ILE_LICZB = 1024;
    err_t 보조항목 = tcp_write(ciąg_dane->połączenie_kontrola, dane, towar_ILE_LICZB, TCP_WRITE_FLAG_COPY); if (보조항목) return numer_błędu(보조항목);
    tcp_output(ciąg_dane->połączenie_kontrola); return towar_ILE_LICZB;
}
int wysłać_datagram(int dojście_do_pliku, const void *dane, unsigned towar_ILE_LICZB, uint32_t Adres, unsigned numer_portu) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane || ciąg_dane->TYP_obszar != 2) return -9;
    if (towar_ILE_LICZB > 512) return -90; if (!numer_portu || numer_portu > 65535) return -22;
    struct pbuf *dane_stanowisko = pbuf_alloc(PBUF_TRANSPORT, towar_ILE_LICZB, PBUF_RAM); if (!dane_stanowisko) return -11;
    pbuf_take(dane_stanowisko, dane, towar_ILE_LICZB); ip_addr_t adres_internetowy; ip_addr_set_ip4_u32(&adres_internetowy, lwip_htonl(Adres));
    err_t 보조항목 = udp_sendto(ciąg_dane->datagram_kontrola, dane_stanowisko, &adres_internetowy, numer_portu); pbuf_free(dane_stanowisko); return 보조항목 ? numer_błędu(보조항목) : (int)towar_ILE_LICZB;
}
int odbierać_datagram(int dojście_do_pliku, void *dane, unsigned towar_ILE_LICZB) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane || ciąg_dane->TYP_obszar != 2) return -9;
    if (!ciąg_dane->wpis_ILE_LICZB) return -11; unsigned bieżący_stanowisko = ciąg_dane->przód_wpis;
    if (towar_ILE_LICZB > ciąg_dane->길이목록[bieżący_stanowisko]) towar_ILE_LICZB = ciąg_dane->길이목록[bieżący_stanowisko]; memcpy(dane, ciąg_dane->dane + bieżący_stanowisko * 512, towar_ILE_LICZB);
    ciąg_dane->węzeł_równorzędny_uczestnik_identyfikator = ciąg_dane->접속번호들[bieżący_stanowisko]; ciąg_dane->węzeł_równorzędny_ADRES = ciąg_dane->주소목록[bieżący_stanowisko]; ciąg_dane->przód_wpis = (bieżący_stanowisko + 1) % 4; ciąg_dane->wpis_ILE_LICZB--; return towar_ILE_LICZB;
}
unsigned sieć_numer_portu(int dojście_do_pliku) { gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); return !ciąg_dane ? 0 : ciąg_dane->połączenie_kontrola ? ciąg_dane->połączenie_kontrola->local_port : ciąg_dane->datagram_kontrola ? ciąg_dane->datagram_kontrola->local_port : 0; }
unsigned węzeł_równorzędny_numer_portu(int dojście_do_pliku) { gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); return ciąg_dane ? ciąg_dane->węzeł_równorzędny_uczestnik_identyfikator : 0; }
uint32_t NET_węzeł_równorzędny_ADRES(int dojście_do_pliku) { gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); return ciąg_dane ? ciąg_dane->węzeł_równorzędny_ADRES : 0; }
void Zamknij_sieć(int dojście_do_pliku) {
    gniazdo_uczestnik_3db661a2 *ciąg_dane = pobrać_WARTOŚĆ(dojście_do_pliku); if (!ciąg_dane) return;
    if (ciąg_dane->odbierać_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYP_obszar && 통신끝점들[순번].systemy_informacyjne_oczekujący == dojście_do_pliku) Zamknij_sieć(순번);
    if (ciąg_dane->połączenie_kontrola) {
        tcp_arg(ciąg_dane->połączenie_kontrola, 0); if (ciąg_dane->odbierać_port) tcp_accept(ciąg_dane->połączenie_kontrola, 0); else { tcp_recv(ciąg_dane->połączenie_kontrola, 0); tcp_err(ciąg_dane->połączenie_kontrola, 0); }
        if (tcp_close(ciąg_dane->połączenie_kontrola) != ERR_OK) tcp_abort(ciąg_dane->połączenie_kontrola);
    }
    if (ciąg_dane->datagram_kontrola) udp_remove(ciąg_dane->datagram_kontrola); ciąg_dane->TYP_obszar = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || sondowanie) return; sondowanie = 1;
    if(używać_przewodowy_sieć)유선망살피기(&połączenie_urządzenie);
    for (unsigned budżet = 0; !używać_przewodowy_sieć && budżet < 4096 && (maszyna_rejestr(보조장치 + 0x54) & 1); budżet++) {
        unsigned kod_znaku = maszyna_rejestr(보조장치 + 0x40) & 255;
        if (kod_znaku == 192) {
            if (odbierać_użycie && !odbierać_błąd && !수신탈출) {
                struct pbuf *dane_stanowisko = pbuf_alloc(PBUF_RAW, odbierać_użycie, PBUF_POOL);
                if (dane_stanowisko) { KWOTA_WYKUP_datagram_ILE_LICZB++; KWOTA_WYKUP_bajt_ILE_LICZB += odbierać_użycie; pbuf_take(dane_stanowisko, odbierać_bufor_danych, odbierać_użycie); if (połączenie_urządzenie.input(dane_stanowisko, &połączenie_urządzenie) != ERR_OK) { 버린전문수++; pbuf_free(dane_stanowisko); } }
                else 버린전문수++;
            }
            else if (odbierać_użycie) 버린전문수++;
            odbierać_użycie = odbierać_błąd = 수신탈출 = 0;
        } else if (kod_znaku == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kod_znaku != 220 && kod_znaku != 221) odbierać_błąd = 1; kod_znaku = kod_znaku == 220 ? 192 : 219; 수신탈출 = 0; }
            if (odbierać_użycie < sizeof(odbierać_bufor_danych)) odbierać_bufor_danych[odbierać_użycie++] = kod_znaku; else odbierać_błąd = 1;
        }
    }
    netif_poll(&połączenie_urządzenie); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budżet = 0; budżet < 4096 && 송신개수 && (maszyna_rejestr(보조장치 + 0x54) & 0x20); budżet++) {
        maszyna_rejestr(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    sondowanie = 0;
}

/* Ustawienia·조회는 lwIP의 rzeczywisty_dane 인터페이스와 Koniec_punkt 표를 사용한다. */
uint32_t 망상태읽기(unsigned wpis_WARTOŚĆ, unsigned INDEKS) {
    if(wpis_WARTOŚĆ==20)return używać_przewodowy_sieć;
    if(wpis_WARTOŚĆ==21)return 준비됨&&netif_is_link_up(&połączenie_urządzenie);
    if(wpis_WARTOŚĆ==22)return używać_przewodowy_sieć?przewodowy_sieć_Statystyka(5):0;
    if (!준비됨) return 0;
    if(używać_przewodowy_sieć&&wpis_WARTOŚĆ>=4&&wpis_WARTOŚĆ<=8)return przewodowy_sieć_Statystyka(wpis_WARTOŚĆ-4);
    if (wpis_WARTOŚĆ == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&połączenie_urządzenie)));
    if (wpis_WARTOŚĆ == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&połączenie_urządzenie)));
    if (wpis_WARTOŚĆ == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&połączenie_urządzenie)));
    if (wpis_WARTOŚĆ == 3) return netif_is_up(&połączenie_urządzenie) != 0;
    if (wpis_WARTOŚĆ == 4) return KWOTA_WYKUP_datagram_ILE_LICZB;
    if (wpis_WARTOŚĆ == 5) return 보낸전문수;
    if (wpis_WARTOŚĆ == 6) return KWOTA_WYKUP_bajt_ILE_LICZB;
    if (wpis_WARTOŚĆ == 7) return 보낸바이트수;
    if (wpis_WARTOŚĆ == 8) return 버린전문수;
    if (wpis_WARTOŚĆ == 9) return 송신개수;
    if (INDEKS >= 32) return 0;
    gniazdo_uczestnik_3db661a2 *Koniec_punkt = &통신끝점들[INDEKS];
    if (wpis_WARTOŚĆ == 10) return Koniec_punkt->TYP_obszar;
    if (!Koniec_punkt->TYP_obszar) return 0;
    if (wpis_WARTOŚĆ == 11) return sieć_numer_portu(INDEKS);
    if (wpis_WARTOŚĆ == 12) return Koniec_punkt->węzeł_równorzędny_ADRES;
    if (wpis_WARTOŚĆ == 13) return Koniec_punkt->węzeł_równorzędny_uczestnik_identyfikator;
    if (wpis_WARTOŚĆ == 14) return Koniec_punkt->odbierać_port ? 1 : Koniec_punkt->Plik_Koniec ? 3 : Koniec_punkt->błąd ? 4 : Koniec_punkt->연결됨 ? 2 : 0;
    if (wpis_WARTOŚĆ == 15) return Koniec_punkt->wpis_ILE_LICZB;
    if (wpis_WARTOŚĆ == 16) {
        const ip_addr_t *Adres = Koniec_punkt->TYP_obszar == 1 && Koniec_punkt->połączenie_kontrola ? &Koniec_punkt->połączenie_kontrola->local_ip :
            Koniec_punkt->TYP_obszar == 2 && Koniec_punkt->datagram_kontrola ? &Koniec_punkt->datagram_kontrola->local_ip : 0;
        return Adres ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adres))) : 0;
    }
    return 0;
}

int konfigurować_sieć(unsigned Akcja, uint32_t Adres, uint32_t maska_WARTOŚĆ, uint32_t brama_WARTOŚĆ) {
    if (!준비됨) return -100;
    if (Akcja == 1) { netif_set_up(&połączenie_urządzenie); return 0; }
    if (Akcja == 2) { netif_set_down(&połączenie_urządzenie); return 0; }
    if (Akcja != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_WARTOŚĆ, 같은 망의 선택적 wartość_domyślna brama_WARTOŚĆ. */
    uint32_t 뒤집은가림 = ~maska_WARTOŚĆ;
    if (!maska_WARTOŚĆ || (뒤집은가림 & (뒤집은가림 + 1)) || !Adres || (Adres >> 24) == 127 ||
        (Adres >> 24) == 0 || (Adres >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(Adres & 뒤집은가림) || (Adres & 뒤집은가림) == 뒤집은가림)) ||
        (brama_WARTOŚĆ && ((brama_WARTOŚĆ & maska_WARTOŚĆ) != (Adres & maska_WARTOŚĆ) || brama_WARTOŚĆ == Adres || (brama_WARTOŚĆ >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(brama_WARTOŚĆ & 뒤집은가림) || (brama_WARTOŚĆ & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 Adres 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEKS = 0; INDEKS < 32; INDEKS++) if (통신끝점들[INDEKS].TYP_obszar &&
        !(통신끝점들[INDEKS].odbierać_port && 통신끝점들[INDEKS].połączenie_kontrola && ip_addr_isany(&통신끝점들[INDEKS].połączenie_kontrola->local_ip))) return -16;
    if(używać_przewodowy_sieć)dhcp_stop(&połączenie_urządzenie);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(Adres)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_WARTOŚĆ)); ip4_addr_set_u32(&새관문, lwip_htonl(brama_WARTOŚĆ));
    netif_set_addr(&połączenie_urządzenie, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *odpowiedź_uczestnik;
static uint32_t test_ADRES, test_CZAS, czas_odpowiedzi;
static unsigned test_SEKWENCJA, test_identyfikator, odpowiedź_SEKWENCJA;
static int odpowiedź_Stan;
static u8_t 응답받음(void *argumenty, struct raw_pcb *Koniec_punkt, struct pbuf *dane, const ip_addr_t *Adres) {
    (void)argumenty; (void)Koniec_punkt;
    unsigned char 머리[20], odpowiedź[16];
    if (odpowiedź_Stan != -11 || dane->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adres))) != test_ADRES || pbuf_copy_partial(dane, 머리, 20, 0) != 20) return 0;
    unsigned Nagłówek_zmienić_rozmiar = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Nagłówek_zmienić_rozmiar < 20 || dane->tot_len < Nagłówek_zmienić_rozmiar + 16 ||
        pbuf_copy_partial(dane, odpowiedź, 16, Nagłówek_zmienić_rozmiar) != 16 || odpowiedź[0] || odpowiedź[1] ||
        (((unsigned)odpowiedź[4] << 8) | odpowiedź[5]) != test_identyfikator ||
        (((unsigned)odpowiedź[6] << 8) | odpowiedź[7]) != test_SEKWENCJA ||
        odpowiedź[8] != 'J' || odpowiedź[9] != 'K' || odpowiedź[10] != 'O' || odpowiedź[11] != 'S' ||
        (((uint32_t)odpowiedź[12] << 24) | ((uint32_t)odpowiedź[13] << 16) | ((uint32_t)odpowiedź[14] << 8) | odpowiedź[15]) != test_CZAS) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(dane, Nagłówek_zmienić_rozmiar)) return 0;
    if (inet_chksum_pbuf(dane)) { pbuf_add_header(dane, Nagłówek_zmienić_rozmiar); return 0; }
    czas_odpowiedzi = (uint32_t)보드밀리초() - test_CZAS; odpowiedź_SEKWENCJA = 머리[8]; odpowiedź_Stan = 0;
    pbuf_free(dane); return 1;
}
int START_odpowiedź_test(uint32_t Adres, unsigned zamówić_WARTOŚĆ) {
    if (!준비됨 || !netif_is_up(&połączenie_urządzenie)) return -100;
    if (!Adres || (Adres >> 28) >= 14 || Adres == 0xffffffffu) return -22;
    if (!odpowiedź_uczestnik) { odpowiedź_uczestnik = raw_new(IP_PROTO_ICMP); if (!odpowiedź_uczestnik) return -12; raw_recv(odpowiedź_uczestnik, 응답받음, 0); }
    test_ADRES = Adres; test_SEKWENCJA = zamówić_WARTOŚĆ & 65535; test_identyfikator = (test_identyfikator + 1) & 65535;
    test_CZAS = 보드밀리초(); odpowiedź_Stan = -11; czas_odpowiedzi = odpowiedź_SEKWENCJA = 0;
    unsigned char dane[32] = {8,0,0,0};
    dane[4] = test_identyfikator >> 8; dane[5] = test_identyfikator; dane[6] = test_SEKWENCJA >> 8; dane[7] = test_SEKWENCJA;
    dane[8]='J'; dane[9]='K'; dane[10]='O'; dane[11]='S';
    dane[12]=test_CZAS >> 24; dane[13]=test_CZAS >> 16; dane[14]=test_CZAS >> 8; dane[15]=test_CZAS;
    for (unsigned indeks_pozycji = 16; indeks_pozycji < sizeof(dane); indeks_pozycji++) dane[indeks_pozycji] = indeks_pozycji;
    uint16_t weryfikacja_suma_kontrolna = inet_chksum(dane, sizeof(dane)); memcpy(dane + 2, &weryfikacja_suma_kontrolna, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(dane), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, dane, sizeof(dane)); ip_addr_t cel_uczestnik; ip_addr_set_ip4_u32(&cel_uczestnik, lwip_htonl(Adres));
    err_t 처리값 = raw_sendto(odpowiedź_uczestnik, datagram, &cel_uczestnik); pbuf_free(datagram);
    if (처리값) odpowiedź_Stan = numer_błędu(처리값);
    return 처리값 ? odpowiedź_Stan : 0;
}
int 응답시험읽기(unsigned wpis_WARTOŚĆ) {
    통신망살피기();
    return wpis_WARTOŚĆ == 0 ? odpowiedź_Stan : wpis_WARTOŚĆ == 1 ? (int)czas_odpowiedzi : wpis_WARTOŚĆ == 2 ? (int)odpowiedź_SEKWENCJA : -22;
}
