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
#include "ତାରଯୁକ୍ତ_ନେଟ୍_ୱାର୍କ୍.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int ବୋର୍ଡ୍_ମେସିନ୍_ଠିକଣା(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ଠିକଣା) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ଠିକଣା)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, ବଫର୍_ଅକାର = 2048 };
static struct {
    unsigned char 받기[고리개수][ବଫର୍_ଅକାର];
    unsigned char ପଠାନ୍ତୁ[고리개수][ବଫର୍_ଅକାର];
    uint16_t 소비, 생산;
    int 물리주소, ପ୍ରସ୍ତୁତ, 속도;
    uint32_t 집계[5];
    uintptr_t ଯାଞ୍ଚ୍_କରିବା_ପରବର୍ତ୍ତୀ_ଆଇଟମ୍;
} ତାରଯୁକ୍ତ_ମୂଲ୍ୟ __attribute__((aligned(64)));

static void ସିଂକ୍ରୋନାଇଜ୍_କରନ୍ତୁ(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void କ୍ଲିନ୍_କ୍ୟାଚ୍(void *ଡାଟା, unsigned ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ଡାଟା + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ;
    for (uintptr_t ଠିକଣା = (uintptr_t)ଡାଟା & ~(uintptr_t)63; ଠିକଣା < 끝; ଠିକଣା += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ଠିକଣା) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ଠିକଣା) : "memory");
    }
#else
    (void)ଡାଟା; (void)ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ; (void)받기;
#endif
    ସିଂକ୍ରୋନାଇଜ୍_କରନ୍ତୁ();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ଠିକଣା, unsigned ଅନୁକ୍ରମଣିକା, int ଲେଖନ୍ତୁ, unsigned ମୂଲ୍ୟ) {
    uint32_t ନିର୍ଦ୍ଦେଶ = (ଲେଖନ୍ତୁ ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ଠିକଣା << GENET_MDIO_ADDR_SHIFT) | (ଅନୁକ୍ରମଣିକା << GENET_MDIO_REG_SHIFT) | (ମୂଲ୍ୟ & 65535);
    유선저장기(GENET_MDIO_CMD) = ନିର୍ଦ୍ଦେଶ;
    유선저장기(GENET_MDIO_CMD) = ନିର୍ଦ୍ଦେଶ | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = 유선저장기(GENET_MDIO_CMD);
        if (!(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 & GENET_MDIO_START_BUSY))
            return ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 & GENET_MDIO_READ_FAILED ? -1 : (int)(ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ଅନୁକ୍ରମଣିକା) { return 물리전송(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.물리주소, ଅନୁକ୍ରମଣିକା, 0, 0); }
static int 물리쓰기(unsigned ଅନୁକ୍ରମଣିକା, unsigned ମୂଲ୍ୟ) { return 물리전송(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.물리주소, ଅନୁକ୍ରମଣିକା, 1, ମୂଲ୍ୟ); }
static int 물리준비(void) {
    ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.물리주소 = -1;
    for (unsigned ଠିକଣା = 0; ଠିକଣା < 32; ଠିକଣା++) {
        int 식별 = 물리전송(ଠିକଣା, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.물리주소 = ଠିକଣା; break; }
    }
    if (ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ମୂଲ୍ୟ = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ମୂଲ୍ୟ < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ମୂଲ୍ୟ & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ମୂଲ୍ୟ = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ମୂଲ୍ୟ < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ମୂଲ୍ୟ & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void ପ୍ରସ୍ତୁତ_ଲୁପ୍(unsigned ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ଲୁପ୍_ମୂଲ୍ୟ = ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned ଅବସ୍ଥାନ = 0; ଅବସ୍ଥାନ <= 0x30; ଅବସ୍ଥାନ += 4) 유선저장기(ଲୁପ୍_ମୂଲ୍ୟ + ଅବସ୍ଥାନ) = 0;
    유선저장기(ଲୁପ୍_ମୂଲ୍ୟ + 0x10) = (고리개수 << 16) | ବଫର୍_ଅକାର;
    유선저장기(ଲୁପ୍_ମୂଲ୍ୟ + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ == GENET_RX_BASE) 유선저장기(ଲୁପ୍_ମୂଲ୍ୟ + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ଲୁପ୍_ମୂଲ୍ୟ + 0x24) = 1;
    유선저장기(ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ + 0x104c) = 8;
    유선저장기(ପୃଷ୍ଠପଟ_ମୂଲ୍ୟ + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା) {
    uintptr_t ଠିକଣା = (uintptr_t)ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.받기[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା];
    କ୍ଲିନ୍_କ୍ୟାଚ୍((void *)ଠିକଣା, ବଫର୍_ଅକାର, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା)) = (uint32_t)ଠିକଣା;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା)) = (uint64_t)ଠିକଣା >> 32;
    유선저장기(GENET_RX_DESC_STATUS(ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା)) = ବଫର୍_ଅକାର << 16;
}
static err_t 전문보내기(struct netif *ଡିଭାଇସ_ମୂଲ୍ୟ, struct pbuf *전문) {
    if (!ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ପ୍ରସ୍ତୁତ || !netif_is_link_up(ଡିଭାଇସ_ମୂଲ୍ୟ)) return ERR_RTE;
    unsigned ଆକାର = 전문->tot_len;
    if (!ଆକାର || ଆକାର > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା = ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.생산 % 고리개수, 송신길이 = ଆକାର < 60 ? 60 : ଆକାର;
    unsigned char *ଡାଟା = ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ପଠାନ୍ତୁ[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା];
    memset(ଡାଟା, 0, 송신길이);
    if (pbuf_copy_partial(전문, ଡାଟା, ଆକାର, 0) != ଆକାର) return ERR_BUF;
    କ୍ଲିନ୍_କ୍ୟାଚ୍(ଡାଟା, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା)) = (uint32_t)(uintptr_t)ଡାଟା;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା)) = (uint64_t)(uintptr_t)ଡାଟା >> 32;
    유선저장기(GENET_TX_DESC_STATUS(ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    ସିଂକ୍ରୋନାଇଜ୍_କରନ୍ତୁ();
    ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.생산;
    ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[2]++; ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[3] += ଆକାର;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t ପ୍ରସ୍ତୁତ_ତାରଯୁକ୍ତ_ନେଟ୍_ୱାର୍କ୍(struct netif *ଡିଭାଇସ_ମୂଲ୍ୟ) {
    unsigned char ଠିକଣା[6];
    if (!유선장치있음() || !ବୋର୍ଡ୍_ମେସିନ୍_ଠିକଣା(ଠିକଣା) || (ଠିକଣା[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= ଠିକଣା[순번];
    if (!합) return ERR_IF;
    memset(&ତାରଯୁକ୍ତ_ମୂଲ୍ୟ, 0, sizeof(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ଠିକଣା[0] << 24 | (uint32_t)ଠିକଣା[1] << 16 | ଠିକଣା[2] << 8 | ଠିକଣା[3];
    유선저장기(GENET_UMAC_MAC1) = ଠିକଣା[4] << 8 | ଠିକଣା[5];
    ପ୍ରସ୍ତୁତ_ଲୁପ୍(GENET_TX_BASE); ପ୍ରସ୍ତୁତ_ଲୁପ୍(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    ସିଂକ୍ରୋନାଇଜ୍_କରନ୍ତୁ();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ଡିଭାଇସ_ମୂଲ୍ୟ->name[0] = 'e'; ଡିଭାଇସ_ମୂଲ୍ୟ->name[1] = 'n'; ଡିଭାଇସ_ମୂଲ୍ୟ->mtu = 1500;
    ଡିଭାଇସ_ମୂଲ୍ୟ->hwaddr_len = 6; memcpy(ଡିଭାଇସ_ମୂଲ୍ୟ->hwaddr, ଠିକଣା, 6);
    ଡିଭାଇସ_ମୂଲ୍ୟ->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ଡିଭାଇସ_ମୂଲ୍ୟ->output = etharp_output; ଡିଭାଇସ_ମୂଲ୍ୟ->linkoutput = 전문보내기;
    ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ପ୍ରସ୍ତୁତ = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ଡିଭାଇସ_ମୂଲ୍ୟ) {
    if (!ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ପ୍ରସ୍ତୁତ) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ଯାଞ୍ଚ୍_କରିବା_ପରବର୍ତ୍ତୀ_ଆଇଟମ୍) {
        ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ଯାଞ୍ଚ୍_କରିବା_ପରବର୍ତ୍ତୀ_ଆଇଟମ୍ = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ପଦ୍ଧତି_ମୋଡ୍ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ପଦ୍ଧତି_ମୋଡ୍ == 7 ? 1000 : ପଦ୍ଧତି_ମୋଡ୍ == 5 ? 100 : ପଦ୍ଧତି_ମୋଡ୍ == 2 ? 10 : 0;
        ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.속도 = ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 >= 0 && (ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.속도) {
            uint32_t ବିନ୍ଯାସ = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            ବିନ୍ଯାସ &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = ବିନ୍ଯାସ | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ବିନ୍ଯାସ = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = ବିନ୍ଯାସ | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ଡିଭାଇସ_ମୂଲ୍ୟ)) netif_set_link_up(ଡିଭାଇସ_ମୂଲ୍ୟ);
        } else if (netif_is_link_up(ଡିଭାଇସ_ମୂଲ୍ୟ)) netif_set_link_down(ଡିଭାଇସ_ମୂଲ୍ୟ);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.소비);
    if (남음 > 고리개수) { ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା = ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.소비 % 고리개수;
        ସିଂକ୍ରୋନାଇଜ୍_କରନ୍ତୁ();
        uint32_t ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 = 유선저장기(GENET_RX_DESC_STATUS(ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା));
        unsigned ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ = (ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((ସ୍ଥିତି_ମୂଲ୍ୟ_e10195a1 & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ < 16 || ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ > 1538) ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[4]++;
        else {
            କ୍ଲିନ୍_କ୍ୟାଚ୍(ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.받기[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା], ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ, 1);
            struct pbuf *ଡାଟା = pbuf_alloc(PBUF_RAW, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ - 2, PBUF_POOL);
            if (!ଡାଟା) ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[4]++;
            else if (pbuf_take(ଡାଟା, ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.받기[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା] + 2, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ - 2) != ERR_OK || ଡିଭାଇସ_ମୂଲ୍ୟ->input(ଡାଟା, ଡିଭାଇସ_ମୂଲ୍ୟ) != ERR_OK) {
                pbuf_free(ଡାଟା); ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[4]++;
            } else { ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[0]++; ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[1] += ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ - 2; }
        }
        받는주소(ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା); ସିଂକ୍ରୋନାଇଜ୍_କରନ୍ତୁ(); ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.소비;
    }
}
uint32_t 유선망집계(unsigned ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ) {
    return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ < 5 ? ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.집계[ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ] : ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == 5 ? ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.속도 : ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ == 6 ? ତାରଯୁକ୍ତ_ମୂଲ୍ୟ.ପ୍ରସ୍ତୁତ : 0;
}
