#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "whatunga_Huinga.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../mamao_uara/mamao_uara.h"
#include "whaiaho_whatunga.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define mīhini_rēhita(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif hononga_pūkoro;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_paita_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_kāwai, 수신창구, 대기중, 연결됨, kōnae_mutu, Pōhēhē;
    struct tcp_pcb *hononga_mana;
    struct udp_pcb *전문제어;
    unsigned 맨앞, tāurunga_COUNT;
    unsigned char raraunga[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], hoa_ADDRESS;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int kōnae_raweke) { return kōnae_raweke >= 0 && kōnae_raweke < 32 && 통신끝점들[kōnae_raweke].TYPE_kāwai ? &통신끝점들[kōnae_raweke] : 0; }
static int 예약하기(int TYPE_kāwai) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_kāwai) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_kāwai = TYPE_kāwai; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned waehere_pūāhua) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = waehere_pūāhua; }
static err_t 출력결과(struct netif *tuemi_COUNT, struct pbuf *raraunga_tūranga, const ip4_addr_t *ADDRESS) {
    (void)tuemi_COUNT; (void)ADDRESS;
    if (raraunga_tūranga->tot_len > 1500 || 송신개수 + 2 * raraunga_tūranga->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Panuku_OFFSET = raraunga_tūranga; Panuku_OFFSET; Panuku_OFFSET = Panuku_OFFSET->next) for (unsigned 순번 = 0; 순번 < Panuku_OFFSET->len; 순번++) {
        unsigned waehere_pūāhua = ((unsigned char *)Panuku_OFFSET->payload)[순번];
        if (waehere_pūāhua == 192 || waehere_pūāhua == 219) { 내보내기(219); 내보내기(waehere_pūāhua == 192 ? 220 : 221); } else 내보내기(waehere_pūāhua);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += raraunga_tūranga->tot_len; return ERR_OK;
}
static err_t Whakarite_wāhaere_reo_noa(struct netif *tuemi_COUNT) { tuemi_COUNT->name[0] = 's'; tuemi_COUNT->name[1] = 'l'; tuemi_COUNT->mtu = 1500; tuemi_COUNT->output = 출력결과; return ERR_OK; }
void Whakarite_whatunga(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    mīhini_rēhita(보조장치 + 4) |= 1; mīhini_rēhita(보조장치 + 0x60) = 0; mīhini_rēhita(보조장치 + 0x44) = 0;
    mīhini_rēhita(보조장치 + 0x48) = 0xc6; mīhini_rēhita(보조장치 + 0x4c) = 3; mīhini_rēhita(보조장치 + 0x68) = 270; mīhini_rēhita(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Wāhitau_ipurangi, moka_hīpoki, waharoa_ADDRESS;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Wāhitau_ipurangi, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&moka_hīpoki, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&waharoa_ADDRESS, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&hononga_pūkoro, &Wāhitau_ipurangi, &moka_hīpoki, &waharoa_ADDRESS, 0, 유선사용?Whakarite_whaiaho_whatunga:Whakarite_wāhaere_reo_noa, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&hononga_pūkoro); netif_set_up(&hononga_pūkoro);if(!유선사용)netif_set_link_up(&hononga_pūkoro); 준비됨 = 1;
    Whakarite_mamao();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *tarenga_mana_aukati, struct pbuf *raraunga_tūranga, err_t Pōhēhē) {
    통신끝점 *aho_raraunga = 부가인수; (void)tarenga_mana_aukati; (void)Pōhēhē;
    if (!raraunga_tūranga) { aho_raraunga->kōnae_mutu = 1; return ERR_OK; }
    if (raraunga_tūranga->tot_len > sizeof(aho_raraunga->raraunga) - aho_raraunga->tāurunga_COUNT) return ERR_MEM;
    unsigned 현재위치 = (aho_raraunga->맨앞 + aho_raraunga->tāurunga_COUNT) % sizeof(aho_raraunga->raraunga);
    for (struct pbuf *Panuku_OFFSET = raraunga_tūranga; Panuku_OFFSET; Panuku_OFFSET = Panuku_OFFSET->next) for (unsigned 순번 = 0; 순번 < Panuku_OFFSET->len; 순번++) {
        aho_raraunga->raraunga[현재위치] = ((unsigned char *)Panuku_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(aho_raraunga->raraunga);
    }
    aho_raraunga->tāurunga_COUNT += raraunga_tūranga->tot_len; pbuf_free(raraunga_tūranga); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Pōhēhē) { 통신끝점 *aho_raraunga = 부가인수; aho_raraunga->hononga_mana = 0; aho_raraunga->Pōhēhē = 오류번호(Pōhēhē); }
static void 되부름목록(통신끝점 *aho_raraunga) { tcp_arg(aho_raraunga->hononga_mana, aho_raraunga); tcp_recv(aho_raraunga->hononga_mana, 수신됨); tcp_err(aho_raraunga->hononga_mana, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *tarenga_mana_aukati, err_t Pōhēhē) {
    통신끝점 *aho_raraunga = 부가인수; (void)tarenga_mana_aukati; if (Pōhēhē) aho_raraunga->Pōhēhē = 오류번호(Pōhēhē); else aho_raraunga->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *tarenga_mana_aukati, err_t Pōhēhē) {
    통신끝점 *부모항목 = 부가인수; if (Pōhēhē) return Pōhēhē;
    int kōnae_raweke = 예약하기(1); if (kōnae_raweke < 0) return ERR_MEM;
    통신끝점 *aho_raraunga = &통신끝점들[kōnae_raweke]; aho_raraunga->hononga_mana = tarenga_mana_aukati; aho_raraunga->연결됨 = 1; aho_raraunga->대기중 = (int)(부모항목 - 통신끝점들);
    aho_raraunga->hoa_ADDRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&tarenga_mana_aukati->remote_ip))); aho_raraunga->상대창구번호 = tarenga_mana_aukati->remote_port;
    되부름목록(aho_raraunga); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *tarenga_mana_aukati, struct pbuf *raraunga_tūranga, const ip_addr_t *ADDRESS, u16_t 접속번호) {
    통신끝점 *aho_raraunga = 부가인수; (void)tarenga_mana_aukati;
    if (aho_raraunga->tāurunga_COUNT < 4 && raraunga_tūranga->tot_len <= 512) {
        unsigned tūranga_INDEX = (aho_raraunga->맨앞 + aho_raraunga->tāurunga_COUNT) % 4;
        pbuf_copy_partial(raraunga_tūranga, aho_raraunga->raraunga + tūranga_INDEX * 512, raraunga_tūranga->tot_len, 0);
        aho_raraunga->길이목록[tūranga_INDEX] = raraunga_tūranga->tot_len; aho_raraunga->접속번호들[tūranga_INDEX] = 접속번호;
        aho_raraunga->주소목록[tūranga_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))); aho_raraunga->tāurunga_COUNT++;
    }
    pbuf_free(raraunga_tūranga);
}
int 통신끝점만들기(int TYPE_kāwai) {
    if (!준비됨) return -100;
    if (TYPE_kāwai != 1 && TYPE_kāwai != 2) return -93;
    int kōnae_raweke = 예약하기(TYPE_kāwai); if (kōnae_raweke < 0) return kōnae_raweke;
    통신끝점 *aho_raraunga = &통신끝점들[kōnae_raweke];
    if (TYPE_kāwai == 1) { aho_raraunga->hononga_mana = tcp_new(); if (aho_raraunga->hononga_mana) 되부름목록(aho_raraunga); }
    else { aho_raraunga->전문제어 = udp_new(); if (aho_raraunga->전문제어) udp_recv(aho_raraunga->전문제어, 전문, aho_raraunga); }
    if (!aho_raraunga->hononga_mana && !aho_raraunga->전문제어) { aho_raraunga->TYPE_kāwai = 0; return -12; } return kōnae_raweke;
}
int 망주소묶기(int kōnae_raweke, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga) return -9;
    if (접속번호 > 65535 || (ADDRESS && ADDRESS != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&hononga_pūkoro))) && ADDRESS != 0x7f000001)) return -99;
    ip_addr_t Wāhitau_ipurangi; ip_addr_set_ip4_u32(&Wāhitau_ipurangi, lwip_htonl(ADDRESS));
    err_t 보조항목 = aho_raraunga->TYPE_kāwai == 1 ? tcp_bind(aho_raraunga->hononga_mana, &Wāhitau_ipurangi, 접속번호) : udp_bind(aho_raraunga->전문제어, &Wāhitau_ipurangi, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int kōnae_raweke) { 통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (aho_raraunga && aho_raraunga->hononga_mana) ip_set_option(aho_raraunga->hononga_mana, SOF_REUSEADDR); }
int 연결기다리기(int kōnae_raweke) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga || aho_raraunga->TYPE_kāwai != 1) return -9;
    if (aho_raraunga->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *tarenga_mana_aukati = tcp_listen_with_backlog_and_err(aho_raraunga->hononga_mana, 4, &보조항목);
    if (!tarenga_mana_aukati) return 오류번호(보조항목); aho_raraunga->hononga_mana = tarenga_mana_aukati; aho_raraunga->수신창구 = 1; tcp_arg(tarenga_mana_aukati, aho_raraunga); tcp_accept(tarenga_mana_aukati, 연결받음); return 0;
}
int 망연결하기(int kōnae_raweke, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga || aho_raraunga->TYPE_kāwai != 1) return -9;
    if (aho_raraunga->Pōhēhē) return aho_raraunga->Pōhēhē;
    if (aho_raraunga->연결됨) return 0;
    if (aho_raraunga->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !ADDRESS) return -22;
    ip_addr_t Wāhitau_ipurangi; ip_addr_set_ip4_u32(&Wāhitau_ipurangi, lwip_htonl(ADDRESS));
    aho_raraunga->hoa_ADDRESS = ADDRESS; aho_raraunga->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(aho_raraunga->hononga_mana, &Wāhitau_ipurangi, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int kōnae_raweke) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga || !aho_raraunga->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_kāwai == 1 && 통신끝점들[순번].대기중 == kōnae_raweke) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int kōnae_raweke, void *raraunga, unsigned tuemi_COUNT) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga || aho_raraunga->TYPE_kāwai != 1) return -9;
    if (!tuemi_COUNT) return 0; if (!aho_raraunga->tāurunga_COUNT) return aho_raraunga->Pōhēhē ? aho_raraunga->Pōhēhē : aho_raraunga->kōnae_mutu ? 0 : -11;
    if (tuemi_COUNT > aho_raraunga->tāurunga_COUNT) tuemi_COUNT = aho_raraunga->tāurunga_COUNT;
    for (unsigned 순번 = 0; 순번 < tuemi_COUNT; 순번++) { ((unsigned char *)raraunga)[순번] = aho_raraunga->raraunga[aho_raraunga->맨앞]; aho_raraunga->맨앞 = (aho_raraunga->맨앞 + 1) % sizeof(aho_raraunga->raraunga); }
    aho_raraunga->tāurunga_COUNT -= tuemi_COUNT; if (aho_raraunga->hononga_mana) tcp_recved(aho_raraunga->hononga_mana, tuemi_COUNT); return tuemi_COUNT;
}
int 통신쓰기(int kōnae_raweke, const void *raraunga, unsigned tuemi_COUNT) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga || aho_raraunga->TYPE_kāwai != 1) return -9;
    if (aho_raraunga->Pōhēhē) return aho_raraunga->Pōhēhē; if (!aho_raraunga->hononga_mana || !aho_raraunga->연결됨) return -107;
    if (!tuemi_COUNT) return 0; if (tuemi_COUNT > tcp_sndbuf(aho_raraunga->hononga_mana)) tuemi_COUNT = tcp_sndbuf(aho_raraunga->hononga_mana);
    if (!tuemi_COUNT) return -11; if (tuemi_COUNT > 1024) tuemi_COUNT = 1024;
    err_t 보조항목 = tcp_write(aho_raraunga->hononga_mana, raraunga, tuemi_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(aho_raraunga->hononga_mana); return tuemi_COUNT;
}
int 전문보내기(int kōnae_raweke, const void *raraunga, unsigned tuemi_COUNT, uint32_t ADDRESS, unsigned 접속번호) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga || aho_raraunga->TYPE_kāwai != 2) return -9;
    if (tuemi_COUNT > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *raraunga_tūranga = pbuf_alloc(PBUF_TRANSPORT, tuemi_COUNT, PBUF_RAM); if (!raraunga_tūranga) return -11;
    pbuf_take(raraunga_tūranga, raraunga, tuemi_COUNT); ip_addr_t Wāhitau_ipurangi; ip_addr_set_ip4_u32(&Wāhitau_ipurangi, lwip_htonl(ADDRESS));
    err_t 보조항목 = udp_sendto(aho_raraunga->전문제어, raraunga_tūranga, &Wāhitau_ipurangi, 접속번호); pbuf_free(raraunga_tūranga); return 보조항목 ? 오류번호(보조항목) : (int)tuemi_COUNT;
}
int 전문받기(int kōnae_raweke, void *raraunga, unsigned tuemi_COUNT) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga || aho_raraunga->TYPE_kāwai != 2) return -9;
    if (!aho_raraunga->tāurunga_COUNT) return -11; unsigned 현재위치 = aho_raraunga->맨앞;
    if (tuemi_COUNT > aho_raraunga->길이목록[현재위치]) tuemi_COUNT = aho_raraunga->길이목록[현재위치]; memcpy(raraunga, aho_raraunga->raraunga + 현재위치 * 512, tuemi_COUNT);
    aho_raraunga->상대창구번호 = aho_raraunga->접속번호들[현재위치]; aho_raraunga->hoa_ADDRESS = aho_raraunga->주소목록[현재위치]; aho_raraunga->맨앞 = (현재위치 + 1) % 4; aho_raraunga->tāurunga_COUNT--; return tuemi_COUNT;
}
unsigned 통신접속번호(int kōnae_raweke) { 통신끝점 *aho_raraunga = 얻기(kōnae_raweke); return !aho_raraunga ? 0 : aho_raraunga->hononga_mana ? aho_raraunga->hononga_mana->local_port : aho_raraunga->전문제어 ? aho_raraunga->전문제어->local_port : 0; }
unsigned 상대접속번호(int kōnae_raweke) { 통신끝점 *aho_raraunga = 얻기(kōnae_raweke); return aho_raraunga ? aho_raraunga->상대창구번호 : 0; }
uint32_t 상대통신주소(int kōnae_raweke) { 통신끝점 *aho_raraunga = 얻기(kōnae_raweke); return aho_raraunga ? aho_raraunga->hoa_ADDRESS : 0; }
void kati_whatunga(int kōnae_raweke) {
    통신끝점 *aho_raraunga = 얻기(kōnae_raweke); if (!aho_raraunga) return;
    if (aho_raraunga->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_kāwai && 통신끝점들[순번].대기중 == kōnae_raweke) kati_whatunga(순번);
    if (aho_raraunga->hononga_mana) {
        tcp_arg(aho_raraunga->hononga_mana, 0); if (aho_raraunga->수신창구) tcp_accept(aho_raraunga->hononga_mana, 0); else { tcp_recv(aho_raraunga->hononga_mana, 0); tcp_err(aho_raraunga->hononga_mana, 0); }
        if (tcp_close(aho_raraunga->hononga_mana) != ERR_OK) tcp_abort(aho_raraunga->hononga_mana);
    }
    if (aho_raraunga->전문제어) udp_remove(aho_raraunga->전문제어); aho_raraunga->TYPE_kāwai = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&hononga_pūkoro);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (mīhini_rēhita(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned waehere_pūāhua = mīhini_rēhita(보조장치 + 0x40) & 255;
        if (waehere_pūāhua == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *raraunga_tūranga = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (raraunga_tūranga) { 받은전문수++; RECEIVED_paita_COUNT += 수신사용량; pbuf_take(raraunga_tūranga, 수신자료, 수신사용량); if (hononga_pūkoro.input(raraunga_tūranga, &hononga_pūkoro) != ERR_OK) { 버린전문수++; pbuf_free(raraunga_tūranga); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (waehere_pūāhua == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (waehere_pūāhua != 220 && waehere_pūāhua != 221) 수신오류 = 1; waehere_pūāhua = waehere_pūāhua == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = waehere_pūāhua; else 수신오류 = 1;
        }
    }
    netif_poll(&hononga_pūkoro); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (mīhini_rēhita(보조장치 + 0x54) & 0x20); 처리한도++) {
        mīhini_rēhita(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Ngā_Tautuhinga·조회는 lwIP의 tūturu_raraunga 인터페이스와 mutu_ira 표를 사용한다. */
uint32_t 망상태읽기(unsigned tāurunga_uara, unsigned INDEX) {
    if(tāurunga_uara==20)return 유선사용;
    if(tāurunga_uara==21)return 준비됨&&netif_is_link_up(&hononga_pūkoro);
    if(tāurunga_uara==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&tāurunga_uara>=4&&tāurunga_uara<=8)return 유선망집계(tāurunga_uara-4);
    if (tāurunga_uara == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&hononga_pūkoro)));
    if (tāurunga_uara == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&hononga_pūkoro)));
    if (tāurunga_uara == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&hononga_pūkoro)));
    if (tāurunga_uara == 3) return netif_is_up(&hononga_pūkoro) != 0;
    if (tāurunga_uara == 4) return 받은전문수;
    if (tāurunga_uara == 5) return 보낸전문수;
    if (tāurunga_uara == 6) return RECEIVED_paita_COUNT;
    if (tāurunga_uara == 7) return 보낸바이트수;
    if (tāurunga_uara == 8) return 버린전문수;
    if (tāurunga_uara == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *mutu_ira = &통신끝점들[INDEX];
    if (tāurunga_uara == 10) return mutu_ira->TYPE_kāwai;
    if (!mutu_ira->TYPE_kāwai) return 0;
    if (tāurunga_uara == 11) return 통신접속번호(INDEX);
    if (tāurunga_uara == 12) return mutu_ira->hoa_ADDRESS;
    if (tāurunga_uara == 13) return mutu_ira->상대창구번호;
    if (tāurunga_uara == 14) return mutu_ira->수신창구 ? 1 : mutu_ira->kōnae_mutu ? 3 : mutu_ira->Pōhēhē ? 4 : mutu_ira->연결됨 ? 2 : 0;
    if (tāurunga_uara == 15) return mutu_ira->tāurunga_COUNT;
    if (tāurunga_uara == 16) {
        const ip_addr_t *ADDRESS = mutu_ira->TYPE_kāwai == 1 && mutu_ira->hononga_mana ? &mutu_ira->hononga_mana->local_ip :
            mutu_ira->TYPE_kāwai == 2 && mutu_ira->전문제어 ? &mutu_ira->전문제어->local_ip : 0;
        return ADDRESS ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) : 0;
    }
    return 0;
}

int whirihora_whatunga(unsigned hohenga, uint32_t ADDRESS, uint32_t hīpoki_uara, uint32_t waharoa_uara) {
    if (!준비됨) return -100;
    if (hohenga == 1) { netif_set_up(&hononga_pūkoro); return 0; }
    if (hohenga == 2) { netif_set_down(&hononga_pūkoro); return 0; }
    if (hohenga != 0) return -22;
    /* 유니캐스트 IPv4, 연속 hīpoki_uara, 같은 망의 선택적 uara_taunoa waharoa_uara. */
    uint32_t 뒤집은가림 = ~hīpoki_uara;
    if (!hīpoki_uara || (뒤집은가림 & (뒤집은가림 + 1)) || !ADDRESS || (ADDRESS >> 24) == 127 ||
        (ADDRESS >> 24) == 0 || (ADDRESS >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADDRESS & 뒤집은가림) || (ADDRESS & 뒤집은가림) == 뒤집은가림)) ||
        (waharoa_uara && ((waharoa_uara & hīpoki_uara) != (ADDRESS & hīpoki_uara) || waharoa_uara == ADDRESS || (waharoa_uara >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(waharoa_uara & 뒤집은가림) || (waharoa_uara & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADDRESS 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_kāwai &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].hononga_mana && ip_addr_isany(&통신끝점들[INDEX].hononga_mana->local_ip))) return -16;
    if(유선사용)dhcp_stop(&hononga_pūkoro);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADDRESS)); ip4_addr_set_u32(&새가림, lwip_htonl(hīpoki_uara)); ip4_addr_set_u32(&새관문, lwip_htonl(waharoa_uara));
    netif_set_addr(&hononga_pūkoro, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *mutu_ira, struct pbuf *raraunga, const ip_addr_t *ADDRESS) {
    (void)인수; (void)mutu_ira;
    unsigned char 머리[20], whakautu[16];
    if (응답상태 != -11 || raraunga->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) != 시험주소 || pbuf_copy_partial(raraunga, 머리, 20, 0) != 20) return 0;
    unsigned Pane_rahi = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Pane_rahi < 20 || raraunga->tot_len < Pane_rahi + 16 ||
        pbuf_copy_partial(raraunga, whakautu, 16, Pane_rahi) != 16 || whakautu[0] || whakautu[1] ||
        (((unsigned)whakautu[4] << 8) | whakautu[5]) != 시험식별자 ||
        (((unsigned)whakautu[6] << 8) | whakautu[7]) != 시험순서 ||
        whakautu[8] != 'J' || whakautu[9] != 'K' || whakautu[10] != 'O' || whakautu[11] != 'S' ||
        (((uint32_t)whakautu[12] << 24) | ((uint32_t)whakautu[13] << 16) | ((uint32_t)whakautu[14] << 8) | whakautu[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(raraunga, Pane_rahi)) return 0;
    if (inet_chksum_pbuf(raraunga)) { pbuf_add_header(raraunga, Pane_rahi); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(raraunga); return 1;
}
int 응답시험시작(uint32_t ADDRESS, unsigned whakaraupapa_uara) {
    if (!준비됨 || !netif_is_up(&hononga_pūkoro)) return -100;
    if (!ADDRESS || (ADDRESS >> 28) >= 14 || ADDRESS == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = ADDRESS; 시험순서 = whakaraupapa_uara & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char raraunga[32] = {8,0,0,0};
    raraunga[4] = 시험식별자 >> 8; raraunga[5] = 시험식별자; raraunga[6] = 시험순서 >> 8; raraunga[7] = 시험순서;
    raraunga[8]='J'; raraunga[9]='K'; raraunga[10]='O'; raraunga[11]='S';
    raraunga[12]=시험시각 >> 24; raraunga[13]=시험시각 >> 16; raraunga[14]=시험시각 >> 8; raraunga[15]=시험시각;
    for (unsigned tūranga_INDEX = 16; tūranga_INDEX < sizeof(raraunga); tūranga_INDEX++) raraunga[tūranga_INDEX] = tūranga_INDEX;
    uint16_t 확인합 = inet_chksum(raraunga, sizeof(raraunga)); memcpy(raraunga + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(raraunga), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, raraunga, sizeof(raraunga)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(ADDRESS));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned tāurunga_uara) {
    통신망살피기();
    return tāurunga_uara == 0 ? 응답상태 : tāurunga_uara == 1 ? (int)응답시간 : tāurunga_uara == 2 ? (int)응답차례 : -22;
}
