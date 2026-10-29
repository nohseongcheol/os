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
#include "проводовий_мережа.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Дошка_дійсна_адреса(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(Адреса) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (Адреса)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, розмір_буфера = 2048 };
static struct {
    unsigned char отримувати[고리개수][розмір_буфера];
    unsigned char надсилати[고리개수][розмір_буфера];
    uint16_t використовувати_значення, 생산;
    int 물리주소, Готувати, 속도;
    uint32_t 집계[5];
    uintptr_t перевіряти_Далі_елемент;
} проводовий_значення __attribute__((aligned(64)));

static void синхронізувати(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Різкість_кеш(void *дані, unsigned 길이, int отримувати) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)дані + 길이;
    for (uintptr_t Адреса = (uintptr_t)дані & ~(uintptr_t)63; Адреса < 끝; Адреса += 64) {
        if (отримувати) __asm__ volatile("dc ivac, %0" :: "r"(Адреса) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(Адреса) : "memory");
    }
#else
    (void)дані; (void)길이; (void)отримувати;
#endif
    синхронізувати();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned Адреса, unsigned індекс, int Запис, unsigned значення) {
    uint32_t команда = (Запис ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (Адреса << GENET_MDIO_ADDR_SHIFT) | (індекс << GENET_MDIO_REG_SHIFT) | (значення & 65535);
    유선저장기(GENET_MDIO_CMD) = команда;
    유선저장기(GENET_MDIO_CMD) = команда | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Стан_значення = 유선저장기(GENET_MDIO_CMD);
        if (!(Стан_значення & GENET_MDIO_START_BUSY))
            return Стан_значення & GENET_MDIO_READ_FAILED ? -1 : (int)(Стан_значення & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned індекс) { return 물리전송(проводовий_значення.물리주소, індекс, 0, 0); }
static int 물리쓰기(unsigned індекс, unsigned значення) { return 물리전송(проводовий_значення.물리주소, індекс, 1, значення); }
static int 물리준비(void) {
    проводовий_значення.물리주소 = -1;
    for (unsigned Адреса = 0; Адреса < 32; Адреса++) {
        int 식별 = 물리전송(Адреса, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { проводовий_значення.물리주소 = Адреса; break; }
    }
    if (проводовий_значення.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int значення = 물리읽기(BRGPHY_MII_AUXCTL);
    if (значення < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (значення & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    значення = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (значення < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (значення & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Готувати_цикл(unsigned Фон_значення) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned цикл_значення_201e2521 = Фон_значення + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned позиція = 0; позиція <= 0x30; позиція += 4) 유선저장기(цикл_значення_201e2521 + позиція) = 0;
    유선저장기(цикл_значення_201e2521 + 0x10) = (고리개수 << 16) | розмір_буфера;
    유선저장기(цикл_значення_201e2521 + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Фон_значення == GENET_RX_BASE) 유선저장기(цикл_значення_201e2521 + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(цикл_значення_201e2521 + 0x24) = 1;
    유선저장기(Фон_значення + 0x104c) = 8;
    유선저장기(Фон_значення + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned індекс_розташування) {
    uintptr_t Адреса = (uintptr_t)проводовий_значення.отримувати[індекс_розташування];
    Різкість_кеш((void *)Адреса, розмір_буфера, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(індекс_розташування)) = (uint32_t)Адреса;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(індекс_розташування)) = (uint64_t)Адреса >> 32;
    유선저장기(GENET_RX_DESC_STATUS(індекс_розташування)) = розмір_буфера << 16;
}
static err_t надсилати_дейтаграма(struct netif *пристрій_значення, struct pbuf *дейтаграма) {
    if (!проводовий_значення.Готувати || !netif_is_link_up(пристрій_значення)) return ERR_RTE;
    unsigned Розмір = дейтаграма->tot_len;
    if (!Розмір || Розмір > 1536) return ERR_BUF;
    uint16_t використовувати_значення = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(проводовий_значення.생산 - використовувати_значення) >= 고리개수 - 1) return ERR_MEM;
    unsigned індекс_розташування = проводовий_значення.생산 % 고리개수, 송신길이 = Розмір < 60 ? 60 : Розмір;
    unsigned char *дані = проводовий_значення.надсилати[індекс_розташування];
    memset(дані, 0, 송신길이);
    if (pbuf_copy_partial(дейтаграма, дані, Розмір, 0) != Розмір) return ERR_BUF;
    Різкість_кеш(дані, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(індекс_розташування)) = (uint32_t)(uintptr_t)дані;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(індекс_розташування)) = (uint64_t)(uintptr_t)дані >> 32;
    유선저장기(GENET_TX_DESC_STATUS(індекс_розташування)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    синхронізувати();
    проводовий_значення.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = проводовий_значення.생산;
    проводовий_значення.집계[2]++; проводовий_значення.집계[3] += Розмір;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Готувати_проводовий_мережа(struct netif *пристрій_значення) {
    unsigned char Адреса[6];
    if (!유선장치있음() || !Дошка_дійсна_адреса(Адреса) || (Адреса[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= Адреса[순번];
    if (!합) return ERR_IF;
    memset(&проводовий_значення, 0, sizeof(проводовий_значення));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t початковий_стан = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = початковий_стан | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = початковий_стан & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)Адреса[0] << 24 | (uint32_t)Адреса[1] << 16 | Адреса[2] << 8 | Адреса[3];
    유선저장기(GENET_UMAC_MAC1) = Адреса[4] << 8 | Адреса[5];
    Готувати_цикл(GENET_TX_BASE); Готувати_цикл(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    синхронізувати();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    пристрій_значення->name[0] = 'e'; пристрій_значення->name[1] = 'n'; пристрій_значення->mtu = 1500;
    пристрій_значення->hwaddr_len = 6; memcpy(пристрій_значення->hwaddr, Адреса, 6);
    пристрій_значення->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    пристрій_значення->output = etharp_output; пристрій_значення->linkoutput = надсилати_дейтаграма;
    проводовий_значення.Готувати = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *пристрій_значення) {
    if (!проводовий_значення.Готувати) return;
    uintptr_t ЗАРАЗ_значення = 보드밀리초();
    if (ЗАРАЗ_значення >= проводовий_значення.перевіряти_Далі_елемент) {
        проводовий_значення.перевіряти_Далі_елемент = ЗАРАЗ_значення + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Стан_значення = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned метод_режим = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = метод_режим == 7 ? 1000 : метод_режим == 5 ? 100 : метод_режим == 2 ? 10 : 0;
        проводовий_значення.속도 = Стан_значення >= 0 && (Стан_значення & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (проводовий_значення.속도) {
            uint32_t Налаштування = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Налаштування &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Налаштування | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Налаштування = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Налаштування | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(пристрій_значення)) netif_set_link_up(пристрій_значення);
        } else if (netif_is_link_up(пристрій_значення)) netif_set_link_down(пристрій_значення);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - проводовий_значення.використовувати_значення);
    if (남음 > 고리개수) { проводовий_значення.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned індекс_розташування = проводовий_значення.використовувати_значення % 고리개수;
        синхронізувати();
        uint32_t Стан_значення = 유선저장기(GENET_RX_DESC_STATUS(індекс_розташування));
        unsigned 길이 = (Стан_значення & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Стан_значення & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || 길이 < 16 || 길이 > 1538) проводовий_значення.집계[4]++;
        else {
            Різкість_кеш(проводовий_значення.отримувати[індекс_розташування], 길이, 1);
            struct pbuf *дані = pbuf_alloc(PBUF_RAW, 길이 - 2, PBUF_POOL);
            if (!дані) проводовий_значення.집계[4]++;
            else if (pbuf_take(дані, проводовий_значення.отримувати[індекс_розташування] + 2, 길이 - 2) != ERR_OK || пристрій_значення->input(дані, пристрій_значення) != ERR_OK) {
                pbuf_free(дані); проводовий_значення.집계[4]++;
            } else { проводовий_значення.집계[0]++; проводовий_значення.집계[1] += 길이 - 2; }
        }
        받는주소(індекс_розташування); синхронізувати(); проводовий_значення.використовувати_значення++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = проводовий_значення.використовувати_значення;
    }
}
uint32_t 유선망집계(unsigned запис_значення_962f286b) {
    return запис_значення_962f286b < 5 ? проводовий_значення.집계[запис_значення_962f286b] : запис_значення_962f286b == 5 ? проводовий_значення.속도 : запис_значення_962f286b == 6 ? проводовий_значення.Готувати : 0;
}
