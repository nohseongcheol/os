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
#include "bekabeld_net.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Bord_absoluut_adres(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ADRES) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ADRES)))
#endif
enum { lus_nummer = 16, lus_AANTAL = 256, buffergrootte = 2048 };
static struct {
    unsigned char ontvangen[lus_AANTAL][buffergrootte];
    unsigned char e_mailen[lus_AANTAL][buffergrootte];
    uint16_t gebruiken_WAARDE, 생산;
    int 물리주소, Bereid_voor, 속도;
    uint32_t Statistieken_WAARDE[5];
    uintptr_t bevestigen_Volgende_item;
} bekabeld_WAARDE __attribute__((aligned(64)));

static void synchroniseren(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Verscherpt_cache(void *gegevens, unsigned tijdsduur_WAARDE, int ontvangen) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)gegevens + tijdsduur_WAARDE;
    for (uintptr_t ADRES = (uintptr_t)gegevens & ~(uintptr_t)63; ADRES < 끝; ADRES += 64) {
        if (ontvangen) __asm__ volatile("dc ivac, %0" :: "r"(ADRES) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ADRES) : "memory");
    }
#else
    (void)gegevens; (void)tijdsduur_WAARDE; (void)ontvangen;
#endif
    synchroniseren();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ADRES, unsigned INDEX, int Schrijven, unsigned WAARDE) {
    uint32_t opdracht = (Schrijven ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ADRES << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (WAARDE & 65535);
    유선저장기(GENET_MDIO_CMD) = opdracht;
    유선저장기(GENET_MDIO_CMD) = opdracht | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Status_WAARDE = 유선저장기(GENET_MDIO_CMD);
        if (!(Status_WAARDE & GENET_MDIO_START_BUSY))
            return Status_WAARDE & GENET_MDIO_READ_FAILED ? -1 : (int)(Status_WAARDE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(bekabeld_WAARDE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned WAARDE) { return 물리전송(bekabeld_WAARDE.물리주소, INDEX, 1, WAARDE); }
static int 물리준비(void) {
    bekabeld_WAARDE.물리주소 = -1;
    for (unsigned ADRES = 0; ADRES < 32; ADRES++) {
        int 식별 = 물리전송(ADRES, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { bekabeld_WAARDE.물리주소 = ADRES; break; }
    }
    if (bekabeld_WAARDE.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int WAARDE = 물리읽기(BRGPHY_MII_AUXCTL);
    if (WAARDE < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (WAARDE & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    WAARDE = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (WAARDE < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (WAARDE & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Bereid_voor_lus(unsigned Achtergrond_WAARDE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned lus_WAARDE = Achtergrond_WAARDE + 0xc00 + GENET_DMA_RING_SIZE * lus_nummer;
    for (unsigned positie = 0; positie <= 0x30; positie += 4) 유선저장기(lus_WAARDE + positie) = 0;
    유선저장기(lus_WAARDE + 0x10) = (lus_AANTAL << 16) | buffergrootte;
    유선저장기(lus_WAARDE + 0x1c) = lus_AANTAL * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Achtergrond_WAARDE == GENET_RX_BASE) 유선저장기(lus_WAARDE + 0x28) = (5 << 16) | (lus_AANTAL >> 4);
    else 유선저장기(lus_WAARDE + 0x24) = 1;
    유선저장기(Achtergrond_WAARDE + 0x104c) = 8;
    유선저장기(Achtergrond_WAARDE + 0x1040) = __BIT(lus_nummer);
}
static void 받는주소(unsigned plaatsingsindex) {
    uintptr_t ADRES = (uintptr_t)bekabeld_WAARDE.ontvangen[plaatsingsindex];
    Verscherpt_cache((void *)ADRES, buffergrootte, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(plaatsingsindex)) = (uint32_t)ADRES;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(plaatsingsindex)) = (uint64_t)ADRES >> 32;
    유선저장기(GENET_RX_DESC_STATUS(plaatsingsindex)) = buffergrootte << 16;
}
static err_t e_mailen_datagram(struct netif *mobiel_WAARDE, struct pbuf *datagram) {
    if (!bekabeld_WAARDE.Bereid_voor || !netif_is_link_up(mobiel_WAARDE)) return ERR_RTE;
    unsigned Grootte = datagram->tot_len;
    if (!Grootte || Grootte > 1536) return ERR_BUF;
    uint16_t gebruiken_WAARDE = 유선저장기(GENET_TX_DMA_CONS_INDEX(lus_nummer));
    if ((uint16_t)(bekabeld_WAARDE.생산 - gebruiken_WAARDE) >= lus_AANTAL - 1) return ERR_MEM;
    unsigned plaatsingsindex = bekabeld_WAARDE.생산 % lus_AANTAL, 송신길이 = Grootte < 60 ? 60 : Grootte;
    unsigned char *gegevens = bekabeld_WAARDE.e_mailen[plaatsingsindex];
    memset(gegevens, 0, 송신길이);
    if (pbuf_copy_partial(datagram, gegevens, Grootte, 0) != Grootte) return ERR_BUF;
    Verscherpt_cache(gegevens, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(plaatsingsindex)) = (uint32_t)(uintptr_t)gegevens;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(plaatsingsindex)) = (uint64_t)(uintptr_t)gegevens >> 32;
    유선저장기(GENET_TX_DESC_STATUS(plaatsingsindex)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synchroniseren();
    bekabeld_WAARDE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(lus_nummer)) = bekabeld_WAARDE.생산;
    bekabeld_WAARDE.Statistieken_WAARDE[2]++; bekabeld_WAARDE.Statistieken_WAARDE[3] += Grootte;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Bereid_voor_bekabeld_net(struct netif *mobiel_WAARDE) {
    unsigned char ADRES[6];
    if (!유선장치있음() || !Bord_absoluut_adres(ADRES) || (ADRES[0] & 1)) return ERR_IF;
    unsigned SOM_WAARDE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SOM_WAARDE |= ADRES[순번];
    if (!SOM_WAARDE) return ERR_IF;
    memset(&bekabeld_WAARDE, 0, sizeof(bekabeld_WAARDE));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t begintoestand = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = begintoestand | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = begintoestand & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ADRES[0] << 24 | (uint32_t)ADRES[1] << 16 | ADRES[2] << 8 | ADRES[3];
    유선저장기(GENET_UMAC_MAC1) = ADRES[4] << 8 | ADRES[5];
    Bereid_voor_lus(GENET_TX_BASE); Bereid_voor_lus(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < lus_AANTAL; 순번++) 받는주소(순번);
    synchroniseren();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(lus_nummer);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(lus_nummer);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    mobiel_WAARDE->name[0] = 'e'; mobiel_WAARDE->name[1] = 'n'; mobiel_WAARDE->mtu = 1500;
    mobiel_WAARDE->hwaddr_len = 6; memcpy(mobiel_WAARDE->hwaddr, ADRES, 6);
    mobiel_WAARDE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    mobiel_WAARDE->output = etharp_output; mobiel_WAARDE->linkoutput = e_mailen_datagram;
    bekabeld_WAARDE.Bereid_voor = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *mobiel_WAARDE) {
    if (!bekabeld_WAARDE.Bereid_voor) return;
    uintptr_t NU_WAARDE = 보드밀리초();
    if (NU_WAARDE >= bekabeld_WAARDE.bevestigen_Volgende_item) {
        bekabeld_WAARDE.bevestigen_Volgende_item = NU_WAARDE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Status_WAARDE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned methode_MODUS = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = methode_MODUS == 7 ? 1000 : methode_MODUS == 5 ? 100 : methode_MODUS == 2 ? 10 : 0;
        bekabeld_WAARDE.속도 = Status_WAARDE >= 0 && (Status_WAARDE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (bekabeld_WAARDE.속도) {
            uint32_t Instellingen = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Instellingen &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Instellingen | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Instellingen = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Instellingen | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(mobiel_WAARDE)) netif_set_link_up(mobiel_WAARDE);
        } else if (netif_is_link_up(mobiel_WAARDE)) netif_set_link_down(mobiel_WAARDE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(lus_nummer));
    unsigned 남음 = (uint16_t)(생산 - bekabeld_WAARDE.gebruiken_WAARDE);
    if (남음 > lus_AANTAL) { bekabeld_WAARDE.Statistieken_WAARDE[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned plaatsingsindex = bekabeld_WAARDE.gebruiken_WAARDE % lus_AANTAL;
        synchroniseren();
        uint32_t Status_WAARDE = 유선저장기(GENET_RX_DESC_STATUS(plaatsingsindex));
        unsigned tijdsduur_WAARDE = (Status_WAARDE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t grens_WAARDE = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Status_WAARDE & (grens_WAARDE | GENET_RX_DESC_STATUS_RX_ERROR)) != grens_WAARDE || tijdsduur_WAARDE < 16 || tijdsduur_WAARDE > 1538) bekabeld_WAARDE.Statistieken_WAARDE[4]++;
        else {
            Verscherpt_cache(bekabeld_WAARDE.ontvangen[plaatsingsindex], tijdsduur_WAARDE, 1);
            struct pbuf *gegevens = pbuf_alloc(PBUF_RAW, tijdsduur_WAARDE - 2, PBUF_POOL);
            if (!gegevens) bekabeld_WAARDE.Statistieken_WAARDE[4]++;
            else if (pbuf_take(gegevens, bekabeld_WAARDE.ontvangen[plaatsingsindex] + 2, tijdsduur_WAARDE - 2) != ERR_OK || mobiel_WAARDE->input(gegevens, mobiel_WAARDE) != ERR_OK) {
                pbuf_free(gegevens); bekabeld_WAARDE.Statistieken_WAARDE[4]++;
            } else { bekabeld_WAARDE.Statistieken_WAARDE[0]++; bekabeld_WAARDE.Statistieken_WAARDE[1] += tijdsduur_WAARDE - 2; }
        }
        받는주소(plaatsingsindex); synchroniseren(); bekabeld_WAARDE.gebruiken_WAARDE++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(lus_nummer)) = bekabeld_WAARDE.gebruiken_WAARDE;
    }
}
uint32_t bekabeld_net_Statistieken(unsigned invoer_WAARDE_962f286b) {
    return invoer_WAARDE_962f286b < 5 ? bekabeld_WAARDE.Statistieken_WAARDE[invoer_WAARDE_962f286b] : invoer_WAARDE_962f286b == 5 ? bekabeld_WAARDE.속도 : invoer_WAARDE_962f286b == 6 ? bekabeld_WAARDE.Bereid_voor : 0;
}
