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
#include "පරිපථගත_ජාලය.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int 보드기계주소(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(යොමුව) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (යොමුව)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, බෆරය_ප්_රමාණනය = 2048 };
static struct {
    unsigned char 받기[고리개수][බෆරය_ප්_රමාණනය];
    unsigned char ඊමේල්[고리개수][බෆරය_ප්_රමාණනය];
    uint16_t 소비, 생산;
    int 물리주소, පිළියෙල_කරන්න, 속도;
    uint32_t 집계[5];
    uintptr_t 다음확인;
} පරිපථගත_අගය __attribute__((aligned(64)));

static void සමමු(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void පැහැදිළි_හැඹිලිය(void *දත්ත, unsigned දිග_අගය, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)දත්ත + දිග_අගය;
    for (uintptr_t යොමුව = (uintptr_t)දත්ත & ~(uintptr_t)63; යොමුව < 끝; යොමුව += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(යොමුව) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(යොමුව) : "memory");
    }
#else
    (void)දත්ත; (void)දිග_අගය; (void)받기;
#endif
    සමමු();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned යොමුව, unsigned සූචිය, int ලිවීම, unsigned අගය) {
    uint32_t විධානය = (ලිවීම ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (යොමුව << GENET_MDIO_ADDR_SHIFT) | (සූචිය << GENET_MDIO_REG_SHIFT) | (අගය & 65535);
    유선저장기(GENET_MDIO_CMD) = විධානය;
    유선저장기(GENET_MDIO_CMD) = විධානය | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t තත්වය_අගය = 유선저장기(GENET_MDIO_CMD);
        if (!(තත්වය_අගය & GENET_MDIO_START_BUSY))
            return තත්වය_අගය & GENET_MDIO_READ_FAILED ? -1 : (int)(තත්වය_අගය & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned සූචිය) { return 물리전송(පරිපථගත_අගය.물리주소, සූචිය, 0, 0); }
static int 물리쓰기(unsigned සූචිය, unsigned අගය) { return 물리전송(පරිපථගත_අගය.물리주소, සූචිය, 1, අගය); }
static int 물리준비(void) {
    පරිපථගත_අගය.물리주소 = -1;
    for (unsigned යොමුව = 0; යොමුව < 32; යොමුව++) {
        int 식별 = 물리전송(යොමුව, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { පරිපථගත_අගය.물리주소 = යොමුව; break; }
    }
    if (පරිපථගත_අගය.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int අගය = 물리읽기(BRGPHY_MII_AUXCTL);
    if (අගය < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (අගය & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    අගය = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (අගය < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (අගය & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void පිළියෙල_කරන්න_ලූපය(unsigned පසුබිම_අගය) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ලූපය_අගය = පසුබිම_අගය + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned පිහිටීම = 0; පිහිටීම <= 0x30; පිහිටීම += 4) 유선저장기(ලූපය_අගය + පිහිටීම) = 0;
    유선저장기(ලූපය_අගය + 0x10) = (고리개수 << 16) | බෆරය_ප්_රමාණනය;
    유선저장기(ලූපය_අගය + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (පසුබිම_අගය == GENET_RX_BASE) 유선저장기(ලූපය_අගය + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ලූපය_අගය + 0x24) = 1;
    유선저장기(පසුබිම_අගය + 0x104c) = 8;
    유선저장기(පසුබිම_අගය + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned 자리) {
    uintptr_t යොමුව = (uintptr_t)පරිපථගත_අගය.받기[자리];
    පැහැදිළි_හැඹිලිය((void *)යොමුව, බෆරය_ප්_රමාණනය, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(자리)) = (uint32_t)යොමුව;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(자리)) = (uint64_t)යොමුව >> 32;
    유선저장기(GENET_RX_DESC_STATUS(자리)) = බෆරය_ප්_රමාණනය << 16;
}
static err_t 전문보내기(struct netif *ජංගම_අගය, struct pbuf *전문) {
    if (!පරිපථගත_අගය.පිළියෙල_කරන්න || !netif_is_link_up(ජංගම_අගය)) return ERR_RTE;
    unsigned ප්_රමාණය = 전문->tot_len;
    if (!ප්_රමාණය || ප්_රමාණය > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(පරිපථගත_අගය.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned 자리 = පරිපථගත_අගය.생산 % 고리개수, 송신길이 = ප්_රමාණය < 60 ? 60 : ප්_රමාණය;
    unsigned char *දත්ත = පරිපථගත_අගය.ඊමේල්[자리];
    memset(දත්ත, 0, 송신길이);
    if (pbuf_copy_partial(전문, දත්ත, ප්_රමාණය, 0) != ප්_රමාණය) return ERR_BUF;
    පැහැදිළි_හැඹිලිය(දත්ත, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(자리)) = (uint32_t)(uintptr_t)දත්ත;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(자리)) = (uint64_t)(uintptr_t)දත්ත >> 32;
    유선저장기(GENET_TX_DESC_STATUS(자리)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    සමමු();
    පරිපථගත_අගය.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = පරිපථගත_අගය.생산;
    පරිපථගත_අගය.집계[2]++; පරිපථගත_අගය.집계[3] += ප්_රමාණය;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t පිළියෙල_කරන්න_පරිපථගත_ජාලය(struct netif *ජංගම_අගය) {
    unsigned char යොමුව[6];
    if (!유선장치있음() || !보드기계주소(යොමුව) || (යොමුව[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= යොමුව[순번];
    if (!합) return ERR_IF;
    memset(&පරිපථගත_අගය, 0, sizeof(පරිපථගත_අගය));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)යොමුව[0] << 24 | (uint32_t)යොමුව[1] << 16 | යොමුව[2] << 8 | යොමුව[3];
    유선저장기(GENET_UMAC_MAC1) = යොමුව[4] << 8 | යොමුව[5];
    පිළියෙල_කරන්න_ලූපය(GENET_TX_BASE); පිළියෙල_කරන්න_ලූපය(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    සමමු();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ජංගම_අගය->name[0] = 'e'; ජංගම_අගය->name[1] = 'n'; ජංගම_අගය->mtu = 1500;
    ජංගම_අගය->hwaddr_len = 6; memcpy(ජංගම_අගය->hwaddr, යොමුව, 6);
    ජංගම_අගය->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ජංගම_අගය->output = etharp_output; ජංගම_අගය->linkoutput = 전문보내기;
    පරිපථගත_අගය.පිළියෙල_කරන්න = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ජංගම_අගය) {
    if (!පරිපථගත_අගය.පිළියෙල_කරන්න) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= පරිපථගත_අගය.다음확인) {
        පරිපථගත_අගය.다음확인 = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int තත්වය_අගය = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ක්_රමය_ප්_රකාරය = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ක්_රමය_ප්_රකාරය == 7 ? 1000 : ක්_රමය_ප්_රකාරය == 5 ? 100 : ක්_රමය_ප්_රකාරය == 2 ? 10 : 0;
        පරිපථගත_අගය.속도 = තත්වය_අගය >= 0 && (තත්වය_අගය & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (පරිපථගත_අගය.속도) {
            uint32_t සැකසුම් = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            සැකසුම් &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = සැකසුම් | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            සැකසුම් = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = සැකසුම් | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ජංගම_අගය)) netif_set_link_up(ජංගම_අගය);
        } else if (netif_is_link_up(ජංගම_අගය)) netif_set_link_down(ජංගම_අගය);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - පරිපථගත_අගය.소비);
    if (남음 > 고리개수) { පරිපථගත_අගය.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned 자리 = පරිපථගත_අගය.소비 % 고리개수;
        සමමු();
        uint32_t තත්වය_අගය = 유선저장기(GENET_RX_DESC_STATUS(자리));
        unsigned දිග_අගය = (තත්වය_අගය & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((තත්වය_අගය & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || දිග_අගය < 16 || දිග_අගය > 1538) පරිපථගත_අගය.집계[4]++;
        else {
            පැහැදිළි_හැඹිලිය(පරිපථගත_අගය.받기[자리], දිග_අගය, 1);
            struct pbuf *දත්ත = pbuf_alloc(PBUF_RAW, දිග_අගය - 2, PBUF_POOL);
            if (!දත්ත) පරිපථගත_අගය.집계[4]++;
            else if (pbuf_take(දත්ත, පරිපථගත_අගය.받기[자리] + 2, දිග_අගය - 2) != ERR_OK || ජංගම_අගය->input(දත්ත, ජංගම_අගය) != ERR_OK) {
                pbuf_free(දත්ත); පරිපථගත_අගය.집계[4]++;
            } else { පරිපථගත_අගය.집계[0]++; පරිපථගත_අගය.집계[1] += දිග_අගය - 2; }
        }
        받는주소(자리); සමමු(); පරිපථගත_අගය.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = පරිපථගත_අගය.소비;
    }
}
uint32_t 유선망집계(unsigned පිවිසුම_අගය) {
    return පිවිසුම_අගය < 5 ? පරිපථගත_අගය.집계[පිවිසුම_අගය] : පිවිසුම_අගය == 5 ? පරිපථගත_අගය.속도 : පිවිසුම_අගය == 6 ? පරිපථගත_අගය.පිළියෙල_කරන්න : 0;
}
