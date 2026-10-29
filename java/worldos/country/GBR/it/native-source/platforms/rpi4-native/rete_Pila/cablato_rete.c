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
#include "cablato_rete.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int scheda_fisico_hardware(void);
extern int scheda_indirizzo_reale(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(e_mail) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (e_mail)))
#endif
enum { Loop_numero = 16, Loop_CONTA_NUMERI = 256, dimensioni_del_buffer = 2048 };
static struct {
    unsigned char ricevere[Loop_CONTA_NUMERI][dimensioni_del_buffer];
    unsigned char inviare[Loop_CONTA_NUMERI][dimensioni_del_buffer];
    uint16_t consumo_VALORE, 생산;
    int fisico_e_mail, Prepara, 속도;
    uint32_t Statistiche_VALORE[5];
    uintptr_t verificare_Avanti_articolo;
} cablato_VALORE __attribute__((aligned(64)));

static void sincronizzare(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void LIBERA_cache(void *dati, unsigned durata_VALORE, int ricevere) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)dati + durata_VALORE;
    for (uintptr_t e_mail = (uintptr_t)dati & ~(uintptr_t)63; e_mail < 끝; e_mail += 64) {
        if (ricevere) __asm__ volatile("dc ivac, %0" :: "r"(e_mail) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(e_mail) : "memory");
    }
#else
    (void)dati; (void)durata_VALORE; (void)ricevere;
#endif
    sincronizzare();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int fisico_trasferire(unsigned e_mail, unsigned INDICE, int Scrittura, unsigned VALORE) {
    uint32_t comando = (Scrittura ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (e_mail << GENET_MDIO_ADDR_SHIFT) | (INDICE << GENET_MDIO_REG_SHIFT) | (VALORE & 65535);
    유선저장기(GENET_MDIO_CMD) = comando;
    유선저장기(GENET_MDIO_CMD) = comando | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Stato_VALORE = 유선저장기(GENET_MDIO_CMD);
        if (!(Stato_VALORE & GENET_MDIO_START_BUSY))
            return Stato_VALORE & GENET_MDIO_READ_FAILED ? -1 : (int)(Stato_VALORE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDICE) { return fisico_trasferire(cablato_VALORE.fisico_e_mail, INDICE, 0, 0); }
static int scrivere_fisico(unsigned INDICE, unsigned VALORE) { return fisico_trasferire(cablato_VALORE.fisico_e_mail, INDICE, 1, VALORE); }
static int Prepara_fisico(void) {
    cablato_VALORE.fisico_e_mail = -1;
    for (unsigned e_mail = 0; e_mail < 32; e_mail++) {
        int 식별 = fisico_trasferire(e_mail, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { cablato_VALORE.fisico_e_mail = e_mail; break; }
    }
    if (cablato_VALORE.fisico_e_mail < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (scrivere_fisico(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VALORE = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VALORE < 0 || scrivere_fisico(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VALORE & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (scrivere_fisico(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VALORE = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VALORE < 0 || scrivere_fisico(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VALORE & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (scrivere_fisico(4, 0x0141) < 0 || scrivere_fisico(9, 0x0200) < 0) return -1;
    return scrivere_fisico(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Prepara_Loop(unsigned sfondo_VALORE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALORE = sfondo_VALORE + 0xc00 + GENET_DMA_RING_SIZE * Loop_numero;
    for (unsigned posizione = 0; posizione <= 0x30; posizione += 4) 유선저장기(Loop_VALORE + posizione) = 0;
    유선저장기(Loop_VALORE + 0x10) = (Loop_CONTA_NUMERI << 16) | dimensioni_del_buffer;
    유선저장기(Loop_VALORE + 0x1c) = Loop_CONTA_NUMERI * GENET_DMA_DESC_SIZE / 4 - 1;
    if (sfondo_VALORE == GENET_RX_BASE) 유선저장기(Loop_VALORE + 0x28) = (5 << 16) | (Loop_CONTA_NUMERI >> 4);
    else 유선저장기(Loop_VALORE + 0x24) = 1;
    유선저장기(sfondo_VALORE + 0x104c) = 8;
    유선저장기(sfondo_VALORE + 0x1040) = __BIT(Loop_numero);
}
static void 받는주소(unsigned funzione_INDICE) {
    uintptr_t e_mail = (uintptr_t)cablato_VALORE.ricevere[funzione_INDICE];
    LIBERA_cache((void *)e_mail, dimensioni_del_buffer, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(funzione_INDICE)) = (uint32_t)e_mail;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(funzione_INDICE)) = (uint64_t)e_mail >> 32;
    유선저장기(GENET_RX_DESC_STATUS(funzione_INDICE)) = dimensioni_del_buffer << 16;
}
static err_t inviare_datagramma(struct netif *cellulare_VALORE, struct pbuf *datagramma) {
    if (!cablato_VALORE.Prepara || !netif_is_link_up(cellulare_VALORE)) return ERR_RTE;
    unsigned Dimensione = datagramma->tot_len;
    if (!Dimensione || Dimensione > 1536) return ERR_BUF;
    uint16_t consumo_VALORE = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_numero));
    if ((uint16_t)(cablato_VALORE.생산 - consumo_VALORE) >= Loop_CONTA_NUMERI - 1) return ERR_MEM;
    unsigned funzione_INDICE = cablato_VALORE.생산 % Loop_CONTA_NUMERI, trasmettere_durata = Dimensione < 60 ? 60 : Dimensione;
    unsigned char *dati = cablato_VALORE.inviare[funzione_INDICE];
    memset(dati, 0, trasmettere_durata);
    if (pbuf_copy_partial(datagramma, dati, Dimensione, 0) != Dimensione) return ERR_BUF;
    LIBERA_cache(dati, trasmettere_durata, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(funzione_INDICE)) = (uint32_t)(uintptr_t)dati;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(funzione_INDICE)) = (uint64_t)(uintptr_t)dati >> 32;
    유선저장기(GENET_TX_DESC_STATUS(funzione_INDICE)) = (trasmettere_durata << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sincronizzare();
    cablato_VALORE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_numero)) = cablato_VALORE.생산;
    cablato_VALORE.Statistiche_VALORE[2]++; cablato_VALORE.Statistiche_VALORE[3] += Dimensione;
    return ERR_OK;
}
int 유선장치있음(void) {
    return scheda_fisico_hardware() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Prepara_cablato_rete(struct netif *cellulare_VALORE) {
    unsigned char e_mail[6];
    if (!유선장치있음() || !scheda_indirizzo_reale(e_mail) || (e_mail[0] & 1)) return ERR_IF;
    unsigned SUM_VALORE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALORE |= e_mail[순번];
    if (!SUM_VALORE) return ERR_IF;
    memset(&cablato_VALORE, 0, sizeof(cablato_VALORE));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t stato_iniziale = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = stato_iniziale | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = stato_iniziale & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (Prepara_fisico() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)e_mail[0] << 24 | (uint32_t)e_mail[1] << 16 | e_mail[2] << 8 | e_mail[3];
    유선저장기(GENET_UMAC_MAC1) = e_mail[4] << 8 | e_mail[5];
    Prepara_Loop(GENET_TX_BASE); Prepara_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_CONTA_NUMERI; 순번++) 받는주소(순번);
    sincronizzare();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_numero);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_numero);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    cellulare_VALORE->name[0] = 'e'; cellulare_VALORE->name[1] = 'n'; cellulare_VALORE->mtu = 1500;
    cellulare_VALORE->hwaddr_len = 6; memcpy(cellulare_VALORE->hwaddr, e_mail, 6);
    cellulare_VALORE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    cellulare_VALORE->output = etharp_output; cellulare_VALORE->linkoutput = inviare_datagramma;
    cablato_VALORE.Prepara = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *cellulare_VALORE) {
    if (!cablato_VALORE.Prepara) return;
    uintptr_t ADESSO_VALORE = 보드밀리초();
    if (ADESSO_VALORE >= cablato_VALORE.verificare_Avanti_articolo) {
        cablato_VALORE.verificare_Avanti_articolo = ADESSO_VALORE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Stato_VALORE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metodo_MODA = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metodo_MODA == 7 ? 1000 : metodo_MODA == 5 ? 100 : metodo_MODA == 2 ? 10 : 0;
        cablato_VALORE.속도 = Stato_VALORE >= 0 && (Stato_VALORE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (cablato_VALORE.속도) {
            uint32_t Impostazioni = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Impostazioni &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Impostazioni | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Impostazioni = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Impostazioni | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(cellulare_VALORE)) netif_set_link_up(cellulare_VALORE);
        } else if (netif_is_link_up(cellulare_VALORE)) netif_set_link_down(cellulare_VALORE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_numero));
    unsigned 남음 = (uint16_t)(생산 - cablato_VALORE.consumo_VALORE);
    if (남음 > Loop_CONTA_NUMERI) { cablato_VALORE.Statistiche_VALORE[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned funzione_INDICE = cablato_VALORE.consumo_VALORE % Loop_CONTA_NUMERI;
        sincronizzare();
        uint32_t Stato_VALORE = 유선저장기(GENET_RX_DESC_STATUS(funzione_INDICE));
        unsigned durata_VALORE = (Stato_VALORE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t limite_VALORE = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Stato_VALORE & (limite_VALORE | GENET_RX_DESC_STATUS_RX_ERROR)) != limite_VALORE || durata_VALORE < 16 || durata_VALORE > 1538) cablato_VALORE.Statistiche_VALORE[4]++;
        else {
            LIBERA_cache(cablato_VALORE.ricevere[funzione_INDICE], durata_VALORE, 1);
            struct pbuf *dati = pbuf_alloc(PBUF_RAW, durata_VALORE - 2, PBUF_POOL);
            if (!dati) cablato_VALORE.Statistiche_VALORE[4]++;
            else if (pbuf_take(dati, cablato_VALORE.ricevere[funzione_INDICE] + 2, durata_VALORE - 2) != ERR_OK || cellulare_VALORE->input(dati, cellulare_VALORE) != ERR_OK) {
                pbuf_free(dati); cablato_VALORE.Statistiche_VALORE[4]++;
            } else { cablato_VALORE.Statistiche_VALORE[0]++; cablato_VALORE.Statistiche_VALORE[1] += durata_VALORE - 2; }
        }
        받는주소(funzione_INDICE); sincronizzare(); cablato_VALORE.consumo_VALORE++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_numero)) = cablato_VALORE.consumo_VALORE;
    }
}
uint32_t cablato_rete_Statistiche(unsigned voce_VALORE) {
    return voce_VALORE < 5 ? cablato_VALORE.Statistiche_VALORE[voce_VALORE] : voce_VALORE == 5 ? cablato_VALORE.속도 : voce_VALORE == 6 ? cablato_VALORE.Prepara : 0;
}
