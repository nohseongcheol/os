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
#include "per_cable_xarxa.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Tauler_màquina_ADREÇA(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(Adreça) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (Adreça)))
#endif
enum { 고리번호 = 16, Loop_COMPT = 256, memòria_intermèdia_canviar_la_mida = 2048 };
static struct {
    unsigned char rebre[Loop_COMPT][memòria_intermèdia_canviar_la_mida];
    unsigned char enviar[Loop_COMPT][memòria_intermèdia_canviar_la_mida];
    uint16_t 소비, 생산;
    int 물리주소, Prepara, 속도;
    uint32_t 집계[5];
    uintptr_t verificar_Següent_element;
} per_cable_VALOR __attribute__((aligned(64)));

static void sincronitzar(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void NETEJA_memòria_cau(void *dades, unsigned durada_VALOR, int rebre) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)dades + durada_VALOR;
    for (uintptr_t Adreça = (uintptr_t)dades & ~(uintptr_t)63; Adreça < 끝; Adreça += 64) {
        if (rebre) __asm__ volatile("dc ivac, %0" :: "r"(Adreça) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(Adreça) : "memory");
    }
#else
    (void)dades; (void)durada_VALOR; (void)rebre;
#endif
    sincronitzar();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned Adreça, unsigned INDEX, int Escriptura, unsigned VALOR) {
    uint32_t Ordre = (Escriptura ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (Adreça << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALOR & 65535);
    유선저장기(GENET_MDIO_CMD) = Ordre;
    유선저장기(GENET_MDIO_CMD) = Ordre | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Estat_VALOR = 유선저장기(GENET_MDIO_CMD);
        if (!(Estat_VALOR & GENET_MDIO_START_BUSY))
            return Estat_VALOR & GENET_MDIO_READ_FAILED ? -1 : (int)(Estat_VALOR & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(per_cable_VALOR.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALOR) { return 물리전송(per_cable_VALOR.물리주소, INDEX, 1, VALOR); }
static int 물리준비(void) {
    per_cable_VALOR.물리주소 = -1;
    for (unsigned Adreça = 0; Adreça < 32; Adreça++) {
        int 식별 = 물리전송(Adreça, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { per_cable_VALOR.물리주소 = Adreça; break; }
    }
    if (per_cable_VALOR.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VALOR = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VALOR < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VALOR & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VALOR = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VALOR < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VALOR & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Prepara_Loop(unsigned Fons_VALOR) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALOR = Fons_VALOR + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Posició = 0; Posició <= 0x30; Posició += 4) 유선저장기(Loop_VALOR + Posició) = 0;
    유선저장기(Loop_VALOR + 0x10) = (Loop_COMPT << 16) | memòria_intermèdia_canviar_la_mida;
    유선저장기(Loop_VALOR + 0x1c) = Loop_COMPT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Fons_VALOR == GENET_RX_BASE) 유선저장기(Loop_VALOR + 0x28) = (5 << 16) | (Loop_COMPT >> 4);
    else 유선저장기(Loop_VALOR + 0x24) = 1;
    유선저장기(Fons_VALOR + 0x104c) = 8;
    유선저장기(Fons_VALOR + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned càrrec_INDEX) {
    uintptr_t Adreça = (uintptr_t)per_cable_VALOR.rebre[càrrec_INDEX];
    NETEJA_memòria_cau((void *)Adreça, memòria_intermèdia_canviar_la_mida, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(càrrec_INDEX)) = (uint32_t)Adreça;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(càrrec_INDEX)) = (uint64_t)Adreça >> 32;
    유선저장기(GENET_RX_DESC_STATUS(càrrec_INDEX)) = memòria_intermèdia_canviar_la_mida << 16;
}
static err_t 전문보내기(struct netif *dispositiu_VALOR, struct pbuf *전문) {
    if (!per_cable_VALOR.Prepara || !netif_is_link_up(dispositiu_VALOR)) return ERR_RTE;
    unsigned Mida = 전문->tot_len;
    if (!Mida || Mida > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(per_cable_VALOR.생산 - 소비) >= Loop_COMPT - 1) return ERR_MEM;
    unsigned càrrec_INDEX = per_cable_VALOR.생산 % Loop_COMPT, 송신길이 = Mida < 60 ? 60 : Mida;
    unsigned char *dades = per_cable_VALOR.enviar[càrrec_INDEX];
    memset(dades, 0, 송신길이);
    if (pbuf_copy_partial(전문, dades, Mida, 0) != Mida) return ERR_BUF;
    NETEJA_memòria_cau(dades, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(càrrec_INDEX)) = (uint32_t)(uintptr_t)dades;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(càrrec_INDEX)) = (uint64_t)(uintptr_t)dades >> 32;
    유선저장기(GENET_TX_DESC_STATUS(càrrec_INDEX)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sincronitzar();
    per_cable_VALOR.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = per_cable_VALOR.생산;
    per_cable_VALOR.집계[2]++; per_cable_VALOR.집계[3] += Mida;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Prepara_per_cable_xarxa(struct netif *dispositiu_VALOR) {
    unsigned char Adreça[6];
    if (!유선장치있음() || !Tauler_màquina_ADREÇA(Adreça) || (Adreça[0] & 1)) return ERR_IF;
    unsigned SUMA_VALOR = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUMA_VALOR |= Adreça[순번];
    if (!SUMA_VALOR) return ERR_IF;
    memset(&per_cable_VALOR, 0, sizeof(per_cable_VALOR));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t 초기 = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 초기 | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 초기 & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)Adreça[0] << 24 | (uint32_t)Adreça[1] << 16 | Adreça[2] << 8 | Adreça[3];
    유선저장기(GENET_UMAC_MAC1) = Adreça[4] << 8 | Adreça[5];
    Prepara_Loop(GENET_TX_BASE); Prepara_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COMPT; 순번++) 받는주소(순번);
    sincronitzar();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    dispositiu_VALOR->name[0] = 'e'; dispositiu_VALOR->name[1] = 'n'; dispositiu_VALOR->mtu = 1500;
    dispositiu_VALOR->hwaddr_len = 6; memcpy(dispositiu_VALOR->hwaddr, Adreça, 6);
    dispositiu_VALOR->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    dispositiu_VALOR->output = etharp_output; dispositiu_VALOR->linkoutput = 전문보내기;
    per_cable_VALOR.Prepara = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *dispositiu_VALOR) {
    if (!per_cable_VALOR.Prepara) return;
    uintptr_t ARA_VALOR = 보드밀리초();
    if (ARA_VALOR >= per_cable_VALOR.verificar_Següent_element) {
        per_cable_VALOR.verificar_Següent_element = ARA_VALOR + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Estat_VALOR = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned 방식 = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = 방식 == 7 ? 1000 : 방식 == 5 ? 100 : 방식 == 2 ? 10 : 0;
        per_cable_VALOR.속도 = Estat_VALOR >= 0 && (Estat_VALOR & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (per_cable_VALOR.속도) {
            uint32_t Ajusts = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Ajusts &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Ajusts | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Ajusts = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Ajusts | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(dispositiu_VALOR)) netif_set_link_up(dispositiu_VALOR);
        } else if (netif_is_link_up(dispositiu_VALOR)) netif_set_link_down(dispositiu_VALOR);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - per_cable_VALOR.소비);
    if (남음 > Loop_COMPT) { per_cable_VALOR.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned càrrec_INDEX = per_cable_VALOR.소비 % Loop_COMPT;
        sincronitzar();
        uint32_t Estat_VALOR = 유선저장기(GENET_RX_DESC_STATUS(càrrec_INDEX));
        unsigned durada_VALOR = (Estat_VALOR & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Estat_VALOR & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || durada_VALOR < 16 || durada_VALOR > 1538) per_cable_VALOR.집계[4]++;
        else {
            NETEJA_memòria_cau(per_cable_VALOR.rebre[càrrec_INDEX], durada_VALOR, 1);
            struct pbuf *dades = pbuf_alloc(PBUF_RAW, durada_VALOR - 2, PBUF_POOL);
            if (!dades) per_cable_VALOR.집계[4]++;
            else if (pbuf_take(dades, per_cable_VALOR.rebre[càrrec_INDEX] + 2, durada_VALOR - 2) != ERR_OK || dispositiu_VALOR->input(dades, dispositiu_VALOR) != ERR_OK) {
                pbuf_free(dades); per_cable_VALOR.집계[4]++;
            } else { per_cable_VALOR.집계[0]++; per_cable_VALOR.집계[1] += durada_VALOR - 2; }
        }
        받는주소(càrrec_INDEX); sincronitzar(); per_cable_VALOR.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = per_cable_VALOR.소비;
    }
}
uint32_t 유선망집계(unsigned introducció_VALOR) {
    return introducció_VALOR < 5 ? per_cable_VALOR.집계[introducció_VALOR] : introducció_VALOR == 5 ? per_cable_VALOR.속도 : introducció_VALOR == 6 ? per_cable_VALOR.Prepara : 0;
}
