#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "síť_Štos.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../vzdálený_HODNOTA/vzdálený_HODNOTA.h"
#include "drátový_síť.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define počítač_registr(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif kontakt_mobilní;
static int 준비됨, cyklické_dotazování;
static int použít_drátový_síť;
static unsigned dostat_využití, 수신탈출, dostat_chyba;
static unsigned char dostat_vyrovnávací_paměť_dat[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_datagram_POČET, 보낸전문수, RECEIVED_bajt_POČET, 보낸바이트수, 버린전문수;
typedef struct {
    int TYP_oblast, dostat_port, informační_systémy_probíhá, 연결됨, Soubor_konec, chyba;
    struct tcp_pcb *kontakt_řízení;
    struct udp_pcb *datagram_řízení;
    unsigned přední_fotoaparát_položka, položka_POČET;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], partner_účastník_číslo;
    uint32_t 주소목록[4], partner_ODKAZ;
} soket_účastník_3db661a2;
static soket_účastník_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int číslo_chyby(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static soket_účastník_3db661a2 *get_HODNOTA(int popisovač_souboru) { return popisovač_souboru >= 0 && popisovač_souboru < 32 && 통신끝점들[popisovač_souboru].TYP_oblast ? &통신끝점들[popisovač_souboru] : 0; }
static int 예약하기(int TYP_oblast) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYP_oblast) {
        memset(&통신끝점들[순번], 0, sizeof(soket_účastník_3db661a2)); 통신끝점들[순번].TYP_oblast = TYP_oblast; 통신끝점들[순번].informační_systémy_probíhá = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned bod_kódu) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = bod_kódu; }
static err_t výstup(struct netif *zboží_POČET, struct pbuf *data_pozice, const ip4_addr_t *Adresa) {
    (void)zboží_POČET; (void)Adresa;
    if (data_pozice->tot_len > 1500 || 송신개수 + 2 * data_pozice->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Další_POSUN = data_pozice; Další_POSUN; Další_POSUN = Další_POSUN->next) for (unsigned 순번 = 0; 순번 < Další_POSUN->len; 순번++) {
        unsigned bod_kódu = ((unsigned char *)Další_POSUN->payload)[순번];
        if (bod_kódu == 192 || bod_kódu == 219) { 내보내기(219); 내보내기(bod_kódu == 192 ? 220 : 221); } else 내보내기(bod_kódu);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_pozice->tot_len; return ERR_OK;
}
static err_t Připravit_CLR(struct netif *zboží_POČET) { zboží_POČET->name[0] = 's'; zboží_POČET->name[1] = 'l'; zboží_POČET->mtu = 1500; zboží_POČET->output = výstup; return ERR_OK; }
void Připravit_síť(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    počítač_registr(보조장치 + 4) |= 1; počítač_registr(보조장치 + 0x60) = 0; počítač_registr(보조장치 + 0x44) = 0;
    počítač_registr(보조장치 + 0x48) = 0xc6; počítač_registr(보조장치 + 0x4c) = 3; počítač_registr(보조장치 + 0x68) = 270; počítač_registr(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetová_adresa, bitová_maska, adresa_brány;
    použít_drátový_síť=유선장치있음();
    ip4_addr_set_u32(&internetová_adresa, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitová_maska, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&adresa_brány, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&kontakt_mobilní, &internetová_adresa, &bitová_maska, &adresa_brány, 0, použít_drátový_síť?Připravit_drátový_síť:Připravit_CLR, použít_drátový_síť?ethernet_input:ip4_input))return;
    netif_set_default(&kontakt_mobilní); netif_set_up(&kontakt_mobilní);if(!použít_drátový_síť)netif_set_link_up(&kontakt_mobilní); 준비됨 = 1;
    Připravit_vzdálený();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *data_pozice, err_t chyba) {
    soket_účastník_3db661a2 *řetězec_data = 부가인수; (void)통신제어블록; (void)chyba;
    if (!data_pozice) { řetězec_data->Soubor_konec = 1; return ERR_OK; }
    if (data_pozice->tot_len > sizeof(řetězec_data->data) - řetězec_data->položka_POČET) return ERR_MEM;
    unsigned dobrá_pozice = (řetězec_data->přední_fotoaparát_položka + řetězec_data->položka_POČET) % sizeof(řetězec_data->data);
    for (struct pbuf *Další_POSUN = data_pozice; Další_POSUN; Další_POSUN = Další_POSUN->next) for (unsigned 순번 = 0; 순번 < Další_POSUN->len; 순번++) {
        řetězec_data->data[dobrá_pozice] = ((unsigned char *)Další_POSUN->payload)[순번]; dobrá_pozice = (dobrá_pozice + 1) % sizeof(řetězec_data->data);
    }
    řetězec_data->položka_POČET += data_pozice->tot_len; pbuf_free(data_pozice); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t chyba) { soket_účastník_3db661a2 *řetězec_data = 부가인수; řetězec_data->kontakt_řízení = 0; řetězec_data->chyba = číslo_chyby(chyba); }
static void 되부름목록(soket_účastník_3db661a2 *řetězec_data) { tcp_arg(řetězec_data->kontakt_řízení, řetězec_data); tcp_recv(řetězec_data->kontakt_řízení, 수신됨); tcp_err(řetězec_data->kontakt_řízení, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t chyba) {
    soket_účastník_3db661a2 *řetězec_data = 부가인수; (void)통신제어블록; if (chyba) řetězec_data->chyba = číslo_chyby(chyba); else řetězec_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t chyba) {
    soket_účastník_3db661a2 *nadřazený = 부가인수; if (chyba) return chyba;
    int popisovač_souboru = 예약하기(1); if (popisovač_souboru < 0) return ERR_MEM;
    soket_účastník_3db661a2 *řetězec_data = &통신끝점들[popisovač_souboru]; řetězec_data->kontakt_řízení = 통신제어블록; řetězec_data->연결됨 = 1; řetězec_data->informační_systémy_probíhá = (int)(nadřazený - 통신끝점들);
    řetězec_data->partner_ODKAZ = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); řetězec_data->partner_účastník_číslo = 통신제어블록->remote_port;
    되부름목록(řetězec_data); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *data_pozice, const ip_addr_t *Adresa, u16_t číslo_portu) {
    soket_účastník_3db661a2 *řetězec_data = 부가인수; (void)통신제어블록;
    if (řetězec_data->položka_POČET < 4 && data_pozice->tot_len <= 512) {
        unsigned poziční_index = (řetězec_data->přední_fotoaparát_položka + řetězec_data->položka_POČET) % 4;
        pbuf_copy_partial(data_pozice, řetězec_data->data + poziční_index * 512, data_pozice->tot_len, 0);
        řetězec_data->길이목록[poziční_index] = data_pozice->tot_len; řetězec_data->접속번호들[poziční_index] = číslo_portu;
        řetězec_data->주소목록[poziční_index] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adresa))); řetězec_data->položka_POČET++;
    }
    pbuf_free(data_pozice);
}
int Create_soket_účastník(int TYP_oblast) {
    if (!준비됨) return -100;
    if (TYP_oblast != 1 && TYP_oblast != 2) return -93;
    int popisovač_souboru = 예약하기(TYP_oblast); if (popisovač_souboru < 0) return popisovač_souboru;
    soket_účastník_3db661a2 *řetězec_data = &통신끝점들[popisovač_souboru];
    if (TYP_oblast == 1) { řetězec_data->kontakt_řízení = tcp_new(); if (řetězec_data->kontakt_řízení) 되부름목록(řetězec_data); }
    else { řetězec_data->datagram_řízení = udp_new(); if (řetězec_data->datagram_řízení) udp_recv(řetězec_data->datagram_řízení, datagram, řetězec_data); }
    if (!řetězec_data->kontakt_řízení && !řetězec_data->datagram_řízení) { řetězec_data->TYP_oblast = 0; return -12; } return popisovač_souboru;
}
int čistý_vázat(int popisovač_souboru, uint32_t Adresa, unsigned číslo_portu) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data) return -9;
    if (číslo_portu > 65535 || (Adresa && Adresa != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_mobilní))) && Adresa != 0x7f000001)) return -99;
    ip_addr_t internetová_adresa; ip_addr_set_ip4_u32(&internetová_adresa, lwip_htonl(Adresa));
    err_t 보조항목 = řetězec_data->TYP_oblast == 1 ? tcp_bind(řetězec_data->kontakt_řízení, &internetová_adresa, číslo_portu) : udp_bind(řetězec_data->datagram_řízení, &internetová_adresa, číslo_portu); return 보조항목 ? číslo_chyby(보조항목) : 0;
}
void 통신주소재사용(int popisovač_souboru) { soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (řetězec_data && řetězec_data->kontakt_řízení) ip_set_option(řetězec_data->kontakt_řízení, SOF_REUSEADDR); }
int čistý_naslouchat(int popisovač_souboru) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data || řetězec_data->TYP_oblast != 1) return -9;
    if (řetězec_data->dostat_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(řetězec_data->kontakt_řízení, 4, &보조항목);
    if (!통신제어블록) return číslo_chyby(보조항목); řetězec_data->kontakt_řízení = 통신제어블록; řetězec_data->dostat_port = 1; tcp_arg(통신제어블록, řetězec_data); tcp_accept(통신제어블록, 연결받음); return 0;
}
int čistý_spojit(int popisovač_souboru, uint32_t Adresa, unsigned číslo_portu) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data || řetězec_data->TYP_oblast != 1) return -9;
    if (řetězec_data->chyba) return řetězec_data->chyba;
    if (řetězec_data->연결됨) return 0;
    if (řetězec_data->partner_účastník_číslo) return -115;
    if (!číslo_portu || číslo_portu > 65535 || !Adresa) return -22;
    ip_addr_t internetová_adresa; ip_addr_set_ip4_u32(&internetová_adresa, lwip_htonl(Adresa));
    řetězec_data->partner_ODKAZ = Adresa; řetězec_data->partner_účastník_číslo = číslo_portu;
    err_t 보조항목 = tcp_connect(řetězec_data->kontakt_řízení, &internetová_adresa, číslo_portu, 연결됨); return 보조항목 ? číslo_chyby(보조항목) : -115;
}
int čistý_přijmout(int popisovač_souboru) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data || !řetězec_data->dostat_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYP_oblast == 1 && 통신끝점들[순번].informační_systémy_probíhá == popisovač_souboru) { 통신끝점들[순번].informační_systémy_probíhá = -1; return 순번; }
    return -11;
}
int 통신읽기(int popisovač_souboru, void *data, unsigned zboží_POČET) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data || řetězec_data->TYP_oblast != 1) return -9;
    if (!zboží_POČET) return 0; if (!řetězec_data->položka_POČET) return řetězec_data->chyba ? řetězec_data->chyba : řetězec_data->Soubor_konec ? 0 : -11;
    if (zboží_POČET > řetězec_data->položka_POČET) zboží_POČET = řetězec_data->položka_POČET;
    for (unsigned 순번 = 0; 순번 < zboží_POČET; 순번++) { ((unsigned char *)data)[순번] = řetězec_data->data[řetězec_data->přední_fotoaparát_položka]; řetězec_data->přední_fotoaparát_položka = (řetězec_data->přední_fotoaparát_položka + 1) % sizeof(řetězec_data->data); }
    řetězec_data->položka_POČET -= zboží_POČET; if (řetězec_data->kontakt_řízení) tcp_recved(řetězec_data->kontakt_řízení, zboží_POČET); return zboží_POČET;
}
int čistý_zápis(int popisovač_souboru, const void *data, unsigned zboží_POČET) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data || řetězec_data->TYP_oblast != 1) return -9;
    if (řetězec_data->chyba) return řetězec_data->chyba; if (!řetězec_data->kontakt_řízení || !řetězec_data->연결됨) return -107;
    if (!zboží_POČET) return 0; if (zboží_POČET > tcp_sndbuf(řetězec_data->kontakt_řízení)) zboží_POČET = tcp_sndbuf(řetězec_data->kontakt_řízení);
    if (!zboží_POČET) return -11; if (zboží_POČET > 1024) zboží_POČET = 1024;
    err_t 보조항목 = tcp_write(řetězec_data->kontakt_řízení, data, zboží_POČET, TCP_WRITE_FLAG_COPY); if (보조항목) return číslo_chyby(보조항목);
    tcp_output(řetězec_data->kontakt_řízení); return zboží_POČET;
}
int poslat_datagram(int popisovač_souboru, const void *data, unsigned zboží_POČET, uint32_t Adresa, unsigned číslo_portu) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data || řetězec_data->TYP_oblast != 2) return -9;
    if (zboží_POČET > 512) return -90; if (!číslo_portu || číslo_portu > 65535) return -22;
    struct pbuf *data_pozice = pbuf_alloc(PBUF_TRANSPORT, zboží_POČET, PBUF_RAM); if (!data_pozice) return -11;
    pbuf_take(data_pozice, data, zboží_POČET); ip_addr_t internetová_adresa; ip_addr_set_ip4_u32(&internetová_adresa, lwip_htonl(Adresa));
    err_t 보조항목 = udp_sendto(řetězec_data->datagram_řízení, data_pozice, &internetová_adresa, číslo_portu); pbuf_free(data_pozice); return 보조항목 ? číslo_chyby(보조항목) : (int)zboží_POČET;
}
int dostat_datagram(int popisovač_souboru, void *data, unsigned zboží_POČET) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data || řetězec_data->TYP_oblast != 2) return -9;
    if (!řetězec_data->položka_POČET) return -11; unsigned dobrá_pozice = řetězec_data->přední_fotoaparát_položka;
    if (zboží_POČET > řetězec_data->길이목록[dobrá_pozice]) zboží_POČET = řetězec_data->길이목록[dobrá_pozice]; memcpy(data, řetězec_data->data + dobrá_pozice * 512, zboží_POČET);
    řetězec_data->partner_účastník_číslo = řetězec_data->접속번호들[dobrá_pozice]; řetězec_data->partner_ODKAZ = řetězec_data->주소목록[dobrá_pozice]; řetězec_data->přední_fotoaparát_položka = (dobrá_pozice + 1) % 4; řetězec_data->položka_POČET--; return zboží_POČET;
}
unsigned síť_číslo_portu(int popisovač_souboru) { soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); return !řetězec_data ? 0 : řetězec_data->kontakt_řízení ? řetězec_data->kontakt_řízení->local_port : řetězec_data->datagram_řízení ? řetězec_data->datagram_řízení->local_port : 0; }
unsigned partner_číslo_portu(int popisovač_souboru) { soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); return řetězec_data ? řetězec_data->partner_účastník_číslo : 0; }
uint32_t čistý_partner_ODKAZ(int popisovač_souboru) { soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); return řetězec_data ? řetězec_data->partner_ODKAZ : 0; }
void Zavřít_síť(int popisovač_souboru) {
    soket_účastník_3db661a2 *řetězec_data = get_HODNOTA(popisovač_souboru); if (!řetězec_data) return;
    if (řetězec_data->dostat_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYP_oblast && 통신끝점들[순번].informační_systémy_probíhá == popisovač_souboru) Zavřít_síť(순번);
    if (řetězec_data->kontakt_řízení) {
        tcp_arg(řetězec_data->kontakt_řízení, 0); if (řetězec_data->dostat_port) tcp_accept(řetězec_data->kontakt_řízení, 0); else { tcp_recv(řetězec_data->kontakt_řízení, 0); tcp_err(řetězec_data->kontakt_řízení, 0); }
        if (tcp_close(řetězec_data->kontakt_řízení) != ERR_OK) tcp_abort(řetězec_data->kontakt_řízení);
    }
    if (řetězec_data->datagram_řízení) udp_remove(řetězec_data->datagram_řízení); řetězec_data->TYP_oblast = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || cyklické_dotazování) return; cyklické_dotazování = 1;
    if(použít_drátový_síť)유선망살피기(&kontakt_mobilní);
    for (unsigned rozpočet = 0; !použít_drátový_síť && rozpočet < 4096 && (počítač_registr(보조장치 + 0x54) & 1); rozpočet++) {
        unsigned bod_kódu = počítač_registr(보조장치 + 0x40) & 255;
        if (bod_kódu == 192) {
            if (dostat_využití && !dostat_chyba && !수신탈출) {
                struct pbuf *data_pozice = pbuf_alloc(PBUF_RAW, dostat_využití, PBUF_POOL);
                if (data_pozice) { RECEIVED_datagram_POČET++; RECEIVED_bajt_POČET += dostat_využití; pbuf_take(data_pozice, dostat_vyrovnávací_paměť_dat, dostat_využití); if (kontakt_mobilní.input(data_pozice, &kontakt_mobilní) != ERR_OK) { 버린전문수++; pbuf_free(data_pozice); } }
                else 버린전문수++;
            }
            else if (dostat_využití) 버린전문수++;
            dostat_využití = dostat_chyba = 수신탈출 = 0;
        } else if (bod_kódu == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (bod_kódu != 220 && bod_kódu != 221) dostat_chyba = 1; bod_kódu = bod_kódu == 220 ? 192 : 219; 수신탈출 = 0; }
            if (dostat_využití < sizeof(dostat_vyrovnávací_paměť_dat)) dostat_vyrovnávací_paměť_dat[dostat_využití++] = bod_kódu; else dostat_chyba = 1;
        }
    }
    netif_poll(&kontakt_mobilní); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned rozpočet = 0; rozpočet < 4096 && 송신개수 && (počítač_registr(보조장치 + 0x54) & 0x20); rozpočet++) {
        počítač_registr(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    cyklické_dotazování = 0;
}

/* Nastavení·조회는 lwIP의 skutečný_data 인터페이스와 konec_bod 표를 사용한다. */
uint32_t 망상태읽기(unsigned položka_HODNOTA, unsigned INDEX) {
    if(položka_HODNOTA==20)return použít_drátový_síť;
    if(položka_HODNOTA==21)return 준비됨&&netif_is_link_up(&kontakt_mobilní);
    if(položka_HODNOTA==22)return použít_drátový_síť?drátový_síť_Statistika(5):0;
    if (!준비됨) return 0;
    if(použít_drátový_síť&&položka_HODNOTA>=4&&položka_HODNOTA<=8)return drátový_síť_Statistika(položka_HODNOTA-4);
    if (položka_HODNOTA == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_mobilní)));
    if (položka_HODNOTA == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&kontakt_mobilní)));
    if (položka_HODNOTA == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&kontakt_mobilní)));
    if (položka_HODNOTA == 3) return netif_is_up(&kontakt_mobilní) != 0;
    if (položka_HODNOTA == 4) return RECEIVED_datagram_POČET;
    if (položka_HODNOTA == 5) return 보낸전문수;
    if (položka_HODNOTA == 6) return RECEIVED_bajt_POČET;
    if (položka_HODNOTA == 7) return 보낸바이트수;
    if (položka_HODNOTA == 8) return 버린전문수;
    if (položka_HODNOTA == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    soket_účastník_3db661a2 *konec_bod = &통신끝점들[INDEX];
    if (položka_HODNOTA == 10) return konec_bod->TYP_oblast;
    if (!konec_bod->TYP_oblast) return 0;
    if (položka_HODNOTA == 11) return síť_číslo_portu(INDEX);
    if (položka_HODNOTA == 12) return konec_bod->partner_ODKAZ;
    if (položka_HODNOTA == 13) return konec_bod->partner_účastník_číslo;
    if (položka_HODNOTA == 14) return konec_bod->dostat_port ? 1 : konec_bod->Soubor_konec ? 3 : konec_bod->chyba ? 4 : konec_bod->연결됨 ? 2 : 0;
    if (položka_HODNOTA == 15) return konec_bod->položka_POČET;
    if (položka_HODNOTA == 16) {
        const ip_addr_t *Adresa = konec_bod->TYP_oblast == 1 && konec_bod->kontakt_řízení ? &konec_bod->kontakt_řízení->local_ip :
            konec_bod->TYP_oblast == 2 && konec_bod->datagram_řízení ? &konec_bod->datagram_řízení->local_ip : 0;
        return Adresa ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adresa))) : 0;
    }
    return 0;
}

int konfigurovat_síť(unsigned Akce, uint32_t Adresa, uint32_t maska_HODNOTA, uint32_t brána_HODNOTA) {
    if (!준비됨) return -100;
    if (Akce == 1) { netif_set_up(&kontakt_mobilní); return 0; }
    if (Akce == 2) { netif_set_down(&kontakt_mobilní); return 0; }
    if (Akce != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_HODNOTA, 같은 망의 선택적 výchozí_hodnota brána_HODNOTA. */
    uint32_t 뒤집은가림 = ~maska_HODNOTA;
    if (!maska_HODNOTA || (뒤집은가림 & (뒤집은가림 + 1)) || !Adresa || (Adresa >> 24) == 127 ||
        (Adresa >> 24) == 0 || (Adresa >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(Adresa & 뒤집은가림) || (Adresa & 뒤집은가림) == 뒤집은가림)) ||
        (brána_HODNOTA && ((brána_HODNOTA & maska_HODNOTA) != (Adresa & maska_HODNOTA) || brána_HODNOTA == Adresa || (brána_HODNOTA >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(brána_HODNOTA & 뒤집은가림) || (brána_HODNOTA & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 Adresa 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYP_oblast &&
        !(통신끝점들[INDEX].dostat_port && 통신끝점들[INDEX].kontakt_řízení && ip_addr_isany(&통신끝점들[INDEX].kontakt_řízení->local_ip))) return -16;
    if(použít_drátový_síť)dhcp_stop(&kontakt_mobilní);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(Adresa)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_HODNOTA)); ip4_addr_set_u32(&새관문, lwip_htonl(brána_HODNOTA));
    netif_set_addr(&kontakt_mobilní, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *odpověď_účastník;
static uint32_t test_ODKAZ, test_ČAS, doba_odezvy;
static unsigned test_SEQUENCE, test_identifikátor, odpověď_SEQUENCE;
static int odpověď_Stav;
static u8_t 응답받음(void *argumenty, struct raw_pcb *konec_bod, struct pbuf *data, const ip_addr_t *Adresa) {
    (void)argumenty; (void)konec_bod;
    unsigned char 머리[20], odezva[16];
    if (odpověď_Stav != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adresa))) != test_ODKAZ || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Nadpis_změnit_velikost = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Nadpis_změnit_velikost < 20 || data->tot_len < Nadpis_změnit_velikost + 16 ||
        pbuf_copy_partial(data, odezva, 16, Nadpis_změnit_velikost) != 16 || odezva[0] || odezva[1] ||
        (((unsigned)odezva[4] << 8) | odezva[5]) != test_identifikátor ||
        (((unsigned)odezva[6] << 8) | odezva[7]) != test_SEQUENCE ||
        odezva[8] != 'J' || odezva[9] != 'K' || odezva[10] != 'O' || odezva[11] != 'S' ||
        (((uint32_t)odezva[12] << 24) | ((uint32_t)odezva[13] << 16) | ((uint32_t)odezva[14] << 8) | odezva[15]) != test_ČAS) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Nadpis_změnit_velikost)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Nadpis_změnit_velikost); return 0; }
    doba_odezvy = (uint32_t)보드밀리초() - test_ČAS; odpověď_SEQUENCE = 머리[8]; odpověď_Stav = 0;
    pbuf_free(data); return 1;
}
int START_odpověď_test(uint32_t Adresa, unsigned pořadí_HODNOTA) {
    if (!준비됨 || !netif_is_up(&kontakt_mobilní)) return -100;
    if (!Adresa || (Adresa >> 28) >= 14 || Adresa == 0xffffffffu) return -22;
    if (!odpověď_účastník) { odpověď_účastník = raw_new(IP_PROTO_ICMP); if (!odpověď_účastník) return -12; raw_recv(odpověď_účastník, 응답받음, 0); }
    test_ODKAZ = Adresa; test_SEQUENCE = pořadí_HODNOTA & 65535; test_identifikátor = (test_identifikátor + 1) & 65535;
    test_ČAS = 보드밀리초(); odpověď_Stav = -11; doba_odezvy = odpověď_SEQUENCE = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = test_identifikátor >> 8; data[5] = test_identifikátor; data[6] = test_SEQUENCE >> 8; data[7] = test_SEQUENCE;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=test_ČAS >> 24; data[13]=test_ČAS >> 16; data[14]=test_ČAS >> 8; data[15]=test_ČAS;
    for (unsigned poziční_index = 16; poziční_index < sizeof(data); poziční_index++) data[poziční_index] = poziční_index;
    uint16_t ověření_kontrolní_součet = inet_chksum(data, sizeof(data)); memcpy(data + 2, &ověření_kontrolní_součet, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, data, sizeof(data)); ip_addr_t cíl_účastník; ip_addr_set_ip4_u32(&cíl_účastník, lwip_htonl(Adresa));
    err_t 처리값 = raw_sendto(odpověď_účastník, datagram, &cíl_účastník); pbuf_free(datagram);
    if (처리값) odpověď_Stav = číslo_chyby(처리값);
    return 처리값 ? odpověď_Stav : 0;
}
int 응답시험읽기(unsigned položka_HODNOTA) {
    통신망살피기();
    return položka_HODNOTA == 0 ? odpověď_Stav : položka_HODNOTA == 1 ? (int)doba_odezvy : položka_HODNOTA == 2 ? (int)odpověď_SEQUENCE : -22;
}
