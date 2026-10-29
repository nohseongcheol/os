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
#include "తంత్రీసంధాన_నెట్_వర్క్.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int బోర్డు_యంత్రం_ఇమెయిల్(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ఇమెయిల్) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ఇమెయిల్)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, బఫర్_పరిమాణం_మార్చు = 2048 };
static struct {
    unsigned char 받기[고리개수][బఫర్_పరిమాణం_మార్చు];
    unsigned char పంపు[고리개수][బఫర్_పరిమాణం_మార్చు];
    uint16_t 소비, 생산;
    int 물리주소, సిద్ధం_చేయు, 속도;
    uint32_t 집계[5];
    uintptr_t సరిచూడు_తదుపరి_అంశం;
} తంత్రీసంధాన_మూల్యం __attribute__((aligned(64)));

static void సింక్(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void పరిశుభ్రమైన_కాష్(void *డేటా, unsigned పొడవు_మూల్యం, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)డేటా + పొడవు_మూల్యం;
    for (uintptr_t ఇమెయిల్ = (uintptr_t)డేటా & ~(uintptr_t)63; ఇమెయిల్ < 끝; ఇమెయిల్ += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ఇమెయిల్) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ఇమెయిల్) : "memory");
    }
#else
    (void)డేటా; (void)పొడవు_మూల్యం; (void)받기;
#endif
    సింక్();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ఇమెయిల్, unsigned సూచీ, int వ్రాయుము, unsigned మూల్యం) {
    uint32_t ఆదేశము = (వ్రాయుము ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ఇమెయిల్ << GENET_MDIO_ADDR_SHIFT) | (సూచీ << GENET_MDIO_REG_SHIFT) | (మూల్యం & 65535);
    유선저장기(GENET_MDIO_CMD) = ఆదేశము;
    유선저장기(GENET_MDIO_CMD) = ఆదేశము | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t స్థితి_మూల్యం = 유선저장기(GENET_MDIO_CMD);
        if (!(స్థితి_మూల్యం & GENET_MDIO_START_BUSY))
            return స్థితి_మూల్యం & GENET_MDIO_READ_FAILED ? -1 : (int)(స్థితి_మూల్యం & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned సూచీ) { return 물리전송(తంత్రీసంధాన_మూల్యం.물리주소, సూచీ, 0, 0); }
static int 물리쓰기(unsigned సూచీ, unsigned మూల్యం) { return 물리전송(తంత్రీసంధాన_మూల్యం.물리주소, సూచీ, 1, మూల్యం); }
static int 물리준비(void) {
    తంత్రీసంధాన_మూల్యం.물리주소 = -1;
    for (unsigned ఇమెయిల్ = 0; ఇమెయిల్ < 32; ఇమెయిల్++) {
        int 식별 = 물리전송(ఇమెయిల్, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { తంత్రీసంధాన_మూల్యం.물리주소 = ఇమెయిల్; break; }
    }
    if (తంత్రీసంధాన_మూల్యం.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int మూల్యం = 물리읽기(BRGPHY_MII_AUXCTL);
    if (మూల్యం < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (మూల్యం & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    మూల్యం = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (మూల్యం < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (మూల్యం & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void సిద్ధం_చేయు_లూప్(unsigned నేపథ్యం_మూల్యం) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned లూప్_మూల్యం = నేపథ్యం_మూల్యం + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned స్థానము = 0; స్థానము <= 0x30; స్థానము += 4) 유선저장기(లూప్_మూల్యం + స్థానము) = 0;
    유선저장기(లూప్_మూల్యం + 0x10) = (고리개수 << 16) | బఫర్_పరిమాణం_మార్చు;
    유선저장기(లూప్_మూల్యం + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (నేపథ్యం_మూల్యం == GENET_RX_BASE) 유선저장기(లూప్_మూల్యం + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(లూప్_మూల్యం + 0x24) = 1;
    유선저장기(నేపథ్యం_మూల్యం + 0x104c) = 8;
    유선저장기(నేపథ్యం_మూల్యం + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned స్థాయి_సూచీ) {
    uintptr_t ఇమెయిల్ = (uintptr_t)తంత్రీసంధాన_మూల్యం.받기[స్థాయి_సూచీ];
    పరిశుభ్రమైన_కాష్((void *)ఇమెయిల్, బఫర్_పరిమాణం_మార్చు, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(స్థాయి_సూచీ)) = (uint32_t)ఇమెయిల్;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(స్థాయి_సూచీ)) = (uint64_t)ఇమెయిల్ >> 32;
    유선저장기(GENET_RX_DESC_STATUS(స్థాయి_సూచీ)) = బఫర్_పరిమాణం_మార్చు << 16;
}
static err_t 전문보내기(struct netif *పరికరం_మూల్యం, struct pbuf *전문) {
    if (!తంత్రీసంధాన_మూల్యం.సిద్ధం_చేయు || !netif_is_link_up(పరికరం_మూల్యం)) return ERR_RTE;
    unsigned పరిమాణం = 전문->tot_len;
    if (!పరిమాణం || పరిమాణం > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(తంత్రీసంధాన_మూల్యం.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned స్థాయి_సూచీ = తంత్రీసంధాన_మూల్యం.생산 % 고리개수, 송신길이 = పరిమాణం < 60 ? 60 : పరిమాణం;
    unsigned char *డేటా = తంత్రీసంధాన_మూల్యం.పంపు[స్థాయి_సూచీ];
    memset(డేటా, 0, 송신길이);
    if (pbuf_copy_partial(전문, డేటా, పరిమాణం, 0) != పరిమాణం) return ERR_BUF;
    పరిశుభ్రమైన_కాష్(డేటా, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(స్థాయి_సూచీ)) = (uint32_t)(uintptr_t)డేటా;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(స్థాయి_సూచీ)) = (uint64_t)(uintptr_t)డేటా >> 32;
    유선저장기(GENET_TX_DESC_STATUS(స్థాయి_సూచీ)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    సింక్();
    తంత్రీసంధాన_మూల్యం.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = తంత్రీసంధాన_మూల్యం.생산;
    తంత్రీసంధాన_మూల్యం.집계[2]++; తంత్రీసంధాన_మూల్యం.집계[3] += పరిమాణం;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t సిద్ధం_చేయు_తంత్రీసంధాన_నెట్_వర్క్(struct netif *పరికరం_మూల్యం) {
    unsigned char ఇమెయిల్[6];
    if (!유선장치있음() || !బోర్డు_యంత్రం_ఇమెయిల్(ఇమెయిల్) || (ఇమెయిల్[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= ఇమెయిల్[순번];
    if (!합) return ERR_IF;
    memset(&తంత్రీసంధాన_మూల్యం, 0, sizeof(తంత్రీసంధాన_మూల్యం));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ఇమెయిల్[0] << 24 | (uint32_t)ఇమెయిల్[1] << 16 | ఇమెయిల్[2] << 8 | ఇమెయిల్[3];
    유선저장기(GENET_UMAC_MAC1) = ఇమెయిల్[4] << 8 | ఇమెయిల్[5];
    సిద్ధం_చేయు_లూప్(GENET_TX_BASE); సిద్ధం_చేయు_లూప్(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    సింక్();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    పరికరం_మూల్యం->name[0] = 'e'; పరికరం_మూల్యం->name[1] = 'n'; పరికరం_మూల్యం->mtu = 1500;
    పరికరం_మూల్యం->hwaddr_len = 6; memcpy(పరికరం_మూల్యం->hwaddr, ఇమెయిల్, 6);
    పరికరం_మూల్యం->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    పరికరం_మూల్యం->output = etharp_output; పరికరం_మూల్యం->linkoutput = 전문보내기;
    తంత్రీసంధాన_మూల్యం.సిద్ధం_చేయు = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *పరికరం_మూల్యం) {
    if (!తంత్రీసంధాన_మూల్యం.సిద్ధం_చేయు) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= తంత్రీసంధాన_మూల్యం.సరిచూడు_తదుపరి_అంశం) {
        తంత్రీసంధాన_మూల్యం.సరిచూడు_తదుపరి_అంశం = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int స్థితి_మూల్యం = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned విధానం_మోడ్_3f5e5497 = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = విధానం_మోడ్_3f5e5497 == 7 ? 1000 : విధానం_మోడ్_3f5e5497 == 5 ? 100 : విధానం_మోడ్_3f5e5497 == 2 ? 10 : 0;
        తంత్రీసంధాన_మూల్యం.속도 = స్థితి_మూల్యం >= 0 && (స్థితి_మూల్యం & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (తంత్రీసంధాన_మూల్యం.속도) {
            uint32_t అమరికలు = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            అమరికలు &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = అమరికలు | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            అమరికలు = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = అమరికలు | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(పరికరం_మూల్యం)) netif_set_link_up(పరికరం_మూల్యం);
        } else if (netif_is_link_up(పరికరం_మూల్యం)) netif_set_link_down(పరికరం_మూల్యం);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - తంత్రీసంధాన_మూల్యం.소비);
    if (남음 > 고리개수) { తంత్రీసంధాన_మూల్యం.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned స్థాయి_సూచీ = తంత్రీసంధాన_మూల్యం.소비 % 고리개수;
        సింక్();
        uint32_t స్థితి_మూల్యం = 유선저장기(GENET_RX_DESC_STATUS(స్థాయి_సూచీ));
        unsigned పొడవు_మూల్యం = (స్థితి_మూల్యం & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((స్థితి_మూల్యం & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || పొడవు_మూల్యం < 16 || పొడవు_మూల్యం > 1538) తంత్రీసంధాన_మూల్యం.집계[4]++;
        else {
            పరిశుభ్రమైన_కాష్(తంత్రీసంధాన_మూల్యం.받기[స్థాయి_సూచీ], పొడవు_మూల్యం, 1);
            struct pbuf *డేటా = pbuf_alloc(PBUF_RAW, పొడవు_మూల్యం - 2, PBUF_POOL);
            if (!డేటా) తంత్రీసంధాన_మూల్యం.집계[4]++;
            else if (pbuf_take(డేటా, తంత్రీసంధాన_మూల్యం.받기[స్థాయి_సూచీ] + 2, పొడవు_మూల్యం - 2) != ERR_OK || పరికరం_మూల్యం->input(డేటా, పరికరం_మూల్యం) != ERR_OK) {
                pbuf_free(డేటా); తంత్రీసంధాన_మూల్యం.집계[4]++;
            } else { తంత్రీసంధాన_మూల్యం.집계[0]++; తంత్రీసంధాన_మూల్యం.집계[1] += పొడవు_మూల్యం - 2; }
        }
        받는주소(స్థాయి_సూచీ); సింక్(); తంత్రీసంధాన_మూల్యం.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = తంత్రీసంధాన_మూల్యం.소비;
    }
}
uint32_t 유선망집계(unsigned ప్రవేశం_మూల్యం) {
    return ప్రవేశం_మూల్యం < 5 ? తంత్రీసంధాన_మూల్యం.집계[ప్రవేశం_మూల్యం] : ప్రవేశం_మూల్యం == 5 ? తంత్రీసంధాన_మూల్యం.속도 : ప్రవేశం_మూల్యం == 6 ? తంత్రీసంధాన_మూల్యం.సిద్ధం_చేయు : 0;
}
