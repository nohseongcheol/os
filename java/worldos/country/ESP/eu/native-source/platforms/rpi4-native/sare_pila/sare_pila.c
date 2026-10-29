#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "sare_pila.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../urruneko_balio/urruneko_balio.h"
#include "haridun_sare.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define gailu_izena_eman(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif konexio_gailu;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_byte_ZENBATU, 보낸바이트수, 버린전문수;
typedef struct {
    int MOTA_Kategoria, 수신창구, informatika_zain, 연결됨, fitxategi_amaitu, errorea;
    struct tcp_pcb *konexio_kontrol;
    struct udp_pcb *전문제어;
    unsigned aurrekoa_sarrera, sarrera_ZENBATU;
    unsigned char datuak[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], pareko_helbide;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int errorearen_zenbaki(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *eskuratu_balio(int fitxategi_helduleku) { return fitxategi_helduleku >= 0 && fitxategi_helduleku < 32 && 통신끝점들[fitxategi_helduleku].MOTA_Kategoria ? &통신끝점들[fitxategi_helduleku] : 0; }
static int 예약하기(int MOTA_Kategoria) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].MOTA_Kategoria) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].MOTA_Kategoria = MOTA_Kategoria; 통신끝점들[순번].informatika_zain = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned karaktere_kode) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = karaktere_kode; }
static err_t 출력결과(struct netif *elementu_ZENBATU, struct pbuf *datuak_kargu, const ip4_addr_t *helbide) {
    (void)elementu_ZENBATU; (void)helbide;
    if (datuak_kargu->tot_len > 1500 || 송신개수 + 2 * datuak_kargu->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Hurrengoa_Geruzak = datuak_kargu; Hurrengoa_Geruzak; Hurrengoa_Geruzak = Hurrengoa_Geruzak->next) for (unsigned 순번 = 0; 순번 < Hurrengoa_Geruzak->len; 순번++) {
        unsigned karaktere_kode = ((unsigned char *)Hurrengoa_Geruzak->payload)[순번];
        if (karaktere_kode == 192 || karaktere_kode == 219) { 내보내기(219); 내보내기(karaktere_kode == 192 ? 220 : 221); } else 내보내기(karaktere_kode);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += datuak_kargu->tot_len; return ERR_OK;
}
static err_t 준비하기(struct netif *elementu_ZENBATU) { elementu_ZENBATU->name[0] = 's'; elementu_ZENBATU->name[1] = 'l'; elementu_ZENBATU->mtu = 1500; elementu_ZENBATU->output = 출력결과; return ERR_OK; }
void 통신망준비(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    gailu_izena_eman(보조장치 + 4) |= 1; gailu_izena_eman(보조장치 + 0x60) = 0; gailu_izena_eman(보조장치 + 0x44) = 0;
    gailu_izena_eman(보조장치 + 0x48) = 0xc6; gailu_izena_eman(보조장치 + 0x4c) = 3; gailu_izena_eman(보조장치 + 0x68) = 270; gailu_izena_eman(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internet_helbide, bit_maskara, atebide_helbide;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Internet_helbide, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_maskara, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&atebide_helbide, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&konexio_gailu, &Internet_helbide, &bit_maskara, &atebide_helbide, 0, 유선사용?유선망준비:준비하기, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&konexio_gailu); netif_set_up(&konexio_gailu);if(!유선사용)netif_set_link_up(&konexio_gailu); 준비됨 = 1;
    원격준비();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *transmisio_kontrol_blokeatu, struct pbuf *datuak_kargu, err_t errorea) {
    통신끝점 *kate_datuak = 부가인수; (void)transmisio_kontrol_blokeatu; (void)errorea;
    if (!datuak_kargu) { kate_datuak->fitxategi_amaitu = 1; return ERR_OK; }
    if (datuak_kargu->tot_len > sizeof(kate_datuak->datuak) - kate_datuak->sarrera_ZENBATU) return ERR_MEM;
    unsigned 현재위치 = (kate_datuak->aurrekoa_sarrera + kate_datuak->sarrera_ZENBATU) % sizeof(kate_datuak->datuak);
    for (struct pbuf *Hurrengoa_Geruzak = datuak_kargu; Hurrengoa_Geruzak; Hurrengoa_Geruzak = Hurrengoa_Geruzak->next) for (unsigned 순번 = 0; 순번 < Hurrengoa_Geruzak->len; 순번++) {
        kate_datuak->datuak[현재위치] = ((unsigned char *)Hurrengoa_Geruzak->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(kate_datuak->datuak);
    }
    kate_datuak->sarrera_ZENBATU += datuak_kargu->tot_len; pbuf_free(datuak_kargu); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t errorea) { 통신끝점 *kate_datuak = 부가인수; kate_datuak->konexio_kontrol = 0; kate_datuak->errorea = errorearen_zenbaki(errorea); }
static void 되부름목록(통신끝점 *kate_datuak) { tcp_arg(kate_datuak->konexio_kontrol, kate_datuak); tcp_recv(kate_datuak->konexio_kontrol, 수신됨); tcp_err(kate_datuak->konexio_kontrol, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *transmisio_kontrol_blokeatu, err_t errorea) {
    통신끝점 *kate_datuak = 부가인수; (void)transmisio_kontrol_blokeatu; if (errorea) kate_datuak->errorea = errorearen_zenbaki(errorea); else kate_datuak->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *transmisio_kontrol_blokeatu, err_t errorea) {
    통신끝점 *부모항목 = 부가인수; if (errorea) return errorea;
    int fitxategi_helduleku = 예약하기(1); if (fitxategi_helduleku < 0) return ERR_MEM;
    통신끝점 *kate_datuak = &통신끝점들[fitxategi_helduleku]; kate_datuak->konexio_kontrol = transmisio_kontrol_blokeatu; kate_datuak->연결됨 = 1; kate_datuak->informatika_zain = (int)(부모항목 - 통신끝점들);
    kate_datuak->pareko_helbide = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&transmisio_kontrol_blokeatu->remote_ip))); kate_datuak->상대창구번호 = transmisio_kontrol_blokeatu->remote_port;
    되부름목록(kate_datuak); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *transmisio_kontrol_blokeatu, struct pbuf *datuak_kargu, const ip_addr_t *helbide, u16_t ataka_zenbaki) {
    통신끝점 *kate_datuak = 부가인수; (void)transmisio_kontrol_blokeatu;
    if (kate_datuak->sarrera_ZENBATU < 4 && datuak_kargu->tot_len <= 512) {
        unsigned kargu_INDIZE = (kate_datuak->aurrekoa_sarrera + kate_datuak->sarrera_ZENBATU) % 4;
        pbuf_copy_partial(datuak_kargu, kate_datuak->datuak + kargu_INDIZE * 512, datuak_kargu->tot_len, 0);
        kate_datuak->길이목록[kargu_INDIZE] = datuak_kargu->tot_len; kate_datuak->접속번호들[kargu_INDIZE] = ataka_zenbaki;
        kate_datuak->주소목록[kargu_INDIZE] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(helbide))); kate_datuak->sarrera_ZENBATU++;
    }
    pbuf_free(datuak_kargu);
}
int 통신끝점만들기(int MOTA_Kategoria) {
    if (!준비됨) return -100;
    if (MOTA_Kategoria != 1 && MOTA_Kategoria != 2) return -93;
    int fitxategi_helduleku = 예약하기(MOTA_Kategoria); if (fitxategi_helduleku < 0) return fitxategi_helduleku;
    통신끝점 *kate_datuak = &통신끝점들[fitxategi_helduleku];
    if (MOTA_Kategoria == 1) { kate_datuak->konexio_kontrol = tcp_new(); if (kate_datuak->konexio_kontrol) 되부름목록(kate_datuak); }
    else { kate_datuak->전문제어 = udp_new(); if (kate_datuak->전문제어) udp_recv(kate_datuak->전문제어, 전문, kate_datuak); }
    if (!kate_datuak->konexio_kontrol && !kate_datuak->전문제어) { kate_datuak->MOTA_Kategoria = 0; return -12; } return fitxategi_helduleku;
}
int 망주소묶기(int fitxategi_helduleku, uint32_t helbide, unsigned ataka_zenbaki) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak) return -9;
    if (ataka_zenbaki > 65535 || (helbide && helbide != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&konexio_gailu))) && helbide != 0x7f000001)) return -99;
    ip_addr_t Internet_helbide; ip_addr_set_ip4_u32(&Internet_helbide, lwip_htonl(helbide));
    err_t 보조항목 = kate_datuak->MOTA_Kategoria == 1 ? tcp_bind(kate_datuak->konexio_kontrol, &Internet_helbide, ataka_zenbaki) : udp_bind(kate_datuak->전문제어, &Internet_helbide, ataka_zenbaki); return 보조항목 ? errorearen_zenbaki(보조항목) : 0;
}
void 통신주소재사용(int fitxategi_helduleku) { 통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (kate_datuak && kate_datuak->konexio_kontrol) ip_set_option(kate_datuak->konexio_kontrol, SOF_REUSEADDR); }
int 연결기다리기(int fitxategi_helduleku) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak || kate_datuak->MOTA_Kategoria != 1) return -9;
    if (kate_datuak->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *transmisio_kontrol_blokeatu = tcp_listen_with_backlog_and_err(kate_datuak->konexio_kontrol, 4, &보조항목);
    if (!transmisio_kontrol_blokeatu) return errorearen_zenbaki(보조항목); kate_datuak->konexio_kontrol = transmisio_kontrol_blokeatu; kate_datuak->수신창구 = 1; tcp_arg(transmisio_kontrol_blokeatu, kate_datuak); tcp_accept(transmisio_kontrol_blokeatu, 연결받음); return 0;
}
int 망연결하기(int fitxategi_helduleku, uint32_t helbide, unsigned ataka_zenbaki) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak || kate_datuak->MOTA_Kategoria != 1) return -9;
    if (kate_datuak->errorea) return kate_datuak->errorea;
    if (kate_datuak->연결됨) return 0;
    if (kate_datuak->상대창구번호) return -115;
    if (!ataka_zenbaki || ataka_zenbaki > 65535 || !helbide) return -22;
    ip_addr_t Internet_helbide; ip_addr_set_ip4_u32(&Internet_helbide, lwip_htonl(helbide));
    kate_datuak->pareko_helbide = helbide; kate_datuak->상대창구번호 = ataka_zenbaki;
    err_t 보조항목 = tcp_connect(kate_datuak->konexio_kontrol, &Internet_helbide, ataka_zenbaki, 연결됨); return 보조항목 ? errorearen_zenbaki(보조항목) : -115;
}
int 망연결받기(int fitxategi_helduleku) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak || !kate_datuak->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].MOTA_Kategoria == 1 && 통신끝점들[순번].informatika_zain == fitxategi_helduleku) { 통신끝점들[순번].informatika_zain = -1; return 순번; }
    return -11;
}
int 통신읽기(int fitxategi_helduleku, void *datuak, unsigned elementu_ZENBATU) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak || kate_datuak->MOTA_Kategoria != 1) return -9;
    if (!elementu_ZENBATU) return 0; if (!kate_datuak->sarrera_ZENBATU) return kate_datuak->errorea ? kate_datuak->errorea : kate_datuak->fitxategi_amaitu ? 0 : -11;
    if (elementu_ZENBATU > kate_datuak->sarrera_ZENBATU) elementu_ZENBATU = kate_datuak->sarrera_ZENBATU;
    for (unsigned 순번 = 0; 순번 < elementu_ZENBATU; 순번++) { ((unsigned char *)datuak)[순번] = kate_datuak->datuak[kate_datuak->aurrekoa_sarrera]; kate_datuak->aurrekoa_sarrera = (kate_datuak->aurrekoa_sarrera + 1) % sizeof(kate_datuak->datuak); }
    kate_datuak->sarrera_ZENBATU -= elementu_ZENBATU; if (kate_datuak->konexio_kontrol) tcp_recved(kate_datuak->konexio_kontrol, elementu_ZENBATU); return elementu_ZENBATU;
}
int 통신쓰기(int fitxategi_helduleku, const void *datuak, unsigned elementu_ZENBATU) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak || kate_datuak->MOTA_Kategoria != 1) return -9;
    if (kate_datuak->errorea) return kate_datuak->errorea; if (!kate_datuak->konexio_kontrol || !kate_datuak->연결됨) return -107;
    if (!elementu_ZENBATU) return 0; if (elementu_ZENBATU > tcp_sndbuf(kate_datuak->konexio_kontrol)) elementu_ZENBATU = tcp_sndbuf(kate_datuak->konexio_kontrol);
    if (!elementu_ZENBATU) return -11; if (elementu_ZENBATU > 1024) elementu_ZENBATU = 1024;
    err_t 보조항목 = tcp_write(kate_datuak->konexio_kontrol, datuak, elementu_ZENBATU, TCP_WRITE_FLAG_COPY); if (보조항목) return errorearen_zenbaki(보조항목);
    tcp_output(kate_datuak->konexio_kontrol); return elementu_ZENBATU;
}
int 전문보내기(int fitxategi_helduleku, const void *datuak, unsigned elementu_ZENBATU, uint32_t helbide, unsigned ataka_zenbaki) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak || kate_datuak->MOTA_Kategoria != 2) return -9;
    if (elementu_ZENBATU > 512) return -90; if (!ataka_zenbaki || ataka_zenbaki > 65535) return -22;
    struct pbuf *datuak_kargu = pbuf_alloc(PBUF_TRANSPORT, elementu_ZENBATU, PBUF_RAM); if (!datuak_kargu) return -11;
    pbuf_take(datuak_kargu, datuak, elementu_ZENBATU); ip_addr_t Internet_helbide; ip_addr_set_ip4_u32(&Internet_helbide, lwip_htonl(helbide));
    err_t 보조항목 = udp_sendto(kate_datuak->전문제어, datuak_kargu, &Internet_helbide, ataka_zenbaki); pbuf_free(datuak_kargu); return 보조항목 ? errorearen_zenbaki(보조항목) : (int)elementu_ZENBATU;
}
int 전문받기(int fitxategi_helduleku, void *datuak, unsigned elementu_ZENBATU) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak || kate_datuak->MOTA_Kategoria != 2) return -9;
    if (!kate_datuak->sarrera_ZENBATU) return -11; unsigned 현재위치 = kate_datuak->aurrekoa_sarrera;
    if (elementu_ZENBATU > kate_datuak->길이목록[현재위치]) elementu_ZENBATU = kate_datuak->길이목록[현재위치]; memcpy(datuak, kate_datuak->datuak + 현재위치 * 512, elementu_ZENBATU);
    kate_datuak->상대창구번호 = kate_datuak->접속번호들[현재위치]; kate_datuak->pareko_helbide = kate_datuak->주소목록[현재위치]; kate_datuak->aurrekoa_sarrera = (현재위치 + 1) % 4; kate_datuak->sarrera_ZENBATU--; return elementu_ZENBATU;
}
unsigned sare_ataka_zenbaki(int fitxategi_helduleku) { 통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); return !kate_datuak ? 0 : kate_datuak->konexio_kontrol ? kate_datuak->konexio_kontrol->local_port : kate_datuak->전문제어 ? kate_datuak->전문제어->local_port : 0; }
unsigned pareko_ataka_zenbaki(int fitxategi_helduleku) { 통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); return kate_datuak ? kate_datuak->상대창구번호 : 0; }
uint32_t 상대통신주소(int fitxategi_helduleku) { 통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); return kate_datuak ? kate_datuak->pareko_helbide : 0; }
void itxi_sare(int fitxategi_helduleku) {
    통신끝점 *kate_datuak = eskuratu_balio(fitxategi_helduleku); if (!kate_datuak) return;
    if (kate_datuak->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].MOTA_Kategoria && 통신끝점들[순번].informatika_zain == fitxategi_helduleku) itxi_sare(순번);
    if (kate_datuak->konexio_kontrol) {
        tcp_arg(kate_datuak->konexio_kontrol, 0); if (kate_datuak->수신창구) tcp_accept(kate_datuak->konexio_kontrol, 0); else { tcp_recv(kate_datuak->konexio_kontrol, 0); tcp_err(kate_datuak->konexio_kontrol, 0); }
        if (tcp_close(kate_datuak->konexio_kontrol) != ERR_OK) tcp_abort(kate_datuak->konexio_kontrol);
    }
    if (kate_datuak->전문제어) udp_remove(kate_datuak->전문제어); kate_datuak->MOTA_Kategoria = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&konexio_gailu);
    for (unsigned esleitutako_aurrekontu = 0; !유선사용 && esleitutako_aurrekontu < 4096 && (gailu_izena_eman(보조장치 + 0x54) & 1); esleitutako_aurrekontu++) {
        unsigned karaktere_kode = gailu_izena_eman(보조장치 + 0x40) & 255;
        if (karaktere_kode == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *datuak_kargu = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (datuak_kargu) { 받은전문수++; RECEIVED_byte_ZENBATU += 수신사용량; pbuf_take(datuak_kargu, 수신자료, 수신사용량); if (konexio_gailu.input(datuak_kargu, &konexio_gailu) != ERR_OK) { 버린전문수++; pbuf_free(datuak_kargu); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (karaktere_kode == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (karaktere_kode != 220 && karaktere_kode != 221) 수신오류 = 1; karaktere_kode = karaktere_kode == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = karaktere_kode; else 수신오류 = 1;
        }
    }
    netif_poll(&konexio_gailu); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned esleitutako_aurrekontu = 0; esleitutako_aurrekontu < 4096 && 송신개수 && (gailu_izena_eman(보조장치 + 0x54) & 0x20); esleitutako_aurrekontu++) {
        gailu_izena_eman(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Ezarpenak·조회는 lwIP의 benetako_datuak 인터페이스와 amaitu_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned sarrera_balio, unsigned INDIZE) {
    if(sarrera_balio==20)return 유선사용;
    if(sarrera_balio==21)return 준비됨&&netif_is_link_up(&konexio_gailu);
    if(sarrera_balio==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&sarrera_balio>=4&&sarrera_balio<=8)return 유선망집계(sarrera_balio-4);
    if (sarrera_balio == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&konexio_gailu)));
    if (sarrera_balio == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&konexio_gailu)));
    if (sarrera_balio == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&konexio_gailu)));
    if (sarrera_balio == 3) return netif_is_up(&konexio_gailu) != 0;
    if (sarrera_balio == 4) return 받은전문수;
    if (sarrera_balio == 5) return 보낸전문수;
    if (sarrera_balio == 6) return RECEIVED_byte_ZENBATU;
    if (sarrera_balio == 7) return 보낸바이트수;
    if (sarrera_balio == 8) return 버린전문수;
    if (sarrera_balio == 9) return 송신개수;
    if (INDIZE >= 32) return 0;
    통신끝점 *amaitu_p = &통신끝점들[INDIZE];
    if (sarrera_balio == 10) return amaitu_p->MOTA_Kategoria;
    if (!amaitu_p->MOTA_Kategoria) return 0;
    if (sarrera_balio == 11) return sare_ataka_zenbaki(INDIZE);
    if (sarrera_balio == 12) return amaitu_p->pareko_helbide;
    if (sarrera_balio == 13) return amaitu_p->상대창구번호;
    if (sarrera_balio == 14) return amaitu_p->수신창구 ? 1 : amaitu_p->fitxategi_amaitu ? 3 : amaitu_p->errorea ? 4 : amaitu_p->연결됨 ? 2 : 0;
    if (sarrera_balio == 15) return amaitu_p->sarrera_ZENBATU;
    if (sarrera_balio == 16) {
        const ip_addr_t *helbide = amaitu_p->MOTA_Kategoria == 1 && amaitu_p->konexio_kontrol ? &amaitu_p->konexio_kontrol->local_ip :
            amaitu_p->MOTA_Kategoria == 2 && amaitu_p->전문제어 ? &amaitu_p->전문제어->local_ip : 0;
        return helbide ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(helbide))) : 0;
    }
    return 0;
}

int konfiguratu_sare(unsigned Ekintza, uint32_t helbide, uint32_t maskara_balio, uint32_t atebide_balio) {
    if (!준비됨) return -100;
    if (Ekintza == 1) { netif_set_up(&konexio_gailu); return 0; }
    if (Ekintza == 2) { netif_set_down(&konexio_gailu); return 0; }
    if (Ekintza != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maskara_balio, 같은 망의 선택적 balio_lehenetsi atebide_balio. */
    uint32_t 뒤집은가림 = ~maskara_balio;
    if (!maskara_balio || (뒤집은가림 & (뒤집은가림 + 1)) || !helbide || (helbide >> 24) == 127 ||
        (helbide >> 24) == 0 || (helbide >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(helbide & 뒤집은가림) || (helbide & 뒤집은가림) == 뒤집은가림)) ||
        (atebide_balio && ((atebide_balio & maskara_balio) != (helbide & maskara_balio) || atebide_balio == helbide || (atebide_balio >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(atebide_balio & 뒤집은가림) || (atebide_balio & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 helbide 변경으로 몰래 끊지 않는다. */
    for (unsigned INDIZE = 0; INDIZE < 32; INDIZE++) if (통신끝점들[INDIZE].MOTA_Kategoria &&
        !(통신끝점들[INDIZE].수신창구 && 통신끝점들[INDIZE].konexio_kontrol && ip_addr_isany(&통신끝점들[INDIZE].konexio_kontrol->local_ip))) return -16;
    if(유선사용)dhcp_stop(&konexio_gailu);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(helbide)); ip4_addr_set_u32(&새가림, lwip_htonl(maskara_balio)); ip4_addr_set_u32(&새관문, lwip_htonl(atebide_balio));
    netif_set_addr(&konexio_gailu, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *erantzun_amaiera_puntu;
static uint32_t 시험주소, 시험시각, erantzun_ordua;
static unsigned 시험순서, 시험식별자, erantzun_SEKUENTZIA;
static int erantzun_Egoera;
static u8_t 응답받음(void *Argumentuak, struct raw_pcb *amaitu_p, struct pbuf *datuak, const ip_addr_t *helbide) {
    (void)Argumentuak; (void)amaitu_p;
    unsigned char 머리[20], erantzun[16];
    if (erantzun_Egoera != -11 || datuak->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(helbide))) != 시험주소 || pbuf_copy_partial(datuak, 머리, 20, 0) != 20) return 0;
    unsigned 머리크기 = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || 머리크기 < 20 || datuak->tot_len < 머리크기 + 16 ||
        pbuf_copy_partial(datuak, erantzun, 16, 머리크기) != 16 || erantzun[0] || erantzun[1] ||
        (((unsigned)erantzun[4] << 8) | erantzun[5]) != 시험식별자 ||
        (((unsigned)erantzun[6] << 8) | erantzun[7]) != 시험순서 ||
        erantzun[8] != 'J' || erantzun[9] != 'K' || erantzun[10] != 'O' || erantzun[11] != 'S' ||
        (((uint32_t)erantzun[12] << 24) | ((uint32_t)erantzun[13] << 16) | ((uint32_t)erantzun[14] << 8) | erantzun[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(datuak, 머리크기)) return 0;
    if (inet_chksum_pbuf(datuak)) { pbuf_add_header(datuak, 머리크기); return 0; }
    erantzun_ordua = (uint32_t)보드밀리초() - 시험시각; erantzun_SEKUENTZIA = 머리[8]; erantzun_Egoera = 0;
    pbuf_free(datuak); return 1;
}
int 응답시험시작(uint32_t helbide, unsigned ordena_balio) {
    if (!준비됨 || !netif_is_up(&konexio_gailu)) return -100;
    if (!helbide || (helbide >> 28) >= 14 || helbide == 0xffffffffu) return -22;
    if (!erantzun_amaiera_puntu) { erantzun_amaiera_puntu = raw_new(IP_PROTO_ICMP); if (!erantzun_amaiera_puntu) return -12; raw_recv(erantzun_amaiera_puntu, 응답받음, 0); }
    시험주소 = helbide; 시험순서 = ordena_balio & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); erantzun_Egoera = -11; erantzun_ordua = erantzun_SEKUENTZIA = 0;
    unsigned char datuak[32] = {8,0,0,0};
    datuak[4] = 시험식별자 >> 8; datuak[5] = 시험식별자; datuak[6] = 시험순서 >> 8; datuak[7] = 시험순서;
    datuak[8]='J'; datuak[9]='K'; datuak[10]='O'; datuak[11]='S';
    datuak[12]=시험시각 >> 24; datuak[13]=시험시각 >> 16; datuak[14]=시험시각 >> 8; datuak[15]=시험시각;
    for (unsigned kargu_INDIZE = 16; kargu_INDIZE < sizeof(datuak); kargu_INDIZE++) datuak[kargu_INDIZE] = kargu_INDIZE;
    uint16_t egiaztapen_kontroleko_batura = inet_chksum(datuak, sizeof(datuak)); memcpy(datuak + 2, &egiaztapen_kontroleko_batura, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(datuak), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, datuak, sizeof(datuak)); ip_addr_t helburu_amaiera_puntu; ip_addr_set_ip4_u32(&helburu_amaiera_puntu, lwip_htonl(helbide));
    err_t 처리값 = raw_sendto(erantzun_amaiera_puntu, 전문, &helburu_amaiera_puntu); pbuf_free(전문);
    if (처리값) erantzun_Egoera = errorearen_zenbaki(처리값);
    return 처리값 ? erantzun_Egoera : 0;
}
int 응답시험읽기(unsigned sarrera_balio) {
    통신망살피기();
    return sarrera_balio == 0 ? erantzun_Egoera : sarrera_balio == 1 ? (int)erantzun_ordua : sarrera_balio == 2 ? (int)erantzun_SEKUENTZIA : -22;
}
