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
#include "зымдуу_Желе.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int 보드기계주소(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(дарек) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (дарек)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, буфер_көлөм = 2048 };
static struct {
    unsigned char 받기[고리개수][буфер_көлөм];
    unsigned char жөнөтүү[고리개수][буфер_көлөм];
    uint16_t 소비, 생산;
    int 물리주소, Даярдоо, 속도;
    uint32_t 집계[5];
    uintptr_t 다음확인;
} зымдуу_маани __attribute__((aligned(64)));

static void синхрондоштуруу(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Таза_кэш(void *берилмелер, unsigned узундук_маани, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)берилмелер + узундук_маани;
    for (uintptr_t дарек = (uintptr_t)берилмелер & ~(uintptr_t)63; дарек < 끝; дарек += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(дарек) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(дарек) : "memory");
    }
#else
    (void)берилмелер; (void)узундук_маани; (void)받기;
#endif
    синхрондоштуруу();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned дарек, unsigned индекс, int Жазуу, unsigned маани) {
    uint32_t Команда = (Жазуу ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (дарек << GENET_MDIO_ADDR_SHIFT) | (индекс << GENET_MDIO_REG_SHIFT) | (маани & 65535);
    유선저장기(GENET_MDIO_CMD) = Команда;
    유선저장기(GENET_MDIO_CMD) = Команда | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t абал_маани = 유선저장기(GENET_MDIO_CMD);
        if (!(абал_маани & GENET_MDIO_START_BUSY))
            return абал_маани & GENET_MDIO_READ_FAILED ? -1 : (int)(абал_маани & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned индекс) { return 물리전송(зымдуу_маани.물리주소, индекс, 0, 0); }
static int 물리쓰기(unsigned индекс, unsigned маани) { return 물리전송(зымдуу_маани.물리주소, индекс, 1, маани); }
static int 물리준비(void) {
    зымдуу_маани.물리주소 = -1;
    for (unsigned дарек = 0; дарек < 32; дарек++) {
        int 식별 = 물리전송(дарек, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { зымдуу_маани.물리주소 = дарек; break; }
    }
    if (зымдуу_маани.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int маани = 물리읽기(BRGPHY_MII_AUXCTL);
    if (маани < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (маани & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    маани = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (маани < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (маани & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Даярдоо_цикл(unsigned Фон_маани) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned цикл_маани = Фон_маани + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Турган_жери = 0; Турган_жери <= 0x30; Турган_жери += 4) 유선저장기(цикл_маани + Турган_жери) = 0;
    유선저장기(цикл_маани + 0x10) = (고리개수 << 16) | буфер_көлөм;
    유선저장기(цикл_маани + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Фон_маани == GENET_RX_BASE) 유선저장기(цикл_маани + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(цикл_маани + 0x24) = 1;
    유선저장기(Фон_маани + 0x104c) = 8;
    유선저장기(Фон_маани + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned 자리) {
    uintptr_t дарек = (uintptr_t)зымдуу_маани.받기[자리];
    Таза_кэш((void *)дарек, буфер_көлөм, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(자리)) = (uint32_t)дарек;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(자리)) = (uint64_t)дарек >> 32;
    유선저장기(GENET_RX_DESC_STATUS(자리)) = буфер_көлөм << 16;
}
static err_t 전문보내기(struct netif *түзмөк_маани, struct pbuf *전문) {
    if (!зымдуу_маани.Даярдоо || !netif_is_link_up(түзмөк_маани)) return ERR_RTE;
    unsigned Өлчөмү = 전문->tot_len;
    if (!Өлчөмү || Өлчөмү > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(зымдуу_маани.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned 자리 = зымдуу_маани.생산 % 고리개수, 송신길이 = Өлчөмү < 60 ? 60 : Өлчөмү;
    unsigned char *берилмелер = зымдуу_маани.жөнөтүү[자리];
    memset(берилмелер, 0, 송신길이);
    if (pbuf_copy_partial(전문, берилмелер, Өлчөмү, 0) != Өлчөмү) return ERR_BUF;
    Таза_кэш(берилмелер, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(자리)) = (uint32_t)(uintptr_t)берилмелер;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(자리)) = (uint64_t)(uintptr_t)берилмелер >> 32;
    유선저장기(GENET_TX_DESC_STATUS(자리)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    синхрондоштуруу();
    зымдуу_маани.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = зымдуу_маани.생산;
    зымдуу_маани.집계[2]++; зымдуу_маани.집계[3] += Өлчөмү;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Даярдоо_зымдуу_Желе(struct netif *түзмөк_маани) {
    unsigned char дарек[6];
    if (!유선장치있음() || !보드기계주소(дарек) || (дарек[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= дарек[순번];
    if (!합) return ERR_IF;
    memset(&зымдуу_маани, 0, sizeof(зымдуу_маани));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)дарек[0] << 24 | (uint32_t)дарек[1] << 16 | дарек[2] << 8 | дарек[3];
    유선저장기(GENET_UMAC_MAC1) = дарек[4] << 8 | дарек[5];
    Даярдоо_цикл(GENET_TX_BASE); Даярдоо_цикл(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    синхрондоштуруу();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    түзмөк_маани->name[0] = 'e'; түзмөк_маани->name[1] = 'n'; түзмөк_маани->mtu = 1500;
    түзмөк_маани->hwaddr_len = 6; memcpy(түзмөк_маани->hwaddr, дарек, 6);
    түзмөк_маани->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    түзмөк_маани->output = etharp_output; түзмөк_маани->linkoutput = 전문보내기;
    зымдуу_маани.Даярдоо = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *түзмөк_маани) {
    if (!зымдуу_маани.Даярдоо) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= зымдуу_маани.다음확인) {
        зымдуу_маани.다음확인 = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int абал_маани = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ыкма_режим = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ыкма_режим == 7 ? 1000 : ыкма_режим == 5 ? 100 : ыкма_режим == 2 ? 10 : 0;
        зымдуу_маани.속도 = абал_маани >= 0 && (абал_маани & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (зымдуу_маани.속도) {
            uint32_t Орнотуулар = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Орнотуулар &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Орнотуулар | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Орнотуулар = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Орнотуулар | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(түзмөк_маани)) netif_set_link_up(түзмөк_маани);
        } else if (netif_is_link_up(түзмөк_маани)) netif_set_link_down(түзмөк_маани);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - зымдуу_маани.소비);
    if (남음 > 고리개수) { зымдуу_маани.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned 자리 = зымдуу_маани.소비 % 고리개수;
        синхрондоштуруу();
        uint32_t абал_маани = 유선저장기(GENET_RX_DESC_STATUS(자리));
        unsigned узундук_маани = (абал_маани & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((абал_маани & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || узундук_маани < 16 || узундук_маани > 1538) зымдуу_маани.집계[4]++;
        else {
            Таза_кэш(зымдуу_маани.받기[자리], узундук_маани, 1);
            struct pbuf *берилмелер = pbuf_alloc(PBUF_RAW, узундук_маани - 2, PBUF_POOL);
            if (!берилмелер) зымдуу_маани.집계[4]++;
            else if (pbuf_take(берилмелер, зымдуу_маани.받기[자리] + 2, узундук_маани - 2) != ERR_OK || түзмөк_маани->input(берилмелер, түзмөк_маани) != ERR_OK) {
                pbuf_free(берилмелер); зымдуу_маани.집계[4]++;
            } else { зымдуу_маани.집계[0]++; зымдуу_маани.집계[1] += узундук_маани - 2; }
        }
        받는주소(자리); синхрондоштуруу(); зымдуу_маани.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = зымдуу_маани.소비;
    }
}
uint32_t 유선망집계(unsigned киргизме_жазуу_маани) {
    return киргизме_жазуу_маани < 5 ? зымдуу_маани.집계[киргизме_жазуу_маани] : киргизме_жазуу_маани == 5 ? зымдуу_маани.속도 : киргизме_жазуу_маани == 6 ? зымдуу_маани.Даярдоо : 0;
}
