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
#include "terkabel_jaringan.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Papan_mesin_surel(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(surel) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (surel)))
#endif
enum { 고리번호 = 16, Loop_COUNT = 256, ukuran_buffer = 2048 };
static struct {
    unsigned char terima[Loop_COUNT][ukuran_buffer];
    unsigned char kirim[Loop_COUNT][ukuran_buffer];
    uint16_t konsumsi_VALUE, 생산;
    int 물리주소, Siapkan, 속도;
    uint32_t 집계[5];
    uintptr_t periksa_Berikutnya_item;
} terkabel_VALUE __attribute__((aligned(64)));

static void sinkro(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_cache(void *data, unsigned panjang_VALUE, int terima) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + panjang_VALUE;
    for (uintptr_t surel = (uintptr_t)data & ~(uintptr_t)63; surel < 끝; surel += 64) {
        if (terima) __asm__ volatile("dc ivac, %0" :: "r"(surel) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(surel) : "memory");
    }
#else
    (void)data; (void)panjang_VALUE; (void)terima;
#endif
    sinkro();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned surel, unsigned INDEX, int Tulis, unsigned VALUE) {
    uint32_t perintah = (Tulis ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (surel << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALUE & 65535);
    유선저장기(GENET_MDIO_CMD) = perintah;
    유선저장기(GENET_MDIO_CMD) = perintah | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Status_VALUE = 유선저장기(GENET_MDIO_CMD);
        if (!(Status_VALUE & GENET_MDIO_START_BUSY))
            return Status_VALUE & GENET_MDIO_READ_FAILED ? -1 : (int)(Status_VALUE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(terkabel_VALUE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALUE) { return 물리전송(terkabel_VALUE.물리주소, INDEX, 1, VALUE); }
static int 물리준비(void) {
    terkabel_VALUE.물리주소 = -1;
    for (unsigned surel = 0; surel < 32; surel++) {
        int 식별 = 물리전송(surel, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { terkabel_VALUE.물리주소 = surel; break; }
    }
    if (terkabel_VALUE.물리주소 < 0) return -1;
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
static void Siapkan_Loop(unsigned wallpaper_VALUE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALUE = wallpaper_VALUE + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned posisi = 0; posisi <= 0x30; posisi += 4) 유선저장기(Loop_VALUE + posisi) = 0;
    유선저장기(Loop_VALUE + 0x10) = (Loop_COUNT << 16) | ukuran_buffer;
    유선저장기(Loop_VALUE + 0x1c) = Loop_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (wallpaper_VALUE == GENET_RX_BASE) 유선저장기(Loop_VALUE + 0x28) = (5 << 16) | (Loop_COUNT >> 4);
    else 유선저장기(Loop_VALUE + 0x24) = 1;
    유선저장기(wallpaper_VALUE + 0x104c) = 8;
    유선저장기(wallpaper_VALUE + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned posisi_INDEX) {
    uintptr_t surel = (uintptr_t)terkabel_VALUE.terima[posisi_INDEX];
    CLEAN_cache((void *)surel, ukuran_buffer, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(posisi_INDEX)) = (uint32_t)surel;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(posisi_INDEX)) = (uint64_t)surel >> 32;
    유선저장기(GENET_RX_DESC_STATUS(posisi_INDEX)) = ukuran_buffer << 16;
}
static err_t 전문보내기(struct netif *Ponsel_VALUE, struct pbuf *전문) {
    if (!terkabel_VALUE.Siapkan || !netif_is_link_up(Ponsel_VALUE)) return ERR_RTE;
    unsigned Ukuran = 전문->tot_len;
    if (!Ukuran || Ukuran > 1536) return ERR_BUF;
    uint16_t konsumsi_VALUE = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(terkabel_VALUE.생산 - konsumsi_VALUE) >= Loop_COUNT - 1) return ERR_MEM;
    unsigned posisi_INDEX = terkabel_VALUE.생산 % Loop_COUNT, 송신길이 = Ukuran < 60 ? 60 : Ukuran;
    unsigned char *data = terkabel_VALUE.kirim[posisi_INDEX];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(전문, data, Ukuran, 0) != Ukuran) return ERR_BUF;
    CLEAN_cache(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(posisi_INDEX)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(posisi_INDEX)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(posisi_INDEX)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sinkro();
    terkabel_VALUE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = terkabel_VALUE.생산;
    terkabel_VALUE.집계[2]++; terkabel_VALUE.집계[3] += Ukuran;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Siapkan_terkabel_jaringan(struct netif *Ponsel_VALUE) {
    unsigned char surel[6];
    if (!유선장치있음() || !Papan_mesin_surel(surel) || (surel[0] & 1)) return ERR_IF;
    unsigned SUM_VALUE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALUE |= surel[순번];
    if (!SUM_VALUE) return ERR_IF;
    memset(&terkabel_VALUE, 0, sizeof(terkabel_VALUE));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t keadaan_awal = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = keadaan_awal | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = keadaan_awal & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)surel[0] << 24 | (uint32_t)surel[1] << 16 | surel[2] << 8 | surel[3];
    유선저장기(GENET_UMAC_MAC1) = surel[4] << 8 | surel[5];
    Siapkan_Loop(GENET_TX_BASE); Siapkan_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COUNT; 순번++) 받는주소(순번);
    sinkro();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    Ponsel_VALUE->name[0] = 'e'; Ponsel_VALUE->name[1] = 'n'; Ponsel_VALUE->mtu = 1500;
    Ponsel_VALUE->hwaddr_len = 6; memcpy(Ponsel_VALUE->hwaddr, surel, 6);
    Ponsel_VALUE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    Ponsel_VALUE->output = etharp_output; Ponsel_VALUE->linkoutput = 전문보내기;
    terkabel_VALUE.Siapkan = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *Ponsel_VALUE) {
    if (!terkabel_VALUE.Siapkan) return;
    uintptr_t NOW_VALUE = 보드밀리초();
    if (NOW_VALUE >= terkabel_VALUE.periksa_Berikutnya_item) {
        terkabel_VALUE.periksa_Berikutnya_item = NOW_VALUE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Status_VALUE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metode_MODE = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metode_MODE == 7 ? 1000 : metode_MODE == 5 ? 100 : metode_MODE == 2 ? 10 : 0;
        terkabel_VALUE.속도 = Status_VALUE >= 0 && (Status_VALUE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (terkabel_VALUE.속도) {
            uint32_t Konfigurasi = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Konfigurasi &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Konfigurasi | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Konfigurasi = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Konfigurasi | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(Ponsel_VALUE)) netif_set_link_up(Ponsel_VALUE);
        } else if (netif_is_link_up(Ponsel_VALUE)) netif_set_link_down(Ponsel_VALUE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - terkabel_VALUE.konsumsi_VALUE);
    if (남음 > Loop_COUNT) { terkabel_VALUE.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned posisi_INDEX = terkabel_VALUE.konsumsi_VALUE % Loop_COUNT;
        sinkro();
        uint32_t Status_VALUE = 유선저장기(GENET_RX_DESC_STATUS(posisi_INDEX));
        unsigned panjang_VALUE = (Status_VALUE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Status_VALUE & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || panjang_VALUE < 16 || panjang_VALUE > 1538) terkabel_VALUE.집계[4]++;
        else {
            CLEAN_cache(terkabel_VALUE.terima[posisi_INDEX], panjang_VALUE, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, panjang_VALUE - 2, PBUF_POOL);
            if (!data) terkabel_VALUE.집계[4]++;
            else if (pbuf_take(data, terkabel_VALUE.terima[posisi_INDEX] + 2, panjang_VALUE - 2) != ERR_OK || Ponsel_VALUE->input(data, Ponsel_VALUE) != ERR_OK) {
                pbuf_free(data); terkabel_VALUE.집계[4]++;
            } else { terkabel_VALUE.집계[0]++; terkabel_VALUE.집계[1] += panjang_VALUE - 2; }
        }
        받는주소(posisi_INDEX); sinkro(); terkabel_VALUE.konsumsi_VALUE++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = terkabel_VALUE.konsumsi_VALUE;
    }
}
uint32_t 유선망집계(unsigned entri_VALUE) {
    return entri_VALUE < 5 ? terkabel_VALUE.집계[entri_VALUE] : entri_VALUE == 5 ? terkabel_VALUE.속도 : entri_VALUE == 6 ? terkabel_VALUE.Siapkan : 0;
}
