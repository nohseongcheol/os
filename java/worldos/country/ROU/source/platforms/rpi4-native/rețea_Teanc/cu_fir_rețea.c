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
#include "cu_fir_rețea.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Avizier_adresă_reală(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(adresa) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (adresa)))
#endif
enum { 고리번호 = 16, Loop_COUNT = 256, dimensiune_zonă_tampon = 2048 };
static struct {
    unsigned char primi[Loop_COUNT][dimensiune_zonă_tampon];
    unsigned char trimite[Loop_COUNT][dimensiune_zonă_tampon];
    uint16_t consum_VALUE, 생산;
    int 물리주소, Pregătiți, 속도;
    uint32_t Statistică_VALUE[5];
    uintptr_t verifica_Următorul_element;
} cu_fir_VALUE __attribute__((aligned(64)));

static void sincroniz(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void CLEAN_cache(void *date, unsigned lungime_VALUE, int primi) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)date + lungime_VALUE;
    for (uintptr_t adresa = (uintptr_t)date & ~(uintptr_t)63; adresa < 끝; adresa += 64) {
        if (primi) __asm__ volatile("dc ivac, %0" :: "r"(adresa) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(adresa) : "memory");
    }
#else
    (void)date; (void)lungime_VALUE; (void)primi;
#endif
    sincroniz();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned adresa, unsigned INDEX, int Scriere, unsigned VALUE) {
    uint32_t Comandă = (Scriere ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (adresa << GENET_MDIO_ADDR_SHIFT) | (INDEX << GENET_MDIO_REG_SHIFT) | (VALUE & 65535);
    유선저장기(GENET_MDIO_CMD) = Comandă;
    유선저장기(GENET_MDIO_CMD) = Comandă | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Stare_VALUE = 유선저장기(GENET_MDIO_CMD);
        if (!(Stare_VALUE & GENET_MDIO_START_BUSY))
            return Stare_VALUE & GENET_MDIO_READ_FAILED ? -1 : (int)(Stare_VALUE & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned INDEX) { return 물리전송(cu_fir_VALUE.물리주소, INDEX, 0, 0); }
static int 물리쓰기(unsigned INDEX, unsigned VALUE) { return 물리전송(cu_fir_VALUE.물리주소, INDEX, 1, VALUE); }
static int 물리준비(void) {
    cu_fir_VALUE.물리주소 = -1;
    for (unsigned adresa = 0; adresa < 32; adresa++) {
        int 식별 = 물리전송(adresa, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { cu_fir_VALUE.물리주소 = adresa; break; }
    }
    if (cu_fir_VALUE.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VALUE = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VALUE < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VALUE & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VALUE = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VALUE < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VALUE & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Pregătiți_Loop(unsigned tapet_VALUE) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALUE = tapet_VALUE + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Poziție = 0; Poziție <= 0x30; Poziție += 4) 유선저장기(Loop_VALUE + Poziție) = 0;
    유선저장기(Loop_VALUE + 0x10) = (Loop_COUNT << 16) | dimensiune_zonă_tampon;
    유선저장기(Loop_VALUE + 0x1c) = Loop_COUNT * GENET_DMA_DESC_SIZE / 4 - 1;
    if (tapet_VALUE == GENET_RX_BASE) 유선저장기(Loop_VALUE + 0x28) = (5 << 16) | (Loop_COUNT >> 4);
    else 유선저장기(Loop_VALUE + 0x24) = 1;
    유선저장기(tapet_VALUE + 0x104c) = 8;
    유선저장기(tapet_VALUE + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned index_de_poziție) {
    uintptr_t adresa = (uintptr_t)cu_fir_VALUE.primi[index_de_poziție];
    CLEAN_cache((void *)adresa, dimensiune_zonă_tampon, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(index_de_poziție)) = (uint32_t)adresa;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(index_de_poziție)) = (uint64_t)adresa >> 32;
    유선저장기(GENET_RX_DESC_STATUS(index_de_poziție)) = dimensiune_zonă_tampon << 16;
}
static err_t trimite_diagramă_informații(struct netif *mobil_VALUE, struct pbuf *diagramă_informații) {
    if (!cu_fir_VALUE.Pregătiți || !netif_is_link_up(mobil_VALUE)) return ERR_RTE;
    unsigned Mărime = diagramă_informații->tot_len;
    if (!Mărime || Mărime > 1536) return ERR_BUF;
    uint16_t consum_VALUE = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(cu_fir_VALUE.생산 - consum_VALUE) >= Loop_COUNT - 1) return ERR_MEM;
    unsigned index_de_poziție = cu_fir_VALUE.생산 % Loop_COUNT, 송신길이 = Mărime < 60 ? 60 : Mărime;
    unsigned char *date = cu_fir_VALUE.trimite[index_de_poziție];
    memset(date, 0, 송신길이);
    if (pbuf_copy_partial(diagramă_informații, date, Mărime, 0) != Mărime) return ERR_BUF;
    CLEAN_cache(date, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(index_de_poziție)) = (uint32_t)(uintptr_t)date;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(index_de_poziție)) = (uint64_t)(uintptr_t)date >> 32;
    유선저장기(GENET_TX_DESC_STATUS(index_de_poziție)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sincroniz();
    cu_fir_VALUE.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = cu_fir_VALUE.생산;
    cu_fir_VALUE.Statistică_VALUE[2]++; cu_fir_VALUE.Statistică_VALUE[3] += Mărime;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Pregătiți_cu_fir_rețea(struct netif *mobil_VALUE) {
    unsigned char adresa[6];
    if (!유선장치있음() || !Avizier_adresă_reală(adresa) || (adresa[0] & 1)) return ERR_IF;
    unsigned SUM_VALUE = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALUE |= adresa[순번];
    if (!SUM_VALUE) return ERR_IF;
    memset(&cu_fir_VALUE, 0, sizeof(cu_fir_VALUE));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t stare_inițială = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = stare_inițială | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = stare_inițială & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)adresa[0] << 24 | (uint32_t)adresa[1] << 16 | adresa[2] << 8 | adresa[3];
    유선저장기(GENET_UMAC_MAC1) = adresa[4] << 8 | adresa[5];
    Pregătiți_Loop(GENET_TX_BASE); Pregătiți_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_COUNT; 순번++) 받는주소(순번);
    sincroniz();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    mobil_VALUE->name[0] = 'e'; mobil_VALUE->name[1] = 'n'; mobil_VALUE->mtu = 1500;
    mobil_VALUE->hwaddr_len = 6; memcpy(mobil_VALUE->hwaddr, adresa, 6);
    mobil_VALUE->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    mobil_VALUE->output = etharp_output; mobil_VALUE->linkoutput = trimite_diagramă_informații;
    cu_fir_VALUE.Pregătiți = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *mobil_VALUE) {
    if (!cu_fir_VALUE.Pregătiți) return;
    uintptr_t NOW_VALUE = 보드밀리초();
    if (NOW_VALUE >= cu_fir_VALUE.verifica_Următorul_element) {
        cu_fir_VALUE.verifica_Următorul_element = NOW_VALUE + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Stare_VALUE = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metodă_mod = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metodă_mod == 7 ? 1000 : metodă_mod == 5 ? 100 : metodă_mod == 2 ? 10 : 0;
        cu_fir_VALUE.속도 = Stare_VALUE >= 0 && (Stare_VALUE & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (cu_fir_VALUE.속도) {
            uint32_t Setări = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Setări &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Setări | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Setări = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Setări | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(mobil_VALUE)) netif_set_link_up(mobil_VALUE);
        } else if (netif_is_link_up(mobil_VALUE)) netif_set_link_down(mobil_VALUE);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - cu_fir_VALUE.consum_VALUE);
    if (남음 > Loop_COUNT) { cu_fir_VALUE.Statistică_VALUE[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned index_de_poziție = cu_fir_VALUE.consum_VALUE % Loop_COUNT;
        sincroniz();
        uint32_t Stare_VALUE = 유선저장기(GENET_RX_DESC_STATUS(index_de_poziție));
        unsigned lungime_VALUE = (Stare_VALUE & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Stare_VALUE & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || lungime_VALUE < 16 || lungime_VALUE > 1538) cu_fir_VALUE.Statistică_VALUE[4]++;
        else {
            CLEAN_cache(cu_fir_VALUE.primi[index_de_poziție], lungime_VALUE, 1);
            struct pbuf *date = pbuf_alloc(PBUF_RAW, lungime_VALUE - 2, PBUF_POOL);
            if (!date) cu_fir_VALUE.Statistică_VALUE[4]++;
            else if (pbuf_take(date, cu_fir_VALUE.primi[index_de_poziție] + 2, lungime_VALUE - 2) != ERR_OK || mobil_VALUE->input(date, mobil_VALUE) != ERR_OK) {
                pbuf_free(date); cu_fir_VALUE.Statistică_VALUE[4]++;
            } else { cu_fir_VALUE.Statistică_VALUE[0]++; cu_fir_VALUE.Statistică_VALUE[1] += lungime_VALUE - 2; }
        }
        받는주소(index_de_poziție); sincroniz(); cu_fir_VALUE.consum_VALUE++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = cu_fir_VALUE.consum_VALUE;
    }
}
uint32_t cu_fir_rețea_Statistică(unsigned intrare_VALUE) {
    return intrare_VALUE < 5 ? cu_fir_VALUE.Statistică_VALUE[intrare_VALUE] : intrare_VALUE == 5 ? cu_fir_VALUE.속도 : intrare_VALUE == 6 ? cu_fir_VALUE.Pregătiți : 0;
}
