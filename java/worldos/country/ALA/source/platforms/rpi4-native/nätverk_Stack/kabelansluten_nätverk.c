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
#include "kabelansluten_nätverk.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Tavla_absolut_adress(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(Adress) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (Adress)))
#endif
enum { Loop_nummer = 16, Loop_ANTAL = 256, buffertstorlek = 2048 };
static struct {
    unsigned char få[Loop_ANTAL][buffertstorlek];
    unsigned char skicka[Loop_ANTAL][buffertstorlek];
    uint16_t använda_värde_84aa75c8, 생산;
    int 물리주소, Förbereda, 속도;
    uint32_t Statistik_värde[5];
    uintptr_t verifiera_Nästa_objekt;
} kabelansluten_värde __attribute__((aligned(64)));

static void synka(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Rent_cache(void *data, unsigned längd_värde, int få) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + längd_värde;
    for (uintptr_t Adress = (uintptr_t)data & ~(uintptr_t)63; Adress < 끝; Adress += 64) {
        if (få) __asm__ volatile("dc ivac, %0" :: "r"(Adress) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(Adress) : "memory");
    }
#else
    (void)data; (void)längd_värde; (void)få;
#endif
    synka();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned Adress, unsigned INDEX, int Skriv, unsigned värde) {
    uint32_t kommando = (Skriv ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (Adress << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (värde & 65535);
    유선저장기(GENET_MDIO_CMD) = kommando;
    유선저장기(GENET_MDIO_CMD) = kommando | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t status_värde = 유선저장기(GENET_MDIO_CMD);
        if (!(status_värde & GENET_MDIO_START_BUSY))
            return status_värde & GENET_MDIO_READ_FAILED ? -1 : (int)(status_värde & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(kabelansluten_värde.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned värde) { return 물리전송(kabelansluten_värde.물리주소, INDEX, 1, värde); }
static int 물리준비(void) {
    kabelansluten_värde.물리주소 = -1;
    for (unsigned Adress = 0; Adress < 32; Adress++) {
        int 식별 = 물리전송(Adress, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { kabelansluten_värde.물리주소 = Adress; break; }
    }
    if (kabelansluten_värde.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int värde = 물리읽기(BRGPHY_MII_AUXCTL);
    if (värde < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (värde & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    värde = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (värde < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (värde & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Förbereda_Loop(unsigned Bakgrund_värde) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_värde = Bakgrund_värde + 0xc00 + GENET_DMA_RING_SIZE * Loop_nummer;
    for (unsigned position = 0; position <= 0x30; position += 4) 유선저장기(Loop_värde + position) = 0;
    유선저장기(Loop_värde + 0x10) = (Loop_ANTAL << 16) | buffertstorlek;
    유선저장기(Loop_värde + 0x1c) = Loop_ANTAL * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Bakgrund_värde == GENET_RX_BASE) 유선저장기(Loop_värde + 0x28) = (5 << 16) | (Loop_ANTAL >> 4);
    else 유선저장기(Loop_värde + 0x24) = 1;
    유선저장기(Bakgrund_värde + 0x104c) = 8;
    유선저장기(Bakgrund_värde + 0x1040) = __BIT(Loop_nummer);
}
static void 받는주소(unsigned positionsindex) {
    uintptr_t Adress = (uintptr_t)kabelansluten_värde.få[positionsindex];
    Rent_cache((void *)Adress, buffertstorlek, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(positionsindex)) = (uint32_t)Adress;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(positionsindex)) = (uint64_t)Adress >> 32;
    유선저장기(GENET_RX_DESC_STATUS(positionsindex)) = buffertstorlek << 16;
}
static err_t skicka_datagram(struct netif *enhet_värde, struct pbuf *datagram) {
    if (!kabelansluten_värde.Förbereda || !netif_is_link_up(enhet_värde)) return ERR_RTE;
    unsigned Storlek = datagram->tot_len;
    if (!Storlek || Storlek > 1536) return ERR_BUF;
    uint16_t använda_värde_84aa75c8 = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_nummer));
    if ((uint16_t)(kabelansluten_värde.생산 - använda_värde_84aa75c8) >= Loop_ANTAL - 1) return ERR_MEM;
    unsigned positionsindex = kabelansluten_värde.생산 % Loop_ANTAL, 송신길이 = Storlek < 60 ? 60 : Storlek;
    unsigned char *data = kabelansluten_värde.skicka[positionsindex];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(datagram, data, Storlek, 0) != Storlek) return ERR_BUF;
    Rent_cache(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(positionsindex)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(positionsindex)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(positionsindex)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synka();
    kabelansluten_värde.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_nummer)) = kabelansluten_värde.생산;
    kabelansluten_värde.Statistik_värde[2]++; kabelansluten_värde.Statistik_värde[3] += Storlek;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Förbereda_kabelansluten_nätverk(struct netif *enhet_värde) {
    unsigned char Adress[6];
    if (!유선장치있음() || !Tavla_absolut_adress(Adress) || (Adress[0] & 1)) return ERR_IF;
    unsigned SUM_värde = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_värde |= Adress[순번];
    if (!SUM_värde) return ERR_IF;
    memset(&kabelansluten_värde, 0, sizeof(kabelansluten_värde));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t starttillstånd = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = starttillstånd | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = starttillstånd & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)Adress[0] << 24 | (uint32_t)Adress[1] << 16 | Adress[2] << 8 | Adress[3];
    유선저장기(GENET_UMAC_MAC1) = Adress[4] << 8 | Adress[5];
    Förbereda_Loop(GENET_TX_BASE); Förbereda_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_ANTAL; 순번++) 받는주소(순번);
    synka();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_nummer);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_nummer);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    enhet_värde->name[0] = 'e'; enhet_värde->name[1] = 'n'; enhet_värde->mtu = 1500;
    enhet_värde->hwaddr_len = 6; memcpy(enhet_värde->hwaddr, Adress, 6);
    enhet_värde->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    enhet_värde->output = etharp_output; enhet_värde->linkoutput = skicka_datagram;
    kabelansluten_värde.Förbereda = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *enhet_värde) {
    if (!kabelansluten_värde.Förbereda) return;
    uintptr_t NU_värde = 보드밀리초();
    if (NU_värde >= kabelansluten_värde.verifiera_Nästa_objekt) {
        kabelansluten_värde.verifiera_Nästa_objekt = NU_värde + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int status_värde = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metod_läge = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metod_läge == 7 ? 1000 : metod_läge == 5 ? 100 : metod_läge == 2 ? 10 : 0;
        kabelansluten_värde.속도 = status_värde >= 0 && (status_värde & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (kabelansluten_värde.속도) {
            uint32_t Inställningar = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Inställningar &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Inställningar | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Inställningar = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Inställningar | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(enhet_värde)) netif_set_link_up(enhet_värde);
        } else if (netif_is_link_up(enhet_värde)) netif_set_link_down(enhet_värde);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_nummer));
    unsigned 남음 = (uint16_t)(생산 - kabelansluten_värde.använda_värde_84aa75c8);
    if (남음 > Loop_ANTAL) { kabelansluten_värde.Statistik_värde[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned positionsindex = kabelansluten_värde.använda_värde_84aa75c8 % Loop_ANTAL;
        synka();
        uint32_t status_värde = 유선저장기(GENET_RX_DESC_STATUS(positionsindex));
        unsigned längd_värde = (status_värde & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t gräns_värde = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((status_värde & (gräns_värde | GENET_RX_DESC_STATUS_RX_ERROR)) != gräns_värde || längd_värde < 16 || längd_värde > 1538) kabelansluten_värde.Statistik_värde[4]++;
        else {
            Rent_cache(kabelansluten_värde.få[positionsindex], längd_värde, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, längd_värde - 2, PBUF_POOL);
            if (!data) kabelansluten_värde.Statistik_värde[4]++;
            else if (pbuf_take(data, kabelansluten_värde.få[positionsindex] + 2, längd_värde - 2) != ERR_OK || enhet_värde->input(data, enhet_värde) != ERR_OK) {
                pbuf_free(data); kabelansluten_värde.Statistik_värde[4]++;
            } else { kabelansluten_värde.Statistik_värde[0]++; kabelansluten_värde.Statistik_värde[1] += längd_värde - 2; }
        }
        받는주소(positionsindex); synka(); kabelansluten_värde.använda_värde_84aa75c8++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_nummer)) = kabelansluten_värde.använda_värde_84aa75c8;
    }
}
uint32_t kabelansluten_nätverk_Statistik(unsigned post_värde) {
    return post_värde < 5 ? kabelansluten_värde.Statistik_värde[post_värde] : post_värde == 5 ? kabelansluten_värde.속도 : post_värde == 6 ? kabelansluten_värde.Förbereda : 0;
}
