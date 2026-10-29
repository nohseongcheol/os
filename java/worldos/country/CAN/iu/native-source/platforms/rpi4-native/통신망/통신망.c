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
#include "../ungasittuq_atuutilik/ungasittuq_atuutilik.h"
#include "nukillautilik_Kasuqatigiitsimajut.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif kasuqsimaniq_sunakkutaaq;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int qanuittuuninga_Ataqatigiivvik, 수신창구, 대기중, 연결됨, ini_isulittuq, tammarniq;
    struct tcp_pcb *kasuqsimaniq_aulattivik;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char titiqqat[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], ilagijaujuq_turaarut;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int ini_nuuttarut) { return ini_nuuttarut >= 0 && ini_nuuttarut < 32 && 통신끝점들[ini_nuuttarut].qanuittuuninga_Ataqatigiivvik ? &통신끝점들[ini_nuuttarut] : 0; }
static int 예약하기(int qanuittuuninga_Ataqatigiivvik) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].qanuittuuninga_Ataqatigiivvik) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].qanuittuuninga_Ataqatigiivvik = qanuittuuninga_Ataqatigiivvik; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned immikkuuqtumut_nalunaikkut) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = immikkuuqtumut_nalunaikkut; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *turaarut) {
    (void)개수; (void)turaarut;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned immikkuuqtumut_nalunaikkut = ((unsigned char *)다음위치->payload)[순번];
        if (immikkuuqtumut_nalunaikkut == 192 || immikkuuqtumut_nalunaikkut == 219) { 내보내기(219); 내보내기(immikkuuqtumut_nalunaikkut == 192 ? 220 : 221); } else 내보내기(immikkuuqtumut_nalunaikkut);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t 준비하기(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Parnalli_Kasuqatigiitsimajut(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    기계저장기(보조장치 + 4) |= 1; 기계저장기(보조장치 + 0x60) = 0; 기계저장기(보조장치 + 0x44) = 0;
    기계저장기(보조장치 + 0x48) = 0xc6; 기계저장기(보조장치 + 0x4c) = 3; 기계저장기(보조장치 + 0x68) = 270; 기계저장기(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Ikiaqqivikkut_turaarut, bit_kiinappak, aqqusiurut_turaarut;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Ikiaqqivikkut_turaarut, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_kiinappak, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&aqqusiurut_turaarut, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&kasuqsimaniq_sunakkutaaq, &Ikiaqqivikkut_turaarut, &bit_kiinappak, &aqqusiurut_turaarut, 0, 유선사용?Parnalli_nukillautilik_Kasuqatigiitsimajut:준비하기, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&kasuqsimaniq_sunakkutaaq); netif_set_up(&kasuqsimaniq_sunakkutaaq);if(!유선사용)netif_set_link_up(&kasuqsimaniq_sunakkutaaq); 준비됨 = 1;
    Parnalli_ungasittuq();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *aullatittiniq_aulattivik_sapummili, struct pbuf *자료위치, err_t tammarniq) {
    통신끝점 *qimiaq_titiqqat = 부가인수; (void)aullatittiniq_aulattivik_sapummili; (void)tammarniq;
    if (!자료위치) { qimiaq_titiqqat->ini_isulittuq = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(qimiaq_titiqqat->titiqqat) - qimiaq_titiqqat->항목수) return ERR_MEM;
    unsigned 현재위치 = (qimiaq_titiqqat->맨앞 + qimiaq_titiqqat->항목수) % sizeof(qimiaq_titiqqat->titiqqat);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        qimiaq_titiqqat->titiqqat[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(qimiaq_titiqqat->titiqqat);
    }
    qimiaq_titiqqat->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t tammarniq) { 통신끝점 *qimiaq_titiqqat = 부가인수; qimiaq_titiqqat->kasuqsimaniq_aulattivik = 0; qimiaq_titiqqat->tammarniq = 오류번호(tammarniq); }
static void 되부름목록(통신끝점 *qimiaq_titiqqat) { tcp_arg(qimiaq_titiqqat->kasuqsimaniq_aulattivik, qimiaq_titiqqat); tcp_recv(qimiaq_titiqqat->kasuqsimaniq_aulattivik, 수신됨); tcp_err(qimiaq_titiqqat->kasuqsimaniq_aulattivik, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *aullatittiniq_aulattivik_sapummili, err_t tammarniq) {
    통신끝점 *qimiaq_titiqqat = 부가인수; (void)aullatittiniq_aulattivik_sapummili; if (tammarniq) qimiaq_titiqqat->tammarniq = 오류번호(tammarniq); else qimiaq_titiqqat->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *aullatittiniq_aulattivik_sapummili, err_t tammarniq) {
    통신끝점 *부모항목 = 부가인수; if (tammarniq) return tammarniq;
    int ini_nuuttarut = 예약하기(1); if (ini_nuuttarut < 0) return ERR_MEM;
    통신끝점 *qimiaq_titiqqat = &통신끝점들[ini_nuuttarut]; qimiaq_titiqqat->kasuqsimaniq_aulattivik = aullatittiniq_aulattivik_sapummili; qimiaq_titiqqat->연결됨 = 1; qimiaq_titiqqat->대기중 = (int)(부모항목 - 통신끝점들);
    qimiaq_titiqqat->ilagijaujuq_turaarut = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&aullatittiniq_aulattivik_sapummili->remote_ip))); qimiaq_titiqqat->상대창구번호 = aullatittiniq_aulattivik_sapummili->remote_port;
    되부름목록(qimiaq_titiqqat); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *aullatittiniq_aulattivik_sapummili, struct pbuf *자료위치, const ip_addr_t *turaarut, u16_t 접속번호) {
    통신끝점 *qimiaq_titiqqat = 부가인수; (void)aullatittiniq_aulattivik_sapummili;
    if (qimiaq_titiqqat->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (qimiaq_titiqqat->맨앞 + qimiaq_titiqqat->항목수) % 4;
        pbuf_copy_partial(자료위치, qimiaq_titiqqat->titiqqat + 자리 * 512, 자료위치->tot_len, 0);
        qimiaq_titiqqat->길이목록[자리] = 자료위치->tot_len; qimiaq_titiqqat->접속번호들[자리] = 접속번호;
        qimiaq_titiqqat->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(turaarut))); qimiaq_titiqqat->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int qanuittuuninga_Ataqatigiivvik) {
    if (!준비됨) return -100;
    if (qanuittuuninga_Ataqatigiivvik != 1 && qanuittuuninga_Ataqatigiivvik != 2) return -93;
    int ini_nuuttarut = 예약하기(qanuittuuninga_Ataqatigiivvik); if (ini_nuuttarut < 0) return ini_nuuttarut;
    통신끝점 *qimiaq_titiqqat = &통신끝점들[ini_nuuttarut];
    if (qanuittuuninga_Ataqatigiivvik == 1) { qimiaq_titiqqat->kasuqsimaniq_aulattivik = tcp_new(); if (qimiaq_titiqqat->kasuqsimaniq_aulattivik) 되부름목록(qimiaq_titiqqat); }
    else { qimiaq_titiqqat->전문제어 = udp_new(); if (qimiaq_titiqqat->전문제어) udp_recv(qimiaq_titiqqat->전문제어, 전문, qimiaq_titiqqat); }
    if (!qimiaq_titiqqat->kasuqsimaniq_aulattivik && !qimiaq_titiqqat->전문제어) { qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik = 0; return -12; } return ini_nuuttarut;
}
int 망주소묶기(int ini_nuuttarut, uint32_t turaarut, unsigned 접속번호) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat) return -9;
    if (접속번호 > 65535 || (turaarut && turaarut != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kasuqsimaniq_sunakkutaaq))) && turaarut != 0x7f000001)) return -99;
    ip_addr_t Ikiaqqivikkut_turaarut; ip_addr_set_ip4_u32(&Ikiaqqivikkut_turaarut, lwip_htonl(turaarut));
    err_t 보조항목 = qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik == 1 ? tcp_bind(qimiaq_titiqqat->kasuqsimaniq_aulattivik, &Ikiaqqivikkut_turaarut, 접속번호) : udp_bind(qimiaq_titiqqat->전문제어, &Ikiaqqivikkut_turaarut, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int ini_nuuttarut) { 통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (qimiaq_titiqqat && qimiaq_titiqqat->kasuqsimaniq_aulattivik) ip_set_option(qimiaq_titiqqat->kasuqsimaniq_aulattivik, SOF_REUSEADDR); }
int 연결기다리기(int ini_nuuttarut) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat || qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik != 1) return -9;
    if (qimiaq_titiqqat->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *aullatittiniq_aulattivik_sapummili = tcp_listen_with_backlog_and_err(qimiaq_titiqqat->kasuqsimaniq_aulattivik, 4, &보조항목);
    if (!aullatittiniq_aulattivik_sapummili) return 오류번호(보조항목); qimiaq_titiqqat->kasuqsimaniq_aulattivik = aullatittiniq_aulattivik_sapummili; qimiaq_titiqqat->수신창구 = 1; tcp_arg(aullatittiniq_aulattivik_sapummili, qimiaq_titiqqat); tcp_accept(aullatittiniq_aulattivik_sapummili, 연결받음); return 0;
}
int 망연결하기(int ini_nuuttarut, uint32_t turaarut, unsigned 접속번호) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat || qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik != 1) return -9;
    if (qimiaq_titiqqat->tammarniq) return qimiaq_titiqqat->tammarniq;
    if (qimiaq_titiqqat->연결됨) return 0;
    if (qimiaq_titiqqat->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !turaarut) return -22;
    ip_addr_t Ikiaqqivikkut_turaarut; ip_addr_set_ip4_u32(&Ikiaqqivikkut_turaarut, lwip_htonl(turaarut));
    qimiaq_titiqqat->ilagijaujuq_turaarut = turaarut; qimiaq_titiqqat->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(qimiaq_titiqqat->kasuqsimaniq_aulattivik, &Ikiaqqivikkut_turaarut, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int ini_nuuttarut) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat || !qimiaq_titiqqat->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].qanuittuuninga_Ataqatigiivvik == 1 && 통신끝점들[순번].대기중 == ini_nuuttarut) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int ini_nuuttarut, void *titiqqat, unsigned 개수) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat || qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik != 1) return -9;
    if (!개수) return 0; if (!qimiaq_titiqqat->항목수) return qimiaq_titiqqat->tammarniq ? qimiaq_titiqqat->tammarniq : qimiaq_titiqqat->ini_isulittuq ? 0 : -11;
    if (개수 > qimiaq_titiqqat->항목수) 개수 = qimiaq_titiqqat->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)titiqqat)[순번] = qimiaq_titiqqat->titiqqat[qimiaq_titiqqat->맨앞]; qimiaq_titiqqat->맨앞 = (qimiaq_titiqqat->맨앞 + 1) % sizeof(qimiaq_titiqqat->titiqqat); }
    qimiaq_titiqqat->항목수 -= 개수; if (qimiaq_titiqqat->kasuqsimaniq_aulattivik) tcp_recved(qimiaq_titiqqat->kasuqsimaniq_aulattivik, 개수); return 개수;
}
int 통신쓰기(int ini_nuuttarut, const void *titiqqat, unsigned 개수) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat || qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik != 1) return -9;
    if (qimiaq_titiqqat->tammarniq) return qimiaq_titiqqat->tammarniq; if (!qimiaq_titiqqat->kasuqsimaniq_aulattivik || !qimiaq_titiqqat->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(qimiaq_titiqqat->kasuqsimaniq_aulattivik)) 개수 = tcp_sndbuf(qimiaq_titiqqat->kasuqsimaniq_aulattivik);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(qimiaq_titiqqat->kasuqsimaniq_aulattivik, titiqqat, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(qimiaq_titiqqat->kasuqsimaniq_aulattivik); return 개수;
}
int 전문보내기(int ini_nuuttarut, const void *titiqqat, unsigned 개수, uint32_t turaarut, unsigned 접속번호) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat || qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, titiqqat, 개수); ip_addr_t Ikiaqqivikkut_turaarut; ip_addr_set_ip4_u32(&Ikiaqqivikkut_turaarut, lwip_htonl(turaarut));
    err_t 보조항목 = udp_sendto(qimiaq_titiqqat->전문제어, 자료위치, &Ikiaqqivikkut_turaarut, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int ini_nuuttarut, void *titiqqat, unsigned 개수) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat || qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik != 2) return -9;
    if (!qimiaq_titiqqat->항목수) return -11; unsigned 현재위치 = qimiaq_titiqqat->맨앞;
    if (개수 > qimiaq_titiqqat->길이목록[현재위치]) 개수 = qimiaq_titiqqat->길이목록[현재위치]; memcpy(titiqqat, qimiaq_titiqqat->titiqqat + 현재위치 * 512, 개수);
    qimiaq_titiqqat->상대창구번호 = qimiaq_titiqqat->접속번호들[현재위치]; qimiaq_titiqqat->ilagijaujuq_turaarut = qimiaq_titiqqat->주소목록[현재위치]; qimiaq_titiqqat->맨앞 = (현재위치 + 1) % 4; qimiaq_titiqqat->항목수--; return 개수;
}
unsigned 통신접속번호(int ini_nuuttarut) { 통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); return !qimiaq_titiqqat ? 0 : qimiaq_titiqqat->kasuqsimaniq_aulattivik ? qimiaq_titiqqat->kasuqsimaniq_aulattivik->local_port : qimiaq_titiqqat->전문제어 ? qimiaq_titiqqat->전문제어->local_port : 0; }
unsigned 상대접속번호(int ini_nuuttarut) { 통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); return qimiaq_titiqqat ? qimiaq_titiqqat->상대창구번호 : 0; }
uint32_t 상대통신주소(int ini_nuuttarut) { 통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); return qimiaq_titiqqat ? qimiaq_titiqqat->ilagijaujuq_turaarut : 0; }
void matuli_Kasuqatigiitsimajut(int ini_nuuttarut) {
    통신끝점 *qimiaq_titiqqat = 얻기(ini_nuuttarut); if (!qimiaq_titiqqat) return;
    if (qimiaq_titiqqat->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].qanuittuuninga_Ataqatigiivvik && 통신끝점들[순번].대기중 == ini_nuuttarut) matuli_Kasuqatigiitsimajut(순번);
    if (qimiaq_titiqqat->kasuqsimaniq_aulattivik) {
        tcp_arg(qimiaq_titiqqat->kasuqsimaniq_aulattivik, 0); if (qimiaq_titiqqat->수신창구) tcp_accept(qimiaq_titiqqat->kasuqsimaniq_aulattivik, 0); else { tcp_recv(qimiaq_titiqqat->kasuqsimaniq_aulattivik, 0); tcp_err(qimiaq_titiqqat->kasuqsimaniq_aulattivik, 0); }
        if (tcp_close(qimiaq_titiqqat->kasuqsimaniq_aulattivik) != ERR_OK) tcp_abort(qimiaq_titiqqat->kasuqsimaniq_aulattivik);
    }
    if (qimiaq_titiqqat->전문제어) udp_remove(qimiaq_titiqqat->전문제어); qimiaq_titiqqat->qanuittuuninga_Ataqatigiivvik = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&kasuqsimaniq_sunakkutaaq);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (기계저장기(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned immikkuuqtumut_nalunaikkut = 기계저장기(보조장치 + 0x40) & 255;
        if (immikkuuqtumut_nalunaikkut == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (kasuqsimaniq_sunakkutaaq.input(자료위치, &kasuqsimaniq_sunakkutaaq) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (immikkuuqtumut_nalunaikkut == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (immikkuuqtumut_nalunaikkut != 220 && immikkuuqtumut_nalunaikkut != 221) 수신오류 = 1; immikkuuqtumut_nalunaikkut = immikkuuqtumut_nalunaikkut == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = immikkuuqtumut_nalunaikkut; else 수신오류 = 1;
        }
    }
    netif_poll(&kasuqsimaniq_sunakkutaaq); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (기계저장기(보조장치 + 0x54) & 0x20); 처리한도++) {
        기계저장기(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* 설정·조회는 lwIP의 taannallarik_titiqqat 인터페이스와 isulittuq_puinti 표를 사용한다. */
uint32_t 망상태읽기(unsigned Iliniku_atuutilik, unsigned nalunaiqsimavik) {
    if(Iliniku_atuutilik==20)return 유선사용;
    if(Iliniku_atuutilik==21)return 준비됨&&netif_is_link_up(&kasuqsimaniq_sunakkutaaq);
    if(Iliniku_atuutilik==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&Iliniku_atuutilik>=4&&Iliniku_atuutilik<=8)return 유선망집계(Iliniku_atuutilik-4);
    if (Iliniku_atuutilik == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kasuqsimaniq_sunakkutaaq)));
    if (Iliniku_atuutilik == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&kasuqsimaniq_sunakkutaaq)));
    if (Iliniku_atuutilik == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&kasuqsimaniq_sunakkutaaq)));
    if (Iliniku_atuutilik == 3) return netif_is_up(&kasuqsimaniq_sunakkutaaq) != 0;
    if (Iliniku_atuutilik == 4) return 받은전문수;
    if (Iliniku_atuutilik == 5) return 보낸전문수;
    if (Iliniku_atuutilik == 6) return 받은바이트수;
    if (Iliniku_atuutilik == 7) return 보낸바이트수;
    if (Iliniku_atuutilik == 8) return 버린전문수;
    if (Iliniku_atuutilik == 9) return 송신개수;
    if (nalunaiqsimavik >= 32) return 0;
    통신끝점 *isulittuq_puinti = &통신끝점들[nalunaiqsimavik];
    if (Iliniku_atuutilik == 10) return isulittuq_puinti->qanuittuuninga_Ataqatigiivvik;
    if (!isulittuq_puinti->qanuittuuninga_Ataqatigiivvik) return 0;
    if (Iliniku_atuutilik == 11) return 통신접속번호(nalunaiqsimavik);
    if (Iliniku_atuutilik == 12) return isulittuq_puinti->ilagijaujuq_turaarut;
    if (Iliniku_atuutilik == 13) return isulittuq_puinti->상대창구번호;
    if (Iliniku_atuutilik == 14) return isulittuq_puinti->수신창구 ? 1 : isulittuq_puinti->ini_isulittuq ? 3 : isulittuq_puinti->tammarniq ? 4 : isulittuq_puinti->연결됨 ? 2 : 0;
    if (Iliniku_atuutilik == 15) return isulittuq_puinti->항목수;
    if (Iliniku_atuutilik == 16) {
        const ip_addr_t *turaarut = isulittuq_puinti->qanuittuuninga_Ataqatigiivvik == 1 && isulittuq_puinti->kasuqsimaniq_aulattivik ? &isulittuq_puinti->kasuqsimaniq_aulattivik->local_ip :
            isulittuq_puinti->qanuittuuninga_Ataqatigiivvik == 2 && isulittuq_puinti->전문제어 ? &isulittuq_puinti->전문제어->local_ip : 0;
        return turaarut ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(turaarut))) : 0;
    }
    return 0;
}

int qarasaujarmut_aaqqissurli_Kasuqatigiitsimajut(unsigned sugiarut, uint32_t turaarut, uint32_t kiinappak_atuutilik, uint32_t aqqusiurut_atuutilik) {
    if (!준비됨) return -100;
    if (sugiarut == 1) { netif_set_up(&kasuqsimaniq_sunakkutaaq); return 0; }
    if (sugiarut == 2) { netif_set_down(&kasuqsimaniq_sunakkutaaq); return 0; }
    if (sugiarut != 0) return -22;
    /* 유니캐스트 IPv4, 연속 kiinappak_atuutilik, 같은 망의 선택적 Aturniliuvagiiqtut aqqusiurut_atuutilik. */
    uint32_t 뒤집은가림 = ~kiinappak_atuutilik;
    if (!kiinappak_atuutilik || (뒤집은가림 & (뒤집은가림 + 1)) || !turaarut || (turaarut >> 24) == 127 ||
        (turaarut >> 24) == 0 || (turaarut >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(turaarut & 뒤집은가림) || (turaarut & 뒤집은가림) == 뒤집은가림)) ||
        (aqqusiurut_atuutilik && ((aqqusiurut_atuutilik & kiinappak_atuutilik) != (turaarut & kiinappak_atuutilik) || aqqusiurut_atuutilik == turaarut || (aqqusiurut_atuutilik >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(aqqusiurut_atuutilik & 뒤집은가림) || (aqqusiurut_atuutilik & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 turaarut 변경으로 몰래 끊지 않는다. */
    for (unsigned nalunaiqsimavik = 0; nalunaiqsimavik < 32; nalunaiqsimavik++) if (통신끝점들[nalunaiqsimavik].qanuittuuninga_Ataqatigiivvik &&
        !(통신끝점들[nalunaiqsimavik].수신창구 && 통신끝점들[nalunaiqsimavik].kasuqsimaniq_aulattivik && ip_addr_isany(&통신끝점들[nalunaiqsimavik].kasuqsimaniq_aulattivik->local_ip))) return -16;
    if(유선사용)dhcp_stop(&kasuqsimaniq_sunakkutaaq);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(turaarut)); ip4_addr_set_u32(&새가림, lwip_htonl(kiinappak_atuutilik)); ip4_addr_set_u32(&새관문, lwip_htonl(aqqusiurut_atuutilik));
    netif_set_addr(&kasuqsimaniq_sunakkutaaq, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *isulittuq_puinti, struct pbuf *titiqqat, const ip_addr_t *turaarut) {
    (void)인수; (void)isulittuq_puinti;
    unsigned char 머리[20], 응답[16];
    if (응답상태 != -11 || titiqqat->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(turaarut))) != 시험주소 || pbuf_copy_partial(titiqqat, 머리, 20, 0) != 20) return 0;
    unsigned Taijaugusinga_anininga = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Taijaugusinga_anininga < 20 || titiqqat->tot_len < Taijaugusinga_anininga + 16 ||
        pbuf_copy_partial(titiqqat, 응답, 16, Taijaugusinga_anininga) != 16 || 응답[0] || 응답[1] ||
        (((unsigned)응답[4] << 8) | 응답[5]) != 시험식별자 ||
        (((unsigned)응답[6] << 8) | 응답[7]) != 시험순서 ||
        응답[8] != 'J' || 응답[9] != 'K' || 응답[10] != 'O' || 응답[11] != 'S' ||
        (((uint32_t)응답[12] << 24) | ((uint32_t)응답[13] << 16) | ((uint32_t)응답[14] << 8) | 응답[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(titiqqat, Taijaugusinga_anininga)) return 0;
    if (inet_chksum_pbuf(titiqqat)) { pbuf_add_header(titiqqat, Taijaugusinga_anininga); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(titiqqat); return 1;
}
int 응답시험시작(uint32_t turaarut, unsigned agguijjut_atuutilik) {
    if (!준비됨 || !netif_is_up(&kasuqsimaniq_sunakkutaaq)) return -100;
    if (!turaarut || (turaarut >> 28) >= 14 || turaarut == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = turaarut; 시험순서 = agguijjut_atuutilik & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char titiqqat[32] = {8,0,0,0};
    titiqqat[4] = 시험식별자 >> 8; titiqqat[5] = 시험식별자; titiqqat[6] = 시험순서 >> 8; titiqqat[7] = 시험순서;
    titiqqat[8]='J'; titiqqat[9]='K'; titiqqat[10]='O'; titiqqat[11]='S';
    titiqqat[12]=시험시각 >> 24; titiqqat[13]=시험시각 >> 16; titiqqat[14]=시험시각 >> 8; titiqqat[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(titiqqat); 자리++) titiqqat[자리] = 자리;
    uint16_t 확인합 = inet_chksum(titiqqat, sizeof(titiqqat)); memcpy(titiqqat + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(titiqqat), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, titiqqat, sizeof(titiqqat)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(turaarut));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned Iliniku_atuutilik) {
    통신망살피기();
    return Iliniku_atuutilik == 0 ? 응답상태 : Iliniku_atuutilik == 1 ? (int)응답시간 : Iliniku_atuutilik == 2 ? (int)응답차례 : -22;
}
