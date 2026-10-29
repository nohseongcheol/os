#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
/* lwIP runs in the bare-metal kernel. The second UART transports RFC 1055 SLIP. */
#include "NgănXếpMạng.h"
#include "string.h"
#include "lwip/init.h"
#include "lwip/netif.h"
#include "lwip/ip4.h"
#include "lwip/tcp.h"
#include "lwip/udp.h"
#include "lwip/timeouts.h"
#include "lwip/raw.h"
#include "lwip/inet_chksum.h"
#include "../giáTrịTừXa/giáTrịTừXa.h"
#include "mạngHữuTuyến.h"
#include "netif/ethernet.h"
#include "lwip/dhcp.h"
#define thanhGhiMáy(giáTrịĐầuTiên) (*(volatile uint32_t *)(uintptr_t)(giáTrịĐầuTiên))
#define thiếtBịPhụTrợ 0xfe215000ul
extern uintptr_t miliGiâyGọnBoMạch(void);
static struct netif thiếtBịKếtNối;
static int làĐãChuẩnBị, thămDò;
static int mạngHữuTuyếnDùng;
static unsigned nhậnCáchDùng, nhậnThoát, nhậnLỗi;
static unsigned char nhậnBộĐệmDữLiệu[1600];
static unsigned char dữLiệuTruyền[32768];
static unsigned đầuPhátGọn, sốLượngPhátGọn;
static uint32_t sốLượngĐiệnDữLiệuĐãNhận, sốLượngĐiệnDữLiệuĐãGửi, sốLượngByteĐãNhận, sốLượngByteĐãGửi, sốLượngĐiệnDữLiệuĐãBỏ;
typedef struct {
    int loạiMụcKiểu, nhậnCổng, làĐangChờ, đãKếtNối, kếtThúcTệp, lỗi;
    struct tcp_pcb *điềuKhiểnKếtNối;
    struct udp_pcb *điềuKhiểnĐiệnDữLiệu;
    unsigned mụcPhíaTrước, sốLượngMục;
    unsigned char DữLiệu[4096];
    unsigned cácĐộDài[4], cácCổng[4], sốĐiểmCuốiĐốiTác;
    uint32_t cácĐịaChỉ[4], địaChỉĐốiTác;
} điểmCuốiỔCắmMạng;
static điểmCuốiỔCắmMạng cácĐiểmCuốiỔCắmMạng[32];
u32_t sys_now(void) { return (u32_t)miliGiâyGọnBoMạch(); }
static int sốLỗi(err_t mụcPhụTrợ) {
    return mụcPhụTrợ == ERR_MEM || mụcPhụTrợ == ERR_BUF || mụcPhụTrợ == ERR_WOULDBLOCK ? -11 : mụcPhụTrợ == ERR_USE ? -98 :
        mụcPhụTrợ == ERR_RTE ? -101 : mụcPhụTrợ == ERR_RST ? -104 : mụcPhụTrợ == ERR_CONN ? -107 : mụcPhụTrợ == ERR_TIMEOUT ? -110 : -5;
}
static điểmCuốiỔCắmMạng *lấyGiáTrị(int thẻXửLýTệp) { return thẻXửLýTệp >= 0 && thẻXửLýTệp < 32 && cácĐiểmCuốiỔCắmMạng[thẻXửLýTệp].loạiMụcKiểu ? &cácĐiểmCuốiỔCắmMạng[thẻXửLýTệp] : 0; }
static int dànhTrước(int loạiMụcKiểu) {
    for (int chỉSốThứBậc = 0; chỉSốThứBậc < 32; ++chỉSốThứBậc) if (!cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc].loạiMụcKiểu) {
        memset(&cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc], 0, sizeof(điểmCuốiỔCắmMạng)); cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc].loạiMụcKiểu = loạiMụcKiểu; cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc].làĐangChờ = -1; return chỉSốThứBậc;
    }
    return -24;
}
static void phátGiáTrị(unsigned mãKýTự) { dữLiệuTruyền[(đầuPhátGọn + sốLượngPhátGọn++) % sizeof(dữLiệuTruyền)] = mãKýTự; }
static err_t đầuRa(struct netif *sốLượngPhầnMục, struct pbuf *vịTríDữLiệu, const ip4_addr_t *địaChỉ) {
    (void)sốLượngPhầnMục; (void)địaChỉ;
    if (vịTríDữLiệu->tot_len > 1500 || sốLượngPhátGọn + 2 * vịTríDữLiệu->tot_len + 2 > sizeof(dữLiệuTruyền)) return ERR_MEM;
    phátGiáTrị(192);
    for (struct pbuf *độLệchKếTiếp = vịTríDữLiệu; độLệchKếTiếp; độLệchKếTiếp = độLệchKếTiếp->next) for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < độLệchKếTiếp->len; chỉSốThứBậc++) {
        unsigned mãKýTự = ((unsigned char *)độLệchKếTiếp->payload)[chỉSốThứBậc];
        if (mãKýTự == 192 || mãKýTự == 219) { phátGiáTrị(219); phátGiáTrị(mãKýTự == 192 ? 220 : 221); } else phátGiáTrị(mãKýTự);
    }
    phátGiáTrị(192); sốLượngĐiệnDữLiệuĐãGửi++; sốLượngByteĐãGửi += vịTríDữLiệu->tot_len; return ERR_OK;
}
static err_t chuẩnBịMôiTrườngChạy(struct netif *sốLượngPhầnMục) { sốLượngPhầnMục->name[0] = 's'; sốLượngPhầnMục->name[1] = 'l'; sốLượngPhầnMục->mtu = 1500; sốLượngPhầnMục->output = đầuRa; return ERR_OK; }
void chuẩnBịMạng(void) {
    if (làĐãChuẩnBị) return;
    /* UART1 AUX. On real hardware this needs its own pin routing/SLIP link. */
    thanhGhiMáy(thiếtBịPhụTrợ + 4) |= 1; thanhGhiMáy(thiếtBịPhụTrợ + 0x60) = 0; thanhGhiMáy(thiếtBịPhụTrợ + 0x44) = 0;
    thanhGhiMáy(thiếtBịPhụTrợ + 0x48) = 0xc6; thanhGhiMáy(thiếtBịPhụTrợ + 0x4c) = 3; thanhGhiMáy(thiếtBịPhụTrợ + 0x68) = 270; thanhGhiMáy(thiếtBịPhụTrợ + 0x60) = 3;
    lwip_init();
    ip4_addr_t ĐịaChỉLiênMạng, mặtNạBit, địaChỉCổngNối;
    mạngHữuTuyếnDùng=cóThiếtBịHữuTuyến();
    ip4_addr_set_u32(&ĐịaChỉLiênMạng, lwip_htonl(IP_CONFIG_IP));
    ip4_addr_set_u32(&mặtNạBit, lwip_htonl(IP_CONFIG_NETMASK));
    ip4_addr_set_u32(&địaChỉCổngNối, lwip_htonl(IP_CONFIG_GATEWAY));
    if(!netif_add(&thiếtBịKếtNối, &ĐịaChỉLiênMạng, &mặtNạBit, &địaChỉCổngNối, 0, mạngHữuTuyếnDùng?chuẩnBịMạngHữuTuyến:chuẩnBịMôiTrườngChạy, mạngHữuTuyếnDùng?ethernet_input:ip4_input))return;
    netif_set_default(&thiếtBịKếtNối); netif_set_up(&thiếtBịKếtNối);if(!mạngHữuTuyếnDùng)netif_set_link_up(&thiếtBịKếtNối); làĐãChuẩnBị = 1;
    chuẩnBịTừXa();
}
static err_t cóĐãNhận(void *cácĐốiSốBổSung, struct tcp_pcb *khốiĐiềuKhiểnSựTruyền, struct pbuf *vịTríDữLiệu, err_t lỗi) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = cácĐốiSốBổSung; (void)khốiĐiềuKhiểnSựTruyền; (void)lỗi;
    if (!vịTríDữLiệu) { dữLiệuChuỗi->kếtThúcTệp = 1; return ERR_OK; }
    if (vịTríDữLiệu->tot_len > sizeof(dữLiệuChuỗi->DữLiệu) - dữLiệuChuỗi->sốLượngMục) return ERR_MEM;
    unsigned vịTríHiệnTại = (dữLiệuChuỗi->mụcPhíaTrước + dữLiệuChuỗi->sốLượngMục) % sizeof(dữLiệuChuỗi->DữLiệu);
    for (struct pbuf *độLệchKếTiếp = vịTríDữLiệu; độLệchKếTiếp; độLệchKếTiếp = độLệchKếTiếp->next) for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < độLệchKếTiếp->len; chỉSốThứBậc++) {
        dữLiệuChuỗi->DữLiệu[vịTríHiệnTại] = ((unsigned char *)độLệchKếTiếp->payload)[chỉSốThứBậc]; vịTríHiệnTại = (vịTríHiệnTại + 1) % sizeof(dữLiệuChuỗi->DữLiệu);
    }
    dữLiệuChuỗi->sốLượngMục += vịTríDữLiệu->tot_len; pbuf_free(vịTríDữLiệu); return ERR_OK;
}
static void cóThấtBại(void *cácĐốiSốBổSung, err_t lỗi) { điểmCuốiỔCắmMạng *dữLiệuChuỗi = cácĐốiSốBổSung; dữLiệuChuỗi->điềuKhiểnKếtNối = 0; dữLiệuChuỗi->lỗi = sốLỗi(lỗi); }
static void cácHàmGọiLại(điểmCuốiỔCắmMạng *dữLiệuChuỗi) { tcp_arg(dữLiệuChuỗi->điềuKhiểnKếtNối, dữLiệuChuỗi); tcp_recv(dữLiệuChuỗi->điềuKhiểnKếtNối, cóĐãNhận); tcp_err(dữLiệuChuỗi->điềuKhiểnKếtNối, cóThấtBại); }
static err_t đãKếtNối(void *cácĐốiSốBổSung, struct tcp_pcb *khốiĐiềuKhiểnSựTruyền, err_t lỗi) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = cácĐốiSốBổSung; (void)khốiĐiềuKhiểnSựTruyền; if (lỗi) dữLiệuChuỗi->lỗi = sốLỗi(lỗi); else dữLiệuChuỗi->đãKếtNối = 1; return ERR_OK;
}
static err_t đãChấpNhận(void *cácĐốiSốBổSung, struct tcp_pcb *khốiĐiềuKhiểnSựTruyền, err_t lỗi) {
    điểmCuốiỔCắmMạng *cha = cácĐốiSốBổSung; if (lỗi) return lỗi;
    int thẻXửLýTệp = dànhTrước(1); if (thẻXửLýTệp < 0) return ERR_MEM;
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = &cácĐiểmCuốiỔCắmMạng[thẻXửLýTệp]; dữLiệuChuỗi->điềuKhiểnKếtNối = khốiĐiềuKhiểnSựTruyền; dữLiệuChuỗi->đãKếtNối = 1; dữLiệuChuỗi->làĐangChờ = (int)(cha - cácĐiểmCuốiỔCắmMạng);
    dữLiệuChuỗi->địaChỉĐốiTác = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(&khốiĐiềuKhiểnSựTruyền->remote_ip))); dữLiệuChuỗi->sốĐiểmCuốiĐốiTác = khốiĐiềuKhiểnSựTruyền->remote_port;
    cácHàmGọiLại(dữLiệuChuỗi); return ERR_OK;
}
static void điệnDữLiệu(void *cácĐốiSốBổSung, struct udp_pcb *khốiĐiềuKhiểnSựTruyền, struct pbuf *vịTríDữLiệu, const ip_addr_t *địaChỉ, u16_t sốCổng) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = cácĐốiSốBổSung; (void)khốiĐiềuKhiểnSựTruyền;
    if (dữLiệuChuỗi->sốLượngMục < 4 && vịTríDữLiệu->tot_len <= 512) {
        unsigned chỉSốVịTrí = (dữLiệuChuỗi->mụcPhíaTrước + dữLiệuChuỗi->sốLượngMục) % 4;
        pbuf_copy_partial(vịTríDữLiệu, dữLiệuChuỗi->DữLiệu + chỉSốVịTrí * 512, vịTríDữLiệu->tot_len, 0);
        dữLiệuChuỗi->cácĐộDài[chỉSốVịTrí] = vịTríDữLiệu->tot_len; dữLiệuChuỗi->cácCổng[chỉSốVịTrí] = sốCổng;
        dữLiệuChuỗi->cácĐịaChỉ[chỉSốVịTrí] = lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(địaChỉ))); dữLiệuChuỗi->sốLượngMục++;
    }
    pbuf_free(vịTríDữLiệu);
}
int tạoĐiểmCuốiỔCắmMạng(int loạiMụcKiểu) {
    if (!làĐãChuẩnBị) return -100;
    if (loạiMụcKiểu != 1 && loạiMụcKiểu != 2) return -93;
    int thẻXửLýTệp = dànhTrước(loạiMụcKiểu); if (thẻXửLýTệp < 0) return thẻXửLýTệp;
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = &cácĐiểmCuốiỔCắmMạng[thẻXửLýTệp];
    if (loạiMụcKiểu == 1) { dữLiệuChuỗi->điềuKhiểnKếtNối = tcp_new(); if (dữLiệuChuỗi->điềuKhiểnKếtNối) cácHàmGọiLại(dữLiệuChuỗi); }
    else { dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu = udp_new(); if (dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu) udp_recv(dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu, điệnDữLiệu, dữLiệuChuỗi); }
    if (!dữLiệuChuỗi->điềuKhiểnKếtNối && !dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu) { dữLiệuChuỗi->loạiMụcKiểu = 0; return -12; } return thẻXửLýTệp;
}
int ràngBuộcMạngGọn(int thẻXửLýTệp, uint32_t địaChỉ, unsigned sốCổng) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi) return -9;
    if (sốCổng > 65535 || (địaChỉ && địaChỉ != lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&thiếtBịKếtNối))) && địaChỉ != 0x7f000001)) return -99;
    ip_addr_t ĐịaChỉLiênMạng; ip_addr_set_ip4_u32(&ĐịaChỉLiênMạng, lwip_htonl(địaChỉ));
    err_t mụcPhụTrợ = dữLiệuChuỗi->loạiMụcKiểu == 1 ? tcp_bind(dữLiệuChuỗi->điềuKhiểnKếtNối, &ĐịaChỉLiênMạng, sốCổng) : udp_bind(dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu, &ĐịaChỉLiênMạng, sốCổng); return mụcPhụTrợ ? sốLỗi(mụcPhụTrợ) : 0;
}
void địaChỉỔCắmMạngDùngLại(int thẻXửLýTệp) { điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (dữLiệuChuỗi && dữLiệuChuỗi->điềuKhiểnKếtNối) ip_set_option(dữLiệuChuỗi->điềuKhiểnKếtNối, SOF_REUSEADDR); }
int lắngNgheMạngGọn(int thẻXửLýTệp) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi || dữLiệuChuỗi->loạiMụcKiểu != 1) return -9;
    if (dữLiệuChuỗi->nhậnCổng) return 0;
    err_t mụcPhụTrợ; struct tcp_pcb *khốiĐiềuKhiểnSựTruyền = tcp_listen_with_backlog_and_err(dữLiệuChuỗi->điềuKhiểnKếtNối, 4, &mụcPhụTrợ);
    if (!khốiĐiềuKhiểnSựTruyền) return sốLỗi(mụcPhụTrợ); dữLiệuChuỗi->điềuKhiểnKếtNối = khốiĐiềuKhiểnSựTruyền; dữLiệuChuỗi->nhậnCổng = 1; tcp_arg(khốiĐiềuKhiểnSựTruyền, dữLiệuChuỗi); tcp_accept(khốiĐiềuKhiểnSựTruyền, đãChấpNhận); return 0;
}
int kếtNốiMạngGọn(int thẻXửLýTệp, uint32_t địaChỉ, unsigned sốCổng) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi || dữLiệuChuỗi->loạiMụcKiểu != 1) return -9;
    if (dữLiệuChuỗi->lỗi) return dữLiệuChuỗi->lỗi;
    if (dữLiệuChuỗi->đãKếtNối) return 0;
    if (dữLiệuChuỗi->sốĐiểmCuốiĐốiTác) return -115;
    if (!sốCổng || sốCổng > 65535 || !địaChỉ) return -22;
    ip_addr_t ĐịaChỉLiênMạng; ip_addr_set_ip4_u32(&ĐịaChỉLiênMạng, lwip_htonl(địaChỉ));
    dữLiệuChuỗi->địaChỉĐốiTác = địaChỉ; dữLiệuChuỗi->sốĐiểmCuốiĐốiTác = sốCổng;
    err_t mụcPhụTrợ = tcp_connect(dữLiệuChuỗi->điềuKhiểnKếtNối, &ĐịaChỉLiênMạng, sốCổng, đãKếtNối); return mụcPhụTrợ ? sốLỗi(mụcPhụTrợ) : -115;
}
int chấpNhậnMạngGọn(int thẻXửLýTệp) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi || !dữLiệuChuỗi->nhậnCổng) return -22;
    for (int chỉSốThứBậc = 0; chỉSốThứBậc < 32; chỉSốThứBậc++) if (cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc].loạiMụcKiểu == 1 && cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc].làĐangChờ == thẻXửLýTệp) { cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc].làĐangChờ = -1; return chỉSốThứBậc; }
    return -11;
}
int đọcMạngGọn(int thẻXửLýTệp, void *DữLiệu, unsigned sốLượngPhầnMục) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi || dữLiệuChuỗi->loạiMụcKiểu != 1) return -9;
    if (!sốLượngPhầnMục) return 0; if (!dữLiệuChuỗi->sốLượngMục) return dữLiệuChuỗi->lỗi ? dữLiệuChuỗi->lỗi : dữLiệuChuỗi->kếtThúcTệp ? 0 : -11;
    if (sốLượngPhầnMục > dữLiệuChuỗi->sốLượngMục) sốLượngPhầnMục = dữLiệuChuỗi->sốLượngMục;
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngPhầnMục; chỉSốThứBậc++) { ((unsigned char *)DữLiệu)[chỉSốThứBậc] = dữLiệuChuỗi->DữLiệu[dữLiệuChuỗi->mụcPhíaTrước]; dữLiệuChuỗi->mụcPhíaTrước = (dữLiệuChuỗi->mụcPhíaTrước + 1) % sizeof(dữLiệuChuỗi->DữLiệu); }
    dữLiệuChuỗi->sốLượngMục -= sốLượngPhầnMục; if (dữLiệuChuỗi->điềuKhiểnKếtNối) tcp_recved(dữLiệuChuỗi->điềuKhiểnKếtNối, sốLượngPhầnMục); return sốLượngPhầnMục;
}
int ghiMạngGọn(int thẻXửLýTệp, const void *DữLiệu, unsigned sốLượngPhầnMục) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi || dữLiệuChuỗi->loạiMụcKiểu != 1) return -9;
    if (dữLiệuChuỗi->lỗi) return dữLiệuChuỗi->lỗi; if (!dữLiệuChuỗi->điềuKhiểnKếtNối || !dữLiệuChuỗi->đãKếtNối) return -107;
    if (!sốLượngPhầnMục) return 0; if (sốLượngPhầnMục > tcp_sndbuf(dữLiệuChuỗi->điềuKhiểnKếtNối)) sốLượngPhầnMục = tcp_sndbuf(dữLiệuChuỗi->điềuKhiểnKếtNối);
    if (!sốLượngPhầnMục) return -11; if (sốLượngPhầnMục > 1024) sốLượngPhầnMục = 1024;
    err_t mụcPhụTrợ = tcp_write(dữLiệuChuỗi->điềuKhiểnKếtNối, DữLiệu, sốLượngPhầnMục, TCP_WRITE_FLAG_COPY); if (mụcPhụTrợ) return sốLỗi(mụcPhụTrợ);
    tcp_output(dữLiệuChuỗi->điềuKhiểnKếtNối); return sốLượngPhầnMục;
}
int gửiĐiệnDữLiệu(int thẻXửLýTệp, const void *DữLiệu, unsigned sốLượngPhầnMục, uint32_t địaChỉ, unsigned sốCổng) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi || dữLiệuChuỗi->loạiMụcKiểu != 2) return -9;
    if (sốLượngPhầnMục > 512) return -90; if (!sốCổng || sốCổng > 65535) return -22;
    struct pbuf *vịTríDữLiệu = pbuf_alloc(PBUF_TRANSPORT, sốLượngPhầnMục, PBUF_RAM); if (!vịTríDữLiệu) return -11;
    pbuf_take(vịTríDữLiệu, DữLiệu, sốLượngPhầnMục); ip_addr_t ĐịaChỉLiênMạng; ip_addr_set_ip4_u32(&ĐịaChỉLiênMạng, lwip_htonl(địaChỉ));
    err_t mụcPhụTrợ = udp_sendto(dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu, vịTríDữLiệu, &ĐịaChỉLiênMạng, sốCổng); pbuf_free(vịTríDữLiệu); return mụcPhụTrợ ? sốLỗi(mụcPhụTrợ) : (int)sốLượngPhầnMục;
}
int nhậnĐiệnDữLiệu(int thẻXửLýTệp, void *DữLiệu, unsigned sốLượngPhầnMục) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi || dữLiệuChuỗi->loạiMụcKiểu != 2) return -9;
    if (!dữLiệuChuỗi->sốLượngMục) return -11; unsigned vịTríHiệnTại = dữLiệuChuỗi->mụcPhíaTrước;
    if (sốLượngPhầnMục > dữLiệuChuỗi->cácĐộDài[vịTríHiệnTại]) sốLượngPhầnMục = dữLiệuChuỗi->cácĐộDài[vịTríHiệnTại]; memcpy(DữLiệu, dữLiệuChuỗi->DữLiệu + vịTríHiệnTại * 512, sốLượngPhầnMục);
    dữLiệuChuỗi->sốĐiểmCuốiĐốiTác = dữLiệuChuỗi->cácCổng[vịTríHiệnTại]; dữLiệuChuỗi->địaChỉĐốiTác = dữLiệuChuỗi->cácĐịaChỉ[vịTríHiệnTại]; dữLiệuChuỗi->mụcPhíaTrước = (vịTríHiệnTại + 1) % 4; dữLiệuChuỗi->sốLượngMục--; return sốLượngPhầnMục;
}
unsigned sốCổngMạng(int thẻXửLýTệp) { điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); return !dữLiệuChuỗi ? 0 : dữLiệuChuỗi->điềuKhiểnKếtNối ? dữLiệuChuỗi->điềuKhiểnKếtNối->local_port : dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu ? dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu->local_port : 0; }
unsigned sốCổngĐốiTác(int thẻXửLýTệp) { điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); return dữLiệuChuỗi ? dữLiệuChuỗi->sốĐiểmCuốiĐốiTác : 0; }
uint32_t địaChỉĐốiTácMạngGọn(int thẻXửLýTệp) { điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); return dữLiệuChuỗi ? dữLiệuChuỗi->địaChỉĐốiTác : 0; }
void đóngMạng(int thẻXửLýTệp) {
    điểmCuốiỔCắmMạng *dữLiệuChuỗi = lấyGiáTrị(thẻXửLýTệp); if (!dữLiệuChuỗi) return;
    if (dữLiệuChuỗi->nhậnCổng) for (int chỉSốThứBậc = 0; chỉSốThứBậc < 32; ++chỉSốThứBậc) if (cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc].loạiMụcKiểu && cácĐiểmCuốiỔCắmMạng[chỉSốThứBậc].làĐangChờ == thẻXửLýTệp) đóngMạng(chỉSốThứBậc);
    if (dữLiệuChuỗi->điềuKhiểnKếtNối) {
        tcp_arg(dữLiệuChuỗi->điềuKhiểnKếtNối, 0); if (dữLiệuChuỗi->nhậnCổng) tcp_accept(dữLiệuChuỗi->điềuKhiểnKếtNối, 0); else { tcp_recv(dữLiệuChuỗi->điềuKhiểnKếtNối, 0); tcp_err(dữLiệuChuỗi->điềuKhiểnKếtNối, 0); }
        if (tcp_close(dữLiệuChuỗi->điềuKhiểnKếtNối) != ERR_OK) tcp_abort(dữLiệuChuỗi->điềuKhiểnKếtNối);
    }
    if (dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu) udp_remove(dữLiệuChuỗi->điềuKhiểnĐiệnDữLiệu); dữLiệuChuỗi->loạiMụcKiểu = 0;
}
void xemXétMạng(void) {
    if (!làĐãChuẩnBị || thămDò) return; thămDò = 1;
    if(mạngHữuTuyếnDùng)xemXétMạngHữuTuyến(&thiếtBịKếtNối);
    for (unsigned hạnMức = 0; !mạngHữuTuyếnDùng && hạnMức < 4096 && (thanhGhiMáy(thiếtBịPhụTrợ + 0x54) & 1); hạnMức++) {
        unsigned mãKýTự = thanhGhiMáy(thiếtBịPhụTrợ + 0x40) & 255;
        if (mãKýTự == 192) {
            if (nhậnCáchDùng && !nhậnLỗi && !nhậnThoát) {
                struct pbuf *vịTríDữLiệu = pbuf_alloc(PBUF_RAW, nhậnCáchDùng, PBUF_POOL);
                if (vịTríDữLiệu) { sốLượngĐiệnDữLiệuĐãNhận++; sốLượngByteĐãNhận += nhậnCáchDùng; pbuf_take(vịTríDữLiệu, nhậnBộĐệmDữLiệu, nhậnCáchDùng); if (thiếtBịKếtNối.input(vịTríDữLiệu, &thiếtBịKếtNối) != ERR_OK) { sốLượngĐiệnDữLiệuĐãBỏ++; pbuf_free(vịTríDữLiệu); } }
                else sốLượngĐiệnDữLiệuĐãBỏ++;
            }
            else if (nhậnCáchDùng) sốLượngĐiệnDữLiệuĐãBỏ++;
            nhậnCáchDùng = nhậnLỗi = nhậnThoát = 0;
        } else if (mãKýTự == 219 && !nhậnThoát) nhậnThoát = 1;
        else {
            if (nhậnThoát) { if (mãKýTự != 220 && mãKýTự != 221) nhậnLỗi = 1; mãKýTự = mãKýTự == 220 ? 192 : 219; nhậnThoát = 0; }
            if (nhậnCáchDùng < sizeof(nhậnBộĐệmDữLiệu)) nhậnBộĐệmDữLiệu[nhậnCáchDùng++] = mãKýTự; else nhậnLỗi = 1;
        }
    }
    netif_poll(&thiếtBịKếtNối); sys_check_timeouts(); xemXétChuyểnGiaoTệp(); xemXétTừXa();
    for (unsigned hạnMức = 0; hạnMức < 4096 && sốLượngPhátGọn && (thanhGhiMáy(thiếtBịPhụTrợ + 0x54) & 0x20); hạnMức++) {
        thanhGhiMáy(thiếtBịPhụTrợ + 0x40) = dữLiệuTruyền[đầuPhátGọn]; đầuPhátGọn = (đầuPhátGọn + 1) % sizeof(dữLiệuTruyền); sốLượngPhátGọn--;
    }
    thămDò = 0;
}

/* cácThiếtLập·조회는 lwIP의 dữLiệuThựcTế 인터페이스와 điểmKếtThúc 표를 사용한다. */
uint32_t đọcTìnhTrạngMạng(unsigned giáTrịMục, unsigned sốHiệu) {
    if(giáTrịMục==20)return mạngHữuTuyếnDùng;
    if(giáTrịMục==21)return làĐãChuẩnBị&&netif_is_link_up(&thiếtBịKếtNối);
    if(giáTrịMục==22)return mạngHữuTuyếnDùng?thốngKêMạngHữuTuyến(5):0;
    if (!làĐãChuẩnBị) return 0;
    if(mạngHữuTuyếnDùng&&giáTrịMục>=4&&giáTrịMục<=8)return thốngKêMạngHữuTuyến(giáTrịMục-4);
    if (giáTrịMục == 0) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_addr(&thiếtBịKếtNối)));
    if (giáTrịMục == 1) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_netmask(&thiếtBịKếtNối)));
    if (giáTrịMục == 2) return lwip_ntohl(ip4_addr_get_u32(netif_ip4_gw(&thiếtBịKếtNối)));
    if (giáTrịMục == 3) return netif_is_up(&thiếtBịKếtNối) != 0;
    if (giáTrịMục == 4) return sốLượngĐiệnDữLiệuĐãNhận;
    if (giáTrịMục == 5) return sốLượngĐiệnDữLiệuĐãGửi;
    if (giáTrịMục == 6) return sốLượngByteĐãNhận;
    if (giáTrịMục == 7) return sốLượngByteĐãGửi;
    if (giáTrịMục == 8) return sốLượngĐiệnDữLiệuĐãBỏ;
    if (giáTrịMục == 9) return sốLượngPhátGọn;
    if (sốHiệu >= 32) return 0;
    điểmCuốiỔCắmMạng *điểmKếtThúc = &cácĐiểmCuốiỔCắmMạng[sốHiệu];
    if (giáTrịMục == 10) return điểmKếtThúc->loạiMụcKiểu;
    if (!điểmKếtThúc->loạiMụcKiểu) return 0;
    if (giáTrịMục == 11) return sốCổngMạng(sốHiệu);
    if (giáTrịMục == 12) return điểmKếtThúc->địaChỉĐốiTác;
    if (giáTrịMục == 13) return điểmKếtThúc->sốĐiểmCuốiĐốiTác;
    if (giáTrịMục == 14) return điểmKếtThúc->nhậnCổng ? 1 : điểmKếtThúc->kếtThúcTệp ? 3 : điểmKếtThúc->lỗi ? 4 : điểmKếtThúc->đãKếtNối ? 2 : 0;
    if (giáTrịMục == 15) return điểmKếtThúc->sốLượngMục;
    if (giáTrịMục == 16) {
        const ip_addr_t *địaChỉ = điểmKếtThúc->loạiMụcKiểu == 1 && điểmKếtThúc->điềuKhiểnKếtNối ? &điểmKếtThúc->điềuKhiểnKếtNối->local_ip :
            điểmKếtThúc->loạiMụcKiểu == 2 && điểmKếtThúc->điềuKhiểnĐiệnDữLiệu ? &điểmKếtThúc->điềuKhiểnĐiệnDữLiệu->local_ip : 0;
        return địaChỉ ? lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(địaChỉ))) : 0;
    }
    return 0;
}

int đặtCấuHìnhMạng(unsigned hànhĐộng, uint32_t địaChỉ, uint32_t giáTrịMặtNạ, uint32_t giáTrịCổngNối) {
    if (!làĐãChuẩnBị) return -100;
    if (hànhĐộng == 1) { netif_set_up(&thiếtBịKếtNối); return 0; }
    if (hànhĐộng == 2) { netif_set_down(&thiếtBịKếtNối); return 0; }
    if (hànhĐộng != 0) return -22;
    /* 유니캐스트 IPv4, cácTrườngHợpChuyểnDày giáTrịMặtNạ, 같은 망의 선택적 giáTrịMặcĐịnh giáTrịCổngNối. */
    uint32_t mặtNạĐảoNgược = ~giáTrịMặtNạ;
    if (!giáTrịMặtNạ || (mặtNạĐảoNgược & (mặtNạĐảoNgược + 1)) || !địaChỉ || (địaChỉ >> 24) == 127 ||
        (địaChỉ >> 24) == 0 || (địaChỉ >> 28) >= 14 ||
        (mặtNạĐảoNgược > 1 && (!(địaChỉ & mặtNạĐảoNgược) || (địaChỉ & mặtNạĐảoNgược) == mặtNạĐảoNgược)) ||
        (giáTrịCổngNối && ((giáTrịCổngNối & giáTrịMặtNạ) != (địaChỉ & giáTrịMặtNạ) || giáTrịCổngNối == địaChỉ || (giáTrịCổngNối >> 28) >= 14 ||
         (mặtNạĐảoNgược > 1 && (!(giáTrịCổngNối & mặtNạĐảoNgược) || (giáTrịCổngNối & mặtNạĐảoNgược) == mặtNạĐảoNgược))))) return -22;
    /* 기존 연결을 địaChỉ 변경으로 몰래 끊지 않는다. */
    for (unsigned sốHiệu = 0; sốHiệu < 32; sốHiệu++) if (cácĐiểmCuốiỔCắmMạng[sốHiệu].loạiMụcKiểu &&
        !(cácĐiểmCuốiỔCắmMạng[sốHiệu].nhậnCổng && cácĐiểmCuốiỔCắmMạng[sốHiệu].điềuKhiểnKếtNối && ip_addr_isany(&cácĐiểmCuốiỔCắmMạng[sốHiệu].điềuKhiểnKếtNối->local_ip))) return -16;
    if(mạngHữuTuyếnDùng)dhcp_stop(&thiếtBịKếtNối);
    ip4_addr_t địaChỉMới, mặtNạMới, giáTrịCổngNốiMới;
    ip4_addr_set_u32(&địaChỉMới, lwip_htonl(địaChỉ)); ip4_addr_set_u32(&mặtNạMới, lwip_htonl(giáTrịMặtNạ)); ip4_addr_set_u32(&giáTrịCổngNốiMới, lwip_htonl(giáTrịCổngNối));
    netif_set_addr(&thiếtBịKếtNối, &địaChỉMới, &mặtNạMới, &giáTrịCổngNốiMới);
    return 0;
}

static struct raw_pcb *điểmCuốiPhảnHồi;
static uint32_t thửĐịaChỉ, thửThờiGian, thờiGianPhảnHồi;
static unsigned thửDãy, thửĐịnhDanh, dãyPhảnHồi;
static int trạngTháiPhảnHồi;
static u8_t cóPhảnHồi(void *cácĐốiSố, struct raw_pcb *điểmKếtThúc, struct pbuf *DữLiệu, const ip_addr_t *địaChỉ) {
    (void)cácĐốiSố; (void)điểmKếtThúc;
    unsigned char giáTrịĐầu[20], lờiĐáp[16];
    if (trạngTháiPhảnHồi != -11 || DữLiệu->tot_len < 36 ||
        lwip_ntohl(ip4_addr_get_u32(ip_2_ip4(địaChỉ))) != thửĐịaChỉ || pbuf_copy_partial(DữLiệu, giáTrịĐầu, 20, 0) != 20) return 0;
    unsigned cỡĐầuMục = (giáTrịĐầu[0] & 15) * 4;
    if ((giáTrịĐầu[0] >> 4) != 4 || cỡĐầuMục < 20 || DữLiệu->tot_len < cỡĐầuMục + 16 ||
        pbuf_copy_partial(DữLiệu, lờiĐáp, 16, cỡĐầuMục) != 16 || lờiĐáp[0] || lờiĐáp[1] ||
        (((unsigned)lờiĐáp[4] << 8) | lờiĐáp[5]) != thửĐịnhDanh ||
        (((unsigned)lờiĐáp[6] << 8) | lờiĐáp[7]) != thửDãy ||
        lờiĐáp[8] != 'J' || lờiĐáp[9] != 'K' || lờiĐáp[10] != 'O' || lờiĐáp[11] != 'S' ||
        (((uint32_t)lờiĐáp[12] << 24) | ((uint32_t)lờiĐáp[13] << 16) | ((uint32_t)lờiĐáp[14] << 8) | lờiĐáp[15]) != thửThờiGian) return 0;
    /* raw callback precedes icmp_input: verify the complete ICMP checksum. */
    if (pbuf_remove_header(DữLiệu, cỡĐầuMục)) return 0;
    if (inet_chksum_pbuf(DữLiệu)) { pbuf_add_header(DữLiệu, cỡĐầuMục); return 0; }
    thờiGianPhảnHồi = (uint32_t)miliGiâyGọnBoMạch() - thửThờiGian; dãyPhảnHồi = giáTrịĐầu[8]; trạngTháiPhảnHồi = 0;
    pbuf_free(DữLiệu); return 1;
}
int bắtChạyThửPhảnHồi(uint32_t địaChỉ, unsigned giáTrịThứTự) {
    if (!làĐãChuẩnBị || !netif_is_up(&thiếtBịKếtNối)) return -100;
    if (!địaChỉ || (địaChỉ >> 28) >= 14 || địaChỉ == 0xffffffffu) return -22;
    if (!điểmCuốiPhảnHồi) { điểmCuốiPhảnHồi = raw_new(IP_PROTO_ICMP); if (!điểmCuốiPhảnHồi) return -12; raw_recv(điểmCuốiPhảnHồi, cóPhảnHồi, 0); }
    thửĐịaChỉ = địaChỉ; thửDãy = giáTrịThứTự & 65535; thửĐịnhDanh = (thửĐịnhDanh + 1) & 65535;
    thửThờiGian = miliGiâyGọnBoMạch(); trạngTháiPhảnHồi = -11; thờiGianPhảnHồi = dãyPhảnHồi = 0;
    unsigned char DữLiệu[32] = {8,0,0,0};
    DữLiệu[4] = thửĐịnhDanh >> 8; DữLiệu[5] = thửĐịnhDanh; DữLiệu[6] = thửDãy >> 8; DữLiệu[7] = thửDãy;
    DữLiệu[8]='J'; DữLiệu[9]='K'; DữLiệu[10]='O'; DữLiệu[11]='S';
    DữLiệu[12]=thửThờiGian >> 24; DữLiệu[13]=thửThờiGian >> 16; DữLiệu[14]=thửThờiGian >> 8; DữLiệu[15]=thửThờiGian;
    for (unsigned chỉSốVịTrí = 16; chỉSốVịTrí < sizeof(DữLiệu); chỉSốVịTrí++) DữLiệu[chỉSốVịTrí] = chỉSốVịTrí;
    uint16_t tổngKiểmViệcXácMinh = inet_chksum(DữLiệu, sizeof(DữLiệu)); memcpy(DữLiệu + 2, &tổngKiểmViệcXácMinh, 2);
    struct pbuf *điệnDữLiệu = pbuf_alloc(PBUF_IP, sizeof(DữLiệu), PBUF_RAM); if (!điệnDữLiệu) return -12;
    pbuf_take(điệnDữLiệu, DữLiệu, sizeof(DữLiệu)); ip_addr_t điểmCuốiĐích; ip_addr_set_ip4_u32(&điểmCuốiĐích, lwip_htonl(địaChỉ));
    err_t giáTrịĐãXửLý = raw_sendto(điểmCuốiPhảnHồi, điệnDữLiệu, &điểmCuốiĐích); pbuf_free(điệnDữLiệu);
    if (giáTrịĐãXửLý) trạngTháiPhảnHồi = sốLỗi(giáTrịĐãXửLý);
    return giáTrịĐãXửLý ? trạngTháiPhảnHồi : 0;
}
int đọcThửPhảnHồi(unsigned giáTrịMục) {
    xemXétMạng();
    return giáTrịMục == 0 ? trạngTháiPhảnHồi : giáTrịMục == 1 ? (int)thờiGianPhảnHồi : giáTrịMục == 2 ? (int)dãyPhảnHồi : -22;
}
