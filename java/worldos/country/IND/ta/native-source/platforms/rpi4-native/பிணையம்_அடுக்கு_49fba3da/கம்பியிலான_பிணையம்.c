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
#include "கம்பியிலான_பிணையம்.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int போர்டு_இயந்திரம்_முகவரி(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(முகவரி) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (முகவரி)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, இடையக_அளவு = 2048 };
static struct {
    unsigned char 받기[고리개수][இடையக_அளவு];
    unsigned char அனுப்பு[고리개수][இடையக_அளவு];
    uint16_t 소비, 생산;
    int 물리주소, தயார்படுத்த, 속도;
    uint32_t 집계[5];
    uintptr_t சரிபார்_அடுத்து_உருப்படி;
} கம்பியிலான_மதிப்பு __attribute__((aligned(64)));

static void ஒத்திசை(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void சுத்தமான_தேக்கு(void *தரவு, unsigned நீளம்_மதிப்பு, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)தரவு + நீளம்_மதிப்பு;
    for (uintptr_t முகவரி = (uintptr_t)தரவு & ~(uintptr_t)63; முகவரி < 끝; முகவரி += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(முகவரி) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(முகவரி) : "memory");
    }
#else
    (void)தரவு; (void)நீளம்_மதிப்பு; (void)받기;
#endif
    ஒத்திசை();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned முகவரி, unsigned அடைவு, int எழுது, unsigned மதிப்பு) {
    uint32_t கட்டளை = (எழுது ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (முகவரி << GENET_MDIO_ADDR_SHIFT) | (அடைவு << GENET_MDIO_REG_SHIFT) | (மதிப்பு & 65535);
    유선저장기(GENET_MDIO_CMD) = கட்டளை;
    유선저장기(GENET_MDIO_CMD) = கட்டளை | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t நிலை_மதிப்பு_e10195a1 = 유선저장기(GENET_MDIO_CMD);
        if (!(நிலை_மதிப்பு_e10195a1 & GENET_MDIO_START_BUSY))
            return நிலை_மதிப்பு_e10195a1 & GENET_MDIO_READ_FAILED ? -1 : (int)(நிலை_மதிப்பு_e10195a1 & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned அடைவு) { return 물리전송(கம்பியிலான_மதிப்பு.물리주소, அடைவு, 0, 0); }
static int 물리쓰기(unsigned அடைவு, unsigned மதிப்பு) { return 물리전송(கம்பியிலான_மதிப்பு.물리주소, அடைவு, 1, மதிப்பு); }
static int 물리준비(void) {
    கம்பியிலான_மதிப்பு.물리주소 = -1;
    for (unsigned முகவரி = 0; முகவரி < 32; முகவரி++) {
        int 식별 = 물리전송(முகவரி, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { கம்பியிலான_மதிப்பு.물리주소 = முகவரி; break; }
    }
    if (கம்பியிலான_மதிப்பு.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int மதிப்பு = 물리읽기(BRGPHY_MII_AUXCTL);
    if (மதிப்பு < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (மதிப்பு & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    மதிப்பு = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (மதிப்பு < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (மதிப்பு & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void தயார்படுத்த_சுழற்சி(unsigned பின்புல_மதிப்பு) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned சுழற்சி_மதிப்பு = பின்புல_மதிப்பு + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned இடம் = 0; இடம் <= 0x30; இடம் += 4) 유선저장기(சுழற்சி_மதிப்பு + இடம்) = 0;
    유선저장기(சுழற்சி_மதிப்பு + 0x10) = (고리개수 << 16) | இடையக_அளவு;
    유선저장기(சுழற்சி_மதிப்பு + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (பின்புல_மதிப்பு == GENET_RX_BASE) 유선저장기(சுழற்சி_மதிப்பு + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(சுழற்சி_மதிப்பு + 0x24) = 1;
    유선저장기(பின்புல_மதிப்பு + 0x104c) = 8;
    유선저장기(பின்புல_மதிப்பு + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned நிலை_அடைவு) {
    uintptr_t முகவரி = (uintptr_t)கம்பியிலான_மதிப்பு.받기[நிலை_அடைவு];
    சுத்தமான_தேக்கு((void *)முகவரி, இடையக_அளவு, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(நிலை_அடைவு)) = (uint32_t)முகவரி;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(நிலை_அடைவு)) = (uint64_t)முகவரி >> 32;
    유선저장기(GENET_RX_DESC_STATUS(நிலை_அடைவு)) = இடையக_அளவு << 16;
}
static err_t 전문보내기(struct netif *சாதனம்_மதிப்பு, struct pbuf *전문) {
    if (!கம்பியிலான_மதிப்பு.தயார்படுத்த || !netif_is_link_up(சாதனம்_மதிப்பு)) return ERR_RTE;
    unsigned அளவு = 전문->tot_len;
    if (!அளவு || அளவு > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(கம்பியிலான_மதிப்பு.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned நிலை_அடைவு = கம்பியிலான_மதிப்பு.생산 % 고리개수, 송신길이 = அளவு < 60 ? 60 : அளவு;
    unsigned char *தரவு = கம்பியிலான_மதிப்பு.அனுப்பு[நிலை_அடைவு];
    memset(தரவு, 0, 송신길이);
    if (pbuf_copy_partial(전문, தரவு, அளவு, 0) != அளவு) return ERR_BUF;
    சுத்தமான_தேக்கு(தரவு, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(நிலை_அடைவு)) = (uint32_t)(uintptr_t)தரவு;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(நிலை_அடைவு)) = (uint64_t)(uintptr_t)தரவு >> 32;
    유선저장기(GENET_TX_DESC_STATUS(நிலை_அடைவு)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    ஒத்திசை();
    கம்பியிலான_மதிப்பு.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = கம்பியிலான_மதிப்பு.생산;
    கம்பியிலான_மதிப்பு.집계[2]++; கம்பியிலான_மதிப்பு.집계[3] += அளவு;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t தயார்படுத்த_கம்பியிலான_பிணையம்(struct netif *சாதனம்_மதிப்பு) {
    unsigned char முகவரி[6];
    if (!유선장치있음() || !போர்டு_இயந்திரம்_முகவரி(முகவரி) || (முகவரி[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= முகவரி[순번];
    if (!합) return ERR_IF;
    memset(&கம்பியிலான_மதிப்பு, 0, sizeof(கம்பியிலான_மதிப்பு));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)முகவரி[0] << 24 | (uint32_t)முகவரி[1] << 16 | முகவரி[2] << 8 | முகவரி[3];
    유선저장기(GENET_UMAC_MAC1) = முகவரி[4] << 8 | முகவரி[5];
    தயார்படுத்த_சுழற்சி(GENET_TX_BASE); தயார்படுத்த_சுழற்சி(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    ஒத்திசை();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    சாதனம்_மதிப்பு->name[0] = 'e'; சாதனம்_மதிப்பு->name[1] = 'n'; சாதனம்_மதிப்பு->mtu = 1500;
    சாதனம்_மதிப்பு->hwaddr_len = 6; memcpy(சாதனம்_மதிப்பு->hwaddr, முகவரி, 6);
    சாதனம்_மதிப்பு->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    சாதனம்_மதிப்பு->output = etharp_output; சாதனம்_மதிப்பு->linkoutput = 전문보내기;
    கம்பியிலான_மதிப்பு.தயார்படுத்த = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *சாதனம்_மதிப்பு) {
    if (!கம்பியிலான_மதிப்பு.தயார்படுத்த) return;
    uintptr_t தொடர்புடையவை_மதிப்பு = 보드밀리초();
    if (தொடர்புடையவை_மதிப்பு >= கம்பியிலான_மதிப்பு.சரிபார்_அடுத்து_உருப்படி) {
        கம்பியிலான_மதிப்பு.சரிபார்_அடுத்து_உருப்படி = தொடர்புடையவை_மதிப்பு + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int நிலை_மதிப்பு_e10195a1 = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned முறை_பயன்முறை = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = முறை_பயன்முறை == 7 ? 1000 : முறை_பயன்முறை == 5 ? 100 : முறை_பயன்முறை == 2 ? 10 : 0;
        கம்பியிலான_மதிப்பு.속도 = நிலை_மதிப்பு_e10195a1 >= 0 && (நிலை_மதிப்பு_e10195a1 & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (கம்பியிலான_மதிப்பு.속도) {
            uint32_t அமைப்புகள் = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            அமைப்புகள் &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = அமைப்புகள் | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            அமைப்புகள் = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = அமைப்புகள் | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(சாதனம்_மதிப்பு)) netif_set_link_up(சாதனம்_மதிப்பு);
        } else if (netif_is_link_up(சாதனம்_மதிப்பு)) netif_set_link_down(சாதனம்_மதிப்பு);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - கம்பியிலான_மதிப்பு.소비);
    if (남음 > 고리개수) { கம்பியிலான_மதிப்பு.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned நிலை_அடைவு = கம்பியிலான_மதிப்பு.소비 % 고리개수;
        ஒத்திசை();
        uint32_t நிலை_மதிப்பு_e10195a1 = 유선저장기(GENET_RX_DESC_STATUS(நிலை_அடைவு));
        unsigned நீளம்_மதிப்பு = (நிலை_மதிப்பு_e10195a1 & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((நிலை_மதிப்பு_e10195a1 & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || நீளம்_மதிப்பு < 16 || நீளம்_மதிப்பு > 1538) கம்பியிலான_மதிப்பு.집계[4]++;
        else {
            சுத்தமான_தேக்கு(கம்பியிலான_மதிப்பு.받기[நிலை_அடைவு], நீளம்_மதிப்பு, 1);
            struct pbuf *தரவு = pbuf_alloc(PBUF_RAW, நீளம்_மதிப்பு - 2, PBUF_POOL);
            if (!தரவு) கம்பியிலான_மதிப்பு.집계[4]++;
            else if (pbuf_take(தரவு, கம்பியிலான_மதிப்பு.받기[நிலை_அடைவு] + 2, நீளம்_மதிப்பு - 2) != ERR_OK || சாதனம்_மதிப்பு->input(தரவு, சாதனம்_மதிப்பு) != ERR_OK) {
                pbuf_free(தரவு); கம்பியிலான_மதிப்பு.집계[4]++;
            } else { கம்பியிலான_மதிப்பு.집계[0]++; கம்பியிலான_மதிப்பு.집계[1] += நீளம்_மதிப்பு - 2; }
        }
        받는주소(நிலை_அடைவு); ஒத்திசை(); கம்பியிலான_மதிப்பு.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = கம்பியிலான_மதிப்பு.소비;
    }
}
uint32_t 유선망집계(unsigned உள்ளீடு_மதிப்பு) {
    return உள்ளீடு_மதிப்பு < 5 ? கம்பியிலான_மதிப்பு.집계[உள்ளீடு_மதிப்பு] : உள்ளீடு_மதிப்பு == 5 ? கம்பியிலான_மதிப்பு.속도 : உள்ளீடு_மதிப்பு == 6 ? கம்பியிலான_மதிப்பு.தயார்படுத்த : 0;
}
