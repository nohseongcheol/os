#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "netwerk_Munzell.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../mill_bogħod_VALUE/mill_bogħod_VALUE.h"
#include "wwajerjat_netwerk.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define kompjuter_i_rreġistra(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif konnessjoni_mowbajl;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_byte_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_kategorija, 수신창구, 대기중, 연결됨, fajl_ttermina, żball;
    struct tcp_pcb *konnessjoni_kontroll;
    struct udp_pcb *전문제어;
    unsigned 맨앞, entrata_COUNT;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], peer_ADDRESS;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int fajl_handle) { return fajl_handle >= 0 && fajl_handle < 32 && 통신끝점들[fajl_handle].TYPE_kategorija ? &통신끝점들[fajl_handle] : 0; }
static int 예약하기(int TYPE_kategorija) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_kategorija) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_kategorija = TYPE_kategorija; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kodiċi_tal_karattru) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kodiċi_tal_karattru; }
static err_t 출력결과(struct netif *element_COUNT, struct pbuf *data_pożizzjoni, const ip4_addr_t *ADDRESS) {
    (void)element_COUNT; (void)ADDRESS;
    if (data_pożizzjoni->tot_len > 1500 || 송신개수 + 2 * data_pożizzjoni->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Li_Jmiss_OFFSET = data_pożizzjoni; Li_Jmiss_OFFSET; Li_Jmiss_OFFSET = Li_Jmiss_OFFSET->next) for (unsigned 순번 = 0; 순번 < Li_Jmiss_OFFSET->len; 순번++) {
        unsigned kodiċi_tal_karattru = ((unsigned char *)Li_Jmiss_OFFSET->payload)[순번];
        if (kodiċi_tal_karattru == 192 || kodiċi_tal_karattru == 219) { 내보내기(219); 내보내기(kodiċi_tal_karattru == 192 ? 220 : 221); } else 내보내기(kodiċi_tal_karattru);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_pożizzjoni->tot_len; return ERR_OK;
}
static err_t Ħejji_tħaddim_tal_lingwa_komuni(struct netif *element_COUNT) { element_COUNT->name[0] = 's'; element_COUNT->name[1] = 'l'; element_COUNT->mtu = 1500; element_COUNT->output = 출력결과; return ERR_OK; }
void Ħejji_netwerk(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    kompjuter_i_rreġistra(보조장치 + 4) |= 1; kompjuter_i_rreġistra(보조장치 + 0x60) = 0; kompjuter_i_rreġistra(보조장치 + 0x44) = 0;
    kompjuter_i_rreġistra(보조장치 + 0x48) = 0xc6; kompjuter_i_rreġistra(보조장치 + 0x4c) = 3; kompjuter_i_rreġistra(보조장치 + 0x68) = 270; kompjuter_i_rreġistra(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t indirizz_tal_Internet, bit_maskra, gateway_ADDRESS;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&indirizz_tal_Internet, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_maskra, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gateway_ADDRESS, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&konnessjoni_mowbajl, &indirizz_tal_Internet, &bit_maskra, &gateway_ADDRESS, 0, 유선사용?Ħejji_wwajerjat_netwerk:Ħejji_tħaddim_tal_lingwa_komuni, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&konnessjoni_mowbajl); netif_set_up(&konnessjoni_mowbajl);if(!유선사용)netif_set_link_up(&konnessjoni_mowbajl); 준비됨 = 1;
    Ħejji_mill_bogħod();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *trażmissjoni_kontroll_imblokka, struct pbuf *data_pożizzjoni, err_t żball) {
    통신끝점 *string_data = 부가인수; (void)trażmissjoni_kontroll_imblokka; (void)żball;
    if (!data_pożizzjoni) { string_data->fajl_ttermina = 1; return ERR_OK; }
    if (data_pożizzjoni->tot_len > sizeof(string_data->data) - string_data->entrata_COUNT) return ERR_MEM;
    unsigned 현재위치 = (string_data->맨앞 + string_data->entrata_COUNT) % sizeof(string_data->data);
    for (struct pbuf *Li_Jmiss_OFFSET = data_pożizzjoni; Li_Jmiss_OFFSET; Li_Jmiss_OFFSET = Li_Jmiss_OFFSET->next) for (unsigned 순번 = 0; 순번 < Li_Jmiss_OFFSET->len; 순번++) {
        string_data->data[현재위치] = ((unsigned char *)Li_Jmiss_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(string_data->data);
    }
    string_data->entrata_COUNT += data_pożizzjoni->tot_len; pbuf_free(data_pożizzjoni); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t żball) { 통신끝점 *string_data = 부가인수; string_data->konnessjoni_kontroll = 0; string_data->żball = 오류번호(żball); }
static void 되부름목록(통신끝점 *string_data) { tcp_arg(string_data->konnessjoni_kontroll, string_data); tcp_recv(string_data->konnessjoni_kontroll, 수신됨); tcp_err(string_data->konnessjoni_kontroll, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *trażmissjoni_kontroll_imblokka, err_t żball) {
    통신끝점 *string_data = 부가인수; (void)trażmissjoni_kontroll_imblokka; if (żball) string_data->żball = 오류번호(żball); else string_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *trażmissjoni_kontroll_imblokka, err_t żball) {
    통신끝점 *부모항목 = 부가인수; if (żball) return żball;
    int fajl_handle = 예약하기(1); if (fajl_handle < 0) return ERR_MEM;
    통신끝점 *string_data = &통신끝점들[fajl_handle]; string_data->konnessjoni_kontroll = trażmissjoni_kontroll_imblokka; string_data->연결됨 = 1; string_data->대기중 = (int)(부모항목 - 통신끝점들);
    string_data->peer_ADDRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&trażmissjoni_kontroll_imblokka->remote_ip))); string_data->상대창구번호 = trażmissjoni_kontroll_imblokka->remote_port;
    되부름목록(string_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *trażmissjoni_kontroll_imblokka, struct pbuf *data_pożizzjoni, const ip_addr_t *ADDRESS, u16_t 접속번호) {
    통신끝점 *string_data = 부가인수; (void)trażmissjoni_kontroll_imblokka;
    if (string_data->entrata_COUNT < 4 && data_pożizzjoni->tot_len <= 512) {
        unsigned pożizzjoni_INDEX = (string_data->맨앞 + string_data->entrata_COUNT) % 4;
        pbuf_copy_partial(data_pożizzjoni, string_data->data + pożizzjoni_INDEX * 512, data_pożizzjoni->tot_len, 0);
        string_data->길이목록[pożizzjoni_INDEX] = data_pożizzjoni->tot_len; string_data->접속번호들[pożizzjoni_INDEX] = 접속번호;
        string_data->주소목록[pożizzjoni_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))); string_data->entrata_COUNT++;
    }
    pbuf_free(data_pożizzjoni);
}
int 통신끝점만들기(int TYPE_kategorija) {
    if (!준비됨) return -100;
    if (TYPE_kategorija != 1 && TYPE_kategorija != 2) return -93;
    int fajl_handle = 예약하기(TYPE_kategorija); if (fajl_handle < 0) return fajl_handle;
    통신끝점 *string_data = &통신끝점들[fajl_handle];
    if (TYPE_kategorija == 1) { string_data->konnessjoni_kontroll = tcp_new(); if (string_data->konnessjoni_kontroll) 되부름목록(string_data); }
    else { string_data->전문제어 = udp_new(); if (string_data->전문제어) udp_recv(string_data->전문제어, 전문, string_data); }
    if (!string_data->konnessjoni_kontroll && !string_data->전문제어) { string_data->TYPE_kategorija = 0; return -12; } return fajl_handle;
}
int 망주소묶기(int fajl_handle, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data) return -9;
    if (접속번호 > 65535 || (ADDRESS && ADDRESS != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&konnessjoni_mowbajl))) && ADDRESS != 0x7f000001)) return -99;
    ip_addr_t indirizz_tal_Internet; ip_addr_set_ip4_u32(&indirizz_tal_Internet, lwip_htonl(ADDRESS));
    err_t 보조항목 = string_data->TYPE_kategorija == 1 ? tcp_bind(string_data->konnessjoni_kontroll, &indirizz_tal_Internet, 접속번호) : udp_bind(string_data->전문제어, &indirizz_tal_Internet, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int fajl_handle) { 통신끝점 *string_data = 얻기(fajl_handle); if (string_data && string_data->konnessjoni_kontroll) ip_set_option(string_data->konnessjoni_kontroll, SOF_REUSEADDR); }
int 연결기다리기(int fajl_handle) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data || string_data->TYPE_kategorija != 1) return -9;
    if (string_data->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *trażmissjoni_kontroll_imblokka = tcp_listen_with_backlog_and_err(string_data->konnessjoni_kontroll, 4, &보조항목);
    if (!trażmissjoni_kontroll_imblokka) return 오류번호(보조항목); string_data->konnessjoni_kontroll = trażmissjoni_kontroll_imblokka; string_data->수신창구 = 1; tcp_arg(trażmissjoni_kontroll_imblokka, string_data); tcp_accept(trażmissjoni_kontroll_imblokka, 연결받음); return 0;
}
int 망연결하기(int fajl_handle, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data || string_data->TYPE_kategorija != 1) return -9;
    if (string_data->żball) return string_data->żball;
    if (string_data->연결됨) return 0;
    if (string_data->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !ADDRESS) return -22;
    ip_addr_t indirizz_tal_Internet; ip_addr_set_ip4_u32(&indirizz_tal_Internet, lwip_htonl(ADDRESS));
    string_data->peer_ADDRESS = ADDRESS; string_data->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(string_data->konnessjoni_kontroll, &indirizz_tal_Internet, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int fajl_handle) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data || !string_data->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_kategorija == 1 && 통신끝점들[순번].대기중 == fajl_handle) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int fajl_handle, void *data, unsigned element_COUNT) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data || string_data->TYPE_kategorija != 1) return -9;
    if (!element_COUNT) return 0; if (!string_data->entrata_COUNT) return string_data->żball ? string_data->żball : string_data->fajl_ttermina ? 0 : -11;
    if (element_COUNT > string_data->entrata_COUNT) element_COUNT = string_data->entrata_COUNT;
    for (unsigned 순번 = 0; 순번 < element_COUNT; 순번++) { ((unsigned char *)data)[순번] = string_data->data[string_data->맨앞]; string_data->맨앞 = (string_data->맨앞 + 1) % sizeof(string_data->data); }
    string_data->entrata_COUNT -= element_COUNT; if (string_data->konnessjoni_kontroll) tcp_recved(string_data->konnessjoni_kontroll, element_COUNT); return element_COUNT;
}
int 통신쓰기(int fajl_handle, const void *data, unsigned element_COUNT) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data || string_data->TYPE_kategorija != 1) return -9;
    if (string_data->żball) return string_data->żball; if (!string_data->konnessjoni_kontroll || !string_data->연결됨) return -107;
    if (!element_COUNT) return 0; if (element_COUNT > tcp_sndbuf(string_data->konnessjoni_kontroll)) element_COUNT = tcp_sndbuf(string_data->konnessjoni_kontroll);
    if (!element_COUNT) return -11; if (element_COUNT > 1024) element_COUNT = 1024;
    err_t 보조항목 = tcp_write(string_data->konnessjoni_kontroll, data, element_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(string_data->konnessjoni_kontroll); return element_COUNT;
}
int 전문보내기(int fajl_handle, const void *data, unsigned element_COUNT, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data || string_data->TYPE_kategorija != 2) return -9;
    if (element_COUNT > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *data_pożizzjoni = pbuf_alloc(PBUF_TRANSPORT, element_COUNT, PBUF_RAM); if (!data_pożizzjoni) return -11;
    pbuf_take(data_pożizzjoni, data, element_COUNT); ip_addr_t indirizz_tal_Internet; ip_addr_set_ip4_u32(&indirizz_tal_Internet, lwip_htonl(ADDRESS));
    err_t 보조항목 = udp_sendto(string_data->전문제어, data_pożizzjoni, &indirizz_tal_Internet, 접속번호); pbuf_free(data_pożizzjoni); return 보조항목 ? 오류번호(보조항목) : (int)element_COUNT;
}
int 전문받기(int fajl_handle, void *data, unsigned element_COUNT) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data || string_data->TYPE_kategorija != 2) return -9;
    if (!string_data->entrata_COUNT) return -11; unsigned 현재위치 = string_data->맨앞;
    if (element_COUNT > string_data->길이목록[현재위치]) element_COUNT = string_data->길이목록[현재위치]; memcpy(data, string_data->data + 현재위치 * 512, element_COUNT);
    string_data->상대창구번호 = string_data->접속번호들[현재위치]; string_data->peer_ADDRESS = string_data->주소목록[현재위치]; string_data->맨앞 = (현재위치 + 1) % 4; string_data->entrata_COUNT--; return element_COUNT;
}
unsigned 통신접속번호(int fajl_handle) { 통신끝점 *string_data = 얻기(fajl_handle); return !string_data ? 0 : string_data->konnessjoni_kontroll ? string_data->konnessjoni_kontroll->local_port : string_data->전문제어 ? string_data->전문제어->local_port : 0; }
unsigned 상대접속번호(int fajl_handle) { 통신끝점 *string_data = 얻기(fajl_handle); return string_data ? string_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int fajl_handle) { 통신끝점 *string_data = 얻기(fajl_handle); return string_data ? string_data->peer_ADDRESS : 0; }
void agħlaq_netwerk(int fajl_handle) {
    통신끝점 *string_data = 얻기(fajl_handle); if (!string_data) return;
    if (string_data->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_kategorija && 통신끝점들[순번].대기중 == fajl_handle) agħlaq_netwerk(순번);
    if (string_data->konnessjoni_kontroll) {
        tcp_arg(string_data->konnessjoni_kontroll, 0); if (string_data->수신창구) tcp_accept(string_data->konnessjoni_kontroll, 0); else { tcp_recv(string_data->konnessjoni_kontroll, 0); tcp_err(string_data->konnessjoni_kontroll, 0); }
        if (tcp_close(string_data->konnessjoni_kontroll) != ERR_OK) tcp_abort(string_data->konnessjoni_kontroll);
    }
    if (string_data->전문제어) udp_remove(string_data->전문제어); string_data->TYPE_kategorija = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&konnessjoni_mowbajl);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (kompjuter_i_rreġistra(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned kodiċi_tal_karattru = kompjuter_i_rreġistra(보조장치 + 0x40) & 255;
        if (kodiċi_tal_karattru == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *data_pożizzjoni = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (data_pożizzjoni) { 받은전문수++; RECEIVED_byte_COUNT += 수신사용량; pbuf_take(data_pożizzjoni, 수신자료, 수신사용량); if (konnessjoni_mowbajl.input(data_pożizzjoni, &konnessjoni_mowbajl) != ERR_OK) { 버린전문수++; pbuf_free(data_pożizzjoni); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (kodiċi_tal_karattru == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kodiċi_tal_karattru != 220 && kodiċi_tal_karattru != 221) 수신오류 = 1; kodiċi_tal_karattru = kodiċi_tal_karattru == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = kodiċi_tal_karattru; else 수신오류 = 1;
        }
    }
    netif_poll(&konnessjoni_mowbajl); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (kompjuter_i_rreġistra(보조장치 + 0x54) & 0x20); 처리한도++) {
        kompjuter_i_rreġistra(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Settings·조회는 lwIP의 attwali_data 인터페이스와 ttermina_punt 표를 사용한다. */
uint32_t 망상태읽기(unsigned entrata_VALUE, unsigned INDEX) {
    if(entrata_VALUE==20)return 유선사용;
    if(entrata_VALUE==21)return 준비됨&&netif_is_link_up(&konnessjoni_mowbajl);
    if(entrata_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&entrata_VALUE>=4&&entrata_VALUE<=8)return 유선망집계(entrata_VALUE-4);
    if (entrata_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&konnessjoni_mowbajl)));
    if (entrata_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&konnessjoni_mowbajl)));
    if (entrata_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&konnessjoni_mowbajl)));
    if (entrata_VALUE == 3) return netif_is_up(&konnessjoni_mowbajl) != 0;
    if (entrata_VALUE == 4) return 받은전문수;
    if (entrata_VALUE == 5) return 보낸전문수;
    if (entrata_VALUE == 6) return RECEIVED_byte_COUNT;
    if (entrata_VALUE == 7) return 보낸바이트수;
    if (entrata_VALUE == 8) return 버린전문수;
    if (entrata_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *ttermina_punt = &통신끝점들[INDEX];
    if (entrata_VALUE == 10) return ttermina_punt->TYPE_kategorija;
    if (!ttermina_punt->TYPE_kategorija) return 0;
    if (entrata_VALUE == 11) return 통신접속번호(INDEX);
    if (entrata_VALUE == 12) return ttermina_punt->peer_ADDRESS;
    if (entrata_VALUE == 13) return ttermina_punt->상대창구번호;
    if (entrata_VALUE == 14) return ttermina_punt->수신창구 ? 1 : ttermina_punt->fajl_ttermina ? 3 : ttermina_punt->żball ? 4 : ttermina_punt->연결됨 ? 2 : 0;
    if (entrata_VALUE == 15) return ttermina_punt->entrata_COUNT;
    if (entrata_VALUE == 16) {
        const ip_addr_t *ADDRESS = ttermina_punt->TYPE_kategorija == 1 && ttermina_punt->konnessjoni_kontroll ? &ttermina_punt->konnessjoni_kontroll->local_ip :
            ttermina_punt->TYPE_kategorija == 2 && ttermina_punt->전문제어 ? &ttermina_punt->전문제어->local_ip : 0;
        return ADDRESS ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) : 0;
    }
    return 0;
}

int kkonfigura_netwerk(unsigned azzjoni, uint32_t ADDRESS, uint32_t maskra_VALUE, uint32_t gateway_VALUE) {
    if (!준비됨) return -100;
    if (azzjoni == 1) { netif_set_up(&konnessjoni_mowbajl); return 0; }
    if (azzjoni == 2) { netif_set_down(&konnessjoni_mowbajl); return 0; }
    if (azzjoni != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maskra_VALUE, 같은 망의 선택적 valur_default gateway_VALUE. */
    uint32_t 뒤집은가림 = ~maskra_VALUE;
    if (!maskra_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !ADDRESS || (ADDRESS >> 24) == 127 ||
        (ADDRESS >> 24) == 0 || (ADDRESS >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADDRESS & 뒤집은가림) || (ADDRESS & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_VALUE && ((gateway_VALUE & maskra_VALUE) != (ADDRESS & maskra_VALUE) || gateway_VALUE == ADDRESS || (gateway_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_VALUE & 뒤집은가림) || (gateway_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADDRESS 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_kategorija &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].konnessjoni_kontroll && ip_addr_isany(&통신끝점들[INDEX].konnessjoni_kontroll->local_ip))) return -16;
    if(유선사용)dhcp_stop(&konnessjoni_mowbajl);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADDRESS)); ip4_addr_set_u32(&새가림, lwip_htonl(maskra_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_VALUE));
    netif_set_addr(&konnessjoni_mowbajl, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *ttermina_punt, struct pbuf *data, const ip_addr_t *ADDRESS) {
    (void)인수; (void)ttermina_punt;
    unsigned char 머리[20], wieġeb[16];
    if (응답상태 != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) != 시험주소 || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Intestazzjoni_daqqas = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Intestazzjoni_daqqas < 20 || data->tot_len < Intestazzjoni_daqqas + 16 ||
        pbuf_copy_partial(data, wieġeb, 16, Intestazzjoni_daqqas) != 16 || wieġeb[0] || wieġeb[1] ||
        (((unsigned)wieġeb[4] << 8) | wieġeb[5]) != 시험식별자 ||
        (((unsigned)wieġeb[6] << 8) | wieġeb[7]) != 시험순서 ||
        wieġeb[8] != 'J' || wieġeb[9] != 'K' || wieġeb[10] != 'O' || wieġeb[11] != 'S' ||
        (((uint32_t)wieġeb[12] << 24) | ((uint32_t)wieġeb[13] << 16) | ((uint32_t)wieġeb[14] << 8) | wieġeb[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Intestazzjoni_daqqas)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Intestazzjoni_daqqas); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(data); return 1;
}
int 응답시험시작(uint32_t ADDRESS, unsigned ordni_VALUE) {
    if (!준비됨 || !netif_is_up(&konnessjoni_mowbajl)) return -100;
    if (!ADDRESS || (ADDRESS >> 28) >= 14 || ADDRESS == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ADDRESS; 시험순서 = ordni_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = 시험순서 >> 8; data[7] = 시험순서;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=시험시각 >> 24; data[13]=시험시각 >> 16; data[14]=시험시각 >> 8; data[15]=시험시각;
    for (unsigned pożizzjoni_INDEX = 16; pożizzjoni_INDEX < sizeof(data); pożizzjoni_INDEX++) data[pożizzjoni_INDEX] = pożizzjoni_INDEX;
    uint16_t 확인합 = inet_chksum(data, sizeof(data)); memcpy(data + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ADDRESS));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned entrata_VALUE) {
    통신망살피기();
    return entrata_VALUE == 0 ? 응답상태 : entrata_VALUE == 1 ? (int)응답시간 : entrata_VALUE == 2 ? (int)응답차례 : -22;
}
