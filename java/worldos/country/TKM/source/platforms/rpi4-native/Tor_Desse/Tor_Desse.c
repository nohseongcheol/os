#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Tor_Desse.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../uzakdan_baha/uzakdan_baha.h"
#include "simli_Tor.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define 기계저장기(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif birikme_enjam;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int ýaz_kategoriýa, 수신창구, 대기중, 연결됨, faýl_tamamla, Hata;
    struct tcp_pcb *birikme_dolandyryş;
    struct udp_pcb *전문제어;
    unsigned 맨앞, 항목수;
    unsigned char maglumat[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], deň_derejeli_düwün_salgy;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int faýl_ryçag) { return faýl_ryçag >= 0 && faýl_ryçag < 32 && 통신끝점들[faýl_ryçag].ýaz_kategoriýa ? &통신끝점들[faýl_ryçag] : 0; }
static int 예약하기(int ýaz_kategoriýa) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].ýaz_kategoriýa) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].ýaz_kategoriýa = ýaz_kategoriýa; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned nyşanyň_kody) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = nyşanyň_kody; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *salgy) {
    (void)개수; (void)salgy;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned nyşanyň_kody = ((unsigned char *)다음위치->payload)[순번];
        if (nyşanyň_kody == 192 || nyşanyň_kody == 219) { 내보내기(219); 내보내기(nyşanyň_kody == 192 ? 220 : 221); } else 내보내기(nyşanyň_kody);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t Taýýarla_umumy_dil_işlediş_gurşawy(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Taýýarla_Tor(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    기계저장기(보조장치 + 4) |= 1; 기계저장기(보조장치 + 0x60) = 0; 기계저장기(보조장치 + 0x44) = 0;
    기계저장기(보조장치 + 0x48) = 0xc6; 기계저장기(보조장치 + 0x4c) = 3; 기계저장기(보조장치 + 0x68) = 270; 기계저장기(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internet_salgy, bit_örtük, şlýuz_salgy;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Internet_salgy, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_örtük, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&şlýuz_salgy, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&birikme_enjam, &Internet_salgy, &bit_örtük, &şlýuz_salgy, 0, 유선사용?Taýýarla_simli_Tor:Taýýarla_umumy_dil_işlediş_gurşawy, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&birikme_enjam); netif_set_up(&birikme_enjam);if(!유선사용)netif_set_link_up(&birikme_enjam); 준비됨 = 1;
    Taýýarla_uzakdan();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *geçiriş_dolandyryş_bökde, struct pbuf *자료위치, err_t Hata) {
    통신끝점 *setir_maglumat = 부가인수; (void)geçiriş_dolandyryş_bökde; (void)Hata;
    if (!자료위치) { setir_maglumat->faýl_tamamla = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(setir_maglumat->maglumat) - setir_maglumat->항목수) return ERR_MEM;
    unsigned 현재위치 = (setir_maglumat->맨앞 + setir_maglumat->항목수) % sizeof(setir_maglumat->maglumat);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        setir_maglumat->maglumat[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(setir_maglumat->maglumat);
    }
    setir_maglumat->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Hata) { 통신끝점 *setir_maglumat = 부가인수; setir_maglumat->birikme_dolandyryş = 0; setir_maglumat->Hata = 오류번호(Hata); }
static void 되부름목록(통신끝점 *setir_maglumat) { tcp_arg(setir_maglumat->birikme_dolandyryş, setir_maglumat); tcp_recv(setir_maglumat->birikme_dolandyryş, 수신됨); tcp_err(setir_maglumat->birikme_dolandyryş, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *geçiriş_dolandyryş_bökde, err_t Hata) {
    통신끝점 *setir_maglumat = 부가인수; (void)geçiriş_dolandyryş_bökde; if (Hata) setir_maglumat->Hata = 오류번호(Hata); else setir_maglumat->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *geçiriş_dolandyryş_bökde, err_t Hata) {
    통신끝점 *부모항목 = 부가인수; if (Hata) return Hata;
    int faýl_ryçag = 예약하기(1); if (faýl_ryçag < 0) return ERR_MEM;
    통신끝점 *setir_maglumat = &통신끝점들[faýl_ryçag]; setir_maglumat->birikme_dolandyryş = geçiriş_dolandyryş_bökde; setir_maglumat->연결됨 = 1; setir_maglumat->대기중 = (int)(부모항목 - 통신끝점들);
    setir_maglumat->deň_derejeli_düwün_salgy = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&geçiriş_dolandyryş_bökde->remote_ip))); setir_maglumat->상대창구번호 = geçiriş_dolandyryş_bökde->remote_port;
    되부름목록(setir_maglumat); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *geçiriş_dolandyryş_bökde, struct pbuf *자료위치, const ip_addr_t *salgy, u16_t 접속번호) {
    통신끝점 *setir_maglumat = 부가인수; (void)geçiriş_dolandyryş_bökde;
    if (setir_maglumat->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (setir_maglumat->맨앞 + setir_maglumat->항목수) % 4;
        pbuf_copy_partial(자료위치, setir_maglumat->maglumat + 자리 * 512, 자료위치->tot_len, 0);
        setir_maglumat->길이목록[자리] = 자료위치->tot_len; setir_maglumat->접속번호들[자리] = 접속번호;
        setir_maglumat->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(salgy))); setir_maglumat->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int ýaz_kategoriýa) {
    if (!준비됨) return -100;
    if (ýaz_kategoriýa != 1 && ýaz_kategoriýa != 2) return -93;
    int faýl_ryçag = 예약하기(ýaz_kategoriýa); if (faýl_ryçag < 0) return faýl_ryçag;
    통신끝점 *setir_maglumat = &통신끝점들[faýl_ryçag];
    if (ýaz_kategoriýa == 1) { setir_maglumat->birikme_dolandyryş = tcp_new(); if (setir_maglumat->birikme_dolandyryş) 되부름목록(setir_maglumat); }
    else { setir_maglumat->전문제어 = udp_new(); if (setir_maglumat->전문제어) udp_recv(setir_maglumat->전문제어, 전문, setir_maglumat); }
    if (!setir_maglumat->birikme_dolandyryş && !setir_maglumat->전문제어) { setir_maglumat->ýaz_kategoriýa = 0; return -12; } return faýl_ryçag;
}
int 망주소묶기(int faýl_ryçag, uint32_t salgy, unsigned 접속번호) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat) return -9;
    if (접속번호 > 65535 || (salgy && salgy != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&birikme_enjam))) && salgy != 0x7f000001)) return -99;
    ip_addr_t Internet_salgy; ip_addr_set_ip4_u32(&Internet_salgy, lwip_htonl(salgy));
    err_t 보조항목 = setir_maglumat->ýaz_kategoriýa == 1 ? tcp_bind(setir_maglumat->birikme_dolandyryş, &Internet_salgy, 접속번호) : udp_bind(setir_maglumat->전문제어, &Internet_salgy, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int faýl_ryçag) { 통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (setir_maglumat && setir_maglumat->birikme_dolandyryş) ip_set_option(setir_maglumat->birikme_dolandyryş, SOF_REUSEADDR); }
int 연결기다리기(int faýl_ryçag) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat || setir_maglumat->ýaz_kategoriýa != 1) return -9;
    if (setir_maglumat->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *geçiriş_dolandyryş_bökde = tcp_listen_with_backlog_and_err(setir_maglumat->birikme_dolandyryş, 4, &보조항목);
    if (!geçiriş_dolandyryş_bökde) return 오류번호(보조항목); setir_maglumat->birikme_dolandyryş = geçiriş_dolandyryş_bökde; setir_maglumat->수신창구 = 1; tcp_arg(geçiriş_dolandyryş_bökde, setir_maglumat); tcp_accept(geçiriş_dolandyryş_bökde, 연결받음); return 0;
}
int 망연결하기(int faýl_ryçag, uint32_t salgy, unsigned 접속번호) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat || setir_maglumat->ýaz_kategoriýa != 1) return -9;
    if (setir_maglumat->Hata) return setir_maglumat->Hata;
    if (setir_maglumat->연결됨) return 0;
    if (setir_maglumat->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !salgy) return -22;
    ip_addr_t Internet_salgy; ip_addr_set_ip4_u32(&Internet_salgy, lwip_htonl(salgy));
    setir_maglumat->deň_derejeli_düwün_salgy = salgy; setir_maglumat->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(setir_maglumat->birikme_dolandyryş, &Internet_salgy, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int faýl_ryçag) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat || !setir_maglumat->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].ýaz_kategoriýa == 1 && 통신끝점들[순번].대기중 == faýl_ryçag) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int faýl_ryçag, void *maglumat, unsigned 개수) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat || setir_maglumat->ýaz_kategoriýa != 1) return -9;
    if (!개수) return 0; if (!setir_maglumat->항목수) return setir_maglumat->Hata ? setir_maglumat->Hata : setir_maglumat->faýl_tamamla ? 0 : -11;
    if (개수 > setir_maglumat->항목수) 개수 = setir_maglumat->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)maglumat)[순번] = setir_maglumat->maglumat[setir_maglumat->맨앞]; setir_maglumat->맨앞 = (setir_maglumat->맨앞 + 1) % sizeof(setir_maglumat->maglumat); }
    setir_maglumat->항목수 -= 개수; if (setir_maglumat->birikme_dolandyryş) tcp_recved(setir_maglumat->birikme_dolandyryş, 개수); return 개수;
}
int 통신쓰기(int faýl_ryçag, const void *maglumat, unsigned 개수) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat || setir_maglumat->ýaz_kategoriýa != 1) return -9;
    if (setir_maglumat->Hata) return setir_maglumat->Hata; if (!setir_maglumat->birikme_dolandyryş || !setir_maglumat->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(setir_maglumat->birikme_dolandyryş)) 개수 = tcp_sndbuf(setir_maglumat->birikme_dolandyryş);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(setir_maglumat->birikme_dolandyryş, maglumat, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(setir_maglumat->birikme_dolandyryş); return 개수;
}
int 전문보내기(int faýl_ryçag, const void *maglumat, unsigned 개수, uint32_t salgy, unsigned 접속번호) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat || setir_maglumat->ýaz_kategoriýa != 2) return -9;
    if (개수 > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, maglumat, 개수); ip_addr_t Internet_salgy; ip_addr_set_ip4_u32(&Internet_salgy, lwip_htonl(salgy));
    err_t 보조항목 = udp_sendto(setir_maglumat->전문제어, 자료위치, &Internet_salgy, 접속번호); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int faýl_ryçag, void *maglumat, unsigned 개수) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat || setir_maglumat->ýaz_kategoriýa != 2) return -9;
    if (!setir_maglumat->항목수) return -11; unsigned 현재위치 = setir_maglumat->맨앞;
    if (개수 > setir_maglumat->길이목록[현재위치]) 개수 = setir_maglumat->길이목록[현재위치]; memcpy(maglumat, setir_maglumat->maglumat + 현재위치 * 512, 개수);
    setir_maglumat->상대창구번호 = setir_maglumat->접속번호들[현재위치]; setir_maglumat->deň_derejeli_düwün_salgy = setir_maglumat->주소목록[현재위치]; setir_maglumat->맨앞 = (현재위치 + 1) % 4; setir_maglumat->항목수--; return 개수;
}
unsigned 통신접속번호(int faýl_ryçag) { 통신끝점 *setir_maglumat = 얻기(faýl_ryçag); return !setir_maglumat ? 0 : setir_maglumat->birikme_dolandyryş ? setir_maglumat->birikme_dolandyryş->local_port : setir_maglumat->전문제어 ? setir_maglumat->전문제어->local_port : 0; }
unsigned 상대접속번호(int faýl_ryçag) { 통신끝점 *setir_maglumat = 얻기(faýl_ryçag); return setir_maglumat ? setir_maglumat->상대창구번호 : 0; }
uint32_t 상대통신주소(int faýl_ryçag) { 통신끝점 *setir_maglumat = 얻기(faýl_ryçag); return setir_maglumat ? setir_maglumat->deň_derejeli_düwün_salgy : 0; }
void ýap_Tor(int faýl_ryçag) {
    통신끝점 *setir_maglumat = 얻기(faýl_ryçag); if (!setir_maglumat) return;
    if (setir_maglumat->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].ýaz_kategoriýa && 통신끝점들[순번].대기중 == faýl_ryçag) ýap_Tor(순번);
    if (setir_maglumat->birikme_dolandyryş) {
        tcp_arg(setir_maglumat->birikme_dolandyryş, 0); if (setir_maglumat->수신창구) tcp_accept(setir_maglumat->birikme_dolandyryş, 0); else { tcp_recv(setir_maglumat->birikme_dolandyryş, 0); tcp_err(setir_maglumat->birikme_dolandyryş, 0); }
        if (tcp_close(setir_maglumat->birikme_dolandyryş) != ERR_OK) tcp_abort(setir_maglumat->birikme_dolandyryş);
    }
    if (setir_maglumat->전문제어) udp_remove(setir_maglumat->전문제어); setir_maglumat->ýaz_kategoriýa = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&birikme_enjam);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (기계저장기(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned nyşanyň_kody = 기계저장기(보조장치 + 0x40) & 255;
        if (nyşanyň_kody == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (birikme_enjam.input(자료위치, &birikme_enjam) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (nyşanyň_kody == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (nyşanyň_kody != 220 && nyşanyň_kody != 221) 수신오류 = 1; nyşanyň_kody = nyşanyň_kody == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = nyşanyň_kody; else 수신오류 = 1;
        }
    }
    netif_poll(&birikme_enjam); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (기계저장기(보조장치 + 0x54) & 0x20); 처리한도++) {
        기계저장기(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Düzümler·조회는 lwIP의 hakyky_maglumat 인터페이스와 tamamla_utuk 표를 사용한다. */
uint32_t 망상태읽기(unsigned girizmeklik_baha, unsigned indeks) {
    if(girizmeklik_baha==20)return 유선사용;
    if(girizmeklik_baha==21)return 준비됨&&netif_is_link_up(&birikme_enjam);
    if(girizmeklik_baha==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&girizmeklik_baha>=4&&girizmeklik_baha<=8)return 유선망집계(girizmeklik_baha-4);
    if (girizmeklik_baha == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&birikme_enjam)));
    if (girizmeklik_baha == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&birikme_enjam)));
    if (girizmeklik_baha == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&birikme_enjam)));
    if (girizmeklik_baha == 3) return netif_is_up(&birikme_enjam) != 0;
    if (girizmeklik_baha == 4) return 받은전문수;
    if (girizmeklik_baha == 5) return 보낸전문수;
    if (girizmeklik_baha == 6) return 받은바이트수;
    if (girizmeklik_baha == 7) return 보낸바이트수;
    if (girizmeklik_baha == 8) return 버린전문수;
    if (girizmeklik_baha == 9) return 송신개수;
    if (indeks >= 32) return 0;
    통신끝점 *tamamla_utuk = &통신끝점들[indeks];
    if (girizmeklik_baha == 10) return tamamla_utuk->ýaz_kategoriýa;
    if (!tamamla_utuk->ýaz_kategoriýa) return 0;
    if (girizmeklik_baha == 11) return 통신접속번호(indeks);
    if (girizmeklik_baha == 12) return tamamla_utuk->deň_derejeli_düwün_salgy;
    if (girizmeklik_baha == 13) return tamamla_utuk->상대창구번호;
    if (girizmeklik_baha == 14) return tamamla_utuk->수신창구 ? 1 : tamamla_utuk->faýl_tamamla ? 3 : tamamla_utuk->Hata ? 4 : tamamla_utuk->연결됨 ? 2 : 0;
    if (girizmeklik_baha == 15) return tamamla_utuk->항목수;
    if (girizmeklik_baha == 16) {
        const ip_addr_t *salgy = tamamla_utuk->ýaz_kategoriýa == 1 && tamamla_utuk->birikme_dolandyryş ? &tamamla_utuk->birikme_dolandyryş->local_ip :
            tamamla_utuk->ýaz_kategoriýa == 2 && tamamla_utuk->전문제어 ? &tamamla_utuk->전문제어->local_ip : 0;
        return salgy ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(salgy))) : 0;
    }
    return 0;
}

int düz_Tor(unsigned iş, uint32_t salgy, uint32_t örtük_baha, uint32_t şlýuz_baha) {
    if (!준비됨) return -100;
    if (iş == 1) { netif_set_up(&birikme_enjam); return 0; }
    if (iş == 2) { netif_set_down(&birikme_enjam); return 0; }
    if (iş != 0) return -22;
    /* 유니캐스트 IPv4, 연속 örtük_baha, 같은 망의 선택적 öňünden_kabul_edilen_baha şlýuz_baha. */
    uint32_t 뒤집은가림 = ~örtük_baha;
    if (!örtük_baha || (뒤집은가림 & (뒤집은가림 + 1)) || !salgy || (salgy >> 24) == 127 ||
        (salgy >> 24) == 0 || (salgy >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(salgy & 뒤집은가림) || (salgy & 뒤집은가림) == 뒤집은가림)) ||
        (şlýuz_baha && ((şlýuz_baha & örtük_baha) != (salgy & örtük_baha) || şlýuz_baha == salgy || (şlýuz_baha >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(şlýuz_baha & 뒤집은가림) || (şlýuz_baha & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 salgy 변경으로 몰래 끊지 않는다. */
    for (unsigned indeks = 0; indeks < 32; indeks++) if (통신끝점들[indeks].ýaz_kategoriýa &&
        !(통신끝점들[indeks].수신창구 && 통신끝점들[indeks].birikme_dolandyryş && ip_addr_isany(&통신끝점들[indeks].birikme_dolandyryş->local_ip))) return -16;
    if(유선사용)dhcp_stop(&birikme_enjam);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(salgy)); ip4_addr_set_u32(&새가림, lwip_htonl(örtük_baha)); ip4_addr_set_u32(&새관문, lwip_htonl(şlýuz_baha));
    netif_set_addr(&birikme_enjam, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *tamamla_utuk, struct pbuf *maglumat, const ip_addr_t *salgy) {
    (void)인수; (void)tamamla_utuk;
    unsigned char 머리[20], jogap_bermek[16];
    if (응답상태 != -11 || maglumat->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(salgy))) != 시험주소 || pbuf_copy_partial(maglumat, 머리, 20, 0) != 20) return 0;
    unsigned At_ölçegi_üýtget = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || At_ölçegi_üýtget < 20 || maglumat->tot_len < At_ölçegi_üýtget + 16 ||
        pbuf_copy_partial(maglumat, jogap_bermek, 16, At_ölçegi_üýtget) != 16 || jogap_bermek[0] || jogap_bermek[1] ||
        (((unsigned)jogap_bermek[4] << 8) | jogap_bermek[5]) != 시험식별자 ||
        (((unsigned)jogap_bermek[6] << 8) | jogap_bermek[7]) != 시험순서 ||
        jogap_bermek[8] != 'J' || jogap_bermek[9] != 'K' || jogap_bermek[10] != 'O' || jogap_bermek[11] != 'S' ||
        (((uint32_t)jogap_bermek[12] << 24) | ((uint32_t)jogap_bermek[13] << 16) | ((uint32_t)jogap_bermek[14] << 8) | jogap_bermek[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(maglumat, At_ölçegi_üýtget)) return 0;
    if (inet_chksum_pbuf(maglumat)) { pbuf_add_header(maglumat, At_ölçegi_üýtget); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(maglumat); return 1;
}
int 응답시험시작(uint32_t salgy, unsigned tertip_baha) {
    if (!준비됨 || !netif_is_up(&birikme_enjam)) return -100;
    if (!salgy || (salgy >> 28) >= 14 || salgy == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = salgy; 시험순서 = tertip_baha & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char maglumat[32] = {8,0,0,0};
    maglumat[4] = 시험식별자 >> 8; maglumat[5] = 시험식별자; maglumat[6] = 시험순서 >> 8; maglumat[7] = 시험순서;
    maglumat[8]='J'; maglumat[9]='K'; maglumat[10]='O'; maglumat[11]='S';
    maglumat[12]=시험시각 >> 24; maglumat[13]=시험시각 >> 16; maglumat[14]=시험시각 >> 8; maglumat[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(maglumat); 자리++) maglumat[자리] = 자리;
    uint16_t 확인합 = inet_chksum(maglumat, sizeof(maglumat)); memcpy(maglumat + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(maglumat), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, maglumat, sizeof(maglumat)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(salgy));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned girizmeklik_baha) {
    통신망살피기();
    return girizmeklik_baha == 0 ? 응답상태 : girizmeklik_baha == 1 ? (int)응답시간 : girizmeklik_baha == 2 ? (int)응답차례 : -22;
}
