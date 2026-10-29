#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "통신망.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../원격/원격.h"
#include "akaaulejuushi_kusu.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif epe_ipajia_serulaalü;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int 유형, 수신창구, 대기중, 연결됨, anaajaalaa_ajattiraa, ajachitia;
    struct tcp_pcb *epe_ipajia_aa_inmajia;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char atijaaya[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], wanaawasü_ejepüsee;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int anaajaalaa_aapaaya) { return anaajaalaa_aapaaya >= 0 && anaajaalaa_aapaaya < 32 && 통신끝점들[anaajaalaa_aapaaya].유형 ? &통신끝점들[anaajaalaa_aapaaya] : 0; }
static int 예약하기(int 유형) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].유형) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].유형 = 유형; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned 문자값) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = 문자값; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *ejepüsee) {
    (void)개수; (void)ejepüsee;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned 문자값 = ((unsigned char *)다음위치->payload)[순번];
        if (문자값 == 192 || 문자값 == 219) { 내보내기(219); 내보내기(문자값 == 192 ? 220 : 221); } else 내보내기(문자값);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t 준비하기(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void 통신망준비(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    기계저장기(보조장치 + 4) |= 1; 기계저장기(보조장치 + 0x60) = 0; 기계저장기(보조장치 + 0x44) = 0;
    기계저장기(보조장치 + 0x48) = 0xc6; 기계저장기(보조장치 + 0x4c) = 3; 기계저장기(보조장치 + 0x68) = 270; 기계저장기(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t ejepüsee_Internet, wiitü_o_upünaa_utajana, miicho_u_a_ttaalee_ejepüsee;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&ejepüsee_Internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&wiitü_o_upünaa_utajana, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&miicho_u_a_ttaalee_ejepüsee, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&epe_ipajia_serulaalü, &ejepüsee_Internet, &wiitü_o_upünaa_utajana, &miicho_u_a_ttaalee_ejepüsee, 0, 유선사용?유선망준비:준비하기, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&epe_ipajia_serulaalü); netif_set_up(&epe_ipajia_serulaalü);if(!유선사용)netif_set_link_up(&epe_ipajia_serulaalü); 준비됨 = 1;
    원격준비();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *자료위치, err_t ajachitia) {
    통신끝점 *kaleena_atijaaya = 부가인수; (void)통신제어블록; (void)ajachitia;
    if (!자료위치) { kaleena_atijaaya->anaajaalaa_ajattiraa = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(kaleena_atijaaya->atijaaya) - kaleena_atijaaya->항목수) return ERR_MEM;
    unsigned 현재위치 = (kaleena_atijaaya->맨앞 + kaleena_atijaaya->항목수) % sizeof(kaleena_atijaaya->atijaaya);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        kaleena_atijaaya->atijaaya[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(kaleena_atijaaya->atijaaya);
    }
    kaleena_atijaaya->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t ajachitia) { 통신끝점 *kaleena_atijaaya = 부가인수; kaleena_atijaaya->epe_ipajia_aa_inmajia = 0; kaleena_atijaaya->ajachitia = 오류번호(ajachitia); }
static void 되부름목록(통신끝점 *kaleena_atijaaya) { tcp_arg(kaleena_atijaaya->epe_ipajia_aa_inmajia, kaleena_atijaaya); tcp_recv(kaleena_atijaaya->epe_ipajia_aa_inmajia, 수신됨); tcp_err(kaleena_atijaaya->epe_ipajia_aa_inmajia, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t ajachitia) {
    통신끝점 *kaleena_atijaaya = 부가인수; (void)통신제어블록; if (ajachitia) kaleena_atijaaya->ajachitia = 오류번호(ajachitia); else kaleena_atijaaya->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t ajachitia) {
    통신끝점 *부모항목 = 부가인수; if (ajachitia) return ajachitia;
    int anaajaalaa_aapaaya = 예약하기(1); if (anaajaalaa_aapaaya < 0) return ERR_MEM;
    통신끝점 *kaleena_atijaaya = &통신끝점들[anaajaalaa_aapaaya]; kaleena_atijaaya->epe_ipajia_aa_inmajia = 통신제어블록; kaleena_atijaaya->연결됨 = 1; kaleena_atijaaya->대기중 = (int)(부모항목 - 통신끝점들);
    kaleena_atijaaya->wanaawasü_ejepüsee = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); kaleena_atijaaya->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(kaleena_atijaaya); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *자료위치, const ip_addr_t *ejepüsee, u16_t 접속번호) {
    통신끝점 *kaleena_atijaaya = 부가인수; (void)통신제어블록;
    if (kaleena_atijaaya->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (kaleena_atijaaya->맨앞 + kaleena_atijaaya->항목수) % 4;
        pbuf_copy_partial(자료위치, kaleena_atijaaya->atijaaya + 자리 * 512, 자료위치->tot_len, 0);
        kaleena_atijaaya->길이목록[자리] = 자료위치->tot_len; kaleena_atijaaya->접속번호들[자리] = 접속번호;
        kaleena_atijaaya->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ejepüsee))); kaleena_atijaaya->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int 유형) {
    if (!준비됨) return -100;
    if (유형 != 1 && 유형 != 2) return -93;
    int anaajaalaa_aapaaya = 예약하기(유형); if (anaajaalaa_aapaaya < 0) return anaajaalaa_aapaaya;
    통신끝점 *kaleena_atijaaya = &통신끝점들[anaajaalaa_aapaaya];
    if (유형 == 1) { kaleena_atijaaya->epe_ipajia_aa_inmajia = tcp_new(); if (kaleena_atijaaya->epe_ipajia_aa_inmajia) 되부름목록(kaleena_atijaaya); }
    else { kaleena_atijaaya->전문제어 = udp_new(); if (kaleena_atijaaya->전문제어) udp_recv(kaleena_atijaaya->전문제어, 전문, kaleena_atijaaya); }
    if (!kaleena_atijaaya->epe_ipajia_aa_inmajia && !kaleena_atijaaya->전문제어) { kaleena_atijaaya->유형 = 0; return -12; } return anaajaalaa_aapaaya;
}
int 망주소묶기(int anaajaalaa_aapaaya, uint32_t ejepüsee, unsigned 접속번호) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya) return -9;
    if (접속번호 > 65535 || (ejepüsee && ejepüsee != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&epe_ipajia_serulaalü))) && ejepüsee != 0x7f000001)) return -99;
    ip_addr_t ejepüsee_Internet; ip_addr_set_ip4_u32(&ejepüsee_Internet, lwip_htonl(ejepüsee));
    err_t 보조항목 = kaleena_atijaaya->유형 == 1 ? tcp_bind(kaleena_atijaaya->epe_ipajia_aa_inmajia, &ejepüsee_Internet, 접속번호) : udp_bind(kaleena_atijaaya->전문제어, &ejepüsee_Internet, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int anaajaalaa_aapaaya) { 통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (kaleena_atijaaya && kaleena_atijaaya->epe_ipajia_aa_inmajia) ip_set_option(kaleena_atijaaya->epe_ipajia_aa_inmajia, SOF_REUSEADDR); }
int 연결기다리기(int anaajaalaa_aapaaya) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya || kaleena_atijaaya->유형 != 1) return -9;
    if (kaleena_atijaaya->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(kaleena_atijaaya->epe_ipajia_aa_inmajia, 4, &보조항목);
    if (!통신제어블록) return 오류번호(보조항목); kaleena_atijaaya->epe_ipajia_aa_inmajia = 통신제어블록; kaleena_atijaaya->수신창구 = 1; tcp_arg(통신제어블록, kaleena_atijaaya); tcp_accept(통신제어블록, 연결받음); return 0;
}
int 망연결하기(int anaajaalaa_aapaaya, uint32_t ejepüsee, unsigned 접속번호) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya || kaleena_atijaaya->유형 != 1) return -9;
    if (kaleena_atijaaya->ajachitia) return kaleena_atijaaya->ajachitia;
    if (kaleena_atijaaya->연결됨) return 0;
    if (kaleena_atijaaya->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !ejepüsee) return -22;
    ip_addr_t ejepüsee_Internet; ip_addr_set_ip4_u32(&ejepüsee_Internet, lwip_htonl(ejepüsee));
    kaleena_atijaaya->wanaawasü_ejepüsee = ejepüsee; kaleena_atijaaya->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(kaleena_atijaaya->epe_ipajia_aa_inmajia, &ejepüsee_Internet, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int anaajaalaa_aapaaya) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya || !kaleena_atijaaya->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].유형 == 1 && 통신끝점들[순번].대기중 == anaajaalaa_aapaaya) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int anaajaalaa_aapaaya, void *atijaaya, unsigned 개수) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya || kaleena_atijaaya->유형 != 1) return -9;
    if (!개수) return 0; if (!kaleena_atijaaya->항목수) return kaleena_atijaaya->ajachitia ? kaleena_atijaaya->ajachitia : kaleena_atijaaya->anaajaalaa_ajattiraa ? 0 : -11;
    if (개수 > kaleena_atijaaya->항목수) 개수 = kaleena_atijaaya->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)atijaaya)[순번] = kaleena_atijaaya->atijaaya[kaleena_atijaaya->맨앞]; kaleena_atijaaya->맨앞 = (kaleena_atijaaya->맨앞 + 1) % sizeof(kaleena_atijaaya->atijaaya); }
    kaleena_atijaaya->항목수 -= 개수; if (kaleena_atijaaya->epe_ipajia_aa_inmajia) tcp_recved(kaleena_atijaaya->epe_ipajia_aa_inmajia, 개수); return 개수;
}
int 통신쓰기(int anaajaalaa_aapaaya, const void *atijaaya, unsigned 개수) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya || kaleena_atijaaya->유형 != 1) return -9;
    if (kaleena_atijaaya->ajachitia) return kaleena_atijaaya->ajachitia; if (!kaleena_atijaaya->epe_ipajia_aa_inmajia || !kaleena_atijaaya->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(kaleena_atijaaya->epe_ipajia_aa_inmajia)) 개수 = tcp_sndbuf(kaleena_atijaaya->epe_ipajia_aa_inmajia);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(kaleena_atijaaya->epe_ipajia_aa_inmajia, atijaaya, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(kaleena_atijaaya->epe_ipajia_aa_inmajia); return 개수;
}
int 전문보내기(int anaajaalaa_aapaaya, const void *atijaaya, unsigned 개수, uint32_t ejepüsee, unsigned 접속번호) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya || kaleena_atijaaya->유형 != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, atijaaya, 개수); ip_addr_t ejepüsee_Internet; ip_addr_set_ip4_u32(&ejepüsee_Internet, lwip_htonl(ejepüsee));
    err_t 보조항목 = udp_sendto(kaleena_atijaaya->전문제어, 자료위치, &ejepüsee_Internet, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int anaajaalaa_aapaaya, void *atijaaya, unsigned 개수) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya || kaleena_atijaaya->유형 != 2) return -9;
    if (!kaleena_atijaaya->항목수) return -11; unsigned 현재위치 = kaleena_atijaaya->맨앞;
    if (개수 > kaleena_atijaaya->길이목록[현재위치]) 개수 = kaleena_atijaaya->길이목록[현재위치]; memcpy(atijaaya, kaleena_atijaaya->atijaaya + 현재위치 * 512, 개수);
    kaleena_atijaaya->상대창구번호 = kaleena_atijaaya->접속번호들[현재위치]; kaleena_atijaaya->wanaawasü_ejepüsee = kaleena_atijaaya->주소목록[현재위치]; kaleena_atijaaya->맨앞 = (현재위치 + 1) % 4; kaleena_atijaaya->항목수--; return 개수;
}
unsigned 통신접속번호(int anaajaalaa_aapaaya) { 통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); return !kaleena_atijaaya ? 0 : kaleena_atijaaya->epe_ipajia_aa_inmajia ? kaleena_atijaaya->epe_ipajia_aa_inmajia->local_port : kaleena_atijaaya->전문제어 ? kaleena_atijaaya->전문제어->local_port : 0; }
unsigned 상대접속번호(int anaajaalaa_aapaaya) { 통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); return kaleena_atijaaya ? kaleena_atijaaya->상대창구번호 : 0; }
uint32_t 상대통신주소(int anaajaalaa_aapaaya) { 통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); return kaleena_atijaaya ? kaleena_atijaaya->wanaawasü_ejepüsee : 0; }
void asürülaa_kusu(int anaajaalaa_aapaaya) {
    통신끝점 *kaleena_atijaaya = 얻기(anaajaalaa_aapaaya); if (!kaleena_atijaaya) return;
    if (kaleena_atijaaya->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].유형 && 통신끝점들[순번].대기중 == anaajaalaa_aapaaya) asürülaa_kusu(순번);
    if (kaleena_atijaaya->epe_ipajia_aa_inmajia) {
        tcp_arg(kaleena_atijaaya->epe_ipajia_aa_inmajia, 0); if (kaleena_atijaaya->수신창구) tcp_accept(kaleena_atijaaya->epe_ipajia_aa_inmajia, 0); else { tcp_recv(kaleena_atijaaya->epe_ipajia_aa_inmajia, 0); tcp_err(kaleena_atijaaya->epe_ipajia_aa_inmajia, 0); }
        if (tcp_close(kaleena_atijaaya->epe_ipajia_aa_inmajia) != ERR_OK) tcp_abort(kaleena_atijaaya->epe_ipajia_aa_inmajia);
    }
    if (kaleena_atijaaya->전문제어) udp_remove(kaleena_atijaaya->전문제어); kaleena_atijaaya->유형 = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&epe_ipajia_serulaalü);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (기계저장기(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned 문자값 = 기계저장기(보조장치 + 0x40) & 255;
        if (문자값 == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (epe_ipajia_serulaalü.input(자료위치, &epe_ipajia_serulaalü) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (문자값 == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (문자값 != 220 && 문자값 != 221) 수신오류 = 1; 문자값 = 문자값 == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = 문자값; else 수신오류 = 1;
        }
    }
    netif_poll(&epe_ipajia_serulaalü); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (기계저장기(보조장치 + 0x54) & 0x20); 처리한도++) {
        기계저장기(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* 설정·조회는 lwIP의 실제 인터페이스와 ajattiraa_o_uchikanain 표를 사용한다. */
uint32_t 망상태읽기(unsigned ekeroliaa_ajutuu, unsigned ee_iyatialujuna) {
    if(ekeroliaa_ajutuu==20)return 유선사용;
    if(ekeroliaa_ajutuu==21)return 준비됨&&netif_is_link_up(&epe_ipajia_serulaalü);
    if(ekeroliaa_ajutuu==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&ekeroliaa_ajutuu>=4&&ekeroliaa_ajutuu<=8)return 유선망집계(ekeroliaa_ajutuu-4);
    if (ekeroliaa_ajutuu == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&epe_ipajia_serulaalü)));
    if (ekeroliaa_ajutuu == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&epe_ipajia_serulaalü)));
    if (ekeroliaa_ajutuu == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&epe_ipajia_serulaalü)));
    if (ekeroliaa_ajutuu == 3) return netif_is_up(&epe_ipajia_serulaalü) != 0;
    if (ekeroliaa_ajutuu == 4) return 받은전문수;
    if (ekeroliaa_ajutuu == 5) return 보낸전문수;
    if (ekeroliaa_ajutuu == 6) return 받은바이트수;
    if (ekeroliaa_ajutuu == 7) return 보낸바이트수;
    if (ekeroliaa_ajutuu == 8) return 버린전문수;
    if (ekeroliaa_ajutuu == 9) return 송신개수;
    if (ee_iyatialujuna >= 32) return 0;
    통신끝점 *ajattiraa_o_uchikanain = &통신끝점들[ee_iyatialujuna];
    if (ekeroliaa_ajutuu == 10) return ajattiraa_o_uchikanain->유형;
    if (!ajattiraa_o_uchikanain->유형) return 0;
    if (ekeroliaa_ajutuu == 11) return 통신접속번호(ee_iyatialujuna);
    if (ekeroliaa_ajutuu == 12) return ajattiraa_o_uchikanain->wanaawasü_ejepüsee;
    if (ekeroliaa_ajutuu == 13) return ajattiraa_o_uchikanain->상대창구번호;
    if (ekeroliaa_ajutuu == 14) return ajattiraa_o_uchikanain->수신창구 ? 1 : ajattiraa_o_uchikanain->anaajaalaa_ajattiraa ? 3 : ajattiraa_o_uchikanain->ajachitia ? 4 : ajattiraa_o_uchikanain->연결됨 ? 2 : 0;
    if (ekeroliaa_ajutuu == 15) return ajattiraa_o_uchikanain->항목수;
    if (ekeroliaa_ajutuu == 16) {
        const ip_addr_t *ejepüsee = ajattiraa_o_uchikanain->유형 == 1 && ajattiraa_o_uchikanain->epe_ipajia_aa_inmajia ? &ajattiraa_o_uchikanain->epe_ipajia_aa_inmajia->local_ip :
            ajattiraa_o_uchikanain->유형 == 2 && ajattiraa_o_uchikanain->전문제어 ? &ajattiraa_o_uchikanain->전문제어->local_ip : 0;
        return ejepüsee ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ejepüsee))) : 0;
    }
    return 0;
}

int anaatiraa_kusu(unsigned aa_inra_awai, uint32_t ejepüsee, uint32_t o_upünaa_utajana_ajutuu, uint32_t miicho_u_a_ttaalee_ajutuu) {
    if (!준비됨) return -100;
    if (aa_inra_awai == 1) { netif_set_up(&epe_ipajia_serulaalü); return 0; }
    if (aa_inra_awai == 2) { netif_set_down(&epe_ipajia_serulaalü); return 0; }
    if (aa_inra_awai != 0) return -22;
    /* 유니캐스트 IPv4, 연속 o_upünaa_utajana_ajutuu, 같은 망의 선택적 ajutuu_aneekuushitüjülia miicho_u_a_ttaalee_ajutuu. */
    uint32_t 뒤집은가림 = ~o_upünaa_utajana_ajutuu;
    if (!o_upünaa_utajana_ajutuu || (뒤집은가림 & (뒤집은가림 + 1)) || !ejepüsee || (ejepüsee >> 24) == 127 ||
        (ejepüsee >> 24) == 0 || (ejepüsee >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ejepüsee & 뒤집은가림) || (ejepüsee & 뒤집은가림) == 뒤집은가림)) ||
        (miicho_u_a_ttaalee_ajutuu && ((miicho_u_a_ttaalee_ajutuu & o_upünaa_utajana_ajutuu) != (ejepüsee & o_upünaa_utajana_ajutuu) || miicho_u_a_ttaalee_ajutuu == ejepüsee || (miicho_u_a_ttaalee_ajutuu >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(miicho_u_a_ttaalee_ajutuu & 뒤집은가림) || (miicho_u_a_ttaalee_ajutuu & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ejepüsee 변경으로 몰래 끊지 않는다. */
    for (unsigned ee_iyatialujuna = 0; ee_iyatialujuna < 32; ee_iyatialujuna++) if (통신끝점들[ee_iyatialujuna].유형 &&
        !(통신끝점들[ee_iyatialujuna].수신창구 && 통신끝점들[ee_iyatialujuna].epe_ipajia_aa_inmajia && ip_addr_isany(&통신끝점들[ee_iyatialujuna].epe_ipajia_aa_inmajia->local_ip))) return -16;
    if(유선사용)dhcp_stop(&epe_ipajia_serulaalü);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ejepüsee)); ip4_addr_set_u32(&새가림, lwip_htonl(o_upünaa_utajana_ajutuu)); ip4_addr_set_u32(&새관문, lwip_htonl(miicho_u_a_ttaalee_ajutuu));
    netif_set_addr(&epe_ipajia_serulaalü, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *ajattiraa_o_uchikanain, struct pbuf *atijaaya, const ip_addr_t *ejepüsee) {
    (void)인수; (void)ajattiraa_o_uchikanain;
    unsigned char 머리[20], 응답[16];
    if (응답상태 != -11 || atijaaya->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ejepüsee))) != 시험주소 || pbuf_copy_partial(atijaaya, 머리, 20, 0) != 20) return 0;
    unsigned 머리크기 = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || 머리크기 < 20 || atijaaya->tot_len < 머리크기 + 16 ||
        pbuf_copy_partial(atijaaya, 응답, 16, 머리크기) != 16 || 응답[0] || 응답[1] ||
        (((unsigned)응답[4] << 8) | 응답[5]) != 시험식별자 ||
        (((unsigned)응답[6] << 8) | 응답[7]) != 시험순서 ||
        응답[8] != 'J' || 응답[9] != 'K' || 응답[10] != 'O' || 응답[11] != 'S' ||
        (((uint32_t)응답[12] << 24) | ((uint32_t)응답[13] << 16) | ((uint32_t)응답[14] << 8) | 응답[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(atijaaya, 머리크기)) return 0;
    if (inet_chksum_pbuf(atijaaya)) { pbuf_add_header(atijaaya, 머리크기); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(atijaaya); return 1;
}
int 응답시험시작(uint32_t ejepüsee, unsigned anaajiaakua_ipa_ajutuu) {
    if (!준비됨 || !netif_is_up(&epe_ipajia_serulaalü)) return -100;
    if (!ejepüsee || (ejepüsee >> 28) >= 14 || ejepüsee == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ejepüsee; 시험순서 = anaajiaakua_ipa_ajutuu & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char atijaaya[32] = {8,0,0,0};
    atijaaya[4] = 시험식별자 >> 8; atijaaya[5] = 시험식별자; atijaaya[6] = 시험순서 >> 8; atijaaya[7] = 시험순서;
    atijaaya[8]='J'; atijaaya[9]='K'; atijaaya[10]='O'; atijaaya[11]='S';
    atijaaya[12]=시험시각 >> 24; atijaaya[13]=시험시각 >> 16; atijaaya[14]=시험시각 >> 8; atijaaya[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(atijaaya); 자리++) atijaaya[자리] = 자리;
    uint16_t 확인합 = inet_chksum(atijaaya, sizeof(atijaaya)); memcpy(atijaaya + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(atijaaya), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, atijaaya, sizeof(atijaaya)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ejepüsee));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned ekeroliaa_ajutuu) {
    통신망살피기();
    return ekeroliaa_ajutuu == 0 ? 응답상태 : ekeroliaa_ajutuu == 1 ? (int)응답시간 : ekeroliaa_ajutuu == 2 ? (int)응답차례 : -22;
}
