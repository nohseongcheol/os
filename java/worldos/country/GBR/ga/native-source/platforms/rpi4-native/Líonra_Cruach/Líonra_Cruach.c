#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Líonra_Cruach.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../cianda_VALUE/cianda_VALUE.h"
#include "sreinge_Líonra.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define meaisín_cláraigh(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif nasc_gléas;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_beart_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_catagóir, 수신창구, teicneolaíocht_faisnéise_Ar_feitheamh, 연결됨, comhad_cuir_deireadh_le, ERREÁID;
    struct tcp_pcb *nasc_rialú;
    struct udp_pcb *전문제어;
    unsigned 맨앞, iontráil_COUNT;
    unsigned char sonraí[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], piara_ADDRESS;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int comhad_hanla) { return comhad_hanla >= 0 && comhad_hanla < 32 && 통신끝점들[comhad_hanla].TYPE_catagóir ? &통신끝점들[comhad_hanla] : 0; }
static int 예약하기(int TYPE_catagóir) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_catagóir) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_catagóir = TYPE_catagóir; 통신끝점들[순번].teicneolaíocht_faisnéise_Ar_feitheamh = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned pointe_cóid) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = pointe_cóid; }
static err_t 출력결과(struct netif *mír_COUNT, struct pbuf *sonraí_suíomh, const ip4_addr_t *ADDRESS) {
    (void)mír_COUNT; (void)ADDRESS;
    if (sonraí_suíomh->tot_len > 1500 || 송신개수 + 2 * sonraí_suíomh->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Ar_aghaidh_OFFSET = sonraí_suíomh; Ar_aghaidh_OFFSET; Ar_aghaidh_OFFSET = Ar_aghaidh_OFFSET->next) for (unsigned 순번 = 0; 순번 < Ar_aghaidh_OFFSET->len; 순번++) {
        unsigned pointe_cóid = ((unsigned char *)Ar_aghaidh_OFFSET->payload)[순번];
        if (pointe_cóid == 192 || pointe_cóid == 219) { 내보내기(219); 내보내기(pointe_cóid == 192 ? 220 : 221); } else 내보내기(pointe_cóid);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += sonraí_suíomh->tot_len; return ERR_OK;
}
static err_t Ullmhaigh_am_rite_teanga_coiteann(struct netif *mír_COUNT) { mír_COUNT->name[0] = 's'; mír_COUNT->name[1] = 'l'; mír_COUNT->mtu = 1500; mír_COUNT->output = 출력결과; return ERR_OK; }
void Ullmhaigh_Líonra(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    meaisín_cláraigh(보조장치 + 4) |= 1; meaisín_cláraigh(보조장치 + 0x60) = 0; meaisín_cláraigh(보조장치 + 0x44) = 0;
    meaisín_cláraigh(보조장치 + 0x48) = 0xc6; meaisín_cláraigh(보조장치 + 0x4c) = 3; meaisín_cláraigh(보조장치 + 0x68) = 270; meaisín_cláraigh(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t seoladh_Idirlín, giotán_masc, geata_ADDRESS;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&seoladh_Idirlín, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&giotán_masc, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&geata_ADDRESS, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&nasc_gléas, &seoladh_Idirlín, &giotán_masc, &geata_ADDRESS, 0, 유선사용?Ullmhaigh_sreinge_Líonra:Ullmhaigh_am_rite_teanga_coiteann, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&nasc_gléas); netif_set_up(&nasc_gléas);if(!유선사용)netif_set_link_up(&nasc_gléas); 준비됨 = 1;
    Ullmhaigh_cianda();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *tarchur_rialú_bac, struct pbuf *sonraí_suíomh, err_t ERREÁID) {
    통신끝점 *teaghrán_sonraí = 부가인수; (void)tarchur_rialú_bac; (void)ERREÁID;
    if (!sonraí_suíomh) { teaghrán_sonraí->comhad_cuir_deireadh_le = 1; return ERR_OK; }
    if (sonraí_suíomh->tot_len > sizeof(teaghrán_sonraí->sonraí) - teaghrán_sonraí->iontráil_COUNT) return ERR_MEM;
    unsigned 현재위치 = (teaghrán_sonraí->맨앞 + teaghrán_sonraí->iontráil_COUNT) % sizeof(teaghrán_sonraí->sonraí);
    for (struct pbuf *Ar_aghaidh_OFFSET = sonraí_suíomh; Ar_aghaidh_OFFSET; Ar_aghaidh_OFFSET = Ar_aghaidh_OFFSET->next) for (unsigned 순번 = 0; 순번 < Ar_aghaidh_OFFSET->len; 순번++) {
        teaghrán_sonraí->sonraí[현재위치] = ((unsigned char *)Ar_aghaidh_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(teaghrán_sonraí->sonraí);
    }
    teaghrán_sonraí->iontráil_COUNT += sonraí_suíomh->tot_len; pbuf_free(sonraí_suíomh); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t ERREÁID) { 통신끝점 *teaghrán_sonraí = 부가인수; teaghrán_sonraí->nasc_rialú = 0; teaghrán_sonraí->ERREÁID = 오류번호(ERREÁID); }
static void 되부름목록(통신끝점 *teaghrán_sonraí) { tcp_arg(teaghrán_sonraí->nasc_rialú, teaghrán_sonraí); tcp_recv(teaghrán_sonraí->nasc_rialú, 수신됨); tcp_err(teaghrán_sonraí->nasc_rialú, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *tarchur_rialú_bac, err_t ERREÁID) {
    통신끝점 *teaghrán_sonraí = 부가인수; (void)tarchur_rialú_bac; if (ERREÁID) teaghrán_sonraí->ERREÁID = 오류번호(ERREÁID); else teaghrán_sonraí->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *tarchur_rialú_bac, err_t ERREÁID) {
    통신끝점 *부모항목 = 부가인수; if (ERREÁID) return ERREÁID;
    int comhad_hanla = 예약하기(1); if (comhad_hanla < 0) return ERR_MEM;
    통신끝점 *teaghrán_sonraí = &통신끝점들[comhad_hanla]; teaghrán_sonraí->nasc_rialú = tarchur_rialú_bac; teaghrán_sonraí->연결됨 = 1; teaghrán_sonraí->teicneolaíocht_faisnéise_Ar_feitheamh = (int)(부모항목 - 통신끝점들);
    teaghrán_sonraí->piara_ADDRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&tarchur_rialú_bac->remote_ip))); teaghrán_sonraí->상대창구번호 = tarchur_rialú_bac->remote_port;
    되부름목록(teaghrán_sonraí); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *tarchur_rialú_bac, struct pbuf *sonraí_suíomh, const ip_addr_t *ADDRESS, u16_t uimhir_phoirt) {
    통신끝점 *teaghrán_sonraí = 부가인수; (void)tarchur_rialú_bac;
    if (teaghrán_sonraí->iontráil_COUNT < 4 && sonraí_suíomh->tot_len <= 512) {
        unsigned suíomh_INDEX = (teaghrán_sonraí->맨앞 + teaghrán_sonraí->iontráil_COUNT) % 4;
        pbuf_copy_partial(sonraí_suíomh, teaghrán_sonraí->sonraí + suíomh_INDEX * 512, sonraí_suíomh->tot_len, 0);
        teaghrán_sonraí->길이목록[suíomh_INDEX] = sonraí_suíomh->tot_len; teaghrán_sonraí->접속번호들[suíomh_INDEX] = uimhir_phoirt;
        teaghrán_sonraí->주소목록[suíomh_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))); teaghrán_sonraí->iontráil_COUNT++;
    }
    pbuf_free(sonraí_suíomh);
}
int 통신끝점만들기(int TYPE_catagóir) {
    if (!준비됨) return -100;
    if (TYPE_catagóir != 1 && TYPE_catagóir != 2) return -93;
    int comhad_hanla = 예약하기(TYPE_catagóir); if (comhad_hanla < 0) return comhad_hanla;
    통신끝점 *teaghrán_sonraí = &통신끝점들[comhad_hanla];
    if (TYPE_catagóir == 1) { teaghrán_sonraí->nasc_rialú = tcp_new(); if (teaghrán_sonraí->nasc_rialú) 되부름목록(teaghrán_sonraí); }
    else { teaghrán_sonraí->전문제어 = udp_new(); if (teaghrán_sonraí->전문제어) udp_recv(teaghrán_sonraí->전문제어, 전문, teaghrán_sonraí); }
    if (!teaghrán_sonraí->nasc_rialú && !teaghrán_sonraí->전문제어) { teaghrán_sonraí->TYPE_catagóir = 0; return -12; } return comhad_hanla;
}
int 망주소묶기(int comhad_hanla, uint32_t ADDRESS, unsigned uimhir_phoirt) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí) return -9;
    if (uimhir_phoirt > 65535 || (ADDRESS && ADDRESS != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&nasc_gléas))) && ADDRESS != 0x7f000001)) return -99;
    ip_addr_t seoladh_Idirlín; ip_addr_set_ip4_u32(&seoladh_Idirlín, lwip_htonl(ADDRESS));
    err_t 보조항목 = teaghrán_sonraí->TYPE_catagóir == 1 ? tcp_bind(teaghrán_sonraí->nasc_rialú, &seoladh_Idirlín, uimhir_phoirt) : udp_bind(teaghrán_sonraí->전문제어, &seoladh_Idirlín, uimhir_phoirt); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int comhad_hanla) { 통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (teaghrán_sonraí && teaghrán_sonraí->nasc_rialú) ip_set_option(teaghrán_sonraí->nasc_rialú, SOF_REUSEADDR); }
int 연결기다리기(int comhad_hanla) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí || teaghrán_sonraí->TYPE_catagóir != 1) return -9;
    if (teaghrán_sonraí->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *tarchur_rialú_bac = tcp_listen_with_backlog_and_err(teaghrán_sonraí->nasc_rialú, 4, &보조항목);
    if (!tarchur_rialú_bac) return 오류번호(보조항목); teaghrán_sonraí->nasc_rialú = tarchur_rialú_bac; teaghrán_sonraí->수신창구 = 1; tcp_arg(tarchur_rialú_bac, teaghrán_sonraí); tcp_accept(tarchur_rialú_bac, 연결받음); return 0;
}
int 망연결하기(int comhad_hanla, uint32_t ADDRESS, unsigned uimhir_phoirt) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí || teaghrán_sonraí->TYPE_catagóir != 1) return -9;
    if (teaghrán_sonraí->ERREÁID) return teaghrán_sonraí->ERREÁID;
    if (teaghrán_sonraí->연결됨) return 0;
    if (teaghrán_sonraí->상대창구번호) return -115;
    if (!uimhir_phoirt || uimhir_phoirt > 65535 || !ADDRESS) return -22;
    ip_addr_t seoladh_Idirlín; ip_addr_set_ip4_u32(&seoladh_Idirlín, lwip_htonl(ADDRESS));
    teaghrán_sonraí->piara_ADDRESS = ADDRESS; teaghrán_sonraí->상대창구번호 = uimhir_phoirt;
    err_t 보조항목 = tcp_connect(teaghrán_sonraí->nasc_rialú, &seoladh_Idirlín, uimhir_phoirt, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int comhad_hanla) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí || !teaghrán_sonraí->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_catagóir == 1 && 통신끝점들[순번].teicneolaíocht_faisnéise_Ar_feitheamh == comhad_hanla) { 통신끝점들[순번].teicneolaíocht_faisnéise_Ar_feitheamh = -1; return 순번; }
    return -11;
}
int 통신읽기(int comhad_hanla, void *sonraí, unsigned mír_COUNT) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí || teaghrán_sonraí->TYPE_catagóir != 1) return -9;
    if (!mír_COUNT) return 0; if (!teaghrán_sonraí->iontráil_COUNT) return teaghrán_sonraí->ERREÁID ? teaghrán_sonraí->ERREÁID : teaghrán_sonraí->comhad_cuir_deireadh_le ? 0 : -11;
    if (mír_COUNT > teaghrán_sonraí->iontráil_COUNT) mír_COUNT = teaghrán_sonraí->iontráil_COUNT;
    for (unsigned 순번 = 0; 순번 < mír_COUNT; 순번++) { ((unsigned char *)sonraí)[순번] = teaghrán_sonraí->sonraí[teaghrán_sonraí->맨앞]; teaghrán_sonraí->맨앞 = (teaghrán_sonraí->맨앞 + 1) % sizeof(teaghrán_sonraí->sonraí); }
    teaghrán_sonraí->iontráil_COUNT -= mír_COUNT; if (teaghrán_sonraí->nasc_rialú) tcp_recved(teaghrán_sonraí->nasc_rialú, mír_COUNT); return mír_COUNT;
}
int 통신쓰기(int comhad_hanla, const void *sonraí, unsigned mír_COUNT) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí || teaghrán_sonraí->TYPE_catagóir != 1) return -9;
    if (teaghrán_sonraí->ERREÁID) return teaghrán_sonraí->ERREÁID; if (!teaghrán_sonraí->nasc_rialú || !teaghrán_sonraí->연결됨) return -107;
    if (!mír_COUNT) return 0; if (mír_COUNT > tcp_sndbuf(teaghrán_sonraí->nasc_rialú)) mír_COUNT = tcp_sndbuf(teaghrán_sonraí->nasc_rialú);
    if (!mír_COUNT) return -11; if (mír_COUNT > 1024) mír_COUNT = 1024;
    err_t 보조항목 = tcp_write(teaghrán_sonraí->nasc_rialú, sonraí, mír_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(teaghrán_sonraí->nasc_rialú); return mír_COUNT;
}
int 전문보내기(int comhad_hanla, const void *sonraí, unsigned mír_COUNT, uint32_t ADDRESS, unsigned uimhir_phoirt) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí || teaghrán_sonraí->TYPE_catagóir != 2) return -9;
    if (mír_COUNT > 512) return -90; if (!uimhir_phoirt || uimhir_phoirt > 65535) return -22;
    struct pbuf *sonraí_suíomh = pbuf_alloc(PBUF_TRANSPORT, mír_COUNT, PBUF_RAM); if (!sonraí_suíomh) return -11;
    pbuf_take(sonraí_suíomh, sonraí, mír_COUNT); ip_addr_t seoladh_Idirlín; ip_addr_set_ip4_u32(&seoladh_Idirlín, lwip_htonl(ADDRESS));
    err_t 보조항목 = udp_sendto(teaghrán_sonraí->전문제어, sonraí_suíomh, &seoladh_Idirlín, uimhir_phoirt); pbuf_free(sonraí_suíomh); return 보조항목 ? 오류번호(보조항목) : (int)mír_COUNT;
}
int 전문받기(int comhad_hanla, void *sonraí, unsigned mír_COUNT) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí || teaghrán_sonraí->TYPE_catagóir != 2) return -9;
    if (!teaghrán_sonraí->iontráil_COUNT) return -11; unsigned 현재위치 = teaghrán_sonraí->맨앞;
    if (mír_COUNT > teaghrán_sonraí->길이목록[현재위치]) mír_COUNT = teaghrán_sonraí->길이목록[현재위치]; memcpy(sonraí, teaghrán_sonraí->sonraí + 현재위치 * 512, mír_COUNT);
    teaghrán_sonraí->상대창구번호 = teaghrán_sonraí->접속번호들[현재위치]; teaghrán_sonraí->piara_ADDRESS = teaghrán_sonraí->주소목록[현재위치]; teaghrán_sonraí->맨앞 = (현재위치 + 1) % 4; teaghrán_sonraí->iontráil_COUNT--; return mír_COUNT;
}
unsigned Líonra_uimhir_phoirt(int comhad_hanla) { 통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); return !teaghrán_sonraí ? 0 : teaghrán_sonraí->nasc_rialú ? teaghrán_sonraí->nasc_rialú->local_port : teaghrán_sonraí->전문제어 ? teaghrán_sonraí->전문제어->local_port : 0; }
unsigned piara_uimhir_phoirt(int comhad_hanla) { 통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); return teaghrán_sonraí ? teaghrán_sonraí->상대창구번호 : 0; }
uint32_t 상대통신주소(int comhad_hanla) { 통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); return teaghrán_sonraí ? teaghrán_sonraí->piara_ADDRESS : 0; }
void dún_Líonra(int comhad_hanla) {
    통신끝점 *teaghrán_sonraí = 얻기(comhad_hanla); if (!teaghrán_sonraí) return;
    if (teaghrán_sonraí->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_catagóir && 통신끝점들[순번].teicneolaíocht_faisnéise_Ar_feitheamh == comhad_hanla) dún_Líonra(순번);
    if (teaghrán_sonraí->nasc_rialú) {
        tcp_arg(teaghrán_sonraí->nasc_rialú, 0); if (teaghrán_sonraí->수신창구) tcp_accept(teaghrán_sonraí->nasc_rialú, 0); else { tcp_recv(teaghrán_sonraí->nasc_rialú, 0); tcp_err(teaghrán_sonraí->nasc_rialú, 0); }
        if (tcp_close(teaghrán_sonraí->nasc_rialú) != ERR_OK) tcp_abort(teaghrán_sonraí->nasc_rialú);
    }
    if (teaghrán_sonraí->전문제어) udp_remove(teaghrán_sonraí->전문제어); teaghrán_sonraí->TYPE_catagóir = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&nasc_gléas);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (meaisín_cláraigh(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned pointe_cóid = meaisín_cláraigh(보조장치 + 0x40) & 255;
        if (pointe_cóid == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *sonraí_suíomh = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (sonraí_suíomh) { 받은전문수++; RECEIVED_beart_COUNT += 수신사용량; pbuf_take(sonraí_suíomh, 수신자료, 수신사용량); if (nasc_gléas.input(sonraí_suíomh, &nasc_gléas) != ERR_OK) { 버린전문수++; pbuf_free(sonraí_suíomh); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (pointe_cóid == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (pointe_cóid != 220 && pointe_cóid != 221) 수신오류 = 1; pointe_cóid = pointe_cóid == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = pointe_cóid; else 수신오류 = 1;
        }
    }
    netif_poll(&nasc_gléas); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (meaisín_cláraigh(보조장치 + 0x54) & 0x20); 처리한도++) {
        meaisín_cláraigh(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Socruithe·조회는 lwIP의 iarbhír_sonraí 인터페이스와 cuir_deireadh_le_pointe 표를 사용한다. */
uint32_t 망상태읽기(unsigned iontráil_VALUE, unsigned INDEX) {
    if(iontráil_VALUE==20)return 유선사용;
    if(iontráil_VALUE==21)return 준비됨&&netif_is_link_up(&nasc_gléas);
    if(iontráil_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&iontráil_VALUE>=4&&iontráil_VALUE<=8)return 유선망집계(iontráil_VALUE-4);
    if (iontráil_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&nasc_gléas)));
    if (iontráil_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&nasc_gléas)));
    if (iontráil_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&nasc_gléas)));
    if (iontráil_VALUE == 3) return netif_is_up(&nasc_gléas) != 0;
    if (iontráil_VALUE == 4) return 받은전문수;
    if (iontráil_VALUE == 5) return 보낸전문수;
    if (iontráil_VALUE == 6) return RECEIVED_beart_COUNT;
    if (iontráil_VALUE == 7) return 보낸바이트수;
    if (iontráil_VALUE == 8) return 버린전문수;
    if (iontráil_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *cuir_deireadh_le_pointe = &통신끝점들[INDEX];
    if (iontráil_VALUE == 10) return cuir_deireadh_le_pointe->TYPE_catagóir;
    if (!cuir_deireadh_le_pointe->TYPE_catagóir) return 0;
    if (iontráil_VALUE == 11) return Líonra_uimhir_phoirt(INDEX);
    if (iontráil_VALUE == 12) return cuir_deireadh_le_pointe->piara_ADDRESS;
    if (iontráil_VALUE == 13) return cuir_deireadh_le_pointe->상대창구번호;
    if (iontráil_VALUE == 14) return cuir_deireadh_le_pointe->수신창구 ? 1 : cuir_deireadh_le_pointe->comhad_cuir_deireadh_le ? 3 : cuir_deireadh_le_pointe->ERREÁID ? 4 : cuir_deireadh_le_pointe->연결됨 ? 2 : 0;
    if (iontráil_VALUE == 15) return cuir_deireadh_le_pointe->iontráil_COUNT;
    if (iontráil_VALUE == 16) {
        const ip_addr_t *ADDRESS = cuir_deireadh_le_pointe->TYPE_catagóir == 1 && cuir_deireadh_le_pointe->nasc_rialú ? &cuir_deireadh_le_pointe->nasc_rialú->local_ip :
            cuir_deireadh_le_pointe->TYPE_catagóir == 2 && cuir_deireadh_le_pointe->전문제어 ? &cuir_deireadh_le_pointe->전문제어->local_ip : 0;
        return ADDRESS ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) : 0;
    }
    return 0;
}

int cumraigh_Líonra(unsigned Gníomh, uint32_t ADDRESS, uint32_t masc_VALUE, uint32_t geata_VALUE) {
    if (!준비됨) return -100;
    if (Gníomh == 1) { netif_set_up(&nasc_gléas); return 0; }
    if (Gníomh == 2) { netif_set_down(&nasc_gléas); return 0; }
    if (Gníomh != 0) return -22;
    /* 유니캐스트 IPv4, 연속 masc_VALUE, 같은 망의 선택적 luach_réamhshocraithe geata_VALUE. */
    uint32_t 뒤집은가림 = ~masc_VALUE;
    if (!masc_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !ADDRESS || (ADDRESS >> 24) == 127 ||
        (ADDRESS >> 24) == 0 || (ADDRESS >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADDRESS & 뒤집은가림) || (ADDRESS & 뒤집은가림) == 뒤집은가림)) ||
        (geata_VALUE && ((geata_VALUE & masc_VALUE) != (ADDRESS & masc_VALUE) || geata_VALUE == ADDRESS || (geata_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(geata_VALUE & 뒤집은가림) || (geata_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADDRESS 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_catagóir &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].nasc_rialú && ip_addr_isany(&통신끝점들[INDEX].nasc_rialú->local_ip))) return -16;
    if(유선사용)dhcp_stop(&nasc_gléas);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADDRESS)); ip4_addr_set_u32(&새가림, lwip_htonl(masc_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(geata_VALUE));
    netif_set_addr(&nasc_gléas, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *Argóintí, struct raw_pcb *cuir_deireadh_le_pointe, struct pbuf *sonraí, const ip_addr_t *ADDRESS) {
    (void)Argóintí; (void)cuir_deireadh_le_pointe;
    unsigned char 머리[20], freagair[16];
    if (응답상태 != -11 || sonraí->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) != 시험주소 || pbuf_copy_partial(sonraí, 머리, 20, 0) != 20) return 0;
    unsigned Ceanntásc_socraigh_méid = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Ceanntásc_socraigh_méid < 20 || sonraí->tot_len < Ceanntásc_socraigh_méid + 16 ||
        pbuf_copy_partial(sonraí, freagair, 16, Ceanntásc_socraigh_méid) != 16 || freagair[0] || freagair[1] ||
        (((unsigned)freagair[4] << 8) | freagair[5]) != 시험식별자 ||
        (((unsigned)freagair[6] << 8) | freagair[7]) != 시험순서 ||
        freagair[8] != 'J' || freagair[9] != 'K' || freagair[10] != 'O' || freagair[11] != 'S' ||
        (((uint32_t)freagair[12] << 24) | ((uint32_t)freagair[13] << 16) | ((uint32_t)freagair[14] << 8) | freagair[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(sonraí, Ceanntásc_socraigh_méid)) return 0;
    if (inet_chksum_pbuf(sonraí)) { pbuf_add_header(sonraí, Ceanntásc_socraigh_méid); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(sonraí); return 1;
}
int 응답시험시작(uint32_t ADDRESS, unsigned ord_VALUE) {
    if (!준비됨 || !netif_is_up(&nasc_gléas)) return -100;
    if (!ADDRESS || (ADDRESS >> 28) >= 14 || ADDRESS == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ADDRESS; 시험순서 = ord_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char sonraí[32] = {8,0,0,0};
    sonraí[4] = 시험식별자 >> 8; sonraí[5] = 시험식별자; sonraí[6] = 시험순서 >> 8; sonraí[7] = 시험순서;
    sonraí[8]='J'; sonraí[9]='K'; sonraí[10]='O'; sonraí[11]='S';
    sonraí[12]=시험시각 >> 24; sonraí[13]=시험시각 >> 16; sonraí[14]=시험시각 >> 8; sonraí[15]=시험시각;
    for (unsigned suíomh_INDEX = 16; suíomh_INDEX < sizeof(sonraí); suíomh_INDEX++) sonraí[suíomh_INDEX] = suíomh_INDEX;
    uint16_t fíorú_suim_seiceála = inet_chksum(sonraí, sizeof(sonraí)); memcpy(sonraí + 2, &fíorú_suim_seiceála, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(sonraí), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, sonraí, sizeof(sonraí)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ADDRESS));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned iontráil_VALUE) {
    통신망살피기();
    return iontráil_VALUE == 0 ? 응답상태 : iontráil_VALUE == 1 ? (int)응답시간 : iontráil_VALUE == 2 ? (int)응답차례 : -22;
}
