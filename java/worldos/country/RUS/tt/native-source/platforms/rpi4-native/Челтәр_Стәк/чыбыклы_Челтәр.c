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
#include "чыбыклы_Челтәр.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int такта_машина_адрес(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(адрес) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (адрес)))
#endif
enum { 고리번호 = 16, Loop_COUNT = 256, буфер_үлчәмен_үзгәртү = 2048 };
static struct {
    unsigned char 받기[Loop_COUNT][буфер_үлчәмен_үзгәртү];
    unsigned char җибәрү[Loop_COUNT][буфер_үлчәмен_үзгәртү];
    uint16_t 소비, 생산;
    int 물리주소, Әзерләү, 속도;
    uint32_t 집계[5];
    uintptr_t раслау_Киләсе_элемент;
} чыбыклы_VALUE __attribute__((aligned(64)));

static void синхронлаштыру(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_кәш(void *мәгълүмат, unsigned озынлык_VALUE, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)мәгълүмат + озынлык_VALUE;
    for (uintptr_t адрес = (uintptr_t)мәгълүмат & ~(uintptr_t)63; адрес < 끝; адрес += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(адрес) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(адрес) : "memory");
    }
#else
    (void)мәгълүмат; (void)озынлык_VALUE; (void)받기;
#endif
    синхронлаштыру();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned адрес, unsigned INDEX, int язу, unsigned VALUE) {
    uint32_t команда = (язу ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (адрес << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALUE & 65535);
    유선저장기(GENET_MDIO_CMD) = команда;
    유선저장기(GENET_MDIO_CMD) = команда | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t халәт_VALUE = 유선저장기(GENET_MDIO_CMD);
        if (!(халәт_VALUE & GENET_MDIO_START_BUSY))
            return халәт_VALUE & GENET_MDIO_READ_FAILED ? -1 : (int)(халәт_VALUE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(чыбыклы_VALUE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALUE) { return 물리전송(чыбыклы_VALUE.물리주소, INDEX, 1, VALUE); }
static int 물리준비(void) {
    чыбыклы_VALUE.물리주소 = -1;
    for (unsigned адрес = 0; адрес < 32; адрес++) {
        int 식별 = 물리전송(адрес, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { чыбыклы_VALUE.물리주소 = адрес; break; }
    }
    if (чыбыклы_VALUE.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VALUE = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VALUE < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VALUE & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VALUE = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VALUE < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VALUE & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Әзерләү_Loop(unsigned Фон_VALUE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALUE = Фон_VALUE + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned урнаштыру = 0; урнаштыру <= 0x30; урнаштыру += 4) 유선저장기(Loop_VALUE + урнаштыру) = 0;
    유선저장기(Loop_VALUE + 0x10) = (Loop_COUNT << 16) | буфер_үлчәмен_үзгәртү;
    유선저장기(Loop_VALUE + 0x1c) = Loop_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Фон_VALUE == GENET_RX_BASE) 유선저장기(Loop_VALUE + 0x28) = (5 << 16) | (Loop_COUNT >> 4);
    else 유선저장기(Loop_VALUE + 0x24) = 1;
    유선저장기(Фон_VALUE + 0x104c) = 8;
    유선저장기(Фон_VALUE + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned урнаштыру_INDEX) {
    uintptr_t адрес = (uintptr_t)чыбыклы_VALUE.받기[урнаштыру_INDEX];
    CLEAN_кәш((void *)адрес, буфер_үлчәмен_үзгәртү, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(урнаштыру_INDEX)) = (uint32_t)адрес;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(урнаштыру_INDEX)) = (uint64_t)адрес >> 32;
    유선저장기(GENET_RX_DESC_STATUS(урнаштыру_INDEX)) = буфер_үлчәмен_үзгәртү << 16;
}
static err_t 전문보내기(struct netif *мобиль_VALUE, struct pbuf *전문) {
    if (!чыбыклы_VALUE.Әзерләү || !netif_is_link_up(мобиль_VALUE)) return ERR_RTE;
    unsigned үлчәмен_үзгәртү = 전문->tot_len;
    if (!үлчәмен_үзгәртү || үлчәмен_үзгәртү > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(чыбыклы_VALUE.생산 - 소비) >= Loop_COUNT - 1) return ERR_MEM;
    unsigned урнаштыру_INDEX = чыбыклы_VALUE.생산 % Loop_COUNT, 송신길이 = үлчәмен_үзгәртү < 60 ? 60 : үлчәмен_үзгәртү;
    unsigned char *мәгълүмат = чыбыклы_VALUE.җибәрү[урнаштыру_INDEX];
    memset(мәгълүмат, 0, 송신길이);
    if (pbuf_copy_partial(전문, мәгълүмат, үлчәмен_үзгәртү, 0) != үлчәмен_үзгәртү) return ERR_BUF;
    CLEAN_кәш(мәгълүмат, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(урнаштыру_INDEX)) = (uint32_t)(uintptr_t)мәгълүмат;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(урнаштыру_INDEX)) = (uint64_t)(uintptr_t)мәгълүмат >> 32;
    유선저장기(GENET_TX_DESC_STATUS(урнаштыру_INDEX)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    синхронлаштыру();
    чыбыклы_VALUE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = чыбыклы_VALUE.생산;
    чыбыклы_VALUE.집계[2]++; чыбыклы_VALUE.집계[3] += үлчәмен_үзгәртү;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Әзерләү_чыбыклы_Челтәр(struct netif *мобиль_VALUE) {
    unsigned char адрес[6];
    if (!유선장치있음() || !такта_машина_адрес(адрес) || (адрес[0] & 1)) return ERR_IF;
    unsigned SUM_VALUE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALUE |= адрес[순번];
    if (!SUM_VALUE) return ERR_IF;
    memset(&чыбыклы_VALUE, 0, sizeof(чыбыклы_VALUE));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)адрес[0] << 24 | (uint32_t)адрес[1] << 16 | адрес[2] << 8 | адрес[3];
    유선저장기(GENET_UMAC_MAC1) = адрес[4] << 8 | адрес[5];
    Әзерләү_Loop(GENET_TX_BASE); Әзерләү_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COUNT; 순번++) 받는주소(순번);
    синхронлаштыру();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    мобиль_VALUE->name[0] = 'e'; мобиль_VALUE->name[1] = 'n'; мобиль_VALUE->mtu = 1500;
    мобиль_VALUE->hwaddr_len = 6; memcpy(мобиль_VALUE->hwaddr, адрес, 6);
    мобиль_VALUE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    мобиль_VALUE->output = etharp_output; мобиль_VALUE->linkoutput = 전문보내기;
    чыбыклы_VALUE.Әзерләү = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *мобиль_VALUE) {
    if (!чыбыклы_VALUE.Әзерләү) return;
    uintptr_t NOW_VALUE = 보드밀리초();
    if (NOW_VALUE >= чыбыклы_VALUE.раслау_Киләсе_элемент) {
        чыбыклы_VALUE.раслау_Киләсе_элемент = NOW_VALUE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int халәт_VALUE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ысул_MODE = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ысул_MODE == 7 ? 1000 : ысул_MODE == 5 ? 100 : ысул_MODE == 2 ? 10 : 0;
        чыбыклы_VALUE.속도 = халәт_VALUE >= 0 && (халәт_VALUE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (чыбыклы_VALUE.속도) {
            uint32_t Caylaw = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Caylaw &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Caylaw | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Caylaw = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Caylaw | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(мобиль_VALUE)) netif_set_link_up(мобиль_VALUE);
        } else if (netif_is_link_up(мобиль_VALUE)) netif_set_link_down(мобиль_VALUE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - чыбыклы_VALUE.소비);
    if (남음 > Loop_COUNT) { чыбыклы_VALUE.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned урнаштыру_INDEX = чыбыклы_VALUE.소비 % Loop_COUNT;
        синхронлаштыру();
        uint32_t халәт_VALUE = 유선저장기(GENET_RX_DESC_STATUS(урнаштыру_INDEX));
        unsigned озынлык_VALUE = (халәт_VALUE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((халәт_VALUE & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || озынлык_VALUE < 16 || озынлык_VALUE > 1538) чыбыклы_VALUE.집계[4]++;
        else {
            CLEAN_кәш(чыбыклы_VALUE.받기[урнаштыру_INDEX], озынлык_VALUE, 1);
            struct pbuf *мәгълүмат = pbuf_alloc(PBUF_RAW, озынлык_VALUE - 2, PBUF_POOL);
            if (!мәгълүмат) чыбыклы_VALUE.집계[4]++;
            else if (pbuf_take(мәгълүмат, чыбыклы_VALUE.받기[урнаштыру_INDEX] + 2, озынлык_VALUE - 2) != ERR_OK || мобиль_VALUE->input(мәгълүмат, мобиль_VALUE) != ERR_OK) {
                pbuf_free(мәгълүмат); чыбыклы_VALUE.집계[4]++;
            } else { чыбыклы_VALUE.집계[0]++; чыбыклы_VALUE.집계[1] += озынлык_VALUE - 2; }
        }
        받는주소(урнаштыру_INDEX); синхронлаштыру(); чыбыклы_VALUE.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = чыбыклы_VALUE.소비;
    }
}
uint32_t 유선망집계(unsigned кертү_VALUE) {
    return кертү_VALUE < 5 ? чыбыклы_VALUE.집계[кертү_VALUE] : кертү_VALUE == 5 ? чыбыклы_VALUE.속도 : кертү_VALUE == 6 ? чыбыклы_VALUE.Әзерләү : 0;
}
