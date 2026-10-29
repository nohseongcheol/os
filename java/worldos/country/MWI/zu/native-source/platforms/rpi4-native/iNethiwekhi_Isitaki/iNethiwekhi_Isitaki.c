#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "iNethiwekhi_Isitaki.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../kude_inani/kude_inani.h"
#include "kunezintambo_iNethiwekhi.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define umshini_bhalisa(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif uxhumano_idivayisi;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int thayipha_umunxa, 수신창구, 대기중, 연결됨, ifayela_yekisa, Iphutha;
    struct tcp_pcb *uxhumano_isilawuli;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char imininingwane[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], untanga_ikheli;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int ifayela_isibambo) { return ifayela_isibambo >= 0 && ifayela_isibambo < 32 && 통신끝점들[ifayela_isibambo].thayipha_umunxa ? &통신끝점들[ifayela_isibambo] : 0; }
static int 예약하기(int thayipha_umunxa) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].thayipha_umunxa) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].thayipha_umunxa = thayipha_umunxa; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned ikhodi_yohlamvu) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = ikhodi_yohlamvu; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *ikheli) {
    (void)개수; (void)ikheli;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned ikhodi_yohlamvu = ((unsigned char *)다음위치->payload)[순번];
        if (ikhodi_yohlamvu == 192 || ikhodi_yohlamvu == 219) { 내보내기(219); 내보내기(ikhodi_yohlamvu == 192 ? 220 : 221); } else 내보내기(ikhodi_yohlamvu);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t Hlela_isikhathi_sokusebenza_solimi_esivamile(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Hlela_iNethiwekhi(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    umshini_bhalisa(보조장치 + 4) |= 1; umshini_bhalisa(보조장치 + 0x60) = 0; umshini_bhalisa(보조장치 + 0x44) = 0;
    umshini_bhalisa(보조장치 + 0x48) = 0xc6; umshini_bhalisa(보조장치 + 0x4c) = 3; umshini_bhalisa(보조장치 + 0x68) = 270; umshini_bhalisa(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t ikheli_le_inthanethi, ibhithi_insitha, isango_ikheli;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&ikheli_le_inthanethi, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&ibhithi_insitha, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&isango_ikheli, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&uxhumano_idivayisi, &ikheli_le_inthanethi, &ibhithi_insitha, &isango_ikheli, 0, 유선사용?Hlela_kunezintambo_iNethiwekhi:Hlela_isikhathi_sokusebenza_solimi_esivamile, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&uxhumano_idivayisi); netif_set_up(&uxhumano_idivayisi);if(!유선사용)netif_set_link_up(&uxhumano_idivayisi); 준비됨 = 1;
    Hlela_kude();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *ukuthumela_isilawuli_vimbela, struct pbuf *자료위치, err_t Iphutha) {
    통신끝점 *uchunge_imininingwane = 부가인수; (void)ukuthumela_isilawuli_vimbela; (void)Iphutha;
    if (!자료위치) { uchunge_imininingwane->ifayela_yekisa = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(uchunge_imininingwane->imininingwane) - uchunge_imininingwane->항목수) return ERR_MEM;
    unsigned 현재위치 = (uchunge_imininingwane->맨앞 + uchunge_imininingwane->항목수) % sizeof(uchunge_imininingwane->imininingwane);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        uchunge_imininingwane->imininingwane[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(uchunge_imininingwane->imininingwane);
    }
    uchunge_imininingwane->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Iphutha) { 통신끝점 *uchunge_imininingwane = 부가인수; uchunge_imininingwane->uxhumano_isilawuli = 0; uchunge_imininingwane->Iphutha = 오류번호(Iphutha); }
static void 되부름목록(통신끝점 *uchunge_imininingwane) { tcp_arg(uchunge_imininingwane->uxhumano_isilawuli, uchunge_imininingwane); tcp_recv(uchunge_imininingwane->uxhumano_isilawuli, 수신됨); tcp_err(uchunge_imininingwane->uxhumano_isilawuli, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *ukuthumela_isilawuli_vimbela, err_t Iphutha) {
    통신끝점 *uchunge_imininingwane = 부가인수; (void)ukuthumela_isilawuli_vimbela; if (Iphutha) uchunge_imininingwane->Iphutha = 오류번호(Iphutha); else uchunge_imininingwane->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *ukuthumela_isilawuli_vimbela, err_t Iphutha) {
    통신끝점 *부모항목 = 부가인수; if (Iphutha) return Iphutha;
    int ifayela_isibambo = 예약하기(1); if (ifayela_isibambo < 0) return ERR_MEM;
    통신끝점 *uchunge_imininingwane = &통신끝점들[ifayela_isibambo]; uchunge_imininingwane->uxhumano_isilawuli = ukuthumela_isilawuli_vimbela; uchunge_imininingwane->연결됨 = 1; uchunge_imininingwane->대기중 = (int)(부모항목 - 통신끝점들);
    uchunge_imininingwane->untanga_ikheli = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&ukuthumela_isilawuli_vimbela->remote_ip))); uchunge_imininingwane->상대창구번호 = ukuthumela_isilawuli_vimbela->remote_port;
    되부름목록(uchunge_imininingwane); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *ukuthumela_isilawuli_vimbela, struct pbuf *자료위치, const ip_addr_t *ikheli, u16_t 접속번호) {
    통신끝점 *uchunge_imininingwane = 부가인수; (void)ukuthumela_isilawuli_vimbela;
    if (uchunge_imininingwane->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (uchunge_imininingwane->맨앞 + uchunge_imininingwane->항목수) % 4;
        pbuf_copy_partial(자료위치, uchunge_imininingwane->imininingwane + 자리 * 512, 자료위치->tot_len, 0);
        uchunge_imininingwane->길이목록[자리] = 자료위치->tot_len; uchunge_imininingwane->접속번호들[자리] = 접속번호;
        uchunge_imininingwane->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ikheli))); uchunge_imininingwane->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int thayipha_umunxa) {
    if (!준비됨) return -100;
    if (thayipha_umunxa != 1 && thayipha_umunxa != 2) return -93;
    int ifayela_isibambo = 예약하기(thayipha_umunxa); if (ifayela_isibambo < 0) return ifayela_isibambo;
    통신끝점 *uchunge_imininingwane = &통신끝점들[ifayela_isibambo];
    if (thayipha_umunxa == 1) { uchunge_imininingwane->uxhumano_isilawuli = tcp_new(); if (uchunge_imininingwane->uxhumano_isilawuli) 되부름목록(uchunge_imininingwane); }
    else { uchunge_imininingwane->전문제어 = udp_new(); if (uchunge_imininingwane->전문제어) udp_recv(uchunge_imininingwane->전문제어, 전문, uchunge_imininingwane); }
    if (!uchunge_imininingwane->uxhumano_isilawuli && !uchunge_imininingwane->전문제어) { uchunge_imininingwane->thayipha_umunxa = 0; return -12; } return ifayela_isibambo;
}
int 망주소묶기(int ifayela_isibambo, uint32_t ikheli, unsigned 접속번호) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane) return -9;
    if (접속번호 > 65535 || (ikheli && ikheli != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&uxhumano_idivayisi))) && ikheli != 0x7f000001)) return -99;
    ip_addr_t ikheli_le_inthanethi; ip_addr_set_ip4_u32(&ikheli_le_inthanethi, lwip_htonl(ikheli));
    err_t 보조항목 = uchunge_imininingwane->thayipha_umunxa == 1 ? tcp_bind(uchunge_imininingwane->uxhumano_isilawuli, &ikheli_le_inthanethi, 접속번호) : udp_bind(uchunge_imininingwane->전문제어, &ikheli_le_inthanethi, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int ifayela_isibambo) { 통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (uchunge_imininingwane && uchunge_imininingwane->uxhumano_isilawuli) ip_set_option(uchunge_imininingwane->uxhumano_isilawuli, SOF_REUSEADDR); }
int 연결기다리기(int ifayela_isibambo) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane || uchunge_imininingwane->thayipha_umunxa != 1) return -9;
    if (uchunge_imininingwane->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *ukuthumela_isilawuli_vimbela = tcp_listen_with_backlog_and_err(uchunge_imininingwane->uxhumano_isilawuli, 4, &보조항목);
    if (!ukuthumela_isilawuli_vimbela) return 오류번호(보조항목); uchunge_imininingwane->uxhumano_isilawuli = ukuthumela_isilawuli_vimbela; uchunge_imininingwane->수신창구 = 1; tcp_arg(ukuthumela_isilawuli_vimbela, uchunge_imininingwane); tcp_accept(ukuthumela_isilawuli_vimbela, 연결받음); return 0;
}
int 망연결하기(int ifayela_isibambo, uint32_t ikheli, unsigned 접속번호) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane || uchunge_imininingwane->thayipha_umunxa != 1) return -9;
    if (uchunge_imininingwane->Iphutha) return uchunge_imininingwane->Iphutha;
    if (uchunge_imininingwane->연결됨) return 0;
    if (uchunge_imininingwane->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !ikheli) return -22;
    ip_addr_t ikheli_le_inthanethi; ip_addr_set_ip4_u32(&ikheli_le_inthanethi, lwip_htonl(ikheli));
    uchunge_imininingwane->untanga_ikheli = ikheli; uchunge_imininingwane->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(uchunge_imininingwane->uxhumano_isilawuli, &ikheli_le_inthanethi, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int ifayela_isibambo) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane || !uchunge_imininingwane->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].thayipha_umunxa == 1 && 통신끝점들[순번].대기중 == ifayela_isibambo) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int ifayela_isibambo, void *imininingwane, unsigned 개수) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane || uchunge_imininingwane->thayipha_umunxa != 1) return -9;
    if (!개수) return 0; if (!uchunge_imininingwane->항목수) return uchunge_imininingwane->Iphutha ? uchunge_imininingwane->Iphutha : uchunge_imininingwane->ifayela_yekisa ? 0 : -11;
    if (개수 > uchunge_imininingwane->항목수) 개수 = uchunge_imininingwane->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)imininingwane)[순번] = uchunge_imininingwane->imininingwane[uchunge_imininingwane->맨앞]; uchunge_imininingwane->맨앞 = (uchunge_imininingwane->맨앞 + 1) % sizeof(uchunge_imininingwane->imininingwane); }
    uchunge_imininingwane->항목수 -= 개수; if (uchunge_imininingwane->uxhumano_isilawuli) tcp_recved(uchunge_imininingwane->uxhumano_isilawuli, 개수); return 개수;
}
int 통신쓰기(int ifayela_isibambo, const void *imininingwane, unsigned 개수) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane || uchunge_imininingwane->thayipha_umunxa != 1) return -9;
    if (uchunge_imininingwane->Iphutha) return uchunge_imininingwane->Iphutha; if (!uchunge_imininingwane->uxhumano_isilawuli || !uchunge_imininingwane->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(uchunge_imininingwane->uxhumano_isilawuli)) 개수 = tcp_sndbuf(uchunge_imininingwane->uxhumano_isilawuli);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(uchunge_imininingwane->uxhumano_isilawuli, imininingwane, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(uchunge_imininingwane->uxhumano_isilawuli); return 개수;
}
int 전문보내기(int ifayela_isibambo, const void *imininingwane, unsigned 개수, uint32_t ikheli, unsigned 접속번호) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane || uchunge_imininingwane->thayipha_umunxa != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, imininingwane, 개수); ip_addr_t ikheli_le_inthanethi; ip_addr_set_ip4_u32(&ikheli_le_inthanethi, lwip_htonl(ikheli));
    err_t 보조항목 = udp_sendto(uchunge_imininingwane->전문제어, 자료위치, &ikheli_le_inthanethi, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int ifayela_isibambo, void *imininingwane, unsigned 개수) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane || uchunge_imininingwane->thayipha_umunxa != 2) return -9;
    if (!uchunge_imininingwane->항목수) return -11; unsigned 현재위치 = uchunge_imininingwane->맨앞;
    if (개수 > uchunge_imininingwane->길이목록[현재위치]) 개수 = uchunge_imininingwane->길이목록[현재위치]; memcpy(imininingwane, uchunge_imininingwane->imininingwane + 현재위치 * 512, 개수);
    uchunge_imininingwane->상대창구번호 = uchunge_imininingwane->접속번호들[현재위치]; uchunge_imininingwane->untanga_ikheli = uchunge_imininingwane->주소목록[현재위치]; uchunge_imininingwane->맨앞 = (현재위치 + 1) % 4; uchunge_imininingwane->항목수--; return 개수;
}
unsigned 통신접속번호(int ifayela_isibambo) { 통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); return !uchunge_imininingwane ? 0 : uchunge_imininingwane->uxhumano_isilawuli ? uchunge_imininingwane->uxhumano_isilawuli->local_port : uchunge_imininingwane->전문제어 ? uchunge_imininingwane->전문제어->local_port : 0; }
unsigned 상대접속번호(int ifayela_isibambo) { 통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); return uchunge_imininingwane ? uchunge_imininingwane->상대창구번호 : 0; }
uint32_t 상대통신주소(int ifayela_isibambo) { 통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); return uchunge_imininingwane ? uchunge_imininingwane->untanga_ikheli : 0; }
void vala_iNethiwekhi(int ifayela_isibambo) {
    통신끝점 *uchunge_imininingwane = 얻기(ifayela_isibambo); if (!uchunge_imininingwane) return;
    if (uchunge_imininingwane->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].thayipha_umunxa && 통신끝점들[순번].대기중 == ifayela_isibambo) vala_iNethiwekhi(순번);
    if (uchunge_imininingwane->uxhumano_isilawuli) {
        tcp_arg(uchunge_imininingwane->uxhumano_isilawuli, 0); if (uchunge_imininingwane->수신창구) tcp_accept(uchunge_imininingwane->uxhumano_isilawuli, 0); else { tcp_recv(uchunge_imininingwane->uxhumano_isilawuli, 0); tcp_err(uchunge_imininingwane->uxhumano_isilawuli, 0); }
        if (tcp_close(uchunge_imininingwane->uxhumano_isilawuli) != ERR_OK) tcp_abort(uchunge_imininingwane->uxhumano_isilawuli);
    }
    if (uchunge_imininingwane->전문제어) udp_remove(uchunge_imininingwane->전문제어); uchunge_imininingwane->thayipha_umunxa = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&uxhumano_idivayisi);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (umshini_bhalisa(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned ikhodi_yohlamvu = umshini_bhalisa(보조장치 + 0x40) & 255;
        if (ikhodi_yohlamvu == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (uxhumano_idivayisi.input(자료위치, &uxhumano_idivayisi) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (ikhodi_yohlamvu == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (ikhodi_yohlamvu != 220 && ikhodi_yohlamvu != 221) 수신오류 = 1; ikhodi_yohlamvu = ikhodi_yohlamvu == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = ikhodi_yohlamvu; else 수신오류 = 1;
        }
    }
    netif_poll(&uxhumano_idivayisi); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (umshini_bhalisa(보조장치 + 0x54) & 0x20); 처리한도++) {
        umshini_bhalisa(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Izinhlelo·조회는 lwIP의 ulwazi_ngokwenzekile_imininingwane 인터페이스와 yekisa_iphoyinti 표를 사용한다. */
uint32_t 망상태읽기(unsigned okufakwayo_inani, unsigned thola_inkomba) {
    if(okufakwayo_inani==20)return 유선사용;
    if(okufakwayo_inani==21)return 준비됨&&netif_is_link_up(&uxhumano_idivayisi);
    if(okufakwayo_inani==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&okufakwayo_inani>=4&&okufakwayo_inani<=8)return 유선망집계(okufakwayo_inani-4);
    if (okufakwayo_inani == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&uxhumano_idivayisi)));
    if (okufakwayo_inani == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&uxhumano_idivayisi)));
    if (okufakwayo_inani == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&uxhumano_idivayisi)));
    if (okufakwayo_inani == 3) return netif_is_up(&uxhumano_idivayisi) != 0;
    if (okufakwayo_inani == 4) return 받은전문수;
    if (okufakwayo_inani == 5) return 보낸전문수;
    if (okufakwayo_inani == 6) return 받은바이트수;
    if (okufakwayo_inani == 7) return 보낸바이트수;
    if (okufakwayo_inani == 8) return 버린전문수;
    if (okufakwayo_inani == 9) return 송신개수;
    if (thola_inkomba >= 32) return 0;
    통신끝점 *yekisa_iphoyinti = &통신끝점들[thola_inkomba];
    if (okufakwayo_inani == 10) return yekisa_iphoyinti->thayipha_umunxa;
    if (!yekisa_iphoyinti->thayipha_umunxa) return 0;
    if (okufakwayo_inani == 11) return 통신접속번호(thola_inkomba);
    if (okufakwayo_inani == 12) return yekisa_iphoyinti->untanga_ikheli;
    if (okufakwayo_inani == 13) return yekisa_iphoyinti->상대창구번호;
    if (okufakwayo_inani == 14) return yekisa_iphoyinti->수신창구 ? 1 : yekisa_iphoyinti->ifayela_yekisa ? 3 : yekisa_iphoyinti->Iphutha ? 4 : yekisa_iphoyinti->연결됨 ? 2 : 0;
    if (okufakwayo_inani == 15) return yekisa_iphoyinti->항목수;
    if (okufakwayo_inani == 16) {
        const ip_addr_t *ikheli = yekisa_iphoyinti->thayipha_umunxa == 1 && yekisa_iphoyinti->uxhumano_isilawuli ? &yekisa_iphoyinti->uxhumano_isilawuli->local_ip :
            yekisa_iphoyinti->thayipha_umunxa == 2 && yekisa_iphoyinti->전문제어 ? &yekisa_iphoyinti->전문제어->local_ip : 0;
        return ikheli ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ikheli))) : 0;
    }
    return 0;
}

int misa_iNethiwekhi(unsigned Isenzo, uint32_t ikheli, uint32_t insitha_inani, uint32_t isango_inani) {
    if (!준비됨) return -100;
    if (Isenzo == 1) { netif_set_up(&uxhumano_idivayisi); return 0; }
    if (Isenzo == 2) { netif_set_down(&uxhumano_idivayisi); return 0; }
    if (Isenzo != 0) return -22;
    /* 유니캐스트 IPv4, 연속 insitha_inani, 같은 망의 선택적 inani_elimisiwe isango_inani. */
    uint32_t 뒤집은가림 = ~insitha_inani;
    if (!insitha_inani || (뒤집은가림 & (뒤집은가림 + 1)) || !ikheli || (ikheli >> 24) == 127 ||
        (ikheli >> 24) == 0 || (ikheli >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ikheli & 뒤집은가림) || (ikheli & 뒤집은가림) == 뒤집은가림)) ||
        (isango_inani && ((isango_inani & insitha_inani) != (ikheli & insitha_inani) || isango_inani == ikheli || (isango_inani >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(isango_inani & 뒤집은가림) || (isango_inani & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ikheli 변경으로 몰래 끊지 않는다. */
    for (unsigned thola_inkomba = 0; thola_inkomba < 32; thola_inkomba++) if (통신끝점들[thola_inkomba].thayipha_umunxa &&
        !(통신끝점들[thola_inkomba].수신창구 && 통신끝점들[thola_inkomba].uxhumano_isilawuli && ip_addr_isany(&통신끝점들[thola_inkomba].uxhumano_isilawuli->local_ip))) return -16;
    if(유선사용)dhcp_stop(&uxhumano_idivayisi);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ikheli)); ip4_addr_set_u32(&새가림, lwip_htonl(insitha_inani)); ip4_addr_set_u32(&새관문, lwip_htonl(isango_inani));
    netif_set_addr(&uxhumano_idivayisi, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *yekisa_iphoyinti, struct pbuf *imininingwane, const ip_addr_t *ikheli) {
    (void)인수; (void)yekisa_iphoyinti;
    unsigned char 머리[20], phendula[16];
    if (응답상태 != -11 || imininingwane->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ikheli))) != 시험주소 || pbuf_copy_partial(imininingwane, 머리, 20, 0) != 20) return 0;
    unsigned Unhlokweni_linganisa = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Unhlokweni_linganisa < 20 || imininingwane->tot_len < Unhlokweni_linganisa + 16 ||
        pbuf_copy_partial(imininingwane, phendula, 16, Unhlokweni_linganisa) != 16 || phendula[0] || phendula[1] ||
        (((unsigned)phendula[4] << 8) | phendula[5]) != 시험식별자 ||
        (((unsigned)phendula[6] << 8) | phendula[7]) != 시험순서 ||
        phendula[8] != 'J' || phendula[9] != 'K' || phendula[10] != 'O' || phendula[11] != 'S' ||
        (((uint32_t)phendula[12] << 24) | ((uint32_t)phendula[13] << 16) | ((uint32_t)phendula[14] << 8) | phendula[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(imininingwane, Unhlokweni_linganisa)) return 0;
    if (inet_chksum_pbuf(imininingwane)) { pbuf_add_header(imininingwane, Unhlokweni_linganisa); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(imininingwane); return 1;
}
int 응답시험시작(uint32_t ikheli, unsigned ukuhleleka_inani) {
    if (!준비됨 || !netif_is_up(&uxhumano_idivayisi)) return -100;
    if (!ikheli || (ikheli >> 28) >= 14 || ikheli == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ikheli; 시험순서 = ukuhleleka_inani & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char imininingwane[32] = {8,0,0,0};
    imininingwane[4] = 시험식별자 >> 8; imininingwane[5] = 시험식별자; imininingwane[6] = 시험순서 >> 8; imininingwane[7] = 시험순서;
    imininingwane[8]='J'; imininingwane[9]='K'; imininingwane[10]='O'; imininingwane[11]='S';
    imininingwane[12]=시험시각 >> 24; imininingwane[13]=시험시각 >> 16; imininingwane[14]=시험시각 >> 8; imininingwane[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(imininingwane); 자리++) imininingwane[자리] = 자리;
    uint16_t 확인합 = inet_chksum(imininingwane, sizeof(imininingwane)); memcpy(imininingwane + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(imininingwane), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, imininingwane, sizeof(imininingwane)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ikheli));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned okufakwayo_inani) {
    통신망살피기();
    return okufakwayo_inani == 0 ? 응답상태 : okufakwayo_inani == 1 ? (int)응답시간 : okufakwayo_inani == 2 ? (int)응답차례 : -22;
}
