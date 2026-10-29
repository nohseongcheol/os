#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "mbaal_Tegalo.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../lu_soree_xëyma/lu_soree_xëyma.h"
#include "tënku_mbaal.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define masin_bindu(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif jokkalóo_toftal;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int xeet_ngiir, 수신창구, 대기중, 연결됨, bara_denc_jeexal, njumte;
    struct tcp_pcb *jokkalóo_Saytu_doxinu_ordinateur;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char mbir[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], Nàttangoo_dëkkuwaay;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int bara_denc_yombal) { return bara_denc_yombal >= 0 && bara_denc_yombal < 32 && 통신끝점들[bara_denc_yombal].xeet_ngiir ? &통신끝점들[bara_denc_yombal] : 0; }
static int 예약하기(int xeet_ngiir) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].xeet_ngiir) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].xeet_ngiir = xeet_ngiir; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kotu_araf) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kotu_araf; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *dëkkuwaay) {
    (void)개수; (void)dëkkuwaay;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned kotu_araf = ((unsigned char *)다음위치->payload)[순번];
        if (kotu_araf == 192 || kotu_araf == 219) { 내보내기(219); 내보내기(kotu_araf == 192 ? 220 : 221); } else 내보내기(kotu_araf);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t jël_matuwaay_common_language_runtime(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void jël_matuwaay_mbaal(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    masin_bindu(보조장치 + 4) |= 1; masin_bindu(보조장치 + 0x60) = 0; masin_bindu(보조장치 + 0x44) = 0;
    masin_bindu(보조장치 + 0x48) = 0xc6; masin_bindu(보조장치 + 0x4c) = 3; masin_bindu(보조장치 + 0x68) = 270; masin_bindu(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t dëkkuwaayu_Internet, bit_muuraay, bunt_dëkkuwaay;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&dëkkuwaayu_Internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_muuraay, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&bunt_dëkkuwaay, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&jokkalóo_toftal, &dëkkuwaayu_Internet, &bit_muuraay, &bunt_dëkkuwaay, 0, 유선사용?jël_matuwaay_tënku_mbaal:jël_matuwaay_common_language_runtime, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&jokkalóo_toftal); netif_set_up(&jokkalóo_toftal);if(!유선사용)netif_set_link_up(&jokkalóo_toftal); 준비됨 = 1;
    jël_matuwaay_lu_soree();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu, struct pbuf *자료위치, err_t njumte) {
    통신끝점 *araf_yu_bennoo_mbir = 부가인수; (void)jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu; (void)njumte;
    if (!자료위치) { araf_yu_bennoo_mbir->bara_denc_jeexal = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(araf_yu_bennoo_mbir->mbir) - araf_yu_bennoo_mbir->항목수) return ERR_MEM;
    unsigned 현재위치 = (araf_yu_bennoo_mbir->맨앞 + araf_yu_bennoo_mbir->항목수) % sizeof(araf_yu_bennoo_mbir->mbir);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        araf_yu_bennoo_mbir->mbir[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(araf_yu_bennoo_mbir->mbir);
    }
    araf_yu_bennoo_mbir->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t njumte) { 통신끝점 *araf_yu_bennoo_mbir = 부가인수; araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur = 0; araf_yu_bennoo_mbir->njumte = 오류번호(njumte); }
static void 되부름목록(통신끝점 *araf_yu_bennoo_mbir) { tcp_arg(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, araf_yu_bennoo_mbir); tcp_recv(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, 수신됨); tcp_err(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu, err_t njumte) {
    통신끝점 *araf_yu_bennoo_mbir = 부가인수; (void)jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu; if (njumte) araf_yu_bennoo_mbir->njumte = 오류번호(njumte); else araf_yu_bennoo_mbir->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu, err_t njumte) {
    통신끝점 *부모항목 = 부가인수; if (njumte) return njumte;
    int bara_denc_yombal = 예약하기(1); if (bara_denc_yombal < 0) return ERR_MEM;
    통신끝점 *araf_yu_bennoo_mbir = &통신끝점들[bara_denc_yombal]; araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur = jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu; araf_yu_bennoo_mbir->연결됨 = 1; araf_yu_bennoo_mbir->대기중 = (int)(부모항목 - 통신끝점들);
    araf_yu_bennoo_mbir->Nàttangoo_dëkkuwaay = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu->remote_ip))); araf_yu_bennoo_mbir->상대창구번호 = jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu->remote_port;
    되부름목록(araf_yu_bennoo_mbir); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu, struct pbuf *자료위치, const ip_addr_t *dëkkuwaay, u16_t 접속번호) {
    통신끝점 *araf_yu_bennoo_mbir = 부가인수; (void)jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu;
    if (araf_yu_bennoo_mbir->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (araf_yu_bennoo_mbir->맨앞 + araf_yu_bennoo_mbir->항목수) % 4;
        pbuf_copy_partial(자료위치, araf_yu_bennoo_mbir->mbir + 자리 * 512, 자료위치->tot_len, 0);
        araf_yu_bennoo_mbir->길이목록[자리] = 자료위치->tot_len; araf_yu_bennoo_mbir->접속번호들[자리] = 접속번호;
        araf_yu_bennoo_mbir->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(dëkkuwaay))); araf_yu_bennoo_mbir->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int xeet_ngiir) {
    if (!준비됨) return -100;
    if (xeet_ngiir != 1 && xeet_ngiir != 2) return -93;
    int bara_denc_yombal = 예약하기(xeet_ngiir); if (bara_denc_yombal < 0) return bara_denc_yombal;
    통신끝점 *araf_yu_bennoo_mbir = &통신끝점들[bara_denc_yombal];
    if (xeet_ngiir == 1) { araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur = tcp_new(); if (araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur) 되부름목록(araf_yu_bennoo_mbir); }
    else { araf_yu_bennoo_mbir->전문제어 = udp_new(); if (araf_yu_bennoo_mbir->전문제어) udp_recv(araf_yu_bennoo_mbir->전문제어, 전문, araf_yu_bennoo_mbir); }
    if (!araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur && !araf_yu_bennoo_mbir->전문제어) { araf_yu_bennoo_mbir->xeet_ngiir = 0; return -12; } return bara_denc_yombal;
}
int 망주소묶기(int bara_denc_yombal, uint32_t dëkkuwaay, unsigned 접속번호) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir) return -9;
    if (접속번호 > 65535 || (dëkkuwaay && dëkkuwaay != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&jokkalóo_toftal))) && dëkkuwaay != 0x7f000001)) return -99;
    ip_addr_t dëkkuwaayu_Internet; ip_addr_set_ip4_u32(&dëkkuwaayu_Internet, lwip_htonl(dëkkuwaay));
    err_t 보조항목 = araf_yu_bennoo_mbir->xeet_ngiir == 1 ? tcp_bind(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, &dëkkuwaayu_Internet, 접속번호) : udp_bind(araf_yu_bennoo_mbir->전문제어, &dëkkuwaayu_Internet, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int bara_denc_yombal) { 통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (araf_yu_bennoo_mbir && araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur) ip_set_option(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, SOF_REUSEADDR); }
int 연결기다리기(int bara_denc_yombal) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir || araf_yu_bennoo_mbir->xeet_ngiir != 1) return -9;
    if (araf_yu_bennoo_mbir->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu = tcp_listen_with_backlog_and_err(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, 4, &보조항목);
    if (!jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu) return 오류번호(보조항목); araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur = jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu; araf_yu_bennoo_mbir->수신창구 = 1; tcp_arg(jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu, araf_yu_bennoo_mbir); tcp_accept(jokalinu_xibaar_Saytu_doxinu_ordinateur_gatandu, 연결받음); return 0;
}
int 망연결하기(int bara_denc_yombal, uint32_t dëkkuwaay, unsigned 접속번호) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir || araf_yu_bennoo_mbir->xeet_ngiir != 1) return -9;
    if (araf_yu_bennoo_mbir->njumte) return araf_yu_bennoo_mbir->njumte;
    if (araf_yu_bennoo_mbir->연결됨) return 0;
    if (araf_yu_bennoo_mbir->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !dëkkuwaay) return -22;
    ip_addr_t dëkkuwaayu_Internet; ip_addr_set_ip4_u32(&dëkkuwaayu_Internet, lwip_htonl(dëkkuwaay));
    araf_yu_bennoo_mbir->Nàttangoo_dëkkuwaay = dëkkuwaay; araf_yu_bennoo_mbir->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, &dëkkuwaayu_Internet, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int bara_denc_yombal) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir || !araf_yu_bennoo_mbir->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].xeet_ngiir == 1 && 통신끝점들[순번].대기중 == bara_denc_yombal) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int bara_denc_yombal, void *mbir, unsigned 개수) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir || araf_yu_bennoo_mbir->xeet_ngiir != 1) return -9;
    if (!개수) return 0; if (!araf_yu_bennoo_mbir->항목수) return araf_yu_bennoo_mbir->njumte ? araf_yu_bennoo_mbir->njumte : araf_yu_bennoo_mbir->bara_denc_jeexal ? 0 : -11;
    if (개수 > araf_yu_bennoo_mbir->항목수) 개수 = araf_yu_bennoo_mbir->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)mbir)[순번] = araf_yu_bennoo_mbir->mbir[araf_yu_bennoo_mbir->맨앞]; araf_yu_bennoo_mbir->맨앞 = (araf_yu_bennoo_mbir->맨앞 + 1) % sizeof(araf_yu_bennoo_mbir->mbir); }
    araf_yu_bennoo_mbir->항목수 -= 개수; if (araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur) tcp_recved(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, 개수); return 개수;
}
int 통신쓰기(int bara_denc_yombal, const void *mbir, unsigned 개수) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir || araf_yu_bennoo_mbir->xeet_ngiir != 1) return -9;
    if (araf_yu_bennoo_mbir->njumte) return araf_yu_bennoo_mbir->njumte; if (!araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur || !araf_yu_bennoo_mbir->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur)) 개수 = tcp_sndbuf(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, mbir, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur); return 개수;
}
int 전문보내기(int bara_denc_yombal, const void *mbir, unsigned 개수, uint32_t dëkkuwaay, unsigned 접속번호) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir || araf_yu_bennoo_mbir->xeet_ngiir != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, mbir, 개수); ip_addr_t dëkkuwaayu_Internet; ip_addr_set_ip4_u32(&dëkkuwaayu_Internet, lwip_htonl(dëkkuwaay));
    err_t 보조항목 = udp_sendto(araf_yu_bennoo_mbir->전문제어, 자료위치, &dëkkuwaayu_Internet, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int bara_denc_yombal, void *mbir, unsigned 개수) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir || araf_yu_bennoo_mbir->xeet_ngiir != 2) return -9;
    if (!araf_yu_bennoo_mbir->항목수) return -11; unsigned 현재위치 = araf_yu_bennoo_mbir->맨앞;
    if (개수 > araf_yu_bennoo_mbir->길이목록[현재위치]) 개수 = araf_yu_bennoo_mbir->길이목록[현재위치]; memcpy(mbir, araf_yu_bennoo_mbir->mbir + 현재위치 * 512, 개수);
    araf_yu_bennoo_mbir->상대창구번호 = araf_yu_bennoo_mbir->접속번호들[현재위치]; araf_yu_bennoo_mbir->Nàttangoo_dëkkuwaay = araf_yu_bennoo_mbir->주소목록[현재위치]; araf_yu_bennoo_mbir->맨앞 = (현재위치 + 1) % 4; araf_yu_bennoo_mbir->항목수--; return 개수;
}
unsigned 통신접속번호(int bara_denc_yombal) { 통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); return !araf_yu_bennoo_mbir ? 0 : araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur ? araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur->local_port : araf_yu_bennoo_mbir->전문제어 ? araf_yu_bennoo_mbir->전문제어->local_port : 0; }
unsigned 상대접속번호(int bara_denc_yombal) { 통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); return araf_yu_bennoo_mbir ? araf_yu_bennoo_mbir->상대창구번호 : 0; }
uint32_t 상대통신주소(int bara_denc_yombal) { 통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); return araf_yu_bennoo_mbir ? araf_yu_bennoo_mbir->Nàttangoo_dëkkuwaay : 0; }
void Tej_mbaal(int bara_denc_yombal) {
    통신끝점 *araf_yu_bennoo_mbir = 얻기(bara_denc_yombal); if (!araf_yu_bennoo_mbir) return;
    if (araf_yu_bennoo_mbir->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].xeet_ngiir && 통신끝점들[순번].대기중 == bara_denc_yombal) Tej_mbaal(순번);
    if (araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur) {
        tcp_arg(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, 0); if (araf_yu_bennoo_mbir->수신창구) tcp_accept(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, 0); else { tcp_recv(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, 0); tcp_err(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur, 0); }
        if (tcp_close(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur) != ERR_OK) tcp_abort(araf_yu_bennoo_mbir->jokkalóo_Saytu_doxinu_ordinateur);
    }
    if (araf_yu_bennoo_mbir->전문제어) udp_remove(araf_yu_bennoo_mbir->전문제어); araf_yu_bennoo_mbir->xeet_ngiir = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&jokkalóo_toftal);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (masin_bindu(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned kotu_araf = masin_bindu(보조장치 + 0x40) & 255;
        if (kotu_araf == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (jokkalóo_toftal.input(자료위치, &jokkalóo_toftal) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (kotu_araf == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kotu_araf != 220 && kotu_araf != 221) 수신오류 = 1; kotu_araf = kotu_araf == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = kotu_araf; else 수신오류 = 1;
        }
    }
    netif_poll(&jokkalóo_toftal); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (masin_bindu(보조장치 + 0x54) & 0x20); 처리한도++) {
        masin_bindu(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Jekkal_yi·조회는 lwIP의 liteew_mbir 인터페이스와 jeexal_Tomb 표를 사용한다. */
uint32_t 망상태읽기(unsigned dugal_xabaar_xëyma, unsigned àlluwa_tur) {
    if(dugal_xabaar_xëyma==20)return 유선사용;
    if(dugal_xabaar_xëyma==21)return 준비됨&&netif_is_link_up(&jokkalóo_toftal);
    if(dugal_xabaar_xëyma==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&dugal_xabaar_xëyma>=4&&dugal_xabaar_xëyma<=8)return 유선망집계(dugal_xabaar_xëyma-4);
    if (dugal_xabaar_xëyma == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&jokkalóo_toftal)));
    if (dugal_xabaar_xëyma == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&jokkalóo_toftal)));
    if (dugal_xabaar_xëyma == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&jokkalóo_toftal)));
    if (dugal_xabaar_xëyma == 3) return netif_is_up(&jokkalóo_toftal) != 0;
    if (dugal_xabaar_xëyma == 4) return 받은전문수;
    if (dugal_xabaar_xëyma == 5) return 보낸전문수;
    if (dugal_xabaar_xëyma == 6) return 받은바이트수;
    if (dugal_xabaar_xëyma == 7) return 보낸바이트수;
    if (dugal_xabaar_xëyma == 8) return 버린전문수;
    if (dugal_xabaar_xëyma == 9) return 송신개수;
    if (àlluwa_tur >= 32) return 0;
    통신끝점 *jeexal_Tomb = &통신끝점들[àlluwa_tur];
    if (dugal_xabaar_xëyma == 10) return jeexal_Tomb->xeet_ngiir;
    if (!jeexal_Tomb->xeet_ngiir) return 0;
    if (dugal_xabaar_xëyma == 11) return 통신접속번호(àlluwa_tur);
    if (dugal_xabaar_xëyma == 12) return jeexal_Tomb->Nàttangoo_dëkkuwaay;
    if (dugal_xabaar_xëyma == 13) return jeexal_Tomb->상대창구번호;
    if (dugal_xabaar_xëyma == 14) return jeexal_Tomb->수신창구 ? 1 : jeexal_Tomb->bara_denc_jeexal ? 3 : jeexal_Tomb->njumte ? 4 : jeexal_Tomb->연결됨 ? 2 : 0;
    if (dugal_xabaar_xëyma == 15) return jeexal_Tomb->항목수;
    if (dugal_xabaar_xëyma == 16) {
        const ip_addr_t *dëkkuwaay = jeexal_Tomb->xeet_ngiir == 1 && jeexal_Tomb->jokkalóo_Saytu_doxinu_ordinateur ? &jeexal_Tomb->jokkalóo_Saytu_doxinu_ordinateur->local_ip :
            jeexal_Tomb->xeet_ngiir == 2 && jeexal_Tomb->전문제어 ? &jeexal_Tomb->전문제어->local_ip : 0;
        return dëkkuwaay ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(dëkkuwaay))) : 0;
    }
    return 0;
}

int Jokkale_ak_ab_ordinateur_mbaal(unsigned jëf, uint32_t dëkkuwaay, uint32_t muuraay_xëyma, uint32_t bunt_xëyma) {
    if (!준비됨) return -100;
    if (jëf == 1) { netif_set_up(&jokkalóo_toftal); return 0; }
    if (jëf == 2) { netif_set_down(&jokkalóo_toftal); return 0; }
    if (jëf != 0) return -22;
    /* 유니캐스트 IPv4, 연속 muuraay_xëyma, 같은 망의 선택적 xayma_bi_teew bunt_xëyma. */
    uint32_t 뒤집은가림 = ~muuraay_xëyma;
    if (!muuraay_xëyma || (뒤집은가림 & (뒤집은가림 + 1)) || !dëkkuwaay || (dëkkuwaay >> 24) == 127 ||
        (dëkkuwaay >> 24) == 0 || (dëkkuwaay >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(dëkkuwaay & 뒤집은가림) || (dëkkuwaay & 뒤집은가림) == 뒤집은가림)) ||
        (bunt_xëyma && ((bunt_xëyma & muuraay_xëyma) != (dëkkuwaay & muuraay_xëyma) || bunt_xëyma == dëkkuwaay || (bunt_xëyma >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(bunt_xëyma & 뒤집은가림) || (bunt_xëyma & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 dëkkuwaay 변경으로 몰래 끊지 않는다. */
    for (unsigned àlluwa_tur = 0; àlluwa_tur < 32; àlluwa_tur++) if (통신끝점들[àlluwa_tur].xeet_ngiir &&
        !(통신끝점들[àlluwa_tur].수신창구 && 통신끝점들[àlluwa_tur].jokkalóo_Saytu_doxinu_ordinateur && ip_addr_isany(&통신끝점들[àlluwa_tur].jokkalóo_Saytu_doxinu_ordinateur->local_ip))) return -16;
    if(유선사용)dhcp_stop(&jokkalóo_toftal);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(dëkkuwaay)); ip4_addr_set_u32(&새가림, lwip_htonl(muuraay_xëyma)); ip4_addr_set_u32(&새관문, lwip_htonl(bunt_xëyma));
    netif_set_addr(&jokkalóo_toftal, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *jeexal_Tomb, struct pbuf *mbir, const ip_addr_t *dëkkuwaay) {
    (void)인수; (void)jeexal_Tomb;
    unsigned char 머리[20], tontu[16];
    if (응답상태 != -11 || mbir->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(dëkkuwaay))) != 시험주소 || pbuf_copy_partial(mbir, 머리, 20, 0) != 20) return 0;
    unsigned Tur_tolluwaay = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Tur_tolluwaay < 20 || mbir->tot_len < Tur_tolluwaay + 16 ||
        pbuf_copy_partial(mbir, tontu, 16, Tur_tolluwaay) != 16 || tontu[0] || tontu[1] ||
        (((unsigned)tontu[4] << 8) | tontu[5]) != 시험식별자 ||
        (((unsigned)tontu[6] << 8) | tontu[7]) != 시험순서 ||
        tontu[8] != 'J' || tontu[9] != 'K' || tontu[10] != 'O' || tontu[11] != 'S' ||
        (((uint32_t)tontu[12] << 24) | ((uint32_t)tontu[13] << 16) | ((uint32_t)tontu[14] << 8) | tontu[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(mbir, Tur_tolluwaay)) return 0;
    if (inet_chksum_pbuf(mbir)) { pbuf_add_header(mbir, Tur_tolluwaay); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(mbir); return 1;
}
int 응답시험시작(uint32_t dëkkuwaay, unsigned toftale_xëyma) {
    if (!준비됨 || !netif_is_up(&jokkalóo_toftal)) return -100;
    if (!dëkkuwaay || (dëkkuwaay >> 28) >= 14 || dëkkuwaay == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = dëkkuwaay; 시험순서 = toftale_xëyma & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char mbir[32] = {8,0,0,0};
    mbir[4] = 시험식별자 >> 8; mbir[5] = 시험식별자; mbir[6] = 시험순서 >> 8; mbir[7] = 시험순서;
    mbir[8]='J'; mbir[9]='K'; mbir[10]='O'; mbir[11]='S';
    mbir[12]=시험시각 >> 24; mbir[13]=시험시각 >> 16; mbir[14]=시험시각 >> 8; mbir[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(mbir); 자리++) mbir[자리] = 자리;
    uint16_t 확인합 = inet_chksum(mbir, sizeof(mbir)); memcpy(mbir + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(mbir), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, mbir, sizeof(mbir)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(dëkkuwaay));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned dugal_xabaar_xëyma) {
    통신망살피기();
    return dugal_xabaar_xëyma == 0 ? 응답상태 : dugal_xabaar_xëyma == 1 ? (int)응답시간 : dugal_xabaar_xëyma == 2 ? (int)응답차례 : -22;
}
