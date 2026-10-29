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
#include "სადენიანი_ქსელი.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int დაფა_კომპიუტერი_მისამართი(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(მისამართი) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (მისამართი)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, ბუფერი_ზომის_შეცვლა = 2048 };
static struct {
    unsigned char 받기[고리개수][ბუფერი_ზომის_შეცვლა];
    unsigned char გაგზავნა[고리개수][ბუფერი_ზომის_შეცვლა];
    uint16_t 소비, 생산;
    int 물리주소, მომზადება, 속도;
    uint32_t 집계[5];
    uintptr_t გადამოწმება_შემდეგი_ელემენტი;
} სადენიანი_მნიშვნელობა __attribute__((aligned(64)));

static void დასინქრონება(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void გაწმენდა_კეშირება(void *მონაცემები, unsigned სიგრძე_მნიშვნელობა, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)მონაცემები + სიგრძე_მნიშვნელობა;
    for (uintptr_t მისამართი = (uintptr_t)მონაცემები & ~(uintptr_t)63; მისამართი < 끝; მისამართი += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(მისამართი) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(მისამართი) : "memory");
    }
#else
    (void)მონაცემები; (void)სიგრძე_მნიშვნელობა; (void)받기;
#endif
    დასინქრონება();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned მისამართი, unsigned ინდექსი, int ჩაწერა, unsigned მნიშვნელობა) {
    uint32_t ბრძანება = (ჩაწერა ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (მისამართი << GENET_MDIO_ADDR_SHIFT) | (ინდექსი << GENET_MDIO_REG_SHIFT) | (მნიშვნელობა & 65535);
    유선저장기(GENET_MDIO_CMD) = ბრძანება;
    유선저장기(GENET_MDIO_CMD) = ბრძანება | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t სტატუსი_მნიშვნელობა = 유선저장기(GENET_MDIO_CMD);
        if (!(სტატუსი_მნიშვნელობა & GENET_MDIO_START_BUSY))
            return სტატუსი_მნიშვნელობა & GENET_MDIO_READ_FAILED ? -1 : (int)(სტატუსი_მნიშვნელობა & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ინდექსი) { return 물리전송(სადენიანი_მნიშვნელობა.물리주소, ინდექსი, 0, 0); }
static int 물리쓰기(unsigned ინდექსი, unsigned მნიშვნელობა) { return 물리전송(სადენიანი_მნიშვნელობა.물리주소, ინდექსი, 1, მნიშვნელობა); }
static int 물리준비(void) {
    სადენიანი_მნიშვნელობა.물리주소 = -1;
    for (unsigned მისამართი = 0; მისამართი < 32; მისამართი++) {
        int 식별 = 물리전송(მისამართი, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { სადენიანი_მნიშვნელობა.물리주소 = მისამართი; break; }
    }
    if (სადენიანი_მნიშვნელობა.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int მნიშვნელობა = 물리읽기(BRGPHY_MII_AUXCTL);
    if (მნიშვნელობა < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (მნიშვნელობა & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    მნიშვნელობა = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (მნიშვნელობა < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (მნიშვნელობა & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void მომზადება_ციკლი(unsigned ფონი_მნიშვნელობა) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ციკლი_მნიშვნელობა_201e2521 = ფონი_მნიშვნელობა + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned პოზიცია = 0; პოზიცია <= 0x30; პოზიცია += 4) 유선저장기(ციკლი_მნიშვნელობა_201e2521 + პოზიცია) = 0;
    유선저장기(ციკლი_მნიშვნელობა_201e2521 + 0x10) = (고리개수 << 16) | ბუფერი_ზომის_შეცვლა;
    유선저장기(ციკლი_მნიშვნელობა_201e2521 + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (ფონი_მნიშვნელობა == GENET_RX_BASE) 유선저장기(ციკლი_მნიშვნელობა_201e2521 + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ციკლი_მნიშვნელობა_201e2521 + 0x24) = 1;
    유선저장기(ფონი_მნიშვნელობა + 0x104c) = 8;
    유선저장기(ფონი_მნიშვნელობა + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned პოზიცია_ინდექსი) {
    uintptr_t მისამართი = (uintptr_t)სადენიანი_მნიშვნელობა.받기[პოზიცია_ინდექსი];
    გაწმენდა_კეშირება((void *)მისამართი, ბუფერი_ზომის_შეცვლა, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(პოზიცია_ინდექსი)) = (uint32_t)მისამართი;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(პოზიცია_ინდექსი)) = (uint64_t)მისამართი >> 32;
    유선저장기(GENET_RX_DESC_STATUS(პოზიცია_ინდექსი)) = ბუფერი_ზომის_შეცვლა << 16;
}
static err_t 전문보내기(struct netif *მობილური_მნიშვნელობა, struct pbuf *전문) {
    if (!სადენიანი_მნიშვნელობა.მომზადება || !netif_is_link_up(მობილური_მნიშვნელობა)) return ERR_RTE;
    unsigned ზომა = 전문->tot_len;
    if (!ზომა || ზომა > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(სადენიანი_მნიშვნელობა.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned პოზიცია_ინდექსი = სადენიანი_მნიშვნელობა.생산 % 고리개수, 송신길이 = ზომა < 60 ? 60 : ზომა;
    unsigned char *მონაცემები = სადენიანი_მნიშვნელობა.გაგზავნა[პოზიცია_ინდექსი];
    memset(მონაცემები, 0, 송신길이);
    if (pbuf_copy_partial(전문, მონაცემები, ზომა, 0) != ზომა) return ERR_BUF;
    გაწმენდა_კეშირება(მონაცემები, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(პოზიცია_ინდექსი)) = (uint32_t)(uintptr_t)მონაცემები;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(პოზიცია_ინდექსი)) = (uint64_t)(uintptr_t)მონაცემები >> 32;
    유선저장기(GENET_TX_DESC_STATUS(პოზიცია_ინდექსი)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    დასინქრონება();
    სადენიანი_მნიშვნელობა.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = სადენიანი_მნიშვნელობა.생산;
    სადენიანი_მნიშვნელობა.집계[2]++; სადენიანი_მნიშვნელობა.집계[3] += ზომა;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t მომზადება_სადენიანი_ქსელი(struct netif *მობილური_მნიშვნელობა) {
    unsigned char მისამართი[6];
    if (!유선장치있음() || !დაფა_კომპიუტერი_მისამართი(მისამართი) || (მისამართი[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= მისამართი[순번];
    if (!합) return ERR_IF;
    memset(&სადენიანი_მნიშვნელობა, 0, sizeof(სადენიანი_მნიშვნელობა));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)მისამართი[0] << 24 | (uint32_t)მისამართი[1] << 16 | მისამართი[2] << 8 | მისამართი[3];
    유선저장기(GENET_UMAC_MAC1) = მისამართი[4] << 8 | მისამართი[5];
    მომზადება_ციკლი(GENET_TX_BASE); მომზადება_ციკლი(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    დასინქრონება();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    მობილური_მნიშვნელობა->name[0] = 'e'; მობილური_მნიშვნელობა->name[1] = 'n'; მობილური_მნიშვნელობა->mtu = 1500;
    მობილური_მნიშვნელობა->hwaddr_len = 6; memcpy(მობილური_მნიშვნელობა->hwaddr, მისამართი, 6);
    მობილური_მნიშვნელობა->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    მობილური_მნიშვნელობა->output = etharp_output; მობილური_მნიშვნელობა->linkoutput = 전문보내기;
    სადენიანი_მნიშვნელობა.მომზადება = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *მობილური_მნიშვნელობა) {
    if (!სადენიანი_მნიშვნელობა.მომზადება) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= სადენიანი_მნიშვნელობა.გადამოწმება_შემდეგი_ელემენტი) {
        სადენიანი_მნიშვნელობა.გადამოწმება_შემდეგი_ელემენტი = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int სტატუსი_მნიშვნელობა = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned მეთოდი_რეჟიმი = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = მეთოდი_რეჟიმი == 7 ? 1000 : მეთოდი_რეჟიმი == 5 ? 100 : მეთოდი_რეჟიმი == 2 ? 10 : 0;
        სადენიანი_მნიშვნელობა.속도 = სტატუსი_მნიშვნელობა >= 0 && (სტატუსი_მნიშვნელობა & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (სადენიანი_მნიშვნელობა.속도) {
            uint32_t პარამეტრები = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            პარამეტრები &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = პარამეტრები | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            პარამეტრები = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = პარამეტრები | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(მობილური_მნიშვნელობა)) netif_set_link_up(მობილური_მნიშვნელობა);
        } else if (netif_is_link_up(მობილური_მნიშვნელობა)) netif_set_link_down(მობილური_მნიშვნელობა);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - სადენიანი_მნიშვნელობა.소비);
    if (남음 > 고리개수) { სადენიანი_მნიშვნელობა.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned პოზიცია_ინდექსი = სადენიანი_მნიშვნელობა.소비 % 고리개수;
        დასინქრონება();
        uint32_t სტატუსი_მნიშვნელობა = 유선저장기(GENET_RX_DESC_STATUS(პოზიცია_ინდექსი));
        unsigned სიგრძე_მნიშვნელობა = (სტატუსი_მნიშვნელობა & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((სტატუსი_მნიშვნელობა & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || სიგრძე_მნიშვნელობა < 16 || სიგრძე_მნიშვნელობა > 1538) სადენიანი_მნიშვნელობა.집계[4]++;
        else {
            გაწმენდა_კეშირება(სადენიანი_მნიშვნელობა.받기[პოზიცია_ინდექსი], სიგრძე_მნიშვნელობა, 1);
            struct pbuf *მონაცემები = pbuf_alloc(PBUF_RAW, სიგრძე_მნიშვნელობა - 2, PBUF_POOL);
            if (!მონაცემები) სადენიანი_მნიშვნელობა.집계[4]++;
            else if (pbuf_take(მონაცემები, სადენიანი_მნიშვნელობა.받기[პოზიცია_ინდექსი] + 2, სიგრძე_მნიშვნელობა - 2) != ERR_OK || მობილური_მნიშვნელობა->input(მონაცემები, მობილური_მნიშვნელობა) != ERR_OK) {
                pbuf_free(მონაცემები); სადენიანი_მნიშვნელობა.집계[4]++;
            } else { სადენიანი_მნიშვნელობა.집계[0]++; სადენიანი_მნიშვნელობა.집계[1] += სიგრძე_მნიშვნელობა - 2; }
        }
        받는주소(პოზიცია_ინდექსი); დასინქრონება(); სადენიანი_მნიშვნელობა.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = სადენიანი_მნიშვნელობა.소비;
    }
}
uint32_t 유선망집계(unsigned შენატანი_მნიშვნელობა) {
    return შენატანი_მნიშვნელობა < 5 ? სადენიანი_მნიშვნელობა.집계[შენატანი_მნიშვნელობა] : შენატანი_მნიშვნელობა == 5 ? სადენიანი_მნიშვნელობა.속도 : შენატანი_მნიშვნელობა == 6 ? სადენიანი_მნიშვნელობა.მომზადება : 0;
}
