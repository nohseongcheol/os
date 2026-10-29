#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Net_bunki.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../fjartengdur_VALUE/fjartengdur_VALUE.h"
#include "vírað_Net.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define vél_skrá(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif tenging_tæki;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_bæti_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_tegund, 수신창구, upplýsingatækni_Í_bið, 연결됨, skrá_ljúka, Villa;
    struct tcp_pcb *tenging_stýring;
    struct udp_pcb *전문제어;
    unsigned myndavél_að_framan_færsla, færsla_COUNT;
    unsigned char gögn[4096];
    unsigned 길이목록[4], 접속번호들[4], jafningi_endastöð_númer;
    uint32_t 주소목록[4], jafningi_slóð;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int villa_númer(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *sækja_VALUE(int skrá_hald) { return skrá_hald >= 0 && skrá_hald < 32 && 통신끝점들[skrá_hald].TYPE_tegund ? &통신끝점들[skrá_hald] : 0; }
static int 예약하기(int TYPE_tegund) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_tegund) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_tegund = TYPE_tegund; 통신끝점들[순번].upplýsingatækni_Í_bið = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned stafkóði) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = stafkóði; }
static err_t úttak_54cd5e1d(struct netif *vara_COUNT, struct pbuf *gögn_staða, const ip4_addr_t *slóð) {
    (void)vara_COUNT; (void)slóð;
    if (gögn_staða->tot_len > 1500 || 송신개수 + 2 * gögn_staða->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Áfram_OFFSET = gögn_staða; Áfram_OFFSET; Áfram_OFFSET = Áfram_OFFSET->next) for (unsigned 순번 = 0; 순번 < Áfram_OFFSET->len; 순번++) {
        unsigned stafkóði = ((unsigned char *)Áfram_OFFSET->payload)[순번];
        if (stafkóði == 192 || stafkóði == 219) { 내보내기(219); 내보내기(stafkóði == 192 ? 220 : 221); } else 내보내기(stafkóði);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += gögn_staða->tot_len; return ERR_OK;
}
static err_t Undirbúa_CLR(struct netif *vara_COUNT) { vara_COUNT->name[0] = 's'; vara_COUNT->name[1] = 'l'; vara_COUNT->mtu = 1500; vara_COUNT->output = úttak_54cd5e1d; return ERR_OK; }
void Undirbúa_Net(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    vél_skrá(보조장치 + 4) |= 1; vél_skrá(보조장치 + 0x60) = 0; vél_skrá(보조장치 + 0x44) = 0;
    vél_skrá(보조장치 + 0x48) = 0xc6; vél_skrá(보조장치 + 0x4c) = 3; vél_skrá(보조장치 + 0x68) = 270; vél_skrá(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t veffang, biti_sía, gátt_slóð;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&veffang, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&biti_sía, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gátt_slóð, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&tenging_tæki, &veffang, &biti_sía, &gátt_slóð, 0, 유선사용?Undirbúa_vírað_Net:Undirbúa_CLR, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&tenging_tæki); netif_set_up(&tenging_tæki);if(!유선사용)netif_set_link_up(&tenging_tæki); 준비됨 = 1;
    Undirbúa_fjartengdur();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *sending_stýring_útiloka, struct pbuf *gögn_staða, err_t Villa) {
    통신끝점 *strengur_gögn = 부가인수; (void)sending_stýring_útiloka; (void)Villa;
    if (!gögn_staða) { strengur_gögn->skrá_ljúka = 1; return ERR_OK; }
    if (gögn_staða->tot_len > sizeof(strengur_gögn->gögn) - strengur_gögn->færsla_COUNT) return ERR_MEM;
    unsigned 현재위치 = (strengur_gögn->myndavél_að_framan_færsla + strengur_gögn->færsla_COUNT) % sizeof(strengur_gögn->gögn);
    for (struct pbuf *Áfram_OFFSET = gögn_staða; Áfram_OFFSET; Áfram_OFFSET = Áfram_OFFSET->next) for (unsigned 순번 = 0; 순번 < Áfram_OFFSET->len; 순번++) {
        strengur_gögn->gögn[현재위치] = ((unsigned char *)Áfram_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(strengur_gögn->gögn);
    }
    strengur_gögn->færsla_COUNT += gögn_staða->tot_len; pbuf_free(gögn_staða); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Villa) { 통신끝점 *strengur_gögn = 부가인수; strengur_gögn->tenging_stýring = 0; strengur_gögn->Villa = villa_númer(Villa); }
static void 되부름목록(통신끝점 *strengur_gögn) { tcp_arg(strengur_gögn->tenging_stýring, strengur_gögn); tcp_recv(strengur_gögn->tenging_stýring, 수신됨); tcp_err(strengur_gögn->tenging_stýring, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *sending_stýring_útiloka, err_t Villa) {
    통신끝점 *strengur_gögn = 부가인수; (void)sending_stýring_útiloka; if (Villa) strengur_gögn->Villa = villa_númer(Villa); else strengur_gögn->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *sending_stýring_útiloka, err_t Villa) {
    통신끝점 *yfireining = 부가인수; if (Villa) return Villa;
    int skrá_hald = 예약하기(1); if (skrá_hald < 0) return ERR_MEM;
    통신끝점 *strengur_gögn = &통신끝점들[skrá_hald]; strengur_gögn->tenging_stýring = sending_stýring_útiloka; strengur_gögn->연결됨 = 1; strengur_gögn->upplýsingatækni_Í_bið = (int)(yfireining - 통신끝점들);
    strengur_gögn->jafningi_slóð = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&sending_stýring_útiloka->remote_ip))); strengur_gögn->jafningi_endastöð_númer = sending_stýring_útiloka->remote_port;
    되부름목록(strengur_gögn); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *sending_stýring_útiloka, struct pbuf *gögn_staða, const ip_addr_t *slóð, u16_t tengisnúmer) {
    통신끝점 *strengur_gögn = 부가인수; (void)sending_stýring_útiloka;
    if (strengur_gögn->færsla_COUNT < 4 && gögn_staða->tot_len <= 512) {
        unsigned staða_INDEX = (strengur_gögn->myndavél_að_framan_færsla + strengur_gögn->færsla_COUNT) % 4;
        pbuf_copy_partial(gögn_staða, strengur_gögn->gögn + staða_INDEX * 512, gögn_staða->tot_len, 0);
        strengur_gögn->길이목록[staða_INDEX] = gögn_staða->tot_len; strengur_gögn->접속번호들[staða_INDEX] = tengisnúmer;
        strengur_gögn->주소목록[staða_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(slóð))); strengur_gögn->færsla_COUNT++;
    }
    pbuf_free(gögn_staða);
}
int 통신끝점만들기(int TYPE_tegund) {
    if (!준비됨) return -100;
    if (TYPE_tegund != 1 && TYPE_tegund != 2) return -93;
    int skrá_hald = 예약하기(TYPE_tegund); if (skrá_hald < 0) return skrá_hald;
    통신끝점 *strengur_gögn = &통신끝점들[skrá_hald];
    if (TYPE_tegund == 1) { strengur_gögn->tenging_stýring = tcp_new(); if (strengur_gögn->tenging_stýring) 되부름목록(strengur_gögn); }
    else { strengur_gögn->전문제어 = udp_new(); if (strengur_gögn->전문제어) udp_recv(strengur_gögn->전문제어, 전문, strengur_gögn); }
    if (!strengur_gögn->tenging_stýring && !strengur_gögn->전문제어) { strengur_gögn->TYPE_tegund = 0; return -12; } return skrá_hald;
}
int nettó_BIND(int skrá_hald, uint32_t slóð, unsigned tengisnúmer) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn) return -9;
    if (tengisnúmer > 65535 || (slóð && slóð != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&tenging_tæki))) && slóð != 0x7f000001)) return -99;
    ip_addr_t veffang; ip_addr_set_ip4_u32(&veffang, lwip_htonl(slóð));
    err_t 보조항목 = strengur_gögn->TYPE_tegund == 1 ? tcp_bind(strengur_gögn->tenging_stýring, &veffang, tengisnúmer) : udp_bind(strengur_gögn->전문제어, &veffang, tengisnúmer); return 보조항목 ? villa_númer(보조항목) : 0;
}
void 통신주소재사용(int skrá_hald) { 통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (strengur_gögn && strengur_gögn->tenging_stýring) ip_set_option(strengur_gögn->tenging_stýring, SOF_REUSEADDR); }
int nettó_hlusta(int skrá_hald) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn || strengur_gögn->TYPE_tegund != 1) return -9;
    if (strengur_gögn->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *sending_stýring_útiloka = tcp_listen_with_backlog_and_err(strengur_gögn->tenging_stýring, 4, &보조항목);
    if (!sending_stýring_útiloka) return villa_númer(보조항목); strengur_gögn->tenging_stýring = sending_stýring_útiloka; strengur_gögn->수신창구 = 1; tcp_arg(sending_stýring_útiloka, strengur_gögn); tcp_accept(sending_stýring_útiloka, 연결받음); return 0;
}
int nettó_TENGJA(int skrá_hald, uint32_t slóð, unsigned tengisnúmer) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn || strengur_gögn->TYPE_tegund != 1) return -9;
    if (strengur_gögn->Villa) return strengur_gögn->Villa;
    if (strengur_gögn->연결됨) return 0;
    if (strengur_gögn->jafningi_endastöð_númer) return -115;
    if (!tengisnúmer || tengisnúmer > 65535 || !slóð) return -22;
    ip_addr_t veffang; ip_addr_set_ip4_u32(&veffang, lwip_htonl(slóð));
    strengur_gögn->jafningi_slóð = slóð; strengur_gögn->jafningi_endastöð_númer = tengisnúmer;
    err_t 보조항목 = tcp_connect(strengur_gögn->tenging_stýring, &veffang, tengisnúmer, 연결됨); return 보조항목 ? villa_númer(보조항목) : -115;
}
int nettó_samþykkja(int skrá_hald) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn || !strengur_gögn->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_tegund == 1 && 통신끝점들[순번].upplýsingatækni_Í_bið == skrá_hald) { 통신끝점들[순번].upplýsingatækni_Í_bið = -1; return 순번; }
    return -11;
}
int 통신읽기(int skrá_hald, void *gögn, unsigned vara_COUNT) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn || strengur_gögn->TYPE_tegund != 1) return -9;
    if (!vara_COUNT) return 0; if (!strengur_gögn->færsla_COUNT) return strengur_gögn->Villa ? strengur_gögn->Villa : strengur_gögn->skrá_ljúka ? 0 : -11;
    if (vara_COUNT > strengur_gögn->færsla_COUNT) vara_COUNT = strengur_gögn->færsla_COUNT;
    for (unsigned 순번 = 0; 순번 < vara_COUNT; 순번++) { ((unsigned char *)gögn)[순번] = strengur_gögn->gögn[strengur_gögn->myndavél_að_framan_færsla]; strengur_gögn->myndavél_að_framan_færsla = (strengur_gögn->myndavél_að_framan_færsla + 1) % sizeof(strengur_gögn->gögn); }
    strengur_gögn->færsla_COUNT -= vara_COUNT; if (strengur_gögn->tenging_stýring) tcp_recved(strengur_gögn->tenging_stýring, vara_COUNT); return vara_COUNT;
}
int nettó_skrifa(int skrá_hald, const void *gögn, unsigned vara_COUNT) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn || strengur_gögn->TYPE_tegund != 1) return -9;
    if (strengur_gögn->Villa) return strengur_gögn->Villa; if (!strengur_gögn->tenging_stýring || !strengur_gögn->연결됨) return -107;
    if (!vara_COUNT) return 0; if (vara_COUNT > tcp_sndbuf(strengur_gögn->tenging_stýring)) vara_COUNT = tcp_sndbuf(strengur_gögn->tenging_stýring);
    if (!vara_COUNT) return -11; if (vara_COUNT > 1024) vara_COUNT = 1024;
    err_t 보조항목 = tcp_write(strengur_gögn->tenging_stýring, gögn, vara_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return villa_númer(보조항목);
    tcp_output(strengur_gögn->tenging_stýring); return vara_COUNT;
}
int 전문보내기(int skrá_hald, const void *gögn, unsigned vara_COUNT, uint32_t slóð, unsigned tengisnúmer) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn || strengur_gögn->TYPE_tegund != 2) return -9;
    if (vara_COUNT > 512) return -90; if (!tengisnúmer || tengisnúmer > 65535) return -22;
    struct pbuf *gögn_staða = pbuf_alloc(PBUF_TRANSPORT, vara_COUNT, PBUF_RAM); if (!gögn_staða) return -11;
    pbuf_take(gögn_staða, gögn, vara_COUNT); ip_addr_t veffang; ip_addr_set_ip4_u32(&veffang, lwip_htonl(slóð));
    err_t 보조항목 = udp_sendto(strengur_gögn->전문제어, gögn_staða, &veffang, tengisnúmer); pbuf_free(gögn_staða); return 보조항목 ? villa_númer(보조항목) : (int)vara_COUNT;
}
int 전문받기(int skrá_hald, void *gögn, unsigned vara_COUNT) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn || strengur_gögn->TYPE_tegund != 2) return -9;
    if (!strengur_gögn->færsla_COUNT) return -11; unsigned 현재위치 = strengur_gögn->myndavél_að_framan_færsla;
    if (vara_COUNT > strengur_gögn->길이목록[현재위치]) vara_COUNT = strengur_gögn->길이목록[현재위치]; memcpy(gögn, strengur_gögn->gögn + 현재위치 * 512, vara_COUNT);
    strengur_gögn->jafningi_endastöð_númer = strengur_gögn->접속번호들[현재위치]; strengur_gögn->jafningi_slóð = strengur_gögn->주소목록[현재위치]; strengur_gögn->myndavél_að_framan_færsla = (현재위치 + 1) % 4; strengur_gögn->færsla_COUNT--; return vara_COUNT;
}
unsigned Net_tengisnúmer(int skrá_hald) { 통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); return !strengur_gögn ? 0 : strengur_gögn->tenging_stýring ? strengur_gögn->tenging_stýring->local_port : strengur_gögn->전문제어 ? strengur_gögn->전문제어->local_port : 0; }
unsigned jafningi_tengisnúmer(int skrá_hald) { 통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); return strengur_gögn ? strengur_gögn->jafningi_endastöð_númer : 0; }
uint32_t nettó_jafningi_slóð(int skrá_hald) { 통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); return strengur_gögn ? strengur_gögn->jafningi_slóð : 0; }
void loka_Net(int skrá_hald) {
    통신끝점 *strengur_gögn = sækja_VALUE(skrá_hald); if (!strengur_gögn) return;
    if (strengur_gögn->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_tegund && 통신끝점들[순번].upplýsingatækni_Í_bið == skrá_hald) loka_Net(순번);
    if (strengur_gögn->tenging_stýring) {
        tcp_arg(strengur_gögn->tenging_stýring, 0); if (strengur_gögn->수신창구) tcp_accept(strengur_gögn->tenging_stýring, 0); else { tcp_recv(strengur_gögn->tenging_stýring, 0); tcp_err(strengur_gögn->tenging_stýring, 0); }
        if (tcp_close(strengur_gögn->tenging_stýring) != ERR_OK) tcp_abort(strengur_gögn->tenging_stýring);
    }
    if (strengur_gögn->전문제어) udp_remove(strengur_gögn->전문제어); strengur_gögn->TYPE_tegund = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&tenging_tæki);
    for (unsigned fjárhagsáætlun = 0; !유선사용 && fjárhagsáætlun < 4096 && (vél_skrá(보조장치 + 0x54) & 1); fjárhagsáætlun++) {
        unsigned stafkóði = vél_skrá(보조장치 + 0x40) & 255;
        if (stafkóði == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *gögn_staða = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (gögn_staða) { 받은전문수++; RECEIVED_bæti_COUNT += 수신사용량; pbuf_take(gögn_staða, 수신자료, 수신사용량); if (tenging_tæki.input(gögn_staða, &tenging_tæki) != ERR_OK) { 버린전문수++; pbuf_free(gögn_staða); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (stafkóði == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (stafkóði != 220 && stafkóði != 221) 수신오류 = 1; stafkóði = stafkóði == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = stafkóði; else 수신오류 = 1;
        }
    }
    netif_poll(&tenging_tæki); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned fjárhagsáætlun = 0; fjárhagsáætlun < 4096 && 송신개수 && (vél_skrá(보조장치 + 0x54) & 0x20); fjárhagsáætlun++) {
        vél_skrá(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Stillingar·조회는 lwIP의 raun_gögn 인터페이스와 ljúka_P 표를 사용한다. */
uint32_t 망상태읽기(unsigned færsla_VALUE, unsigned INDEX) {
    if(færsla_VALUE==20)return 유선사용;
    if(færsla_VALUE==21)return 준비됨&&netif_is_link_up(&tenging_tæki);
    if(færsla_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&færsla_VALUE>=4&&færsla_VALUE<=8)return 유선망집계(færsla_VALUE-4);
    if (færsla_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&tenging_tæki)));
    if (færsla_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&tenging_tæki)));
    if (færsla_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&tenging_tæki)));
    if (færsla_VALUE == 3) return netif_is_up(&tenging_tæki) != 0;
    if (færsla_VALUE == 4) return 받은전문수;
    if (færsla_VALUE == 5) return 보낸전문수;
    if (færsla_VALUE == 6) return RECEIVED_bæti_COUNT;
    if (færsla_VALUE == 7) return 보낸바이트수;
    if (færsla_VALUE == 8) return 버린전문수;
    if (færsla_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *ljúka_P = &통신끝점들[INDEX];
    if (færsla_VALUE == 10) return ljúka_P->TYPE_tegund;
    if (!ljúka_P->TYPE_tegund) return 0;
    if (færsla_VALUE == 11) return Net_tengisnúmer(INDEX);
    if (færsla_VALUE == 12) return ljúka_P->jafningi_slóð;
    if (færsla_VALUE == 13) return ljúka_P->jafningi_endastöð_númer;
    if (færsla_VALUE == 14) return ljúka_P->수신창구 ? 1 : ljúka_P->skrá_ljúka ? 3 : ljúka_P->Villa ? 4 : ljúka_P->연결됨 ? 2 : 0;
    if (færsla_VALUE == 15) return ljúka_P->færsla_COUNT;
    if (færsla_VALUE == 16) {
        const ip_addr_t *slóð = ljúka_P->TYPE_tegund == 1 && ljúka_P->tenging_stýring ? &ljúka_P->tenging_stýring->local_ip :
            ljúka_P->TYPE_tegund == 2 && ljúka_P->전문제어 ? &ljúka_P->전문제어->local_ip : 0;
        return slóð ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(slóð))) : 0;
    }
    return 0;
}

int grunnstilla_Net(unsigned Aðgerð, uint32_t slóð, uint32_t sía_VALUE_3fef50ae, uint32_t gátt_VALUE_cfee51e8) {
    if (!준비됨) return -100;
    if (Aðgerð == 1) { netif_set_up(&tenging_tæki); return 0; }
    if (Aðgerð == 2) { netif_set_down(&tenging_tæki); return 0; }
    if (Aðgerð != 0) return -22;
    /* 유니캐스트 IPv4, 연속 sía_VALUE_3fef50ae, 같은 망의 선택적 sjálfgildi gátt_VALUE_cfee51e8. */
    uint32_t 뒤집은가림 = ~sía_VALUE_3fef50ae;
    if (!sía_VALUE_3fef50ae || (뒤집은가림 & (뒤집은가림 + 1)) || !slóð || (slóð >> 24) == 127 ||
        (slóð >> 24) == 0 || (slóð >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(slóð & 뒤집은가림) || (slóð & 뒤집은가림) == 뒤집은가림)) ||
        (gátt_VALUE_cfee51e8 && ((gátt_VALUE_cfee51e8 & sía_VALUE_3fef50ae) != (slóð & sía_VALUE_3fef50ae) || gátt_VALUE_cfee51e8 == slóð || (gátt_VALUE_cfee51e8 >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gátt_VALUE_cfee51e8 & 뒤집은가림) || (gátt_VALUE_cfee51e8 & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 slóð 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_tegund &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].tenging_stýring && ip_addr_isany(&통신끝점들[INDEX].tenging_stýring->local_ip))) return -16;
    if(유선사용)dhcp_stop(&tenging_tæki);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(slóð)); ip4_addr_set_u32(&새가림, lwip_htonl(sía_VALUE_3fef50ae)); ip4_addr_set_u32(&새관문, lwip_htonl(gátt_VALUE_cfee51e8));
    netif_set_addr(&tenging_tæki, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *Viðföng, struct raw_pcb *ljúka_P, struct pbuf *gögn, const ip_addr_t *slóð) {
    (void)Viðföng; (void)ljúka_P;
    unsigned char 머리[20], svara[16];
    if (응답상태 != -11 || gögn->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(slóð))) != 시험주소 || pbuf_copy_partial(gögn, 머리, 20, 0) != 20) return 0;
    unsigned Haus_breyta_stærð = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Haus_breyta_stærð < 20 || gögn->tot_len < Haus_breyta_stærð + 16 ||
        pbuf_copy_partial(gögn, svara, 16, Haus_breyta_stærð) != 16 || svara[0] || svara[1] ||
        (((unsigned)svara[4] << 8) | svara[5]) != 시험식별자 ||
        (((unsigned)svara[6] << 8) | svara[7]) != 시험순서 ||
        svara[8] != 'J' || svara[9] != 'K' || svara[10] != 'O' || svara[11] != 'S' ||
        (((uint32_t)svara[12] << 24) | ((uint32_t)svara[13] << 16) | ((uint32_t)svara[14] << 8) | svara[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(gögn, Haus_breyta_stærð)) return 0;
    if (inet_chksum_pbuf(gögn)) { pbuf_add_header(gögn, Haus_breyta_stærð); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(gögn); return 1;
}
int 응답시험시작(uint32_t slóð, unsigned röð_VALUE) {
    if (!준비됨 || !netif_is_up(&tenging_tæki)) return -100;
    if (!slóð || (slóð >> 28) >= 14 || slóð == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = slóð; 시험순서 = röð_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char gögn[32] = {8,0,0,0};
    gögn[4] = 시험식별자 >> 8; gögn[5] = 시험식별자; gögn[6] = 시험순서 >> 8; gögn[7] = 시험순서;
    gögn[8]='J'; gögn[9]='K'; gögn[10]='O'; gögn[11]='S';
    gögn[12]=시험시각 >> 24; gögn[13]=시험시각 >> 16; gögn[14]=시험시각 >> 8; gögn[15]=시험시각;
    for (unsigned staða_INDEX = 16; staða_INDEX < sizeof(gögn); staða_INDEX++) gögn[staða_INDEX] = staða_INDEX;
    uint16_t sannprófun_prófsumma = inet_chksum(gögn, sizeof(gögn)); memcpy(gögn + 2, &sannprófun_prófsumma, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(gögn), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, gögn, sizeof(gögn)); ip_addr_t endastaður_endastöð; ip_addr_set_ip4_u32(&endastaður_endastöð, lwip_htonl(slóð));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &endastaður_endastöð); pbuf_free(전문);
    if (처리값) 응답상태 = villa_númer(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned færsla_VALUE) {
    통신망살피기();
    return færsla_VALUE == 0 ? 응답상태 : færsla_VALUE == 1 ? (int)응답시간 : færsla_VALUE == 2 ? (int)응답차례 : -22;
}
