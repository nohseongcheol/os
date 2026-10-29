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
#include "유선망.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int 보드기계주소(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(پتو) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (پتو)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, بفر_سائيز = 2048 };
static struct {
    unsigned char 받기[고리개수][بفر_سائيز];
    unsigned char اي_ميل[고리개수][بفر_سائيز];
    uint16_t 소비, 생산;
    int 물리주소, تياري_ڪريو, 속도;
    uint32_t 집계[5];
    uintptr_t 다음확인;
} 유선 __attribute__((aligned(64)));

static void هم_وقت(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void ڪلين_ڪيشي(void *ڪوائف, unsigned لمبائي_قدر, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ڪوائف + لمبائي_قدر;
    for (uintptr_t پتو = (uintptr_t)ڪوائف & ~(uintptr_t)63; پتو < 끝; پتو += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(پتو) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(پتو) : "memory");
    }
#else
    (void)ڪوائف; (void)لمبائي_قدر; (void)받기;
#endif
    هم_وقت();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned پتو, unsigned ابتدائي, int لکو, unsigned قدر) {
    uint32_t حڪم = (لکو ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (پتو << GENET_MDIO_ADDR_SHIFT) | (ابتدائي << GENET_MDIO_REG_SHIFT) | (قدر & 65535);
    유선저장기(GENET_MDIO_CMD) = حڪم;
    유선저장기(GENET_MDIO_CMD) = حڪم | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t حالت_قدر = 유선저장기(GENET_MDIO_CMD);
        if (!(حالت_قدر & GENET_MDIO_START_BUSY))
            return حالت_قدر & GENET_MDIO_READ_FAILED ? -1 : (int)(حالت_قدر & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ابتدائي) { return 물리전송(유선.물리주소, ابتدائي, 0, 0); }
static int 물리쓰기(unsigned ابتدائي, unsigned قدر) { return 물리전송(유선.물리주소, ابتدائي, 1, قدر); }
static int 물리준비(void) {
    유선.물리주소 = -1;
    for (unsigned پتو = 0; پتو < 32; پتو++) {
        int 식별 = 물리전송(پتو, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { 유선.물리주소 = پتو; break; }
    }
    if (유선.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int قدر = 물리읽기(BRGPHY_MII_AUXCTL);
    if (قدر < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (قدر & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    قدر = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (قدر < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (قدر & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void تياري_ڪريو_لوپ(unsigned پس_منظر_قدر) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned لوپ_قدر = پس_منظر_قدر + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned 위치 = 0; 위치 <= 0x30; 위치 += 4) 유선저장기(لوپ_قدر + 위치) = 0;
    유선저장기(لوپ_قدر + 0x10) = (고리개수 << 16) | بفر_سائيز;
    유선저장기(لوپ_قدر + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (پس_منظر_قدر == GENET_RX_BASE) 유선저장기(لوپ_قدر + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(لوپ_قدر + 0x24) = 1;
    유선저장기(پس_منظر_قدر + 0x104c) = 8;
    유선저장기(پس_منظر_قدر + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned 자리) {
    uintptr_t پتو = (uintptr_t)유선.받기[자리];
    ڪلين_ڪيشي((void *)پتو, بفر_سائيز, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(자리)) = (uint32_t)پتو;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(자리)) = (uint64_t)پتو >> 32;
    유선저장기(GENET_RX_DESC_STATUS(자리)) = بفر_سائيز << 16;
}
static err_t 전문보내기(struct netif *آلو_قدر, struct pbuf *전문) {
    if (!유선.تياري_ڪريو || !netif_is_link_up(آلو_قدر)) return ERR_RTE;
    unsigned سائيز = 전문->tot_len;
    if (!سائيز || سائيز > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(유선.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned 자리 = 유선.생산 % 고리개수, 송신길이 = سائيز < 60 ? 60 : سائيز;
    unsigned char *ڪوائف = 유선.اي_ميل[자리];
    memset(ڪوائف, 0, 송신길이);
    if (pbuf_copy_partial(전문, ڪوائف, سائيز, 0) != سائيز) return ERR_BUF;
    ڪلين_ڪيشي(ڪوائف, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(자리)) = (uint32_t)(uintptr_t)ڪوائف;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(자리)) = (uint64_t)(uintptr_t)ڪوائف >> 32;
    유선저장기(GENET_TX_DESC_STATUS(자리)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    هم_وقت();
    유선.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = 유선.생산;
    유선.집계[2]++; 유선.집계[3] += سائيز;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t 유선망준비(struct netif *آلو_قدر) {
    unsigned char پتو[6];
    if (!유선장치있음() || !보드기계주소(پتو) || (پتو[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= پتو[순번];
    if (!합) return ERR_IF;
    memset(&유선, 0, sizeof(유선));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)پتو[0] << 24 | (uint32_t)پتو[1] << 16 | پتو[2] << 8 | پتو[3];
    유선저장기(GENET_UMAC_MAC1) = پتو[4] << 8 | پتو[5];
    تياري_ڪريو_لوپ(GENET_TX_BASE); تياري_ڪريو_لوپ(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    هم_وقت();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    آلو_قدر->name[0] = 'e'; آلو_قدر->name[1] = 'n'; آلو_قدر->mtu = 1500;
    آلو_قدر->hwaddr_len = 6; memcpy(آلو_قدر->hwaddr, پتو, 6);
    آلو_قدر->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    آلو_قدر->output = etharp_output; آلو_قدر->linkoutput = 전문보내기;
    유선.تياري_ڪريو = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *آلو_قدر) {
    if (!유선.تياري_ڪريو) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= 유선.다음확인) {
        유선.다음확인 = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int حالت_قدر = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned طريقو_موڊ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = طريقو_موڊ == 7 ? 1000 : طريقو_موڊ == 5 ? 100 : طريقو_موڊ == 2 ? 10 : 0;
        유선.속도 = حالت_قدر >= 0 && (حالت_قدر & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (유선.속도) {
            uint32_t سيٽنگون = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            سيٽنگون &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = سيٽنگون | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            سيٽنگون = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = سيٽنگون | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(آلو_قدر)) netif_set_link_up(آلو_قدر);
        } else if (netif_is_link_up(آلو_قدر)) netif_set_link_down(آلو_قدر);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - 유선.소비);
    if (남음 > 고리개수) { 유선.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned 자리 = 유선.소비 % 고리개수;
        هم_وقت();
        uint32_t حالت_قدر = 유선저장기(GENET_RX_DESC_STATUS(자리));
        unsigned لمبائي_قدر = (حالت_قدر & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((حالت_قدر & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || لمبائي_قدر < 16 || لمبائي_قدر > 1538) 유선.집계[4]++;
        else {
            ڪلين_ڪيشي(유선.받기[자리], لمبائي_قدر, 1);
            struct pbuf *ڪوائف = pbuf_alloc(PBUF_RAW, لمبائي_قدر - 2, PBUF_POOL);
            if (!ڪوائف) 유선.집계[4]++;
            else if (pbuf_take(ڪوائف, 유선.받기[자리] + 2, لمبائي_قدر - 2) != ERR_OK || آلو_قدر->input(ڪوائف, آلو_قدر) != ERR_OK) {
                pbuf_free(ڪوائف); 유선.집계[4]++;
            } else { 유선.집계[0]++; 유선.집계[1] += لمبائي_قدر - 2; }
        }
        받는주소(자리); هم_وقت(); 유선.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = 유선.소비;
    }
}
uint32_t 유선망집계(unsigned داخلا_قدر) {
    return داخلا_قدر < 5 ? 유선.집계[داخلا_قدر] : داخلا_قدر == 5 ? 유선.속도 : داخلا_قدر == 6 ? 유선.تياري_ڪريو : 0;
}
