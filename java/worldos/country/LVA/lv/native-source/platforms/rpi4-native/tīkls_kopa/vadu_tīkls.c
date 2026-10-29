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
#include "vadu_tīkls.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Panelis_reālā_adrese(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(adrese) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (adrese)))
#endif
enum { Loop_numurs = 16, Loop_COUNT = 256, bufera_lielums = 2048 };
static struct {
    unsigned char saņemt[Loop_COUNT][bufera_lielums];
    unsigned char sūtīt[Loop_COUNT][bufera_lielums];
    uint16_t patērēt_VALUE, 생산;
    int 물리주소, Sagatavot, 속도;
    uint32_t 집계[5];
    uintptr_t verificēt_Tālāk_krājums;
} vadu_VALUE __attribute__((aligned(64)));

static void sinhronizēt(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_kešatmiņa(void *dati, unsigned 길이, int saņemt) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)dati + 길이;
    for (uintptr_t adrese = (uintptr_t)dati & ~(uintptr_t)63; adrese < 끝; adrese += 64) {
        if (saņemt) __asm__ volatile("dc ivac, %0" :: "r"(adrese) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(adrese) : "memory");
    }
#else
    (void)dati; (void)길이; (void)saņemt;
#endif
    sinhronizēt();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned adrese, unsigned INDEX, int Rakstīt, unsigned VALUE) {
    uint32_t Komanda = (Rakstīt ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (adrese << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALUE & 65535);
    유선저장기(GENET_MDIO_CMD) = Komanda;
    유선저장기(GENET_MDIO_CMD) = Komanda | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Statuss_VALUE = 유선저장기(GENET_MDIO_CMD);
        if (!(Statuss_VALUE & GENET_MDIO_START_BUSY))
            return Statuss_VALUE & GENET_MDIO_READ_FAILED ? -1 : (int)(Statuss_VALUE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(vadu_VALUE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALUE) { return 물리전송(vadu_VALUE.물리주소, INDEX, 1, VALUE); }
static int 물리준비(void) {
    vadu_VALUE.물리주소 = -1;
    for (unsigned adrese = 0; adrese < 32; adrese++) {
        int 식별 = 물리전송(adrese, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { vadu_VALUE.물리주소 = adrese; break; }
    }
    if (vadu_VALUE.물리주소 < 0) return -1;
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
static void Sagatavot_Loop(unsigned Fons_VALUE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALUE = Fons_VALUE + 0xc00 + GENET_DMA_RING_SIZE * Loop_numurs;
    for (unsigned Novietojums = 0; Novietojums <= 0x30; Novietojums += 4) 유선저장기(Loop_VALUE + Novietojums) = 0;
    유선저장기(Loop_VALUE + 0x10) = (Loop_COUNT << 16) | bufera_lielums;
    유선저장기(Loop_VALUE + 0x1c) = Loop_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Fons_VALUE == GENET_RX_BASE) 유선저장기(Loop_VALUE + 0x28) = (5 << 16) | (Loop_COUNT >> 4);
    else 유선저장기(Loop_VALUE + 0x24) = 1;
    유선저장기(Fons_VALUE + 0x104c) = 8;
    유선저장기(Fons_VALUE + 0x1040) = __BIT(Loop_numurs);
}
static void 받는주소(unsigned pozīcijas_indekss) {
    uintptr_t adrese = (uintptr_t)vadu_VALUE.saņemt[pozīcijas_indekss];
    CLEAN_kešatmiņa((void *)adrese, bufera_lielums, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(pozīcijas_indekss)) = (uint32_t)adrese;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(pozīcijas_indekss)) = (uint64_t)adrese >> 32;
    유선저장기(GENET_RX_DESC_STATUS(pozīcijas_indekss)) = bufera_lielums << 16;
}
static err_t sūtīt_datogramma(struct netif *ierīce_VALUE, struct pbuf *datogramma) {
    if (!vadu_VALUE.Sagatavot || !netif_is_link_up(ierīce_VALUE)) return ERR_RTE;
    unsigned Izmērs = datogramma->tot_len;
    if (!Izmērs || Izmērs > 1536) return ERR_BUF;
    uint16_t patērēt_VALUE = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_numurs));
    if ((uint16_t)(vadu_VALUE.생산 - patērēt_VALUE) >= Loop_COUNT - 1) return ERR_MEM;
    unsigned pozīcijas_indekss = vadu_VALUE.생산 % Loop_COUNT, 송신길이 = Izmērs < 60 ? 60 : Izmērs;
    unsigned char *dati = vadu_VALUE.sūtīt[pozīcijas_indekss];
    memset(dati, 0, 송신길이);
    if (pbuf_copy_partial(datogramma, dati, Izmērs, 0) != Izmērs) return ERR_BUF;
    CLEAN_kešatmiņa(dati, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(pozīcijas_indekss)) = (uint32_t)(uintptr_t)dati;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(pozīcijas_indekss)) = (uint64_t)(uintptr_t)dati >> 32;
    유선저장기(GENET_TX_DESC_STATUS(pozīcijas_indekss)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sinhronizēt();
    vadu_VALUE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_numurs)) = vadu_VALUE.생산;
    vadu_VALUE.집계[2]++; vadu_VALUE.집계[3] += Izmērs;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Sagatavot_vadu_tīkls(struct netif *ierīce_VALUE) {
    unsigned char adrese[6];
    if (!유선장치있음() || !Panelis_reālā_adrese(adrese) || (adrese[0] & 1)) return ERR_IF;
    unsigned SUM_VALUE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALUE |= adrese[순번];
    if (!SUM_VALUE) return ERR_IF;
    memset(&vadu_VALUE, 0, sizeof(vadu_VALUE));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t sākumstāvoklis = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = sākumstāvoklis | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = sākumstāvoklis & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)adrese[0] << 24 | (uint32_t)adrese[1] << 16 | adrese[2] << 8 | adrese[3];
    유선저장기(GENET_UMAC_MAC1) = adrese[4] << 8 | adrese[5];
    Sagatavot_Loop(GENET_TX_BASE); Sagatavot_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COUNT; 순번++) 받는주소(순번);
    sinhronizēt();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_numurs);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_numurs);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ierīce_VALUE->name[0] = 'e'; ierīce_VALUE->name[1] = 'n'; ierīce_VALUE->mtu = 1500;
    ierīce_VALUE->hwaddr_len = 6; memcpy(ierīce_VALUE->hwaddr, adrese, 6);
    ierīce_VALUE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ierīce_VALUE->output = etharp_output; ierīce_VALUE->linkoutput = sūtīt_datogramma;
    vadu_VALUE.Sagatavot = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ierīce_VALUE) {
    if (!vadu_VALUE.Sagatavot) return;
    uintptr_t NOW_VALUE = 보드밀리초();
    if (NOW_VALUE >= vadu_VALUE.verificēt_Tālāk_krājums) {
        vadu_VALUE.verificēt_Tālāk_krājums = NOW_VALUE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Statuss_VALUE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metode_MODE = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metode_MODE == 7 ? 1000 : metode_MODE == 5 ? 100 : metode_MODE == 2 ? 10 : 0;
        vadu_VALUE.속도 = Statuss_VALUE >= 0 && (Statuss_VALUE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (vadu_VALUE.속도) {
            uint32_t Uzstādījumi = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Uzstādījumi &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Uzstādījumi | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Uzstādījumi = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Uzstādījumi | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ierīce_VALUE)) netif_set_link_up(ierīce_VALUE);
        } else if (netif_is_link_up(ierīce_VALUE)) netif_set_link_down(ierīce_VALUE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_numurs));
    unsigned 남음 = (uint16_t)(생산 - vadu_VALUE.patērēt_VALUE);
    if (남음 > Loop_COUNT) { vadu_VALUE.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned pozīcijas_indekss = vadu_VALUE.patērēt_VALUE % Loop_COUNT;
        sinhronizēt();
        uint32_t Statuss_VALUE = 유선저장기(GENET_RX_DESC_STATUS(pozīcijas_indekss));
        unsigned 길이 = (Statuss_VALUE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Statuss_VALUE & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || 길이 < 16 || 길이 > 1538) vadu_VALUE.집계[4]++;
        else {
            CLEAN_kešatmiņa(vadu_VALUE.saņemt[pozīcijas_indekss], 길이, 1);
            struct pbuf *dati = pbuf_alloc(PBUF_RAW, 길이 - 2, PBUF_POOL);
            if (!dati) vadu_VALUE.집계[4]++;
            else if (pbuf_take(dati, vadu_VALUE.saņemt[pozīcijas_indekss] + 2, 길이 - 2) != ERR_OK || ierīce_VALUE->input(dati, ierīce_VALUE) != ERR_OK) {
                pbuf_free(dati); vadu_VALUE.집계[4]++;
            } else { vadu_VALUE.집계[0]++; vadu_VALUE.집계[1] += 길이 - 2; }
        }
        받는주소(pozīcijas_indekss); sinhronizēt(); vadu_VALUE.patērēt_VALUE++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_numurs)) = vadu_VALUE.patērēt_VALUE;
    }
}
uint32_t 유선망집계(unsigned ievade_VALUE) {
    return ievade_VALUE < 5 ? vadu_VALUE.집계[ievade_VALUE] : ievade_VALUE == 5 ? vadu_VALUE.속도 : ievade_VALUE == 6 ? vadu_VALUE.Sagatavot : 0;
}
