#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "rrjet_Stivë.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../në_largësi_VALUE/në_largësi_VALUE.h"
#include "i_lidhur_rrjet.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define makinë_regjistroj(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif lidhje_pajisje;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_bajt_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_kategori, 수신창구, teknologjia_e_informacionit_në_pritje, 연결됨, skedar_mbaroj, GABIM;
    struct tcp_pcb *lidhje_kontroll;
    struct udp_pcb *전문제어;
    unsigned e_përparme_futje, futje_COUNT;
    unsigned char të_dhëna[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], homolog_email;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *marr_VALUE(int skedar_dorezë) { return skedar_dorezë >= 0 && skedar_dorezë < 32 && 통신끝점들[skedar_dorezë].TYPE_kategori ? &통신끝점들[skedar_dorezë] : 0; }
static int 예약하기(int TYPE_kategori) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_kategori) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_kategori = TYPE_kategori; 통신끝점들[순번].teknologjia_e_informacionit_në_pritje = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kodi_i_karakterit) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kodi_i_karakterit; }
static err_t 출력결과(struct netif *njësi_COUNT, struct pbuf *të_dhëna_pozicioni, const ip4_addr_t *email) {
    (void)njësi_COUNT; (void)email;
    if (të_dhëna_pozicioni->tot_len > 1500 || 송신개수 + 2 * të_dhëna_pozicioni->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Tjetër_OFFSET = të_dhëna_pozicioni; Tjetër_OFFSET; Tjetër_OFFSET = Tjetër_OFFSET->next) for (unsigned 순번 = 0; 순번 < Tjetër_OFFSET->len; 순번++) {
        unsigned kodi_i_karakterit = ((unsigned char *)Tjetër_OFFSET->payload)[순번];
        if (kodi_i_karakterit == 192 || kodi_i_karakterit == 219) { 내보내기(219); 내보내기(kodi_i_karakterit == 192 ? 220 : 221); } else 내보내기(kodi_i_karakterit);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += të_dhëna_pozicioni->tot_len; return ERR_OK;
}
static err_t Përgatit_koha_e_ekzekutimit_të_gjuhës_së_zakonshme(struct netif *njësi_COUNT) { njësi_COUNT->name[0] = 's'; njësi_COUNT->name[1] = 'l'; njësi_COUNT->mtu = 1500; njësi_COUNT->output = 출력결과; return ERR_OK; }
void Përgatit_rrjet(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    makinë_regjistroj(보조장치 + 4) |= 1; makinë_regjistroj(보조장치 + 0x60) = 0; makinë_regjistroj(보조장치 + 0x44) = 0;
    makinë_regjistroj(보조장치 + 0x48) = 0xc6; makinë_regjistroj(보조장치 + 0x4c) = 3; makinë_regjistroj(보조장치 + 0x68) = 270; makinë_regjistroj(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t adresë_në_internet, bit_maskë, portëkalimi_email;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&adresë_në_internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_maskë, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&portëkalimi_email, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&lidhje_pajisje, &adresë_në_internet, &bit_maskë, &portëkalimi_email, 0, 유선사용?Përgatit_i_lidhur_rrjet:Përgatit_koha_e_ekzekutimit_të_gjuhës_së_zakonshme, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&lidhje_pajisje); netif_set_up(&lidhje_pajisje);if(!유선사용)netif_set_link_up(&lidhje_pajisje); 준비됨 = 1;
    Përgatit_në_largësi();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *transmetim_kontroll_bllokoj, struct pbuf *të_dhëna_pozicioni, err_t GABIM) {
    통신끝점 *varg_të_dhëna = 부가인수; (void)transmetim_kontroll_bllokoj; (void)GABIM;
    if (!të_dhëna_pozicioni) { varg_të_dhëna->skedar_mbaroj = 1; return ERR_OK; }
    if (të_dhëna_pozicioni->tot_len > sizeof(varg_të_dhëna->të_dhëna) - varg_të_dhëna->futje_COUNT) return ERR_MEM;
    unsigned 현재위치 = (varg_të_dhëna->e_përparme_futje + varg_të_dhëna->futje_COUNT) % sizeof(varg_të_dhëna->të_dhëna);
    for (struct pbuf *Tjetër_OFFSET = të_dhëna_pozicioni; Tjetër_OFFSET; Tjetër_OFFSET = Tjetër_OFFSET->next) for (unsigned 순번 = 0; 순번 < Tjetër_OFFSET->len; 순번++) {
        varg_të_dhëna->të_dhëna[현재위치] = ((unsigned char *)Tjetër_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(varg_të_dhëna->të_dhëna);
    }
    varg_të_dhëna->futje_COUNT += të_dhëna_pozicioni->tot_len; pbuf_free(të_dhëna_pozicioni); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t GABIM) { 통신끝점 *varg_të_dhëna = 부가인수; varg_të_dhëna->lidhje_kontroll = 0; varg_të_dhëna->GABIM = 오류번호(GABIM); }
static void 되부름목록(통신끝점 *varg_të_dhëna) { tcp_arg(varg_të_dhëna->lidhje_kontroll, varg_të_dhëna); tcp_recv(varg_të_dhëna->lidhje_kontroll, 수신됨); tcp_err(varg_të_dhëna->lidhje_kontroll, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *transmetim_kontroll_bllokoj, err_t GABIM) {
    통신끝점 *varg_të_dhëna = 부가인수; (void)transmetim_kontroll_bllokoj; if (GABIM) varg_të_dhëna->GABIM = 오류번호(GABIM); else varg_të_dhëna->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *transmetim_kontroll_bllokoj, err_t GABIM) {
    통신끝점 *부모항목 = 부가인수; if (GABIM) return GABIM;
    int skedar_dorezë = 예약하기(1); if (skedar_dorezë < 0) return ERR_MEM;
    통신끝점 *varg_të_dhëna = &통신끝점들[skedar_dorezë]; varg_të_dhëna->lidhje_kontroll = transmetim_kontroll_bllokoj; varg_të_dhëna->연결됨 = 1; varg_të_dhëna->teknologjia_e_informacionit_në_pritje = (int)(부모항목 - 통신끝점들);
    varg_të_dhëna->homolog_email = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&transmetim_kontroll_bllokoj->remote_ip))); varg_të_dhëna->상대창구번호 = transmetim_kontroll_bllokoj->remote_port;
    되부름목록(varg_të_dhëna); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *transmetim_kontroll_bllokoj, struct pbuf *të_dhëna_pozicioni, const ip_addr_t *email, u16_t numri_i_portës) {
    통신끝점 *varg_të_dhëna = 부가인수; (void)transmetim_kontroll_bllokoj;
    if (varg_të_dhëna->futje_COUNT < 4 && të_dhëna_pozicioni->tot_len <= 512) {
        unsigned pozicioni_INDEX = (varg_të_dhëna->e_përparme_futje + varg_të_dhëna->futje_COUNT) % 4;
        pbuf_copy_partial(të_dhëna_pozicioni, varg_të_dhëna->të_dhëna + pozicioni_INDEX * 512, të_dhëna_pozicioni->tot_len, 0);
        varg_të_dhëna->길이목록[pozicioni_INDEX] = të_dhëna_pozicioni->tot_len; varg_të_dhëna->접속번호들[pozicioni_INDEX] = numri_i_portës;
        varg_të_dhëna->주소목록[pozicioni_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(email))); varg_të_dhëna->futje_COUNT++;
    }
    pbuf_free(të_dhëna_pozicioni);
}
int 통신끝점만들기(int TYPE_kategori) {
    if (!준비됨) return -100;
    if (TYPE_kategori != 1 && TYPE_kategori != 2) return -93;
    int skedar_dorezë = 예약하기(TYPE_kategori); if (skedar_dorezë < 0) return skedar_dorezë;
    통신끝점 *varg_të_dhëna = &통신끝점들[skedar_dorezë];
    if (TYPE_kategori == 1) { varg_të_dhëna->lidhje_kontroll = tcp_new(); if (varg_të_dhëna->lidhje_kontroll) 되부름목록(varg_të_dhëna); }
    else { varg_të_dhëna->전문제어 = udp_new(); if (varg_të_dhëna->전문제어) udp_recv(varg_të_dhëna->전문제어, 전문, varg_të_dhëna); }
    if (!varg_të_dhëna->lidhje_kontroll && !varg_të_dhëna->전문제어) { varg_të_dhëna->TYPE_kategori = 0; return -12; } return skedar_dorezë;
}
int 망주소묶기(int skedar_dorezë, uint32_t email, unsigned numri_i_portës) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna) return -9;
    if (numri_i_portës > 65535 || (email && email != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&lidhje_pajisje))) && email != 0x7f000001)) return -99;
    ip_addr_t adresë_në_internet; ip_addr_set_ip4_u32(&adresë_në_internet, lwip_htonl(email));
    err_t 보조항목 = varg_të_dhëna->TYPE_kategori == 1 ? tcp_bind(varg_të_dhëna->lidhje_kontroll, &adresë_në_internet, numri_i_portës) : udp_bind(varg_të_dhëna->전문제어, &adresë_në_internet, numri_i_portës); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int skedar_dorezë) { 통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (varg_të_dhëna && varg_të_dhëna->lidhje_kontroll) ip_set_option(varg_të_dhëna->lidhje_kontroll, SOF_REUSEADDR); }
int 연결기다리기(int skedar_dorezë) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna || varg_të_dhëna->TYPE_kategori != 1) return -9;
    if (varg_të_dhëna->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *transmetim_kontroll_bllokoj = tcp_listen_with_backlog_and_err(varg_të_dhëna->lidhje_kontroll, 4, &보조항목);
    if (!transmetim_kontroll_bllokoj) return 오류번호(보조항목); varg_të_dhëna->lidhje_kontroll = transmetim_kontroll_bllokoj; varg_të_dhëna->수신창구 = 1; tcp_arg(transmetim_kontroll_bllokoj, varg_të_dhëna); tcp_accept(transmetim_kontroll_bllokoj, 연결받음); return 0;
}
int 망연결하기(int skedar_dorezë, uint32_t email, unsigned numri_i_portës) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna || varg_të_dhëna->TYPE_kategori != 1) return -9;
    if (varg_të_dhëna->GABIM) return varg_të_dhëna->GABIM;
    if (varg_të_dhëna->연결됨) return 0;
    if (varg_të_dhëna->상대창구번호) return -115;
    if (!numri_i_portës || numri_i_portës > 65535 || !email) return -22;
    ip_addr_t adresë_në_internet; ip_addr_set_ip4_u32(&adresë_në_internet, lwip_htonl(email));
    varg_të_dhëna->homolog_email = email; varg_të_dhëna->상대창구번호 = numri_i_portës;
    err_t 보조항목 = tcp_connect(varg_të_dhëna->lidhje_kontroll, &adresë_në_internet, numri_i_portës, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int skedar_dorezë) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna || !varg_të_dhëna->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_kategori == 1 && 통신끝점들[순번].teknologjia_e_informacionit_në_pritje == skedar_dorezë) { 통신끝점들[순번].teknologjia_e_informacionit_në_pritje = -1; return 순번; }
    return -11;
}
int 통신읽기(int skedar_dorezë, void *të_dhëna, unsigned njësi_COUNT) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna || varg_të_dhëna->TYPE_kategori != 1) return -9;
    if (!njësi_COUNT) return 0; if (!varg_të_dhëna->futje_COUNT) return varg_të_dhëna->GABIM ? varg_të_dhëna->GABIM : varg_të_dhëna->skedar_mbaroj ? 0 : -11;
    if (njësi_COUNT > varg_të_dhëna->futje_COUNT) njësi_COUNT = varg_të_dhëna->futje_COUNT;
    for (unsigned 순번 = 0; 순번 < njësi_COUNT; 순번++) { ((unsigned char *)të_dhëna)[순번] = varg_të_dhëna->të_dhëna[varg_të_dhëna->e_përparme_futje]; varg_të_dhëna->e_përparme_futje = (varg_të_dhëna->e_përparme_futje + 1) % sizeof(varg_të_dhëna->të_dhëna); }
    varg_të_dhëna->futje_COUNT -= njësi_COUNT; if (varg_të_dhëna->lidhje_kontroll) tcp_recved(varg_të_dhëna->lidhje_kontroll, njësi_COUNT); return njësi_COUNT;
}
int 통신쓰기(int skedar_dorezë, const void *të_dhëna, unsigned njësi_COUNT) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna || varg_të_dhëna->TYPE_kategori != 1) return -9;
    if (varg_të_dhëna->GABIM) return varg_të_dhëna->GABIM; if (!varg_të_dhëna->lidhje_kontroll || !varg_të_dhëna->연결됨) return -107;
    if (!njësi_COUNT) return 0; if (njësi_COUNT > tcp_sndbuf(varg_të_dhëna->lidhje_kontroll)) njësi_COUNT = tcp_sndbuf(varg_të_dhëna->lidhje_kontroll);
    if (!njësi_COUNT) return -11; if (njësi_COUNT > 1024) njësi_COUNT = 1024;
    err_t 보조항목 = tcp_write(varg_të_dhëna->lidhje_kontroll, të_dhëna, njësi_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(varg_të_dhëna->lidhje_kontroll); return njësi_COUNT;
}
int 전문보내기(int skedar_dorezë, const void *të_dhëna, unsigned njësi_COUNT, uint32_t email, unsigned numri_i_portës) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna || varg_të_dhëna->TYPE_kategori != 2) return -9;
    if (njësi_COUNT > 512) return -90; if (!numri_i_portës || numri_i_portës > 65535) return -22;
    struct pbuf *të_dhëna_pozicioni = pbuf_alloc(PBUF_TRANSPORT, njësi_COUNT, PBUF_RAM); if (!të_dhëna_pozicioni) return -11;
    pbuf_take(të_dhëna_pozicioni, të_dhëna, njësi_COUNT); ip_addr_t adresë_në_internet; ip_addr_set_ip4_u32(&adresë_në_internet, lwip_htonl(email));
    err_t 보조항목 = udp_sendto(varg_të_dhëna->전문제어, të_dhëna_pozicioni, &adresë_në_internet, numri_i_portës); pbuf_free(të_dhëna_pozicioni); return 보조항목 ? 오류번호(보조항목) : (int)njësi_COUNT;
}
int 전문받기(int skedar_dorezë, void *të_dhëna, unsigned njësi_COUNT) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna || varg_të_dhëna->TYPE_kategori != 2) return -9;
    if (!varg_të_dhëna->futje_COUNT) return -11; unsigned 현재위치 = varg_të_dhëna->e_përparme_futje;
    if (njësi_COUNT > varg_të_dhëna->길이목록[현재위치]) njësi_COUNT = varg_të_dhëna->길이목록[현재위치]; memcpy(të_dhëna, varg_të_dhëna->të_dhëna + 현재위치 * 512, njësi_COUNT);
    varg_të_dhëna->상대창구번호 = varg_të_dhëna->접속번호들[현재위치]; varg_të_dhëna->homolog_email = varg_të_dhëna->주소목록[현재위치]; varg_të_dhëna->e_përparme_futje = (현재위치 + 1) % 4; varg_të_dhëna->futje_COUNT--; return njësi_COUNT;
}
unsigned rrjet_numri_i_portës(int skedar_dorezë) { 통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); return !varg_të_dhëna ? 0 : varg_të_dhëna->lidhje_kontroll ? varg_të_dhëna->lidhje_kontroll->local_port : varg_të_dhëna->전문제어 ? varg_të_dhëna->전문제어->local_port : 0; }
unsigned homolog_numri_i_portës(int skedar_dorezë) { 통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); return varg_të_dhëna ? varg_të_dhëna->상대창구번호 : 0; }
uint32_t 상대통신주소(int skedar_dorezë) { 통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); return varg_të_dhëna ? varg_të_dhëna->homolog_email : 0; }
void mbyll_rrjet(int skedar_dorezë) {
    통신끝점 *varg_të_dhëna = marr_VALUE(skedar_dorezë); if (!varg_të_dhëna) return;
    if (varg_të_dhëna->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_kategori && 통신끝점들[순번].teknologjia_e_informacionit_në_pritje == skedar_dorezë) mbyll_rrjet(순번);
    if (varg_të_dhëna->lidhje_kontroll) {
        tcp_arg(varg_të_dhëna->lidhje_kontroll, 0); if (varg_të_dhëna->수신창구) tcp_accept(varg_të_dhëna->lidhje_kontroll, 0); else { tcp_recv(varg_të_dhëna->lidhje_kontroll, 0); tcp_err(varg_të_dhëna->lidhje_kontroll, 0); }
        if (tcp_close(varg_të_dhëna->lidhje_kontroll) != ERR_OK) tcp_abort(varg_të_dhëna->lidhje_kontroll);
    }
    if (varg_të_dhëna->전문제어) udp_remove(varg_të_dhëna->전문제어); varg_të_dhëna->TYPE_kategori = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&lidhje_pajisje);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (makinë_regjistroj(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned kodi_i_karakterit = makinë_regjistroj(보조장치 + 0x40) & 255;
        if (kodi_i_karakterit == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *të_dhëna_pozicioni = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (të_dhëna_pozicioni) { 받은전문수++; RECEIVED_bajt_COUNT += 수신사용량; pbuf_take(të_dhëna_pozicioni, 수신자료, 수신사용량); if (lidhje_pajisje.input(të_dhëna_pozicioni, &lidhje_pajisje) != ERR_OK) { 버린전문수++; pbuf_free(të_dhëna_pozicioni); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (kodi_i_karakterit == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kodi_i_karakterit != 220 && kodi_i_karakterit != 221) 수신오류 = 1; kodi_i_karakterit = kodi_i_karakterit == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = kodi_i_karakterit; else 수신오류 = 1;
        }
    }
    netif_poll(&lidhje_pajisje); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (makinë_regjistroj(보조장치 + 0x54) & 0x20); 처리한도++) {
        makinë_regjistroj(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Rregullime·조회는 lwIP의 aktual_të_dhëna 인터페이스와 mbaroj_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned futje_VALUE, unsigned INDEX) {
    if(futje_VALUE==20)return 유선사용;
    if(futje_VALUE==21)return 준비됨&&netif_is_link_up(&lidhje_pajisje);
    if(futje_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&futje_VALUE>=4&&futje_VALUE<=8)return 유선망집계(futje_VALUE-4);
    if (futje_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&lidhje_pajisje)));
    if (futje_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&lidhje_pajisje)));
    if (futje_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&lidhje_pajisje)));
    if (futje_VALUE == 3) return netif_is_up(&lidhje_pajisje) != 0;
    if (futje_VALUE == 4) return 받은전문수;
    if (futje_VALUE == 5) return 보낸전문수;
    if (futje_VALUE == 6) return RECEIVED_bajt_COUNT;
    if (futje_VALUE == 7) return 보낸바이트수;
    if (futje_VALUE == 8) return 버린전문수;
    if (futje_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *mbaroj_p = &통신끝점들[INDEX];
    if (futje_VALUE == 10) return mbaroj_p->TYPE_kategori;
    if (!mbaroj_p->TYPE_kategori) return 0;
    if (futje_VALUE == 11) return rrjet_numri_i_portës(INDEX);
    if (futje_VALUE == 12) return mbaroj_p->homolog_email;
    if (futje_VALUE == 13) return mbaroj_p->상대창구번호;
    if (futje_VALUE == 14) return mbaroj_p->수신창구 ? 1 : mbaroj_p->skedar_mbaroj ? 3 : mbaroj_p->GABIM ? 4 : mbaroj_p->연결됨 ? 2 : 0;
    if (futje_VALUE == 15) return mbaroj_p->futje_COUNT;
    if (futje_VALUE == 16) {
        const ip_addr_t *email = mbaroj_p->TYPE_kategori == 1 && mbaroj_p->lidhje_kontroll ? &mbaroj_p->lidhje_kontroll->local_ip :
            mbaroj_p->TYPE_kategori == 2 && mbaroj_p->전문제어 ? &mbaroj_p->전문제어->local_ip : 0;
        return email ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(email))) : 0;
    }
    return 0;
}

int konfiguroj_rrjet(unsigned Veprim, uint32_t email, uint32_t maskë_VALUE, uint32_t portëkalimi_VALUE) {
    if (!준비됨) return -100;
    if (Veprim == 1) { netif_set_up(&lidhje_pajisje); return 0; }
    if (Veprim == 2) { netif_set_down(&lidhje_pajisje); return 0; }
    if (Veprim != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maskë_VALUE, 같은 망의 선택적 vlerë_e_parazgjedhur portëkalimi_VALUE. */
    uint32_t 뒤집은가림 = ~maskë_VALUE;
    if (!maskë_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !email || (email >> 24) == 127 ||
        (email >> 24) == 0 || (email >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(email & 뒤집은가림) || (email & 뒤집은가림) == 뒤집은가림)) ||
        (portëkalimi_VALUE && ((portëkalimi_VALUE & maskë_VALUE) != (email & maskë_VALUE) || portëkalimi_VALUE == email || (portëkalimi_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(portëkalimi_VALUE & 뒤집은가림) || (portëkalimi_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 email 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_kategori &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].lidhje_kontroll && ip_addr_isany(&통신끝점들[INDEX].lidhje_kontroll->local_ip))) return -16;
    if(유선사용)dhcp_stop(&lidhje_pajisje);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(email)); ip4_addr_set_u32(&새가림, lwip_htonl(maskë_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(portëkalimi_VALUE));
    netif_set_addr(&lidhje_pajisje, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, përgjigje_Ora;
static unsigned 시험순서, 시험식별자, përgjigje_SEQUENCE;
static int përgjigje_status;
static u8_t 응답받음(void *Argumente, struct raw_pcb *mbaroj_p, struct pbuf *të_dhëna, const ip_addr_t *email) {
    (void)Argumente; (void)mbaroj_p;
    unsigned char 머리[20], replikë[16];
    if (përgjigje_status != -11 || të_dhëna->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(email))) != 시험주소 || pbuf_copy_partial(të_dhëna, 머리, 20, 0) != 20) return 0;
    unsigned Kreu_ndryshoj_përmasat = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Kreu_ndryshoj_përmasat < 20 || të_dhëna->tot_len < Kreu_ndryshoj_përmasat + 16 ||
        pbuf_copy_partial(të_dhëna, replikë, 16, Kreu_ndryshoj_përmasat) != 16 || replikë[0] || replikë[1] ||
        (((unsigned)replikë[4] << 8) | replikë[5]) != 시험식별자 ||
        (((unsigned)replikë[6] << 8) | replikë[7]) != 시험순서 ||
        replikë[8] != 'J' || replikë[9] != 'K' || replikë[10] != 'O' || replikë[11] != 'S' ||
        (((uint32_t)replikë[12] << 24) | ((uint32_t)replikë[13] << 16) | ((uint32_t)replikë[14] << 8) | replikë[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(të_dhëna, Kreu_ndryshoj_përmasat)) return 0;
    if (inet_chksum_pbuf(të_dhëna)) { pbuf_add_header(të_dhëna, Kreu_ndryshoj_përmasat); return 0; }
    përgjigje_Ora = (uint32_t)보드밀리초() - 시험시각; përgjigje_SEQUENCE = 머리[8]; përgjigje_status = 0;
    pbuf_free(të_dhëna); return 1;
}
int 응답시험시작(uint32_t email, unsigned renditja_VALUE) {
    if (!준비됨 || !netif_is_up(&lidhje_pajisje)) return -100;
    if (!email || (email >> 28) >= 14 || email == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = email; 시험순서 = renditja_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); përgjigje_status = -11; përgjigje_Ora = përgjigje_SEQUENCE = 0;
    unsigned char të_dhëna[32] = {8,0,0,0};
    të_dhëna[4] = 시험식별자 >> 8; të_dhëna[5] = 시험식별자; të_dhëna[6] = 시험순서 >> 8; të_dhëna[7] = 시험순서;
    të_dhëna[8]='J'; të_dhëna[9]='K'; të_dhëna[10]='O'; të_dhëna[11]='S';
    të_dhëna[12]=시험시각 >> 24; të_dhëna[13]=시험시각 >> 16; të_dhëna[14]=시험시각 >> 8; të_dhëna[15]=시험시각;
    for (unsigned pozicioni_INDEX = 16; pozicioni_INDEX < sizeof(të_dhëna); pozicioni_INDEX++) të_dhëna[pozicioni_INDEX] = pozicioni_INDEX;
    uint16_t verifikim_kontrolli_i_shumës = inet_chksum(të_dhëna, sizeof(të_dhëna)); memcpy(të_dhëna + 2, &verifikim_kontrolli_i_shumës, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(të_dhëna), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, të_dhëna, sizeof(të_dhëna)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(email));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) përgjigje_status = 오류번호(처리값);
    return 처리값 ? përgjigje_status : 0;
}
int 응답시험읽기(unsigned futje_VALUE) {
    통신망살피기();
    return futje_VALUE == 0 ? përgjigje_status : futje_VALUE == 1 ? (int)përgjigje_Ora : futje_VALUE == 2 ? (int)përgjigje_SEQUENCE : -22;
}
