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
#include "lanka_verkko.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Taulu_absoluuttinen_osoite(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(OSOITE) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (OSOITE)))
#endif
enum { Loop_numero = 16, Loop_LASKE = 256, puskurin_koko = 2048 };
static struct {
    unsigned char saada[Loop_LASKE][puskurin_koko];
    unsigned char lähettää[Loop_LASKE][puskurin_koko];
    uint16_t käyttää_ARVO, 생산;
    int 물리주소, Valmistele, 속도;
    uint32_t Tilastotiedot_ARVO[5];
    uintptr_t tarkistaa_Seuraava_kohde;
} lanka_ARVO __attribute__((aligned(64)));

static void synkronoi(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void SIIVOA_välimuisti(void *data, unsigned kesto_ARVO, int saada) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + kesto_ARVO;
    for (uintptr_t OSOITE = (uintptr_t)data & ~(uintptr_t)63; OSOITE < 끝; OSOITE += 64) {
        if (saada) __asm__ volatile("dc ivac, %0" :: "r"(OSOITE) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(OSOITE) : "memory");
    }
#else
    (void)data; (void)kesto_ARVO; (void)saada;
#endif
    synkronoi();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned OSOITE, unsigned INDEKSI, int Kirjoitus, unsigned ARVO) {
    uint32_t komento = (Kirjoitus ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (OSOITE << GENET_MDIO_ADDR_SHIFT) | (INDEKSI << GENET_MDIO_REG_SHIFT) | (ARVO & 65535);
    유선저장기(GENET_MDIO_CMD) = komento;
    유선저장기(GENET_MDIO_CMD) = komento | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Tila_ARVO = 유선저장기(GENET_MDIO_CMD);
        if (!(Tila_ARVO & GENET_MDIO_START_BUSY))
            return Tila_ARVO & GENET_MDIO_READ_FAILED ? -1 : (int)(Tila_ARVO & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEKSI) { return 물리전송(lanka_ARVO.물리주소, INDEKSI, 0, 0); }
static int 물리쓰기(unsigned INDEKSI, unsigned ARVO) { return 물리전송(lanka_ARVO.물리주소, INDEKSI, 1, ARVO); }
static int 물리준비(void) {
    lanka_ARVO.물리주소 = -1;
    for (unsigned OSOITE = 0; OSOITE < 32; OSOITE++) {
        int 식별 = 물리전송(OSOITE, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { lanka_ARVO.물리주소 = OSOITE; break; }
    }
    if (lanka_ARVO.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ARVO = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ARVO < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ARVO & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ARVO = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ARVO < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ARVO & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Valmistele_Loop(unsigned Tausta_ARVO) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_ARVO = Tausta_ARVO + 0xc00 + GENET_DMA_RING_SIZE * Loop_numero;
    for (unsigned paikka = 0; paikka <= 0x30; paikka += 4) 유선저장기(Loop_ARVO + paikka) = 0;
    유선저장기(Loop_ARVO + 0x10) = (Loop_LASKE << 16) | puskurin_koko;
    유선저장기(Loop_ARVO + 0x1c) = Loop_LASKE * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Tausta_ARVO == GENET_RX_BASE) 유선저장기(Loop_ARVO + 0x28) = (5 << 16) | (Loop_LASKE >> 4);
    else 유선저장기(Loop_ARVO + 0x24) = 1;
    유선저장기(Tausta_ARVO + 0x104c) = 8;
    유선저장기(Tausta_ARVO + 0x1040) = __BIT(Loop_numero);
}
static void 받는주소(unsigned sijainti) {
    uintptr_t OSOITE = (uintptr_t)lanka_ARVO.saada[sijainti];
    SIIVOA_välimuisti((void *)OSOITE, puskurin_koko, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(sijainti)) = (uint32_t)OSOITE;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(sijainti)) = (uint64_t)OSOITE >> 32;
    유선저장기(GENET_RX_DESC_STATUS(sijainti)) = puskurin_koko << 16;
}
static err_t lähettää_datagrammi(struct netif *laite_ARVO, struct pbuf *datagrammi) {
    if (!lanka_ARVO.Valmistele || !netif_is_link_up(laite_ARVO)) return ERR_RTE;
    unsigned Koko = datagrammi->tot_len;
    if (!Koko || Koko > 1536) return ERR_BUF;
    uint16_t käyttää_ARVO = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_numero));
    if ((uint16_t)(lanka_ARVO.생산 - käyttää_ARVO) >= Loop_LASKE - 1) return ERR_MEM;
    unsigned sijainti = lanka_ARVO.생산 % Loop_LASKE, lähettää_kesto = Koko < 60 ? 60 : Koko;
    unsigned char *data = lanka_ARVO.lähettää[sijainti];
    memset(data, 0, lähettää_kesto);
    if (pbuf_copy_partial(datagrammi, data, Koko, 0) != Koko) return ERR_BUF;
    SIIVOA_välimuisti(data, lähettää_kesto, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(sijainti)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(sijainti)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(sijainti)) = (lähettää_kesto << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synkronoi();
    lanka_ARVO.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_numero)) = lanka_ARVO.생산;
    lanka_ARVO.Tilastotiedot_ARVO[2]++; lanka_ARVO.Tilastotiedot_ARVO[3] += Koko;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Valmistele_lanka_verkko(struct netif *laite_ARVO) {
    unsigned char OSOITE[6];
    if (!유선장치있음() || !Taulu_absoluuttinen_osoite(OSOITE) || (OSOITE[0] & 1)) return ERR_IF;
    unsigned SUM_ARVO = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_ARVO |= OSOITE[순번];
    if (!SUM_ARVO) return ERR_IF;
    memset(&lanka_ARVO, 0, sizeof(lanka_ARVO));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t alkutila = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = alkutila | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = alkutila & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)OSOITE[0] << 24 | (uint32_t)OSOITE[1] << 16 | OSOITE[2] << 8 | OSOITE[3];
    유선저장기(GENET_UMAC_MAC1) = OSOITE[4] << 8 | OSOITE[5];
    Valmistele_Loop(GENET_TX_BASE); Valmistele_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_LASKE; 순번++) 받는주소(순번);
    synkronoi();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_numero);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_numero);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    laite_ARVO->name[0] = 'e'; laite_ARVO->name[1] = 'n'; laite_ARVO->mtu = 1500;
    laite_ARVO->hwaddr_len = 6; memcpy(laite_ARVO->hwaddr, OSOITE, 6);
    laite_ARVO->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    laite_ARVO->output = etharp_output; laite_ARVO->linkoutput = lähettää_datagrammi;
    lanka_ARVO.Valmistele = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *laite_ARVO) {
    if (!lanka_ARVO.Valmistele) return;
    uintptr_t NYT_ARVO = 보드밀리초();
    if (NYT_ARVO >= lanka_ARVO.tarkistaa_Seuraava_kohde) {
        lanka_ARVO.tarkistaa_Seuraava_kohde = NYT_ARVO + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Tila_ARVO = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned menetelmä_tila = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = menetelmä_tila == 7 ? 1000 : menetelmä_tila == 5 ? 100 : menetelmä_tila == 2 ? 10 : 0;
        lanka_ARVO.속도 = Tila_ARVO >= 0 && (Tila_ARVO & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (lanka_ARVO.속도) {
            uint32_t Asetukset = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Asetukset &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Asetukset | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Asetukset = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Asetukset | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(laite_ARVO)) netif_set_link_up(laite_ARVO);
        } else if (netif_is_link_up(laite_ARVO)) netif_set_link_down(laite_ARVO);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_numero));
    unsigned 남음 = (uint16_t)(생산 - lanka_ARVO.käyttää_ARVO);
    if (남음 > Loop_LASKE) { lanka_ARVO.Tilastotiedot_ARVO[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned sijainti = lanka_ARVO.käyttää_ARVO % Loop_LASKE;
        synkronoi();
        uint32_t Tila_ARVO = 유선저장기(GENET_RX_DESC_STATUS(sijainti));
        unsigned kesto_ARVO = (Tila_ARVO & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t rajattu_alue_ARVO = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Tila_ARVO & (rajattu_alue_ARVO | GENET_RX_DESC_STATUS_RX_ERROR)) != rajattu_alue_ARVO || kesto_ARVO < 16 || kesto_ARVO > 1538) lanka_ARVO.Tilastotiedot_ARVO[4]++;
        else {
            SIIVOA_välimuisti(lanka_ARVO.saada[sijainti], kesto_ARVO, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, kesto_ARVO - 2, PBUF_POOL);
            if (!data) lanka_ARVO.Tilastotiedot_ARVO[4]++;
            else if (pbuf_take(data, lanka_ARVO.saada[sijainti] + 2, kesto_ARVO - 2) != ERR_OK || laite_ARVO->input(data, laite_ARVO) != ERR_OK) {
                pbuf_free(data); lanka_ARVO.Tilastotiedot_ARVO[4]++;
            } else { lanka_ARVO.Tilastotiedot_ARVO[0]++; lanka_ARVO.Tilastotiedot_ARVO[1] += kesto_ARVO - 2; }
        }
        받는주소(sijainti); synkronoi(); lanka_ARVO.käyttää_ARVO++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_numero)) = lanka_ARVO.käyttää_ARVO;
    }
}
uint32_t lanka_verkko_Tilastotiedot(unsigned merkintä_ARVO_962f286b) {
    return merkintä_ARVO_962f286b < 5 ? lanka_ARVO.Tilastotiedot_ARVO[merkintä_ARVO_962f286b] : merkintä_ARVO_962f286b == 5 ? lanka_ARVO.속도 : merkintä_ARVO_962f286b == 6 ? lanka_ARVO.Valmistele : 0;
}
