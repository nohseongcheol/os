#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "tīkls_kopa.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../attāls_VALUE/attāls_VALUE.h"
#include "vadu_tīkls.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define mašīna_reģistrs(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif paziņa_ierīce;
static int 준비됨, aptauja;
static int lietot_vadu_tīkls;
static unsigned saņemt_patēriņš, 수신탈출, saņemt_kļūda;
static unsigned char saņemt_datu_buferis[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_datogramma_COUNT, 보낸전문수, RECEIVED_byte_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_joma, saņemt_ports, informācijas_tehnoloģija_gaida, 연결됨, Fails_beigt_zvanu, Kļūda;
    struct tcp_pcb *paziņa_vadība;
    struct udp_pcb *datogramma_vadība;
    unsigned priekšējā_ievade, ievade_COUNT;
    unsigned char dati[4096];
    unsigned 길이목록[4], 접속번호들[4], vienranga_dalībnieks_numurs;
    uint32_t 주소목록[4], vienranga_adrese;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int kļūdas_numurs(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *iegūt_VALUE(int Fails_turis) { return Fails_turis >= 0 && Fails_turis < 32 && 통신끝점들[Fails_turis].TYPE_joma ? &통신끝점들[Fails_turis] : 0; }
static int 예약하기(int TYPE_joma) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_joma) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_joma = TYPE_joma; 통신끝점들[순번].informācijas_tehnoloģija_gaida = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned koda_punkts) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = koda_punkts; }
static err_t ražojums(struct netif *krājums_COUNT, struct pbuf *dati_amats, const ip4_addr_t *adrese) {
    (void)krājums_COUNT; (void)adrese;
    if (dati_amats->tot_len > 1500 || 송신개수 + 2 * dati_amats->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Tālāk_Nobīde = dati_amats; Tālāk_Nobīde; Tālāk_Nobīde = Tālāk_Nobīde->next) for (unsigned 순번 = 0; 순번 < Tālāk_Nobīde->len; 순번++) {
        unsigned koda_punkts = ((unsigned char *)Tālāk_Nobīde->payload)[순번];
        if (koda_punkts == 192 || koda_punkts == 219) { 내보내기(219); 내보내기(koda_punkts == 192 ? 220 : 221); } else 내보내기(koda_punkts);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += dati_amats->tot_len; return ERR_OK;
}
static err_t Sagatavot_CLR(struct netif *krājums_COUNT) { krājums_COUNT->name[0] = 's'; krājums_COUNT->name[1] = 'l'; krājums_COUNT->mtu = 1500; krājums_COUNT->output = ražojums; return ERR_OK; }
void Sagatavot_tīkls(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    mašīna_reģistrs(보조장치 + 4) |= 1; mašīna_reģistrs(보조장치 + 0x60) = 0; mašīna_reģistrs(보조장치 + 0x44) = 0;
    mašīna_reģistrs(보조장치 + 0x48) = 0xc6; mašīna_reģistrs(보조장치 + 0x4c) = 3; mašīna_reģistrs(보조장치 + 0x68) = 270; mašīna_reģistrs(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t interneta_adrese, bitmaska, vārtejas_adrese;
    lietot_vadu_tīkls=유선장치있음();
    ip4_addr_set_u32(&interneta_adrese, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bitmaska, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&vārtejas_adrese, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&paziņa_ierīce, &interneta_adrese, &bitmaska, &vārtejas_adrese, 0, lietot_vadu_tīkls?Sagatavot_vadu_tīkls:Sagatavot_CLR, lietot_vadu_tīkls?ethernet_input:ip4_input))return;
    netif_set_default(&paziņa_ierīce); netif_set_up(&paziņa_ierīce);if(!lietot_vadu_tīkls)netif_set_link_up(&paziņa_ierīce); 준비됨 = 1;
    Sagatavot_attāls();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *dati_amats, err_t Kļūda) {
    통신끝점 *virkne_dati = 부가인수; (void)통신제어블록; (void)Kļūda;
    if (!dati_amats) { virkne_dati->Fails_beigt_zvanu = 1; return ERR_OK; }
    if (dati_amats->tot_len > sizeof(virkne_dati->dati) - virkne_dati->ievade_COUNT) return ERR_MEM;
    unsigned pašreizējais_amats = (virkne_dati->priekšējā_ievade + virkne_dati->ievade_COUNT) % sizeof(virkne_dati->dati);
    for (struct pbuf *Tālāk_Nobīde = dati_amats; Tālāk_Nobīde; Tālāk_Nobīde = Tālāk_Nobīde->next) for (unsigned 순번 = 0; 순번 < Tālāk_Nobīde->len; 순번++) {
        virkne_dati->dati[pašreizējais_amats] = ((unsigned char *)Tālāk_Nobīde->payload)[순번]; pašreizējais_amats = (pašreizējais_amats + 1) % sizeof(virkne_dati->dati);
    }
    virkne_dati->ievade_COUNT += dati_amats->tot_len; pbuf_free(dati_amats); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t Kļūda) { 통신끝점 *virkne_dati = 부가인수; virkne_dati->paziņa_vadība = 0; virkne_dati->Kļūda = kļūdas_numurs(Kļūda); }
static void 되부름목록(통신끝점 *virkne_dati) { tcp_arg(virkne_dati->paziņa_vadība, virkne_dati); tcp_recv(virkne_dati->paziņa_vadība, 수신됨); tcp_err(virkne_dati->paziņa_vadība, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t Kļūda) {
    통신끝점 *virkne_dati = 부가인수; (void)통신제어블록; if (Kļūda) virkne_dati->Kļūda = kļūdas_numurs(Kļūda); else virkne_dati->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t Kļūda) {
    통신끝점 *vecākobjekts = 부가인수; if (Kļūda) return Kļūda;
    int Fails_turis = 예약하기(1); if (Fails_turis < 0) return ERR_MEM;
    통신끝점 *virkne_dati = &통신끝점들[Fails_turis]; virkne_dati->paziņa_vadība = 통신제어블록; virkne_dati->연결됨 = 1; virkne_dati->informācijas_tehnoloģija_gaida = (int)(vecākobjekts - 통신끝점들);
    virkne_dati->vienranga_adrese = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); virkne_dati->vienranga_dalībnieks_numurs = 통신제어블록->remote_port;
    되부름목록(virkne_dati); return ERR_OK;
}
static void datogramma(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *dati_amats, const ip_addr_t *adrese, u16_t porta_numurs) {
    통신끝점 *virkne_dati = 부가인수; (void)통신제어블록;
    if (virkne_dati->ievade_COUNT < 4 && dati_amats->tot_len <= 512) {
        unsigned pozīcijas_indekss = (virkne_dati->priekšējā_ievade + virkne_dati->ievade_COUNT) % 4;
        pbuf_copy_partial(dati_amats, virkne_dati->dati + pozīcijas_indekss * 512, dati_amats->tot_len, 0);
        virkne_dati->길이목록[pozīcijas_indekss] = dati_amats->tot_len; virkne_dati->접속번호들[pozīcijas_indekss] = porta_numurs;
        virkne_dati->주소목록[pozīcijas_indekss] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adrese))); virkne_dati->ievade_COUNT++;
    }
    pbuf_free(dati_amats);
}
int 통신끝점만들기(int TYPE_joma) {
    if (!준비됨) return -100;
    if (TYPE_joma != 1 && TYPE_joma != 2) return -93;
    int Fails_turis = 예약하기(TYPE_joma); if (Fails_turis < 0) return Fails_turis;
    통신끝점 *virkne_dati = &통신끝점들[Fails_turis];
    if (TYPE_joma == 1) { virkne_dati->paziņa_vadība = tcp_new(); if (virkne_dati->paziņa_vadība) 되부름목록(virkne_dati); }
    else { virkne_dati->datogramma_vadība = udp_new(); if (virkne_dati->datogramma_vadība) udp_recv(virkne_dati->datogramma_vadība, datogramma, virkne_dati); }
    if (!virkne_dati->paziņa_vadība && !virkne_dati->datogramma_vadība) { virkne_dati->TYPE_joma = 0; return -12; } return Fails_turis;
}
int NET_BIND(int Fails_turis, uint32_t adrese, unsigned porta_numurs) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati) return -9;
    if (porta_numurs > 65535 || (adrese && adrese != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&paziņa_ierīce))) && adrese != 0x7f000001)) return -99;
    ip_addr_t interneta_adrese; ip_addr_set_ip4_u32(&interneta_adrese, lwip_htonl(adrese));
    err_t 보조항목 = virkne_dati->TYPE_joma == 1 ? tcp_bind(virkne_dati->paziņa_vadība, &interneta_adrese, porta_numurs) : udp_bind(virkne_dati->datogramma_vadība, &interneta_adrese, porta_numurs); return 보조항목 ? kļūdas_numurs(보조항목) : 0;
}
void 통신주소재사용(int Fails_turis) { 통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (virkne_dati && virkne_dati->paziņa_vadība) ip_set_option(virkne_dati->paziņa_vadība, SOF_REUSEADDR); }
int NET_klausīties(int Fails_turis) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati || virkne_dati->TYPE_joma != 1) return -9;
    if (virkne_dati->saņemt_ports) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(virkne_dati->paziņa_vadība, 4, &보조항목);
    if (!통신제어블록) return kļūdas_numurs(보조항목); virkne_dati->paziņa_vadība = 통신제어블록; virkne_dati->saņemt_ports = 1; tcp_arg(통신제어블록, virkne_dati); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_saziņa(int Fails_turis, uint32_t adrese, unsigned porta_numurs) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati || virkne_dati->TYPE_joma != 1) return -9;
    if (virkne_dati->Kļūda) return virkne_dati->Kļūda;
    if (virkne_dati->연결됨) return 0;
    if (virkne_dati->vienranga_dalībnieks_numurs) return -115;
    if (!porta_numurs || porta_numurs > 65535 || !adrese) return -22;
    ip_addr_t interneta_adrese; ip_addr_set_ip4_u32(&interneta_adrese, lwip_htonl(adrese));
    virkne_dati->vienranga_adrese = adrese; virkne_dati->vienranga_dalībnieks_numurs = porta_numurs;
    err_t 보조항목 = tcp_connect(virkne_dati->paziņa_vadība, &interneta_adrese, porta_numurs, 연결됨); return 보조항목 ? kļūdas_numurs(보조항목) : -115;
}
int NET_akceptēt(int Fails_turis) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati || !virkne_dati->saņemt_ports) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_joma == 1 && 통신끝점들[순번].informācijas_tehnoloģija_gaida == Fails_turis) { 통신끝점들[순번].informācijas_tehnoloģija_gaida = -1; return 순번; }
    return -11;
}
int 통신읽기(int Fails_turis, void *dati, unsigned krājums_COUNT) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati || virkne_dati->TYPE_joma != 1) return -9;
    if (!krājums_COUNT) return 0; if (!virkne_dati->ievade_COUNT) return virkne_dati->Kļūda ? virkne_dati->Kļūda : virkne_dati->Fails_beigt_zvanu ? 0 : -11;
    if (krājums_COUNT > virkne_dati->ievade_COUNT) krājums_COUNT = virkne_dati->ievade_COUNT;
    for (unsigned 순번 = 0; 순번 < krājums_COUNT; 순번++) { ((unsigned char *)dati)[순번] = virkne_dati->dati[virkne_dati->priekšējā_ievade]; virkne_dati->priekšējā_ievade = (virkne_dati->priekšējā_ievade + 1) % sizeof(virkne_dati->dati); }
    virkne_dati->ievade_COUNT -= krājums_COUNT; if (virkne_dati->paziņa_vadība) tcp_recved(virkne_dati->paziņa_vadība, krājums_COUNT); return krājums_COUNT;
}
int NET_rakstīšana(int Fails_turis, const void *dati, unsigned krājums_COUNT) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati || virkne_dati->TYPE_joma != 1) return -9;
    if (virkne_dati->Kļūda) return virkne_dati->Kļūda; if (!virkne_dati->paziņa_vadība || !virkne_dati->연결됨) return -107;
    if (!krājums_COUNT) return 0; if (krājums_COUNT > tcp_sndbuf(virkne_dati->paziņa_vadība)) krājums_COUNT = tcp_sndbuf(virkne_dati->paziņa_vadība);
    if (!krājums_COUNT) return -11; if (krājums_COUNT > 1024) krājums_COUNT = 1024;
    err_t 보조항목 = tcp_write(virkne_dati->paziņa_vadība, dati, krājums_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return kļūdas_numurs(보조항목);
    tcp_output(virkne_dati->paziņa_vadība); return krājums_COUNT;
}
int sūtīt_datogramma(int Fails_turis, const void *dati, unsigned krājums_COUNT, uint32_t adrese, unsigned porta_numurs) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati || virkne_dati->TYPE_joma != 2) return -9;
    if (krājums_COUNT > 512) return -90; if (!porta_numurs || porta_numurs > 65535) return -22;
    struct pbuf *dati_amats = pbuf_alloc(PBUF_TRANSPORT, krājums_COUNT, PBUF_RAM); if (!dati_amats) return -11;
    pbuf_take(dati_amats, dati, krājums_COUNT); ip_addr_t interneta_adrese; ip_addr_set_ip4_u32(&interneta_adrese, lwip_htonl(adrese));
    err_t 보조항목 = udp_sendto(virkne_dati->datogramma_vadība, dati_amats, &interneta_adrese, porta_numurs); pbuf_free(dati_amats); return 보조항목 ? kļūdas_numurs(보조항목) : (int)krājums_COUNT;
}
int saņemt_datogramma(int Fails_turis, void *dati, unsigned krājums_COUNT) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati || virkne_dati->TYPE_joma != 2) return -9;
    if (!virkne_dati->ievade_COUNT) return -11; unsigned pašreizējais_amats = virkne_dati->priekšējā_ievade;
    if (krājums_COUNT > virkne_dati->길이목록[pašreizējais_amats]) krājums_COUNT = virkne_dati->길이목록[pašreizējais_amats]; memcpy(dati, virkne_dati->dati + pašreizējais_amats * 512, krājums_COUNT);
    virkne_dati->vienranga_dalībnieks_numurs = virkne_dati->접속번호들[pašreizējais_amats]; virkne_dati->vienranga_adrese = virkne_dati->주소목록[pašreizējais_amats]; virkne_dati->priekšējā_ievade = (pašreizējais_amats + 1) % 4; virkne_dati->ievade_COUNT--; return krājums_COUNT;
}
unsigned tīkls_porta_numurs(int Fails_turis) { 통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); return !virkne_dati ? 0 : virkne_dati->paziņa_vadība ? virkne_dati->paziņa_vadība->local_port : virkne_dati->datogramma_vadība ? virkne_dati->datogramma_vadība->local_port : 0; }
unsigned vienranga_porta_numurs(int Fails_turis) { 통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); return virkne_dati ? virkne_dati->vienranga_dalībnieks_numurs : 0; }
uint32_t NET_vienranga_adrese(int Fails_turis) { 통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); return virkne_dati ? virkne_dati->vienranga_adrese : 0; }
void Aizvērt_tīkls(int Fails_turis) {
    통신끝점 *virkne_dati = iegūt_VALUE(Fails_turis); if (!virkne_dati) return;
    if (virkne_dati->saņemt_ports) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_joma && 통신끝점들[순번].informācijas_tehnoloģija_gaida == Fails_turis) Aizvērt_tīkls(순번);
    if (virkne_dati->paziņa_vadība) {
        tcp_arg(virkne_dati->paziņa_vadība, 0); if (virkne_dati->saņemt_ports) tcp_accept(virkne_dati->paziņa_vadība, 0); else { tcp_recv(virkne_dati->paziņa_vadība, 0); tcp_err(virkne_dati->paziņa_vadība, 0); }
        if (tcp_close(virkne_dati->paziņa_vadība) != ERR_OK) tcp_abort(virkne_dati->paziņa_vadība);
    }
    if (virkne_dati->datogramma_vadība) udp_remove(virkne_dati->datogramma_vadība); virkne_dati->TYPE_joma = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || aptauja) return; aptauja = 1;
    if(lietot_vadu_tīkls)유선망살피기(&paziņa_ierīce);
    for (unsigned budžets = 0; !lietot_vadu_tīkls && budžets < 4096 && (mašīna_reģistrs(보조장치 + 0x54) & 1); budžets++) {
        unsigned koda_punkts = mašīna_reģistrs(보조장치 + 0x40) & 255;
        if (koda_punkts == 192) {
            if (saņemt_patēriņš && !saņemt_kļūda && !수신탈출) {
                struct pbuf *dati_amats = pbuf_alloc(PBUF_RAW, saņemt_patēriņš, PBUF_POOL);
                if (dati_amats) { RECEIVED_datogramma_COUNT++; RECEIVED_byte_COUNT += saņemt_patēriņš; pbuf_take(dati_amats, saņemt_datu_buferis, saņemt_patēriņš); if (paziņa_ierīce.input(dati_amats, &paziņa_ierīce) != ERR_OK) { 버린전문수++; pbuf_free(dati_amats); } }
                else 버린전문수++;
            }
            else if (saņemt_patēriņš) 버린전문수++;
            saņemt_patēriņš = saņemt_kļūda = 수신탈출 = 0;
        } else if (koda_punkts == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (koda_punkts != 220 && koda_punkts != 221) saņemt_kļūda = 1; koda_punkts = koda_punkts == 220 ? 192 : 219; 수신탈출 = 0; }
            if (saņemt_patēriņš < sizeof(saņemt_datu_buferis)) saņemt_datu_buferis[saņemt_patēriņš++] = koda_punkts; else saņemt_kļūda = 1;
        }
    }
    netif_poll(&paziņa_ierīce); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budžets = 0; budžets < 4096 && 송신개수 && (mašīna_reģistrs(보조장치 + 0x54) & 0x20); budžets++) {
        mašīna_reģistrs(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    aptauja = 0;
}

/* Uzstādījumi·조회는 lwIP의 faktisks_dati 인터페이스와 beigt_zvanu_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned ievade_VALUE, unsigned INDEX) {
    if(ievade_VALUE==20)return lietot_vadu_tīkls;
    if(ievade_VALUE==21)return 준비됨&&netif_is_link_up(&paziņa_ierīce);
    if(ievade_VALUE==22)return lietot_vadu_tīkls?유선망집계(5):0;
    if (!준비됨) return 0;
    if(lietot_vadu_tīkls&&ievade_VALUE>=4&&ievade_VALUE<=8)return 유선망집계(ievade_VALUE-4);
    if (ievade_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&paziņa_ierīce)));
    if (ievade_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&paziņa_ierīce)));
    if (ievade_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&paziņa_ierīce)));
    if (ievade_VALUE == 3) return netif_is_up(&paziņa_ierīce) != 0;
    if (ievade_VALUE == 4) return RECEIVED_datogramma_COUNT;
    if (ievade_VALUE == 5) return 보낸전문수;
    if (ievade_VALUE == 6) return RECEIVED_byte_COUNT;
    if (ievade_VALUE == 7) return 보낸바이트수;
    if (ievade_VALUE == 8) return 버린전문수;
    if (ievade_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *beigt_zvanu_p = &통신끝점들[INDEX];
    if (ievade_VALUE == 10) return beigt_zvanu_p->TYPE_joma;
    if (!beigt_zvanu_p->TYPE_joma) return 0;
    if (ievade_VALUE == 11) return tīkls_porta_numurs(INDEX);
    if (ievade_VALUE == 12) return beigt_zvanu_p->vienranga_adrese;
    if (ievade_VALUE == 13) return beigt_zvanu_p->vienranga_dalībnieks_numurs;
    if (ievade_VALUE == 14) return beigt_zvanu_p->saņemt_ports ? 1 : beigt_zvanu_p->Fails_beigt_zvanu ? 3 : beigt_zvanu_p->Kļūda ? 4 : beigt_zvanu_p->연결됨 ? 2 : 0;
    if (ievade_VALUE == 15) return beigt_zvanu_p->ievade_COUNT;
    if (ievade_VALUE == 16) {
        const ip_addr_t *adrese = beigt_zvanu_p->TYPE_joma == 1 && beigt_zvanu_p->paziņa_vadība ? &beigt_zvanu_p->paziņa_vadība->local_ip :
            beigt_zvanu_p->TYPE_joma == 2 && beigt_zvanu_p->datogramma_vadība ? &beigt_zvanu_p->datogramma_vadība->local_ip : 0;
        return adrese ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adrese))) : 0;
    }
    return 0;
}

int konfigurēt_tīkls(unsigned Darbība, uint32_t adrese, uint32_t maska_VALUE, uint32_t vārteja_VALUE) {
    if (!준비됨) return -100;
    if (Darbība == 1) { netif_set_up(&paziņa_ierīce); return 0; }
    if (Darbība == 2) { netif_set_down(&paziņa_ierīce); return 0; }
    if (Darbība != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maska_VALUE, 같은 망의 선택적 noklusējuma_vērtība vārteja_VALUE. */
    uint32_t 뒤집은가림 = ~maska_VALUE;
    if (!maska_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !adrese || (adrese >> 24) == 127 ||
        (adrese >> 24) == 0 || (adrese >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(adrese & 뒤집은가림) || (adrese & 뒤집은가림) == 뒤집은가림)) ||
        (vārteja_VALUE && ((vārteja_VALUE & maska_VALUE) != (adrese & maska_VALUE) || vārteja_VALUE == adrese || (vārteja_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(vārteja_VALUE & 뒤집은가림) || (vārteja_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 adrese 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_joma &&
        !(통신끝점들[INDEX].saņemt_ports && 통신끝점들[INDEX].paziņa_vadība && ip_addr_isany(&통신끝점들[INDEX].paziņa_vadība->local_ip))) return -16;
    if(lietot_vadu_tīkls)dhcp_stop(&paziņa_ierīce);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(adrese)); ip4_addr_set_u32(&새가림, lwip_htonl(maska_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(vārteja_VALUE));
    netif_set_addr(&paziņa_ierīce, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *atbilde_dalībnieks;
static uint32_t 시험주소, 시험시각, atbildes_laiks;
static unsigned 시험순서, 시험식별자, atbilde_SEQUENCE;
static int atbilde_Statuss;
static u8_t 응답받음(void *Parametri, struct raw_pcb *beigt_zvanu_p, struct pbuf *dati, const ip_addr_t *adrese) {
    (void)Parametri; (void)beigt_zvanu_p;
    unsigned char 머리[20], atbilde[16];
    if (atbilde_Statuss != -11 || dati->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(adrese))) != 시험주소 || pbuf_copy_partial(dati, 머리, 20, 0) != 20) return 0;
    unsigned galvene_mainīt_izmērus = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || galvene_mainīt_izmērus < 20 || dati->tot_len < galvene_mainīt_izmērus + 16 ||
        pbuf_copy_partial(dati, atbilde, 16, galvene_mainīt_izmērus) != 16 || atbilde[0] || atbilde[1] ||
        (((unsigned)atbilde[4] << 8) | atbilde[5]) != 시험식별자 ||
        (((unsigned)atbilde[6] << 8) | atbilde[7]) != 시험순서 ||
        atbilde[8] != 'J' || atbilde[9] != 'K' || atbilde[10] != 'O' || atbilde[11] != 'S' ||
        (((uint32_t)atbilde[12] << 24) | ((uint32_t)atbilde[13] << 16) | ((uint32_t)atbilde[14] << 8) | atbilde[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(dati, galvene_mainīt_izmērus)) return 0;
    if (inet_chksum_pbuf(dati)) { pbuf_add_header(dati, galvene_mainīt_izmērus); return 0; }
    atbildes_laiks = (uint32_t)보드밀리초() - 시험시각; atbilde_SEQUENCE = 머리[8]; atbilde_Statuss = 0;
    pbuf_free(dati); return 1;
}
int 응답시험시작(uint32_t adrese, unsigned secība_VALUE) {
    if (!준비됨 || !netif_is_up(&paziņa_ierīce)) return -100;
    if (!adrese || (adrese >> 28) >= 14 || adrese == 0xffffffffu) return -22;
    if (!atbilde_dalībnieks) { atbilde_dalībnieks = raw_new(IP_PROTO_ICMP); if (!atbilde_dalībnieks) return -12; raw_recv(atbilde_dalībnieks, 응답받음, 0); }
    시험주소 = adrese; 시험순서 = secība_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); atbilde_Statuss = -11; atbildes_laiks = atbilde_SEQUENCE = 0;
    unsigned char dati[32] = {8,0,0,0};
    dati[4] = 시험식별자 >> 8; dati[5] = 시험식별자; dati[6] = 시험순서 >> 8; dati[7] = 시험순서;
    dati[8]='J'; dati[9]='K'; dati[10]='O'; dati[11]='S';
    dati[12]=시험시각 >> 24; dati[13]=시험시각 >> 16; dati[14]=시험시각 >> 8; dati[15]=시험시각;
    for (unsigned pozīcijas_indekss = 16; pozīcijas_indekss < sizeof(dati); pozīcijas_indekss++) dati[pozīcijas_indekss] = pozīcijas_indekss;
    uint16_t verifikācija_kontrolsumma = inet_chksum(dati, sizeof(dati)); memcpy(dati + 2, &verifikācija_kontrolsumma, 2);
    struct pbuf *datogramma = pbuf_alloc(PBUF_IP, sizeof(dati), PBUF_RAM); if (!datogramma) return -12;
    pbuf_take(datogramma, dati, sizeof(dati)); ip_addr_t mērķis_dalībnieks; ip_addr_set_ip4_u32(&mērķis_dalībnieks, lwip_htonl(adrese));
    err_t 처리값 = raw_sendto(atbilde_dalībnieks, datogramma, &mērķis_dalībnieks); pbuf_free(datogramma);
    if (처리값) atbilde_Statuss = kļūdas_numurs(처리값);
    return 처리값 ? atbilde_Statuss : 0;
}
int 응답시험읽기(unsigned ievade_VALUE) {
    통신망살피기();
    return ievade_VALUE == 0 ? atbilde_Statuss : ievade_VALUE == 1 ? (int)atbildes_laiks : ievade_VALUE == 2 ? (int)atbilde_SEQUENCE : -22;
}
