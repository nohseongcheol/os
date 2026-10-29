#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Inethiwekhi_fumba.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../kude_ixabiso/kude_ixabiso.h"
#include "eqhagamshelweyo_Inethiwekhi.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define umatshini_bhalisa(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif uqhagamshelo_isixhobo;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int uhlobo_udidi, 수신창구, 대기중, 연결됨, ifayile_phela, Impazamo;
    struct tcp_pcb *uqhagamshelo_isilawuli;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char iingcombolo[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], untanga_idilesi;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int ifayile_isibambi) { return ifayile_isibambi >= 0 && ifayile_isibambi < 32 && 통신끝점들[ifayile_isibambi].uhlobo_udidi ? &통신끝점들[ifayile_isibambi] : 0; }
static int 예약하기(int uhlobo_udidi) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].uhlobo_udidi) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].uhlobo_udidi = uhlobo_udidi; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned ikhowudi_yekharakhtha) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = ikhowudi_yekharakhtha; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *idilesi) {
    (void)개수; (void)idilesi;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned ikhowudi_yekharakhtha = ((unsigned char *)다음위치->payload)[순번];
        if (ikhowudi_yekharakhtha == 192 || ikhowudi_yekharakhtha == 219) { 내보내기(219); 내보내기(ikhowudi_yekharakhtha == 192 ? 220 : 221); } else 내보내기(ikhowudi_yekharakhtha);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t lungisa_ixesha_lokusebenza_kolwimi_oluqhelekileyo(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void lungisa_Inethiwekhi(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    umatshini_bhalisa(보조장치 + 4) |= 1; umatshini_bhalisa(보조장치 + 0x60) = 0; umatshini_bhalisa(보조장치 + 0x44) = 0;
    umatshini_bhalisa(보조장치 + 0x48) = 0xc6; umatshini_bhalisa(보조장치 + 0x4c) = 3; umatshini_bhalisa(보조장치 + 0x68) = 270; umatshini_bhalisa(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t idilesi_yeintanethi, ibhithi_imaskhi, isango_lekhompyutha_idilesi;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&idilesi_yeintanethi, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&ibhithi_imaskhi, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&isango_lekhompyutha_idilesi, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&uqhagamshelo_isixhobo, &idilesi_yeintanethi, &ibhithi_imaskhi, &isango_lekhompyutha_idilesi, 0, 유선사용?lungisa_eqhagamshelweyo_Inethiwekhi:lungisa_ixesha_lokusebenza_kolwimi_oluqhelekileyo, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&uqhagamshelo_isixhobo); netif_set_up(&uqhagamshelo_isixhobo);if(!유선사용)netif_set_link_up(&uqhagamshelo_isixhobo); 준비됨 = 1;
    lungisa_kude();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *ukugqithiswa_kwengcaciso_isilawuli_thintela, struct pbuf *자료위치, err_t Impazamo) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 부가인수; (void)ukugqithiswa_kwengcaciso_isilawuli_thintela; (void)Impazamo;
    if (!자료위치) { uluhlu_lweekharektha_iingcombolo->ifayile_phela = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(uluhlu_lweekharektha_iingcombolo->iingcombolo) - uluhlu_lweekharektha_iingcombolo->항목수) return ERR_MEM;
    unsigned 현재위치 = (uluhlu_lweekharektha_iingcombolo->맨앞 + uluhlu_lweekharektha_iingcombolo->항목수) % sizeof(uluhlu_lweekharektha_iingcombolo->iingcombolo);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        uluhlu_lweekharektha_iingcombolo->iingcombolo[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(uluhlu_lweekharektha_iingcombolo->iingcombolo);
    }
    uluhlu_lweekharektha_iingcombolo->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Impazamo) { 통신끝점 *uluhlu_lweekharektha_iingcombolo = 부가인수; uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli = 0; uluhlu_lweekharektha_iingcombolo->Impazamo = 오류번호(Impazamo); }
static void 되부름목록(통신끝점 *uluhlu_lweekharektha_iingcombolo) { tcp_arg(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, uluhlu_lweekharektha_iingcombolo); tcp_recv(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, 수신됨); tcp_err(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *ukugqithiswa_kwengcaciso_isilawuli_thintela, err_t Impazamo) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 부가인수; (void)ukugqithiswa_kwengcaciso_isilawuli_thintela; if (Impazamo) uluhlu_lweekharektha_iingcombolo->Impazamo = 오류번호(Impazamo); else uluhlu_lweekharektha_iingcombolo->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *ukugqithiswa_kwengcaciso_isilawuli_thintela, err_t Impazamo) {
    통신끝점 *부모항목 = 부가인수; if (Impazamo) return Impazamo;
    int ifayile_isibambi = 예약하기(1); if (ifayile_isibambi < 0) return ERR_MEM;
    통신끝점 *uluhlu_lweekharektha_iingcombolo = &통신끝점들[ifayile_isibambi]; uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli = ukugqithiswa_kwengcaciso_isilawuli_thintela; uluhlu_lweekharektha_iingcombolo->연결됨 = 1; uluhlu_lweekharektha_iingcombolo->대기중 = (int)(부모항목 - 통신끝점들);
    uluhlu_lweekharektha_iingcombolo->untanga_idilesi = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&ukugqithiswa_kwengcaciso_isilawuli_thintela->remote_ip))); uluhlu_lweekharektha_iingcombolo->상대창구번호 = ukugqithiswa_kwengcaciso_isilawuli_thintela->remote_port;
    되부름목록(uluhlu_lweekharektha_iingcombolo); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *ukugqithiswa_kwengcaciso_isilawuli_thintela, struct pbuf *자료위치, const ip_addr_t *idilesi, u16_t 접속번호) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 부가인수; (void)ukugqithiswa_kwengcaciso_isilawuli_thintela;
    if (uluhlu_lweekharektha_iingcombolo->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (uluhlu_lweekharektha_iingcombolo->맨앞 + uluhlu_lweekharektha_iingcombolo->항목수) % 4;
        pbuf_copy_partial(자료위치, uluhlu_lweekharektha_iingcombolo->iingcombolo + 자리 * 512, 자료위치->tot_len, 0);
        uluhlu_lweekharektha_iingcombolo->길이목록[자리] = 자료위치->tot_len; uluhlu_lweekharektha_iingcombolo->접속번호들[자리] = 접속번호;
        uluhlu_lweekharektha_iingcombolo->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(idilesi))); uluhlu_lweekharektha_iingcombolo->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int uhlobo_udidi) {
    if (!준비됨) return -100;
    if (uhlobo_udidi != 1 && uhlobo_udidi != 2) return -93;
    int ifayile_isibambi = 예약하기(uhlobo_udidi); if (ifayile_isibambi < 0) return ifayile_isibambi;
    통신끝점 *uluhlu_lweekharektha_iingcombolo = &통신끝점들[ifayile_isibambi];
    if (uhlobo_udidi == 1) { uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli = tcp_new(); if (uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli) 되부름목록(uluhlu_lweekharektha_iingcombolo); }
    else { uluhlu_lweekharektha_iingcombolo->전문제어 = udp_new(); if (uluhlu_lweekharektha_iingcombolo->전문제어) udp_recv(uluhlu_lweekharektha_iingcombolo->전문제어, 전문, uluhlu_lweekharektha_iingcombolo); }
    if (!uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli && !uluhlu_lweekharektha_iingcombolo->전문제어) { uluhlu_lweekharektha_iingcombolo->uhlobo_udidi = 0; return -12; } return ifayile_isibambi;
}
int 망주소묶기(int ifayile_isibambi, uint32_t idilesi, unsigned 접속번호) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo) return -9;
    if (접속번호 > 65535 || (idilesi && idilesi != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&uqhagamshelo_isixhobo))) && idilesi != 0x7f000001)) return -99;
    ip_addr_t idilesi_yeintanethi; ip_addr_set_ip4_u32(&idilesi_yeintanethi, lwip_htonl(idilesi));
    err_t 보조항목 = uluhlu_lweekharektha_iingcombolo->uhlobo_udidi == 1 ? tcp_bind(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, &idilesi_yeintanethi, 접속번호) : udp_bind(uluhlu_lweekharektha_iingcombolo->전문제어, &idilesi_yeintanethi, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int ifayile_isibambi) { 통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (uluhlu_lweekharektha_iingcombolo && uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli) ip_set_option(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, SOF_REUSEADDR); }
int 연결기다리기(int ifayile_isibambi) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo || uluhlu_lweekharektha_iingcombolo->uhlobo_udidi != 1) return -9;
    if (uluhlu_lweekharektha_iingcombolo->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *ukugqithiswa_kwengcaciso_isilawuli_thintela = tcp_listen_with_backlog_and_err(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, 4, &보조항목);
    if (!ukugqithiswa_kwengcaciso_isilawuli_thintela) return 오류번호(보조항목); uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli = ukugqithiswa_kwengcaciso_isilawuli_thintela; uluhlu_lweekharektha_iingcombolo->수신창구 = 1; tcp_arg(ukugqithiswa_kwengcaciso_isilawuli_thintela, uluhlu_lweekharektha_iingcombolo); tcp_accept(ukugqithiswa_kwengcaciso_isilawuli_thintela, 연결받음); return 0;
}
int 망연결하기(int ifayile_isibambi, uint32_t idilesi, unsigned 접속번호) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo || uluhlu_lweekharektha_iingcombolo->uhlobo_udidi != 1) return -9;
    if (uluhlu_lweekharektha_iingcombolo->Impazamo) return uluhlu_lweekharektha_iingcombolo->Impazamo;
    if (uluhlu_lweekharektha_iingcombolo->연결됨) return 0;
    if (uluhlu_lweekharektha_iingcombolo->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !idilesi) return -22;
    ip_addr_t idilesi_yeintanethi; ip_addr_set_ip4_u32(&idilesi_yeintanethi, lwip_htonl(idilesi));
    uluhlu_lweekharektha_iingcombolo->untanga_idilesi = idilesi; uluhlu_lweekharektha_iingcombolo->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, &idilesi_yeintanethi, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int ifayile_isibambi) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo || !uluhlu_lweekharektha_iingcombolo->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].uhlobo_udidi == 1 && 통신끝점들[순번].대기중 == ifayile_isibambi) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int ifayile_isibambi, void *iingcombolo, unsigned 개수) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo || uluhlu_lweekharektha_iingcombolo->uhlobo_udidi != 1) return -9;
    if (!개수) return 0; if (!uluhlu_lweekharektha_iingcombolo->항목수) return uluhlu_lweekharektha_iingcombolo->Impazamo ? uluhlu_lweekharektha_iingcombolo->Impazamo : uluhlu_lweekharektha_iingcombolo->ifayile_phela ? 0 : -11;
    if (개수 > uluhlu_lweekharektha_iingcombolo->항목수) 개수 = uluhlu_lweekharektha_iingcombolo->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)iingcombolo)[순번] = uluhlu_lweekharektha_iingcombolo->iingcombolo[uluhlu_lweekharektha_iingcombolo->맨앞]; uluhlu_lweekharektha_iingcombolo->맨앞 = (uluhlu_lweekharektha_iingcombolo->맨앞 + 1) % sizeof(uluhlu_lweekharektha_iingcombolo->iingcombolo); }
    uluhlu_lweekharektha_iingcombolo->항목수 -= 개수; if (uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli) tcp_recved(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, 개수); return 개수;
}
int 통신쓰기(int ifayile_isibambi, const void *iingcombolo, unsigned 개수) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo || uluhlu_lweekharektha_iingcombolo->uhlobo_udidi != 1) return -9;
    if (uluhlu_lweekharektha_iingcombolo->Impazamo) return uluhlu_lweekharektha_iingcombolo->Impazamo; if (!uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli || !uluhlu_lweekharektha_iingcombolo->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli)) 개수 = tcp_sndbuf(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, iingcombolo, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli); return 개수;
}
int 전문보내기(int ifayile_isibambi, const void *iingcombolo, unsigned 개수, uint32_t idilesi, unsigned 접속번호) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo || uluhlu_lweekharektha_iingcombolo->uhlobo_udidi != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, iingcombolo, 개수); ip_addr_t idilesi_yeintanethi; ip_addr_set_ip4_u32(&idilesi_yeintanethi, lwip_htonl(idilesi));
    err_t 보조항목 = udp_sendto(uluhlu_lweekharektha_iingcombolo->전문제어, 자료위치, &idilesi_yeintanethi, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int ifayile_isibambi, void *iingcombolo, unsigned 개수) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo || uluhlu_lweekharektha_iingcombolo->uhlobo_udidi != 2) return -9;
    if (!uluhlu_lweekharektha_iingcombolo->항목수) return -11; unsigned 현재위치 = uluhlu_lweekharektha_iingcombolo->맨앞;
    if (개수 > uluhlu_lweekharektha_iingcombolo->길이목록[현재위치]) 개수 = uluhlu_lweekharektha_iingcombolo->길이목록[현재위치]; memcpy(iingcombolo, uluhlu_lweekharektha_iingcombolo->iingcombolo + 현재위치 * 512, 개수);
    uluhlu_lweekharektha_iingcombolo->상대창구번호 = uluhlu_lweekharektha_iingcombolo->접속번호들[현재위치]; uluhlu_lweekharektha_iingcombolo->untanga_idilesi = uluhlu_lweekharektha_iingcombolo->주소목록[현재위치]; uluhlu_lweekharektha_iingcombolo->맨앞 = (현재위치 + 1) % 4; uluhlu_lweekharektha_iingcombolo->항목수--; return 개수;
}
unsigned 통신접속번호(int ifayile_isibambi) { 통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); return !uluhlu_lweekharektha_iingcombolo ? 0 : uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli ? uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli->local_port : uluhlu_lweekharektha_iingcombolo->전문제어 ? uluhlu_lweekharektha_iingcombolo->전문제어->local_port : 0; }
unsigned 상대접속번호(int ifayile_isibambi) { 통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); return uluhlu_lweekharektha_iingcombolo ? uluhlu_lweekharektha_iingcombolo->상대창구번호 : 0; }
uint32_t 상대통신주소(int ifayile_isibambi) { 통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); return uluhlu_lweekharektha_iingcombolo ? uluhlu_lweekharektha_iingcombolo->untanga_idilesi : 0; }
void vala_Inethiwekhi(int ifayile_isibambi) {
    통신끝점 *uluhlu_lweekharektha_iingcombolo = 얻기(ifayile_isibambi); if (!uluhlu_lweekharektha_iingcombolo) return;
    if (uluhlu_lweekharektha_iingcombolo->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].uhlobo_udidi && 통신끝점들[순번].대기중 == ifayile_isibambi) vala_Inethiwekhi(순번);
    if (uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli) {
        tcp_arg(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, 0); if (uluhlu_lweekharektha_iingcombolo->수신창구) tcp_accept(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, 0); else { tcp_recv(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, 0); tcp_err(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli, 0); }
        if (tcp_close(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli) != ERR_OK) tcp_abort(uluhlu_lweekharektha_iingcombolo->uqhagamshelo_isilawuli);
    }
    if (uluhlu_lweekharektha_iingcombolo->전문제어) udp_remove(uluhlu_lweekharektha_iingcombolo->전문제어); uluhlu_lweekharektha_iingcombolo->uhlobo_udidi = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&uqhagamshelo_isixhobo);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (umatshini_bhalisa(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned ikhowudi_yekharakhtha = umatshini_bhalisa(보조장치 + 0x40) & 255;
        if (ikhowudi_yekharakhtha == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (uqhagamshelo_isixhobo.input(자료위치, &uqhagamshelo_isixhobo) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (ikhowudi_yekharakhtha == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (ikhowudi_yekharakhtha != 220 && ikhowudi_yekharakhtha != 221) 수신오류 = 1; ikhowudi_yekharakhtha = ikhowudi_yekharakhtha == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = ikhowudi_yekharakhtha; else 수신오류 = 1;
        }
    }
    netif_poll(&uqhagamshelo_isixhobo); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (umatshini_bhalisa(보조장치 + 0x54) & 0x20); 처리한도++) {
        umatshini_bhalisa(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Imimiselo·조회는 lwIP의 eyona_yenzekileyo_iingcombolo 인터페이스와 phela_inqaku 표를 사용한다. */
uint32_t 망상태읽기(unsigned ufako_nkcukacha_ixabiso, unsigned indeksa) {
    if(ufako_nkcukacha_ixabiso==20)return 유선사용;
    if(ufako_nkcukacha_ixabiso==21)return 준비됨&&netif_is_link_up(&uqhagamshelo_isixhobo);
    if(ufako_nkcukacha_ixabiso==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&ufako_nkcukacha_ixabiso>=4&&ufako_nkcukacha_ixabiso<=8)return 유선망집계(ufako_nkcukacha_ixabiso-4);
    if (ufako_nkcukacha_ixabiso == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&uqhagamshelo_isixhobo)));
    if (ufako_nkcukacha_ixabiso == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&uqhagamshelo_isixhobo)));
    if (ufako_nkcukacha_ixabiso == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&uqhagamshelo_isixhobo)));
    if (ufako_nkcukacha_ixabiso == 3) return netif_is_up(&uqhagamshelo_isixhobo) != 0;
    if (ufako_nkcukacha_ixabiso == 4) return 받은전문수;
    if (ufako_nkcukacha_ixabiso == 5) return 보낸전문수;
    if (ufako_nkcukacha_ixabiso == 6) return 받은바이트수;
    if (ufako_nkcukacha_ixabiso == 7) return 보낸바이트수;
    if (ufako_nkcukacha_ixabiso == 8) return 버린전문수;
    if (ufako_nkcukacha_ixabiso == 9) return 송신개수;
    if (indeksa >= 32) return 0;
    통신끝점 *phela_inqaku = &통신끝점들[indeksa];
    if (ufako_nkcukacha_ixabiso == 10) return phela_inqaku->uhlobo_udidi;
    if (!phela_inqaku->uhlobo_udidi) return 0;
    if (ufako_nkcukacha_ixabiso == 11) return 통신접속번호(indeksa);
    if (ufako_nkcukacha_ixabiso == 12) return phela_inqaku->untanga_idilesi;
    if (ufako_nkcukacha_ixabiso == 13) return phela_inqaku->상대창구번호;
    if (ufako_nkcukacha_ixabiso == 14) return phela_inqaku->수신창구 ? 1 : phela_inqaku->ifayile_phela ? 3 : phela_inqaku->Impazamo ? 4 : phela_inqaku->연결됨 ? 2 : 0;
    if (ufako_nkcukacha_ixabiso == 15) return phela_inqaku->항목수;
    if (ufako_nkcukacha_ixabiso == 16) {
        const ip_addr_t *idilesi = phela_inqaku->uhlobo_udidi == 1 && phela_inqaku->uqhagamshelo_isilawuli ? &phela_inqaku->uqhagamshelo_isilawuli->local_ip :
            phela_inqaku->uhlobo_udidi == 2 && phela_inqaku->전문제어 ? &phela_inqaku->전문제어->local_ip : 0;
        return idilesi ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(idilesi))) : 0;
    }
    return 0;
}

int lungiselela_Inethiwekhi(unsigned Intshukumo, uint32_t idilesi, uint32_t imaskhi_ixabiso, uint32_t isango_lekhompyutha_ixabiso) {
    if (!준비됨) return -100;
    if (Intshukumo == 1) { netif_set_up(&uqhagamshelo_isixhobo); return 0; }
    if (Intshukumo == 2) { netif_set_down(&uqhagamshelo_isixhobo); return 0; }
    if (Intshukumo != 0) return -22;
    /* 유니캐스트 IPv4, 연속 imaskhi_ixabiso, 같은 망의 선택적 ixabiso_elisisiseko isango_lekhompyutha_ixabiso. */
    uint32_t 뒤집은가림 = ~imaskhi_ixabiso;
    if (!imaskhi_ixabiso || (뒤집은가림 & (뒤집은가림 + 1)) || !idilesi || (idilesi >> 24) == 127 ||
        (idilesi >> 24) == 0 || (idilesi >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(idilesi & 뒤집은가림) || (idilesi & 뒤집은가림) == 뒤집은가림)) ||
        (isango_lekhompyutha_ixabiso && ((isango_lekhompyutha_ixabiso & imaskhi_ixabiso) != (idilesi & imaskhi_ixabiso) || isango_lekhompyutha_ixabiso == idilesi || (isango_lekhompyutha_ixabiso >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(isango_lekhompyutha_ixabiso & 뒤집은가림) || (isango_lekhompyutha_ixabiso & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 idilesi 변경으로 몰래 끊지 않는다. */
    for (unsigned indeksa = 0; indeksa < 32; indeksa++) if (통신끝점들[indeksa].uhlobo_udidi &&
        !(통신끝점들[indeksa].수신창구 && 통신끝점들[indeksa].uqhagamshelo_isilawuli && ip_addr_isany(&통신끝점들[indeksa].uqhagamshelo_isilawuli->local_ip))) return -16;
    if(유선사용)dhcp_stop(&uqhagamshelo_isixhobo);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(idilesi)); ip4_addr_set_u32(&새가림, lwip_htonl(imaskhi_ixabiso)); ip4_addr_set_u32(&새관문, lwip_htonl(isango_lekhompyutha_ixabiso));
    netif_set_addr(&uqhagamshelo_isixhobo, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *phela_inqaku, struct pbuf *iingcombolo, const ip_addr_t *idilesi) {
    (void)인수; (void)phela_inqaku;
    unsigned char 머리[20], phendula[16];
    if (응답상태 != -11 || iingcombolo->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(idilesi))) != 시험주소 || pbuf_copy_partial(iingcombolo, 머리, 20, 0) != 20) return 0;
    unsigned Iheda_isayizi = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Iheda_isayizi < 20 || iingcombolo->tot_len < Iheda_isayizi + 16 ||
        pbuf_copy_partial(iingcombolo, phendula, 16, Iheda_isayizi) != 16 || phendula[0] || phendula[1] ||
        (((unsigned)phendula[4] << 8) | phendula[5]) != 시험식별자 ||
        (((unsigned)phendula[6] << 8) | phendula[7]) != 시험순서 ||
        phendula[8] != 'J' || phendula[9] != 'K' || phendula[10] != 'O' || phendula[11] != 'S' ||
        (((uint32_t)phendula[12] << 24) | ((uint32_t)phendula[13] << 16) | ((uint32_t)phendula[14] << 8) | phendula[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(iingcombolo, Iheda_isayizi)) return 0;
    if (inet_chksum_pbuf(iingcombolo)) { pbuf_add_header(iingcombolo, Iheda_isayizi); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(iingcombolo); return 1;
}
int 응답시험시작(uint32_t idilesi, unsigned ulandelelwano_ixabiso) {
    if (!준비됨 || !netif_is_up(&uqhagamshelo_isixhobo)) return -100;
    if (!idilesi || (idilesi >> 28) >= 14 || idilesi == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = idilesi; 시험순서 = ulandelelwano_ixabiso & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char iingcombolo[32] = {8,0,0,0};
    iingcombolo[4] = 시험식별자 >> 8; iingcombolo[5] = 시험식별자; iingcombolo[6] = 시험순서 >> 8; iingcombolo[7] = 시험순서;
    iingcombolo[8]='J'; iingcombolo[9]='K'; iingcombolo[10]='O'; iingcombolo[11]='S';
    iingcombolo[12]=시험시각 >> 24; iingcombolo[13]=시험시각 >> 16; iingcombolo[14]=시험시각 >> 8; iingcombolo[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(iingcombolo); 자리++) iingcombolo[자리] = 자리;
    uint16_t 확인합 = inet_chksum(iingcombolo, sizeof(iingcombolo)); memcpy(iingcombolo + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(iingcombolo), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, iingcombolo, sizeof(iingcombolo)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(idilesi));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned ufako_nkcukacha_ixabiso) {
    통신망살피기();
    return ufako_nkcukacha_ixabiso == 0 ? 응답상태 : ufako_nkcukacha_ixabiso == 1 ? (int)응답시간 : ufako_nkcukacha_ixabiso == 2 ? (int)응답차례 : -22;
}
