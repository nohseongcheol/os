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
#include "vezetékes_hálózat.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int fal_valódi_cím(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(CÍM) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (CÍM)))
#endif
enum { Loop_szám = 16, Loop_DARAB = 256, pufferméret = 2048 };
static struct {
    unsigned char fogad[Loop_DARAB][pufferméret];
    unsigned char küld[Loop_DARAB][pufferméret];
    uint16_t felhasznál_ÉRTÉK, 생산;
    int 물리주소, Előkészítés, 속도;
    uint32_t statisztika_ÉRTÉK[5];
    uintptr_t igazol_Tovább_cikk;
} vezetékes_ÉRTÉK __attribute__((aligned(64)));

static void szinkronizál(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void TISZTÍT_gyorsítótár(void *adat, unsigned hossz_ÉRTÉK, int fogad) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)adat + hossz_ÉRTÉK;
    for (uintptr_t CÍM = (uintptr_t)adat & ~(uintptr_t)63; CÍM < 끝; CÍM += 64) {
        if (fogad) __asm__ volatile("dc ivac, %0" :: "r"(CÍM) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(CÍM) : "memory");
    }
#else
    (void)adat; (void)hossz_ÉRTÉK; (void)fogad;
#endif
    szinkronizál();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned CÍM, unsigned INDEX, int Írás, unsigned ÉRTÉK) {
    uint32_t Parancs = (Írás ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (CÍM << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (ÉRTÉK & 65535);
    유선저장기(GENET_MDIO_CMD) = Parancs;
    유선저장기(GENET_MDIO_CMD) = Parancs | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Állapot_ÉRTÉK = 유선저장기(GENET_MDIO_CMD);
        if (!(Állapot_ÉRTÉK & GENET_MDIO_START_BUSY))
            return Állapot_ÉRTÉK & GENET_MDIO_READ_FAILED ? -1 : (int)(Állapot_ÉRTÉK & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(vezetékes_ÉRTÉK.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned ÉRTÉK) { return 물리전송(vezetékes_ÉRTÉK.물리주소, INDEX, 1, ÉRTÉK); }
static int 물리준비(void) {
    vezetékes_ÉRTÉK.물리주소 = -1;
    for (unsigned CÍM = 0; CÍM < 32; CÍM++) {
        int 식별 = 물리전송(CÍM, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { vezetékes_ÉRTÉK.물리주소 = CÍM; break; }
    }
    if (vezetékes_ÉRTÉK.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ÉRTÉK = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ÉRTÉK < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ÉRTÉK & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ÉRTÉK = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ÉRTÉK < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ÉRTÉK & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Előkészítés_Loop(unsigned Háttér_ÉRTÉK) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_ÉRTÉK = Háttér_ÉRTÉK + 0xc00 + GENET_DMA_RING_SIZE * Loop_szám;
    for (unsigned Pozíció = 0; Pozíció <= 0x30; Pozíció += 4) 유선저장기(Loop_ÉRTÉK + Pozíció) = 0;
    유선저장기(Loop_ÉRTÉK + 0x10) = (Loop_DARAB << 16) | pufferméret;
    유선저장기(Loop_ÉRTÉK + 0x1c) = Loop_DARAB * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Háttér_ÉRTÉK == GENET_RX_BASE) 유선저장기(Loop_ÉRTÉK + 0x28) = (5 << 16) | (Loop_DARAB >> 4);
    else 유선저장기(Loop_ÉRTÉK + 0x24) = 1;
    유선저장기(Háttér_ÉRTÉK + 0x104c) = 8;
    유선저장기(Háttér_ÉRTÉK + 0x1040) = __BIT(Loop_szám);
}
static void 받는주소(unsigned helyzetindex) {
    uintptr_t CÍM = (uintptr_t)vezetékes_ÉRTÉK.fogad[helyzetindex];
    TISZTÍT_gyorsítótár((void *)CÍM, pufferméret, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(helyzetindex)) = (uint32_t)CÍM;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(helyzetindex)) = (uint64_t)CÍM >> 32;
    유선저장기(GENET_RX_DESC_STATUS(helyzetindex)) = pufferméret << 16;
}
static err_t küld_datagram(struct netif *mobil_ÉRTÉK, struct pbuf *datagram) {
    if (!vezetékes_ÉRTÉK.Előkészítés || !netif_is_link_up(mobil_ÉRTÉK)) return ERR_RTE;
    unsigned Méret = datagram->tot_len;
    if (!Méret || Méret > 1536) return ERR_BUF;
    uint16_t felhasznál_ÉRTÉK = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_szám));
    if ((uint16_t)(vezetékes_ÉRTÉK.생산 - felhasznál_ÉRTÉK) >= Loop_DARAB - 1) return ERR_MEM;
    unsigned helyzetindex = vezetékes_ÉRTÉK.생산 % Loop_DARAB, 송신길이 = Méret < 60 ? 60 : Méret;
    unsigned char *adat = vezetékes_ÉRTÉK.küld[helyzetindex];
    memset(adat, 0, 송신길이);
    if (pbuf_copy_partial(datagram, adat, Méret, 0) != Méret) return ERR_BUF;
    TISZTÍT_gyorsítótár(adat, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(helyzetindex)) = (uint32_t)(uintptr_t)adat;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(helyzetindex)) = (uint64_t)(uintptr_t)adat >> 32;
    유선저장기(GENET_TX_DESC_STATUS(helyzetindex)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    szinkronizál();
    vezetékes_ÉRTÉK.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_szám)) = vezetékes_ÉRTÉK.생산;
    vezetékes_ÉRTÉK.statisztika_ÉRTÉK[2]++; vezetékes_ÉRTÉK.statisztika_ÉRTÉK[3] += Méret;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Előkészítés_vezetékes_hálózat(struct netif *mobil_ÉRTÉK) {
    unsigned char CÍM[6];
    if (!유선장치있음() || !fal_valódi_cím(CÍM) || (CÍM[0] & 1)) return ERR_IF;
    unsigned SUM_ÉRTÉK = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_ÉRTÉK |= CÍM[순번];
    if (!SUM_ÉRTÉK) return ERR_IF;
    memset(&vezetékes_ÉRTÉK, 0, sizeof(vezetékes_ÉRTÉK));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t kiinduló_állapot = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = kiinduló_állapot | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = kiinduló_állapot & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)CÍM[0] << 24 | (uint32_t)CÍM[1] << 16 | CÍM[2] << 8 | CÍM[3];
    유선저장기(GENET_UMAC_MAC1) = CÍM[4] << 8 | CÍM[5];
    Előkészítés_Loop(GENET_TX_BASE); Előkészítés_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_DARAB; 순번++) 받는주소(순번);
    szinkronizál();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_szám);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_szám);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    mobil_ÉRTÉK->name[0] = 'e'; mobil_ÉRTÉK->name[1] = 'n'; mobil_ÉRTÉK->mtu = 1500;
    mobil_ÉRTÉK->hwaddr_len = 6; memcpy(mobil_ÉRTÉK->hwaddr, CÍM, 6);
    mobil_ÉRTÉK->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    mobil_ÉRTÉK->output = etharp_output; mobil_ÉRTÉK->linkoutput = küld_datagram;
    vezetékes_ÉRTÉK.Előkészítés = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *mobil_ÉRTÉK) {
    if (!vezetékes_ÉRTÉK.Előkészítés) return;
    uintptr_t MOST_ÉRTÉK = 보드밀리초();
    if (MOST_ÉRTÉK >= vezetékes_ÉRTÉK.igazol_Tovább_cikk) {
        vezetékes_ÉRTÉK.igazol_Tovább_cikk = MOST_ÉRTÉK + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Állapot_ÉRTÉK = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metódus_mód = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metódus_mód == 7 ? 1000 : metódus_mód == 5 ? 100 : metódus_mód == 2 ? 10 : 0;
        vezetékes_ÉRTÉK.속도 = Állapot_ÉRTÉK >= 0 && (Állapot_ÉRTÉK & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (vezetékes_ÉRTÉK.속도) {
            uint32_t Beállítások = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Beállítások &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Beállítások | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Beállítások = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Beállítások | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(mobil_ÉRTÉK)) netif_set_link_up(mobil_ÉRTÉK);
        } else if (netif_is_link_up(mobil_ÉRTÉK)) netif_set_link_down(mobil_ÉRTÉK);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_szám));
    unsigned 남음 = (uint16_t)(생산 - vezetékes_ÉRTÉK.felhasznál_ÉRTÉK);
    if (남음 > Loop_DARAB) { vezetékes_ÉRTÉK.statisztika_ÉRTÉK[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned helyzetindex = vezetékes_ÉRTÉK.felhasznál_ÉRTÉK % Loop_DARAB;
        szinkronizál();
        uint32_t Állapot_ÉRTÉK = 유선저장기(GENET_RX_DESC_STATUS(helyzetindex));
        unsigned hossz_ÉRTÉK = (Állapot_ÉRTÉK & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t határ_ÉRTÉK = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Állapot_ÉRTÉK & (határ_ÉRTÉK | GENET_RX_DESC_STATUS_RX_ERROR)) != határ_ÉRTÉK || hossz_ÉRTÉK < 16 || hossz_ÉRTÉK > 1538) vezetékes_ÉRTÉK.statisztika_ÉRTÉK[4]++;
        else {
            TISZTÍT_gyorsítótár(vezetékes_ÉRTÉK.fogad[helyzetindex], hossz_ÉRTÉK, 1);
            struct pbuf *adat = pbuf_alloc(PBUF_RAW, hossz_ÉRTÉK - 2, PBUF_POOL);
            if (!adat) vezetékes_ÉRTÉK.statisztika_ÉRTÉK[4]++;
            else if (pbuf_take(adat, vezetékes_ÉRTÉK.fogad[helyzetindex] + 2, hossz_ÉRTÉK - 2) != ERR_OK || mobil_ÉRTÉK->input(adat, mobil_ÉRTÉK) != ERR_OK) {
                pbuf_free(adat); vezetékes_ÉRTÉK.statisztika_ÉRTÉK[4]++;
            } else { vezetékes_ÉRTÉK.statisztika_ÉRTÉK[0]++; vezetékes_ÉRTÉK.statisztika_ÉRTÉK[1] += hossz_ÉRTÉK - 2; }
        }
        받는주소(helyzetindex); szinkronizál(); vezetékes_ÉRTÉK.felhasznál_ÉRTÉK++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_szám)) = vezetékes_ÉRTÉK.felhasznál_ÉRTÉK;
    }
}
uint32_t vezetékes_hálózat_statisztika(unsigned bejegyzés_ÉRTÉK) {
    return bejegyzés_ÉRTÉK < 5 ? vezetékes_ÉRTÉK.statisztika_ÉRTÉK[bejegyzés_ÉRTÉK] : bejegyzés_ÉRTÉK == 5 ? vezetékes_ÉRTÉK.속도 : bejegyzés_ÉRTÉK == 6 ? vezetékes_ÉRTÉK.Előkészítés : 0;
}
