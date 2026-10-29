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
#include "ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਨੈਟਵਰਕ.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int ਬੋਰਡ_ਮਸ਼ੀਨ_ਪਤਾ(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ਪਤਾ) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ਪਤਾ)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, ਨਕਲ_ਆਕਾਰ = 2048 };
static struct {
    unsigned char 받기[고리개수][ਨਕਲ_ਆਕਾਰ];
    unsigned char ਈਮੇਲ[고리개수][ਨਕਲ_ਆਕਾਰ];
    uint16_t 소비, 생산;
    int 물리주소, ਤਿਆਰ_ਕਰੋ, 속도;
    uint32_t 집계[5];
    uintptr_t ਤਸਦੀਕ_ਅਗਲਾ_ਆਇਟਮ;
} ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ __attribute__((aligned(64)));

static void ਸਿੰਕ_ਕਰੋ(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void ਸਾਫ਼_ਕੈਸ਼(void *ਸਮੱਗਰੀ, unsigned ਲੰਬਾਈ_ਕੀਮਤ, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ਸਮੱਗਰੀ + ਲੰਬਾਈ_ਕੀਮਤ;
    for (uintptr_t ਪਤਾ = (uintptr_t)ਸਮੱਗਰੀ & ~(uintptr_t)63; ਪਤਾ < 끝; ਪਤਾ += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ਪਤਾ) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ਪਤਾ) : "memory");
    }
#else
    (void)ਸਮੱਗਰੀ; (void)ਲੰਬਾਈ_ਕੀਮਤ; (void)받기;
#endif
    ਸਿੰਕ_ਕਰੋ();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ਪਤਾ, unsigned ਅਨੁਕ੍ਰਮਣਿਕਾ, int ਲਿਖਣ, unsigned ਕੀਮਤ) {
    uint32_t ਕਮਾਂਡ = (ਲਿਖਣ ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ਪਤਾ << GENET_MDIO_ADDR_SHIFT) | (ਅਨੁਕ੍ਰਮਣਿਕਾ << GENET_MDIO_REG_SHIFT) | (ਕੀਮਤ & 65535);
    유선저장기(GENET_MDIO_CMD) = ਕਮਾਂਡ;
    유선저장기(GENET_MDIO_CMD) = ਕਮਾਂਡ | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t ਸਥਿਤੀ_ਕੀਮਤ = 유선저장기(GENET_MDIO_CMD);
        if (!(ਸਥਿਤੀ_ਕੀਮਤ & GENET_MDIO_START_BUSY))
            return ਸਥਿਤੀ_ਕੀਮਤ & GENET_MDIO_READ_FAILED ? -1 : (int)(ਸਥਿਤੀ_ਕੀਮਤ & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ਅਨੁਕ੍ਰਮਣਿਕਾ) { return 물리전송(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.물리주소, ਅਨੁਕ੍ਰਮਣਿਕਾ, 0, 0); }
static int 물리쓰기(unsigned ਅਨੁਕ੍ਰਮਣਿਕਾ, unsigned ਕੀਮਤ) { return 물리전송(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.물리주소, ਅਨੁਕ੍ਰਮਣਿਕਾ, 1, ਕੀਮਤ); }
static int 물리준비(void) {
    ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.물리주소 = -1;
    for (unsigned ਪਤਾ = 0; ਪਤਾ < 32; ਪਤਾ++) {
        int 식별 = 물리전송(ਪਤਾ, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.물리주소 = ਪਤਾ; break; }
    }
    if (ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ਕੀਮਤ = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ਕੀਮਤ < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ਕੀਮਤ & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ਕੀਮਤ = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ਕੀਮਤ < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ਕੀਮਤ & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void ਤਿਆਰ_ਕਰੋ_ਲੂਪ(unsigned ਪਿਛੋਕੜ_ਕੀਮਤ) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ਲੂਪ_ਕੀਮਤ = ਪਿਛੋਕੜ_ਕੀਮਤ + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned ਸਥਿਤੀ = 0; ਸਥਿਤੀ <= 0x30; ਸਥਿਤੀ += 4) 유선저장기(ਲੂਪ_ਕੀਮਤ + ਸਥਿਤੀ) = 0;
    유선저장기(ਲੂਪ_ਕੀਮਤ + 0x10) = (고리개수 << 16) | ਨਕਲ_ਆਕਾਰ;
    유선저장기(ਲੂਪ_ਕੀਮਤ + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (ਪਿਛੋਕੜ_ਕੀਮਤ == GENET_RX_BASE) 유선저장기(ਲੂਪ_ਕੀਮਤ + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ਲੂਪ_ਕੀਮਤ + 0x24) = 1;
    유선저장기(ਪਿਛੋਕੜ_ਕੀਮਤ + 0x104c) = 8;
    유선저장기(ਪਿਛੋਕੜ_ਕੀਮਤ + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ) {
    uintptr_t ਪਤਾ = (uintptr_t)ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.받기[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ];
    ਸਾਫ਼_ਕੈਸ਼((void *)ਪਤਾ, ਨਕਲ_ਆਕਾਰ, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ)) = (uint32_t)ਪਤਾ;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ)) = (uint64_t)ਪਤਾ >> 32;
    유선저장기(GENET_RX_DESC_STATUS(ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ)) = ਨਕਲ_ਆਕਾਰ << 16;
}
static err_t 전문보내기(struct netif *ਤਜਵੀਜ_ਕੀਮਤ, struct pbuf *전문) {
    if (!ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਤਿਆਰ_ਕਰੋ || !netif_is_link_up(ਤਜਵੀਜ_ਕੀਮਤ)) return ERR_RTE;
    unsigned ਆਕਾਰ = 전문->tot_len;
    if (!ਆਕਾਰ || ਆਕਾਰ > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ = ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.생산 % 고리개수, 송신길이 = ਆਕਾਰ < 60 ? 60 : ਆਕਾਰ;
    unsigned char *ਸਮੱਗਰੀ = ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਈਮੇਲ[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ];
    memset(ਸਮੱਗਰੀ, 0, 송신길이);
    if (pbuf_copy_partial(전문, ਸਮੱਗਰੀ, ਆਕਾਰ, 0) != ਆਕਾਰ) return ERR_BUF;
    ਸਾਫ਼_ਕੈਸ਼(ਸਮੱਗਰੀ, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ)) = (uint32_t)(uintptr_t)ਸਮੱਗਰੀ;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ)) = (uint64_t)(uintptr_t)ਸਮੱਗਰੀ >> 32;
    유선저장기(GENET_TX_DESC_STATUS(ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    ਸਿੰਕ_ਕਰੋ();
    ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.생산;
    ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[2]++; ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[3] += ਆਕਾਰ;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t ਤਿਆਰ_ਕਰੋ_ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਨੈਟਵਰਕ(struct netif *ਤਜਵੀਜ_ਕੀਮਤ) {
    unsigned char ਪਤਾ[6];
    if (!유선장치있음() || !ਬੋਰਡ_ਮਸ਼ੀਨ_ਪਤਾ(ਪਤਾ) || (ਪਤਾ[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= ਪਤਾ[순번];
    if (!합) return ERR_IF;
    memset(&ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ, 0, sizeof(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ਪਤਾ[0] << 24 | (uint32_t)ਪਤਾ[1] << 16 | ਪਤਾ[2] << 8 | ਪਤਾ[3];
    유선저장기(GENET_UMAC_MAC1) = ਪਤਾ[4] << 8 | ਪਤਾ[5];
    ਤਿਆਰ_ਕਰੋ_ਲੂਪ(GENET_TX_BASE); ਤਿਆਰ_ਕਰੋ_ਲੂਪ(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    ਸਿੰਕ_ਕਰੋ();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ਤਜਵੀਜ_ਕੀਮਤ->name[0] = 'e'; ਤਜਵੀਜ_ਕੀਮਤ->name[1] = 'n'; ਤਜਵੀਜ_ਕੀਮਤ->mtu = 1500;
    ਤਜਵੀਜ_ਕੀਮਤ->hwaddr_len = 6; memcpy(ਤਜਵੀਜ_ਕੀਮਤ->hwaddr, ਪਤਾ, 6);
    ਤਜਵੀਜ_ਕੀਮਤ->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ਤਜਵੀਜ_ਕੀਮਤ->output = etharp_output; ਤਜਵੀਜ_ਕੀਮਤ->linkoutput = 전문보내기;
    ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਤਿਆਰ_ਕਰੋ = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ਤਜਵੀਜ_ਕੀਮਤ) {
    if (!ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਤਿਆਰ_ਕਰੋ) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਤਸਦੀਕ_ਅਗਲਾ_ਆਇਟਮ) {
        ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਤਸਦੀਕ_ਅਗਲਾ_ਆਇਟਮ = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int ਸਥਿਤੀ_ਕੀਮਤ = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ਮੈਥਡ_ਮੋਡ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ਮੈਥਡ_ਮੋਡ == 7 ? 1000 : ਮੈਥਡ_ਮੋਡ == 5 ? 100 : ਮੈਥਡ_ਮੋਡ == 2 ? 10 : 0;
        ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.속도 = ਸਥਿਤੀ_ਕੀਮਤ >= 0 && (ਸਥਿਤੀ_ਕੀਮਤ & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.속도) {
            uint32_t ਸੈਟਿੰਗ = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            ਸੈਟਿੰਗ &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = ਸੈਟਿੰਗ | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ਸੈਟਿੰਗ = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = ਸੈਟਿੰਗ | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ਤਜਵੀਜ_ਕੀਮਤ)) netif_set_link_up(ਤਜਵੀਜ_ਕੀਮਤ);
        } else if (netif_is_link_up(ਤਜਵੀਜ_ਕੀਮਤ)) netif_set_link_down(ਤਜਵੀਜ_ਕੀਮਤ);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.소비);
    if (남음 > 고리개수) { ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ = ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.소비 % 고리개수;
        ਸਿੰਕ_ਕਰੋ();
        uint32_t ਸਥਿਤੀ_ਕੀਮਤ = 유선저장기(GENET_RX_DESC_STATUS(ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ));
        unsigned ਲੰਬਾਈ_ਕੀਮਤ = (ਸਥਿਤੀ_ਕੀਮਤ & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((ਸਥਿਤੀ_ਕੀਮਤ & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || ਲੰਬਾਈ_ਕੀਮਤ < 16 || ਲੰਬਾਈ_ਕੀਮਤ > 1538) ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[4]++;
        else {
            ਸਾਫ਼_ਕੈਸ਼(ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.받기[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ], ਲੰਬਾਈ_ਕੀਮਤ, 1);
            struct pbuf *ਸਮੱਗਰੀ = pbuf_alloc(PBUF_RAW, ਲੰਬਾਈ_ਕੀਮਤ - 2, PBUF_POOL);
            if (!ਸਮੱਗਰੀ) ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[4]++;
            else if (pbuf_take(ਸਮੱਗਰੀ, ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.받기[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ] + 2, ਲੰਬਾਈ_ਕੀਮਤ - 2) != ERR_OK || ਤਜਵੀਜ_ਕੀਮਤ->input(ਸਮੱਗਰੀ, ਤਜਵੀਜ_ਕੀਮਤ) != ERR_OK) {
                pbuf_free(ਸਮੱਗਰੀ); ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[4]++;
            } else { ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[0]++; ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[1] += ਲੰਬਾਈ_ਕੀਮਤ - 2; }
        }
        받는주소(ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ); ਸਿੰਕ_ਕਰੋ(); ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.소비;
    }
}
uint32_t 유선망집계(unsigned ਦਾਖਲਾ_ਕੀਮਤ) {
    return ਦਾਖਲਾ_ਕੀਮਤ < 5 ? ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.집계[ਦਾਖਲਾ_ਕੀਮਤ] : ਦਾਖਲਾ_ਕੀਮਤ == 5 ? ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.속도 : ਦਾਖਲਾ_ਕੀਮਤ == 6 ? ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ.ਤਿਆਰ_ਕਰੋ : 0;
}
