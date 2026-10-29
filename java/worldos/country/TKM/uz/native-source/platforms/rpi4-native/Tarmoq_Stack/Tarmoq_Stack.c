#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Tarmoq_Stack.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../masofaviy_VALUE/masofaviy_VALUE.h"
#include "o_tkazish_Tarmoq.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif aloqa_qurilma;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_bayt_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_toifa, 수신창구, 대기중, 연결됨, fayl_to_xtatmoq, Xato;
    struct tcp_pcb *aloqa_boshqaruv;
    struct udp_pcb *전문제어;
    unsigned old_kamera_kiritish, kiritish_COUNT;
    unsigned char ma_lumotlar[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], bir_rangli_manzil;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *olish_VALUE(int fayl_deskriptor) { return fayl_deskriptor >= 0 && fayl_deskriptor < 32 && 통신끝점들[fayl_deskriptor].TYPE_toifa ? &통신끝점들[fayl_deskriptor] : 0; }
static int 예약하기(int TYPE_toifa) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_toifa) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_toifa = TYPE_toifa; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned belgi_kodi) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = belgi_kodi; }
static err_t 출력결과(struct netif *element_COUNT, struct pbuf *ma_lumotlar_holat, const ip4_addr_t *manzil) {
    (void)element_COUNT; (void)manzil;
    if (ma_lumotlar_holat->tot_len > 1500 || 송신개수 + 2 * ma_lumotlar_holat->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Keyingi_OFFSET = ma_lumotlar_holat; Keyingi_OFFSET; Keyingi_OFFSET = Keyingi_OFFSET->next) for (unsigned 순번 = 0; 순번 < Keyingi_OFFSET->len; 순번++) {
        unsigned belgi_kodi = ((unsigned char *)Keyingi_OFFSET->payload)[순번];
        if (belgi_kodi == 192 || belgi_kodi == 219) { 내보내기(219); 내보내기(belgi_kodi == 192 ? 220 : 221); } else 내보내기(belgi_kodi);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += ma_lumotlar_holat->tot_len; return ERR_OK;
}
static err_t Tayyorlamoq_umumiy_til_ish_jarayoni(struct netif *element_COUNT) { element_COUNT->name[0] = 's'; element_COUNT->name[1] = 'l'; element_COUNT->mtu = 1500; element_COUNT->output = 출력결과; return ERR_OK; }
void Tayyorlamoq_Tarmoq(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    기계저장기(보조장치 + 4) |= 1; 기계저장기(보조장치 + 0x60) = 0; 기계저장기(보조장치 + 0x44) = 0;
    기계저장기(보조장치 + 0x48) = 0xc6; 기계저장기(보조장치 + 0x4c) = 3; 기계저장기(보조장치 + 0x68) = 270; 기계저장기(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internetdagi_manzil, bit_niqob, shluz_manzil;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Internetdagi_manzil, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_niqob, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&shluz_manzil, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&aloqa_qurilma, &Internetdagi_manzil, &bit_niqob, &shluz_manzil, 0, 유선사용?Tayyorlamoq_o_tkazish_Tarmoq:Tayyorlamoq_umumiy_til_ish_jarayoni, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&aloqa_qurilma); netif_set_up(&aloqa_qurilma);if(!유선사용)netif_set_link_up(&aloqa_qurilma); 준비됨 = 1;
    Tayyorlamoq_masofaviy();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *uzatish_boshqaruv_bloklash, struct pbuf *ma_lumotlar_holat, err_t Xato) {
    통신끝점 *satr_ma_lumotlar = 부가인수; (void)uzatish_boshqaruv_bloklash; (void)Xato;
    if (!ma_lumotlar_holat) { satr_ma_lumotlar->fayl_to_xtatmoq = 1; return ERR_OK; }
    if (ma_lumotlar_holat->tot_len > sizeof(satr_ma_lumotlar->ma_lumotlar) - satr_ma_lumotlar->kiritish_COUNT) return ERR_MEM;
    unsigned 현재위치 = (satr_ma_lumotlar->old_kamera_kiritish + satr_ma_lumotlar->kiritish_COUNT) % sizeof(satr_ma_lumotlar->ma_lumotlar);
    for (struct pbuf *Keyingi_OFFSET = ma_lumotlar_holat; Keyingi_OFFSET; Keyingi_OFFSET = Keyingi_OFFSET->next) for (unsigned 순번 = 0; 순번 < Keyingi_OFFSET->len; 순번++) {
        satr_ma_lumotlar->ma_lumotlar[현재위치] = ((unsigned char *)Keyingi_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(satr_ma_lumotlar->ma_lumotlar);
    }
    satr_ma_lumotlar->kiritish_COUNT += ma_lumotlar_holat->tot_len; pbuf_free(ma_lumotlar_holat); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Xato) { 통신끝점 *satr_ma_lumotlar = 부가인수; satr_ma_lumotlar->aloqa_boshqaruv = 0; satr_ma_lumotlar->Xato = 오류번호(Xato); }
static void 되부름목록(통신끝점 *satr_ma_lumotlar) { tcp_arg(satr_ma_lumotlar->aloqa_boshqaruv, satr_ma_lumotlar); tcp_recv(satr_ma_lumotlar->aloqa_boshqaruv, 수신됨); tcp_err(satr_ma_lumotlar->aloqa_boshqaruv, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *uzatish_boshqaruv_bloklash, err_t Xato) {
    통신끝점 *satr_ma_lumotlar = 부가인수; (void)uzatish_boshqaruv_bloklash; if (Xato) satr_ma_lumotlar->Xato = 오류번호(Xato); else satr_ma_lumotlar->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *uzatish_boshqaruv_bloklash, err_t Xato) {
    통신끝점 *부모항목 = 부가인수; if (Xato) return Xato;
    int fayl_deskriptor = 예약하기(1); if (fayl_deskriptor < 0) return ERR_MEM;
    통신끝점 *satr_ma_lumotlar = &통신끝점들[fayl_deskriptor]; satr_ma_lumotlar->aloqa_boshqaruv = uzatish_boshqaruv_bloklash; satr_ma_lumotlar->연결됨 = 1; satr_ma_lumotlar->대기중 = (int)(부모항목 - 통신끝점들);
    satr_ma_lumotlar->bir_rangli_manzil = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&uzatish_boshqaruv_bloklash->remote_ip))); satr_ma_lumotlar->상대창구번호 = uzatish_boshqaruv_bloklash->remote_port;
    되부름목록(satr_ma_lumotlar); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *uzatish_boshqaruv_bloklash, struct pbuf *ma_lumotlar_holat, const ip_addr_t *manzil, u16_t 접속번호) {
    통신끝점 *satr_ma_lumotlar = 부가인수; (void)uzatish_boshqaruv_bloklash;
    if (satr_ma_lumotlar->kiritish_COUNT < 4 && ma_lumotlar_holat->tot_len <= 512) {
        unsigned holat_INDEX = (satr_ma_lumotlar->old_kamera_kiritish + satr_ma_lumotlar->kiritish_COUNT) % 4;
        pbuf_copy_partial(ma_lumotlar_holat, satr_ma_lumotlar->ma_lumotlar + holat_INDEX * 512, ma_lumotlar_holat->tot_len, 0);
        satr_ma_lumotlar->길이목록[holat_INDEX] = ma_lumotlar_holat->tot_len; satr_ma_lumotlar->접속번호들[holat_INDEX] = 접속번호;
        satr_ma_lumotlar->주소목록[holat_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(manzil))); satr_ma_lumotlar->kiritish_COUNT++;
    }
    pbuf_free(ma_lumotlar_holat);
}
int 통신끝점만들기(int TYPE_toifa) {
    if (!준비됨) return -100;
    if (TYPE_toifa != 1 && TYPE_toifa != 2) return -93;
    int fayl_deskriptor = 예약하기(TYPE_toifa); if (fayl_deskriptor < 0) return fayl_deskriptor;
    통신끝점 *satr_ma_lumotlar = &통신끝점들[fayl_deskriptor];
    if (TYPE_toifa == 1) { satr_ma_lumotlar->aloqa_boshqaruv = tcp_new(); if (satr_ma_lumotlar->aloqa_boshqaruv) 되부름목록(satr_ma_lumotlar); }
    else { satr_ma_lumotlar->전문제어 = udp_new(); if (satr_ma_lumotlar->전문제어) udp_recv(satr_ma_lumotlar->전문제어, 전문, satr_ma_lumotlar); }
    if (!satr_ma_lumotlar->aloqa_boshqaruv && !satr_ma_lumotlar->전문제어) { satr_ma_lumotlar->TYPE_toifa = 0; return -12; } return fayl_deskriptor;
}
int 망주소묶기(int fayl_deskriptor, uint32_t manzil, unsigned 접속번호) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar) return -9;
    if (접속번호 > 65535 || (manzil && manzil != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&aloqa_qurilma))) && manzil != 0x7f000001)) return -99;
    ip_addr_t Internetdagi_manzil; ip_addr_set_ip4_u32(&Internetdagi_manzil, lwip_htonl(manzil));
    err_t 보조항목 = satr_ma_lumotlar->TYPE_toifa == 1 ? tcp_bind(satr_ma_lumotlar->aloqa_boshqaruv, &Internetdagi_manzil, 접속번호) : udp_bind(satr_ma_lumotlar->전문제어, &Internetdagi_manzil, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int fayl_deskriptor) { 통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (satr_ma_lumotlar && satr_ma_lumotlar->aloqa_boshqaruv) ip_set_option(satr_ma_lumotlar->aloqa_boshqaruv, SOF_REUSEADDR); }
int 연결기다리기(int fayl_deskriptor) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar || satr_ma_lumotlar->TYPE_toifa != 1) return -9;
    if (satr_ma_lumotlar->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *uzatish_boshqaruv_bloklash = tcp_listen_with_backlog_and_err(satr_ma_lumotlar->aloqa_boshqaruv, 4, &보조항목);
    if (!uzatish_boshqaruv_bloklash) return 오류번호(보조항목); satr_ma_lumotlar->aloqa_boshqaruv = uzatish_boshqaruv_bloklash; satr_ma_lumotlar->수신창구 = 1; tcp_arg(uzatish_boshqaruv_bloklash, satr_ma_lumotlar); tcp_accept(uzatish_boshqaruv_bloklash, 연결받음); return 0;
}
int 망연결하기(int fayl_deskriptor, uint32_t manzil, unsigned 접속번호) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar || satr_ma_lumotlar->TYPE_toifa != 1) return -9;
    if (satr_ma_lumotlar->Xato) return satr_ma_lumotlar->Xato;
    if (satr_ma_lumotlar->연결됨) return 0;
    if (satr_ma_lumotlar->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !manzil) return -22;
    ip_addr_t Internetdagi_manzil; ip_addr_set_ip4_u32(&Internetdagi_manzil, lwip_htonl(manzil));
    satr_ma_lumotlar->bir_rangli_manzil = manzil; satr_ma_lumotlar->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(satr_ma_lumotlar->aloqa_boshqaruv, &Internetdagi_manzil, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int fayl_deskriptor) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar || !satr_ma_lumotlar->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_toifa == 1 && 통신끝점들[순번].대기중 == fayl_deskriptor) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int fayl_deskriptor, void *ma_lumotlar, unsigned element_COUNT) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar || satr_ma_lumotlar->TYPE_toifa != 1) return -9;
    if (!element_COUNT) return 0; if (!satr_ma_lumotlar->kiritish_COUNT) return satr_ma_lumotlar->Xato ? satr_ma_lumotlar->Xato : satr_ma_lumotlar->fayl_to_xtatmoq ? 0 : -11;
    if (element_COUNT > satr_ma_lumotlar->kiritish_COUNT) element_COUNT = satr_ma_lumotlar->kiritish_COUNT;
    for (unsigned 순번 = 0; 순번 < element_COUNT; 순번++) { ((unsigned char *)ma_lumotlar)[순번] = satr_ma_lumotlar->ma_lumotlar[satr_ma_lumotlar->old_kamera_kiritish]; satr_ma_lumotlar->old_kamera_kiritish = (satr_ma_lumotlar->old_kamera_kiritish + 1) % sizeof(satr_ma_lumotlar->ma_lumotlar); }
    satr_ma_lumotlar->kiritish_COUNT -= element_COUNT; if (satr_ma_lumotlar->aloqa_boshqaruv) tcp_recved(satr_ma_lumotlar->aloqa_boshqaruv, element_COUNT); return element_COUNT;
}
int 통신쓰기(int fayl_deskriptor, const void *ma_lumotlar, unsigned element_COUNT) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar || satr_ma_lumotlar->TYPE_toifa != 1) return -9;
    if (satr_ma_lumotlar->Xato) return satr_ma_lumotlar->Xato; if (!satr_ma_lumotlar->aloqa_boshqaruv || !satr_ma_lumotlar->연결됨) return -107;
    if (!element_COUNT) return 0; if (element_COUNT > tcp_sndbuf(satr_ma_lumotlar->aloqa_boshqaruv)) element_COUNT = tcp_sndbuf(satr_ma_lumotlar->aloqa_boshqaruv);
    if (!element_COUNT) return -11; if (element_COUNT > 1024) element_COUNT = 1024;
    err_t 보조항목 = tcp_write(satr_ma_lumotlar->aloqa_boshqaruv, ma_lumotlar, element_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(satr_ma_lumotlar->aloqa_boshqaruv); return element_COUNT;
}
int 전문보내기(int fayl_deskriptor, const void *ma_lumotlar, unsigned element_COUNT, uint32_t manzil, unsigned 접속번호) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar || satr_ma_lumotlar->TYPE_toifa != 2) return -9;
    if (element_COUNT > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *ma_lumotlar_holat = pbuf_alloc(PBUF_TRANSPORT, element_COUNT, PBUF_RAM); if (!ma_lumotlar_holat) return -11;
    pbuf_take(ma_lumotlar_holat, ma_lumotlar, element_COUNT); ip_addr_t Internetdagi_manzil; ip_addr_set_ip4_u32(&Internetdagi_manzil, lwip_htonl(manzil));
    err_t 보조항목 = udp_sendto(satr_ma_lumotlar->전문제어, ma_lumotlar_holat, &Internetdagi_manzil, 접속번호); pbuf_free(ma_lumotlar_holat); return 보조항목 ? 오류번호(보조항목) : (int)element_COUNT;
}
int 전문받기(int fayl_deskriptor, void *ma_lumotlar, unsigned element_COUNT) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar || satr_ma_lumotlar->TYPE_toifa != 2) return -9;
    if (!satr_ma_lumotlar->kiritish_COUNT) return -11; unsigned 현재위치 = satr_ma_lumotlar->old_kamera_kiritish;
    if (element_COUNT > satr_ma_lumotlar->길이목록[현재위치]) element_COUNT = satr_ma_lumotlar->길이목록[현재위치]; memcpy(ma_lumotlar, satr_ma_lumotlar->ma_lumotlar + 현재위치 * 512, element_COUNT);
    satr_ma_lumotlar->상대창구번호 = satr_ma_lumotlar->접속번호들[현재위치]; satr_ma_lumotlar->bir_rangli_manzil = satr_ma_lumotlar->주소목록[현재위치]; satr_ma_lumotlar->old_kamera_kiritish = (현재위치 + 1) % 4; satr_ma_lumotlar->kiritish_COUNT--; return element_COUNT;
}
unsigned 통신접속번호(int fayl_deskriptor) { 통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); return !satr_ma_lumotlar ? 0 : satr_ma_lumotlar->aloqa_boshqaruv ? satr_ma_lumotlar->aloqa_boshqaruv->local_port : satr_ma_lumotlar->전문제어 ? satr_ma_lumotlar->전문제어->local_port : 0; }
unsigned 상대접속번호(int fayl_deskriptor) { 통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); return satr_ma_lumotlar ? satr_ma_lumotlar->상대창구번호 : 0; }
uint32_t 상대통신주소(int fayl_deskriptor) { 통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); return satr_ma_lumotlar ? satr_ma_lumotlar->bir_rangli_manzil : 0; }
void yopmoq_Tarmoq(int fayl_deskriptor) {
    통신끝점 *satr_ma_lumotlar = olish_VALUE(fayl_deskriptor); if (!satr_ma_lumotlar) return;
    if (satr_ma_lumotlar->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_toifa && 통신끝점들[순번].대기중 == fayl_deskriptor) yopmoq_Tarmoq(순번);
    if (satr_ma_lumotlar->aloqa_boshqaruv) {
        tcp_arg(satr_ma_lumotlar->aloqa_boshqaruv, 0); if (satr_ma_lumotlar->수신창구) tcp_accept(satr_ma_lumotlar->aloqa_boshqaruv, 0); else { tcp_recv(satr_ma_lumotlar->aloqa_boshqaruv, 0); tcp_err(satr_ma_lumotlar->aloqa_boshqaruv, 0); }
        if (tcp_close(satr_ma_lumotlar->aloqa_boshqaruv) != ERR_OK) tcp_abort(satr_ma_lumotlar->aloqa_boshqaruv);
    }
    if (satr_ma_lumotlar->전문제어) udp_remove(satr_ma_lumotlar->전문제어); satr_ma_lumotlar->TYPE_toifa = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&aloqa_qurilma);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (기계저장기(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned belgi_kodi = 기계저장기(보조장치 + 0x40) & 255;
        if (belgi_kodi == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *ma_lumotlar_holat = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (ma_lumotlar_holat) { 받은전문수++; RECEIVED_bayt_COUNT += 수신사용량; pbuf_take(ma_lumotlar_holat, 수신자료, 수신사용량); if (aloqa_qurilma.input(ma_lumotlar_holat, &aloqa_qurilma) != ERR_OK) { 버린전문수++; pbuf_free(ma_lumotlar_holat); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (belgi_kodi == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (belgi_kodi != 220 && belgi_kodi != 221) 수신오류 = 1; belgi_kodi = belgi_kodi == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = belgi_kodi; else 수신오류 = 1;
        }
    }
    netif_poll(&aloqa_qurilma); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (기계저장기(보조장치 + 0x54) & 0x20); 처리한도++) {
        기계저장기(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Moslamalar·조회는 lwIP의 real_ma_lumotlar 인터페이스와 to_xtatmoq_nuqta 표를 사용한다. */
uint32_t 망상태읽기(unsigned kiritish_VALUE, unsigned INDEX) {
    if(kiritish_VALUE==20)return 유선사용;
    if(kiritish_VALUE==21)return 준비됨&&netif_is_link_up(&aloqa_qurilma);
    if(kiritish_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&kiritish_VALUE>=4&&kiritish_VALUE<=8)return 유선망집계(kiritish_VALUE-4);
    if (kiritish_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&aloqa_qurilma)));
    if (kiritish_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&aloqa_qurilma)));
    if (kiritish_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&aloqa_qurilma)));
    if (kiritish_VALUE == 3) return netif_is_up(&aloqa_qurilma) != 0;
    if (kiritish_VALUE == 4) return 받은전문수;
    if (kiritish_VALUE == 5) return 보낸전문수;
    if (kiritish_VALUE == 6) return RECEIVED_bayt_COUNT;
    if (kiritish_VALUE == 7) return 보낸바이트수;
    if (kiritish_VALUE == 8) return 버린전문수;
    if (kiritish_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *to_xtatmoq_nuqta = &통신끝점들[INDEX];
    if (kiritish_VALUE == 10) return to_xtatmoq_nuqta->TYPE_toifa;
    if (!to_xtatmoq_nuqta->TYPE_toifa) return 0;
    if (kiritish_VALUE == 11) return 통신접속번호(INDEX);
    if (kiritish_VALUE == 12) return to_xtatmoq_nuqta->bir_rangli_manzil;
    if (kiritish_VALUE == 13) return to_xtatmoq_nuqta->상대창구번호;
    if (kiritish_VALUE == 14) return to_xtatmoq_nuqta->수신창구 ? 1 : to_xtatmoq_nuqta->fayl_to_xtatmoq ? 3 : to_xtatmoq_nuqta->Xato ? 4 : to_xtatmoq_nuqta->연결됨 ? 2 : 0;
    if (kiritish_VALUE == 15) return to_xtatmoq_nuqta->kiritish_COUNT;
    if (kiritish_VALUE == 16) {
        const ip_addr_t *manzil = to_xtatmoq_nuqta->TYPE_toifa == 1 && to_xtatmoq_nuqta->aloqa_boshqaruv ? &to_xtatmoq_nuqta->aloqa_boshqaruv->local_ip :
            to_xtatmoq_nuqta->TYPE_toifa == 2 && to_xtatmoq_nuqta->전문제어 ? &to_xtatmoq_nuqta->전문제어->local_ip : 0;
        return manzil ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(manzil))) : 0;
    }
    return 0;
}

int sozlamoq_Tarmoq(unsigned Amal, uint32_t manzil, uint32_t niqob_VALUE, uint32_t shluz_VALUE) {
    if (!준비됨) return -100;
    if (Amal == 1) { netif_set_up(&aloqa_qurilma); return 0; }
    if (Amal == 2) { netif_set_down(&aloqa_qurilma); return 0; }
    if (Amal != 0) return -22;
    /* 유니캐스트 IPv4, 연속 niqob_VALUE, 같은 망의 선택적 sukut_bo_yicha_qiymat shluz_VALUE. */
    uint32_t 뒤집은가림 = ~niqob_VALUE;
    if (!niqob_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !manzil || (manzil >> 24) == 127 ||
        (manzil >> 24) == 0 || (manzil >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(manzil & 뒤집은가림) || (manzil & 뒤집은가림) == 뒤집은가림)) ||
        (shluz_VALUE && ((shluz_VALUE & niqob_VALUE) != (manzil & niqob_VALUE) || shluz_VALUE == manzil || (shluz_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(shluz_VALUE & 뒤집은가림) || (shluz_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 manzil 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_toifa &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].aloqa_boshqaruv && ip_addr_isany(&통신끝점들[INDEX].aloqa_boshqaruv->local_ip))) return -16;
    if(유선사용)dhcp_stop(&aloqa_qurilma);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(manzil)); ip4_addr_set_u32(&새가림, lwip_htonl(niqob_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(shluz_VALUE));
    netif_set_addr(&aloqa_qurilma, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *to_xtatmoq_nuqta, struct pbuf *ma_lumotlar, const ip_addr_t *manzil) {
    (void)인수; (void)to_xtatmoq_nuqta;
    unsigned char 머리[20], javob_berish[16];
    if (응답상태 != -11 || ma_lumotlar->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(manzil))) != 시험주소 || pbuf_copy_partial(ma_lumotlar, 머리, 20, 0) != 20) return 0;
    unsigned Sarlavha_o_lcham = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Sarlavha_o_lcham < 20 || ma_lumotlar->tot_len < Sarlavha_o_lcham + 16 ||
        pbuf_copy_partial(ma_lumotlar, javob_berish, 16, Sarlavha_o_lcham) != 16 || javob_berish[0] || javob_berish[1] ||
        (((unsigned)javob_berish[4] << 8) | javob_berish[5]) != 시험식별자 ||
        (((unsigned)javob_berish[6] << 8) | javob_berish[7]) != 시험순서 ||
        javob_berish[8] != 'J' || javob_berish[9] != 'K' || javob_berish[10] != 'O' || javob_berish[11] != 'S' ||
        (((uint32_t)javob_berish[12] << 24) | ((uint32_t)javob_berish[13] << 16) | ((uint32_t)javob_berish[14] << 8) | javob_berish[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(ma_lumotlar, Sarlavha_o_lcham)) return 0;
    if (inet_chksum_pbuf(ma_lumotlar)) { pbuf_add_header(ma_lumotlar, Sarlavha_o_lcham); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(ma_lumotlar); return 1;
}
int 응답시험시작(uint32_t manzil, unsigned tartib_VALUE) {
    if (!준비됨 || !netif_is_up(&aloqa_qurilma)) return -100;
    if (!manzil || (manzil >> 28) >= 14 || manzil == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = manzil; 시험순서 = tartib_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char ma_lumotlar[32] = {8,0,0,0};
    ma_lumotlar[4] = 시험식별자 >> 8; ma_lumotlar[5] = 시험식별자; ma_lumotlar[6] = 시험순서 >> 8; ma_lumotlar[7] = 시험순서;
    ma_lumotlar[8]='J'; ma_lumotlar[9]='K'; ma_lumotlar[10]='O'; ma_lumotlar[11]='S';
    ma_lumotlar[12]=시험시각 >> 24; ma_lumotlar[13]=시험시각 >> 16; ma_lumotlar[14]=시험시각 >> 8; ma_lumotlar[15]=시험시각;
    for (unsigned holat_INDEX = 16; holat_INDEX < sizeof(ma_lumotlar); holat_INDEX++) ma_lumotlar[holat_INDEX] = holat_INDEX;
    uint16_t 확인합 = inet_chksum(ma_lumotlar, sizeof(ma_lumotlar)); memcpy(ma_lumotlar + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(ma_lumotlar), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, ma_lumotlar, sizeof(ma_lumotlar)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(manzil));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned kiritish_VALUE) {
    통신망살피기();
    return kiritish_VALUE == 0 ? 응답상태 : kiritish_VALUE == 1 ? (int)응답시간 : kiritish_VALUE == 2 ? (int)응답차례 : -22;
}
