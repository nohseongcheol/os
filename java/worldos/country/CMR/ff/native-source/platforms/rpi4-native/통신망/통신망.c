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
#include "유선망.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif ceŋondiral_kaɓirgal;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int 유형, 수신창구, 대기중, 연결됨, fiilde_taƴde, juumre;
    struct tcp_pcb *ceŋondiral_yuurnitorde;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char keɓe[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], giƴiraaɗo_ñiiɓirde;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int fiilde_jaggoode) { return fiilde_jaggoode >= 0 && fiilde_jaggoode < 32 && 통신끝점들[fiilde_jaggoode].유형 ? &통신끝점들[fiilde_jaggoode] : 0; }
static int 예약하기(int 유형) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].유형) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].유형 = 유형; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned 문자값) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = 문자값; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *ñiiɓirde) {
    (void)개수; (void)ñiiɓirde;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned 문자값 = ((unsigned char *)다음위치->payload)[순번];
        if (문자값 == 192 || 문자값 == 219) { 내보내기(219); 내보내기(문자값 == 192 ? 220 : 221); } else 내보내기(문자값);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t 준비하기(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Heblu_laylaytol(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    기계저장기(보조장치 + 4) |= 1; 기계저장기(보조장치 + 0x60) = 0; 기계저장기(보조장치 + 0x44) = 0;
    기계저장기(보조장치 + 0x48) = 0xc6; 기계저장기(보조장치 + 0x4c) = 3; 기계저장기(보조장치 + 0x68) = 270; 기계저장기(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t ñiiɓirde_enternet, 가림값, 관문주소;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&ñiiɓirde_enternet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&가림값, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&관문주소, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&ceŋondiral_kaɓirgal, &ñiiɓirde_enternet, &가림값, &관문주소, 0, 유선사용?유선망준비:준비하기, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&ceŋondiral_kaɓirgal); netif_set_up(&ceŋondiral_kaɓirgal);if(!유선사용)netif_set_link_up(&ceŋondiral_kaɓirgal); 준비됨 = 1;
    원격준비();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *자료위치, err_t juumre) {
    통신끝점 *ɓoggol_keɓe = 부가인수; (void)통신제어블록; (void)juumre;
    if (!자료위치) { ɓoggol_keɓe->fiilde_taƴde = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(ɓoggol_keɓe->keɓe) - ɓoggol_keɓe->항목수) return ERR_MEM;
    unsigned 현재위치 = (ɓoggol_keɓe->맨앞 + ɓoggol_keɓe->항목수) % sizeof(ɓoggol_keɓe->keɓe);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        ɓoggol_keɓe->keɓe[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(ɓoggol_keɓe->keɓe);
    }
    ɓoggol_keɓe->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t juumre) { 통신끝점 *ɓoggol_keɓe = 부가인수; ɓoggol_keɓe->ceŋondiral_yuurnitorde = 0; ɓoggol_keɓe->juumre = 오류번호(juumre); }
static void 되부름목록(통신끝점 *ɓoggol_keɓe) { tcp_arg(ɓoggol_keɓe->ceŋondiral_yuurnitorde, ɓoggol_keɓe); tcp_recv(ɓoggol_keɓe->ceŋondiral_yuurnitorde, 수신됨); tcp_err(ɓoggol_keɓe->ceŋondiral_yuurnitorde, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t juumre) {
    통신끝점 *ɓoggol_keɓe = 부가인수; (void)통신제어블록; if (juumre) ɓoggol_keɓe->juumre = 오류번호(juumre); else ɓoggol_keɓe->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t juumre) {
    통신끝점 *부모항목 = 부가인수; if (juumre) return juumre;
    int fiilde_jaggoode = 예약하기(1); if (fiilde_jaggoode < 0) return ERR_MEM;
    통신끝점 *ɓoggol_keɓe = &통신끝점들[fiilde_jaggoode]; ɓoggol_keɓe->ceŋondiral_yuurnitorde = 통신제어블록; ɓoggol_keɓe->연결됨 = 1; ɓoggol_keɓe->대기중 = (int)(부모항목 - 통신끝점들);
    ɓoggol_keɓe->giƴiraaɗo_ñiiɓirde = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); ɓoggol_keɓe->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(ɓoggol_keɓe); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *자료위치, const ip_addr_t *ñiiɓirde, u16_t 접속번호) {
    통신끝점 *ɓoggol_keɓe = 부가인수; (void)통신제어블록;
    if (ɓoggol_keɓe->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (ɓoggol_keɓe->맨앞 + ɓoggol_keɓe->항목수) % 4;
        pbuf_copy_partial(자료위치, ɓoggol_keɓe->keɓe + 자리 * 512, 자료위치->tot_len, 0);
        ɓoggol_keɓe->길이목록[자리] = 자료위치->tot_len; ɓoggol_keɓe->접속번호들[자리] = 접속번호;
        ɓoggol_keɓe->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ñiiɓirde))); ɓoggol_keɓe->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int 유형) {
    if (!준비됨) return -100;
    if (유형 != 1 && 유형 != 2) return -93;
    int fiilde_jaggoode = 예약하기(유형); if (fiilde_jaggoode < 0) return fiilde_jaggoode;
    통신끝점 *ɓoggol_keɓe = &통신끝점들[fiilde_jaggoode];
    if (유형 == 1) { ɓoggol_keɓe->ceŋondiral_yuurnitorde = tcp_new(); if (ɓoggol_keɓe->ceŋondiral_yuurnitorde) 되부름목록(ɓoggol_keɓe); }
    else { ɓoggol_keɓe->전문제어 = udp_new(); if (ɓoggol_keɓe->전문제어) udp_recv(ɓoggol_keɓe->전문제어, 전문, ɓoggol_keɓe); }
    if (!ɓoggol_keɓe->ceŋondiral_yuurnitorde && !ɓoggol_keɓe->전문제어) { ɓoggol_keɓe->유형 = 0; return -12; } return fiilde_jaggoode;
}
int 망주소묶기(int fiilde_jaggoode, uint32_t ñiiɓirde, unsigned 접속번호) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe) return -9;
    if (접속번호 > 65535 || (ñiiɓirde && ñiiɓirde != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ceŋondiral_kaɓirgal))) && ñiiɓirde != 0x7f000001)) return -99;
    ip_addr_t ñiiɓirde_enternet; ip_addr_set_ip4_u32(&ñiiɓirde_enternet, lwip_htonl(ñiiɓirde));
    err_t 보조항목 = ɓoggol_keɓe->유형 == 1 ? tcp_bind(ɓoggol_keɓe->ceŋondiral_yuurnitorde, &ñiiɓirde_enternet, 접속번호) : udp_bind(ɓoggol_keɓe->전문제어, &ñiiɓirde_enternet, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int fiilde_jaggoode) { 통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (ɓoggol_keɓe && ɓoggol_keɓe->ceŋondiral_yuurnitorde) ip_set_option(ɓoggol_keɓe->ceŋondiral_yuurnitorde, SOF_REUSEADDR); }
int 연결기다리기(int fiilde_jaggoode) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe || ɓoggol_keɓe->유형 != 1) return -9;
    if (ɓoggol_keɓe->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(ɓoggol_keɓe->ceŋondiral_yuurnitorde, 4, &보조항목);
    if (!통신제어블록) return 오류번호(보조항목); ɓoggol_keɓe->ceŋondiral_yuurnitorde = 통신제어블록; ɓoggol_keɓe->수신창구 = 1; tcp_arg(통신제어블록, ɓoggol_keɓe); tcp_accept(통신제어블록, 연결받음); return 0;
}
int 망연결하기(int fiilde_jaggoode, uint32_t ñiiɓirde, unsigned 접속번호) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe || ɓoggol_keɓe->유형 != 1) return -9;
    if (ɓoggol_keɓe->juumre) return ɓoggol_keɓe->juumre;
    if (ɓoggol_keɓe->연결됨) return 0;
    if (ɓoggol_keɓe->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !ñiiɓirde) return -22;
    ip_addr_t ñiiɓirde_enternet; ip_addr_set_ip4_u32(&ñiiɓirde_enternet, lwip_htonl(ñiiɓirde));
    ɓoggol_keɓe->giƴiraaɗo_ñiiɓirde = ñiiɓirde; ɓoggol_keɓe->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(ɓoggol_keɓe->ceŋondiral_yuurnitorde, &ñiiɓirde_enternet, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int fiilde_jaggoode) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe || !ɓoggol_keɓe->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].유형 == 1 && 통신끝점들[순번].대기중 == fiilde_jaggoode) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int fiilde_jaggoode, void *keɓe, unsigned 개수) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe || ɓoggol_keɓe->유형 != 1) return -9;
    if (!개수) return 0; if (!ɓoggol_keɓe->항목수) return ɓoggol_keɓe->juumre ? ɓoggol_keɓe->juumre : ɓoggol_keɓe->fiilde_taƴde ? 0 : -11;
    if (개수 > ɓoggol_keɓe->항목수) 개수 = ɓoggol_keɓe->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)keɓe)[순번] = ɓoggol_keɓe->keɓe[ɓoggol_keɓe->맨앞]; ɓoggol_keɓe->맨앞 = (ɓoggol_keɓe->맨앞 + 1) % sizeof(ɓoggol_keɓe->keɓe); }
    ɓoggol_keɓe->항목수 -= 개수; if (ɓoggol_keɓe->ceŋondiral_yuurnitorde) tcp_recved(ɓoggol_keɓe->ceŋondiral_yuurnitorde, 개수); return 개수;
}
int 통신쓰기(int fiilde_jaggoode, const void *keɓe, unsigned 개수) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe || ɓoggol_keɓe->유형 != 1) return -9;
    if (ɓoggol_keɓe->juumre) return ɓoggol_keɓe->juumre; if (!ɓoggol_keɓe->ceŋondiral_yuurnitorde || !ɓoggol_keɓe->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(ɓoggol_keɓe->ceŋondiral_yuurnitorde)) 개수 = tcp_sndbuf(ɓoggol_keɓe->ceŋondiral_yuurnitorde);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(ɓoggol_keɓe->ceŋondiral_yuurnitorde, keɓe, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(ɓoggol_keɓe->ceŋondiral_yuurnitorde); return 개수;
}
int 전문보내기(int fiilde_jaggoode, const void *keɓe, unsigned 개수, uint32_t ñiiɓirde, unsigned 접속번호) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe || ɓoggol_keɓe->유형 != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, keɓe, 개수); ip_addr_t ñiiɓirde_enternet; ip_addr_set_ip4_u32(&ñiiɓirde_enternet, lwip_htonl(ñiiɓirde));
    err_t 보조항목 = udp_sendto(ɓoggol_keɓe->전문제어, 자료위치, &ñiiɓirde_enternet, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int fiilde_jaggoode, void *keɓe, unsigned 개수) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe || ɓoggol_keɓe->유형 != 2) return -9;
    if (!ɓoggol_keɓe->항목수) return -11; unsigned 현재위치 = ɓoggol_keɓe->맨앞;
    if (개수 > ɓoggol_keɓe->길이목록[현재위치]) 개수 = ɓoggol_keɓe->길이목록[현재위치]; memcpy(keɓe, ɓoggol_keɓe->keɓe + 현재위치 * 512, 개수);
    ɓoggol_keɓe->상대창구번호 = ɓoggol_keɓe->접속번호들[현재위치]; ɓoggol_keɓe->giƴiraaɗo_ñiiɓirde = ɓoggol_keɓe->주소목록[현재위치]; ɓoggol_keɓe->맨앞 = (현재위치 + 1) % 4; ɓoggol_keɓe->항목수--; return 개수;
}
unsigned 통신접속번호(int fiilde_jaggoode) { 통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); return !ɓoggol_keɓe ? 0 : ɓoggol_keɓe->ceŋondiral_yuurnitorde ? ɓoggol_keɓe->ceŋondiral_yuurnitorde->local_port : ɓoggol_keɓe->전문제어 ? ɓoggol_keɓe->전문제어->local_port : 0; }
unsigned 상대접속번호(int fiilde_jaggoode) { 통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); return ɓoggol_keɓe ? ɓoggol_keɓe->상대창구번호 : 0; }
uint32_t 상대통신주소(int fiilde_jaggoode) { 통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); return ɓoggol_keɓe ? ɓoggol_keɓe->giƴiraaɗo_ñiiɓirde : 0; }
void uddude_laylaytol(int fiilde_jaggoode) {
    통신끝점 *ɓoggol_keɓe = 얻기(fiilde_jaggoode); if (!ɓoggol_keɓe) return;
    if (ɓoggol_keɓe->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].유형 && 통신끝점들[순번].대기중 == fiilde_jaggoode) uddude_laylaytol(순번);
    if (ɓoggol_keɓe->ceŋondiral_yuurnitorde) {
        tcp_arg(ɓoggol_keɓe->ceŋondiral_yuurnitorde, 0); if (ɓoggol_keɓe->수신창구) tcp_accept(ɓoggol_keɓe->ceŋondiral_yuurnitorde, 0); else { tcp_recv(ɓoggol_keɓe->ceŋondiral_yuurnitorde, 0); tcp_err(ɓoggol_keɓe->ceŋondiral_yuurnitorde, 0); }
        if (tcp_close(ɓoggol_keɓe->ceŋondiral_yuurnitorde) != ERR_OK) tcp_abort(ɓoggol_keɓe->ceŋondiral_yuurnitorde);
    }
    if (ɓoggol_keɓe->전문제어) udp_remove(ɓoggol_keɓe->전문제어); ɓoggol_keɓe->유형 = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&ceŋondiral_kaɓirgal);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (기계저장기(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned 문자값 = 기계저장기(보조장치 + 0x40) & 255;
        if (문자값 == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (ceŋondiral_kaɓirgal.input(자료위치, &ceŋondiral_kaɓirgal) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
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
    netif_poll(&ceŋondiral_kaɓirgal); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (기계저장기(보조장치 + 0x54) & 0x20); 처리한도++) {
        기계저장기(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* 설정·조회는 lwIP의 laatii_keɓe 인터페이스와 taƴde_toɓɓere 표를 사용한다. */
uint32_t 망상태읽기(unsigned naatnugol_njaru, unsigned joopirdu) {
    if(naatnugol_njaru==20)return 유선사용;
    if(naatnugol_njaru==21)return 준비됨&&netif_is_link_up(&ceŋondiral_kaɓirgal);
    if(naatnugol_njaru==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&naatnugol_njaru>=4&&naatnugol_njaru<=8)return 유선망집계(naatnugol_njaru-4);
    if (naatnugol_njaru == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ceŋondiral_kaɓirgal)));
    if (naatnugol_njaru == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&ceŋondiral_kaɓirgal)));
    if (naatnugol_njaru == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&ceŋondiral_kaɓirgal)));
    if (naatnugol_njaru == 3) return netif_is_up(&ceŋondiral_kaɓirgal) != 0;
    if (naatnugol_njaru == 4) return 받은전문수;
    if (naatnugol_njaru == 5) return 보낸전문수;
    if (naatnugol_njaru == 6) return 받은바이트수;
    if (naatnugol_njaru == 7) return 보낸바이트수;
    if (naatnugol_njaru == 8) return 버린전문수;
    if (naatnugol_njaru == 9) return 송신개수;
    if (joopirdu >= 32) return 0;
    통신끝점 *taƴde_toɓɓere = &통신끝점들[joopirdu];
    if (naatnugol_njaru == 10) return taƴde_toɓɓere->유형;
    if (!taƴde_toɓɓere->유형) return 0;
    if (naatnugol_njaru == 11) return 통신접속번호(joopirdu);
    if (naatnugol_njaru == 12) return taƴde_toɓɓere->giƴiraaɗo_ñiiɓirde;
    if (naatnugol_njaru == 13) return taƴde_toɓɓere->상대창구번호;
    if (naatnugol_njaru == 14) return taƴde_toɓɓere->수신창구 ? 1 : taƴde_toɓɓere->fiilde_taƴde ? 3 : taƴde_toɓɓere->juumre ? 4 : taƴde_toɓɓere->연결됨 ? 2 : 0;
    if (naatnugol_njaru == 15) return taƴde_toɓɓere->항목수;
    if (naatnugol_njaru == 16) {
        const ip_addr_t *ñiiɓirde = taƴde_toɓɓere->유형 == 1 && taƴde_toɓɓere->ceŋondiral_yuurnitorde ? &taƴde_toɓɓere->ceŋondiral_yuurnitorde->local_ip :
            taƴde_toɓɓere->유형 == 2 && taƴde_toɓɓere->전문제어 ? &taƴde_toɓɓere->전문제어->local_ip : 0;
        return ñiiɓirde ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ñiiɓirde))) : 0;
    }
    return 0;
}

int heblude_laylaytol(unsigned gollal, uint32_t ñiiɓirde, uint32_t 가림, uint32_t 관문) {
    if (!준비됨) return -100;
    if (gollal == 1) { netif_set_up(&ceŋondiral_kaɓirgal); return 0; }
    if (gollal == 2) { netif_set_down(&ceŋondiral_kaɓirgal); return 0; }
    if (gollal != 0) return -22;
    /* 유니캐스트 IPv4, 연속 가림, 같은 망의 선택적 lasli_njaru 관문. */
    uint32_t 뒤집은가림 = ~가림;
    if (!가림 || (뒤집은가림 & (뒤집은가림 + 1)) || !ñiiɓirde || (ñiiɓirde >> 24) == 127 ||
        (ñiiɓirde >> 24) == 0 || (ñiiɓirde >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ñiiɓirde & 뒤집은가림) || (ñiiɓirde & 뒤집은가림) == 뒤집은가림)) ||
        (관문 && ((관문 & 가림) != (ñiiɓirde & 가림) || 관문 == ñiiɓirde || (관문 >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(관문 & 뒤집은가림) || (관문 & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ñiiɓirde 변경으로 몰래 끊지 않는다. */
    for (unsigned joopirdu = 0; joopirdu < 32; joopirdu++) if (통신끝점들[joopirdu].유형 &&
        !(통신끝점들[joopirdu].수신창구 && 통신끝점들[joopirdu].ceŋondiral_yuurnitorde && ip_addr_isany(&통신끝점들[joopirdu].ceŋondiral_yuurnitorde->local_ip))) return -16;
    if(유선사용)dhcp_stop(&ceŋondiral_kaɓirgal);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ñiiɓirde)); ip4_addr_set_u32(&새가림, lwip_htonl(가림)); ip4_addr_set_u32(&새관문, lwip_htonl(관문));
    netif_set_addr(&ceŋondiral_kaɓirgal, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *taƴde_toɓɓere, struct pbuf *keɓe, const ip_addr_t *ñiiɓirde) {
    (void)인수; (void)taƴde_toɓɓere;
    unsigned char 머리[20], 응답[16];
    if (응답상태 != -11 || keɓe->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ñiiɓirde))) != 시험주소 || pbuf_copy_partial(keɓe, 머리, 20, 0) != 20) return 0;
    unsigned meetalol_hello_waylude_etannde = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || meetalol_hello_waylude_etannde < 20 || keɓe->tot_len < meetalol_hello_waylude_etannde + 16 ||
        pbuf_copy_partial(keɓe, 응답, 16, meetalol_hello_waylude_etannde) != 16 || 응답[0] || 응답[1] ||
        (((unsigned)응답[4] << 8) | 응답[5]) != 시험식별자 ||
        (((unsigned)응답[6] << 8) | 응답[7]) != 시험순서 ||
        응답[8] != 'J' || 응답[9] != 'K' || 응답[10] != 'O' || 응답[11] != 'S' ||
        (((uint32_t)응답[12] << 24) | ((uint32_t)응답[13] << 16) | ((uint32_t)응답[14] << 8) | 응답[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(keɓe, meetalol_hello_waylude_etannde)) return 0;
    if (inet_chksum_pbuf(keɓe)) { pbuf_add_header(keɓe, meetalol_hello_waylude_etannde); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(keɓe); return 1;
}
int 응답시험시작(uint32_t ñiiɓirde, unsigned deggondiral_njaru) {
    if (!준비됨 || !netif_is_up(&ceŋondiral_kaɓirgal)) return -100;
    if (!ñiiɓirde || (ñiiɓirde >> 28) >= 14 || ñiiɓirde == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ñiiɓirde; 시험순서 = deggondiral_njaru & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char keɓe[32] = {8,0,0,0};
    keɓe[4] = 시험식별자 >> 8; keɓe[5] = 시험식별자; keɓe[6] = 시험순서 >> 8; keɓe[7] = 시험순서;
    keɓe[8]='J'; keɓe[9]='K'; keɓe[10]='O'; keɓe[11]='S';
    keɓe[12]=시험시각 >> 24; keɓe[13]=시험시각 >> 16; keɓe[14]=시험시각 >> 8; keɓe[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(keɓe); 자리++) keɓe[자리] = 자리;
    uint16_t 확인합 = inet_chksum(keɓe, sizeof(keɓe)); memcpy(keɓe + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(keɓe), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, keɓe, sizeof(keɓe)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ñiiɓirde));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned naatnugol_njaru) {
    통신망살피기();
    return naatnugol_njaru == 0 ? 응답상태 : naatnugol_njaru == 1 ? (int)응답시간 : naatnugol_njaru == 2 ? (int)응답차례 : -22;
}
