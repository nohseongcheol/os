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
#include "przewodowy_sieć.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Tablica_adres_bezwzględny(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(Adres) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (Adres)))
#endif
enum { Loop_identyfikator = 16, Loop_ILE_LICZB = 256, rozmiar_buforu = 2048 };
static struct {
    unsigned char odbierać[Loop_ILE_LICZB][rozmiar_buforu];
    unsigned char wysłać[Loop_ILE_LICZB][rozmiar_buforu];
    uint16_t zużycie_WARTOŚĆ, 생산;
    int 물리주소, Przygotuj, 속도;
    uint32_t Statystyka_WARTOŚĆ[5];
    uintptr_t 다음확인;
} przewodowy_WARTOŚĆ __attribute__((aligned(64)));

static void synchronizować(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void OCZYŚĆ_bufor(void *dane, unsigned długość_WARTOŚĆ, int odbierać) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)dane + długość_WARTOŚĆ;
    for (uintptr_t Adres = (uintptr_t)dane & ~(uintptr_t)63; Adres < 끝; Adres += 64) {
        if (odbierać) __asm__ volatile("dc ivac, %0" :: "r"(Adres) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(Adres) : "memory");
    }
#else
    (void)dane; (void)długość_WARTOŚĆ; (void)odbierać;
#endif
    synchronizować();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned Adres, unsigned INDEKS, int Zapis, unsigned WARTOŚĆ) {
    uint32_t polecenie = (Zapis ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (Adres << GENET_MDIO_ADDR_SHIFT) | (INDEKS << GENET_MDIO_REG_SHIFT) | (WARTOŚĆ & 65535);
    유선저장기(GENET_MDIO_CMD) = polecenie;
    유선저장기(GENET_MDIO_CMD) = polecenie | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Stan_WARTOŚĆ = 유선저장기(GENET_MDIO_CMD);
        if (!(Stan_WARTOŚĆ & GENET_MDIO_START_BUSY))
            return Stan_WARTOŚĆ & GENET_MDIO_READ_FAILED ? -1 : (int)(Stan_WARTOŚĆ & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEKS) { return 물리전송(przewodowy_WARTOŚĆ.물리주소, INDEKS, 0, 0); }
static int 물리쓰기(unsigned INDEKS, unsigned WARTOŚĆ) { return 물리전송(przewodowy_WARTOŚĆ.물리주소, INDEKS, 1, WARTOŚĆ); }
static int 물리준비(void) {
    przewodowy_WARTOŚĆ.물리주소 = -1;
    for (unsigned Adres = 0; Adres < 32; Adres++) {
        int 식별 = 물리전송(Adres, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { przewodowy_WARTOŚĆ.물리주소 = Adres; break; }
    }
    if (przewodowy_WARTOŚĆ.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int WARTOŚĆ = 물리읽기(BRGPHY_MII_AUXCTL);
    if (WARTOŚĆ < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (WARTOŚĆ & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    WARTOŚĆ = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (WARTOŚĆ < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (WARTOŚĆ & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Przygotuj_Loop(unsigned Tło_WARTOŚĆ) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_WARTOŚĆ = Tło_WARTOŚĆ + 0xc00 + GENET_DMA_RING_SIZE * Loop_identyfikator;
    for (unsigned pozycja = 0; pozycja <= 0x30; pozycja += 4) 유선저장기(Loop_WARTOŚĆ + pozycja) = 0;
    유선저장기(Loop_WARTOŚĆ + 0x10) = (Loop_ILE_LICZB << 16) | rozmiar_buforu;
    유선저장기(Loop_WARTOŚĆ + 0x1c) = Loop_ILE_LICZB * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Tło_WARTOŚĆ == GENET_RX_BASE) 유선저장기(Loop_WARTOŚĆ + 0x28) = (5 << 16) | (Loop_ILE_LICZB >> 4);
    else 유선저장기(Loop_WARTOŚĆ + 0x24) = 1;
    유선저장기(Tło_WARTOŚĆ + 0x104c) = 8;
    유선저장기(Tło_WARTOŚĆ + 0x1040) = __BIT(Loop_identyfikator);
}
static void 받는주소(unsigned indeks_pozycji) {
    uintptr_t Adres = (uintptr_t)przewodowy_WARTOŚĆ.odbierać[indeks_pozycji];
    OCZYŚĆ_bufor((void *)Adres, rozmiar_buforu, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(indeks_pozycji)) = (uint32_t)Adres;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(indeks_pozycji)) = (uint64_t)Adres >> 32;
    유선저장기(GENET_RX_DESC_STATUS(indeks_pozycji)) = rozmiar_buforu << 16;
}
static err_t wysłać_datagram(struct netif *urządzenie_WARTOŚĆ, struct pbuf *datagram) {
    if (!przewodowy_WARTOŚĆ.Przygotuj || !netif_is_link_up(urządzenie_WARTOŚĆ)) return ERR_RTE;
    unsigned Rozmiar = datagram->tot_len;
    if (!Rozmiar || Rozmiar > 1536) return ERR_BUF;
    uint16_t zużycie_WARTOŚĆ = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_identyfikator));
    if ((uint16_t)(przewodowy_WARTOŚĆ.생산 - zużycie_WARTOŚĆ) >= Loop_ILE_LICZB - 1) return ERR_MEM;
    unsigned indeks_pozycji = przewodowy_WARTOŚĆ.생산 % Loop_ILE_LICZB, 송신길이 = Rozmiar < 60 ? 60 : Rozmiar;
    unsigned char *dane = przewodowy_WARTOŚĆ.wysłać[indeks_pozycji];
    memset(dane, 0, 송신길이);
    if (pbuf_copy_partial(datagram, dane, Rozmiar, 0) != Rozmiar) return ERR_BUF;
    OCZYŚĆ_bufor(dane, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(indeks_pozycji)) = (uint32_t)(uintptr_t)dane;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(indeks_pozycji)) = (uint64_t)(uintptr_t)dane >> 32;
    유선저장기(GENET_TX_DESC_STATUS(indeks_pozycji)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synchronizować();
    przewodowy_WARTOŚĆ.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_identyfikator)) = przewodowy_WARTOŚĆ.생산;
    przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[2]++; przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[3] += Rozmiar;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Przygotuj_przewodowy_sieć(struct netif *urządzenie_WARTOŚĆ) {
    unsigned char Adres[6];
    if (!유선장치있음() || !Tablica_adres_bezwzględny(Adres) || (Adres[0] & 1)) return ERR_IF;
    unsigned SUMA_WARTOŚĆ = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUMA_WARTOŚĆ |= Adres[순번];
    if (!SUMA_WARTOŚĆ) return ERR_IF;
    memset(&przewodowy_WARTOŚĆ, 0, sizeof(przewodowy_WARTOŚĆ));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t stan_początkowy = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = stan_początkowy | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = stan_początkowy & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)Adres[0] << 24 | (uint32_t)Adres[1] << 16 | Adres[2] << 8 | Adres[3];
    유선저장기(GENET_UMAC_MAC1) = Adres[4] << 8 | Adres[5];
    Przygotuj_Loop(GENET_TX_BASE); Przygotuj_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_ILE_LICZB; 순번++) 받는주소(순번);
    synchronizować();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_identyfikator);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_identyfikator);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    urządzenie_WARTOŚĆ->name[0] = 'e'; urządzenie_WARTOŚĆ->name[1] = 'n'; urządzenie_WARTOŚĆ->mtu = 1500;
    urządzenie_WARTOŚĆ->hwaddr_len = 6; memcpy(urządzenie_WARTOŚĆ->hwaddr, Adres, 6);
    urządzenie_WARTOŚĆ->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    urządzenie_WARTOŚĆ->output = etharp_output; urządzenie_WARTOŚĆ->linkoutput = wysłać_datagram;
    przewodowy_WARTOŚĆ.Przygotuj = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *urządzenie_WARTOŚĆ) {
    if (!przewodowy_WARTOŚĆ.Przygotuj) return;
    uintptr_t TERAZ_WARTOŚĆ = 보드밀리초();
    if (TERAZ_WARTOŚĆ >= przewodowy_WARTOŚĆ.다음확인) {
        przewodowy_WARTOŚĆ.다음확인 = TERAZ_WARTOŚĆ + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Stan_WARTOŚĆ = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metoda_tryb = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metoda_tryb == 7 ? 1000 : metoda_tryb == 5 ? 100 : metoda_tryb == 2 ? 10 : 0;
        przewodowy_WARTOŚĆ.속도 = Stan_WARTOŚĆ >= 0 && (Stan_WARTOŚĆ & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (przewodowy_WARTOŚĆ.속도) {
            uint32_t Ustawienia = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Ustawienia &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Ustawienia | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Ustawienia = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Ustawienia | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(urządzenie_WARTOŚĆ)) netif_set_link_up(urządzenie_WARTOŚĆ);
        } else if (netif_is_link_up(urządzenie_WARTOŚĆ)) netif_set_link_down(urządzenie_WARTOŚĆ);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_identyfikator));
    unsigned 남음 = (uint16_t)(생산 - przewodowy_WARTOŚĆ.zużycie_WARTOŚĆ);
    if (남음 > Loop_ILE_LICZB) { przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned indeks_pozycji = przewodowy_WARTOŚĆ.zużycie_WARTOŚĆ % Loop_ILE_LICZB;
        synchronizować();
        uint32_t Stan_WARTOŚĆ = 유선저장기(GENET_RX_DESC_STATUS(indeks_pozycji));
        unsigned długość_WARTOŚĆ = (Stan_WARTOŚĆ & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t granica_WARTOŚĆ = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Stan_WARTOŚĆ & (granica_WARTOŚĆ | GENET_RX_DESC_STATUS_RX_ERROR)) != granica_WARTOŚĆ || długość_WARTOŚĆ < 16 || długość_WARTOŚĆ > 1538) przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[4]++;
        else {
            OCZYŚĆ_bufor(przewodowy_WARTOŚĆ.odbierać[indeks_pozycji], długość_WARTOŚĆ, 1);
            struct pbuf *dane = pbuf_alloc(PBUF_RAW, długość_WARTOŚĆ - 2, PBUF_POOL);
            if (!dane) przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[4]++;
            else if (pbuf_take(dane, przewodowy_WARTOŚĆ.odbierać[indeks_pozycji] + 2, długość_WARTOŚĆ - 2) != ERR_OK || urządzenie_WARTOŚĆ->input(dane, urządzenie_WARTOŚĆ) != ERR_OK) {
                pbuf_free(dane); przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[4]++;
            } else { przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[0]++; przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[1] += długość_WARTOŚĆ - 2; }
        }
        받는주소(indeks_pozycji); synchronizować(); przewodowy_WARTOŚĆ.zużycie_WARTOŚĆ++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_identyfikator)) = przewodowy_WARTOŚĆ.zużycie_WARTOŚĆ;
    }
}
uint32_t przewodowy_sieć_Statystyka(unsigned wpis_WARTOŚĆ) {
    return wpis_WARTOŚĆ < 5 ? przewodowy_WARTOŚĆ.Statystyka_WARTOŚĆ[wpis_WARTOŚĆ] : wpis_WARTOŚĆ == 5 ? przewodowy_WARTOŚĆ.속도 : wpis_WARTOŚĆ == 6 ? przewodowy_WARTOŚĆ.Przygotuj : 0;
}
