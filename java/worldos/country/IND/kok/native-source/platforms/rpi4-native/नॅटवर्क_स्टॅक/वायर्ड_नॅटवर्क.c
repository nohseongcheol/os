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
#include "वायर्ड_नॅटवर्क.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int बोर्ड_यंत्र_नामो(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(नामो) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (नामो)))
#endif
enum { 고리번호 = 16, लूप_COUNT = 256, बफर_आवाठ = 2048 };
static struct {
    unsigned char 받기[लूप_COUNT][बफर_आवाठ];
    unsigned char धाडचें[लूप_COUNT][बफर_आवाठ];
    uint16_t 소비, 생산;
    int 물리주소, तयार_करचें_9ce364fc, 속도;
    uint32_t 집계[5];
    uintptr_t पुनर्तपासणी_करची_फुडलें_आयटम;
} वायर्ड_मोल __attribute__((aligned(64)));

static void सिंक्रोनायझ(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void नितळ_कॅश(void *डेटा, unsigned लांबाय_मोल, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)डेटा + लांबाय_मोल;
    for (uintptr_t नामो = (uintptr_t)डेटा & ~(uintptr_t)63; नामो < 끝; नामो += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(नामो) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(नामो) : "memory");
    }
#else
    (void)डेटा; (void)लांबाय_मोल; (void)받기;
#endif
    सिंक्रोनायझ();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned नामो, unsigned INDEX, int बरोवचें, unsigned मोल) {
    uint32_t आदेश = (बरोवचें ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (नामो << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (मोल & 65535);
    유선저장기(GENET_MDIO_CMD) = आदेश;
    유선저장기(GENET_MDIO_CMD) = आदेश | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t स्थिती_मोल_e10195a1 = 유선저장기(GENET_MDIO_CMD);
        if (!(स्थिती_मोल_e10195a1 & GENET_MDIO_START_BUSY))
            return स्थिती_मोल_e10195a1 & GENET_MDIO_READ_FAILED ? -1 : (int)(स्थिती_मोल_e10195a1 & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(वायर्ड_मोल.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned मोल) { return 물리전송(वायर्ड_मोल.물리주소, INDEX, 1, मोल); }
static int 물리준비(void) {
    वायर्ड_मोल.물리주소 = -1;
    for (unsigned नामो = 0; नामो < 32; नामो++) {
        int 식별 = 물리전송(नामो, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { वायर्ड_मोल.물리주소 = नामो; break; }
    }
    if (वायर्ड_मोल.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int मोल = 물리읽기(BRGPHY_MII_AUXCTL);
    if (मोल < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (मोल & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    मोल = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (मोल < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (मोल & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void तयार_करचें_लूप(unsigned फाटभूंय_मोल) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned लूप_मोल = फाटभूंय_मोल + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned स्थिती = 0; स्थिती <= 0x30; स्थिती += 4) 유선저장기(लूप_मोल + स्थिती) = 0;
    유선저장기(लूप_मोल + 0x10) = (लूप_COUNT << 16) | बफर_आवाठ;
    유선저장기(लूप_मोल + 0x1c) = लूप_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (फाटभूंय_मोल == GENET_RX_BASE) 유선저장기(लूप_मोल + 0x28) = (5 << 16) | (लूप_COUNT >> 4);
    else 유선저장기(लूप_मोल + 0x24) = 1;
    유선저장기(फाटभूंय_मोल + 0x104c) = 8;
    유선저장기(फाटभूंय_मोल + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned स्थिती_INDEX) {
    uintptr_t नामो = (uintptr_t)वायर्ड_मोल.받기[स्थिती_INDEX];
    नितळ_कॅश((void *)नामो, बफर_आवाठ, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(स्थिती_INDEX)) = (uint32_t)नामो;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(स्थिती_INDEX)) = (uint64_t)नामो >> 32;
    유선저장기(GENET_RX_DESC_STATUS(स्थिती_INDEX)) = बफर_आवाठ << 16;
}
static err_t 전문보내기(struct netif *मोबायल_मोल, struct pbuf *전문) {
    if (!वायर्ड_मोल.तयार_करचें_9ce364fc || !netif_is_link_up(मोबायल_मोल)) return ERR_RTE;
    unsigned आवाठ = 전문->tot_len;
    if (!आवाठ || आवाठ > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(वायर्ड_मोल.생산 - 소비) >= लूप_COUNT - 1) return ERR_MEM;
    unsigned स्थिती_INDEX = वायर्ड_मोल.생산 % लूप_COUNT, 송신길이 = आवाठ < 60 ? 60 : आवाठ;
    unsigned char *डेटा = वायर्ड_मोल.धाडचें[स्थिती_INDEX];
    memset(डेटा, 0, 송신길이);
    if (pbuf_copy_partial(전문, डेटा, आवाठ, 0) != आवाठ) return ERR_BUF;
    नितळ_कॅश(डेटा, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(स्थिती_INDEX)) = (uint32_t)(uintptr_t)डेटा;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(स्थिती_INDEX)) = (uint64_t)(uintptr_t)डेटा >> 32;
    유선저장기(GENET_TX_DESC_STATUS(स्थिती_INDEX)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    सिंक्रोनायझ();
    वायर्ड_मोल.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = वायर्ड_मोल.생산;
    वायर्ड_मोल.집계[2]++; वायर्ड_मोल.집계[3] += आवाठ;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t तयार_करचें_वायर्ड_नॅटवर्क(struct netif *मोबायल_मोल) {
    unsigned char नामो[6];
    if (!유선장치있음() || !बोर्ड_यंत्र_नामो(नामो) || (नामो[0] & 1)) return ERR_IF;
    unsigned SUM_मोल = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_मोल |= नामो[순번];
    if (!SUM_मोल) return ERR_IF;
    memset(&वायर्ड_मोल, 0, sizeof(वायर्ड_मोल));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)नामो[0] << 24 | (uint32_t)नामो[1] << 16 | नामो[2] << 8 | नामो[3];
    유선저장기(GENET_UMAC_MAC1) = नामो[4] << 8 | नामो[5];
    तयार_करचें_लूप(GENET_TX_BASE); तयार_करचें_लूप(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < लूप_COUNT; 순번++) 받는주소(순번);
    सिंक्रोनायझ();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    मोबायल_मोल->name[0] = 'e'; मोबायल_मोल->name[1] = 'n'; मोबायल_मोल->mtu = 1500;
    मोबायल_मोल->hwaddr_len = 6; memcpy(मोबायल_मोल->hwaddr, नामो, 6);
    मोबायल_मोल->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    मोबायल_मोल->output = etharp_output; मोबायल_मोल->linkoutput = 전문보내기;
    वायर्ड_मोल.तयार_करचें_9ce364fc = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *मोबायल_मोल) {
    if (!वायर्ड_मोल.तयार_करचें_9ce364fc) return;
    uintptr_t NOW_मोल = 보드밀리초();
    if (NOW_मोल >= वायर्ड_मोल.पुनर्तपासणी_करची_फुडलें_आयटम) {
        वायर्ड_मोल.पुनर्तपासणी_करची_फुडलें_आयटम = NOW_मोल + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int स्थिती_मोल_e10195a1 = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned पद्दत_मोड = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = पद्दत_मोड == 7 ? 1000 : पद्दत_मोड == 5 ? 100 : पद्दत_मोड == 2 ? 10 : 0;
        वायर्ड_मोल.속도 = स्थिती_मोल_e10195a1 >= 0 && (स्थिती_मोल_e10195a1 & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (वायर्ड_मोल.속도) {
            uint32_t मांडावळी = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            मांडावळी &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = मांडावळी | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            मांडावळी = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = मांडावळी | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(मोबायल_मोल)) netif_set_link_up(मोबायल_मोल);
        } else if (netif_is_link_up(मोबायल_मोल)) netif_set_link_down(मोबायल_मोल);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - वायर्ड_मोल.소비);
    if (남음 > लूप_COUNT) { वायर्ड_मोल.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned स्थिती_INDEX = वायर्ड_मोल.소비 % लूप_COUNT;
        सिंक्रोनायझ();
        uint32_t स्थिती_मोल_e10195a1 = 유선저장기(GENET_RX_DESC_STATUS(स्थिती_INDEX));
        unsigned लांबाय_मोल = (स्थिती_मोल_e10195a1 & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((स्थिती_मोल_e10195a1 & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || लांबाय_मोल < 16 || लांबाय_मोल > 1538) वायर्ड_मोल.집계[4]++;
        else {
            नितळ_कॅश(वायर्ड_मोल.받기[स्थिती_INDEX], लांबाय_मोल, 1);
            struct pbuf *डेटा = pbuf_alloc(PBUF_RAW, लांबाय_मोल - 2, PBUF_POOL);
            if (!डेटा) वायर्ड_मोल.집계[4]++;
            else if (pbuf_take(डेटा, वायर्ड_मोल.받기[स्थिती_INDEX] + 2, लांबाय_मोल - 2) != ERR_OK || मोबायल_मोल->input(डेटा, मोबायल_मोल) != ERR_OK) {
                pbuf_free(डेटा); वायर्ड_मोल.집계[4]++;
            } else { वायर्ड_मोल.집계[0]++; वायर्ड_मोल.집계[1] += लांबाय_मोल - 2; }
        }
        받는주소(स्थिती_INDEX); सिंक्रोनायझ(); वायर्ड_मोल.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = वायर्ड_मोल.소비;
    }
}
uint32_t 유선망집계(unsigned प्रवेश_मोल) {
    return प्रवेश_मोल < 5 ? वायर्ड_मोल.집계[प्रवेश_मोल] : प्रवेश_मोल == 5 ? वायर्ड_मोल.속도 : प्रवेश_मोल == 6 ? वायर्ड_मोल.तयार_करचें_9ce364fc : 0;
}
