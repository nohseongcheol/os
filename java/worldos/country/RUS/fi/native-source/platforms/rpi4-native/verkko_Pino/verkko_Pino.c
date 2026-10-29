#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "verkko_Pino.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../etä_ARVO/etä_ARVO.h"
#include "lanka_verkko.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define kone_rekisteri(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif yhteys_laite;
static int 준비됨, kysely;
static int käyttö_lanka_verkko;
static unsigned saada_kulutus, 수신탈출, saada_virhe;
static unsigned char saada_tietopuskuri[1600];
static unsigned char lähettää_data[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t SAATU_HINTA_datagrammi_LASKE, 보낸전문수, SAATU_HINTA_tavu_LASKE, 보낸바이트수, 버린전문수;
typedef struct {
    int TYYPPI_alue, saada_portti, tietojärjestelmät_Odottaa, 연결됨, Tiedosto_lopettaa_puhelu, VIRHE;
    struct tcp_pcb *yhteys_ohjain;
    struct udp_pcb *datagrammi_ohjain;
    unsigned etukamera_merkintä, merkintä_LASKE;
    unsigned char data[4096];
    unsigned 길이목록[4], 접속번호들[4], vertaissolmu_päätepiste_numero;
    uint32_t 주소목록[4], vertaissolmu_OSOITE;
} vastake_päätepiste_3db661a2;
static vastake_päätepiste_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int virhenumero(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static vastake_päätepiste_3db661a2 *noutaa_ARVO(int Tiedosto_kahva) { return Tiedosto_kahva >= 0 && Tiedosto_kahva < 32 && 통신끝점들[Tiedosto_kahva].TYYPPI_alue ? &통신끝점들[Tiedosto_kahva] : 0; }
static int 예약하기(int TYYPPI_alue) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TYYPPI_alue) {
        memset(&통신끝점들[순번], 0, sizeof(vastake_päätepiste_3db661a2)); 통신끝점들[순번].TYYPPI_alue = TYYPPI_alue; 통신끝점들[순번].tietojärjestelmät_Odottaa = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned merkkikoodi) { lähettää_data[(송신앞자리 + 송신개수++) % sizeof(lähettää_data)] = merkkikoodi; }
static err_t tulos(struct netif *kohde_LASKE, struct pbuf *data_toimi, const ip4_addr_t *OSOITE) {
    (void)kohde_LASKE; (void)OSOITE;
    if (data_toimi->tot_len > 1500 || 송신개수 + 2 * data_toimi->tot_len + 2 > sizeof(lähettää_data)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Seuraava_SIIRTYMÄ = data_toimi; Seuraava_SIIRTYMÄ; Seuraava_SIIRTYMÄ = Seuraava_SIIRTYMÄ->next) for (unsigned 순번 = 0; 순번 < Seuraava_SIIRTYMÄ->len; 순번++) {
        unsigned merkkikoodi = ((unsigned char *)Seuraava_SIIRTYMÄ->payload)[순번];
        if (merkkikoodi == 192 || merkkikoodi == 219) { 내보내기(219); 내보내기(merkkikoodi == 192 ? 220 : 221); } else 내보내기(merkkikoodi);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += data_toimi->tot_len; return ERR_OK;
}
static err_t Valmistele_CLR(struct netif *kohde_LASKE) { kohde_LASKE->name[0] = 's'; kohde_LASKE->name[1] = 'l'; kohde_LASKE->mtu = 1500; kohde_LASKE->output = tulos; return ERR_OK; }
void Valmistele_verkko(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    kone_rekisteri(보조장치 + 4) |= 1; kone_rekisteri(보조장치 + 0x60) = 0; kone_rekisteri(보조장치 + 0x44) = 0;
    kone_rekisteri(보조장치 + 0x48) = 0xc6; kone_rekisteri(보조장치 + 0x4c) = 3; kone_rekisteri(보조장치 + 0x68) = 270; kone_rekisteri(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t Internet_osoite, bittipeite, yhdyskäytävän_osoite;
    käyttö_lanka_verkko=유선장치있음();
    ip4_addr_set_u32(&Internet_osoite, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bittipeite, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&yhdyskäytävän_osoite, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&yhteys_laite, &Internet_osoite, &bittipeite, &yhdyskäytävän_osoite, 0, käyttö_lanka_verkko?Valmistele_lanka_verkko:Valmistele_CLR, käyttö_lanka_verkko?ethernet_input:ip4_input))return;
    netif_set_default(&yhteys_laite); netif_set_up(&yhteys_laite);if(!käyttö_lanka_verkko)netif_set_link_up(&yhteys_laite); 준비됨 = 1;
    Valmistele_etä();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *lähettäminen_ohjain_Esto, struct pbuf *data_toimi, err_t VIRHE) {
    vastake_päätepiste_3db661a2 *merkkijono_data = 부가인수; (void)lähettäminen_ohjain_Esto; (void)VIRHE;
    if (!data_toimi) { merkkijono_data->Tiedosto_lopettaa_puhelu = 1; return ERR_OK; }
    if (data_toimi->tot_len > sizeof(merkkijono_data->data) - merkkijono_data->merkintä_LASKE) return ERR_MEM;
    unsigned nykyinen_toimi = (merkkijono_data->etukamera_merkintä + merkkijono_data->merkintä_LASKE) % sizeof(merkkijono_data->data);
    for (struct pbuf *Seuraava_SIIRTYMÄ = data_toimi; Seuraava_SIIRTYMÄ; Seuraava_SIIRTYMÄ = Seuraava_SIIRTYMÄ->next) for (unsigned 순번 = 0; 순번 < Seuraava_SIIRTYMÄ->len; 순번++) {
        merkkijono_data->data[nykyinen_toimi] = ((unsigned char *)Seuraava_SIIRTYMÄ->payload)[순번]; nykyinen_toimi = (nykyinen_toimi + 1) % sizeof(merkkijono_data->data);
    }
    merkkijono_data->merkintä_LASKE += data_toimi->tot_len; pbuf_free(data_toimi); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t VIRHE) { vastake_päätepiste_3db661a2 *merkkijono_data = 부가인수; merkkijono_data->yhteys_ohjain = 0; merkkijono_data->VIRHE = virhenumero(VIRHE); }
static void 되부름목록(vastake_päätepiste_3db661a2 *merkkijono_data) { tcp_arg(merkkijono_data->yhteys_ohjain, merkkijono_data); tcp_recv(merkkijono_data->yhteys_ohjain, 수신됨); tcp_err(merkkijono_data->yhteys_ohjain, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *lähettäminen_ohjain_Esto, err_t VIRHE) {
    vastake_päätepiste_3db661a2 *merkkijono_data = 부가인수; (void)lähettäminen_ohjain_Esto; if (VIRHE) merkkijono_data->VIRHE = virhenumero(VIRHE); else merkkijono_data->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *lähettäminen_ohjain_Esto, err_t VIRHE) {
    vastake_päätepiste_3db661a2 *pää = 부가인수; if (VIRHE) return VIRHE;
    int Tiedosto_kahva = 예약하기(1); if (Tiedosto_kahva < 0) return ERR_MEM;
    vastake_päätepiste_3db661a2 *merkkijono_data = &통신끝점들[Tiedosto_kahva]; merkkijono_data->yhteys_ohjain = lähettäminen_ohjain_Esto; merkkijono_data->연결됨 = 1; merkkijono_data->tietojärjestelmät_Odottaa = (int)(pää - 통신끝점들);
    merkkijono_data->vertaissolmu_OSOITE = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&lähettäminen_ohjain_Esto->remote_ip))); merkkijono_data->vertaissolmu_päätepiste_numero = lähettäminen_ohjain_Esto->remote_port;
    되부름목록(merkkijono_data); return ERR_OK;
}
static void datagrammi(void *부가인수, struct udp_pcb *lähettäminen_ohjain_Esto, struct pbuf *data_toimi, const ip_addr_t *OSOITE, u16_t portin_numero) {
    vastake_päätepiste_3db661a2 *merkkijono_data = 부가인수; (void)lähettäminen_ohjain_Esto;
    if (merkkijono_data->merkintä_LASKE < 4 && data_toimi->tot_len <= 512) {
        unsigned sijainti = (merkkijono_data->etukamera_merkintä + merkkijono_data->merkintä_LASKE) % 4;
        pbuf_copy_partial(data_toimi, merkkijono_data->data + sijainti * 512, data_toimi->tot_len, 0);
        merkkijono_data->길이목록[sijainti] = data_toimi->tot_len; merkkijono_data->접속번호들[sijainti] = portin_numero;
        merkkijono_data->주소목록[sijainti] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(OSOITE))); merkkijono_data->merkintä_LASKE++;
    }
    pbuf_free(data_toimi);
}
int Luo_vastake_päätepiste(int TYYPPI_alue) {
    if (!준비됨) return -100;
    if (TYYPPI_alue != 1 && TYYPPI_alue != 2) return -93;
    int Tiedosto_kahva = 예약하기(TYYPPI_alue); if (Tiedosto_kahva < 0) return Tiedosto_kahva;
    vastake_päätepiste_3db661a2 *merkkijono_data = &통신끝점들[Tiedosto_kahva];
    if (TYYPPI_alue == 1) { merkkijono_data->yhteys_ohjain = tcp_new(); if (merkkijono_data->yhteys_ohjain) 되부름목록(merkkijono_data); }
    else { merkkijono_data->datagrammi_ohjain = udp_new(); if (merkkijono_data->datagrammi_ohjain) udp_recv(merkkijono_data->datagrammi_ohjain, datagrammi, merkkijono_data); }
    if (!merkkijono_data->yhteys_ohjain && !merkkijono_data->datagrammi_ohjain) { merkkijono_data->TYYPPI_alue = 0; return -12; } return Tiedosto_kahva;
}
int NET_BIND(int Tiedosto_kahva, uint32_t OSOITE, unsigned portin_numero) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data) return -9;
    if (portin_numero > 65535 || (OSOITE && OSOITE != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&yhteys_laite))) && OSOITE != 0x7f000001)) return -99;
    ip_addr_t Internet_osoite; ip_addr_set_ip4_u32(&Internet_osoite, lwip_htonl(OSOITE));
    err_t 보조항목 = merkkijono_data->TYYPPI_alue == 1 ? tcp_bind(merkkijono_data->yhteys_ohjain, &Internet_osoite, portin_numero) : udp_bind(merkkijono_data->datagrammi_ohjain, &Internet_osoite, portin_numero); return 보조항목 ? virhenumero(보조항목) : 0;
}
void 통신주소재사용(int Tiedosto_kahva) { vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (merkkijono_data && merkkijono_data->yhteys_ohjain) ip_set_option(merkkijono_data->yhteys_ohjain, SOF_REUSEADDR); }
int NET_kuunnella(int Tiedosto_kahva) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data || merkkijono_data->TYYPPI_alue != 1) return -9;
    if (merkkijono_data->saada_portti) return 0;
    err_t 보조항목; struct tcp_pcb *lähettäminen_ohjain_Esto = tcp_listen_with_backlog_and_err(merkkijono_data->yhteys_ohjain, 4, &보조항목);
    if (!lähettäminen_ohjain_Esto) return virhenumero(보조항목); merkkijono_data->yhteys_ohjain = lähettäminen_ohjain_Esto; merkkijono_data->saada_portti = 1; tcp_arg(lähettäminen_ohjain_Esto, merkkijono_data); tcp_accept(lähettäminen_ohjain_Esto, 연결받음); return 0;
}
int NET_YHDISTÄ(int Tiedosto_kahva, uint32_t OSOITE, unsigned portin_numero) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data || merkkijono_data->TYYPPI_alue != 1) return -9;
    if (merkkijono_data->VIRHE) return merkkijono_data->VIRHE;
    if (merkkijono_data->연결됨) return 0;
    if (merkkijono_data->vertaissolmu_päätepiste_numero) return -115;
    if (!portin_numero || portin_numero > 65535 || !OSOITE) return -22;
    ip_addr_t Internet_osoite; ip_addr_set_ip4_u32(&Internet_osoite, lwip_htonl(OSOITE));
    merkkijono_data->vertaissolmu_OSOITE = OSOITE; merkkijono_data->vertaissolmu_päätepiste_numero = portin_numero;
    err_t 보조항목 = tcp_connect(merkkijono_data->yhteys_ohjain, &Internet_osoite, portin_numero, 연결됨); return 보조항목 ? virhenumero(보조항목) : -115;
}
int NET_hyväksyä(int Tiedosto_kahva) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data || !merkkijono_data->saada_portti) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TYYPPI_alue == 1 && 통신끝점들[순번].tietojärjestelmät_Odottaa == Tiedosto_kahva) { 통신끝점들[순번].tietojärjestelmät_Odottaa = -1; return 순번; }
    return -11;
}
int NET_lukea(int Tiedosto_kahva, void *data, unsigned kohde_LASKE) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data || merkkijono_data->TYYPPI_alue != 1) return -9;
    if (!kohde_LASKE) return 0; if (!merkkijono_data->merkintä_LASKE) return merkkijono_data->VIRHE ? merkkijono_data->VIRHE : merkkijono_data->Tiedosto_lopettaa_puhelu ? 0 : -11;
    if (kohde_LASKE > merkkijono_data->merkintä_LASKE) kohde_LASKE = merkkijono_data->merkintä_LASKE;
    for (unsigned 순번 = 0; 순번 < kohde_LASKE; 순번++) { ((unsigned char *)data)[순번] = merkkijono_data->data[merkkijono_data->etukamera_merkintä]; merkkijono_data->etukamera_merkintä = (merkkijono_data->etukamera_merkintä + 1) % sizeof(merkkijono_data->data); }
    merkkijono_data->merkintä_LASKE -= kohde_LASKE; if (merkkijono_data->yhteys_ohjain) tcp_recved(merkkijono_data->yhteys_ohjain, kohde_LASKE); return kohde_LASKE;
}
int NET_kirjoitus(int Tiedosto_kahva, const void *data, unsigned kohde_LASKE) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data || merkkijono_data->TYYPPI_alue != 1) return -9;
    if (merkkijono_data->VIRHE) return merkkijono_data->VIRHE; if (!merkkijono_data->yhteys_ohjain || !merkkijono_data->연결됨) return -107;
    if (!kohde_LASKE) return 0; if (kohde_LASKE > tcp_sndbuf(merkkijono_data->yhteys_ohjain)) kohde_LASKE = tcp_sndbuf(merkkijono_data->yhteys_ohjain);
    if (!kohde_LASKE) return -11; if (kohde_LASKE > 1024) kohde_LASKE = 1024;
    err_t 보조항목 = tcp_write(merkkijono_data->yhteys_ohjain, data, kohde_LASKE, TCP_WRITE_FLAG_COPY); if (보조항목) return virhenumero(보조항목);
    tcp_output(merkkijono_data->yhteys_ohjain); return kohde_LASKE;
}
int lähettää_datagrammi(int Tiedosto_kahva, const void *data, unsigned kohde_LASKE, uint32_t OSOITE, unsigned portin_numero) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data || merkkijono_data->TYYPPI_alue != 2) return -9;
    if (kohde_LASKE > 512) return -90; if (!portin_numero || portin_numero > 65535) return -22;
    struct pbuf *data_toimi = pbuf_alloc(PBUF_TRANSPORT, kohde_LASKE, PBUF_RAM); if (!data_toimi) return -11;
    pbuf_take(data_toimi, data, kohde_LASKE); ip_addr_t Internet_osoite; ip_addr_set_ip4_u32(&Internet_osoite, lwip_htonl(OSOITE));
    err_t 보조항목 = udp_sendto(merkkijono_data->datagrammi_ohjain, data_toimi, &Internet_osoite, portin_numero); pbuf_free(data_toimi); return 보조항목 ? virhenumero(보조항목) : (int)kohde_LASKE;
}
int saada_datagrammi(int Tiedosto_kahva, void *data, unsigned kohde_LASKE) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data || merkkijono_data->TYYPPI_alue != 2) return -9;
    if (!merkkijono_data->merkintä_LASKE) return -11; unsigned nykyinen_toimi = merkkijono_data->etukamera_merkintä;
    if (kohde_LASKE > merkkijono_data->길이목록[nykyinen_toimi]) kohde_LASKE = merkkijono_data->길이목록[nykyinen_toimi]; memcpy(data, merkkijono_data->data + nykyinen_toimi * 512, kohde_LASKE);
    merkkijono_data->vertaissolmu_päätepiste_numero = merkkijono_data->접속번호들[nykyinen_toimi]; merkkijono_data->vertaissolmu_OSOITE = merkkijono_data->주소목록[nykyinen_toimi]; merkkijono_data->etukamera_merkintä = (nykyinen_toimi + 1) % 4; merkkijono_data->merkintä_LASKE--; return kohde_LASKE;
}
unsigned verkko_portin_numero(int Tiedosto_kahva) { vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); return !merkkijono_data ? 0 : merkkijono_data->yhteys_ohjain ? merkkijono_data->yhteys_ohjain->local_port : merkkijono_data->datagrammi_ohjain ? merkkijono_data->datagrammi_ohjain->local_port : 0; }
unsigned vertaissolmu_portin_numero(int Tiedosto_kahva) { vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); return merkkijono_data ? merkkijono_data->vertaissolmu_päätepiste_numero : 0; }
uint32_t NET_vertaissolmu_OSOITE(int Tiedosto_kahva) { vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); return merkkijono_data ? merkkijono_data->vertaissolmu_OSOITE : 0; }
void Sulje_verkko(int Tiedosto_kahva) {
    vastake_päätepiste_3db661a2 *merkkijono_data = noutaa_ARVO(Tiedosto_kahva); if (!merkkijono_data) return;
    if (merkkijono_data->saada_portti) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TYYPPI_alue && 통신끝점들[순번].tietojärjestelmät_Odottaa == Tiedosto_kahva) Sulje_verkko(순번);
    if (merkkijono_data->yhteys_ohjain) {
        tcp_arg(merkkijono_data->yhteys_ohjain, 0); if (merkkijono_data->saada_portti) tcp_accept(merkkijono_data->yhteys_ohjain, 0); else { tcp_recv(merkkijono_data->yhteys_ohjain, 0); tcp_err(merkkijono_data->yhteys_ohjain, 0); }
        if (tcp_close(merkkijono_data->yhteys_ohjain) != ERR_OK) tcp_abort(merkkijono_data->yhteys_ohjain);
    }
    if (merkkijono_data->datagrammi_ohjain) udp_remove(merkkijono_data->datagrammi_ohjain); merkkijono_data->TYYPPI_alue = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || kysely) return; kysely = 1;
    if(käyttö_lanka_verkko)유선망살피기(&yhteys_laite);
    for (unsigned budjetti = 0; !käyttö_lanka_verkko && budjetti < 4096 && (kone_rekisteri(보조장치 + 0x54) & 1); budjetti++) {
        unsigned merkkikoodi = kone_rekisteri(보조장치 + 0x40) & 255;
        if (merkkikoodi == 192) {
            if (saada_kulutus && !saada_virhe && !수신탈출) {
                struct pbuf *data_toimi = pbuf_alloc(PBUF_RAW, saada_kulutus, PBUF_POOL);
                if (data_toimi) { SAATU_HINTA_datagrammi_LASKE++; SAATU_HINTA_tavu_LASKE += saada_kulutus; pbuf_take(data_toimi, saada_tietopuskuri, saada_kulutus); if (yhteys_laite.input(data_toimi, &yhteys_laite) != ERR_OK) { 버린전문수++; pbuf_free(data_toimi); } }
                else 버린전문수++;
            }
            else if (saada_kulutus) 버린전문수++;
            saada_kulutus = saada_virhe = 수신탈출 = 0;
        } else if (merkkikoodi == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (merkkikoodi != 220 && merkkikoodi != 221) saada_virhe = 1; merkkikoodi = merkkikoodi == 220 ? 192 : 219; 수신탈출 = 0; }
            if (saada_kulutus < sizeof(saada_tietopuskuri)) saada_tietopuskuri[saada_kulutus++] = merkkikoodi; else saada_virhe = 1;
        }
    }
    netif_poll(&yhteys_laite); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned budjetti = 0; budjetti < 4096 && 송신개수 && (kone_rekisteri(보조장치 + 0x54) & 0x20); budjetti++) {
        kone_rekisteri(보조장치 + 0x40) = lähettää_data[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(lähettää_data); 송신개수--;
    }
    kysely = 0;
}

/* Asetukset·조회는 lwIP의 todellinen_data 인터페이스와 lopettaa_puhelu_piste 표를 사용한다. */
uint32_t lukea_verkko_tila(unsigned merkintä_ARVO_962f286b, unsigned INDEKSI) {
    if(merkintä_ARVO_962f286b==20)return käyttö_lanka_verkko;
    if(merkintä_ARVO_962f286b==21)return 준비됨&&netif_is_link_up(&yhteys_laite);
    if(merkintä_ARVO_962f286b==22)return käyttö_lanka_verkko?lanka_verkko_Tilastotiedot(5):0;
    if (!준비됨) return 0;
    if(käyttö_lanka_verkko&&merkintä_ARVO_962f286b>=4&&merkintä_ARVO_962f286b<=8)return lanka_verkko_Tilastotiedot(merkintä_ARVO_962f286b-4);
    if (merkintä_ARVO_962f286b == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&yhteys_laite)));
    if (merkintä_ARVO_962f286b == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&yhteys_laite)));
    if (merkintä_ARVO_962f286b == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&yhteys_laite)));
    if (merkintä_ARVO_962f286b == 3) return netif_is_up(&yhteys_laite) != 0;
    if (merkintä_ARVO_962f286b == 4) return SAATU_HINTA_datagrammi_LASKE;
    if (merkintä_ARVO_962f286b == 5) return 보낸전문수;
    if (merkintä_ARVO_962f286b == 6) return SAATU_HINTA_tavu_LASKE;
    if (merkintä_ARVO_962f286b == 7) return 보낸바이트수;
    if (merkintä_ARVO_962f286b == 8) return 버린전문수;
    if (merkintä_ARVO_962f286b == 9) return 송신개수;
    if (INDEKSI >= 32) return 0;
    vastake_päätepiste_3db661a2 *lopettaa_puhelu_piste = &통신끝점들[INDEKSI];
    if (merkintä_ARVO_962f286b == 10) return lopettaa_puhelu_piste->TYYPPI_alue;
    if (!lopettaa_puhelu_piste->TYYPPI_alue) return 0;
    if (merkintä_ARVO_962f286b == 11) return verkko_portin_numero(INDEKSI);
    if (merkintä_ARVO_962f286b == 12) return lopettaa_puhelu_piste->vertaissolmu_OSOITE;
    if (merkintä_ARVO_962f286b == 13) return lopettaa_puhelu_piste->vertaissolmu_päätepiste_numero;
    if (merkintä_ARVO_962f286b == 14) return lopettaa_puhelu_piste->saada_portti ? 1 : lopettaa_puhelu_piste->Tiedosto_lopettaa_puhelu ? 3 : lopettaa_puhelu_piste->VIRHE ? 4 : lopettaa_puhelu_piste->연결됨 ? 2 : 0;
    if (merkintä_ARVO_962f286b == 15) return lopettaa_puhelu_piste->merkintä_LASKE;
    if (merkintä_ARVO_962f286b == 16) {
        const ip_addr_t *OSOITE = lopettaa_puhelu_piste->TYYPPI_alue == 1 && lopettaa_puhelu_piste->yhteys_ohjain ? &lopettaa_puhelu_piste->yhteys_ohjain->local_ip :
            lopettaa_puhelu_piste->TYYPPI_alue == 2 && lopettaa_puhelu_piste->datagrammi_ohjain ? &lopettaa_puhelu_piste->datagrammi_ohjain->local_ip : 0;
        return OSOITE ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(OSOITE))) : 0;
    }
    return 0;
}

int määrittää_verkko(unsigned Toiminto, uint32_t OSOITE, uint32_t peite_ARVO, uint32_t yhdyskäytävä_ARVO) {
    if (!준비됨) return -100;
    if (Toiminto == 1) { netif_set_up(&yhteys_laite); return 0; }
    if (Toiminto == 2) { netif_set_down(&yhteys_laite); return 0; }
    if (Toiminto != 0) return -22;
    /* 유니캐스트 IPv4, 연속 peite_ARVO, 같은 망의 선택적 oletusarvo yhdyskäytävä_ARVO. */
    uint32_t 뒤집은가림 = ~peite_ARVO;
    if (!peite_ARVO || (뒤집은가림 & (뒤집은가림 + 1)) || !OSOITE || (OSOITE >> 24) == 127 ||
        (OSOITE >> 24) == 0 || (OSOITE >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(OSOITE & 뒤집은가림) || (OSOITE & 뒤집은가림) == 뒤집은가림)) ||
        (yhdyskäytävä_ARVO && ((yhdyskäytävä_ARVO & peite_ARVO) != (OSOITE & peite_ARVO) || yhdyskäytävä_ARVO == OSOITE || (yhdyskäytävä_ARVO >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(yhdyskäytävä_ARVO & 뒤집은가림) || (yhdyskäytävä_ARVO & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 OSOITE 변경으로 몰래 끊지 않는다. */
    for (unsigned INDEKSI = 0; INDEKSI < 32; INDEKSI++) if (통신끝점들[INDEKSI].TYYPPI_alue &&
        !(통신끝점들[INDEKSI].saada_portti && 통신끝점들[INDEKSI].yhteys_ohjain && ip_addr_isany(&통신끝점들[INDEKSI].yhteys_ohjain->local_ip))) return -16;
    if(käyttö_lanka_verkko)dhcp_stop(&yhteys_laite);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(OSOITE)); ip4_addr_set_u32(&새가림, lwip_htonl(peite_ARVO)); ip4_addr_set_u32(&새관문, lwip_htonl(yhdyskäytävä_ARVO));
    netif_set_addr(&yhteys_laite, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *vastaus_päätepiste;
static uint32_t testi_OSOITE, testi_AIKA, vasteaika;
static unsigned testi_JONO, testi_tunniste, vastaus_JONO;
static int vastaus_Tila;
static u8_t 응답받음(void *argumentit, struct raw_pcb *lopettaa_puhelu_piste, struct pbuf *data, const ip_addr_t *OSOITE) {
    (void)argumentit; (void)lopettaa_puhelu_piste;
    unsigned char 머리[20], palaute[16];
    if (vastaus_Tila != -11 || data->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(OSOITE))) != testi_OSOITE || pbuf_copy_partial(data, 머리, 20, 0) != 20) return 0;
    unsigned otsikko_muuttaa_kokoa = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || otsikko_muuttaa_kokoa < 20 || data->tot_len < otsikko_muuttaa_kokoa + 16 ||
        pbuf_copy_partial(data, palaute, 16, otsikko_muuttaa_kokoa) != 16 || palaute[0] || palaute[1] ||
        (((unsigned)palaute[4] << 8) | palaute[5]) != testi_tunniste ||
        (((unsigned)palaute[6] << 8) | palaute[7]) != testi_JONO ||
        palaute[8] != 'J' || palaute[9] != 'K' || palaute[10] != 'O' || palaute[11] != 'S' ||
        (((uint32_t)palaute[12] << 24) | ((uint32_t)palaute[13] << 16) | ((uint32_t)palaute[14] << 8) | palaute[15]) != testi_AIKA) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(data, otsikko_muuttaa_kokoa)) return 0;
    if (inet_chksum_pbuf(data)) { pbuf_add_header(data, otsikko_muuttaa_kokoa); return 0; }
    vasteaika = (uint32_t)보드밀리초() - testi_AIKA; vastaus_JONO = 머리[8]; vastaus_Tila = 0;
    pbuf_free(data); return 1;
}
int alku_vastaus_testi(uint32_t OSOITE, unsigned tilata_ARVO) {
    if (!준비됨 || !netif_is_up(&yhteys_laite)) return -100;
    if (!OSOITE || (OSOITE >> 28) >= 14 || OSOITE == 0xffffffffu) return -22;
    if (!vastaus_päätepiste) { vastaus_päätepiste = raw_new(IP_PROTO_ICMP); if (!vastaus_päätepiste) return -12; raw_recv(vastaus_päätepiste, 응답받음, 0); }
    testi_OSOITE = OSOITE; testi_JONO = tilata_ARVO & 65535; testi_tunniste = (testi_tunniste + 1) & 65535;
    testi_AIKA = 보드밀리초(); vastaus_Tila = -11; vasteaika = vastaus_JONO = 0;
    unsigned char data[32] = {8,0,0,0};
    data[4] = testi_tunniste >> 8; data[5] = testi_tunniste; data[6] = testi_JONO >> 8; data[7] = testi_JONO;
    data[8]='J'; data[9]='K'; data[10]='O'; data[11]='S';
    data[12]=testi_AIKA >> 24; data[13]=testi_AIKA >> 16; data[14]=testi_AIKA >> 8; data[15]=testi_AIKA;
    for (unsigned sijainti = 16; sijainti < sizeof(data); sijainti++) data[sijainti] = sijainti;
    uint16_t tarkistaminen_tarkistussumma = inet_chksum(data, sizeof(data)); memcpy(data + 2, &tarkistaminen_tarkistussumma, 2);
    struct pbuf *datagrammi = pbuf_alloc(PBUF_IP, sizeof(data), PBUF_RAM); if (!datagrammi) return -12;
    pbuf_take(datagrammi, data, sizeof(data)); ip_addr_t kohde_päätepiste; ip_addr_set_ip4_u32(&kohde_päätepiste, lwip_htonl(OSOITE));
    err_t 처리값 = raw_sendto(vastaus_päätepiste, datagrammi, &kohde_päätepiste); pbuf_free(datagrammi);
    if (처리값) vastaus_Tila = virhenumero(처리값);
    return 처리값 ? vastaus_Tila : 0;
}
int lukea_vastaus_testi(unsigned merkintä_ARVO_962f286b) {
    통신망살피기();
    return merkintä_ARVO_962f286b == 0 ? vastaus_Tila : merkintä_ARVO_962f286b == 1 ? (int)vasteaika : merkintä_ARVO_962f286b == 2 ? (int)vastaus_JONO : -22;
}
