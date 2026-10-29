#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Nettverk_Stabel.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../fjern_VALUE/fjern_VALUE.h"
#include "kabelbasert_Nettverk.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define maskin_registrere(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif kontakt_mobil;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_byte_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_kategori, 수신창구, informasjonsteknologi_ventande, 연결됨, fil_avslutte, FEIL;
    struct tcp_pcb *kontakt_styring;
    struct udp_pcb *전문제어;
    unsigned 맨앞, oppføring_COUNT;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], node_ADDRESS;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int feilnummer(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int fil_handtak) { return fil_handtak >= 0 && fil_handtak < 32 && 통신끝점들[fil_handtak].TYPE_kategori ? &통신끝점들[fil_handtak] : 0; }
static int 예약하기(int TYPE_kategori) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_kategori) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_kategori = TYPE_kategori; 통신끝점들[순번].informasjonsteknologi_ventande = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned teiknkode) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = teiknkode; }
static err_t 출력결과(struct netif *vare_COUNT, struct pbuf *data_plassere, const ip4_addr_t *ADDRESS) {
    (void)vare_COUNT; (void)ADDRESS;
    if (data_plassere->tot_len > 1500 || 송신개수 + 2 * data_plassere->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Neste_OFFSET = data_plassere; Neste_OFFSET; Neste_OFFSET = Neste_OFFSET->next) for (unsigned 순번 = 0; 순번 < Neste_OFFSET->len; 순번++) {
        unsigned teiknkode = ((unsigned char *)Neste_OFFSET->payload)[순번];
        if (teiknkode == 192 || teiknkode == 219) { 내보내기(219); 내보내기(teiknkode == 192 ? 220 : 221); } else 내보내기(teiknkode);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_plassere->tot_len; return ERR_OK;
}
static err_t Klargjer_Common_Language_Runtime(struct netif *vare_COUNT) { vare_COUNT->name[0] = 's'; vare_COUNT->name[1] = 'l'; vare_COUNT->mtu = 1500; vare_COUNT->output = 출력결과; return ERR_OK; }
void Klargjer_Nettverk(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    maskin_registrere(보조장치 + 4) |= 1; maskin_registrere(보조장치 + 0x60) = 0; maskin_registrere(보조장치 + 0x44) = 0;
    maskin_registrere(보조장치 + 0x48) = 0xc6; maskin_registrere(보조장치 + 0x4c) = 3; maskin_registrere(보조장치 + 0x68) = 270; maskin_registrere(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internett_adresse, bit_maske, gateway_ADDRESS;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Internett_adresse, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_maske, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gateway_ADDRESS, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&kontakt_mobil, &Internett_adresse, &bit_maske, &gateway_ADDRESS, 0, 유선사용?Klargjer_kabelbasert_Nettverk:Klargjer_Common_Language_Runtime, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&kontakt_mobil); netif_set_up(&kontakt_mobil);if(!유선사용)netif_set_link_up(&kontakt_mobil); 준비됨 = 1;
    Klargjer_fjern();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *overføring_styring_Blokker, struct pbuf *data_plassere, err_t FEIL) {
    통신끝점 *streng_data = 부가인수; (void)overføring_styring_Blokker; (void)FEIL;
    if (!data_plassere) { streng_data->fil_avslutte = 1; return ERR_OK; }
    if (data_plassere->tot_len > sizeof(streng_data->data) - streng_data->oppføring_COUNT) return ERR_MEM;
    unsigned betalt_plassere = (streng_data->맨앞 + streng_data->oppføring_COUNT) % sizeof(streng_data->data);
    for (struct pbuf *Neste_OFFSET = data_plassere; Neste_OFFSET; Neste_OFFSET = Neste_OFFSET->next) for (unsigned 순번 = 0; 순번 < Neste_OFFSET->len; 순번++) {
        streng_data->data[betalt_plassere] = ((unsigned char *)Neste_OFFSET->payload)[순번]; betalt_plassere = (betalt_plassere + 1) % sizeof(streng_data->data);
    }
    streng_data->oppføring_COUNT += data_plassere->tot_len; pbuf_free(data_plassere); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t FEIL) { 통신끝점 *streng_data = 부가인수; streng_data->kontakt_styring = 0; streng_data->FEIL = feilnummer(FEIL); }
static void 되부름목록(통신끝점 *streng_data) { tcp_arg(streng_data->kontakt_styring, streng_data); tcp_recv(streng_data->kontakt_styring, 수신됨); tcp_err(streng_data->kontakt_styring, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *overføring_styring_Blokker, err_t FEIL) {
    통신끝점 *streng_data = 부가인수; (void)overføring_styring_Blokker; if (FEIL) streng_data->FEIL = feilnummer(FEIL); else streng_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *overføring_styring_Blokker, err_t FEIL) {
    통신끝점 *forelder = 부가인수; if (FEIL) return FEIL;
    int fil_handtak = 예약하기(1); if (fil_handtak < 0) return ERR_MEM;
    통신끝점 *streng_data = &통신끝점들[fil_handtak]; streng_data->kontakt_styring = overføring_styring_Blokker; streng_data->연결됨 = 1; streng_data->informasjonsteknologi_ventande = (int)(forelder - 통신끝점들);
    streng_data->node_ADDRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&overføring_styring_Blokker->remote_ip))); streng_data->상대창구번호 = overføring_styring_Blokker->remote_port;
    되부름목록(streng_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *overføring_styring_Blokker, struct pbuf *data_plassere, const ip_addr_t *ADDRESS, u16_t portnummer) {
    통신끝점 *streng_data = 부가인수; (void)overføring_styring_Blokker;
    if (streng_data->oppføring_COUNT < 4 && data_plassere->tot_len <= 512) {
        unsigned plassere_INDEX = (streng_data->맨앞 + streng_data->oppføring_COUNT) % 4;
        pbuf_copy_partial(data_plassere, streng_data->data + plassere_INDEX * 512, data_plassere->tot_len, 0);
        streng_data->길이목록[plassere_INDEX] = data_plassere->tot_len; streng_data->접속번호들[plassere_INDEX] = portnummer;
        streng_data->주소목록[plassere_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))); streng_data->oppføring_COUNT++;
    }
    pbuf_free(data_plassere);
}
int 통신끝점만들기(int TYPE_kategori) {
    if (!준비됨) return -100;
    if (TYPE_kategori != 1 && TYPE_kategori != 2) return -93;
    int fil_handtak = 예약하기(TYPE_kategori); if (fil_handtak < 0) return fil_handtak;
    통신끝점 *streng_data = &통신끝점들[fil_handtak];
    if (TYPE_kategori == 1) { streng_data->kontakt_styring = tcp_new(); if (streng_data->kontakt_styring) 되부름목록(streng_data); }
    else { streng_data->전문제어 = udp_new(); if (streng_data->전문제어) udp_recv(streng_data->전문제어, 전문, streng_data); }
    if (!streng_data->kontakt_styring && !streng_data->전문제어) { streng_data->TYPE_kategori = 0; return -12; } return fil_handtak;
}
int 망주소묶기(int fil_handtak, uint32_t ADDRESS, unsigned portnummer) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data) return -9;
    if (portnummer > 65535 || (ADDRESS && ADDRESS != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_mobil))) && ADDRESS != 0x7f000001)) return -99;
    ip_addr_t Internett_adresse; ip_addr_set_ip4_u32(&Internett_adresse, lwip_htonl(ADDRESS));
    err_t 보조항목 = streng_data->TYPE_kategori == 1 ? tcp_bind(streng_data->kontakt_styring, &Internett_adresse, portnummer) : udp_bind(streng_data->전문제어, &Internett_adresse, portnummer); return 보조항목 ? feilnummer(보조항목) : 0;
}
void 통신주소재사용(int fil_handtak) { 통신끝점 *streng_data = 얻기(fil_handtak); if (streng_data && streng_data->kontakt_styring) ip_set_option(streng_data->kontakt_styring, SOF_REUSEADDR); }
int 연결기다리기(int fil_handtak) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data || streng_data->TYPE_kategori != 1) return -9;
    if (streng_data->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *overføring_styring_Blokker = tcp_listen_with_backlog_and_err(streng_data->kontakt_styring, 4, &보조항목);
    if (!overføring_styring_Blokker) return feilnummer(보조항목); streng_data->kontakt_styring = overføring_styring_Blokker; streng_data->수신창구 = 1; tcp_arg(overføring_styring_Blokker, streng_data); tcp_accept(overføring_styring_Blokker, 연결받음); return 0;
}
int 망연결하기(int fil_handtak, uint32_t ADDRESS, unsigned portnummer) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data || streng_data->TYPE_kategori != 1) return -9;
    if (streng_data->FEIL) return streng_data->FEIL;
    if (streng_data->연결됨) return 0;
    if (streng_data->상대창구번호) return -115;
    if (!portnummer || portnummer > 65535 || !ADDRESS) return -22;
    ip_addr_t Internett_adresse; ip_addr_set_ip4_u32(&Internett_adresse, lwip_htonl(ADDRESS));
    streng_data->node_ADDRESS = ADDRESS; streng_data->상대창구번호 = portnummer;
    err_t 보조항목 = tcp_connect(streng_data->kontakt_styring, &Internett_adresse, portnummer, 연결됨); return 보조항목 ? feilnummer(보조항목) : -115;
}
int 망연결받기(int fil_handtak) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data || !streng_data->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_kategori == 1 && 통신끝점들[순번].informasjonsteknologi_ventande == fil_handtak) { 통신끝점들[순번].informasjonsteknologi_ventande = -1; return 순번; }
    return -11;
}
int 통신읽기(int fil_handtak, void *data, unsigned vare_COUNT) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data || streng_data->TYPE_kategori != 1) return -9;
    if (!vare_COUNT) return 0; if (!streng_data->oppføring_COUNT) return streng_data->FEIL ? streng_data->FEIL : streng_data->fil_avslutte ? 0 : -11;
    if (vare_COUNT > streng_data->oppføring_COUNT) vare_COUNT = streng_data->oppføring_COUNT;
    for (unsigned 순번 = 0; 순번 < vare_COUNT; 순번++) { ((unsigned char *)data)[순번] = streng_data->data[streng_data->맨앞]; streng_data->맨앞 = (streng_data->맨앞 + 1) % sizeof(streng_data->data); }
    streng_data->oppføring_COUNT -= vare_COUNT; if (streng_data->kontakt_styring) tcp_recved(streng_data->kontakt_styring, vare_COUNT); return vare_COUNT;
}
int 통신쓰기(int fil_handtak, const void *data, unsigned vare_COUNT) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data || streng_data->TYPE_kategori != 1) return -9;
    if (streng_data->FEIL) return streng_data->FEIL; if (!streng_data->kontakt_styring || !streng_data->연결됨) return -107;
    if (!vare_COUNT) return 0; if (vare_COUNT > tcp_sndbuf(streng_data->kontakt_styring)) vare_COUNT = tcp_sndbuf(streng_data->kontakt_styring);
    if (!vare_COUNT) return -11; if (vare_COUNT > 1024) vare_COUNT = 1024;
    err_t 보조항목 = tcp_write(streng_data->kontakt_styring, data, vare_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return feilnummer(보조항목);
    tcp_output(streng_data->kontakt_styring); return vare_COUNT;
}
int 전문보내기(int fil_handtak, const void *data, unsigned vare_COUNT, uint32_t ADDRESS, unsigned portnummer) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data || streng_data->TYPE_kategori != 2) return -9;
    if (vare_COUNT > 512) return -90; if (!portnummer || portnummer > 65535) return -22;
    struct pbuf *data_plassere = pbuf_alloc(PBUF_TRANSPORT, vare_COUNT, PBUF_RAM); if (!data_plassere) return -11;
    pbuf_take(data_plassere, data, vare_COUNT); ip_addr_t Internett_adresse; ip_addr_set_ip4_u32(&Internett_adresse, lwip_htonl(ADDRESS));
    err_t 보조항목 = udp_sendto(streng_data->전문제어, data_plassere, &Internett_adresse, portnummer); pbuf_free(data_plassere); return 보조항목 ? feilnummer(보조항목) : (int)vare_COUNT;
}
int 전문받기(int fil_handtak, void *data, unsigned vare_COUNT) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data || streng_data->TYPE_kategori != 2) return -9;
    if (!streng_data->oppføring_COUNT) return -11; unsigned betalt_plassere = streng_data->맨앞;
    if (vare_COUNT > streng_data->길이목록[betalt_plassere]) vare_COUNT = streng_data->길이목록[betalt_plassere]; memcpy(data, streng_data->data + betalt_plassere * 512, vare_COUNT);
    streng_data->상대창구번호 = streng_data->접속번호들[betalt_plassere]; streng_data->node_ADDRESS = streng_data->주소목록[betalt_plassere]; streng_data->맨앞 = (betalt_plassere + 1) % 4; streng_data->oppføring_COUNT--; return vare_COUNT;
}
unsigned Nettverk_portnummer(int fil_handtak) { 통신끝점 *streng_data = 얻기(fil_handtak); return !streng_data ? 0 : streng_data->kontakt_styring ? streng_data->kontakt_styring->local_port : streng_data->전문제어 ? streng_data->전문제어->local_port : 0; }
unsigned node_portnummer(int fil_handtak) { 통신끝점 *streng_data = 얻기(fil_handtak); return streng_data ? streng_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int fil_handtak) { 통신끝점 *streng_data = 얻기(fil_handtak); return streng_data ? streng_data->node_ADDRESS : 0; }
void Lukk_Nettverk(int fil_handtak) {
    통신끝점 *streng_data = 얻기(fil_handtak); if (!streng_data) return;
    if (streng_data->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_kategori && 통신끝점들[순번].informasjonsteknologi_ventande == fil_handtak) Lukk_Nettverk(순번);
    if (streng_data->kontakt_styring) {
        tcp_arg(streng_data->kontakt_styring, 0); if (streng_data->수신창구) tcp_accept(streng_data->kontakt_styring, 0); else { tcp_recv(streng_data->kontakt_styring, 0); tcp_err(streng_data->kontakt_styring, 0); }
        if (tcp_close(streng_data->kontakt_styring) != ERR_OK) tcp_abort(streng_data->kontakt_styring);
    }
    if (streng_data->전문제어) udp_remove(streng_data->전문제어); streng_data->TYPE_kategori = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&kontakt_mobil);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (maskin_registrere(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned teiknkode = maskin_registrere(보조장치 + 0x40) & 255;
        if (teiknkode == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *data_plassere = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (data_plassere) { 받은전문수++; RECEIVED_byte_COUNT += 수신사용량; pbuf_take(data_plassere, 수신자료, 수신사용량); if (kontakt_mobil.input(data_plassere, &kontakt_mobil) != ERR_OK) { 버린전문수++; pbuf_free(data_plassere); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (teiknkode == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (teiknkode != 220 && teiknkode != 221) 수신오류 = 1; teiknkode = teiknkode == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = teiknkode; else 수신오류 = 1;
        }
    }
    netif_poll(&kontakt_mobil); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (maskin_registrere(보조장치 + 0x54) & 0x20); 처리한도++) {
        maskin_registrere(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Innstillingar·조회는 lwIP의 faktisk_data 인터페이스와 avslutte_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned oppføring_VALUE, unsigned INDEX) {
    if(oppføring_VALUE==20)return 유선사용;
    if(oppføring_VALUE==21)return 준비됨&&netif_is_link_up(&kontakt_mobil);
    if(oppføring_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&oppføring_VALUE>=4&&oppføring_VALUE<=8)return 유선망집계(oppføring_VALUE-4);
    if (oppføring_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&kontakt_mobil)));
    if (oppføring_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&kontakt_mobil)));
    if (oppføring_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&kontakt_mobil)));
    if (oppføring_VALUE == 3) return netif_is_up(&kontakt_mobil) != 0;
    if (oppføring_VALUE == 4) return 받은전문수;
    if (oppføring_VALUE == 5) return 보낸전문수;
    if (oppføring_VALUE == 6) return RECEIVED_byte_COUNT;
    if (oppføring_VALUE == 7) return 보낸바이트수;
    if (oppføring_VALUE == 8) return 버린전문수;
    if (oppføring_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *avslutte_p = &통신끝점들[INDEX];
    if (oppføring_VALUE == 10) return avslutte_p->TYPE_kategori;
    if (!avslutte_p->TYPE_kategori) return 0;
    if (oppføring_VALUE == 11) return Nettverk_portnummer(INDEX);
    if (oppføring_VALUE == 12) return avslutte_p->node_ADDRESS;
    if (oppføring_VALUE == 13) return avslutte_p->상대창구번호;
    if (oppføring_VALUE == 14) return avslutte_p->수신창구 ? 1 : avslutte_p->fil_avslutte ? 3 : avslutte_p->FEIL ? 4 : avslutte_p->연결됨 ? 2 : 0;
    if (oppføring_VALUE == 15) return avslutte_p->oppføring_COUNT;
    if (oppføring_VALUE == 16) {
        const ip_addr_t *ADDRESS = avslutte_p->TYPE_kategori == 1 && avslutte_p->kontakt_styring ? &avslutte_p->kontakt_styring->local_ip :
            avslutte_p->TYPE_kategori == 2 && avslutte_p->전문제어 ? &avslutte_p->전문제어->local_ip : 0;
        return ADDRESS ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) : 0;
    }
    return 0;
}

int konfigurere_Nettverk(unsigned Handling, uint32_t ADDRESS, uint32_t maske_VALUE, uint32_t gateway_VALUE) {
    if (!준비됨) return -100;
    if (Handling == 1) { netif_set_up(&kontakt_mobil); return 0; }
    if (Handling == 2) { netif_set_down(&kontakt_mobil); return 0; }
    if (Handling != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maske_VALUE, 같은 망의 선택적 standardverdi gateway_VALUE. */
    uint32_t 뒤집은가림 = ~maske_VALUE;
    if (!maske_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !ADDRESS || (ADDRESS >> 24) == 127 ||
        (ADDRESS >> 24) == 0 || (ADDRESS >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADDRESS & 뒤집은가림) || (ADDRESS & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_VALUE && ((gateway_VALUE & maske_VALUE) != (ADDRESS & maske_VALUE) || gateway_VALUE == ADDRESS || (gateway_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_VALUE & 뒤집은가림) || (gateway_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADDRESS 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_kategori &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].kontakt_styring && ip_addr_isany(&통신끝점들[INDEX].kontakt_styring->local_ip))) return -16;
    if(유선사용)dhcp_stop(&kontakt_mobil);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADDRESS)); ip4_addr_set_u32(&새가림, lwip_htonl(maske_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_VALUE));
    netif_set_addr(&kontakt_mobil, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *Argument, struct raw_pcb *avslutte_p, struct pbuf *data, const ip_addr_t *ADDRESS) {
    (void)Argument; (void)avslutte_p;
    unsigned char 머리[20], svare[16];
    if (응답상태 != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) != 시험주소 || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned hode_endre_storleik = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || hode_endre_storleik < 20 || data->tot_len < hode_endre_storleik + 16 ||
        pbuf_copy_partial(data, svare, 16, hode_endre_storleik) != 16 || svare[0] || svare[1] ||
        (((unsigned)svare[4] << 8) | svare[5]) != 시험식별자 ||
        (((unsigned)svare[6] << 8) | svare[7]) != 시험순서 ||
        svare[8] != 'J' || svare[9] != 'K' || svare[10] != 'O' || svare[11] != 'S' ||
        (((uint32_t)svare[12] << 24) | ((uint32_t)svare[13] << 16) | ((uint32_t)svare[14] << 8) | svare[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, hode_endre_storleik)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, hode_endre_storleik); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(data); return 1;
}
int 응답시험시작(uint32_t ADDRESS, unsigned rekkjefølgje_VALUE) {
    if (!준비됨 || !netif_is_up(&kontakt_mobil)) return -100;
    if (!ADDRESS || (ADDRESS >> 28) >= 14 || ADDRESS == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ADDRESS; 시험순서 = rekkjefølgje_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = 시험순서 >> 8; data[7] = 시험순서;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=시험시각 >> 24; data[13]=시험시각 >> 16; data[14]=시험시각 >> 8; data[15]=시험시각;
    for (unsigned plassere_INDEX = 16; plassere_INDEX < sizeof(data); plassere_INDEX++) data[plassere_INDEX] = plassere_INDEX;
    uint16_t kontroll_kontrollsum = inet_chksum(data, sizeof(data)); memcpy(data + 2, &kontroll_kontrollsum, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t mål_endepunkt; ip_addr_set_ip4_u32(&mål_endepunkt, lwip_htonl(ADDRESS));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &mål_endepunkt); pbuf_free(전문);
    if (처리값) 응답상태 = feilnummer(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned oppføring_VALUE) {
    통신망살피기();
    return oppføring_VALUE == 0 ? 응답상태 : oppføring_VALUE == 1 ? (int)응답시간 : oppføring_VALUE == 2 ? (int)응답차례 : -22;
}
