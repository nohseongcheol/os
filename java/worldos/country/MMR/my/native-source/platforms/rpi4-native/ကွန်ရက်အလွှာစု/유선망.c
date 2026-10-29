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

#include "../명명/စက်ချိတ်အမည်များ.h"
#include "유선망.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int ဆားကစ်ပြားရုပ်ပိုင်းစက်ပစ္စည်း(void);
extern int ဆားကစ်ပြားစက်လိပ်စာ(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(လိပ်စာ) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (လိပ်စာ)))
#endif
enum { ထပ်ခါလည်ပတ်မှုကိန်း = 16, ထပ်ခါလည်ပတ်မှုအရေအတွက် = 256, ကြားခံအရွယ် = 2048 };
static struct {
    unsigned char လက်ခံ[ထပ်ခါလည်ပတ်မှုအရေအတွက်][ကြားခံအရွယ်];
    unsigned char ပို့[ထပ်ခါလည်ပတ်မှုအရေအတွက်][ကြားခံအရွယ်];
    uint16_t 소비, 생산;
    int ရုပ်ပိုင်းလိပ်စာ, ပြင်ဆင်, 속도;
    uint32_t 집계[5];
    uintptr_t နောက်တစ်ခုအချက်အလက်တစ်ခုအတည်ပြု;
} 유선 __attribute__((aligned(64)));

static void တစ်ပြေးညီလုပ်(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void 캐시정리(void *ဒေတာ, unsigned အလျား, int လက်ခံ) {
#ifndef JKOROS_GENET_TEST
    uintptr_t အဆုံး = (uintptr_t)ဒေတာ + အလျား;
    for (uintptr_t လိပ်စာ = (uintptr_t)ဒေတာ & ~(uintptr_t)63; လိပ်စာ < အဆုံး; လိပ်စာ += 64) {
        if (လက်ခံ) __asm__ volatile("dc ivac, %0" :: "r"(လိပ်စာ) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(လိပ်စာ) : "memory");
    }
#else
    (void)ဒေတာ; (void)အလျား; (void)လက်ခံ;
#endif
    တစ်ပြေးညီလုပ်();
}
static void 잠깐(void) {
    uintptr_t အဆုံး = 보드밀리초() + 1;
    while (보드밀리초() < အဆုံး) {}
}
static int ရုပ်ပိုင်းလွှဲပြောင်း(unsigned လိပ်စာ, unsigned နံပါတ်, int ရေး, unsigned တန်ဖိုး) {
    uint32_t အမိန့် = (ရေး ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (လိပ်စာ << GENET_MDIO_ADDR_SHIFT) | (နံပါတ် << GENET_MDIO_REG_SHIFT) | (တန်ဖိုး & 65535);
    유선저장기(GENET_MDIO_CMD) = အမိန့်;
    유선저장기(GENET_MDIO_CMD) = အမိန့် | GENET_MDIO_START_BUSY;
    uintptr_t အဆုံး = 보드밀리초() + 20;
    for (;;) {
        uint32_t အခြေအနေတန်ဖိုး = 유선저장기(GENET_MDIO_CMD);
        if (!(အခြေအနေတန်ဖိုး & GENET_MDIO_START_BUSY))
            return အခြေအနေတန်ဖိုး & GENET_MDIO_READ_FAILED ? -1 : (int)(အခြေအနေတန်ဖိုး & 65535);
        if (보드밀리초() >= အဆုံး) return -1;
    }
}
static int ရုပ်ပိုင်းဖတ်(unsigned နံပါတ်) { return ရုပ်ပိုင်းလွှဲပြောင်း(유선.ရုပ်ပိုင်းလိပ်စာ, နံပါတ်, 0, 0); }
static int ရုပ်ပိုင်းရေး(unsigned နံပါတ်, unsigned တန်ဖိုး) { return ရုပ်ပိုင်းလွှဲပြောင်း(유선.ရုပ်ပိုင်းလိပ်စာ, နံပါတ်, 1, တန်ဖိုး); }
static int ရုပ်ပိုင်းပြင်ဆင်(void) {
    유선.ရုပ်ပိုင်းလိပ်စာ = -1;
    for (unsigned လိပ်စာ = 0; လိပ်စာ < 32; လိပ်စာ++) {
        int 식별 = ရုပ်ပိုင်းလွှဲပြောင်း(လိပ်စာ, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { 유선.ရုပ်ပိုင်းလိပ်စာ = လိပ်စာ; break; }
    }
    if (유선.ရုပ်ပိုင်းလိပ်စာ < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (ရုပ်ပိုင်းရေး(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int တန်ဖိုး = ရုပ်ပိုင်းဖတ်(BRGPHY_MII_AUXCTL);
    if (တန်ဖိုး < 0 || ရုပ်ပိုင်းရေး(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (တန်ဖိုး & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (ရုပ်ပိုင်းရေး(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    တန်ဖိုး = ရုပ်ပိုင်းဖတ်(BRGPHY_MII_SHADOW_1C);
    if (တန်ဖိုး < 0 || ရုပ်ပိုင်းရေး(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (တန်ဖိုး & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (ရုပ်ပိုင်းရေး(4, 0x0141) < 0 || ရုပ်ပိုင်းရေး(9, 0x0200) < 0) return -1;
    return ရုပ်ပိုင်းရေး(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void ထပ်ခါလည်ပတ်မှုပြင်ဆင်(unsigned နောက်ခံတန်ဖိုး) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ထပ်ခါလည်ပတ်မှုတန်ဖိုး = နောက်ခံတန်ဖိုး + 0xc00 + GENET_DMA_RING_SIZE * ထပ်ခါလည်ပတ်မှုကိန်း;
    for (unsigned နေရာ = 0; နေရာ <= 0x30; နေရာ += 4) 유선저장기(ထပ်ခါလည်ပတ်မှုတန်ဖိုး + နေရာ) = 0;
    유선저장기(ထပ်ခါလည်ပတ်မှုတန်ဖိုး + 0x10) = (ထပ်ခါလည်ပတ်မှုအရေအတွက် << 16) | ကြားခံအရွယ်;
    유선저장기(ထပ်ခါလည်ပတ်မှုတန်ဖိုး + 0x1c) = ထပ်ခါလည်ပတ်မှုအရေအတွက် * GENET_DMA_DESC_SIZE / 4 - 1;
    if (နောက်ခံတန်ဖိုး == GENET_RX_BASE) 유선저장기(ထပ်ခါလည်ပတ်မှုတန်ဖိုး + 0x28) = (5 << 16) | (ထပ်ခါလည်ပတ်မှုအရေအတွက် >> 4);
    else 유선저장기(ထပ်ခါလည်ပတ်မှုတန်ဖိုး + 0x24) = 1;
    유선저장기(နောက်ခံတန်ဖိုး + 0x104c) = 8;
    유선저장기(နောက်ခံတန်ဖိုး + 0x1040) = __BIT(ထပ်ခါလည်ပတ်မှုကိန်း);
}
static void 받는주소(unsigned နေရာအညွှန်းကိန်း) {
    uintptr_t လိပ်စာ = (uintptr_t)유선.လက်ခံ[နေရာအညွှန်းကိန်း];
    캐시정리((void *)လိပ်စာ, ကြားခံအရွယ်, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(နေရာအညွှန်းကိန်း)) = (uint32_t)လိပ်စာ;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(နေရာအညွှန်းကိန်း)) = (uint64_t)လိပ်စာ >> 32;
    유선저장기(GENET_RX_DESC_STATUS(နေရာအညွှန်းကိန်း)) = ကြားခံအရွယ် << 16;
}
static err_t ဒေတာစာပို့(struct netif *ကိရိယာ, struct pbuf *ဒေတာစာ) {
    if (!유선.ပြင်ဆင် || !netif_is_link_up(ကိရိယာ)) return ERR_RTE;
    unsigned အရွယ် = ဒေတာစာ->tot_len;
    if (!အရွယ် || အရွယ် > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(ထပ်ခါလည်ပတ်မှုကိန်း));
    if ((uint16_t)(유선.생산 - 소비) >= ထပ်ခါလည်ပတ်မှုအရေအတွက် - 1) return ERR_MEM;
    unsigned နေရာအညွှန်းကိန်း = 유선.생산 % ထပ်ခါလည်ပတ်မှုအရေအတွက်, ထုတ်ပို့အလျား = အရွယ် < 60 ? 60 : အရွယ်;
    unsigned char *ဒေတာ = 유선.ပို့[နေရာအညွှန်းကိန်း];
    memset(ဒေတာ, 0, ထုတ်ပို့အလျား);
    if (pbuf_copy_partial(ဒေတာစာ, ဒေတာ, အရွယ်, 0) != အရွယ်) return ERR_BUF;
    캐시정리(ဒေတာ, ထုတ်ပို့အလျား, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(နေရာအညွှန်းကိန်း)) = (uint32_t)(uintptr_t)ဒေတာ;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(နေရာအညွှန်းကိန်း)) = (uint64_t)(uintptr_t)ဒေတာ >> 32;
    유선저장기(GENET_TX_DESC_STATUS(နေရာအညွှန်းကိန်း)) = (ထုတ်ပို့အလျား << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    တစ်ပြေးညီလုပ်();
    유선.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(ထပ်ခါလည်ပတ်မှုကိန်း)) = 유선.생산;
    유선.집계[2]++; 유선.집계[3] += အရွယ်;
    return ERR_OK;
}
int 유선장치있음(void) {
    return ဆားကစ်ပြားရုပ်ပိုင်းစက်ပစ္စည်း() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t 유선망준비(struct netif *ကိရိယာ) {
    unsigned char လိပ်စာ[6];
    if (!유선장치있음() || !ဆားကစ်ပြားစက်လိပ်စာ(လိပ်စာ) || (လိပ်စာ[0] & 1)) return ERR_IF;
    unsigned စုစုပေါင်းတန်ဖိုး = 0; for (unsigned အစဉ်အမှတ် = 0; အစဉ်အမှတ် < 6; အစဉ်အမှတ်++) စုစုပေါင်းတန်ဖိုး |= လိပ်စာ[အစဉ်အမှတ်];
    if (!စုစုပေါင်းတန်ဖိုး) return ERR_IF;
    memset(&유선, 0, sizeof(유선));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t အစဦးအခြေအနေ = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = အစဦးအခြေအနေ | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = အစဦးအခြေအနေ & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (ရုပ်ပိုင်းပြင်ဆင်() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)လိပ်စာ[0] << 24 | (uint32_t)လိပ်စာ[1] << 16 | လိပ်စာ[2] << 8 | လိပ်စာ[3];
    유선저장기(GENET_UMAC_MAC1) = လိပ်စာ[4] << 8 | လိပ်စာ[5];
    ထပ်ခါလည်ပတ်မှုပြင်ဆင်(GENET_TX_BASE); ထပ်ခါလည်ပတ်မှုပြင်ဆင်(GENET_RX_BASE);
    for (unsigned အစဉ်အမှတ် = 0; အစဉ်အမှတ် < ထပ်ခါလည်ပတ်မှုအရေအတွက်; အစဉ်အမှတ်++) 받는주소(အစဉ်အမှတ်);
    တစ်ပြေးညီလုပ်();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(ထပ်ခါလည်ပတ်မှုကိန်း);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(ထပ်ခါလည်ပတ်မှုကိန်း);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ကိရိယာ->name[0] = 'e'; ကိရိယာ->name[1] = 'n'; ကိရိယာ->mtu = 1500;
    ကိရိယာ->hwaddr_len = 6; memcpy(ကိရိယာ->hwaddr, လိပ်စာ, 6);
    ကိရိယာ->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ကိရိယာ->output = etharp_output; ကိရိယာ->linkoutput = ဒေတာစာပို့;
    유선.ပြင်ဆင် = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ကိရိယာ) {
    if (!유선.ပြင်ဆင်) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= 유선.နောက်တစ်ခုအချက်အလက်တစ်ခုအတည်ပြု) {
        유선.နောက်တစ်ခုအချက်အလက်တစ်ခုအတည်ပြု = 지금 + 500;
        ရုပ်ပိုင်းဖတ်(BRGPHY_MII_BMSR);
        int အခြေအနေတန်ဖိုး = ရုပ်ပိုင်းဖတ်(BRGPHY_MII_BMSR), 보조 = ရုပ်ပိုင်းဖတ်(BRGPHY_MII_AUXSTS);
        unsigned နည်းလမ်းနည်းစနစ် = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = နည်းလမ်းနည်းစနစ် == 7 ? 1000 : နည်းလမ်းနည်းစနစ် == 5 ? 100 : နည်းလမ်းနည်းစနစ် == 2 ? 10 : 0;
        유선.속도 = အခြေအနေတန်ဖိုး >= 0 && (အခြေအနေတန်ဖိုး & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (유선.속도) {
            uint32_t သတ်မှတ်ချက် = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            သတ်မှတ်ချက် &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = သတ်မှတ်ချက် | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            သတ်မှတ်ချက် = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = သတ်မှတ်ချက် | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ကိရိယာ)) netif_set_link_up(ကိရိယာ);
        } else if (netif_is_link_up(ကိရိယာ)) netif_set_link_down(ကိရိယာ);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(ထပ်ခါလည်ပတ်မှုကိန်း));
    unsigned လက်ကျန်ဒေတာ = (uint16_t)(생산 - 유선.소비);
    if (လက်ကျန်ဒေတာ > ထပ်ခါလည်ပတ်မှုအရေအတွက်) { 유선.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < လက်ကျန်ဒေတာ && 고리순번 < 32; 고리순번++) {
        unsigned နေရာအညွှန်းကိန်း = 유선.소비 % ထပ်ခါလည်ပတ်မှုအရေအတွက်;
        တစ်ပြေးညီလုပ်();
        uint32_t အခြေအနေတန်ဖိုး = 유선저장기(GENET_RX_DESC_STATUS(နေရာအညွှန်းကိန်း));
        unsigned အလျား = (အခြေအနေတန်ဖိုး & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t နယ်နိမိတ်တန်ဖိုး = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((အခြေအနေတန်ဖိုး & (နယ်နိမိတ်တန်ဖိုး | GENET_RX_DESC_STATUS_RX_ERROR)) != နယ်နိမိတ်တန်ဖိုး || အလျား < 16 || အလျား > 1538) 유선.집계[4]++;
        else {
            캐시정리(유선.လက်ခံ[နေရာအညွှန်းကိန်း], အလျား, 1);
            struct pbuf *ဒေတာ = pbuf_alloc(PBUF_RAW, အလျား - 2, PBUF_POOL);
            if (!ဒေတာ) 유선.집계[4]++;
            else if (pbuf_take(ဒေတာ, 유선.လက်ခံ[နေရာအညွှန်းကိန်း] + 2, အလျား - 2) != ERR_OK || ကိရိယာ->input(ဒေတာ, ကိရိယာ) != ERR_OK) {
                pbuf_free(ဒေတာ); 유선.집계[4]++;
            } else { 유선.집계[0]++; 유선.집계[1] += အလျား - 2; }
        }
        받는주소(နေရာအညွှန်းကိန်း); တစ်ပြေးညီလုပ်(); 유선.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(ထပ်ခါလည်ပတ်မှုကိန်း)) = 유선.소비;
    }
}
uint32_t 유선망집계(unsigned အချက်တန်ဖိုး) {
    return အချက်တန်ဖိုး < 5 ? 유선.집계[အချက်တန်ဖိုး] : အချက်တန်ဖိုး == 5 ? 유선.속도 : အချက်တန်ဖိုး == 6 ? 유선.ပြင်ဆင် : 0;
}
