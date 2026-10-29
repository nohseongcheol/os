#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "lìonra_stac.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../cian_VALUE/cian_VALUE.h"
#include "유선망.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define inneal_clàraich(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif ceangal_uidheam;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_baidht_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_roinn_seòrsa, 수신창구, 대기중, 연결됨, faidhle_crìochnaich, Mearachd;
    struct tcp_pcb *ceangal_smachd;
    struct udp_pcb *전문제어;
    unsigned 맨앞, cur_a_steach_COUNT;
    unsigned char dàta[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], seise_ADDRESS;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int faidhle_làmhrachan) { return faidhle_làmhrachan >= 0 && faidhle_làmhrachan < 32 && 통신끝점들[faidhle_làmhrachan].TYPE_roinn_seòrsa ? &통신끝점들[faidhle_làmhrachan] : 0; }
static int 예약하기(int TYPE_roinn_seòrsa) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_roinn_seòrsa) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_roinn_seòrsa = TYPE_roinn_seòrsa; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned còd_a_charactair) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = còd_a_charactair; }
static err_t 출력결과(struct netif *nì_COUNT, struct pbuf *dàta_suidhich, const ip4_addr_t *ADDRESS) {
    (void)nì_COUNT; (void)ADDRESS;
    if (dàta_suidhich->tot_len > 1500 || 송신개수 + 2 * dàta_suidhich->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *air_adhart_OFFSET = dàta_suidhich; air_adhart_OFFSET; air_adhart_OFFSET = air_adhart_OFFSET->next) for (unsigned 순번 = 0; 순번 < air_adhart_OFFSET->len; 순번++) {
        unsigned còd_a_charactair = ((unsigned char *)air_adhart_OFFSET->payload)[순번];
        if (còd_a_charactair == 192 || còd_a_charactair == 219) { 내보내기(219); 내보내기(còd_a_charactair == 192 ? 220 : 221); } else 내보내기(còd_a_charactair);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += dàta_suidhich->tot_len; return ERR_OK;
}
static err_t Ullaich_Common_Language_Runtime(struct netif *nì_COUNT) { nì_COUNT->name[0] = 's'; nì_COUNT->name[1] = 'l'; nì_COUNT->mtu = 1500; nì_COUNT->output = 출력결과; return ERR_OK; }
void Ullaich_lìonra(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    inneal_clàraich(보조장치 + 4) |= 1; inneal_clàraich(보조장치 + 0x60) = 0; inneal_clàraich(보조장치 + 0x44) = 0;
    inneal_clàraich(보조장치 + 0x48) = 0xc6; inneal_clàraich(보조장치 + 0x4c) = 3; inneal_clàraich(보조장치 + 0x68) = 270; inneal_clàraich(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Seòladh_eadar_lìn, 가림값, 관문주소;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Seòladh_eadar_lìn, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&가림값, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&관문주소, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&ceangal_uidheam, &Seòladh_eadar_lìn, &가림값, &관문주소, 0, 유선사용?유선망준비:Ullaich_Common_Language_Runtime, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&ceangal_uidheam); netif_set_up(&ceangal_uidheam);if(!유선사용)netif_set_link_up(&ceangal_uidheam); 준비됨 = 1;
    Ullaich_cian();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *dàta_suidhich, err_t Mearachd) {
    통신끝점 *sreang_dàta = 부가인수; (void)통신제어블록; (void)Mearachd;
    if (!dàta_suidhich) { sreang_dàta->faidhle_crìochnaich = 1; return ERR_OK; }
    if (dàta_suidhich->tot_len > sizeof(sreang_dàta->dàta) - sreang_dàta->cur_a_steach_COUNT) return ERR_MEM;
    unsigned 현재위치 = (sreang_dàta->맨앞 + sreang_dàta->cur_a_steach_COUNT) % sizeof(sreang_dàta->dàta);
    for (struct pbuf *air_adhart_OFFSET = dàta_suidhich; air_adhart_OFFSET; air_adhart_OFFSET = air_adhart_OFFSET->next) for (unsigned 순번 = 0; 순번 < air_adhart_OFFSET->len; 순번++) {
        sreang_dàta->dàta[현재위치] = ((unsigned char *)air_adhart_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(sreang_dàta->dàta);
    }
    sreang_dàta->cur_a_steach_COUNT += dàta_suidhich->tot_len; pbuf_free(dàta_suidhich); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Mearachd) { 통신끝점 *sreang_dàta = 부가인수; sreang_dàta->ceangal_smachd = 0; sreang_dàta->Mearachd = 오류번호(Mearachd); }
static void 되부름목록(통신끝점 *sreang_dàta) { tcp_arg(sreang_dàta->ceangal_smachd, sreang_dàta); tcp_recv(sreang_dàta->ceangal_smachd, 수신됨); tcp_err(sreang_dàta->ceangal_smachd, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t Mearachd) {
    통신끝점 *sreang_dàta = 부가인수; (void)통신제어블록; if (Mearachd) sreang_dàta->Mearachd = 오류번호(Mearachd); else sreang_dàta->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t Mearachd) {
    통신끝점 *부모항목 = 부가인수; if (Mearachd) return Mearachd;
    int faidhle_làmhrachan = 예약하기(1); if (faidhle_làmhrachan < 0) return ERR_MEM;
    통신끝점 *sreang_dàta = &통신끝점들[faidhle_làmhrachan]; sreang_dàta->ceangal_smachd = 통신제어블록; sreang_dàta->연결됨 = 1; sreang_dàta->대기중 = (int)(부모항목 - 통신끝점들);
    sreang_dàta->seise_ADDRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); sreang_dàta->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(sreang_dàta); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *dàta_suidhich, const ip_addr_t *ADDRESS, u16_t 접속번호) {
    통신끝점 *sreang_dàta = 부가인수; (void)통신제어블록;
    if (sreang_dàta->cur_a_steach_COUNT < 4 && dàta_suidhich->tot_len <= 512) {
        unsigned suidhich_INDEX = (sreang_dàta->맨앞 + sreang_dàta->cur_a_steach_COUNT) % 4;
        pbuf_copy_partial(dàta_suidhich, sreang_dàta->dàta + suidhich_INDEX * 512, dàta_suidhich->tot_len, 0);
        sreang_dàta->길이목록[suidhich_INDEX] = dàta_suidhich->tot_len; sreang_dàta->접속번호들[suidhich_INDEX] = 접속번호;
        sreang_dàta->주소목록[suidhich_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))); sreang_dàta->cur_a_steach_COUNT++;
    }
    pbuf_free(dàta_suidhich);
}
int 통신끝점만들기(int TYPE_roinn_seòrsa) {
    if (!준비됨) return -100;
    if (TYPE_roinn_seòrsa != 1 && TYPE_roinn_seòrsa != 2) return -93;
    int faidhle_làmhrachan = 예약하기(TYPE_roinn_seòrsa); if (faidhle_làmhrachan < 0) return faidhle_làmhrachan;
    통신끝점 *sreang_dàta = &통신끝점들[faidhle_làmhrachan];
    if (TYPE_roinn_seòrsa == 1) { sreang_dàta->ceangal_smachd = tcp_new(); if (sreang_dàta->ceangal_smachd) 되부름목록(sreang_dàta); }
    else { sreang_dàta->전문제어 = udp_new(); if (sreang_dàta->전문제어) udp_recv(sreang_dàta->전문제어, 전문, sreang_dàta); }
    if (!sreang_dàta->ceangal_smachd && !sreang_dàta->전문제어) { sreang_dàta->TYPE_roinn_seòrsa = 0; return -12; } return faidhle_làmhrachan;
}
int 망주소묶기(int faidhle_làmhrachan, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta) return -9;
    if (접속번호 > 65535 || (ADDRESS && ADDRESS != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ceangal_uidheam))) && ADDRESS != 0x7f000001)) return -99;
    ip_addr_t Seòladh_eadar_lìn; ip_addr_set_ip4_u32(&Seòladh_eadar_lìn, lwip_htonl(ADDRESS));
    err_t 보조항목 = sreang_dàta->TYPE_roinn_seòrsa == 1 ? tcp_bind(sreang_dàta->ceangal_smachd, &Seòladh_eadar_lìn, 접속번호) : udp_bind(sreang_dàta->전문제어, &Seòladh_eadar_lìn, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int faidhle_làmhrachan) { 통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (sreang_dàta && sreang_dàta->ceangal_smachd) ip_set_option(sreang_dàta->ceangal_smachd, SOF_REUSEADDR); }
int 연결기다리기(int faidhle_làmhrachan) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta || sreang_dàta->TYPE_roinn_seòrsa != 1) return -9;
    if (sreang_dàta->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(sreang_dàta->ceangal_smachd, 4, &보조항목);
    if (!통신제어블록) return 오류번호(보조항목); sreang_dàta->ceangal_smachd = 통신제어블록; sreang_dàta->수신창구 = 1; tcp_arg(통신제어블록, sreang_dàta); tcp_accept(통신제어블록, 연결받음); return 0;
}
int 망연결하기(int faidhle_làmhrachan, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta || sreang_dàta->TYPE_roinn_seòrsa != 1) return -9;
    if (sreang_dàta->Mearachd) return sreang_dàta->Mearachd;
    if (sreang_dàta->연결됨) return 0;
    if (sreang_dàta->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !ADDRESS) return -22;
    ip_addr_t Seòladh_eadar_lìn; ip_addr_set_ip4_u32(&Seòladh_eadar_lìn, lwip_htonl(ADDRESS));
    sreang_dàta->seise_ADDRESS = ADDRESS; sreang_dàta->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(sreang_dàta->ceangal_smachd, &Seòladh_eadar_lìn, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int faidhle_làmhrachan) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta || !sreang_dàta->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_roinn_seòrsa == 1 && 통신끝점들[순번].대기중 == faidhle_làmhrachan) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int faidhle_làmhrachan, void *dàta, unsigned nì_COUNT) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta || sreang_dàta->TYPE_roinn_seòrsa != 1) return -9;
    if (!nì_COUNT) return 0; if (!sreang_dàta->cur_a_steach_COUNT) return sreang_dàta->Mearachd ? sreang_dàta->Mearachd : sreang_dàta->faidhle_crìochnaich ? 0 : -11;
    if (nì_COUNT > sreang_dàta->cur_a_steach_COUNT) nì_COUNT = sreang_dàta->cur_a_steach_COUNT;
    for (unsigned 순번 = 0; 순번 < nì_COUNT; 순번++) { ((unsigned char *)dàta)[순번] = sreang_dàta->dàta[sreang_dàta->맨앞]; sreang_dàta->맨앞 = (sreang_dàta->맨앞 + 1) % sizeof(sreang_dàta->dàta); }
    sreang_dàta->cur_a_steach_COUNT -= nì_COUNT; if (sreang_dàta->ceangal_smachd) tcp_recved(sreang_dàta->ceangal_smachd, nì_COUNT); return nì_COUNT;
}
int 통신쓰기(int faidhle_làmhrachan, const void *dàta, unsigned nì_COUNT) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta || sreang_dàta->TYPE_roinn_seòrsa != 1) return -9;
    if (sreang_dàta->Mearachd) return sreang_dàta->Mearachd; if (!sreang_dàta->ceangal_smachd || !sreang_dàta->연결됨) return -107;
    if (!nì_COUNT) return 0; if (nì_COUNT > tcp_sndbuf(sreang_dàta->ceangal_smachd)) nì_COUNT = tcp_sndbuf(sreang_dàta->ceangal_smachd);
    if (!nì_COUNT) return -11; if (nì_COUNT > 1024) nì_COUNT = 1024;
    err_t 보조항목 = tcp_write(sreang_dàta->ceangal_smachd, dàta, nì_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(sreang_dàta->ceangal_smachd); return nì_COUNT;
}
int 전문보내기(int faidhle_làmhrachan, const void *dàta, unsigned nì_COUNT, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta || sreang_dàta->TYPE_roinn_seòrsa != 2) return -9;
    if (nì_COUNT > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *dàta_suidhich = pbuf_alloc(PBUF_TRANSPORT, nì_COUNT, PBUF_RAM); if (!dàta_suidhich) return -11;
    pbuf_take(dàta_suidhich, dàta, nì_COUNT); ip_addr_t Seòladh_eadar_lìn; ip_addr_set_ip4_u32(&Seòladh_eadar_lìn, lwip_htonl(ADDRESS));
    err_t 보조항목 = udp_sendto(sreang_dàta->전문제어, dàta_suidhich, &Seòladh_eadar_lìn, 접속번호); pbuf_free(dàta_suidhich); return 보조항목 ? 오류번호(보조항목) : (int)nì_COUNT;
}
int 전문받기(int faidhle_làmhrachan, void *dàta, unsigned nì_COUNT) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta || sreang_dàta->TYPE_roinn_seòrsa != 2) return -9;
    if (!sreang_dàta->cur_a_steach_COUNT) return -11; unsigned 현재위치 = sreang_dàta->맨앞;
    if (nì_COUNT > sreang_dàta->길이목록[현재위치]) nì_COUNT = sreang_dàta->길이목록[현재위치]; memcpy(dàta, sreang_dàta->dàta + 현재위치 * 512, nì_COUNT);
    sreang_dàta->상대창구번호 = sreang_dàta->접속번호들[현재위치]; sreang_dàta->seise_ADDRESS = sreang_dàta->주소목록[현재위치]; sreang_dàta->맨앞 = (현재위치 + 1) % 4; sreang_dàta->cur_a_steach_COUNT--; return nì_COUNT;
}
unsigned 통신접속번호(int faidhle_làmhrachan) { 통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); return !sreang_dàta ? 0 : sreang_dàta->ceangal_smachd ? sreang_dàta->ceangal_smachd->local_port : sreang_dàta->전문제어 ? sreang_dàta->전문제어->local_port : 0; }
unsigned 상대접속번호(int faidhle_làmhrachan) { 통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); return sreang_dàta ? sreang_dàta->상대창구번호 : 0; }
uint32_t 상대통신주소(int faidhle_làmhrachan) { 통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); return sreang_dàta ? sreang_dàta->seise_ADDRESS : 0; }
void dùin_lìonra(int faidhle_làmhrachan) {
    통신끝점 *sreang_dàta = 얻기(faidhle_làmhrachan); if (!sreang_dàta) return;
    if (sreang_dàta->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_roinn_seòrsa && 통신끝점들[순번].대기중 == faidhle_làmhrachan) dùin_lìonra(순번);
    if (sreang_dàta->ceangal_smachd) {
        tcp_arg(sreang_dàta->ceangal_smachd, 0); if (sreang_dàta->수신창구) tcp_accept(sreang_dàta->ceangal_smachd, 0); else { tcp_recv(sreang_dàta->ceangal_smachd, 0); tcp_err(sreang_dàta->ceangal_smachd, 0); }
        if (tcp_close(sreang_dàta->ceangal_smachd) != ERR_OK) tcp_abort(sreang_dàta->ceangal_smachd);
    }
    if (sreang_dàta->전문제어) udp_remove(sreang_dàta->전문제어); sreang_dàta->TYPE_roinn_seòrsa = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&ceangal_uidheam);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (inneal_clàraich(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned còd_a_charactair = inneal_clàraich(보조장치 + 0x40) & 255;
        if (còd_a_charactair == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *dàta_suidhich = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (dàta_suidhich) { 받은전문수++; RECEIVED_baidht_COUNT += 수신사용량; pbuf_take(dàta_suidhich, 수신자료, 수신사용량); if (ceangal_uidheam.input(dàta_suidhich, &ceangal_uidheam) != ERR_OK) { 버린전문수++; pbuf_free(dàta_suidhich); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (còd_a_charactair == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (còd_a_charactair != 220 && còd_a_charactair != 221) 수신오류 = 1; còd_a_charactair = còd_a_charactair == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = còd_a_charactair; else 수신오류 = 1;
        }
    }
    netif_poll(&ceangal_uidheam); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (inneal_clàraich(보조장치 + 0x54) & 0x20); 처리한도++) {
        inneal_clàraich(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* roghainnean·조회는 lwIP의 dearbh_dàta 인터페이스와 crìochnaich_puing 표를 사용한다. */
uint32_t 망상태읽기(unsigned cur_a_steach_VALUE, unsigned INDEX) {
    if(cur_a_steach_VALUE==20)return 유선사용;
    if(cur_a_steach_VALUE==21)return 준비됨&&netif_is_link_up(&ceangal_uidheam);
    if(cur_a_steach_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&cur_a_steach_VALUE>=4&&cur_a_steach_VALUE<=8)return 유선망집계(cur_a_steach_VALUE-4);
    if (cur_a_steach_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ceangal_uidheam)));
    if (cur_a_steach_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&ceangal_uidheam)));
    if (cur_a_steach_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&ceangal_uidheam)));
    if (cur_a_steach_VALUE == 3) return netif_is_up(&ceangal_uidheam) != 0;
    if (cur_a_steach_VALUE == 4) return 받은전문수;
    if (cur_a_steach_VALUE == 5) return 보낸전문수;
    if (cur_a_steach_VALUE == 6) return RECEIVED_baidht_COUNT;
    if (cur_a_steach_VALUE == 7) return 보낸바이트수;
    if (cur_a_steach_VALUE == 8) return 버린전문수;
    if (cur_a_steach_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *crìochnaich_puing = &통신끝점들[INDEX];
    if (cur_a_steach_VALUE == 10) return crìochnaich_puing->TYPE_roinn_seòrsa;
    if (!crìochnaich_puing->TYPE_roinn_seòrsa) return 0;
    if (cur_a_steach_VALUE == 11) return 통신접속번호(INDEX);
    if (cur_a_steach_VALUE == 12) return crìochnaich_puing->seise_ADDRESS;
    if (cur_a_steach_VALUE == 13) return crìochnaich_puing->상대창구번호;
    if (cur_a_steach_VALUE == 14) return crìochnaich_puing->수신창구 ? 1 : crìochnaich_puing->faidhle_crìochnaich ? 3 : crìochnaich_puing->Mearachd ? 4 : crìochnaich_puing->연결됨 ? 2 : 0;
    if (cur_a_steach_VALUE == 15) return crìochnaich_puing->cur_a_steach_COUNT;
    if (cur_a_steach_VALUE == 16) {
        const ip_addr_t *ADDRESS = crìochnaich_puing->TYPE_roinn_seòrsa == 1 && crìochnaich_puing->ceangal_smachd ? &crìochnaich_puing->ceangal_smachd->local_ip :
            crìochnaich_puing->TYPE_roinn_seòrsa == 2 && crìochnaich_puing->전문제어 ? &crìochnaich_puing->전문제어->local_ip : 0;
        return ADDRESS ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) : 0;
    }
    return 0;
}

int rèitich_lìonra(unsigned Gnìomh, uint32_t ADDRESS, uint32_t 가림, uint32_t 관문) {
    if (!준비됨) return -100;
    if (Gnìomh == 1) { netif_set_up(&ceangal_uidheam); return 0; }
    if (Gnìomh == 2) { netif_set_down(&ceangal_uidheam); return 0; }
    if (Gnìomh != 0) return -22;
    /* 유니캐스트 IPv4, 연속 가림, 같은 망의 선택적 luach_bunaiteach 관문. */
    uint32_t 뒤집은가림 = ~가림;
    if (!가림 || (뒤집은가림 & (뒤집은가림 + 1)) || !ADDRESS || (ADDRESS >> 24) == 127 ||
        (ADDRESS >> 24) == 0 || (ADDRESS >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADDRESS & 뒤집은가림) || (ADDRESS & 뒤집은가림) == 뒤집은가림)) ||
        (관문 && ((관문 & 가림) != (ADDRESS & 가림) || 관문 == ADDRESS || (관문 >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(관문 & 뒤집은가림) || (관문 & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADDRESS 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_roinn_seòrsa &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].ceangal_smachd && ip_addr_isany(&통신끝점들[INDEX].ceangal_smachd->local_ip))) return -16;
    if(유선사용)dhcp_stop(&ceangal_uidheam);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADDRESS)); ip4_addr_set_u32(&새가림, lwip_htonl(가림)); ip4_addr_set_u32(&새관문, lwip_htonl(관문));
    netif_set_addr(&ceangal_uidheam, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *crìochnaich_puing, struct pbuf *dàta, const ip_addr_t *ADDRESS) {
    (void)인수; (void)crìochnaich_puing;
    unsigned char 머리[20], freagair[16];
    if (응답상태 != -11 || dàta->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) != 시험주소 || pbuf_copy_partial(dàta, 머리, 20, 0) != 20) return 0;
    unsigned bann_cinn_atharraich_am_meud = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || bann_cinn_atharraich_am_meud < 20 || dàta->tot_len < bann_cinn_atharraich_am_meud + 16 ||
        pbuf_copy_partial(dàta, freagair, 16, bann_cinn_atharraich_am_meud) != 16 || freagair[0] || freagair[1] ||
        (((unsigned)freagair[4] << 8) | freagair[5]) != 시험식별자 ||
        (((unsigned)freagair[6] << 8) | freagair[7]) != 시험순서 ||
        freagair[8] != 'J' || freagair[9] != 'K' || freagair[10] != 'O' || freagair[11] != 'S' ||
        (((uint32_t)freagair[12] << 24) | ((uint32_t)freagair[13] << 16) | ((uint32_t)freagair[14] << 8) | freagair[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(dàta, bann_cinn_atharraich_am_meud)) return 0;
    if (inet_chksum_pbuf(dàta)) { pbuf_add_header(dàta, bann_cinn_atharraich_am_meud); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(dàta); return 1;
}
int 응답시험시작(uint32_t ADDRESS, unsigned òrdugh_VALUE) {
    if (!준비됨 || !netif_is_up(&ceangal_uidheam)) return -100;
    if (!ADDRESS || (ADDRESS >> 28) >= 14 || ADDRESS == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ADDRESS; 시험순서 = òrdugh_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char dàta[32] = {8,0,0,0};
    dàta[4] = 시험식별자 >> 8; dàta[5] = 시험식별자; dàta[6] = 시험순서 >> 8; dàta[7] = 시험순서;
    dàta[8]='J'; dàta[9]='K'; dàta[10]='O'; dàta[11]='S';
    dàta[12]=시험시각 >> 24; dàta[13]=시험시각 >> 16; dàta[14]=시험시각 >> 8; dàta[15]=시험시각;
    for (unsigned suidhich_INDEX = 16; suidhich_INDEX < sizeof(dàta); suidhich_INDEX++) dàta[suidhich_INDEX] = suidhich_INDEX;
    uint16_t 확인합 = inet_chksum(dàta, sizeof(dàta)); memcpy(dàta + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(dàta), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, dàta, sizeof(dàta)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ADDRESS));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned cur_a_steach_VALUE) {
    통신망살피기();
    return cur_a_steach_VALUE == 0 ? 응답상태 : cur_a_steach_VALUE == 1 ? (int)응답시간 : cur_a_steach_VALUE == 2 ? (int)응답차례 : -22;
}
