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
#include "traditionel_netværk.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Tavle_absolut_adresse(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(mail) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (mail)))
#endif
enum { Loop_tal = 16, Loop_TÆL = 256, bufferstørrelse = 2048 };
static struct {
    unsigned char modtage[Loop_TÆL][bufferstørrelse];
    unsigned char maile[Loop_TÆL][bufferstørrelse];
    uint16_t bruge_VÆRDI, 생산;
    int 물리주소, Tilrettelæg, 속도;
    uint32_t Statistik_VÆRDI[5];
    uintptr_t bekræfte_Næste_vare;
} traditionel_VÆRDI __attribute__((aligned(64)));

static void synkronisere(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void Ren_cache(void *data, unsigned varighed_VÆRDI, int modtage) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)data + varighed_VÆRDI;
    for (uintptr_t mail = (uintptr_t)data & ~(uintptr_t)63; mail < 끝; mail += 64) {
        if (modtage) __asm__ volatile("dc ivac, %0" :: "r"(mail) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(mail) : "memory");
    }
#else
    (void)data; (void)varighed_VÆRDI; (void)modtage;
#endif
    synkronisere();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned mail, unsigned INDEKS, int Skrive, unsigned VÆRDI) {
    uint32_t Kommando = (Skrive ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (mail << GENET_MDIO_ADDR_SHIFT) | (INDEKS << GENET_MDIO_REG_SHIFT) | (VÆRDI & 65535);
    유선저장기(GENET_MDIO_CMD) = Kommando;
    유선저장기(GENET_MDIO_CMD) = Kommando | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t status_VÆRDI = 유선저장기(GENET_MDIO_CMD);
        if (!(status_VÆRDI & GENET_MDIO_START_BUSY))
            return status_VÆRDI & GENET_MDIO_READ_FAILED ? -1 : (int)(status_VÆRDI & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEKS) { return 물리전송(traditionel_VÆRDI.물리주소, INDEKS, 0, 0); }
static int 물리쓰기(unsigned INDEKS, unsigned VÆRDI) { return 물리전송(traditionel_VÆRDI.물리주소, INDEKS, 1, VÆRDI); }
static int 물리준비(void) {
    traditionel_VÆRDI.물리주소 = -1;
    for (unsigned mail = 0; mail < 32; mail++) {
        int 식별 = 물리전송(mail, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { traditionel_VÆRDI.물리주소 = mail; break; }
    }
    if (traditionel_VÆRDI.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VÆRDI = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VÆRDI < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VÆRDI & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VÆRDI = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VÆRDI < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VÆRDI & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Tilrettelæg_Loop(unsigned Baggrund_VÆRDI) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VÆRDI = Baggrund_VÆRDI + 0xc00 + GENET_DMA_RING_SIZE * Loop_tal;
    for (unsigned Placering = 0; Placering <= 0x30; Placering += 4) 유선저장기(Loop_VÆRDI + Placering) = 0;
    유선저장기(Loop_VÆRDI + 0x10) = (Loop_TÆL << 16) | bufferstørrelse;
    유선저장기(Loop_VÆRDI + 0x1c) = Loop_TÆL * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Baggrund_VÆRDI == GENET_RX_BASE) 유선저장기(Loop_VÆRDI + 0x28) = (5 << 16) | (Loop_TÆL >> 4);
    else 유선저장기(Loop_VÆRDI + 0x24) = 1;
    유선저장기(Baggrund_VÆRDI + 0x104c) = 8;
    유선저장기(Baggrund_VÆRDI + 0x1040) = __BIT(Loop_tal);
}
static void 받는주소(unsigned positionsindeks) {
    uintptr_t mail = (uintptr_t)traditionel_VÆRDI.modtage[positionsindeks];
    Ren_cache((void *)mail, bufferstørrelse, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(positionsindeks)) = (uint32_t)mail;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(positionsindeks)) = (uint64_t)mail >> 32;
    유선저장기(GENET_RX_DESC_STATUS(positionsindeks)) = bufferstørrelse << 16;
}
static err_t maile_datagram(struct netif *enhed_VÆRDI, struct pbuf *datagram) {
    if (!traditionel_VÆRDI.Tilrettelæg || !netif_is_link_up(enhed_VÆRDI)) return ERR_RTE;
    unsigned Størrelse = datagram->tot_len;
    if (!Størrelse || Størrelse > 1536) return ERR_BUF;
    uint16_t bruge_VÆRDI = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_tal));
    if ((uint16_t)(traditionel_VÆRDI.생산 - bruge_VÆRDI) >= Loop_TÆL - 1) return ERR_MEM;
    unsigned positionsindeks = traditionel_VÆRDI.생산 % Loop_TÆL, 송신길이 = Størrelse < 60 ? 60 : Størrelse;
    unsigned char *data = traditionel_VÆRDI.maile[positionsindeks];
    memset(data, 0, 송신길이);
    if (pbuf_copy_partial(datagram, data, Størrelse, 0) != Størrelse) return ERR_BUF;
    Ren_cache(data, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(positionsindeks)) = (uint32_t)(uintptr_t)data;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(positionsindeks)) = (uint64_t)(uintptr_t)data >> 32;
    유선저장기(GENET_TX_DESC_STATUS(positionsindeks)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synkronisere();
    traditionel_VÆRDI.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_tal)) = traditionel_VÆRDI.생산;
    traditionel_VÆRDI.Statistik_VÆRDI[2]++; traditionel_VÆRDI.Statistik_VÆRDI[3] += Størrelse;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Tilrettelæg_traditionel_netværk(struct netif *enhed_VÆRDI) {
    unsigned char mail[6];
    if (!유선장치있음() || !Tavle_absolut_adresse(mail) || (mail[0] & 1)) return ERR_IF;
    unsigned SUM_VÆRDI = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VÆRDI |= mail[순번];
    if (!SUM_VÆRDI) return ERR_IF;
    memset(&traditionel_VÆRDI, 0, sizeof(traditionel_VÆRDI));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t starttilstand = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = starttilstand | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = starttilstand & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)mail[0] << 24 | (uint32_t)mail[1] << 16 | mail[2] << 8 | mail[3];
    유선저장기(GENET_UMAC_MAC1) = mail[4] << 8 | mail[5];
    Tilrettelæg_Loop(GENET_TX_BASE); Tilrettelæg_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_TÆL; 순번++) 받는주소(순번);
    synkronisere();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_tal);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_tal);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    enhed_VÆRDI->name[0] = 'e'; enhed_VÆRDI->name[1] = 'n'; enhed_VÆRDI->mtu = 1500;
    enhed_VÆRDI->hwaddr_len = 6; memcpy(enhed_VÆRDI->hwaddr, mail, 6);
    enhed_VÆRDI->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    enhed_VÆRDI->output = etharp_output; enhed_VÆRDI->linkoutput = maile_datagram;
    traditionel_VÆRDI.Tilrettelæg = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *enhed_VÆRDI) {
    if (!traditionel_VÆRDI.Tilrettelæg) return;
    uintptr_t NU_VÆRDI = 보드밀리초();
    if (NU_VÆRDI >= traditionel_VÆRDI.bekræfte_Næste_vare) {
        traditionel_VÆRDI.bekræfte_Næste_vare = NU_VÆRDI + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int status_VÆRDI = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metode_HYPPIGST = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metode_HYPPIGST == 7 ? 1000 : metode_HYPPIGST == 5 ? 100 : metode_HYPPIGST == 2 ? 10 : 0;
        traditionel_VÆRDI.속도 = status_VÆRDI >= 0 && (status_VÆRDI & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (traditionel_VÆRDI.속도) {
            uint32_t Indstillinger = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Indstillinger &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Indstillinger | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Indstillinger = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Indstillinger | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(enhed_VÆRDI)) netif_set_link_up(enhed_VÆRDI);
        } else if (netif_is_link_up(enhed_VÆRDI)) netif_set_link_down(enhed_VÆRDI);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_tal));
    unsigned 남음 = (uint16_t)(생산 - traditionel_VÆRDI.bruge_VÆRDI);
    if (남음 > Loop_TÆL) { traditionel_VÆRDI.Statistik_VÆRDI[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned positionsindeks = traditionel_VÆRDI.bruge_VÆRDI % Loop_TÆL;
        synkronisere();
        uint32_t status_VÆRDI = 유선저장기(GENET_RX_DESC_STATUS(positionsindeks));
        unsigned varighed_VÆRDI = (status_VÆRDI & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t grænse_VÆRDI = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((status_VÆRDI & (grænse_VÆRDI | GENET_RX_DESC_STATUS_RX_ERROR)) != grænse_VÆRDI || varighed_VÆRDI < 16 || varighed_VÆRDI > 1538) traditionel_VÆRDI.Statistik_VÆRDI[4]++;
        else {
            Ren_cache(traditionel_VÆRDI.modtage[positionsindeks], varighed_VÆRDI, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, varighed_VÆRDI - 2, PBUF_POOL);
            if (!data) traditionel_VÆRDI.Statistik_VÆRDI[4]++;
            else if (pbuf_take(data, traditionel_VÆRDI.modtage[positionsindeks] + 2, varighed_VÆRDI - 2) != ERR_OK || enhed_VÆRDI->input(data, enhed_VÆRDI) != ERR_OK) {
                pbuf_free(data); traditionel_VÆRDI.Statistik_VÆRDI[4]++;
            } else { traditionel_VÆRDI.Statistik_VÆRDI[0]++; traditionel_VÆRDI.Statistik_VÆRDI[1] += varighed_VÆRDI - 2; }
        }
        받는주소(positionsindeks); synkronisere(); traditionel_VÆRDI.bruge_VÆRDI++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_tal)) = traditionel_VÆRDI.bruge_VÆRDI;
    }
}
uint32_t traditionel_netværk_Statistik(unsigned post_VÆRDI_962f286b) {
    return post_VÆRDI_962f286b < 5 ? traditionel_VÆRDI.Statistik_VÆRDI[post_VÆRDI_962f286b] : post_VÆRDI_962f286b == 5 ? traditionel_VÆRDI.속도 : post_VÆRDI_962f286b == 6 ? traditionel_VÆRDI.Tilrettelæg : 0;
}
