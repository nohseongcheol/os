#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Alásopọ̀_kójọ.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../Ìjìnnà_iye/Ìjìnnà_iye.h"
#include "aláfiwáyàsopọ̀_Alásopọ̀.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define maṣíìnì_forúkọsílẹ̀(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif Ìsomọ́_ohun_èlò;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int irú_ìsọ̀rí, 수신창구, 대기중, 연결됨, fáìlì_parí, àṣìṣe;
    struct tcp_pcb *Ìsomọ́_ìdarí;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char détà[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], ọ̀gbà_àdírẹ́ẹ̀sì;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int fáìlì_èkù) { return fáìlì_èkù >= 0 && fáìlì_èkù < 32 && 통신끝점들[fáìlì_èkù].irú_ìsọ̀rí ? &통신끝점들[fáìlì_èkù] : 0; }
static int 예약하기(int irú_ìsọ̀rí) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].irú_ìsọ̀rí) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].irú_ìsọ̀rí = irú_ìsọ̀rí; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kóòdù_ẹyọ_ọ̀rọ̀) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kóòdù_ẹyọ_ọ̀rọ̀; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *àdírẹ́ẹ̀sì) {
    (void)개수; (void)àdírẹ́ẹ̀sì;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned kóòdù_ẹyọ_ọ̀rọ̀ = ((unsigned char *)다음위치->payload)[순번];
        if (kóòdù_ẹyọ_ọ̀rọ̀ == 192 || kóòdù_ẹyọ_ọ̀rọ̀ == 219) { 내보내기(219); 내보내기(kóòdù_ẹyọ_ọ̀rọ̀ == 192 ? 220 : 221); } else 내보내기(kóòdù_ẹyọ_ọ̀rọ̀);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t gbaradì_àkókò_iṣẹ́_èdè_tówọ́pọ̀(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void gbaradì_Alásopọ̀(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    maṣíìnì_forúkọsílẹ̀(보조장치 + 4) |= 1; maṣíìnì_forúkọsílẹ̀(보조장치 + 0x60) = 0; maṣíìnì_forúkọsílẹ̀(보조장치 + 0x44) = 0;
    maṣíìnì_forúkọsílẹ̀(보조장치 + 0x48) = 0xc6; maṣíìnì_forúkọsílẹ̀(보조장치 + 0x4c) = 3; maṣíìnì_forúkọsílẹ̀(보조장치 + 0x68) = 270; maṣíìnì_forúkọsílẹ̀(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t àdíréẹ̀sì_íntánẹ́ẹ̀tì, bíìtì_asẹ́_iye, ẹnu_odi_àdírẹ́ẹ̀sì;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&àdíréẹ̀sì_íntánẹ́ẹ̀tì, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bíìtì_asẹ́_iye, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&ẹnu_odi_àdírẹ́ẹ̀sì, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&Ìsomọ́_ohun_èlò, &àdíréẹ̀sì_íntánẹ́ẹ̀tì, &bíìtì_asẹ́_iye, &ẹnu_odi_àdírẹ́ẹ̀sì, 0, 유선사용?gbaradì_aláfiwáyàsopọ̀_Alásopọ̀:gbaradì_àkókò_iṣẹ́_èdè_tówọ́pọ̀, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&Ìsomọ́_ohun_èlò); netif_set_up(&Ìsomọ́_ohun_èlò);if(!유선사용)netif_set_link_up(&Ìsomọ́_ohun_èlò); 준비됨 = 1;
    gbaradì_Ìjìnnà();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *ìfiránṣẹ́_ìdarí_sèdíwọ, struct pbuf *자료위치, err_t àṣìṣe) {
    통신끝점 *fọ́nrán_détà = 부가인수; (void)ìfiránṣẹ́_ìdarí_sèdíwọ; (void)àṣìṣe;
    if (!자료위치) { fọ́nrán_détà->fáìlì_parí = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(fọ́nrán_détà->détà) - fọ́nrán_détà->항목수) return ERR_MEM;
    unsigned 현재위치 = (fọ́nrán_détà->맨앞 + fọ́nrán_détà->항목수) % sizeof(fọ́nrán_détà->détà);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        fọ́nrán_détà->détà[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(fọ́nrán_détà->détà);
    }
    fọ́nrán_détà->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t àṣìṣe) { 통신끝점 *fọ́nrán_détà = 부가인수; fọ́nrán_détà->Ìsomọ́_ìdarí = 0; fọ́nrán_détà->àṣìṣe = 오류번호(àṣìṣe); }
static void 되부름목록(통신끝점 *fọ́nrán_détà) { tcp_arg(fọ́nrán_détà->Ìsomọ́_ìdarí, fọ́nrán_détà); tcp_recv(fọ́nrán_détà->Ìsomọ́_ìdarí, 수신됨); tcp_err(fọ́nrán_détà->Ìsomọ́_ìdarí, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *ìfiránṣẹ́_ìdarí_sèdíwọ, err_t àṣìṣe) {
    통신끝점 *fọ́nrán_détà = 부가인수; (void)ìfiránṣẹ́_ìdarí_sèdíwọ; if (àṣìṣe) fọ́nrán_détà->àṣìṣe = 오류번호(àṣìṣe); else fọ́nrán_détà->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *ìfiránṣẹ́_ìdarí_sèdíwọ, err_t àṣìṣe) {
    통신끝점 *부모항목 = 부가인수; if (àṣìṣe) return àṣìṣe;
    int fáìlì_èkù = 예약하기(1); if (fáìlì_èkù < 0) return ERR_MEM;
    통신끝점 *fọ́nrán_détà = &통신끝점들[fáìlì_èkù]; fọ́nrán_détà->Ìsomọ́_ìdarí = ìfiránṣẹ́_ìdarí_sèdíwọ; fọ́nrán_détà->연결됨 = 1; fọ́nrán_détà->대기중 = (int)(부모항목 - 통신끝점들);
    fọ́nrán_détà->ọ̀gbà_àdírẹ́ẹ̀sì = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&ìfiránṣẹ́_ìdarí_sèdíwọ->remote_ip))); fọ́nrán_détà->상대창구번호 = ìfiránṣẹ́_ìdarí_sèdíwọ->remote_port;
    되부름목록(fọ́nrán_détà); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *ìfiránṣẹ́_ìdarí_sèdíwọ, struct pbuf *자료위치, const ip_addr_t *àdírẹ́ẹ̀sì, u16_t 접속번호) {
    통신끝점 *fọ́nrán_détà = 부가인수; (void)ìfiránṣẹ́_ìdarí_sèdíwọ;
    if (fọ́nrán_détà->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (fọ́nrán_détà->맨앞 + fọ́nrán_détà->항목수) % 4;
        pbuf_copy_partial(자료위치, fọ́nrán_détà->détà + 자리 * 512, 자료위치->tot_len, 0);
        fọ́nrán_détà->길이목록[자리] = 자료위치->tot_len; fọ́nrán_détà->접속번호들[자리] = 접속번호;
        fọ́nrán_détà->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(àdírẹ́ẹ̀sì))); fọ́nrán_détà->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int irú_ìsọ̀rí) {
    if (!준비됨) return -100;
    if (irú_ìsọ̀rí != 1 && irú_ìsọ̀rí != 2) return -93;
    int fáìlì_èkù = 예약하기(irú_ìsọ̀rí); if (fáìlì_èkù < 0) return fáìlì_èkù;
    통신끝점 *fọ́nrán_détà = &통신끝점들[fáìlì_èkù];
    if (irú_ìsọ̀rí == 1) { fọ́nrán_détà->Ìsomọ́_ìdarí = tcp_new(); if (fọ́nrán_détà->Ìsomọ́_ìdarí) 되부름목록(fọ́nrán_détà); }
    else { fọ́nrán_détà->전문제어 = udp_new(); if (fọ́nrán_détà->전문제어) udp_recv(fọ́nrán_détà->전문제어, 전문, fọ́nrán_détà); }
    if (!fọ́nrán_détà->Ìsomọ́_ìdarí && !fọ́nrán_détà->전문제어) { fọ́nrán_détà->irú_ìsọ̀rí = 0; return -12; } return fáìlì_èkù;
}
int 망주소묶기(int fáìlì_èkù, uint32_t àdírẹ́ẹ̀sì, unsigned 접속번호) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà) return -9;
    if (접속번호 > 65535 || (àdírẹ́ẹ̀sì && àdírẹ́ẹ̀sì != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&Ìsomọ́_ohun_èlò))) && àdírẹ́ẹ̀sì != 0x7f000001)) return -99;
    ip_addr_t àdíréẹ̀sì_íntánẹ́ẹ̀tì; ip_addr_set_ip4_u32(&àdíréẹ̀sì_íntánẹ́ẹ̀tì, lwip_htonl(àdírẹ́ẹ̀sì));
    err_t 보조항목 = fọ́nrán_détà->irú_ìsọ̀rí == 1 ? tcp_bind(fọ́nrán_détà->Ìsomọ́_ìdarí, &àdíréẹ̀sì_íntánẹ́ẹ̀tì, 접속번호) : udp_bind(fọ́nrán_détà->전문제어, &àdíréẹ̀sì_íntánẹ́ẹ̀tì, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int fáìlì_èkù) { 통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (fọ́nrán_détà && fọ́nrán_détà->Ìsomọ́_ìdarí) ip_set_option(fọ́nrán_détà->Ìsomọ́_ìdarí, SOF_REUSEADDR); }
int 연결기다리기(int fáìlì_èkù) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà || fọ́nrán_détà->irú_ìsọ̀rí != 1) return -9;
    if (fọ́nrán_détà->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *ìfiránṣẹ́_ìdarí_sèdíwọ = tcp_listen_with_backlog_and_err(fọ́nrán_détà->Ìsomọ́_ìdarí, 4, &보조항목);
    if (!ìfiránṣẹ́_ìdarí_sèdíwọ) return 오류번호(보조항목); fọ́nrán_détà->Ìsomọ́_ìdarí = ìfiránṣẹ́_ìdarí_sèdíwọ; fọ́nrán_détà->수신창구 = 1; tcp_arg(ìfiránṣẹ́_ìdarí_sèdíwọ, fọ́nrán_détà); tcp_accept(ìfiránṣẹ́_ìdarí_sèdíwọ, 연결받음); return 0;
}
int 망연결하기(int fáìlì_èkù, uint32_t àdírẹ́ẹ̀sì, unsigned 접속번호) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà || fọ́nrán_détà->irú_ìsọ̀rí != 1) return -9;
    if (fọ́nrán_détà->àṣìṣe) return fọ́nrán_détà->àṣìṣe;
    if (fọ́nrán_détà->연결됨) return 0;
    if (fọ́nrán_détà->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !àdírẹ́ẹ̀sì) return -22;
    ip_addr_t àdíréẹ̀sì_íntánẹ́ẹ̀tì; ip_addr_set_ip4_u32(&àdíréẹ̀sì_íntánẹ́ẹ̀tì, lwip_htonl(àdírẹ́ẹ̀sì));
    fọ́nrán_détà->ọ̀gbà_àdírẹ́ẹ̀sì = àdírẹ́ẹ̀sì; fọ́nrán_détà->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(fọ́nrán_détà->Ìsomọ́_ìdarí, &àdíréẹ̀sì_íntánẹ́ẹ̀tì, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int fáìlì_èkù) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà || !fọ́nrán_détà->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].irú_ìsọ̀rí == 1 && 통신끝점들[순번].대기중 == fáìlì_èkù) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int fáìlì_èkù, void *détà, unsigned 개수) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà || fọ́nrán_détà->irú_ìsọ̀rí != 1) return -9;
    if (!개수) return 0; if (!fọ́nrán_détà->항목수) return fọ́nrán_détà->àṣìṣe ? fọ́nrán_détà->àṣìṣe : fọ́nrán_détà->fáìlì_parí ? 0 : -11;
    if (개수 > fọ́nrán_détà->항목수) 개수 = fọ́nrán_détà->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)détà)[순번] = fọ́nrán_détà->détà[fọ́nrán_détà->맨앞]; fọ́nrán_détà->맨앞 = (fọ́nrán_détà->맨앞 + 1) % sizeof(fọ́nrán_détà->détà); }
    fọ́nrán_détà->항목수 -= 개수; if (fọ́nrán_détà->Ìsomọ́_ìdarí) tcp_recved(fọ́nrán_détà->Ìsomọ́_ìdarí, 개수); return 개수;
}
int 통신쓰기(int fáìlì_èkù, const void *détà, unsigned 개수) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà || fọ́nrán_détà->irú_ìsọ̀rí != 1) return -9;
    if (fọ́nrán_détà->àṣìṣe) return fọ́nrán_détà->àṣìṣe; if (!fọ́nrán_détà->Ìsomọ́_ìdarí || !fọ́nrán_détà->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(fọ́nrán_détà->Ìsomọ́_ìdarí)) 개수 = tcp_sndbuf(fọ́nrán_détà->Ìsomọ́_ìdarí);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(fọ́nrán_détà->Ìsomọ́_ìdarí, détà, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(fọ́nrán_détà->Ìsomọ́_ìdarí); return 개수;
}
int 전문보내기(int fáìlì_èkù, const void *détà, unsigned 개수, uint32_t àdírẹ́ẹ̀sì, unsigned 접속번호) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà || fọ́nrán_détà->irú_ìsọ̀rí != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, détà, 개수); ip_addr_t àdíréẹ̀sì_íntánẹ́ẹ̀tì; ip_addr_set_ip4_u32(&àdíréẹ̀sì_íntánẹ́ẹ̀tì, lwip_htonl(àdírẹ́ẹ̀sì));
    err_t 보조항목 = udp_sendto(fọ́nrán_détà->전문제어, 자료위치, &àdíréẹ̀sì_íntánẹ́ẹ̀tì, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int fáìlì_èkù, void *détà, unsigned 개수) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà || fọ́nrán_détà->irú_ìsọ̀rí != 2) return -9;
    if (!fọ́nrán_détà->항목수) return -11; unsigned 현재위치 = fọ́nrán_détà->맨앞;
    if (개수 > fọ́nrán_détà->길이목록[현재위치]) 개수 = fọ́nrán_détà->길이목록[현재위치]; memcpy(détà, fọ́nrán_détà->détà + 현재위치 * 512, 개수);
    fọ́nrán_détà->상대창구번호 = fọ́nrán_détà->접속번호들[현재위치]; fọ́nrán_détà->ọ̀gbà_àdírẹ́ẹ̀sì = fọ́nrán_détà->주소목록[현재위치]; fọ́nrán_détà->맨앞 = (현재위치 + 1) % 4; fọ́nrán_détà->항목수--; return 개수;
}
unsigned 통신접속번호(int fáìlì_èkù) { 통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); return !fọ́nrán_détà ? 0 : fọ́nrán_détà->Ìsomọ́_ìdarí ? fọ́nrán_détà->Ìsomọ́_ìdarí->local_port : fọ́nrán_détà->전문제어 ? fọ́nrán_détà->전문제어->local_port : 0; }
unsigned 상대접속번호(int fáìlì_èkù) { 통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); return fọ́nrán_détà ? fọ́nrán_détà->상대창구번호 : 0; }
uint32_t 상대통신주소(int fáìlì_èkù) { 통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); return fọ́nrán_détà ? fọ́nrán_détà->ọ̀gbà_àdírẹ́ẹ̀sì : 0; }
void pa_dé_Alásopọ̀(int fáìlì_èkù) {
    통신끝점 *fọ́nrán_détà = 얻기(fáìlì_èkù); if (!fọ́nrán_détà) return;
    if (fọ́nrán_détà->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].irú_ìsọ̀rí && 통신끝점들[순번].대기중 == fáìlì_èkù) pa_dé_Alásopọ̀(순번);
    if (fọ́nrán_détà->Ìsomọ́_ìdarí) {
        tcp_arg(fọ́nrán_détà->Ìsomọ́_ìdarí, 0); if (fọ́nrán_détà->수신창구) tcp_accept(fọ́nrán_détà->Ìsomọ́_ìdarí, 0); else { tcp_recv(fọ́nrán_détà->Ìsomọ́_ìdarí, 0); tcp_err(fọ́nrán_détà->Ìsomọ́_ìdarí, 0); }
        if (tcp_close(fọ́nrán_détà->Ìsomọ́_ìdarí) != ERR_OK) tcp_abort(fọ́nrán_détà->Ìsomọ́_ìdarí);
    }
    if (fọ́nrán_détà->전문제어) udp_remove(fọ́nrán_détà->전문제어); fọ́nrán_détà->irú_ìsọ̀rí = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&Ìsomọ́_ohun_èlò);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (maṣíìnì_forúkọsílẹ̀(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned kóòdù_ẹyọ_ọ̀rọ̀ = maṣíìnì_forúkọsílẹ̀(보조장치 + 0x40) & 255;
        if (kóòdù_ẹyọ_ọ̀rọ̀ == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (Ìsomọ́_ohun_èlò.input(자료위치, &Ìsomọ́_ohun_èlò) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (kóòdù_ẹyọ_ọ̀rọ̀ == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kóòdù_ẹyọ_ọ̀rọ̀ != 220 && kóòdù_ẹyọ_ọ̀rọ̀ != 221) 수신오류 = 1; kóòdù_ẹyọ_ọ̀rọ̀ = kóòdù_ẹyọ_ọ̀rọ̀ == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = kóòdù_ẹyọ_ọ̀rọ̀; else 수신오류 = 1;
        }
    }
    netif_poll(&Ìsomọ́_ohun_èlò); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (maṣíìnì_forúkọsílẹ̀(보조장치 + 0x54) & 0x20); 처리한도++) {
        maṣíìnì_forúkọsílẹ̀(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Àwọn_ààtò·조회는 lwIP의 gangan_détà 인터페이스와 parí_kókó 표를 사용한다. */
uint32_t 망상태읽기(unsigned ìgbéwọlé_iye, unsigned wá_atọ̀ka_àkóónú) {
    if(ìgbéwọlé_iye==20)return 유선사용;
    if(ìgbéwọlé_iye==21)return 준비됨&&netif_is_link_up(&Ìsomọ́_ohun_èlò);
    if(ìgbéwọlé_iye==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&ìgbéwọlé_iye>=4&&ìgbéwọlé_iye<=8)return 유선망집계(ìgbéwọlé_iye-4);
    if (ìgbéwọlé_iye == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&Ìsomọ́_ohun_èlò)));
    if (ìgbéwọlé_iye == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&Ìsomọ́_ohun_èlò)));
    if (ìgbéwọlé_iye == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&Ìsomọ́_ohun_èlò)));
    if (ìgbéwọlé_iye == 3) return netif_is_up(&Ìsomọ́_ohun_èlò) != 0;
    if (ìgbéwọlé_iye == 4) return 받은전문수;
    if (ìgbéwọlé_iye == 5) return 보낸전문수;
    if (ìgbéwọlé_iye == 6) return 받은바이트수;
    if (ìgbéwọlé_iye == 7) return 보낸바이트수;
    if (ìgbéwọlé_iye == 8) return 버린전문수;
    if (ìgbéwọlé_iye == 9) return 송신개수;
    if (wá_atọ̀ka_àkóónú >= 32) return 0;
    통신끝점 *parí_kókó = &통신끝점들[wá_atọ̀ka_àkóónú];
    if (ìgbéwọlé_iye == 10) return parí_kókó->irú_ìsọ̀rí;
    if (!parí_kókó->irú_ìsọ̀rí) return 0;
    if (ìgbéwọlé_iye == 11) return 통신접속번호(wá_atọ̀ka_àkóónú);
    if (ìgbéwọlé_iye == 12) return parí_kókó->ọ̀gbà_àdírẹ́ẹ̀sì;
    if (ìgbéwọlé_iye == 13) return parí_kókó->상대창구번호;
    if (ìgbéwọlé_iye == 14) return parí_kókó->수신창구 ? 1 : parí_kókó->fáìlì_parí ? 3 : parí_kókó->àṣìṣe ? 4 : parí_kókó->연결됨 ? 2 : 0;
    if (ìgbéwọlé_iye == 15) return parí_kókó->항목수;
    if (ìgbéwọlé_iye == 16) {
        const ip_addr_t *àdírẹ́ẹ̀sì = parí_kókó->irú_ìsọ̀rí == 1 && parí_kókó->Ìsomọ́_ìdarí ? &parí_kókó->Ìsomọ́_ìdarí->local_ip :
            parí_kókó->irú_ìsọ̀rí == 2 && parí_kókó->전문제어 ? &parí_kókó->전문제어->local_ip : 0;
        return àdírẹ́ẹ̀sì ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(àdírẹ́ẹ̀sì))) : 0;
    }
    return 0;
}

int ṣàtòpọ̀_Alásopọ̀(unsigned ìṣe, uint32_t àdírẹ́ẹ̀sì, uint32_t asẹ́_iye_iye, uint32_t ẹnu_odi_iye) {
    if (!준비됨) return -100;
    if (ìṣe == 1) { netif_set_up(&Ìsomọ́_ohun_èlò); return 0; }
    if (ìṣe == 2) { netif_set_down(&Ìsomọ́_ohun_èlò); return 0; }
    if (ìṣe != 0) return -22;
    /* 유니캐스트 IPv4, 연속 asẹ́_iye_iye, 같은 망의 선택적 àdáwọ̀ ẹnu_odi_iye. */
    uint32_t 뒤집은가림 = ~asẹ́_iye_iye;
    if (!asẹ́_iye_iye || (뒤집은가림 & (뒤집은가림 + 1)) || !àdírẹ́ẹ̀sì || (àdírẹ́ẹ̀sì >> 24) == 127 ||
        (àdírẹ́ẹ̀sì >> 24) == 0 || (àdírẹ́ẹ̀sì >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(àdírẹ́ẹ̀sì & 뒤집은가림) || (àdírẹ́ẹ̀sì & 뒤집은가림) == 뒤집은가림)) ||
        (ẹnu_odi_iye && ((ẹnu_odi_iye & asẹ́_iye_iye) != (àdírẹ́ẹ̀sì & asẹ́_iye_iye) || ẹnu_odi_iye == àdírẹ́ẹ̀sì || (ẹnu_odi_iye >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(ẹnu_odi_iye & 뒤집은가림) || (ẹnu_odi_iye & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 àdírẹ́ẹ̀sì 변경으로 몰래 끊지 않는다. */
    for (unsigned wá_atọ̀ka_àkóónú = 0; wá_atọ̀ka_àkóónú < 32; wá_atọ̀ka_àkóónú++) if (통신끝점들[wá_atọ̀ka_àkóónú].irú_ìsọ̀rí &&
        !(통신끝점들[wá_atọ̀ka_àkóónú].수신창구 && 통신끝점들[wá_atọ̀ka_àkóónú].Ìsomọ́_ìdarí && ip_addr_isany(&통신끝점들[wá_atọ̀ka_àkóónú].Ìsomọ́_ìdarí->local_ip))) return -16;
    if(유선사용)dhcp_stop(&Ìsomọ́_ohun_èlò);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(àdírẹ́ẹ̀sì)); ip4_addr_set_u32(&새가림, lwip_htonl(asẹ́_iye_iye)); ip4_addr_set_u32(&새관문, lwip_htonl(ẹnu_odi_iye));
    netif_set_addr(&Ìsomọ́_ohun_èlò, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *parí_kókó, struct pbuf *détà, const ip_addr_t *àdírẹ́ẹ̀sì) {
    (void)인수; (void)parí_kókó;
    unsigned char 머리[20], Fèsì[16];
    if (응답상태 != -11 || détà->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(àdírẹ́ẹ̀sì))) != 시험주소 || pbuf_copy_partial(détà, 머리, 20, 0) != 20) return 0;
    unsigned àkọlé_ìwọn = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || àkọlé_ìwọn < 20 || détà->tot_len < àkọlé_ìwọn + 16 ||
        pbuf_copy_partial(détà, Fèsì, 16, àkọlé_ìwọn) != 16 || Fèsì[0] || Fèsì[1] ||
        (((unsigned)Fèsì[4] << 8) | Fèsì[5]) != 시험식별자 ||
        (((unsigned)Fèsì[6] << 8) | Fèsì[7]) != 시험순서 ||
        Fèsì[8] != 'J' || Fèsì[9] != 'K' || Fèsì[10] != 'O' || Fèsì[11] != 'S' ||
        (((uint32_t)Fèsì[12] << 24) | ((uint32_t)Fèsì[13] << 16) | ((uint32_t)Fèsì[14] << 8) | Fèsì[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(détà, àkọlé_ìwọn)) return 0;
    if (inet_chksum_pbuf(détà)) { pbuf_add_header(détà, àkọlé_ìwọn); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(détà); return 1;
}
int 응답시험시작(uint32_t àdírẹ́ẹ̀sì, unsigned ìtodátà_iye) {
    if (!준비됨 || !netif_is_up(&Ìsomọ́_ohun_èlò)) return -100;
    if (!àdírẹ́ẹ̀sì || (àdírẹ́ẹ̀sì >> 28) >= 14 || àdírẹ́ẹ̀sì == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = àdírẹ́ẹ̀sì; 시험순서 = ìtodátà_iye & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char détà[32] = {8,0,0,0};
    détà[4] = 시험식별자 >> 8; détà[5] = 시험식별자; détà[6] = 시험순서 >> 8; détà[7] = 시험순서;
    détà[8]='J'; détà[9]='K'; détà[10]='O'; détà[11]='S';
    détà[12]=시험시각 >> 24; détà[13]=시험시각 >> 16; détà[14]=시험시각 >> 8; détà[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(détà); 자리++) détà[자리] = 자리;
    uint16_t 확인합 = inet_chksum(détà, sizeof(détà)); memcpy(détà + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(détà), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, détà, sizeof(détà)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(àdírẹ́ẹ̀sì));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned ìgbéwọlé_iye) {
    통신망살피기();
    return ìgbéwọlé_iye == 0 ? 응답상태 : ìgbéwọlé_iye == 1 ? (int)응답시간 : ìgbéwọlé_iye == 2 ? (int)응답차례 : -22;
}
