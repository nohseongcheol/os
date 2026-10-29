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
#include "ባለሽቦ_መረብ.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int ቦርድ_ማሽን_አድራሻ(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(አድራሻ) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (አድራሻ)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, ቋት_መጠን_ቀይር = 2048 };
static struct {
    unsigned char 받기[고리개수][ቋት_መጠን_ቀይር];
    unsigned char ላክ[고리개수][ቋት_መጠን_ቀይር];
    uint16_t 소비, 생산;
    int 물리주소, አዘጋጅ_9ce364fc, 속도;
    uint32_t 집계[5];
    uintptr_t አረጋግጥ_ቀጣይ_ንጥል_ነገር;
} ባለሽቦ_እሴት __attribute__((aligned(64)));

static void አመሳስል(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void ንጹህ_ሸጉጥ(void *ውሂብ, unsigned ርዝመት_እሴት, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ውሂብ + ርዝመት_እሴት;
    for (uintptr_t አድራሻ = (uintptr_t)ውሂብ & ~(uintptr_t)63; አድራሻ < 끝; አድራሻ += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(አድራሻ) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(አድራሻ) : "memory");
    }
#else
    (void)ውሂብ; (void)ርዝመት_እሴት; (void)받기;
#endif
    አመሳስል();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned አድራሻ, unsigned መረጃ_ጠቆመ, int መጻፊያ, unsigned እሴት) {
    uint32_t ትእዛዝ = (መጻፊያ ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (አድራሻ << GENET_MDIO_ADDR_SHIFT) | (መረጃ_ጠቆመ << GENET_MDIO_REG_SHIFT) | (እሴት & 65535);
    유선저장기(GENET_MDIO_CMD) = ትእዛዝ;
    유선저장기(GENET_MDIO_CMD) = ትእዛዝ | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t ዞን_እሴት = 유선저장기(GENET_MDIO_CMD);
        if (!(ዞን_እሴት & GENET_MDIO_START_BUSY))
            return ዞን_እሴት & GENET_MDIO_READ_FAILED ? -1 : (int)(ዞን_እሴት & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned መረጃ_ጠቆመ) { return 물리전송(ባለሽቦ_እሴት.물리주소, መረጃ_ጠቆመ, 0, 0); }
static int 물리쓰기(unsigned መረጃ_ጠቆመ, unsigned እሴት) { return 물리전송(ባለሽቦ_እሴት.물리주소, መረጃ_ጠቆመ, 1, እሴት); }
static int 물리준비(void) {
    ባለሽቦ_እሴት.물리주소 = -1;
    for (unsigned አድራሻ = 0; አድራሻ < 32; አድራሻ++) {
        int 식별 = 물리전송(አድራሻ, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ባለሽቦ_እሴት.물리주소 = አድራሻ; break; }
    }
    if (ባለሽቦ_እሴት.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int እሴት = 물리읽기(BRGPHY_MII_AUXCTL);
    if (እሴት < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (እሴት & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    እሴት = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (እሴት < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (እሴት & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void አዘጋጅ_ድግግሞሽ(unsigned ልጣፍ_እሴት) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ድግግሞሽ_እሴት = ልጣፍ_እሴት + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned አካባቢ = 0; አካባቢ <= 0x30; አካባቢ += 4) 유선저장기(ድግግሞሽ_እሴት + አካባቢ) = 0;
    유선저장기(ድግግሞሽ_እሴት + 0x10) = (고리개수 << 16) | ቋት_መጠን_ቀይር;
    유선저장기(ድግግሞሽ_እሴት + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (ልጣፍ_እሴት == GENET_RX_BASE) 유선저장기(ድግግሞሽ_እሴት + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ድግግሞሽ_እሴት + 0x24) = 1;
    유선저장기(ልጣፍ_እሴት + 0x104c) = 8;
    유선저장기(ልጣፍ_እሴት + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned በቦታ_አስቀመጠ_መረጃ_ጠቆመ) {
    uintptr_t አድራሻ = (uintptr_t)ባለሽቦ_እሴት.받기[በቦታ_አስቀመጠ_መረጃ_ጠቆመ];
    ንጹህ_ሸጉጥ((void *)አድራሻ, ቋት_መጠን_ቀይር, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(በቦታ_አስቀመጠ_መረጃ_ጠቆመ)) = (uint32_t)አድራሻ;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(በቦታ_አስቀመጠ_መረጃ_ጠቆመ)) = (uint64_t)አድራሻ >> 32;
    유선저장기(GENET_RX_DESC_STATUS(በቦታ_አስቀመጠ_መረጃ_ጠቆመ)) = ቋት_መጠን_ቀይር << 16;
}
static err_t 전문보내기(struct netif *መሳሪያ_እሴት, struct pbuf *전문) {
    if (!ባለሽቦ_እሴት.አዘጋጅ_9ce364fc || !netif_is_link_up(መሳሪያ_እሴት)) return ERR_RTE;
    unsigned መጠን = 전문->tot_len;
    if (!መጠን || መጠን > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ባለሽቦ_እሴት.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned በቦታ_አስቀመጠ_መረጃ_ጠቆመ = ባለሽቦ_እሴት.생산 % 고리개수, 송신길이 = መጠን < 60 ? 60 : መጠን;
    unsigned char *ውሂብ = ባለሽቦ_እሴት.ላክ[በቦታ_አስቀመጠ_መረጃ_ጠቆመ];
    memset(ውሂብ, 0, 송신길이);
    if (pbuf_copy_partial(전문, ውሂብ, መጠን, 0) != መጠን) return ERR_BUF;
    ንጹህ_ሸጉጥ(ውሂብ, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(በቦታ_አስቀመጠ_መረጃ_ጠቆመ)) = (uint32_t)(uintptr_t)ውሂብ;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(በቦታ_አስቀመጠ_መረጃ_ጠቆመ)) = (uint64_t)(uintptr_t)ውሂብ >> 32;
    유선저장기(GENET_TX_DESC_STATUS(በቦታ_አስቀመጠ_መረጃ_ጠቆመ)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    አመሳስል();
    ባለሽቦ_እሴት.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ባለሽቦ_እሴት.생산;
    ባለሽቦ_እሴት.집계[2]++; ባለሽቦ_እሴት.집계[3] += መጠን;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t አዘጋጅ_ባለሽቦ_መረብ(struct netif *መሳሪያ_እሴት) {
    unsigned char አድራሻ[6];
    if (!유선장치있음() || !ቦርድ_ማሽን_አድራሻ(አድራሻ) || (አድራሻ[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= አድራሻ[순번];
    if (!합) return ERR_IF;
    memset(&ባለሽቦ_እሴት, 0, sizeof(ባለሽቦ_እሴት));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)አድራሻ[0] << 24 | (uint32_t)አድራሻ[1] << 16 | አድራሻ[2] << 8 | አድራሻ[3];
    유선저장기(GENET_UMAC_MAC1) = አድራሻ[4] << 8 | አድራሻ[5];
    አዘጋጅ_ድግግሞሽ(GENET_TX_BASE); አዘጋጅ_ድግግሞሽ(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    አመሳስል();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    መሳሪያ_እሴት->name[0] = 'e'; መሳሪያ_እሴት->name[1] = 'n'; መሳሪያ_እሴት->mtu = 1500;
    መሳሪያ_እሴት->hwaddr_len = 6; memcpy(መሳሪያ_እሴት->hwaddr, አድራሻ, 6);
    መሳሪያ_እሴት->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    መሳሪያ_እሴት->output = etharp_output; መሳሪያ_እሴት->linkoutput = 전문보내기;
    ባለሽቦ_እሴት.አዘጋጅ_9ce364fc = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *መሳሪያ_እሴት) {
    if (!ባለሽቦ_እሴት.አዘጋጅ_9ce364fc) return;
    uintptr_t አሁን_እሴት = 보드밀리초();
    if (አሁን_እሴት >= ባለሽቦ_እሴት.አረጋግጥ_ቀጣይ_ንጥል_ነገር) {
        ባለሽቦ_እሴት.አረጋግጥ_ቀጣይ_ንጥል_ነገር = አሁን_እሴት + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int ዞን_እሴት = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ስልት_ሁነታ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ስልት_ሁነታ == 7 ? 1000 : ስልት_ሁነታ == 5 ? 100 : ስልት_ሁነታ == 2 ? 10 : 0;
        ባለሽቦ_እሴት.속도 = ዞን_እሴት >= 0 && (ዞን_እሴት & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ባለሽቦ_እሴት.속도) {
            uint32_t ማሰናጃዎች = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            ማሰናጃዎች &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = ማሰናጃዎች | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ማሰናጃዎች = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = ማሰናጃዎች | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(መሳሪያ_እሴት)) netif_set_link_up(መሳሪያ_እሴት);
        } else if (netif_is_link_up(መሳሪያ_እሴት)) netif_set_link_down(መሳሪያ_እሴት);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ባለሽቦ_እሴት.소비);
    if (남음 > 고리개수) { ባለሽቦ_እሴት.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned በቦታ_አስቀመጠ_መረጃ_ጠቆመ = ባለሽቦ_እሴት.소비 % 고리개수;
        አመሳስል();
        uint32_t ዞን_እሴት = 유선저장기(GENET_RX_DESC_STATUS(በቦታ_አስቀመጠ_መረጃ_ጠቆመ));
        unsigned ርዝመት_እሴት = (ዞን_እሴት & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((ዞን_እሴት & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || ርዝመት_እሴት < 16 || ርዝመት_እሴት > 1538) ባለሽቦ_እሴት.집계[4]++;
        else {
            ንጹህ_ሸጉጥ(ባለሽቦ_እሴት.받기[በቦታ_አስቀመጠ_መረጃ_ጠቆመ], ርዝመት_እሴት, 1);
            struct pbuf *ውሂብ = pbuf_alloc(PBUF_RAW, ርዝመት_እሴት - 2, PBUF_POOL);
            if (!ውሂብ) ባለሽቦ_እሴት.집계[4]++;
            else if (pbuf_take(ውሂብ, ባለሽቦ_እሴት.받기[በቦታ_አስቀመጠ_መረጃ_ጠቆመ] + 2, ርዝመት_እሴት - 2) != ERR_OK || መሳሪያ_እሴት->input(ውሂብ, መሳሪያ_እሴት) != ERR_OK) {
                pbuf_free(ውሂብ); ባለሽቦ_እሴት.집계[4]++;
            } else { ባለሽቦ_እሴት.집계[0]++; ባለሽቦ_እሴት.집계[1] += ርዝመት_እሴት - 2; }
        }
        받는주소(በቦታ_አስቀመጠ_መረጃ_ጠቆመ); አመሳስል(); ባለሽቦ_እሴት.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ባለሽቦ_እሴት.소비;
    }
}
uint32_t 유선망집계(unsigned ምዝግብ_እሴት) {
    return ምዝግብ_እሴት < 5 ? ባለሽቦ_እሴት.집계[ምዝግብ_እሴት] : ምዝግብ_እሴት == 5 ? ባለሽቦ_እሴት.속도 : ምዝግብ_እሴት == 6 ? ባለሽቦ_እሴት.አዘጋጅ_9ce364fc : 0;
}
