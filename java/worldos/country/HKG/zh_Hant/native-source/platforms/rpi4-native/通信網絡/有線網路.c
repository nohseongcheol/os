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

#include "../命名/計算機連接名稱列.h"
#include "有線網路.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(循環序數) (UINT32_C(1) << (循環序數))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 板經過毫秒(void);
extern int 板物理硬件(void);
extern int 板計算機地址(unsigned char *);
#ifndef 有線寄存器集
#define 有線寄存器集(地址) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (地址)))
#endif
enum { 循環編號 = 16, 循環個數 = 256, 緩衝區大小 = 2048 };
static struct {
    unsigned char 接收[循環個數][緩衝區大小];
    unsigned char 發送[循環個數][緩衝區大小];
    uint16_t 消耗值, 產生值;
    int 物理地址, 準備, 速度值;
    uint32_t 統計值[5];
    uintptr_t 驗證下一項目;
} 有線值 __attribute__((aligned(64)));

static void 同步化(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void 清潔快取(void *資料, unsigned 長度, int 接收) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 結尾 = (uintptr_t)資料 + 長度;
    for (uintptr_t 地址 = (uintptr_t)資料 & ~(uintptr_t)63; 地址 < 結尾; 地址 += 64) {
        if (接收) __asm__ volatile("dc ivac, %0" :: "r"(地址) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(地址) : "memory");
    }
#else
    (void)資料; (void)長度; (void)接收;
#endif
    同步化();
}
static void 短暫延遲(void) {
    uintptr_t 結尾 = 板經過毫秒() + 1;
    while (板經過毫秒() < 結尾) {}
}
static int 物理傳送(unsigned 地址, unsigned 編號, int 寫入, unsigned 值) {
    uint32_t 命令 = (寫入 ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (地址 << GENET_MDIO_ADDR_SHIFT) | (編號 << GENET_MDIO_REG_SHIFT) | (值 & 65535);
    有線寄存器集(GENET_MDIO_CMD) = 命令;
    有線寄存器集(GENET_MDIO_CMD) = 命令 | GENET_MDIO_START_BUSY;
    uintptr_t 結尾 = 板經過毫秒() + 20;
    for (;;) {
        uint32_t 狀態值 = 有線寄存器集(GENET_MDIO_CMD);
        if (!(狀態值 & GENET_MDIO_START_BUSY))
            return 狀態值 & GENET_MDIO_READ_FAILED ? -1 : (int)(狀態值 & 65535);
        if (板經過毫秒() >= 結尾) return -1;
    }
}
static int 讀取物理(unsigned 編號) { return 物理傳送(有線值.物理地址, 編號, 0, 0); }
static int 寫入物理(unsigned 編號, unsigned 值) { return 物理傳送(有線值.物理地址, 編號, 1, 值); }
static int 準備物理(void) {
    有線值.物理地址 = -1;
    for (unsigned 地址 = 0; 地址 < 32; 地址++) {
        int 識別值 = 物理傳送(地址, 2, 0, 0);
        if (識別值 > 0 && 識別值 != 65535) { 有線值.物理地址 = 地址; break; }
    }
    if (有線值.物理地址 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (寫入物理(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int 值 = 讀取物理(BRGPHY_MII_AUXCTL);
    if (值 < 0 || 寫入物理(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (值 & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (寫入物理(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    值 = 讀取物理(BRGPHY_MII_SHADOW_1C);
    if (值 < 0 || 寫入物理(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (值 & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (寫入物理(4, 0x0141) < 0 || 寫入物理(9, 0x0200) < 0) return -1;
    return 寫入物理(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void 準備循環(unsigned 背景值) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned 循環值 = 背景值 + 0xc00 + GENET_DMA_RING_SIZE * 循環編號;
    for (unsigned 位置 = 0; 位置 <= 0x30; 位置 += 4) 有線寄存器集(循環值 + 位置) = 0;
    有線寄存器集(循環值 + 0x10) = (循環個數 << 16) | 緩衝區大小;
    有線寄存器集(循環值 + 0x1c) = 循環個數 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (背景值 == GENET_RX_BASE) 有線寄存器集(循環值 + 0x28) = (5 << 16) | (循環個數 >> 4);
    else 有線寄存器集(循環值 + 0x24) = 1;
    有線寄存器集(背景值 + 0x104c) = 8;
    有線寄存器集(背景值 + 0x1040) = __BIT(循環編號);
}
static void 接收中地址(unsigned 位置索引) {
    uintptr_t 地址 = (uintptr_t)有線值.接收[位置索引];
    清潔快取((void *)地址, 緩衝區大小, 0);
    有線寄存器集(GENET_RX_DESC_ADDRESS_LO(位置索引)) = (uint32_t)地址;
    有線寄存器集(GENET_RX_DESC_ADDRESS_HI(位置索引)) = (uint64_t)地址 >> 32;
    有線寄存器集(GENET_RX_DESC_STATUS(位置索引)) = 緩衝區大小 << 16;
}
static err_t 發送數據報(struct netif *設備, struct pbuf *數據報) {
    if (!有線值.準備 || !netif_is_link_up(設備)) return ERR_RTE;
    unsigned 大小 = 數據報->tot_len;
    if (!大小 || 大小 > 1536) return ERR_BUF;
    uint16_t 消耗值 = 有線寄存器集(GENET_TX_DMA_CONS_INDEX(循環編號));
    if ((uint16_t)(有線值.產生值 - 消耗值) >= 循環個數 - 1) return ERR_MEM;
    unsigned 位置索引 = 有線值.產生值 % 循環個數, 傳輸長度 = 大小 < 60 ? 60 : 大小;
    unsigned char *資料 = 有線值.發送[位置索引];
    memset(資料, 0, 傳輸長度);
    if (pbuf_copy_partial(數據報, 資料, 大小, 0) != 大小) return ERR_BUF;
    清潔快取(資料, 傳輸長度, 0);
    有線寄存器集(GENET_TX_DESC_ADDRESS_LO(位置索引)) = (uint32_t)(uintptr_t)資料;
    有線寄存器集(GENET_TX_DESC_ADDRESS_HI(位置索引)) = (uint64_t)(uintptr_t)資料 >> 32;
    有線寄存器集(GENET_TX_DESC_STATUS(位置索引)) = (傳輸長度 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    同步化();
    有線值.產生值++;
    有線寄存器集(GENET_TX_DMA_PROD_INDEX(循環編號)) = 有線值.產生值;
    有線值.統計值[2]++; 有線值.統計值[3] += 大小;
    return ERR_OK;
}
int 擁有有線設備(void) {
    return 板物理硬件() && ((有線寄存器集(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t 準備有線網路(struct netif *設備) {
    unsigned char 地址[6];
    if (!擁有有線設備() || !板計算機地址(地址) || (地址[0] & 1)) return ERR_IF;
    unsigned 總和值 = 0; for (unsigned 序數索引 = 0; 序數索引 < 6; 序數索引++) 總和值 |= 地址[序數索引];
    if (!總和值) return ERR_IF;
    memset(&有線值, 0, sizeof(有線值));
    有線寄存器集(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    有線寄存器集(GENET_RX_DMA_CTRL) = 有線寄存器集(GENET_TX_DMA_CTRL) = 0;
    uint32_t 初始狀態 = 有線寄存器集(GENET_SYS_RBUF_FLUSH_CTRL);
    有線寄存器集(GENET_SYS_RBUF_FLUSH_CTRL) = 初始狀態 | GENET_SYS_RBUF_FLUSH_RESET; 短暫延遲();
    有線寄存器集(GENET_SYS_RBUF_FLUSH_CTRL) = 初始狀態 & ~GENET_SYS_RBUF_FLUSH_RESET; 短暫延遲();
    有線寄存器集(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 短暫延遲();
    有線寄存器集(GENET_UMAC_CMD) = 0;
    有線寄存器集(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 短暫延遲();
    有線寄存器集(GENET_UMAC_CMD) = 0;
    有線寄存器集(GENET_UMAC_MIB_CTRL) = 7;
    有線寄存器集(GENET_UMAC_MIB_CTRL) = 0;
    有線寄存器集(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (準備物理() < 0) return ERR_IF;
    有線寄存器集(GENET_UMAC_MAC0) = (uint32_t)地址[0] << 24 | (uint32_t)地址[1] << 16 | 地址[2] << 8 | 地址[3];
    有線寄存器集(GENET_UMAC_MAC1) = 地址[4] << 8 | 地址[5];
    準備循環(GENET_TX_BASE); 準備循環(GENET_RX_BASE);
    for (unsigned 序數索引 = 0; 序數索引 < 循環個數; 序數索引++) 接收中地址(序數索引);
    同步化();
    有線寄存器集(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(循環編號);
    有線寄存器集(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(循環編號);
    有線寄存器集(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    有線寄存器集(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    有線寄存器集(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    有線寄存器集(GENET_UMAC_MDF_CTRL) = 0;
    有線寄存器集(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    設備->name[0] = 'e'; 設備->name[1] = 'n'; 設備->mtu = 1500;
    設備->hwaddr_len = 6; memcpy(設備->hwaddr, 地址, 6);
    設備->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    設備->output = etharp_output; 設備->linkoutput = 發送數據報;
    有線值.準備 = 1;
    return ERR_OK;
}
void 審查有線網路(struct netif *設備) {
    if (!有線值.準備) return;
    uintptr_t 當前時刻值 = 板經過毫秒();
    if (當前時刻值 >= 有線值.驗證下一項目) {
        有線值.驗證下一項目 = 當前時刻值 + 500;
        讀取物理(BRGPHY_MII_BMSR);
        int 狀態值 = 讀取物理(BRGPHY_MII_BMSR), 輔助值 = 讀取物理(BRGPHY_MII_AUXSTS);
        unsigned 方法模式 = 輔助值 < 0 ? 0 : (輔助值 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 速度值 = 方法模式 == 7 ? 1000 : 方法模式 == 5 ? 100 : 方法模式 == 2 ? 10 : 0;
        有線值.速度值 = 狀態值 >= 0 && (狀態值 & BRGPHY_BMSR_LINK) ? 速度值 : 0;
        if (有線值.速度值) {
            uint32_t 設置 = 有線寄存器集(GENET_EXT_RGMII_OOB_CTRL);
            設置 &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            有線寄存器集(GENET_EXT_RGMII_OOB_CTRL) = 設置 | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            設置 = 有線寄存器集(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            有線寄存器集(GENET_UMAC_CMD) = 設置 | (速度值 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 速度值 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(設備)) netif_set_link_up(設備);
        } else if (netif_is_link_up(設備)) netif_set_link_down(設備);
    }
    uint16_t 產生值 = 有線寄存器集(GENET_RX_DMA_PROD_INDEX(循環編號));
    unsigned 餘數資料 = (uint16_t)(產生值 - 有線值.消耗值);
    if (餘數資料 > 循環個數) { 有線值.統計值[4]++; return; }
    for (unsigned 循環序數 = 0; 循環序數 < 餘數資料 && 循環序數 < 32; 循環序數++) {
        unsigned 位置索引 = 有線值.消耗值 % 循環個數;
        同步化();
        uint32_t 狀態值 = 有線寄存器集(GENET_RX_DESC_STATUS(位置索引));
        unsigned 長度 = (狀態值 & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 邊界位置值 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((狀態值 & (邊界位置值 | GENET_RX_DESC_STATUS_RX_ERROR)) != 邊界位置值 || 長度 < 16 || 長度 > 1538) 有線值.統計值[4]++;
        else {
            清潔快取(有線值.接收[位置索引], 長度, 1);
            struct pbuf *資料 = pbuf_alloc(PBUF_RAW, 長度 - 2, PBUF_POOL);
            if (!資料) 有線值.統計值[4]++;
            else if (pbuf_take(資料, 有線值.接收[位置索引] + 2, 長度 - 2) != ERR_OK || 設備->input(資料, 設備) != ERR_OK) {
                pbuf_free(資料); 有線值.統計值[4]++;
            } else { 有線值.統計值[0]++; 有線值.統計值[1] += 長度 - 2; }
        }
        接收中地址(位置索引); 同步化(); 有線值.消耗值++;
        有線寄存器集(GENET_RX_DMA_CONS_INDEX(循環編號)) = 有線值.消耗值;
    }
}
uint32_t 有線網路統計(unsigned 條目值) {
    return 條目值 < 5 ? 有線值.統計值[條目值] : 條目值 == 5 ? 有線值.速度值 : 條目值 == 6 ? 有線值.準備 : 0;
}
