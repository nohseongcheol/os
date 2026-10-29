#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Netweke_kgoboko.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../ya_kgole_boleng/ya_kgole_boleng.h"
#include "ya_mathale_Netweke.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define motšhene_ngwadiša(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif kgokaganya_sedirišwa;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int thaepa_legoro, 수신창구, 대기중, 연결됨, faele_fetša, Phošo;
    struct tcp_pcb *kgokaganya_taolo;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], sedirišwa_sa_legoro_le_tee_atrese;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int faele_tshwaro) { return faele_tshwaro >= 0 && faele_tshwaro < 32 && 통신끝점들[faele_tshwaro].thaepa_legoro ? &통신끝점들[faele_tshwaro] : 0; }
static int 예약하기(int thaepa_legoro) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].thaepa_legoro) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].thaepa_legoro = thaepa_legoro; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned khouto_ya_tlhaka) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = khouto_ya_tlhaka; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *atrese) {
    (void)개수; (void)atrese;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned khouto_ya_tlhaka = ((unsigned char *)다음위치->payload)[순번];
        if (khouto_ya_tlhaka == 192 || khouto_ya_tlhaka == 219) { 내보내기(219); 내보내기(khouto_ya_tlhaka == 192 ? 220 : 221); } else 내보내기(khouto_ya_tlhaka);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t Lokišetša_lebakanako_la_polelotlwaelwa(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Lokišetša_Netweke(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    motšhene_ngwadiša(보조장치 + 4) |= 1; motšhene_ngwadiša(보조장치 + 0x60) = 0; motšhene_ngwadiša(보조장치 + 0x44) = 0;
    motšhene_ngwadiša(보조장치 + 0x48) = 0xc6; motšhene_ngwadiša(보조장치 + 0x4c) = 3; motšhene_ngwadiša(보조장치 + 0x68) = 270; motšhene_ngwadiša(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t atrese_ya_Inthanete, paente_maseke, tsela_ya_netweke_atrese;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&atrese_ya_Inthanete, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&paente_maseke, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&tsela_ya_netweke_atrese, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&kgokaganya_sedirišwa, &atrese_ya_Inthanete, &paente_maseke, &tsela_ya_netweke_atrese, 0, 유선사용?Lokišetša_ya_mathale_Netweke:Lokišetša_lebakanako_la_polelotlwaelwa, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&kgokaganya_sedirišwa); netif_set_up(&kgokaganya_sedirišwa);if(!유선사용)netif_set_link_up(&kgokaganya_sedirišwa); 준비됨 = 1;
    Lokišetša_ya_kgole();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *phetišetšo_taolo_thibela, struct pbuf *자료위치, err_t Phošo) {
    통신끝점 *molokoloko_data = 부가인수; (void)phetišetšo_taolo_thibela; (void)Phošo;
    if (!자료위치) { molokoloko_data->faele_fetša = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(molokoloko_data->data) - molokoloko_data->항목수) return ERR_MEM;
    unsigned 현재위치 = (molokoloko_data->맨앞 + molokoloko_data->항목수) % sizeof(molokoloko_data->data);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        molokoloko_data->data[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(molokoloko_data->data);
    }
    molokoloko_data->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Phošo) { 통신끝점 *molokoloko_data = 부가인수; molokoloko_data->kgokaganya_taolo = 0; molokoloko_data->Phošo = 오류번호(Phošo); }
static void 되부름목록(통신끝점 *molokoloko_data) { tcp_arg(molokoloko_data->kgokaganya_taolo, molokoloko_data); tcp_recv(molokoloko_data->kgokaganya_taolo, 수신됨); tcp_err(molokoloko_data->kgokaganya_taolo, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *phetišetšo_taolo_thibela, err_t Phošo) {
    통신끝점 *molokoloko_data = 부가인수; (void)phetišetšo_taolo_thibela; if (Phošo) molokoloko_data->Phošo = 오류번호(Phošo); else molokoloko_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *phetišetšo_taolo_thibela, err_t Phošo) {
    통신끝점 *부모항목 = 부가인수; if (Phošo) return Phošo;
    int faele_tshwaro = 예약하기(1); if (faele_tshwaro < 0) return ERR_MEM;
    통신끝점 *molokoloko_data = &통신끝점들[faele_tshwaro]; molokoloko_data->kgokaganya_taolo = phetišetšo_taolo_thibela; molokoloko_data->연결됨 = 1; molokoloko_data->대기중 = (int)(부모항목 - 통신끝점들);
    molokoloko_data->sedirišwa_sa_legoro_le_tee_atrese = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&phetišetšo_taolo_thibela->remote_ip))); molokoloko_data->상대창구번호 = phetišetšo_taolo_thibela->remote_port;
    되부름목록(molokoloko_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *phetišetšo_taolo_thibela, struct pbuf *자료위치, const ip_addr_t *atrese, u16_t 접속번호) {
    통신끝점 *molokoloko_data = 부가인수; (void)phetišetšo_taolo_thibela;
    if (molokoloko_data->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (molokoloko_data->맨앞 + molokoloko_data->항목수) % 4;
        pbuf_copy_partial(자료위치, molokoloko_data->data + 자리 * 512, 자료위치->tot_len, 0);
        molokoloko_data->길이목록[자리] = 자료위치->tot_len; molokoloko_data->접속번호들[자리] = 접속번호;
        molokoloko_data->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(atrese))); molokoloko_data->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int thaepa_legoro) {
    if (!준비됨) return -100;
    if (thaepa_legoro != 1 && thaepa_legoro != 2) return -93;
    int faele_tshwaro = 예약하기(thaepa_legoro); if (faele_tshwaro < 0) return faele_tshwaro;
    통신끝점 *molokoloko_data = &통신끝점들[faele_tshwaro];
    if (thaepa_legoro == 1) { molokoloko_data->kgokaganya_taolo = tcp_new(); if (molokoloko_data->kgokaganya_taolo) 되부름목록(molokoloko_data); }
    else { molokoloko_data->전문제어 = udp_new(); if (molokoloko_data->전문제어) udp_recv(molokoloko_data->전문제어, 전문, molokoloko_data); }
    if (!molokoloko_data->kgokaganya_taolo && !molokoloko_data->전문제어) { molokoloko_data->thaepa_legoro = 0; return -12; } return faele_tshwaro;
}
int 망주소묶기(int faele_tshwaro, uint32_t atrese, unsigned 접속번호) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data) return -9;
    if (접속번호 > 65535 || (atrese && atrese != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kgokaganya_sedirišwa))) && atrese != 0x7f000001)) return -99;
    ip_addr_t atrese_ya_Inthanete; ip_addr_set_ip4_u32(&atrese_ya_Inthanete, lwip_htonl(atrese));
    err_t 보조항목 = molokoloko_data->thaepa_legoro == 1 ? tcp_bind(molokoloko_data->kgokaganya_taolo, &atrese_ya_Inthanete, 접속번호) : udp_bind(molokoloko_data->전문제어, &atrese_ya_Inthanete, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int faele_tshwaro) { 통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (molokoloko_data && molokoloko_data->kgokaganya_taolo) ip_set_option(molokoloko_data->kgokaganya_taolo, SOF_REUSEADDR); }
int 연결기다리기(int faele_tshwaro) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data || molokoloko_data->thaepa_legoro != 1) return -9;
    if (molokoloko_data->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *phetišetšo_taolo_thibela = tcp_listen_with_backlog_and_err(molokoloko_data->kgokaganya_taolo, 4, &보조항목);
    if (!phetišetšo_taolo_thibela) return 오류번호(보조항목); molokoloko_data->kgokaganya_taolo = phetišetšo_taolo_thibela; molokoloko_data->수신창구 = 1; tcp_arg(phetišetšo_taolo_thibela, molokoloko_data); tcp_accept(phetišetšo_taolo_thibela, 연결받음); return 0;
}
int 망연결하기(int faele_tshwaro, uint32_t atrese, unsigned 접속번호) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data || molokoloko_data->thaepa_legoro != 1) return -9;
    if (molokoloko_data->Phošo) return molokoloko_data->Phošo;
    if (molokoloko_data->연결됨) return 0;
    if (molokoloko_data->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !atrese) return -22;
    ip_addr_t atrese_ya_Inthanete; ip_addr_set_ip4_u32(&atrese_ya_Inthanete, lwip_htonl(atrese));
    molokoloko_data->sedirišwa_sa_legoro_le_tee_atrese = atrese; molokoloko_data->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(molokoloko_data->kgokaganya_taolo, &atrese_ya_Inthanete, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int faele_tshwaro) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data || !molokoloko_data->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].thaepa_legoro == 1 && 통신끝점들[순번].대기중 == faele_tshwaro) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int faele_tshwaro, void *data, unsigned 개수) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data || molokoloko_data->thaepa_legoro != 1) return -9;
    if (!개수) return 0; if (!molokoloko_data->항목수) return molokoloko_data->Phošo ? molokoloko_data->Phošo : molokoloko_data->faele_fetša ? 0 : -11;
    if (개수 > molokoloko_data->항목수) 개수 = molokoloko_data->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)data)[순번] = molokoloko_data->data[molokoloko_data->맨앞]; molokoloko_data->맨앞 = (molokoloko_data->맨앞 + 1) % sizeof(molokoloko_data->data); }
    molokoloko_data->항목수 -= 개수; if (molokoloko_data->kgokaganya_taolo) tcp_recved(molokoloko_data->kgokaganya_taolo, 개수); return 개수;
}
int 통신쓰기(int faele_tshwaro, const void *data, unsigned 개수) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data || molokoloko_data->thaepa_legoro != 1) return -9;
    if (molokoloko_data->Phošo) return molokoloko_data->Phošo; if (!molokoloko_data->kgokaganya_taolo || !molokoloko_data->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(molokoloko_data->kgokaganya_taolo)) 개수 = tcp_sndbuf(molokoloko_data->kgokaganya_taolo);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(molokoloko_data->kgokaganya_taolo, data, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(molokoloko_data->kgokaganya_taolo); return 개수;
}
int 전문보내기(int faele_tshwaro, const void *data, unsigned 개수, uint32_t atrese, unsigned 접속번호) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data || molokoloko_data->thaepa_legoro != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, data, 개수); ip_addr_t atrese_ya_Inthanete; ip_addr_set_ip4_u32(&atrese_ya_Inthanete, lwip_htonl(atrese));
    err_t 보조항목 = udp_sendto(molokoloko_data->전문제어, 자료위치, &atrese_ya_Inthanete, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int faele_tshwaro, void *data, unsigned 개수) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data || molokoloko_data->thaepa_legoro != 2) return -9;
    if (!molokoloko_data->항목수) return -11; unsigned 현재위치 = molokoloko_data->맨앞;
    if (개수 > molokoloko_data->길이목록[현재위치]) 개수 = molokoloko_data->길이목록[현재위치]; memcpy(data, molokoloko_data->data + 현재위치 * 512, 개수);
    molokoloko_data->상대창구번호 = molokoloko_data->접속번호들[현재위치]; molokoloko_data->sedirišwa_sa_legoro_le_tee_atrese = molokoloko_data->주소목록[현재위치]; molokoloko_data->맨앞 = (현재위치 + 1) % 4; molokoloko_data->항목수--; return 개수;
}
unsigned 통신접속번호(int faele_tshwaro) { 통신끝점 *molokoloko_data = 얻기(faele_tshwaro); return !molokoloko_data ? 0 : molokoloko_data->kgokaganya_taolo ? molokoloko_data->kgokaganya_taolo->local_port : molokoloko_data->전문제어 ? molokoloko_data->전문제어->local_port : 0; }
unsigned 상대접속번호(int faele_tshwaro) { 통신끝점 *molokoloko_data = 얻기(faele_tshwaro); return molokoloko_data ? molokoloko_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int faele_tshwaro) { 통신끝점 *molokoloko_data = 얻기(faele_tshwaro); return molokoloko_data ? molokoloko_data->sedirišwa_sa_legoro_le_tee_atrese : 0; }
void tswalela_Netweke(int faele_tshwaro) {
    통신끝점 *molokoloko_data = 얻기(faele_tshwaro); if (!molokoloko_data) return;
    if (molokoloko_data->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].thaepa_legoro && 통신끝점들[순번].대기중 == faele_tshwaro) tswalela_Netweke(순번);
    if (molokoloko_data->kgokaganya_taolo) {
        tcp_arg(molokoloko_data->kgokaganya_taolo, 0); if (molokoloko_data->수신창구) tcp_accept(molokoloko_data->kgokaganya_taolo, 0); else { tcp_recv(molokoloko_data->kgokaganya_taolo, 0); tcp_err(molokoloko_data->kgokaganya_taolo, 0); }
        if (tcp_close(molokoloko_data->kgokaganya_taolo) != ERR_OK) tcp_abort(molokoloko_data->kgokaganya_taolo);
    }
    if (molokoloko_data->전문제어) udp_remove(molokoloko_data->전문제어); molokoloko_data->thaepa_legoro = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&kgokaganya_sedirišwa);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (motšhene_ngwadiša(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned khouto_ya_tlhaka = motšhene_ngwadiša(보조장치 + 0x40) & 255;
        if (khouto_ya_tlhaka == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (kgokaganya_sedirišwa.input(자료위치, &kgokaganya_sedirišwa) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (khouto_ya_tlhaka == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (khouto_ya_tlhaka != 220 && khouto_ya_tlhaka != 221) 수신오류 = 1; khouto_ya_tlhaka = khouto_ya_tlhaka == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = khouto_ya_tlhaka; else 수신오류 = 1;
        }
    }
    netif_poll(&kgokaganya_sedirišwa); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (motšhene_ngwadiša(보조장치 + 0x54) & 0x20); 처리한도++) {
        motšhene_ngwadiša(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Dipeakanyo·조회는 lwIP의 kgonthe_data 인터페이스와 fetša_ntlha 표를 사용한다. */
uint32_t 망상태읽기(unsigned go_tsenya_tshedimošo_boleng, unsigned lokela) {
    if(go_tsenya_tshedimošo_boleng==20)return 유선사용;
    if(go_tsenya_tshedimošo_boleng==21)return 준비됨&&netif_is_link_up(&kgokaganya_sedirišwa);
    if(go_tsenya_tshedimošo_boleng==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&go_tsenya_tshedimošo_boleng>=4&&go_tsenya_tshedimošo_boleng<=8)return 유선망집계(go_tsenya_tshedimošo_boleng-4);
    if (go_tsenya_tshedimošo_boleng == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kgokaganya_sedirišwa)));
    if (go_tsenya_tshedimošo_boleng == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&kgokaganya_sedirišwa)));
    if (go_tsenya_tshedimošo_boleng == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&kgokaganya_sedirišwa)));
    if (go_tsenya_tshedimošo_boleng == 3) return netif_is_up(&kgokaganya_sedirišwa) != 0;
    if (go_tsenya_tshedimošo_boleng == 4) return 받은전문수;
    if (go_tsenya_tshedimošo_boleng == 5) return 보낸전문수;
    if (go_tsenya_tshedimošo_boleng == 6) return 받은바이트수;
    if (go_tsenya_tshedimošo_boleng == 7) return 보낸바이트수;
    if (go_tsenya_tshedimošo_boleng == 8) return 버린전문수;
    if (go_tsenya_tshedimošo_boleng == 9) return 송신개수;
    if (lokela >= 32) return 0;
    통신끝점 *fetša_ntlha = &통신끝점들[lokela];
    if (go_tsenya_tshedimošo_boleng == 10) return fetša_ntlha->thaepa_legoro;
    if (!fetša_ntlha->thaepa_legoro) return 0;
    if (go_tsenya_tshedimošo_boleng == 11) return 통신접속번호(lokela);
    if (go_tsenya_tshedimošo_boleng == 12) return fetša_ntlha->sedirišwa_sa_legoro_le_tee_atrese;
    if (go_tsenya_tshedimošo_boleng == 13) return fetša_ntlha->상대창구번호;
    if (go_tsenya_tshedimošo_boleng == 14) return fetša_ntlha->수신창구 ? 1 : fetša_ntlha->faele_fetša ? 3 : fetša_ntlha->Phošo ? 4 : fetša_ntlha->연결됨 ? 2 : 0;
    if (go_tsenya_tshedimošo_boleng == 15) return fetša_ntlha->항목수;
    if (go_tsenya_tshedimošo_boleng == 16) {
        const ip_addr_t *atrese = fetša_ntlha->thaepa_legoro == 1 && fetša_ntlha->kgokaganya_taolo ? &fetša_ntlha->kgokaganya_taolo->local_ip :
            fetša_ntlha->thaepa_legoro == 2 && fetša_ntlha->전문제어 ? &fetša_ntlha->전문제어->local_ip : 0;
        return atrese ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(atrese))) : 0;
    }
    return 0;
}

int lomaganya_Netweke(unsigned Mogato, uint32_t atrese, uint32_t maseke_boleng, uint32_t tsela_ya_netweke_boleng) {
    if (!준비됨) return -100;
    if (Mogato == 1) { netif_set_up(&kgokaganya_sedirišwa); return 0; }
    if (Mogato == 2) { netif_set_down(&kgokaganya_sedirišwa); return 0; }
    if (Mogato != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maseke_boleng, 같은 망의 선택적 setsenywa_sa_tirelwa tsela_ya_netweke_boleng. */
    uint32_t 뒤집은가림 = ~maseke_boleng;
    if (!maseke_boleng || (뒤집은가림 & (뒤집은가림 + 1)) || !atrese || (atrese >> 24) == 127 ||
        (atrese >> 24) == 0 || (atrese >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(atrese & 뒤집은가림) || (atrese & 뒤집은가림) == 뒤집은가림)) ||
        (tsela_ya_netweke_boleng && ((tsela_ya_netweke_boleng & maseke_boleng) != (atrese & maseke_boleng) || tsela_ya_netweke_boleng == atrese || (tsela_ya_netweke_boleng >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(tsela_ya_netweke_boleng & 뒤집은가림) || (tsela_ya_netweke_boleng & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 atrese 변경으로 몰래 끊지 않는다. */
    for (unsigned lokela = 0; lokela < 32; lokela++) if (통신끝점들[lokela].thaepa_legoro &&
        !(통신끝점들[lokela].수신창구 && 통신끝점들[lokela].kgokaganya_taolo && ip_addr_isany(&통신끝점들[lokela].kgokaganya_taolo->local_ip))) return -16;
    if(유선사용)dhcp_stop(&kgokaganya_sedirišwa);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(atrese)); ip4_addr_set_u32(&새가림, lwip_htonl(maseke_boleng)); ip4_addr_set_u32(&새관문, lwip_htonl(tsela_ya_netweke_boleng));
    netif_set_addr(&kgokaganya_sedirišwa, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *fetša_ntlha, struct pbuf *data, const ip_addr_t *atrese) {
    (void)인수; (void)fetša_ntlha;
    unsigned char 머리[20], fetola[16];
    if (응답상태 != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(atrese))) != 시험주소 || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Hlogo_bogolo = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Hlogo_bogolo < 20 || data->tot_len < Hlogo_bogolo + 16 ||
        pbuf_copy_partial(data, fetola, 16, Hlogo_bogolo) != 16 || fetola[0] || fetola[1] ||
        (((unsigned)fetola[4] << 8) | fetola[5]) != 시험식별자 ||
        (((unsigned)fetola[6] << 8) | fetola[7]) != 시험순서 ||
        fetola[8] != 'J' || fetola[9] != 'K' || fetola[10] != 'O' || fetola[11] != 'S' ||
        (((uint32_t)fetola[12] << 24) | ((uint32_t)fetola[13] << 16) | ((uint32_t)fetola[14] << 8) | fetola[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Hlogo_bogolo)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Hlogo_bogolo); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(data); return 1;
}
int 응답시험시작(uint32_t atrese, unsigned thulaganyo_boleng) {
    if (!준비됨 || !netif_is_up(&kgokaganya_sedirišwa)) return -100;
    if (!atrese || (atrese >> 28) >= 14 || atrese == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = atrese; 시험순서 = thulaganyo_boleng & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = 시험순서 >> 8; data[7] = 시험순서;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=시험시각 >> 24; data[13]=시험시각 >> 16; data[14]=시험시각 >> 8; data[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(data); 자리++) data[자리] = 자리;
    uint16_t 확인합 = inet_chksum(data, sizeof(data)); memcpy(data + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(atrese));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned go_tsenya_tshedimošo_boleng) {
    통신망살피기();
    return go_tsenya_tshedimošo_boleng == 0 ? 응답상태 : go_tsenya_tshedimošo_boleng == 1 ? (int)응답시간 : go_tsenya_tshedimošo_boleng == 2 ? (int)응답차례 : -22;
}
