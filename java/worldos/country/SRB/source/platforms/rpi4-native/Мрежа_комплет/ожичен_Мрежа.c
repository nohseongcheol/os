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
#include "ожичен_Мрежа.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Табла_рачунар_адреса(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(адреса) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (адреса)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, бафер_подесити_величину = 2048 };
static struct {
    unsigned char 받기[고리개수][бафер_подесити_величину];
    unsigned char послати[고리개수][бафер_подесити_величину];
    uint16_t 소비, 생산;
    int 물리주소, Припремити, 속도;
    uint32_t 집계[5];
    uintptr_t потврдити_Даље_ставка;
} ожичен_вриједност __attribute__((aligned(64)));

static void синхронизирати(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Јасноћа_кеш(void *подаци, unsigned дужина_вриједност, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)подаци + дужина_вриједност;
    for (uintptr_t адреса = (uintptr_t)подаци & ~(uintptr_t)63; адреса < 끝; адреса += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(адреса) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(адреса) : "memory");
    }
#else
    (void)подаци; (void)дужина_вриједност; (void)받기;
#endif
    синхронизирати();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned адреса, unsigned индекс, int Пише, unsigned вриједност) {
    uint32_t Наредба = (Пише ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (адреса << GENET_MDIO_ADDR_SHIFT) | (индекс << GENET_MDIO_REG_SHIFT) | (вриједност & 65535);
    유선저장기(GENET_MDIO_CMD) = Наредба;
    유선저장기(GENET_MDIO_CMD) = Наредба | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t стање_вриједност = 유선저장기(GENET_MDIO_CMD);
        if (!(стање_вриједност & GENET_MDIO_START_BUSY))
            return стање_вриједност & GENET_MDIO_READ_FAILED ? -1 : (int)(стање_вриједност & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned индекс) { return 물리전송(ожичен_вриједност.물리주소, индекс, 0, 0); }
static int 물리쓰기(unsigned индекс, unsigned вриједност) { return 물리전송(ожичен_вриједност.물리주소, индекс, 1, вриједност); }
static int 물리준비(void) {
    ожичен_вриједност.물리주소 = -1;
    for (unsigned адреса = 0; адреса < 32; адреса++) {
        int 식별 = 물리전송(адреса, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ожичен_вриједност.물리주소 = адреса; break; }
    }
    if (ожичен_вриједност.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int вриједност = 물리읽기(BRGPHY_MII_AUXCTL);
    if (вриједност < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (вриједност & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    вриједност = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (вриједност < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (вриједност & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Припремити_петља(unsigned постер_вриједност) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned петља_вриједност = постер_вриједност + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Положај = 0; Положај <= 0x30; Положај += 4) 유선저장기(петља_вриједност + Положај) = 0;
    유선저장기(петља_вриједност + 0x10) = (고리개수 << 16) | бафер_подесити_величину;
    유선저장기(петља_вриједност + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (постер_вриједност == GENET_RX_BASE) 유선저장기(петља_вриједност + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(петља_вриједност + 0x24) = 1;
    유선저장기(постер_вриједност + 0x104c) = 8;
    유선저장기(постер_вриједност + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned позиција_индекс) {
    uintptr_t адреса = (uintptr_t)ожичен_вриједност.받기[позиција_индекс];
    Јасноћа_кеш((void *)адреса, бафер_подесити_величину, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(позиција_индекс)) = (uint32_t)адреса;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(позиција_индекс)) = (uint64_t)адреса >> 32;
    유선저장기(GENET_RX_DESC_STATUS(позиција_индекс)) = бафер_подесити_величину << 16;
}
static err_t 전문보내기(struct netif *уређај_вриједност, struct pbuf *전문) {
    if (!ожичен_вриједност.Припремити || !netif_is_link_up(уређај_вриједност)) return ERR_RTE;
    unsigned Величина = 전문->tot_len;
    if (!Величина || Величина > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ожичен_вриједност.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned позиција_индекс = ожичен_вриједност.생산 % 고리개수, 송신길이 = Величина < 60 ? 60 : Величина;
    unsigned char *подаци = ожичен_вриједност.послати[позиција_индекс];
    memset(подаци, 0, 송신길이);
    if (pbuf_copy_partial(전문, подаци, Величина, 0) != Величина) return ERR_BUF;
    Јасноћа_кеш(подаци, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(позиција_индекс)) = (uint32_t)(uintptr_t)подаци;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(позиција_индекс)) = (uint64_t)(uintptr_t)подаци >> 32;
    유선저장기(GENET_TX_DESC_STATUS(позиција_индекс)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    синхронизирати();
    ожичен_вриједност.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ожичен_вриједност.생산;
    ожичен_вриједност.집계[2]++; ожичен_вриједност.집계[3] += Величина;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Припремити_ожичен_Мрежа(struct netif *уређај_вриједност) {
    unsigned char адреса[6];
    if (!유선장치있음() || !Табла_рачунар_адреса(адреса) || (адреса[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= адреса[순번];
    if (!합) return ERR_IF;
    memset(&ожичен_вриједност, 0, sizeof(ожичен_вриједност));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)адреса[0] << 24 | (uint32_t)адреса[1] << 16 | адреса[2] << 8 | адреса[3];
    유선저장기(GENET_UMAC_MAC1) = адреса[4] << 8 | адреса[5];
    Припремити_петља(GENET_TX_BASE); Припремити_петља(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    синхронизирати();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    уређај_вриједност->name[0] = 'e'; уређај_вриједност->name[1] = 'n'; уређај_вриједност->mtu = 1500;
    уређај_вриједност->hwaddr_len = 6; memcpy(уређај_вриједност->hwaddr, адреса, 6);
    уређај_вриједност->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    уређај_вриједност->output = etharp_output; уређај_вриједност->linkoutput = 전문보내기;
    ожичен_вриједност.Припремити = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *уређај_вриједност) {
    if (!ожичен_вриједност.Припремити) return;
    uintptr_t САДА_вриједност = 보드밀리초();
    if (САДА_вриједност >= ожичен_вриједност.потврдити_Даље_ставка) {
        ожичен_вриједност.потврдити_Даље_ставка = САДА_вриједност + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int стање_вриједност = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned метода_мод = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = метода_мод == 7 ? 1000 : метода_мод == 5 ? 100 : метода_мод == 2 ? 10 : 0;
        ожичен_вриједност.속도 = стање_вриједност >= 0 && (стање_вриједност & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ожичен_вриједност.속도) {
            uint32_t Поставке = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Поставке &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Поставке | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Поставке = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Поставке | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(уређај_вриједност)) netif_set_link_up(уређај_вриједност);
        } else if (netif_is_link_up(уређај_вриједност)) netif_set_link_down(уређај_вриједност);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ожичен_вриједност.소비);
    if (남음 > 고리개수) { ожичен_вриједност.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned позиција_индекс = ожичен_вриједност.소비 % 고리개수;
        синхронизирати();
        uint32_t стање_вриједност = 유선저장기(GENET_RX_DESC_STATUS(позиција_индекс));
        unsigned дужина_вриједност = (стање_вриједност & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((стање_вриједност & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || дужина_вриједност < 16 || дужина_вриједност > 1538) ожичен_вриједност.집계[4]++;
        else {
            Јасноћа_кеш(ожичен_вриједност.받기[позиција_индекс], дужина_вриједност, 1);
            struct pbuf *подаци = pbuf_alloc(PBUF_RAW, дужина_вриједност - 2, PBUF_POOL);
            if (!подаци) ожичен_вриједност.집계[4]++;
            else if (pbuf_take(подаци, ожичен_вриједност.받기[позиција_индекс] + 2, дужина_вриједност - 2) != ERR_OK || уређај_вриједност->input(подаци, уређај_вриједност) != ERR_OK) {
                pbuf_free(подаци); ожичен_вриједност.집계[4]++;
            } else { ожичен_вриједност.집계[0]++; ожичен_вриједност.집계[1] += дужина_вриједност - 2; }
        }
        받는주소(позиција_индекс); синхронизирати(); ожичен_вриједност.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ожичен_вриједност.소비;
    }
}
uint32_t 유선망집계(unsigned унос_вриједност) {
    return унос_вриједност < 5 ? ожичен_вриједност.집계[унос_вриједност] : унос_вриједност == 5 ? ожичен_вриједност.속도 : унос_вриједност == 6 ? ожичен_вриједност.Припремити : 0;
}
