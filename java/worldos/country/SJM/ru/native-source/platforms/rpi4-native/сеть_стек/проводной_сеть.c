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
#include "проводной_сеть.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Доска_абсолютный_адрес(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(АДРЕС) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (АДРЕС)))
#endif
enum { 고리번호 = 16, Loop_СЧЁТ = 256, размер_буфера = 2048 };
static struct {
    unsigned char получить[Loop_СЧЁТ][размер_буфера];
    unsigned char написать[Loop_СЧЁТ][размер_буфера];
    uint16_t потребление_ЗНАЧЕН, 생산;
    int 물리주소, Подготовить, 속도;
    uint32_t Статистика_ЗНАЧЕН[5];
    uintptr_t проверять_Далее_товар;
} проводной_ЗНАЧЕН __attribute__((aligned(64)));

static void синхронизировать(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void ПЕЧСИМВ_кэш(void *данные, unsigned длина_ЗНАЧЕН, int получить) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)данные + длина_ЗНАЧЕН;
    for (uintptr_t АДРЕС = (uintptr_t)данные & ~(uintptr_t)63; АДРЕС < 끝; АДРЕС += 64) {
        if (получить) __asm__ volatile("dc ivac, %0" :: "r"(АДРЕС) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(АДРЕС) : "memory");
    }
#else
    (void)данные; (void)длина_ЗНАЧЕН; (void)получить;
#endif
    синхронизировать();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned АДРЕС, unsigned ИНДЕКС, int Запись, unsigned ЗНАЧЕН) {
    uint32_t команда = (Запись ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (АДРЕС << GENET_MDIO_ADDR_SHIFT) | (ИНДЕКС << GENET_MDIO_REG_SHIFT) | (ЗНАЧЕН & 65535);
    유선저장기(GENET_MDIO_CMD) = команда;
    유선저장기(GENET_MDIO_CMD) = команда | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Состояние_ЗНАЧЕН = 유선저장기(GENET_MDIO_CMD);
        if (!(Состояние_ЗНАЧЕН & GENET_MDIO_START_BUSY))
            return Состояние_ЗНАЧЕН & GENET_MDIO_READ_FAILED ? -1 : (int)(Состояние_ЗНАЧЕН & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ИНДЕКС) { return 물리전송(проводной_ЗНАЧЕН.물리주소, ИНДЕКС, 0, 0); }
static int 물리쓰기(unsigned ИНДЕКС, unsigned ЗНАЧЕН) { return 물리전송(проводной_ЗНАЧЕН.물리주소, ИНДЕКС, 1, ЗНАЧЕН); }
static int 물리준비(void) {
    проводной_ЗНАЧЕН.물리주소 = -1;
    for (unsigned АДРЕС = 0; АДРЕС < 32; АДРЕС++) {
        int 식별 = 물리전송(АДРЕС, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { проводной_ЗНАЧЕН.물리주소 = АДРЕС; break; }
    }
    if (проводной_ЗНАЧЕН.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ЗНАЧЕН = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ЗНАЧЕН < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ЗНАЧЕН & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ЗНАЧЕН = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ЗНАЧЕН < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ЗНАЧЕН & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Подготовить_Loop(unsigned фон_ЗНАЧЕН) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_ЗНАЧЕН = фон_ЗНАЧЕН + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned позиция = 0; позиция <= 0x30; позиция += 4) 유선저장기(Loop_ЗНАЧЕН + позиция) = 0;
    유선저장기(Loop_ЗНАЧЕН + 0x10) = (Loop_СЧЁТ << 16) | размер_буфера;
    유선저장기(Loop_ЗНАЧЕН + 0x1c) = Loop_СЧЁТ * GENET_DMA_DESC_SIZE / 4 - 1;
    if (фон_ЗНАЧЕН == GENET_RX_BASE) 유선저장기(Loop_ЗНАЧЕН + 0x28) = (5 << 16) | (Loop_СЧЁТ >> 4);
    else 유선저장기(Loop_ЗНАЧЕН + 0x24) = 1;
    유선저장기(фон_ЗНАЧЕН + 0x104c) = 8;
    유선저장기(фон_ЗНАЧЕН + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned позиция_ИНДЕКС) {
    uintptr_t АДРЕС = (uintptr_t)проводной_ЗНАЧЕН.получить[позиция_ИНДЕКС];
    ПЕЧСИМВ_кэш((void *)АДРЕС, размер_буфера, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(позиция_ИНДЕКС)) = (uint32_t)АДРЕС;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(позиция_ИНДЕКС)) = (uint64_t)АДРЕС >> 32;
    유선저장기(GENET_RX_DESC_STATUS(позиция_ИНДЕКС)) = размер_буфера << 16;
}
static err_t написать_датаграмма(struct netif *устройство_ЗНАЧЕН, struct pbuf *датаграмма) {
    if (!проводной_ЗНАЧЕН.Подготовить || !netif_is_link_up(устройство_ЗНАЧЕН)) return ERR_RTE;
    unsigned Размер = датаграмма->tot_len;
    if (!Размер || Размер > 1536) return ERR_BUF;
    uint16_t потребление_ЗНАЧЕН = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(проводной_ЗНАЧЕН.생산 - потребление_ЗНАЧЕН) >= Loop_СЧЁТ - 1) return ERR_MEM;
    unsigned позиция_ИНДЕКС = проводной_ЗНАЧЕН.생산 % Loop_СЧЁТ, 송신길이 = Размер < 60 ? 60 : Размер;
    unsigned char *данные = проводной_ЗНАЧЕН.написать[позиция_ИНДЕКС];
    memset(данные, 0, 송신길이);
    if (pbuf_copy_partial(датаграмма, данные, Размер, 0) != Размер) return ERR_BUF;
    ПЕЧСИМВ_кэш(данные, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(позиция_ИНДЕКС)) = (uint32_t)(uintptr_t)данные;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(позиция_ИНДЕКС)) = (uint64_t)(uintptr_t)данные >> 32;
    유선저장기(GENET_TX_DESC_STATUS(позиция_ИНДЕКС)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    синхронизировать();
    проводной_ЗНАЧЕН.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = проводной_ЗНАЧЕН.생산;
    проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[2]++; проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[3] += Размер;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Подготовить_проводной_сеть(struct netif *устройство_ЗНАЧЕН) {
    unsigned char АДРЕС[6];
    if (!유선장치있음() || !Доска_абсолютный_адрес(АДРЕС) || (АДРЕС[0] & 1)) return ERR_IF;
    unsigned SUM_ЗНАЧЕН = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_ЗНАЧЕН |= АДРЕС[순번];
    if (!SUM_ЗНАЧЕН) return ERR_IF;
    memset(&проводной_ЗНАЧЕН, 0, sizeof(проводной_ЗНАЧЕН));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t начальное_состояние = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = начальное_состояние | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = начальное_состояние & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)АДРЕС[0] << 24 | (uint32_t)АДРЕС[1] << 16 | АДРЕС[2] << 8 | АДРЕС[3];
    유선저장기(GENET_UMAC_MAC1) = АДРЕС[4] << 8 | АДРЕС[5];
    Подготовить_Loop(GENET_TX_BASE); Подготовить_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_СЧЁТ; 순번++) 받는주소(순번);
    синхронизировать();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    устройство_ЗНАЧЕН->name[0] = 'e'; устройство_ЗНАЧЕН->name[1] = 'n'; устройство_ЗНАЧЕН->mtu = 1500;
    устройство_ЗНАЧЕН->hwaddr_len = 6; memcpy(устройство_ЗНАЧЕН->hwaddr, АДРЕС, 6);
    устройство_ЗНАЧЕН->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    устройство_ЗНАЧЕН->output = etharp_output; устройство_ЗНАЧЕН->linkoutput = написать_датаграмма;
    проводной_ЗНАЧЕН.Подготовить = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *устройство_ЗНАЧЕН) {
    if (!проводной_ЗНАЧЕН.Подготовить) return;
    uintptr_t ТДАТА_ЗНАЧЕН = 보드밀리초();
    if (ТДАТА_ЗНАЧЕН >= проводной_ЗНАЧЕН.проверять_Далее_товар) {
        проводной_ЗНАЧЕН.проверять_Далее_товар = ТДАТА_ЗНАЧЕН + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Состояние_ЗНАЧЕН = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned метод_МОДА = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = метод_МОДА == 7 ? 1000 : метод_МОДА == 5 ? 100 : метод_МОДА == 2 ? 10 : 0;
        проводной_ЗНАЧЕН.속도 = Состояние_ЗНАЧЕН >= 0 && (Состояние_ЗНАЧЕН & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (проводной_ЗНАЧЕН.속도) {
            uint32_t Настройки = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Настройки &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Настройки | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Настройки = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Настройки | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(устройство_ЗНАЧЕН)) netif_set_link_up(устройство_ЗНАЧЕН);
        } else if (netif_is_link_up(устройство_ЗНАЧЕН)) netif_set_link_down(устройство_ЗНАЧЕН);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - проводной_ЗНАЧЕН.потребление_ЗНАЧЕН);
    if (남음 > Loop_СЧЁТ) { проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned позиция_ИНДЕКС = проводной_ЗНАЧЕН.потребление_ЗНАЧЕН % Loop_СЧЁТ;
        синхронизировать();
        uint32_t Состояние_ЗНАЧЕН = 유선저장기(GENET_RX_DESC_STATUS(позиция_ИНДЕКС));
        unsigned длина_ЗНАЧЕН = (Состояние_ЗНАЧЕН & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t граница_ЗНАЧЕН = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Состояние_ЗНАЧЕН & (граница_ЗНАЧЕН | GENET_RX_DESC_STATUS_RX_ERROR)) != граница_ЗНАЧЕН || длина_ЗНАЧЕН < 16 || длина_ЗНАЧЕН > 1538) проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[4]++;
        else {
            ПЕЧСИМВ_кэш(проводной_ЗНАЧЕН.получить[позиция_ИНДЕКС], длина_ЗНАЧЕН, 1);
            struct pbuf *данные = pbuf_alloc(PBUF_RAW, длина_ЗНАЧЕН - 2, PBUF_POOL);
            if (!данные) проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[4]++;
            else if (pbuf_take(данные, проводной_ЗНАЧЕН.получить[позиция_ИНДЕКС] + 2, длина_ЗНАЧЕН - 2) != ERR_OK || устройство_ЗНАЧЕН->input(данные, устройство_ЗНАЧЕН) != ERR_OK) {
                pbuf_free(данные); проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[4]++;
            } else { проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[0]++; проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[1] += длина_ЗНАЧЕН - 2; }
        }
        받는주소(позиция_ИНДЕКС); синхронизировать(); проводной_ЗНАЧЕН.потребление_ЗНАЧЕН++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = проводной_ЗНАЧЕН.потребление_ЗНАЧЕН;
    }
}
uint32_t проводной_сеть_Статистика(unsigned ввод_ЗНАЧЕН) {
    return ввод_ЗНАЧЕН < 5 ? проводной_ЗНАЧЕН.Статистика_ЗНАЧЕН[ввод_ЗНАЧЕН] : ввод_ЗНАЧЕН == 5 ? проводной_ЗНАЧЕН.속도 : ввод_ЗНАЧЕН == 6 ? проводной_ЗНАЧЕН.Подготовить : 0;
}
