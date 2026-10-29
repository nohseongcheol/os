#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "tinklas_eilė.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../nuotolinis_VALUE/nuotolinis_VALUE.h"
#include "laidinis_tinklas.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define mašina_registras(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif ryšys_įrenginys;
static int 준비됨, apklausa;
static int naudoti_laidinis_tinklas;
static unsigned gauti_naudojimas, 수신탈출, 수신오류;
static unsigned char gauti_duomenų_buferis[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t RECEIVED_paketų_kelio_schema_COUNT, 보낸전문수, RECEIVED_baitas_COUNT, 보낸바이트수, 버린전문수;
typedef struct {
    int TYPE_sritis, gauti_jungtis, informacinės_technologijos_laukiama, 연결됨, Failas_baigti_pokalbį, KLAIDA;
    struct tcp_pcb *ryšys_valdymas;
    struct udp_pcb *paketų_kelio_schema_valdymas;
    unsigned priekinis_įrašas, įrašas_COUNT;
    unsigned char duomenys[4096];
    unsigned 길이목록[4], 접속번호들[4], lygiavertis_mazgas_dalyvis_numeris;
    uint32_t 주소목록[4], lygiavertis_mazgas_ADDRESS;
} 통신끝점;
static 통신끝점 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int klaidos_numeris(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static 통신끝점 *gauti_VALUE(int Failas_rodyklė) { return Failas_rodyklė >= 0 && Failas_rodyklė < 32 && 통신끝점들[Failas_rodyklė].TYPE_sritis ? &통신끝점들[Failas_rodyklė] : 0; }
static int 예약하기(int TYPE_sritis) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYPE_sritis) {
        memset(&통신끝점들[순번], 0, sizeof(통신끝점)); 통신끝점들[순번].TYPE_sritis = TYPE_sritis; 통신끝점들[순번].informacinės_technologijos_laukiama = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned simbolio_kodas) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = simbolio_kodas; }
static err_t išeiga(struct netif *prekė_COUNT, struct pbuf *duomenys_padėtis, const ip4_addr_t *ADDRESS) {
    (void)prekė_COUNT; (void)ADDRESS;
    if (duomenys_padėtis->tot_len > 1500 || 송신개수 + 2 * duomenys_padėtis->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *toliau_OFFSET = duomenys_padėtis; toliau_OFFSET; toliau_OFFSET = toliau_OFFSET->next) for (unsigned 순번 = 0; 순번 < toliau_OFFSET->len; 순번++) {
        unsigned simbolio_kodas = ((unsigned char *)toliau_OFFSET->payload)[순번];
        if (simbolio_kodas == 192 || simbolio_kodas == 219) { 내보내기(219); 내보내기(simbolio_kodas == 192 ? 220 : 221); } else 내보내기(simbolio_kodas);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += duomenys_padėtis->tot_len; return ERR_OK;
}
static err_t Parengti_CLR(struct netif *prekė_COUNT) { prekė_COUNT->name[0] = 's'; prekė_COUNT->name[1] = 'l'; prekė_COUNT->mtu = 1500; prekė_COUNT->output = išeiga; return ERR_OK; }
void Parengti_tinklas(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    mašina_registras(보조장치 + 4) |= 1; mašina_registras(보조장치 + 0x60) = 0; mašina_registras(보조장치 + 0x44) = 0;
    mašina_registras(보조장치 + 0x48) = 0xc6; mašina_registras(보조장치 + 0x4c) = 3; mašina_registras(보조장치 + 0x68) = 270; mašina_registras(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t interneto_adresas, šablonas, šliuzo_adresas;
    naudoti_laidinis_tinklas=유선장치있음();
    ip4_addr_set_u32(&interneto_adresas, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&šablonas, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&šliuzo_adresas, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&ryšys_įrenginys, &interneto_adresas, &šablonas, &šliuzo_adresas, 0, naudoti_laidinis_tinklas?Parengti_laidinis_tinklas:Parengti_CLR, naudoti_laidinis_tinklas?ethernet_input:ip4_input))return;
    netif_set_default(&ryšys_įrenginys); netif_set_up(&ryšys_įrenginys);if(!naudoti_laidinis_tinklas)netif_set_link_up(&ryšys_įrenginys); 준비됨 = 1;
    Parengti_nuotolinis();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *duomenys_padėtis, err_t KLAIDA) {
    통신끝점 *eilutė_duomenys = 부가인수; (void)통신제어블록; (void)KLAIDA;
    if (!duomenys_padėtis) { eilutė_duomenys->Failas_baigti_pokalbį = 1; return ERR_OK; }
    if (duomenys_padėtis->tot_len > sizeof(eilutė_duomenys->duomenys) - eilutė_duomenys->įrašas_COUNT) return ERR_MEM;
    unsigned dabartinis_padėtis = (eilutė_duomenys->priekinis_įrašas + eilutė_duomenys->įrašas_COUNT) % sizeof(eilutė_duomenys->duomenys);
    for (struct pbuf *toliau_OFFSET = duomenys_padėtis; toliau_OFFSET; toliau_OFFSET = toliau_OFFSET->next) for (unsigned 순번 = 0; 순번 < toliau_OFFSET->len; 순번++) {
        eilutė_duomenys->duomenys[dabartinis_padėtis] = ((unsigned char *)toliau_OFFSET->payload)[순번]; dabartinis_padėtis = (dabartinis_padėtis + 1) % sizeof(eilutė_duomenys->duomenys);
    }
    eilutė_duomenys->įrašas_COUNT += duomenys_padėtis->tot_len; pbuf_free(duomenys_padėtis); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t KLAIDA) { 통신끝점 *eilutė_duomenys = 부가인수; eilutė_duomenys->ryšys_valdymas = 0; eilutė_duomenys->KLAIDA = klaidos_numeris(KLAIDA); }
static void 되부름목록(통신끝점 *eilutė_duomenys) { tcp_arg(eilutė_duomenys->ryšys_valdymas, eilutė_duomenys); tcp_recv(eilutė_duomenys->ryšys_valdymas, 수신됨); tcp_err(eilutė_duomenys->ryšys_valdymas, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t KLAIDA) {
    통신끝점 *eilutė_duomenys = 부가인수; (void)통신제어블록; if (KLAIDA) eilutė_duomenys->KLAIDA = klaidos_numeris(KLAIDA); else eilutė_duomenys->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t KLAIDA) {
    통신끝점 *pirminis = 부가인수; if (KLAIDA) return KLAIDA;
    int Failas_rodyklė = 예약하기(1); if (Failas_rodyklė < 0) return ERR_MEM;
    통신끝점 *eilutė_duomenys = &통신끝점들[Failas_rodyklė]; eilutė_duomenys->ryšys_valdymas = 통신제어블록; eilutė_duomenys->연결됨 = 1; eilutė_duomenys->informacinės_technologijos_laukiama = (int)(pirminis - 통신끝점들);
    eilutė_duomenys->lygiavertis_mazgas_ADDRESS = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); eilutė_duomenys->lygiavertis_mazgas_dalyvis_numeris = 통신제어블록->remote_port;
    되부름목록(eilutė_duomenys); return ERR_OK;
}
static void paketų_kelio_schema(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *duomenys_padėtis, const ip_addr_t *ADDRESS, u16_t prievado_numeris) {
    통신끝점 *eilutė_duomenys = 부가인수; (void)통신제어블록;
    if (eilutė_duomenys->įrašas_COUNT < 4 && duomenys_padėtis->tot_len <= 512) {
        unsigned vietos_rodyklė = (eilutė_duomenys->priekinis_įrašas + eilutė_duomenys->įrašas_COUNT) % 4;
        pbuf_copy_partial(duomenys_padėtis, eilutė_duomenys->duomenys + vietos_rodyklė * 512, duomenys_padėtis->tot_len, 0);
        eilutė_duomenys->길이목록[vietos_rodyklė] = duomenys_padėtis->tot_len; eilutė_duomenys->접속번호들[vietos_rodyklė] = prievado_numeris;
        eilutė_duomenys->주소목록[vietos_rodyklė] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))); eilutė_duomenys->įrašas_COUNT++;
    }
    pbuf_free(duomenys_padėtis);
}
int 통신끝점만들기(int TYPE_sritis) {
    if (!준비됨) return -100;
    if (TYPE_sritis != 1 && TYPE_sritis != 2) return -93;
    int Failas_rodyklė = 예약하기(TYPE_sritis); if (Failas_rodyklė < 0) return Failas_rodyklė;
    통신끝점 *eilutė_duomenys = &통신끝점들[Failas_rodyklė];
    if (TYPE_sritis == 1) { eilutė_duomenys->ryšys_valdymas = tcp_new(); if (eilutė_duomenys->ryšys_valdymas) 되부름목록(eilutė_duomenys); }
    else { eilutė_duomenys->paketų_kelio_schema_valdymas = udp_new(); if (eilutė_duomenys->paketų_kelio_schema_valdymas) udp_recv(eilutė_duomenys->paketų_kelio_schema_valdymas, paketų_kelio_schema, eilutė_duomenys); }
    if (!eilutė_duomenys->ryšys_valdymas && !eilutė_duomenys->paketų_kelio_schema_valdymas) { eilutė_duomenys->TYPE_sritis = 0; return -12; } return Failas_rodyklė;
}
int NET_BIND(int Failas_rodyklė, uint32_t ADDRESS, unsigned prievado_numeris) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys) return -9;
    if (prievado_numeris > 65535 || (ADDRESS && ADDRESS != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ryšys_įrenginys))) && ADDRESS != 0x7f000001)) return -99;
    ip_addr_t interneto_adresas; ip_addr_set_ip4_u32(&interneto_adresas, lwip_htonl(ADDRESS));
    err_t 보조항목 = eilutė_duomenys->TYPE_sritis == 1 ? tcp_bind(eilutė_duomenys->ryšys_valdymas, &interneto_adresas, prievado_numeris) : udp_bind(eilutė_duomenys->paketų_kelio_schema_valdymas, &interneto_adresas, prievado_numeris); return 보조항목 ? klaidos_numeris(보조항목) : 0;
}
void 통신주소재사용(int Failas_rodyklė) { 통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (eilutė_duomenys && eilutė_duomenys->ryšys_valdymas) ip_set_option(eilutė_duomenys->ryšys_valdymas, SOF_REUSEADDR); }
int NET_laukti(int Failas_rodyklė) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys || eilutė_duomenys->TYPE_sritis != 1) return -9;
    if (eilutė_duomenys->gauti_jungtis) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(eilutė_duomenys->ryšys_valdymas, 4, &보조항목);
    if (!통신제어블록) return klaidos_numeris(보조항목); eilutė_duomenys->ryšys_valdymas = 통신제어블록; eilutė_duomenys->gauti_jungtis = 1; tcp_arg(통신제어블록, eilutė_duomenys); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_ryšys(int Failas_rodyklė, uint32_t ADDRESS, unsigned prievado_numeris) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys || eilutė_duomenys->TYPE_sritis != 1) return -9;
    if (eilutė_duomenys->KLAIDA) return eilutė_duomenys->KLAIDA;
    if (eilutė_duomenys->연결됨) return 0;
    if (eilutė_duomenys->lygiavertis_mazgas_dalyvis_numeris) return -115;
    if (!prievado_numeris || prievado_numeris > 65535 || !ADDRESS) return -22;
    ip_addr_t interneto_adresas; ip_addr_set_ip4_u32(&interneto_adresas, lwip_htonl(ADDRESS));
    eilutė_duomenys->lygiavertis_mazgas_ADDRESS = ADDRESS; eilutė_duomenys->lygiavertis_mazgas_dalyvis_numeris = prievado_numeris;
    err_t 보조항목 = tcp_connect(eilutė_duomenys->ryšys_valdymas, &interneto_adresas, prievado_numeris, 연결됨); return 보조항목 ? klaidos_numeris(보조항목) : -115;
}
int NET_priimti(int Failas_rodyklė) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys || !eilutė_duomenys->gauti_jungtis) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYPE_sritis == 1 && 통신끝점들[순번].informacinės_technologijos_laukiama == Failas_rodyklė) { 통신끝점들[순번].informacinės_technologijos_laukiama = -1; return 순번; }
    return -11;
}
int 통신읽기(int Failas_rodyklė, void *duomenys, unsigned prekė_COUNT) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys || eilutė_duomenys->TYPE_sritis != 1) return -9;
    if (!prekė_COUNT) return 0; if (!eilutė_duomenys->įrašas_COUNT) return eilutė_duomenys->KLAIDA ? eilutė_duomenys->KLAIDA : eilutė_duomenys->Failas_baigti_pokalbį ? 0 : -11;
    if (prekė_COUNT > eilutė_duomenys->įrašas_COUNT) prekė_COUNT = eilutė_duomenys->įrašas_COUNT;
    for (unsigned 순번 = 0; 순번 < prekė_COUNT; 순번++) { ((unsigned char *)duomenys)[순번] = eilutė_duomenys->duomenys[eilutė_duomenys->priekinis_įrašas]; eilutė_duomenys->priekinis_įrašas = (eilutė_duomenys->priekinis_įrašas + 1) % sizeof(eilutė_duomenys->duomenys); }
    eilutė_duomenys->įrašas_COUNT -= prekė_COUNT; if (eilutė_duomenys->ryšys_valdymas) tcp_recved(eilutė_duomenys->ryšys_valdymas, prekė_COUNT); return prekė_COUNT;
}
int NET_rašymas(int Failas_rodyklė, const void *duomenys, unsigned prekė_COUNT) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys || eilutė_duomenys->TYPE_sritis != 1) return -9;
    if (eilutė_duomenys->KLAIDA) return eilutė_duomenys->KLAIDA; if (!eilutė_duomenys->ryšys_valdymas || !eilutė_duomenys->연결됨) return -107;
    if (!prekė_COUNT) return 0; if (prekė_COUNT > tcp_sndbuf(eilutė_duomenys->ryšys_valdymas)) prekė_COUNT = tcp_sndbuf(eilutė_duomenys->ryšys_valdymas);
    if (!prekė_COUNT) return -11; if (prekė_COUNT > 1024) prekė_COUNT = 1024;
    err_t 보조항목 = tcp_write(eilutė_duomenys->ryšys_valdymas, duomenys, prekė_COUNT, TCP_WRITE_FLAG_COPY); if (보조항목) return klaidos_numeris(보조항목);
    tcp_output(eilutė_duomenys->ryšys_valdymas); return prekė_COUNT;
}
int siųsti_paketų_kelio_schema(int Failas_rodyklė, const void *duomenys, unsigned prekė_COUNT, uint32_t ADDRESS, unsigned prievado_numeris) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys || eilutė_duomenys->TYPE_sritis != 2) return -9;
    if (prekė_COUNT > 512) return -90; if (!prievado_numeris || prievado_numeris > 65535) return -22;
    struct pbuf *duomenys_padėtis = pbuf_alloc(PBUF_TRANSPORT, prekė_COUNT, PBUF_RAM); if (!duomenys_padėtis) return -11;
    pbuf_take(duomenys_padėtis, duomenys, prekė_COUNT); ip_addr_t interneto_adresas; ip_addr_set_ip4_u32(&interneto_adresas, lwip_htonl(ADDRESS));
    err_t 보조항목 = udp_sendto(eilutė_duomenys->paketų_kelio_schema_valdymas, duomenys_padėtis, &interneto_adresas, prievado_numeris); pbuf_free(duomenys_padėtis); return 보조항목 ? klaidos_numeris(보조항목) : (int)prekė_COUNT;
}
int gauti_paketų_kelio_schema(int Failas_rodyklė, void *duomenys, unsigned prekė_COUNT) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys || eilutė_duomenys->TYPE_sritis != 2) return -9;
    if (!eilutė_duomenys->įrašas_COUNT) return -11; unsigned dabartinis_padėtis = eilutė_duomenys->priekinis_įrašas;
    if (prekė_COUNT > eilutė_duomenys->길이목록[dabartinis_padėtis]) prekė_COUNT = eilutė_duomenys->길이목록[dabartinis_padėtis]; memcpy(duomenys, eilutė_duomenys->duomenys + dabartinis_padėtis * 512, prekė_COUNT);
    eilutė_duomenys->lygiavertis_mazgas_dalyvis_numeris = eilutė_duomenys->접속번호들[dabartinis_padėtis]; eilutė_duomenys->lygiavertis_mazgas_ADDRESS = eilutė_duomenys->주소목록[dabartinis_padėtis]; eilutė_duomenys->priekinis_įrašas = (dabartinis_padėtis + 1) % 4; eilutė_duomenys->įrašas_COUNT--; return prekė_COUNT;
}
unsigned tinklas_prievado_numeris(int Failas_rodyklė) { 통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); return !eilutė_duomenys ? 0 : eilutė_duomenys->ryšys_valdymas ? eilutė_duomenys->ryšys_valdymas->local_port : eilutė_duomenys->paketų_kelio_schema_valdymas ? eilutė_duomenys->paketų_kelio_schema_valdymas->local_port : 0; }
unsigned lygiavertis_mazgas_prievado_numeris(int Failas_rodyklė) { 통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); return eilutė_duomenys ? eilutė_duomenys->lygiavertis_mazgas_dalyvis_numeris : 0; }
uint32_t NET_lygiavertis_mazgas_ADDRESS(int Failas_rodyklė) { 통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); return eilutė_duomenys ? eilutė_duomenys->lygiavertis_mazgas_ADDRESS : 0; }
void Uždaryti_tinklas(int Failas_rodyklė) {
    통신끝점 *eilutė_duomenys = gauti_VALUE(Failas_rodyklė); if (!eilutė_duomenys) return;
    if (eilutė_duomenys->gauti_jungtis) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYPE_sritis && 통신끝점들[순번].informacinės_technologijos_laukiama == Failas_rodyklė) Uždaryti_tinklas(순번);
    if (eilutė_duomenys->ryšys_valdymas) {
        tcp_arg(eilutė_duomenys->ryšys_valdymas, 0); if (eilutė_duomenys->gauti_jungtis) tcp_accept(eilutė_duomenys->ryšys_valdymas, 0); else { tcp_recv(eilutė_duomenys->ryšys_valdymas, 0); tcp_err(eilutė_duomenys->ryšys_valdymas, 0); }
        if (tcp_close(eilutė_duomenys->ryšys_valdymas) != ERR_OK) tcp_abort(eilutė_duomenys->ryšys_valdymas);
    }
    if (eilutė_duomenys->paketų_kelio_schema_valdymas) udp_remove(eilutė_duomenys->paketų_kelio_schema_valdymas); eilutė_duomenys->TYPE_sritis = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || apklausa) return; apklausa = 1;
    if(naudoti_laidinis_tinklas)유선망살피기(&ryšys_įrenginys);
    for (unsigned biudžetas = 0; !naudoti_laidinis_tinklas && biudžetas < 4096 && (mašina_registras(보조장치 + 0x54) & 1); biudžetas++) {
        unsigned simbolio_kodas = mašina_registras(보조장치 + 0x40) & 255;
        if (simbolio_kodas == 192) {
            if (gauti_naudojimas && !수신오류 && !수신탈출) {
                struct pbuf *duomenys_padėtis = pbuf_alloc(PBUF_RAW, gauti_naudojimas, PBUF_POOL);
                if (duomenys_padėtis) { RECEIVED_paketų_kelio_schema_COUNT++; RECEIVED_baitas_COUNT += gauti_naudojimas; pbuf_take(duomenys_padėtis, gauti_duomenų_buferis, gauti_naudojimas); if (ryšys_įrenginys.input(duomenys_padėtis, &ryšys_įrenginys) != ERR_OK) { 버린전문수++; pbuf_free(duomenys_padėtis); } }
                else 버린전문수++;
            }
            else if (gauti_naudojimas) 버린전문수++;
            gauti_naudojimas = 수신오류 = 수신탈출 = 0;
        } else if (simbolio_kodas == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (simbolio_kodas != 220 && simbolio_kodas != 221) 수신오류 = 1; simbolio_kodas = simbolio_kodas == 220 ? 192 : 219; 수신탈출 = 0; }
            if (gauti_naudojimas < sizeof(gauti_duomenų_buferis)) gauti_duomenų_buferis[gauti_naudojimas++] = simbolio_kodas; else 수신오류 = 1;
        }
    }
    netif_poll(&ryšys_įrenginys); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned biudžetas = 0; biudžetas < 4096 && 송신개수 && (mašina_registras(보조장치 + 0x54) & 0x20); biudžetas++) {
        mašina_registras(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    apklausa = 0;
}

/* Nustatymai·조회는 lwIP의 faktinis_duomenys 인터페이스와 baigti_pokalbį_p 표를 사용한다. */
uint32_t 망상태읽기(unsigned įrašas_VALUE, unsigned INDEX) {
    if(įrašas_VALUE==20)return naudoti_laidinis_tinklas;
    if(įrašas_VALUE==21)return 준비됨&&netif_is_link_up(&ryšys_įrenginys);
    if(įrašas_VALUE==22)return naudoti_laidinis_tinklas?유선망집계(5):0;
    if (!준비됨) return 0;
    if(naudoti_laidinis_tinklas&&įrašas_VALUE>=4&&įrašas_VALUE<=8)return 유선망집계(įrašas_VALUE-4);
    if (įrašas_VALUE == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&ryšys_įrenginys)));
    if (įrašas_VALUE == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&ryšys_įrenginys)));
    if (įrašas_VALUE == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&ryšys_įrenginys)));
    if (įrašas_VALUE == 3) return netif_is_up(&ryšys_įrenginys) != 0;
    if (įrašas_VALUE == 4) return RECEIVED_paketų_kelio_schema_COUNT;
    if (įrašas_VALUE == 5) return 보낸전문수;
    if (įrašas_VALUE == 6) return RECEIVED_baitas_COUNT;
    if (įrašas_VALUE == 7) return 보낸바이트수;
    if (įrašas_VALUE == 8) return 버린전문수;
    if (įrašas_VALUE == 9) return 송신개수;
    if (INDEX >= 32) return 0;
    통신끝점 *baigti_pokalbį_p = &통신끝점들[INDEX];
    if (įrašas_VALUE == 10) return baigti_pokalbį_p->TYPE_sritis;
    if (!baigti_pokalbį_p->TYPE_sritis) return 0;
    if (įrašas_VALUE == 11) return tinklas_prievado_numeris(INDEX);
    if (įrašas_VALUE == 12) return baigti_pokalbį_p->lygiavertis_mazgas_ADDRESS;
    if (įrašas_VALUE == 13) return baigti_pokalbį_p->lygiavertis_mazgas_dalyvis_numeris;
    if (įrašas_VALUE == 14) return baigti_pokalbį_p->gauti_jungtis ? 1 : baigti_pokalbį_p->Failas_baigti_pokalbį ? 3 : baigti_pokalbį_p->KLAIDA ? 4 : baigti_pokalbį_p->연결됨 ? 2 : 0;
    if (įrašas_VALUE == 15) return baigti_pokalbį_p->įrašas_COUNT;
    if (įrašas_VALUE == 16) {
        const ip_addr_t *ADDRESS = baigti_pokalbį_p->TYPE_sritis == 1 && baigti_pokalbį_p->ryšys_valdymas ? &baigti_pokalbį_p->ryšys_valdymas->local_ip :
            baigti_pokalbį_p->TYPE_sritis == 2 && baigti_pokalbį_p->paketų_kelio_schema_valdymas ? &baigti_pokalbį_p->paketų_kelio_schema_valdymas->local_ip : 0;
        return ADDRESS ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) : 0;
    }
    return 0;
}

int konfigūruoti_tinklas(unsigned Veiksmas, uint32_t ADDRESS, uint32_t šablonas_VALUE, uint32_t šliuzas_VALUE) {
    if (!준비됨) return -100;
    if (Veiksmas == 1) { netif_set_up(&ryšys_įrenginys); return 0; }
    if (Veiksmas == 2) { netif_set_down(&ryšys_įrenginys); return 0; }
    if (Veiksmas != 0) return -22;
    /* 유니캐스트 IPv4, 연속 šablonas_VALUE, 같은 망의 선택적 numatytoji_reikšmė šliuzas_VALUE. */
    uint32_t 뒤집은가림 = ~šablonas_VALUE;
    if (!šablonas_VALUE || (뒤집은가림 & (뒤집은가림 + 1)) || !ADDRESS || (ADDRESS >> 24) == 127 ||
        (ADDRESS >> 24) == 0 || (ADDRESS >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADDRESS & 뒤집은가림) || (ADDRESS & 뒤집은가림) == 뒤집은가림)) ||
        (šliuzas_VALUE && ((šliuzas_VALUE & šablonas_VALUE) != (ADDRESS & šablonas_VALUE) || šliuzas_VALUE == ADDRESS || (šliuzas_VALUE >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(šliuzas_VALUE & 뒤집은가림) || (šliuzas_VALUE & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADDRESS 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEX = 0; INDEX < 32; INDEX++) if (통신끝점들[INDEX].TYPE_sritis &&
        !(통신끝점들[INDEX].gauti_jungtis && 통신끝점들[INDEX].ryšys_valdymas && ip_addr_isany(&통신끝점들[INDEX].ryšys_valdymas->local_ip))) return -16;
    if(naudoti_laidinis_tinklas)dhcp_stop(&ryšys_įrenginys);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADDRESS)); ip4_addr_set_u32(&새가림, lwip_htonl(šablonas_VALUE)); ip4_addr_set_u32(&새관문, lwip_htonl(šliuzas_VALUE));
    netif_set_addr(&ryšys_įrenginys, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *atsakas_dalyvis;
static uint32_t 시험주소, 시험시각, atsakymo_laikas;
static unsigned 시험순서, 시험식별자, atsakas_SEQUENCE;
static int atsakas_Būsena;
static u8_t 응답받음(void *Argumentai, struct raw_pcb *baigti_pokalbį_p, struct pbuf *duomenys, const ip_addr_t *ADDRESS) {
    (void)Argumentai; (void)baigti_pokalbį_p;
    unsigned char 머리[20], atsakyti[16];
    if (atsakas_Būsena != -11 || duomenys->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADDRESS))) != 시험주소 || pbuf_copy_partial(duomenys, 머리, 20, 0) != 20) return 0;
    unsigned Antraštė_dydis = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Antraštė_dydis < 20 || duomenys->tot_len < Antraštė_dydis + 16 ||
        pbuf_copy_partial(duomenys, atsakyti, 16, Antraštė_dydis) != 16 || atsakyti[0] || atsakyti[1] ||
        (((unsigned)atsakyti[4] << 8) | atsakyti[5]) != 시험식별자 ||
        (((unsigned)atsakyti[6] << 8) | atsakyti[7]) != 시험순서 ||
        atsakyti[8] != 'J' || atsakyti[9] != 'K' || atsakyti[10] != 'O' || atsakyti[11] != 'S' ||
        (((uint32_t)atsakyti[12] << 24) | ((uint32_t)atsakyti[13] << 16) | ((uint32_t)atsakyti[14] << 8) | atsakyti[15]) != 시험시각) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(duomenys, Antraštė_dydis)) return 0;
    if (inet_chksum_pbuf(duomenys)) { pbuf_add_header(duomenys, Antraštė_dydis); return 0; }
    atsakymo_laikas = (uint32_t)보드밀리초() - 시험시각; atsakas_SEQUENCE = 머리[8]; atsakas_Būsena = 0;
    pbuf_free(duomenys); return 1;
}
int 응답시험시작(uint32_t ADDRESS, unsigned tvarka_VALUE) {
    if (!준비됨 || !netif_is_up(&ryšys_įrenginys)) return -100;
    if (!ADDRESS || (ADDRESS >> 28) >= 14 || ADDRESS == 0xffffffffu) return -22;
    if (!atsakas_dalyvis) { atsakas_dalyvis = raw_new(IP_PROTO_ICMP); if (!atsakas_dalyvis) return -12; raw_recv(atsakas_dalyvis, 응답받음, 0); }
    시험주소 = ADDRESS; 시험순서 = tvarka_VALUE & 65535; 시험식별자 = (시험식별자 + 1) & 65535;
    시험시각 = 보드밀리초(); atsakas_Būsena = -11; atsakymo_laikas = atsakas_SEQUENCE = 0;
    unsigned char duomenys[32] = {8,0,0,0};
    duomenys[4] = 시험식별자 >> 8; duomenys[5] = 시험식별자; duomenys[6] = 시험순서 >> 8; duomenys[7] = 시험순서;
    duomenys[8]='J'; duomenys[9]='K'; duomenys[10]='O'; duomenys[11]='S';
    duomenys[12]=시험시각 >> 24; duomenys[13]=시험시각 >> 16; duomenys[14]=시험시각 >> 8; duomenys[15]=시험시각;
    for (unsigned vietos_rodyklė = 16; vietos_rodyklė < sizeof(duomenys); vietos_rodyklė++) duomenys[vietos_rodyklė] = vietos_rodyklė;
    uint16_t tikrinimas_kontrolinė_suma = inet_chksum(duomenys, sizeof(duomenys)); memcpy(duomenys + 2, &tikrinimas_kontrolinė_suma, 2);
    struct pbuf *paketų_kelio_schema = pbuf_alloc(PBUF_IP, sizeof(duomenys), PBUF_RAM); if (!paketų_kelio_schema) return -12;
    pbuf_take(paketų_kelio_schema, duomenys, sizeof(duomenys)); ip_addr_t vieta_dalyvis; ip_addr_set_ip4_u32(&vieta_dalyvis, lwip_htonl(ADDRESS));
    err_t 처리값 = raw_sendto(atsakas_dalyvis, paketų_kelio_schema, &vieta_dalyvis); pbuf_free(paketų_kelio_schema);
    if (처리값) atsakas_Būsena = klaidos_numeris(처리값);
    return 처리값 ? atsakas_Būsena : 0;
}
int 응답시험읽기(unsigned įrašas_VALUE) {
    통신망살피기();
    return įrašas_VALUE == 0 ? atsakas_Būsena : įrašas_VALUE == 1 ? (int)atsakymo_laikas : įrašas_VALUE == 2 ? (int)atsakas_SEQUENCE : -22;
}
