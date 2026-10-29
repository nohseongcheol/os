#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "hálózat_Sor.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../távoli_ÉRTÉK/távoli_ÉRTÉK.h"
#include "vezetékes_hálózat.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define gép_jegyzék(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif ismerős_mobil;
static int 준비됨, ciklikus_lekérdezés;
static int használ_vezetékes_hálózat;
static unsigned fogad_felhasználás, 수신탈출, fogad_hiba;
static unsigned char fogad_adatpuffer[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t KAPOTT_datagram_DARAB, 보낸전문수, KAPOTT_bájt_DARAB, 보낸바이트수, 버린전문수;
typedef struct {
    int beír_terület, fogad_port, informatikai_részleg_Függő, 연결됨, Fájl_megszüntet, HIBA;
    struct tcp_pcb *ismerős_vezérlő;
    struct udp_pcb *datagram_vezérlő;
    unsigned elülső_kamera_bejegyzés, bejegyzés_DARAB;
    unsigned char adat[4096];
    unsigned 길이목록[4], 접속번호들[4], társ_végpont_szám;
    uint32_t 주소목록[4], társ_CÍM;
} szoftvercsatorna_végpont_3db661a2;
static szoftvercsatorna_végpont_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int hibaszám(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static szoftvercsatorna_végpont_3db661a2 *áthúz_ÉRTÉK(int fájlleíró) { return fájlleíró >= 0 && fájlleíró < 32 && 통신끝점들[fájlleíró].beír_terület ? &통신끝점들[fájlleíró] : 0; }
static int 예약하기(int beír_terület) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].beír_terület) {
        memset(&통신끝점들[순번], 0, sizeof(szoftvercsatorna_végpont_3db661a2)); 통신끝점들[순번].beír_terület = beír_terület; 통신끝점들[순번].informatikai_részleg_Függő = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kódpont) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kódpont; }
static err_t kimenet(struct netif *cikk_DARAB, struct pbuf *adat_pozíció, const ip4_addr_t *CÍM) {
    (void)cikk_DARAB; (void)CÍM;
    if (adat_pozíció->tot_len > 1500 || 송신개수 + 2 * adat_pozíció->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Tovább_Ofszet = adat_pozíció; Tovább_Ofszet; Tovább_Ofszet = Tovább_Ofszet->next) for (unsigned 순번 = 0; 순번 < Tovább_Ofszet->len; 순번++) {
        unsigned kódpont = ((unsigned char *)Tovább_Ofszet->payload)[순번];
        if (kódpont == 192 || kódpont == 219) { 내보내기(219); 내보내기(kódpont == 192 ? 220 : 221); } else 내보내기(kódpont);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += adat_pozíció->tot_len; return ERR_OK;
}
static err_t Előkészítés_CLR(struct netif *cikk_DARAB) { cikk_DARAB->name[0] = 's'; cikk_DARAB->name[1] = 'l'; cikk_DARAB->mtu = 1500; cikk_DARAB->output = kimenet; return ERR_OK; }
void Előkészítés_hálózat(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    gép_jegyzék(보조장치 + 4) |= 1; gép_jegyzék(보조장치 + 0x60) = 0; gép_jegyzék(보조장치 + 0x44) = 0;
    gép_jegyzék(보조장치 + 0x48) = 0xc6; gép_jegyzék(보조장치 + 0x4c) = 3; gép_jegyzék(보조장치 + 0x68) = 270; gép_jegyzék(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetcím, bitmaszk, átjárócím;
    használ_vezetékes_hálózat=유선장치있음();
    ip4_addr_set_u32(&internetcím, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmaszk, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&átjárócím, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&ismerős_mobil, &internetcím, &bitmaszk, &átjárócím, 0, használ_vezetékes_hálózat?Előkészítés_vezetékes_hálózat:Előkészítés_CLR, használ_vezetékes_hálózat?ethernet_input:ip4_input))return;
    netif_set_default(&ismerős_mobil); netif_set_up(&ismerős_mobil);if(!használ_vezetékes_hálózat)netif_set_link_up(&ismerős_mobil); 준비됨 = 1;
    Előkészítés_távoli();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *adat_pozíció, err_t HIBA) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = 부가인수; (void)통신제어블록; (void)HIBA;
    if (!adat_pozíció) { sztring_adat->Fájl_megszüntet = 1; return ERR_OK; }
    if (adat_pozíció->tot_len > sizeof(sztring_adat->adat) - sztring_adat->bejegyzés_DARAB) return ERR_MEM;
    unsigned aktuális_pozíció = (sztring_adat->elülső_kamera_bejegyzés + sztring_adat->bejegyzés_DARAB) % sizeof(sztring_adat->adat);
    for (struct pbuf *Tovább_Ofszet = adat_pozíció; Tovább_Ofszet; Tovább_Ofszet = Tovább_Ofszet->next) for (unsigned 순번 = 0; 순번 < Tovább_Ofszet->len; 순번++) {
        sztring_adat->adat[aktuális_pozíció] = ((unsigned char *)Tovább_Ofszet->payload)[순번]; aktuális_pozíció = (aktuális_pozíció + 1) % sizeof(sztring_adat->adat);
    }
    sztring_adat->bejegyzés_DARAB += adat_pozíció->tot_len; pbuf_free(adat_pozíció); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t HIBA) { szoftvercsatorna_végpont_3db661a2 *sztring_adat = 부가인수; sztring_adat->ismerős_vezérlő = 0; sztring_adat->HIBA = hibaszám(HIBA); }
static void 되부름목록(szoftvercsatorna_végpont_3db661a2 *sztring_adat) { tcp_arg(sztring_adat->ismerős_vezérlő, sztring_adat); tcp_recv(sztring_adat->ismerős_vezérlő, 수신됨); tcp_err(sztring_adat->ismerős_vezérlő, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t HIBA) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = 부가인수; (void)통신제어블록; if (HIBA) sztring_adat->HIBA = hibaszám(HIBA); else sztring_adat->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t HIBA) {
    szoftvercsatorna_végpont_3db661a2 *szülő = 부가인수; if (HIBA) return HIBA;
    int fájlleíró = 예약하기(1); if (fájlleíró < 0) return ERR_MEM;
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = &통신끝점들[fájlleíró]; sztring_adat->ismerős_vezérlő = 통신제어블록; sztring_adat->연결됨 = 1; sztring_adat->informatikai_részleg_Függő = (int)(szülő - 통신끝점들);
    sztring_adat->társ_CÍM = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); sztring_adat->társ_végpont_szám = 통신제어블록->remote_port;
    되부름목록(sztring_adat); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *adat_pozíció, const ip_addr_t *CÍM, u16_t portszám) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = 부가인수; (void)통신제어블록;
    if (sztring_adat->bejegyzés_DARAB < 4 && adat_pozíció->tot_len <= 512) {
        unsigned helyzetindex = (sztring_adat->elülső_kamera_bejegyzés + sztring_adat->bejegyzés_DARAB) % 4;
        pbuf_copy_partial(adat_pozíció, sztring_adat->adat + helyzetindex * 512, adat_pozíció->tot_len, 0);
        sztring_adat->길이목록[helyzetindex] = adat_pozíció->tot_len; sztring_adat->접속번호들[helyzetindex] = portszám;
        sztring_adat->주소목록[helyzetindex] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(CÍM))); sztring_adat->bejegyzés_DARAB++;
    }
    pbuf_free(adat_pozíció);
}
int készít_szoftvercsatorna_végpont(int beír_terület) {
    if (!준비됨) return -100;
    if (beír_terület != 1 && beír_terület != 2) return -93;
    int fájlleíró = 예약하기(beír_terület); if (fájlleíró < 0) return fájlleíró;
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = &통신끝점들[fájlleíró];
    if (beír_terület == 1) { sztring_adat->ismerős_vezérlő = tcp_new(); if (sztring_adat->ismerős_vezérlő) 되부름목록(sztring_adat); }
    else { sztring_adat->datagram_vezérlő = udp_new(); if (sztring_adat->datagram_vezérlő) udp_recv(sztring_adat->datagram_vezérlő, datagram, sztring_adat); }
    if (!sztring_adat->ismerős_vezérlő && !sztring_adat->datagram_vezérlő) { sztring_adat->beír_terület = 0; return -12; } return fájlleíró;
}
int NET_BIND(int fájlleíró, uint32_t CÍM, unsigned portszám) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat) return -9;
    if (portszám > 65535 || (CÍM && CÍM != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ismerős_mobil))) && CÍM != 0x7f000001)) return -99;
    ip_addr_t internetcím; ip_addr_set_ip4_u32(&internetcím, lwip_htonl(CÍM));
    err_t 보조항목 = sztring_adat->beír_terület == 1 ? tcp_bind(sztring_adat->ismerős_vezérlő, &internetcím, portszám) : udp_bind(sztring_adat->datagram_vezérlő, &internetcím, portszám); return 보조항목 ? hibaszám(보조항목) : 0;
}
void 통신주소재사용(int fájlleíró) { szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (sztring_adat && sztring_adat->ismerős_vezérlő) ip_set_option(sztring_adat->ismerős_vezérlő, SOF_REUSEADDR); }
int NET_figyelés(int fájlleíró) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat || sztring_adat->beír_terület != 1) return -9;
    if (sztring_adat->fogad_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(sztring_adat->ismerős_vezérlő, 4, &보조항목);
    if (!통신제어블록) return hibaszám(보조항목); sztring_adat->ismerős_vezérlő = 통신제어블록; sztring_adat->fogad_port = 1; tcp_arg(통신제어블록, sztring_adat); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_KAPCSOLAT(int fájlleíró, uint32_t CÍM, unsigned portszám) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat || sztring_adat->beír_terület != 1) return -9;
    if (sztring_adat->HIBA) return sztring_adat->HIBA;
    if (sztring_adat->연결됨) return 0;
    if (sztring_adat->társ_végpont_szám) return -115;
    if (!portszám || portszám > 65535 || !CÍM) return -22;
    ip_addr_t internetcím; ip_addr_set_ip4_u32(&internetcím, lwip_htonl(CÍM));
    sztring_adat->társ_CÍM = CÍM; sztring_adat->társ_végpont_szám = portszám;
    err_t 보조항목 = tcp_connect(sztring_adat->ismerős_vezérlő, &internetcím, portszám, 연결됨); return 보조항목 ? hibaszám(보조항목) : -115;
}
int NET_elfogad(int fájlleíró) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat || !sztring_adat->fogad_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].beír_terület == 1 && 통신끝점들[순번].informatikai_részleg_Függő == fájlleíró) { 통신끝점들[순번].informatikai_részleg_Függő = -1; return 순번; }
    return -11;
}
int 통신읽기(int fájlleíró, void *adat, unsigned cikk_DARAB) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat || sztring_adat->beír_terület != 1) return -9;
    if (!cikk_DARAB) return 0; if (!sztring_adat->bejegyzés_DARAB) return sztring_adat->HIBA ? sztring_adat->HIBA : sztring_adat->Fájl_megszüntet ? 0 : -11;
    if (cikk_DARAB > sztring_adat->bejegyzés_DARAB) cikk_DARAB = sztring_adat->bejegyzés_DARAB;
    for (unsigned 순번 = 0; 순번 < cikk_DARAB; 순번++) { ((unsigned char *)adat)[순번] = sztring_adat->adat[sztring_adat->elülső_kamera_bejegyzés]; sztring_adat->elülső_kamera_bejegyzés = (sztring_adat->elülső_kamera_bejegyzés + 1) % sizeof(sztring_adat->adat); }
    sztring_adat->bejegyzés_DARAB -= cikk_DARAB; if (sztring_adat->ismerős_vezérlő) tcp_recved(sztring_adat->ismerős_vezérlő, cikk_DARAB); return cikk_DARAB;
}
int NET_ír(int fájlleíró, const void *adat, unsigned cikk_DARAB) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat || sztring_adat->beír_terület != 1) return -9;
    if (sztring_adat->HIBA) return sztring_adat->HIBA; if (!sztring_adat->ismerős_vezérlő || !sztring_adat->연결됨) return -107;
    if (!cikk_DARAB) return 0; if (cikk_DARAB > tcp_sndbuf(sztring_adat->ismerős_vezérlő)) cikk_DARAB = tcp_sndbuf(sztring_adat->ismerős_vezérlő);
    if (!cikk_DARAB) return -11; if (cikk_DARAB > 1024) cikk_DARAB = 1024;
    err_t 보조항목 = tcp_write(sztring_adat->ismerős_vezérlő, adat, cikk_DARAB, TCP_WRITE_FLAG_COPY); if (보조항목) return hibaszám(보조항목);
    tcp_output(sztring_adat->ismerős_vezérlő); return cikk_DARAB;
}
int küld_datagram(int fájlleíró, const void *adat, unsigned cikk_DARAB, uint32_t CÍM, unsigned portszám) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat || sztring_adat->beír_terület != 2) return -9;
    if (cikk_DARAB > 512) return -90; if (!portszám || portszám > 65535) return -22;
    struct pbuf *adat_pozíció = pbuf_alloc(PBUF_TRANSPORT, cikk_DARAB, PBUF_RAM); if (!adat_pozíció) return -11;
    pbuf_take(adat_pozíció, adat, cikk_DARAB); ip_addr_t internetcím; ip_addr_set_ip4_u32(&internetcím, lwip_htonl(CÍM));
    err_t 보조항목 = udp_sendto(sztring_adat->datagram_vezérlő, adat_pozíció, &internetcím, portszám); pbuf_free(adat_pozíció); return 보조항목 ? hibaszám(보조항목) : (int)cikk_DARAB;
}
int fogad_datagram(int fájlleíró, void *adat, unsigned cikk_DARAB) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat || sztring_adat->beír_terület != 2) return -9;
    if (!sztring_adat->bejegyzés_DARAB) return -11; unsigned aktuális_pozíció = sztring_adat->elülső_kamera_bejegyzés;
    if (cikk_DARAB > sztring_adat->길이목록[aktuális_pozíció]) cikk_DARAB = sztring_adat->길이목록[aktuális_pozíció]; memcpy(adat, sztring_adat->adat + aktuális_pozíció * 512, cikk_DARAB);
    sztring_adat->társ_végpont_szám = sztring_adat->접속번호들[aktuális_pozíció]; sztring_adat->társ_CÍM = sztring_adat->주소목록[aktuális_pozíció]; sztring_adat->elülső_kamera_bejegyzés = (aktuális_pozíció + 1) % 4; sztring_adat->bejegyzés_DARAB--; return cikk_DARAB;
}
unsigned hálózat_portszám(int fájlleíró) { szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); return !sztring_adat ? 0 : sztring_adat->ismerős_vezérlő ? sztring_adat->ismerős_vezérlő->local_port : sztring_adat->datagram_vezérlő ? sztring_adat->datagram_vezérlő->local_port : 0; }
unsigned társ_portszám(int fájlleíró) { szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); return sztring_adat ? sztring_adat->társ_végpont_szám : 0; }
uint32_t NET_társ_CÍM(int fájlleíró) { szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); return sztring_adat ? sztring_adat->társ_CÍM : 0; }
void bezár_hálózat(int fájlleíró) {
    szoftvercsatorna_végpont_3db661a2 *sztring_adat = áthúz_ÉRTÉK(fájlleíró); if (!sztring_adat) return;
    if (sztring_adat->fogad_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].beír_terület && 통신끝점들[순번].informatikai_részleg_Függő == fájlleíró) bezár_hálózat(순번);
    if (sztring_adat->ismerős_vezérlő) {
        tcp_arg(sztring_adat->ismerős_vezérlő, 0); if (sztring_adat->fogad_port) tcp_accept(sztring_adat->ismerős_vezérlő, 0); else { tcp_recv(sztring_adat->ismerős_vezérlő, 0); tcp_err(sztring_adat->ismerős_vezérlő, 0); }
        if (tcp_close(sztring_adat->ismerős_vezérlő) != ERR_OK) tcp_abort(sztring_adat->ismerős_vezérlő);
    }
    if (sztring_adat->datagram_vezérlő) udp_remove(sztring_adat->datagram_vezérlő); sztring_adat->beír_terület = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || ciklikus_lekérdezés) return; ciklikus_lekérdezés = 1;
    if(használ_vezetékes_hálózat)유선망살피기(&ismerős_mobil);
    for (unsigned költségkeret = 0; !használ_vezetékes_hálózat && költségkeret < 4096 && (gép_jegyzék(보조장치 + 0x54) & 1); költségkeret++) {
        unsigned kódpont = gép_jegyzék(보조장치 + 0x40) & 255;
        if (kódpont == 192) {
            if (fogad_felhasználás && !fogad_hiba && !수신탈출) {
                struct pbuf *adat_pozíció = pbuf_alloc(PBUF_RAW, fogad_felhasználás, PBUF_POOL);
                if (adat_pozíció) { KAPOTT_datagram_DARAB++; KAPOTT_bájt_DARAB += fogad_felhasználás; pbuf_take(adat_pozíció, fogad_adatpuffer, fogad_felhasználás); if (ismerős_mobil.input(adat_pozíció, &ismerős_mobil) != ERR_OK) { 버린전문수++; pbuf_free(adat_pozíció); } }
                else 버린전문수++;
            }
            else if (fogad_felhasználás) 버린전문수++;
            fogad_felhasználás = fogad_hiba = 수신탈출 = 0;
        } else if (kódpont == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kódpont != 220 && kódpont != 221) fogad_hiba = 1; kódpont = kódpont == 220 ? 192 : 219; 수신탈출 = 0; }
            if (fogad_felhasználás < sizeof(fogad_adatpuffer)) fogad_adatpuffer[fogad_felhasználás++] = kódpont; else fogad_hiba = 1;
        }
    }
    netif_poll(&ismerős_mobil); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned költségkeret = 0; költségkeret < 4096 && 송신개수 && (gép_jegyzék(보조장치 + 0x54) & 0x20); költségkeret++) {
        gép_jegyzék(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    ciklikus_lekérdezés = 0;
}

/* Beállítások·조회는 lwIP의 tényleges_adat 인터페이스와 megszüntet_pont 표를 사용한다. */
uint32_t 망상태읽기(unsigned bejegyzés_ÉRTÉK, unsigned INDEX) {
    if(bejegyzés_ÉRTÉK==20)return használ_vezetékes_hálózat;
    if(bejegyzés_ÉRTÉK==21)return 준비됨&&netif_is_link_up(&ismerős_mobil);
    if(bejegyzés_ÉRTÉK==22)return használ_vezetékes_hálózat?vezetékes_hálózat_statisztika(5):0;
    if (!준비됨) return 0;
    if(használ_vezetékes_hálózat&&bejegyzés_ÉRTÉK>=4&&bejegyzés_ÉRTÉK<=8)return vezetékes_hálózat_statisztika(bejegyzés_ÉRTÉK-4);
    if (bejegyzés_ÉRTÉK == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ismerős_mobil)));
    if (bejegyzés_ÉRTÉK == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&ismerős_mobil)));
    if (bejegyzés_ÉRTÉK == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&ismerős_mobil)));
    if (bejegyzés_ÉRTÉK == 3) return netif_is_up(&ismerős_mobil) != 0;
    if (bejegyzés_ÉRTÉK == 4) return KAPOTT_datagram_DARAB;
    if (bejegyzés_ÉRTÉK == 5) return 보낸전문수;
    if (bejegyzés_ÉRTÉK == 6) return KAPOTT_bájt_DARAB;
    if (bejegyzés_ÉRTÉK == 7) return 보낸바이트수;
    if (bejegyzés_ÉRTÉK == 8) return 버린전문수;
    if (bejegyzés_ÉRTÉK == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    szoftvercsatorna_végpont_3db661a2 *megszüntet_pont = &통신끝점들[INDEX];
    if (bejegyzés_ÉRTÉK == 10) return megszüntet_pont->beír_terület;
    if (!megszüntet_pont->beír_terület) return 0;
    if (bejegyzés_ÉRTÉK == 11) return hálózat_portszám(INDEX);
    if (bejegyzés_ÉRTÉK == 12) return megszüntet_pont->társ_CÍM;
    if (bejegyzés_ÉRTÉK == 13) return megszüntet_pont->társ_végpont_szám;
    if (bejegyzés_ÉRTÉK == 14) return megszüntet_pont->fogad_port ? 1 : megszüntet_pont->Fájl_megszüntet ? 3 : megszüntet_pont->HIBA ? 4 : megszüntet_pont->연결됨 ? 2 : 0;
    if (bejegyzés_ÉRTÉK == 15) return megszüntet_pont->bejegyzés_DARAB;
    if (bejegyzés_ÉRTÉK == 16) {
        const ip_addr_t *CÍM = megszüntet_pont->beír_terület == 1 && megszüntet_pont->ismerős_vezérlő ? &megszüntet_pont->ismerős_vezérlő->local_ip :
            megszüntet_pont->beír_terület == 2 && megszüntet_pont->datagram_vezérlő ? &megszüntet_pont->datagram_vezérlő->local_ip : 0;
        return CÍM ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(CÍM))) : 0;
    }
    return 0;
}

int 망설정하기(unsigned Művelet, uint32_t CÍM, uint32_t maszk_ÉRTÉK, uint32_t átjáró_ÉRTÉK) {
    if (!준비됨) return -100;
    if (Művelet == 1) { netif_set_up(&ismerős_mobil); return 0; }
    if (Művelet == 2) { netif_set_down(&ismerős_mobil); return 0; }
    if (Művelet != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maszk_ÉRTÉK, 같은 망의 선택적 alapértelmezett_érték átjáró_ÉRTÉK. */
    uint32_t 뒤집은가림 = ~maszk_ÉRTÉK;
    if (!maszk_ÉRTÉK || (뒤집은가림 & (뒤집은가림 + 1)) || !CÍM || (CÍM >> 24) == 127 ||
        (CÍM >> 24) == 0 || (CÍM >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(CÍM & 뒤집은가림) || (CÍM & 뒤집은가림) == 뒤집은가림)) ||
        (átjáró_ÉRTÉK && ((átjáró_ÉRTÉK & maszk_ÉRTÉK) != (CÍM & maszk_ÉRTÉK) || átjáró_ÉRTÉK == CÍM || (átjáró_ÉRTÉK >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(átjáró_ÉRTÉK & 뒤집은가림) || (átjáró_ÉRTÉK & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 CÍM 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].beír_terület &&
        !(통신끝점들[INDEX].fogad_port && 통신끝점들[INDEX].ismerős_vezérlő && ip_addr_isany(&통신끝점들[INDEX].ismerős_vezérlő->local_ip))) return -16;
    if(használ_vezetékes_hálózat)dhcp_stop(&ismerős_mobil);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(CÍM)); ip4_addr_set_u32(&새가림, lwip_htonl(maszk_ÉRTÉK)); ip4_addr_set_u32(&새관문, lwip_htonl(átjáró_ÉRTÉK));
    netif_set_addr(&ismerős_mobil, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *válasz_végpont;
static uint32_t teszt_CÍM, teszt_IDŐ, válaszidő;
static unsigned teszt_szekvencia, teszt_azonosító, válasz_szekvencia;
static int válasz_Állapot;
static u8_t 응답받음(void *Argumentumok, struct raw_pcb *megszüntet_pont, struct pbuf *adat, const ip_addr_t *CÍM) {
    (void)Argumentumok; (void)megszüntet_pont;
    unsigned char 머리[20], válasz[16];
    if (válasz_Állapot != -11 || adat->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(CÍM))) != teszt_CÍM || pbuf_copy_partial(adat, 머리, 20, 0) != 20) return 0;
    unsigned fejléc_méretez = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || fejléc_méretez < 20 || adat->tot_len < fejléc_méretez + 16 ||
        pbuf_copy_partial(adat, válasz, 16, fejléc_méretez) != 16 || válasz[0] || válasz[1] ||
        (((unsigned)válasz[4] << 8) | válasz[5]) != teszt_azonosító ||
        (((unsigned)válasz[6] << 8) | válasz[7]) != teszt_szekvencia ||
        válasz[8] != 'J' || válasz[9] != 'K' || válasz[10] != 'O' || válasz[11] != 'S' ||
        (((uint32_t)válasz[12] << 24) | ((uint32_t)válasz[13] << 16) | ((uint32_t)válasz[14] << 8) | válasz[15]) != teszt_IDŐ) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(adat, fejléc_méretez)) return 0;
    if (inet_chksum_pbuf(adat)) { pbuf_add_header(adat, fejléc_méretez); return 0; }
    válaszidő = (uint32_t)보드밀리초() - teszt_IDŐ; válasz_szekvencia = 머리[8]; válasz_Állapot = 0;
    pbuf_free(adat); return 1;
}
int START_válasz_teszt(uint32_t CÍM, unsigned rendel_ÉRTÉK) {
    if (!준비됨 || !netif_is_up(&ismerős_mobil)) return -100;
    if (!CÍM || (CÍM >> 28) >= 14 || CÍM == 0xffffffffu) return -22;
    if (!válasz_végpont) { válasz_végpont = raw_new(IP_PROTO_ICMP); if (!válasz_végpont) return -12; raw_recv(válasz_végpont, 응답받음, 0); }
    teszt_CÍM = CÍM; teszt_szekvencia = rendel_ÉRTÉK & 65535; teszt_azonosító = (teszt_azonosító + 1) & 65535;
    teszt_IDŐ = 보드밀리초(); válasz_Állapot = -11; válaszidő = válasz_szekvencia = 0;
    unsigned char adat[32] = {8,0,0,0};
    adat[4] = teszt_azonosító >> 8; adat[5] = teszt_azonosító; adat[6] = teszt_szekvencia >> 8; adat[7] = teszt_szekvencia;
    adat[8]='J'; adat[9]='K'; adat[10]='O'; adat[11]='S';
    adat[12]=teszt_IDŐ >> 24; adat[13]=teszt_IDŐ >> 16; adat[14]=teszt_IDŐ >> 8; adat[15]=teszt_IDŐ;
    for (unsigned helyzetindex = 16; helyzetindex < sizeof(adat); helyzetindex++) adat[helyzetindex] = helyzetindex;
    uint16_t ellenőrzés_ellenőrzőösszeg = inet_chksum(adat, sizeof(adat)); memcpy(adat + 2, &ellenőrzés_ellenőrzőösszeg, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(adat), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, adat, sizeof(adat)); ip_addr_t cél_végpont; ip_addr_set_ip4_u32(&cél_végpont, lwip_htonl(CÍM));
    err_t 처리값 = raw_sendto(válasz_végpont, datagram, &cél_végpont); pbuf_free(datagram);
    if (처리값) válasz_Állapot = hibaszám(처리값);
    return 처리값 ? válasz_Állapot : 0;
}
int 응답시험읽기(unsigned bejegyzés_ÉRTÉK) {
    통신망살피기();
    return bejegyzés_ÉRTÉK == 0 ? válasz_Állapot : bejegyzés_ÉRTÉK == 1 ? (int)válaszidő : bejegyzés_ÉRTÉK == 2 ? (int)válasz_szekvencia : -22;
}
