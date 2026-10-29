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
#include "laidinis_tinklas.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Lenta_absoliutusis_adresas(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ADDRESS) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ADDRESS)))
#endif
enum { Loop_numeris = 16, Loop_COUNT = 256, buferio_dydis = 2048 };
static struct {
    unsigned char gauti[Loop_COUNT][buferio_dydis];
    unsigned char siųsti[Loop_COUNT][buferio_dydis];
    uint16_t vartoti_VALUE, 생산;
    int 물리주소, Parengti, 속도;
    uint32_t 집계[5];
    uintptr_t patvirtinti_toliau_prekė;
} laidinis_VALUE __attribute__((aligned(64)));

static void sinchronizuoti(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_podėlis(void *duomenys, unsigned 길이, int gauti) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)duomenys + 길이;
    for (uintptr_t ADDRESS = (uintptr_t)duomenys & ~(uintptr_t)63; ADDRESS < 끝; ADDRESS += 64) {
        if (gauti) __asm__ volatile("dc ivac, %0" :: "r"(ADDRESS) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ADDRESS) : "memory");
    }
#else
    (void)duomenys; (void)길이; (void)gauti;
#endif
    sinchronizuoti();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ADDRESS, unsigned INDEX, int Rašymas, unsigned VALUE) {
    uint32_t Komanda = (Rašymas ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ADDRESS << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALUE & 65535);
    유선저장기(GENET_MDIO_CMD) = Komanda;
    유선저장기(GENET_MDIO_CMD) = Komanda | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Būsena_VALUE = 유선저장기(GENET_MDIO_CMD);
        if (!(Būsena_VALUE & GENET_MDIO_START_BUSY))
            return Būsena_VALUE & GENET_MDIO_READ_FAILED ? -1 : (int)(Būsena_VALUE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(laidinis_VALUE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALUE) { return 물리전송(laidinis_VALUE.물리주소, INDEX, 1, VALUE); }
static int 물리준비(void) {
    laidinis_VALUE.물리주소 = -1;
    for (unsigned ADDRESS = 0; ADDRESS < 32; ADDRESS++) {
        int 식별 = 물리전송(ADDRESS, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { laidinis_VALUE.물리주소 = ADDRESS; break; }
    }
    if (laidinis_VALUE.물리주소 < 0) return -1;
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
static void Parengti_Loop(unsigned Fonas_VALUE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALUE = Fonas_VALUE + 0xc00 + GENET_DMA_RING_SIZE * Loop_numeris;
    for (unsigned Pozicija = 0; Pozicija <= 0x30; Pozicija += 4) 유선저장기(Loop_VALUE + Pozicija) = 0;
    유선저장기(Loop_VALUE + 0x10) = (Loop_COUNT << 16) | buferio_dydis;
    유선저장기(Loop_VALUE + 0x1c) = Loop_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Fonas_VALUE == GENET_RX_BASE) 유선저장기(Loop_VALUE + 0x28) = (5 << 16) | (Loop_COUNT >> 4);
    else 유선저장기(Loop_VALUE + 0x24) = 1;
    유선저장기(Fonas_VALUE + 0x104c) = 8;
    유선저장기(Fonas_VALUE + 0x1040) = __BIT(Loop_numeris);
}
static void 받는주소(unsigned vietos_rodyklė) {
    uintptr_t ADDRESS = (uintptr_t)laidinis_VALUE.gauti[vietos_rodyklė];
    CLEAN_podėlis((void *)ADDRESS, buferio_dydis, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(vietos_rodyklė)) = (uint32_t)ADDRESS;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(vietos_rodyklė)) = (uint64_t)ADDRESS >> 32;
    유선저장기(GENET_RX_DESC_STATUS(vietos_rodyklė)) = buferio_dydis << 16;
}
static err_t siųsti_paketų_kelio_schema(struct netif *įrenginys_VALUE, struct pbuf *paketų_kelio_schema) {
    if (!laidinis_VALUE.Parengti || !netif_is_link_up(įrenginys_VALUE)) return ERR_RTE;
    unsigned Dydis = paketų_kelio_schema->tot_len;
    if (!Dydis || Dydis > 1536) return ERR_BUF;
    uint16_t vartoti_VALUE = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_numeris));
    if ((uint16_t)(laidinis_VALUE.생산 - vartoti_VALUE) >= Loop_COUNT - 1) return ERR_MEM;
    unsigned vietos_rodyklė = laidinis_VALUE.생산 % Loop_COUNT, 송신길이 = Dydis < 60 ? 60 : Dydis;
    unsigned char *duomenys = laidinis_VALUE.siųsti[vietos_rodyklė];
    memset(duomenys, 0, 송신길이);
    if (pbuf_copy_partial(paketų_kelio_schema, duomenys, Dydis, 0) != Dydis) return ERR_BUF;
    CLEAN_podėlis(duomenys, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(vietos_rodyklė)) = (uint32_t)(uintptr_t)duomenys;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(vietos_rodyklė)) = (uint64_t)(uintptr_t)duomenys >> 32;
    유선저장기(GENET_TX_DESC_STATUS(vietos_rodyklė)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sinchronizuoti();
    laidinis_VALUE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_numeris)) = laidinis_VALUE.생산;
    laidinis_VALUE.집계[2]++; laidinis_VALUE.집계[3] += Dydis;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Parengti_laidinis_tinklas(struct netif *įrenginys_VALUE) {
    unsigned char ADDRESS[6];
    if (!유선장치있음() || !Lenta_absoliutusis_adresas(ADDRESS) || (ADDRESS[0] & 1)) return ERR_IF;
    unsigned SUM_VALUE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALUE |= ADDRESS[순번];
    if (!SUM_VALUE) return ERR_IF;
    memset(&laidinis_VALUE, 0, sizeof(laidinis_VALUE));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t pradinė_būsena = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = pradinė_būsena | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = pradinė_būsena & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
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
    Parengti_Loop(GENET_TX_BASE); Parengti_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COUNT; 순번++) 받는주소(순번);
    sinchronizuoti();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_numeris);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_numeris);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    įrenginys_VALUE->name[0] = 'e'; įrenginys_VALUE->name[1] = 'n'; įrenginys_VALUE->mtu = 1500;
    įrenginys_VALUE->hwaddr_len = 6; memcpy(įrenginys_VALUE->hwaddr, ADDRESS, 6);
    įrenginys_VALUE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    įrenginys_VALUE->output = etharp_output; įrenginys_VALUE->linkoutput = siųsti_paketų_kelio_schema;
    laidinis_VALUE.Parengti = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *įrenginys_VALUE) {
    if (!laidinis_VALUE.Parengti) return;
    uintptr_t NOW_VALUE = 보드밀리초();
    if (NOW_VALUE >= laidinis_VALUE.patvirtinti_toliau_prekė) {
        laidinis_VALUE.patvirtinti_toliau_prekė = NOW_VALUE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Būsena_VALUE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metodas_MODE = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metodas_MODE == 7 ? 1000 : metodas_MODE == 5 ? 100 : metodas_MODE == 2 ? 10 : 0;
        laidinis_VALUE.속도 = Būsena_VALUE >= 0 && (Būsena_VALUE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (laidinis_VALUE.속도) {
            uint32_t Nustatymai = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Nustatymai &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Nustatymai | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Nustatymai = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Nustatymai | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(įrenginys_VALUE)) netif_set_link_up(įrenginys_VALUE);
        } else if (netif_is_link_up(įrenginys_VALUE)) netif_set_link_down(įrenginys_VALUE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_numeris));
    unsigned 남음 = (uint16_t)(생산 - laidinis_VALUE.vartoti_VALUE);
    if (남음 > Loop_COUNT) { laidinis_VALUE.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned vietos_rodyklė = laidinis_VALUE.vartoti_VALUE % Loop_COUNT;
        sinchronizuoti();
        uint32_t Būsena_VALUE = 유선저장기(GENET_RX_DESC_STATUS(vietos_rodyklė));
        unsigned 길이 = (Būsena_VALUE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Būsena_VALUE & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || 길이 < 16 || 길이 > 1538) laidinis_VALUE.집계[4]++;
        else {
            CLEAN_podėlis(laidinis_VALUE.gauti[vietos_rodyklė], 길이, 1);
            struct pbuf *duomenys = pbuf_alloc(PBUF_RAW, 길이 - 2, PBUF_POOL);
            if (!duomenys) laidinis_VALUE.집계[4]++;
            else if (pbuf_take(duomenys, laidinis_VALUE.gauti[vietos_rodyklė] + 2, 길이 - 2) != ERR_OK || įrenginys_VALUE->input(duomenys, įrenginys_VALUE) != ERR_OK) {
                pbuf_free(duomenys); laidinis_VALUE.집계[4]++;
            } else { laidinis_VALUE.집계[0]++; laidinis_VALUE.집계[1] += 길이 - 2; }
        }
        받는주소(vietos_rodyklė); sinchronizuoti(); laidinis_VALUE.vartoti_VALUE++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_numeris)) = laidinis_VALUE.vartoti_VALUE;
    }
}
uint32_t 유선망집계(unsigned įrašas_VALUE) {
    return įrašas_VALUE < 5 ? laidinis_VALUE.집계[įrašas_VALUE] : įrašas_VALUE == 5 ? laidinis_VALUE.속도 : įrašas_VALUE == 6 ? laidinis_VALUE.Parengti : 0;
}
