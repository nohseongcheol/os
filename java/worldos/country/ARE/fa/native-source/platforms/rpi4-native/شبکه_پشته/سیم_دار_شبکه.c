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
#include "سیم_دار_شبکه.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int تخته_ای_دستگاه_آدرس(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(آدرس) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (آدرس)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, حافظه_میانی_اندازه_کردن = 2048 };
static struct {
    unsigned char 받기[고리개수][حافظه_میانی_اندازه_کردن];
    unsigned char ارسال[고리개수][حافظه_میانی_اندازه_کردن];
    uint16_t 소비, 생산;
    int 물리주소, آماده_کردن, 속도;
    uint32_t 집계[5];
    uintptr_t تأیید_صحت_بعدی_مورد;
} سیم_دار_مقدار __attribute__((aligned(64)));

static void همگام_سازی(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void تمیز_حافظه_پنهان(void *داده_ها, unsigned طول_مقدار, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)داده_ها + طول_مقدار;
    for (uintptr_t آدرس = (uintptr_t)داده_ها & ~(uintptr_t)63; آدرس < 끝; آدرس += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(آدرس) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(آدرس) : "memory");
    }
#else
    (void)داده_ها; (void)طول_مقدار; (void)받기;
#endif
    همگام_سازی();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned آدرس, unsigned فهرست, int نوشتن, unsigned مقدار) {
    uint32_t فرمان = (نوشتن ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (آدرس << GENET_MDIO_ADDR_SHIFT) | (فهرست << GENET_MDIO_REG_SHIFT) | (مقدار & 65535);
    유선저장기(GENET_MDIO_CMD) = فرمان;
    유선저장기(GENET_MDIO_CMD) = فرمان | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t وضعیت_مقدار = 유선저장기(GENET_MDIO_CMD);
        if (!(وضعیت_مقدار & GENET_MDIO_START_BUSY))
            return وضعیت_مقدار & GENET_MDIO_READ_FAILED ? -1 : (int)(وضعیت_مقدار & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned فهرست) { return 물리전송(سیم_دار_مقدار.물리주소, فهرست, 0, 0); }
static int 물리쓰기(unsigned فهرست, unsigned مقدار) { return 물리전송(سیم_دار_مقدار.물리주소, فهرست, 1, مقدار); }
static int 물리준비(void) {
    سیم_دار_مقدار.물리주소 = -1;
    for (unsigned آدرس = 0; آدرس < 32; آدرس++) {
        int 식별 = 물리전송(آدرس, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { سیم_دار_مقدار.물리주소 = آدرس; break; }
    }
    if (سیم_دار_مقدار.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int مقدار = 물리읽기(BRGPHY_MII_AUXCTL);
    if (مقدار < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (مقدار & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    مقدار = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (مقدار < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (مقدار & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void آماده_کردن_حلقه(unsigned زمینه_مقدار_0764f371) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned حلقه_مقدار = زمینه_مقدار_0764f371 + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned مرتب_کردن = 0; مرتب_کردن <= 0x30; مرتب_کردن += 4) 유선저장기(حلقه_مقدار + مرتب_کردن) = 0;
    유선저장기(حلقه_مقدار + 0x10) = (고리개수 << 16) | حافظه_میانی_اندازه_کردن;
    유선저장기(حلقه_مقدار + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (زمینه_مقدار_0764f371 == GENET_RX_BASE) 유선저장기(حلقه_مقدار + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(حلقه_مقدار + 0x24) = 1;
    유선저장기(زمینه_مقدار_0764f371 + 0x104c) = 8;
    유선저장기(زمینه_مقدار_0764f371 + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned مرتب_کردن_فهرست) {
    uintptr_t آدرس = (uintptr_t)سیم_دار_مقدار.받기[مرتب_کردن_فهرست];
    تمیز_حافظه_پنهان((void *)آدرس, حافظه_میانی_اندازه_کردن, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(مرتب_کردن_فهرست)) = (uint32_t)آدرس;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(مرتب_کردن_فهرست)) = (uint64_t)آدرس >> 32;
    유선저장기(GENET_RX_DESC_STATUS(مرتب_کردن_فهرست)) = حافظه_میانی_اندازه_کردن << 16;
}
static err_t 전문보내기(struct netif *دستگاه_مقدار, struct pbuf *전문) {
    if (!سیم_دار_مقدار.آماده_کردن || !netif_is_link_up(دستگاه_مقدار)) return ERR_RTE;
    unsigned اندازه = 전문->tot_len;
    if (!اندازه || اندازه > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(سیم_دار_مقدار.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned مرتب_کردن_فهرست = سیم_دار_مقدار.생산 % 고리개수, 송신길이 = اندازه < 60 ? 60 : اندازه;
    unsigned char *داده_ها = سیم_دار_مقدار.ارسال[مرتب_کردن_فهرست];
    memset(داده_ها, 0, 송신길이);
    if (pbuf_copy_partial(전문, داده_ها, اندازه, 0) != اندازه) return ERR_BUF;
    تمیز_حافظه_پنهان(داده_ها, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(مرتب_کردن_فهرست)) = (uint32_t)(uintptr_t)داده_ها;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(مرتب_کردن_فهرست)) = (uint64_t)(uintptr_t)داده_ها >> 32;
    유선저장기(GENET_TX_DESC_STATUS(مرتب_کردن_فهرست)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    همگام_سازی();
    سیم_دار_مقدار.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = سیم_دار_مقدار.생산;
    سیم_دار_مقدار.집계[2]++; سیم_دار_مقدار.집계[3] += اندازه;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t آماده_کردن_سیم_دار_شبکه(struct netif *دستگاه_مقدار) {
    unsigned char آدرس[6];
    if (!유선장치있음() || !تخته_ای_دستگاه_آدرس(آدرس) || (آدرس[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= آدرس[순번];
    if (!합) return ERR_IF;
    memset(&سیم_دار_مقدار, 0, sizeof(سیم_دار_مقدار));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)آدرس[0] << 24 | (uint32_t)آدرس[1] << 16 | آدرس[2] << 8 | آدرس[3];
    유선저장기(GENET_UMAC_MAC1) = آدرس[4] << 8 | آدرس[5];
    آماده_کردن_حلقه(GENET_TX_BASE); آماده_کردن_حلقه(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    همگام_سازی();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    دستگاه_مقدار->name[0] = 'e'; دستگاه_مقدار->name[1] = 'n'; دستگاه_مقدار->mtu = 1500;
    دستگاه_مقدار->hwaddr_len = 6; memcpy(دستگاه_مقدار->hwaddr, آدرس, 6);
    دستگاه_مقدار->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    دستگاه_مقدار->output = etharp_output; دستگاه_مقدار->linkoutput = 전문보내기;
    سیم_دار_مقدار.آماده_کردن = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *دستگاه_مقدار) {
    if (!سیم_دار_مقدار.آماده_کردن) return;
    uintptr_t هم_اکنون_مقدار = 보드밀리초();
    if (هم_اکنون_مقدار >= سیم_دار_مقدار.تأیید_صحت_بعدی_مورد) {
        سیم_دار_مقدار.تأیید_صحت_بعدی_مورد = هم_اکنون_مقدار + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int وضعیت_مقدار = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned روش_حالت = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = روش_حالت == 7 ? 1000 : روش_حالت == 5 ? 100 : روش_حالت == 2 ? 10 : 0;
        سیم_دار_مقدار.속도 = وضعیت_مقدار >= 0 && (وضعیت_مقدار & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (سیم_دار_مقدار.속도) {
            uint32_t تنظیمات = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            تنظیمات &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = تنظیمات | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            تنظیمات = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = تنظیمات | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(دستگاه_مقدار)) netif_set_link_up(دستگاه_مقدار);
        } else if (netif_is_link_up(دستگاه_مقدار)) netif_set_link_down(دستگاه_مقدار);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - سیم_دار_مقدار.소비);
    if (남음 > 고리개수) { سیم_دار_مقدار.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned مرتب_کردن_فهرست = سیم_دار_مقدار.소비 % 고리개수;
        همگام_سازی();
        uint32_t وضعیت_مقدار = 유선저장기(GENET_RX_DESC_STATUS(مرتب_کردن_فهرست));
        unsigned طول_مقدار = (وضعیت_مقدار & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((وضعیت_مقدار & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || طول_مقدار < 16 || طول_مقدار > 1538) سیم_دار_مقدار.집계[4]++;
        else {
            تمیز_حافظه_پنهان(سیم_دار_مقدار.받기[مرتب_کردن_فهرست], طول_مقدار, 1);
            struct pbuf *داده_ها = pbuf_alloc(PBUF_RAW, طول_مقدار - 2, PBUF_POOL);
            if (!داده_ها) سیم_دار_مقدار.집계[4]++;
            else if (pbuf_take(داده_ها, سیم_دار_مقدار.받기[مرتب_کردن_فهرست] + 2, طول_مقدار - 2) != ERR_OK || دستگاه_مقدار->input(داده_ها, دستگاه_مقدار) != ERR_OK) {
                pbuf_free(داده_ها); سیم_دار_مقدار.집계[4]++;
            } else { سیم_دار_مقدار.집계[0]++; سیم_دار_مقدار.집계[1] += طول_مقدار - 2; }
        }
        받는주소(مرتب_کردن_فهرست); همگام_سازی(); سیم_دار_مقدار.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = سیم_دار_مقدار.소비;
    }
}
uint32_t 유선망집계(unsigned ورودی_مقدار) {
    return ورودی_مقدار < 5 ? سیم_دار_مقدار.집계[ورودی_مقدار] : ورودی_مقدار == 5 ? سیم_دار_مقدار.속도 : ورودی_مقدار == 6 ? سیم_دار_مقدار.آماده_کردن : 0;
}
