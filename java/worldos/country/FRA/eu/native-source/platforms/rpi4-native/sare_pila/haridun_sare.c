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
#include "haridun_sare.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int arbel_gailu_helbide(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(helbide) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (helbide)))
#endif
enum { 고리번호 = 16, Loop_ZENBATU = 256, 완충크기 = 2048 };
static struct {
    unsigned char 받기[Loop_ZENBATU][완충크기];
    unsigned char bidali[Loop_ZENBATU][완충크기];
    uint16_t 소비, 생산;
    int 물리주소, 준비, 속도;
    uint32_t 집계[5];
    uintptr_t egiaztatu_Hurrengoa_elementu;
} haridun_balio __attribute__((aligned(64)));

static void sinkronizatu(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void GARBITU_cache(void *datuak, unsigned luzera_balio, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)datuak + luzera_balio;
    for (uintptr_t helbide = (uintptr_t)datuak & ~(uintptr_t)63; helbide < 끝; helbide += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(helbide) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(helbide) : "memory");
    }
#else
    (void)datuak; (void)luzera_balio; (void)받기;
#endif
    sinkronizatu();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned helbide, unsigned INDIZE, int Idatzi, unsigned balio) {
    uint32_t Komandoa = (Idatzi ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (helbide << GENET_MDIO_ADDR_SHIFT) | (INDIZE << GENET_MDIO_REG_SHIFT) | (balio & 65535);
    유선저장기(GENET_MDIO_CMD) = Komandoa;
    유선저장기(GENET_MDIO_CMD) = Komandoa | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Egoera_balio = 유선저장기(GENET_MDIO_CMD);
        if (!(Egoera_balio & GENET_MDIO_START_BUSY))
            return Egoera_balio & GENET_MDIO_READ_FAILED ? -1 : (int)(Egoera_balio & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDIZE) { return 물리전송(haridun_balio.물리주소, INDIZE, 0, 0); }
static int 물리쓰기(unsigned INDIZE, unsigned balio) { return 물리전송(haridun_balio.물리주소, INDIZE, 1, balio); }
static int 물리준비(void) {
    haridun_balio.물리주소 = -1;
    for (unsigned helbide = 0; helbide < 32; helbide++) {
        int 식별 = 물리전송(helbide, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { haridun_balio.물리주소 = helbide; break; }
    }
    if (haridun_balio.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int balio = 물리읽기(BRGPHY_MII_AUXCTL);
    if (balio < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (balio & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    balio = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (balio < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (balio & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void 고리준비(unsigned horma_paper_balio) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_balio = horma_paper_balio + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Posizioa = 0; Posizioa <= 0x30; Posizioa += 4) 유선저장기(Loop_balio + Posizioa) = 0;
    유선저장기(Loop_balio + 0x10) = (Loop_ZENBATU << 16) | 완충크기;
    유선저장기(Loop_balio + 0x1c) = Loop_ZENBATU * GENET_DMA_DESC_SIZE / 4 - 1;
    if (horma_paper_balio == GENET_RX_BASE) 유선저장기(Loop_balio + 0x28) = (5 << 16) | (Loop_ZENBATU >> 4);
    else 유선저장기(Loop_balio + 0x24) = 1;
    유선저장기(horma_paper_balio + 0x104c) = 8;
    유선저장기(horma_paper_balio + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned kargu_INDIZE) {
    uintptr_t helbide = (uintptr_t)haridun_balio.받기[kargu_INDIZE];
    GARBITU_cache((void *)helbide, 완충크기, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(kargu_INDIZE)) = (uint32_t)helbide;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(kargu_INDIZE)) = (uint64_t)helbide >> 32;
    유선저장기(GENET_RX_DESC_STATUS(kargu_INDIZE)) = 완충크기 << 16;
}
static err_t 전문보내기(struct netif *gailu_balio, struct pbuf *전문) {
    if (!haridun_balio.준비 || !netif_is_link_up(gailu_balio)) return ERR_RTE;
    unsigned Tamaina = 전문->tot_len;
    if (!Tamaina || Tamaina > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(haridun_balio.생산 - 소비) >= Loop_ZENBATU - 1) return ERR_MEM;
    unsigned kargu_INDIZE = haridun_balio.생산 % Loop_ZENBATU, 송신길이 = Tamaina < 60 ? 60 : Tamaina;
    unsigned char *datuak = haridun_balio.bidali[kargu_INDIZE];
    memset(datuak, 0, 송신길이);
    if (pbuf_copy_partial(전문, datuak, Tamaina, 0) != Tamaina) return ERR_BUF;
    GARBITU_cache(datuak, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(kargu_INDIZE)) = (uint32_t)(uintptr_t)datuak;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(kargu_INDIZE)) = (uint64_t)(uintptr_t)datuak >> 32;
    유선저장기(GENET_TX_DESC_STATUS(kargu_INDIZE)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sinkronizatu();
    haridun_balio.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = haridun_balio.생산;
    haridun_balio.집계[2]++; haridun_balio.집계[3] += Tamaina;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t 유선망준비(struct netif *gailu_balio) {
    unsigned char helbide[6];
    if (!유선장치있음() || !arbel_gailu_helbide(helbide) || (helbide[0] & 1)) return ERR_IF;
    unsigned BATU_balio = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) BATU_balio |= helbide[순번];
    if (!BATU_balio) return ERR_IF;
    memset(&haridun_balio, 0, sizeof(haridun_balio));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)helbide[0] << 24 | (uint32_t)helbide[1] << 16 | helbide[2] << 8 | helbide[3];
    유선저장기(GENET_UMAC_MAC1) = helbide[4] << 8 | helbide[5];
    고리준비(GENET_TX_BASE); 고리준비(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_ZENBATU; 순번++) 받는주소(순번);
    sinkronizatu();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    gailu_balio->name[0] = 'e'; gailu_balio->name[1] = 'n'; gailu_balio->mtu = 1500;
    gailu_balio->hwaddr_len = 6; memcpy(gailu_balio->hwaddr, helbide, 6);
    gailu_balio->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    gailu_balio->output = etharp_output; gailu_balio->linkoutput = 전문보내기;
    haridun_balio.준비 = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *gailu_balio) {
    if (!haridun_balio.준비) return;
    uintptr_t ORAIN_balio = 보드밀리초();
    if (ORAIN_balio >= haridun_balio.egiaztatu_Hurrengoa_elementu) {
        haridun_balio.egiaztatu_Hurrengoa_elementu = ORAIN_balio + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Egoera_balio = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned 방식 = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = 방식 == 7 ? 1000 : 방식 == 5 ? 100 : 방식 == 2 ? 10 : 0;
        haridun_balio.속도 = Egoera_balio >= 0 && (Egoera_balio & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (haridun_balio.속도) {
            uint32_t Ezarpenak = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Ezarpenak &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Ezarpenak | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Ezarpenak = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Ezarpenak | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(gailu_balio)) netif_set_link_up(gailu_balio);
        } else if (netif_is_link_up(gailu_balio)) netif_set_link_down(gailu_balio);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - haridun_balio.소비);
    if (남음 > Loop_ZENBATU) { haridun_balio.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned kargu_INDIZE = haridun_balio.소비 % Loop_ZENBATU;
        sinkronizatu();
        uint32_t Egoera_balio = 유선저장기(GENET_RX_DESC_STATUS(kargu_INDIZE));
        unsigned luzera_balio = (Egoera_balio & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Egoera_balio & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || luzera_balio < 16 || luzera_balio > 1538) haridun_balio.집계[4]++;
        else {
            GARBITU_cache(haridun_balio.받기[kargu_INDIZE], luzera_balio, 1);
            struct pbuf *datuak = pbuf_alloc(PBUF_RAW, luzera_balio - 2, PBUF_POOL);
            if (!datuak) haridun_balio.집계[4]++;
            else if (pbuf_take(datuak, haridun_balio.받기[kargu_INDIZE] + 2, luzera_balio - 2) != ERR_OK || gailu_balio->input(datuak, gailu_balio) != ERR_OK) {
                pbuf_free(datuak); haridun_balio.집계[4]++;
            } else { haridun_balio.집계[0]++; haridun_balio.집계[1] += luzera_balio - 2; }
        }
        받는주소(kargu_INDIZE); sinkronizatu(); haridun_balio.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = haridun_balio.소비;
    }
}
uint32_t 유선망집계(unsigned sarrera_balio) {
    return sarrera_balio < 5 ? haridun_balio.집계[sarrera_balio] : sarrera_balio == 5 ? haridun_balio.속도 : sarrera_balio == 6 ? haridun_balio.준비 : 0;
}
