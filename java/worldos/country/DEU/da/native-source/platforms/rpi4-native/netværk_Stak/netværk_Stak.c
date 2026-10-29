#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "netværk_Stak.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../fjern_VÆRDI/fjern_VÆRDI.h"
#include "traditionel_netværk.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define maskine_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif forbindelse_enhed;
static int 준비됨, forespørgsel;
static int brug_traditionel_netværk;
static unsigned modtage_brug, 수신탈출, modtage_fejl;
static unsigned char modtage_data_buffer[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t MODTAGET_VED_UDLØB_datagram_TÆL, 보낸전문수, MODTAGET_VED_UDLØB_byte_TÆL, 보낸바이트수, 버린전문수;
typedef struct {
    int Type_område, modtage_port, it_Afventer, 연결됨, fil_afslutte_et_opkald, fejl;
    struct tcp_pcb *forbindelse_kontrol;
    struct udp_pcb *datagram_kontrol;
    unsigned frontvendt_post, post_TÆL_8f7753a1;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], peer_slutpunkt_tal;
    uint32_t 주소목록[4], peer_mail;
} socket_slutpunkt_3db661a2;
static socket_slutpunkt_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int fejlnummer(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static socket_slutpunkt_3db661a2 *hente_VÆRDI(int fil_handle) { return fil_handle >= 0 && fil_handle < 32 && 통신끝점들[fil_handle].Type_område ? &통신끝점들[fil_handle] : 0; }
static int 예약하기(int Type_område) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].Type_område) {
        memset(&통신끝점들[순번], 0, sizeof(socket_slutpunkt_3db661a2)); 통신끝점들[순번].Type_område = Type_område; 통신끝점들[순번].it_Afventer = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned tegnkode) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = tegnkode; }
static err_t produktoutput(struct netif *vare_TÆL, struct pbuf *data_placere, const ip4_addr_t *mail) {
    (void)vare_TÆL; (void)mail;
    if (data_placere->tot_len > 1500 || 송신개수 + 2 * data_placere->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Næste_FORSKYDNING = data_placere; Næste_FORSKYDNING; Næste_FORSKYDNING = Næste_FORSKYDNING->next) for (unsigned 순번 = 0; 순번 < Næste_FORSKYDNING->len; 순번++) {
        unsigned tegnkode = ((unsigned char *)Næste_FORSKYDNING->payload)[순번];
        if (tegnkode == 192 || tegnkode == 219) { 내보내기(219); 내보내기(tegnkode == 192 ? 220 : 221); } else 내보내기(tegnkode);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_placere->tot_len; return ERR_OK;
}
static err_t Tilrettelæg_CLR(struct netif *vare_TÆL) { vare_TÆL->name[0] = 's'; vare_TÆL->name[1] = 'l'; vare_TÆL->mtu = 1500; vare_TÆL->output = produktoutput; return ERR_OK; }
void Tilrettelæg_netværk(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    maskine_register(보조장치 + 4) |= 1; maskine_register(보조장치 + 0x60) = 0; maskine_register(보조장치 + 0x44) = 0;
    maskine_register(보조장치 + 0x48) = 0xc6; maskine_register(보조장치 + 0x4c) = 3; maskine_register(보조장치 + 0x68) = 270; maskine_register(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t internetadresse, bitmaske, gatewayadresse;
    brug_traditionel_netværk=유선장치있음();
    ip4_addr_set_u32(&internetadresse, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmaske, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&gatewayadresse, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&forbindelse_enhed, &internetadresse, &bitmaske, &gatewayadresse, 0, brug_traditionel_netværk?Tilrettelæg_traditionel_netværk:Tilrettelæg_CLR, brug_traditionel_netværk?ethernet_input:ip4_input))return;
    netif_set_default(&forbindelse_enhed); netif_set_up(&forbindelse_enhed);if(!brug_traditionel_netværk)netif_set_link_up(&forbindelse_enhed); 준비됨 = 1;
    Tilrettelæg_fjern();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *data_placere, err_t fejl) {
    socket_slutpunkt_3db661a2 *streng_data = 부가인수; (void)통신제어블록; (void)fejl;
    if (!data_placere) { streng_data->fil_afslutte_et_opkald = 1; return ERR_OK; }
    if (data_placere->tot_len > sizeof(streng_data->data) - streng_data->post_TÆL_8f7753a1) return ERR_MEM;
    unsigned aktuel_placere = (streng_data->frontvendt_post + streng_data->post_TÆL_8f7753a1) % sizeof(streng_data->data);
    for (struct pbuf *Næste_FORSKYDNING = data_placere; Næste_FORSKYDNING; Næste_FORSKYDNING = Næste_FORSKYDNING->next) for (unsigned 순번 = 0; 순번 < Næste_FORSKYDNING->len; 순번++) {
        streng_data->data[aktuel_placere] = ((unsigned char *)Næste_FORSKYDNING->payload)[순번]; aktuel_placere = (aktuel_placere + 1) % sizeof(streng_data->data);
    }
    streng_data->post_TÆL_8f7753a1 += data_placere->tot_len; pbuf_free(data_placere); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t fejl) { socket_slutpunkt_3db661a2 *streng_data = 부가인수; streng_data->forbindelse_kontrol = 0; streng_data->fejl = fejlnummer(fejl); }
static void 되부름목록(socket_slutpunkt_3db661a2 *streng_data) { tcp_arg(streng_data->forbindelse_kontrol, streng_data); tcp_recv(streng_data->forbindelse_kontrol, 수신됨); tcp_err(streng_data->forbindelse_kontrol, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t fejl) {
    socket_slutpunkt_3db661a2 *streng_data = 부가인수; (void)통신제어블록; if (fejl) streng_data->fejl = fejlnummer(fejl); else streng_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t fejl) {
    socket_slutpunkt_3db661a2 *overordnet = 부가인수; if (fejl) return fejl;
    int fil_handle = 예약하기(1); if (fil_handle < 0) return ERR_MEM;
    socket_slutpunkt_3db661a2 *streng_data = &통신끝점들[fil_handle]; streng_data->forbindelse_kontrol = 통신제어블록; streng_data->연결됨 = 1; streng_data->it_Afventer = (int)(overordnet - 통신끝점들);
    streng_data->peer_mail = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); streng_data->peer_slutpunkt_tal = 통신제어블록->remote_port;
    되부름목록(streng_data); return ERR_OK;
}
static void datagram(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *data_placere, const ip_addr_t *mail, u16_t portnummer) {
    socket_slutpunkt_3db661a2 *streng_data = 부가인수; (void)통신제어블록;
    if (streng_data->post_TÆL_8f7753a1 < 4 && data_placere->tot_len <= 512) {
        unsigned positionsindeks = (streng_data->frontvendt_post + streng_data->post_TÆL_8f7753a1) % 4;
        pbuf_copy_partial(data_placere, streng_data->data + positionsindeks * 512, data_placere->tot_len, 0);
        streng_data->길이목록[positionsindeks] = data_placere->tot_len; streng_data->접속번호들[positionsindeks] = portnummer;
        streng_data->주소목록[positionsindeks] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(mail))); streng_data->post_TÆL_8f7753a1++;
    }
    pbuf_free(data_placere);
}
int åbne_socket_slutpunkt(int Type_område) {
    if (!준비됨) return -100;
    if (Type_område != 1 && Type_område != 2) return -93;
    int fil_handle = 예약하기(Type_område); if (fil_handle < 0) return fil_handle;
    socket_slutpunkt_3db661a2 *streng_data = &통신끝점들[fil_handle];
    if (Type_område == 1) { streng_data->forbindelse_kontrol = tcp_new(); if (streng_data->forbindelse_kontrol) 되부름목록(streng_data); }
    else { streng_data->datagram_kontrol = udp_new(); if (streng_data->datagram_kontrol) udp_recv(streng_data->datagram_kontrol, datagram, streng_data); }
    if (!streng_data->forbindelse_kontrol && !streng_data->datagram_kontrol) { streng_data->Type_område = 0; return -12; } return fil_handle;
}
int NET_BIND(int fil_handle, uint32_t mail, unsigned portnummer) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data) return -9;
    if (portnummer > 65535 || (mail && mail != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&forbindelse_enhed))) && mail != 0x7f000001)) return -99;
    ip_addr_t internetadresse; ip_addr_set_ip4_u32(&internetadresse, lwip_htonl(mail));
    err_t 보조항목 = streng_data->Type_område == 1 ? tcp_bind(streng_data->forbindelse_kontrol, &internetadresse, portnummer) : udp_bind(streng_data->datagram_kontrol, &internetadresse, portnummer); return 보조항목 ? fejlnummer(보조항목) : 0;
}
void 통신주소재사용(int fil_handle) { socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (streng_data && streng_data->forbindelse_kontrol) ip_set_option(streng_data->forbindelse_kontrol, SOF_REUSEADDR); }
int NET_lytte(int fil_handle) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data || streng_data->Type_område != 1) return -9;
    if (streng_data->modtage_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(streng_data->forbindelse_kontrol, 4, &보조항목);
    if (!통신제어블록) return fejlnummer(보조항목); streng_data->forbindelse_kontrol = 통신제어블록; streng_data->modtage_port = 1; tcp_arg(통신제어블록, streng_data); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_Forbind(int fil_handle, uint32_t mail, unsigned portnummer) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data || streng_data->Type_område != 1) return -9;
    if (streng_data->fejl) return streng_data->fejl;
    if (streng_data->연결됨) return 0;
    if (streng_data->peer_slutpunkt_tal) return -115;
    if (!portnummer || portnummer > 65535 || !mail) return -22;
    ip_addr_t internetadresse; ip_addr_set_ip4_u32(&internetadresse, lwip_htonl(mail));
    streng_data->peer_mail = mail; streng_data->peer_slutpunkt_tal = portnummer;
    err_t 보조항목 = tcp_connect(streng_data->forbindelse_kontrol, &internetadresse, portnummer, 연결됨); return 보조항목 ? fejlnummer(보조항목) : -115;
}
int NET_acceptere(int fil_handle) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data || !streng_data->modtage_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].Type_område == 1 && 통신끝점들[순번].it_Afventer == fil_handle) { 통신끝점들[순번].it_Afventer = -1; return 순번; }
    return -11;
}
int 통신읽기(int fil_handle, void *data, unsigned vare_TÆL) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data || streng_data->Type_område != 1) return -9;
    if (!vare_TÆL) return 0; if (!streng_data->post_TÆL_8f7753a1) return streng_data->fejl ? streng_data->fejl : streng_data->fil_afslutte_et_opkald ? 0 : -11;
    if (vare_TÆL > streng_data->post_TÆL_8f7753a1) vare_TÆL = streng_data->post_TÆL_8f7753a1;
    for (unsigned 순번 = 0; 순번 < vare_TÆL; 순번++) { ((unsigned char *)data)[순번] = streng_data->data[streng_data->frontvendt_post]; streng_data->frontvendt_post = (streng_data->frontvendt_post + 1) % sizeof(streng_data->data); }
    streng_data->post_TÆL_8f7753a1 -= vare_TÆL; if (streng_data->forbindelse_kontrol) tcp_recved(streng_data->forbindelse_kontrol, vare_TÆL); return vare_TÆL;
}
int NET_skrive(int fil_handle, const void *data, unsigned vare_TÆL) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data || streng_data->Type_område != 1) return -9;
    if (streng_data->fejl) return streng_data->fejl; if (!streng_data->forbindelse_kontrol || !streng_data->연결됨) return -107;
    if (!vare_TÆL) return 0; if (vare_TÆL > tcp_sndbuf(streng_data->forbindelse_kontrol)) vare_TÆL = tcp_sndbuf(streng_data->forbindelse_kontrol);
    if (!vare_TÆL) return -11; if (vare_TÆL > 1024) vare_TÆL = 1024;
    err_t 보조항목 = tcp_write(streng_data->forbindelse_kontrol, data, vare_TÆL, TCP_WRITE_FLAG_COPY); if (보조항목) return fejlnummer(보조항목);
    tcp_output(streng_data->forbindelse_kontrol); return vare_TÆL;
}
int maile_datagram(int fil_handle, const void *data, unsigned vare_TÆL, uint32_t mail, unsigned portnummer) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data || streng_data->Type_område != 2) return -9;
    if (vare_TÆL > 512) return -90; if (!portnummer || portnummer > 65535) return -22;
    struct pbuf *data_placere = pbuf_alloc(PBUF_TRANSPORT, vare_TÆL, PBUF_RAM); if (!data_placere) return -11;
    pbuf_take(data_placere, data, vare_TÆL); ip_addr_t internetadresse; ip_addr_set_ip4_u32(&internetadresse, lwip_htonl(mail));
    err_t 보조항목 = udp_sendto(streng_data->datagram_kontrol, data_placere, &internetadresse, portnummer); pbuf_free(data_placere); return 보조항목 ? fejlnummer(보조항목) : (int)vare_TÆL;
}
int modtage_datagram(int fil_handle, void *data, unsigned vare_TÆL) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data || streng_data->Type_område != 2) return -9;
    if (!streng_data->post_TÆL_8f7753a1) return -11; unsigned aktuel_placere = streng_data->frontvendt_post;
    if (vare_TÆL > streng_data->길이목록[aktuel_placere]) vare_TÆL = streng_data->길이목록[aktuel_placere]; memcpy(data, streng_data->data + aktuel_placere * 512, vare_TÆL);
    streng_data->peer_slutpunkt_tal = streng_data->접속번호들[aktuel_placere]; streng_data->peer_mail = streng_data->주소목록[aktuel_placere]; streng_data->frontvendt_post = (aktuel_placere + 1) % 4; streng_data->post_TÆL_8f7753a1--; return vare_TÆL;
}
unsigned netværk_portnummer(int fil_handle) { socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); return !streng_data ? 0 : streng_data->forbindelse_kontrol ? streng_data->forbindelse_kontrol->local_port : streng_data->datagram_kontrol ? streng_data->datagram_kontrol->local_port : 0; }
unsigned peer_portnummer(int fil_handle) { socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); return streng_data ? streng_data->peer_slutpunkt_tal : 0; }
uint32_t NET_peer_mail(int fil_handle) { socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); return streng_data ? streng_data->peer_mail : 0; }
void Luk_netværk(int fil_handle) {
    socket_slutpunkt_3db661a2 *streng_data = hente_VÆRDI(fil_handle); if (!streng_data) return;
    if (streng_data->modtage_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].Type_område && 통신끝점들[순번].it_Afventer == fil_handle) Luk_netværk(순번);
    if (streng_data->forbindelse_kontrol) {
        tcp_arg(streng_data->forbindelse_kontrol, 0); if (streng_data->modtage_port) tcp_accept(streng_data->forbindelse_kontrol, 0); else { tcp_recv(streng_data->forbindelse_kontrol, 0); tcp_err(streng_data->forbindelse_kontrol, 0); }
        if (tcp_close(streng_data->forbindelse_kontrol) != ERR_OK) tcp_abort(streng_data->forbindelse_kontrol);
    }
    if (streng_data->datagram_kontrol) udp_remove(streng_data->datagram_kontrol); streng_data->Type_område = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || forespørgsel) return; forespørgsel = 1;
    if(brug_traditionel_netværk)유선망살피기(&forbindelse_enhed);
    for (unsigned budget = 0; !brug_traditionel_netværk && budget < 4096 && (maskine_register(보조장치 + 0x54) & 1); budget++) {
        unsigned tegnkode = maskine_register(보조장치 + 0x40) & 255;
        if (tegnkode == 192) {
            if (modtage_brug && !modtage_fejl && !수신탈출) {
                struct pbuf *data_placere = pbuf_alloc(PBUF_RAW, modtage_brug, PBUF_POOL);
                if (data_placere) { MODTAGET_VED_UDLØB_datagram_TÆL++; MODTAGET_VED_UDLØB_byte_TÆL += modtage_brug; pbuf_take(data_placere, modtage_data_buffer, modtage_brug); if (forbindelse_enhed.input(data_placere, &forbindelse_enhed) != ERR_OK) { 버린전문수++; pbuf_free(data_placere); } }
                else 버린전문수++;
            }
            else if (modtage_brug) 버린전문수++;
            modtage_brug = modtage_fejl = 수신탈출 = 0;
        } else if (tegnkode == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (tegnkode != 220 && tegnkode != 221) modtage_fejl = 1; tegnkode = tegnkode == 220 ? 192 : 219; 수신탈출 = 0; }
            if (modtage_brug < sizeof(modtage_data_buffer)) modtage_data_buffer[modtage_brug++] = tegnkode; else modtage_fejl = 1;
        }
    }
    netif_poll(&forbindelse_enhed); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budget = 0; budget < 4096 && 송신개수 && (maskine_register(보조장치 + 0x54) & 0x20); budget++) {
        maskine_register(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    forespørgsel = 0;
}

/* Indstillinger·조회는 lwIP의 faktisk_data 인터페이스와 afslutte_et_opkald_pege 표를 사용한다. */
uint32_t 망상태읽기(unsigned post_VÆRDI_962f286b, unsigned INDEKS) {
    if(post_VÆRDI_962f286b==20)return brug_traditionel_netværk;
    if(post_VÆRDI_962f286b==21)return 준비됨&&netif_is_link_up(&forbindelse_enhed);
    if(post_VÆRDI_962f286b==22)return brug_traditionel_netværk?traditionel_netværk_Statistik(5):0;
    if (!준비됨) return 0;
    if(brug_traditionel_netværk&&post_VÆRDI_962f286b>=4&&post_VÆRDI_962f286b<=8)return traditionel_netværk_Statistik(post_VÆRDI_962f286b-4);
    if (post_VÆRDI_962f286b == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&forbindelse_enhed)));
    if (post_VÆRDI_962f286b == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&forbindelse_enhed)));
    if (post_VÆRDI_962f286b == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&forbindelse_enhed)));
    if (post_VÆRDI_962f286b == 3) return netif_is_up(&forbindelse_enhed) != 0;
    if (post_VÆRDI_962f286b == 4) return MODTAGET_VED_UDLØB_datagram_TÆL;
    if (post_VÆRDI_962f286b == 5) return 보낸전문수;
    if (post_VÆRDI_962f286b == 6) return MODTAGET_VED_UDLØB_byte_TÆL;
    if (post_VÆRDI_962f286b == 7) return 보낸바이트수;
    if (post_VÆRDI_962f286b == 8) return 버린전문수;
    if (post_VÆRDI_962f286b == 9) return 송신개수;
    if (INDEKS >= 32) return 0;
    socket_slutpunkt_3db661a2 *afslutte_et_opkald_pege = &통신끝점들[INDEKS];
    if (post_VÆRDI_962f286b == 10) return afslutte_et_opkald_pege->Type_område;
    if (!afslutte_et_opkald_pege->Type_område) return 0;
    if (post_VÆRDI_962f286b == 11) return netværk_portnummer(INDEKS);
    if (post_VÆRDI_962f286b == 12) return afslutte_et_opkald_pege->peer_mail;
    if (post_VÆRDI_962f286b == 13) return afslutte_et_opkald_pege->peer_slutpunkt_tal;
    if (post_VÆRDI_962f286b == 14) return afslutte_et_opkald_pege->modtage_port ? 1 : afslutte_et_opkald_pege->fil_afslutte_et_opkald ? 3 : afslutte_et_opkald_pege->fejl ? 4 : afslutte_et_opkald_pege->연결됨 ? 2 : 0;
    if (post_VÆRDI_962f286b == 15) return afslutte_et_opkald_pege->post_TÆL_8f7753a1;
    if (post_VÆRDI_962f286b == 16) {
        const ip_addr_t *mail = afslutte_et_opkald_pege->Type_område == 1 && afslutte_et_opkald_pege->forbindelse_kontrol ? &afslutte_et_opkald_pege->forbindelse_kontrol->local_ip :
            afslutte_et_opkald_pege->Type_område == 2 && afslutte_et_opkald_pege->datagram_kontrol ? &afslutte_et_opkald_pege->datagram_kontrol->local_ip : 0;
        return mail ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(mail))) : 0;
    }
    return 0;
}

int konfigurere_netværk(unsigned Handling, uint32_t mail, uint32_t maske_VÆRDI, uint32_t gateway_VÆRDI) {
    if (!준비됨) return -100;
    if (Handling == 1) { netif_set_up(&forbindelse_enhed); return 0; }
    if (Handling == 2) { netif_set_down(&forbindelse_enhed); return 0; }
    if (Handling != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maske_VÆRDI, 같은 망의 선택적 standardværdi gateway_VÆRDI. */
    uint32_t 뒤집은가림 = ~maske_VÆRDI;
    if (!maske_VÆRDI || (뒤집은가림 & (뒤집은가림 + 1)) || !mail || (mail >> 24) == 127 ||
        (mail >> 24) == 0 || (mail >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(mail & 뒤집은가림) || (mail & 뒤집은가림) == 뒤집은가림)) ||
        (gateway_VÆRDI && ((gateway_VÆRDI & maske_VÆRDI) != (mail & maske_VÆRDI) || gateway_VÆRDI == mail || (gateway_VÆRDI >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(gateway_VÆRDI & 뒤집은가림) || (gateway_VÆRDI & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 mail 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEKS = 0; INDEKS < 32; INDEKS++) if (통신끝점들[INDEKS].Type_område &&
        !(통신끝점들[INDEKS].modtage_port && 통신끝점들[INDEKS].forbindelse_kontrol && ip_addr_isany(&통신끝점들[INDEKS].forbindelse_kontrol->local_ip))) return -16;
    if(brug_traditionel_netværk)dhcp_stop(&forbindelse_enhed);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(mail)); ip4_addr_set_u32(&새가림, lwip_htonl(maske_VÆRDI)); ip4_addr_set_u32(&새관문, lwip_htonl(gateway_VÆRDI));
    netif_set_addr(&forbindelse_enhed, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *svar_slutpunkt;
static uint32_t test_mail, test_TID, svartid;
static unsigned test_SEKVENS, test_identifikator, svar_SEKVENS;
static int svar_status;
static u8_t 응답받음(void *Argumenter, struct raw_pcb *afslutte_et_opkald_pege, struct pbuf *data, const ip_addr_t *mail) {
    (void)Argumenter; (void)afslutte_et_opkald_pege;
    unsigned char 머리[20], svar[16];
    if (svar_status != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(mail))) != test_mail || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned Header_tilpasse_størrelse = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Header_tilpasse_størrelse < 20 || data->tot_len < Header_tilpasse_størrelse + 16 ||
        pbuf_copy_partial(data, svar, 16, Header_tilpasse_størrelse) != 16 || svar[0] || svar[1] ||
        (((unsigned)svar[4] << 8) | svar[5]) != test_identifikator ||
        (((unsigned)svar[6] << 8) | svar[7]) != test_SEKVENS ||
        svar[8] != 'J' || svar[9] != 'K' || svar[10] != 'O' || svar[11] != 'S' ||
        (((uint32_t)svar[12] << 24) | ((uint32_t)svar[13] << 16) | ((uint32_t)svar[14] << 8) | svar[15]) != test_TID) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, Header_tilpasse_størrelse)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, Header_tilpasse_størrelse); return 0; }
    svartid = (uint32_t)보드밀리초() - test_TID; svar_SEKVENS = 머리[8]; svar_status = 0;
    pbuf_free(data); return 1;
}
int START_svar_test(uint32_t mail, unsigned ordre_VÆRDI) {
    if (!준비됨 || !netif_is_up(&forbindelse_enhed)) return -100;
    if (!mail || (mail >> 28) >= 14 || mail == 0xffffffffu) return -22;
    if (!svar_slutpunkt) { svar_slutpunkt = raw_new(IP_PROTO_ICMP); if (!svar_slutpunkt) return -12; raw_recv(svar_slutpunkt, 응답받음, 0); }
    test_mail = mail; test_SEKVENS = ordre_VÆRDI & 65535; test_identifikator = (test_identifikator + 1) & 65535;
    test_TID = 보드밀리초(); svar_status = -11; svartid = svar_SEKVENS = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = test_identifikator >> 8; data[5] = test_identifikator; data[6] = test_SEKVENS >> 8; data[7] = test_SEKVENS;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=test_TID >> 24; data[13]=test_TID >> 16; data[14]=test_TID >> 8; data[15]=test_TID;
    for (unsigned positionsindeks = 16; positionsindeks < sizeof(data); positionsindeks++) data[positionsindeks] = positionsindeks;
    uint16_t bekræftelse_kontrolsum = inet_chksum(data, sizeof(data)); memcpy(data + 2, &bekræftelse_kontrolsum, 2);
    struct pbuf *datagram = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!datagram) return -12;
    pbuf_take(datagram, data, sizeof(data)); ip_addr_t destination_slutpunkt; ip_addr_set_ip4_u32(&destination_slutpunkt, lwip_htonl(mail));
    err_t 처리값 = raw_sendto(svar_slutpunkt, datagram, &destination_slutpunkt); pbuf_free(datagram);
    if (처리값) svar_status = fejlnummer(처리값);
    return 처리값 ? svar_status : 0;
}
int 응답시험읽기(unsigned post_VÆRDI_962f286b) {
    통신망살피기();
    return post_VÆRDI_962f286b == 0 ? svar_status : post_VÆRDI_962f286b == 1 ? (int)svartid : post_VÆRDI_962f286b == 2 ? (int)svar_SEKVENS : -22;
}
