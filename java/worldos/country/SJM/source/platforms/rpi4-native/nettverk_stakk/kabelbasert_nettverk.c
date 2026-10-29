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
#include "kabelbasert_nettverk.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Tavle_absolutt_adresse(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(e_post) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (e_post)))
#endif
enum { Loop_nummer = 16, Loop_ANTALL = 256, bufre_skalere = 2048 };
static struct {
    unsigned char motta[Loop_ANTALL][bufre_skalere];
    unsigned char sende[Loop_ANTALL][bufre_skalere];
    uint16_t bruke_VERDI, 생산;
    int 물리주소, Forbered, 속도;
    uint32_t statistikk_VERDI[5];
    uintptr_t bekrefte_Neste_vare;
} kabelbasert_VERDI __attribute__((aligned(64)));

static void synkronisere(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void RENSK_bufre(void *data, unsigned lengde_VERDI, int motta) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + lengde_VERDI;
    for (uintptr_t e_post = (uintptr_t)data & ~(uintptr_t)63; e_post < 끝; e_post += 64) {
        if (motta) __asm__ volatile("dc ivac, %0" :: "r"(e_post) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(e_post) : "memory");
    }
#else
    (void)data; (void)lengde_VERDI; (void)motta;
#endif
    synkronisere();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned e_post, unsigned INDEKS, int Skriv, unsigned VERDI) {
    uint32_t Kommando = (Skriv ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (e_post << GENET_MDIO_ADDR_SHIFT) | (INDEKS << GENET_MDIO_REG_SHIFT) | (VERDI & 65535);
    유선저장기(GENET_MDIO_CMD) = Kommando;
    유선저장기(GENET_MDIO_CMD) = Kommando | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t status_VERDI = 유선저장기(GENET_MDIO_CMD);
        if (!(status_VERDI & GENET_MDIO_START_BUSY))
            return status_VERDI & GENET_MDIO_READ_FAILED ? -1 : (int)(status_VERDI & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEKS) { return 물리전송(kabelbasert_VERDI.물리주소, INDEKS, 0, 0); }
static int 물리쓰기(unsigned INDEKS, unsigned VERDI) { return 물리전송(kabelbasert_VERDI.물리주소, INDEKS, 1, VERDI); }
static int 물리준비(void) {
    kabelbasert_VERDI.물리주소 = -1;
    for (unsigned e_post = 0; e_post < 32; e_post++) {
        int 식별 = 물리전송(e_post, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { kabelbasert_VERDI.물리주소 = e_post; break; }
    }
    if (kabelbasert_VERDI.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VERDI = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VERDI < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VERDI & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VERDI = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VERDI < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VERDI & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Forbered_Loop(unsigned bakgrunn_VERDI) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VERDI = bakgrunn_VERDI + 0xc00 + GENET_DMA_RING_SIZE * Loop_nummer;
    for (unsigned Posisjon = 0; Posisjon <= 0x30; Posisjon += 4) 유선저장기(Loop_VERDI + Posisjon) = 0;
    유선저장기(Loop_VERDI + 0x10) = (Loop_ANTALL << 16) | bufre_skalere;
    유선저장기(Loop_VERDI + 0x1c) = Loop_ANTALL * GENET_DMA_DESC_SIZE / 4 - 1;
    if (bakgrunn_VERDI == GENET_RX_BASE) 유선저장기(Loop_VERDI + 0x28) = (5 << 16) | (Loop_ANTALL >> 4);
    else 유선저장기(Loop_VERDI + 0x24) = 1;
    유선저장기(bakgrunn_VERDI + 0x104c) = 8;
    유선저장기(bakgrunn_VERDI + 0x1040) = __BIT(Loop_nummer);
}
static void 받는주소(unsigned posisjonsindeks) {
    uintptr_t e_post = (uintptr_t)kabelbasert_VERDI.motta[posisjonsindeks];
    RENSK_bufre((void *)e_post, bufre_skalere, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(posisjonsindeks)) = (uint32_t)e_post;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(posisjonsindeks)) = (uint64_t)e_post >> 32;
    유선저장기(GENET_RX_DESC_STATUS(posisjonsindeks)) = bufre_skalere << 16;
}
static err_t sende_datagram(struct netif *enhet_VERDI, struct pbuf *datagram) {
    if (!kabelbasert_VERDI.Forbered || !netif_is_link_up(enhet_VERDI)) return ERR_RTE;
    unsigned Størrelse = datagram->tot_len;
    if (!Størrelse || Størrelse > 1536) return ERR_BUF;
    uint16_t bruke_VERDI = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_nummer));
    if ((uint16_t)(kabelbasert_VERDI.생산 - bruke_VERDI) >= Loop_ANTALL - 1) return ERR_MEM;
    unsigned posisjonsindeks = kabelbasert_VERDI.생산 % Loop_ANTALL, 송신길이 = Størrelse < 60 ? 60 : Størrelse;
    unsigned char *data = kabelbasert_VERDI.sende[posisjonsindeks];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(datagram, data, Størrelse, 0) != Størrelse) return ERR_BUF;
    RENSK_bufre(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(posisjonsindeks)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(posisjonsindeks)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(posisjonsindeks)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synkronisere();
    kabelbasert_VERDI.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_nummer)) = kabelbasert_VERDI.생산;
    kabelbasert_VERDI.statistikk_VERDI[2]++; kabelbasert_VERDI.statistikk_VERDI[3] += Størrelse;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Forbered_kabelbasert_nettverk(struct netif *enhet_VERDI) {
    unsigned char e_post[6];
    if (!유선장치있음() || !Tavle_absolutt_adresse(e_post) || (e_post[0] & 1)) return ERR_IF;
    unsigned SUMMER_VERDI = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUMMER_VERDI |= e_post[순번];
    if (!SUMMER_VERDI) return ERR_IF;
    memset(&kabelbasert_VERDI, 0, sizeof(kabelbasert_VERDI));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t opprinnelig_tilstand = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = opprinnelig_tilstand | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = opprinnelig_tilstand & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)e_post[0] << 24 | (uint32_t)e_post[1] << 16 | e_post[2] << 8 | e_post[3];
    유선저장기(GENET_UMAC_MAC1) = e_post[4] << 8 | e_post[5];
    Forbered_Loop(GENET_TX_BASE); Forbered_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_ANTALL; 순번++) 받는주소(순번);
    synkronisere();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_nummer);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_nummer);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    enhet_VERDI->name[0] = 'e'; enhet_VERDI->name[1] = 'n'; enhet_VERDI->mtu = 1500;
    enhet_VERDI->hwaddr_len = 6; memcpy(enhet_VERDI->hwaddr, e_post, 6);
    enhet_VERDI->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    enhet_VERDI->output = etharp_output; enhet_VERDI->linkoutput = sende_datagram;
    kabelbasert_VERDI.Forbered = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *enhet_VERDI) {
    if (!kabelbasert_VERDI.Forbered) return;
    uintptr_t NÅ_VERDI = 보드밀리초();
    if (NÅ_VERDI >= kabelbasert_VERDI.bekrefte_Neste_vare) {
        kabelbasert_VERDI.bekrefte_Neste_vare = NÅ_VERDI + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int status_VERDI = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metode_MODUS = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metode_MODUS == 7 ? 1000 : metode_MODUS == 5 ? 100 : metode_MODUS == 2 ? 10 : 0;
        kabelbasert_VERDI.속도 = status_VERDI >= 0 && (status_VERDI & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (kabelbasert_VERDI.속도) {
            uint32_t Innstillinger = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Innstillinger &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Innstillinger | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Innstillinger = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Innstillinger | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(enhet_VERDI)) netif_set_link_up(enhet_VERDI);
        } else if (netif_is_link_up(enhet_VERDI)) netif_set_link_down(enhet_VERDI);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_nummer));
    unsigned 남음 = (uint16_t)(생산 - kabelbasert_VERDI.bruke_VERDI);
    if (남음 > Loop_ANTALL) { kabelbasert_VERDI.statistikk_VERDI[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned posisjonsindeks = kabelbasert_VERDI.bruke_VERDI % Loop_ANTALL;
        synkronisere();
        uint32_t status_VERDI = 유선저장기(GENET_RX_DESC_STATUS(posisjonsindeks));
        unsigned lengde_VERDI = (status_VERDI & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t grense_VERDI = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((status_VERDI & (grense_VERDI | GENET_RX_DESC_STATUS_RX_ERROR)) != grense_VERDI || lengde_VERDI < 16 || lengde_VERDI > 1538) kabelbasert_VERDI.statistikk_VERDI[4]++;
        else {
            RENSK_bufre(kabelbasert_VERDI.motta[posisjonsindeks], lengde_VERDI, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, lengde_VERDI - 2, PBUF_POOL);
            if (!data) kabelbasert_VERDI.statistikk_VERDI[4]++;
            else if (pbuf_take(data, kabelbasert_VERDI.motta[posisjonsindeks] + 2, lengde_VERDI - 2) != ERR_OK || enhet_VERDI->input(data, enhet_VERDI) != ERR_OK) {
                pbuf_free(data); kabelbasert_VERDI.statistikk_VERDI[4]++;
            } else { kabelbasert_VERDI.statistikk_VERDI[0]++; kabelbasert_VERDI.statistikk_VERDI[1] += lengde_VERDI - 2; }
        }
        받는주소(posisjonsindeks); synkronisere(); kabelbasert_VERDI.bruke_VERDI++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_nummer)) = kabelbasert_VERDI.bruke_VERDI;
    }
}
uint32_t kabelbasert_nettverk_statistikk(unsigned oppføring_VERDI) {
    return oppføring_VERDI < 5 ? kabelbasert_VERDI.statistikk_VERDI[oppføring_VERDI] : oppføring_VERDI == 5 ? kabelbasert_VERDI.속도 : oppføring_VERDI == 6 ? kabelbasert_VERDI.Forbered : 0;
}
