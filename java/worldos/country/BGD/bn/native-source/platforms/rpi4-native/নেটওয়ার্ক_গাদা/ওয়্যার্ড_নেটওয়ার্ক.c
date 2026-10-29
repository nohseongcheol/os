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
#include "ওয়্যার্ড_নেটওয়ার্ক.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int বোর্ড_মেশিন_ইমেইল(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ইমেইল) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ইমেইল)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, বাফার_আয়তন = 2048 };
static struct {
    unsigned char 받기[고리개수][বাফার_আয়তন];
    unsigned char পাঠান[고리개수][বাফার_আয়তন];
    uint16_t 소비, 생산;
    int 물리주소, প্রস্তুত_করুন, 속도;
    uint32_t 집계[5];
    uintptr_t যাচাই_করা_পরবর্তী_দফা;
} ওয়্যার্ড_মান __attribute__((aligned(64)));

static void সমলয়_করা(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void পরিষ্কার_করুন_ক্যাশ(void *ডাটা, unsigned দৈর্ঘ্য_মান, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ডাটা + দৈর্ঘ্য_মান;
    for (uintptr_t ইমেইল = (uintptr_t)ডাটা & ~(uintptr_t)63; ইমেইল < 끝; ইমেইল += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ইমেইল) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ইমেইল) : "memory");
    }
#else
    (void)ডাটা; (void)দৈর্ঘ্য_মান; (void)받기;
#endif
    সমলয়_করা();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ইমেইল, unsigned সূচি, int লেখা, unsigned মান) {
    uint32_t আদেশ = (লেখা ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ইমেইল << GENET_MDIO_ADDR_SHIFT) | (সূচি << GENET_MDIO_REG_SHIFT) | (মান & 65535);
    유선저장기(GENET_MDIO_CMD) = আদেশ;
    유선저장기(GENET_MDIO_CMD) = আদেশ | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t অবস্হা_মান = 유선저장기(GENET_MDIO_CMD);
        if (!(অবস্হা_মান & GENET_MDIO_START_BUSY))
            return অবস্হা_মান & GENET_MDIO_READ_FAILED ? -1 : (int)(অবস্হা_মান & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned সূচি) { return 물리전송(ওয়্যার্ড_মান.물리주소, সূচি, 0, 0); }
static int 물리쓰기(unsigned সূচি, unsigned মান) { return 물리전송(ওয়্যার্ড_মান.물리주소, সূচি, 1, মান); }
static int 물리준비(void) {
    ওয়্যার্ড_মান.물리주소 = -1;
    for (unsigned ইমেইল = 0; ইমেইল < 32; ইমেইল++) {
        int 식별 = 물리전송(ইমেইল, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ওয়্যার্ড_মান.물리주소 = ইমেইল; break; }
    }
    if (ওয়্যার্ড_মান.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int মান = 물리읽기(BRGPHY_MII_AUXCTL);
    if (মান < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (মান & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    মান = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (মান < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (মান & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void প্রস্তুত_করুন_লুপ(unsigned পটভূমি_মান) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned লুপ_মান = পটভূমি_মান + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned অবস্থান = 0; অবস্থান <= 0x30; অবস্থান += 4) 유선저장기(লুপ_মান + অবস্থান) = 0;
    유선저장기(লুপ_মান + 0x10) = (고리개수 << 16) | বাফার_আয়তন;
    유선저장기(লুপ_মান + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (পটভূমি_মান == GENET_RX_BASE) 유선저장기(লুপ_মান + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(লুপ_মান + 0x24) = 1;
    유선저장기(পটভূমি_মান + 0x104c) = 8;
    유선저장기(পটভূমি_মান + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned পদ_সূচি) {
    uintptr_t ইমেইল = (uintptr_t)ওয়্যার্ড_মান.받기[পদ_সূচি];
    পরিষ্কার_করুন_ক্যাশ((void *)ইমেইল, বাফার_আয়তন, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(পদ_সূচি)) = (uint32_t)ইমেইল;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(পদ_সূচি)) = (uint64_t)ইমেইল >> 32;
    유선저장기(GENET_RX_DESC_STATUS(পদ_সূচি)) = বাফার_আয়তন << 16;
}
static err_t 전문보내기(struct netif *ডিভাইস_মান, struct pbuf *전문) {
    if (!ওয়্যার্ড_মান.প্রস্তুত_করুন || !netif_is_link_up(ডিভাইস_মান)) return ERR_RTE;
    unsigned আকার = 전문->tot_len;
    if (!আকার || আকার > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ওয়্যার্ড_মান.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned পদ_সূচি = ওয়্যার্ড_মান.생산 % 고리개수, 송신길이 = আকার < 60 ? 60 : আকার;
    unsigned char *ডাটা = ওয়্যার্ড_মান.পাঠান[পদ_সূচি];
    memset(ডাটা, 0, 송신길이);
    if (pbuf_copy_partial(전문, ডাটা, আকার, 0) != আকার) return ERR_BUF;
    পরিষ্কার_করুন_ক্যাশ(ডাটা, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(পদ_সূচি)) = (uint32_t)(uintptr_t)ডাটা;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(পদ_সূচি)) = (uint64_t)(uintptr_t)ডাটা >> 32;
    유선저장기(GENET_TX_DESC_STATUS(পদ_সূচি)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    সমলয়_করা();
    ওয়্যার্ড_মান.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ওয়্যার্ড_মান.생산;
    ওয়্যার্ড_মান.집계[2]++; ওয়্যার্ড_মান.집계[3] += আকার;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t প্রস্তুত_করুন_ওয়্যার্ড_নেটওয়ার্ক(struct netif *ডিভাইস_মান) {
    unsigned char ইমেইল[6];
    if (!유선장치있음() || !বোর্ড_মেশিন_ইমেইল(ইমেইল) || (ইমেইল[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= ইমেইল[순번];
    if (!합) return ERR_IF;
    memset(&ওয়্যার্ড_মান, 0, sizeof(ওয়্যার্ড_মান));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ইমেইল[0] << 24 | (uint32_t)ইমেইল[1] << 16 | ইমেইল[2] << 8 | ইমেইল[3];
    유선저장기(GENET_UMAC_MAC1) = ইমেইল[4] << 8 | ইমেইল[5];
    প্রস্তুত_করুন_লুপ(GENET_TX_BASE); প্রস্তুত_করুন_লুপ(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    সমলয়_করা();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ডিভাইস_মান->name[0] = 'e'; ডিভাইস_মান->name[1] = 'n'; ডিভাইস_মান->mtu = 1500;
    ডিভাইস_মান->hwaddr_len = 6; memcpy(ডিভাইস_মান->hwaddr, ইমেইল, 6);
    ডিভাইস_মান->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ডিভাইস_মান->output = etharp_output; ডিভাইস_মান->linkoutput = 전문보내기;
    ওয়্যার্ড_মান.প্রস্তুত_করুন = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ডিভাইস_মান) {
    if (!ওয়্যার্ড_মান.প্রস্তুত_করুন) return;
    uintptr_t নাউ_মান = 보드밀리초();
    if (নাউ_মান >= ওয়্যার্ড_মান.যাচাই_করা_পরবর্তী_দফা) {
        ওয়্যার্ড_মান.যাচাই_করা_পরবর্তী_দফা = নাউ_মান + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int অবস্হা_মান = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned পদ্ধতি_মোড = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = পদ্ধতি_মোড == 7 ? 1000 : পদ্ধতি_মোড == 5 ? 100 : পদ্ধতি_মোড == 2 ? 10 : 0;
        ওয়্যার্ড_মান.속도 = অবস্হা_মান >= 0 && (অবস্হা_মান & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ওয়্যার্ড_মান.속도) {
            uint32_t সেটিংস = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            সেটিংস &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = সেটিংস | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            সেটিংস = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = সেটিংস | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ডিভাইস_মান)) netif_set_link_up(ডিভাইস_মান);
        } else if (netif_is_link_up(ডিভাইস_মান)) netif_set_link_down(ডিভাইস_মান);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ওয়্যার্ড_মান.소비);
    if (남음 > 고리개수) { ওয়্যার্ড_মান.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned পদ_সূচি = ওয়্যার্ড_মান.소비 % 고리개수;
        সমলয়_করা();
        uint32_t অবস্হা_মান = 유선저장기(GENET_RX_DESC_STATUS(পদ_সূচি));
        unsigned দৈর্ঘ্য_মান = (অবস্হা_মান & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((অবস্হা_মান & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || দৈর্ঘ্য_মান < 16 || দৈর্ঘ্য_মান > 1538) ওয়্যার্ড_মান.집계[4]++;
        else {
            পরিষ্কার_করুন_ক্যাশ(ওয়্যার্ড_মান.받기[পদ_সূচি], দৈর্ঘ্য_মান, 1);
            struct pbuf *ডাটা = pbuf_alloc(PBUF_RAW, দৈর্ঘ্য_মান - 2, PBUF_POOL);
            if (!ডাটা) ওয়্যার্ড_মান.집계[4]++;
            else if (pbuf_take(ডাটা, ওয়্যার্ড_মান.받기[পদ_সূচি] + 2, দৈর্ঘ্য_মান - 2) != ERR_OK || ডিভাইস_মান->input(ডাটা, ডিভাইস_মান) != ERR_OK) {
                pbuf_free(ডাটা); ওয়্যার্ড_মান.집계[4]++;
            } else { ওয়্যার্ড_মান.집계[0]++; ওয়্যার্ড_মান.집계[1] += দৈর্ঘ্য_মান - 2; }
        }
        받는주소(পদ_সূচি); সমলয়_করা(); ওয়্যার্ড_মান.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ওয়্যার্ড_মান.소비;
    }
}
uint32_t 유선망집계(unsigned ভুক্তি_মান) {
    return ভুক্তি_মান < 5 ? ওয়্যার্ড_মান.집계[ভুক্তি_মান] : ভুক্তি_মান == 5 ? ওয়্যার্ড_মান.속도 : ভুক্তি_মান == 6 ? ওয়্যার্ড_মান.প্রস্তুত_করুন : 0;
}
