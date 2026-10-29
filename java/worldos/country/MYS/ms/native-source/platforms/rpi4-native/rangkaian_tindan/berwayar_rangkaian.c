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
#include "berwayar_rangkaian.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Papan_mesin_e_mel(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(e_mel) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (e_mel)))
#endif
enum { 고리번호 = 16, Loop_COUNT = 256, saiz_penimbal = 2048 };
static struct {
    unsigned char 받기[Loop_COUNT][saiz_penimbal];
    unsigned char e_mel_9aee63bd[Loop_COUNT][saiz_penimbal];
    uint16_t 소비, 생산;
    int 물리주소, Sediakan, 속도;
    uint32_t 집계[5];
    uintptr_t tentu_sahkan_Seterusnya_item;
} berwayar_VALUE __attribute__((aligned(64)));

static void segerak(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_cache(void *data, unsigned kepanjangan_VALUE, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + kepanjangan_VALUE;
    for (uintptr_t e_mel = (uintptr_t)data & ~(uintptr_t)63; e_mel < 끝; e_mel += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(e_mel) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(e_mel) : "memory");
    }
#else
    (void)data; (void)kepanjangan_VALUE; (void)받기;
#endif
    segerak();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned e_mel, unsigned INDEX, int Tulis, unsigned VALUE) {
    uint32_t Perintah = (Tulis ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (e_mel << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALUE & 65535);
    유선저장기(GENET_MDIO_CMD) = Perintah;
    유선저장기(GENET_MDIO_CMD) = Perintah | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t status_VALUE = 유선저장기(GENET_MDIO_CMD);
        if (!(status_VALUE & GENET_MDIO_START_BUSY))
            return status_VALUE & GENET_MDIO_READ_FAILED ? -1 : (int)(status_VALUE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(berwayar_VALUE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALUE) { return 물리전송(berwayar_VALUE.물리주소, INDEX, 1, VALUE); }
static int 물리준비(void) {
    berwayar_VALUE.물리주소 = -1;
    for (unsigned e_mel = 0; e_mel < 32; e_mel++) {
        int 식별 = 물리전송(e_mel, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { berwayar_VALUE.물리주소 = e_mel; break; }
    }
    if (berwayar_VALUE.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VALUE = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VALUE < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VALUE & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VALUE = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VALUE < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VALUE & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Sediakan_Loop(unsigned latar_VALUE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALUE = latar_VALUE + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Kedudukan = 0; Kedudukan <= 0x30; Kedudukan += 4) 유선저장기(Loop_VALUE + Kedudukan) = 0;
    유선저장기(Loop_VALUE + 0x10) = (Loop_COUNT << 16) | saiz_penimbal;
    유선저장기(Loop_VALUE + 0x1c) = Loop_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (latar_VALUE == GENET_RX_BASE) 유선저장기(Loop_VALUE + 0x28) = (5 << 16) | (Loop_COUNT >> 4);
    else 유선저장기(Loop_VALUE + 0x24) = 1;
    유선저장기(latar_VALUE + 0x104c) = 8;
    유선저장기(latar_VALUE + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned jawatan_INDEX) {
    uintptr_t e_mel = (uintptr_t)berwayar_VALUE.받기[jawatan_INDEX];
    CLEAN_cache((void *)e_mel, saiz_penimbal, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(jawatan_INDEX)) = (uint32_t)e_mel;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(jawatan_INDEX)) = (uint64_t)e_mel >> 32;
    유선저장기(GENET_RX_DESC_STATUS(jawatan_INDEX)) = saiz_penimbal << 16;
}
static err_t 전문보내기(struct netif *peranti_VALUE, struct pbuf *전문) {
    if (!berwayar_VALUE.Sediakan || !netif_is_link_up(peranti_VALUE)) return ERR_RTE;
    unsigned Saiz = 전문->tot_len;
    if (!Saiz || Saiz > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(berwayar_VALUE.생산 - 소비) >= Loop_COUNT - 1) return ERR_MEM;
    unsigned jawatan_INDEX = berwayar_VALUE.생산 % Loop_COUNT, 송신길이 = Saiz < 60 ? 60 : Saiz;
    unsigned char *data = berwayar_VALUE.e_mel_9aee63bd[jawatan_INDEX];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(전문, data, Saiz, 0) != Saiz) return ERR_BUF;
    CLEAN_cache(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(jawatan_INDEX)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(jawatan_INDEX)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(jawatan_INDEX)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    segerak();
    berwayar_VALUE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = berwayar_VALUE.생산;
    berwayar_VALUE.집계[2]++; berwayar_VALUE.집계[3] += Saiz;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Sediakan_berwayar_rangkaian(struct netif *peranti_VALUE) {
    unsigned char e_mel[6];
    if (!유선장치있음() || !Papan_mesin_e_mel(e_mel) || (e_mel[0] & 1)) return ERR_IF;
    unsigned SUM_VALUE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALUE |= e_mel[순번];
    if (!SUM_VALUE) return ERR_IF;
    memset(&berwayar_VALUE, 0, sizeof(berwayar_VALUE));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)e_mel[0] << 24 | (uint32_t)e_mel[1] << 16 | e_mel[2] << 8 | e_mel[3];
    유선저장기(GENET_UMAC_MAC1) = e_mel[4] << 8 | e_mel[5];
    Sediakan_Loop(GENET_TX_BASE); Sediakan_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COUNT; 순번++) 받는주소(순번);
    segerak();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    peranti_VALUE->name[0] = 'e'; peranti_VALUE->name[1] = 'n'; peranti_VALUE->mtu = 1500;
    peranti_VALUE->hwaddr_len = 6; memcpy(peranti_VALUE->hwaddr, e_mel, 6);
    peranti_VALUE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    peranti_VALUE->output = etharp_output; peranti_VALUE->linkoutput = 전문보내기;
    berwayar_VALUE.Sediakan = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *peranti_VALUE) {
    if (!berwayar_VALUE.Sediakan) return;
    uintptr_t NOW_VALUE = 보드밀리초();
    if (NOW_VALUE >= berwayar_VALUE.tentu_sahkan_Seterusnya_item) {
        berwayar_VALUE.tentu_sahkan_Seterusnya_item = NOW_VALUE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int status_VALUE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned kaedah_mod = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = kaedah_mod == 7 ? 1000 : kaedah_mod == 5 ? 100 : kaedah_mod == 2 ? 10 : 0;
        berwayar_VALUE.속도 = status_VALUE >= 0 && (status_VALUE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (berwayar_VALUE.속도) {
            uint32_t Tetapan = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Tetapan &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Tetapan | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Tetapan = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Tetapan | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(peranti_VALUE)) netif_set_link_up(peranti_VALUE);
        } else if (netif_is_link_up(peranti_VALUE)) netif_set_link_down(peranti_VALUE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - berwayar_VALUE.소비);
    if (남음 > Loop_COUNT) { berwayar_VALUE.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned jawatan_INDEX = berwayar_VALUE.소비 % Loop_COUNT;
        segerak();
        uint32_t status_VALUE = 유선저장기(GENET_RX_DESC_STATUS(jawatan_INDEX));
        unsigned kepanjangan_VALUE = (status_VALUE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((status_VALUE & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || kepanjangan_VALUE < 16 || kepanjangan_VALUE > 1538) berwayar_VALUE.집계[4]++;
        else {
            CLEAN_cache(berwayar_VALUE.받기[jawatan_INDEX], kepanjangan_VALUE, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, kepanjangan_VALUE - 2, PBUF_POOL);
            if (!data) berwayar_VALUE.집계[4]++;
            else if (pbuf_take(data, berwayar_VALUE.받기[jawatan_INDEX] + 2, kepanjangan_VALUE - 2) != ERR_OK || peranti_VALUE->input(data, peranti_VALUE) != ERR_OK) {
                pbuf_free(data); berwayar_VALUE.집계[4]++;
            } else { berwayar_VALUE.집계[0]++; berwayar_VALUE.집계[1] += kepanjangan_VALUE - 2; }
        }
        받는주소(jawatan_INDEX); segerak(); berwayar_VALUE.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = berwayar_VALUE.소비;
    }
}
uint32_t 유선망집계(unsigned pemasukan_VALUE) {
    return pemasukan_VALUE < 5 ? berwayar_VALUE.집계[pemasukan_VALUE] : pemasukan_VALUE == 5 ? berwayar_VALUE.속도 : pemasukan_VALUE == 6 ? berwayar_VALUE.Sediakan : 0;
}
