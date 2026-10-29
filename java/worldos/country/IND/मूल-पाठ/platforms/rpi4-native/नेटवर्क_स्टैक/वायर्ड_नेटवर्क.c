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
#include "वायर्ड_नेटवर्क.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int बोर्ड_वास्तविक_पता(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(पता) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (पता)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, बफ़र_आकार = 2048 };
static struct {
    unsigned char 받기[고리개수][बफ़र_आकार];
    unsigned char भेजें[고리개수][बफ़र_आकार];
    uint16_t उपयोग_करें_मान, 생산;
    int 물리주소, 준비, 속도;
    uint32_t 집계[5];
    uintptr_t सत्यापित_करें_अगला_आइटम;
} वायर्ड_मान __attribute__((aligned(64)));

static void सिंक्रनाइज़_करें(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void साफ_कैश(void *आँकड़े, unsigned 길이, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)आँकड़े + 길이;
    for (uintptr_t पता = (uintptr_t)आँकड़े & ~(uintptr_t)63; पता < 끝; पता += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(पता) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(पता) : "memory");
    }
#else
    (void)आँकड़े; (void)길이; (void)받기;
#endif
    सिंक्रनाइज़_करें();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned पता, unsigned इंडेक्स, int लिखें, unsigned मान) {
    uint32_t आदेश = (लिखें ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (पता << GENET_MDIO_ADDR_SHIFT) | (इंडेक्स << GENET_MDIO_REG_SHIFT) | (मान & 65535);
    유선저장기(GENET_MDIO_CMD) = आदेश;
    유선저장기(GENET_MDIO_CMD) = आदेश | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t अवस्था_मान = 유선저장기(GENET_MDIO_CMD);
        if (!(अवस्था_मान & GENET_MDIO_START_BUSY))
            return अवस्था_मान & GENET_MDIO_READ_FAILED ? -1 : (int)(अवस्था_मान & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned इंडेक्स) { return 물리전송(वायर्ड_मान.물리주소, इंडेक्स, 0, 0); }
static int 물리쓰기(unsigned इंडेक्स, unsigned मान) { return 물리전송(वायर्ड_मान.물리주소, इंडेक्स, 1, मान); }
static int 물리준비(void) {
    वायर्ड_मान.물리주소 = -1;
    for (unsigned पता = 0; पता < 32; पता++) {
        int 식별 = 물리전송(पता, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { वायर्ड_मान.물리주소 = पता; break; }
    }
    if (वायर्ड_मान.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int मान = 물리읽기(BRGPHY_MII_AUXCTL);
    if (मान < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (मान & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    मान = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (मान < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (मान & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void 고리준비(unsigned वॉलपेपर_मान) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned लूप_मान = वॉलपेपर_मान + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned स्थान = 0; स्थान <= 0x30; स्थान += 4) 유선저장기(लूप_मान + स्थान) = 0;
    유선저장기(लूप_मान + 0x10) = (고리개수 << 16) | बफ़र_आकार;
    유선저장기(लूप_मान + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (वॉलपेपर_मान == GENET_RX_BASE) 유선저장기(लूप_मान + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(लूप_मान + 0x24) = 1;
    유선저장기(वॉलपेपर_मान + 0x104c) = 8;
    유선저장기(वॉलपेपर_मान + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned पद_इंडेक्स) {
    uintptr_t पता = (uintptr_t)वायर्ड_मान.받기[पद_इंडेक्स];
    साफ_कैश((void *)पता, बफ़र_आकार, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(पद_इंडेक्स)) = (uint32_t)पता;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(पद_इंडेक्स)) = (uint64_t)पता >> 32;
    유선저장기(GENET_RX_DESC_STATUS(पद_इंडेक्स)) = बफ़र_आकार << 16;
}
static err_t 전문보내기(struct netif *उपकरण_मान, struct pbuf *स्वतंत्रसंदेश) {
    if (!वायर्ड_मान.준비 || !netif_is_link_up(उपकरण_मान)) return ERR_RTE;
    unsigned आकार = स्वतंत्रसंदेश->tot_len;
    if (!आकार || आकार > 1536) return ERR_BUF;
    uint16_t उपयोग_करें_मान = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(वायर्ड_मान.생산 - उपयोग_करें_मान) >= 고리개수 - 1) return ERR_MEM;
    unsigned पद_इंडेक्स = वायर्ड_मान.생산 % 고리개수, 송신길이 = आकार < 60 ? 60 : आकार;
    unsigned char *आँकड़े = वायर्ड_मान.भेजें[पद_इंडेक्स];
    memset(आँकड़े, 0, 송신길이);
    if (pbuf_copy_partial(स्वतंत्रसंदेश, आँकड़े, आकार, 0) != आकार) return ERR_BUF;
    साफ_कैश(आँकड़े, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(पद_इंडेक्स)) = (uint32_t)(uintptr_t)आँकड़े;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(पद_इंडेक्स)) = (uint64_t)(uintptr_t)आँकड़े >> 32;
    유선저장기(GENET_TX_DESC_STATUS(पद_इंडेक्स)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    सिंक्रनाइज़_करें();
    वायर्ड_मान.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = वायर्ड_मान.생산;
    वायर्ड_मान.집계[2]++; वायर्ड_मान.집계[3] += आकार;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t 유선망준비(struct netif *उपकरण_मान) {
    unsigned char पता[6];
    if (!유선장치있음() || !बोर्ड_वास्तविक_पता(पता) || (पता[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= पता[순번];
    if (!합) return ERR_IF;
    memset(&वायर्ड_मान, 0, sizeof(वायर्ड_मान));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t प्रारंभिक_स्थिति = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = प्रारंभिक_स्थिति | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = प्रारंभिक_स्थिति & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)पता[0] << 24 | (uint32_t)पता[1] << 16 | पता[2] << 8 | पता[3];
    유선저장기(GENET_UMAC_MAC1) = पता[4] << 8 | पता[5];
    고리준비(GENET_TX_BASE); 고리준비(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    सिंक्रनाइज़_करें();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    उपकरण_मान->name[0] = 'e'; उपकरण_मान->name[1] = 'n'; उपकरण_मान->mtu = 1500;
    उपकरण_मान->hwaddr_len = 6; memcpy(उपकरण_मान->hwaddr, पता, 6);
    उपकरण_मान->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    उपकरण_मान->output = etharp_output; उपकरण_मान->linkoutput = 전문보내기;
    वायर्ड_मान.준비 = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *उपकरण_मान) {
    if (!वायर्ड_मान.준비) return;
    uintptr_t अभी_प्रासंगिक_मान = 보드밀리초();
    if (अभी_प्रासंगिक_मान >= वायर्ड_मान.सत्यापित_करें_अगला_आइटम) {
        वायर्ड_मान.सत्यापित_करें_अगला_आइटम = अभी_प्रासंगिक_मान + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int अवस्था_मान = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned विधि_मोड = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = विधि_मोड == 7 ? 1000 : विधि_मोड == 5 ? 100 : विधि_मोड == 2 ? 10 : 0;
        वायर्ड_मान.속도 = अवस्था_मान >= 0 && (अवस्था_मान & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (वायर्ड_मान.속도) {
            uint32_t विन्यास = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            विन्यास &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = विन्यास | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            विन्यास = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = विन्यास | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(उपकरण_मान)) netif_set_link_up(उपकरण_मान);
        } else if (netif_is_link_up(उपकरण_मान)) netif_set_link_down(उपकरण_मान);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - वायर्ड_मान.उपयोग_करें_मान);
    if (남음 > 고리개수) { वायर्ड_मान.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned पद_इंडेक्स = वायर्ड_मान.उपयोग_करें_मान % 고리개수;
        सिंक्रनाइज़_करें();
        uint32_t अवस्था_मान = 유선저장기(GENET_RX_DESC_STATUS(पद_इंडेक्स));
        unsigned 길이 = (अवस्था_मान & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((अवस्था_मान & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || 길이 < 16 || 길이 > 1538) वायर्ड_मान.집계[4]++;
        else {
            साफ_कैश(वायर्ड_मान.받기[पद_इंडेक्स], 길이, 1);
            struct pbuf *आँकड़े = pbuf_alloc(PBUF_RAW, 길이 - 2, PBUF_POOL);
            if (!आँकड़े) वायर्ड_मान.집계[4]++;
            else if (pbuf_take(आँकड़े, वायर्ड_मान.받기[पद_इंडेक्स] + 2, 길이 - 2) != ERR_OK || उपकरण_मान->input(आँकड़े, उपकरण_मान) != ERR_OK) {
                pbuf_free(आँकड़े); वायर्ड_मान.집계[4]++;
            } else { वायर्ड_मान.집계[0]++; वायर्ड_मान.집계[1] += 길이 - 2; }
        }
        받는주소(पद_इंडेक्स); सिंक्रनाइज़_करें(); वायर्ड_मान.उपयोग_करें_मान++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = वायर्ड_मान.उपयोग_करें_मान;
    }
}
uint32_t 유선망집계(unsigned एन्ट्री_मान) {
    return एन्ट्री_मान < 5 ? वायर्ड_मान.집계[एन्ट्री_मान] : एन्ट्री_मान == 5 ? वायर्ड_मान.속도 : एन्ट्री_मान == 6 ? वायर्ड_मान.준비 : 0;
}
