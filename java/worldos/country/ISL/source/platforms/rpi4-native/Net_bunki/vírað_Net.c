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
#include "vírað_Net.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int bretti_vél_slóð(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(slóð) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (slóð)))
#endif
enum { Loop_númer = 16, Loop_COUNT = 256, biðminni_breyta_stærð = 2048 };
static struct {
    unsigned char 받기[Loop_COUNT][biðminni_breyta_stærð];
    unsigned char senda[Loop_COUNT][biðminni_breyta_stærð];
    uint16_t nota_VALUE, 생산;
    int 물리주소, Undirbúa, 속도;
    uint32_t 집계[5];
    uintptr_t sannprófa_Áfram_vara;
} vírað_VALUE __attribute__((aligned(64)));

static void samstilla(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_skyndiminni(void *gögn, unsigned lengd_VALUE, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)gögn + lengd_VALUE;
    for (uintptr_t slóð = (uintptr_t)gögn & ~(uintptr_t)63; slóð < 끝; slóð += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(slóð) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(slóð) : "memory");
    }
#else
    (void)gögn; (void)lengd_VALUE; (void)받기;
#endif
    samstilla();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned slóð, unsigned INDEX, int Skrift, unsigned VALUE) {
    uint32_t Skipun = (Skrift ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (slóð << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALUE & 65535);
    유선저장기(GENET_MDIO_CMD) = Skipun;
    유선저장기(GENET_MDIO_CMD) = Skipun | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t staða_VALUE_e10195a1 = 유선저장기(GENET_MDIO_CMD);
        if (!(staða_VALUE_e10195a1 & GENET_MDIO_START_BUSY))
            return staða_VALUE_e10195a1 & GENET_MDIO_READ_FAILED ? -1 : (int)(staða_VALUE_e10195a1 & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(vírað_VALUE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALUE) { return 물리전송(vírað_VALUE.물리주소, INDEX, 1, VALUE); }
static int 물리준비(void) {
    vírað_VALUE.물리주소 = -1;
    for (unsigned slóð = 0; slóð < 32; slóð++) {
        int 식별 = 물리전송(slóð, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { vírað_VALUE.물리주소 = slóð; break; }
    }
    if (vírað_VALUE.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VALUE = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VALUE < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VALUE & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VALUE = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VALUE < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VALUE & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Undirbúa_Loop(unsigned veggfóður_VALUE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALUE = veggfóður_VALUE + 0xc00 + GENET_DMA_RING_SIZE * Loop_númer;
    for (unsigned Staðsetning = 0; Staðsetning <= 0x30; Staðsetning += 4) 유선저장기(Loop_VALUE + Staðsetning) = 0;
    유선저장기(Loop_VALUE + 0x10) = (Loop_COUNT << 16) | biðminni_breyta_stærð;
    유선저장기(Loop_VALUE + 0x1c) = Loop_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (veggfóður_VALUE == GENET_RX_BASE) 유선저장기(Loop_VALUE + 0x28) = (5 << 16) | (Loop_COUNT >> 4);
    else 유선저장기(Loop_VALUE + 0x24) = 1;
    유선저장기(veggfóður_VALUE + 0x104c) = 8;
    유선저장기(veggfóður_VALUE + 0x1040) = __BIT(Loop_númer);
}
static void 받는주소(unsigned staða_INDEX) {
    uintptr_t slóð = (uintptr_t)vírað_VALUE.받기[staða_INDEX];
    CLEAN_skyndiminni((void *)slóð, biðminni_breyta_stærð, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(staða_INDEX)) = (uint32_t)slóð;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(staða_INDEX)) = (uint64_t)slóð >> 32;
    유선저장기(GENET_RX_DESC_STATUS(staða_INDEX)) = biðminni_breyta_stærð << 16;
}
static err_t 전문보내기(struct netif *tæki_VALUE, struct pbuf *전문) {
    if (!vírað_VALUE.Undirbúa || !netif_is_link_up(tæki_VALUE)) return ERR_RTE;
    unsigned Stærð = 전문->tot_len;
    if (!Stærð || Stærð > 1536) return ERR_BUF;
    uint16_t nota_VALUE = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_númer));
    if ((uint16_t)(vírað_VALUE.생산 - nota_VALUE) >= Loop_COUNT - 1) return ERR_MEM;
    unsigned staða_INDEX = vírað_VALUE.생산 % Loop_COUNT, 송신길이 = Stærð < 60 ? 60 : Stærð;
    unsigned char *gögn = vírað_VALUE.senda[staða_INDEX];
    memset(gögn, 0, 송신길이);
    if (pbuf_copy_partial(전문, gögn, Stærð, 0) != Stærð) return ERR_BUF;
    CLEAN_skyndiminni(gögn, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(staða_INDEX)) = (uint32_t)(uintptr_t)gögn;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(staða_INDEX)) = (uint64_t)(uintptr_t)gögn >> 32;
    유선저장기(GENET_TX_DESC_STATUS(staða_INDEX)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    samstilla();
    vírað_VALUE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_númer)) = vírað_VALUE.생산;
    vírað_VALUE.집계[2]++; vírað_VALUE.집계[3] += Stærð;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Undirbúa_vírað_Net(struct netif *tæki_VALUE) {
    unsigned char slóð[6];
    if (!유선장치있음() || !bretti_vél_slóð(slóð) || (slóð[0] & 1)) return ERR_IF;
    unsigned SUM_VALUE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALUE |= slóð[순번];
    if (!SUM_VALUE) return ERR_IF;
    memset(&vírað_VALUE, 0, sizeof(vírað_VALUE));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)slóð[0] << 24 | (uint32_t)slóð[1] << 16 | slóð[2] << 8 | slóð[3];
    유선저장기(GENET_UMAC_MAC1) = slóð[4] << 8 | slóð[5];
    Undirbúa_Loop(GENET_TX_BASE); Undirbúa_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COUNT; 순번++) 받는주소(순번);
    samstilla();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_númer);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_númer);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    tæki_VALUE->name[0] = 'e'; tæki_VALUE->name[1] = 'n'; tæki_VALUE->mtu = 1500;
    tæki_VALUE->hwaddr_len = 6; memcpy(tæki_VALUE->hwaddr, slóð, 6);
    tæki_VALUE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    tæki_VALUE->output = etharp_output; tæki_VALUE->linkoutput = 전문보내기;
    vírað_VALUE.Undirbúa = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *tæki_VALUE) {
    if (!vírað_VALUE.Undirbúa) return;
    uintptr_t NOW_VALUE = 보드밀리초();
    if (NOW_VALUE >= vírað_VALUE.sannprófa_Áfram_vara) {
        vírað_VALUE.sannprófa_Áfram_vara = NOW_VALUE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int staða_VALUE_e10195a1 = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned aðferð_MODE = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = aðferð_MODE == 7 ? 1000 : aðferð_MODE == 5 ? 100 : aðferð_MODE == 2 ? 10 : 0;
        vírað_VALUE.속도 = staða_VALUE_e10195a1 >= 0 && (staða_VALUE_e10195a1 & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (vírað_VALUE.속도) {
            uint32_t Stillingar = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Stillingar &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Stillingar | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Stillingar = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Stillingar | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(tæki_VALUE)) netif_set_link_up(tæki_VALUE);
        } else if (netif_is_link_up(tæki_VALUE)) netif_set_link_down(tæki_VALUE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_númer));
    unsigned 남음 = (uint16_t)(생산 - vírað_VALUE.nota_VALUE);
    if (남음 > Loop_COUNT) { vírað_VALUE.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned staða_INDEX = vírað_VALUE.nota_VALUE % Loop_COUNT;
        samstilla();
        uint32_t staða_VALUE_e10195a1 = 유선저장기(GENET_RX_DESC_STATUS(staða_INDEX));
        unsigned lengd_VALUE = (staða_VALUE_e10195a1 & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((staða_VALUE_e10195a1 & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || lengd_VALUE < 16 || lengd_VALUE > 1538) vírað_VALUE.집계[4]++;
        else {
            CLEAN_skyndiminni(vírað_VALUE.받기[staða_INDEX], lengd_VALUE, 1);
            struct pbuf *gögn = pbuf_alloc(PBUF_RAW, lengd_VALUE - 2, PBUF_POOL);
            if (!gögn) vírað_VALUE.집계[4]++;
            else if (pbuf_take(gögn, vírað_VALUE.받기[staða_INDEX] + 2, lengd_VALUE - 2) != ERR_OK || tæki_VALUE->input(gögn, tæki_VALUE) != ERR_OK) {
                pbuf_free(gögn); vírað_VALUE.집계[4]++;
            } else { vírað_VALUE.집계[0]++; vírað_VALUE.집계[1] += lengd_VALUE - 2; }
        }
        받는주소(staða_INDEX); samstilla(); vírað_VALUE.nota_VALUE++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_númer)) = vírað_VALUE.nota_VALUE;
    }
}
uint32_t 유선망집계(unsigned færsla_VALUE) {
    return færsla_VALUE < 5 ? vírað_VALUE.집계[færsla_VALUE] : færsla_VALUE == 5 ? vírað_VALUE.속도 : færsla_VALUE == 6 ? vírað_VALUE.Undirbúa : 0;
}
