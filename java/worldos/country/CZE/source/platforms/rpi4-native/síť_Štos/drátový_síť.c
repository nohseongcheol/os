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
#include "drátový_síť.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Panel_absolutní_adresa(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(Adresa) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (Adresa)))
#endif
enum { Loop_číslo = 16, Loop_POČET = 256, zásobník_změnit_velikost = 2048 };
static struct {
    unsigned char dostat[Loop_POČET][zásobník_změnit_velikost];
    unsigned char poslat[Loop_POČET][zásobník_změnit_velikost];
    uint16_t využívat_HODNOTA, 생산;
    int 물리주소, Připravit, 속도;
    uint32_t Statistika_HODNOTA[5];
    uintptr_t ověřit_Další_zboží;
} drátový_HODNOTA __attribute__((aligned(64)));

static void synchronizovat(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Čisté_mezipaměť(void *data, unsigned délka_HODNOTA, int dostat) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + délka_HODNOTA;
    for (uintptr_t Adresa = (uintptr_t)data & ~(uintptr_t)63; Adresa < 끝; Adresa += 64) {
        if (dostat) __asm__ volatile("dc ivac, %0" :: "r"(Adresa) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(Adresa) : "memory");
    }
#else
    (void)data; (void)délka_HODNOTA; (void)dostat;
#endif
    synchronizovat();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned Adresa, unsigned INDEX, int Zápis, unsigned HODNOTA) {
    uint32_t příkaz = (Zápis ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (Adresa << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (HODNOTA & 65535);
    유선저장기(GENET_MDIO_CMD) = příkaz;
    유선저장기(GENET_MDIO_CMD) = příkaz | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Stav_HODNOTA = 유선저장기(GENET_MDIO_CMD);
        if (!(Stav_HODNOTA & GENET_MDIO_START_BUSY))
            return Stav_HODNOTA & GENET_MDIO_READ_FAILED ? -1 : (int)(Stav_HODNOTA & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(drátový_HODNOTA.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned HODNOTA) { return 물리전송(drátový_HODNOTA.물리주소, INDEX, 1, HODNOTA); }
static int 물리준비(void) {
    drátový_HODNOTA.물리주소 = -1;
    for (unsigned Adresa = 0; Adresa < 32; Adresa++) {
        int 식별 = 물리전송(Adresa, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { drátový_HODNOTA.물리주소 = Adresa; break; }
    }
    if (drátový_HODNOTA.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int HODNOTA = 물리읽기(BRGPHY_MII_AUXCTL);
    if (HODNOTA < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (HODNOTA & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    HODNOTA = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (HODNOTA < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (HODNOTA & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Připravit_Loop(unsigned Pozadí_HODNOTA) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_HODNOTA = Pozadí_HODNOTA + 0xc00 + GENET_DMA_RING_SIZE * Loop_číslo;
    for (unsigned pozice = 0; pozice <= 0x30; pozice += 4) 유선저장기(Loop_HODNOTA + pozice) = 0;
    유선저장기(Loop_HODNOTA + 0x10) = (Loop_POČET << 16) | zásobník_změnit_velikost;
    유선저장기(Loop_HODNOTA + 0x1c) = Loop_POČET * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Pozadí_HODNOTA == GENET_RX_BASE) 유선저장기(Loop_HODNOTA + 0x28) = (5 << 16) | (Loop_POČET >> 4);
    else 유선저장기(Loop_HODNOTA + 0x24) = 1;
    유선저장기(Pozadí_HODNOTA + 0x104c) = 8;
    유선저장기(Pozadí_HODNOTA + 0x1040) = __BIT(Loop_číslo);
}
static void 받는주소(unsigned poziční_index) {
    uintptr_t Adresa = (uintptr_t)drátový_HODNOTA.dostat[poziční_index];
    Čisté_mezipaměť((void *)Adresa, zásobník_změnit_velikost, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(poziční_index)) = (uint32_t)Adresa;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(poziční_index)) = (uint64_t)Adresa >> 32;
    유선저장기(GENET_RX_DESC_STATUS(poziční_index)) = zásobník_změnit_velikost << 16;
}
static err_t poslat_datagram(struct netif *mobilní_HODNOTA, struct pbuf *datagram) {
    if (!drátový_HODNOTA.Připravit || !netif_is_link_up(mobilní_HODNOTA)) return ERR_RTE;
    unsigned Velikost = datagram->tot_len;
    if (!Velikost || Velikost > 1536) return ERR_BUF;
    uint16_t využívat_HODNOTA = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_číslo));
    if ((uint16_t)(drátový_HODNOTA.생산 - využívat_HODNOTA) >= Loop_POČET - 1) return ERR_MEM;
    unsigned poziční_index = drátový_HODNOTA.생산 % Loop_POČET, 송신길이 = Velikost < 60 ? 60 : Velikost;
    unsigned char *data = drátový_HODNOTA.poslat[poziční_index];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(datagram, data, Velikost, 0) != Velikost) return ERR_BUF;
    Čisté_mezipaměť(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(poziční_index)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(poziční_index)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(poziční_index)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synchronizovat();
    drátový_HODNOTA.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_číslo)) = drátový_HODNOTA.생산;
    drátový_HODNOTA.Statistika_HODNOTA[2]++; drátový_HODNOTA.Statistika_HODNOTA[3] += Velikost;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Připravit_drátový_síť(struct netif *mobilní_HODNOTA) {
    unsigned char Adresa[6];
    if (!유선장치있음() || !Panel_absolutní_adresa(Adresa) || (Adresa[0] & 1)) return ERR_IF;
    unsigned SUMA_HODNOTA = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUMA_HODNOTA |= Adresa[순번];
    if (!SUMA_HODNOTA) return ERR_IF;
    memset(&drátový_HODNOTA, 0, sizeof(drátový_HODNOTA));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t počáteční_stav = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = počáteční_stav | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = počáteční_stav & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)Adresa[0] << 24 | (uint32_t)Adresa[1] << 16 | Adresa[2] << 8 | Adresa[3];
    유선저장기(GENET_UMAC_MAC1) = Adresa[4] << 8 | Adresa[5];
    Připravit_Loop(GENET_TX_BASE); Připravit_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_POČET; 순번++) 받는주소(순번);
    synchronizovat();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_číslo);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_číslo);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    mobilní_HODNOTA->name[0] = 'e'; mobilní_HODNOTA->name[1] = 'n'; mobilní_HODNOTA->mtu = 1500;
    mobilní_HODNOTA->hwaddr_len = 6; memcpy(mobilní_HODNOTA->hwaddr, Adresa, 6);
    mobilní_HODNOTA->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    mobilní_HODNOTA->output = etharp_output; mobilní_HODNOTA->linkoutput = poslat_datagram;
    drátový_HODNOTA.Připravit = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *mobilní_HODNOTA) {
    if (!drátový_HODNOTA.Připravit) return;
    uintptr_t NOW_HODNOTA = 보드밀리초();
    if (NOW_HODNOTA >= drátový_HODNOTA.ověřit_Další_zboží) {
        drátový_HODNOTA.ověřit_Další_zboží = NOW_HODNOTA + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Stav_HODNOTA = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metoda_MODE = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metoda_MODE == 7 ? 1000 : metoda_MODE == 5 ? 100 : metoda_MODE == 2 ? 10 : 0;
        drátový_HODNOTA.속도 = Stav_HODNOTA >= 0 && (Stav_HODNOTA & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (drátový_HODNOTA.속도) {
            uint32_t Nastavení = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Nastavení &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Nastavení | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Nastavení = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Nastavení | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(mobilní_HODNOTA)) netif_set_link_up(mobilní_HODNOTA);
        } else if (netif_is_link_up(mobilní_HODNOTA)) netif_set_link_down(mobilní_HODNOTA);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_číslo));
    unsigned 남음 = (uint16_t)(생산 - drátový_HODNOTA.využívat_HODNOTA);
    if (남음 > Loop_POČET) { drátový_HODNOTA.Statistika_HODNOTA[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned poziční_index = drátový_HODNOTA.využívat_HODNOTA % Loop_POČET;
        synchronizovat();
        uint32_t Stav_HODNOTA = 유선저장기(GENET_RX_DESC_STATUS(poziční_index));
        unsigned délka_HODNOTA = (Stav_HODNOTA & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t mez_HODNOTA = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Stav_HODNOTA & (mez_HODNOTA | GENET_RX_DESC_STATUS_RX_ERROR)) != mez_HODNOTA || délka_HODNOTA < 16 || délka_HODNOTA > 1538) drátový_HODNOTA.Statistika_HODNOTA[4]++;
        else {
            Čisté_mezipaměť(drátový_HODNOTA.dostat[poziční_index], délka_HODNOTA, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, délka_HODNOTA - 2, PBUF_POOL);
            if (!data) drátový_HODNOTA.Statistika_HODNOTA[4]++;
            else if (pbuf_take(data, drátový_HODNOTA.dostat[poziční_index] + 2, délka_HODNOTA - 2) != ERR_OK || mobilní_HODNOTA->input(data, mobilní_HODNOTA) != ERR_OK) {
                pbuf_free(data); drátový_HODNOTA.Statistika_HODNOTA[4]++;
            } else { drátový_HODNOTA.Statistika_HODNOTA[0]++; drátový_HODNOTA.Statistika_HODNOTA[1] += délka_HODNOTA - 2; }
        }
        받는주소(poziční_index); synchronizovat(); drátový_HODNOTA.využívat_HODNOTA++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_číslo)) = drátový_HODNOTA.využívat_HODNOTA;
    }
}
uint32_t drátový_síť_Statistika(unsigned položka_HODNOTA) {
    return položka_HODNOTA < 5 ? drátový_HODNOTA.Statistika_HODNOTA[položka_HODNOTA] : položka_HODNOTA == 5 ? drátový_HODNOTA.속도 : položka_HODNOTA == 6 ? drátový_HODNOTA.Připravit : 0;
}
