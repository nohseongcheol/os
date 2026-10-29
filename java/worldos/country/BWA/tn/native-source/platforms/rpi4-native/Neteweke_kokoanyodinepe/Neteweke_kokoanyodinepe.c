#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Neteweke_kokoanyodinepe.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../kgakala_Boleng/kgakala_Boleng.h"
#include "golagantsweng_ka_megala_Neteweke.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define motšhine_kwadisa(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif Kgolagano_mobaele;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int tlanya_setlhopha, 수신창구, 대기중, 연결됨, faele_kgaola, phoso;
    struct tcp_pcb *Kgolagano_taolo;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char tshedimosetso[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], semphato_aterese;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int faele_mokgwakamogelo) { return faele_mokgwakamogelo >= 0 && faele_mokgwakamogelo < 32 && 통신끝점들[faele_mokgwakamogelo].tlanya_setlhopha ? &통신끝점들[faele_mokgwakamogelo] : 0; }
static int 예약하기(int tlanya_setlhopha) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].tlanya_setlhopha) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].tlanya_setlhopha = tlanya_setlhopha; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned khoutuletshwao) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = khoutuletshwao; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *aterese) {
    (void)개수; (void)aterese;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned khoutuletshwao = ((unsigned char *)다음위치->payload)[순번];
        if (khoutuletshwao == 192 || khoutuletshwao == 219) { 내보내기(219); 내보내기(khoutuletshwao == 192 ? 220 : 221); } else 내보내기(khoutuletshwao);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t Baakanya_nakotsamaiso_ya_puo_e_e_tlwaelegileng(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Baakanya_Neteweke(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    motšhine_kwadisa(보조장치 + 4) |= 1; motšhine_kwadisa(보조장치 + 0x60) = 0; motšhine_kwadisa(보조장치 + 0x44) = 0;
    motšhine_kwadisa(보조장치 + 0x48) = 0xc6; motšhine_kwadisa(보조장치 + 0x4c) = 3; motšhine_kwadisa(보조장치 + 0x68) = 270; motšhine_kwadisa(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t aterese_ya_Inthanete, bit_mmaseke, kgorotsamaiso_aterese;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&aterese_ya_Inthanete, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_mmaseke, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&kgorotsamaiso_aterese, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&Kgolagano_mobaele, &aterese_ya_Inthanete, &bit_mmaseke, &kgorotsamaiso_aterese, 0, 유선사용?Baakanya_golagantsweng_ka_megala_Neteweke:Baakanya_nakotsamaiso_ya_puo_e_e_tlwaelegileng, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&Kgolagano_mobaele); netif_set_up(&Kgolagano_mobaele);if(!유선사용)netif_set_link_up(&Kgolagano_mobaele); 준비됨 = 1;
    Baakanya_kgakala();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *phetiso_taolo_thibela, struct pbuf *자료위치, err_t phoso) {
    통신끝점 *dikwalwa_tshedimosetso = 부가인수; (void)phetiso_taolo_thibela; (void)phoso;
    if (!자료위치) { dikwalwa_tshedimosetso->faele_kgaola = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(dikwalwa_tshedimosetso->tshedimosetso) - dikwalwa_tshedimosetso->항목수) return ERR_MEM;
    unsigned 현재위치 = (dikwalwa_tshedimosetso->맨앞 + dikwalwa_tshedimosetso->항목수) % sizeof(dikwalwa_tshedimosetso->tshedimosetso);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        dikwalwa_tshedimosetso->tshedimosetso[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(dikwalwa_tshedimosetso->tshedimosetso);
    }
    dikwalwa_tshedimosetso->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t phoso) { 통신끝점 *dikwalwa_tshedimosetso = 부가인수; dikwalwa_tshedimosetso->Kgolagano_taolo = 0; dikwalwa_tshedimosetso->phoso = 오류번호(phoso); }
static void 되부름목록(통신끝점 *dikwalwa_tshedimosetso) { tcp_arg(dikwalwa_tshedimosetso->Kgolagano_taolo, dikwalwa_tshedimosetso); tcp_recv(dikwalwa_tshedimosetso->Kgolagano_taolo, 수신됨); tcp_err(dikwalwa_tshedimosetso->Kgolagano_taolo, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *phetiso_taolo_thibela, err_t phoso) {
    통신끝점 *dikwalwa_tshedimosetso = 부가인수; (void)phetiso_taolo_thibela; if (phoso) dikwalwa_tshedimosetso->phoso = 오류번호(phoso); else dikwalwa_tshedimosetso->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *phetiso_taolo_thibela, err_t phoso) {
    통신끝점 *부모항목 = 부가인수; if (phoso) return phoso;
    int faele_mokgwakamogelo = 예약하기(1); if (faele_mokgwakamogelo < 0) return ERR_MEM;
    통신끝점 *dikwalwa_tshedimosetso = &통신끝점들[faele_mokgwakamogelo]; dikwalwa_tshedimosetso->Kgolagano_taolo = phetiso_taolo_thibela; dikwalwa_tshedimosetso->연결됨 = 1; dikwalwa_tshedimosetso->대기중 = (int)(부모항목 - 통신끝점들);
    dikwalwa_tshedimosetso->semphato_aterese = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&phetiso_taolo_thibela->remote_ip))); dikwalwa_tshedimosetso->상대창구번호 = phetiso_taolo_thibela->remote_port;
    되부름목록(dikwalwa_tshedimosetso); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *phetiso_taolo_thibela, struct pbuf *자료위치, const ip_addr_t *aterese, u16_t 접속번호) {
    통신끝점 *dikwalwa_tshedimosetso = 부가인수; (void)phetiso_taolo_thibela;
    if (dikwalwa_tshedimosetso->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (dikwalwa_tshedimosetso->맨앞 + dikwalwa_tshedimosetso->항목수) % 4;
        pbuf_copy_partial(자료위치, dikwalwa_tshedimosetso->tshedimosetso + 자리 * 512, 자료위치->tot_len, 0);
        dikwalwa_tshedimosetso->길이목록[자리] = 자료위치->tot_len; dikwalwa_tshedimosetso->접속번호들[자리] = 접속번호;
        dikwalwa_tshedimosetso->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(aterese))); dikwalwa_tshedimosetso->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int tlanya_setlhopha) {
    if (!준비됨) return -100;
    if (tlanya_setlhopha != 1 && tlanya_setlhopha != 2) return -93;
    int faele_mokgwakamogelo = 예약하기(tlanya_setlhopha); if (faele_mokgwakamogelo < 0) return faele_mokgwakamogelo;
    통신끝점 *dikwalwa_tshedimosetso = &통신끝점들[faele_mokgwakamogelo];
    if (tlanya_setlhopha == 1) { dikwalwa_tshedimosetso->Kgolagano_taolo = tcp_new(); if (dikwalwa_tshedimosetso->Kgolagano_taolo) 되부름목록(dikwalwa_tshedimosetso); }
    else { dikwalwa_tshedimosetso->전문제어 = udp_new(); if (dikwalwa_tshedimosetso->전문제어) udp_recv(dikwalwa_tshedimosetso->전문제어, 전문, dikwalwa_tshedimosetso); }
    if (!dikwalwa_tshedimosetso->Kgolagano_taolo && !dikwalwa_tshedimosetso->전문제어) { dikwalwa_tshedimosetso->tlanya_setlhopha = 0; return -12; } return faele_mokgwakamogelo;
}
int 망주소묶기(int faele_mokgwakamogelo, uint32_t aterese, unsigned 접속번호) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso) return -9;
    if (접속번호 > 65535 || (aterese && aterese != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&Kgolagano_mobaele))) && aterese != 0x7f000001)) return -99;
    ip_addr_t aterese_ya_Inthanete; ip_addr_set_ip4_u32(&aterese_ya_Inthanete, lwip_htonl(aterese));
    err_t 보조항목 = dikwalwa_tshedimosetso->tlanya_setlhopha == 1 ? tcp_bind(dikwalwa_tshedimosetso->Kgolagano_taolo, &aterese_ya_Inthanete, 접속번호) : udp_bind(dikwalwa_tshedimosetso->전문제어, &aterese_ya_Inthanete, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int faele_mokgwakamogelo) { 통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (dikwalwa_tshedimosetso && dikwalwa_tshedimosetso->Kgolagano_taolo) ip_set_option(dikwalwa_tshedimosetso->Kgolagano_taolo, SOF_REUSEADDR); }
int 연결기다리기(int faele_mokgwakamogelo) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso || dikwalwa_tshedimosetso->tlanya_setlhopha != 1) return -9;
    if (dikwalwa_tshedimosetso->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *phetiso_taolo_thibela = tcp_listen_with_backlog_and_err(dikwalwa_tshedimosetso->Kgolagano_taolo, 4, &보조항목);
    if (!phetiso_taolo_thibela) return 오류번호(보조항목); dikwalwa_tshedimosetso->Kgolagano_taolo = phetiso_taolo_thibela; dikwalwa_tshedimosetso->수신창구 = 1; tcp_arg(phetiso_taolo_thibela, dikwalwa_tshedimosetso); tcp_accept(phetiso_taolo_thibela, 연결받음); return 0;
}
int 망연결하기(int faele_mokgwakamogelo, uint32_t aterese, unsigned 접속번호) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso || dikwalwa_tshedimosetso->tlanya_setlhopha != 1) return -9;
    if (dikwalwa_tshedimosetso->phoso) return dikwalwa_tshedimosetso->phoso;
    if (dikwalwa_tshedimosetso->연결됨) return 0;
    if (dikwalwa_tshedimosetso->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !aterese) return -22;
    ip_addr_t aterese_ya_Inthanete; ip_addr_set_ip4_u32(&aterese_ya_Inthanete, lwip_htonl(aterese));
    dikwalwa_tshedimosetso->semphato_aterese = aterese; dikwalwa_tshedimosetso->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(dikwalwa_tshedimosetso->Kgolagano_taolo, &aterese_ya_Inthanete, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int faele_mokgwakamogelo) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso || !dikwalwa_tshedimosetso->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].tlanya_setlhopha == 1 && 통신끝점들[순번].대기중 == faele_mokgwakamogelo) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int faele_mokgwakamogelo, void *tshedimosetso, unsigned 개수) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso || dikwalwa_tshedimosetso->tlanya_setlhopha != 1) return -9;
    if (!개수) return 0; if (!dikwalwa_tshedimosetso->항목수) return dikwalwa_tshedimosetso->phoso ? dikwalwa_tshedimosetso->phoso : dikwalwa_tshedimosetso->faele_kgaola ? 0 : -11;
    if (개수 > dikwalwa_tshedimosetso->항목수) 개수 = dikwalwa_tshedimosetso->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)tshedimosetso)[순번] = dikwalwa_tshedimosetso->tshedimosetso[dikwalwa_tshedimosetso->맨앞]; dikwalwa_tshedimosetso->맨앞 = (dikwalwa_tshedimosetso->맨앞 + 1) % sizeof(dikwalwa_tshedimosetso->tshedimosetso); }
    dikwalwa_tshedimosetso->항목수 -= 개수; if (dikwalwa_tshedimosetso->Kgolagano_taolo) tcp_recved(dikwalwa_tshedimosetso->Kgolagano_taolo, 개수); return 개수;
}
int 통신쓰기(int faele_mokgwakamogelo, const void *tshedimosetso, unsigned 개수) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso || dikwalwa_tshedimosetso->tlanya_setlhopha != 1) return -9;
    if (dikwalwa_tshedimosetso->phoso) return dikwalwa_tshedimosetso->phoso; if (!dikwalwa_tshedimosetso->Kgolagano_taolo || !dikwalwa_tshedimosetso->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(dikwalwa_tshedimosetso->Kgolagano_taolo)) 개수 = tcp_sndbuf(dikwalwa_tshedimosetso->Kgolagano_taolo);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(dikwalwa_tshedimosetso->Kgolagano_taolo, tshedimosetso, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(dikwalwa_tshedimosetso->Kgolagano_taolo); return 개수;
}
int 전문보내기(int faele_mokgwakamogelo, const void *tshedimosetso, unsigned 개수, uint32_t aterese, unsigned 접속번호) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso || dikwalwa_tshedimosetso->tlanya_setlhopha != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, tshedimosetso, 개수); ip_addr_t aterese_ya_Inthanete; ip_addr_set_ip4_u32(&aterese_ya_Inthanete, lwip_htonl(aterese));
    err_t 보조항목 = udp_sendto(dikwalwa_tshedimosetso->전문제어, 자료위치, &aterese_ya_Inthanete, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int faele_mokgwakamogelo, void *tshedimosetso, unsigned 개수) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso || dikwalwa_tshedimosetso->tlanya_setlhopha != 2) return -9;
    if (!dikwalwa_tshedimosetso->항목수) return -11; unsigned 현재위치 = dikwalwa_tshedimosetso->맨앞;
    if (개수 > dikwalwa_tshedimosetso->길이목록[현재위치]) 개수 = dikwalwa_tshedimosetso->길이목록[현재위치]; memcpy(tshedimosetso, dikwalwa_tshedimosetso->tshedimosetso + 현재위치 * 512, 개수);
    dikwalwa_tshedimosetso->상대창구번호 = dikwalwa_tshedimosetso->접속번호들[현재위치]; dikwalwa_tshedimosetso->semphato_aterese = dikwalwa_tshedimosetso->주소목록[현재위치]; dikwalwa_tshedimosetso->맨앞 = (현재위치 + 1) % 4; dikwalwa_tshedimosetso->항목수--; return 개수;
}
unsigned 통신접속번호(int faele_mokgwakamogelo) { 통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); return !dikwalwa_tshedimosetso ? 0 : dikwalwa_tshedimosetso->Kgolagano_taolo ? dikwalwa_tshedimosetso->Kgolagano_taolo->local_port : dikwalwa_tshedimosetso->전문제어 ? dikwalwa_tshedimosetso->전문제어->local_port : 0; }
unsigned 상대접속번호(int faele_mokgwakamogelo) { 통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); return dikwalwa_tshedimosetso ? dikwalwa_tshedimosetso->상대창구번호 : 0; }
uint32_t 상대통신주소(int faele_mokgwakamogelo) { 통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); return dikwalwa_tshedimosetso ? dikwalwa_tshedimosetso->semphato_aterese : 0; }
void tswala_Neteweke(int faele_mokgwakamogelo) {
    통신끝점 *dikwalwa_tshedimosetso = 얻기(faele_mokgwakamogelo); if (!dikwalwa_tshedimosetso) return;
    if (dikwalwa_tshedimosetso->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].tlanya_setlhopha && 통신끝점들[순번].대기중 == faele_mokgwakamogelo) tswala_Neteweke(순번);
    if (dikwalwa_tshedimosetso->Kgolagano_taolo) {
        tcp_arg(dikwalwa_tshedimosetso->Kgolagano_taolo, 0); if (dikwalwa_tshedimosetso->수신창구) tcp_accept(dikwalwa_tshedimosetso->Kgolagano_taolo, 0); else { tcp_recv(dikwalwa_tshedimosetso->Kgolagano_taolo, 0); tcp_err(dikwalwa_tshedimosetso->Kgolagano_taolo, 0); }
        if (tcp_close(dikwalwa_tshedimosetso->Kgolagano_taolo) != ERR_OK) tcp_abort(dikwalwa_tshedimosetso->Kgolagano_taolo);
    }
    if (dikwalwa_tshedimosetso->전문제어) udp_remove(dikwalwa_tshedimosetso->전문제어); dikwalwa_tshedimosetso->tlanya_setlhopha = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&Kgolagano_mobaele);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (motšhine_kwadisa(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned khoutuletshwao = motšhine_kwadisa(보조장치 + 0x40) & 255;
        if (khoutuletshwao == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (Kgolagano_mobaele.input(자료위치, &Kgolagano_mobaele) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (khoutuletshwao == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (khoutuletshwao != 220 && khoutuletshwao != 221) 수신오류 = 1; khoutuletshwao = khoutuletshwao == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = khoutuletshwao; else 수신오류 = 1;
        }
    }
    netif_poll(&Kgolagano_mobaele); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (motšhine_kwadisa(보조장치 + 0x54) & 0x20); 처리한도++) {
        motšhine_kwadisa(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Diseting·조회는 lwIP의 tota_tshedimosetso 인터페이스와 kgaola_ntlha 표를 사용한다. */
uint32_t 망상태읽기(unsigned tsenyo_Boleng, unsigned tshupane) {
    if(tsenyo_Boleng==20)return 유선사용;
    if(tsenyo_Boleng==21)return 준비됨&&netif_is_link_up(&Kgolagano_mobaele);
    if(tsenyo_Boleng==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&tsenyo_Boleng>=4&&tsenyo_Boleng<=8)return 유선망집계(tsenyo_Boleng-4);
    if (tsenyo_Boleng == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&Kgolagano_mobaele)));
    if (tsenyo_Boleng == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&Kgolagano_mobaele)));
    if (tsenyo_Boleng == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&Kgolagano_mobaele)));
    if (tsenyo_Boleng == 3) return netif_is_up(&Kgolagano_mobaele) != 0;
    if (tsenyo_Boleng == 4) return 받은전문수;
    if (tsenyo_Boleng == 5) return 보낸전문수;
    if (tsenyo_Boleng == 6) return 받은바이트수;
    if (tsenyo_Boleng == 7) return 보낸바이트수;
    if (tsenyo_Boleng == 8) return 버린전문수;
    if (tsenyo_Boleng == 9) return 송신개수;
    if (tshupane >= 32) return 0;
    통신끝점 *kgaola_ntlha = &통신끝점들[tshupane];
    if (tsenyo_Boleng == 10) return kgaola_ntlha->tlanya_setlhopha;
    if (!kgaola_ntlha->tlanya_setlhopha) return 0;
    if (tsenyo_Boleng == 11) return 통신접속번호(tshupane);
    if (tsenyo_Boleng == 12) return kgaola_ntlha->semphato_aterese;
    if (tsenyo_Boleng == 13) return kgaola_ntlha->상대창구번호;
    if (tsenyo_Boleng == 14) return kgaola_ntlha->수신창구 ? 1 : kgaola_ntlha->faele_kgaola ? 3 : kgaola_ntlha->phoso ? 4 : kgaola_ntlha->연결됨 ? 2 : 0;
    if (tsenyo_Boleng == 15) return kgaola_ntlha->항목수;
    if (tsenyo_Boleng == 16) {
        const ip_addr_t *aterese = kgaola_ntlha->tlanya_setlhopha == 1 && kgaola_ntlha->Kgolagano_taolo ? &kgaola_ntlha->Kgolagano_taolo->local_ip :
            kgaola_ntlha->tlanya_setlhopha == 2 && kgaola_ntlha->전문제어 ? &kgaola_ntlha->전문제어->local_ip : 0;
        return aterese ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(aterese))) : 0;
    }
    return 0;
}

int Rulaganya_Neteweke(unsigned tiro, uint32_t aterese, uint32_t mmaseke_Boleng, uint32_t kgorotsamaiso_Boleng) {
    if (!준비됨) return -100;
    if (tiro == 1) { netif_set_up(&Kgolagano_mobaele); return 0; }
    if (tiro == 2) { netif_set_down(&Kgolagano_mobaele); return 0; }
    if (tiro != 0) return -22;
    /* 유니캐스트 IPv4, 연속 mmaseke_Boleng, 같은 망의 선택적 boleng_jo_bo_rulaganyeditsweng_ruri kgorotsamaiso_Boleng. */
    uint32_t 뒤집은가림 = ~mmaseke_Boleng;
    if (!mmaseke_Boleng || (뒤집은가림 & (뒤집은가림 + 1)) || !aterese || (aterese >> 24) == 127 ||
        (aterese >> 24) == 0 || (aterese >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(aterese & 뒤집은가림) || (aterese & 뒤집은가림) == 뒤집은가림)) ||
        (kgorotsamaiso_Boleng && ((kgorotsamaiso_Boleng & mmaseke_Boleng) != (aterese & mmaseke_Boleng) || kgorotsamaiso_Boleng == aterese || (kgorotsamaiso_Boleng >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(kgorotsamaiso_Boleng & 뒤집은가림) || (kgorotsamaiso_Boleng & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 aterese 변경으로 몰래 끊지 않는다. */
    for (unsigned tshupane = 0; tshupane < 32; tshupane++) if (통신끝점들[tshupane].tlanya_setlhopha &&
        !(통신끝점들[tshupane].수신창구 && 통신끝점들[tshupane].Kgolagano_taolo && ip_addr_isany(&통신끝점들[tshupane].Kgolagano_taolo->local_ip))) return -16;
    if(유선사용)dhcp_stop(&Kgolagano_mobaele);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(aterese)); ip4_addr_set_u32(&새가림, lwip_htonl(mmaseke_Boleng)); ip4_addr_set_u32(&새관문, lwip_htonl(kgorotsamaiso_Boleng));
    netif_set_addr(&Kgolagano_mobaele, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *kgaola_ntlha, struct pbuf *tshedimosetso, const ip_addr_t *aterese) {
    (void)인수; (void)kgaola_ntlha;
    unsigned char 머리[20], araba[16];
    if (응답상태 != -11 || tshedimosetso->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(aterese))) != 시험주소 || pbuf_copy_partial(tshedimosetso, 머리, 20, 0) != 20) return 0;
    unsigned setlhogo_lekanya = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || setlhogo_lekanya < 20 || tshedimosetso->tot_len < setlhogo_lekanya + 16 ||
        pbuf_copy_partial(tshedimosetso, araba, 16, setlhogo_lekanya) != 16 || araba[0] || araba[1] ||
        (((unsigned)araba[4] << 8) | araba[5]) != 시험식별자 ||
        (((unsigned)araba[6] << 8) | araba[7]) != 시험순서 ||
        araba[8] != 'J' || araba[9] != 'K' || araba[10] != 'O' || araba[11] != 'S' ||
        (((uint32_t)araba[12] << 24) | ((uint32_t)araba[13] << 16) | ((uint32_t)araba[14] << 8) | araba[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(tshedimosetso, setlhogo_lekanya)) return 0;
    if (inet_chksum_pbuf(tshedimosetso)) { pbuf_add_header(tshedimosetso, setlhogo_lekanya); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(tshedimosetso); return 1;
}
int 응답시험시작(uint32_t aterese, unsigned thulaganyo_Boleng) {
    if (!준비됨 || !netif_is_up(&Kgolagano_mobaele)) return -100;
    if (!aterese || (aterese >> 28) >= 14 || aterese == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = aterese; 시험순서 = thulaganyo_Boleng & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char tshedimosetso[32] = {8,0,0,0};
    tshedimosetso[4] = 시험식별자 >> 8; tshedimosetso[5] = 시험식별자; tshedimosetso[6] = 시험순서 >> 8; tshedimosetso[7] = 시험순서;
    tshedimosetso[8]='J'; tshedimosetso[9]='K'; tshedimosetso[10]='O'; tshedimosetso[11]='S';
    tshedimosetso[12]=시험시각 >> 24; tshedimosetso[13]=시험시각 >> 16; tshedimosetso[14]=시험시각 >> 8; tshedimosetso[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(tshedimosetso); 자리++) tshedimosetso[자리] = 자리;
    uint16_t 확인합 = inet_chksum(tshedimosetso, sizeof(tshedimosetso)); memcpy(tshedimosetso + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(tshedimosetso), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, tshedimosetso, sizeof(tshedimosetso)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(aterese));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned tsenyo_Boleng) {
    통신망살피기();
    return tsenyo_Boleng == 0 ? 응답상태 : tsenyo_Boleng == 1 ? (int)응답시간 : tsenyo_Boleng == 2 ? (int)응답차례 : -22;
}
