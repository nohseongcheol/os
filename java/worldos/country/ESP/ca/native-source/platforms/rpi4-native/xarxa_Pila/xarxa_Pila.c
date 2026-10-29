#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "xarxa_Pila.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../remot_VALOR/remot_VALOR.h"
#include "per_cable_xarxa.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define màquina_registrar_se(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif connexió_dispositiu;
static int 준비됨, 살피는중;
static int ús_per_cable_xarxa;
static unsigned 수신사용량, 수신탈출, rebre_error;
static unsigned char rebre_memòria_intermèdia_de_dades[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, CANTIDAD_RECIBIDA_byte_COMPT, 보낸바이트수, 버린전문수;
typedef struct {
    int TIPUS_Categoria, rebre_port, tecnologies_de_la_informació_pendent, 연결됨, arxiu_finalitzar, s_ha_produït_un_error;
    struct tcp_pcb *connexió_control;
    struct udp_pcb *전문제어;
    unsigned frontal_introducció, introducció_COMPT;
    unsigned char dades[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], homòleg_ADREÇA;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int número_d_error(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *obtenir_VALOR(int arxiu_control_7f4cdfd5) { return arxiu_control_7f4cdfd5 >= 0 && arxiu_control_7f4cdfd5 < 32 && 통신끝점들[arxiu_control_7f4cdfd5].TIPUS_Categoria ? &통신끝점들[arxiu_control_7f4cdfd5] : 0; }
static int 예약하기(int TIPUS_Categoria) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TIPUS_Categoria) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TIPUS_Categoria = TIPUS_Categoria; 통신끝점들[순번].tecnologies_de_la_informació_pendent = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned codi_de_caràcter) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = codi_de_caràcter; }
static err_t 출력결과(struct netif *element_COMPT, struct pbuf *dades_càrrec, const ip4_addr_t *Adreça) {
    (void)element_COMPT; (void)Adreça;
    if (dades_càrrec->tot_len > 1500 || 송신개수 + 2 * dades_càrrec->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Següent_DESPLAÇAMENT = dades_càrrec; Següent_DESPLAÇAMENT; Següent_DESPLAÇAMENT = Següent_DESPLAÇAMENT->next) for (unsigned 순번 = 0; 순번 < Següent_DESPLAÇAMENT->len; 순번++) {
        unsigned codi_de_caràcter = ((unsigned char *)Següent_DESPLAÇAMENT->payload)[순번];
        if (codi_de_caràcter == 192 || codi_de_caràcter == 219) { 내보내기(219); 내보내기(codi_de_caràcter == 192 ? 220 : 221); } else 내보내기(codi_de_caràcter);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += dades_càrrec->tot_len; return ERR_OK;
}
static err_t 준비하기(struct netif *element_COMPT) { element_COMPT->name[0] = 's'; element_COMPT->name[1] = 'l'; element_COMPT->mtu = 1500; element_COMPT->output = 출력결과; return ERR_OK; }
void Prepara_xarxa(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    màquina_registrar_se(보조장치 + 4) |= 1; màquina_registrar_se(보조장치 + 0x60) = 0; màquina_registrar_se(보조장치 + 0x44) = 0;
    màquina_registrar_se(보조장치 + 0x48) = 0xc6; màquina_registrar_se(보조장치 + 0x4c) = 3; màquina_registrar_se(보조장치 + 0x68) = 270; màquina_registrar_se(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t adreça_d_Internet, màscara_de_bits, passarel_la_ADREÇA;
    ús_per_cable_xarxa=유선장치있음();
    ip4_addr_set_u32(&adreça_d_Internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&màscara_de_bits, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&passarel_la_ADREÇA, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&connexió_dispositiu, &adreça_d_Internet, &màscara_de_bits, &passarel_la_ADREÇA, 0, ús_per_cable_xarxa?Prepara_per_cable_xarxa:준비하기, ús_per_cable_xarxa?ethernet_input:ip4_input))return;
    netif_set_default(&connexió_dispositiu); netif_set_up(&connexió_dispositiu);if(!ús_per_cable_xarxa)netif_set_link_up(&connexió_dispositiu); 준비됨 = 1;
    Prepara_remot();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *transmissió_control_bloquejar, struct pbuf *dades_càrrec, err_t s_ha_produït_un_error) {
    통신끝점 *cadena_dades = 부가인수; (void)transmissió_control_bloquejar; (void)s_ha_produït_un_error;
    if (!dades_càrrec) { cadena_dades->arxiu_finalitzar = 1; return ERR_OK; }
    if (dades_càrrec->tot_len > sizeof(cadena_dades->dades) - cadena_dades->introducció_COMPT) return ERR_MEM;
    unsigned 현재위치 = (cadena_dades->frontal_introducció + cadena_dades->introducció_COMPT) % sizeof(cadena_dades->dades);
    for (struct pbuf *Següent_DESPLAÇAMENT = dades_càrrec; Següent_DESPLAÇAMENT; Següent_DESPLAÇAMENT = Següent_DESPLAÇAMENT->next) for (unsigned 순번 = 0; 순번 < Següent_DESPLAÇAMENT->len; 순번++) {
        cadena_dades->dades[현재위치] = ((unsigned char *)Següent_DESPLAÇAMENT->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(cadena_dades->dades);
    }
    cadena_dades->introducció_COMPT += dades_càrrec->tot_len; pbuf_free(dades_càrrec); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t s_ha_produït_un_error) { 통신끝점 *cadena_dades = 부가인수; cadena_dades->connexió_control = 0; cadena_dades->s_ha_produït_un_error = número_d_error(s_ha_produït_un_error); }
static void 되부름목록(통신끝점 *cadena_dades) { tcp_arg(cadena_dades->connexió_control, cadena_dades); tcp_recv(cadena_dades->connexió_control, 수신됨); tcp_err(cadena_dades->connexió_control, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *transmissió_control_bloquejar, err_t s_ha_produït_un_error) {
    통신끝점 *cadena_dades = 부가인수; (void)transmissió_control_bloquejar; if (s_ha_produït_un_error) cadena_dades->s_ha_produït_un_error = número_d_error(s_ha_produït_un_error); else cadena_dades->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *transmissió_control_bloquejar, err_t s_ha_produït_un_error) {
    통신끝점 *부모항목 = 부가인수; if (s_ha_produït_un_error) return s_ha_produït_un_error;
    int arxiu_control_7f4cdfd5 = 예약하기(1); if (arxiu_control_7f4cdfd5 < 0) return ERR_MEM;
    통신끝점 *cadena_dades = &통신끝점들[arxiu_control_7f4cdfd5]; cadena_dades->connexió_control = transmissió_control_bloquejar; cadena_dades->연결됨 = 1; cadena_dades->tecnologies_de_la_informació_pendent = (int)(부모항목 - 통신끝점들);
    cadena_dades->homòleg_ADREÇA = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&transmissió_control_bloquejar->remote_ip))); cadena_dades->상대창구번호 = transmissió_control_bloquejar->remote_port;
    되부름목록(cadena_dades); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *transmissió_control_bloquejar, struct pbuf *dades_càrrec, const ip_addr_t *Adreça, u16_t número_de_port) {
    통신끝점 *cadena_dades = 부가인수; (void)transmissió_control_bloquejar;
    if (cadena_dades->introducció_COMPT < 4 && dades_càrrec->tot_len <= 512) {
        unsigned càrrec_INDEX = (cadena_dades->frontal_introducció + cadena_dades->introducció_COMPT) % 4;
        pbuf_copy_partial(dades_càrrec, cadena_dades->dades + càrrec_INDEX * 512, dades_càrrec->tot_len, 0);
        cadena_dades->길이목록[càrrec_INDEX] = dades_càrrec->tot_len; cadena_dades->접속번호들[càrrec_INDEX] = número_de_port;
        cadena_dades->주소목록[càrrec_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adreça))); cadena_dades->introducció_COMPT++;
    }
    pbuf_free(dades_càrrec);
}
int 통신끝점만들기(int TIPUS_Categoria) {
    if (!준비됨) return -100;
    if (TIPUS_Categoria != 1 && TIPUS_Categoria != 2) return -93;
    int arxiu_control_7f4cdfd5 = 예약하기(TIPUS_Categoria); if (arxiu_control_7f4cdfd5 < 0) return arxiu_control_7f4cdfd5;
    통신끝점 *cadena_dades = &통신끝점들[arxiu_control_7f4cdfd5];
    if (TIPUS_Categoria == 1) { cadena_dades->connexió_control = tcp_new(); if (cadena_dades->connexió_control) 되부름목록(cadena_dades); }
    else { cadena_dades->전문제어 = udp_new(); if (cadena_dades->전문제어) udp_recv(cadena_dades->전문제어, 전문, cadena_dades); }
    if (!cadena_dades->connexió_control && !cadena_dades->전문제어) { cadena_dades->TIPUS_Categoria = 0; return -12; } return arxiu_control_7f4cdfd5;
}
int 망주소묶기(int arxiu_control_7f4cdfd5, uint32_t Adreça, unsigned número_de_port) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades) return -9;
    if (número_de_port > 65535 || (Adreça && Adreça != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&connexió_dispositiu))) && Adreça != 0x7f000001)) return -99;
    ip_addr_t adreça_d_Internet; ip_addr_set_ip4_u32(&adreça_d_Internet, lwip_htonl(Adreça));
    err_t 보조항목 = cadena_dades->TIPUS_Categoria == 1 ? tcp_bind(cadena_dades->connexió_control, &adreça_d_Internet, número_de_port) : udp_bind(cadena_dades->전문제어, &adreça_d_Internet, número_de_port); return 보조항목 ? número_d_error(보조항목) : 0;
}
void 통신주소재사용(int arxiu_control_7f4cdfd5) { 통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (cadena_dades && cadena_dades->connexió_control) ip_set_option(cadena_dades->connexió_control, SOF_REUSEADDR); }
int 연결기다리기(int arxiu_control_7f4cdfd5) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades || cadena_dades->TIPUS_Categoria != 1) return -9;
    if (cadena_dades->rebre_port) return 0;
    err_t 보조항목; struct tcp_pcb *transmissió_control_bloquejar = tcp_listen_with_backlog_and_err(cadena_dades->connexió_control, 4, &보조항목);
    if (!transmissió_control_bloquejar) return número_d_error(보조항목); cadena_dades->connexió_control = transmissió_control_bloquejar; cadena_dades->rebre_port = 1; tcp_arg(transmissió_control_bloquejar, cadena_dades); tcp_accept(transmissió_control_bloquejar, 연결받음); return 0;
}
int 망연결하기(int arxiu_control_7f4cdfd5, uint32_t Adreça, unsigned número_de_port) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades || cadena_dades->TIPUS_Categoria != 1) return -9;
    if (cadena_dades->s_ha_produït_un_error) return cadena_dades->s_ha_produït_un_error;
    if (cadena_dades->연결됨) return 0;
    if (cadena_dades->상대창구번호) return -115;
    if (!número_de_port || número_de_port > 65535 || !Adreça) return -22;
    ip_addr_t adreça_d_Internet; ip_addr_set_ip4_u32(&adreça_d_Internet, lwip_htonl(Adreça));
    cadena_dades->homòleg_ADREÇA = Adreça; cadena_dades->상대창구번호 = número_de_port;
    err_t 보조항목 = tcp_connect(cadena_dades->connexió_control, &adreça_d_Internet, número_de_port, 연결됨); return 보조항목 ? número_d_error(보조항목) : -115;
}
int 망연결받기(int arxiu_control_7f4cdfd5) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades || !cadena_dades->rebre_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TIPUS_Categoria == 1 && 통신끝점들[순번].tecnologies_de_la_informació_pendent == arxiu_control_7f4cdfd5) { 통신끝점들[순번].tecnologies_de_la_informació_pendent = -1; return 순번; }
    return -11;
}
int 통신읽기(int arxiu_control_7f4cdfd5, void *dades, unsigned element_COMPT) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades || cadena_dades->TIPUS_Categoria != 1) return -9;
    if (!element_COMPT) return 0; if (!cadena_dades->introducció_COMPT) return cadena_dades->s_ha_produït_un_error ? cadena_dades->s_ha_produït_un_error : cadena_dades->arxiu_finalitzar ? 0 : -11;
    if (element_COMPT > cadena_dades->introducció_COMPT) element_COMPT = cadena_dades->introducció_COMPT;
    for (unsigned 순번 = 0; 순번 < element_COMPT; 순번++) { ((unsigned char *)dades)[순번] = cadena_dades->dades[cadena_dades->frontal_introducció]; cadena_dades->frontal_introducció = (cadena_dades->frontal_introducció + 1) % sizeof(cadena_dades->dades); }
    cadena_dades->introducció_COMPT -= element_COMPT; if (cadena_dades->connexió_control) tcp_recved(cadena_dades->connexió_control, element_COMPT); return element_COMPT;
}
int 통신쓰기(int arxiu_control_7f4cdfd5, const void *dades, unsigned element_COMPT) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades || cadena_dades->TIPUS_Categoria != 1) return -9;
    if (cadena_dades->s_ha_produït_un_error) return cadena_dades->s_ha_produït_un_error; if (!cadena_dades->connexió_control || !cadena_dades->연결됨) return -107;
    if (!element_COMPT) return 0; if (element_COMPT > tcp_sndbuf(cadena_dades->connexió_control)) element_COMPT = tcp_sndbuf(cadena_dades->connexió_control);
    if (!element_COMPT) return -11; if (element_COMPT > 1024) element_COMPT = 1024;
    err_t 보조항목 = tcp_write(cadena_dades->connexió_control, dades, element_COMPT, TCP_WRITE_FLAG_COPY); if (보조항목) return número_d_error(보조항목);
    tcp_output(cadena_dades->connexió_control); return element_COMPT;
}
int 전문보내기(int arxiu_control_7f4cdfd5, const void *dades, unsigned element_COMPT, uint32_t Adreça, unsigned número_de_port) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades || cadena_dades->TIPUS_Categoria != 2) return -9;
    if (element_COMPT > 512) return -90; if (!número_de_port || número_de_port > 65535) return -22;
    struct pbuf *dades_càrrec = pbuf_alloc(PBUF_TRANSPORT, element_COMPT, PBUF_RAM); if (!dades_càrrec) return -11;
    pbuf_take(dades_càrrec, dades, element_COMPT); ip_addr_t adreça_d_Internet; ip_addr_set_ip4_u32(&adreça_d_Internet, lwip_htonl(Adreça));
    err_t 보조항목 = udp_sendto(cadena_dades->전문제어, dades_càrrec, &adreça_d_Internet, número_de_port); pbuf_free(dades_càrrec); return 보조항목 ? número_d_error(보조항목) : (int)element_COMPT;
}
int 전문받기(int arxiu_control_7f4cdfd5, void *dades, unsigned element_COMPT) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades || cadena_dades->TIPUS_Categoria != 2) return -9;
    if (!cadena_dades->introducció_COMPT) return -11; unsigned 현재위치 = cadena_dades->frontal_introducció;
    if (element_COMPT > cadena_dades->길이목록[현재위치]) element_COMPT = cadena_dades->길이목록[현재위치]; memcpy(dades, cadena_dades->dades + 현재위치 * 512, element_COMPT);
    cadena_dades->상대창구번호 = cadena_dades->접속번호들[현재위치]; cadena_dades->homòleg_ADREÇA = cadena_dades->주소목록[현재위치]; cadena_dades->frontal_introducció = (현재위치 + 1) % 4; cadena_dades->introducció_COMPT--; return element_COMPT;
}
unsigned xarxa_número_de_port(int arxiu_control_7f4cdfd5) { 통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); return !cadena_dades ? 0 : cadena_dades->connexió_control ? cadena_dades->connexió_control->local_port : cadena_dades->전문제어 ? cadena_dades->전문제어->local_port : 0; }
unsigned homòleg_número_de_port(int arxiu_control_7f4cdfd5) { 통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); return cadena_dades ? cadena_dades->상대창구번호 : 0; }
uint32_t 상대통신주소(int arxiu_control_7f4cdfd5) { 통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); return cadena_dades ? cadena_dades->homòleg_ADREÇA : 0; }
void Tanca_xarxa(int arxiu_control_7f4cdfd5) {
    통신끝점 *cadena_dades = obtenir_VALOR(arxiu_control_7f4cdfd5); if (!cadena_dades) return;
    if (cadena_dades->rebre_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TIPUS_Categoria && 통신끝점들[순번].tecnologies_de_la_informació_pendent == arxiu_control_7f4cdfd5) Tanca_xarxa(순번);
    if (cadena_dades->connexió_control) {
        tcp_arg(cadena_dades->connexió_control, 0); if (cadena_dades->rebre_port) tcp_accept(cadena_dades->connexió_control, 0); else { tcp_recv(cadena_dades->connexió_control, 0); tcp_err(cadena_dades->connexió_control, 0); }
        if (tcp_close(cadena_dades->connexió_control) != ERR_OK) tcp_abort(cadena_dades->connexió_control);
    }
    if (cadena_dades->전문제어) udp_remove(cadena_dades->전문제어); cadena_dades->TIPUS_Categoria = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(ús_per_cable_xarxa)유선망살피기(&connexió_dispositiu);
    for (unsigned pressupost_assignat = 0; !ús_per_cable_xarxa && pressupost_assignat < 4096 && (màquina_registrar_se(보조장치 + 0x54) & 1); pressupost_assignat++) {
        unsigned codi_de_caràcter = màquina_registrar_se(보조장치 + 0x40) & 255;
        if (codi_de_caràcter == 192) {
            if (수신사용량 && !rebre_error && !수신탈출) {
                struct pbuf *dades_càrrec = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (dades_càrrec) { 받은전문수++; CANTIDAD_RECIBIDA_byte_COMPT += 수신사용량; pbuf_take(dades_càrrec, rebre_memòria_intermèdia_de_dades, 수신사용량); if (connexió_dispositiu.input(dades_càrrec, &connexió_dispositiu) != ERR_OK) { 버린전문수++; pbuf_free(dades_càrrec); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = rebre_error = 수신탈출 = 0;
        } else if (codi_de_caràcter == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (codi_de_caràcter != 220 && codi_de_caràcter != 221) rebre_error = 1; codi_de_caràcter = codi_de_caràcter == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(rebre_memòria_intermèdia_de_dades)) rebre_memòria_intermèdia_de_dades[수신사용량++] = codi_de_caràcter; else rebre_error = 1;
        }
    }
    netif_poll(&connexió_dispositiu); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned pressupost_assignat = 0; pressupost_assignat < 4096 && 송신개수 && (màquina_registrar_se(보조장치 + 0x54) & 0x20); pressupost_assignat++) {
        màquina_registrar_se(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Ajusts·조회는 lwIP의 real_dades 인터페이스와 finalitzar_p 표를 사용한다. */
uint32_t tancar_xarxa_estat(unsigned introducció_VALOR, unsigned INDEX) {
    if(introducció_VALOR==20)return ús_per_cable_xarxa;
    if(introducció_VALOR==21)return 준비됨&&netif_is_link_up(&connexió_dispositiu);
    if(introducció_VALOR==22)return ús_per_cable_xarxa?유선망집계(5):0;
    if (!준비됨) return 0;
    if(ús_per_cable_xarxa&&introducció_VALOR>=4&&introducció_VALOR<=8)return 유선망집계(introducció_VALOR-4);
    if (introducció_VALOR == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&connexió_dispositiu)));
    if (introducció_VALOR == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&connexió_dispositiu)));
    if (introducció_VALOR == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&connexió_dispositiu)));
    if (introducció_VALOR == 3) return netif_is_up(&connexió_dispositiu) != 0;
    if (introducció_VALOR == 4) return 받은전문수;
    if (introducció_VALOR == 5) return 보낸전문수;
    if (introducció_VALOR == 6) return CANTIDAD_RECIBIDA_byte_COMPT;
    if (introducció_VALOR == 7) return 보낸바이트수;
    if (introducció_VALOR == 8) return 버린전문수;
    if (introducció_VALOR == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *finalitzar_p = &통신끝점들[INDEX];
    if (introducció_VALOR == 10) return finalitzar_p->TIPUS_Categoria;
    if (!finalitzar_p->TIPUS_Categoria) return 0;
    if (introducció_VALOR == 11) return xarxa_número_de_port(INDEX);
    if (introducció_VALOR == 12) return finalitzar_p->homòleg_ADREÇA;
    if (introducció_VALOR == 13) return finalitzar_p->상대창구번호;
    if (introducció_VALOR == 14) return finalitzar_p->rebre_port ? 1 : finalitzar_p->arxiu_finalitzar ? 3 : finalitzar_p->s_ha_produït_un_error ? 4 : finalitzar_p->연결됨 ? 2 : 0;
    if (introducció_VALOR == 15) return finalitzar_p->introducció_COMPT;
    if (introducció_VALOR == 16) {
        const ip_addr_t *Adreça = finalitzar_p->TIPUS_Categoria == 1 && finalitzar_p->connexió_control ? &finalitzar_p->connexió_control->local_ip :
            finalitzar_p->TIPUS_Categoria == 2 && finalitzar_p->전문제어 ? &finalitzar_p->전문제어->local_ip : 0;
        return Adreça ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adreça))) : 0;
    }
    return 0;
}

int configurar_xarxa(unsigned Acció, uint32_t Adreça, uint32_t màscara_VALOR, uint32_t passarel_la_VALOR) {
    if (!준비됨) return -100;
    if (Acció == 1) { netif_set_up(&connexió_dispositiu); return 0; }
    if (Acció == 2) { netif_set_down(&connexió_dispositiu); return 0; }
    if (Acció != 0) return -22;
    /* 유니캐스트 IPv4, 연속 màscara_VALOR, 같은 망의 선택적 valor_per_defecte passarel_la_VALOR. */
    uint32_t 뒤집은가림 = ~màscara_VALOR;
    if (!màscara_VALOR || (뒤집은가림 & (뒤집은가림 + 1)) || !Adreça || (Adreça >> 24) == 127 ||
        (Adreça >> 24) == 0 || (Adreça >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(Adreça & 뒤집은가림) || (Adreça & 뒤집은가림) == 뒤집은가림)) ||
        (passarel_la_VALOR && ((passarel_la_VALOR & màscara_VALOR) != (Adreça & màscara_VALOR) || passarel_la_VALOR == Adreça || (passarel_la_VALOR >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(passarel_la_VALOR & 뒤집은가림) || (passarel_la_VALOR & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 Adreça 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TIPUS_Categoria &&
        !(통신끝점들[INDEX].rebre_port && 통신끝점들[INDEX].connexió_control && ip_addr_isany(&통신끝점들[INDEX].connexió_control->local_ip))) return -16;
    if(ús_per_cable_xarxa)dhcp_stop(&connexió_dispositiu);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(Adreça)); ip4_addr_set_u32(&새가림, lwip_htonl(màscara_VALOR)); ip4_addr_set_u32(&새관문, lwip_htonl(passarel_la_VALOR));
    netif_set_addr(&connexió_dispositiu, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *resposta_extrem;
static uint32_t 시험주소, 시험시각, resposta_Hora;
static unsigned 시험순서, 시험식별자, resposta_SEQÜÈNCIA;
static int resposta_Estat;
static u8_t 응답받음(void *인수, struct raw_pcb *finalitzar_p, struct pbuf *dades, const ip_addr_t *Adreça) {
    (void)인수; (void)finalitzar_p;
    unsigned char 머리[20], resposta[16];
    if (resposta_Estat != -11 || dades->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adreça))) != 시험주소 || pbuf_copy_partial(dades, 머리, 20, 0) != 20) return 0;
    unsigned Capçalera_canviar_la_mida = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Capçalera_canviar_la_mida < 20 || dades->tot_len < Capçalera_canviar_la_mida + 16 ||
        pbuf_copy_partial(dades, resposta, 16, Capçalera_canviar_la_mida) != 16 || resposta[0] || resposta[1] ||
        (((unsigned)resposta[4] << 8) | resposta[5]) != 시험식별자 ||
        (((unsigned)resposta[6] << 8) | resposta[7]) != 시험순서 ||
        resposta[8] != 'J' || resposta[9] != 'K' || resposta[10] != 'O' || resposta[11] != 'S' ||
        (((uint32_t)resposta[12] << 24) | ((uint32_t)resposta[13] << 16) | ((uint32_t)resposta[14] << 8) | resposta[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(dades, Capçalera_canviar_la_mida)) return 0;
    if (inet_chksum_pbuf(dades)) { pbuf_add_header(dades, Capçalera_canviar_la_mida); return 0; }
    resposta_Hora = (uint32_t)보드밀리초() - 시험시각; resposta_SEQÜÈNCIA = 머리[8]; resposta_Estat = 0;
    pbuf_free(dades); return 1;
}
int 응답시험시작(uint32_t Adreça, unsigned comanda_VALOR) {
    if (!준비됨 || !netif_is_up(&connexió_dispositiu)) return -100;
    if (!Adreça || (Adreça >> 28) >= 14 || Adreça == 0xffffffffu) return -22;
    if (!resposta_extrem) { resposta_extrem = raw_new(IP_PROTO_ICMP); if (!resposta_extrem) return -12; raw_recv(resposta_extrem, 응답받음, 0); }
    시험주소 = Adreça; 시험순서 = comanda_VALOR & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); resposta_Estat = -11; resposta_Hora = resposta_SEQÜÈNCIA = 0;
    unsigned char dades[32] = {8,0,0,0};
    dades[4] = 시험식별자 >> 8; dades[5] = 시험식별자; dades[6] = 시험순서 >> 8; dades[7] = 시험순서;
    dades[8]='J'; dades[9]='K'; dades[10]='O'; dades[11]='S';
    dades[12]=시험시각 >> 24; dades[13]=시험시각 >> 16; dades[14]=시험시각 >> 8; dades[15]=시험시각;
    for (unsigned càrrec_INDEX = 16; càrrec_INDEX < sizeof(dades); càrrec_INDEX++) dades[càrrec_INDEX] = càrrec_INDEX;
    uint16_t verificació_suma_de_comprovació = inet_chksum(dades, sizeof(dades)); memcpy(dades + 2, &verificació_suma_de_comprovació, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(dades), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, dades, sizeof(dades)); ip_addr_t destinació_extrem; ip_addr_set_ip4_u32(&destinació_extrem, lwip_htonl(Adreça));
    err_t 처리값 = raw_sendto(resposta_extrem, 전문, &destinació_extrem); pbuf_free(전문);
    if (처리값) resposta_Estat = número_d_error(처리값);
    return 처리값 ? resposta_Estat : 0;
}
int 응답시험읽기(unsigned introducció_VALOR) {
    통신망살피기();
    return introducció_VALOR == 0 ? resposta_Estat : introducció_VALOR == 1 ? (int)resposta_Hora : introducció_VALOR == 2 ? (int)resposta_SEQÜÈNCIA : -22;
}
