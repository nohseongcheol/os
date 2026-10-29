#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Netwọọkụ_ikpo.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../ebe_dị̀anyā_valuu/ebe_dị̀anyā_valuu.h"
#include "èjìrìwayàrụ_Netwọọkụ.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif njikọ_njìarụ;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int pinye_otu, 수신창구, 대기중, 연결됨, ọbọakwụkwọ_mèdebe, mmejọ;
    struct tcp_pcb *njikọ_njizi;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char datà[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], ibè_àdreèsì;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int ọbọakwụkwọ_ebenjìaka) { return ọbọakwụkwọ_ebenjìaka >= 0 && ọbọakwụkwọ_ebenjìaka < 32 && 통신끝점들[ọbọakwụkwọ_ebenjìaka].pinye_otu ? &통신끝점들[ọbọakwụkwọ_ebenjìaka] : 0; }
static int 예약하기(int pinye_otu) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].pinye_otu) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].pinye_otu = pinye_otu; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned koòdù_nkeakàrà) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = koòdù_nkeakàrà; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *àdreèsì) {
    (void)개수; (void)àdreèsì;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned koòdù_nkeakàrà = ((unsigned char *)다음위치->payload)[순번];
        if (koòdù_nkeakàrà == 192 || koòdù_nkeakàrà == 219) { 내보내기(219); 내보내기(koòdù_nkeakàrà == 192 ? 220 : 221); } else 내보내기(koòdù_nkeakàrà);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t Kwado_ọgịga_oge_otu_asụsụ(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Kwado_Netwọọkụ(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    기계저장기(보조장치 + 4) |= 1; 기계저장기(보조장치 + 0x60) = 0; 기계저장기(보조장치 + 0x44) = 0;
    기계저장기(보조장치 + 0x48) = 0xc6; 기계저장기(보조장치 + 0x4c) = 3; 기계저장기(보조장치 + 0x68) = 270; 기계저장기(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t adreesi_ịntaneèt, bit_mkpù, ụzọmbànye_àdreèsì;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&adreesi_ịntaneèt, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_mkpù, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&ụzọmbànye_àdreèsì, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&njikọ_njìarụ, &adreesi_ịntaneèt, &bit_mkpù, &ụzọmbànye_àdreèsì, 0, 유선사용?Kwado_èjìrìwayàrụ_Netwọọkụ:Kwado_ọgịga_oge_otu_asụsụ, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&njikọ_njìarụ); netif_set_up(&njikọ_njìarụ);if(!유선사용)netif_set_link_up(&njikọ_njìarụ); 준비됨 = 1;
    Kwado_ebe_dị̀anyā();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *nzìfèozī_njizi_gbochie, struct pbuf *자료위치, err_t mmejọ) {
    통신끝점 *ùsòròokwū_datà = 부가인수; (void)nzìfèozī_njizi_gbochie; (void)mmejọ;
    if (!자료위치) { ùsòròokwū_datà->ọbọakwụkwọ_mèdebe = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(ùsòròokwū_datà->datà) - ùsòròokwū_datà->항목수) return ERR_MEM;
    unsigned 현재위치 = (ùsòròokwū_datà->맨앞 + ùsòròokwū_datà->항목수) % sizeof(ùsòròokwū_datà->datà);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        ùsòròokwū_datà->datà[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(ùsòròokwū_datà->datà);
    }
    ùsòròokwū_datà->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t mmejọ) { 통신끝점 *ùsòròokwū_datà = 부가인수; ùsòròokwū_datà->njikọ_njizi = 0; ùsòròokwū_datà->mmejọ = 오류번호(mmejọ); }
static void 되부름목록(통신끝점 *ùsòròokwū_datà) { tcp_arg(ùsòròokwū_datà->njikọ_njizi, ùsòròokwū_datà); tcp_recv(ùsòròokwū_datà->njikọ_njizi, 수신됨); tcp_err(ùsòròokwū_datà->njikọ_njizi, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *nzìfèozī_njizi_gbochie, err_t mmejọ) {
    통신끝점 *ùsòròokwū_datà = 부가인수; (void)nzìfèozī_njizi_gbochie; if (mmejọ) ùsòròokwū_datà->mmejọ = 오류번호(mmejọ); else ùsòròokwū_datà->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *nzìfèozī_njizi_gbochie, err_t mmejọ) {
    통신끝점 *부모항목 = 부가인수; if (mmejọ) return mmejọ;
    int ọbọakwụkwọ_ebenjìaka = 예약하기(1); if (ọbọakwụkwọ_ebenjìaka < 0) return ERR_MEM;
    통신끝점 *ùsòròokwū_datà = &통신끝점들[ọbọakwụkwọ_ebenjìaka]; ùsòròokwū_datà->njikọ_njizi = nzìfèozī_njizi_gbochie; ùsòròokwū_datà->연결됨 = 1; ùsòròokwū_datà->대기중 = (int)(부모항목 - 통신끝점들);
    ùsòròokwū_datà->ibè_àdreèsì = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&nzìfèozī_njizi_gbochie->remote_ip))); ùsòròokwū_datà->상대창구번호 = nzìfèozī_njizi_gbochie->remote_port;
    되부름목록(ùsòròokwū_datà); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *nzìfèozī_njizi_gbochie, struct pbuf *자료위치, const ip_addr_t *àdreèsì, u16_t 접속번호) {
    통신끝점 *ùsòròokwū_datà = 부가인수; (void)nzìfèozī_njizi_gbochie;
    if (ùsòròokwū_datà->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (ùsòròokwū_datà->맨앞 + ùsòròokwū_datà->항목수) % 4;
        pbuf_copy_partial(자료위치, ùsòròokwū_datà->datà + 자리 * 512, 자료위치->tot_len, 0);
        ùsòròokwū_datà->길이목록[자리] = 자료위치->tot_len; ùsòròokwū_datà->접속번호들[자리] = 접속번호;
        ùsòròokwū_datà->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(àdreèsì))); ùsòròokwū_datà->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int pinye_otu) {
    if (!준비됨) return -100;
    if (pinye_otu != 1 && pinye_otu != 2) return -93;
    int ọbọakwụkwọ_ebenjìaka = 예약하기(pinye_otu); if (ọbọakwụkwọ_ebenjìaka < 0) return ọbọakwụkwọ_ebenjìaka;
    통신끝점 *ùsòròokwū_datà = &통신끝점들[ọbọakwụkwọ_ebenjìaka];
    if (pinye_otu == 1) { ùsòròokwū_datà->njikọ_njizi = tcp_new(); if (ùsòròokwū_datà->njikọ_njizi) 되부름목록(ùsòròokwū_datà); }
    else { ùsòròokwū_datà->전문제어 = udp_new(); if (ùsòròokwū_datà->전문제어) udp_recv(ùsòròokwū_datà->전문제어, 전문, ùsòròokwū_datà); }
    if (!ùsòròokwū_datà->njikọ_njizi && !ùsòròokwū_datà->전문제어) { ùsòròokwū_datà->pinye_otu = 0; return -12; } return ọbọakwụkwọ_ebenjìaka;
}
int 망주소묶기(int ọbọakwụkwọ_ebenjìaka, uint32_t àdreèsì, unsigned 접속번호) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà) return -9;
    if (접속번호 > 65535 || (àdreèsì && àdreèsì != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&njikọ_njìarụ))) && àdreèsì != 0x7f000001)) return -99;
    ip_addr_t adreesi_ịntaneèt; ip_addr_set_ip4_u32(&adreesi_ịntaneèt, lwip_htonl(àdreèsì));
    err_t 보조항목 = ùsòròokwū_datà->pinye_otu == 1 ? tcp_bind(ùsòròokwū_datà->njikọ_njizi, &adreesi_ịntaneèt, 접속번호) : udp_bind(ùsòròokwū_datà->전문제어, &adreesi_ịntaneèt, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int ọbọakwụkwọ_ebenjìaka) { 통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (ùsòròokwū_datà && ùsòròokwū_datà->njikọ_njizi) ip_set_option(ùsòròokwū_datà->njikọ_njizi, SOF_REUSEADDR); }
int 연결기다리기(int ọbọakwụkwọ_ebenjìaka) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà || ùsòròokwū_datà->pinye_otu != 1) return -9;
    if (ùsòròokwū_datà->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *nzìfèozī_njizi_gbochie = tcp_listen_with_backlog_and_err(ùsòròokwū_datà->njikọ_njizi, 4, &보조항목);
    if (!nzìfèozī_njizi_gbochie) return 오류번호(보조항목); ùsòròokwū_datà->njikọ_njizi = nzìfèozī_njizi_gbochie; ùsòròokwū_datà->수신창구 = 1; tcp_arg(nzìfèozī_njizi_gbochie, ùsòròokwū_datà); tcp_accept(nzìfèozī_njizi_gbochie, 연결받음); return 0;
}
int 망연결하기(int ọbọakwụkwọ_ebenjìaka, uint32_t àdreèsì, unsigned 접속번호) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà || ùsòròokwū_datà->pinye_otu != 1) return -9;
    if (ùsòròokwū_datà->mmejọ) return ùsòròokwū_datà->mmejọ;
    if (ùsòròokwū_datà->연결됨) return 0;
    if (ùsòròokwū_datà->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !àdreèsì) return -22;
    ip_addr_t adreesi_ịntaneèt; ip_addr_set_ip4_u32(&adreesi_ịntaneèt, lwip_htonl(àdreèsì));
    ùsòròokwū_datà->ibè_àdreèsì = àdreèsì; ùsòròokwū_datà->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(ùsòròokwū_datà->njikọ_njizi, &adreesi_ịntaneèt, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int ọbọakwụkwọ_ebenjìaka) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà || !ùsòròokwū_datà->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].pinye_otu == 1 && 통신끝점들[순번].대기중 == ọbọakwụkwọ_ebenjìaka) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int ọbọakwụkwọ_ebenjìaka, void *datà, unsigned 개수) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà || ùsòròokwū_datà->pinye_otu != 1) return -9;
    if (!개수) return 0; if (!ùsòròokwū_datà->항목수) return ùsòròokwū_datà->mmejọ ? ùsòròokwū_datà->mmejọ : ùsòròokwū_datà->ọbọakwụkwọ_mèdebe ? 0 : -11;
    if (개수 > ùsòròokwū_datà->항목수) 개수 = ùsòròokwū_datà->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)datà)[순번] = ùsòròokwū_datà->datà[ùsòròokwū_datà->맨앞]; ùsòròokwū_datà->맨앞 = (ùsòròokwū_datà->맨앞 + 1) % sizeof(ùsòròokwū_datà->datà); }
    ùsòròokwū_datà->항목수 -= 개수; if (ùsòròokwū_datà->njikọ_njizi) tcp_recved(ùsòròokwū_datà->njikọ_njizi, 개수); return 개수;
}
int 통신쓰기(int ọbọakwụkwọ_ebenjìaka, const void *datà, unsigned 개수) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà || ùsòròokwū_datà->pinye_otu != 1) return -9;
    if (ùsòròokwū_datà->mmejọ) return ùsòròokwū_datà->mmejọ; if (!ùsòròokwū_datà->njikọ_njizi || !ùsòròokwū_datà->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(ùsòròokwū_datà->njikọ_njizi)) 개수 = tcp_sndbuf(ùsòròokwū_datà->njikọ_njizi);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(ùsòròokwū_datà->njikọ_njizi, datà, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(ùsòròokwū_datà->njikọ_njizi); return 개수;
}
int 전문보내기(int ọbọakwụkwọ_ebenjìaka, const void *datà, unsigned 개수, uint32_t àdreèsì, unsigned 접속번호) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà || ùsòròokwū_datà->pinye_otu != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, datà, 개수); ip_addr_t adreesi_ịntaneèt; ip_addr_set_ip4_u32(&adreesi_ịntaneèt, lwip_htonl(àdreèsì));
    err_t 보조항목 = udp_sendto(ùsòròokwū_datà->전문제어, 자료위치, &adreesi_ịntaneèt, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int ọbọakwụkwọ_ebenjìaka, void *datà, unsigned 개수) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà || ùsòròokwū_datà->pinye_otu != 2) return -9;
    if (!ùsòròokwū_datà->항목수) return -11; unsigned 현재위치 = ùsòròokwū_datà->맨앞;
    if (개수 > ùsòròokwū_datà->길이목록[현재위치]) 개수 = ùsòròokwū_datà->길이목록[현재위치]; memcpy(datà, ùsòròokwū_datà->datà + 현재위치 * 512, 개수);
    ùsòròokwū_datà->상대창구번호 = ùsòròokwū_datà->접속번호들[현재위치]; ùsòròokwū_datà->ibè_àdreèsì = ùsòròokwū_datà->주소목록[현재위치]; ùsòròokwū_datà->맨앞 = (현재위치 + 1) % 4; ùsòròokwū_datà->항목수--; return 개수;
}
unsigned 통신접속번호(int ọbọakwụkwọ_ebenjìaka) { 통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); return !ùsòròokwū_datà ? 0 : ùsòròokwū_datà->njikọ_njizi ? ùsòròokwū_datà->njikọ_njizi->local_port : ùsòròokwū_datà->전문제어 ? ùsòròokwū_datà->전문제어->local_port : 0; }
unsigned 상대접속번호(int ọbọakwụkwọ_ebenjìaka) { 통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); return ùsòròokwū_datà ? ùsòròokwū_datà->상대창구번호 : 0; }
uint32_t 상대통신주소(int ọbọakwụkwọ_ebenjìaka) { 통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); return ùsòròokwū_datà ? ùsòròokwū_datà->ibè_àdreèsì : 0; }
void mmechi_Netwọọkụ(int ọbọakwụkwọ_ebenjìaka) {
    통신끝점 *ùsòròokwū_datà = 얻기(ọbọakwụkwọ_ebenjìaka); if (!ùsòròokwū_datà) return;
    if (ùsòròokwū_datà->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].pinye_otu && 통신끝점들[순번].대기중 == ọbọakwụkwọ_ebenjìaka) mmechi_Netwọọkụ(순번);
    if (ùsòròokwū_datà->njikọ_njizi) {
        tcp_arg(ùsòròokwū_datà->njikọ_njizi, 0); if (ùsòròokwū_datà->수신창구) tcp_accept(ùsòròokwū_datà->njikọ_njizi, 0); else { tcp_recv(ùsòròokwū_datà->njikọ_njizi, 0); tcp_err(ùsòròokwū_datà->njikọ_njizi, 0); }
        if (tcp_close(ùsòròokwū_datà->njikọ_njizi) != ERR_OK) tcp_abort(ùsòròokwū_datà->njikọ_njizi);
    }
    if (ùsòròokwū_datà->전문제어) udp_remove(ùsòròokwū_datà->전문제어); ùsòròokwū_datà->pinye_otu = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&njikọ_njìarụ);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (기계저장기(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned koòdù_nkeakàrà = 기계저장기(보조장치 + 0x40) & 255;
        if (koòdù_nkeakàrà == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (njikọ_njìarụ.input(자료위치, &njikọ_njìarụ) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (koòdù_nkeakàrà == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (koòdù_nkeakàrà != 220 && koòdù_nkeakàrà != 221) 수신오류 = 1; koòdù_nkeakàrà = koòdù_nkeakàrà == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = koòdù_nkeakàrà; else 수신오류 = 1;
        }
    }
    netif_poll(&njikọ_njìarụ); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (기계저장기(보조장치 + 0x54) & 0x20); 처리한도++) {
        기계저장기(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Mwube·조회는 lwIP의 ǹdịnezie_datà 인터페이스와 mèdebe_akara 표를 사용한다. */
uint32_t 망상태읽기(unsigned ndebà_valuu, unsigned indèks) {
    if(ndebà_valuu==20)return 유선사용;
    if(ndebà_valuu==21)return 준비됨&&netif_is_link_up(&njikọ_njìarụ);
    if(ndebà_valuu==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&ndebà_valuu>=4&&ndebà_valuu<=8)return 유선망집계(ndebà_valuu-4);
    if (ndebà_valuu == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&njikọ_njìarụ)));
    if (ndebà_valuu == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&njikọ_njìarụ)));
    if (ndebà_valuu == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&njikọ_njìarụ)));
    if (ndebà_valuu == 3) return netif_is_up(&njikọ_njìarụ) != 0;
    if (ndebà_valuu == 4) return 받은전문수;
    if (ndebà_valuu == 5) return 보낸전문수;
    if (ndebà_valuu == 6) return 받은바이트수;
    if (ndebà_valuu == 7) return 보낸바이트수;
    if (ndebà_valuu == 8) return 버린전문수;
    if (ndebà_valuu == 9) return 송신개수;
    if (indèks >= 32) return 0;
    통신끝점 *mèdebe_akara = &통신끝점들[indèks];
    if (ndebà_valuu == 10) return mèdebe_akara->pinye_otu;
    if (!mèdebe_akara->pinye_otu) return 0;
    if (ndebà_valuu == 11) return 통신접속번호(indèks);
    if (ndebà_valuu == 12) return mèdebe_akara->ibè_àdreèsì;
    if (ndebà_valuu == 13) return mèdebe_akara->상대창구번호;
    if (ndebà_valuu == 14) return mèdebe_akara->수신창구 ? 1 : mèdebe_akara->ọbọakwụkwọ_mèdebe ? 3 : mèdebe_akara->mmejọ ? 4 : mèdebe_akara->연결됨 ? 2 : 0;
    if (ndebà_valuu == 15) return mèdebe_akara->항목수;
    if (ndebà_valuu == 16) {
        const ip_addr_t *àdreèsì = mèdebe_akara->pinye_otu == 1 && mèdebe_akara->njikọ_njizi ? &mèdebe_akara->njikọ_njizi->local_ip :
            mèdebe_akara->pinye_otu == 2 && mèdebe_akara->전문제어 ? &mèdebe_akara->전문제어->local_ip : 0;
        return àdreèsì ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(àdreèsì))) : 0;
    }
    return 0;
}

int hàkọọ_ngwaāhụ_kọmputa_Netwọọkụ(unsigned mmèm, uint32_t àdreèsì, uint32_t mkpù_valuu, uint32_t ụzọmbànye_valuu) {
    if (!준비됨) return -100;
    if (mmèm == 1) { netif_set_up(&njikọ_njìarụ); return 0; }
    if (mmèm == 2) { netif_set_down(&njikọ_njìarụ); return 0; }
    if (mmèm != 0) return -22;
    /* 유니캐스트 IPv4, 연속 mkpù_valuu, 같은 망의 선택적 Ngwa_ihe_dịadị ụzọmbànye_valuu. */
    uint32_t 뒤집은가림 = ~mkpù_valuu;
    if (!mkpù_valuu || (뒤집은가림 & (뒤집은가림 + 1)) || !àdreèsì || (àdreèsì >> 24) == 127 ||
        (àdreèsì >> 24) == 0 || (àdreèsì >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(àdreèsì & 뒤집은가림) || (àdreèsì & 뒤집은가림) == 뒤집은가림)) ||
        (ụzọmbànye_valuu && ((ụzọmbànye_valuu & mkpù_valuu) != (àdreèsì & mkpù_valuu) || ụzọmbànye_valuu == àdreèsì || (ụzọmbànye_valuu >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(ụzọmbànye_valuu & 뒤집은가림) || (ụzọmbànye_valuu & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 àdreèsì 변경으로 몰래 끊지 않는다. */
    for (unsigned indèks = 0; indèks < 32; indèks++) if (통신끝점들[indèks].pinye_otu &&
        !(통신끝점들[indèks].수신창구 && 통신끝점들[indèks].njikọ_njizi && ip_addr_isany(&통신끝점들[indèks].njikọ_njizi->local_ip))) return -16;
    if(유선사용)dhcp_stop(&njikọ_njìarụ);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(àdreèsì)); ip4_addr_set_u32(&새가림, lwip_htonl(mkpù_valuu)); ip4_addr_set_u32(&새관문, lwip_htonl(ụzọmbànye_valuu));
    netif_set_addr(&njikọ_njìarụ, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *mèdebe_akara, struct pbuf *datà, const ip_addr_t *àdreèsì) {
    (void)인수; (void)mèdebe_akara;
    unsigned char 머리[20], nzaghachi[16];
    if (응답상태 != -11 || datà->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(àdreèsì))) != 시험주소 || pbuf_copy_partial(datà, 머리, 20, 0) != 20) return 0;
    unsigned isi_ụha = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || isi_ụha < 20 || datà->tot_len < isi_ụha + 16 ||
        pbuf_copy_partial(datà, nzaghachi, 16, isi_ụha) != 16 || nzaghachi[0] || nzaghachi[1] ||
        (((unsigned)nzaghachi[4] << 8) | nzaghachi[5]) != 시험식별자 ||
        (((unsigned)nzaghachi[6] << 8) | nzaghachi[7]) != 시험순서 ||
        nzaghachi[8] != 'J' || nzaghachi[9] != 'K' || nzaghachi[10] != 'O' || nzaghachi[11] != 'S' ||
        (((uint32_t)nzaghachi[12] << 24) | ((uint32_t)nzaghachi[13] << 16) | ((uint32_t)nzaghachi[14] << 8) | nzaghachi[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(datà, isi_ụha)) return 0;
    if (inet_chksum_pbuf(datà)) { pbuf_add_header(datà, isi_ụha); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(datà); return 1;
}
int 응답시험시작(uint32_t àdreèsì, unsigned ùsòrò_valuu) {
    if (!준비됨 || !netif_is_up(&njikọ_njìarụ)) return -100;
    if (!àdreèsì || (àdreèsì >> 28) >= 14 || àdreèsì == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = àdreèsì; 시험순서 = ùsòrò_valuu & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char datà[32] = {8,0,0,0};
    datà[4] = 시험식별자 >> 8; datà[5] = 시험식별자; datà[6] = 시험순서 >> 8; datà[7] = 시험순서;
    datà[8]='J'; datà[9]='K'; datà[10]='O'; datà[11]='S';
    datà[12]=시험시각 >> 24; datà[13]=시험시각 >> 16; datà[14]=시험시각 >> 8; datà[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(datà); 자리++) datà[자리] = 자리;
    uint16_t 확인합 = inet_chksum(datà, sizeof(datà)); memcpy(datà + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(datà), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, datà, sizeof(datà)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(àdreèsì));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned ndebà_valuu) {
    통신망살피기();
    return ndebà_valuu == 0 ? 응답상태 : ndebà_valuu == 1 ? (int)응답시간 : ndebà_valuu == 2 ? (int)응답차례 : -22;
}
