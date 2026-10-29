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

#include "../nommage/nomsLierMachine.h"
#include "réseauCâblé.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(ordinalBoucle) (UINT32_C(1) << (ordinalBoucle))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t millisecondesÉcouléesCarteMatérielle(void);
extern int matérielPhysiqueCarteMatérielle(void);
extern int adresseMachineCarteMatérielle(unsigned char *);
#ifndef registresCâblé
#define registresCâblé(adresse) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (adresse)))
#endif
enum { numéroBoucle = 16, nombreÉlémentsBoucle = 256, tailleTampon = 2048 };
static struct {
    unsigned char recevoir[nombreÉlémentsBoucle][tailleTampon];
    unsigned char envoyer[nombreÉlémentsBoucle][tailleTampon];
    uint16_t consommerValeur, valeurProduire;
    int adressePhysique, préparer, valeurVitesse;
    uint32_t valeurStatistiques[5];
    uintptr_t vérifierÉlémentListeSuivant;
} valeurCâblé __attribute__((aligned(64)));

static void synchroniser(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void cacheMémoireNettoyer(void *Données, unsigned longueur, int recevoir) {
#ifndef JKOROS_GENET_TEST
    uintptr_t terminaison = (uintptr_t)Données + longueur;
    for (uintptr_t adresse = (uintptr_t)Données & ~(uintptr_t)63; adresse < terminaison; adresse += 64) {
        if (recevoir) __asm__ volatile("dc ivac, %0" :: "r"(adresse) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(adresse) : "memory");
    }
#else
    (void)Données; (void)longueur; (void)recevoir;
#endif
    synchroniser();
}
static void retardBref(void) {
    uintptr_t terminaison = millisecondesÉcouléesCarteMatérielle() + 1;
    while (millisecondesÉcouléesCarteMatérielle() < terminaison) {}
}
static int transfertPhysique(unsigned adresse, unsigned numéro, int écrire, unsigned valeur) {
    uint32_t commande = (écrire ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (adresse << GENET_MDIO_ADDR_SHIFT) | (numéro << GENET_MDIO_REG_SHIFT) | (valeur & 65535);
    registresCâblé(GENET_MDIO_CMD) = commande;
    registresCâblé(GENET_MDIO_CMD) = commande | GENET_MDIO_START_BUSY;
    uintptr_t terminaison = millisecondesÉcouléesCarteMatérielle() + 20;
    for (;;) {
        uint32_t valeurÉtatValeur = registresCâblé(GENET_MDIO_CMD);
        if (!(valeurÉtatValeur & GENET_MDIO_START_BUSY))
            return valeurÉtatValeur & GENET_MDIO_READ_FAILED ? -1 : (int)(valeurÉtatValeur & 65535);
        if (millisecondesÉcouléesCarteMatérielle() >= terminaison) return -1;
    }
}
static int lirePhysique(unsigned numéro) { return transfertPhysique(valeurCâblé.adressePhysique, numéro, 0, 0); }
static int écrirePhysique(unsigned numéro, unsigned valeur) { return transfertPhysique(valeurCâblé.adressePhysique, numéro, 1, valeur); }
static int préparerPhysique(void) {
    valeurCâblé.adressePhysique = -1;
    for (unsigned adresse = 0; adresse < 32; adresse++) {
        int identifierValeur = transfertPhysique(adresse, 2, 0, 0);
        if (identifierValeur > 0 && identifierValeur != 65535) { valeurCâblé.adressePhysique = adresse; break; }
    }
    if (valeurCâblé.adressePhysique < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (écrirePhysique(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int valeur = lirePhysique(BRGPHY_MII_AUXCTL);
    if (valeur < 0 || écrirePhysique(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (valeur & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (écrirePhysique(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    valeur = lirePhysique(BRGPHY_MII_SHADOW_1C);
    if (valeur < 0 || écrirePhysique(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (valeur & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (écrirePhysique(4, 0x0141) < 0 || écrirePhysique(9, 0x0200) < 0) return -1;
    return écrirePhysique(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void préparerBoucle(unsigned valeurArrièrePlan) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned valeurBoucle = valeurArrièrePlan + 0xc00 + GENET_DMA_RING_SIZE * numéroBoucle;
    for (unsigned position = 0; position <= 0x30; position += 4) registresCâblé(valeurBoucle + position) = 0;
    registresCâblé(valeurBoucle + 0x10) = (nombreÉlémentsBoucle << 16) | tailleTampon;
    registresCâblé(valeurBoucle + 0x1c) = nombreÉlémentsBoucle * GENET_DMA_DESC_SIZE / 4 - 1;
    if (valeurArrièrePlan == GENET_RX_BASE) registresCâblé(valeurBoucle + 0x28) = (5 << 16) | (nombreÉlémentsBoucle >> 4);
    else registresCâblé(valeurBoucle + 0x24) = 1;
    registresCâblé(valeurArrièrePlan + 0x104c) = 8;
    registresCâblé(valeurArrièrePlan + 0x1040) = __BIT(numéroBoucle);
}
static void adresseRéceptionEnCours(unsigned indicePosition) {
    uintptr_t adresse = (uintptr_t)valeurCâblé.recevoir[indicePosition];
    cacheMémoireNettoyer((void *)adresse, tailleTampon, 0);
    registresCâblé(GENET_RX_DESC_ADDRESS_LO(indicePosition)) = (uint32_t)adresse;
    registresCâblé(GENET_RX_DESC_ADDRESS_HI(indicePosition)) = (uint64_t)adresse >> 32;
    registresCâblé(GENET_RX_DESC_STATUS(indicePosition)) = tailleTampon << 16;
}
static err_t envoyerDatagramme(struct netif *Périphérique, struct pbuf *datagramme) {
    if (!valeurCâblé.préparer || !netif_is_link_up(Périphérique)) return ERR_RTE;
    unsigned taille = datagramme->tot_len;
    if (!taille || taille > 1536) return ERR_BUF;
    uint16_t consommerValeur = registresCâblé(GENET_TX_DMA_CONS_INDEX(numéroBoucle));
    if ((uint16_t)(valeurCâblé.valeurProduire - consommerValeur) >= nombreÉlémentsBoucle - 1) return ERR_MEM;
    unsigned indicePosition = valeurCâblé.valeurProduire % nombreÉlémentsBoucle, longueurTransmettre = taille < 60 ? 60 : taille;
    unsigned char *Données = valeurCâblé.envoyer[indicePosition];
    memset(Données, 0, longueurTransmettre);
    if (pbuf_copy_partial(datagramme, Données, taille, 0) != taille) return ERR_BUF;
    cacheMémoireNettoyer(Données, longueurTransmettre, 0);
    registresCâblé(GENET_TX_DESC_ADDRESS_LO(indicePosition)) = (uint32_t)(uintptr_t)Données;
    registresCâblé(GENET_TX_DESC_ADDRESS_HI(indicePosition)) = (uint64_t)(uintptr_t)Données >> 32;
    registresCâblé(GENET_TX_DESC_STATUS(indicePosition)) = (longueurTransmettre << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synchroniser();
    valeurCâblé.valeurProduire++;
    registresCâblé(GENET_TX_DMA_PROD_INDEX(numéroBoucle)) = valeurCâblé.valeurProduire;
    valeurCâblé.valeurStatistiques[2]++; valeurCâblé.valeurStatistiques[3] += taille;
    return ERR_OK;
}
int possèdePériphériqueCâblé(void) {
    return matérielPhysiqueCarteMatérielle() && ((registresCâblé(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t préparerRéseauCâblé(struct netif *Périphérique) {
    unsigned char adresse[6];
    if (!possèdePériphériqueCâblé() || !adresseMachineCarteMatérielle(adresse) || (adresse[0] & 1)) return ERR_IF;
    unsigned valeurSomme = 0; for (unsigned indiceOrdinal = 0; indiceOrdinal < 6; indiceOrdinal++) valeurSomme |= adresse[indiceOrdinal];
    if (!valeurSomme) return ERR_IF;
    memset(&valeurCâblé, 0, sizeof(valeurCâblé));
    registresCâblé(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    registresCâblé(GENET_RX_DMA_CTRL) = registresCâblé(GENET_TX_DMA_CTRL) = 0;
    uint32_t étatValeurInitialValeur = registresCâblé(GENET_SYS_RBUF_FLUSH_CTRL);
    registresCâblé(GENET_SYS_RBUF_FLUSH_CTRL) = étatValeurInitialValeur | GENET_SYS_RBUF_FLUSH_RESET; retardBref();
    registresCâblé(GENET_SYS_RBUF_FLUSH_CTRL) = étatValeurInitialValeur & ~GENET_SYS_RBUF_FLUSH_RESET; retardBref();
    registresCâblé(GENET_SYS_RBUF_FLUSH_CTRL) = 0; retardBref();
    registresCâblé(GENET_UMAC_CMD) = 0;
    registresCâblé(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; retardBref();
    registresCâblé(GENET_UMAC_CMD) = 0;
    registresCâblé(GENET_UMAC_MIB_CTRL) = 7;
    registresCâblé(GENET_UMAC_MIB_CTRL) = 0;
    registresCâblé(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (préparerPhysique() < 0) return ERR_IF;
    registresCâblé(GENET_UMAC_MAC0) = (uint32_t)adresse[0] << 24 | (uint32_t)adresse[1] << 16 | adresse[2] << 8 | adresse[3];
    registresCâblé(GENET_UMAC_MAC1) = adresse[4] << 8 | adresse[5];
    préparerBoucle(GENET_TX_BASE); préparerBoucle(GENET_RX_BASE);
    for (unsigned indiceOrdinal = 0; indiceOrdinal < nombreÉlémentsBoucle; indiceOrdinal++) adresseRéceptionEnCours(indiceOrdinal);
    synchroniser();
    registresCâblé(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(numéroBoucle);
    registresCâblé(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(numéroBoucle);
    registresCâblé(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    registresCâblé(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    registresCâblé(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    registresCâblé(GENET_UMAC_MDF_CTRL) = 0;
    registresCâblé(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    Périphérique->name[0] = 'e'; Périphérique->name[1] = 'n'; Périphérique->mtu = 1500;
    Périphérique->hwaddr_len = 6; memcpy(Périphérique->hwaddr, adresse, 6);
    Périphérique->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    Périphérique->output = etharp_output; Périphérique->linkoutput = envoyerDatagramme;
    valeurCâblé.préparer = 1;
    return ERR_OK;
}
void inspecterRéseauCâblé(struct netif *Périphérique) {
    if (!valeurCâblé.préparer) return;
    uintptr_t valeurMaintenant = millisecondesÉcouléesCarteMatérielle();
    if (valeurMaintenant >= valeurCâblé.vérifierÉlémentListeSuivant) {
        valeurCâblé.vérifierÉlémentListeSuivant = valeurMaintenant + 500;
        lirePhysique(BRGPHY_MII_BMSR);
        int valeurÉtatValeur = lirePhysique(BRGPHY_MII_BMSR), valeurAuxiliaire = lirePhysique(BRGPHY_MII_AUXSTS);
        unsigned modeMéthode = valeurAuxiliaire < 0 ? 0 : (valeurAuxiliaire & BRGPHY_AUXSTS_AN_RES) >> 8;
        int valeurVitesse = modeMéthode == 7 ? 1000 : modeMéthode == 5 ? 100 : modeMéthode == 2 ? 10 : 0;
        valeurCâblé.valeurVitesse = valeurÉtatValeur >= 0 && (valeurÉtatValeur & BRGPHY_BMSR_LINK) ? valeurVitesse : 0;
        if (valeurCâblé.valeurVitesse) {
            uint32_t réglages = registresCâblé(GENET_EXT_RGMII_OOB_CTRL);
            réglages &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            registresCâblé(GENET_EXT_RGMII_OOB_CTRL) = réglages | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            réglages = registresCâblé(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            registresCâblé(GENET_UMAC_CMD) = réglages | (valeurVitesse == 1000 ? GENET_UMAC_CMD_SPEED_1000 : valeurVitesse == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(Périphérique)) netif_set_link_up(Périphérique);
        } else if (netif_is_link_up(Périphérique)) netif_set_link_down(Périphérique);
    }
    uint16_t valeurProduire = registresCâblé(GENET_RX_DMA_PROD_INDEX(numéroBoucle));
    unsigned donnéesResteDivision = (uint16_t)(valeurProduire - valeurCâblé.consommerValeur);
    if (donnéesResteDivision > nombreÉlémentsBoucle) { valeurCâblé.valeurStatistiques[4]++; return; }
    for (unsigned ordinalBoucle = 0; ordinalBoucle < donnéesResteDivision && ordinalBoucle < 32; ordinalBoucle++) {
        unsigned indicePosition = valeurCâblé.consommerValeur % nombreÉlémentsBoucle;
        synchroniser();
        uint32_t valeurÉtatValeur = registresCâblé(GENET_RX_DESC_STATUS(indicePosition));
        unsigned longueur = (valeurÉtatValeur & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t valeurFrontière = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((valeurÉtatValeur & (valeurFrontière | GENET_RX_DESC_STATUS_RX_ERROR)) != valeurFrontière || longueur < 16 || longueur > 1538) valeurCâblé.valeurStatistiques[4]++;
        else {
            cacheMémoireNettoyer(valeurCâblé.recevoir[indicePosition], longueur, 1);
            struct pbuf *Données = pbuf_alloc(PBUF_RAW, longueur - 2, PBUF_POOL);
            if (!Données) valeurCâblé.valeurStatistiques[4]++;
            else if (pbuf_take(Données, valeurCâblé.recevoir[indicePosition] + 2, longueur - 2) != ERR_OK || Périphérique->input(Données, Périphérique) != ERR_OK) {
                pbuf_free(Données); valeurCâblé.valeurStatistiques[4]++;
            } else { valeurCâblé.valeurStatistiques[0]++; valeurCâblé.valeurStatistiques[1] += longueur - 2; }
        }
        adresseRéceptionEnCours(indicePosition); synchroniser(); valeurCâblé.consommerValeur++;
        registresCâblé(GENET_RX_DMA_CONS_INDEX(numéroBoucle)) = valeurCâblé.consommerValeur;
    }
}
uint32_t statistiquesRéseauCâblé(unsigned valeurEntréeÉlément) {
    return valeurEntréeÉlément < 5 ? valeurCâblé.valeurStatistiques[valeurEntréeÉlément] : valeurEntréeÉlément == 5 ? valeurCâblé.valeurVitesse : valeurEntréeÉlément == 6 ? valeurCâblé.préparer : 0;
}
