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
#include "aláfiwáyàsopọ̀_Alásopọ̀.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int 보드기계주소(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(àdírẹ́ẹ̀sì) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (àdírẹ́ẹ̀sì)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, àká_ìwọn = 2048 };
static struct {
    unsigned char 받기[고리개수][àká_ìwọn];
    unsigned char í_meèlì[고리개수][àká_ìwọn];
    uint16_t 소비, 생산;
    int 물리주소, gbaradì, 속도;
    uint32_t 집계[5];
    uintptr_t 다음확인;
} aláfiwáyàsopọ̀_iye __attribute__((aligned(64)));

static void múdọ́gba(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void 캐시정리(void *détà, unsigned gígùn_iye, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)détà + gígùn_iye;
    for (uintptr_t àdírẹ́ẹ̀sì = (uintptr_t)détà & ~(uintptr_t)63; àdírẹ́ẹ̀sì < 끝; àdírẹ́ẹ̀sì += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(àdírẹ́ẹ̀sì) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(àdírẹ́ẹ̀sì) : "memory");
    }
#else
    (void)détà; (void)gígùn_iye; (void)받기;
#endif
    múdọ́gba();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned àdírẹ́ẹ̀sì, unsigned wá_atọ̀ka_àkóónú, int Kọ, unsigned iye) {
    uint32_t Àṣẹ = (Kọ ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (àdírẹ́ẹ̀sì << GENET_MDIO_ADDR_SHIFT) | (wá_atọ̀ka_àkóónú << GENET_MDIO_REG_SHIFT) | (iye & 65535);
    유선저장기(GENET_MDIO_CMD) = Àṣẹ;
    유선저장기(GENET_MDIO_CMD) = Àṣẹ | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t ipò_iye = 유선저장기(GENET_MDIO_CMD);
        if (!(ipò_iye & GENET_MDIO_START_BUSY))
            return ipò_iye & GENET_MDIO_READ_FAILED ? -1 : (int)(ipò_iye & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned wá_atọ̀ka_àkóónú) { return 물리전송(aláfiwáyàsopọ̀_iye.물리주소, wá_atọ̀ka_àkóónú, 0, 0); }
static int 물리쓰기(unsigned wá_atọ̀ka_àkóónú, unsigned iye) { return 물리전송(aláfiwáyàsopọ̀_iye.물리주소, wá_atọ̀ka_àkóónú, 1, iye); }
static int 물리준비(void) {
    aláfiwáyàsopọ̀_iye.물리주소 = -1;
    for (unsigned àdírẹ́ẹ̀sì = 0; àdírẹ́ẹ̀sì < 32; àdírẹ́ẹ̀sì++) {
        int 식별 = 물리전송(àdírẹ́ẹ̀sì, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { aláfiwáyàsopọ̀_iye.물리주소 = àdírẹ́ẹ̀sì; break; }
    }
    if (aláfiwáyàsopọ̀_iye.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int iye = 물리읽기(BRGPHY_MII_AUXCTL);
    if (iye < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (iye & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    iye = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (iye < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (iye & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void gbaradì_ṣetúnṣe(unsigned Àgbétẹ́lẹ̀_iye) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ṣetúnṣe_iye = Àgbétẹ́lẹ̀_iye + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned 위치 = 0; 위치 <= 0x30; 위치 += 4) 유선저장기(ṣetúnṣe_iye + 위치) = 0;
    유선저장기(ṣetúnṣe_iye + 0x10) = (고리개수 << 16) | àká_ìwọn;
    유선저장기(ṣetúnṣe_iye + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Àgbétẹ́lẹ̀_iye == GENET_RX_BASE) 유선저장기(ṣetúnṣe_iye + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ṣetúnṣe_iye + 0x24) = 1;
    유선저장기(Àgbétẹ́lẹ̀_iye + 0x104c) = 8;
    유선저장기(Àgbétẹ́lẹ̀_iye + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned 자리) {
    uintptr_t àdírẹ́ẹ̀sì = (uintptr_t)aláfiwáyàsopọ̀_iye.받기[자리];
    캐시정리((void *)àdírẹ́ẹ̀sì, àká_ìwọn, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(자리)) = (uint32_t)àdírẹ́ẹ̀sì;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(자리)) = (uint64_t)àdírẹ́ẹ̀sì >> 32;
    유선저장기(GENET_RX_DESC_STATUS(자리)) = àká_ìwọn << 16;
}
static err_t 전문보내기(struct netif *ohun_èlò_iye, struct pbuf *전문) {
    if (!aláfiwáyàsopọ̀_iye.gbaradì || !netif_is_link_up(ohun_èlò_iye)) return ERR_RTE;
    unsigned Ìwọ̀n = 전문->tot_len;
    if (!Ìwọ̀n || Ìwọ̀n > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(aláfiwáyàsopọ̀_iye.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned 자리 = aláfiwáyàsopọ̀_iye.생산 % 고리개수, 송신길이 = Ìwọ̀n < 60 ? 60 : Ìwọ̀n;
    unsigned char *détà = aláfiwáyàsopọ̀_iye.í_meèlì[자리];
    memset(détà, 0, 송신길이);
    if (pbuf_copy_partial(전문, détà, Ìwọ̀n, 0) != Ìwọ̀n) return ERR_BUF;
    캐시정리(détà, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(자리)) = (uint32_t)(uintptr_t)détà;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(자리)) = (uint64_t)(uintptr_t)détà >> 32;
    유선저장기(GENET_TX_DESC_STATUS(자리)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    múdọ́gba();
    aláfiwáyàsopọ̀_iye.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = aláfiwáyàsopọ̀_iye.생산;
    aláfiwáyàsopọ̀_iye.집계[2]++; aláfiwáyàsopọ̀_iye.집계[3] += Ìwọ̀n;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t gbaradì_aláfiwáyàsopọ̀_Alásopọ̀(struct netif *ohun_èlò_iye) {
    unsigned char àdírẹ́ẹ̀sì[6];
    if (!유선장치있음() || !보드기계주소(àdírẹ́ẹ̀sì) || (àdírẹ́ẹ̀sì[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= àdírẹ́ẹ̀sì[순번];
    if (!합) return ERR_IF;
    memset(&aláfiwáyàsopọ̀_iye, 0, sizeof(aláfiwáyàsopọ̀_iye));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)àdírẹ́ẹ̀sì[0] << 24 | (uint32_t)àdírẹ́ẹ̀sì[1] << 16 | àdírẹ́ẹ̀sì[2] << 8 | àdírẹ́ẹ̀sì[3];
    유선저장기(GENET_UMAC_MAC1) = àdírẹ́ẹ̀sì[4] << 8 | àdírẹ́ẹ̀sì[5];
    gbaradì_ṣetúnṣe(GENET_TX_BASE); gbaradì_ṣetúnṣe(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    múdọ́gba();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ohun_èlò_iye->name[0] = 'e'; ohun_èlò_iye->name[1] = 'n'; ohun_èlò_iye->mtu = 1500;
    ohun_èlò_iye->hwaddr_len = 6; memcpy(ohun_èlò_iye->hwaddr, àdírẹ́ẹ̀sì, 6);
    ohun_èlò_iye->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ohun_èlò_iye->output = etharp_output; ohun_èlò_iye->linkoutput = 전문보내기;
    aláfiwáyàsopọ̀_iye.gbaradì = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ohun_èlò_iye) {
    if (!aláfiwáyàsopọ̀_iye.gbaradì) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= aláfiwáyàsopọ̀_iye.다음확인) {
        aláfiwáyàsopọ̀_iye.다음확인 = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int ipò_iye = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ìlànà_móòdù = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ìlànà_móòdù == 7 ? 1000 : ìlànà_móòdù == 5 ? 100 : ìlànà_móòdù == 2 ? 10 : 0;
        aláfiwáyàsopọ̀_iye.속도 = ipò_iye >= 0 && (ipò_iye & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (aláfiwáyàsopọ̀_iye.속도) {
            uint32_t Àwọn_ààtò = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Àwọn_ààtò &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Àwọn_ààtò | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Àwọn_ààtò = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Àwọn_ààtò | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ohun_èlò_iye)) netif_set_link_up(ohun_èlò_iye);
        } else if (netif_is_link_up(ohun_èlò_iye)) netif_set_link_down(ohun_èlò_iye);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - aláfiwáyàsopọ̀_iye.소비);
    if (남음 > 고리개수) { aláfiwáyàsopọ̀_iye.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned 자리 = aláfiwáyàsopọ̀_iye.소비 % 고리개수;
        múdọ́gba();
        uint32_t ipò_iye = 유선저장기(GENET_RX_DESC_STATUS(자리));
        unsigned gígùn_iye = (ipò_iye & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((ipò_iye & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || gígùn_iye < 16 || gígùn_iye > 1538) aláfiwáyàsopọ̀_iye.집계[4]++;
        else {
            캐시정리(aláfiwáyàsopọ̀_iye.받기[자리], gígùn_iye, 1);
            struct pbuf *détà = pbuf_alloc(PBUF_RAW, gígùn_iye - 2, PBUF_POOL);
            if (!détà) aláfiwáyàsopọ̀_iye.집계[4]++;
            else if (pbuf_take(détà, aláfiwáyàsopọ̀_iye.받기[자리] + 2, gígùn_iye - 2) != ERR_OK || ohun_èlò_iye->input(détà, ohun_èlò_iye) != ERR_OK) {
                pbuf_free(détà); aláfiwáyàsopọ̀_iye.집계[4]++;
            } else { aláfiwáyàsopọ̀_iye.집계[0]++; aláfiwáyàsopọ̀_iye.집계[1] += gígùn_iye - 2; }
        }
        받는주소(자리); múdọ́gba(); aláfiwáyàsopọ̀_iye.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = aláfiwáyàsopọ̀_iye.소비;
    }
}
uint32_t 유선망집계(unsigned ìgbéwọlé_iye) {
    return ìgbéwọlé_iye < 5 ? aláfiwáyàsopọ̀_iye.집계[ìgbéwọlé_iye] : ìgbéwọlé_iye == 5 ? aláfiwáyàsopọ̀_iye.속도 : ìgbéwọlé_iye == 6 ? aláfiwáyàsopọ̀_iye.gbaradì : 0;
}
