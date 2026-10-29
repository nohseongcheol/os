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
#include "akaaulejuushi_kusu.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int 보드기계주소(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ejepüsee) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ejepüsee)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, 완충크기 = 2048 };
static struct {
    unsigned char 받기[고리개수][완충크기];
    unsigned char ajütaa[고리개수][완충크기];
    uint16_t 소비, 생산;
    int 물리주소, 준비, 속도;
    uint32_t 집계[5];
    uintptr_t 다음확인;
} akaaulejuushi_ajutuu __attribute__((aligned(64)));

static void awanaawajaa(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void 캐시정리(void *atijaaya, unsigned akaliaa_ajutuu, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)atijaaya + akaliaa_ajutuu;
    for (uintptr_t ejepüsee = (uintptr_t)atijaaya & ~(uintptr_t)63; ejepüsee < 끝; ejepüsee += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ejepüsee) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ejepüsee) : "memory");
    }
#else
    (void)atijaaya; (void)akaliaa_ajutuu; (void)받기;
#endif
    awanaawajaa();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ejepüsee, unsigned ee_iyatialujuna, int ashajaa, unsigned ajutuu) {
    uint32_t aluwataaya = (ashajaa ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ejepüsee << GENET_MDIO_ADDR_SHIFT) | (ee_iyatialujuna << GENET_MDIO_REG_SHIFT) | (ajutuu & 65535);
    유선저장기(GENET_MDIO_CMD) = aluwataaya;
    유선저장기(GENET_MDIO_CMD) = aluwataaya | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t jamakua_iparülein_ajutuu = 유선저장기(GENET_MDIO_CMD);
        if (!(jamakua_iparülein_ajutuu & GENET_MDIO_START_BUSY))
            return jamakua_iparülein_ajutuu & GENET_MDIO_READ_FAILED ? -1 : (int)(jamakua_iparülein_ajutuu & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ee_iyatialujuna) { return 물리전송(akaaulejuushi_ajutuu.물리주소, ee_iyatialujuna, 0, 0); }
static int 물리쓰기(unsigned ee_iyatialujuna, unsigned ajutuu) { return 물리전송(akaaulejuushi_ajutuu.물리주소, ee_iyatialujuna, 1, ajutuu); }
static int 물리준비(void) {
    akaaulejuushi_ajutuu.물리주소 = -1;
    for (unsigned ejepüsee = 0; ejepüsee < 32; ejepüsee++) {
        int 식별 = 물리전송(ejepüsee, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { akaaulejuushi_ajutuu.물리주소 = ejepüsee; break; }
    }
    if (akaaulejuushi_ajutuu.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ajutuu = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ajutuu < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ajutuu & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ajutuu = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ajutuu < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ajutuu & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void 고리준비(unsigned apa_ajanaa_ajutuu) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned eitawaakualü_ajutuu = apa_ajanaa_ajutuu + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned 위치 = 0; 위치 <= 0x30; 위치 += 4) 유선저장기(eitawaakualü_ajutuu + 위치) = 0;
    유선저장기(eitawaakualü_ajutuu + 0x10) = (고리개수 << 16) | 완충크기;
    유선저장기(eitawaakualü_ajutuu + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (apa_ajanaa_ajutuu == GENET_RX_BASE) 유선저장기(eitawaakualü_ajutuu + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(eitawaakualü_ajutuu + 0x24) = 1;
    유선저장기(apa_ajanaa_ajutuu + 0x104c) = 8;
    유선저장기(apa_ajanaa_ajutuu + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned 자리) {
    uintptr_t ejepüsee = (uintptr_t)akaaulejuushi_ajutuu.받기[자리];
    캐시정리((void *)ejepüsee, 완충크기, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(자리)) = (uint32_t)ejepüsee;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(자리)) = (uint64_t)ejepüsee >> 32;
    유선저장기(GENET_RX_DESC_STATUS(자리)) = 완충크기 << 16;
}
static err_t 전문보내기(struct netif *serulaalü_ajutuu, struct pbuf *전문) {
    if (!akaaulejuushi_ajutuu.준비 || !netif_is_link_up(serulaalü_ajutuu)) return ERR_RTE;
    unsigned 크기 = 전문->tot_len;
    if (!크기 || 크기 > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(akaaulejuushi_ajutuu.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned 자리 = akaaulejuushi_ajutuu.생산 % 고리개수, 송신길이 = 크기 < 60 ? 60 : 크기;
    unsigned char *atijaaya = akaaulejuushi_ajutuu.ajütaa[자리];
    memset(atijaaya, 0, 송신길이);
    if (pbuf_copy_partial(전문, atijaaya, 크기, 0) != 크기) return ERR_BUF;
    캐시정리(atijaaya, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(자리)) = (uint32_t)(uintptr_t)atijaaya;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(자리)) = (uint64_t)(uintptr_t)atijaaya >> 32;
    유선저장기(GENET_TX_DESC_STATUS(자리)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    awanaawajaa();
    akaaulejuushi_ajutuu.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = akaaulejuushi_ajutuu.생산;
    akaaulejuushi_ajutuu.집계[2]++; akaaulejuushi_ajutuu.집계[3] += 크기;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t 유선망준비(struct netif *serulaalü_ajutuu) {
    unsigned char ejepüsee[6];
    if (!유선장치있음() || !보드기계주소(ejepüsee) || (ejepüsee[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= ejepüsee[순번];
    if (!합) return ERR_IF;
    memset(&akaaulejuushi_ajutuu, 0, sizeof(akaaulejuushi_ajutuu));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ejepüsee[0] << 24 | (uint32_t)ejepüsee[1] << 16 | ejepüsee[2] << 8 | ejepüsee[3];
    유선저장기(GENET_UMAC_MAC1) = ejepüsee[4] << 8 | ejepüsee[5];
    고리준비(GENET_TX_BASE); 고리준비(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    awanaawajaa();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    serulaalü_ajutuu->name[0] = 'e'; serulaalü_ajutuu->name[1] = 'n'; serulaalü_ajutuu->mtu = 1500;
    serulaalü_ajutuu->hwaddr_len = 6; memcpy(serulaalü_ajutuu->hwaddr, ejepüsee, 6);
    serulaalü_ajutuu->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    serulaalü_ajutuu->output = etharp_output; serulaalü_ajutuu->linkoutput = 전문보내기;
    akaaulejuushi_ajutuu.준비 = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *serulaalü_ajutuu) {
    if (!akaaulejuushi_ajutuu.준비) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= akaaulejuushi_ajutuu.다음확인) {
        akaaulejuushi_ajutuu.다음확인 = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int jamakua_iparülein_ajutuu = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned 방식 = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = 방식 == 7 ? 1000 : 방식 == 5 ? 100 : 방식 == 2 ? 10 : 0;
        akaaulejuushi_ajutuu.속도 = jamakua_iparülein_ajutuu >= 0 && (jamakua_iparülein_ajutuu & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (akaaulejuushi_ajutuu.속도) {
            uint32_t 설정 = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            설정 &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = 설정 | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            설정 = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = 설정 | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(serulaalü_ajutuu)) netif_set_link_up(serulaalü_ajutuu);
        } else if (netif_is_link_up(serulaalü_ajutuu)) netif_set_link_down(serulaalü_ajutuu);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - akaaulejuushi_ajutuu.소비);
    if (남음 > 고리개수) { akaaulejuushi_ajutuu.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned 자리 = akaaulejuushi_ajutuu.소비 % 고리개수;
        awanaawajaa();
        uint32_t jamakua_iparülein_ajutuu = 유선저장기(GENET_RX_DESC_STATUS(자리));
        unsigned akaliaa_ajutuu = (jamakua_iparülein_ajutuu & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((jamakua_iparülein_ajutuu & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || akaliaa_ajutuu < 16 || akaliaa_ajutuu > 1538) akaaulejuushi_ajutuu.집계[4]++;
        else {
            캐시정리(akaaulejuushi_ajutuu.받기[자리], akaliaa_ajutuu, 1);
            struct pbuf *atijaaya = pbuf_alloc(PBUF_RAW, akaliaa_ajutuu - 2, PBUF_POOL);
            if (!atijaaya) akaaulejuushi_ajutuu.집계[4]++;
            else if (pbuf_take(atijaaya, akaaulejuushi_ajutuu.받기[자리] + 2, akaliaa_ajutuu - 2) != ERR_OK || serulaalü_ajutuu->input(atijaaya, serulaalü_ajutuu) != ERR_OK) {
                pbuf_free(atijaaya); akaaulejuushi_ajutuu.집계[4]++;
            } else { akaaulejuushi_ajutuu.집계[0]++; akaaulejuushi_ajutuu.집계[1] += akaliaa_ajutuu - 2; }
        }
        받는주소(자리); awanaawajaa(); akaaulejuushi_ajutuu.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = akaaulejuushi_ajutuu.소비;
    }
}
uint32_t 유선망집계(unsigned ekeroliaa_ajutuu) {
    return ekeroliaa_ajutuu < 5 ? akaaulejuushi_ajutuu.집계[ekeroliaa_ajutuu] : ekeroliaa_ajutuu == 5 ? akaaulejuushi_ajutuu.속도 : ekeroliaa_ajutuu == 6 ? akaaulejuushi_ajutuu.준비 : 0;
}
