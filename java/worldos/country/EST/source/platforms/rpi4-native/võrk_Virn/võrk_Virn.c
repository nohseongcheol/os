#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "võrk_Virn.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../kauge_VALUE/kauge_VALUE.h"
#include "juhtmega_ühendatud_võrk.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define arvuti_register(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif ühendus_seade;
static int 준비됨, pollimine;
static int kasutus_juhtmega_ühendatud_võrk;
static unsigned saama_kasutus, 수신탈출, saama_tõrge;
static unsigned char saama_andmepuhver[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_datagramm_COUNT, 보낸전문수, RECEIVED_bait_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_ala, saama_port, infotehnoloogia_ootel, 연결됨, Fail_lõpeta_kõne, VIGA;
    struct tcp_pcb *ühendus_meede;
    struct udp_pcb *datagramm_meede;
    unsigned esikaamera_kirje, kirje_COUNT;
    unsigned char andmed[4096];
    unsigned 길이목록[4], 접속번호들[4], partner_osaleja_number;
    uint32_t 주소목록[4], partner_ADDRESS;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int tõrke_number(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *tooma_VALUE(int Fail_pide) { return Fail_pide >= 0 && Fail_pide < 32 && 통신끝점들[Fail_pide].TYPE_ala ? &통신끝점들[Fail_pide] : 0; }
static int 예약하기(int TYPE_ala) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_ala) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_ala = TYPE_ala; 통신끝점들[순번].infotehnoloogia_ootel = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned koodipunkt) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = koodipunkt; }
static err_t toodang(struct netif *kaup_COUNT, struct pbuf *andmed_ametikoht, const ip4_addr_t *ADDRESS) {
    (void)kaup_COUNT; (void)ADDRESS;
    if (andmed_ametikoht->tot_len > 1500 || 송신개수 + 2 * andmed_ametikoht->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Edasi_nihe = andmed_ametikoht; Edasi_nihe; Edasi_nihe = Edasi_nihe->next) for (unsigned 순번 = 0; 순번 < Edasi_nihe->len; 순번++) {
        unsigned koodipunkt = ((unsigned char *)Edasi_nihe->payload)[순번];
        if (koodipunkt == 192 || koodipunkt == 219) { 내보내기(219); 내보내기(koodipunkt == 192 ? 220 : 221); } else 내보내기(koodipunkt);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += andmed_ametikoht->tot_len; return ERR_OK;
}
static err_t Ettevalmistamine_CLR(struct netif *kaup_COUNT) { kaup_COUNT->name[0] = 's'; kaup_COUNT->name[1] = 'l'; kaup_COUNT->mtu = 1500; kaup_COUNT->output = toodang; return ERR_OK; }
void Ettevalmistamine_võrk(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    arvuti_register(보조장치 + 4) |= 1; arvuti_register(보조장치 + 0x60) = 0; arvuti_register(보조장치 + 0x44) = 0;
    arvuti_register(보조장치 + 0x48) = 0xc6; arvuti_register(보조장치 + 0x4c) = 3; arvuti_register(보조장치 + 0x68) = 270; arvuti_register(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Interneti_aadress, bitimask, lüüsi_aadress;
    kasutus_juhtmega_ühendatud_võrk=유선장치있음();
    ip4_addr_set_u32(&Interneti_aadress, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitimask, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&lüüsi_aadress, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&ühendus_seade, &Interneti_aadress, &bitimask, &lüüsi_aadress, 0, kasutus_juhtmega_ühendatud_võrk?Ettevalmistamine_juhtmega_ühendatud_võrk:Ettevalmistamine_CLR, kasutus_juhtmega_ühendatud_võrk?ethernet_input:ip4_input))return;
    netif_set_default(&ühendus_seade); netif_set_up(&ühendus_seade);if(!kasutus_juhtmega_ühendatud_võrk)netif_set_link_up(&ühendus_seade); 준비됨 = 1;
    Ettevalmistamine_kauge();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *andmed_ametikoht, err_t VIGA) {
    통신끝점 *string_andmed = 부가인수; (void)통신제어블록; (void)VIGA;
    if (!andmed_ametikoht) { string_andmed->Fail_lõpeta_kõne = 1; return ERR_OK; }
    if (andmed_ametikoht->tot_len > sizeof(string_andmed->andmed) - string_andmed->kirje_COUNT) return ERR_MEM;
    unsigned tähtaja_piires_ametikoht = (string_andmed->esikaamera_kirje + string_andmed->kirje_COUNT) % sizeof(string_andmed->andmed);
    for (struct pbuf *Edasi_nihe = andmed_ametikoht; Edasi_nihe; Edasi_nihe = Edasi_nihe->next) for (unsigned 순번 = 0; 순번 < Edasi_nihe->len; 순번++) {
        string_andmed->andmed[tähtaja_piires_ametikoht] = ((unsigned char *)Edasi_nihe->payload)[순번]; tähtaja_piires_ametikoht = (tähtaja_piires_ametikoht + 1) % sizeof(string_andmed->andmed);
    }
    string_andmed->kirje_COUNT += andmed_ametikoht->tot_len; pbuf_free(andmed_ametikoht); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t VIGA) { 통신끝점 *string_andmed = 부가인수; string_andmed->ühendus_meede = 0; string_andmed->VIGA = tõrke_number(VIGA); }
static void 되부름목록(통신끝점 *string_andmed) { tcp_arg(string_andmed->ühendus_meede, string_andmed); tcp_recv(string_andmed->ühendus_meede, 수신됨); tcp_err(string_andmed->ühendus_meede, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t VIGA) {
    통신끝점 *string_andmed = 부가인수; (void)통신제어블록; if (VIGA) string_andmed->VIGA = tõrke_number(VIGA); else string_andmed->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t VIGA) {
    통신끝점 *ema = 부가인수; if (VIGA) return VIGA;
    int Fail_pide = 예약하기(1); if (Fail_pide < 0) return ERR_MEM;
    통신끝점 *string_andmed = &통신끝점들[Fail_pide]; string_andmed->ühendus_meede = 통신제어블록; string_andmed->연결됨 = 1; string_andmed->infotehnoloogia_ootel = (int)(ema - 통신끝점들);
    string_andmed->partner_ADDRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); string_andmed->partner_osaleja_number = 통신제어블록->remote_port;
    되부름목록(string_andmed); return ERR_OK;
}
static void datagramm(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *andmed_ametikoht, const ip_addr_t *ADDRESS, u16_t pordinumber) {
    통신끝점 *string_andmed = 부가인수; (void)통신제어블록;
    if (string_andmed->kirje_COUNT < 4 && andmed_ametikoht->tot_len <= 512) {
        unsigned asukohaindeks = (string_andmed->esikaamera_kirje + string_andmed->kirje_COUNT) % 4;
        pbuf_copy_partial(andmed_ametikoht, string_andmed->andmed + asukohaindeks * 512, andmed_ametikoht->tot_len, 0);
        string_andmed->길이목록[asukohaindeks] = andmed_ametikoht->tot_len; string_andmed->접속번호들[asukohaindeks] = pordinumber;
        string_andmed->주소목록[asukohaindeks] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))); string_andmed->kirje_COUNT++;
    }
    pbuf_free(andmed_ametikoht);
}
int 통신끝점만들기(int TYPE_ala) {
    if (!준비됨) return -100;
    if (TYPE_ala != 1 && TYPE_ala != 2) return -93;
    int Fail_pide = 예약하기(TYPE_ala); if (Fail_pide < 0) return Fail_pide;
    통신끝점 *string_andmed = &통신끝점들[Fail_pide];
    if (TYPE_ala == 1) { string_andmed->ühendus_meede = tcp_new(); if (string_andmed->ühendus_meede) 되부름목록(string_andmed); }
    else { string_andmed->datagramm_meede = udp_new(); if (string_andmed->datagramm_meede) udp_recv(string_andmed->datagramm_meede, datagramm, string_andmed); }
    if (!string_andmed->ühendus_meede && !string_andmed->datagramm_meede) { string_andmed->TYPE_ala = 0; return -12; } return Fail_pide;
}
int NET_BIND(int Fail_pide, uint32_t ADDRESS, unsigned pordinumber) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed) return -9;
    if (pordinumber > 65535 || (ADDRESS && ADDRESS != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ühendus_seade))) && ADDRESS != 0x7f000001)) return -99;
    ip_addr_t Interneti_aadress; ip_addr_set_ip4_u32(&Interneti_aadress, lwip_htonl(ADDRESS));
    err_t 보조항목 = string_andmed->TYPE_ala == 1 ? tcp_bind(string_andmed->ühendus_meede, &Interneti_aadress, pordinumber) : udp_bind(string_andmed->datagramm_meede, &Interneti_aadress, pordinumber); return 보조항목 ? tõrke_number(보조항목) : 0;
}
void 통신주소재사용(int Fail_pide) { 통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (string_andmed && string_andmed->ühendus_meede) ip_set_option(string_andmed->ühendus_meede, SOF_REUSEADDR); }
int NET_jälgima(int Fail_pide) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed || string_andmed->TYPE_ala != 1) return -9;
    if (string_andmed->saama_port) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(string_andmed->ühendus_meede, 4, &보조항목);
    if (!통신제어블록) return tõrke_number(보조항목); string_andmed->ühendus_meede = 통신제어블록; string_andmed->saama_port = 1; tcp_arg(통신제어블록, string_andmed); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_Ühenda(int Fail_pide, uint32_t ADDRESS, unsigned pordinumber) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed || string_andmed->TYPE_ala != 1) return -9;
    if (string_andmed->VIGA) return string_andmed->VIGA;
    if (string_andmed->연결됨) return 0;
    if (string_andmed->partner_osaleja_number) return -115;
    if (!pordinumber || pordinumber > 65535 || !ADDRESS) return -22;
    ip_addr_t Interneti_aadress; ip_addr_set_ip4_u32(&Interneti_aadress, lwip_htonl(ADDRESS));
    string_andmed->partner_ADDRESS = ADDRESS; string_andmed->partner_osaleja_number = pordinumber;
    err_t 보조항목 = tcp_connect(string_andmed->ühendus_meede, &Interneti_aadress, pordinumber, 연결됨); return 보조항목 ? tõrke_number(보조항목) : -115;
}
int NET_aktsepteerima(int Fail_pide) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed || !string_andmed->saama_port) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_ala == 1 && 통신끝점들[순번].infotehnoloogia_ootel == Fail_pide) { 통신끝점들[순번].infotehnoloogia_ootel = -1; return 순번; }
    return -11;
}
int 통신읽기(int Fail_pide, void *andmed, unsigned kaup_COUNT) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed || string_andmed->TYPE_ala != 1) return -9;
    if (!kaup_COUNT) return 0; if (!string_andmed->kirje_COUNT) return string_andmed->VIGA ? string_andmed->VIGA : string_andmed->Fail_lõpeta_kõne ? 0 : -11;
    if (kaup_COUNT > string_andmed->kirje_COUNT) kaup_COUNT = string_andmed->kirje_COUNT;
    for (unsigned 순번 = 0; 순번 < kaup_COUNT; 순번++) { ((unsigned char *)andmed)[순번] = string_andmed->andmed[string_andmed->esikaamera_kirje]; string_andmed->esikaamera_kirje = (string_andmed->esikaamera_kirje + 1) % sizeof(string_andmed->andmed); }
    string_andmed->kirje_COUNT -= kaup_COUNT; if (string_andmed->ühendus_meede) tcp_recved(string_andmed->ühendus_meede, kaup_COUNT); return kaup_COUNT;
}
int NET_kirjutamine(int Fail_pide, const void *andmed, unsigned kaup_COUNT) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed || string_andmed->TYPE_ala != 1) return -9;
    if (string_andmed->VIGA) return string_andmed->VIGA; if (!string_andmed->ühendus_meede || !string_andmed->연결됨) return -107;
    if (!kaup_COUNT) return 0; if (kaup_COUNT > tcp_sndbuf(string_andmed->ühendus_meede)) kaup_COUNT = tcp_sndbuf(string_andmed->ühendus_meede);
    if (!kaup_COUNT) return -11; if (kaup_COUNT > 1024) kaup_COUNT = 1024;
    err_t 보조항목 = tcp_write(string_andmed->ühendus_meede, andmed, kaup_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return tõrke_number(보조항목);
    tcp_output(string_andmed->ühendus_meede); return kaup_COUNT;
}
int saatma_datagramm(int Fail_pide, const void *andmed, unsigned kaup_COUNT, uint32_t ADDRESS, unsigned pordinumber) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed || string_andmed->TYPE_ala != 2) return -9;
    if (kaup_COUNT > 512) return -90; if (!pordinumber || pordinumber > 65535) return -22;
    struct pbuf *andmed_ametikoht = pbuf_alloc(PBUF_TRANSPORT, kaup_COUNT, PBUF_RAM); if (!andmed_ametikoht) return -11;
    pbuf_take(andmed_ametikoht, andmed, kaup_COUNT); ip_addr_t Interneti_aadress; ip_addr_set_ip4_u32(&Interneti_aadress, lwip_htonl(ADDRESS));
    err_t 보조항목 = udp_sendto(string_andmed->datagramm_meede, andmed_ametikoht, &Interneti_aadress, pordinumber); pbuf_free(andmed_ametikoht); return 보조항목 ? tõrke_number(보조항목) : (int)kaup_COUNT;
}
int saama_datagramm(int Fail_pide, void *andmed, unsigned kaup_COUNT) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed || string_andmed->TYPE_ala != 2) return -9;
    if (!string_andmed->kirje_COUNT) return -11; unsigned tähtaja_piires_ametikoht = string_andmed->esikaamera_kirje;
    if (kaup_COUNT > string_andmed->길이목록[tähtaja_piires_ametikoht]) kaup_COUNT = string_andmed->길이목록[tähtaja_piires_ametikoht]; memcpy(andmed, string_andmed->andmed + tähtaja_piires_ametikoht * 512, kaup_COUNT);
    string_andmed->partner_osaleja_number = string_andmed->접속번호들[tähtaja_piires_ametikoht]; string_andmed->partner_ADDRESS = string_andmed->주소목록[tähtaja_piires_ametikoht]; string_andmed->esikaamera_kirje = (tähtaja_piires_ametikoht + 1) % 4; string_andmed->kirje_COUNT--; return kaup_COUNT;
}
unsigned võrk_pordinumber(int Fail_pide) { 통신끝점 *string_andmed = tooma_VALUE(Fail_pide); return !string_andmed ? 0 : string_andmed->ühendus_meede ? string_andmed->ühendus_meede->local_port : string_andmed->datagramm_meede ? string_andmed->datagramm_meede->local_port : 0; }
unsigned partner_pordinumber(int Fail_pide) { 통신끝점 *string_andmed = tooma_VALUE(Fail_pide); return string_andmed ? string_andmed->partner_osaleja_number : 0; }
uint32_t NET_partner_ADDRESS(int Fail_pide) { 통신끝점 *string_andmed = tooma_VALUE(Fail_pide); return string_andmed ? string_andmed->partner_ADDRESS : 0; }
void Sule_võrk(int Fail_pide) {
    통신끝점 *string_andmed = tooma_VALUE(Fail_pide); if (!string_andmed) return;
    if (string_andmed->saama_port) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_ala && 통신끝점들[순번].infotehnoloogia_ootel == Fail_pide) Sule_võrk(순번);
    if (string_andmed->ühendus_meede) {
        tcp_arg(string_andmed->ühendus_meede, 0); if (string_andmed->saama_port) tcp_accept(string_andmed->ühendus_meede, 0); else { tcp_recv(string_andmed->ühendus_meede, 0); tcp_err(string_andmed->ühendus_meede, 0); }
        if (tcp_close(string_andmed->ühendus_meede) != ERR_OK) tcp_abort(string_andmed->ühendus_meede);
    }
    if (string_andmed->datagramm_meede) udp_remove(string_andmed->datagramm_meede); string_andmed->TYPE_ala = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || pollimine) return; pollimine = 1;
    if(kasutus_juhtmega_ühendatud_võrk)유선망살피기(&ühendus_seade);
    for (unsigned eelarve = 0; !kasutus_juhtmega_ühendatud_võrk && eelarve < 4096 && (arvuti_register(보조장치 + 0x54) & 1); eelarve++) {
        unsigned koodipunkt = arvuti_register(보조장치 + 0x40) & 255;
        if (koodipunkt == 192) {
            if (saama_kasutus && !saama_tõrge && !수신탈출) {
                struct pbuf *andmed_ametikoht = pbuf_alloc(PBUF_RAW, saama_kasutus, PBUF_POOL);
                if (andmed_ametikoht) { RECEIVED_datagramm_COUNT++; RECEIVED_bait_COUNT += saama_kasutus; pbuf_take(andmed_ametikoht, saama_andmepuhver, saama_kasutus); if (ühendus_seade.input(andmed_ametikoht, &ühendus_seade) != ERR_OK) { 버린전문수++; pbuf_free(andmed_ametikoht); } }
                else 버린전문수++;
            }
            else if (saama_kasutus) 버린전문수++;
            saama_kasutus = saama_tõrge = 수신탈출 = 0;
        } else if (koodipunkt == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (koodipunkt != 220 && koodipunkt != 221) saama_tõrge = 1; koodipunkt = koodipunkt == 220 ? 192 : 219; 수신탈출 = 0; }
            if (saama_kasutus < sizeof(saama_andmepuhver)) saama_andmepuhver[saama_kasutus++] = koodipunkt; else saama_tõrge = 1;
        }
    }
    netif_poll(&ühendus_seade); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned eelarve = 0; eelarve < 4096 && 송신개수 && (arvuti_register(보조장치 + 0x54) & 0x20); eelarve++) {
        arvuti_register(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    pollimine = 0;
}

/* Seaded·조회는 lwIP의 tegelik_andmed 인터페이스와 lõpeta_kõne_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned kirje_VALUE, unsigned INDEX) {
    if(kirje_VALUE==20)return kasutus_juhtmega_ühendatud_võrk;
    if(kirje_VALUE==21)return 준비됨&&netif_is_link_up(&ühendus_seade);
    if(kirje_VALUE==22)return kasutus_juhtmega_ühendatud_võrk?유선망집계(5):0;
    if (!준비됨) return 0;
    if(kasutus_juhtmega_ühendatud_võrk&&kirje_VALUE>=4&&kirje_VALUE<=8)return 유선망집계(kirje_VALUE-4);
    if (kirje_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ühendus_seade)));
    if (kirje_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&ühendus_seade)));
    if (kirje_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&ühendus_seade)));
    if (kirje_VALUE == 3) return netif_is_up(&ühendus_seade) != 0;
    if (kirje_VALUE == 4) return RECEIVED_datagramm_COUNT;
    if (kirje_VALUE == 5) return 보낸전문수;
    if (kirje_VALUE == 6) return RECEIVED_bait_COUNT;
    if (kirje_VALUE == 7) return 보낸바이트수;
    if (kirje_VALUE == 8) return 버린전문수;
    if (kirje_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *lõpeta_kõne_p = &통신끝점들[INDEX];
    if (kirje_VALUE == 10) return lõpeta_kõne_p->TYPE_ala;
    if (!lõpeta_kõne_p->TYPE_ala) return 0;
    if (kirje_VALUE == 11) return võrk_pordinumber(INDEX);
    if (kirje_VALUE == 12) return lõpeta_kõne_p->partner_ADDRESS;
    if (kirje_VALUE == 13) return lõpeta_kõne_p->partner_osaleja_number;
    if (kirje_VALUE == 14) return lõpeta_kõne_p->saama_port ? 1 : lõpeta_kõne_p->Fail_lõpeta_kõne ? 3 : lõpeta_kõne_p->VIGA ? 4 : lõpeta_kõne_p->연결됨 ? 2 : 0;
    if (kirje_VALUE == 15) return lõpeta_kõne_p->kirje_COUNT;
    if (kirje_VALUE == 16) {
        const ip_addr_t *ADDRESS = lõpeta_kõne_p->TYPE_ala == 1 && lõpeta_kõne_p->ühendus_meede ? &lõpeta_kõne_p->ühendus_meede->local_ip :
            lõpeta_kõne_p->TYPE_ala == 2 && lõpeta_kõne_p->datagramm_meede ? &lõpeta_kõne_p->datagramm_meede->local_ip : 0;
        return ADDRESS ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) : 0;
    }
    return 0;
}

int konfigureerima_võrk(unsigned Nimi, uint32_t ADDRESS, uint32_t mask_VALUE, uint32_t lüüs_VALUE) {
    if (!준비됨) return -100;
    if (Nimi == 1) { netif_set_up(&ühendus_seade); return 0; }
    if (Nimi == 2) { netif_set_down(&ühendus_seade); return 0; }
    if (Nimi != 0) return -22;
    /* 유니캐스트 IPv4, 연속 mask_VALUE, 같은 망의 선택적 vaikeväärtus lüüs_VALUE. */
    uint32_t 뒤집은가림 = ~mask_VALUE;
    if (!mask_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !ADDRESS || (ADDRESS >> 24) == 127 ||
        (ADDRESS >> 24) == 0 || (ADDRESS >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADDRESS & 뒤집은가림) || (ADDRESS & 뒤집은가림) == 뒤집은가림)) ||
        (lüüs_VALUE && ((lüüs_VALUE & mask_VALUE) != (ADDRESS & mask_VALUE) || lüüs_VALUE == ADDRESS || (lüüs_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(lüüs_VALUE & 뒤집은가림) || (lüüs_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADDRESS 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_ala &&
        !(통신끝점들[INDEX].saama_port && 통신끝점들[INDEX].ühendus_meede && ip_addr_isany(&통신끝점들[INDEX].ühendus_meede->local_ip))) return -16;
    if(kasutus_juhtmega_ühendatud_võrk)dhcp_stop(&ühendus_seade);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADDRESS)); ip4_addr_set_u32(&새가림, lwip_htonl(mask_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(lüüs_VALUE));
    netif_set_addr(&ühendus_seade, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *vastus_osaleja;
static uint32_t 시험주소, 시험시각, reaktsiooniaeg;
static unsigned 시험순서, 시험식별자, vastus_SEQUENCE;
static int vastus_Olek;
static u8_t 응답받음(void *Argumendid, struct raw_pcb *lõpeta_kõne_p, struct pbuf *andmed, const ip_addr_t *ADDRESS) {
    (void)Argumendid; (void)lõpeta_kõne_p;
    unsigned char 머리[20], vastus[16];
    if (vastus_Olek != -11 || andmed->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) != 시험주소 || pbuf_copy_partial(andmed, 머리, 20, 0) != 20) return 0;
    unsigned Päis_suurust_muutma = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Päis_suurust_muutma < 20 || andmed->tot_len < Päis_suurust_muutma + 16 ||
        pbuf_copy_partial(andmed, vastus, 16, Päis_suurust_muutma) != 16 || vastus[0] || vastus[1] ||
        (((unsigned)vastus[4] << 8) | vastus[5]) != 시험식별자 ||
        (((unsigned)vastus[6] << 8) | vastus[7]) != 시험순서 ||
        vastus[8] != 'J' || vastus[9] != 'K' || vastus[10] != 'O' || vastus[11] != 'S' ||
        (((uint32_t)vastus[12] << 24) | ((uint32_t)vastus[13] << 16) | ((uint32_t)vastus[14] << 8) | vastus[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(andmed, Päis_suurust_muutma)) return 0;
    if (inet_chksum_pbuf(andmed)) { pbuf_add_header(andmed, Päis_suurust_muutma); return 0; }
    reaktsiooniaeg = (uint32_t)보드밀리초() - 시험시각; vastus_SEQUENCE = 머리[8]; vastus_Olek = 0;
    pbuf_free(andmed); return 1;
}
int 응답시험시작(uint32_t ADDRESS, unsigned tellimus_VALUE) {
    if (!준비됨 || !netif_is_up(&ühendus_seade)) return -100;
    if (!ADDRESS || (ADDRESS >> 28) >= 14 || ADDRESS == 0xffffffffu) return -22;
    if (!vastus_osaleja) { vastus_osaleja = raw_new(IP_PROTO_ICMP); if (!vastus_osaleja) return -12; raw_recv(vastus_osaleja, 응답받음, 0); }
    시험주소 = ADDRESS; 시험순서 = tellimus_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); vastus_Olek = -11; reaktsiooniaeg = vastus_SEQUENCE = 0;
    unsigned char andmed[32] = {8,0,0,0};
    andmed[4] = 시험식별자 >> 8; andmed[5] = 시험식별자; andmed[6] = 시험순서 >> 8; andmed[7] = 시험순서;
    andmed[8]='J'; andmed[9]='K'; andmed[10]='O'; andmed[11]='S';
    andmed[12]=시험시각 >> 24; andmed[13]=시험시각 >> 16; andmed[14]=시험시각 >> 8; andmed[15]=시험시각;
    for (unsigned asukohaindeks = 16; asukohaindeks < sizeof(andmed); asukohaindeks++) andmed[asukohaindeks] = asukohaindeks;
    uint16_t kontrollimine_kontrollsumma = inet_chksum(andmed, sizeof(andmed)); memcpy(andmed + 2, &kontrollimine_kontrollsumma, 2);
    struct pbuf *datagramm = pbuf_alloc(PBUF_IP, sizeof(andmed), PBUF_RAM); if (!datagramm) return -12;
    pbuf_take(datagramm, andmed, sizeof(andmed)); ip_addr_t sihtkoht_osaleja; ip_addr_set_ip4_u32(&sihtkoht_osaleja, lwip_htonl(ADDRESS));
    err_t 처리값 = raw_sendto(vastus_osaleja, datagramm, &sihtkoht_osaleja); pbuf_free(datagramm);
    if (처리값) vastus_Olek = tõrke_number(처리값);
    return 처리값 ? vastus_Olek : 0;
}
int 응답시험읽기(unsigned kirje_VALUE) {
    통신망살피기();
    return kirje_VALUE == 0 ? vastus_Olek : kirje_VALUE == 1 ? (int)reaktsiooniaeg : kirje_VALUE == 2 ? (int)vastus_SEQUENCE : -22;
}
