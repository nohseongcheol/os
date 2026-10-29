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
#include "ដែលប្រើខ្សែ_ណិតវឺក.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int ផ្ទាំង_ម៉ាស៊ីន_អ៊ីម៉ែល(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(អ៊ីម៉ែល) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (អ៊ីម៉ែល)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, អង្គចងចាំបណ្តោះអាសន្ន_ដាក់ទំហំ = 2048 };
static struct {
    unsigned char 받기[고리개수][អង្គចងចាំបណ្តោះអាសន្ន_ដាក់ទំហំ];
    unsigned char ផ្ញើ[고리개수][អង្គចងចាំបណ្តោះអាសន្ន_ដាក់ទំហំ];
    uint16_t 소비, 생산;
    int 물리주소, រៀបចំ, 속도;
    uint32_t 집계[5];
    uintptr_t ផ្ទៀងផ្ទាត់_បន្ទាប់_ធាតុ;
} ដែលប្រើខ្សែ_តំលៃ __attribute__((aligned(64)));

static void សមកាលកម្ម(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void សម្អាត_បំរុងទុកបណ្តោះអាសន្ន(void *ទិន្នន័យ, unsigned ប្រវែង_តំលៃ, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ទិន្នន័យ + ប្រវែង_តំលៃ;
    for (uintptr_t អ៊ីម៉ែល = (uintptr_t)ទិន្នន័យ & ~(uintptr_t)63; អ៊ីម៉ែល < 끝; អ៊ីម៉ែល += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(អ៊ីម៉ែល) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(អ៊ីម៉ែល) : "memory");
    }
#else
    (void)ទិន្នន័យ; (void)ប្រវែង_តំលៃ; (void)받기;
#endif
    សមកាលកម្ម();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned អ៊ីម៉ែល, unsigned សន្ទស្សន៏, int សរសេរ, unsigned តំលៃ) {
    uint32_t ពាក្យ_បញ្ជា = (សរសេរ ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (អ៊ីម៉ែល << GENET_MDIO_ADDR_SHIFT) | (សន្ទស្សន៏ << GENET_MDIO_REG_SHIFT) | (តំលៃ & 65535);
    유선저장기(GENET_MDIO_CMD) = ពាក្យ_បញ្ជា;
    유선저장기(GENET_MDIO_CMD) = ពាក្យ_បញ្ជា | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t ភាព_តំលៃ = 유선저장기(GENET_MDIO_CMD);
        if (!(ភាព_តំលៃ & GENET_MDIO_START_BUSY))
            return ភាព_តំលៃ & GENET_MDIO_READ_FAILED ? -1 : (int)(ភាព_តំលៃ & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned សន្ទស្សន៏) { return 물리전송(ដែលប្រើខ្សែ_តំលៃ.물리주소, សន្ទស្សន៏, 0, 0); }
static int 물리쓰기(unsigned សន្ទស្សន៏, unsigned តំលៃ) { return 물리전송(ដែលប្រើខ្សែ_តំលៃ.물리주소, សន្ទស្សន៏, 1, តំលៃ); }
static int 물리준비(void) {
    ដែលប្រើខ្សែ_តំលៃ.물리주소 = -1;
    for (unsigned អ៊ីម៉ែល = 0; អ៊ីម៉ែល < 32; អ៊ីម៉ែល++) {
        int 식별 = 물리전송(អ៊ីម៉ែល, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ដែលប្រើខ្សែ_តំលៃ.물리주소 = អ៊ីម៉ែល; break; }
    }
    if (ដែលប្រើខ្សែ_តំលៃ.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int តំលៃ = 물리읽기(BRGPHY_MII_AUXCTL);
    if (តំលៃ < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (តំលៃ & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    តំលៃ = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (តំលៃ < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (តំលៃ & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void រៀបចំ_រង្វិលជុំ(unsigned គំរូដែសថប_តំលៃ) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned រង្វិលជុំ_តំលៃ = គំរូដែសថប_តំលៃ + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned កំណត់ទីតាំង = 0; កំណត់ទីតាំង <= 0x30; កំណត់ទីតាំង += 4) 유선저장기(រង្វិលជុំ_តំលៃ + កំណត់ទីតាំង) = 0;
    유선저장기(រង្វិលជុំ_តំលៃ + 0x10) = (고리개수 << 16) | អង្គចងចាំបណ្តោះអាសន្ន_ដាក់ទំហំ;
    유선저장기(រង្វិលជុំ_តំលៃ + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (គំរូដែសថប_តំលៃ == GENET_RX_BASE) 유선저장기(រង្វិលជុំ_តំលៃ + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(រង្វិលជុំ_តំលៃ + 0x24) = 1;
    유선저장기(គំរូដែសថប_តំលៃ + 0x104c) = 8;
    유선저장기(គំរូដែសថប_តំលៃ + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned កំណត់ទីតាំង_សន្ទស្សន៏) {
    uintptr_t អ៊ីម៉ែល = (uintptr_t)ដែលប្រើខ្សែ_តំលៃ.받기[កំណត់ទីតាំង_សន្ទស្សន៏];
    សម្អាត_បំរុងទុកបណ្តោះអាសន្ន((void *)អ៊ីម៉ែល, អង្គចងចាំបណ្តោះអាសន្ន_ដាក់ទំហំ, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(កំណត់ទីតាំង_សន្ទស្សន៏)) = (uint32_t)អ៊ីម៉ែល;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(កំណត់ទីតាំង_សន្ទស្សន៏)) = (uint64_t)អ៊ីម៉ែល >> 32;
    유선저장기(GENET_RX_DESC_STATUS(កំណត់ទីតាំង_សន្ទស្សន៏)) = អង្គចងចាំបណ្តោះអាសន្ន_ដាក់ទំហំ << 16;
}
static err_t 전문보내기(struct netif *ឧបករណ៍_តំលៃ, struct pbuf *전문) {
    if (!ដែលប្រើខ្សែ_តំលៃ.រៀបចំ || !netif_is_link_up(ឧបករណ៍_តំលៃ)) return ERR_RTE;
    unsigned ដាក់ទំហំ = 전문->tot_len;
    if (!ដាក់ទំហំ || ដាក់ទំហំ > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ដែលប្រើខ្សែ_តំលៃ.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned កំណត់ទីតាំង_សន្ទស្សន៏ = ដែលប្រើខ្សែ_តំលៃ.생산 % 고리개수, 송신길이 = ដាក់ទំហំ < 60 ? 60 : ដាក់ទំហំ;
    unsigned char *ទិន្នន័យ = ដែលប្រើខ្សែ_តំលៃ.ផ្ញើ[កំណត់ទីតាំង_សន្ទស្សន៏];
    memset(ទិន្នន័យ, 0, 송신길이);
    if (pbuf_copy_partial(전문, ទិន្នន័យ, ដាក់ទំហំ, 0) != ដាក់ទំហំ) return ERR_BUF;
    សម្អាត_បំរុងទុកបណ្តោះអាសន្ន(ទិន្នន័យ, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(កំណត់ទីតាំង_សន្ទស្សន៏)) = (uint32_t)(uintptr_t)ទិន្នន័យ;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(កំណត់ទីតាំង_សន្ទស្សន៏)) = (uint64_t)(uintptr_t)ទិន្នន័យ >> 32;
    유선저장기(GENET_TX_DESC_STATUS(កំណត់ទីតាំង_សន្ទស្សន៏)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    សមកាលកម្ម();
    ដែលប្រើខ្សែ_តំលៃ.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ដែលប្រើខ្សែ_តំលៃ.생산;
    ដែលប្រើខ្សែ_តំលៃ.집계[2]++; ដែលប្រើខ្សែ_តំលៃ.집계[3] += ដាក់ទំហំ;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t រៀបចំ_ដែលប្រើខ្សែ_ណិតវឺក(struct netif *ឧបករណ៍_តំលៃ) {
    unsigned char អ៊ីម៉ែល[6];
    if (!유선장치있음() || !ផ្ទាំង_ម៉ាស៊ីន_អ៊ីម៉ែល(អ៊ីម៉ែល) || (អ៊ីម៉ែល[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= អ៊ីម៉ែល[순번];
    if (!합) return ERR_IF;
    memset(&ដែលប្រើខ្សែ_តំលៃ, 0, sizeof(ដែលប្រើខ្សែ_តំលៃ));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)អ៊ីម៉ែល[0] << 24 | (uint32_t)អ៊ីម៉ែល[1] << 16 | អ៊ីម៉ែល[2] << 8 | អ៊ីម៉ែល[3];
    유선저장기(GENET_UMAC_MAC1) = អ៊ីម៉ែល[4] << 8 | អ៊ីម៉ែល[5];
    រៀបចំ_រង្វិលជុំ(GENET_TX_BASE); រៀបចំ_រង្វិលជុំ(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    សមកាលកម្ម();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ឧបករណ៍_តំលៃ->name[0] = 'e'; ឧបករណ៍_តំលៃ->name[1] = 'n'; ឧបករណ៍_តំលៃ->mtu = 1500;
    ឧបករណ៍_តំលៃ->hwaddr_len = 6; memcpy(ឧបករណ៍_តំលៃ->hwaddr, អ៊ីម៉ែល, 6);
    ឧបករណ៍_តំលៃ->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ឧបករណ៍_តំលៃ->output = etharp_output; ឧបករណ៍_តំលៃ->linkoutput = 전문보내기;
    ដែលប្រើខ្សែ_តំលៃ.រៀបចំ = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ឧបករណ៍_តំលៃ) {
    if (!ដែលប្រើខ្សែ_តំលៃ.រៀបចំ) return;
    uintptr_t ឥឡូវ_តំលៃ = 보드밀리초();
    if (ឥឡូវ_តំលៃ >= ដែលប្រើខ្សែ_តំលៃ.ផ្ទៀងផ្ទាត់_បន្ទាប់_ធាតុ) {
        ដែលប្រើខ្សែ_តំលៃ.ផ្ទៀងផ្ទាត់_បន្ទាប់_ធាតុ = ឥឡូវ_តំលៃ + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int ភាព_តំលៃ = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned វិធីសាស្រ្ត_ម៉ូដ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = វិធីសាស្រ្ត_ម៉ូដ == 7 ? 1000 : វិធីសាស្រ្ត_ម៉ូដ == 5 ? 100 : វិធីសាស្រ្ត_ម៉ូដ == 2 ? 10 : 0;
        ដែលប្រើខ្សែ_តំលៃ.속도 = ភាព_តំលៃ >= 0 && (ភាព_តំលៃ & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ដែលប្រើខ្សែ_តំលៃ.속도) {
            uint32_t ការកំណត់ = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            ការកំណត់ &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = ការកំណត់ | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ការកំណត់ = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = ការកំណត់ | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ឧបករណ៍_តំលៃ)) netif_set_link_up(ឧបករណ៍_តំលៃ);
        } else if (netif_is_link_up(ឧបករណ៍_តំលៃ)) netif_set_link_down(ឧបករណ៍_តំលៃ);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ដែលប្រើខ្សែ_តំលៃ.소비);
    if (남음 > 고리개수) { ដែលប្រើខ្សែ_តំលៃ.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned កំណត់ទីតាំង_សន្ទស្សន៏ = ដែលប្រើខ្សែ_តំលៃ.소비 % 고리개수;
        សមកាលកម្ម();
        uint32_t ភាព_តំលៃ = 유선저장기(GENET_RX_DESC_STATUS(កំណត់ទីតាំង_សន្ទស្សន៏));
        unsigned ប្រវែង_តំលៃ = (ភាព_តំលៃ & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((ភាព_តំលៃ & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || ប្រវែង_តំលៃ < 16 || ប្រវែង_តំលៃ > 1538) ដែលប្រើខ្សែ_តំលៃ.집계[4]++;
        else {
            សម្អាត_បំរុងទុកបណ្តោះអាសន្ន(ដែលប្រើខ្សែ_តំលៃ.받기[កំណត់ទីតាំង_សន្ទស្សន៏], ប្រវែង_តំលៃ, 1);
            struct pbuf *ទិន្នន័យ = pbuf_alloc(PBUF_RAW, ប្រវែង_តំលៃ - 2, PBUF_POOL);
            if (!ទិន្នន័យ) ដែលប្រើខ្សែ_តំលៃ.집계[4]++;
            else if (pbuf_take(ទិន្នន័យ, ដែលប្រើខ្សែ_តំលៃ.받기[កំណត់ទីតាំង_សន្ទស្សន៏] + 2, ប្រវែង_តំលៃ - 2) != ERR_OK || ឧបករណ៍_តំលៃ->input(ទិន្នន័យ, ឧបករណ៍_តំលៃ) != ERR_OK) {
                pbuf_free(ទិន្នន័យ); ដែលប្រើខ្សែ_តំលៃ.집계[4]++;
            } else { ដែលប្រើខ្សែ_តំលៃ.집계[0]++; ដែលប្រើខ្សែ_តំលៃ.집계[1] += ប្រវែង_តំលៃ - 2; }
        }
        받는주소(កំណត់ទីតាំង_សន្ទស្សន៏); សមកាលកម្ម(); ដែលប្រើខ្សែ_តំលៃ.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ដែលប្រើខ្សែ_តំលៃ.소비;
    }
}
uint32_t 유선망집계(unsigned ការបញ្ចូល_តំលៃ) {
    return ការបញ្ចូល_តំលៃ < 5 ? ដែលប្រើខ្សែ_តំលៃ.집계[ការបញ្ចូល_តំលៃ] : ការបញ្ចូល_តំលៃ == 5 ? ដែលប្រើខ្សែ_តំលៃ.속도 : ការបញ្ចូល_តំលៃ == 6 ? ដែលប្រើខ្សែ_តំលៃ.រៀបចំ : 0;
}
