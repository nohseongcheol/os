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

#include "../benennung/maschineBindenNamen.h"
#include "verdrahtetNetzwerk.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(schleifeOrdnungszahl) (UINT32_C(1) << (schleifeOrdnungszahl))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t platineVergangeneMillisekunden(void);
extern int platinePhysischHardware(void);
extern int platineMaschineAdresse(unsigned char *);
#ifndef verdrahtetRegisterliste
#define verdrahtetRegisterliste(adresse) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (adresse)))
#endif
enum { schleifeNummer = 16, schleifeAnzahl = 256, pufferGröße = 2048 };
static struct {
    unsigned char empfangen[schleifeAnzahl][pufferGröße];
    unsigned char senden[schleifeAnzahl][pufferGröße];
    uint16_t wertVerbrauchen, erzeugenWert;
    int physischAdresse, vorbereiten, geschwindigkeitWert;
    uint32_t statistikWert[5];
    uintptr_t nächsterElementeintragÜberprüfen;
} verdrahtetWert __attribute__((aligned(64)));

static void synchronisieren(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void bereinigenZwischenspeicher(void *Daten, unsigned Länge, int empfangen) {
#ifndef JKOROS_GENET_TEST
    uintptr_t endung = (uintptr_t)Daten + Länge;
    for (uintptr_t adresse = (uintptr_t)Daten & ~(uintptr_t)63; adresse < endung; adresse += 64) {
        if (empfangen) __asm__ volatile("dc ivac, %0" :: "r"(adresse) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(adresse) : "memory");
    }
#else
    (void)Daten; (void)Länge; (void)empfangen;
#endif
    synchronisieren();
}
static void kurzzeitigVerzögerung(void) {
    uintptr_t endung = platineVergangeneMillisekunden() + 1;
    while (platineVergangeneMillisekunden() < endung) {}
}
static int physischÜbertragung(unsigned adresse, unsigned Nummer, int schreiben, unsigned Wert) {
    uint32_t befehl = (schreiben ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (adresse << GENET_MDIO_ADDR_SHIFT) | (Nummer << GENET_MDIO_REG_SHIFT) | (Wert & 65535);
    verdrahtetRegisterliste(GENET_MDIO_CMD) = befehl;
    verdrahtetRegisterliste(GENET_MDIO_CMD) = befehl | GENET_MDIO_START_BUSY;
    uintptr_t endung = platineVergangeneMillisekunden() + 20;
    for (;;) {
        uint32_t statuswertWert = verdrahtetRegisterliste(GENET_MDIO_CMD);
        if (!(statuswertWert & GENET_MDIO_START_BUSY))
            return statuswertWert & GENET_MDIO_READ_FAILED ? -1 : (int)(statuswertWert & 65535);
        if (platineVergangeneMillisekunden() >= endung) return -1;
    }
}
static int physischLesen(unsigned Nummer) { return physischÜbertragung(verdrahtetWert.physischAdresse, Nummer, 0, 0); }
static int physischSchreiben(unsigned Nummer, unsigned Wert) { return physischÜbertragung(verdrahtetWert.physischAdresse, Nummer, 1, Wert); }
static int physischVorbereiten(void) {
    verdrahtetWert.physischAdresse = -1;
    for (unsigned adresse = 0; adresse < 32; adresse++) {
        int wertIdentifizieren = physischÜbertragung(adresse, 2, 0, 0);
        if (wertIdentifizieren > 0 && wertIdentifizieren != 65535) { verdrahtetWert.physischAdresse = adresse; break; }
    }
    if (verdrahtetWert.physischAdresse < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (physischSchreiben(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int Wert = physischLesen(BRGPHY_MII_AUXCTL);
    if (Wert < 0 || physischSchreiben(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (Wert & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (physischSchreiben(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    Wert = physischLesen(BRGPHY_MII_SHADOW_1C);
    if (Wert < 0 || physischSchreiben(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (Wert & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (physischSchreiben(4, 0x0141) < 0 || physischSchreiben(9, 0x0200) < 0) return -1;
    return physischSchreiben(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void schleifeVorbereiten(unsigned hintergrundWert) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned schleifeWert = hintergrundWert + 0xc00 + GENET_DMA_RING_SIZE * schleifeNummer;
    for (unsigned position = 0; position <= 0x30; position += 4) verdrahtetRegisterliste(schleifeWert + position) = 0;
    verdrahtetRegisterliste(schleifeWert + 0x10) = (schleifeAnzahl << 16) | pufferGröße;
    verdrahtetRegisterliste(schleifeWert + 0x1c) = schleifeAnzahl * GENET_DMA_DESC_SIZE / 4 - 1;
    if (hintergrundWert == GENET_RX_BASE) verdrahtetRegisterliste(schleifeWert + 0x28) = (5 << 16) | (schleifeAnzahl >> 4);
    else verdrahtetRegisterliste(schleifeWert + 0x24) = 1;
    verdrahtetRegisterliste(hintergrundWert + 0x104c) = 8;
    verdrahtetRegisterliste(hintergrundWert + 0x1040) = __BIT(schleifeNummer);
}
static void empfangendAdresse(unsigned positionIndex) {
    uintptr_t adresse = (uintptr_t)verdrahtetWert.empfangen[positionIndex];
    bereinigenZwischenspeicher((void *)adresse, pufferGröße, 0);
    verdrahtetRegisterliste(GENET_RX_DESC_ADDRESS_LO(positionIndex)) = (uint32_t)adresse;
    verdrahtetRegisterliste(GENET_RX_DESC_ADDRESS_HI(positionIndex)) = (uint64_t)adresse >> 32;
    verdrahtetRegisterliste(GENET_RX_DESC_STATUS(positionIndex)) = pufferGröße << 16;
}
static err_t datagrammSenden(struct netif *Gerät, struct pbuf *datagramm) {
    if (!verdrahtetWert.vorbereiten || !netif_is_link_up(Gerät)) return ERR_RTE;
    unsigned größe = datagramm->tot_len;
    if (!größe || größe > 1536) return ERR_BUF;
    uint16_t wertVerbrauchen = verdrahtetRegisterliste(GENET_TX_DMA_CONS_INDEX(schleifeNummer));
    if ((uint16_t)(verdrahtetWert.erzeugenWert - wertVerbrauchen) >= schleifeAnzahl - 1) return ERR_MEM;
    unsigned positionIndex = verdrahtetWert.erzeugenWert % schleifeAnzahl, übertragenLänge = größe < 60 ? 60 : größe;
    unsigned char *Daten = verdrahtetWert.senden[positionIndex];
    memset(Daten, 0, übertragenLänge);
    if (pbuf_copy_partial(datagramm, Daten, größe, 0) != größe) return ERR_BUF;
    bereinigenZwischenspeicher(Daten, übertragenLänge, 0);
    verdrahtetRegisterliste(GENET_TX_DESC_ADDRESS_LO(positionIndex)) = (uint32_t)(uintptr_t)Daten;
    verdrahtetRegisterliste(GENET_TX_DESC_ADDRESS_HI(positionIndex)) = (uint64_t)(uintptr_t)Daten >> 32;
    verdrahtetRegisterliste(GENET_TX_DESC_STATUS(positionIndex)) = (übertragenLänge << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synchronisieren();
    verdrahtetWert.erzeugenWert++;
    verdrahtetRegisterliste(GENET_TX_DMA_PROD_INDEX(schleifeNummer)) = verdrahtetWert.erzeugenWert;
    verdrahtetWert.statistikWert[2]++; verdrahtetWert.statistikWert[3] += größe;
    return ERR_OK;
}
int hatVerdrahtetGerät(void) {
    return platinePhysischHardware() && ((verdrahtetRegisterliste(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t verdrahtetNetzwerkVorbereiten(struct netif *Gerät) {
    unsigned char adresse[6];
    if (!hatVerdrahtetGerät() || !platineMaschineAdresse(adresse) || (adresse[0] & 1)) return ERR_IF;
    unsigned summeWert = 0; for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < 6; ordnungszahlIndex++) summeWert |= adresse[ordnungszahlIndex];
    if (!summeWert) return ERR_IF;
    memset(&verdrahtetWert, 0, sizeof(verdrahtetWert));
    verdrahtetRegisterliste(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    verdrahtetRegisterliste(GENET_RX_DMA_CTRL) = verdrahtetRegisterliste(GENET_TX_DMA_CTRL) = 0;
    uint32_t anfänglichStatuswert = verdrahtetRegisterliste(GENET_SYS_RBUF_FLUSH_CTRL);
    verdrahtetRegisterliste(GENET_SYS_RBUF_FLUSH_CTRL) = anfänglichStatuswert | GENET_SYS_RBUF_FLUSH_RESET; kurzzeitigVerzögerung();
    verdrahtetRegisterliste(GENET_SYS_RBUF_FLUSH_CTRL) = anfänglichStatuswert & ~GENET_SYS_RBUF_FLUSH_RESET; kurzzeitigVerzögerung();
    verdrahtetRegisterliste(GENET_SYS_RBUF_FLUSH_CTRL) = 0; kurzzeitigVerzögerung();
    verdrahtetRegisterliste(GENET_UMAC_CMD) = 0;
    verdrahtetRegisterliste(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; kurzzeitigVerzögerung();
    verdrahtetRegisterliste(GENET_UMAC_CMD) = 0;
    verdrahtetRegisterliste(GENET_UMAC_MIB_CTRL) = 7;
    verdrahtetRegisterliste(GENET_UMAC_MIB_CTRL) = 0;
    verdrahtetRegisterliste(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (physischVorbereiten() < 0) return ERR_IF;
    verdrahtetRegisterliste(GENET_UMAC_MAC0) = (uint32_t)adresse[0] << 24 | (uint32_t)adresse[1] << 16 | adresse[2] << 8 | adresse[3];
    verdrahtetRegisterliste(GENET_UMAC_MAC1) = adresse[4] << 8 | adresse[5];
    schleifeVorbereiten(GENET_TX_BASE); schleifeVorbereiten(GENET_RX_BASE);
    for (unsigned ordnungszahlIndex = 0; ordnungszahlIndex < schleifeAnzahl; ordnungszahlIndex++) empfangendAdresse(ordnungszahlIndex);
    synchronisieren();
    verdrahtetRegisterliste(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(schleifeNummer);
    verdrahtetRegisterliste(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(schleifeNummer);
    verdrahtetRegisterliste(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    verdrahtetRegisterliste(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    verdrahtetRegisterliste(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    verdrahtetRegisterliste(GENET_UMAC_MDF_CTRL) = 0;
    verdrahtetRegisterliste(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    Gerät->name[0] = 'e'; Gerät->name[1] = 'n'; Gerät->mtu = 1500;
    Gerät->hwaddr_len = 6; memcpy(Gerät->hwaddr, adresse, 6);
    Gerät->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    Gerät->output = etharp_output; Gerät->linkoutput = datagrammSenden;
    verdrahtetWert.vorbereiten = 1;
    return ERR_OK;
}
void verdrahtetNetzwerkUntersuchen(struct netif *Gerät) {
    if (!verdrahtetWert.vorbereiten) return;
    uintptr_t jetztWert = platineVergangeneMillisekunden();
    if (jetztWert >= verdrahtetWert.nächsterElementeintragÜberprüfen) {
        verdrahtetWert.nächsterElementeintragÜberprüfen = jetztWert + 500;
        physischLesen(BRGPHY_MII_BMSR);
        int statuswertWert = physischLesen(BRGPHY_MII_BMSR), hilfsWert = physischLesen(BRGPHY_MII_AUXSTS);
        unsigned methodeBetriebsart = hilfsWert < 0 ? 0 : (hilfsWert & BRGPHY_AUXSTS_AN_RES) >> 8;
        int geschwindigkeitWert = methodeBetriebsart == 7 ? 1000 : methodeBetriebsart == 5 ? 100 : methodeBetriebsart == 2 ? 10 : 0;
        verdrahtetWert.geschwindigkeitWert = statuswertWert >= 0 && (statuswertWert & BRGPHY_BMSR_LINK) ? geschwindigkeitWert : 0;
        if (verdrahtetWert.geschwindigkeitWert) {
            uint32_t einstellungen = verdrahtetRegisterliste(GENET_EXT_RGMII_OOB_CTRL);
            einstellungen &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            verdrahtetRegisterliste(GENET_EXT_RGMII_OOB_CTRL) = einstellungen | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            einstellungen = verdrahtetRegisterliste(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            verdrahtetRegisterliste(GENET_UMAC_CMD) = einstellungen | (geschwindigkeitWert == 1000 ? GENET_UMAC_CMD_SPEED_1000 : geschwindigkeitWert == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(Gerät)) netif_set_link_up(Gerät);
        } else if (netif_is_link_up(Gerät)) netif_set_link_down(Gerät);
    }
    uint16_t erzeugenWert = verdrahtetRegisterliste(GENET_RX_DMA_PROD_INDEX(schleifeNummer));
    unsigned restwertDaten = (uint16_t)(erzeugenWert - verdrahtetWert.wertVerbrauchen);
    if (restwertDaten > schleifeAnzahl) { verdrahtetWert.statistikWert[4]++; return; }
    for (unsigned schleifeOrdnungszahl = 0; schleifeOrdnungszahl < restwertDaten && schleifeOrdnungszahl < 32; schleifeOrdnungszahl++) {
        unsigned positionIndex = verdrahtetWert.wertVerbrauchen % schleifeAnzahl;
        synchronisieren();
        uint32_t statuswertWert = verdrahtetRegisterliste(GENET_RX_DESC_STATUS(positionIndex));
        unsigned Länge = (statuswertWert & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t grenzstelleWert = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((statuswertWert & (grenzstelleWert | GENET_RX_DESC_STATUS_RX_ERROR)) != grenzstelleWert || Länge < 16 || Länge > 1538) verdrahtetWert.statistikWert[4]++;
        else {
            bereinigenZwischenspeicher(verdrahtetWert.empfangen[positionIndex], Länge, 1);
            struct pbuf *Daten = pbuf_alloc(PBUF_RAW, Länge - 2, PBUF_POOL);
            if (!Daten) verdrahtetWert.statistikWert[4]++;
            else if (pbuf_take(Daten, verdrahtetWert.empfangen[positionIndex] + 2, Länge - 2) != ERR_OK || Gerät->input(Daten, Gerät) != ERR_OK) {
                pbuf_free(Daten); verdrahtetWert.statistikWert[4]++;
            } else { verdrahtetWert.statistikWert[0]++; verdrahtetWert.statistikWert[1] += Länge - 2; }
        }
        empfangendAdresse(positionIndex); synchronisieren(); verdrahtetWert.wertVerbrauchen++;
        verdrahtetRegisterliste(GENET_RX_DMA_CONS_INDEX(schleifeNummer)) = verdrahtetWert.wertVerbrauchen;
    }
}
uint32_t verdrahtetNetzwerkStatistik(unsigned eintragWert) {
    return eintragWert < 5 ? verdrahtetWert.statistikWert[eintragWert] : eintragWert == 5 ? verdrahtetWert.geschwindigkeitWert : eintragWert == 6 ? verdrahtetWert.vorbereiten : 0;
}
