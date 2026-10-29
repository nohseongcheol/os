#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Hanyar_sadarwa_tara.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../na_nesa_Daraja/na_nesa_Daraja.h"
#include "Hade_da_waya_Hanyar_sadarwa.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif haɗi_na_ura;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int rubuta_ɓangare, 수신창구, kimiyar_bayanai_mai_jira, 연결됨, Fayil_Ƙarshe, Kuskure;
    struct tcp_pcb *haɗi_masarrafa;
    struct udp_pcb *전문제어;
    unsigned kyamarar_gaba_Mashigar_bayanai, 항목수;
    unsigned char Tarin_bayani[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], Fiya_imel;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *samo_Daraja(int Fayil_Mariki) { return Fayil_Mariki >= 0 && Fayil_Mariki < 32 && 통신끝점들[Fayil_Mariki].rubuta_ɓangare ? &통신끝점들[Fayil_Mariki] : 0; }
static int 예약하기(int rubuta_ɓangare) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].rubuta_ɓangare) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].rubuta_ɓangare = rubuta_ɓangare; 통신끝점들[순번].kimiyar_bayanai_mai_jira = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned Lambar_sirrin_harafi) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = Lambar_sirrin_harafi; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *imel) {
    (void)개수; (void)imel;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned Lambar_sirrin_harafi = ((unsigned char *)다음위치->payload)[순번];
        if (Lambar_sirrin_harafi == 192 || Lambar_sirrin_harafi == 219) { 내보내기(219); 내보내기(Lambar_sirrin_harafi == 192 ? 220 : 221); } else 내보내기(Lambar_sirrin_harafi);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t Shirya_lokacin_bude_yaren_gama_gari(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Shirya_Hanyar_sadarwa(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    기계저장기(보조장치 + 4) |= 1; 기계저장기(보조장치 + 0x60) = 0; 기계저장기(보조장치 + 0x44) = 0;
    기계저장기(보조장치 + 0x48) = 0xc6; 기계저장기(보조장치 + 0x4c) = 3; 기계저장기(보조장치 + 0x68) = 270; 기계저장기(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Adireshin_yanar_gizo, bit_Burtu, Mashiga_imel;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Adireshin_yanar_gizo, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_Burtu, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&Mashiga_imel, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&haɗi_na_ura, &Adireshin_yanar_gizo, &bit_Burtu, &Mashiga_imel, 0, 유선사용?Shirya_Hade_da_waya_Hanyar_sadarwa:Shirya_lokacin_bude_yaren_gama_gari, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&haɗi_na_ura); netif_set_up(&haɗi_na_ura);if(!유선사용)netif_set_link_up(&haɗi_na_ura); 준비됨 = 1;
    Shirya_na_nesa();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *Watsa_bayanai_masarrafa_bulo, struct pbuf *자료위치, err_t Kuskure) {
    통신끝점 *Zare_Tarin_bayani = 부가인수; (void)Watsa_bayanai_masarrafa_bulo; (void)Kuskure;
    if (!자료위치) { Zare_Tarin_bayani->Fayil_Ƙarshe = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(Zare_Tarin_bayani->Tarin_bayani) - Zare_Tarin_bayani->항목수) return ERR_MEM;
    unsigned 현재위치 = (Zare_Tarin_bayani->kyamarar_gaba_Mashigar_bayanai + Zare_Tarin_bayani->항목수) % sizeof(Zare_Tarin_bayani->Tarin_bayani);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        Zare_Tarin_bayani->Tarin_bayani[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(Zare_Tarin_bayani->Tarin_bayani);
    }
    Zare_Tarin_bayani->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Kuskure) { 통신끝점 *Zare_Tarin_bayani = 부가인수; Zare_Tarin_bayani->haɗi_masarrafa = 0; Zare_Tarin_bayani->Kuskure = 오류번호(Kuskure); }
static void 되부름목록(통신끝점 *Zare_Tarin_bayani) { tcp_arg(Zare_Tarin_bayani->haɗi_masarrafa, Zare_Tarin_bayani); tcp_recv(Zare_Tarin_bayani->haɗi_masarrafa, 수신됨); tcp_err(Zare_Tarin_bayani->haɗi_masarrafa, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *Watsa_bayanai_masarrafa_bulo, err_t Kuskure) {
    통신끝점 *Zare_Tarin_bayani = 부가인수; (void)Watsa_bayanai_masarrafa_bulo; if (Kuskure) Zare_Tarin_bayani->Kuskure = 오류번호(Kuskure); else Zare_Tarin_bayani->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *Watsa_bayanai_masarrafa_bulo, err_t Kuskure) {
    통신끝점 *부모항목 = 부가인수; if (Kuskure) return Kuskure;
    int Fayil_Mariki = 예약하기(1); if (Fayil_Mariki < 0) return ERR_MEM;
    통신끝점 *Zare_Tarin_bayani = &통신끝점들[Fayil_Mariki]; Zare_Tarin_bayani->haɗi_masarrafa = Watsa_bayanai_masarrafa_bulo; Zare_Tarin_bayani->연결됨 = 1; Zare_Tarin_bayani->kimiyar_bayanai_mai_jira = (int)(부모항목 - 통신끝점들);
    Zare_Tarin_bayani->Fiya_imel = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&Watsa_bayanai_masarrafa_bulo->remote_ip))); Zare_Tarin_bayani->상대창구번호 = Watsa_bayanai_masarrafa_bulo->remote_port;
    되부름목록(Zare_Tarin_bayani); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *Watsa_bayanai_masarrafa_bulo, struct pbuf *자료위치, const ip_addr_t *imel, u16_t lambar_kafa) {
    통신끝점 *Zare_Tarin_bayani = 부가인수; (void)Watsa_bayanai_masarrafa_bulo;
    if (Zare_Tarin_bayani->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (Zare_Tarin_bayani->kyamarar_gaba_Mashigar_bayanai + Zare_Tarin_bayani->항목수) % 4;
        pbuf_copy_partial(자료위치, Zare_Tarin_bayani->Tarin_bayani + 자리 * 512, 자료위치->tot_len, 0);
        Zare_Tarin_bayani->길이목록[자리] = 자료위치->tot_len; Zare_Tarin_bayani->접속번호들[자리] = lambar_kafa;
        Zare_Tarin_bayani->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(imel))); Zare_Tarin_bayani->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int rubuta_ɓangare) {
    if (!준비됨) return -100;
    if (rubuta_ɓangare != 1 && rubuta_ɓangare != 2) return -93;
    int Fayil_Mariki = 예약하기(rubuta_ɓangare); if (Fayil_Mariki < 0) return Fayil_Mariki;
    통신끝점 *Zare_Tarin_bayani = &통신끝점들[Fayil_Mariki];
    if (rubuta_ɓangare == 1) { Zare_Tarin_bayani->haɗi_masarrafa = tcp_new(); if (Zare_Tarin_bayani->haɗi_masarrafa) 되부름목록(Zare_Tarin_bayani); }
    else { Zare_Tarin_bayani->전문제어 = udp_new(); if (Zare_Tarin_bayani->전문제어) udp_recv(Zare_Tarin_bayani->전문제어, 전문, Zare_Tarin_bayani); }
    if (!Zare_Tarin_bayani->haɗi_masarrafa && !Zare_Tarin_bayani->전문제어) { Zare_Tarin_bayani->rubuta_ɓangare = 0; return -12; } return Fayil_Mariki;
}
int 망주소묶기(int Fayil_Mariki, uint32_t imel, unsigned lambar_kafa) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani) return -9;
    if (lambar_kafa > 65535 || (imel && imel != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&haɗi_na_ura))) && imel != 0x7f000001)) return -99;
    ip_addr_t Adireshin_yanar_gizo; ip_addr_set_ip4_u32(&Adireshin_yanar_gizo, lwip_htonl(imel));
    err_t 보조항목 = Zare_Tarin_bayani->rubuta_ɓangare == 1 ? tcp_bind(Zare_Tarin_bayani->haɗi_masarrafa, &Adireshin_yanar_gizo, lambar_kafa) : udp_bind(Zare_Tarin_bayani->전문제어, &Adireshin_yanar_gizo, lambar_kafa); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int Fayil_Mariki) { 통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (Zare_Tarin_bayani && Zare_Tarin_bayani->haɗi_masarrafa) ip_set_option(Zare_Tarin_bayani->haɗi_masarrafa, SOF_REUSEADDR); }
int 연결기다리기(int Fayil_Mariki) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani || Zare_Tarin_bayani->rubuta_ɓangare != 1) return -9;
    if (Zare_Tarin_bayani->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *Watsa_bayanai_masarrafa_bulo = tcp_listen_with_backlog_and_err(Zare_Tarin_bayani->haɗi_masarrafa, 4, &보조항목);
    if (!Watsa_bayanai_masarrafa_bulo) return 오류번호(보조항목); Zare_Tarin_bayani->haɗi_masarrafa = Watsa_bayanai_masarrafa_bulo; Zare_Tarin_bayani->수신창구 = 1; tcp_arg(Watsa_bayanai_masarrafa_bulo, Zare_Tarin_bayani); tcp_accept(Watsa_bayanai_masarrafa_bulo, 연결받음); return 0;
}
int 망연결하기(int Fayil_Mariki, uint32_t imel, unsigned lambar_kafa) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani || Zare_Tarin_bayani->rubuta_ɓangare != 1) return -9;
    if (Zare_Tarin_bayani->Kuskure) return Zare_Tarin_bayani->Kuskure;
    if (Zare_Tarin_bayani->연결됨) return 0;
    if (Zare_Tarin_bayani->상대창구번호) return -115;
    if (!lambar_kafa || lambar_kafa > 65535 || !imel) return -22;
    ip_addr_t Adireshin_yanar_gizo; ip_addr_set_ip4_u32(&Adireshin_yanar_gizo, lwip_htonl(imel));
    Zare_Tarin_bayani->Fiya_imel = imel; Zare_Tarin_bayani->상대창구번호 = lambar_kafa;
    err_t 보조항목 = tcp_connect(Zare_Tarin_bayani->haɗi_masarrafa, &Adireshin_yanar_gizo, lambar_kafa, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int Fayil_Mariki) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani || !Zare_Tarin_bayani->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].rubuta_ɓangare == 1 && 통신끝점들[순번].kimiyar_bayanai_mai_jira == Fayil_Mariki) { 통신끝점들[순번].kimiyar_bayanai_mai_jira = -1; return 순번; }
    return -11;
}
int 통신읽기(int Fayil_Mariki, void *Tarin_bayani, unsigned 개수) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani || Zare_Tarin_bayani->rubuta_ɓangare != 1) return -9;
    if (!개수) return 0; if (!Zare_Tarin_bayani->항목수) return Zare_Tarin_bayani->Kuskure ? Zare_Tarin_bayani->Kuskure : Zare_Tarin_bayani->Fayil_Ƙarshe ? 0 : -11;
    if (개수 > Zare_Tarin_bayani->항목수) 개수 = Zare_Tarin_bayani->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)Tarin_bayani)[순번] = Zare_Tarin_bayani->Tarin_bayani[Zare_Tarin_bayani->kyamarar_gaba_Mashigar_bayanai]; Zare_Tarin_bayani->kyamarar_gaba_Mashigar_bayanai = (Zare_Tarin_bayani->kyamarar_gaba_Mashigar_bayanai + 1) % sizeof(Zare_Tarin_bayani->Tarin_bayani); }
    Zare_Tarin_bayani->항목수 -= 개수; if (Zare_Tarin_bayani->haɗi_masarrafa) tcp_recved(Zare_Tarin_bayani->haɗi_masarrafa, 개수); return 개수;
}
int 통신쓰기(int Fayil_Mariki, const void *Tarin_bayani, unsigned 개수) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani || Zare_Tarin_bayani->rubuta_ɓangare != 1) return -9;
    if (Zare_Tarin_bayani->Kuskure) return Zare_Tarin_bayani->Kuskure; if (!Zare_Tarin_bayani->haɗi_masarrafa || !Zare_Tarin_bayani->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(Zare_Tarin_bayani->haɗi_masarrafa)) 개수 = tcp_sndbuf(Zare_Tarin_bayani->haɗi_masarrafa);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(Zare_Tarin_bayani->haɗi_masarrafa, Tarin_bayani, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(Zare_Tarin_bayani->haɗi_masarrafa); return 개수;
}
int 전문보내기(int Fayil_Mariki, const void *Tarin_bayani, unsigned 개수, uint32_t imel, unsigned lambar_kafa) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani || Zare_Tarin_bayani->rubuta_ɓangare != 2) return -9;
    if (개수 > 512) return -90; if (!lambar_kafa || lambar_kafa > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, Tarin_bayani, 개수); ip_addr_t Adireshin_yanar_gizo; ip_addr_set_ip4_u32(&Adireshin_yanar_gizo, lwip_htonl(imel));
    err_t 보조항목 = udp_sendto(Zare_Tarin_bayani->전문제어, 자료위치, &Adireshin_yanar_gizo, lambar_kafa); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int Fayil_Mariki, void *Tarin_bayani, unsigned 개수) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani || Zare_Tarin_bayani->rubuta_ɓangare != 2) return -9;
    if (!Zare_Tarin_bayani->항목수) return -11; unsigned 현재위치 = Zare_Tarin_bayani->kyamarar_gaba_Mashigar_bayanai;
    if (개수 > Zare_Tarin_bayani->길이목록[현재위치]) 개수 = Zare_Tarin_bayani->길이목록[현재위치]; memcpy(Tarin_bayani, Zare_Tarin_bayani->Tarin_bayani + 현재위치 * 512, 개수);
    Zare_Tarin_bayani->상대창구번호 = Zare_Tarin_bayani->접속번호들[현재위치]; Zare_Tarin_bayani->Fiya_imel = Zare_Tarin_bayani->주소목록[현재위치]; Zare_Tarin_bayani->kyamarar_gaba_Mashigar_bayanai = (현재위치 + 1) % 4; Zare_Tarin_bayani->항목수--; return 개수;
}
unsigned Hanyar_sadarwa_lambar_kafa(int Fayil_Mariki) { 통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); return !Zare_Tarin_bayani ? 0 : Zare_Tarin_bayani->haɗi_masarrafa ? Zare_Tarin_bayani->haɗi_masarrafa->local_port : Zare_Tarin_bayani->전문제어 ? Zare_Tarin_bayani->전문제어->local_port : 0; }
unsigned Fiya_lambar_kafa(int Fayil_Mariki) { 통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); return Zare_Tarin_bayani ? Zare_Tarin_bayani->상대창구번호 : 0; }
uint32_t 상대통신주소(int Fayil_Mariki) { 통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); return Zare_Tarin_bayani ? Zare_Tarin_bayani->Fiya_imel : 0; }
void Rufe_Hanyar_sadarwa(int Fayil_Mariki) {
    통신끝점 *Zare_Tarin_bayani = samo_Daraja(Fayil_Mariki); if (!Zare_Tarin_bayani) return;
    if (Zare_Tarin_bayani->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].rubuta_ɓangare && 통신끝점들[순번].kimiyar_bayanai_mai_jira == Fayil_Mariki) Rufe_Hanyar_sadarwa(순번);
    if (Zare_Tarin_bayani->haɗi_masarrafa) {
        tcp_arg(Zare_Tarin_bayani->haɗi_masarrafa, 0); if (Zare_Tarin_bayani->수신창구) tcp_accept(Zare_Tarin_bayani->haɗi_masarrafa, 0); else { tcp_recv(Zare_Tarin_bayani->haɗi_masarrafa, 0); tcp_err(Zare_Tarin_bayani->haɗi_masarrafa, 0); }
        if (tcp_close(Zare_Tarin_bayani->haɗi_masarrafa) != ERR_OK) tcp_abort(Zare_Tarin_bayani->haɗi_masarrafa);
    }
    if (Zare_Tarin_bayani->전문제어) udp_remove(Zare_Tarin_bayani->전문제어); Zare_Tarin_bayani->rubuta_ɓangare = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&haɗi_na_ura);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (기계저장기(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned Lambar_sirrin_harafi = 기계저장기(보조장치 + 0x40) & 255;
        if (Lambar_sirrin_harafi == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (haɗi_na_ura.input(자료위치, &haɗi_na_ura) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (Lambar_sirrin_harafi == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (Lambar_sirrin_harafi != 220 && Lambar_sirrin_harafi != 221) 수신오류 = 1; Lambar_sirrin_harafi = Lambar_sirrin_harafi == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = Lambar_sirrin_harafi; else 수신오류 = 1;
        }
    }
    netif_poll(&haɗi_na_ura); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (기계저장기(보조장치 + 0x54) & 0x20); 처리한도++) {
        기계저장기(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Saituna·조회는 lwIP의 Na_hakika_Tarin_bayani 인터페이스와 Ƙarshe_maki 표를 사용한다. */
uint32_t 망상태읽기(unsigned Mashigar_bayanai_Daraja, unsigned Indes) {
    if(Mashigar_bayanai_Daraja==20)return 유선사용;
    if(Mashigar_bayanai_Daraja==21)return 준비됨&&netif_is_link_up(&haɗi_na_ura);
    if(Mashigar_bayanai_Daraja==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&Mashigar_bayanai_Daraja>=4&&Mashigar_bayanai_Daraja<=8)return 유선망집계(Mashigar_bayanai_Daraja-4);
    if (Mashigar_bayanai_Daraja == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&haɗi_na_ura)));
    if (Mashigar_bayanai_Daraja == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&haɗi_na_ura)));
    if (Mashigar_bayanai_Daraja == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&haɗi_na_ura)));
    if (Mashigar_bayanai_Daraja == 3) return netif_is_up(&haɗi_na_ura) != 0;
    if (Mashigar_bayanai_Daraja == 4) return 받은전문수;
    if (Mashigar_bayanai_Daraja == 5) return 보낸전문수;
    if (Mashigar_bayanai_Daraja == 6) return 받은바이트수;
    if (Mashigar_bayanai_Daraja == 7) return 보낸바이트수;
    if (Mashigar_bayanai_Daraja == 8) return 버린전문수;
    if (Mashigar_bayanai_Daraja == 9) return 송신개수;
    if (Indes >= 32) return 0;
    통신끝점 *Ƙarshe_maki = &통신끝점들[Indes];
    if (Mashigar_bayanai_Daraja == 10) return Ƙarshe_maki->rubuta_ɓangare;
    if (!Ƙarshe_maki->rubuta_ɓangare) return 0;
    if (Mashigar_bayanai_Daraja == 11) return Hanyar_sadarwa_lambar_kafa(Indes);
    if (Mashigar_bayanai_Daraja == 12) return Ƙarshe_maki->Fiya_imel;
    if (Mashigar_bayanai_Daraja == 13) return Ƙarshe_maki->상대창구번호;
    if (Mashigar_bayanai_Daraja == 14) return Ƙarshe_maki->수신창구 ? 1 : Ƙarshe_maki->Fayil_Ƙarshe ? 3 : Ƙarshe_maki->Kuskure ? 4 : Ƙarshe_maki->연결됨 ? 2 : 0;
    if (Mashigar_bayanai_Daraja == 15) return Ƙarshe_maki->항목수;
    if (Mashigar_bayanai_Daraja == 16) {
        const ip_addr_t *imel = Ƙarshe_maki->rubuta_ɓangare == 1 && Ƙarshe_maki->haɗi_masarrafa ? &Ƙarshe_maki->haɗi_masarrafa->local_ip :
            Ƙarshe_maki->rubuta_ɓangare == 2 && Ƙarshe_maki->전문제어 ? &Ƙarshe_maki->전문제어->local_ip : 0;
        return imel ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(imel))) : 0;
    }
    return 0;
}

int hada_kayan_Hanyar_sadarwa(unsigned Aiki, uint32_t imel, uint32_t Burtu_Daraja, uint32_t Mashiga_Daraja) {
    if (!준비됨) return -100;
    if (Aiki == 1) { netif_set_up(&haɗi_na_ura); return 0; }
    if (Aiki == 2) { netif_set_down(&haɗi_na_ura); return 0; }
    if (Aiki != 0) return -22;
    /* 유니캐스트 IPv4, 연속 Burtu_Daraja, 같은 망의 선택적 Tanadaddiyar_daraja Mashiga_Daraja. */
    uint32_t 뒤집은가림 = ~Burtu_Daraja;
    if (!Burtu_Daraja || (뒤집은가림 & (뒤집은가림 + 1)) || !imel || (imel >> 24) == 127 ||
        (imel >> 24) == 0 || (imel >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(imel & 뒤집은가림) || (imel & 뒤집은가림) == 뒤집은가림)) ||
        (Mashiga_Daraja && ((Mashiga_Daraja & Burtu_Daraja) != (imel & Burtu_Daraja) || Mashiga_Daraja == imel || (Mashiga_Daraja >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(Mashiga_Daraja & 뒤집은가림) || (Mashiga_Daraja & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 imel 변경으로 몰래 끊지 않는다. */
    for (unsigned Indes = 0; Indes < 32; Indes++) if (통신끝점들[Indes].rubuta_ɓangare &&
        !(통신끝점들[Indes].수신창구 && 통신끝점들[Indes].haɗi_masarrafa && ip_addr_isany(&통신끝점들[Indes].haɗi_masarrafa->local_ip))) return -16;
    if(유선사용)dhcp_stop(&haɗi_na_ura);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(imel)); ip4_addr_set_u32(&새가림, lwip_htonl(Burtu_Daraja)); ip4_addr_set_u32(&새관문, lwip_htonl(Mashiga_Daraja));
    netif_set_addr(&haɗi_na_ura, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *Ƙarshe_maki, struct pbuf *Tarin_bayani, const ip_addr_t *imel) {
    (void)인수; (void)Ƙarshe_maki;
    unsigned char 머리[20], mayar_da_martani[16];
    if (응답상태 != -11 || Tarin_bayani->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(imel))) != 시험주소 || pbuf_copy_partial(Tarin_bayani, 머리, 20, 0) != 20) return 0;
    unsigned Kai_girma = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Kai_girma < 20 || Tarin_bayani->tot_len < Kai_girma + 16 ||
        pbuf_copy_partial(Tarin_bayani, mayar_da_martani, 16, Kai_girma) != 16 || mayar_da_martani[0] || mayar_da_martani[1] ||
        (((unsigned)mayar_da_martani[4] << 8) | mayar_da_martani[5]) != 시험식별자 ||
        (((unsigned)mayar_da_martani[6] << 8) | mayar_da_martani[7]) != 시험순서 ||
        mayar_da_martani[8] != 'J' || mayar_da_martani[9] != 'K' || mayar_da_martani[10] != 'O' || mayar_da_martani[11] != 'S' ||
        (((uint32_t)mayar_da_martani[12] << 24) | ((uint32_t)mayar_da_martani[13] << 16) | ((uint32_t)mayar_da_martani[14] << 8) | mayar_da_martani[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(Tarin_bayani, Kai_girma)) return 0;
    if (inet_chksum_pbuf(Tarin_bayani)) { pbuf_add_header(Tarin_bayani, Kai_girma); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(Tarin_bayani); return 1;
}
int 응답시험시작(uint32_t imel, unsigned Hanyar_jejjerawa_Daraja) {
    if (!준비됨 || !netif_is_up(&haɗi_na_ura)) return -100;
    if (!imel || (imel >> 28) >= 14 || imel == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = imel; 시험순서 = Hanyar_jejjerawa_Daraja & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char Tarin_bayani[32] = {8,0,0,0};
    Tarin_bayani[4] = 시험식별자 >> 8; Tarin_bayani[5] = 시험식별자; Tarin_bayani[6] = 시험순서 >> 8; Tarin_bayani[7] = 시험순서;
    Tarin_bayani[8]='J'; Tarin_bayani[9]='K'; Tarin_bayani[10]='O'; Tarin_bayani[11]='S';
    Tarin_bayani[12]=시험시각 >> 24; Tarin_bayani[13]=시험시각 >> 16; Tarin_bayani[14]=시험시각 >> 8; Tarin_bayani[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(Tarin_bayani); 자리++) Tarin_bayani[자리] = 자리;
    uint16_t tabatawa_checksum = inet_chksum(Tarin_bayani, sizeof(Tarin_bayani)); memcpy(Tarin_bayani + 2, &tabatawa_checksum, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(Tarin_bayani), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, Tarin_bayani, sizeof(Tarin_bayani)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(imel));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned Mashigar_bayanai_Daraja) {
    통신망살피기();
    return Mashigar_bayanai_Daraja == 0 ? 응답상태 : Mashigar_bayanai_Daraja == 1 ? (int)응답시간 : Mashigar_bayanai_Daraja == 2 ? (int)응답차례 : -22;
}
