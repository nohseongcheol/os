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

#include "../命名/计算机连接名称列.h"
#include "有线网络.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(循环序数) (UINT32_C(1) << (循环序数))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 板经过毫秒(void);
extern int 板物理硬件(void);
extern int 板计算机地址(unsigned char *);
#ifndef 有线寄存器集
#define 有线寄存器集(地址) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (地址)))
#endif
enum { 循环编号 = 16, 循环个数 = 256, 缓冲大小 = 2048 };
static struct {
    unsigned char 接收[循环个数][缓冲大小];
    unsigned char 发送[循环个数][缓冲大小];
    uint16_t 消耗值, 产生值;
    int 物理地址, 准备, 速度值;
    uint32_t 统计值[5];
    uintptr_t 验证下一项目;
} 有线值 __attribute__((aligned(64)));

static void 同步化(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void 清洁缓存(void *数据, unsigned 长度, int 接收) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 结尾 = (uintptr_t)数据 + 长度;
    for (uintptr_t 地址 = (uintptr_t)数据 & ~(uintptr_t)63; 地址 < 结尾; 地址 += 64) {
        if (接收) __asm__ volatile("dc ivac, %0" :: "r"(地址) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(地址) : "memory");
    }
#else
    (void)数据; (void)长度; (void)接收;
#endif
    同步化();
}
static void 短暂延迟(void) {
    uintptr_t 结尾 = 板经过毫秒() + 1;
    while (板经过毫秒() < 结尾) {}
}
static int 物理传送(unsigned 地址, unsigned 编号, int 写入, unsigned 值) {
    uint32_t 命令 = (写入 ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (地址 << GENET_MDIO_ADDR_SHIFT) | (编号 << GENET_MDIO_REG_SHIFT) | (值 & 65535);
    有线寄存器集(GENET_MDIO_CMD) = 命令;
    有线寄存器集(GENET_MDIO_CMD) = 命令 | GENET_MDIO_START_BUSY;
    uintptr_t 结尾 = 板经过毫秒() + 20;
    for (;;) {
        uint32_t 状态值 = 有线寄存器集(GENET_MDIO_CMD);
        if (!(状态值 & GENET_MDIO_START_BUSY))
            return 状态值 & GENET_MDIO_READ_FAILED ? -1 : (int)(状态值 & 65535);
        if (板经过毫秒() >= 结尾) return -1;
    }
}
static int 读取物理(unsigned 编号) { return 物理传送(有线值.物理地址, 编号, 0, 0); }
static int 写入物理(unsigned 编号, unsigned 值) { return 物理传送(有线值.物理地址, 编号, 1, 值); }
static int 准备物理(void) {
    有线值.物理地址 = -1;
    for (unsigned 地址 = 0; 地址 < 32; 地址++) {
        int 识别值 = 物理传送(地址, 2, 0, 0);
        if (识别值 > 0 && 识别值 != 65535) { 有线值.物理地址 = 地址; break; }
    }
    if (有线值.物理地址 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (写入物理(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int 值 = 读取物理(BRGPHY_MII_AUXCTL);
    if (值 < 0 || 写入物理(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (值 & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (写入物理(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    值 = 读取物理(BRGPHY_MII_SHADOW_1C);
    if (值 < 0 || 写入物理(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (值 & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (写入物理(4, 0x0141) < 0 || 写入物理(9, 0x0200) < 0) return -1;
    return 写入物理(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void 准备循环(unsigned 背景值) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned 循环值 = 背景值 + 0xc00 + GENET_DMA_RING_SIZE * 循环编号;
    for (unsigned 位置 = 0; 位置 <= 0x30; 位置 += 4) 有线寄存器集(循环值 + 位置) = 0;
    有线寄存器集(循环值 + 0x10) = (循环个数 << 16) | 缓冲大小;
    有线寄存器集(循环值 + 0x1c) = 循环个数 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (背景值 == GENET_RX_BASE) 有线寄存器集(循环值 + 0x28) = (5 << 16) | (循环个数 >> 4);
    else 有线寄存器集(循环值 + 0x24) = 1;
    有线寄存器集(背景值 + 0x104c) = 8;
    有线寄存器集(背景值 + 0x1040) = __BIT(循环编号);
}
static void 接收中地址(unsigned 位置索引) {
    uintptr_t 地址 = (uintptr_t)有线值.接收[位置索引];
    清洁缓存((void *)地址, 缓冲大小, 0);
    有线寄存器集(GENET_RX_DESC_ADDRESS_LO(位置索引)) = (uint32_t)地址;
    有线寄存器集(GENET_RX_DESC_ADDRESS_HI(位置索引)) = (uint64_t)地址 >> 32;
    有线寄存器集(GENET_RX_DESC_STATUS(位置索引)) = 缓冲大小 << 16;
}
static err_t 发送数据报(struct netif *设备, struct pbuf *数据报) {
    if (!有线值.准备 || !netif_is_link_up(设备)) return ERR_RTE;
    unsigned 大小 = 数据报->tot_len;
    if (!大小 || 大小 > 1536) return ERR_BUF;
    uint16_t 消耗值 = 有线寄存器集(GENET_TX_DMA_CONS_INDEX(循环编号));
    if ((uint16_t)(有线值.产生值 - 消耗值) >= 循环个数 - 1) return ERR_MEM;
    unsigned 位置索引 = 有线值.产生值 % 循环个数, 传输长度 = 大小 < 60 ? 60 : 大小;
    unsigned char *数据 = 有线值.发送[位置索引];
    memset(数据, 0, 传输长度);
    if (pbuf_copy_partial(数据报, 数据, 大小, 0) != 大小) return ERR_BUF;
    清洁缓存(数据, 传输长度, 0);
    有线寄存器集(GENET_TX_DESC_ADDRESS_LO(位置索引)) = (uint32_t)(uintptr_t)数据;
    有线寄存器集(GENET_TX_DESC_ADDRESS_HI(位置索引)) = (uint64_t)(uintptr_t)数据 >> 32;
    有线寄存器集(GENET_TX_DESC_STATUS(位置索引)) = (传输长度 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    同步化();
    有线值.产生值++;
    有线寄存器集(GENET_TX_DMA_PROD_INDEX(循环编号)) = 有线值.产生值;
    有线值.统计值[2]++; 有线值.统计值[3] += 大小;
    return ERR_OK;
}
int 拥有有线设备(void) {
    return 板物理硬件() && ((有线寄存器集(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t 准备有线网络(struct netif *设备) {
    unsigned char 地址[6];
    if (!拥有有线设备() || !板计算机地址(地址) || (地址[0] & 1)) return ERR_IF;
    unsigned 总和值 = 0; for (unsigned 序数索引 = 0; 序数索引 < 6; 序数索引++) 总和值 |= 地址[序数索引];
    if (!总和值) return ERR_IF;
    memset(&有线值, 0, sizeof(有线值));
    有线寄存器集(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    有线寄存器集(GENET_RX_DMA_CTRL) = 有线寄存器集(GENET_TX_DMA_CTRL) = 0;
    uint32_t 初始状态 = 有线寄存器集(GENET_SYS_RBUF_FLUSH_CTRL);
    有线寄存器集(GENET_SYS_RBUF_FLUSH_CTRL) = 初始状态 | GENET_SYS_RBUF_FLUSH_RESET; 短暂延迟();
    有线寄存器集(GENET_SYS_RBUF_FLUSH_CTRL) = 初始状态 & ~GENET_SYS_RBUF_FLUSH_RESET; 短暂延迟();
    有线寄存器集(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 短暂延迟();
    有线寄存器集(GENET_UMAC_CMD) = 0;
    有线寄存器集(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 短暂延迟();
    有线寄存器集(GENET_UMAC_CMD) = 0;
    有线寄存器集(GENET_UMAC_MIB_CTRL) = 7;
    有线寄存器集(GENET_UMAC_MIB_CTRL) = 0;
    有线寄存器集(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (准备物理() < 0) return ERR_IF;
    有线寄存器集(GENET_UMAC_MAC0) = (uint32_t)地址[0] << 24 | (uint32_t)地址[1] << 16 | 地址[2] << 8 | 地址[3];
    有线寄存器集(GENET_UMAC_MAC1) = 地址[4] << 8 | 地址[5];
    准备循环(GENET_TX_BASE); 准备循环(GENET_RX_BASE);
    for (unsigned 序数索引 = 0; 序数索引 < 循环个数; 序数索引++) 接收中地址(序数索引);
    同步化();
    有线寄存器集(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(循环编号);
    有线寄存器集(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(循环编号);
    有线寄存器集(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    有线寄存器集(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    有线寄存器集(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    有线寄存器集(GENET_UMAC_MDF_CTRL) = 0;
    有线寄存器集(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    设备->name[0] = 'e'; 设备->name[1] = 'n'; 设备->mtu = 1500;
    设备->hwaddr_len = 6; memcpy(设备->hwaddr, 地址, 6);
    设备->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    设备->output = etharp_output; 设备->linkoutput = 发送数据报;
    有线值.准备 = 1;
    return ERR_OK;
}
void 审查有线网络(struct netif *设备) {
    if (!有线值.准备) return;
    uintptr_t 当前时刻值 = 板经过毫秒();
    if (当前时刻值 >= 有线值.验证下一项目) {
        有线值.验证下一项目 = 当前时刻值 + 500;
        读取物理(BRGPHY_MII_BMSR);
        int 状态值 = 读取物理(BRGPHY_MII_BMSR), 辅助值 = 读取物理(BRGPHY_MII_AUXSTS);
        unsigned 方法模式 = 辅助值 < 0 ? 0 : (辅助值 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 速度值 = 方法模式 == 7 ? 1000 : 方法模式 == 5 ? 100 : 方法模式 == 2 ? 10 : 0;
        有线值.速度值 = 状态值 >= 0 && (状态值 & BRGPHY_BMSR_LINK) ? 速度值 : 0;
        if (有线值.速度值) {
            uint32_t 设置 = 有线寄存器集(GENET_EXT_RGMII_OOB_CTRL);
            设置 &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            有线寄存器集(GENET_EXT_RGMII_OOB_CTRL) = 设置 | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            设置 = 有线寄存器集(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            有线寄存器集(GENET_UMAC_CMD) = 设置 | (速度值 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 速度值 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(设备)) netif_set_link_up(设备);
        } else if (netif_is_link_up(设备)) netif_set_link_down(设备);
    }
    uint16_t 产生值 = 有线寄存器集(GENET_RX_DMA_PROD_INDEX(循环编号));
    unsigned 余数数据 = (uint16_t)(产生值 - 有线值.消耗值);
    if (余数数据 > 循环个数) { 有线值.统计值[4]++; return; }
    for (unsigned 循环序数 = 0; 循环序数 < 余数数据 && 循环序数 < 32; 循环序数++) {
        unsigned 位置索引 = 有线值.消耗值 % 循环个数;
        同步化();
        uint32_t 状态值 = 有线寄存器集(GENET_RX_DESC_STATUS(位置索引));
        unsigned 长度 = (状态值 & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 边界位置值 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((状态值 & (边界位置值 | GENET_RX_DESC_STATUS_RX_ERROR)) != 边界位置值 || 长度 < 16 || 长度 > 1538) 有线值.统计值[4]++;
        else {
            清洁缓存(有线值.接收[位置索引], 长度, 1);
            struct pbuf *数据 = pbuf_alloc(PBUF_RAW, 长度 - 2, PBUF_POOL);
            if (!数据) 有线值.统计值[4]++;
            else if (pbuf_take(数据, 有线值.接收[位置索引] + 2, 长度 - 2) != ERR_OK || 设备->input(数据, 设备) != ERR_OK) {
                pbuf_free(数据); 有线值.统计值[4]++;
            } else { 有线值.统计值[0]++; 有线值.统计值[1] += 长度 - 2; }
        }
        接收中地址(位置索引); 同步化(); 有线值.消耗值++;
        有线寄存器集(GENET_RX_DMA_CONS_INDEX(循环编号)) = 有线值.消耗值;
    }
}
uint32_t 有线网络统计(unsigned 条目值) {
    return 条目值 < 5 ? 有线值.统计值[条目值] : 条目值 == 5 ? 有线值.速度值 : 条目值 == 6 ? 有线值.准备 : 0;
}
