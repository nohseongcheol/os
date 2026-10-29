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
#include "kuwekwa_waya_Mtandao.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int 보드기계주소(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(anwani) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (anwani)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, bafa_panga_ukubwa = 2048 };
static struct {
    unsigned char 받기[고리개수][bafa_panga_ukubwa];
    unsigned char tuma[고리개수][bafa_panga_ukubwa];
    uint16_t 소비, 생산;
    int 물리주소, Andaa, 속도;
    uint32_t 집계[5];
    uintptr_t 다음확인;
} kuwekwa_waya_thamani __attribute__((aligned(64)));

static void landanisha(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Safi_hifadhi_muda(void *data, unsigned urefu_thamani, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + urefu_thamani;
    for (uintptr_t anwani = (uintptr_t)data & ~(uintptr_t)63; anwani < 끝; anwani += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(anwani) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(anwani) : "memory");
    }
#else
    (void)data; (void)urefu_thamani; (void)받기;
#endif
    landanisha();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned anwani, unsigned kielezo, int andika, unsigned thamani) {
    uint32_t amri = (andika ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (anwani << GENET_MDIO_ADDR_SHIFT) | (kielezo << GENET_MDIO_REG_SHIFT) | (thamani & 65535);
    유선저장기(GENET_MDIO_CMD) = amri;
    유선저장기(GENET_MDIO_CMD) = amri | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t hali_thamani = 유선저장기(GENET_MDIO_CMD);
        if (!(hali_thamani & GENET_MDIO_START_BUSY))
            return hali_thamani & GENET_MDIO_READ_FAILED ? -1 : (int)(hali_thamani & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned kielezo) { return 물리전송(kuwekwa_waya_thamani.물리주소, kielezo, 0, 0); }
static int 물리쓰기(unsigned kielezo, unsigned thamani) { return 물리전송(kuwekwa_waya_thamani.물리주소, kielezo, 1, thamani); }
static int 물리준비(void) {
    kuwekwa_waya_thamani.물리주소 = -1;
    for (unsigned anwani = 0; anwani < 32; anwani++) {
        int 식별 = 물리전송(anwani, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { kuwekwa_waya_thamani.물리주소 = anwani; break; }
    }
    if (kuwekwa_waya_thamani.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int thamani = 물리읽기(BRGPHY_MII_AUXCTL);
    if (thamani < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (thamani & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    thamani = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (thamani < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (thamani & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Andaa_kitanzi(unsigned nyuma_thamani) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned kitanzi_thamani = nyuma_thamani + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned 위치 = 0; 위치 <= 0x30; 위치 += 4) 유선저장기(kitanzi_thamani + 위치) = 0;
    유선저장기(kitanzi_thamani + 0x10) = (고리개수 << 16) | bafa_panga_ukubwa;
    유선저장기(kitanzi_thamani + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (nyuma_thamani == GENET_RX_BASE) 유선저장기(kitanzi_thamani + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(kitanzi_thamani + 0x24) = 1;
    유선저장기(nyuma_thamani + 0x104c) = 8;
    유선저장기(nyuma_thamani + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned 자리) {
    uintptr_t anwani = (uintptr_t)kuwekwa_waya_thamani.받기[자리];
    Safi_hifadhi_muda((void *)anwani, bafa_panga_ukubwa, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(자리)) = (uint32_t)anwani;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(자리)) = (uint64_t)anwani >> 32;
    유선저장기(GENET_RX_DESC_STATUS(자리)) = bafa_panga_ukubwa << 16;
}
static err_t 전문보내기(struct netif *kifaa_thamani, struct pbuf *전문) {
    if (!kuwekwa_waya_thamani.Andaa || !netif_is_link_up(kifaa_thamani)) return ERR_RTE;
    unsigned panga_ukubwa = 전문->tot_len;
    if (!panga_ukubwa || panga_ukubwa > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(kuwekwa_waya_thamani.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned 자리 = kuwekwa_waya_thamani.생산 % 고리개수, 송신길이 = panga_ukubwa < 60 ? 60 : panga_ukubwa;
    unsigned char *data = kuwekwa_waya_thamani.tuma[자리];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(전문, data, panga_ukubwa, 0) != panga_ukubwa) return ERR_BUF;
    Safi_hifadhi_muda(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(자리)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(자리)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(자리)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    landanisha();
    kuwekwa_waya_thamani.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = kuwekwa_waya_thamani.생산;
    kuwekwa_waya_thamani.집계[2]++; kuwekwa_waya_thamani.집계[3] += panga_ukubwa;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Andaa_kuwekwa_waya_Mtandao(struct netif *kifaa_thamani) {
    unsigned char anwani[6];
    if (!유선장치있음() || !보드기계주소(anwani) || (anwani[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= anwani[순번];
    if (!합) return ERR_IF;
    memset(&kuwekwa_waya_thamani, 0, sizeof(kuwekwa_waya_thamani));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)anwani[0] << 24 | (uint32_t)anwani[1] << 16 | anwani[2] << 8 | anwani[3];
    유선저장기(GENET_UMAC_MAC1) = anwani[4] << 8 | anwani[5];
    Andaa_kitanzi(GENET_TX_BASE); Andaa_kitanzi(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    landanisha();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    kifaa_thamani->name[0] = 'e'; kifaa_thamani->name[1] = 'n'; kifaa_thamani->mtu = 1500;
    kifaa_thamani->hwaddr_len = 6; memcpy(kifaa_thamani->hwaddr, anwani, 6);
    kifaa_thamani->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    kifaa_thamani->output = etharp_output; kifaa_thamani->linkoutput = 전문보내기;
    kuwekwa_waya_thamani.Andaa = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *kifaa_thamani) {
    if (!kuwekwa_waya_thamani.Andaa) return;
    uintptr_t SASA_thamani = 보드밀리초();
    if (SASA_thamani >= kuwekwa_waya_thamani.다음확인) {
        kuwekwa_waya_thamani.다음확인 = SASA_thamani + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int hali_thamani = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned mbinu_hali_tumizi = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = mbinu_hali_tumizi == 7 ? 1000 : mbinu_hali_tumizi == 5 ? 100 : mbinu_hali_tumizi == 2 ? 10 : 0;
        kuwekwa_waya_thamani.속도 = hali_thamani >= 0 && (hali_thamani & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (kuwekwa_waya_thamani.속도) {
            uint32_t Mipangilio = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Mipangilio &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Mipangilio | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Mipangilio = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Mipangilio | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(kifaa_thamani)) netif_set_link_up(kifaa_thamani);
        } else if (netif_is_link_up(kifaa_thamani)) netif_set_link_down(kifaa_thamani);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - kuwekwa_waya_thamani.소비);
    if (남음 > 고리개수) { kuwekwa_waya_thamani.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned 자리 = kuwekwa_waya_thamani.소비 % 고리개수;
        landanisha();
        uint32_t hali_thamani = 유선저장기(GENET_RX_DESC_STATUS(자리));
        unsigned urefu_thamani = (hali_thamani & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((hali_thamani & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || urefu_thamani < 16 || urefu_thamani > 1538) kuwekwa_waya_thamani.집계[4]++;
        else {
            Safi_hifadhi_muda(kuwekwa_waya_thamani.받기[자리], urefu_thamani, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, urefu_thamani - 2, PBUF_POOL);
            if (!data) kuwekwa_waya_thamani.집계[4]++;
            else if (pbuf_take(data, kuwekwa_waya_thamani.받기[자리] + 2, urefu_thamani - 2) != ERR_OK || kifaa_thamani->input(data, kifaa_thamani) != ERR_OK) {
                pbuf_free(data); kuwekwa_waya_thamani.집계[4]++;
            } else { kuwekwa_waya_thamani.집계[0]++; kuwekwa_waya_thamani.집계[1] += urefu_thamani - 2; }
        }
        받는주소(자리); landanisha(); kuwekwa_waya_thamani.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = kuwekwa_waya_thamani.소비;
    }
}
uint32_t 유선망집계(unsigned ingizo_thamani) {
    return ingizo_thamani < 5 ? kuwekwa_waya_thamani.집계[ingizo_thamani] : ingizo_thamani == 5 ? kuwekwa_waya_thamani.속도 : ingizo_thamani == 6 ? kuwekwa_waya_thamani.Andaa : 0;
}
