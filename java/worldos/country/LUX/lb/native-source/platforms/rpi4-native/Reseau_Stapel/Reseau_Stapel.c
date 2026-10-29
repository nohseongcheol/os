#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "Reseau_Stapel.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../extern_VALUE/extern_VALUE.h"
#include "verkabelt_Reseau.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define Computer_registréieren(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif Verbindung_Mobil;
static int 준비됨, 살피는중;
static int 유선사용;
static unsigned 수신사용량, 수신탈출, 수신오류;
static unsigned char 수신자료[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t 받은전문수, 보낸전문수, RECEIVED_Byte_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_Kategorie, 수신창구, 대기중, 연결됨, Fichier_bëennegen, Feeler;
    struct tcp_pcb *Verbindung_Kontroll;
    struct udp_pcb *전문제어;
    unsigned 맨앞, Agab_COUNT;
    unsigned char Daten[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], Peer_Adress;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int 오류번호(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *얻기(int Fichier_Handle) { return Fichier_Handle >= 0 && Fichier_Handle < 32 && 통신끝점들[Fichier_Handle].TYPE_Kategorie ? &통신끝점들[Fichier_Handle] : 0; }
static int 예약하기(int TYPE_Kategorie) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_Kategorie) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_Kategorie = TYPE_Kategorie; 통신끝점들[순번].대기중 = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned Zeechecode) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = Zeechecode; }
static err_t 출력결과(struct netif *Element_COUNT, struct pbuf *Daten_positionéieren, const ip4_addr_t *Adress) {
    (void)Element_COUNT; (void)Adress;
    if (Daten_positionéieren->tot_len > 1500 || 송신개수 + 2 * Daten_positionéieren->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Weider_OFFSET = Daten_positionéieren; Weider_OFFSET; Weider_OFFSET = Weider_OFFSET->next) for (unsigned 순번 = 0; 순번 < Weider_OFFSET->len; 순번++) {
        unsigned Zeechecode = ((unsigned char *)Weider_OFFSET->payload)[순번];
        if (Zeechecode == 192 || Zeechecode == 219) { 내보내기(219); 내보내기(Zeechecode == 192 ? 220 : 221); } else 내보내기(Zeechecode);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += Daten_positionéieren->tot_len; return ERR_OK;
}
static err_t Préparéieren_Common_Language_Runtime(struct netif *Element_COUNT) { Element_COUNT->name[0] = 's'; Element_COUNT->name[1] = 'l'; Element_COUNT->mtu = 1500; Element_COUNT->output = 출력결과; return ERR_OK; }
void Préparéieren_Reseau(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    Computer_registréieren(보조장치 + 4) |= 1; Computer_registréieren(보조장치 + 0x60) = 0; Computer_registréieren(보조장치 + 0x44) = 0;
    Computer_registréieren(보조장치 + 0x48) = 0xc6; Computer_registréieren(보조장치 + 0x4c) = 3; Computer_registréieren(보조장치 + 0x68) = 270; Computer_registréieren(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internetsadress, Bit_Mask, Gateway_Adress;
    유선사용=유선장치있음();
    ip4_addr_set_u32(&Internetsadress, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&Bit_Mask, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&Gateway_Adress, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&Verbindung_Mobil, &Internetsadress, &Bit_Mask, &Gateway_Adress, 0, 유선사용?Préparéieren_verkabelt_Reseau:Préparéieren_Common_Language_Runtime, 유선사용?ethernet_input:ip4_input))return;
    netif_set_default(&Verbindung_Mobil); netif_set_up(&Verbindung_Mobil);if(!유선사용)netif_set_link_up(&Verbindung_Mobil); 준비됨 = 1;
    Préparéieren_extern();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *Transmissioun_Kontroll_blockéieren, struct pbuf *Daten_positionéieren, err_t Feeler) {
    통신끝점 *Zeechefolleg_Daten = 부가인수; (void)Transmissioun_Kontroll_blockéieren; (void)Feeler;
    if (!Daten_positionéieren) { Zeechefolleg_Daten->Fichier_bëennegen = 1; return ERR_OK; }
    if (Daten_positionéieren->tot_len > sizeof(Zeechefolleg_Daten->Daten) - Zeechefolleg_Daten->Agab_COUNT) return ERR_MEM;
    unsigned 현재위치 = (Zeechefolleg_Daten->맨앞 + Zeechefolleg_Daten->Agab_COUNT) % sizeof(Zeechefolleg_Daten->Daten);
    for (struct pbuf *Weider_OFFSET = Daten_positionéieren; Weider_OFFSET; Weider_OFFSET = Weider_OFFSET->next) for (unsigned 순번 = 0; 순번 < Weider_OFFSET->len; 순번++) {
        Zeechefolleg_Daten->Daten[현재위치] = ((unsigned char *)Weider_OFFSET->payload)[순번]; 현재위치 = (현재위치 + 1) % sizeof(Zeechefolleg_Daten->Daten);
    }
    Zeechefolleg_Daten->Agab_COUNT += Daten_positionéieren->tot_len; pbuf_free(Daten_positionéieren); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Feeler) { 통신끝점 *Zeechefolleg_Daten = 부가인수; Zeechefolleg_Daten->Verbindung_Kontroll = 0; Zeechefolleg_Daten->Feeler = 오류번호(Feeler); }
static void 되부름목록(통신끝점 *Zeechefolleg_Daten) { tcp_arg(Zeechefolleg_Daten->Verbindung_Kontroll, Zeechefolleg_Daten); tcp_recv(Zeechefolleg_Daten->Verbindung_Kontroll, 수신됨); tcp_err(Zeechefolleg_Daten->Verbindung_Kontroll, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *Transmissioun_Kontroll_blockéieren, err_t Feeler) {
    통신끝점 *Zeechefolleg_Daten = 부가인수; (void)Transmissioun_Kontroll_blockéieren; if (Feeler) Zeechefolleg_Daten->Feeler = 오류번호(Feeler); else Zeechefolleg_Daten->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *Transmissioun_Kontroll_blockéieren, err_t Feeler) {
    통신끝점 *부모항목 = 부가인수; if (Feeler) return Feeler;
    int Fichier_Handle = 예약하기(1); if (Fichier_Handle < 0) return ERR_MEM;
    통신끝점 *Zeechefolleg_Daten = &통신끝점들[Fichier_Handle]; Zeechefolleg_Daten->Verbindung_Kontroll = Transmissioun_Kontroll_blockéieren; Zeechefolleg_Daten->연결됨 = 1; Zeechefolleg_Daten->대기중 = (int)(부모항목 - 통신끝점들);
    Zeechefolleg_Daten->Peer_Adress = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&Transmissioun_Kontroll_blockéieren->remote_ip))); Zeechefolleg_Daten->상대창구번호 = Transmissioun_Kontroll_blockéieren->remote_port;
    되부름목록(Zeechefolleg_Daten); return ERR_OK;
}
static void 전문(void *부가인수, struct udp_pcb *Transmissioun_Kontroll_blockéieren, struct pbuf *Daten_positionéieren, const ip_addr_t *Adress, u16_t 접속번호) {
    통신끝점 *Zeechefolleg_Daten = 부가인수; (void)Transmissioun_Kontroll_blockéieren;
    if (Zeechefolleg_Daten->Agab_COUNT < 4 && Daten_positionéieren->tot_len <= 512) {
        unsigned positionéieren_INDEX = (Zeechefolleg_Daten->맨앞 + Zeechefolleg_Daten->Agab_COUNT) % 4;
        pbuf_copy_partial(Daten_positionéieren, Zeechefolleg_Daten->Daten + positionéieren_INDEX * 512, Daten_positionéieren->tot_len, 0);
        Zeechefolleg_Daten->길이목록[positionéieren_INDEX] = Daten_positionéieren->tot_len; Zeechefolleg_Daten->접속번호들[positionéieren_INDEX] = 접속번호;
        Zeechefolleg_Daten->주소목록[positionéieren_INDEX] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adress))); Zeechefolleg_Daten->Agab_COUNT++;
    }
    pbuf_free(Daten_positionéieren);
}
int 통신끝점만들기(int TYPE_Kategorie) {
    if (!준비됨) return -100;
    if (TYPE_Kategorie != 1 && TYPE_Kategorie != 2) return -93;
    int Fichier_Handle = 예약하기(TYPE_Kategorie); if (Fichier_Handle < 0) return Fichier_Handle;
    통신끝점 *Zeechefolleg_Daten = &통신끝점들[Fichier_Handle];
    if (TYPE_Kategorie == 1) { Zeechefolleg_Daten->Verbindung_Kontroll = tcp_new(); if (Zeechefolleg_Daten->Verbindung_Kontroll) 되부름목록(Zeechefolleg_Daten); }
    else { Zeechefolleg_Daten->전문제어 = udp_new(); if (Zeechefolleg_Daten->전문제어) udp_recv(Zeechefolleg_Daten->전문제어, 전문, Zeechefolleg_Daten); }
    if (!Zeechefolleg_Daten->Verbindung_Kontroll && !Zeechefolleg_Daten->전문제어) { Zeechefolleg_Daten->TYPE_Kategorie = 0; return -12; } return Fichier_Handle;
}
int 망주소묶기(int Fichier_Handle, uint32_t Adress, unsigned 접속번호) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten) return -9;
    if (접속번호 > 65535 || (Adress && Adress != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&Verbindung_Mobil))) && Adress != 0x7f000001)) return -99;
    ip_addr_t Internetsadress; ip_addr_set_ip4_u32(&Internetsadress, lwip_htonl(Adress));
    err_t 보조항목 = Zeechefolleg_Daten->TYPE_Kategorie == 1 ? tcp_bind(Zeechefolleg_Daten->Verbindung_Kontroll, &Internetsadress, 접속번호) : udp_bind(Zeechefolleg_Daten->전문제어, &Internetsadress, 접속번호); return 보조항목 ? 오류번호(보조항목) : 0;
}
void 통신주소재사용(int Fichier_Handle) { 통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (Zeechefolleg_Daten && Zeechefolleg_Daten->Verbindung_Kontroll) ip_set_option(Zeechefolleg_Daten->Verbindung_Kontroll, SOF_REUSEADDR); }
int 연결기다리기(int Fichier_Handle) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten || Zeechefolleg_Daten->TYPE_Kategorie != 1) return -9;
    if (Zeechefolleg_Daten->수신창구) return 0;
    err_t 보조항목; struct tcp_pcb *Transmissioun_Kontroll_blockéieren = tcp_listen_with_backlog_and_err(Zeechefolleg_Daten->Verbindung_Kontroll, 4, &보조항목);
    if (!Transmissioun_Kontroll_blockéieren) return 오류번호(보조항목); Zeechefolleg_Daten->Verbindung_Kontroll = Transmissioun_Kontroll_blockéieren; Zeechefolleg_Daten->수신창구 = 1; tcp_arg(Transmissioun_Kontroll_blockéieren, Zeechefolleg_Daten); tcp_accept(Transmissioun_Kontroll_blockéieren, 연결받음); return 0;
}
int 망연결하기(int Fichier_Handle, uint32_t Adress, unsigned 접속번호) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten || Zeechefolleg_Daten->TYPE_Kategorie != 1) return -9;
    if (Zeechefolleg_Daten->Feeler) return Zeechefolleg_Daten->Feeler;
    if (Zeechefolleg_Daten->연결됨) return 0;
    if (Zeechefolleg_Daten->상대창구번호) return -115;
    if (!접속번호 || 접속번호 > 65535 || !Adress) return -22;
    ip_addr_t Internetsadress; ip_addr_set_ip4_u32(&Internetsadress, lwip_htonl(Adress));
    Zeechefolleg_Daten->Peer_Adress = Adress; Zeechefolleg_Daten->상대창구번호 = 접속번호;
    err_t 보조항목 = tcp_connect(Zeechefolleg_Daten->Verbindung_Kontroll, &Internetsadress, 접속번호, 연결됨); return 보조항목 ? 오류번호(보조항목) : -115;
}
int 망연결받기(int Fichier_Handle) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten || !Zeechefolleg_Daten->수신창구) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_Kategorie == 1 && 통신끝점들[순번].대기중 == Fichier_Handle) { 통신끝점들[순번].대기중 = -1; return 순번; }
    return -11;
}
int 통신읽기(int Fichier_Handle, void *Daten, unsigned Element_COUNT) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten || Zeechefolleg_Daten->TYPE_Kategorie != 1) return -9;
    if (!Element_COUNT) return 0; if (!Zeechefolleg_Daten->Agab_COUNT) return Zeechefolleg_Daten->Feeler ? Zeechefolleg_Daten->Feeler : Zeechefolleg_Daten->Fichier_bëennegen ? 0 : -11;
    if (Element_COUNT > Zeechefolleg_Daten->Agab_COUNT) Element_COUNT = Zeechefolleg_Daten->Agab_COUNT;
    for (unsigned 순번 = 0; 순번 < Element_COUNT; 순번++) { ((unsigned char *)Daten)[순번] = Zeechefolleg_Daten->Daten[Zeechefolleg_Daten->맨앞]; Zeechefolleg_Daten->맨앞 = (Zeechefolleg_Daten->맨앞 + 1) % sizeof(Zeechefolleg_Daten->Daten); }
    Zeechefolleg_Daten->Agab_COUNT -= Element_COUNT; if (Zeechefolleg_Daten->Verbindung_Kontroll) tcp_recved(Zeechefolleg_Daten->Verbindung_Kontroll, Element_COUNT); return Element_COUNT;
}
int 통신쓰기(int Fichier_Handle, const void *Daten, unsigned Element_COUNT) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten || Zeechefolleg_Daten->TYPE_Kategorie != 1) return -9;
    if (Zeechefolleg_Daten->Feeler) return Zeechefolleg_Daten->Feeler; if (!Zeechefolleg_Daten->Verbindung_Kontroll || !Zeechefolleg_Daten->연결됨) return -107;
    if (!Element_COUNT) return 0; if (Element_COUNT > tcp_sndbuf(Zeechefolleg_Daten->Verbindung_Kontroll)) Element_COUNT = tcp_sndbuf(Zeechefolleg_Daten->Verbindung_Kontroll);
    if (!Element_COUNT) return -11; if (Element_COUNT > 1024) Element_COUNT = 1024;
    err_t 보조항목 = tcp_write(Zeechefolleg_Daten->Verbindung_Kontroll, Daten, Element_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return 오류번호(보조항목);
    tcp_output(Zeechefolleg_Daten->Verbindung_Kontroll); return Element_COUNT;
}
int 전문보내기(int Fichier_Handle, const void *Daten, unsigned Element_COUNT, uint32_t Adress, unsigned 접속번호) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten || Zeechefolleg_Daten->TYPE_Kategorie != 2) return -9;
    if (Element_COUNT > 512) return -90; if (!접속번호 || 접속번호 > 65535) return -22;
    struct pbuf *Daten_positionéieren = pbuf_alloc(PBUF_TRANSPORT, Element_COUNT, PBUF_RAM); if (!Daten_positionéieren) return -11;
    pbuf_take(Daten_positionéieren, Daten, Element_COUNT); ip_addr_t Internetsadress; ip_addr_set_ip4_u32(&Internetsadress, lwip_htonl(Adress));
    err_t 보조항목 = udp_sendto(Zeechefolleg_Daten->전문제어, Daten_positionéieren, &Internetsadress, 접속번호); pbuf_free(Daten_positionéieren); return 보조항목 ? 오류번호(보조항목) : (int)Element_COUNT;
}
int 전문받기(int Fichier_Handle, void *Daten, unsigned Element_COUNT) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten || Zeechefolleg_Daten->TYPE_Kategorie != 2) return -9;
    if (!Zeechefolleg_Daten->Agab_COUNT) return -11; unsigned 현재위치 = Zeechefolleg_Daten->맨앞;
    if (Element_COUNT > Zeechefolleg_Daten->길이목록[현재위치]) Element_COUNT = Zeechefolleg_Daten->길이목록[현재위치]; memcpy(Daten, Zeechefolleg_Daten->Daten + 현재위치 * 512, Element_COUNT);
    Zeechefolleg_Daten->상대창구번호 = Zeechefolleg_Daten->접속번호들[현재위치]; Zeechefolleg_Daten->Peer_Adress = Zeechefolleg_Daten->주소목록[현재위치]; Zeechefolleg_Daten->맨앞 = (현재위치 + 1) % 4; Zeechefolleg_Daten->Agab_COUNT--; return Element_COUNT;
}
unsigned 통신접속번호(int Fichier_Handle) { 통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); return !Zeechefolleg_Daten ? 0 : Zeechefolleg_Daten->Verbindung_Kontroll ? Zeechefolleg_Daten->Verbindung_Kontroll->local_port : Zeechefolleg_Daten->전문제어 ? Zeechefolleg_Daten->전문제어->local_port : 0; }
unsigned 상대접속번호(int Fichier_Handle) { 통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); return Zeechefolleg_Daten ? Zeechefolleg_Daten->상대창구번호 : 0; }
uint32_t 상대통신주소(int Fichier_Handle) { 통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); return Zeechefolleg_Daten ? Zeechefolleg_Daten->Peer_Adress : 0; }
void Clôture_Reseau(int Fichier_Handle) {
    통신끝점 *Zeechefolleg_Daten = 얻기(Fichier_Handle); if (!Zeechefolleg_Daten) return;
    if (Zeechefolleg_Daten->수신창구) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_Kategorie && 통신끝점들[순번].대기중 == Fichier_Handle) Clôture_Reseau(순번);
    if (Zeechefolleg_Daten->Verbindung_Kontroll) {
        tcp_arg(Zeechefolleg_Daten->Verbindung_Kontroll, 0); if (Zeechefolleg_Daten->수신창구) tcp_accept(Zeechefolleg_Daten->Verbindung_Kontroll, 0); else { tcp_recv(Zeechefolleg_Daten->Verbindung_Kontroll, 0); tcp_err(Zeechefolleg_Daten->Verbindung_Kontroll, 0); }
        if (tcp_close(Zeechefolleg_Daten->Verbindung_Kontroll) != ERR_OK) tcp_abort(Zeechefolleg_Daten->Verbindung_Kontroll);
    }
    if (Zeechefolleg_Daten->전문제어) udp_remove(Zeechefolleg_Daten->전문제어); Zeechefolleg_Daten->TYPE_Kategorie = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || 살피는중) return; 살피는중 = 1;
    if(유선사용)유선망살피기(&Verbindung_Mobil);
    for (unsigned 처리한도 = 0; !유선사용 && 처리한도 < 4096 && (Computer_registréieren(보조장치 + 0x54) & 1); 처리한도++) {
        unsigned Zeechecode = Computer_registréieren(보조장치 + 0x40) & 255;
        if (Zeechecode == 192) {
            if (수신사용량 && !수신오류 && !수신탈출) {
                struct pbuf *Daten_positionéieren = pbuf_alloc(PBUF_RAW, 수신사용량, PBUF_POOL);
                if (Daten_positionéieren) { 받은전문수++; RECEIVED_Byte_COUNT += 수신사용량; pbuf_take(Daten_positionéieren, 수신자료, 수신사용량); if (Verbindung_Mobil.input(Daten_positionéieren, &Verbindung_Mobil) != ERR_OK) { 버린전문수++; pbuf_free(Daten_positionéieren); } }
                else 버린전문수++;
            }
            else if (수신사용량) 버린전문수++;
            수신사용량 = 수신오류 = 수신탈출 = 0;
        } else if (Zeechecode == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (Zeechecode != 220 && Zeechecode != 221) 수신오류 = 1; Zeechecode = Zeechecode == 220 ? 192 : 219; 수신탈출 = 0; }
            if (수신사용량 < sizeof(수신자료)) 수신자료[수신사용량++] = Zeechecode; else 수신오류 = 1;
        }
    }
    netif_poll(&Verbindung_Mobil); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned 처리한도 = 0; 처리한도 < 4096 && 송신개수 && (Computer_registréieren(보조장치 + 0x54) & 0x20); 처리한도++) {
        Computer_registréieren(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    살피는중 = 0;
}

/* Astellungen·조회는 lwIP의 aktuell_Daten 인터페이스와 bëennegen_Punkt 표를 사용한다. */
uint32_t 망상태읽기(unsigned Agab_VALUE, unsigned INDEX) {
    if(Agab_VALUE==20)return 유선사용;
    if(Agab_VALUE==21)return 준비됨&&netif_is_link_up(&Verbindung_Mobil);
    if(Agab_VALUE==22)return 유선사용?유선망집계(5):0;
    if (!준비됨) return 0;
    if(유선사용&&Agab_VALUE>=4&&Agab_VALUE<=8)return 유선망집계(Agab_VALUE-4);
    if (Agab_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&Verbindung_Mobil)));
    if (Agab_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&Verbindung_Mobil)));
    if (Agab_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&Verbindung_Mobil)));
    if (Agab_VALUE == 3) return netif_is_up(&Verbindung_Mobil) != 0;
    if (Agab_VALUE == 4) return 받은전문수;
    if (Agab_VALUE == 5) return 보낸전문수;
    if (Agab_VALUE == 6) return RECEIVED_Byte_COUNT;
    if (Agab_VALUE == 7) return 보낸바이트수;
    if (Agab_VALUE == 8) return 버린전문수;
    if (Agab_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *bëennegen_Punkt = &통신끝점들[INDEX];
    if (Agab_VALUE == 10) return bëennegen_Punkt->TYPE_Kategorie;
    if (!bëennegen_Punkt->TYPE_Kategorie) return 0;
    if (Agab_VALUE == 11) return 통신접속번호(INDEX);
    if (Agab_VALUE == 12) return bëennegen_Punkt->Peer_Adress;
    if (Agab_VALUE == 13) return bëennegen_Punkt->상대창구번호;
    if (Agab_VALUE == 14) return bëennegen_Punkt->수신창구 ? 1 : bëennegen_Punkt->Fichier_bëennegen ? 3 : bëennegen_Punkt->Feeler ? 4 : bëennegen_Punkt->연결됨 ? 2 : 0;
    if (Agab_VALUE == 15) return bëennegen_Punkt->Agab_COUNT;
    if (Agab_VALUE == 16) {
        const ip_addr_t *Adress = bëennegen_Punkt->TYPE_Kategorie == 1 && bëennegen_Punkt->Verbindung_Kontroll ? &bëennegen_Punkt->Verbindung_Kontroll->local_ip :
            bëennegen_Punkt->TYPE_Kategorie == 2 && bëennegen_Punkt->전문제어 ? &bëennegen_Punkt->전문제어->local_ip : 0;
        return Adress ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adress))) : 0;
    }
    return 0;
}

int konfiguréieren_Reseau(unsigned Aktioun, uint32_t Adress, uint32_t Mask_VALUE, uint32_t Gateway_VALUE) {
    if (!준비됨) return -100;
    if (Aktioun == 1) { netif_set_up(&Verbindung_Mobil); return 0; }
    if (Aktioun == 2) { netif_set_down(&Verbindung_Mobil); return 0; }
    if (Aktioun != 0) return -22;
    /* 유니캐스트 IPv4, 연속 Mask_VALUE, 같은 망의 선택적 Standardwäert Gateway_VALUE. */
    uint32_t 뒤집은가림 = ~Mask_VALUE;
    if (!Mask_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !Adress || (Adress >> 24) == 127 ||
        (Adress >> 24) == 0 || (Adress >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(Adress & 뒤집은가림) || (Adress & 뒤집은가림) == 뒤집은가림)) ||
        (Gateway_VALUE && ((Gateway_VALUE & Mask_VALUE) != (Adress & Mask_VALUE) || Gateway_VALUE == Adress || (Gateway_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(Gateway_VALUE & 뒤집은가림) || (Gateway_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 Adress 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_Kategorie &&
        !(통신끝점들[INDEX].수신창구 && 통신끝점들[INDEX].Verbindung_Kontroll && ip_addr_isany(&통신끝점들[INDEX].Verbindung_Kontroll->local_ip))) return -16;
    if(유선사용)dhcp_stop(&Verbindung_Mobil);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(Adress)); ip4_addr_set_u32(&새가림, lwip_htonl(Mask_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(Gateway_VALUE));
    netif_set_addr(&Verbindung_Mobil, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *응답끝점;
static uint32_t 시험주소, 시험시각, 응답시간;
static unsigned 시험순서, 시험식별자, 응답차례;
static int 응답상태;
static u8_t 응답받음(void *인수, struct raw_pcb *bëennegen_Punkt, struct pbuf *Daten, const ip_addr_t *Adress) {
    (void)인수; (void)bëennegen_Punkt;
    unsigned char 머리[20], äntweren[16];
    if (응답상태 != -11 || Daten->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(Adress))) != 시험주소 || pbuf_copy_partial(Daten, 머리, 20, 0) != 20) return 0;
    unsigned En_tête_d_Gréisst_veränneren = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || En_tête_d_Gréisst_veränneren < 20 || Daten->tot_len < En_tête_d_Gréisst_veränneren + 16 ||
        pbuf_copy_partial(Daten, äntweren, 16, En_tête_d_Gréisst_veränneren) != 16 || äntweren[0] || äntweren[1] ||
        (((unsigned)äntweren[4] << 8) | äntweren[5]) != 시험식별자 ||
        (((unsigned)äntweren[6] << 8) | äntweren[7]) != 시험순서 ||
        äntweren[8] != 'J' || äntweren[9] != 'K' || äntweren[10] != 'O' || äntweren[11] != 'S' ||
        (((uint32_t)äntweren[12] << 24) | ((uint32_t)äntweren[13] << 16) | ((uint32_t)äntweren[14] << 8) | äntweren[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(Daten, En_tête_d_Gréisst_veränneren)) return 0;
    if (inet_chksum_pbuf(Daten)) { pbuf_add_header(Daten, En_tête_d_Gréisst_veränneren); return 0; }
    응답시간 = (uint32_t)보드밀리초() - 시험시각; 응답차례 = 머리[8]; 응답상태 = 0;
    pbuf_free(Daten); return 1;
}
int 응답시험시작(uint32_t Adress, unsigned Reiefolleg_VALUE) {
    if (!준비됨 || !netif_is_up(&Verbindung_Mobil)) return -100;
    if (!Adress || (Adress >> 28) >= 14 || Adress == 0xffffffffu) return -22;
    if (!응답끝점) { 응답끝점 = raw_new(IP_PROTO_ICMP); if (!응답끝점) return -12; raw_recv(응답끝점, 응답받음, 0); }
    시험주소 = Adress; 시험순서 = Reiefolleg_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); 응답상태 = -11; 응답시간 = 응답차례 = 0;
    unsigned char Daten[32] = {8,0,0,0};
    Daten[4] = 시험식별자 >> 8; Daten[5] = 시험식별자; Daten[6] = 시험순서 >> 8; Daten[7] = 시험순서;
    Daten[8]='J'; Daten[9]='K'; Daten[10]='O'; Daten[11]='S';
    Daten[12]=시험시각 >> 24; Daten[13]=시험시각 >> 16; Daten[14]=시험시각 >> 8; Daten[15]=시험시각;
    for (unsigned positionéieren_INDEX = 16; positionéieren_INDEX < sizeof(Daten); positionéieren_INDEX++) Daten[positionéieren_INDEX] = positionéieren_INDEX;
    uint16_t 확인합 = inet_chksum(Daten, sizeof(Daten)); memcpy(Daten + 2, &확인합, 2);
    struct pbuf *전문 = pbuf_alloc(PBUF_IP, sizeof(Daten), PBUF_RAM); if (!전문) return -12;
    pbuf_take(전문, Daten, sizeof(Daten)); ip_addr_t 목적지; ip_addr_set_ip4_u32(&목적지, lwip_htonl(Adress));
    err_t 처리값 = raw_sendto(응답끝점, 전문, &목적지); pbuf_free(전문);
    if (처리값) 응답상태 = 오류번호(처리값);
    return 처리값 ? 응답상태 : 0;
}
int 응답시험읽기(unsigned Agab_VALUE) {
    통신망살피기();
    return Agab_VALUE == 0 ? 응답상태 : Agab_VALUE == 1 ? (int)응답시간 : Agab_VALUE == 2 ? (int)응답차례 : -22;
}
