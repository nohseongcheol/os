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

#include "../命名/機械連結名前一覧.h"
#include "結線済み通信網.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(ループ序数) (UINT32_C(1) << (ループ序数))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 基板経過ミリ秒(void);
extern int 基板物理機器(void);
extern int 基板機械番地(unsigned char *);
#ifndef 結線済みレジスタ群
#define 結線済みレジスタ群(番地) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (番地)))
#endif
enum { ループ番号 = 16, ループ個数 = 256, 緩衝域容量 = 2048 };
static struct {
    unsigned char 受取[ループ個数][緩衝域容量];
    unsigned char 送信[ループ個数][緩衝域容量];
    uint16_t 値消費, 生成処理値;
    int 物理番地, 用意, 速度値;
    uint32_t 統計値[5];
    uintptr_t 次回項目検証;
} 結線済み値 __attribute__((aligned(64)));

static void 同期化(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void 清掃キャッシュ(void *データ, unsigned 長さ, int 受取) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 終端 = (uintptr_t)データ + 長さ;
    for (uintptr_t 番地 = (uintptr_t)データ & ~(uintptr_t)63; 番地 < 終端; 番地 += 64) {
        if (受取) __asm__ volatile("dc ivac, %0" :: "r"(番地) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(番地) : "memory");
    }
#else
    (void)データ; (void)長さ; (void)受取;
#endif
    同期化();
}
static void 短時間遅延(void) {
    uintptr_t 終端 = 基板経過ミリ秒() + 1;
    while (基板経過ミリ秒() < 終端) {}
}
static int 物理転送(unsigned 番地, unsigned 番号, int 書込, unsigned 値) {
    uint32_t 命令 = (書込 ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (番地 << GENET_MDIO_ADDR_SHIFT) | (番号 << GENET_MDIO_REG_SHIFT) | (値 & 65535);
    結線済みレジスタ群(GENET_MDIO_CMD) = 命令;
    結線済みレジスタ群(GENET_MDIO_CMD) = 命令 | GENET_MDIO_START_BUSY;
    uintptr_t 終端 = 基板経過ミリ秒() + 20;
    for (;;) {
        uint32_t 状況値 = 結線済みレジスタ群(GENET_MDIO_CMD);
        if (!(状況値 & GENET_MDIO_START_BUSY))
            return 状況値 & GENET_MDIO_READ_FAILED ? -1 : (int)(状況値 & 65535);
        if (基板経過ミリ秒() >= 終端) return -1;
    }
}
static int 物理読取(unsigned 番号) { return 物理転送(結線済み値.物理番地, 番号, 0, 0); }
static int 物理書込(unsigned 番号, unsigned 値) { return 物理転送(結線済み値.物理番地, 番号, 1, 値); }
static int 物理用意(void) {
    結線済み値.物理番地 = -1;
    for (unsigned 番地 = 0; 番地 < 32; 番地++) {
        int 値識別処理 = 物理転送(番地, 2, 0, 0);
        if (値識別処理 > 0 && 値識別処理 != 65535) { 結線済み値.物理番地 = 番地; break; }
    }
    if (結線済み値.物理番地 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (物理書込(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int 値 = 物理読取(BRGPHY_MII_AUXCTL);
    if (値 < 0 || 物理書込(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (値 & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (物理書込(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    値 = 物理読取(BRGPHY_MII_SHADOW_1C);
    if (値 < 0 || 物理書込(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (値 & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (物理書込(4, 0x0141) < 0 || 物理書込(9, 0x0200) < 0) return -1;
    return 物理書込(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void ループ用意(unsigned 背景値) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ループ値 = 背景値 + 0xc00 + GENET_DMA_RING_SIZE * ループ番号;
    for (unsigned 位置 = 0; 位置 <= 0x30; 位置 += 4) 結線済みレジスタ群(ループ値 + 位置) = 0;
    結線済みレジスタ群(ループ値 + 0x10) = (ループ個数 << 16) | 緩衝域容量;
    結線済みレジスタ群(ループ値 + 0x1c) = ループ個数 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (背景値 == GENET_RX_BASE) 結線済みレジスタ群(ループ値 + 0x28) = (5 << 16) | (ループ個数 >> 4);
    else 結線済みレジスタ群(ループ値 + 0x24) = 1;
    結線済みレジスタ群(背景値 + 0x104c) = 8;
    結線済みレジスタ群(背景値 + 0x1040) = __BIT(ループ番号);
}
static void 受信中番地(unsigned 位置添字) {
    uintptr_t 番地 = (uintptr_t)結線済み値.受取[位置添字];
    清掃キャッシュ((void *)番地, 緩衝域容量, 0);
    結線済みレジスタ群(GENET_RX_DESC_ADDRESS_LO(位置添字)) = (uint32_t)番地;
    結線済みレジスタ群(GENET_RX_DESC_ADDRESS_HI(位置添字)) = (uint64_t)番地 >> 32;
    結線済みレジスタ群(GENET_RX_DESC_STATUS(位置添字)) = 緩衝域容量 << 16;
}
static err_t データグラム送信(struct netif *装置, struct pbuf *データグラム) {
    if (!結線済み値.用意 || !netif_is_link_up(装置)) return ERR_RTE;
    unsigned 容量 = データグラム->tot_len;
    if (!容量 || 容量 > 1536) return ERR_BUF;
    uint16_t 値消費 = 結線済みレジスタ群(GENET_TX_DMA_CONS_INDEX(ループ番号));
    if ((uint16_t)(結線済み値.生成処理値 - 値消費) >= ループ個数 - 1) return ERR_MEM;
    unsigned 位置添字 = 結線済み値.生成処理値 % ループ個数, 伝送長さ = 容量 < 60 ? 60 : 容量;
    unsigned char *データ = 結線済み値.送信[位置添字];
    memset(データ, 0, 伝送長さ);
    if (pbuf_copy_partial(データグラム, データ, 容量, 0) != 容量) return ERR_BUF;
    清掃キャッシュ(データ, 伝送長さ, 0);
    結線済みレジスタ群(GENET_TX_DESC_ADDRESS_LO(位置添字)) = (uint32_t)(uintptr_t)データ;
    結線済みレジスタ群(GENET_TX_DESC_ADDRESS_HI(位置添字)) = (uint64_t)(uintptr_t)データ >> 32;
    結線済みレジスタ群(GENET_TX_DESC_STATUS(位置添字)) = (伝送長さ << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    同期化();
    結線済み値.生成処理値++;
    結線済みレジスタ群(GENET_TX_DMA_PROD_INDEX(ループ番号)) = 結線済み値.生成処理値;
    結線済み値.統計値[2]++; 結線済み値.統計値[3] += 容量;
    return ERR_OK;
}
int 保有結線済み装置(void) {
    return 基板物理機器() && ((結線済みレジスタ群(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t 結線済み通信網用意(struct netif *装置) {
    unsigned char 番地[6];
    if (!保有結線済み装置() || !基板機械番地(番地) || (番地[0] & 1)) return ERR_IF;
    unsigned 総和値 = 0; for (unsigned 序数添字 = 0; 序数添字 < 6; 序数添字++) 総和値 |= 番地[序数添字];
    if (!総和値) return ERR_IF;
    memset(&結線済み値, 0, sizeof(結線済み値));
    結線済みレジスタ群(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    結線済みレジスタ群(GENET_RX_DMA_CTRL) = 結線済みレジスタ群(GENET_TX_DMA_CTRL) = 0;
    uint32_t 初期状況 = 結線済みレジスタ群(GENET_SYS_RBUF_FLUSH_CTRL);
    結線済みレジスタ群(GENET_SYS_RBUF_FLUSH_CTRL) = 初期状況 | GENET_SYS_RBUF_FLUSH_RESET; 短時間遅延();
    結線済みレジスタ群(GENET_SYS_RBUF_FLUSH_CTRL) = 初期状況 & ~GENET_SYS_RBUF_FLUSH_RESET; 短時間遅延();
    結線済みレジスタ群(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 短時間遅延();
    結線済みレジスタ群(GENET_UMAC_CMD) = 0;
    結線済みレジスタ群(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 短時間遅延();
    結線済みレジスタ群(GENET_UMAC_CMD) = 0;
    結線済みレジスタ群(GENET_UMAC_MIB_CTRL) = 7;
    結線済みレジスタ群(GENET_UMAC_MIB_CTRL) = 0;
    結線済みレジスタ群(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (物理用意() < 0) return ERR_IF;
    結線済みレジスタ群(GENET_UMAC_MAC0) = (uint32_t)番地[0] << 24 | (uint32_t)番地[1] << 16 | 番地[2] << 8 | 番地[3];
    結線済みレジスタ群(GENET_UMAC_MAC1) = 番地[4] << 8 | 番地[5];
    ループ用意(GENET_TX_BASE); ループ用意(GENET_RX_BASE);
    for (unsigned 序数添字 = 0; 序数添字 < ループ個数; 序数添字++) 受信中番地(序数添字);
    同期化();
    結線済みレジスタ群(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(ループ番号);
    結線済みレジスタ群(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(ループ番号);
    結線済みレジスタ群(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    結線済みレジスタ群(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    結線済みレジスタ群(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    結線済みレジスタ群(GENET_UMAC_MDF_CTRL) = 0;
    結線済みレジスタ群(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    装置->name[0] = 'e'; 装置->name[1] = 'n'; 装置->mtu = 1500;
    装置->hwaddr_len = 6; memcpy(装置->hwaddr, 番地, 6);
    装置->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    装置->output = etharp_output; 装置->linkoutput = データグラム送信;
    結線済み値.用意 = 1;
    return ERR_OK;
}
void 結線済み通信網調査(struct netif *装置) {
    if (!結線済み値.用意) return;
    uintptr_t 現時点値 = 基板経過ミリ秒();
    if (現時点値 >= 結線済み値.次回項目検証) {
        結線済み値.次回項目検証 = 現時点値 + 500;
        物理読取(BRGPHY_MII_BMSR);
        int 状況値 = 物理読取(BRGPHY_MII_BMSR), 補助値 = 物理読取(BRGPHY_MII_AUXSTS);
        unsigned メソッド方式 = 補助値 < 0 ? 0 : (補助値 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 速度値 = メソッド方式 == 7 ? 1000 : メソッド方式 == 5 ? 100 : メソッド方式 == 2 ? 10 : 0;
        結線済み値.速度値 = 状況値 >= 0 && (状況値 & BRGPHY_BMSR_LINK) ? 速度値 : 0;
        if (結線済み値.速度値) {
            uint32_t 設定値 = 結線済みレジスタ群(GENET_EXT_RGMII_OOB_CTRL);
            設定値 &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            結線済みレジスタ群(GENET_EXT_RGMII_OOB_CTRL) = 設定値 | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            設定値 = 結線済みレジスタ群(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            結線済みレジスタ群(GENET_UMAC_CMD) = 設定値 | (速度値 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 速度値 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(装置)) netif_set_link_up(装置);
        } else if (netif_is_link_up(装置)) netif_set_link_down(装置);
    }
    uint16_t 生成処理値 = 結線済みレジスタ群(GENET_RX_DMA_PROD_INDEX(ループ番号));
    unsigned 剰余データ = (uint16_t)(生成処理値 - 結線済み値.値消費);
    if (剰余データ > ループ個数) { 結線済み値.統計値[4]++; return; }
    for (unsigned ループ序数 = 0; ループ序数 < 剰余データ && ループ序数 < 32; ループ序数++) {
        unsigned 位置添字 = 結線済み値.値消費 % ループ個数;
        同期化();
        uint32_t 状況値 = 結線済みレジスタ群(GENET_RX_DESC_STATUS(位置添字));
        unsigned 長さ = (状況値 & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 境界位置値 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((状況値 & (境界位置値 | GENET_RX_DESC_STATUS_RX_ERROR)) != 境界位置値 || 長さ < 16 || 長さ > 1538) 結線済み値.統計値[4]++;
        else {
            清掃キャッシュ(結線済み値.受取[位置添字], 長さ, 1);
            struct pbuf *データ = pbuf_alloc(PBUF_RAW, 長さ - 2, PBUF_POOL);
            if (!データ) 結線済み値.統計値[4]++;
            else if (pbuf_take(データ, 結線済み値.受取[位置添字] + 2, 長さ - 2) != ERR_OK || 装置->input(データ, 装置) != ERR_OK) {
                pbuf_free(データ); 結線済み値.統計値[4]++;
            } else { 結線済み値.統計値[0]++; 結線済み値.統計値[1] += 長さ - 2; }
        }
        受信中番地(位置添字); 同期化(); 結線済み値.値消費++;
        結線済みレジスタ群(GENET_RX_DMA_CONS_INDEX(ループ番号)) = 結線済み値.値消費;
    }
}
uint32_t 結線済み通信網統計(unsigned 入口値) {
    return 入口値 < 5 ? 結線済み値.統計値[入口値] : 入口値 == 5 ? 結線済み値.速度値 : 入口値 == 6 ? 結線済み値.用意 : 0;
}
