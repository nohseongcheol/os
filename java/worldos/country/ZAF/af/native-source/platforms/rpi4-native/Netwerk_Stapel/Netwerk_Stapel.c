#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Netwerk_Stapel.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../afstands_VALUE/afstands_VALUE.h"
#include "bedraad_Netwerk.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define masjien_registreer(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif verbinding_mobiel;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_greep_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_kategorie, 수신창구, 대기중, 연결됨, lêer_beëindig, Fout;
    struct tcp_pcb *verbinding_kontrole;
    struct udp_pcb *전문제어;
    unsigned voor_inskrywing, inskrywing_COUNT;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], portuur_adres;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *kry_VALUE(int lêer_handvatsel) { return lêer_handvatsel >= 0 && lêer_handvatsel < 32 && 통신끝점들[lêer_handvatsel].TYPE_kategorie ? &통신끝점들[lêer_handvatsel] : 0; }
static int 예약하기(int TYPE_kategorie) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_kategorie) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_kategorie = TYPE_kategorie; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned karakterkode) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = karakterkode; }
static err_t 출력결과(struct netif *item_COUNT, struct pbuf *data_plaas, const ip4_addr_t *adres) {
    (void)item_COUNT; (void)adres;
    if (data_plaas->tot_len > 1500 || 송신개수 + 2 * data_plaas->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Volgende_OFFSET = data_plaas; Volgende_OFFSET; Volgende_OFFSET = Volgende_OFFSET->next) for (unsigned 순번 = 0; 순번 < Volgende_OFFSET->len; 순번++) {
        unsigned karakterkode = ((unsigned char *)Volgende_OFFSET->payload)[순번];
        if (karakterkode == 192 || karakterkode == 219) { 내보내기(219); 내보내기(karakterkode == 192 ? 220 : 221); } else 내보내기(karakterkode);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_plaas->tot_len; return ERR_OK;
}
static err_t Maak_gereed_algemene_taallooptyd(struct netif *item_COUNT) { item_COUNT->name[0] = 's'; item_COUNT->name[1] = 'l'; item_COUNT->mtu = 1500; item_COUNT->output = 출력결과; return ERR_OK; }
void Maak_gereed_Netwerk(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    masjien_registreer(보조장치 + 4) |= 1; masjien_registreer(보조장치 + 0x60) = 0; masjien_registreer(보조장치 + 0x44) = 0;
    masjien_registreer(보조장치 + 0x48) = 0xc6; masjien_registreer(보조장치 + 0x4c) = 3; masjien_registreer(보조장치 + 0x68) = 270; masjien_registreer(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetadres, bis_masker, deurgang_adres;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&internetadres, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bis_masker, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&deurgang_adres, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&verbinding_mobiel, &internetadres, &bis_masker, &deurgang_adres, 0, 유선사용?Maak_gereed_bedraad_Netwerk:Maak_gereed_algemene_taallooptyd, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&verbinding_mobiel); netif_set_up(&verbinding_mobiel);if(!유선사용)netif_set_link_up(&verbinding_mobiel); 준비됨 = 1;
    Maak_gereed_afstands();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *oordrag_kontrole_blokkeer, struct pbuf *data_plaas, err_t Fout) {
    통신끝점 *string_data = 부가인수; (void)oordrag_kontrole_blokkeer; (void)Fout;
    if (!data_plaas) { string_data->lêer_beëindig = 1; return ERR_OK; }
    if (data_plaas->tot_len > sizeof(string_data->data) - string_data->inskrywing_COUNT) return ERR_MEM;
    unsigned 현재위치 = (string_data->voor_inskrywing + string_data->inskrywing_COUNT) % sizeof(string_data->data);
    for (struct pbuf *Volgende_OFFSET = data_plaas; Volgende_OFFSET; Volgende_OFFSET = Volgende_OFFSET->next) for (unsigned 순번 = 0; 순번 < Volgende_OFFSET->len; 순번++) {
        string_data->data[현재위치] = ((unsigned char *)Volgende_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(string_data->data);
    }
    string_data->inskrywing_COUNT += data_plaas->tot_len; pbuf_free(data_plaas); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Fout) { 통신끝점 *string_data = 부가인수; string_data->verbinding_kontrole = 0; string_data->Fout = 오류번호(Fout); }
static void 되부름목록(통신끝점 *string_data) { tcp_arg(string_data->verbinding_kontrole, string_data); tcp_recv(string_data->verbinding_kontrole, 수신됨); tcp_err(string_data->verbinding_kontrole, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *oordrag_kontrole_blokkeer, err_t Fout) {
    통신끝점 *string_data = 부가인수; (void)oordrag_kontrole_blokkeer; if (Fout) string_data->Fout = 오류번호(Fout); else string_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *oordrag_kontrole_blokkeer, err_t Fout) {
    통신끝점 *부모항목 = 부가인수; if (Fout) return Fout;
    int lêer_handvatsel = 예약하기(1); if (lêer_handvatsel < 0) return ERR_MEM;
    통신끝점 *string_data = &통신끝점들[lêer_handvatsel]; string_data->verbinding_kontrole = oordrag_kontrole_blokkeer; string_data->연결됨 = 1; string_data->대기중 = (int)(부모항목 - 통신끝점들);
    string_data->portuur_adres = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&oordrag_kontrole_blokkeer->remote_ip))); string_data->상대창구번호 = oordrag_kontrole_blokkeer->remote_port;
    되부름목록(string_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *oordrag_kontrole_blokkeer, struct pbuf *data_plaas, const ip_addr_t *adres, u16_t 접속번호) {
    통신끝점 *string_data = 부가인수; (void)oordrag_kontrole_blokkeer;
    if (string_data->inskrywing_COUNT < 4 && data_plaas->tot_len <= 512) {
        unsigned plaas_INDEX = (string_data->voor_inskrywing + string_data->inskrywing_COUNT) % 4;
        pbuf_copy_partial(data_plaas, string_data->data + plaas_INDEX * 512, data_plaas->tot_len, 0);
        string_data->길이목록[plaas_INDEX] = data_plaas->tot_len; string_data->접속번호들[plaas_INDEX] = 접속번호;
        string_data->주소목록[plaas_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adres))); string_data->inskrywing_COUNT++;
    }
    pbuf_free(data_plaas);
}
int 통신끝점만들기(int TYPE_kategorie) {
    if (!준비됨) return -100;
    if (TYPE_kategorie != 1 && TYPE_kategorie != 2) return -93;
    int lêer_handvatsel = 예약하기(TYPE_kategorie); if (lêer_handvatsel < 0) return lêer_handvatsel;
    통신끝점 *string_data = &통신끝점들[lêer_handvatsel];
    if (TYPE_kategorie == 1) { string_data->verbinding_kontrole = tcp_new(); if (string_data->verbinding_kontrole) 되부름목록(string_data); }
    else { string_data->전문제어 = udp_new(); if (string_data->전문제어) udp_recv(string_data->전문제어, 전문, string_data); }
    if (!string_data->verbinding_kontrole && !string_data->전문제어) { string_data->TYPE_kategorie = 0; return -12; } return lêer_handvatsel;
}
int 망주소묶기(int lêer_handvatsel, uint32_t adres, unsigned 접속번호) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data) return -9;
    if (접속번호 > 65535 || (adres && adres != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&verbinding_mobiel))) && adres != 0x7f000001)) return -99;
    ip_addr_t internetadres; ip_addr_set_ip4_u32(&internetadres, lwip_htonl(adres));
    err_t 보조항목 = string_data->TYPE_kategorie == 1 ? tcp_bind(string_data->verbinding_kontrole, &internetadres, 접속번호) : udp_bind(string_data->전문제어, &internetadres, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int lêer_handvatsel) { 통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (string_data && string_data->verbinding_kontrole) ip_set_option(string_data->verbinding_kontrole, SOF_REUSEADDR); }
int 연결기다리기(int lêer_handvatsel) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data || string_data->TYPE_kategorie != 1) return -9;
    if (string_data->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *oordrag_kontrole_blokkeer = tcp_listen_with_backlog_and_err(string_data->verbinding_kontrole, 4, &보조항목);
    if (!oordrag_kontrole_blokkeer) return 오류번호(보조항목); string_data->verbinding_kontrole = oordrag_kontrole_blokkeer; string_data->수신창구 = 1; tcp_arg(oordrag_kontrole_blokkeer, string_data); tcp_accept(oordrag_kontrole_blokkeer, 연결받음); return 0;
}
int 망연결하기(int lêer_handvatsel, uint32_t adres, unsigned 접속번호) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data || string_data->TYPE_kategorie != 1) return -9;
    if (string_data->Fout) return string_data->Fout;
    if (string_data->연결됨) return 0;
    if (string_data->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !adres) return -22;
    ip_addr_t internetadres; ip_addr_set_ip4_u32(&internetadres, lwip_htonl(adres));
    string_data->portuur_adres = adres; string_data->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(string_data->verbinding_kontrole, &internetadres, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int lêer_handvatsel) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data || !string_data->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_kategorie == 1 && 통신끝점들[순번].대기중 == lêer_handvatsel) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int lêer_handvatsel, void *data, unsigned item_COUNT) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data || string_data->TYPE_kategorie != 1) return -9;
    if (!item_COUNT) return 0; if (!string_data->inskrywing_COUNT) return string_data->Fout ? string_data->Fout : string_data->lêer_beëindig ? 0 : -11;
    if (item_COUNT > string_data->inskrywing_COUNT) item_COUNT = string_data->inskrywing_COUNT;
    for (unsigned 순번 = 0; 순번 < item_COUNT; 순번++) { ((unsigned char *)data)[순번] = string_data->data[string_data->voor_inskrywing]; string_data->voor_inskrywing = (string_data->voor_inskrywing + 1) % sizeof(string_data->data); }
    string_data->inskrywing_COUNT -= item_COUNT; if (string_data->verbinding_kontrole) tcp_recved(string_data->verbinding_kontrole, item_COUNT); return item_COUNT;
}
int 통신쓰기(int lêer_handvatsel, const void *data, unsigned item_COUNT) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data || string_data->TYPE_kategorie != 1) return -9;
    if (string_data->Fout) return string_data->Fout; if (!string_data->verbinding_kontrole || !string_data->연결됨) return -107;
    if (!item_COUNT) return 0; if (item_COUNT > tcp_sndbuf(string_data->verbinding_kontrole)) item_COUNT = tcp_sndbuf(string_data->verbinding_kontrole);
    if (!item_COUNT) return -11; if (item_COUNT > 1024) item_COUNT = 1024;
    err_t 보조항목 = tcp_write(string_data->verbinding_kontrole, data, item_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(string_data->verbinding_kontrole); return item_COUNT;
}
int 전문보내기(int lêer_handvatsel, const void *data, unsigned item_COUNT, uint32_t adres, unsigned 접속번호) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data || string_data->TYPE_kategorie != 2) return -9;
    if (item_COUNT > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *data_plaas = pbuf_alloc(PBUF_TRANSPORT, item_COUNT, PBUF_RAM); if (!data_plaas) return -11;
    pbuf_take(data_plaas, data, item_COUNT); ip_addr_t internetadres; ip_addr_set_ip4_u32(&internetadres, lwip_htonl(adres));
    err_t 보조항목 = udp_sendto(string_data->전문제어, data_plaas, &internetadres, 접속번호); pbuf_free(data_plaas); return 보조항목 ? 오류번호(보조항목) : (int)item_COUNT;
}
int 전문받기(int lêer_handvatsel, void *data, unsigned item_COUNT) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data || string_data->TYPE_kategorie != 2) return -9;
    if (!string_data->inskrywing_COUNT) return -11; unsigned 현재위치 = string_data->voor_inskrywing;
    if (item_COUNT > string_data->길이목록[현재위치]) item_COUNT = string_data->길이목록[현재위치]; memcpy(data, string_data->data + 현재위치 * 512, item_COUNT);
    string_data->상대창구번호 = string_data->접속번호들[현재위치]; string_data->portuur_adres = string_data->주소목록[현재위치]; string_data->voor_inskrywing = (현재위치 + 1) % 4; string_data->inskrywing_COUNT--; return item_COUNT;
}
unsigned 통신접속번호(int lêer_handvatsel) { 통신끝점 *string_data = kry_VALUE(lêer_handvatsel); return !string_data ? 0 : string_data->verbinding_kontrole ? string_data->verbinding_kontrole->local_port : string_data->전문제어 ? string_data->전문제어->local_port : 0; }
unsigned 상대접속번호(int lêer_handvatsel) { 통신끝점 *string_data = kry_VALUE(lêer_handvatsel); return string_data ? string_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int lêer_handvatsel) { 통신끝점 *string_data = kry_VALUE(lêer_handvatsel); return string_data ? string_data->portuur_adres : 0; }
void sluit_Netwerk(int lêer_handvatsel) {
    통신끝점 *string_data = kry_VALUE(lêer_handvatsel); if (!string_data) return;
    if (string_data->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_kategorie && 통신끝점들[순번].대기중 == lêer_handvatsel) sluit_Netwerk(순번);
    if (string_data->verbinding_kontrole) {
        tcp_arg(string_data->verbinding_kontrole, 0); if (string_data->수신창구) tcp_accept(string_data->verbinding_kontrole, 0); else { tcp_recv(string_data->verbinding_kontrole, 0); tcp_err(string_data->verbinding_kontrole, 0); }
        if (tcp_close(string_data->verbinding_kontrole) != ERR_OK) tcp_abort(string_data->verbinding_kontrole);
    }
    if (string_data->전문제어) udp_remove(string_data->전문제어); string_data->TYPE_kategorie = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&verbinding_mobiel);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (masjien_registreer(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned karakterkode = masjien_registreer(보조장치 + 0x40) & 255;
        if (karakterkode == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *data_plaas = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (data_plaas) { 받은전문수++; RECEIVED_greep_COUNT += 수신사용량; pbuf_take(data_plaas, 수신자료, 수신사용량); if (verbinding_mobiel.input(data_plaas, &verbinding_mobiel) != ERR_OK) { 버린전문수++; pbuf_free(data_plaas); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (karakterkode == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (karakterkode != 220 && karakterkode != 221) 수신오류 = 1; karakterkode = karakterkode == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = karakterkode; else 수신오류 = 1;
        }
    }
    netif_poll(&verbinding_mobiel); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (masjien_registreer(보조장치 + 0x54) & 0x20); 처리한도++) {
        masjien_registreer(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Instellings·조회는 lwIP의 werklik_data 인터페이스와 beëindig_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned inskrywing_VALUE, unsigned INDEX) {
    if(inskrywing_VALUE==20)return 유선사용;
    if(inskrywing_VALUE==21)return 준비됨&&netif_is_link_up(&verbinding_mobiel);
    if(inskrywing_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&inskrywing_VALUE>=4&&inskrywing_VALUE<=8)return 유선망집계(inskrywing_VALUE-4);
    if (inskrywing_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&verbinding_mobiel)));
    if (inskrywing_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&verbinding_mobiel)));
    if (inskrywing_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&verbinding_mobiel)));
    if (inskrywing_VALUE == 3) return netif_is_up(&verbinding_mobiel) != 0;
    if (inskrywing_VALUE == 4) return 받은전문수;
    if (inskrywing_VALUE == 5) return 보낸전문수;
    if (inskrywing_VALUE == 6) return RECEIVED_greep_COUNT;
    if (inskrywing_VALUE == 7) return 보낸바이트수;
    if (inskrywing_VALUE == 8) return 버린전문수;
    if (inskrywing_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *beëindig_p = &통신끝점들[INDEX];
    if (inskrywing_VALUE == 10) return beëindig_p->TYPE_kategorie;
    if (!beëindig_p->TYPE_kategorie) return 0;
    if (inskrywing_VALUE == 11) return 통신접속번호(INDEX);
    if (inskrywing_VALUE == 12) return beëindig_p->portuur_adres;
    if (inskrywing_VALUE == 13) return beëindig_p->상대창구번호;
    if (inskrywing_VALUE == 14) return beëindig_p->수신창구 ? 1 : beëindig_p->lêer_beëindig ? 3 : beëindig_p->Fout ? 4 : beëindig_p->연결됨 ? 2 : 0;
    if (inskrywing_VALUE == 15) return beëindig_p->inskrywing_COUNT;
    if (inskrywing_VALUE == 16) {
        const ip_addr_t *adres = beëindig_p->TYPE_kategorie == 1 && beëindig_p->verbinding_kontrole ? &beëindig_p->verbinding_kontrole->local_ip :
            beëindig_p->TYPE_kategorie == 2 && beëindig_p->전문제어 ? &beëindig_p->전문제어->local_ip : 0;
        return adres ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adres))) : 0;
    }
    return 0;
}

int konfigureer_Netwerk(unsigned Aksie, uint32_t adres, uint32_t masker_VALUE, uint32_t deurgang_VALUE) {
    if (!준비됨) return -100;
    if (Aksie == 1) { netif_set_up(&verbinding_mobiel); return 0; }
    if (Aksie == 2) { netif_set_down(&verbinding_mobiel); return 0; }
    if (Aksie != 0) return -22;
    /* 유니캐스트 IPv4, 연속 masker_VALUE, 같은 망의 선택적 verstekwaarde deurgang_VALUE. */
    uint32_t 뒤집은가림 = ~masker_VALUE;
    if (!masker_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !adres || (adres >> 24) == 127 ||
        (adres >> 24) == 0 || (adres >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(adres & 뒤집은가림) || (adres & 뒤집은가림) == 뒤집은가림)) ||
        (deurgang_VALUE && ((deurgang_VALUE & masker_VALUE) != (adres & masker_VALUE) || deurgang_VALUE == adres || (deurgang_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(deurgang_VALUE & 뒤집은가림) || (deurgang_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 adres 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_kategorie &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].verbinding_kontrole && ip_addr_isany(&통신끝점들[INDEX].verbinding_kontrole->local_ip))) return -16;
    if(유선사용)dhcp_stop(&verbinding_mobiel);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(adres)); ip4_addr_set_u32(&새가림, lwip_htonl(masker_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(deurgang_VALUE));
    netif_set_addr(&verbinding_mobiel, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *beëindig_p, struct pbuf *data, const ip_addr_t *adres) {
    (void)인수; (void)beëindig_p;
    unsigned char 머리[20], antwoord[16];
    if (응답상태 != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adres))) != 시험주소 || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Loopkop_verstel = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Loopkop_verstel < 20 || data->tot_len < Loopkop_verstel + 16 ||
        pbuf_copy_partial(data, antwoord, 16, Loopkop_verstel) != 16 || antwoord[0] || antwoord[1] ||
        (((unsigned)antwoord[4] << 8) | antwoord[5]) != 시험식별자 ||
        (((unsigned)antwoord[6] << 8) | antwoord[7]) != 시험순서 ||
        antwoord[8] != 'J' || antwoord[9] != 'K' || antwoord[10] != 'O' || antwoord[11] != 'S' ||
        (((uint32_t)antwoord[12] << 24) | ((uint32_t)antwoord[13] << 16) | ((uint32_t)antwoord[14] << 8) | antwoord[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Loopkop_verstel)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Loopkop_verstel); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(data); return 1;
}
int 응답시험시작(uint32_t adres, unsigned volgorde_VALUE) {
    if (!준비됨 || !netif_is_up(&verbinding_mobiel)) return -100;
    if (!adres || (adres >> 28) >= 14 || adres == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = adres; 시험순서 = volgorde_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = 시험순서 >> 8; data[7] = 시험순서;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=시험시각 >> 24; data[13]=시험시각 >> 16; data[14]=시험시각 >> 8; data[15]=시험시각;
    for (unsigned plaas_INDEX = 16; plaas_INDEX < sizeof(data); plaas_INDEX++) data[plaas_INDEX] = plaas_INDEX;
    uint16_t 확인합 = inet_chksum(data, sizeof(data)); memcpy(data + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(adres));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned inskrywing_VALUE) {
    통신망살피기();
    return inskrywing_VALUE == 0 ? 응답상태 : inskrywing_VALUE == 1 ? (int)응답시간 : inskrywing_VALUE == 2 ? (int)응답차례 : -22;
}
