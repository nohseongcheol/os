#include "../명명/기계연결이름.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "ağ_Yığın.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../uzak_değer/uzak_değer.h"
#include "kablolu_ağ.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define makine_yazmaç(첫째값) (*(volatile uint32_t *)(uintptr_t)(첫째값))
#define 보조장치 0xfe215000ul
extern uintptr_t 보드밀리초(void);
static struct netif cxn_cihaz;
static int 준비됨, yoklama;
static int kullanmak_kablolu_ağ;
static unsigned almak_kullanım, 수신탈출, almak_hata;
static unsigned char almak_veri_arabelleği[1600];
static unsigned char 송신자료[32768];
static unsigned 송신앞자리, 송신개수;
static uint32_t GETİRİ_veri_birimi_BAĞ_DEĞ_SAY, 보낸전문수, GETİRİ_bayt_BAĞ_DEĞ_SAY, 보낸바이트수, 버린전문수;
typedef struct {
    int TÜR_alan, almak_taşımak, bilgi_teknolojisi_Beklemede, 연결됨, Dosya_Bitiş, hata;
    struct tcp_pcb *cxn_denetim;
    struct udp_pcb *veri_birimi_denetim;
    unsigned ön_kamera_girdi, girdi_BAĞ_DEĞ_SAY;
    unsigned char veri[4096];
    unsigned 길이목록[4], 접속번호들[4], 상대창구번호;
    uint32_t 주소목록[4], eş_ADRES;
} yuva_uç_nokta_3db661a2;
static yuva_uç_nokta_3db661a2 통신끝점들[32];
u32_t sys_now(void) { return (u32_t)보드밀리초(); }
static int hata_numarası(err_t 보조항목) {
    return 보조항목 == ERR_MEM || 보조항목 == ERR_BUF || 보조항목 == ERR_WOULDBLOCK ? -11 : 보조항목 == ERR_USE ? -98 :
        보조항목 == ERR_RTE ? -101 : 보조항목 == ERR_RST ? -104 : 보조항목 == ERR_CONN ? -107 : 보조항목 == ERR_TIMEOUT ? -110 : -5;
}
static yuva_uç_nokta_3db661a2 *get_değer(int dosya_tanıtıcısı) { return dosya_tanıtıcısı >= 0 && dosya_tanıtıcısı < 32 && 통신끝점들[dosya_tanıtıcısı].TÜR_alan ? &통신끝점들[dosya_tanıtıcısı] : 0; }
static int 예약하기(int TÜR_alan) {
    for (int 순번 = 0; 순번 < 32; ++순번) if (!통신끝점들[순번].TÜR_alan) {
        memset(&통신끝점들[순번], 0, sizeof(yuva_uç_nokta_3db661a2)); 통신끝점들[순번].TÜR_alan = TÜR_alan; 통신끝점들[순번].bilgi_teknolojisi_Beklemede = -1; return 순번;
    }
    return -24;
}
static void 내보내기(unsigned kod_noktası) { 송신자료[(송신앞자리 + 송신개수++) % sizeof(송신자료)] = kod_noktası; }
static err_t çıktı(struct netif *öğe_BAĞ_DEĞ_SAY, struct pbuf *veri_konum, const ip4_addr_t *ADRES) {
    (void)öğe_BAĞ_DEĞ_SAY; (void)ADRES;
    if (veri_konum->tot_len > 1500 || 송신개수 + 2 * veri_konum->tot_len + 2 > sizeof(송신자료)) return ERR_MEM;
    내보내기(192);
    for (struct pbuf *Sonraki_Ofset = veri_konum; Sonraki_Ofset; Sonraki_Ofset = Sonraki_Ofset->next) for (unsigned 순번 = 0; 순번 < Sonraki_Ofset->len; 순번++) {
        unsigned kod_noktası = ((unsigned char *)Sonraki_Ofset->payload)[순번];
        if (kod_noktası == 192 || kod_noktası == 219) { 내보내기(219); 내보내기(kod_noktası == 192 ? 220 : 221); } else 내보내기(kod_noktası);
    }
    내보내기(192); 보낸전문수++; 보낸바이트수 += veri_konum->tot_len; return ERR_OK;
}
static err_t Hazırlan_CLR(struct netif *öğe_BAĞ_DEĞ_SAY) { öğe_BAĞ_DEĞ_SAY->name[0] = 's'; öğe_BAĞ_DEĞ_SAY->name[1] = 'l'; öğe_BAĞ_DEĞ_SAY->mtu = 1500; öğe_BAĞ_DEĞ_SAY->output = çıktı; return ERR_OK; }
void Hazırlan_ağ(void) {
    if (준비됨) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    makine_yazmaç(보조장치 + 4) |= 1; makine_yazmaç(보조장치 + 0x60) = 0; makine_yazmaç(보조장치 + 0x44) = 0;
    makine_yazmaç(보조장치 + 0x48) = 0xc6; makine_yazmaç(보조장치 + 0x4c) = 3; makine_yazmaç(보조장치 + 0x68) = 270; makine_yazmaç(보조장치 + 0x60) = 3;
    lwip_init();
    ip4_addr_t İnternet_adresi, bit_maskesi, ağ_geçidi_adresi;
    kullanmak_kablolu_ağ=유선장치있음();
    ip4_addr_set_u32(&İnternet_adresi, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&bit_maskesi, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&ağ_geçidi_adresi, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&cxn_cihaz, &İnternet_adresi, &bit_maskesi, &ağ_geçidi_adresi, 0, kullanmak_kablolu_ağ?Hazırlan_kablolu_ağ:Hazırlan_CLR, kullanmak_kablolu_ağ?ethernet_input:ip4_input))return;
    netif_set_default(&cxn_cihaz); netif_set_up(&cxn_cihaz);if(!kullanmak_kablolu_ağ)netif_set_link_up(&cxn_cihaz); 준비됨 = 1;
    Hazırlan_uzak();
}
static err_t 수신됨(void *부가인수, struct tcp_pcb *통신제어블록, struct pbuf *veri_konum, err_t hata) {
    yuva_uç_nokta_3db661a2 *dize_veri = 부가인수; (void)통신제어블록; (void)hata;
    if (!veri_konum) { dize_veri->Dosya_Bitiş = 1; return ERR_OK; }
    if (veri_konum->tot_len > sizeof(dize_veri->veri) - dize_veri->girdi_BAĞ_DEĞ_SAY) return ERR_MEM;
    unsigned geçerli_konum = (dize_veri->ön_kamera_girdi + dize_veri->girdi_BAĞ_DEĞ_SAY) % sizeof(dize_veri->veri);
    for (struct pbuf *Sonraki_Ofset = veri_konum; Sonraki_Ofset; Sonraki_Ofset = Sonraki_Ofset->next) for (unsigned 순번 = 0; 순번 < Sonraki_Ofset->len; 순번++) {
        dize_veri->veri[geçerli_konum] = ((unsigned char *)Sonraki_Ofset->payload)[순번]; geçerli_konum = (geçerli_konum + 1) % sizeof(dize_veri->veri);
    }
    dize_veri->girdi_BAĞ_DEĞ_SAY += veri_konum->tot_len; pbuf_free(veri_konum); return ERR_OK;
}
static void 실패여부(void *부가인수, err_t hata) { yuva_uç_nokta_3db661a2 *dize_veri = 부가인수; dize_veri->cxn_denetim = 0; dize_veri->hata = hata_numarası(hata); }
static void 되부름목록(yuva_uç_nokta_3db661a2 *dize_veri) { tcp_arg(dize_veri->cxn_denetim, dize_veri); tcp_recv(dize_veri->cxn_denetim, 수신됨); tcp_err(dize_veri->cxn_denetim, 실패여부); }
static err_t 연결됨(void *부가인수, struct tcp_pcb *통신제어블록, err_t hata) {
    yuva_uç_nokta_3db661a2 *dize_veri = 부가인수; (void)통신제어블록; if (hata) dize_veri->hata = hata_numarası(hata); else dize_veri->연결됨 = 1; return ERR_OK;
}
static err_t 연결받음(void *부가인수, struct tcp_pcb *통신제어블록, err_t hata) {
    yuva_uç_nokta_3db661a2 *ana = 부가인수; if (hata) return hata;
    int dosya_tanıtıcısı = 예약하기(1); if (dosya_tanıtıcısı < 0) return ERR_MEM;
    yuva_uç_nokta_3db661a2 *dize_veri = &통신끝점들[dosya_tanıtıcısı]; dize_veri->cxn_denetim = 통신제어블록; dize_veri->연결됨 = 1; dize_veri->bilgi_teknolojisi_Beklemede = (int)(ana - 통신끝점들);
    dize_veri->eş_ADRES = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&통신제어블록->remote_ip))); dize_veri->상대창구번호 = 통신제어블록->remote_port;
    되부름목록(dize_veri); return ERR_OK;
}
static void veri_birimi(void *부가인수, struct udp_pcb *통신제어블록, struct pbuf *veri_konum, const ip_addr_t *ADRES, u16_t bağlantı_noktası_numarası) {
    yuva_uç_nokta_3db661a2 *dize_veri = 부가인수; (void)통신제어블록;
    if (dize_veri->girdi_BAĞ_DEĞ_SAY < 4 && veri_konum->tot_len <= 512) {
        unsigned konum_dizini = (dize_veri->ön_kamera_girdi + dize_veri->girdi_BAĞ_DEĞ_SAY) % 4;
        pbuf_copy_partial(veri_konum, dize_veri->veri + konum_dizini * 512, veri_konum->tot_len, 0);
        dize_veri->길이목록[konum_dizini] = veri_konum->tot_len; dize_veri->접속번호들[konum_dizini] = bağlantı_noktası_numarası;
        dize_veri->주소목록[konum_dizini] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADRES))); dize_veri->girdi_BAĞ_DEĞ_SAY++;
    }
    pbuf_free(veri_konum);
}
int açmak_yuva_uç_nokta(int TÜR_alan) {
    if (!준비됨) return -100;
    if (TÜR_alan != 1 && TÜR_alan != 2) return -93;
    int dosya_tanıtıcısı = 예약하기(TÜR_alan); if (dosya_tanıtıcısı < 0) return dosya_tanıtıcısı;
    yuva_uç_nokta_3db661a2 *dize_veri = &통신끝점들[dosya_tanıtıcısı];
    if (TÜR_alan == 1) { dize_veri->cxn_denetim = tcp_new(); if (dize_veri->cxn_denetim) 되부름목록(dize_veri); }
    else { dize_veri->veri_birimi_denetim = udp_new(); if (dize_veri->veri_birimi_denetim) udp_recv(dize_veri->veri_birimi_denetim, veri_birimi, dize_veri); }
    if (!dize_veri->cxn_denetim && !dize_veri->veri_birimi_denetim) { dize_veri->TÜR_alan = 0; return -12; } return dosya_tanıtıcısı;
}
int NET_BIND(int dosya_tanıtıcısı, uint32_t ADRES, unsigned bağlantı_noktası_numarası) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri) return -9;
    if (bağlantı_noktası_numarası > 65535 || (ADRES && ADRES != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&cxn_cihaz))) && ADRES != 0x7f000001)) return -99;
    ip_addr_t İnternet_adresi; ip_addr_set_ip4_u32(&İnternet_adresi, lwip_htonl(ADRES));
    err_t 보조항목 = dize_veri->TÜR_alan == 1 ? tcp_bind(dize_veri->cxn_denetim, &İnternet_adresi, bağlantı_noktası_numarası) : udp_bind(dize_veri->veri_birimi_denetim, &İnternet_adresi, bağlantı_noktası_numarası); return 보조항목 ? hata_numarası(보조항목) : 0;
}
void 통신주소재사용(int dosya_tanıtıcısı) { yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (dize_veri && dize_veri->cxn_denetim) ip_set_option(dize_veri->cxn_denetim, SOF_REUSEADDR); }
int NET_dinlemek(int dosya_tanıtıcısı) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri || dize_veri->TÜR_alan != 1) return -9;
    if (dize_veri->almak_taşımak) return 0;
    err_t 보조항목; struct tcp_pcb *통신제어블록 = tcp_listen_with_backlog_and_err(dize_veri->cxn_denetim, 4, &보조항목);
    if (!통신제어블록) return hata_numarası(보조항목); dize_veri->cxn_denetim = 통신제어블록; dize_veri->almak_taşımak = 1; tcp_arg(통신제어블록, dize_veri); tcp_accept(통신제어블록, 연결받음); return 0;
}
int NET_bağla(int dosya_tanıtıcısı, uint32_t ADRES, unsigned bağlantı_noktası_numarası) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri || dize_veri->TÜR_alan != 1) return -9;
    if (dize_veri->hata) return dize_veri->hata;
    if (dize_veri->연결됨) return 0;
    if (dize_veri->상대창구번호) return -115;
    if (!bağlantı_noktası_numarası || bağlantı_noktası_numarası > 65535 || !ADRES) return -22;
    ip_addr_t İnternet_adresi; ip_addr_set_ip4_u32(&İnternet_adresi, lwip_htonl(ADRES));
    dize_veri->eş_ADRES = ADRES; dize_veri->상대창구번호 = bağlantı_noktası_numarası;
    err_t 보조항목 = tcp_connect(dize_veri->cxn_denetim, &İnternet_adresi, bağlantı_noktası_numarası, 연결됨); return 보조항목 ? hata_numarası(보조항목) : -115;
}
int NET_kabul_etmek(int dosya_tanıtıcısı) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri || !dize_veri->almak_taşımak) return -22;
    for (int 순번 = 0; 순번 < 32; 순번++) if (통신끝점들[순번].TÜR_alan == 1 && 통신끝점들[순번].bilgi_teknolojisi_Beklemede == dosya_tanıtıcısı) { 통신끝점들[순번].bilgi_teknolojisi_Beklemede = -1; return 순번; }
    return -11;
}
int 통신읽기(int dosya_tanıtıcısı, void *veri, unsigned öğe_BAĞ_DEĞ_SAY) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri || dize_veri->TÜR_alan != 1) return -9;
    if (!öğe_BAĞ_DEĞ_SAY) return 0; if (!dize_veri->girdi_BAĞ_DEĞ_SAY) return dize_veri->hata ? dize_veri->hata : dize_veri->Dosya_Bitiş ? 0 : -11;
    if (öğe_BAĞ_DEĞ_SAY > dize_veri->girdi_BAĞ_DEĞ_SAY) öğe_BAĞ_DEĞ_SAY = dize_veri->girdi_BAĞ_DEĞ_SAY;
    for (unsigned 순번 = 0; 순번 < öğe_BAĞ_DEĞ_SAY; 순번++) { ((unsigned char *)veri)[순번] = dize_veri->veri[dize_veri->ön_kamera_girdi]; dize_veri->ön_kamera_girdi = (dize_veri->ön_kamera_girdi + 1) % sizeof(dize_veri->veri); }
    dize_veri->girdi_BAĞ_DEĞ_SAY -= öğe_BAĞ_DEĞ_SAY; if (dize_veri->cxn_denetim) tcp_recved(dize_veri->cxn_denetim, öğe_BAĞ_DEĞ_SAY); return öğe_BAĞ_DEĞ_SAY;
}
int NET_yazma(int dosya_tanıtıcısı, const void *veri, unsigned öğe_BAĞ_DEĞ_SAY) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri || dize_veri->TÜR_alan != 1) return -9;
    if (dize_veri->hata) return dize_veri->hata; if (!dize_veri->cxn_denetim || !dize_veri->연결됨) return -107;
    if (!öğe_BAĞ_DEĞ_SAY) return 0; if (öğe_BAĞ_DEĞ_SAY > tcp_sndbuf(dize_veri->cxn_denetim)) öğe_BAĞ_DEĞ_SAY = tcp_sndbuf(dize_veri->cxn_denetim);
    if (!öğe_BAĞ_DEĞ_SAY) return -11; if (öğe_BAĞ_DEĞ_SAY > 1024) öğe_BAĞ_DEĞ_SAY = 1024;
    err_t 보조항목 = tcp_write(dize_veri->cxn_denetim, veri, öğe_BAĞ_DEĞ_SAY, TCP_WRITE_FLAG_COPY); if (보조항목) return hata_numarası(보조항목);
    tcp_output(dize_veri->cxn_denetim); return öğe_BAĞ_DEĞ_SAY;
}
int göndermek_veri_birimi(int dosya_tanıtıcısı, const void *veri, unsigned öğe_BAĞ_DEĞ_SAY, uint32_t ADRES, unsigned bağlantı_noktası_numarası) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri || dize_veri->TÜR_alan != 2) return -9;
    if (öğe_BAĞ_DEĞ_SAY > 512) return -90; if (!bağlantı_noktası_numarası || bağlantı_noktası_numarası > 65535) return -22;
    struct pbuf *veri_konum = pbuf_alloc(PBUF_TRANSPORT, öğe_BAĞ_DEĞ_SAY, PBUF_RAM); if (!veri_konum) return -11;
    pbuf_take(veri_konum, veri, öğe_BAĞ_DEĞ_SAY); ip_addr_t İnternet_adresi; ip_addr_set_ip4_u32(&İnternet_adresi, lwip_htonl(ADRES));
    err_t 보조항목 = udp_sendto(dize_veri->veri_birimi_denetim, veri_konum, &İnternet_adresi, bağlantı_noktası_numarası); pbuf_free(veri_konum); return 보조항목 ? hata_numarası(보조항목) : (int)öğe_BAĞ_DEĞ_SAY;
}
int almak_veri_birimi(int dosya_tanıtıcısı, void *veri, unsigned öğe_BAĞ_DEĞ_SAY) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri || dize_veri->TÜR_alan != 2) return -9;
    if (!dize_veri->girdi_BAĞ_DEĞ_SAY) return -11; unsigned geçerli_konum = dize_veri->ön_kamera_girdi;
    if (öğe_BAĞ_DEĞ_SAY > dize_veri->길이목록[geçerli_konum]) öğe_BAĞ_DEĞ_SAY = dize_veri->길이목록[geçerli_konum]; memcpy(veri, dize_veri->veri + geçerli_konum * 512, öğe_BAĞ_DEĞ_SAY);
    dize_veri->상대창구번호 = dize_veri->접속번호들[geçerli_konum]; dize_veri->eş_ADRES = dize_veri->주소목록[geçerli_konum]; dize_veri->ön_kamera_girdi = (geçerli_konum + 1) % 4; dize_veri->girdi_BAĞ_DEĞ_SAY--; return öğe_BAĞ_DEĞ_SAY;
}
unsigned ağ_bağlantı_noktası_numarası(int dosya_tanıtıcısı) { yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); return !dize_veri ? 0 : dize_veri->cxn_denetim ? dize_veri->cxn_denetim->local_port : dize_veri->veri_birimi_denetim ? dize_veri->veri_birimi_denetim->local_port : 0; }
unsigned eş_bağlantı_noktası_numarası(int dosya_tanıtıcısı) { yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); return dize_veri ? dize_veri->상대창구번호 : 0; }
uint32_t NET_eş_ADRES(int dosya_tanıtıcısı) { yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); return dize_veri ? dize_veri->eş_ADRES : 0; }
void Kapat_ağ(int dosya_tanıtıcısı) {
    yuva_uç_nokta_3db661a2 *dize_veri = get_değer(dosya_tanıtıcısı); if (!dize_veri) return;
    if (dize_veri->almak_taşımak) for (int 순번 = 0; 순번 < 32; ++순번) if (통신끝점들[순번].TÜR_alan && 통신끝점들[순번].bilgi_teknolojisi_Beklemede == dosya_tanıtıcısı) Kapat_ağ(순번);
    if (dize_veri->cxn_denetim) {
        tcp_arg(dize_veri->cxn_denetim, 0); if (dize_veri->almak_taşımak) tcp_accept(dize_veri->cxn_denetim, 0); else { tcp_recv(dize_veri->cxn_denetim, 0); tcp_err(dize_veri->cxn_denetim, 0); }
        if (tcp_close(dize_veri->cxn_denetim) != ERR_OK) tcp_abort(dize_veri->cxn_denetim);
    }
    if (dize_veri->veri_birimi_denetim) udp_remove(dize_veri->veri_birimi_denetim); dize_veri->TÜR_alan = 0;
}
void 통신망살피기(void) {
    if (!준비됨 || yoklama) return; yoklama = 1;
    if(kullanmak_kablolu_ağ)유선망살피기(&cxn_cihaz);
    for (unsigned bütçe = 0; !kullanmak_kablolu_ağ && bütçe < 4096 && (makine_yazmaç(보조장치 + 0x54) & 1); bütçe++) {
        unsigned kod_noktası = makine_yazmaç(보조장치 + 0x40) & 255;
        if (kod_noktası == 192) {
            if (almak_kullanım && !almak_hata && !수신탈출) {
                struct pbuf *veri_konum = pbuf_alloc(PBUF_RAW, almak_kullanım, PBUF_POOL);
                if (veri_konum) { GETİRİ_veri_birimi_BAĞ_DEĞ_SAY++; GETİRİ_bayt_BAĞ_DEĞ_SAY += almak_kullanım; pbuf_take(veri_konum, almak_veri_arabelleği, almak_kullanım); if (cxn_cihaz.input(veri_konum, &cxn_cihaz) != ERR_OK) { 버린전문수++; pbuf_free(veri_konum); } }
                else 버린전문수++;
            }
            else if (almak_kullanım) 버린전문수++;
            almak_kullanım = almak_hata = 수신탈출 = 0;
        } else if (kod_noktası == 219 && !수신탈출) 수신탈출 = 1;
        else {
            if (수신탈출) { if (kod_noktası != 220 && kod_noktası != 221) almak_hata = 1; kod_noktası = kod_noktası == 220 ? 192 : 219; 수신탈출 = 0; }
            if (almak_kullanım < sizeof(almak_veri_arabelleği)) almak_veri_arabelleği[almak_kullanım++] = kod_noktası; else almak_hata = 1;
        }
    }
    netif_poll(&cxn_cihaz); sys_check_timeouts(); 파일전송살피기(); 원격살피기();
    for (unsigned bütçe = 0; bütçe < 4096 && 송신개수 && (makine_yazmaç(보조장치 + 0x54) & 0x20); bütçe++) {
        makine_yazmaç(보조장치 + 0x40) = 송신자료[송신앞자리]; 송신앞자리 = (송신앞자리 + 1) % sizeof(송신자료); 송신개수--;
    }
    yoklama = 0;
}

/* Ayarlar·조회는 lwIP의 fiili_veri 인터페이스와 Bitiş_puan 표를 사용한다. */
uint32_t 망상태읽기(unsigned girdi_değer, unsigned Dizin) {
    if(girdi_değer==20)return kullanmak_kablolu_ağ;
    if(girdi_değer==21)return 준비됨&&netif_is_link_up(&cxn_cihaz);
    if(girdi_değer==22)return kullanmak_kablolu_ağ?kablolu_ağ_İstatistik(5):0;
    if (!준비됨) return 0;
    if(kullanmak_kablolu_ağ&&girdi_değer>=4&&girdi_değer<=8)return kablolu_ağ_İstatistik(girdi_değer-4);
    if (girdi_değer == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&cxn_cihaz)));
    if (girdi_değer == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&cxn_cihaz)));
    if (girdi_değer == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&cxn_cihaz)));
    if (girdi_değer == 3) return netif_is_up(&cxn_cihaz) != 0;
    if (girdi_değer == 4) return GETİRİ_veri_birimi_BAĞ_DEĞ_SAY;
    if (girdi_değer == 5) return 보낸전문수;
    if (girdi_değer == 6) return GETİRİ_bayt_BAĞ_DEĞ_SAY;
    if (girdi_değer == 7) return 보낸바이트수;
    if (girdi_değer == 8) return 버린전문수;
    if (girdi_değer == 9) return 송신개수;
    if (Dizin >= 32) return 0;
    yuva_uç_nokta_3db661a2 *Bitiş_puan = &통신끝점들[Dizin];
    if (girdi_değer == 10) return Bitiş_puan->TÜR_alan;
    if (!Bitiş_puan->TÜR_alan) return 0;
    if (girdi_değer == 11) return ağ_bağlantı_noktası_numarası(Dizin);
    if (girdi_değer == 12) return Bitiş_puan->eş_ADRES;
    if (girdi_değer == 13) return Bitiş_puan->상대창구번호;
    if (girdi_değer == 14) return Bitiş_puan->almak_taşımak ? 1 : Bitiş_puan->Dosya_Bitiş ? 3 : Bitiş_puan->hata ? 4 : Bitiş_puan->연결됨 ? 2 : 0;
    if (girdi_değer == 15) return Bitiş_puan->girdi_BAĞ_DEĞ_SAY;
    if (girdi_değer == 16) {
        const ip_addr_t *ADRES = Bitiş_puan->TÜR_alan == 1 && Bitiş_puan->cxn_denetim ? &Bitiş_puan->cxn_denetim->local_ip :
            Bitiş_puan->TÜR_alan == 2 && Bitiş_puan->veri_birimi_denetim ? &Bitiş_puan->veri_birimi_denetim->local_ip : 0;
        return ADRES ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADRES))) : 0;
    }
    return 0;
}

int yapılandırmak_ağ(unsigned Eylem, uint32_t ADRES, uint32_t maske_değer, uint32_t ağ_geçidi_değer) {
    if (!준비됨) return -100;
    if (Eylem == 1) { netif_set_up(&cxn_cihaz); return 0; }
    if (Eylem == 2) { netif_set_down(&cxn_cihaz); return 0; }
    if (Eylem != 0) return -22;
    /* 유니캐스트 IPv4, 연속 maske_değer, 같은 망의 선택적 varsayılan_değer ağ_geçidi_değer. */
    uint32_t 뒤집은가림 = ~maske_değer;
    if (!maske_değer || (뒤집은가림 & (뒤집은가림 + 1)) || !ADRES || (ADRES >> 24) == 127 ||
        (ADRES >> 24) == 0 || (ADRES >> 28) >= 14 ||
        (뒤집은가림 > 1 && (!(ADRES & 뒤집은가림) || (ADRES & 뒤집은가림) == 뒤집은가림)) ||
        (ağ_geçidi_değer && ((ağ_geçidi_değer & maske_değer) != (ADRES & maske_değer) || ağ_geçidi_değer == ADRES || (ağ_geçidi_değer >> 28) >= 14 ||
         (뒤집은가림 > 1 && (!(ağ_geçidi_değer & 뒤집은가림) || (ağ_geçidi_değer & 뒤집은가림) == 뒤집은가림))))) return -22;
    /* 기존 연결을 ADRES 변경으로 몰래 끊지 않는다. */
    for (unsigned Dizin = 0; Dizin < 32; Dizin++) if (통신끝점들[Dizin].TÜR_alan &&
        !(통신끝점들[Dizin].almak_taşımak && 통신끝점들[Dizin].cxn_denetim && ip_addr_isany(&통신끝점들[Dizin].cxn_denetim->local_ip))) return -16;
    if(kullanmak_kablolu_ağ)dhcp_stop(&cxn_cihaz);
    ip4_addr_t 새주소, 새가림, 새관문;
    ip4_addr_set_u32(&새주소, lwip_htonl(ADRES)); ip4_addr_set_u32(&새가림, lwip_htonl(maske_değer)); ip4_addr_set_u32(&새관문, lwip_htonl(ağ_geçidi_değer));
    netif_set_addr(&cxn_cihaz, &새주소, &새가림, &새관문);
    return 0;
}

static struct raw_pcb *cevap_uç_nokta;
static uint32_t test_ADRES, test_saat, yanıt_süresi;
static unsigned test_dizi, test_tanımlayıcı, cevap_dizi;
static int cevap_Durum;
static u8_t 응답받음(void *bağımsız_değişkenler, struct raw_pcb *Bitiş_puan, struct pbuf *veri, const ip_addr_t *ADRES) {
    (void)bağımsız_değişkenler; (void)Bitiş_puan;
    unsigned char 머리[20], yanıt[16];
    if (cevap_Durum != -11 || veri->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(ADRES))) != test_ADRES || pbuf_copy_partial(veri, 머리, 20, 0) != 20) return 0;
    unsigned Başlık_boyutlandırmak = (머리[0] & 15) * 4;
    if ((머리[0] >> 4) != 4 || Başlık_boyutlandırmak < 20 || veri->tot_len < Başlık_boyutlandırmak + 16 ||
        pbuf_copy_partial(veri, yanıt, 16, Başlık_boyutlandırmak) != 16 || yanıt[0] || yanıt[1] ||
        (((unsigned)yanıt[4] << 8) | yanıt[5]) != test_tanımlayıcı ||
        (((unsigned)yanıt[6] << 8) | yanıt[7]) != test_dizi ||
        yanıt[8] != 'J' || yanıt[9] != 'K' || yanıt[10] != 'O' || yanıt[11] != 'S' ||
        (((uint32_t)yanıt[12] << 24) | ((uint32_t)yanıt[13] << 16) | ((uint32_t)yanıt[14] << 8) | yanıt[15]) != test_saat) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(veri, Başlık_boyutlandırmak)) return 0;
    if (inet_chksum_pbuf(veri)) { pbuf_add_header(veri, Başlık_boyutlandırmak); return 0; }
    yanıt_süresi = (uint32_t)보드밀리초() - test_saat; cevap_dizi = 머리[8]; cevap_Durum = 0;
    pbuf_free(veri); return 1;
}
int Start_cevap_test(uint32_t ADRES, unsigned düzen_değer) {
    if (!준비됨 || !netif_is_up(&cxn_cihaz)) return -100;
    if (!ADRES || (ADRES >> 28) >= 14 || ADRES == 0xffffffffu) return -22;
    if (!cevap_uç_nokta) { cevap_uç_nokta = raw_new(IP_PROTO_ICMP); if (!cevap_uç_nokta) return -12; raw_recv(cevap_uç_nokta, 응답받음, 0); }
    test_ADRES = ADRES; test_dizi = düzen_değer & 65535; test_tanımlayıcı = (test_tanımlayıcı + 1) & 65535;
    test_saat = 보드밀리초(); cevap_Durum = -11; yanıt_süresi = cevap_dizi = 0;
    unsigned char veri[32] = {8,0,0,0};
    veri[4] = test_tanımlayıcı >> 8; veri[5] = test_tanımlayıcı; veri[6] = test_dizi >> 8; veri[7] = test_dizi;
    veri[8]='J'; veri[9]='K'; veri[10]='O'; veri[11]='S';
    veri[12]=test_saat >> 24; veri[13]=test_saat >> 16; veri[14]=test_saat >> 8; veri[15]=test_saat;
    for (unsigned konum_dizini = 16; konum_dizini < sizeof(veri); konum_dizini++) veri[konum_dizini] = konum_dizini;
    uint16_t onaylama_sağlama_toplamı = inet_chksum(veri, sizeof(veri)); memcpy(veri + 2, &onaylama_sağlama_toplamı, 2);
    struct pbuf *veri_birimi = pbuf_alloc(PBUF_IP, sizeof(veri), PBUF_RAM); if (!veri_birimi) return -12;
    pbuf_take(veri_birimi, veri, sizeof(veri)); ip_addr_t hedef_uç_nokta; ip_addr_set_ip4_u32(&hedef_uç_nokta, lwip_htonl(ADRES));
    err_t 처리값 = raw_sendto(cevap_uç_nokta, veri_birimi, &hedef_uç_nokta); pbuf_free(veri_birimi);
    if (처리값) cevap_Durum = hata_numarası(처리값);
    return 처리값 ? cevap_Durum : 0;
}
int 응답시험읽기(unsigned girdi_değer) {
    통신망살피기();
    return girdi_değer == 0 ? cevap_Durum : girdi_değer == 1 ? (int)yanıt_süresi : girdi_değer == 2 ? (int)cevap_dizi : -22;
}
