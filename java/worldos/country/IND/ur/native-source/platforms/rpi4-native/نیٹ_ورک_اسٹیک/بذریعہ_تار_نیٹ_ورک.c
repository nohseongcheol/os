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
#include "بذریعہ_تار_نیٹ_ورک.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int بورڈ_مشین_پتہ(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(پتہ) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (پتہ)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, بفر_سائز_دیں = 2048 };
static struct {
    unsigned char 받기[고리개수][بفر_سائز_دیں];
    unsigned char بھیجیں[고리개수][بفر_سائز_دیں];
    uint16_t 소비, 생산;
    int 물리주소, تیار_کریں, 속도;
    uint32_t 집계[5];
    uintptr_t تصدیق_کریں_اگلا_شے;
} بذریعہ_تار_قدر __attribute__((aligned(64)));

static void ہم_وقت_ساز(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void صاف_کیش(void *کوائف, unsigned لمبا_ئی_قدر, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)کوائف + لمبا_ئی_قدر;
    for (uintptr_t پتہ = (uintptr_t)کوائف & ~(uintptr_t)63; پتہ < 끝; پتہ += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(پتہ) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(پتہ) : "memory");
    }
#else
    (void)کوائف; (void)لمبا_ئی_قدر; (void)받기;
#endif
    ہم_وقت_ساز();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned پتہ, unsigned اشاریہ, int لکھیں, unsigned قدر) {
    uint32_t حکم = (لکھیں ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (پتہ << GENET_MDIO_ADDR_SHIFT) | (اشاریہ << GENET_MDIO_REG_SHIFT) | (قدر & 65535);
    유선저장기(GENET_MDIO_CMD) = حکم;
    유선저장기(GENET_MDIO_CMD) = حکم | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t حالت_قدر = 유선저장기(GENET_MDIO_CMD);
        if (!(حالت_قدر & GENET_MDIO_START_BUSY))
            return حالت_قدر & GENET_MDIO_READ_FAILED ? -1 : (int)(حالت_قدر & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned اشاریہ) { return 물리전송(بذریعہ_تار_قدر.물리주소, اشاریہ, 0, 0); }
static int 물리쓰기(unsigned اشاریہ, unsigned قدر) { return 물리전송(بذریعہ_تار_قدر.물리주소, اشاریہ, 1, قدر); }
static int 물리준비(void) {
    بذریعہ_تار_قدر.물리주소 = -1;
    for (unsigned پتہ = 0; پتہ < 32; پتہ++) {
        int 식별 = 물리전송(پتہ, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { بذریعہ_تار_قدر.물리주소 = پتہ; break; }
    }
    if (بذریعہ_تار_قدر.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int قدر = 물리읽기(BRGPHY_MII_AUXCTL);
    if (قدر < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (قدر & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    قدر = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (قدر < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (قدر & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void تیار_کریں_لوپ(unsigned پس_منظر_قدر) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned لوپ_قدر = پس_منظر_قدر + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned مقام = 0; مقام <= 0x30; مقام += 4) 유선저장기(لوپ_قدر + مقام) = 0;
    유선저장기(لوپ_قدر + 0x10) = (고리개수 << 16) | بفر_سائز_دیں;
    유선저장기(لوپ_قدر + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (پس_منظر_قدر == GENET_RX_BASE) 유선저장기(لوپ_قدر + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(لوپ_قدر + 0x24) = 1;
    유선저장기(پس_منظر_قدر + 0x104c) = 8;
    유선저장기(پس_منظر_قدر + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned پوزیشن_ٹھیک_کریں_اشاریہ) {
    uintptr_t پتہ = (uintptr_t)بذریعہ_تار_قدر.받기[پوزیشن_ٹھیک_کریں_اشاریہ];
    صاف_کیش((void *)پتہ, بفر_سائز_دیں, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(پوزیشن_ٹھیک_کریں_اشاریہ)) = (uint32_t)پتہ;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(پوزیشن_ٹھیک_کریں_اشاریہ)) = (uint64_t)پتہ >> 32;
    유선저장기(GENET_RX_DESC_STATUS(پوزیشن_ٹھیک_کریں_اشاریہ)) = بفر_سائز_دیں << 16;
}
static err_t 전문보내기(struct netif *آلہ_قدر, struct pbuf *전문) {
    if (!بذریعہ_تار_قدر.تیار_کریں || !netif_is_link_up(آلہ_قدر)) return ERR_RTE;
    unsigned حجم = 전문->tot_len;
    if (!حجم || حجم > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(بذریعہ_تار_قدر.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned پوزیشن_ٹھیک_کریں_اشاریہ = بذریعہ_تار_قدر.생산 % 고리개수, 송신길이 = حجم < 60 ? 60 : حجم;
    unsigned char *کوائف = بذریعہ_تار_قدر.بھیجیں[پوزیشن_ٹھیک_کریں_اشاریہ];
    memset(کوائف, 0, 송신길이);
    if (pbuf_copy_partial(전문, کوائف, حجم, 0) != حجم) return ERR_BUF;
    صاف_کیش(کوائف, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(پوزیشن_ٹھیک_کریں_اشاریہ)) = (uint32_t)(uintptr_t)کوائف;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(پوزیشن_ٹھیک_کریں_اشاریہ)) = (uint64_t)(uintptr_t)کوائف >> 32;
    유선저장기(GENET_TX_DESC_STATUS(پوزیشن_ٹھیک_کریں_اشاریہ)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    ہم_وقت_ساز();
    بذریعہ_تار_قدر.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = بذریعہ_تار_قدر.생산;
    بذریعہ_تار_قدر.집계[2]++; بذریعہ_تار_قدر.집계[3] += حجم;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t تیار_کریں_بذریعہ_تار_نیٹ_ورک(struct netif *آلہ_قدر) {
    unsigned char پتہ[6];
    if (!유선장치있음() || !بورڈ_مشین_پتہ(پتہ) || (پتہ[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= پتہ[순번];
    if (!합) return ERR_IF;
    memset(&بذریعہ_تار_قدر, 0, sizeof(بذریعہ_تار_قدر));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)پتہ[0] << 24 | (uint32_t)پتہ[1] << 16 | پتہ[2] << 8 | پتہ[3];
    유선저장기(GENET_UMAC_MAC1) = پتہ[4] << 8 | پتہ[5];
    تیار_کریں_لوپ(GENET_TX_BASE); تیار_کریں_لوپ(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    ہم_وقت_ساز();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    آلہ_قدر->name[0] = 'e'; آلہ_قدر->name[1] = 'n'; آلہ_قدر->mtu = 1500;
    آلہ_قدر->hwaddr_len = 6; memcpy(آلہ_قدر->hwaddr, پتہ, 6);
    آلہ_قدر->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    آلہ_قدر->output = etharp_output; آلہ_قدر->linkoutput = 전문보내기;
    بذریعہ_تار_قدر.تیار_کریں = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *آلہ_قدر) {
    if (!بذریعہ_تار_قدر.تیار_کریں) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= بذریعہ_تار_قدر.تصدیق_کریں_اگلا_شے) {
        بذریعہ_تار_قدر.تصدیق_کریں_اگلا_شے = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int حالت_قدر = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned طریقہ_موڈ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = طریقہ_موڈ == 7 ? 1000 : طریقہ_موڈ == 5 ? 100 : طریقہ_موڈ == 2 ? 10 : 0;
        بذریعہ_تار_قدر.속도 = حالت_قدر >= 0 && (حالت_قدر & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (بذریعہ_تار_قدر.속도) {
            uint32_t ترتیبات = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            ترتیبات &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = ترتیبات | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ترتیبات = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = ترتیبات | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(آلہ_قدر)) netif_set_link_up(آلہ_قدر);
        } else if (netif_is_link_up(آلہ_قدر)) netif_set_link_down(آلہ_قدر);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - بذریعہ_تار_قدر.소비);
    if (남음 > 고리개수) { بذریعہ_تار_قدر.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned پوزیشن_ٹھیک_کریں_اشاریہ = بذریعہ_تار_قدر.소비 % 고리개수;
        ہم_وقت_ساز();
        uint32_t حالت_قدر = 유선저장기(GENET_RX_DESC_STATUS(پوزیشن_ٹھیک_کریں_اشاریہ));
        unsigned لمبا_ئی_قدر = (حالت_قدر & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((حالت_قدر & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || لمبا_ئی_قدر < 16 || لمبا_ئی_قدر > 1538) بذریعہ_تار_قدر.집계[4]++;
        else {
            صاف_کیش(بذریعہ_تار_قدر.받기[پوزیشن_ٹھیک_کریں_اشاریہ], لمبا_ئی_قدر, 1);
            struct pbuf *کوائف = pbuf_alloc(PBUF_RAW, لمبا_ئی_قدر - 2, PBUF_POOL);
            if (!کوائف) بذریعہ_تار_قدر.집계[4]++;
            else if (pbuf_take(کوائف, بذریعہ_تار_قدر.받기[پوزیشن_ٹھیک_کریں_اشاریہ] + 2, لمبا_ئی_قدر - 2) != ERR_OK || آلہ_قدر->input(کوائف, آلہ_قدر) != ERR_OK) {
                pbuf_free(کوائف); بذریعہ_تار_قدر.집계[4]++;
            } else { بذریعہ_تار_قدر.집계[0]++; بذریعہ_تار_قدر.집계[1] += لمبا_ئی_قدر - 2; }
        }
        받는주소(پوزیشن_ٹھیک_کریں_اشاریہ); ہم_وقت_ساز(); بذریعہ_تار_قدر.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = بذریعہ_تار_قدر.소비;
    }
}
uint32_t 유선망집계(unsigned اندراج_قدر) {
    return اندراج_قدر < 5 ? بذریعہ_تار_قدر.집계[اندراج_قدر] : اندراج_قدر == 5 ? بذریعہ_تار_قدر.속도 : اندراج_قدر == 6 ? بذریعہ_تار_قدر.تیار_کریں : 0;
}
