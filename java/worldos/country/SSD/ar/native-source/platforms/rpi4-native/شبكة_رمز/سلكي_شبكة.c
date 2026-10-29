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
#include "سلكي_شبكة.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int لوحة_عنوان_حقيقي(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(عنوان) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (عنوان)))
#endif
enum { يكرر_رقم = 16, 고리개수 = 256, حجم_المخزن_المؤقت = 2048 };
static struct {
    unsigned char يستلم[고리개수][حجم_المخزن_المؤقت];
    unsigned char يرسل[고리개수][حجم_المخزن_المؤقت];
    uint16_t يستخدم_قيمة_84aa75c8, 생산;
    int 물리주소, إعداد, 속도;
    uint32_t 집계[5];
    uintptr_t يتحقق_التالي_عنصر;
} سلكي_قيمة __attribute__((aligned(64)));

static void تزامن(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void نظيف_يخزن_مؤقتا(void *بيانات, unsigned 길이, int يستلم) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)بيانات + 길이;
    for (uintptr_t عنوان = (uintptr_t)بيانات & ~(uintptr_t)63; عنوان < 끝; عنوان += 64) {
        if (يستلم) __asm__ volatile("dc ivac, %0" :: "r"(عنوان) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(عنوان) : "memory");
    }
#else
    (void)بيانات; (void)길이; (void)يستلم;
#endif
    تزامن();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned عنوان, unsigned فهرس, int كتابة, unsigned قيمة) {
    uint32_t أمر = (كتابة ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (عنوان << GENET_MDIO_ADDR_SHIFT) | (فهرس << GENET_MDIO_REG_SHIFT) | (قيمة & 65535);
    유선저장기(GENET_MDIO_CMD) = أمر;
    유선저장기(GENET_MDIO_CMD) = أمر | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t حالة_قيمة = 유선저장기(GENET_MDIO_CMD);
        if (!(حالة_قيمة & GENET_MDIO_START_BUSY))
            return حالة_قيمة & GENET_MDIO_READ_FAILED ? -1 : (int)(حالة_قيمة & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned فهرس) { return 물리전송(سلكي_قيمة.물리주소, فهرس, 0, 0); }
static int 물리쓰기(unsigned فهرس, unsigned قيمة) { return 물리전송(سلكي_قيمة.물리주소, فهرس, 1, قيمة); }
static int 물리준비(void) {
    سلكي_قيمة.물리주소 = -1;
    for (unsigned عنوان = 0; عنوان < 32; عنوان++) {
        int 식별 = 물리전송(عنوان, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { سلكي_قيمة.물리주소 = عنوان; break; }
    }
    if (سلكي_قيمة.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int قيمة = 물리읽기(BRGPHY_MII_AUXCTL);
    if (قيمة < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (قيمة & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    قيمة = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (قيمة < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (قيمة & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void إعداد_يكرر(unsigned خلفية_قيمة) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned يكرر_قيمة = خلفية_قيمة + 0xc00 + GENET_DMA_RING_SIZE * يكرر_رقم;
    for (unsigned موضع = 0; موضع <= 0x30; موضع += 4) 유선저장기(يكرر_قيمة + موضع) = 0;
    유선저장기(يكرر_قيمة + 0x10) = (고리개수 << 16) | حجم_المخزن_المؤقت;
    유선저장기(يكرر_قيمة + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (خلفية_قيمة == GENET_RX_BASE) 유선저장기(يكرر_قيمة + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(يكرر_قيمة + 0x24) = 1;
    유선저장기(خلفية_قيمة + 0x104c) = 8;
    유선저장기(خلفية_قيمة + 0x1040) = __BIT(يكرر_رقم);
}
static void 받는주소(unsigned منصب_فهرس) {
    uintptr_t عنوان = (uintptr_t)سلكي_قيمة.يستلم[منصب_فهرس];
    نظيف_يخزن_مؤقتا((void *)عنوان, حجم_المخزن_المؤقت, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(منصب_فهرس)) = (uint32_t)عنوان;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(منصب_فهرس)) = (uint64_t)عنوان >> 32;
    유선저장기(GENET_RX_DESC_STATUS(منصب_فهرس)) = حجم_المخزن_المؤقت << 16;
}
static err_t يرسل_مخطط_بيانات(struct netif *جهاز_قيمة, struct pbuf *رزمةمستقلة) {
    if (!سلكي_قيمة.إعداد || !netif_is_link_up(جهاز_قيمة)) return ERR_RTE;
    unsigned حجم = رزمةمستقلة->tot_len;
    if (!حجم || حجم > 1536) return ERR_BUF;
    uint16_t يستخدم_قيمة_84aa75c8 = 유선저장기(GENET_TX_DMA_CONS_INDEX(يكرر_رقم));
    if ((uint16_t)(سلكي_قيمة.생산 - يستخدم_قيمة_84aa75c8) >= 고리개수 - 1) return ERR_MEM;
    unsigned منصب_فهرس = سلكي_قيمة.생산 % 고리개수, 송신길이 = حجم < 60 ? 60 : حجم;
    unsigned char *بيانات = سلكي_قيمة.يرسل[منصب_فهرس];
    memset(بيانات, 0, 송신길이);
    if (pbuf_copy_partial(رزمةمستقلة, بيانات, حجم, 0) != حجم) return ERR_BUF;
    نظيف_يخزن_مؤقتا(بيانات, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(منصب_فهرس)) = (uint32_t)(uintptr_t)بيانات;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(منصب_فهرس)) = (uint64_t)(uintptr_t)بيانات >> 32;
    유선저장기(GENET_TX_DESC_STATUS(منصب_فهرس)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    تزامن();
    سلكي_قيمة.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(يكرر_رقم)) = سلكي_قيمة.생산;
    سلكي_قيمة.집계[2]++; سلكي_قيمة.집계[3] += حجم;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t إعداد_سلكي_شبكة(struct netif *جهاز_قيمة) {
    unsigned char عنوان[6];
    if (!유선장치있음() || !لوحة_عنوان_حقيقي(عنوان) || (عنوان[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= عنوان[순번];
    if (!합) return ERR_IF;
    memset(&سلكي_قيمة, 0, sizeof(سلكي_قيمة));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t حالة_أولية = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = حالة_أولية | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = حالة_أولية & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)عنوان[0] << 24 | (uint32_t)عنوان[1] << 16 | عنوان[2] << 8 | عنوان[3];
    유선저장기(GENET_UMAC_MAC1) = عنوان[4] << 8 | عنوان[5];
    إعداد_يكرر(GENET_TX_BASE); إعداد_يكرر(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    تزامن();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(يكرر_رقم);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(يكرر_رقم);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    جهاز_قيمة->name[0] = 'e'; جهاز_قيمة->name[1] = 'n'; جهاز_قيمة->mtu = 1500;
    جهاز_قيمة->hwaddr_len = 6; memcpy(جهاز_قيمة->hwaddr, عنوان, 6);
    جهاز_قيمة->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    جهاز_قيمة->output = etharp_output; جهاز_قيمة->linkoutput = يرسل_مخطط_بيانات;
    سلكي_قيمة.إعداد = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *جهاز_قيمة) {
    if (!سلكي_قيمة.إعداد) return;
    uintptr_t الآن_قيمة = 보드밀리초();
    if (الآن_قيمة >= سلكي_قيمة.يتحقق_التالي_عنصر) {
        سلكي_قيمة.يتحقق_التالي_عنصر = الآن_قيمة + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int حالة_قيمة = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned أسلوب_الوضع = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = أسلوب_الوضع == 7 ? 1000 : أسلوب_الوضع == 5 ? 100 : أسلوب_الوضع == 2 ? 10 : 0;
        سلكي_قيمة.속도 = حالة_قيمة >= 0 && (حالة_قيمة & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (سلكي_قيمة.속도) {
            uint32_t إعدادات = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            إعدادات &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = إعدادات | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            إعدادات = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = إعدادات | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(جهاز_قيمة)) netif_set_link_up(جهاز_قيمة);
        } else if (netif_is_link_up(جهاز_قيمة)) netif_set_link_down(جهاز_قيمة);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(يكرر_رقم));
    unsigned 남음 = (uint16_t)(생산 - سلكي_قيمة.يستخدم_قيمة_84aa75c8);
    if (남음 > 고리개수) { سلكي_قيمة.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned منصب_فهرس = سلكي_قيمة.يستخدم_قيمة_84aa75c8 % 고리개수;
        تزامن();
        uint32_t حالة_قيمة = 유선저장기(GENET_RX_DESC_STATUS(منصب_فهرس));
        unsigned 길이 = (حالة_قيمة & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((حالة_قيمة & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || 길이 < 16 || 길이 > 1538) سلكي_قيمة.집계[4]++;
        else {
            نظيف_يخزن_مؤقتا(سلكي_قيمة.يستلم[منصب_فهرس], 길이, 1);
            struct pbuf *بيانات = pbuf_alloc(PBUF_RAW, 길이 - 2, PBUF_POOL);
            if (!بيانات) سلكي_قيمة.집계[4]++;
            else if (pbuf_take(بيانات, سلكي_قيمة.يستلم[منصب_فهرس] + 2, 길이 - 2) != ERR_OK || جهاز_قيمة->input(بيانات, جهاز_قيمة) != ERR_OK) {
                pbuf_free(بيانات); سلكي_قيمة.집계[4]++;
            } else { سلكي_قيمة.집계[0]++; سلكي_قيمة.집계[1] += 길이 - 2; }
        }
        받는주소(منصب_فهرس); تزامن(); سلكي_قيمة.يستخدم_قيمة_84aa75c8++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(يكرر_رقم)) = سلكي_قيمة.يستخدم_قيمة_84aa75c8;
    }
}
uint32_t 유선망집계(unsigned إدخال_قيمة_962f286b) {
    return إدخال_قيمة_962f286b < 5 ? سلكي_قيمة.집계[إدخال_قيمة_962f286b] : إدخال_قيمة_962f286b == 5 ? سلكي_قيمة.속도 : إدخال_قيمة_962f286b == 6 ? سلكي_قيمة.إعداد : 0;
}
