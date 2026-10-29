#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Urusobemiyoboro_Ikirundo.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../kure_agaciro/kure_agaciro.h"
#include "y_umugozi_Urusobemiyoboro.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif kwihuza_igendanwa;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int 유형, 수신창구, 대기중, 연결됨, dosiye_kurangiza, IKOSA;
    struct tcp_pcb *kwihuza_icunga;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char amakurushingiro[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], Mugenzi_aderesi;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int dosiye_umukondo) { return dosiye_umukondo >= 0 && dosiye_umukondo < 32 && 통신끝점들[dosiye_umukondo].유형 ? &통신끝점들[dosiye_umukondo] : 0; }
static int 예약하기(int 유형) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].유형) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].유형 = 유형; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned 문자값) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = 문자값; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *aderesi) {
    (void)개수; (void)aderesi;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned 문자값 = ((unsigned char *)다음위치->payload)[순번];
        if (문자값 == 192 || 문자값 == 219) { 내보내기(219); 내보내기(문자값 == 192 ? 220 : 221); } else 내보내기(문자값);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t Gutegura_igihe_ururimi_rukorwamo(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Gutegura_Urusobemiyoboro(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    기계저장기(보조장치 + 4) |= 1; 기계저장기(보조장치 + 0x60) = 0; 기계저장기(보조장치 + 0x44) = 0;
    기계저장기(보조장치 + 0x48) = 0xc6; 기계저장기(보조장치 + 0x4c) = 3; 기계저장기(보조장치 + 0x68) = 270; 기계저장기(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Aderesi_ya_Interineti, bit_masiki, muhuzaporotokore_aderesi;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Aderesi_ya_Interineti, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_masiki, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&muhuzaporotokore_aderesi, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&kwihuza_igendanwa, &Aderesi_ya_Interineti, &bit_masiki, &muhuzaporotokore_aderesi, 0, 유선사용?Gutegura_y_umugozi_Urusobemiyoboro:Gutegura_igihe_ururimi_rukorwamo, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&kwihuza_igendanwa); netif_set_up(&kwihuza_igendanwa);if(!유선사용)netif_set_link_up(&kwihuza_igendanwa); 준비됨 = 1;
    Gutegura_kure();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *iyohereza_icunga_guheza, struct pbuf *자료위치, err_t IKOSA) {
    통신끝점 *igicenteruro_amakurushingiro = 부가인수; (void)iyohereza_icunga_guheza; (void)IKOSA;
    if (!자료위치) { igicenteruro_amakurushingiro->dosiye_kurangiza = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(igicenteruro_amakurushingiro->amakurushingiro) - igicenteruro_amakurushingiro->항목수) return ERR_MEM;
    unsigned 현재위치 = (igicenteruro_amakurushingiro->맨앞 + igicenteruro_amakurushingiro->항목수) % sizeof(igicenteruro_amakurushingiro->amakurushingiro);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        igicenteruro_amakurushingiro->amakurushingiro[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(igicenteruro_amakurushingiro->amakurushingiro);
    }
    igicenteruro_amakurushingiro->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t IKOSA) { 통신끝점 *igicenteruro_amakurushingiro = 부가인수; igicenteruro_amakurushingiro->kwihuza_icunga = 0; igicenteruro_amakurushingiro->IKOSA = 오류번호(IKOSA); }
static void 되부름목록(통신끝점 *igicenteruro_amakurushingiro) { tcp_arg(igicenteruro_amakurushingiro->kwihuza_icunga, igicenteruro_amakurushingiro); tcp_recv(igicenteruro_amakurushingiro->kwihuza_icunga, 수신됨); tcp_err(igicenteruro_amakurushingiro->kwihuza_icunga, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *iyohereza_icunga_guheza, err_t IKOSA) {
    통신끝점 *igicenteruro_amakurushingiro = 부가인수; (void)iyohereza_icunga_guheza; if (IKOSA) igicenteruro_amakurushingiro->IKOSA = 오류번호(IKOSA); else igicenteruro_amakurushingiro->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *iyohereza_icunga_guheza, err_t IKOSA) {
    통신끝점 *부모항목 = 부가인수; if (IKOSA) return IKOSA;
    int dosiye_umukondo = 예약하기(1); if (dosiye_umukondo < 0) return ERR_MEM;
    통신끝점 *igicenteruro_amakurushingiro = &통신끝점들[dosiye_umukondo]; igicenteruro_amakurushingiro->kwihuza_icunga = iyohereza_icunga_guheza; igicenteruro_amakurushingiro->연결됨 = 1; igicenteruro_amakurushingiro->대기중 = (int)(부모항목 - 통신끝점들);
    igicenteruro_amakurushingiro->Mugenzi_aderesi = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&iyohereza_icunga_guheza->remote_ip))); igicenteruro_amakurushingiro->상대창구번호 = iyohereza_icunga_guheza->remote_port;
    되부름목록(igicenteruro_amakurushingiro); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *iyohereza_icunga_guheza, struct pbuf *자료위치, const ip_addr_t *aderesi, u16_t 접속번호) {
    통신끝점 *igicenteruro_amakurushingiro = 부가인수; (void)iyohereza_icunga_guheza;
    if (igicenteruro_amakurushingiro->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (igicenteruro_amakurushingiro->맨앞 + igicenteruro_amakurushingiro->항목수) % 4;
        pbuf_copy_partial(자료위치, igicenteruro_amakurushingiro->amakurushingiro + 자리 * 512, 자료위치->tot_len, 0);
        igicenteruro_amakurushingiro->길이목록[자리] = 자료위치->tot_len; igicenteruro_amakurushingiro->접속번호들[자리] = 접속번호;
        igicenteruro_amakurushingiro->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(aderesi))); igicenteruro_amakurushingiro->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int 유형) {
    if (!준비됨) return -100;
    if (유형 != 1 && 유형 != 2) return -93;
    int dosiye_umukondo = 예약하기(유형); if (dosiye_umukondo < 0) return dosiye_umukondo;
    통신끝점 *igicenteruro_amakurushingiro = &통신끝점들[dosiye_umukondo];
    if (유형 == 1) { igicenteruro_amakurushingiro->kwihuza_icunga = tcp_new(); if (igicenteruro_amakurushingiro->kwihuza_icunga) 되부름목록(igicenteruro_amakurushingiro); }
    else { igicenteruro_amakurushingiro->전문제어 = udp_new(); if (igicenteruro_amakurushingiro->전문제어) udp_recv(igicenteruro_amakurushingiro->전문제어, 전문, igicenteruro_amakurushingiro); }
    if (!igicenteruro_amakurushingiro->kwihuza_icunga && !igicenteruro_amakurushingiro->전문제어) { igicenteruro_amakurushingiro->유형 = 0; return -12; } return dosiye_umukondo;
}
int 망주소묶기(int dosiye_umukondo, uint32_t aderesi, unsigned 접속번호) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro) return -9;
    if (접속번호 > 65535 || (aderesi && aderesi != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kwihuza_igendanwa))) && aderesi != 0x7f000001)) return -99;
    ip_addr_t Aderesi_ya_Interineti; ip_addr_set_ip4_u32(&Aderesi_ya_Interineti, lwip_htonl(aderesi));
    err_t 보조항목 = igicenteruro_amakurushingiro->유형 == 1 ? tcp_bind(igicenteruro_amakurushingiro->kwihuza_icunga, &Aderesi_ya_Interineti, 접속번호) : udp_bind(igicenteruro_amakurushingiro->전문제어, &Aderesi_ya_Interineti, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int dosiye_umukondo) { 통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (igicenteruro_amakurushingiro && igicenteruro_amakurushingiro->kwihuza_icunga) ip_set_option(igicenteruro_amakurushingiro->kwihuza_icunga, SOF_REUSEADDR); }
int 연결기다리기(int dosiye_umukondo) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro || igicenteruro_amakurushingiro->유형 != 1) return -9;
    if (igicenteruro_amakurushingiro->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *iyohereza_icunga_guheza = tcp_listen_with_backlog_and_err(igicenteruro_amakurushingiro->kwihuza_icunga, 4, &보조항목);
    if (!iyohereza_icunga_guheza) return 오류번호(보조항목); igicenteruro_amakurushingiro->kwihuza_icunga = iyohereza_icunga_guheza; igicenteruro_amakurushingiro->수신창구 = 1; tcp_arg(iyohereza_icunga_guheza, igicenteruro_amakurushingiro); tcp_accept(iyohereza_icunga_guheza, 연결받음); return 0;
}
int 망연결하기(int dosiye_umukondo, uint32_t aderesi, unsigned 접속번호) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro || igicenteruro_amakurushingiro->유형 != 1) return -9;
    if (igicenteruro_amakurushingiro->IKOSA) return igicenteruro_amakurushingiro->IKOSA;
    if (igicenteruro_amakurushingiro->연결됨) return 0;
    if (igicenteruro_amakurushingiro->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !aderesi) return -22;
    ip_addr_t Aderesi_ya_Interineti; ip_addr_set_ip4_u32(&Aderesi_ya_Interineti, lwip_htonl(aderesi));
    igicenteruro_amakurushingiro->Mugenzi_aderesi = aderesi; igicenteruro_amakurushingiro->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(igicenteruro_amakurushingiro->kwihuza_icunga, &Aderesi_ya_Interineti, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int dosiye_umukondo) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro || !igicenteruro_amakurushingiro->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].유형 == 1 && 통신끝점들[순번].대기중 == dosiye_umukondo) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int dosiye_umukondo, void *amakurushingiro, unsigned 개수) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro || igicenteruro_amakurushingiro->유형 != 1) return -9;
    if (!개수) return 0; if (!igicenteruro_amakurushingiro->항목수) return igicenteruro_amakurushingiro->IKOSA ? igicenteruro_amakurushingiro->IKOSA : igicenteruro_amakurushingiro->dosiye_kurangiza ? 0 : -11;
    if (개수 > igicenteruro_amakurushingiro->항목수) 개수 = igicenteruro_amakurushingiro->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)amakurushingiro)[순번] = igicenteruro_amakurushingiro->amakurushingiro[igicenteruro_amakurushingiro->맨앞]; igicenteruro_amakurushingiro->맨앞 = (igicenteruro_amakurushingiro->맨앞 + 1) % sizeof(igicenteruro_amakurushingiro->amakurushingiro); }
    igicenteruro_amakurushingiro->항목수 -= 개수; if (igicenteruro_amakurushingiro->kwihuza_icunga) tcp_recved(igicenteruro_amakurushingiro->kwihuza_icunga, 개수); return 개수;
}
int 통신쓰기(int dosiye_umukondo, const void *amakurushingiro, unsigned 개수) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro || igicenteruro_amakurushingiro->유형 != 1) return -9;
    if (igicenteruro_amakurushingiro->IKOSA) return igicenteruro_amakurushingiro->IKOSA; if (!igicenteruro_amakurushingiro->kwihuza_icunga || !igicenteruro_amakurushingiro->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(igicenteruro_amakurushingiro->kwihuza_icunga)) 개수 = tcp_sndbuf(igicenteruro_amakurushingiro->kwihuza_icunga);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(igicenteruro_amakurushingiro->kwihuza_icunga, amakurushingiro, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(igicenteruro_amakurushingiro->kwihuza_icunga); return 개수;
}
int 전문보내기(int dosiye_umukondo, const void *amakurushingiro, unsigned 개수, uint32_t aderesi, unsigned 접속번호) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro || igicenteruro_amakurushingiro->유형 != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, amakurushingiro, 개수); ip_addr_t Aderesi_ya_Interineti; ip_addr_set_ip4_u32(&Aderesi_ya_Interineti, lwip_htonl(aderesi));
    err_t 보조항목 = udp_sendto(igicenteruro_amakurushingiro->전문제어, 자료위치, &Aderesi_ya_Interineti, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int dosiye_umukondo, void *amakurushingiro, unsigned 개수) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro || igicenteruro_amakurushingiro->유형 != 2) return -9;
    if (!igicenteruro_amakurushingiro->항목수) return -11; unsigned 현재위치 = igicenteruro_amakurushingiro->맨앞;
    if (개수 > igicenteruro_amakurushingiro->길이목록[현재위치]) 개수 = igicenteruro_amakurushingiro->길이목록[현재위치]; memcpy(amakurushingiro, igicenteruro_amakurushingiro->amakurushingiro + 현재위치 * 512, 개수);
    igicenteruro_amakurushingiro->상대창구번호 = igicenteruro_amakurushingiro->접속번호들[현재위치]; igicenteruro_amakurushingiro->Mugenzi_aderesi = igicenteruro_amakurushingiro->주소목록[현재위치]; igicenteruro_amakurushingiro->맨앞 = (현재위치 + 1) % 4; igicenteruro_amakurushingiro->항목수--; return 개수;
}
unsigned 통신접속번호(int dosiye_umukondo) { 통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); return !igicenteruro_amakurushingiro ? 0 : igicenteruro_amakurushingiro->kwihuza_icunga ? igicenteruro_amakurushingiro->kwihuza_icunga->local_port : igicenteruro_amakurushingiro->전문제어 ? igicenteruro_amakurushingiro->전문제어->local_port : 0; }
unsigned 상대접속번호(int dosiye_umukondo) { 통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); return igicenteruro_amakurushingiro ? igicenteruro_amakurushingiro->상대창구번호 : 0; }
uint32_t 상대통신주소(int dosiye_umukondo) { 통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); return igicenteruro_amakurushingiro ? igicenteruro_amakurushingiro->Mugenzi_aderesi : 0; }
void gufunga_Urusobemiyoboro(int dosiye_umukondo) {
    통신끝점 *igicenteruro_amakurushingiro = 얻기(dosiye_umukondo); if (!igicenteruro_amakurushingiro) return;
    if (igicenteruro_amakurushingiro->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].유형 && 통신끝점들[순번].대기중 == dosiye_umukondo) gufunga_Urusobemiyoboro(순번);
    if (igicenteruro_amakurushingiro->kwihuza_icunga) {
        tcp_arg(igicenteruro_amakurushingiro->kwihuza_icunga, 0); if (igicenteruro_amakurushingiro->수신창구) tcp_accept(igicenteruro_amakurushingiro->kwihuza_icunga, 0); else { tcp_recv(igicenteruro_amakurushingiro->kwihuza_icunga, 0); tcp_err(igicenteruro_amakurushingiro->kwihuza_icunga, 0); }
        if (tcp_close(igicenteruro_amakurushingiro->kwihuza_icunga) != ERR_OK) tcp_abort(igicenteruro_amakurushingiro->kwihuza_icunga);
    }
    if (igicenteruro_amakurushingiro->전문제어) udp_remove(igicenteruro_amakurushingiro->전문제어); igicenteruro_amakurushingiro->유형 = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&kwihuza_igendanwa);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (기계저장기(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned 문자값 = 기계저장기(보조장치 + 0x40) & 255;
        if (문자값 == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (kwihuza_igendanwa.input(자료위치, &kwihuza_igendanwa) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
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
    netif_poll(&kwihuza_igendanwa); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (기계저장기(보조장치 + 0x54) & 0x20); 처리한도++) {
        기계저장기(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Amagenamiterere·조회는 lwIP의 nyakuri_amakurushingiro 인터페이스와 kurangiza_inota 표를 사용한다. */
uint32_t 망상태읽기(unsigned icyinjizwa_agaciro, unsigned umugerekashakiro) {
    if(icyinjizwa_agaciro==20)return 유선사용;
    if(icyinjizwa_agaciro==21)return 준비됨&&netif_is_link_up(&kwihuza_igendanwa);
    if(icyinjizwa_agaciro==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&icyinjizwa_agaciro>=4&&icyinjizwa_agaciro<=8)return 유선망집계(icyinjizwa_agaciro-4);
    if (icyinjizwa_agaciro == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kwihuza_igendanwa)));
    if (icyinjizwa_agaciro == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&kwihuza_igendanwa)));
    if (icyinjizwa_agaciro == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&kwihuza_igendanwa)));
    if (icyinjizwa_agaciro == 3) return netif_is_up(&kwihuza_igendanwa) != 0;
    if (icyinjizwa_agaciro == 4) return 받은전문수;
    if (icyinjizwa_agaciro == 5) return 보낸전문수;
    if (icyinjizwa_agaciro == 6) return 받은바이트수;
    if (icyinjizwa_agaciro == 7) return 보낸바이트수;
    if (icyinjizwa_agaciro == 8) return 버린전문수;
    if (icyinjizwa_agaciro == 9) return 송신개수;
    if (umugerekashakiro >= 32) return 0;
    통신끝점 *kurangiza_inota = &통신끝점들[umugerekashakiro];
    if (icyinjizwa_agaciro == 10) return kurangiza_inota->유형;
    if (!kurangiza_inota->유형) return 0;
    if (icyinjizwa_agaciro == 11) return 통신접속번호(umugerekashakiro);
    if (icyinjizwa_agaciro == 12) return kurangiza_inota->Mugenzi_aderesi;
    if (icyinjizwa_agaciro == 13) return kurangiza_inota->상대창구번호;
    if (icyinjizwa_agaciro == 14) return kurangiza_inota->수신창구 ? 1 : kurangiza_inota->dosiye_kurangiza ? 3 : kurangiza_inota->IKOSA ? 4 : kurangiza_inota->연결됨 ? 2 : 0;
    if (icyinjizwa_agaciro == 15) return kurangiza_inota->항목수;
    if (icyinjizwa_agaciro == 16) {
        const ip_addr_t *aderesi = kurangiza_inota->유형 == 1 && kurangiza_inota->kwihuza_icunga ? &kurangiza_inota->kwihuza_icunga->local_ip :
            kurangiza_inota->유형 == 2 && kurangiza_inota->전문제어 ? &kurangiza_inota->전문제어->local_ip : 0;
        return aderesi ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(aderesi))) : 0;
    }
    return 0;
}

int kuboneza_Urusobemiyoboro(unsigned Igikorwa, uint32_t aderesi, uint32_t masiki_agaciro, uint32_t muhuzaporotokore_agaciro) {
    if (!준비됨) return -100;
    if (Igikorwa == 1) { netif_set_up(&kwihuza_igendanwa); return 0; }
    if (Igikorwa == 2) { netif_set_down(&kwihuza_igendanwa); return 0; }
    if (Igikorwa != 0) return -22;
    /* 유니캐스트 IPv4, 연속 masiki_agaciro, 같은 망의 선택적 agaciro_gasanzweho muhuzaporotokore_agaciro. */
    uint32_t 뒤집은가림 = ~masiki_agaciro;
    if (!masiki_agaciro || (뒤집은가림 & (뒤집은가림 + 1)) || !aderesi || (aderesi >> 24) == 127 ||
        (aderesi >> 24) == 0 || (aderesi >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(aderesi & 뒤집은가림) || (aderesi & 뒤집은가림) == 뒤집은가림)) ||
        (muhuzaporotokore_agaciro && ((muhuzaporotokore_agaciro & masiki_agaciro) != (aderesi & masiki_agaciro) || muhuzaporotokore_agaciro == aderesi || (muhuzaporotokore_agaciro >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(muhuzaporotokore_agaciro & 뒤집은가림) || (muhuzaporotokore_agaciro & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 aderesi 변경으로 몰래 끊지 않는다. */
    for (unsigned umugerekashakiro = 0; umugerekashakiro < 32; umugerekashakiro++) if (통신끝점들[umugerekashakiro].유형 &&
        !(통신끝점들[umugerekashakiro].수신창구 && 통신끝점들[umugerekashakiro].kwihuza_icunga && ip_addr_isany(&통신끝점들[umugerekashakiro].kwihuza_icunga->local_ip))) return -16;
    if(유선사용)dhcp_stop(&kwihuza_igendanwa);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(aderesi)); ip4_addr_set_u32(&새가림, lwip_htonl(masiki_agaciro)); ip4_addr_set_u32(&새관문, lwip_htonl(muhuzaporotokore_agaciro));
    netif_set_addr(&kwihuza_igendanwa, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *kurangiza_inota, struct pbuf *amakurushingiro, const ip_addr_t *aderesi) {
    (void)인수; (void)kurangiza_inota;
    unsigned char 머리[20], gusubiza[16];
    if (응답상태 != -11 || amakurushingiro->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(aderesi))) != 시험주소 || pbuf_copy_partial(amakurushingiro, 머리, 20, 0) != 20) return 0;
    unsigned Umutwengaruka_ingano = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Umutwengaruka_ingano < 20 || amakurushingiro->tot_len < Umutwengaruka_ingano + 16 ||
        pbuf_copy_partial(amakurushingiro, gusubiza, 16, Umutwengaruka_ingano) != 16 || gusubiza[0] || gusubiza[1] ||
        (((unsigned)gusubiza[4] << 8) | gusubiza[5]) != 시험식별자 ||
        (((unsigned)gusubiza[6] << 8) | gusubiza[7]) != 시험순서 ||
        gusubiza[8] != 'J' || gusubiza[9] != 'K' || gusubiza[10] != 'O' || gusubiza[11] != 'S' ||
        (((uint32_t)gusubiza[12] << 24) | ((uint32_t)gusubiza[13] << 16) | ((uint32_t)gusubiza[14] << 8) | gusubiza[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(amakurushingiro, Umutwengaruka_ingano)) return 0;
    if (inet_chksum_pbuf(amakurushingiro)) { pbuf_add_header(amakurushingiro, Umutwengaruka_ingano); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(amakurushingiro); return 1;
}
int 응답시험시작(uint32_t aderesi, unsigned umujyo_agaciro) {
    if (!준비됨 || !netif_is_up(&kwihuza_igendanwa)) return -100;
    if (!aderesi || (aderesi >> 28) >= 14 || aderesi == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = aderesi; 시험순서 = umujyo_agaciro & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char amakurushingiro[32] = {8,0,0,0};
    amakurushingiro[4] = 시험식별자 >> 8; amakurushingiro[5] = 시험식별자; amakurushingiro[6] = 시험순서 >> 8; amakurushingiro[7] = 시험순서;
    amakurushingiro[8]='J'; amakurushingiro[9]='K'; amakurushingiro[10]='O'; amakurushingiro[11]='S';
    amakurushingiro[12]=시험시각 >> 24; amakurushingiro[13]=시험시각 >> 16; amakurushingiro[14]=시험시각 >> 8; amakurushingiro[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(amakurushingiro); 자리++) amakurushingiro[자리] = 자리;
    uint16_t 확인합 = inet_chksum(amakurushingiro, sizeof(amakurushingiro)); memcpy(amakurushingiro + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(amakurushingiro), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, amakurushingiro, sizeof(amakurushingiro)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(aderesi));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned icyinjizwa_agaciro) {
    통신망살피기();
    return icyinjizwa_agaciro == 0 ? 응답상태 : icyinjizwa_agaciro == 1 ? (int)응답시간 : icyinjizwa_agaciro == 2 ? (int)응답차례 : -22;
}
