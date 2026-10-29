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
#include "кабелен_мрежа.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Табло_реален_адрес(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(адрес) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (адрес)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, размер_на_буфера = 2048 };
static struct {
    unsigned char получавам[고리개수][размер_на_буфера];
    unsigned char изпращам[고리개수][размер_на_буфера];
    uint16_t използвам_стойност_84aa75c8, 생산;
    int 물리주소, Подготвяне, 속도;
    uint32_t 집계[5];
    uintptr_t проверявам_Следваща_артикул;
} кабелен_стойност __attribute__((aligned(64)));

static void синхронизирам(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Изостряне_кеш(void *данни, unsigned 길이, int получавам) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)данни + 길이;
    for (uintptr_t адрес = (uintptr_t)данни & ~(uintptr_t)63; адрес < 끝; адрес += 64) {
        if (получавам) __asm__ volatile("dc ivac, %0" :: "r"(адрес) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(адрес) : "memory");
    }
#else
    (void)данни; (void)길이; (void)получавам;
#endif
    синхронизирам();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned адрес, unsigned индекс, int Писане, unsigned стойност) {
    uint32_t Команда = (Писане ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (адрес << GENET_MDIO_ADDR_SHIFT) | (индекс << GENET_MDIO_REG_SHIFT) | (стойност & 65535);
    유선저장기(GENET_MDIO_CMD) = Команда;
    유선저장기(GENET_MDIO_CMD) = Команда | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Състояние_стойност = 유선저장기(GENET_MDIO_CMD);
        if (!(Състояние_стойност & GENET_MDIO_START_BUSY))
            return Състояние_стойност & GENET_MDIO_READ_FAILED ? -1 : (int)(Състояние_стойност & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned индекс) { return 물리전송(кабелен_стойност.물리주소, индекс, 0, 0); }
static int 물리쓰기(unsigned индекс, unsigned стойност) { return 물리전송(кабелен_стойност.물리주소, индекс, 1, стойност); }
static int 물리준비(void) {
    кабелен_стойност.물리주소 = -1;
    for (unsigned адрес = 0; адрес < 32; адрес++) {
        int 식별 = 물리전송(адрес, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { кабелен_стойност.물리주소 = адрес; break; }
    }
    if (кабелен_стойност.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int стойност = 물리읽기(BRGPHY_MII_AUXCTL);
    if (стойност < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (стойност & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    стойност = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (стойност < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (стойност & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Подготвяне_цикъл(unsigned Фон_стойност) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned цикъл_стойност = Фон_стойност + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Позиция = 0; Позиция <= 0x30; Позиция += 4) 유선저장기(цикъл_стойност + Позиция) = 0;
    유선저장기(цикъл_стойност + 0x10) = (고리개수 << 16) | размер_на_буфера;
    유선저장기(цикъл_стойност + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Фон_стойност == GENET_RX_BASE) 유선저장기(цикъл_стойност + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(цикъл_стойност + 0x24) = 1;
    유선저장기(Фон_стойност + 0x104c) = 8;
    유선저장기(Фон_стойност + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned позиционен_указател) {
    uintptr_t адрес = (uintptr_t)кабелен_стойност.получавам[позиционен_указател];
    Изостряне_кеш((void *)адрес, размер_на_буфера, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(позиционен_указател)) = (uint32_t)адрес;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(позиционен_указател)) = (uint64_t)адрес >> 32;
    유선저장기(GENET_RX_DESC_STATUS(позиционен_указател)) = размер_на_буфера << 16;
}
static err_t изпращам_дейтаграма(struct netif *устройство_стойност, struct pbuf *дейтаграма) {
    if (!кабелен_стойност.Подготвяне || !netif_is_link_up(устройство_стойност)) return ERR_RTE;
    unsigned Размер = дейтаграма->tot_len;
    if (!Размер || Размер > 1536) return ERR_BUF;
    uint16_t използвам_стойност_84aa75c8 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(кабелен_стойност.생산 - използвам_стойност_84aa75c8) >= 고리개수 - 1) return ERR_MEM;
    unsigned позиционен_указател = кабелен_стойност.생산 % 고리개수, 송신길이 = Размер < 60 ? 60 : Размер;
    unsigned char *данни = кабелен_стойност.изпращам[позиционен_указател];
    memset(данни, 0, 송신길이);
    if (pbuf_copy_partial(дейтаграма, данни, Размер, 0) != Размер) return ERR_BUF;
    Изостряне_кеш(данни, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(позиционен_указател)) = (uint32_t)(uintptr_t)данни;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(позиционен_указател)) = (uint64_t)(uintptr_t)данни >> 32;
    유선저장기(GENET_TX_DESC_STATUS(позиционен_указател)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    синхронизирам();
    кабелен_стойност.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = кабелен_стойност.생산;
    кабелен_стойност.집계[2]++; кабелен_стойност.집계[3] += Размер;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Подготвяне_кабелен_мрежа(struct netif *устройство_стойност) {
    unsigned char адрес[6];
    if (!유선장치있음() || !Табло_реален_адрес(адрес) || (адрес[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= адрес[순번];
    if (!합) return ERR_IF;
    memset(&кабелен_стойност, 0, sizeof(кабелен_стойност));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t първоначално_състояние = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = първоначално_състояние | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = първоначално_състояние & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)адрес[0] << 24 | (uint32_t)адрес[1] << 16 | адрес[2] << 8 | адрес[3];
    유선저장기(GENET_UMAC_MAC1) = адрес[4] << 8 | адрес[5];
    Подготвяне_цикъл(GENET_TX_BASE); Подготвяне_цикъл(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    синхронизирам();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    устройство_стойност->name[0] = 'e'; устройство_стойност->name[1] = 'n'; устройство_стойност->mtu = 1500;
    устройство_стойност->hwaddr_len = 6; memcpy(устройство_стойност->hwaddr, адрес, 6);
    устройство_стойност->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    устройство_стойност->output = etharp_output; устройство_стойност->linkoutput = изпращам_дейтаграма;
    кабелен_стойност.Подготвяне = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *устройство_стойност) {
    if (!кабелен_стойност.Подготвяне) return;
    uintptr_t СЕГА_стойност = 보드밀리초();
    if (СЕГА_стойност >= кабелен_стойност.проверявам_Следваща_артикул) {
        кабелен_стойност.проверявам_Следваща_артикул = СЕГА_стойност + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Състояние_стойност = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned метод_режим = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = метод_режим == 7 ? 1000 : метод_режим == 5 ? 100 : метод_режим == 2 ? 10 : 0;
        кабелен_стойност.속도 = Състояние_стойност >= 0 && (Състояние_стойност & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (кабелен_стойност.속도) {
            uint32_t Настройки = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Настройки &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Настройки | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Настройки = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Настройки | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(устройство_стойност)) netif_set_link_up(устройство_стойност);
        } else if (netif_is_link_up(устройство_стойност)) netif_set_link_down(устройство_стойност);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - кабелен_стойност.използвам_стойност_84aa75c8);
    if (남음 > 고리개수) { кабелен_стойност.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned позиционен_указател = кабелен_стойност.използвам_стойност_84aa75c8 % 고리개수;
        синхронизирам();
        uint32_t Състояние_стойност = 유선저장기(GENET_RX_DESC_STATUS(позиционен_указател));
        unsigned 길이 = (Състояние_стойност & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Състояние_стойност & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || 길이 < 16 || 길이 > 1538) кабелен_стойност.집계[4]++;
        else {
            Изостряне_кеш(кабелен_стойност.получавам[позиционен_указател], 길이, 1);
            struct pbuf *данни = pbuf_alloc(PBUF_RAW, 길이 - 2, PBUF_POOL);
            if (!данни) кабелен_стойност.집계[4]++;
            else if (pbuf_take(данни, кабелен_стойност.получавам[позиционен_указател] + 2, 길이 - 2) != ERR_OK || устройство_стойност->input(данни, устройство_стойност) != ERR_OK) {
                pbuf_free(данни); кабелен_стойност.집계[4]++;
            } else { кабелен_стойност.집계[0]++; кабелен_стойност.집계[1] += 길이 - 2; }
        }
        받는주소(позиционен_указател); синхронизирам(); кабелен_стойност.използвам_стойност_84aa75c8++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = кабелен_стойност.използвам_стойност_84aa75c8;
    }
}
uint32_t 유선망집계(unsigned запис_стойност) {
    return запис_стойност < 5 ? кабелен_стойност.집계[запис_стойност] : запис_стойност == 5 ? кабелен_стойност.속도 : запис_стойност == 6 ? кабелен_стойност.Подготвяне : 0;
}
