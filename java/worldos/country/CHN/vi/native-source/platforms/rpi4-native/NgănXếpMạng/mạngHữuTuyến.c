/* SPDX-License-Identifier: LicenseRef-COSL AND BSD-2-Clause AND BSD-4-Clause
 * jkoros lwIP port of FreeBSD releng/14.3 GENET and BCM54xx PHY support.
 * This replaces the U-Boot-derived implementation; it is not a relicensing.
 * Original notices follow. Register definitions remain under their own notices.
 */
/*-
 * Copyright (c) 2020 Michael J Karels
 * Copyright (c) 2016, 2020 Jared McNeill <jmcneill@invisible.ca>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

/*-
 * SPDX-License-Identifier: BSD-4-Clause
 *
 * Copyright (c) 2000
 *	Bill Paul <wpaul@ee.columbia.edu>.  All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. All advertising materials mentioning features or use of this software
 *    must display the following acknowledgement:
 *	This product includes software developed by Bill Paul.
 * 4. Neither the name of the author nor the names of any co-contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY Bill Paul AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL Bill Paul OR THE VOICES IN HIS HEAD
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "../cáchĐặtTên/cácTênLiênKếtMáy.h"
#include "mạngHữuTuyến.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(thứBậcVòngLặp) (UINT32_C(1) << (thứBậcVòngLặp))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t miliGiâyGọnBoMạch(void);
extern int phầnCứngVậtLýBoMạch(void);
extern int địaChỉMáyBoMạch(unsigned char *);
#ifndef cácThanhGhiHữuTuyến
#define cácThanhGhiHữuTuyến(địaChỉ) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (địaChỉ)))
#endif
enum { sốVòngLặp = 16, sốLượngVòngLặp = 256, cỡBộĐệm = 2048 };
static struct {
    unsigned char nhận[sốLượngVòngLặp][cỡBộĐệm];
    unsigned char gửi[sốLượngVòngLặp][cỡBộĐệm];
    uint16_t tiêuThụGiáTrị, giáTrịSảnSinh;
    int địaChỉVậtLý, chuẩnBị, giáTrịTốcĐộ;
    uint32_t giáTrịThốngKê[5];
    uintptr_t xácMinhPhầnMụcKếTiếp;
} giáTrịHữuTuyến __attribute__((aligned(64)));

static void đồngBộHóa(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void bộNhớĐệmSạch(void *DữLiệu, unsigned độDài, int nhận) {
#ifndef JKOROS_GENET_TEST
    uintptr_t phầnKết = (uintptr_t)DữLiệu + độDài;
    for (uintptr_t địaChỉ = (uintptr_t)DữLiệu & ~(uintptr_t)63; địaChỉ < phầnKết; địaChỉ += 64) {
        if (nhận) __asm__ volatile("dc ivac, %0" :: "r"(địaChỉ) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(địaChỉ) : "memory");
    }
#else
    (void)DữLiệu; (void)độDài; (void)nhận;
#endif
    đồngBộHóa();
}
static void độTrễNgắnGọn(void) {
    uintptr_t phầnKết = miliGiâyGọnBoMạch() + 1;
    while (miliGiâyGọnBoMạch() < phầnKết) {}
}
static int chuyểnGiaoVậtLý(unsigned địaChỉ, unsigned sốHiệu, int ghi, unsigned giáTrị) {
    uint32_t lệnh = (ghi ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (địaChỉ << GENET_MDIO_ADDR_SHIFT) | (sốHiệu << GENET_MDIO_REG_SHIFT) | (giáTrị & 65535);
    cácThanhGhiHữuTuyến(GENET_MDIO_CMD) = lệnh;
    cácThanhGhiHữuTuyến(GENET_MDIO_CMD) = lệnh | GENET_MDIO_START_BUSY;
    uintptr_t phầnKết = miliGiâyGọnBoMạch() + 20;
    for (;;) {
        uint32_t giáTrịTrạngThái = cácThanhGhiHữuTuyến(GENET_MDIO_CMD);
        if (!(giáTrịTrạngThái & GENET_MDIO_START_BUSY))
            return giáTrịTrạngThái & GENET_MDIO_READ_FAILED ? -1 : (int)(giáTrịTrạngThái & 65535);
        if (miliGiâyGọnBoMạch() >= phầnKết) return -1;
    }
}
static int đọcVậtLý(unsigned sốHiệu) { return chuyểnGiaoVậtLý(giáTrịHữuTuyến.địaChỉVậtLý, sốHiệu, 0, 0); }
static int ghiVậtLý(unsigned sốHiệu, unsigned giáTrị) { return chuyểnGiaoVậtLý(giáTrịHữuTuyến.địaChỉVậtLý, sốHiệu, 1, giáTrị); }
static int chuẩnBịVậtLý(void) {
    giáTrịHữuTuyến.địaChỉVậtLý = -1;
    for (unsigned địaChỉ = 0; địaChỉ < 32; địaChỉ++) {
        int nhậnDạngGiáTrị = chuyểnGiaoVậtLý(địaChỉ, 2, 0, 0);
        if (nhậnDạngGiáTrị > 0 && nhậnDạngGiáTrị != 65535) { giáTrịHữuTuyến.địaChỉVậtLý = địaChỉ; break; }
    }
    if (giáTrịHữuTuyến.địaChỉVậtLý < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (ghiVậtLý(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int giáTrị = đọcVậtLý(BRGPHY_MII_AUXCTL);
    if (giáTrị < 0 || ghiVậtLý(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (giáTrị & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (ghiVậtLý(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    giáTrị = đọcVậtLý(BRGPHY_MII_SHADOW_1C);
    if (giáTrị < 0 || ghiVậtLý(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (giáTrị & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (ghiVậtLý(4, 0x0141) < 0 || ghiVậtLý(9, 0x0200) < 0) return -1;
    return ghiVậtLý(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void chuẩnBịVòngLặp(unsigned giáTrịNền) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned giáTrịVòngLặp = giáTrịNền + 0xc00 + GENET_DMA_RING_SIZE * sốVòngLặp;
    for (unsigned vịTrí = 0; vịTrí <= 0x30; vịTrí += 4) cácThanhGhiHữuTuyến(giáTrịVòngLặp + vịTrí) = 0;
    cácThanhGhiHữuTuyến(giáTrịVòngLặp + 0x10) = (sốLượngVòngLặp << 16) | cỡBộĐệm;
    cácThanhGhiHữuTuyến(giáTrịVòngLặp + 0x1c) = sốLượngVòngLặp * GENET_DMA_DESC_SIZE / 4 - 1;
    if (giáTrịNền == GENET_RX_BASE) cácThanhGhiHữuTuyến(giáTrịVòngLặp + 0x28) = (5 << 16) | (sốLượngVòngLặp >> 4);
    else cácThanhGhiHữuTuyến(giáTrịVòngLặp + 0x24) = 1;
    cácThanhGhiHữuTuyến(giáTrịNền + 0x104c) = 8;
    cácThanhGhiHữuTuyến(giáTrịNền + 0x1040) = __BIT(sốVòngLặp);
}
static void địaChỉĐangNhận(unsigned chỉSốVịTrí) {
    uintptr_t địaChỉ = (uintptr_t)giáTrịHữuTuyến.nhận[chỉSốVịTrí];
    bộNhớĐệmSạch((void *)địaChỉ, cỡBộĐệm, 0);
    cácThanhGhiHữuTuyến(GENET_RX_DESC_ADDRESS_LO(chỉSốVịTrí)) = (uint32_t)địaChỉ;
    cácThanhGhiHữuTuyến(GENET_RX_DESC_ADDRESS_HI(chỉSốVịTrí)) = (uint64_t)địaChỉ >> 32;
    cácThanhGhiHữuTuyến(GENET_RX_DESC_STATUS(chỉSốVịTrí)) = cỡBộĐệm << 16;
}
static err_t gửiĐiệnDữLiệu(struct netif *ThiếtBị, struct pbuf *điệnDữLiệu) {
    if (!giáTrịHữuTuyến.chuẩnBị || !netif_is_link_up(ThiếtBị)) return ERR_RTE;
    unsigned cỡ = điệnDữLiệu->tot_len;
    if (!cỡ || cỡ > 1536) return ERR_BUF;
    uint16_t tiêuThụGiáTrị = cácThanhGhiHữuTuyến(GENET_TX_DMA_CONS_INDEX(sốVòngLặp));
    if ((uint16_t)(giáTrịHữuTuyến.giáTrịSảnSinh - tiêuThụGiáTrị) >= sốLượngVòngLặp - 1) return ERR_MEM;
    unsigned chỉSốVịTrí = giáTrịHữuTuyến.giáTrịSảnSinh % sốLượngVòngLặp, độDàiTruyền = cỡ < 60 ? 60 : cỡ;
    unsigned char *DữLiệu = giáTrịHữuTuyến.gửi[chỉSốVịTrí];
    memset(DữLiệu, 0, độDàiTruyền);
    if (pbuf_copy_partial(điệnDữLiệu, DữLiệu, cỡ, 0) != cỡ) return ERR_BUF;
    bộNhớĐệmSạch(DữLiệu, độDàiTruyền, 0);
    cácThanhGhiHữuTuyến(GENET_TX_DESC_ADDRESS_LO(chỉSốVịTrí)) = (uint32_t)(uintptr_t)DữLiệu;
    cácThanhGhiHữuTuyến(GENET_TX_DESC_ADDRESS_HI(chỉSốVịTrí)) = (uint64_t)(uintptr_t)DữLiệu >> 32;
    cácThanhGhiHữuTuyến(GENET_TX_DESC_STATUS(chỉSốVịTrí)) = (độDàiTruyền << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    đồngBộHóa();
    giáTrịHữuTuyến.giáTrịSảnSinh++;
    cácThanhGhiHữuTuyến(GENET_TX_DMA_PROD_INDEX(sốVòngLặp)) = giáTrịHữuTuyến.giáTrịSảnSinh;
    giáTrịHữuTuyến.giáTrịThốngKê[2]++; giáTrịHữuTuyến.giáTrịThốngKê[3] += cỡ;
    return ERR_OK;
}
int cóThiếtBịHữuTuyến(void) {
    return phầnCứngVậtLýBoMạch() && ((cácThanhGhiHữuTuyến(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t chuẩnBịMạngHữuTuyến(struct netif *ThiếtBị) {
    unsigned char địaChỉ[6];
    if (!cóThiếtBịHữuTuyến() || !địaChỉMáyBoMạch(địaChỉ) || (địaChỉ[0] & 1)) return ERR_IF;
    unsigned giáTrịTổng = 0; for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < 6; chỉSốThứBậc++) giáTrịTổng |= địaChỉ[chỉSốThứBậc];
    if (!giáTrịTổng) return ERR_IF;
    memset(&giáTrịHữuTuyến, 0, sizeof(giáTrịHữuTuyến));
    cácThanhGhiHữuTuyến(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    cácThanhGhiHữuTuyến(GENET_RX_DMA_CTRL) = cácThanhGhiHữuTuyến(GENET_TX_DMA_CTRL) = 0;
    uint32_t trạngTháiBanĐầu = cácThanhGhiHữuTuyến(GENET_SYS_RBUF_FLUSH_CTRL);
    cácThanhGhiHữuTuyến(GENET_SYS_RBUF_FLUSH_CTRL) = trạngTháiBanĐầu | GENET_SYS_RBUF_FLUSH_RESET; độTrễNgắnGọn();
    cácThanhGhiHữuTuyến(GENET_SYS_RBUF_FLUSH_CTRL) = trạngTháiBanĐầu & ~GENET_SYS_RBUF_FLUSH_RESET; độTrễNgắnGọn();
    cácThanhGhiHữuTuyến(GENET_SYS_RBUF_FLUSH_CTRL) = 0; độTrễNgắnGọn();
    cácThanhGhiHữuTuyến(GENET_UMAC_CMD) = 0;
    cácThanhGhiHữuTuyến(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; độTrễNgắnGọn();
    cácThanhGhiHữuTuyến(GENET_UMAC_CMD) = 0;
    cácThanhGhiHữuTuyến(GENET_UMAC_MIB_CTRL) = 7;
    cácThanhGhiHữuTuyến(GENET_UMAC_MIB_CTRL) = 0;
    cácThanhGhiHữuTuyến(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (chuẩnBịVậtLý() < 0) return ERR_IF;
    cácThanhGhiHữuTuyến(GENET_UMAC_MAC0) = (uint32_t)địaChỉ[0] << 24 | (uint32_t)địaChỉ[1] << 16 | địaChỉ[2] << 8 | địaChỉ[3];
    cácThanhGhiHữuTuyến(GENET_UMAC_MAC1) = địaChỉ[4] << 8 | địaChỉ[5];
    chuẩnBịVòngLặp(GENET_TX_BASE); chuẩnBịVòngLặp(GENET_RX_BASE);
    for (unsigned chỉSốThứBậc = 0; chỉSốThứBậc < sốLượngVòngLặp; chỉSốThứBậc++) địaChỉĐangNhận(chỉSốThứBậc);
    đồngBộHóa();
    cácThanhGhiHữuTuyến(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(sốVòngLặp);
    cácThanhGhiHữuTuyến(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(sốVòngLặp);
    cácThanhGhiHữuTuyến(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    cácThanhGhiHữuTuyến(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    cácThanhGhiHữuTuyến(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    cácThanhGhiHữuTuyến(GENET_UMAC_MDF_CTRL) = 0;
    cácThanhGhiHữuTuyến(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ThiếtBị->name[0] = 'e'; ThiếtBị->name[1] = 'n'; ThiếtBị->mtu = 1500;
    ThiếtBị->hwaddr_len = 6; memcpy(ThiếtBị->hwaddr, địaChỉ, 6);
    ThiếtBị->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ThiếtBị->output = etharp_output; ThiếtBị->linkoutput = gửiĐiệnDữLiệu;
    giáTrịHữuTuyến.chuẩnBị = 1;
    return ERR_OK;
}
void xemXétMạngHữuTuyến(struct netif *ThiếtBị) {
    if (!giáTrịHữuTuyến.chuẩnBị) return;
    uintptr_t giáTrịBâyGiờ = miliGiâyGọnBoMạch();
    if (giáTrịBâyGiờ >= giáTrịHữuTuyến.xácMinhPhầnMụcKếTiếp) {
        giáTrịHữuTuyến.xácMinhPhầnMụcKếTiếp = giáTrịBâyGiờ + 500;
        đọcVậtLý(BRGPHY_MII_BMSR);
        int giáTrịTrạngThái = đọcVậtLý(BRGPHY_MII_BMSR), giáTrịPhụTrợ = đọcVậtLý(BRGPHY_MII_AUXSTS);
        unsigned chếĐộPhươngThức = giáTrịPhụTrợ < 0 ? 0 : (giáTrịPhụTrợ & BRGPHY_AUXSTS_AN_RES) >> 8;
        int giáTrịTốcĐộ = chếĐộPhươngThức == 7 ? 1000 : chếĐộPhươngThức == 5 ? 100 : chếĐộPhươngThức == 2 ? 10 : 0;
        giáTrịHữuTuyến.giáTrịTốcĐộ = giáTrịTrạngThái >= 0 && (giáTrịTrạngThái & BRGPHY_BMSR_LINK) ? giáTrịTốcĐộ : 0;
        if (giáTrịHữuTuyến.giáTrịTốcĐộ) {
            uint32_t cácThiếtLập = cácThanhGhiHữuTuyến(GENET_EXT_RGMII_OOB_CTRL);
            cácThiếtLập &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            cácThanhGhiHữuTuyến(GENET_EXT_RGMII_OOB_CTRL) = cácThiếtLập | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            cácThiếtLập = cácThanhGhiHữuTuyến(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            cácThanhGhiHữuTuyến(GENET_UMAC_CMD) = cácThiếtLập | (giáTrịTốcĐộ == 1000 ? GENET_UMAC_CMD_SPEED_1000 : giáTrịTốcĐộ == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ThiếtBị)) netif_set_link_up(ThiếtBị);
        } else if (netif_is_link_up(ThiếtBị)) netif_set_link_down(ThiếtBị);
    }
    uint16_t giáTrịSảnSinh = cácThanhGhiHữuTuyến(GENET_RX_DMA_PROD_INDEX(sốVòngLặp));
    unsigned dữLiệuSốDư = (uint16_t)(giáTrịSảnSinh - giáTrịHữuTuyến.tiêuThụGiáTrị);
    if (dữLiệuSốDư > sốLượngVòngLặp) { giáTrịHữuTuyến.giáTrịThốngKê[4]++; return; }
    for (unsigned thứBậcVòngLặp = 0; thứBậcVòngLặp < dữLiệuSốDư && thứBậcVòngLặp < 32; thứBậcVòngLặp++) {
        unsigned chỉSốVịTrí = giáTrịHữuTuyến.tiêuThụGiáTrị % sốLượngVòngLặp;
        đồngBộHóa();
        uint32_t giáTrịTrạngThái = cácThanhGhiHữuTuyến(GENET_RX_DESC_STATUS(chỉSốVịTrí));
        unsigned độDài = (giáTrịTrạngThái & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t giáTrịRanhGiới = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((giáTrịTrạngThái & (giáTrịRanhGiới | GENET_RX_DESC_STATUS_RX_ERROR)) != giáTrịRanhGiới || độDài < 16 || độDài > 1538) giáTrịHữuTuyến.giáTrịThốngKê[4]++;
        else {
            bộNhớĐệmSạch(giáTrịHữuTuyến.nhận[chỉSốVịTrí], độDài, 1);
            struct pbuf *DữLiệu = pbuf_alloc(PBUF_RAW, độDài - 2, PBUF_POOL);
            if (!DữLiệu) giáTrịHữuTuyến.giáTrịThốngKê[4]++;
            else if (pbuf_take(DữLiệu, giáTrịHữuTuyến.nhận[chỉSốVịTrí] + 2, độDài - 2) != ERR_OK || ThiếtBị->input(DữLiệu, ThiếtBị) != ERR_OK) {
                pbuf_free(DữLiệu); giáTrịHữuTuyến.giáTrịThốngKê[4]++;
            } else { giáTrịHữuTuyến.giáTrịThốngKê[0]++; giáTrịHữuTuyến.giáTrịThốngKê[1] += độDài - 2; }
        }
        địaChỉĐangNhận(chỉSốVịTrí); đồngBộHóa(); giáTrịHữuTuyến.tiêuThụGiáTrị++;
        cácThanhGhiHữuTuyến(GENET_RX_DMA_CONS_INDEX(sốVòngLặp)) = giáTrịHữuTuyến.tiêuThụGiáTrị;
    }
}
uint32_t thốngKêMạngHữuTuyến(unsigned giáTrịMục) {
    return giáTrịMục < 5 ? giáTrịHữuTuyến.giáTrịThốngKê[giáTrịMục] : giáTrịMục == 5 ? giáTrịHữuTuyến.giáTrịTốcĐộ : giáTrịMục == 6 ? giáTrịHữuTuyến.chuẩnBị : 0;
}
