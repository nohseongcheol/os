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

#include "../명명/기계연결이름.h"
#include "વાયર્ડ_નેટવર્ક.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int બોર્ડ_મશીન_સરનામું(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(સરનામું) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (સરનામું)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, બફર_આકાર = 2048 };
static struct {
    unsigned char 받기[고리개수][બફર_આકાર];
    unsigned char મોકલો[고리개수][બફર_આકાર];
    uint16_t 소비, 생산;
    int 물리주소, તૈયાર_કરો, 속도;
    uint32_t 집계[5];
    uintptr_t ચકાસવું_આગલું_આઇટમ;
} વાયર્ડ_મૂલ્ય __attribute__((aligned(64)));

static void સિંક્રનાઇઝ(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void નિર્મળ_કૅશ(void *ડેટા, unsigned લંબાઈ_મૂલ્ય, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ડેટા + લંબાઈ_મૂલ્ય;
    for (uintptr_t સરનામું = (uintptr_t)ડેટા & ~(uintptr_t)63; સરનામું < 끝; સરનામું += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(સરનામું) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(સરનામું) : "memory");
    }
#else
    (void)ડેટા; (void)લંબાઈ_મૂલ્ય; (void)받기;
#endif
    સિંક્રનાઇઝ();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned સરનામું, unsigned અનુક્રમણિકા, int લખો, unsigned મૂલ્ય) {
    uint32_t આદેશ = (લખો ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (સરનામું << GENET_MDIO_ADDR_SHIFT) | (અનુક્રમણિકા << GENET_MDIO_REG_SHIFT) | (મૂલ્ય & 65535);
    유선저장기(GENET_MDIO_CMD) = આદેશ;
    유선저장기(GENET_MDIO_CMD) = આદેશ | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t સ્થિતિ_મૂલ્ય_e10195a1 = 유선저장기(GENET_MDIO_CMD);
        if (!(સ્થિતિ_મૂલ્ય_e10195a1 & GENET_MDIO_START_BUSY))
            return સ્થિતિ_મૂલ્ય_e10195a1 & GENET_MDIO_READ_FAILED ? -1 : (int)(સ્થિતિ_મૂલ્ય_e10195a1 & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned અનુક્રમણિકા) { return 물리전송(વાયર્ડ_મૂલ્ય.물리주소, અનુક્રમણિકા, 0, 0); }
static int 물리쓰기(unsigned અનુક્રમણિકા, unsigned મૂલ્ય) { return 물리전송(વાયર્ડ_મૂલ્ય.물리주소, અનુક્રમણિકા, 1, મૂલ્ય); }
static int 물리준비(void) {
    વાયર્ડ_મૂલ્ય.물리주소 = -1;
    for (unsigned સરનામું = 0; સરનામું < 32; સરનામું++) {
        int 식별 = 물리전송(સરનામું, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { વાયર્ડ_મૂલ્ય.물리주소 = સરનામું; break; }
    }
    if (વાયર્ડ_મૂલ્ય.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int મૂલ્ય = 물리읽기(BRGPHY_MII_AUXCTL);
    if (મૂલ્ય < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (મૂલ્ય & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    મૂલ્ય = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (મૂલ્ય < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (મૂલ્ય & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void તૈયાર_કરો_લૂપ(unsigned વૉલપેપર_મૂલ્ય) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned લૂપ_મૂલ્ય = વૉલપેપર_મૂલ્ય + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned સ્થાન = 0; સ્થાન <= 0x30; સ્થાન += 4) 유선저장기(લૂપ_મૂલ્ય + સ્થાન) = 0;
    유선저장기(લૂપ_મૂલ્ય + 0x10) = (고리개수 << 16) | બફર_આકાર;
    유선저장기(લૂપ_મૂલ્ય + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (વૉલપેપર_મૂલ્ય == GENET_RX_BASE) 유선저장기(લૂપ_મૂલ્ય + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(લૂપ_મૂલ્ય + 0x24) = 1;
    유선저장기(વૉલપેપર_મૂલ્ય + 0x104c) = 8;
    유선저장기(વૉલપેપર_મૂલ્ય + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned સ્થિતિ_અનુક્રમણિકા) {
    uintptr_t સરનામું = (uintptr_t)વાયર્ડ_મૂલ્ય.받기[સ્થિતિ_અનુક્રમણિકા];
    નિર્મળ_કૅશ((void *)સરનામું, બફર_આકાર, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(સ્થિતિ_અનુક્રમણિકા)) = (uint32_t)સરનામું;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(સ્થિતિ_અનુક્રમણિકા)) = (uint64_t)સરનામું >> 32;
    유선저장기(GENET_RX_DESC_STATUS(સ્થિતિ_અનુક્રમણિકા)) = બફર_આકાર << 16;
}
static err_t 전문보내기(struct netif *ડિવાઇસ_મૂલ્ય, struct pbuf *전문) {
    if (!વાયર્ડ_મૂલ્ય.તૈયાર_કરો || !netif_is_link_up(ડિવાઇસ_મૂલ્ય)) return ERR_RTE;
    unsigned માપ = 전문->tot_len;
    if (!માપ || માપ > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(વાયર્ડ_મૂલ્ય.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned સ્થિતિ_અનુક્રમણિકા = વાયર્ડ_મૂલ્ય.생산 % 고리개수, 송신길이 = માપ < 60 ? 60 : માપ;
    unsigned char *ડેટા = વાયર્ડ_મૂલ્ય.મોકલો[સ્થિતિ_અનુક્રમણિકા];
    memset(ડેટા, 0, 송신길이);
    if (pbuf_copy_partial(전문, ડેટા, માપ, 0) != માપ) return ERR_BUF;
    નિર્મળ_કૅશ(ડેટા, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(સ્થિતિ_અનુક્રમણિકા)) = (uint32_t)(uintptr_t)ડેટા;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(સ્થિતિ_અનુક્રમણિકા)) = (uint64_t)(uintptr_t)ડેટા >> 32;
    유선저장기(GENET_TX_DESC_STATUS(સ્થિતિ_અનુક્રમણિકા)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    સિંક્રનાઇઝ();
    વાયર્ડ_મૂલ્ય.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = વાયર્ડ_મૂલ્ય.생산;
    વાયર્ડ_મૂલ્ય.집계[2]++; વાયર્ડ_મૂલ્ય.집계[3] += માપ;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t તૈયાર_કરો_વાયર્ડ_નેટવર્ક(struct netif *ડિવાઇસ_મૂલ્ય) {
    unsigned char સરનામું[6];
    if (!유선장치있음() || !બોર્ડ_મશીન_સરનામું(સરનામું) || (સરનામું[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= સરનામું[순번];
    if (!합) return ERR_IF;
    memset(&વાયર્ડ_મૂલ્ય, 0, sizeof(વાયર્ડ_મૂલ્ય));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t 초기 = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 초기 | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 초기 & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)સરનામું[0] << 24 | (uint32_t)સરનામું[1] << 16 | સરનામું[2] << 8 | સરનામું[3];
    유선저장기(GENET_UMAC_MAC1) = સરનામું[4] << 8 | સરનામું[5];
    તૈયાર_કરો_લૂપ(GENET_TX_BASE); તૈયાર_કરો_લૂપ(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    સિંક્રનાઇઝ();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ડિવાઇસ_મૂલ્ય->name[0] = 'e'; ડિવાઇસ_મૂલ્ય->name[1] = 'n'; ડિવાઇસ_મૂલ્ય->mtu = 1500;
    ડિવાઇસ_મૂલ્ય->hwaddr_len = 6; memcpy(ડિવાઇસ_મૂલ્ય->hwaddr, સરનામું, 6);
    ડિવાઇસ_મૂલ્ય->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ડિવાઇસ_મૂલ્ય->output = etharp_output; ડિવાઇસ_મૂલ્ય->linkoutput = 전문보내기;
    વાયર્ડ_મૂલ્ય.તૈયાર_કરો = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ડિવાઇસ_મૂલ્ય) {
    if (!વાયર્ડ_મૂલ્ય.તૈયાર_કરો) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= વાયર્ડ_મૂલ્ય.ચકાસવું_આગલું_આઇટમ) {
        વાયર્ડ_મૂલ્ય.ચકાસવું_આગલું_આઇટમ = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int સ્થિતિ_મૂલ્ય_e10195a1 = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned પદ્ધતિ_મોડ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = પદ્ધતિ_મોડ == 7 ? 1000 : પદ્ધતિ_મોડ == 5 ? 100 : પદ્ધતિ_મોડ == 2 ? 10 : 0;
        વાયર્ડ_મૂલ્ય.속도 = સ્થિતિ_મૂલ્ય_e10195a1 >= 0 && (સ્થિતિ_મૂલ્ય_e10195a1 & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (વાયર્ડ_મૂલ્ય.속도) {
            uint32_t સુયોજના = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            સુયોજના &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = સુયોજના | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            સુયોજના = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = સુયોજના | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ડિવાઇસ_મૂલ્ય)) netif_set_link_up(ડિવાઇસ_મૂલ્ય);
        } else if (netif_is_link_up(ડિવાઇસ_મૂલ્ય)) netif_set_link_down(ડિવાઇસ_મૂલ્ય);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - વાયર્ડ_મૂલ્ય.소비);
    if (남음 > 고리개수) { વાયર્ડ_મૂલ્ય.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned સ્થિતિ_અનુક્રમણિકા = વાયર્ડ_મૂલ્ય.소비 % 고리개수;
        સિંક્રનાઇઝ();
        uint32_t સ્થિતિ_મૂલ્ય_e10195a1 = 유선저장기(GENET_RX_DESC_STATUS(સ્થિતિ_અનુક્રમણિકા));
        unsigned લંબાઈ_મૂલ્ય = (સ્થિતિ_મૂલ્ય_e10195a1 & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((સ્થિતિ_મૂલ્ય_e10195a1 & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || લંબાઈ_મૂલ્ય < 16 || લંબાઈ_મૂલ્ય > 1538) વાયર્ડ_મૂલ્ય.집계[4]++;
        else {
            નિર્મળ_કૅશ(વાયર્ડ_મૂલ્ય.받기[સ્થિતિ_અનુક્રમણિકા], લંબાઈ_મૂલ્ય, 1);
            struct pbuf *ડેટા = pbuf_alloc(PBUF_RAW, લંબાઈ_મૂલ્ય - 2, PBUF_POOL);
            if (!ડેટા) વાયર્ડ_મૂલ્ય.집계[4]++;
            else if (pbuf_take(ડેટા, વાયર્ડ_મૂલ્ય.받기[સ્થિતિ_અનુક્રમણિકા] + 2, લંબાઈ_મૂલ્ય - 2) != ERR_OK || ડિવાઇસ_મૂલ્ય->input(ડેટા, ડિવાઇસ_મૂલ્ય) != ERR_OK) {
                pbuf_free(ડેટા); વાયર્ડ_મૂલ્ય.집계[4]++;
            } else { વાયર્ડ_મૂલ્ય.집계[0]++; વાયર્ડ_મૂલ્ય.집계[1] += લંબાઈ_મૂલ્ય - 2; }
        }
        받는주소(સ્થિતિ_અનુક્રમણિકા); સિંક્રનાઇઝ(); વાયર્ડ_મૂલ્ય.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = વાયર્ડ_મૂલ્ય.소비;
    }
}
uint32_t 유선망집계(unsigned પ્રવેશ_મૂલ્ય) {
    return પ્રવેશ_મૂલ્ય < 5 ? વાયર્ડ_મૂલ્ય.집계[પ્રવેશ_મૂલ્ય] : પ્રવેશ_મૂલ્ય == 5 ? વાયર્ડ_મૂલ્ય.속도 : પ્રવેશ_મૂલ્ય == 6 ? વાયર્ડ_મૂલ્ય.તૈયાર_કરો : 0;
}
