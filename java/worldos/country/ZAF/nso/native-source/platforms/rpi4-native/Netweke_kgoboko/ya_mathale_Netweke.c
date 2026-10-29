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
#include "ya_mathale_Netweke.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int 보드기계주소(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(atrese) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (atrese)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, pafara_bogolo = 2048 };
static struct {
    unsigned char 받기[고리개수][pafara_bogolo];
    unsigned char Romela[고리개수][pafara_bogolo];
    uint16_t 소비, 생산;
    int 물리주소, Lokišetša, 속도;
    uint32_t 집계[5];
    uintptr_t 다음확인;
} ya_mathale_boleng __attribute__((aligned(64)));

static void kopanya(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void 캐시정리(void *data, unsigned botelele_boleng, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + botelele_boleng;
    for (uintptr_t atrese = (uintptr_t)data & ~(uintptr_t)63; atrese < 끝; atrese += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(atrese) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(atrese) : "memory");
    }
#else
    (void)data; (void)botelele_boleng; (void)받기;
#endif
    kopanya();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned atrese, unsigned lokela, int Ngwala, unsigned boleng) {
    uint32_t Taelo = (Ngwala ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (atrese << GENET_MDIO_ADDR_SHIFT) | (lokela << GENET_MDIO_REG_SHIFT) | (boleng & 65535);
    유선저장기(GENET_MDIO_CMD) = Taelo;
    유선저장기(GENET_MDIO_CMD) = Taelo | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t boemo_boleng = 유선저장기(GENET_MDIO_CMD);
        if (!(boemo_boleng & GENET_MDIO_START_BUSY))
            return boemo_boleng & GENET_MDIO_READ_FAILED ? -1 : (int)(boemo_boleng & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned lokela) { return 물리전송(ya_mathale_boleng.물리주소, lokela, 0, 0); }
static int 물리쓰기(unsigned lokela, unsigned boleng) { return 물리전송(ya_mathale_boleng.물리주소, lokela, 1, boleng); }
static int 물리준비(void) {
    ya_mathale_boleng.물리주소 = -1;
    for (unsigned atrese = 0; atrese < 32; atrese++) {
        int 식별 = 물리전송(atrese, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ya_mathale_boleng.물리주소 = atrese; break; }
    }
    if (ya_mathale_boleng.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int boleng = 물리읽기(BRGPHY_MII_AUXCTL);
    if (boleng < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (boleng & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    boleng = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (boleng < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (boleng & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Lokišetša_ditaelopoeletšwa(unsigned Bokamorago_boleng) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ditaelopoeletšwa_boleng = Bokamorago_boleng + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned 위치 = 0; 위치 <= 0x30; 위치 += 4) 유선저장기(ditaelopoeletšwa_boleng + 위치) = 0;
    유선저장기(ditaelopoeletšwa_boleng + 0x10) = (고리개수 << 16) | pafara_bogolo;
    유선저장기(ditaelopoeletšwa_boleng + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Bokamorago_boleng == GENET_RX_BASE) 유선저장기(ditaelopoeletšwa_boleng + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ditaelopoeletšwa_boleng + 0x24) = 1;
    유선저장기(Bokamorago_boleng + 0x104c) = 8;
    유선저장기(Bokamorago_boleng + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned 자리) {
    uintptr_t atrese = (uintptr_t)ya_mathale_boleng.받기[자리];
    캐시정리((void *)atrese, pafara_bogolo, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(자리)) = (uint32_t)atrese;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(자리)) = (uint64_t)atrese >> 32;
    유선저장기(GENET_RX_DESC_STATUS(자리)) = pafara_bogolo << 16;
}
static err_t 전문보내기(struct netif *sedirišwa_boleng, struct pbuf *전문) {
    if (!ya_mathale_boleng.Lokišetša || !netif_is_link_up(sedirišwa_boleng)) return ERR_RTE;
    unsigned Bogolo = 전문->tot_len;
    if (!Bogolo || Bogolo > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ya_mathale_boleng.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned 자리 = ya_mathale_boleng.생산 % 고리개수, 송신길이 = Bogolo < 60 ? 60 : Bogolo;
    unsigned char *data = ya_mathale_boleng.Romela[자리];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(전문, data, Bogolo, 0) != Bogolo) return ERR_BUF;
    캐시정리(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(자리)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(자리)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(자리)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    kopanya();
    ya_mathale_boleng.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ya_mathale_boleng.생산;
    ya_mathale_boleng.집계[2]++; ya_mathale_boleng.집계[3] += Bogolo;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Lokišetša_ya_mathale_Netweke(struct netif *sedirišwa_boleng) {
    unsigned char atrese[6];
    if (!유선장치있음() || !보드기계주소(atrese) || (atrese[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= atrese[순번];
    if (!합) return ERR_IF;
    memset(&ya_mathale_boleng, 0, sizeof(ya_mathale_boleng));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)atrese[0] << 24 | (uint32_t)atrese[1] << 16 | atrese[2] << 8 | atrese[3];
    유선저장기(GENET_UMAC_MAC1) = atrese[4] << 8 | atrese[5];
    Lokišetša_ditaelopoeletšwa(GENET_TX_BASE); Lokišetša_ditaelopoeletšwa(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    kopanya();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    sedirišwa_boleng->name[0] = 'e'; sedirišwa_boleng->name[1] = 'n'; sedirišwa_boleng->mtu = 1500;
    sedirišwa_boleng->hwaddr_len = 6; memcpy(sedirišwa_boleng->hwaddr, atrese, 6);
    sedirišwa_boleng->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    sedirišwa_boleng->output = etharp_output; sedirišwa_boleng->linkoutput = 전문보내기;
    ya_mathale_boleng.Lokišetša = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *sedirišwa_boleng) {
    if (!ya_mathale_boleng.Lokišetša) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= ya_mathale_boleng.다음확인) {
        ya_mathale_boleng.다음확인 = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int boemo_boleng = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned mokgwa_mokgwa = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = mokgwa_mokgwa == 7 ? 1000 : mokgwa_mokgwa == 5 ? 100 : mokgwa_mokgwa == 2 ? 10 : 0;
        ya_mathale_boleng.속도 = boemo_boleng >= 0 && (boemo_boleng & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ya_mathale_boleng.속도) {
            uint32_t Dipeakanyo = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Dipeakanyo &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Dipeakanyo | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Dipeakanyo = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Dipeakanyo | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(sedirišwa_boleng)) netif_set_link_up(sedirišwa_boleng);
        } else if (netif_is_link_up(sedirišwa_boleng)) netif_set_link_down(sedirišwa_boleng);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ya_mathale_boleng.소비);
    if (남음 > 고리개수) { ya_mathale_boleng.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned 자리 = ya_mathale_boleng.소비 % 고리개수;
        kopanya();
        uint32_t boemo_boleng = 유선저장기(GENET_RX_DESC_STATUS(자리));
        unsigned botelele_boleng = (boemo_boleng & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((boemo_boleng & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || botelele_boleng < 16 || botelele_boleng > 1538) ya_mathale_boleng.집계[4]++;
        else {
            캐시정리(ya_mathale_boleng.받기[자리], botelele_boleng, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, botelele_boleng - 2, PBUF_POOL);
            if (!data) ya_mathale_boleng.집계[4]++;
            else if (pbuf_take(data, ya_mathale_boleng.받기[자리] + 2, botelele_boleng - 2) != ERR_OK || sedirišwa_boleng->input(data, sedirišwa_boleng) != ERR_OK) {
                pbuf_free(data); ya_mathale_boleng.집계[4]++;
            } else { ya_mathale_boleng.집계[0]++; ya_mathale_boleng.집계[1] += botelele_boleng - 2; }
        }
        받는주소(자리); kopanya(); ya_mathale_boleng.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ya_mathale_boleng.소비;
    }
}
uint32_t 유선망집계(unsigned go_tsenya_tshedimošo_boleng) {
    return go_tsenya_tshedimošo_boleng < 5 ? ya_mathale_boleng.집계[go_tsenya_tshedimošo_boleng] : go_tsenya_tshedimošo_boleng == 5 ? ya_mathale_boleng.속도 : go_tsenya_tshedimošo_boleng == 6 ? ya_mathale_boleng.Lokišetša : 0;
}
