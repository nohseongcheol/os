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
#include "bedraad_Netwerk.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int bord_masjien_adres(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(adres) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (adres)))
#endif
enum { 고리번호 = 16, lus_COUNT = 256, buffer_verstel = 2048 };
static struct {
    unsigned char 받기[lus_COUNT][buffer_verstel];
    unsigned char e_pos[lus_COUNT][buffer_verstel];
    uint16_t 소비, 생산;
    int 물리주소, Maak_gereed, 속도;
    uint32_t 집계[5];
    uintptr_t verifieer_Volgende_item;
} bedraad_VALUE __attribute__((aligned(64)));

static void sinc(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_cache(void *data, unsigned lengte_VALUE, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + lengte_VALUE;
    for (uintptr_t adres = (uintptr_t)data & ~(uintptr_t)63; adres < 끝; adres += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(adres) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(adres) : "memory");
    }
#else
    (void)data; (void)lengte_VALUE; (void)받기;
#endif
    sinc();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned adres, unsigned INDEX, int Skryf, unsigned VALUE) {
    uint32_t Opdrag = (Skryf ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (adres << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALUE & 65535);
    유선저장기(GENET_MDIO_CMD) = Opdrag;
    유선저장기(GENET_MDIO_CMD) = Opdrag | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t stand_VALUE = 유선저장기(GENET_MDIO_CMD);
        if (!(stand_VALUE & GENET_MDIO_START_BUSY))
            return stand_VALUE & GENET_MDIO_READ_FAILED ? -1 : (int)(stand_VALUE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(bedraad_VALUE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALUE) { return 물리전송(bedraad_VALUE.물리주소, INDEX, 1, VALUE); }
static int 물리준비(void) {
    bedraad_VALUE.물리주소 = -1;
    for (unsigned adres = 0; adres < 32; adres++) {
        int 식별 = 물리전송(adres, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { bedraad_VALUE.물리주소 = adres; break; }
    }
    if (bedraad_VALUE.물리주소 < 0) return -1;
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
static void Maak_gereed_lus(unsigned muur_VALUE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned lus_VALUE = muur_VALUE + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Posisie = 0; Posisie <= 0x30; Posisie += 4) 유선저장기(lus_VALUE + Posisie) = 0;
    유선저장기(lus_VALUE + 0x10) = (lus_COUNT << 16) | buffer_verstel;
    유선저장기(lus_VALUE + 0x1c) = lus_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (muur_VALUE == GENET_RX_BASE) 유선저장기(lus_VALUE + 0x28) = (5 << 16) | (lus_COUNT >> 4);
    else 유선저장기(lus_VALUE + 0x24) = 1;
    유선저장기(muur_VALUE + 0x104c) = 8;
    유선저장기(muur_VALUE + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned plaas_INDEX) {
    uintptr_t adres = (uintptr_t)bedraad_VALUE.받기[plaas_INDEX];
    CLEAN_cache((void *)adres, buffer_verstel, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(plaas_INDEX)) = (uint32_t)adres;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(plaas_INDEX)) = (uint64_t)adres >> 32;
    유선저장기(GENET_RX_DESC_STATUS(plaas_INDEX)) = buffer_verstel << 16;
}
static err_t 전문보내기(struct netif *mobiel_VALUE, struct pbuf *전문) {
    if (!bedraad_VALUE.Maak_gereed || !netif_is_link_up(mobiel_VALUE)) return ERR_RTE;
    unsigned Grootte = 전문->tot_len;
    if (!Grootte || Grootte > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(bedraad_VALUE.생산 - 소비) >= lus_COUNT - 1) return ERR_MEM;
    unsigned plaas_INDEX = bedraad_VALUE.생산 % lus_COUNT, 송신길이 = Grootte < 60 ? 60 : Grootte;
    unsigned char *data = bedraad_VALUE.e_pos[plaas_INDEX];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(전문, data, Grootte, 0) != Grootte) return ERR_BUF;
    CLEAN_cache(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(plaas_INDEX)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(plaas_INDEX)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(plaas_INDEX)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sinc();
    bedraad_VALUE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = bedraad_VALUE.생산;
    bedraad_VALUE.집계[2]++; bedraad_VALUE.집계[3] += Grootte;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Maak_gereed_bedraad_Netwerk(struct netif *mobiel_VALUE) {
    unsigned char adres[6];
    if (!유선장치있음() || !bord_masjien_adres(adres) || (adres[0] & 1)) return ERR_IF;
    unsigned SUM_VALUE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALUE |= adres[순번];
    if (!SUM_VALUE) return ERR_IF;
    memset(&bedraad_VALUE, 0, sizeof(bedraad_VALUE));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)adres[0] << 24 | (uint32_t)adres[1] << 16 | adres[2] << 8 | adres[3];
    유선저장기(GENET_UMAC_MAC1) = adres[4] << 8 | adres[5];
    Maak_gereed_lus(GENET_TX_BASE); Maak_gereed_lus(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < lus_COUNT; 순번++) 받는주소(순번);
    sinc();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    mobiel_VALUE->name[0] = 'e'; mobiel_VALUE->name[1] = 'n'; mobiel_VALUE->mtu = 1500;
    mobiel_VALUE->hwaddr_len = 6; memcpy(mobiel_VALUE->hwaddr, adres, 6);
    mobiel_VALUE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    mobiel_VALUE->output = etharp_output; mobiel_VALUE->linkoutput = 전문보내기;
    bedraad_VALUE.Maak_gereed = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *mobiel_VALUE) {
    if (!bedraad_VALUE.Maak_gereed) return;
    uintptr_t NOU_VALUE = 보드밀리초();
    if (NOU_VALUE >= bedraad_VALUE.verifieer_Volgende_item) {
        bedraad_VALUE.verifieer_Volgende_item = NOU_VALUE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int stand_VALUE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metode_MODE = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metode_MODE == 7 ? 1000 : metode_MODE == 5 ? 100 : metode_MODE == 2 ? 10 : 0;
        bedraad_VALUE.속도 = stand_VALUE >= 0 && (stand_VALUE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (bedraad_VALUE.속도) {
            uint32_t Instellings = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Instellings &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Instellings | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Instellings = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Instellings | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(mobiel_VALUE)) netif_set_link_up(mobiel_VALUE);
        } else if (netif_is_link_up(mobiel_VALUE)) netif_set_link_down(mobiel_VALUE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - bedraad_VALUE.소비);
    if (남음 > lus_COUNT) { bedraad_VALUE.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned plaas_INDEX = bedraad_VALUE.소비 % lus_COUNT;
        sinc();
        uint32_t stand_VALUE = 유선저장기(GENET_RX_DESC_STATUS(plaas_INDEX));
        unsigned lengte_VALUE = (stand_VALUE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((stand_VALUE & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || lengte_VALUE < 16 || lengte_VALUE > 1538) bedraad_VALUE.집계[4]++;
        else {
            CLEAN_cache(bedraad_VALUE.받기[plaas_INDEX], lengte_VALUE, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, lengte_VALUE - 2, PBUF_POOL);
            if (!data) bedraad_VALUE.집계[4]++;
            else if (pbuf_take(data, bedraad_VALUE.받기[plaas_INDEX] + 2, lengte_VALUE - 2) != ERR_OK || mobiel_VALUE->input(data, mobiel_VALUE) != ERR_OK) {
                pbuf_free(data); bedraad_VALUE.집계[4]++;
            } else { bedraad_VALUE.집계[0]++; bedraad_VALUE.집계[1] += lengte_VALUE - 2; }
        }
        받는주소(plaas_INDEX); sinc(); bedraad_VALUE.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = bedraad_VALUE.소비;
    }
}
uint32_t 유선망집계(unsigned inskrywing_VALUE) {
    return inskrywing_VALUE < 5 ? bedraad_VALUE.집계[inskrywing_VALUE] : inskrywing_VALUE == 5 ? bedraad_VALUE.속도 : inskrywing_VALUE == 6 ? bedraad_VALUE.Maak_gereed : 0;
}
