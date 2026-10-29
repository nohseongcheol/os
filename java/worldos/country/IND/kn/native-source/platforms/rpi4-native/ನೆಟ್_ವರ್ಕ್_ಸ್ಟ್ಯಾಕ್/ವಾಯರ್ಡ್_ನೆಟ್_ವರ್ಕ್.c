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
#include "ವಾಯರ್ಡ್_ನೆಟ್_ವರ್ಕ್.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int ಬೋರ್ಡ್_ಯಂತ್ರ_ಇಮೇಲ್(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ಇಮೇಲ್) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ಇಮೇಲ್)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, ಬಫರ್_ಗಾತ್ರಿಸು = 2048 };
static struct {
    unsigned char 받기[고리개수][ಬಫರ್_ಗಾತ್ರಿಸು];
    unsigned char ಕಳುಹಿಸಿ[고리개수][ಬಫರ್_ಗಾತ್ರಿಸು];
    uint16_t 소비, 생산;
    int 물리주소, ಸಿದ್ಧಪಡಿಸು, 속도;
    uint32_t 집계[5];
    uintptr_t ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಮುಂದೆ_ಅಂಶ;
} ವಾಯರ್ಡ್_ಮೌಲ್ಯ __attribute__((aligned(64)));

static void ಸಿಂಕ್_ಮಾಡು(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void ಸ್ವಚ್ಛ_ಕ್ಯಾಶ್(void *ಡೇಟಾ, unsigned ಉದ್ದ_ಮೌಲ್ಯ, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ಡೇಟಾ + ಉದ್ದ_ಮೌಲ್ಯ;
    for (uintptr_t ಇಮೇಲ್ = (uintptr_t)ಡೇಟಾ & ~(uintptr_t)63; ಇಮೇಲ್ < 끝; ಇಮೇಲ್ += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ಇಮೇಲ್) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ಇಮೇಲ್) : "memory");
    }
#else
    (void)ಡೇಟಾ; (void)ಉದ್ದ_ಮೌಲ್ಯ; (void)받기;
#endif
    ಸಿಂಕ್_ಮಾಡು();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ಇಮೇಲ್, unsigned ಪದಸೂಚಿ, int ಬರೆ, unsigned ಮೌಲ್ಯ) {
    uint32_t ಆಜ್ಞೆ = (ಬರೆ ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ಇಮೇಲ್ << GENET_MDIO_ADDR_SHIFT) | (ಪದಸೂಚಿ << GENET_MDIO_REG_SHIFT) | (ಮೌಲ್ಯ & 65535);
    유선저장기(GENET_MDIO_CMD) = ಆಜ್ಞೆ;
    유선저장기(GENET_MDIO_CMD) = ಆಜ್ಞೆ | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t ಸ್ಥಿತಿ_ಮೌಲ್ಯ = 유선저장기(GENET_MDIO_CMD);
        if (!(ಸ್ಥಿತಿ_ಮೌಲ್ಯ & GENET_MDIO_START_BUSY))
            return ಸ್ಥಿತಿ_ಮೌಲ್ಯ & GENET_MDIO_READ_FAILED ? -1 : (int)(ಸ್ಥಿತಿ_ಮೌಲ್ಯ & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ಪದಸೂಚಿ) { return 물리전송(ವಾಯರ್ಡ್_ಮೌಲ್ಯ.물리주소, ಪದಸೂಚಿ, 0, 0); }
static int 물리쓰기(unsigned ಪದಸೂಚಿ, unsigned ಮೌಲ್ಯ) { return 물리전송(ವಾಯರ್ಡ್_ಮೌಲ್ಯ.물리주소, ಪದಸೂಚಿ, 1, ಮೌಲ್ಯ); }
static int 물리준비(void) {
    ವಾಯರ್ಡ್_ಮೌಲ್ಯ.물리주소 = -1;
    for (unsigned ಇಮೇಲ್ = 0; ಇಮೇಲ್ < 32; ಇಮೇಲ್++) {
        int 식별 = 물리전송(ಇಮೇಲ್, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ವಾಯರ್ಡ್_ಮೌಲ್ಯ.물리주소 = ಇಮೇಲ್; break; }
    }
    if (ವಾಯರ್ಡ್_ಮೌಲ್ಯ.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ಮೌಲ್ಯ = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ಮೌಲ್ಯ < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ಮೌಲ್ಯ & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ಮೌಲ್ಯ = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ಮೌಲ್ಯ < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ಮೌಲ್ಯ & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void ಸಿದ್ಧಪಡಿಸು_ಲೂಪ್(unsigned ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ಲೂಪ್_ಮೌಲ್ಯ = ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned ಸ್ಥಾನ = 0; ಸ್ಥಾನ <= 0x30; ಸ್ಥಾನ += 4) 유선저장기(ಲೂಪ್_ಮೌಲ್ಯ + ಸ್ಥಾನ) = 0;
    유선저장기(ಲೂಪ್_ಮೌಲ್ಯ + 0x10) = (고리개수 << 16) | ಬಫರ್_ಗಾತ್ರಿಸು;
    유선저장기(ಲೂಪ್_ಮೌಲ್ಯ + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ == GENET_RX_BASE) 유선저장기(ಲೂಪ್_ಮೌಲ್ಯ + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ಲೂಪ್_ಮೌಲ್ಯ + 0x24) = 1;
    유선저장기(ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ + 0x104c) = 8;
    유선저장기(ಹಿನ್ನೆಲೆ_ಮೌಲ್ಯ + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned ಹುದ್ದೆ_ಪದಸೂಚಿ) {
    uintptr_t ಇಮೇಲ್ = (uintptr_t)ವಾಯರ್ಡ್_ಮೌಲ್ಯ.받기[ಹುದ್ದೆ_ಪದಸೂಚಿ];
    ಸ್ವಚ್ಛ_ಕ್ಯಾಶ್((void *)ಇಮೇಲ್, ಬಫರ್_ಗಾತ್ರಿಸು, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(ಹುದ್ದೆ_ಪದಸೂಚಿ)) = (uint32_t)ಇಮೇಲ್;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(ಹುದ್ದೆ_ಪದಸೂಚಿ)) = (uint64_t)ಇಮೇಲ್ >> 32;
    유선저장기(GENET_RX_DESC_STATUS(ಹುದ್ದೆ_ಪದಸೂಚಿ)) = ಬಫರ್_ಗಾತ್ರಿಸು << 16;
}
static err_t 전문보내기(struct netif *ಸಾಧನ_ಮೌಲ್ಯ, struct pbuf *전문) {
    if (!ವಾಯರ್ಡ್_ಮೌಲ್ಯ.ಸಿದ್ಧಪಡಿಸು || !netif_is_link_up(ಸಾಧನ_ಮೌಲ್ಯ)) return ERR_RTE;
    unsigned ಗಾತ್ರ = 전문->tot_len;
    if (!ಗಾತ್ರ || ಗಾತ್ರ > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ವಾಯರ್ಡ್_ಮೌಲ್ಯ.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned ಹುದ್ದೆ_ಪದಸೂಚಿ = ವಾಯರ್ಡ್_ಮೌಲ್ಯ.생산 % 고리개수, 송신길이 = ಗಾತ್ರ < 60 ? 60 : ಗಾತ್ರ;
    unsigned char *ಡೇಟಾ = ವಾಯರ್ಡ್_ಮೌಲ್ಯ.ಕಳುಹಿಸಿ[ಹುದ್ದೆ_ಪದಸೂಚಿ];
    memset(ಡೇಟಾ, 0, 송신길이);
    if (pbuf_copy_partial(전문, ಡೇಟಾ, ಗಾತ್ರ, 0) != ಗಾತ್ರ) return ERR_BUF;
    ಸ್ವಚ್ಛ_ಕ್ಯಾಶ್(ಡೇಟಾ, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(ಹುದ್ದೆ_ಪದಸೂಚಿ)) = (uint32_t)(uintptr_t)ಡೇಟಾ;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(ಹುದ್ದೆ_ಪದಸೂಚಿ)) = (uint64_t)(uintptr_t)ಡೇಟಾ >> 32;
    유선저장기(GENET_TX_DESC_STATUS(ಹುದ್ದೆ_ಪದಸೂಚಿ)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    ಸಿಂಕ್_ಮಾಡು();
    ವಾಯರ್ಡ್_ಮೌಲ್ಯ.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ವಾಯರ್ಡ್_ಮೌಲ್ಯ.생산;
    ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[2]++; ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[3] += ಗಾತ್ರ;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t ಸಿದ್ಧಪಡಿಸು_ವಾಯರ್ಡ್_ನೆಟ್_ವರ್ಕ್(struct netif *ಸಾಧನ_ಮೌಲ್ಯ) {
    unsigned char ಇಮೇಲ್[6];
    if (!유선장치있음() || !ಬೋರ್ಡ್_ಯಂತ್ರ_ಇಮೇಲ್(ಇಮೇಲ್) || (ಇಮೇಲ್[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= ಇಮೇಲ್[순번];
    if (!합) return ERR_IF;
    memset(&ವಾಯರ್ಡ್_ಮೌಲ್ಯ, 0, sizeof(ವಾಯರ್ಡ್_ಮೌಲ್ಯ));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ಇಮೇಲ್[0] << 24 | (uint32_t)ಇಮೇಲ್[1] << 16 | ಇಮೇಲ್[2] << 8 | ಇಮೇಲ್[3];
    유선저장기(GENET_UMAC_MAC1) = ಇಮೇಲ್[4] << 8 | ಇಮೇಲ್[5];
    ಸಿದ್ಧಪಡಿಸು_ಲೂಪ್(GENET_TX_BASE); ಸಿದ್ಧಪಡಿಸು_ಲೂಪ್(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    ಸಿಂಕ್_ಮಾಡು();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ಸಾಧನ_ಮೌಲ್ಯ->name[0] = 'e'; ಸಾಧನ_ಮೌಲ್ಯ->name[1] = 'n'; ಸಾಧನ_ಮೌಲ್ಯ->mtu = 1500;
    ಸಾಧನ_ಮೌಲ್ಯ->hwaddr_len = 6; memcpy(ಸಾಧನ_ಮೌಲ್ಯ->hwaddr, ಇಮೇಲ್, 6);
    ಸಾಧನ_ಮೌಲ್ಯ->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ಸಾಧನ_ಮೌಲ್ಯ->output = etharp_output; ಸಾಧನ_ಮೌಲ್ಯ->linkoutput = 전문보내기;
    ವಾಯರ್ಡ್_ಮೌಲ್ಯ.ಸಿದ್ಧಪಡಿಸು = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ಸಾಧನ_ಮೌಲ್ಯ) {
    if (!ವಾಯರ್ಡ್_ಮೌಲ್ಯ.ಸಿದ್ಧಪಡಿಸು) return;
    uintptr_t ಇದೀಗ_ಮೌಲ್ಯ = 보드밀리초();
    if (ಇದೀಗ_ಮೌಲ್ಯ >= ವಾಯರ್ಡ್_ಮೌಲ್ಯ.ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಮುಂದೆ_ಅಂಶ) {
        ವಾಯರ್ಡ್_ಮೌಲ್ಯ.ಖಚಿತಪಡಿಸಿಕೊಳ್ಳು_ಮುಂದೆ_ಅಂಶ = ಇದೀಗ_ಮೌಲ್ಯ + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int ಸ್ಥಿತಿ_ಮೌಲ್ಯ = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ವಿಧಾನ_ಮೋಡ್ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ವಿಧಾನ_ಮೋಡ್ == 7 ? 1000 : ವಿಧಾನ_ಮೋಡ್ == 5 ? 100 : ವಿಧಾನ_ಮೋಡ್ == 2 ? 10 : 0;
        ವಾಯರ್ಡ್_ಮೌಲ್ಯ.속도 = ಸ್ಥಿತಿ_ಮೌಲ್ಯ >= 0 && (ಸ್ಥಿತಿ_ಮೌಲ್ಯ & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ವಾಯರ್ಡ್_ಮೌಲ್ಯ.속도) {
            uint32_t ಸಿದ್ಧತೆಗಳು = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            ಸಿದ್ಧತೆಗಳು &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = ಸಿದ್ಧತೆಗಳು | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ಸಿದ್ಧತೆಗಳು = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = ಸಿದ್ಧತೆಗಳು | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ಸಾಧನ_ಮೌಲ್ಯ)) netif_set_link_up(ಸಾಧನ_ಮೌಲ್ಯ);
        } else if (netif_is_link_up(ಸಾಧನ_ಮೌಲ್ಯ)) netif_set_link_down(ಸಾಧನ_ಮೌಲ್ಯ);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ವಾಯರ್ಡ್_ಮೌಲ್ಯ.소비);
    if (남음 > 고리개수) { ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned ಹುದ್ದೆ_ಪದಸೂಚಿ = ವಾಯರ್ಡ್_ಮೌಲ್ಯ.소비 % 고리개수;
        ಸಿಂಕ್_ಮಾಡು();
        uint32_t ಸ್ಥಿತಿ_ಮೌಲ್ಯ = 유선저장기(GENET_RX_DESC_STATUS(ಹುದ್ದೆ_ಪದಸೂಚಿ));
        unsigned ಉದ್ದ_ಮೌಲ್ಯ = (ಸ್ಥಿತಿ_ಮೌಲ್ಯ & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((ಸ್ಥಿತಿ_ಮೌಲ್ಯ & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || ಉದ್ದ_ಮೌಲ್ಯ < 16 || ಉದ್ದ_ಮೌಲ್ಯ > 1538) ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[4]++;
        else {
            ಸ್ವಚ್ಛ_ಕ್ಯಾಶ್(ವಾಯರ್ಡ್_ಮೌಲ್ಯ.받기[ಹುದ್ದೆ_ಪದಸೂಚಿ], ಉದ್ದ_ಮೌಲ್ಯ, 1);
            struct pbuf *ಡೇಟಾ = pbuf_alloc(PBUF_RAW, ಉದ್ದ_ಮೌಲ್ಯ - 2, PBUF_POOL);
            if (!ಡೇಟಾ) ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[4]++;
            else if (pbuf_take(ಡೇಟಾ, ವಾಯರ್ಡ್_ಮೌಲ್ಯ.받기[ಹುದ್ದೆ_ಪದಸೂಚಿ] + 2, ಉದ್ದ_ಮೌಲ್ಯ - 2) != ERR_OK || ಸಾಧನ_ಮೌಲ್ಯ->input(ಡೇಟಾ, ಸಾಧನ_ಮೌಲ್ಯ) != ERR_OK) {
                pbuf_free(ಡೇಟಾ); ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[4]++;
            } else { ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[0]++; ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[1] += ಉದ್ದ_ಮೌಲ್ಯ - 2; }
        }
        받는주소(ಹುದ್ದೆ_ಪದಸೂಚಿ); ಸಿಂಕ್_ಮಾಡು(); ವಾಯರ್ಡ್_ಮೌಲ್ಯ.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ವಾಯರ್ಡ್_ಮೌಲ್ಯ.소비;
    }
}
uint32_t 유선망집계(unsigned ನಮೂದು_ಮೌಲ್ಯ) {
    return ನಮೂದು_ಮೌಲ್ಯ < 5 ? ವಾಯರ್ಡ್_ಮೌಲ್ಯ.집계[ನಮೂದು_ಮೌಲ್ಯ] : ನಮೂದು_ಮೌಲ್ಯ == 5 ? ವಾಯರ್ಡ್_ಮೌಲ್ಯ.속도 : ನಮೂದು_ಮೌಲ್ಯ == 6 ? ವಾಯರ್ಡ್_ಮೌಲ್ಯ.ಸಿದ್ಧಪಡಿಸು : 0;
}
