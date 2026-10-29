#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Mtandao_Mpororo.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../kwa_mbali_thamani/kwa_mbali_thamani.h"
#include "kuwekwa_waya_Mtandao.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define mashine_sajili(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif muunganisho_kifaa;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, 받은바이트수, 보낸바이트수, 버린전문수;
typedef struct {
    int aina_kategoria, 수신창구, teknolojia_ya_maelezo_inayosubiri, 연결됨, faili_tamatia, kosa;
    struct tcp_pcb *muunganisho_udhibiti;
    struct udp_pcb *전문제어;
    unsigned mbele_ingizo, 항목수;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], kompyuta_rika_anwani;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *pata_thamani(int faili_kishiko) { return faili_kishiko >= 0 && faili_kishiko < 32 && 통신끝점들[faili_kishiko].aina_kategoria ? &통신끝점들[faili_kishiko] : 0; }
static int 예약하기(int aina_kategoria) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].aina_kategoria) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].aina_kategoria = aina_kategoria; 통신끝점들[순번].teknolojia_ya_maelezo_inayosubiri = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned msimbo_wa_kibambo) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = msimbo_wa_kibambo; }
static err_t 출력결과(struct netif *개수, struct pbuf *자료위치, const ip4_addr_t *anwani) {
    (void)개수; (void)anwani;
    if (자료위치->tot_len > 1500 || 송신개수 + 2 * 자료위치->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        unsigned msimbo_wa_kibambo = ((unsigned char *)다음위치->payload)[순번];
        if (msimbo_wa_kibambo == 192 || msimbo_wa_kibambo == 219) { 내보내기(219); 내보내기(msimbo_wa_kibambo == 192 ? 220 : 221); } else 내보내기(msimbo_wa_kibambo);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += 자료위치->tot_len; return ERR_OK;
}
static err_t Andaa_muda_wa_kuendesha_lugha_ya_kawaida(struct netif *개수) { 개수->name[0] = 's'; 개수->name[1] = 'l'; 개수->mtu = 1500; 개수->output = 출력결과; return ERR_OK; }
void Andaa_Mtandao(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    mashine_sajili(보조장치 + 4) |= 1; mashine_sajili(보조장치 + 0x60) = 0; mashine_sajili(보조장치 + 0x44) = 0;
    mashine_sajili(보조장치 + 0x48) = 0xc6; mashine_sajili(보조장치 + 0x4c) = 3; mashine_sajili(보조장치 + 0x68) = 270; mashine_sajili(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Anwani_tovuti, biti_barakoa, kichanganishi_mtandao_anwani;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Anwani_tovuti, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&biti_barakoa, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&kichanganishi_mtandao_anwani, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&muunganisho_kifaa, &Anwani_tovuti, &biti_barakoa, &kichanganishi_mtandao_anwani, 0, 유선사용?Andaa_kuwekwa_waya_Mtandao:Andaa_muda_wa_kuendesha_lugha_ya_kawaida, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&muunganisho_kifaa); netif_set_up(&muunganisho_kifaa);if(!유선사용)netif_set_link_up(&muunganisho_kifaa); 준비됨 = 1;
    Andaa_kwa_mbali();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *urushaji_udhibiti_zuia, struct pbuf *자료위치, err_t kosa) {
    통신끝점 *tungo_data = 부가인수; (void)urushaji_udhibiti_zuia; (void)kosa;
    if (!자료위치) { tungo_data->faili_tamatia = 1; return ERR_OK; }
    if (자료위치->tot_len > sizeof(tungo_data->data) - tungo_data->항목수) return ERR_MEM;
    unsigned 현재위치 = (tungo_data->mbele_ingizo + tungo_data->항목수) % sizeof(tungo_data->data);
    for (struct pbuf *다음위치 = 자료위치; 다음위치; 다음위치 = 다음위치->next) for (unsigned 순번 = 0; 순번 < 다음위치->len; 순번++) {
        tungo_data->data[현재위치] = ((unsigned char *)다음위치->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(tungo_data->data);
    }
    tungo_data->항목수 += 자료위치->tot_len; pbuf_free(자료위치); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t kosa) { 통신끝점 *tungo_data = 부가인수; tungo_data->muunganisho_udhibiti = 0; tungo_data->kosa = 오류번호(kosa); }
static void 되부름목록(통신끝점 *tungo_data) { tcp_arg(tungo_data->muunganisho_udhibiti, tungo_data); tcp_recv(tungo_data->muunganisho_udhibiti, 수신됨); tcp_err(tungo_data->muunganisho_udhibiti, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *urushaji_udhibiti_zuia, err_t kosa) {
    통신끝점 *tungo_data = 부가인수; (void)urushaji_udhibiti_zuia; if (kosa) tungo_data->kosa = 오류번호(kosa); else tungo_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *urushaji_udhibiti_zuia, err_t kosa) {
    통신끝점 *부모항목 = 부가인수; if (kosa) return kosa;
    int faili_kishiko = 예약하기(1); if (faili_kishiko < 0) return ERR_MEM;
    통신끝점 *tungo_data = &통신끝점들[faili_kishiko]; tungo_data->muunganisho_udhibiti = urushaji_udhibiti_zuia; tungo_data->연결됨 = 1; tungo_data->teknolojia_ya_maelezo_inayosubiri = (int)(부모항목 - 통신끝점들);
    tungo_data->kompyuta_rika_anwani = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&urushaji_udhibiti_zuia->remote_ip))); tungo_data->상대창구번호 = urushaji_udhibiti_zuia->remote_port;
    되부름목록(tungo_data); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *urushaji_udhibiti_zuia, struct pbuf *자료위치, const ip_addr_t *anwani, u16_t namba_ya_kituo) {
    통신끝점 *tungo_data = 부가인수; (void)urushaji_udhibiti_zuia;
    if (tungo_data->항목수 < 4 && 자료위치->tot_len <= 512) {
        unsigned 자리 = (tungo_data->mbele_ingizo + tungo_data->항목수) % 4;
        pbuf_copy_partial(자료위치, tungo_data->data + 자리 * 512, 자료위치->tot_len, 0);
        tungo_data->길이목록[자리] = 자료위치->tot_len; tungo_data->접속번호들[자리] = namba_ya_kituo;
        tungo_data->주소목록[자리] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(anwani))); tungo_data->항목수++;
    }
    pbuf_free(자료위치);
}
int 통신끝점만들기(int aina_kategoria) {
    if (!준비됨) return -100;
    if (aina_kategoria != 1 && aina_kategoria != 2) return -93;
    int faili_kishiko = 예약하기(aina_kategoria); if (faili_kishiko < 0) return faili_kishiko;
    통신끝점 *tungo_data = &통신끝점들[faili_kishiko];
    if (aina_kategoria == 1) { tungo_data->muunganisho_udhibiti = tcp_new(); if (tungo_data->muunganisho_udhibiti) 되부름목록(tungo_data); }
    else { tungo_data->전문제어 = udp_new(); if (tungo_data->전문제어) udp_recv(tungo_data->전문제어, 전문, tungo_data); }
    if (!tungo_data->muunganisho_udhibiti && !tungo_data->전문제어) { tungo_data->aina_kategoria = 0; return -12; } return faili_kishiko;
}
int 망주소묶기(int faili_kishiko, uint32_t anwani, unsigned namba_ya_kituo) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data) return -9;
    if (namba_ya_kituo > 65535 || (anwani && anwani != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&muunganisho_kifaa))) && anwani != 0x7f000001)) return -99;
    ip_addr_t Anwani_tovuti; ip_addr_set_ip4_u32(&Anwani_tovuti, lwip_htonl(anwani));
    err_t 보조항목 = tungo_data->aina_kategoria == 1 ? tcp_bind(tungo_data->muunganisho_udhibiti, &Anwani_tovuti, namba_ya_kituo) : udp_bind(tungo_data->전문제어, &Anwani_tovuti, namba_ya_kituo); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int faili_kishiko) { 통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (tungo_data && tungo_data->muunganisho_udhibiti) ip_set_option(tungo_data->muunganisho_udhibiti, SOF_REUSEADDR); }
int 연결기다리기(int faili_kishiko) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data || tungo_data->aina_kategoria != 1) return -9;
    if (tungo_data->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *urushaji_udhibiti_zuia = tcp_listen_with_backlog_and_err(tungo_data->muunganisho_udhibiti, 4, &보조항목);
    if (!urushaji_udhibiti_zuia) return 오류번호(보조항목); tungo_data->muunganisho_udhibiti = urushaji_udhibiti_zuia; tungo_data->수신창구 = 1; tcp_arg(urushaji_udhibiti_zuia, tungo_data); tcp_accept(urushaji_udhibiti_zuia, 연결받음); return 0;
}
int 망연결하기(int faili_kishiko, uint32_t anwani, unsigned namba_ya_kituo) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data || tungo_data->aina_kategoria != 1) return -9;
    if (tungo_data->kosa) return tungo_data->kosa;
    if (tungo_data->연결됨) return 0;
    if (tungo_data->상대창구번호) return -115;
    if (!namba_ya_kituo || namba_ya_kituo > 65535 || !anwani) return -22;
    ip_addr_t Anwani_tovuti; ip_addr_set_ip4_u32(&Anwani_tovuti, lwip_htonl(anwani));
    tungo_data->kompyuta_rika_anwani = anwani; tungo_data->상대창구번호 = namba_ya_kituo;
    err_t 보조항목 = tcp_connect(tungo_data->muunganisho_udhibiti, &Anwani_tovuti, namba_ya_kituo, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int faili_kishiko) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data || !tungo_data->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].aina_kategoria == 1 && 통신끝점들[순번].teknolojia_ya_maelezo_inayosubiri == faili_kishiko) { 통신끝점들[순번].teknolojia_ya_maelezo_inayosubiri = -1; return 순번; }
    return -11;
}
int 통신읽기(int faili_kishiko, void *data, unsigned 개수) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data || tungo_data->aina_kategoria != 1) return -9;
    if (!개수) return 0; if (!tungo_data->항목수) return tungo_data->kosa ? tungo_data->kosa : tungo_data->faili_tamatia ? 0 : -11;
    if (개수 > tungo_data->항목수) 개수 = tungo_data->항목수;
    for (unsigned 순번 = 0; 순번 < 개수; 순번++) { ((unsigned char *)data)[순번] = tungo_data->data[tungo_data->mbele_ingizo]; tungo_data->mbele_ingizo = (tungo_data->mbele_ingizo + 1) % sizeof(tungo_data->data); }
    tungo_data->항목수 -= 개수; if (tungo_data->muunganisho_udhibiti) tcp_recved(tungo_data->muunganisho_udhibiti, 개수); return 개수;
}
int 통신쓰기(int faili_kishiko, const void *data, unsigned 개수) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data || tungo_data->aina_kategoria != 1) return -9;
    if (tungo_data->kosa) return tungo_data->kosa; if (!tungo_data->muunganisho_udhibiti || !tungo_data->연결됨) return -107;
    if (!개수) return 0; if (개수 > tcp_sndbuf(tungo_data->muunganisho_udhibiti)) 개수 = tcp_sndbuf(tungo_data->muunganisho_udhibiti);
    if (!개수) return -11; if (개수 > 1024) 개수 = 1024;
    err_t 보조항목 = tcp_write(tungo_data->muunganisho_udhibiti, data, 개수, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(tungo_data->muunganisho_udhibiti); return 개수;
}
int 전문보내기(int faili_kishiko, const void *data, unsigned 개수, uint32_t anwani, unsigned namba_ya_kituo) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data || tungo_data->aina_kategoria != 2) return -9;
    if (개수 > 512) return -90; if (!namba_ya_kituo || namba_ya_kituo > 65535) return -22;
    struct pbuf *자료위치 = pbuf_alloc(PBUF_TRANSPORT, 개수, PBUF_RAM); if (!자료위치) return -11;
    pbuf_take(자료위치, data, 개수); ip_addr_t Anwani_tovuti; ip_addr_set_ip4_u32(&Anwani_tovuti, lwip_htonl(anwani));
    err_t 보조항목 = udp_sendto(tungo_data->전문제어, 자료위치, &Anwani_tovuti, namba_ya_kituo); pbuf_free(자료위치); return 보조항목 ? 오류번호(보조항목) : (int)개수;
}
int 전문받기(int faili_kishiko, void *data, unsigned 개수) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data || tungo_data->aina_kategoria != 2) return -9;
    if (!tungo_data->항목수) return -11; unsigned 현재위치 = tungo_data->mbele_ingizo;
    if (개수 > tungo_data->길이목록[현재위치]) 개수 = tungo_data->길이목록[현재위치]; memcpy(data, tungo_data->data + 현재위치 * 512, 개수);
    tungo_data->상대창구번호 = tungo_data->접속번호들[현재위치]; tungo_data->kompyuta_rika_anwani = tungo_data->주소목록[현재위치]; tungo_data->mbele_ingizo = (현재위치 + 1) % 4; tungo_data->항목수--; return 개수;
}
unsigned Mtandao_namba_ya_kituo(int faili_kishiko) { 통신끝점 *tungo_data = pata_thamani(faili_kishiko); return !tungo_data ? 0 : tungo_data->muunganisho_udhibiti ? tungo_data->muunganisho_udhibiti->local_port : tungo_data->전문제어 ? tungo_data->전문제어->local_port : 0; }
unsigned kompyuta_rika_namba_ya_kituo(int faili_kishiko) { 통신끝점 *tungo_data = pata_thamani(faili_kishiko); return tungo_data ? tungo_data->상대창구번호 : 0; }
uint32_t 상대통신주소(int faili_kishiko) { 통신끝점 *tungo_data = pata_thamani(faili_kishiko); return tungo_data ? tungo_data->kompyuta_rika_anwani : 0; }
void funga_Mtandao(int faili_kishiko) {
    통신끝점 *tungo_data = pata_thamani(faili_kishiko); if (!tungo_data) return;
    if (tungo_data->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].aina_kategoria && 통신끝점들[순번].teknolojia_ya_maelezo_inayosubiri == faili_kishiko) funga_Mtandao(순번);
    if (tungo_data->muunganisho_udhibiti) {
        tcp_arg(tungo_data->muunganisho_udhibiti, 0); if (tungo_data->수신창구) tcp_accept(tungo_data->muunganisho_udhibiti, 0); else { tcp_recv(tungo_data->muunganisho_udhibiti, 0); tcp_err(tungo_data->muunganisho_udhibiti, 0); }
        if (tcp_close(tungo_data->muunganisho_udhibiti) != ERR_OK) tcp_abort(tungo_data->muunganisho_udhibiti);
    }
    if (tungo_data->전문제어) udp_remove(tungo_data->전문제어); tungo_data->aina_kategoria = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&muunganisho_kifaa);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (mashine_sajili(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned msimbo_wa_kibambo = mashine_sajili(보조장치 + 0x40) & 255;
        if (msimbo_wa_kibambo == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *자료위치 = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (자료위치) { 받은전문수++; 받은바이트수 += 수신사용량; pbuf_take(자료위치, 수신자료, 수신사용량); if (muunganisho_kifaa.input(자료위치, &muunganisho_kifaa) != ERR_OK) { 버린전문수++; pbuf_free(자료위치); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (msimbo_wa_kibambo == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (msimbo_wa_kibambo != 220 && msimbo_wa_kibambo != 221) 수신오류 = 1; msimbo_wa_kibambo = msimbo_wa_kibambo == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = msimbo_wa_kibambo; else 수신오류 = 1;
        }
    }
    netif_poll(&muunganisho_kifaa); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (mashine_sajili(보조장치 + 0x54) & 0x20); 처리한도++) {
        mashine_sajili(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Mipangilio·조회는 lwIP의 halisi_data 인터페이스와 tamatia_pointi 표를 사용한다. */
uint32_t 망상태읽기(unsigned ingizo_thamani, unsigned kielezo) {
    if(ingizo_thamani==20)return 유선사용;
    if(ingizo_thamani==21)return 준비됨&&netif_is_link_up(&muunganisho_kifaa);
    if(ingizo_thamani==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&ingizo_thamani>=4&&ingizo_thamani<=8)return 유선망집계(ingizo_thamani-4);
    if (ingizo_thamani == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&muunganisho_kifaa)));
    if (ingizo_thamani == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&muunganisho_kifaa)));
    if (ingizo_thamani == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&muunganisho_kifaa)));
    if (ingizo_thamani == 3) return netif_is_up(&muunganisho_kifaa) != 0;
    if (ingizo_thamani == 4) return 받은전문수;
    if (ingizo_thamani == 5) return 보낸전문수;
    if (ingizo_thamani == 6) return 받은바이트수;
    if (ingizo_thamani == 7) return 보낸바이트수;
    if (ingizo_thamani == 8) return 버린전문수;
    if (ingizo_thamani == 9) return 송신개수;
    if (kielezo >= 32) return 0;
    통신끝점 *tamatia_pointi = &통신끝점들[kielezo];
    if (ingizo_thamani == 10) return tamatia_pointi->aina_kategoria;
    if (!tamatia_pointi->aina_kategoria) return 0;
    if (ingizo_thamani == 11) return Mtandao_namba_ya_kituo(kielezo);
    if (ingizo_thamani == 12) return tamatia_pointi->kompyuta_rika_anwani;
    if (ingizo_thamani == 13) return tamatia_pointi->상대창구번호;
    if (ingizo_thamani == 14) return tamatia_pointi->수신창구 ? 1 : tamatia_pointi->faili_tamatia ? 3 : tamatia_pointi->kosa ? 4 : tamatia_pointi->연결됨 ? 2 : 0;
    if (ingizo_thamani == 15) return tamatia_pointi->항목수;
    if (ingizo_thamani == 16) {
        const ip_addr_t *anwani = tamatia_pointi->aina_kategoria == 1 && tamatia_pointi->muunganisho_udhibiti ? &tamatia_pointi->muunganisho_udhibiti->local_ip :
            tamatia_pointi->aina_kategoria == 2 && tamatia_pointi->전문제어 ? &tamatia_pointi->전문제어->local_ip : 0;
        return anwani ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(anwani))) : 0;
    }
    return 0;
}

int sanidi_Mtandao(unsigned Kitendo, uint32_t anwani, uint32_t barakoa_thamani, uint32_t kichanganishi_mtandao_thamani) {
    if (!준비됨) return -100;
    if (Kitendo == 1) { netif_set_up(&muunganisho_kifaa); return 0; }
    if (Kitendo == 2) { netif_set_down(&muunganisho_kifaa); return 0; }
    if (Kitendo != 0) return -22;
    /* 유니캐스트 IPv4, 연속 barakoa_thamani, 같은 망의 선택적 hali_ya_chaguo_msingi kichanganishi_mtandao_thamani. */
    uint32_t 뒤집은가림 = ~barakoa_thamani;
    if (!barakoa_thamani || (뒤집은가림 & (뒤집은가림 + 1)) || !anwani || (anwani >> 24) == 127 ||
        (anwani >> 24) == 0 || (anwani >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(anwani & 뒤집은가림) || (anwani & 뒤집은가림) == 뒤집은가림)) ||
        (kichanganishi_mtandao_thamani && ((kichanganishi_mtandao_thamani & barakoa_thamani) != (anwani & barakoa_thamani) || kichanganishi_mtandao_thamani == anwani || (kichanganishi_mtandao_thamani >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(kichanganishi_mtandao_thamani & 뒤집은가림) || (kichanganishi_mtandao_thamani & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 anwani 변경으로 몰래 끊지 않는다. */
    for (unsigned kielezo = 0; kielezo < 32; kielezo++) if (통신끝점들[kielezo].aina_kategoria &&
        !(통신끝점들[kielezo].수신창구 && 통신끝점들[kielezo].muunganisho_udhibiti && ip_addr_isany(&통신끝점들[kielezo].muunganisho_udhibiti->local_ip))) return -16;
    if(유선사용)dhcp_stop(&muunganisho_kifaa);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(anwani)); ip4_addr_set_u32(&새가림, lwip_htonl(barakoa_thamani)); ip4_addr_set_u32(&새관문, lwip_htonl(kichanganishi_mtandao_thamani));
    netif_set_addr(&muunganisho_kifaa, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *tamatia_pointi, struct pbuf *data, const ip_addr_t *anwani) {
    (void)인수; (void)tamatia_pointi;
    unsigned char 머리[20], jibu[16];
    if (응답상태 != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(anwani))) != 시험주소 || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned kichwa_panga_ukubwa = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || kichwa_panga_ukubwa < 20 || data->tot_len < kichwa_panga_ukubwa + 16 ||
        pbuf_copy_partial(data, jibu, 16, kichwa_panga_ukubwa) != 16 || jibu[0] || jibu[1] ||
        (((unsigned)jibu[4] << 8) | jibu[5]) != 시험식별자 ||
        (((unsigned)jibu[6] << 8) | jibu[7]) != 시험순서 ||
        jibu[8] != 'J' || jibu[9] != 'K' || jibu[10] != 'O' || jibu[11] != 'S' ||
        (((uint32_t)jibu[12] << 24) | ((uint32_t)jibu[13] << 16) | ((uint32_t)jibu[14] << 8) | jibu[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, kichwa_panga_ukubwa)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, kichwa_panga_ukubwa); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(data); return 1;
}
int 응답시험시작(uint32_t anwani, unsigned mpangilio_thamani) {
    if (!준비됨 || !netif_is_up(&muunganisho_kifaa)) return -100;
    if (!anwani || (anwani >> 28) >= 14 || anwani == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = anwani; 시험순서 = mpangilio_thamani & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = 시험식별자 >> 8; data[5] = 시험식별자; data[6] = 시험순서 >> 8; data[7] = 시험순서;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=시험시각 >> 24; data[13]=시험시각 >> 16; data[14]=시험시각 >> 8; data[15]=시험시각;
    for (unsigned 자리 = 16; 자리 < sizeof(data); 자리++) data[자리] = 자리;
    uint16_t uthibitishaji_jumla = inet_chksum(data, sizeof(data)); memcpy(data + 2, &uthibitishaji_jumla, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, data, sizeof(data)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(anwani));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned ingizo_thamani) {
    통신망살피기();
    return ingizo_thamani == 0 ? 응답상태 : ingizo_thamani == 1 ? (int)응답시간 : ingizo_thamani == 2 ? (int)응답차례 : -22;
}
