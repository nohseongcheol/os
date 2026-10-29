#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Şəbəkə_Yığın.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../uzaq_VALUE/uzaq_VALUE.h"
#include "naqilli_Şəbəkə.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define maşın_qeydiyyatdan_keçmək(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif qoşulma_cihaz;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_bayt_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_sahə, 수신창구, 대기중, 연결됨, fayl_bitirmək, XƏTA;
    struct tcp_pcb *qoşulma_nəzarət;
    struct udp_pcb *전문제어;
    unsigned ön_daxiletmə, daxiletmə_COUNT;
    unsigned char verilənlər[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], eynisəviyyəli_ünvan;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *əldə_et_VALUE(int fayl_tutacaq) { return fayl_tutacaq >= 0 && fayl_tutacaq < 32 && 통신끝점들[fayl_tutacaq].TYPE_sahə ? &통신끝점들[fayl_tutacaq] : 0; }
static int 예약하기(int TYPE_sahə) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_sahə) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_sahə = TYPE_sahə; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned simvol_kodu) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = simvol_kodu; }
static err_t 출력결과(struct netif *element_COUNT, struct pbuf *verilənlər_yerinə_qoymaq, const ip4_addr_t *ünvan) {
    (void)element_COUNT; (void)ünvan;
    if (verilənlər_yerinə_qoymaq->tot_len > 1500 || 송신개수 + 2 * verilənlər_yerinə_qoymaq->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Sonrakı_OFFSET = verilənlər_yerinə_qoymaq; Sonrakı_OFFSET; Sonrakı_OFFSET = Sonrakı_OFFSET->next) for (unsigned 순번 = 0; 순번 < Sonrakı_OFFSET->len; 순번++) {
        unsigned simvol_kodu = ((unsigned char *)Sonrakı_OFFSET->payload)[순번];
        if (simvol_kodu == 192 || simvol_kodu == 219) { 내보내기(219); 내보내기(simvol_kodu == 192 ? 220 : 221); } else 내보내기(simvol_kodu);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += verilənlər_yerinə_qoymaq->tot_len; return ERR_OK;
}
static err_t Hazırla_ümumi_dil_icrası(struct netif *element_COUNT) { element_COUNT->name[0] = 's'; element_COUNT->name[1] = 'l'; element_COUNT->mtu = 1500; element_COUNT->output = 출력결과; return ERR_OK; }
void Hazırla_Şəbəkə(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    maşın_qeydiyyatdan_keçmək(보조장치 + 4) |= 1; maşın_qeydiyyatdan_keçmək(보조장치 + 0x60) = 0; maşın_qeydiyyatdan_keçmək(보조장치 + 0x44) = 0;
    maşın_qeydiyyatdan_keçmək(보조장치 + 0x48) = 0xc6; maşın_qeydiyyatdan_keçmək(보조장치 + 0x4c) = 3; maşın_qeydiyyatdan_keçmək(보조장치 + 0x68) = 270; maşın_qeydiyyatdan_keçmək(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t İnternet_ünvanı, bit_maska, şlüz_ünvan;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&İnternet_ünvanı, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_maska, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&şlüz_ünvan, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&qoşulma_cihaz, &İnternet_ünvanı, &bit_maska, &şlüz_ünvan, 0, 유선사용?Hazırla_naqilli_Şəbəkə:Hazırla_ümumi_dil_icrası, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&qoşulma_cihaz); netif_set_up(&qoşulma_cihaz);if(!유선사용)netif_set_link_up(&qoşulma_cihaz); 준비됨 = 1;
    Hazırla_uzaq();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *ötürülmə_nəzarət_blokla, struct pbuf *verilənlər_yerinə_qoymaq, err_t XƏTA) {
    통신끝점 *sətir_verilənlər = 부가인수; (void)ötürülmə_nəzarət_blokla; (void)XƏTA;
    if (!verilənlər_yerinə_qoymaq) { sətir_verilənlər->fayl_bitirmək = 1; return ERR_OK; }
    if (verilənlər_yerinə_qoymaq->tot_len > sizeof(sətir_verilənlər->verilənlər) - sətir_verilənlər->daxiletmə_COUNT) return ERR_MEM;
    unsigned 현재위치 = (sətir_verilənlər->ön_daxiletmə + sətir_verilənlər->daxiletmə_COUNT) % sizeof(sətir_verilənlər->verilənlər);
    for (struct pbuf *Sonrakı_OFFSET = verilənlər_yerinə_qoymaq; Sonrakı_OFFSET; Sonrakı_OFFSET = Sonrakı_OFFSET->next) for (unsigned 순번 = 0; 순번 < Sonrakı_OFFSET->len; 순번++) {
        sətir_verilənlər->verilənlər[현재위치] = ((unsigned char *)Sonrakı_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(sətir_verilənlər->verilənlər);
    }
    sətir_verilənlər->daxiletmə_COUNT += verilənlər_yerinə_qoymaq->tot_len; pbuf_free(verilənlər_yerinə_qoymaq); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t XƏTA) { 통신끝점 *sətir_verilənlər = 부가인수; sətir_verilənlər->qoşulma_nəzarət = 0; sətir_verilənlər->XƏTA = 오류번호(XƏTA); }
static void 되부름목록(통신끝점 *sətir_verilənlər) { tcp_arg(sətir_verilənlər->qoşulma_nəzarət, sətir_verilənlər); tcp_recv(sətir_verilənlər->qoşulma_nəzarət, 수신됨); tcp_err(sətir_verilənlər->qoşulma_nəzarət, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *ötürülmə_nəzarət_blokla, err_t XƏTA) {
    통신끝점 *sətir_verilənlər = 부가인수; (void)ötürülmə_nəzarət_blokla; if (XƏTA) sətir_verilənlər->XƏTA = 오류번호(XƏTA); else sətir_verilənlər->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *ötürülmə_nəzarət_blokla, err_t XƏTA) {
    통신끝점 *부모항목 = 부가인수; if (XƏTA) return XƏTA;
    int fayl_tutacaq = 예약하기(1); if (fayl_tutacaq < 0) return ERR_MEM;
    통신끝점 *sətir_verilənlər = &통신끝점들[fayl_tutacaq]; sətir_verilənlər->qoşulma_nəzarət = ötürülmə_nəzarət_blokla; sətir_verilənlər->연결됨 = 1; sətir_verilənlər->대기중 = (int)(부모항목 - 통신끝점들);
    sətir_verilənlər->eynisəviyyəli_ünvan = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&ötürülmə_nəzarət_blokla->remote_ip))); sətir_verilənlər->상대창구번호 = ötürülmə_nəzarət_blokla->remote_port;
    되부름목록(sətir_verilənlər); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *ötürülmə_nəzarət_blokla, struct pbuf *verilənlər_yerinə_qoymaq, const ip_addr_t *ünvan, u16_t 접속번호) {
    통신끝점 *sətir_verilənlər = 부가인수; (void)ötürülmə_nəzarət_blokla;
    if (sətir_verilənlər->daxiletmə_COUNT < 4 && verilənlər_yerinə_qoymaq->tot_len <= 512) {
        unsigned yerinə_qoymaq_INDEX = (sətir_verilənlər->ön_daxiletmə + sətir_verilənlər->daxiletmə_COUNT) % 4;
        pbuf_copy_partial(verilənlər_yerinə_qoymaq, sətir_verilənlər->verilənlər + yerinə_qoymaq_INDEX * 512, verilənlər_yerinə_qoymaq->tot_len, 0);
        sətir_verilənlər->길이목록[yerinə_qoymaq_INDEX] = verilənlər_yerinə_qoymaq->tot_len; sətir_verilənlər->접속번호들[yerinə_qoymaq_INDEX] = 접속번호;
        sətir_verilənlər->주소목록[yerinə_qoymaq_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ünvan))); sətir_verilənlər->daxiletmə_COUNT++;
    }
    pbuf_free(verilənlər_yerinə_qoymaq);
}
int 통신끝점만들기(int TYPE_sahə) {
    if (!준비됨) return -100;
    if (TYPE_sahə != 1 && TYPE_sahə != 2) return -93;
    int fayl_tutacaq = 예약하기(TYPE_sahə); if (fayl_tutacaq < 0) return fayl_tutacaq;
    통신끝점 *sətir_verilənlər = &통신끝점들[fayl_tutacaq];
    if (TYPE_sahə == 1) { sətir_verilənlər->qoşulma_nəzarət = tcp_new(); if (sətir_verilənlər->qoşulma_nəzarət) 되부름목록(sətir_verilənlər); }
    else { sətir_verilənlər->전문제어 = udp_new(); if (sətir_verilənlər->전문제어) udp_recv(sətir_verilənlər->전문제어, 전문, sətir_verilənlər); }
    if (!sətir_verilənlər->qoşulma_nəzarət && !sətir_verilənlər->전문제어) { sətir_verilənlər->TYPE_sahə = 0; return -12; } return fayl_tutacaq;
}
int 망주소묶기(int fayl_tutacaq, uint32_t ünvan, unsigned 접속번호) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər) return -9;
    if (접속번호 > 65535 || (ünvan && ünvan != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&qoşulma_cihaz))) && ünvan != 0x7f000001)) return -99;
    ip_addr_t İnternet_ünvanı; ip_addr_set_ip4_u32(&İnternet_ünvanı, lwip_htonl(ünvan));
    err_t 보조항목 = sətir_verilənlər->TYPE_sahə == 1 ? tcp_bind(sətir_verilənlər->qoşulma_nəzarət, &İnternet_ünvanı, 접속번호) : udp_bind(sətir_verilənlər->전문제어, &İnternet_ünvanı, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int fayl_tutacaq) { 통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (sətir_verilənlər && sətir_verilənlər->qoşulma_nəzarət) ip_set_option(sətir_verilənlər->qoşulma_nəzarət, SOF_REUSEADDR); }
int 연결기다리기(int fayl_tutacaq) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər || sətir_verilənlər->TYPE_sahə != 1) return -9;
    if (sətir_verilənlər->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *ötürülmə_nəzarət_blokla = tcp_listen_with_backlog_and_err(sətir_verilənlər->qoşulma_nəzarət, 4, &보조항목);
    if (!ötürülmə_nəzarət_blokla) return 오류번호(보조항목); sətir_verilənlər->qoşulma_nəzarət = ötürülmə_nəzarət_blokla; sətir_verilənlər->수신창구 = 1; tcp_arg(ötürülmə_nəzarət_blokla, sətir_verilənlər); tcp_accept(ötürülmə_nəzarət_blokla, 연결받음); return 0;
}
int 망연결하기(int fayl_tutacaq, uint32_t ünvan, unsigned 접속번호) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər || sətir_verilənlər->TYPE_sahə != 1) return -9;
    if (sətir_verilənlər->XƏTA) return sətir_verilənlər->XƏTA;
    if (sətir_verilənlər->연결됨) return 0;
    if (sətir_verilənlər->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !ünvan) return -22;
    ip_addr_t İnternet_ünvanı; ip_addr_set_ip4_u32(&İnternet_ünvanı, lwip_htonl(ünvan));
    sətir_verilənlər->eynisəviyyəli_ünvan = ünvan; sətir_verilənlər->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(sətir_verilənlər->qoşulma_nəzarət, &İnternet_ünvanı, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int fayl_tutacaq) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər || !sətir_verilənlər->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_sahə == 1 && 통신끝점들[순번].대기중 == fayl_tutacaq) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int fayl_tutacaq, void *verilənlər, unsigned element_COUNT) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər || sətir_verilənlər->TYPE_sahə != 1) return -9;
    if (!element_COUNT) return 0; if (!sətir_verilənlər->daxiletmə_COUNT) return sətir_verilənlər->XƏTA ? sətir_verilənlər->XƏTA : sətir_verilənlər->fayl_bitirmək ? 0 : -11;
    if (element_COUNT > sətir_verilənlər->daxiletmə_COUNT) element_COUNT = sətir_verilənlər->daxiletmə_COUNT;
    for (unsigned 순번 = 0; 순번 < element_COUNT; 순번++) { ((unsigned char *)verilənlər)[순번] = sətir_verilənlər->verilənlər[sətir_verilənlər->ön_daxiletmə]; sətir_verilənlər->ön_daxiletmə = (sətir_verilənlər->ön_daxiletmə + 1) % sizeof(sətir_verilənlər->verilənlər); }
    sətir_verilənlər->daxiletmə_COUNT -= element_COUNT; if (sətir_verilənlər->qoşulma_nəzarət) tcp_recved(sətir_verilənlər->qoşulma_nəzarət, element_COUNT); return element_COUNT;
}
int 통신쓰기(int fayl_tutacaq, const void *verilənlər, unsigned element_COUNT) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər || sətir_verilənlər->TYPE_sahə != 1) return -9;
    if (sətir_verilənlər->XƏTA) return sətir_verilənlər->XƏTA; if (!sətir_verilənlər->qoşulma_nəzarət || !sətir_verilənlər->연결됨) return -107;
    if (!element_COUNT) return 0; if (element_COUNT > tcp_sndbuf(sətir_verilənlər->qoşulma_nəzarət)) element_COUNT = tcp_sndbuf(sətir_verilənlər->qoşulma_nəzarət);
    if (!element_COUNT) return -11; if (element_COUNT > 1024) element_COUNT = 1024;
    err_t 보조항목 = tcp_write(sətir_verilənlər->qoşulma_nəzarət, verilənlər, element_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(sətir_verilənlər->qoşulma_nəzarət); return element_COUNT;
}
int 전문보내기(int fayl_tutacaq, const void *verilənlər, unsigned element_COUNT, uint32_t ünvan, unsigned 접속번호) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər || sətir_verilənlər->TYPE_sahə != 2) return -9;
    if (element_COUNT > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *verilənlər_yerinə_qoymaq = pbuf_alloc(PBUF_TRANSPORT, element_COUNT, PBUF_RAM); if (!verilənlər_yerinə_qoymaq) return -11;
    pbuf_take(verilənlər_yerinə_qoymaq, verilənlər, element_COUNT); ip_addr_t İnternet_ünvanı; ip_addr_set_ip4_u32(&İnternet_ünvanı, lwip_htonl(ünvan));
    err_t 보조항목 = udp_sendto(sətir_verilənlər->전문제어, verilənlər_yerinə_qoymaq, &İnternet_ünvanı, 접속번호); pbuf_free(verilənlər_yerinə_qoymaq); return 보조항목 ? 오류번호(보조항목) : (int)element_COUNT;
}
int 전문받기(int fayl_tutacaq, void *verilənlər, unsigned element_COUNT) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər || sətir_verilənlər->TYPE_sahə != 2) return -9;
    if (!sətir_verilənlər->daxiletmə_COUNT) return -11; unsigned 현재위치 = sətir_verilənlər->ön_daxiletmə;
    if (element_COUNT > sətir_verilənlər->길이목록[현재위치]) element_COUNT = sətir_verilənlər->길이목록[현재위치]; memcpy(verilənlər, sətir_verilənlər->verilənlər + 현재위치 * 512, element_COUNT);
    sətir_verilənlər->상대창구번호 = sətir_verilənlər->접속번호들[현재위치]; sətir_verilənlər->eynisəviyyəli_ünvan = sətir_verilənlər->주소목록[현재위치]; sətir_verilənlər->ön_daxiletmə = (현재위치 + 1) % 4; sətir_verilənlər->daxiletmə_COUNT--; return element_COUNT;
}
unsigned 통신접속번호(int fayl_tutacaq) { 통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); return !sətir_verilənlər ? 0 : sətir_verilənlər->qoşulma_nəzarət ? sətir_verilənlər->qoşulma_nəzarət->local_port : sətir_verilənlər->전문제어 ? sətir_verilənlər->전문제어->local_port : 0; }
unsigned 상대접속번호(int fayl_tutacaq) { 통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); return sətir_verilənlər ? sətir_verilənlər->상대창구번호 : 0; }
uint32_t 상대통신주소(int fayl_tutacaq) { 통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); return sətir_verilənlər ? sətir_verilənlər->eynisəviyyəli_ünvan : 0; }
void bağlamaq_Şəbəkə(int fayl_tutacaq) {
    통신끝점 *sətir_verilənlər = əldə_et_VALUE(fayl_tutacaq); if (!sətir_verilənlər) return;
    if (sətir_verilənlər->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_sahə && 통신끝점들[순번].대기중 == fayl_tutacaq) bağlamaq_Şəbəkə(순번);
    if (sətir_verilənlər->qoşulma_nəzarət) {
        tcp_arg(sətir_verilənlər->qoşulma_nəzarət, 0); if (sətir_verilənlər->수신창구) tcp_accept(sətir_verilənlər->qoşulma_nəzarət, 0); else { tcp_recv(sətir_verilənlər->qoşulma_nəzarət, 0); tcp_err(sətir_verilənlər->qoşulma_nəzarət, 0); }
        if (tcp_close(sətir_verilənlər->qoşulma_nəzarət) != ERR_OK) tcp_abort(sətir_verilənlər->qoşulma_nəzarət);
    }
    if (sətir_verilənlər->전문제어) udp_remove(sətir_verilənlər->전문제어); sətir_verilənlər->TYPE_sahə = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&qoşulma_cihaz);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (maşın_qeydiyyatdan_keçmək(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned simvol_kodu = maşın_qeydiyyatdan_keçmək(보조장치 + 0x40) & 255;
        if (simvol_kodu == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *verilənlər_yerinə_qoymaq = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (verilənlər_yerinə_qoymaq) { 받은전문수++; RECEIVED_bayt_COUNT += 수신사용량; pbuf_take(verilənlər_yerinə_qoymaq, 수신자료, 수신사용량); if (qoşulma_cihaz.input(verilənlər_yerinə_qoymaq, &qoşulma_cihaz) != ERR_OK) { 버린전문수++; pbuf_free(verilənlər_yerinə_qoymaq); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (simvol_kodu == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (simvol_kodu != 220 && simvol_kodu != 221) 수신오류 = 1; simvol_kodu = simvol_kodu == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = simvol_kodu; else 수신오류 = 1;
        }
    }
    netif_poll(&qoşulma_cihaz); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (maşın_qeydiyyatdan_keçmək(보조장치 + 0x54) & 0x20); 처리한도++) {
        maşın_qeydiyyatdan_keçmək(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Sazlama·조회는 lwIP의 faktiki_verilənlər 인터페이스와 bitirmək_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned daxiletmə_VALUE, unsigned INDEX) {
    if(daxiletmə_VALUE==20)return 유선사용;
    if(daxiletmə_VALUE==21)return 준비됨&&netif_is_link_up(&qoşulma_cihaz);
    if(daxiletmə_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&daxiletmə_VALUE>=4&&daxiletmə_VALUE<=8)return 유선망집계(daxiletmə_VALUE-4);
    if (daxiletmə_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&qoşulma_cihaz)));
    if (daxiletmə_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&qoşulma_cihaz)));
    if (daxiletmə_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&qoşulma_cihaz)));
    if (daxiletmə_VALUE == 3) return netif_is_up(&qoşulma_cihaz) != 0;
    if (daxiletmə_VALUE == 4) return 받은전문수;
    if (daxiletmə_VALUE == 5) return 보낸전문수;
    if (daxiletmə_VALUE == 6) return RECEIVED_bayt_COUNT;
    if (daxiletmə_VALUE == 7) return 보낸바이트수;
    if (daxiletmə_VALUE == 8) return 버린전문수;
    if (daxiletmə_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *bitirmək_p = &통신끝점들[INDEX];
    if (daxiletmə_VALUE == 10) return bitirmək_p->TYPE_sahə;
    if (!bitirmək_p->TYPE_sahə) return 0;
    if (daxiletmə_VALUE == 11) return 통신접속번호(INDEX);
    if (daxiletmə_VALUE == 12) return bitirmək_p->eynisəviyyəli_ünvan;
    if (daxiletmə_VALUE == 13) return bitirmək_p->상대창구번호;
    if (daxiletmə_VALUE == 14) return bitirmək_p->수신창구 ? 1 : bitirmək_p->fayl_bitirmək ? 3 : bitirmək_p->XƏTA ? 4 : bitirmək_p->연결됨 ? 2 : 0;
    if (daxiletmə_VALUE == 15) return bitirmək_p->daxiletmə_COUNT;
    if (daxiletmə_VALUE == 16) {
        const ip_addr_t *ünvan = bitirmək_p->TYPE_sahə == 1 && bitirmək_p->qoşulma_nəzarət ? &bitirmək_p->qoşulma_nəzarət->local_ip :
            bitirmək_p->TYPE_sahə == 2 && bitirmək_p->전문제어 ? &bitirmək_p->전문제어->local_ip : 0;
        return ünvan ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ünvan))) : 0;
    }
    return 0;
}

int konfiqurasiya_etmək_Şəbəkə(unsigned Gedişat, uint32_t ünvan, uint32_t maska_VALUE, uint32_t şlüz_VALUE) {
    if (!준비됨) return -100;
    if (Gedişat == 1) { netif_set_up(&qoşulma_cihaz); return 0; }
    if (Gedişat == 2) { netif_set_down(&qoşulma_cihaz); return 0; }
    if (Gedişat != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_VALUE, 같은 망의 선택적 standart_qiymət şlüz_VALUE. */
    uint32_t 뒤집은가림 = ~maska_VALUE;
    if (!maska_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !ünvan || (ünvan >> 24) == 127 ||
        (ünvan >> 24) == 0 || (ünvan >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ünvan & 뒤집은가림) || (ünvan & 뒤집은가림) == 뒤집은가림)) ||
        (şlüz_VALUE && ((şlüz_VALUE & maska_VALUE) != (ünvan & maska_VALUE) || şlüz_VALUE == ünvan || (şlüz_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(şlüz_VALUE & 뒤집은가림) || (şlüz_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ünvan 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_sahə &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].qoşulma_nəzarət && ip_addr_isany(&통신끝점들[INDEX].qoşulma_nəzarət->local_ip))) return -16;
    if(유선사용)dhcp_stop(&qoşulma_cihaz);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ünvan)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(şlüz_VALUE));
    netif_set_addr(&qoşulma_cihaz, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, video_münasibət_TIME;
static unsigned 시험순서, 시험식별자, video_münasibət_SEQUENCE;
static int video_münasibət_vəziyyət;
static u8_t 응답받음(void *인수, struct raw_pcb *bitirmək_p, struct pbuf *verilənlər, const ip_addr_t *ünvan) {
    (void)인수; (void)bitirmək_p;
    unsigned char 머리[20], cavab[16];
    if (video_münasibət_vəziyyət != -11 || verilənlər->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ünvan))) != 시험주소 || pbuf_copy_partial(verilənlər, 머리, 20, 0) != 20) return 0;
    unsigned Başlıq_ölçünü_dəyişmək = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Başlıq_ölçünü_dəyişmək < 20 || verilənlər->tot_len < Başlıq_ölçünü_dəyişmək + 16 ||
        pbuf_copy_partial(verilənlər, cavab, 16, Başlıq_ölçünü_dəyişmək) != 16 || cavab[0] || cavab[1] ||
        (((unsigned)cavab[4] << 8) | cavab[5]) != 시험식별자 ||
        (((unsigned)cavab[6] << 8) | cavab[7]) != 시험순서 ||
        cavab[8] != 'J' || cavab[9] != 'K' || cavab[10] != 'O' || cavab[11] != 'S' ||
        (((uint32_t)cavab[12] << 24) | ((uint32_t)cavab[13] << 16) | ((uint32_t)cavab[14] << 8) | cavab[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(verilənlər, Başlıq_ölçünü_dəyişmək)) return 0;
    if (inet_chksum_pbuf(verilənlər)) { pbuf_add_header(verilənlər, Başlıq_ölçünü_dəyişmək); return 0; }
    video_münasibət_TIME = (uint32_t)보드밀리초() - 시험시각; video_münasibət_SEQUENCE = 머리[8]; video_münasibət_vəziyyət = 0;
    pbuf_free(verilənlər); return 1;
}
int 응답시험시작(uint32_t ünvan, unsigned ardıcıllıq_VALUE) {
    if (!준비됨 || !netif_is_up(&qoşulma_cihaz)) return -100;
    if (!ünvan || (ünvan >> 28) >= 14 || ünvan == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ünvan; 시험순서 = ardıcıllıq_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); video_münasibət_vəziyyət = -11; video_münasibət_TIME = video_münasibət_SEQUENCE = 0;
    unsigned char verilənlər[32] = {8,0,0,0};
    verilənlər[4] = 시험식별자 >> 8; verilənlər[5] = 시험식별자; verilənlər[6] = 시험순서 >> 8; verilənlər[7] = 시험순서;
    verilənlər[8]='J'; verilənlər[9]='K'; verilənlər[10]='O'; verilənlər[11]='S';
    verilənlər[12]=시험시각 >> 24; verilənlər[13]=시험시각 >> 16; verilənlər[14]=시험시각 >> 8; verilənlər[15]=시험시각;
    for (unsigned yerinə_qoymaq_INDEX = 16; yerinə_qoymaq_INDEX < sizeof(verilənlər); yerinə_qoymaq_INDEX++) verilənlər[yerinə_qoymaq_INDEX] = yerinə_qoymaq_INDEX;
    uint16_t 확인합 = inet_chksum(verilənlər, sizeof(verilənlər)); memcpy(verilənlər + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(verilənlər), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, verilənlər, sizeof(verilənlər)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ünvan));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) video_münasibət_vəziyyət = 오류번호(처리값);
    return 처리값 ? video_münasibət_vəziyyət : 0;
}
int 응답시험읽기(unsigned daxiletmə_VALUE) {
    통신망살피기();
    return daxiletmə_VALUE == 0 ? video_münasibət_vəziyyət : daxiletmə_VALUE == 1 ? (int)video_münasibət_TIME : daxiletmə_VALUE == 2 ? (int)video_münasibət_SEQUENCE : -22;
}
