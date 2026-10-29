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
#include "ενσύρματος_δίκτυο.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Πίνακας_απόλυτη_διεύθυνση(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(διεύθυνση) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (διεύθυνση)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, μέγεθος_buffer = 2048 };
static struct {
    unsigned char λαμβάνω[고리개수][μέγεθος_buffer];
    unsigned char στέλνω[고리개수][μέγεθος_buffer];
    uint16_t ανάλωση_τιμή, 생산;
    int 물리주소, Προετοίμασε, 속도;
    uint32_t Στατιστικά_τιμή[5];
    uintptr_t επαληθεύω_Επόμενο_στοιχείο;
} ενσύρματος_τιμή __attribute__((aligned(64)));

static void συγχρονίζω(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void 캐시정리(void *δεδομένα, unsigned διάρκεια_τιμή, int λαμβάνω) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)δεδομένα + διάρκεια_τιμή;
    for (uintptr_t διεύθυνση = (uintptr_t)δεδομένα & ~(uintptr_t)63; διεύθυνση < 끝; διεύθυνση += 64) {
        if (λαμβάνω) __asm__ volatile("dc ivac, %0" :: "r"(διεύθυνση) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(διεύθυνση) : "memory");
    }
#else
    (void)δεδομένα; (void)διάρκεια_τιμή; (void)λαμβάνω;
#endif
    συγχρονίζω();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned διεύθυνση, unsigned Ευρετήριο, int Εγγραφή, unsigned τιμή) {
    uint32_t Εντολή = (Εγγραφή ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (διεύθυνση << GENET_MDIO_ADDR_SHIFT) | (Ευρετήριο << GENET_MDIO_REG_SHIFT) | (τιμή & 65535);
    유선저장기(GENET_MDIO_CMD) = Εντολή;
    유선저장기(GENET_MDIO_CMD) = Εντολή | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Κατάσταση_τιμή = 유선저장기(GENET_MDIO_CMD);
        if (!(Κατάσταση_τιμή & GENET_MDIO_START_BUSY))
            return Κατάσταση_τιμή & GENET_MDIO_READ_FAILED ? -1 : (int)(Κατάσταση_τιμή & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned Ευρετήριο) { return 물리전송(ενσύρματος_τιμή.물리주소, Ευρετήριο, 0, 0); }
static int 물리쓰기(unsigned Ευρετήριο, unsigned τιμή) { return 물리전송(ενσύρματος_τιμή.물리주소, Ευρετήριο, 1, τιμή); }
static int 물리준비(void) {
    ενσύρματος_τιμή.물리주소 = -1;
    for (unsigned διεύθυνση = 0; διεύθυνση < 32; διεύθυνση++) {
        int 식별 = 물리전송(διεύθυνση, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ενσύρματος_τιμή.물리주소 = διεύθυνση; break; }
    }
    if (ενσύρματος_τιμή.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int τιμή = 물리읽기(BRGPHY_MII_AUXCTL);
    if (τιμή < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (τιμή & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    τιμή = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (τιμή < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (τιμή & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Προετοίμασε_βρόχος(unsigned φόντο_τιμή) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned βρόχος_τιμή = φόντο_τιμή + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned Θέση = 0; Θέση <= 0x30; Θέση += 4) 유선저장기(βρόχος_τιμή + Θέση) = 0;
    유선저장기(βρόχος_τιμή + 0x10) = (고리개수 << 16) | μέγεθος_buffer;
    유선저장기(βρόχος_τιμή + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (φόντο_τιμή == GENET_RX_BASE) 유선저장기(βρόχος_τιμή + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(βρόχος_τιμή + 0x24) = 1;
    유선저장기(φόντο_τιμή + 0x104c) = 8;
    유선저장기(φόντο_τιμή + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned δείκτης_θέσης) {
    uintptr_t διεύθυνση = (uintptr_t)ενσύρματος_τιμή.λαμβάνω[δείκτης_θέσης];
    캐시정리((void *)διεύθυνση, μέγεθος_buffer, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(δείκτης_θέσης)) = (uint32_t)διεύθυνση;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(δείκτης_θέσης)) = (uint64_t)διεύθυνση >> 32;
    유선저장기(GENET_RX_DESC_STATUS(δείκτης_θέσης)) = μέγεθος_buffer << 16;
}
static err_t στέλνω_αυτοδύναμο_πακέτο(struct netif *συσκευή_τιμή, struct pbuf *αυτοδύναμο_πακέτο) {
    if (!ενσύρματος_τιμή.Προετοίμασε || !netif_is_link_up(συσκευή_τιμή)) return ERR_RTE;
    unsigned Μέγεθος = αυτοδύναμο_πακέτο->tot_len;
    if (!Μέγεθος || Μέγεθος > 1536) return ERR_BUF;
    uint16_t ανάλωση_τιμή = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ενσύρματος_τιμή.생산 - ανάλωση_τιμή) >= 고리개수 - 1) return ERR_MEM;
    unsigned δείκτης_θέσης = ενσύρματος_τιμή.생산 % 고리개수, 송신길이 = Μέγεθος < 60 ? 60 : Μέγεθος;
    unsigned char *δεδομένα = ενσύρματος_τιμή.στέλνω[δείκτης_θέσης];
    memset(δεδομένα, 0, 송신길이);
    if (pbuf_copy_partial(αυτοδύναμο_πακέτο, δεδομένα, Μέγεθος, 0) != Μέγεθος) return ERR_BUF;
    캐시정리(δεδομένα, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(δείκτης_θέσης)) = (uint32_t)(uintptr_t)δεδομένα;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(δείκτης_θέσης)) = (uint64_t)(uintptr_t)δεδομένα >> 32;
    유선저장기(GENET_TX_DESC_STATUS(δείκτης_θέσης)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    συγχρονίζω();
    ενσύρματος_τιμή.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ενσύρματος_τιμή.생산;
    ενσύρματος_τιμή.Στατιστικά_τιμή[2]++; ενσύρματος_τιμή.Στατιστικά_τιμή[3] += Μέγεθος;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Προετοίμασε_ενσύρματος_δίκτυο(struct netif *συσκευή_τιμή) {
    unsigned char διεύθυνση[6];
    if (!유선장치있음() || !Πίνακας_απόλυτη_διεύθυνση(διεύθυνση) || (διεύθυνση[0] & 1)) return ERR_IF;
    unsigned Διαχείριση_ενημερώσεων_λογισμικού_τιμή = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) Διαχείριση_ενημερώσεων_λογισμικού_τιμή |= διεύθυνση[순번];
    if (!Διαχείριση_ενημερώσεων_λογισμικού_τιμή) return ERR_IF;
    memset(&ενσύρματος_τιμή, 0, sizeof(ενσύρματος_τιμή));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t αρχική_κατάσταση = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = αρχική_κατάσταση | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = αρχική_κατάσταση & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)διεύθυνση[0] << 24 | (uint32_t)διεύθυνση[1] << 16 | διεύθυνση[2] << 8 | διεύθυνση[3];
    유선저장기(GENET_UMAC_MAC1) = διεύθυνση[4] << 8 | διεύθυνση[5];
    Προετοίμασε_βρόχος(GENET_TX_BASE); Προετοίμασε_βρόχος(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    συγχρονίζω();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    συσκευή_τιμή->name[0] = 'e'; συσκευή_τιμή->name[1] = 'n'; συσκευή_τιμή->mtu = 1500;
    συσκευή_τιμή->hwaddr_len = 6; memcpy(συσκευή_τιμή->hwaddr, διεύθυνση, 6);
    συσκευή_τιμή->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    συσκευή_τιμή->output = etharp_output; συσκευή_τιμή->linkoutput = στέλνω_αυτοδύναμο_πακέτο;
    ενσύρματος_τιμή.Προετοίμασε = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *συσκευή_τιμή) {
    if (!ενσύρματος_τιμή.Προετοίμασε) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= ενσύρματος_τιμή.επαληθεύω_Επόμενο_στοιχείο) {
        ενσύρματος_τιμή.επαληθεύω_Επόμενο_στοιχείο = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Κατάσταση_τιμή = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned μέθοδος_λειτουργία = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = μέθοδος_λειτουργία == 7 ? 1000 : μέθοδος_λειτουργία == 5 ? 100 : μέθοδος_λειτουργία == 2 ? 10 : 0;
        ενσύρματος_τιμή.속도 = Κατάσταση_τιμή >= 0 && (Κατάσταση_τιμή & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ενσύρματος_τιμή.속도) {
            uint32_t Ρυθμίσεις = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Ρυθμίσεις &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Ρυθμίσεις | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Ρυθμίσεις = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Ρυθμίσεις | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(συσκευή_τιμή)) netif_set_link_up(συσκευή_τιμή);
        } else if (netif_is_link_up(συσκευή_τιμή)) netif_set_link_down(συσκευή_τιμή);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ενσύρματος_τιμή.ανάλωση_τιμή);
    if (남음 > 고리개수) { ενσύρματος_τιμή.Στατιστικά_τιμή[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned δείκτης_θέσης = ενσύρματος_τιμή.ανάλωση_τιμή % 고리개수;
        συγχρονίζω();
        uint32_t Κατάσταση_τιμή = 유선저장기(GENET_RX_DESC_STATUS(δείκτης_θέσης));
        unsigned διάρκεια_τιμή = (Κατάσταση_τιμή & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t όριο_τιμή = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Κατάσταση_τιμή & (όριο_τιμή | GENET_RX_DESC_STATUS_RX_ERROR)) != όριο_τιμή || διάρκεια_τιμή < 16 || διάρκεια_τιμή > 1538) ενσύρματος_τιμή.Στατιστικά_τιμή[4]++;
        else {
            캐시정리(ενσύρματος_τιμή.λαμβάνω[δείκτης_θέσης], διάρκεια_τιμή, 1);
            struct pbuf *δεδομένα = pbuf_alloc(PBUF_RAW, διάρκεια_τιμή - 2, PBUF_POOL);
            if (!δεδομένα) ενσύρματος_τιμή.Στατιστικά_τιμή[4]++;
            else if (pbuf_take(δεδομένα, ενσύρματος_τιμή.λαμβάνω[δείκτης_θέσης] + 2, διάρκεια_τιμή - 2) != ERR_OK || συσκευή_τιμή->input(δεδομένα, συσκευή_τιμή) != ERR_OK) {
                pbuf_free(δεδομένα); ενσύρματος_τιμή.Στατιστικά_τιμή[4]++;
            } else { ενσύρματος_τιμή.Στατιστικά_τιμή[0]++; ενσύρματος_τιμή.Στατιστικά_τιμή[1] += διάρκεια_τιμή - 2; }
        }
        받는주소(δείκτης_θέσης); συγχρονίζω(); ενσύρματος_τιμή.ανάλωση_τιμή++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ενσύρματος_τιμή.ανάλωση_τιμή;
    }
}
uint32_t ενσύρματος_δίκτυο_Στατιστικά(unsigned καταχώρηση_τιμή) {
    return καταχώρηση_τιμή < 5 ? ενσύρματος_τιμή.Στατιστικά_τιμή[καταχώρηση_τιμή] : καταχώρηση_τιμή == 5 ? ενσύρματος_τιμή.속도 : καταχώρηση_τιμή == 6 ? ενσύρματος_τιμή.Προετοίμασε : 0;
}
