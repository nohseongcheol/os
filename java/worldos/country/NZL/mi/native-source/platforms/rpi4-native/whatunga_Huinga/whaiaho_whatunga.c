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
#include "whaiaho_whatunga.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int papa_mīhini_ADDRESS(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ADDRESS) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ADDRESS)))
#endif
enum { 고리번호 = 16, Loop_COUNT = 256, pūreirei_rahi = 2048 };
static struct {
    unsigned char 받기[Loop_COUNT][pūreirei_rahi];
    unsigned char tuku[Loop_COUNT][pūreirei_rahi];
    uint16_t 소비, 생산;
    int 물리주소, Whakarite, 속도;
    uint32_t 집계[5];
    uintptr_t manatoko_Panuku_tuemi;
} whaiaho_uara __attribute__((aligned(64)));

static void tukutahi(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_keteroki(void *raraunga, unsigned roa_uara, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)raraunga + roa_uara;
    for (uintptr_t ADDRESS = (uintptr_t)raraunga & ~(uintptr_t)63; ADDRESS < 끝; ADDRESS += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ADDRESS) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ADDRESS) : "memory");
    }
#else
    (void)raraunga; (void)roa_uara; (void)받기;
#endif
    tukutahi();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ADDRESS, unsigned INDEX, int Tuhia, unsigned uara) {
    uint32_t tono = (Tuhia ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ADDRESS << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (uara & 65535);
    유선저장기(GENET_MDIO_CMD) = tono;
    유선저장기(GENET_MDIO_CMD) = tono | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t tūnga_uara = 유선저장기(GENET_MDIO_CMD);
        if (!(tūnga_uara & GENET_MDIO_START_BUSY))
            return tūnga_uara & GENET_MDIO_READ_FAILED ? -1 : (int)(tūnga_uara & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(whaiaho_uara.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned uara) { return 물리전송(whaiaho_uara.물리주소, INDEX, 1, uara); }
static int 물리준비(void) {
    whaiaho_uara.물리주소 = -1;
    for (unsigned ADDRESS = 0; ADDRESS < 32; ADDRESS++) {
        int 식별 = 물리전송(ADDRESS, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { whaiaho_uara.물리주소 = ADDRESS; break; }
    }
    if (whaiaho_uara.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int uara = 물리읽기(BRGPHY_MII_AUXCTL);
    if (uara < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (uara & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    uara = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (uara < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (uara & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Whakarite_Loop(unsigned Papamuri_uara) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_uara = Papamuri_uara + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned tūranga = 0; tūranga <= 0x30; tūranga += 4) 유선저장기(Loop_uara + tūranga) = 0;
    유선저장기(Loop_uara + 0x10) = (Loop_COUNT << 16) | pūreirei_rahi;
    유선저장기(Loop_uara + 0x1c) = Loop_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Papamuri_uara == GENET_RX_BASE) 유선저장기(Loop_uara + 0x28) = (5 << 16) | (Loop_COUNT >> 4);
    else 유선저장기(Loop_uara + 0x24) = 1;
    유선저장기(Papamuri_uara + 0x104c) = 8;
    유선저장기(Papamuri_uara + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned tūranga_INDEX) {
    uintptr_t ADDRESS = (uintptr_t)whaiaho_uara.받기[tūranga_INDEX];
    CLEAN_keteroki((void *)ADDRESS, pūreirei_rahi, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(tūranga_INDEX)) = (uint32_t)ADDRESS;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(tūranga_INDEX)) = (uint64_t)ADDRESS >> 32;
    유선저장기(GENET_RX_DESC_STATUS(tūranga_INDEX)) = pūreirei_rahi << 16;
}
static err_t 전문보내기(struct netif *pūkoro_uara, struct pbuf *전문) {
    if (!whaiaho_uara.Whakarite || !netif_is_link_up(pūkoro_uara)) return ERR_RTE;
    unsigned rahi = 전문->tot_len;
    if (!rahi || rahi > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(whaiaho_uara.생산 - 소비) >= Loop_COUNT - 1) return ERR_MEM;
    unsigned tūranga_INDEX = whaiaho_uara.생산 % Loop_COUNT, 송신길이 = rahi < 60 ? 60 : rahi;
    unsigned char *raraunga = whaiaho_uara.tuku[tūranga_INDEX];
    memset(raraunga, 0, 송신길이);
    if (pbuf_copy_partial(전문, raraunga, rahi, 0) != rahi) return ERR_BUF;
    CLEAN_keteroki(raraunga, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(tūranga_INDEX)) = (uint32_t)(uintptr_t)raraunga;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(tūranga_INDEX)) = (uint64_t)(uintptr_t)raraunga >> 32;
    유선저장기(GENET_TX_DESC_STATUS(tūranga_INDEX)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    tukutahi();
    whaiaho_uara.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = whaiaho_uara.생산;
    whaiaho_uara.집계[2]++; whaiaho_uara.집계[3] += rahi;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Whakarite_whaiaho_whatunga(struct netif *pūkoro_uara) {
    unsigned char ADDRESS[6];
    if (!유선장치있음() || !papa_mīhini_ADDRESS(ADDRESS) || (ADDRESS[0] & 1)) return ERR_IF;
    unsigned SUM_uara = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_uara |= ADDRESS[순번];
    if (!SUM_uara) return ERR_IF;
    memset(&whaiaho_uara, 0, sizeof(whaiaho_uara));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ADDRESS[0] << 24 | (uint32_t)ADDRESS[1] << 16 | ADDRESS[2] << 8 | ADDRESS[3];
    유선저장기(GENET_UMAC_MAC1) = ADDRESS[4] << 8 | ADDRESS[5];
    Whakarite_Loop(GENET_TX_BASE); Whakarite_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COUNT; 순번++) 받는주소(순번);
    tukutahi();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    pūkoro_uara->name[0] = 'e'; pūkoro_uara->name[1] = 'n'; pūkoro_uara->mtu = 1500;
    pūkoro_uara->hwaddr_len = 6; memcpy(pūkoro_uara->hwaddr, ADDRESS, 6);
    pūkoro_uara->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    pūkoro_uara->output = etharp_output; pūkoro_uara->linkoutput = 전문보내기;
    whaiaho_uara.Whakarite = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *pūkoro_uara) {
    if (!whaiaho_uara.Whakarite) return;
    uintptr_t NOW_uara = 보드밀리초();
    if (NOW_uara >= whaiaho_uara.manatoko_Panuku_tuemi) {
        whaiaho_uara.manatoko_Panuku_tuemi = NOW_uara + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int tūnga_uara = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned aratuka_MODE = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = aratuka_MODE == 7 ? 1000 : aratuka_MODE == 5 ? 100 : aratuka_MODE == 2 ? 10 : 0;
        whaiaho_uara.속도 = tūnga_uara >= 0 && (tūnga_uara & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (whaiaho_uara.속도) {
            uint32_t Ngā_Tautuhinga = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Ngā_Tautuhinga &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Ngā_Tautuhinga | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Ngā_Tautuhinga = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Ngā_Tautuhinga | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(pūkoro_uara)) netif_set_link_up(pūkoro_uara);
        } else if (netif_is_link_up(pūkoro_uara)) netif_set_link_down(pūkoro_uara);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - whaiaho_uara.소비);
    if (남음 > Loop_COUNT) { whaiaho_uara.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned tūranga_INDEX = whaiaho_uara.소비 % Loop_COUNT;
        tukutahi();
        uint32_t tūnga_uara = 유선저장기(GENET_RX_DESC_STATUS(tūranga_INDEX));
        unsigned roa_uara = (tūnga_uara & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((tūnga_uara & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || roa_uara < 16 || roa_uara > 1538) whaiaho_uara.집계[4]++;
        else {
            CLEAN_keteroki(whaiaho_uara.받기[tūranga_INDEX], roa_uara, 1);
            struct pbuf *raraunga = pbuf_alloc(PBUF_RAW, roa_uara - 2, PBUF_POOL);
            if (!raraunga) whaiaho_uara.집계[4]++;
            else if (pbuf_take(raraunga, whaiaho_uara.받기[tūranga_INDEX] + 2, roa_uara - 2) != ERR_OK || pūkoro_uara->input(raraunga, pūkoro_uara) != ERR_OK) {
                pbuf_free(raraunga); whaiaho_uara.집계[4]++;
            } else { whaiaho_uara.집계[0]++; whaiaho_uara.집계[1] += roa_uara - 2; }
        }
        받는주소(tūranga_INDEX); tukutahi(); whaiaho_uara.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = whaiaho_uara.소비;
    }
}
uint32_t 유선망집계(unsigned tāurunga_uara) {
    return tāurunga_uara < 5 ? whaiaho_uara.집계[tāurunga_uara] : tāurunga_uara == 5 ? whaiaho_uara.속도 : tāurunga_uara == 6 ? whaiaho_uara.Whakarite : 0;
}
