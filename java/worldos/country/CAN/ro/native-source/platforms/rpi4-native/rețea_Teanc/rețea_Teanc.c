#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "rețea_Teanc.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../la_distanță_VALUE/la_distanță_VALUE.h"
#include "cu_fir_rețea.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define mașină_registru(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif conexiune_mobil;
static int 준비됨, interogare_ciclică;
static int utiliza_cu_fir_rețea;
static unsigned primi_consum, 수신탈출, primi_eroare;
static unsigned char primi_tampon_de_date[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_diagramă_informații_COUNT, 보낸전문수, RECEIVED_byte_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int Tip_zonă, primi_muta, sisteme_de_informații_în_așteptare, 연결됨, Fișier_termina_un_apel, eroare;
    struct tcp_pcb *conexiune_control;
    struct udp_pcb *diagramă_informații_control;
    unsigned frontală_intrare, intrare_COUNT;
    unsigned char date[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], pereche_adresa;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int număr_de_eroare(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *prelua_VALUE(int Fișier_handle) { return Fișier_handle >= 0 && Fișier_handle < 32 && 통신끝점들[Fișier_handle].Tip_zonă ? &통신끝점들[Fișier_handle] : 0; }
static int 예약하기(int Tip_zonă) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].Tip_zonă) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].Tip_zonă = Tip_zonă; 통신끝점들[순번].sisteme_de_informații_în_așteptare = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned cod_caracter) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = cod_caracter; }
static err_t 출력결과(struct netif *element_COUNT, struct pbuf *date_poziție, const ip4_addr_t *adresa) {
    (void)element_COUNT; (void)adresa;
    if (date_poziție->tot_len > 1500 || 송신개수 + 2 * date_poziție->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Următorul_OFFSET = date_poziție; Următorul_OFFSET; Următorul_OFFSET = Următorul_OFFSET->next) for (unsigned 순번 = 0; 순번 < Următorul_OFFSET->len; 순번++) {
        unsigned cod_caracter = ((unsigned char *)Următorul_OFFSET->payload)[순번];
        if (cod_caracter == 192 || cod_caracter == 219) { 내보내기(219); 내보내기(cod_caracter == 192 ? 220 : 221); } else 내보내기(cod_caracter);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += date_poziție->tot_len; return ERR_OK;
}
static err_t Pregătiți_CLR(struct netif *element_COUNT) { element_COUNT->name[0] = 's'; element_COUNT->name[1] = 'l'; element_COUNT->mtu = 1500; element_COUNT->output = 출력결과; return ERR_OK; }
void Pregătiți_rețea(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    mașină_registru(보조장치 + 4) |= 1; mașină_registru(보조장치 + 0x60) = 0; mașină_registru(보조장치 + 0x44) = 0;
    mașină_registru(보조장치 + 0x48) = 0xc6; mașină_registru(보조장치 + 0x4c) = 3; mașină_registru(보조장치 + 0x68) = 270; mașină_registru(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t adresă_internet, mască_binară, adresă_gateway;
    utiliza_cu_fir_rețea=유선장치있음();
    ip4_addr_set_u32(&adresă_internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&mască_binară, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&adresă_gateway, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&conexiune_mobil, &adresă_internet, &mască_binară, &adresă_gateway, 0, utiliza_cu_fir_rețea?Pregătiți_cu_fir_rețea:Pregătiți_CLR, utiliza_cu_fir_rețea?ethernet_input:ip4_input))return;
    netif_set_default(&conexiune_mobil); netif_set_up(&conexiune_mobil);if(!utiliza_cu_fir_rețea)netif_set_link_up(&conexiune_mobil); 준비됨 = 1;
    Pregătiți_la_distanță();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *date_poziție, err_t eroare) {
    통신끝점 *șir_date = 부가인수; (void)통신제어블록; (void)eroare;
    if (!date_poziție) { șir_date->Fișier_termina_un_apel = 1; return ERR_OK; }
    if (date_poziție->tot_len > sizeof(șir_date->date) - șir_date->intrare_COUNT) return ERR_MEM;
    unsigned curent_poziție = (șir_date->frontală_intrare + șir_date->intrare_COUNT) % sizeof(șir_date->date);
    for (struct pbuf *Următorul_OFFSET = date_poziție; Următorul_OFFSET; Următorul_OFFSET = Următorul_OFFSET->next) for (unsigned 순번 = 0; 순번 < Următorul_OFFSET->len; 순번++) {
        șir_date->date[curent_poziție] = ((unsigned char *)Următorul_OFFSET->payload)[순번]; curent_poziție = (curent_poziție + 1) % sizeof(șir_date->date);
    }
    șir_date->intrare_COUNT += date_poziție->tot_len; pbuf_free(date_poziție); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t eroare) { 통신끝점 *șir_date = 부가인수; șir_date->conexiune_control = 0; șir_date->eroare = număr_de_eroare(eroare); }
static void 되부름목록(통신끝점 *șir_date) { tcp_arg(șir_date->conexiune_control, șir_date); tcp_recv(șir_date->conexiune_control, 수신됨); tcp_err(șir_date->conexiune_control, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t eroare) {
    통신끝점 *șir_date = 부가인수; (void)통신제어블록; if (eroare) șir_date->eroare = număr_de_eroare(eroare); else șir_date->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t eroare) {
    통신끝점 *părinte = 부가인수; if (eroare) return eroare;
    int Fișier_handle = 예약하기(1); if (Fișier_handle < 0) return ERR_MEM;
    통신끝점 *șir_date = &통신끝점들[Fișier_handle]; șir_date->conexiune_control = 통신제어블록; șir_date->연결됨 = 1; șir_date->sisteme_de_informații_în_așteptare = (int)(părinte - 통신끝점들);
    șir_date->pereche_adresa = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); șir_date->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(șir_date); return ERR_OK;
}
static void diagramă_informații(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *date_poziție, const ip_addr_t *adresa, u16_t număr_port) {
    통신끝점 *șir_date = 부가인수; (void)통신제어블록;
    if (șir_date->intrare_COUNT < 4 && date_poziție->tot_len <= 512) {
        unsigned index_de_poziție = (șir_date->frontală_intrare + șir_date->intrare_COUNT) % 4;
        pbuf_copy_partial(date_poziție, șir_date->date + index_de_poziție * 512, date_poziție->tot_len, 0);
        șir_date->길이목록[index_de_poziție] = date_poziție->tot_len; șir_date->접속번호들[index_de_poziție] = număr_port;
        șir_date->주소목록[index_de_poziție] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))); șir_date->intrare_COUNT++;
    }
    pbuf_free(date_poziție);
}
int 통신끝점만들기(int Tip_zonă) {
    if (!준비됨) return -100;
    if (Tip_zonă != 1 && Tip_zonă != 2) return -93;
    int Fișier_handle = 예약하기(Tip_zonă); if (Fișier_handle < 0) return Fișier_handle;
    통신끝점 *șir_date = &통신끝점들[Fișier_handle];
    if (Tip_zonă == 1) { șir_date->conexiune_control = tcp_new(); if (șir_date->conexiune_control) 되부름목록(șir_date); }
    else { șir_date->diagramă_informații_control = udp_new(); if (șir_date->diagramă_informații_control) udp_recv(șir_date->diagramă_informații_control, diagramă_informații, șir_date); }
    if (!șir_date->conexiune_control && !șir_date->diagramă_informații_control) { șir_date->Tip_zonă = 0; return -12; } return Fișier_handle;
}
int NET_BIND(int Fișier_handle, uint32_t adresa, unsigned număr_port) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date) return -9;
    if (număr_port > 65535 || (adresa && adresa != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&conexiune_mobil))) && adresa != 0x7f000001)) return -99;
    ip_addr_t adresă_internet; ip_addr_set_ip4_u32(&adresă_internet, lwip_htonl(adresa));
    err_t 보조항목 = șir_date->Tip_zonă == 1 ? tcp_bind(șir_date->conexiune_control, &adresă_internet, număr_port) : udp_bind(șir_date->diagramă_informații_control, &adresă_internet, număr_port); return 보조항목 ? număr_de_eroare(보조항목) : 0;
}
void 통신주소재사용(int Fișier_handle) { 통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (șir_date && șir_date->conexiune_control) ip_set_option(șir_date->conexiune_control, SOF_REUSEADDR); }
int NET_asculta(int Fișier_handle) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date || șir_date->Tip_zonă != 1) return -9;
    if (șir_date->primi_muta) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(șir_date->conexiune_control, 4, &보조항목);
    if (!통신제어블록) return număr_de_eroare(보조항목); șir_date->conexiune_control = 통신제어블록; șir_date->primi_muta = 1; tcp_arg(통신제어블록, șir_date); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_conecta(int Fișier_handle, uint32_t adresa, unsigned număr_port) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date || șir_date->Tip_zonă != 1) return -9;
    if (șir_date->eroare) return șir_date->eroare;
    if (șir_date->연결됨) return 0;
    if (șir_date->상대창구번호) return -115;
    if (!număr_port || număr_port > 65535 || !adresa) return -22;
    ip_addr_t adresă_internet; ip_addr_set_ip4_u32(&adresă_internet, lwip_htonl(adresa));
    șir_date->pereche_adresa = adresa; șir_date->상대창구번호 = număr_port;
    err_t 보조항목 = tcp_connect(șir_date->conexiune_control, &adresă_internet, număr_port, 연결됨); return 보조항목 ? număr_de_eroare(보조항목) : -115;
}
int NET_accepta(int Fișier_handle) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date || !șir_date->primi_muta) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].Tip_zonă == 1 && 통신끝점들[순번].sisteme_de_informații_în_așteptare == Fișier_handle) { 통신끝점들[순번].sisteme_de_informații_în_așteptare = -1; return 순번; }
    return -11;
}
int 통신읽기(int Fișier_handle, void *date, unsigned element_COUNT) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date || șir_date->Tip_zonă != 1) return -9;
    if (!element_COUNT) return 0; if (!șir_date->intrare_COUNT) return șir_date->eroare ? șir_date->eroare : șir_date->Fișier_termina_un_apel ? 0 : -11;
    if (element_COUNT > șir_date->intrare_COUNT) element_COUNT = șir_date->intrare_COUNT;
    for (unsigned 순번 = 0; 순번 < element_COUNT; 순번++) { ((unsigned char *)date)[순번] = șir_date->date[șir_date->frontală_intrare]; șir_date->frontală_intrare = (șir_date->frontală_intrare + 1) % sizeof(șir_date->date); }
    șir_date->intrare_COUNT -= element_COUNT; if (șir_date->conexiune_control) tcp_recved(șir_date->conexiune_control, element_COUNT); return element_COUNT;
}
int NET_scriere(int Fișier_handle, const void *date, unsigned element_COUNT) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date || șir_date->Tip_zonă != 1) return -9;
    if (șir_date->eroare) return șir_date->eroare; if (!șir_date->conexiune_control || !șir_date->연결됨) return -107;
    if (!element_COUNT) return 0; if (element_COUNT > tcp_sndbuf(șir_date->conexiune_control)) element_COUNT = tcp_sndbuf(șir_date->conexiune_control);
    if (!element_COUNT) return -11; if (element_COUNT > 1024) element_COUNT = 1024;
    err_t 보조항목 = tcp_write(șir_date->conexiune_control, date, element_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return număr_de_eroare(보조항목);
    tcp_output(șir_date->conexiune_control); return element_COUNT;
}
int trimite_diagramă_informații(int Fișier_handle, const void *date, unsigned element_COUNT, uint32_t adresa, unsigned număr_port) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date || șir_date->Tip_zonă != 2) return -9;
    if (element_COUNT > 512) return -90; if (!număr_port || număr_port > 65535) return -22;
    struct pbuf *date_poziție = pbuf_alloc(PBUF_TRANSPORT, element_COUNT, PBUF_RAM); if (!date_poziție) return -11;
    pbuf_take(date_poziție, date, element_COUNT); ip_addr_t adresă_internet; ip_addr_set_ip4_u32(&adresă_internet, lwip_htonl(adresa));
    err_t 보조항목 = udp_sendto(șir_date->diagramă_informații_control, date_poziție, &adresă_internet, număr_port); pbuf_free(date_poziție); return 보조항목 ? număr_de_eroare(보조항목) : (int)element_COUNT;
}
int primi_diagramă_informații(int Fișier_handle, void *date, unsigned element_COUNT) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date || șir_date->Tip_zonă != 2) return -9;
    if (!șir_date->intrare_COUNT) return -11; unsigned curent_poziție = șir_date->frontală_intrare;
    if (element_COUNT > șir_date->길이목록[curent_poziție]) element_COUNT = șir_date->길이목록[curent_poziție]; memcpy(date, șir_date->date + curent_poziție * 512, element_COUNT);
    șir_date->상대창구번호 = șir_date->접속번호들[curent_poziție]; șir_date->pereche_adresa = șir_date->주소목록[curent_poziție]; șir_date->frontală_intrare = (curent_poziție + 1) % 4; șir_date->intrare_COUNT--; return element_COUNT;
}
unsigned rețea_număr_port(int Fișier_handle) { 통신끝점 *șir_date = prelua_VALUE(Fișier_handle); return !șir_date ? 0 : șir_date->conexiune_control ? șir_date->conexiune_control->local_port : șir_date->diagramă_informații_control ? șir_date->diagramă_informații_control->local_port : 0; }
unsigned pereche_număr_port(int Fișier_handle) { 통신끝점 *șir_date = prelua_VALUE(Fișier_handle); return șir_date ? șir_date->상대창구번호 : 0; }
uint32_t NET_pereche_adresa(int Fișier_handle) { 통신끝점 *șir_date = prelua_VALUE(Fișier_handle); return șir_date ? șir_date->pereche_adresa : 0; }
void închide_rețea(int Fișier_handle) {
    통신끝점 *șir_date = prelua_VALUE(Fișier_handle); if (!șir_date) return;
    if (șir_date->primi_muta) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].Tip_zonă && 통신끝점들[순번].sisteme_de_informații_în_așteptare == Fișier_handle) închide_rețea(순번);
    if (șir_date->conexiune_control) {
        tcp_arg(șir_date->conexiune_control, 0); if (șir_date->primi_muta) tcp_accept(șir_date->conexiune_control, 0); else { tcp_recv(șir_date->conexiune_control, 0); tcp_err(șir_date->conexiune_control, 0); }
        if (tcp_close(șir_date->conexiune_control) != ERR_OK) tcp_abort(șir_date->conexiune_control);
    }
    if (șir_date->diagramă_informații_control) udp_remove(șir_date->diagramă_informații_control); șir_date->Tip_zonă = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || interogare_ciclică) return; interogare_ciclică = 1;
    if(utiliza_cu_fir_rețea)유선망살피기(&conexiune_mobil);
    for (unsigned buget = 0; !utiliza_cu_fir_rețea && buget < 4096 && (mașină_registru(보조장치 + 0x54) & 1); buget++) {
        unsigned cod_caracter = mașină_registru(보조장치 + 0x40) & 255;
        if (cod_caracter == 192) {
            if (primi_consum && !primi_eroare && !수신탈출) {
                struct pbuf *date_poziție = pbuf_alloc(PBUF_RAW, primi_consum, PBUF_POOL);
                if (date_poziție) { RECEIVED_diagramă_informații_COUNT++; RECEIVED_byte_COUNT += primi_consum; pbuf_take(date_poziție, primi_tampon_de_date, primi_consum); if (conexiune_mobil.input(date_poziție, &conexiune_mobil) != ERR_OK) { 버린전문수++; pbuf_free(date_poziție); } }
                else 버린전문수++;
            }
            else if (primi_consum) 버린전문수++;
            primi_consum = primi_eroare = 수신탈출 = 0;
        } else if (cod_caracter == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (cod_caracter != 220 && cod_caracter != 221) primi_eroare = 1; cod_caracter = cod_caracter == 220 ? 192 : 219; 수신탈출 = 0; }
            if (primi_consum < sizeof(primi_tampon_de_date)) primi_tampon_de_date[primi_consum++] = cod_caracter; else primi_eroare = 1;
        }
    }
    netif_poll(&conexiune_mobil); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned buget = 0; buget < 4096 && 송신개수 && (mașină_registru(보조장치 + 0x54) & 0x20); buget++) {
        mașină_registru(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    interogare_ciclică = 0;
}

/* Setări·조회는 lwIP의 real_date 인터페이스와 termina_un_apel_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned intrare_VALUE, unsigned INDEX) {
    if(intrare_VALUE==20)return utiliza_cu_fir_rețea;
    if(intrare_VALUE==21)return 준비됨&&netif_is_link_up(&conexiune_mobil);
    if(intrare_VALUE==22)return utiliza_cu_fir_rețea?cu_fir_rețea_Statistică(5):0;
    if (!준비됨) return 0;
    if(utiliza_cu_fir_rețea&&intrare_VALUE>=4&&intrare_VALUE<=8)return cu_fir_rețea_Statistică(intrare_VALUE-4);
    if (intrare_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&conexiune_mobil)));
    if (intrare_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&conexiune_mobil)));
    if (intrare_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&conexiune_mobil)));
    if (intrare_VALUE == 3) return netif_is_up(&conexiune_mobil) != 0;
    if (intrare_VALUE == 4) return RECEIVED_diagramă_informații_COUNT;
    if (intrare_VALUE == 5) return 보낸전문수;
    if (intrare_VALUE == 6) return RECEIVED_byte_COUNT;
    if (intrare_VALUE == 7) return 보낸바이트수;
    if (intrare_VALUE == 8) return 버린전문수;
    if (intrare_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *termina_un_apel_p = &통신끝점들[INDEX];
    if (intrare_VALUE == 10) return termina_un_apel_p->Tip_zonă;
    if (!termina_un_apel_p->Tip_zonă) return 0;
    if (intrare_VALUE == 11) return rețea_număr_port(INDEX);
    if (intrare_VALUE == 12) return termina_un_apel_p->pereche_adresa;
    if (intrare_VALUE == 13) return termina_un_apel_p->상대창구번호;
    if (intrare_VALUE == 14) return termina_un_apel_p->primi_muta ? 1 : termina_un_apel_p->Fișier_termina_un_apel ? 3 : termina_un_apel_p->eroare ? 4 : termina_un_apel_p->연결됨 ? 2 : 0;
    if (intrare_VALUE == 15) return termina_un_apel_p->intrare_COUNT;
    if (intrare_VALUE == 16) {
        const ip_addr_t *adresa = termina_un_apel_p->Tip_zonă == 1 && termina_un_apel_p->conexiune_control ? &termina_un_apel_p->conexiune_control->local_ip :
            termina_un_apel_p->Tip_zonă == 2 && termina_un_apel_p->diagramă_informații_control ? &termina_un_apel_p->diagramă_informații_control->local_ip : 0;
        return adresa ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) : 0;
    }
    return 0;
}

int configura_rețea(unsigned Acțiuni, uint32_t adresa, uint32_t mască_VALUE, uint32_t gateway_VALUE) {
    if (!준비됨) return -100;
    if (Acțiuni == 1) { netif_set_up(&conexiune_mobil); return 0; }
    if (Acțiuni == 2) { netif_set_down(&conexiune_mobil); return 0; }
    if (Acțiuni != 0) return -22;
    /* 유니캐스트 IPv4, 연속 mască_VALUE, 같은 망의 선택적 valoare_implicită gateway_VALUE. */
    uint32_t 뒤집은가림 = ~mască_VALUE;
    if (!mască_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !adresa || (adresa >> 24) == 127 ||
        (adresa >> 24) == 0 || (adresa >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(adresa & 뒤집은가림) || (adresa & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_VALUE && ((gateway_VALUE & mască_VALUE) != (adresa & mască_VALUE) || gateway_VALUE == adresa || (gateway_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_VALUE & 뒤집은가림) || (gateway_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 adresa 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].Tip_zonă &&
        !(통신끝점들[INDEX].primi_muta && 통신끝점들[INDEX].conexiune_control && ip_addr_isany(&통신끝점들[INDEX].conexiune_control->local_ip))) return -16;
    if(utiliza_cu_fir_rețea)dhcp_stop(&conexiune_mobil);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(adresa)); ip4_addr_set_u32(&새가림, lwip_htonl(mască_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_VALUE));
    netif_set_addr(&conexiune_mobil, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *răspuns_participant;
static uint32_t 시험주소, 시험시각, timp_de_răspuns;
static unsigned 시험순서, 시험식별자, răspuns_SEQUENCE;
static int răspuns_Stare;
static u8_t 응답받음(void *Argumente, struct raw_pcb *termina_un_apel_p, struct pbuf *date, const ip_addr_t *adresa) {
    (void)Argumente; (void)termina_un_apel_p;
    unsigned char 머리[20], replică[16];
    if (răspuns_Stare != -11 || date->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) != 시험주소 || pbuf_copy_partial(date, 머리, 20, 0) != 20) return 0;
    unsigned Antet_dimensiona = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Antet_dimensiona < 20 || date->tot_len < Antet_dimensiona + 16 ||
        pbuf_copy_partial(date, replică, 16, Antet_dimensiona) != 16 || replică[0] || replică[1] ||
        (((unsigned)replică[4] << 8) | replică[5]) != 시험식별자 ||
        (((unsigned)replică[6] << 8) | replică[7]) != 시험순서 ||
        replică[8] != 'J' || replică[9] != 'K' || replică[10] != 'O' || replică[11] != 'S' ||
        (((uint32_t)replică[12] << 24) | ((uint32_t)replică[13] << 16) | ((uint32_t)replică[14] << 8) | replică[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(date, Antet_dimensiona)) return 0;
    if (inet_chksum_pbuf(date)) { pbuf_add_header(date, Antet_dimensiona); return 0; }
    timp_de_răspuns = (uint32_t)보드밀리초() - 시험시각; răspuns_SEQUENCE = 머리[8]; răspuns_Stare = 0;
    pbuf_free(date); return 1;
}
int 응답시험시작(uint32_t adresa, unsigned ordine_VALUE) {
    if (!준비됨 || !netif_is_up(&conexiune_mobil)) return -100;
    if (!adresa || (adresa >> 28) >= 14 || adresa == 0xffffffffu) return -22;
    if (!răspuns_participant) { răspuns_participant = raw_new(IP_PROTO_ICMP); if (!răspuns_participant) return -12; raw_recv(răspuns_participant, 응답받음, 0); }
    시험주소 = adresa; 시험순서 = ordine_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); răspuns_Stare = -11; timp_de_răspuns = răspuns_SEQUENCE = 0;
    unsigned char date[32] = {8,0,0,0};
    date[4] = 시험식별자 >> 8; date[5] = 시험식별자; date[6] = 시험순서 >> 8; date[7] = 시험순서;
    date[8]='J'; date[9]='K'; date[10]='O'; date[11]='S';
    date[12]=시험시각 >> 24; date[13]=시험시각 >> 16; date[14]=시험시각 >> 8; date[15]=시험시각;
    for (unsigned index_de_poziție = 16; index_de_poziție < sizeof(date); index_de_poziție++) date[index_de_poziție] = index_de_poziție;
    uint16_t verificare_sumă_de_verificare = inet_chksum(date, sizeof(date)); memcpy(date + 2, &verificare_sumă_de_verificare, 2);
    struct pbuf *diagramă_informații = pbuf_alloc(PBUF_IP, sizeof(date), PBUF_RAM); if (!diagramă_informații) return -12;
    pbuf_take(diagramă_informații, date, sizeof(date)); ip_addr_t destinație_participant; ip_addr_set_ip4_u32(&destinație_participant, lwip_htonl(adresa));
    err_t 처리값 = raw_sendto(răspuns_participant, diagramă_informații, &destinație_participant); pbuf_free(diagramă_informații);
    if (처리값) răspuns_Stare = număr_de_eroare(처리값);
    return 처리값 ? răspuns_Stare : 0;
}
int 응답시험읽기(unsigned intrare_VALUE) {
    통신망살피기();
    return intrare_VALUE == 0 ? răspuns_Stare : intrare_VALUE == 1 ? (int)timp_de_răspuns : intrare_VALUE == 2 ? (int)răspuns_SEQUENCE : -22;
}
