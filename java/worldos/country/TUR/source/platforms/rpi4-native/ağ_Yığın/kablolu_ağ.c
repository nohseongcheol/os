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
#include "kablolu_ağ.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Pano_mutlak_adres(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ADRES) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ADRES)))
#endif
enum { 고리번호 = 16, Loop_BAĞ_DEĞ_SAY = 256, arabellek_boyutu = 2048 };
static struct {
    unsigned char almak[Loop_BAĞ_DEĞ_SAY][arabellek_boyutu];
    unsigned char göndermek[Loop_BAĞ_DEĞ_SAY][arabellek_boyutu];
    uint16_t tüketmek_değer, 생산;
    int 물리주소, Hazırlan, 속도;
    uint32_t İstatistik_değer[5];
    uintptr_t doğrulamak_Sonraki_öğe;
} kablolu_değer __attribute__((aligned(64)));

static void eşitlemek(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void TEMİZ_önbellek(void *veri, unsigned süre_değer, int almak) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)veri + süre_değer;
    for (uintptr_t ADRES = (uintptr_t)veri & ~(uintptr_t)63; ADRES < 끝; ADRES += 64) {
        if (almak) __asm__ volatile("dc ivac, %0" :: "r"(ADRES) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ADRES) : "memory");
    }
#else
    (void)veri; (void)süre_değer; (void)almak;
#endif
    eşitlemek();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ADRES, unsigned Dizin, int Yazma, unsigned değer) {
    uint32_t komut = (Yazma ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ADRES << GENET_MDIO_ADDR_SHIFT) | (Dizin << GENET_MDIO_REG_SHIFT) | (değer & 65535);
    유선저장기(GENET_MDIO_CMD) = komut;
    유선저장기(GENET_MDIO_CMD) = komut | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Durum_değer = 유선저장기(GENET_MDIO_CMD);
        if (!(Durum_değer & GENET_MDIO_START_BUSY))
            return Durum_değer & GENET_MDIO_READ_FAILED ? -1 : (int)(Durum_değer & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned Dizin) { return 물리전송(kablolu_değer.물리주소, Dizin, 0, 0); }
static int 물리쓰기(unsigned Dizin, unsigned değer) { return 물리전송(kablolu_değer.물리주소, Dizin, 1, değer); }
static int 물리준비(void) {
    kablolu_değer.물리주소 = -1;
    for (unsigned ADRES = 0; ADRES < 32; ADRES++) {
        int 식별 = 물리전송(ADRES, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { kablolu_değer.물리주소 = ADRES; break; }
    }
    if (kablolu_değer.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int değer = 물리읽기(BRGPHY_MII_AUXCTL);
    if (değer < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (değer & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    değer = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (değer < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (değer & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Hazırlan_Loop(unsigned Arka_Plan_değer) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_değer = Arka_Plan_değer + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned konum = 0; konum <= 0x30; konum += 4) 유선저장기(Loop_değer + konum) = 0;
    유선저장기(Loop_değer + 0x10) = (Loop_BAĞ_DEĞ_SAY << 16) | arabellek_boyutu;
    유선저장기(Loop_değer + 0x1c) = Loop_BAĞ_DEĞ_SAY * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Arka_Plan_değer == GENET_RX_BASE) 유선저장기(Loop_değer + 0x28) = (5 << 16) | (Loop_BAĞ_DEĞ_SAY >> 4);
    else 유선저장기(Loop_değer + 0x24) = 1;
    유선저장기(Arka_Plan_değer + 0x104c) = 8;
    유선저장기(Arka_Plan_değer + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned konum_dizini) {
    uintptr_t ADRES = (uintptr_t)kablolu_değer.almak[konum_dizini];
    TEMİZ_önbellek((void *)ADRES, arabellek_boyutu, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(konum_dizini)) = (uint32_t)ADRES;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(konum_dizini)) = (uint64_t)ADRES >> 32;
    유선저장기(GENET_RX_DESC_STATUS(konum_dizini)) = arabellek_boyutu << 16;
}
static err_t göndermek_veri_birimi(struct netif *cihaz_değer, struct pbuf *veri_birimi) {
    if (!kablolu_değer.Hazırlan || !netif_is_link_up(cihaz_değer)) return ERR_RTE;
    unsigned Boyut = veri_birimi->tot_len;
    if (!Boyut || Boyut > 1536) return ERR_BUF;
    uint16_t tüketmek_değer = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(kablolu_değer.생산 - tüketmek_değer) >= Loop_BAĞ_DEĞ_SAY - 1) return ERR_MEM;
    unsigned konum_dizini = kablolu_değer.생산 % Loop_BAĞ_DEĞ_SAY, 송신길이 = Boyut < 60 ? 60 : Boyut;
    unsigned char *veri = kablolu_değer.göndermek[konum_dizini];
    memset(veri, 0, 송신길이);
    if (pbuf_copy_partial(veri_birimi, veri, Boyut, 0) != Boyut) return ERR_BUF;
    TEMİZ_önbellek(veri, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(konum_dizini)) = (uint32_t)(uintptr_t)veri;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(konum_dizini)) = (uint64_t)(uintptr_t)veri >> 32;
    유선저장기(GENET_TX_DESC_STATUS(konum_dizini)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    eşitlemek();
    kablolu_değer.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = kablolu_değer.생산;
    kablolu_değer.İstatistik_değer[2]++; kablolu_değer.İstatistik_değer[3] += Boyut;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Hazırlan_kablolu_ağ(struct netif *cihaz_değer) {
    unsigned char ADRES[6];
    if (!유선장치있음() || !Pano_mutlak_adres(ADRES) || (ADRES[0] & 1)) return ERR_IF;
    unsigned SUM_değer = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_değer |= ADRES[순번];
    if (!SUM_değer) return ERR_IF;
    memset(&kablolu_değer, 0, sizeof(kablolu_değer));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t başlangıç_durumu = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = başlangıç_durumu | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = başlangıç_durumu & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
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
    Hazırlan_Loop(GENET_TX_BASE); Hazırlan_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_BAĞ_DEĞ_SAY; 순번++) 받는주소(순번);
    eşitlemek();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    cihaz_değer->name[0] = 'e'; cihaz_değer->name[1] = 'n'; cihaz_değer->mtu = 1500;
    cihaz_değer->hwaddr_len = 6; memcpy(cihaz_değer->hwaddr, ADRES, 6);
    cihaz_değer->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    cihaz_değer->output = etharp_output; cihaz_değer->linkoutput = göndermek_veri_birimi;
    kablolu_değer.Hazırlan = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *cihaz_değer) {
    if (!kablolu_değer.Hazırlan) return;
    uintptr_t ŞİMDİ_değer = 보드밀리초();
    if (ŞİMDİ_değer >= kablolu_değer.doğrulamak_Sonraki_öğe) {
        kablolu_değer.doğrulamak_Sonraki_öğe = ŞİMDİ_değer + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Durum_değer = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned metot_mod = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = metot_mod == 7 ? 1000 : metot_mod == 5 ? 100 : metot_mod == 2 ? 10 : 0;
        kablolu_değer.속도 = Durum_değer >= 0 && (Durum_değer & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (kablolu_değer.속도) {
            uint32_t Ayarlar = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Ayarlar &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Ayarlar | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Ayarlar = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Ayarlar | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(cihaz_değer)) netif_set_link_up(cihaz_değer);
        } else if (netif_is_link_up(cihaz_değer)) netif_set_link_down(cihaz_değer);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - kablolu_değer.tüketmek_değer);
    if (남음 > Loop_BAĞ_DEĞ_SAY) { kablolu_değer.İstatistik_değer[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned konum_dizini = kablolu_değer.tüketmek_değer % Loop_BAĞ_DEĞ_SAY;
        eşitlemek();
        uint32_t Durum_değer = 유선저장기(GENET_RX_DESC_STATUS(konum_dizini));
        unsigned süre_değer = (Durum_değer & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t sınır_değer = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Durum_değer & (sınır_değer | GENET_RX_DESC_STATUS_RX_ERROR)) != sınır_değer || süre_değer < 16 || süre_değer > 1538) kablolu_değer.İstatistik_değer[4]++;
        else {
            TEMİZ_önbellek(kablolu_değer.almak[konum_dizini], süre_değer, 1);
            struct pbuf *veri = pbuf_alloc(PBUF_RAW, süre_değer - 2, PBUF_POOL);
            if (!veri) kablolu_değer.İstatistik_değer[4]++;
            else if (pbuf_take(veri, kablolu_değer.almak[konum_dizini] + 2, süre_değer - 2) != ERR_OK || cihaz_değer->input(veri, cihaz_değer) != ERR_OK) {
                pbuf_free(veri); kablolu_değer.İstatistik_değer[4]++;
            } else { kablolu_değer.İstatistik_değer[0]++; kablolu_değer.İstatistik_değer[1] += süre_değer - 2; }
        }
        받는주소(konum_dizini); eşitlemek(); kablolu_değer.tüketmek_değer++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = kablolu_değer.tüketmek_değer;
    }
}
uint32_t kablolu_ağ_İstatistik(unsigned girdi_değer) {
    return girdi_değer < 5 ? kablolu_değer.İstatistik_değer[girdi_değer] : girdi_değer == 5 ? kablolu_değer.속도 : girdi_değer == 6 ? kablolu_değer.Hazırlan : 0;
}
