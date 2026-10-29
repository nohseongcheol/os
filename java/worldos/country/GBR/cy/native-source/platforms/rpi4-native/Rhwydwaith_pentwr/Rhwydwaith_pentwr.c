#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Rhwydwaith_pentwr.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../pell_VALUE/pell_VALUE.h"
#include "wedi_i_wifro_Rhwydwaith.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define peiriant_cofrestru(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif cyswllt_dyfais;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_beit_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_ardal, 수신창구, technoleg_gwybodaeth_yn_disgwyl, 연결됨, ffeil_gorffen, Gwall;
    struct tcp_pcb *cyswllt_rheoli;
    struct udp_pcb *전문제어;
    unsigned 맨앞, cofnod_COUNT;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], cymar_ADDRESS;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int ffeil_dolen) { return ffeil_dolen >= 0 && ffeil_dolen < 32 && 통신끝점들[ffeil_dolen].TYPE_ardal ? &통신끝점들[ffeil_dolen] : 0; }
static int 예약하기(int TYPE_ardal) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_ardal) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_ardal = TYPE_ardal; 통신끝점들[순번].technoleg_gwybodaeth_yn_disgwyl = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned cod_nod) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = cod_nod; }
static err_t 출력결과(struct netif *eitem_COUNT, struct pbuf *data_safle, const ip4_addr_t *ADDRESS) {
    (void)eitem_COUNT; (void)ADDRESS;
    if (data_safle->tot_len > 1500 || 송신개수 + 2 * data_safle->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Nesaf_OFFSET = data_safle; Nesaf_OFFSET; Nesaf_OFFSET = Nesaf_OFFSET->next) for (unsigned 순번 = 0; 순번 < Nesaf_OFFSET->len; 순번++) {
        unsigned cod_nod = ((unsigned char *)Nesaf_OFFSET->payload)[순번];
        if (cod_nod == 192 || cod_nod == 219) { 내보내기(219); 내보내기(cod_nod == 192 ? 220 : 221); } else 내보내기(cod_nod);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_safle->tot_len; return ERR_OK;
}
static err_t Paratoi_amser_rhedeg_iaith_gyffredin(struct netif *eitem_COUNT) { eitem_COUNT->name[0] = 's'; eitem_COUNT->name[1] = 'l'; eitem_COUNT->mtu = 1500; eitem_COUNT->output = 출력결과; return ERR_OK; }
void Paratoi_Rhwydwaith(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    peiriant_cofrestru(보조장치 + 4) |= 1; peiriant_cofrestru(보조장치 + 0x60) = 0; peiriant_cofrestru(보조장치 + 0x44) = 0;
    peiriant_cofrestru(보조장치 + 0x48) = 0xc6; peiriant_cofrestru(보조장치 + 0x4c) = 3; peiriant_cofrestru(보조장치 + 0x68) = 270; peiriant_cofrestru(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t cyfeiriad_rhyngrwyd, did_masgio, adwy_ADDRESS;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&cyfeiriad_rhyngrwyd, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&did_masgio, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&adwy_ADDRESS, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&cyswllt_dyfais, &cyfeiriad_rhyngrwyd, &did_masgio, &adwy_ADDRESS, 0, 유선사용?Paratoi_wedi_i_wifro_Rhwydwaith:Paratoi_amser_rhedeg_iaith_gyffredin, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&cyswllt_dyfais); netif_set_up(&cyswllt_dyfais);if(!유선사용)netif_set_link_up(&cyswllt_dyfais); 준비됨 = 1;
    Paratoi_pell();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *trawsyriant_rheoli_rhwystro, struct pbuf *data_safle, err_t Gwall) {
    통신끝점 *testun_data = 부가인수; (void)trawsyriant_rheoli_rhwystro; (void)Gwall;
    if (!data_safle) { testun_data->ffeil_gorffen = 1; return ERR_OK; }
    if (data_safle->tot_len > sizeof(testun_data->data) - testun_data->cofnod_COUNT) return ERR_MEM;
    unsigned 현재위치 = (testun_data->맨앞 + testun_data->cofnod_COUNT) % sizeof(testun_data->data);
    for (struct pbuf *Nesaf_OFFSET = data_safle; Nesaf_OFFSET; Nesaf_OFFSET = Nesaf_OFFSET->next) for (unsigned 순번 = 0; 순번 < Nesaf_OFFSET->len; 순번++) {
        testun_data->data[현재위치] = ((unsigned char *)Nesaf_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(testun_data->data);
    }
    testun_data->cofnod_COUNT += data_safle->tot_len; pbuf_free(data_safle); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Gwall) { 통신끝점 *testun_data = 부가인수; testun_data->cyswllt_rheoli = 0; testun_data->Gwall = 오류번호(Gwall); }
static void 되부름목록(통신끝점 *testun_data) { tcp_arg(testun_data->cyswllt_rheoli, testun_data); tcp_recv(testun_data->cyswllt_rheoli, 수신됨); tcp_err(testun_data->cyswllt_rheoli, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *trawsyriant_rheoli_rhwystro, err_t Gwall) {
    통신끝점 *testun_data = 부가인수; (void)trawsyriant_rheoli_rhwystro; if (Gwall) testun_data->Gwall = 오류번호(Gwall); else testun_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *trawsyriant_rheoli_rhwystro, err_t Gwall) {
    통신끝점 *부모항목 = 부가인수; if (Gwall) return Gwall;
    int ffeil_dolen = 예약하기(1); if (ffeil_dolen < 0) return ERR_MEM;
    통신끝점 *testun_data = &통신끝점들[ffeil_dolen]; testun_data->cyswllt_rheoli = trawsyriant_rheoli_rhwystro; testun_data->연결됨 = 1; testun_data->technoleg_gwybodaeth_yn_disgwyl = (int)(부모항목 - 통신끝점들);
    testun_data->cymar_ADDRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&trawsyriant_rheoli_rhwystro->remote_ip))); testun_data->상대창구번호 = trawsyriant_rheoli_rhwystro->remote_port;
    되부름목록(testun_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *trawsyriant_rheoli_rhwystro, struct pbuf *data_safle, const ip_addr_t *ADDRESS, u16_t rhif_porth) {
    통신끝점 *testun_data = 부가인수; (void)trawsyriant_rheoli_rhwystro;
    if (testun_data->cofnod_COUNT < 4 && data_safle->tot_len <= 512) {
        unsigned safle_INDEX = (testun_data->맨앞 + testun_data->cofnod_COUNT) % 4;
        pbuf_copy_partial(data_safle, testun_data->data + safle_INDEX * 512, data_safle->tot_len, 0);
        testun_data->길이목록[safle_INDEX] = data_safle->tot_len; testun_data->접속번호들[safle_INDEX] = rhif_porth;
        testun_data->주소목록[safle_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))); testun_data->cofnod_COUNT++;
    }
    pbuf_free(data_safle);
}
int 통신끝점만들기(int TYPE_ardal) {
    if (!준비됨) return -100;
    if (TYPE_ardal != 1 && TYPE_ardal != 2) return -93;
    int ffeil_dolen = 예약하기(TYPE_ardal); if (ffeil_dolen < 0) return ffeil_dolen;
    통신끝점 *testun_data = &통신끝점들[ffeil_dolen];
    if (TYPE_ardal == 1) { testun_data->cyswllt_rheoli = tcp_new(); if (testun_data->cyswllt_rheoli) 되부름목록(testun_data); }
    else { testun_data->전문제어 = udp_new(); if (testun_data->전문제어) udp_recv(testun_data->전문제어, 전문, testun_data); }
    if (!testun_data->cyswllt_rheoli && !testun_data->전문제어) { testun_data->TYPE_ardal = 0; return -12; } return ffeil_dolen;
}
int 망주소묶기(int ffeil_dolen, uint32_t ADDRESS, unsigned rhif_porth) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data) return -9;
    if (rhif_porth > 65535 || (ADDRESS && ADDRESS != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&cyswllt_dyfais))) && ADDRESS != 0x7f000001)) return -99;
    ip_addr_t cyfeiriad_rhyngrwyd; ip_addr_set_ip4_u32(&cyfeiriad_rhyngrwyd, lwip_htonl(ADDRESS));
    err_t 보조항목 = testun_data->TYPE_ardal == 1 ? tcp_bind(testun_data->cyswllt_rheoli, &cyfeiriad_rhyngrwyd, rhif_porth) : udp_bind(testun_data->전문제어, &cyfeiriad_rhyngrwyd, rhif_porth); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int ffeil_dolen) { 통신끝점 *testun_data = 얻기(ffeil_dolen); if (testun_data && testun_data->cyswllt_rheoli) ip_set_option(testun_data->cyswllt_rheoli, SOF_REUSEADDR); }
int 연결기다리기(int ffeil_dolen) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data || testun_data->TYPE_ardal != 1) return -9;
    if (testun_data->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *trawsyriant_rheoli_rhwystro = tcp_listen_with_backlog_and_err(testun_data->cyswllt_rheoli, 4, &보조항목);
    if (!trawsyriant_rheoli_rhwystro) return 오류번호(보조항목); testun_data->cyswllt_rheoli = trawsyriant_rheoli_rhwystro; testun_data->수신창구 = 1; tcp_arg(trawsyriant_rheoli_rhwystro, testun_data); tcp_accept(trawsyriant_rheoli_rhwystro, 연결받음); return 0;
}
int 망연결하기(int ffeil_dolen, uint32_t ADDRESS, unsigned rhif_porth) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data || testun_data->TYPE_ardal != 1) return -9;
    if (testun_data->Gwall) return testun_data->Gwall;
    if (testun_data->연결됨) return 0;
    if (testun_data->상대창구번호) return -115;
    if (!rhif_porth || rhif_porth > 65535 || !ADDRESS) return -22;
    ip_addr_t cyfeiriad_rhyngrwyd; ip_addr_set_ip4_u32(&cyfeiriad_rhyngrwyd, lwip_htonl(ADDRESS));
    testun_data->cymar_ADDRESS = ADDRESS; testun_data->상대창구번호 = rhif_porth;
    err_t 보조항목 = tcp_connect(testun_data->cyswllt_rheoli, &cyfeiriad_rhyngrwyd, rhif_porth, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int ffeil_dolen) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data || !testun_data->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_ardal == 1 && 통신끝점들[순번].technoleg_gwybodaeth_yn_disgwyl == ffeil_dolen) { 통신끝점들[순번].technoleg_gwybodaeth_yn_disgwyl = -1; return 순번; }
    return -11;
}
int 통신읽기(int ffeil_dolen, void *data, unsigned eitem_COUNT) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data || testun_data->TYPE_ardal != 1) return -9;
    if (!eitem_COUNT) return 0; if (!testun_data->cofnod_COUNT) return testun_data->Gwall ? testun_data->Gwall : testun_data->ffeil_gorffen ? 0 : -11;
    if (eitem_COUNT > testun_data->cofnod_COUNT) eitem_COUNT = testun_data->cofnod_COUNT;
    for (unsigned 순번 = 0; 순번 < eitem_COUNT; 순번++) { ((unsigned char *)data)[순번] = testun_data->data[testun_data->맨앞]; testun_data->맨앞 = (testun_data->맨앞 + 1) % sizeof(testun_data->data); }
    testun_data->cofnod_COUNT -= eitem_COUNT; if (testun_data->cyswllt_rheoli) tcp_recved(testun_data->cyswllt_rheoli, eitem_COUNT); return eitem_COUNT;
}
int 통신쓰기(int ffeil_dolen, const void *data, unsigned eitem_COUNT) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data || testun_data->TYPE_ardal != 1) return -9;
    if (testun_data->Gwall) return testun_data->Gwall; if (!testun_data->cyswllt_rheoli || !testun_data->연결됨) return -107;
    if (!eitem_COUNT) return 0; if (eitem_COUNT > tcp_sndbuf(testun_data->cyswllt_rheoli)) eitem_COUNT = tcp_sndbuf(testun_data->cyswllt_rheoli);
    if (!eitem_COUNT) return -11; if (eitem_COUNT > 1024) eitem_COUNT = 1024;
    err_t 보조항목 = tcp_write(testun_data->cyswllt_rheoli, data, eitem_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(testun_data->cyswllt_rheoli); return eitem_COUNT;
}
int 전문보내기(int ffeil_dolen, const void *data, unsigned eitem_COUNT, uint32_t ADDRESS, unsigned rhif_porth) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data || testun_data->TYPE_ardal != 2) return -9;
    if (eitem_COUNT > 512) return -90; if (!rhif_porth || rhif_porth > 65535) return -22;
    struct pbuf *data_safle = pbuf_alloc(PBUF_TRANSPORT, eitem_COUNT, PBUF_RAM); if (!data_safle) return -11;
    pbuf_take(data_safle, data, eitem_COUNT); ip_addr_t cyfeiriad_rhyngrwyd; ip_addr_set_ip4_u32(&cyfeiriad_rhyngrwyd, lwip_htonl(ADDRESS));
    err_t 보조항목 = udp_sendto(testun_data->전문제어, data_safle, &cyfeiriad_rhyngrwyd, rhif_porth); pbuf_free(data_safle); return 보조항목 ? 오류번호(보조항목) : (int)eitem_COUNT;
}
int 전문받기(int ffeil_dolen, void *data, unsigned eitem_COUNT) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data || testun_data->TYPE_ardal != 2) return -9;
    if (!testun_data->cofnod_COUNT) return -11; unsigned 현재위치 = testun_data->맨앞;
    if (eitem_COUNT > testun_data->길이목록[현재위치]) eitem_COUNT = testun_data->길이목록[현재위치]; memcpy(data, testun_data->data + 현재위치 * 512, eitem_COUNT);
    testun_data->상대창구번호 = testun_data->접속번호들[현재위치]; testun_data->cymar_ADDRESS = testun_data->주소목록[현재위치]; testun_data->맨앞 = (현재위치 + 1) % 4; testun_data->cofnod_COUNT--; return eitem_COUNT;
}
unsigned Rhwydwaith_rhif_porth(int ffeil_dolen) { 통신끝점 *testun_data = 얻기(ffeil_dolen); return !testun_data ? 0 : testun_data->cyswllt_rheoli ? testun_data->cyswllt_rheoli->local_port : testun_data->전문제어 ? testun_data->전문제어->local_port : 0; }
unsigned cymar_rhif_porth(int ffeil_dolen) { 통신끝점 *testun_data = 얻기(ffeil_dolen); return testun_data ? testun_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int ffeil_dolen) { 통신끝점 *testun_data = 얻기(ffeil_dolen); return testun_data ? testun_data->cymar_ADDRESS : 0; }
void cau_Rhwydwaith(int ffeil_dolen) {
    통신끝점 *testun_data = 얻기(ffeil_dolen); if (!testun_data) return;
    if (testun_data->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_ardal && 통신끝점들[순번].technoleg_gwybodaeth_yn_disgwyl == ffeil_dolen) cau_Rhwydwaith(순번);
    if (testun_data->cyswllt_rheoli) {
        tcp_arg(testun_data->cyswllt_rheoli, 0); if (testun_data->수신창구) tcp_accept(testun_data->cyswllt_rheoli, 0); else { tcp_recv(testun_data->cyswllt_rheoli, 0); tcp_err(testun_data->cyswllt_rheoli, 0); }
        if (tcp_close(testun_data->cyswllt_rheoli) != ERR_OK) tcp_abort(testun_data->cyswllt_rheoli);
    }
    if (testun_data->전문제어) udp_remove(testun_data->전문제어); testun_data->TYPE_ardal = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&cyswllt_dyfais);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (peiriant_cofrestru(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned cod_nod = peiriant_cofrestru(보조장치 + 0x40) & 255;
        if (cod_nod == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *data_safle = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (data_safle) { 받은전문수++; RECEIVED_beit_COUNT += 수신사용량; pbuf_take(data_safle, 수신자료, 수신사용량); if (cyswllt_dyfais.input(data_safle, &cyswllt_dyfais) != ERR_OK) { 버린전문수++; pbuf_free(data_safle); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (cod_nod == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (cod_nod != 220 && cod_nod != 221) 수신오류 = 1; cod_nod = cod_nod == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = cod_nod; else 수신오류 = 1;
        }
    }
    netif_poll(&cyswllt_dyfais); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (peiriant_cofrestru(보조장치 + 0x54) & 0x20); 처리한도++) {
        peiriant_cofrestru(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Gosodiadau·조회는 lwIP의 go_iawn_data 인터페이스와 gorffen_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned cofnod_VALUE, unsigned INDEX) {
    if(cofnod_VALUE==20)return 유선사용;
    if(cofnod_VALUE==21)return 준비됨&&netif_is_link_up(&cyswllt_dyfais);
    if(cofnod_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&cofnod_VALUE>=4&&cofnod_VALUE<=8)return 유선망집계(cofnod_VALUE-4);
    if (cofnod_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&cyswllt_dyfais)));
    if (cofnod_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&cyswllt_dyfais)));
    if (cofnod_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&cyswllt_dyfais)));
    if (cofnod_VALUE == 3) return netif_is_up(&cyswllt_dyfais) != 0;
    if (cofnod_VALUE == 4) return 받은전문수;
    if (cofnod_VALUE == 5) return 보낸전문수;
    if (cofnod_VALUE == 6) return RECEIVED_beit_COUNT;
    if (cofnod_VALUE == 7) return 보낸바이트수;
    if (cofnod_VALUE == 8) return 버린전문수;
    if (cofnod_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *gorffen_p = &통신끝점들[INDEX];
    if (cofnod_VALUE == 10) return gorffen_p->TYPE_ardal;
    if (!gorffen_p->TYPE_ardal) return 0;
    if (cofnod_VALUE == 11) return Rhwydwaith_rhif_porth(INDEX);
    if (cofnod_VALUE == 12) return gorffen_p->cymar_ADDRESS;
    if (cofnod_VALUE == 13) return gorffen_p->상대창구번호;
    if (cofnod_VALUE == 14) return gorffen_p->수신창구 ? 1 : gorffen_p->ffeil_gorffen ? 3 : gorffen_p->Gwall ? 4 : gorffen_p->연결됨 ? 2 : 0;
    if (cofnod_VALUE == 15) return gorffen_p->cofnod_COUNT;
    if (cofnod_VALUE == 16) {
        const ip_addr_t *ADDRESS = gorffen_p->TYPE_ardal == 1 && gorffen_p->cyswllt_rheoli ? &gorffen_p->cyswllt_rheoli->local_ip :
            gorffen_p->TYPE_ardal == 2 && gorffen_p->전문제어 ? &gorffen_p->전문제어->local_ip : 0;
        return ADDRESS ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) : 0;
    }
    return 0;
}

int ffurfweddu_Rhwydwaith(unsigned Gweithrediad, uint32_t ADDRESS, uint32_t masgio_VALUE, uint32_t adwy_VALUE) {
    if (!준비됨) return -100;
    if (Gweithrediad == 1) { netif_set_up(&cyswllt_dyfais); return 0; }
    if (Gweithrediad == 2) { netif_set_down(&cyswllt_dyfais); return 0; }
    if (Gweithrediad != 0) return -22;
    /* 유니캐스트 IPv4, 연속 masgio_VALUE, 같은 망의 선택적 gwerth_diofyn adwy_VALUE. */
    uint32_t 뒤집은가림 = ~masgio_VALUE;
    if (!masgio_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !ADDRESS || (ADDRESS >> 24) == 127 ||
        (ADDRESS >> 24) == 0 || (ADDRESS >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADDRESS & 뒤집은가림) || (ADDRESS & 뒤집은가림) == 뒤집은가림)) ||
        (adwy_VALUE && ((adwy_VALUE & masgio_VALUE) != (ADDRESS & masgio_VALUE) || adwy_VALUE == ADDRESS || (adwy_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(adwy_VALUE & 뒤집은가림) || (adwy_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADDRESS 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_ardal &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].cyswllt_rheoli && ip_addr_isany(&통신끝점들[INDEX].cyswllt_rheoli->local_ip))) return -16;
    if(유선사용)dhcp_stop(&cyswllt_dyfais);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADDRESS)); ip4_addr_set_u32(&새가림, lwip_htonl(masgio_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(adwy_VALUE));
    netif_set_addr(&cyswllt_dyfais, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *gorffen_p, struct pbuf *data, const ip_addr_t *ADDRESS) {
    (void)인수; (void)gorffen_p;
    unsigned char 머리[20], ateb[16];
    if (응답상태 != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) != 시험주소 || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Pennyn_newid_maint = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Pennyn_newid_maint < 20 || data->tot_len < Pennyn_newid_maint + 16 ||
        pbuf_copy_partial(data, ateb, 16, Pennyn_newid_maint) != 16 || ateb[0] || ateb[1] ||
        (((unsigned)ateb[4] << 8) | ateb[5]) != 시험식별자 ||
        (((unsigned)ateb[6] << 8) | ateb[7]) != 시험순서 ||
        ateb[8] != 'J' || ateb[9] != 'K' || ateb[10] != 'O' || ateb[11] != 'S' ||
        (((uint32_t)ateb[12] << 24) | ((uint32_t)ateb[13] << 16) | ((uint32_t)ateb[14] << 8) | ateb[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Pennyn_newid_maint)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Pennyn_newid_maint); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(data); return 1;
}
int 응답시험시작(uint32_t ADDRESS, unsigned trefn_VALUE) {
    if (!준비됨 || !netif_is_up(&cyswllt_dyfais)) return -100;
    if (!ADDRESS || (ADDRESS >> 28) >= 14 || ADDRESS == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ADDRESS; 시험순서 = trefn_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = 시험순서 >> 8; data[7] = 시험순서;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=시험시각 >> 24; data[13]=시험시각 >> 16; data[14]=시험시각 >> 8; data[15]=시험시각;
    for (unsigned safle_INDEX = 16; safle_INDEX < sizeof(data); safle_INDEX++) data[safle_INDEX] = safle_INDEX;
    uint16_t gwirio_prawfswm = inet_chksum(data, sizeof(data)); memcpy(data + 2, &gwirio_prawfswm, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ADDRESS));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned cofnod_VALUE) {
    통신망살피기();
    return cofnod_VALUE == 0 ? 응답상태 : cofnod_VALUE == 1 ? (int)응답시간 : cofnod_VALUE == 2 ? (int)응답차례 : -22;
}
