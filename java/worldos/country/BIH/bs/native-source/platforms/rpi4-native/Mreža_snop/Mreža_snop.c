#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Mreža_snop.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../udaljeno_VALUE/udaljeno_VALUE.h"
#include "ožičen_Mreža.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define mašina_registrirati(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif veza_uređaj;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char prenositi_podaci[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_bajt_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_oblast, 수신창구, odjel_za_informacijske_tehnologije_na_čekanju, 연결됨, fajl_završiti, GRESKA;
    struct tcp_pcb *veza_kontrola;
    struct udp_pcb *전문제어;
    unsigned 맨앞, unos_COUNT;
    unsigned char podaci[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], peer_adresa;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int broj_greške(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int fajl_hvatište) { return fajl_hvatište >= 0 && fajl_hvatište < 32 && 통신끝점들[fajl_hvatište].TYPE_oblast ? &통신끝점들[fajl_hvatište] : 0; }
static int 예약하기(int TYPE_oblast) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_oblast) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_oblast = TYPE_oblast; 통신끝점들[순번].odjel_za_informacijske_tehnologije_na_čekanju = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kôd_znaka) { prenositi_podaci[(송신앞자리 + 송신개수++) % sizeof(prenositi_podaci)] = kôd_znaka; }
static err_t 출력결과(struct netif *stavka_COUNT, struct pbuf *podaci_položaj, const ip4_addr_t *adresa) {
    (void)stavka_COUNT; (void)adresa;
    if (podaci_položaj->tot_len > 1500 || 송신개수 + 2 * podaci_položaj->tot_len + 2 > sizeof(prenositi_podaci)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Dalje_Pomak = podaci_položaj; Dalje_Pomak; Dalje_Pomak = Dalje_Pomak->next) for (unsigned 순번 = 0; 순번 < Dalje_Pomak->len; 순번++) {
        unsigned kôd_znaka = ((unsigned char *)Dalje_Pomak->payload)[순번];
        if (kôd_znaka == 192 || kôd_znaka == 219) { 내보내기(219); 내보내기(kôd_znaka == 192 ? 220 : 221); } else 내보내기(kôd_znaka);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += podaci_položaj->tot_len; return ERR_OK;
}
static err_t Pripremiti_zajednička_jezička_biblioteka(struct netif *stavka_COUNT) { stavka_COUNT->name[0] = 's'; stavka_COUNT->name[1] = 'l'; stavka_COUNT->mtu = 1500; stavka_COUNT->output = 출력결과; return ERR_OK; }
void Pripremiti_Mreža(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    mašina_registrirati(보조장치 + 4) |= 1; mašina_registrirati(보조장치 + 0x60) = 0; mašina_registrirati(보조장치 + 0x44) = 0;
    mašina_registrirati(보조장치 + 0x48) = 0xc6; mašina_registrirati(보조장치 + 0x4c) = 3; mašina_registrirati(보조장치 + 0x68) = 270; mašina_registrirati(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetska_adresa, bit_maska, pristupni_uređaj_adresa;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&internetska_adresa, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_maska, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&pristupni_uređaj_adresa, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&veza_uređaj, &internetska_adresa, &bit_maska, &pristupni_uređaj_adresa, 0, 유선사용?Pripremiti_ožičen_Mreža:Pripremiti_zajednička_jezička_biblioteka, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&veza_uređaj); netif_set_up(&veza_uređaj);if(!유선사용)netif_set_link_up(&veza_uređaj); 준비됨 = 1;
    Pripremiti_udaljeno();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *prijenos_kontrola_blokirati, struct pbuf *podaci_položaj, err_t GRESKA) {
    통신끝점 *string_podaci = 부가인수; (void)prijenos_kontrola_blokirati; (void)GRESKA;
    if (!podaci_položaj) { string_podaci->fajl_završiti = 1; return ERR_OK; }
    if (podaci_položaj->tot_len > sizeof(string_podaci->podaci) - string_podaci->unos_COUNT) return ERR_MEM;
    unsigned trenutno_položaj = (string_podaci->맨앞 + string_podaci->unos_COUNT) % sizeof(string_podaci->podaci);
    for (struct pbuf *Dalje_Pomak = podaci_položaj; Dalje_Pomak; Dalje_Pomak = Dalje_Pomak->next) for (unsigned 순번 = 0; 순번 < Dalje_Pomak->len; 순번++) {
        string_podaci->podaci[trenutno_položaj] = ((unsigned char *)Dalje_Pomak->payload)[순번]; trenutno_položaj = (trenutno_položaj + 1) % sizeof(string_podaci->podaci);
    }
    string_podaci->unos_COUNT += podaci_položaj->tot_len; pbuf_free(podaci_položaj); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t GRESKA) { 통신끝점 *string_podaci = 부가인수; string_podaci->veza_kontrola = 0; string_podaci->GRESKA = broj_greške(GRESKA); }
static void 되부름목록(통신끝점 *string_podaci) { tcp_arg(string_podaci->veza_kontrola, string_podaci); tcp_recv(string_podaci->veza_kontrola, 수신됨); tcp_err(string_podaci->veza_kontrola, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *prijenos_kontrola_blokirati, err_t GRESKA) {
    통신끝점 *string_podaci = 부가인수; (void)prijenos_kontrola_blokirati; if (GRESKA) string_podaci->GRESKA = broj_greške(GRESKA); else string_podaci->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *prijenos_kontrola_blokirati, err_t GRESKA) {
    통신끝점 *roditelj = 부가인수; if (GRESKA) return GRESKA;
    int fajl_hvatište = 예약하기(1); if (fajl_hvatište < 0) return ERR_MEM;
    통신끝점 *string_podaci = &통신끝점들[fajl_hvatište]; string_podaci->veza_kontrola = prijenos_kontrola_blokirati; string_podaci->연결됨 = 1; string_podaci->odjel_za_informacijske_tehnologije_na_čekanju = (int)(roditelj - 통신끝점들);
    string_podaci->peer_adresa = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&prijenos_kontrola_blokirati->remote_ip))); string_podaci->상대창구번호 = prijenos_kontrola_blokirati->remote_port;
    되부름목록(string_podaci); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *prijenos_kontrola_blokirati, struct pbuf *podaci_položaj, const ip_addr_t *adresa, u16_t broj_priključka) {
    통신끝점 *string_podaci = 부가인수; (void)prijenos_kontrola_blokirati;
    if (string_podaci->unos_COUNT < 4 && podaci_položaj->tot_len <= 512) {
        unsigned položaj_INDEX = (string_podaci->맨앞 + string_podaci->unos_COUNT) % 4;
        pbuf_copy_partial(podaci_položaj, string_podaci->podaci + položaj_INDEX * 512, podaci_položaj->tot_len, 0);
        string_podaci->길이목록[položaj_INDEX] = podaci_položaj->tot_len; string_podaci->접속번호들[položaj_INDEX] = broj_priključka;
        string_podaci->주소목록[položaj_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))); string_podaci->unos_COUNT++;
    }
    pbuf_free(podaci_položaj);
}
int 통신끝점만들기(int TYPE_oblast) {
    if (!준비됨) return -100;
    if (TYPE_oblast != 1 && TYPE_oblast != 2) return -93;
    int fajl_hvatište = 예약하기(TYPE_oblast); if (fajl_hvatište < 0) return fajl_hvatište;
    통신끝점 *string_podaci = &통신끝점들[fajl_hvatište];
    if (TYPE_oblast == 1) { string_podaci->veza_kontrola = tcp_new(); if (string_podaci->veza_kontrola) 되부름목록(string_podaci); }
    else { string_podaci->전문제어 = udp_new(); if (string_podaci->전문제어) udp_recv(string_podaci->전문제어, 전문, string_podaci); }
    if (!string_podaci->veza_kontrola && !string_podaci->전문제어) { string_podaci->TYPE_oblast = 0; return -12; } return fajl_hvatište;
}
int 망주소묶기(int fajl_hvatište, uint32_t adresa, unsigned broj_priključka) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci) return -9;
    if (broj_priključka > 65535 || (adresa && adresa != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&veza_uređaj))) && adresa != 0x7f000001)) return -99;
    ip_addr_t internetska_adresa; ip_addr_set_ip4_u32(&internetska_adresa, lwip_htonl(adresa));
    err_t 보조항목 = string_podaci->TYPE_oblast == 1 ? tcp_bind(string_podaci->veza_kontrola, &internetska_adresa, broj_priključka) : udp_bind(string_podaci->전문제어, &internetska_adresa, broj_priključka); return 보조항목 ? broj_greške(보조항목) : 0;
}
void 통신주소재사용(int fajl_hvatište) { 통신끝점 *string_podaci = 얻기(fajl_hvatište); if (string_podaci && string_podaci->veza_kontrola) ip_set_option(string_podaci->veza_kontrola, SOF_REUSEADDR); }
int 연결기다리기(int fajl_hvatište) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci || string_podaci->TYPE_oblast != 1) return -9;
    if (string_podaci->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *prijenos_kontrola_blokirati = tcp_listen_with_backlog_and_err(string_podaci->veza_kontrola, 4, &보조항목);
    if (!prijenos_kontrola_blokirati) return broj_greške(보조항목); string_podaci->veza_kontrola = prijenos_kontrola_blokirati; string_podaci->수신창구 = 1; tcp_arg(prijenos_kontrola_blokirati, string_podaci); tcp_accept(prijenos_kontrola_blokirati, 연결받음); return 0;
}
int 망연결하기(int fajl_hvatište, uint32_t adresa, unsigned broj_priključka) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci || string_podaci->TYPE_oblast != 1) return -9;
    if (string_podaci->GRESKA) return string_podaci->GRESKA;
    if (string_podaci->연결됨) return 0;
    if (string_podaci->상대창구번호) return -115;
    if (!broj_priključka || broj_priključka > 65535 || !adresa) return -22;
    ip_addr_t internetska_adresa; ip_addr_set_ip4_u32(&internetska_adresa, lwip_htonl(adresa));
    string_podaci->peer_adresa = adresa; string_podaci->상대창구번호 = broj_priključka;
    err_t 보조항목 = tcp_connect(string_podaci->veza_kontrola, &internetska_adresa, broj_priključka, 연결됨); return 보조항목 ? broj_greške(보조항목) : -115;
}
int 망연결받기(int fajl_hvatište) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci || !string_podaci->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_oblast == 1 && 통신끝점들[순번].odjel_za_informacijske_tehnologije_na_čekanju == fajl_hvatište) { 통신끝점들[순번].odjel_za_informacijske_tehnologije_na_čekanju = -1; return 순번; }
    return -11;
}
int 통신읽기(int fajl_hvatište, void *podaci, unsigned stavka_COUNT) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci || string_podaci->TYPE_oblast != 1) return -9;
    if (!stavka_COUNT) return 0; if (!string_podaci->unos_COUNT) return string_podaci->GRESKA ? string_podaci->GRESKA : string_podaci->fajl_završiti ? 0 : -11;
    if (stavka_COUNT > string_podaci->unos_COUNT) stavka_COUNT = string_podaci->unos_COUNT;
    for (unsigned 순번 = 0; 순번 < stavka_COUNT; 순번++) { ((unsigned char *)podaci)[순번] = string_podaci->podaci[string_podaci->맨앞]; string_podaci->맨앞 = (string_podaci->맨앞 + 1) % sizeof(string_podaci->podaci); }
    string_podaci->unos_COUNT -= stavka_COUNT; if (string_podaci->veza_kontrola) tcp_recved(string_podaci->veza_kontrola, stavka_COUNT); return stavka_COUNT;
}
int 통신쓰기(int fajl_hvatište, const void *podaci, unsigned stavka_COUNT) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci || string_podaci->TYPE_oblast != 1) return -9;
    if (string_podaci->GRESKA) return string_podaci->GRESKA; if (!string_podaci->veza_kontrola || !string_podaci->연결됨) return -107;
    if (!stavka_COUNT) return 0; if (stavka_COUNT > tcp_sndbuf(string_podaci->veza_kontrola)) stavka_COUNT = tcp_sndbuf(string_podaci->veza_kontrola);
    if (!stavka_COUNT) return -11; if (stavka_COUNT > 1024) stavka_COUNT = 1024;
    err_t 보조항목 = tcp_write(string_podaci->veza_kontrola, podaci, stavka_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return broj_greške(보조항목);
    tcp_output(string_podaci->veza_kontrola); return stavka_COUNT;
}
int 전문보내기(int fajl_hvatište, const void *podaci, unsigned stavka_COUNT, uint32_t adresa, unsigned broj_priključka) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci || string_podaci->TYPE_oblast != 2) return -9;
    if (stavka_COUNT > 512) return -90; if (!broj_priključka || broj_priključka > 65535) return -22;
    struct pbuf *podaci_položaj = pbuf_alloc(PBUF_TRANSPORT, stavka_COUNT, PBUF_RAM); if (!podaci_položaj) return -11;
    pbuf_take(podaci_položaj, podaci, stavka_COUNT); ip_addr_t internetska_adresa; ip_addr_set_ip4_u32(&internetska_adresa, lwip_htonl(adresa));
    err_t 보조항목 = udp_sendto(string_podaci->전문제어, podaci_položaj, &internetska_adresa, broj_priključka); pbuf_free(podaci_položaj); return 보조항목 ? broj_greške(보조항목) : (int)stavka_COUNT;
}
int 전문받기(int fajl_hvatište, void *podaci, unsigned stavka_COUNT) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci || string_podaci->TYPE_oblast != 2) return -9;
    if (!string_podaci->unos_COUNT) return -11; unsigned trenutno_položaj = string_podaci->맨앞;
    if (stavka_COUNT > string_podaci->길이목록[trenutno_položaj]) stavka_COUNT = string_podaci->길이목록[trenutno_položaj]; memcpy(podaci, string_podaci->podaci + trenutno_položaj * 512, stavka_COUNT);
    string_podaci->상대창구번호 = string_podaci->접속번호들[trenutno_položaj]; string_podaci->peer_adresa = string_podaci->주소목록[trenutno_položaj]; string_podaci->맨앞 = (trenutno_položaj + 1) % 4; string_podaci->unos_COUNT--; return stavka_COUNT;
}
unsigned Mreža_broj_priključka(int fajl_hvatište) { 통신끝점 *string_podaci = 얻기(fajl_hvatište); return !string_podaci ? 0 : string_podaci->veza_kontrola ? string_podaci->veza_kontrola->local_port : string_podaci->전문제어 ? string_podaci->전문제어->local_port : 0; }
unsigned peer_broj_priključka(int fajl_hvatište) { 통신끝점 *string_podaci = 얻기(fajl_hvatište); return string_podaci ? string_podaci->상대창구번호 : 0; }
uint32_t 상대통신주소(int fajl_hvatište) { 통신끝점 *string_podaci = 얻기(fajl_hvatište); return string_podaci ? string_podaci->peer_adresa : 0; }
void zatvoriti_Mreža(int fajl_hvatište) {
    통신끝점 *string_podaci = 얻기(fajl_hvatište); if (!string_podaci) return;
    if (string_podaci->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_oblast && 통신끝점들[순번].odjel_za_informacijske_tehnologije_na_čekanju == fajl_hvatište) zatvoriti_Mreža(순번);
    if (string_podaci->veza_kontrola) {
        tcp_arg(string_podaci->veza_kontrola, 0); if (string_podaci->수신창구) tcp_accept(string_podaci->veza_kontrola, 0); else { tcp_recv(string_podaci->veza_kontrola, 0); tcp_err(string_podaci->veza_kontrola, 0); }
        if (tcp_close(string_podaci->veza_kontrola) != ERR_OK) tcp_abort(string_podaci->veza_kontrola);
    }
    if (string_podaci->전문제어) udp_remove(string_podaci->전문제어); string_podaci->TYPE_oblast = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&veza_uređaj);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (mašina_registrirati(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned kôd_znaka = mašina_registrirati(보조장치 + 0x40) & 255;
        if (kôd_znaka == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *podaci_položaj = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (podaci_položaj) { 받은전문수++; RECEIVED_bajt_COUNT += 수신사용량; pbuf_take(podaci_položaj, 수신자료, 수신사용량); if (veza_uređaj.input(podaci_položaj, &veza_uređaj) != ERR_OK) { 버린전문수++; pbuf_free(podaci_položaj); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (kôd_znaka == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kôd_znaka != 220 && kôd_znaka != 221) 수신오류 = 1; kôd_znaka = kôd_znaka == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = kôd_znaka; else 수신오류 = 1;
        }
    }
    netif_poll(&veza_uređaj); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (mašina_registrirati(보조장치 + 0x54) & 0x20); 처리한도++) {
        mašina_registrirati(보조장치 + 0x40) = prenositi_podaci[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(prenositi_podaci); 송신개수--;
    }
    살피는중 = 0;
}

/* Postavke·조회는 lwIP의 stvaran_podaci 인터페이스와 završiti_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned unos_VALUE, unsigned INDEX) {
    if(unos_VALUE==20)return 유선사용;
    if(unos_VALUE==21)return 준비됨&&netif_is_link_up(&veza_uređaj);
    if(unos_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&unos_VALUE>=4&&unos_VALUE<=8)return 유선망집계(unos_VALUE-4);
    if (unos_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&veza_uređaj)));
    if (unos_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&veza_uređaj)));
    if (unos_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&veza_uređaj)));
    if (unos_VALUE == 3) return netif_is_up(&veza_uređaj) != 0;
    if (unos_VALUE == 4) return 받은전문수;
    if (unos_VALUE == 5) return 보낸전문수;
    if (unos_VALUE == 6) return RECEIVED_bajt_COUNT;
    if (unos_VALUE == 7) return 보낸바이트수;
    if (unos_VALUE == 8) return 버린전문수;
    if (unos_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *završiti_p = &통신끝점들[INDEX];
    if (unos_VALUE == 10) return završiti_p->TYPE_oblast;
    if (!završiti_p->TYPE_oblast) return 0;
    if (unos_VALUE == 11) return Mreža_broj_priključka(INDEX);
    if (unos_VALUE == 12) return završiti_p->peer_adresa;
    if (unos_VALUE == 13) return završiti_p->상대창구번호;
    if (unos_VALUE == 14) return završiti_p->수신창구 ? 1 : završiti_p->fajl_završiti ? 3 : završiti_p->GRESKA ? 4 : završiti_p->연결됨 ? 2 : 0;
    if (unos_VALUE == 15) return završiti_p->unos_COUNT;
    if (unos_VALUE == 16) {
        const ip_addr_t *adresa = završiti_p->TYPE_oblast == 1 && završiti_p->veza_kontrola ? &završiti_p->veza_kontrola->local_ip :
            završiti_p->TYPE_oblast == 2 && završiti_p->전문제어 ? &završiti_p->전문제어->local_ip : 0;
        return adresa ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) : 0;
    }
    return 0;
}

int konfigurirati_Mreža(unsigned radnja, uint32_t adresa, uint32_t maska_VALUE, uint32_t pristupni_uređaj_VALUE) {
    if (!준비됨) return -100;
    if (radnja == 1) { netif_set_up(&veza_uređaj); return 0; }
    if (radnja == 2) { netif_set_down(&veza_uređaj); return 0; }
    if (radnja != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_VALUE, 같은 망의 선택적 zadana_vrijednost pristupni_uređaj_VALUE. */
    uint32_t 뒤집은가림 = ~maska_VALUE;
    if (!maska_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !adresa || (adresa >> 24) == 127 ||
        (adresa >> 24) == 0 || (adresa >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(adresa & 뒤집은가림) || (adresa & 뒤집은가림) == 뒤집은가림)) ||
        (pristupni_uređaj_VALUE && ((pristupni_uređaj_VALUE & maska_VALUE) != (adresa & maska_VALUE) || pristupni_uređaj_VALUE == adresa || (pristupni_uređaj_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(pristupni_uređaj_VALUE & 뒤집은가림) || (pristupni_uređaj_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 adresa 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_oblast &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].veza_kontrola && ip_addr_isany(&통신끝점들[INDEX].veza_kontrola->local_ip))) return -16;
    if(유선사용)dhcp_stop(&veza_uređaj);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(adresa)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(pristupni_uređaj_VALUE));
    netif_set_addr(&veza_uređaj, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *Argumenti, struct raw_pcb *završiti_p, struct pbuf *podaci, const ip_addr_t *adresa) {
    (void)Argumenti; (void)završiti_p;
    unsigned char 머리[20], odgovoriti[16];
    if (응답상태 != -11 || podaci->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adresa))) != 시험주소 || pbuf_copy_partial(podaci, 머리, 20, 0) != 20) return 0;
    unsigned Zaglavlje_podesiti_veličinu = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Zaglavlje_podesiti_veličinu < 20 || podaci->tot_len < Zaglavlje_podesiti_veličinu + 16 ||
        pbuf_copy_partial(podaci, odgovoriti, 16, Zaglavlje_podesiti_veličinu) != 16 || odgovoriti[0] || odgovoriti[1] ||
        (((unsigned)odgovoriti[4] << 8) | odgovoriti[5]) != 시험식별자 ||
        (((unsigned)odgovoriti[6] << 8) | odgovoriti[7]) != 시험순서 ||
        odgovoriti[8] != 'J' || odgovoriti[9] != 'K' || odgovoriti[10] != 'O' || odgovoriti[11] != 'S' ||
        (((uint32_t)odgovoriti[12] << 24) | ((uint32_t)odgovoriti[13] << 16) | ((uint32_t)odgovoriti[14] << 8) | odgovoriti[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(podaci, Zaglavlje_podesiti_veličinu)) return 0;
    if (inet_chksum_pbuf(podaci)) { pbuf_add_header(podaci, Zaglavlje_podesiti_veličinu); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(podaci); return 1;
}
int 응답시험시작(uint32_t adresa, unsigned redoslijed_VALUE) {
    if (!준비됨 || !netif_is_up(&veza_uređaj)) return -100;
    if (!adresa || (adresa >> 28) >= 14 || adresa == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = adresa; 시험순서 = redoslijed_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char podaci[32] = {8,0,0,0};
    podaci[4] = 시험식별자 >> 8; podaci[5] = 시험식별자; podaci[6] = 시험순서 >> 8; podaci[7] = 시험순서;
    podaci[8]='J'; podaci[9]='K'; podaci[10]='O'; podaci[11]='S';
    podaci[12]=시험시각 >> 24; podaci[13]=시험시각 >> 16; podaci[14]=시험시각 >> 8; podaci[15]=시험시각;
    for (unsigned položaj_INDEX = 16; položaj_INDEX < sizeof(podaci); položaj_INDEX++) podaci[položaj_INDEX] = položaj_INDEX;
    uint16_t provjera_programa_kontrolni_zbir = inet_chksum(podaci, sizeof(podaci)); memcpy(podaci + 2, &provjera_programa_kontrolni_zbir, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(podaci), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, podaci, sizeof(podaci)); ip_addr_t odredište_završna_tačka; ip_addr_set_ip4_u32(&odredište_završna_tačka, lwip_htonl(adresa));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &odredište_završna_tačka); pbuf_free(전문);
    if (처리값) 응답상태 = broj_greške(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned unos_VALUE) {
    통신망살피기();
    return unos_VALUE == 0 ? 응답상태 : unos_VALUE == 1 ? (int)응답시간 : unos_VALUE == 2 ? (int)응답차례 : -22;
}
