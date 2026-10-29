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
#include "сымды_желі.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Тақта_нақпа_нақ_мекенжай(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(мекенжай) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (мекенжай)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, буфер_өлшемі = 2048 };
static struct {
    unsigned char 받기[고리개수][буфер_өлшемі];
    unsigned char жіберу[고리개수][буфер_өлшемі];
    uint16_t пайдалану_мән, 생산;
    int 물리주소, Дайындау, 속도;
    uint32_t 집계[5];
    uintptr_t тексеру_Келесі_элемент;
} сымды_мән __attribute__((aligned(64)));

static void үндестіру(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Анықтық_кэш(void *деректер, unsigned ұзындық_мән, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)деректер + ұзындық_мән;
    for (uintptr_t мекенжай = (uintptr_t)деректер & ~(uintptr_t)63; мекенжай < 끝; мекенжай += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(мекенжай) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(мекенжай) : "memory");
    }
#else
    (void)деректер; (void)ұзындық_мән; (void)받기;
#endif
    үндестіру();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned мекенжай, unsigned индекс, int Жазу, unsigned мән) {
    uint32_t Команда = (Жазу ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (мекенжай << GENET_MDIO_ADDR_SHIFT) | (индекс << GENET_MDIO_REG_SHIFT) | (мән & 65535);
    유선저장기(GENET_MDIO_CMD) = Команда;
    유선저장기(GENET_MDIO_CMD) = Команда | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t күй_мән = 유선저장기(GENET_MDIO_CMD);
        if (!(күй_мән & GENET_MDIO_START_BUSY))
            return күй_мән & GENET_MDIO_READ_FAILED ? -1 : (int)(күй_мән & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned индекс) { return 물리전송(сымды_мән.물리주소, индекс, 0, 0); }
static int 물리쓰기(unsigned индекс, unsigned мән) { return 물리전송(сымды_мән.물리주소, индекс, 1, мән); }
static int 물리준비(void) {
    сымды_мән.물리주소 = -1;
    for (unsigned мекенжай = 0; мекенжай < 32; мекенжай++) {
        int 식별 = 물리전송(мекенжай, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { сымды_мән.물리주소 = мекенжай; break; }
    }
    if (сымды_мән.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int мән = 물리읽기(BRGPHY_MII_AUXCTL);
    if (мән < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (мән & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    мән = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (мән < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (мән & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Дайындау_тұйық(unsigned Фон_мән) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned тұйық_мән = Фон_мән + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Орны = 0; Орны <= 0x30; Орны += 4) 유선저장기(тұйық_мән + Орны) = 0;
    유선저장기(тұйық_мән + 0x10) = (고리개수 << 16) | буфер_өлшемі;
    유선저장기(тұйық_мән + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Фон_мән == GENET_RX_BASE) 유선저장기(тұйық_мән + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(тұйық_мән + 0x24) = 1;
    유선저장기(Фон_мән + 0x104c) = 8;
    유선저장기(Фон_мән + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned лауазым_индекс) {
    uintptr_t мекенжай = (uintptr_t)сымды_мән.받기[лауазым_индекс];
    Анықтық_кэш((void *)мекенжай, буфер_өлшемі, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(лауазым_индекс)) = (uint32_t)мекенжай;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(лауазым_индекс)) = (uint64_t)мекенжай >> 32;
    유선저장기(GENET_RX_DESC_STATUS(лауазым_индекс)) = буфер_өлшемі << 16;
}
static err_t 전문보내기(struct netif *құрылғы_мән, struct pbuf *전문) {
    if (!сымды_мән.Дайындау || !netif_is_link_up(құрылғы_мән)) return ERR_RTE;
    unsigned Өлшемі = 전문->tot_len;
    if (!Өлшемі || Өлшемі > 1536) return ERR_BUF;
    uint16_t пайдалану_мән = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(сымды_мән.생산 - пайдалану_мән) >= 고리개수 - 1) return ERR_MEM;
    unsigned лауазым_индекс = сымды_мән.생산 % 고리개수, 송신길이 = Өлшемі < 60 ? 60 : Өлшемі;
    unsigned char *деректер = сымды_мән.жіберу[лауазым_индекс];
    memset(деректер, 0, 송신길이);
    if (pbuf_copy_partial(전문, деректер, Өлшемі, 0) != Өлшемі) return ERR_BUF;
    Анықтық_кэш(деректер, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(лауазым_индекс)) = (uint32_t)(uintptr_t)деректер;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(лауазым_индекс)) = (uint64_t)(uintptr_t)деректер >> 32;
    유선저장기(GENET_TX_DESC_STATUS(лауазым_индекс)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    үндестіру();
    сымды_мән.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = сымды_мән.생산;
    сымды_мән.집계[2]++; сымды_мән.집계[3] += Өлшемі;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Дайындау_сымды_желі(struct netif *құрылғы_мән) {
    unsigned char мекенжай[6];
    if (!유선장치있음() || !Тақта_нақпа_нақ_мекенжай(мекенжай) || (мекенжай[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= мекенжай[순번];
    if (!합) return ERR_IF;
    memset(&сымды_мән, 0, sizeof(сымды_мән));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t бастапқы_күй = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = бастапқы_күй | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = бастапқы_күй & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)мекенжай[0] << 24 | (uint32_t)мекенжай[1] << 16 | мекенжай[2] << 8 | мекенжай[3];
    유선저장기(GENET_UMAC_MAC1) = мекенжай[4] << 8 | мекенжай[5];
    Дайындау_тұйық(GENET_TX_BASE); Дайындау_тұйық(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    үндестіру();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    құрылғы_мән->name[0] = 'e'; құрылғы_мән->name[1] = 'n'; құрылғы_мән->mtu = 1500;
    құрылғы_мән->hwaddr_len = 6; memcpy(құрылғы_мән->hwaddr, мекенжай, 6);
    құрылғы_мән->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    құрылғы_мән->output = etharp_output; құрылғы_мән->linkoutput = 전문보내기;
    сымды_мән.Дайындау = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *құрылғы_мән) {
    if (!сымды_мән.Дайындау) return;
    uintptr_t ҚАЗІР_мән = 보드밀리초();
    if (ҚАЗІР_мән >= сымды_мән.тексеру_Келесі_элемент) {
        сымды_мән.тексеру_Келесі_элемент = ҚАЗІР_мән + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int күй_мән = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned әдіс_режим = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = әдіс_режим == 7 ? 1000 : әдіс_режим == 5 ? 100 : әдіс_режим == 2 ? 10 : 0;
        сымды_мән.속도 = күй_мән >= 0 && (күй_мән & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (сымды_мән.속도) {
            uint32_t Баптаулар = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Баптаулар &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Баптаулар | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Баптаулар = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Баптаулар | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(құрылғы_мән)) netif_set_link_up(құрылғы_мән);
        } else if (netif_is_link_up(құрылғы_мән)) netif_set_link_down(құрылғы_мән);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - сымды_мән.пайдалану_мән);
    if (남음 > 고리개수) { сымды_мән.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned лауазым_индекс = сымды_мән.пайдалану_мән % 고리개수;
        үндестіру();
        uint32_t күй_мән = 유선저장기(GENET_RX_DESC_STATUS(лауазым_индекс));
        unsigned ұзындық_мән = (күй_мән & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((күй_мән & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || ұзындық_мән < 16 || ұзындық_мән > 1538) сымды_мән.집계[4]++;
        else {
            Анықтық_кэш(сымды_мән.받기[лауазым_индекс], ұзындық_мән, 1);
            struct pbuf *деректер = pbuf_alloc(PBUF_RAW, ұзындық_мән - 2, PBUF_POOL);
            if (!деректер) сымды_мән.집계[4]++;
            else if (pbuf_take(деректер, сымды_мән.받기[лауазым_индекс] + 2, ұзындық_мән - 2) != ERR_OK || құрылғы_мән->input(деректер, құрылғы_мән) != ERR_OK) {
                pbuf_free(деректер); сымды_мән.집계[4]++;
            } else { сымды_мән.집계[0]++; сымды_мән.집계[1] += ұзындық_мән - 2; }
        }
        받는주소(лауазым_индекс); үндестіру(); сымды_мән.пайдалану_мән++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = сымды_мән.пайдалану_мән;
    }
}
uint32_t 유선망집계(unsigned енгізу_мән) {
    return енгізу_мән < 5 ? сымды_мән.집계[енгізу_мән] : енгізу_мән == 5 ? сымды_мән.속도 : енгізу_мән == 6 ? сымды_мән.Дайындау : 0;
}
