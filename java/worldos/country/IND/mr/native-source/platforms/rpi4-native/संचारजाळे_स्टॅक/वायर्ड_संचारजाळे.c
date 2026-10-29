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

#include "../नामकरण/मशीन_लिंक_नावे.h"
#include "वायर्ड_संचारजाळे.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(लूप_क्रमांक) (UINT32_C(1) << (लूप_क्रमांक))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t बोर्ड_मिलिसेकंद(void);
extern int बोर्ड_भौतिक_हार्डवेअर(void);
extern int बोर्ड_मशीन_पत्ता(unsigned char *);
#ifndef वायर्ड_नोंदणीस्थाने
#define वायर्ड_नोंदणीस्थाने(पत्ता) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (पत्ता)))
#endif
enum { लूप_संख्या_e7119cc7 = 16, लूप_संख्या = 256, बफर_आकारा = 2048 };
static struct {
    unsigned char स्वीकारा[लूप_संख्या][बफर_आकारा];
    unsigned char पाठवा[लूप_संख्या][बफर_आकारा];
    uint16_t वापरा_मूल्य, निर्माणकरा_मूल्य;
    int भौतिक_पत्ता, तयार_करणे, वेग_मूल्य;
    uint32_t सांख्यिकी_मूल्य[5];
    uintptr_t पुढील_आयटम_पडताळा;
} वायर्ड_मूल्य __attribute__((aligned(64)));

static void समन्वय_साधा(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void सुबक_कॅशे(void *डेटा, unsigned लांबी_मूल्य, int स्वीकारा) {
#ifndef JKOROS_GENET_TEST
    uintptr_t शेवट = (uintptr_t)डेटा + लांबी_मूल्य;
    for (uintptr_t पत्ता = (uintptr_t)डेटा & ~(uintptr_t)63; पत्ता < शेवट; पत्ता += 64) {
        if (स्वीकारा) __asm__ volatile("dc ivac, %0" :: "r"(पत्ता) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(पत्ता) : "memory");
    }
#else
    (void)डेटा; (void)लांबी_मूल्य; (void)स्वीकारा;
#endif
    समन्वय_साधा();
}
static void संक्षिप्त_विलंब(void) {
    uintptr_t शेवट = बोर्ड_मिलिसेकंद() + 1;
    while (बोर्ड_मिलिसेकंद() < शेवट) {}
}
static int भौतिक_स्थानांतर(unsigned पत्ता, unsigned अनुक्रमणिका, int लेखन, unsigned मूल्य) {
    uint32_t आदेश = (लेखन ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (पत्ता << GENET_MDIO_ADDR_SHIFT) | (अनुक्रमणिका << GENET_MDIO_REG_SHIFT) | (मूल्य & 65535);
    वायर्ड_नोंदणीस्थाने(GENET_MDIO_CMD) = आदेश;
    वायर्ड_नोंदणीस्थाने(GENET_MDIO_CMD) = आदेश | GENET_MDIO_START_BUSY;
    uintptr_t शेवट = बोर्ड_मिलिसेकंद() + 20;
    for (;;) {
        uint32_t राज्य_मूल्य = वायर्ड_नोंदणीस्थाने(GENET_MDIO_CMD);
        if (!(राज्य_मूल्य & GENET_MDIO_START_BUSY))
            return राज्य_मूल्य & GENET_MDIO_READ_FAILED ? -1 : (int)(राज्य_मूल्य & 65535);
        if (बोर्ड_मिलिसेकंद() >= शेवट) return -1;
    }
}
static int भौतिक_वाचा(unsigned अनुक्रमणिका) { return भौतिक_स्थानांतर(वायर्ड_मूल्य.भौतिक_पत्ता, अनुक्रमणिका, 0, 0); }
static int भौतिक_लिहा(unsigned अनुक्रमणिका, unsigned मूल्य) { return भौतिक_स्थानांतर(वायर्ड_मूल्य.भौतिक_पत्ता, अनुक्रमणिका, 1, मूल्य); }
static int तयार_करणे_भौतिक(void) {
    वायर्ड_मूल्य.भौतिक_पत्ता = -1;
    for (unsigned पत्ता = 0; पत्ता < 32; पत्ता++) {
        int ओळखा_मूल्य = भौतिक_स्थानांतर(पत्ता, 2, 0, 0);
        if (ओळखा_मूल्य > 0 && ओळखा_मूल्य != 65535) { वायर्ड_मूल्य.भौतिक_पत्ता = पत्ता; break; }
    }
    if (वायर्ड_मूल्य.भौतिक_पत्ता < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (भौतिक_लिहा(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int मूल्य = भौतिक_वाचा(BRGPHY_MII_AUXCTL);
    if (मूल्य < 0 || भौतिक_लिहा(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (मूल्य & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (भौतिक_लिहा(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    मूल्य = भौतिक_वाचा(BRGPHY_MII_SHADOW_1C);
    if (मूल्य < 0 || भौतिक_लिहा(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (मूल्य & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (भौतिक_लिहा(4, 0x0141) < 0 || भौतिक_लिहा(9, 0x0200) < 0) return -1;
    return भौतिक_लिहा(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void तयार_करणे_लूप(unsigned वॉलपेपर_मूल्य) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned लूप_मूल्य = वॉलपेपर_मूल्य + 0xc00 + GENET_DMA_RING_SIZE * लूप_संख्या_e7119cc7;
    for (unsigned जागा = 0; जागा <= 0x30; जागा += 4) वायर्ड_नोंदणीस्थाने(लूप_मूल्य + जागा) = 0;
    वायर्ड_नोंदणीस्थाने(लूप_मूल्य + 0x10) = (लूप_संख्या << 16) | बफर_आकारा;
    वायर्ड_नोंदणीस्थाने(लूप_मूल्य + 0x1c) = लूप_संख्या * GENET_DMA_DESC_SIZE / 4 - 1;
    if (वॉलपेपर_मूल्य == GENET_RX_BASE) वायर्ड_नोंदणीस्थाने(लूप_मूल्य + 0x28) = (5 << 16) | (लूप_संख्या >> 4);
    else वायर्ड_नोंदणीस्थाने(लूप_मूल्य + 0x24) = 1;
    वायर्ड_नोंदणीस्थाने(वॉलपेपर_मूल्य + 0x104c) = 8;
    वायर्ड_नोंदणीस्थाने(वॉलपेपर_मूल्य + 0x1040) = __BIT(लूप_संख्या_e7119cc7);
}
static void स्वीकारणे_पत्ता(unsigned स्थान_अनुक्रमणिका) {
    uintptr_t पत्ता = (uintptr_t)वायर्ड_मूल्य.स्वीकारा[स्थान_अनुक्रमणिका];
    सुबक_कॅशे((void *)पत्ता, बफर_आकारा, 0);
    वायर्ड_नोंदणीस्थाने(GENET_RX_DESC_ADDRESS_LO(स्थान_अनुक्रमणिका)) = (uint32_t)पत्ता;
    वायर्ड_नोंदणीस्थाने(GENET_RX_DESC_ADDRESS_HI(स्थान_अनुक्रमणिका)) = (uint64_t)पत्ता >> 32;
    वायर्ड_नोंदणीस्थाने(GENET_RX_DESC_STATUS(स्थान_अनुक्रमणिका)) = बफर_आकारा << 16;
}
static err_t स्वतंत्रसंदेश_पाठवा(struct netif *मोबाइल_मूल्य, struct pbuf *स्वतंत्रसंदेश) {
    if (!वायर्ड_मूल्य.तयार_करणे || !netif_is_link_up(मोबाइल_मूल्य)) return ERR_RTE;
    unsigned आकार = स्वतंत्रसंदेश->tot_len;
    if (!आकार || आकार > 1536) return ERR_BUF;
    uint16_t वापरा_मूल्य = वायर्ड_नोंदणीस्थाने(GENET_TX_DMA_CONS_INDEX(लूप_संख्या_e7119cc7));
    if ((uint16_t)(वायर्ड_मूल्य.निर्माणकरा_मूल्य - वापरा_मूल्य) >= लूप_संख्या - 1) return ERR_MEM;
    unsigned स्थान_अनुक्रमणिका = वायर्ड_मूल्य.निर्माणकरा_मूल्य % लूप_संख्या, प्रेषितकरा_लांबी = आकार < 60 ? 60 : आकार;
    unsigned char *डेटा = वायर्ड_मूल्य.पाठवा[स्थान_अनुक्रमणिका];
    memset(डेटा, 0, प्रेषितकरा_लांबी);
    if (pbuf_copy_partial(स्वतंत्रसंदेश, डेटा, आकार, 0) != आकार) return ERR_BUF;
    सुबक_कॅशे(डेटा, प्रेषितकरा_लांबी, 0);
    वायर्ड_नोंदणीस्थाने(GENET_TX_DESC_ADDRESS_LO(स्थान_अनुक्रमणिका)) = (uint32_t)(uintptr_t)डेटा;
    वायर्ड_नोंदणीस्थाने(GENET_TX_DESC_ADDRESS_HI(स्थान_अनुक्रमणिका)) = (uint64_t)(uintptr_t)डेटा >> 32;
    वायर्ड_नोंदणीस्थाने(GENET_TX_DESC_STATUS(स्थान_अनुक्रमणिका)) = (प्रेषितकरा_लांबी << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    समन्वय_साधा();
    वायर्ड_मूल्य.निर्माणकरा_मूल्य++;
    वायर्ड_नोंदणीस्थाने(GENET_TX_DMA_PROD_INDEX(लूप_संख्या_e7119cc7)) = वायर्ड_मूल्य.निर्माणकरा_मूल्य;
    वायर्ड_मूल्य.सांख्यिकी_मूल्य[2]++; वायर्ड_मूल्य.सांख्यिकी_मूल्य[3] += आकार;
    return ERR_OK;
}
int आहे_वायर्ड_मोबाइल(void) {
    return बोर्ड_भौतिक_हार्डवेअर() && ((वायर्ड_नोंदणीस्थाने(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t तयार_करणे_वायर्ड_संचारजाळे(struct netif *मोबाइल_मूल्य) {
    unsigned char पत्ता[6];
    if (!आहे_वायर्ड_मोबाइल() || !बोर्ड_मशीन_पत्ता(पत्ता) || (पत्ता[0] & 1)) return ERR_IF;
    unsigned बेरीज_मूल्य = 0; for (unsigned क्रमांक_अनुक्रमणिका = 0; क्रमांक_अनुक्रमणिका < 6; क्रमांक_अनुक्रमणिका++) बेरीज_मूल्य |= पत्ता[क्रमांक_अनुक्रमणिका];
    if (!बेरीज_मूल्य) return ERR_IF;
    memset(&वायर्ड_मूल्य, 0, sizeof(वायर्ड_मूल्य));
    वायर्ड_नोंदणीस्थाने(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    वायर्ड_नोंदणीस्थाने(GENET_RX_DMA_CTRL) = वायर्ड_नोंदणीस्थाने(GENET_TX_DMA_CTRL) = 0;
    uint32_t प्रारंभिक_राज्य = वायर्ड_नोंदणीस्थाने(GENET_SYS_RBUF_FLUSH_CTRL);
    वायर्ड_नोंदणीस्थाने(GENET_SYS_RBUF_FLUSH_CTRL) = प्रारंभिक_राज्य | GENET_SYS_RBUF_FLUSH_RESET; संक्षिप्त_विलंब();
    वायर्ड_नोंदणीस्थाने(GENET_SYS_RBUF_FLUSH_CTRL) = प्रारंभिक_राज्य & ~GENET_SYS_RBUF_FLUSH_RESET; संक्षिप्त_विलंब();
    वायर्ड_नोंदणीस्थाने(GENET_SYS_RBUF_FLUSH_CTRL) = 0; संक्षिप्त_विलंब();
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_CMD) = 0;
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; संक्षिप्त_विलंब();
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_CMD) = 0;
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_MIB_CTRL) = 7;
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_MIB_CTRL) = 0;
    वायर्ड_नोंदणीस्थाने(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (तयार_करणे_भौतिक() < 0) return ERR_IF;
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_MAC0) = (uint32_t)पत्ता[0] << 24 | (uint32_t)पत्ता[1] << 16 | पत्ता[2] << 8 | पत्ता[3];
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_MAC1) = पत्ता[4] << 8 | पत्ता[5];
    तयार_करणे_लूप(GENET_TX_BASE); तयार_करणे_लूप(GENET_RX_BASE);
    for (unsigned क्रमांक_अनुक्रमणिका = 0; क्रमांक_अनुक्रमणिका < लूप_संख्या; क्रमांक_अनुक्रमणिका++) स्वीकारणे_पत्ता(क्रमांक_अनुक्रमणिका);
    समन्वय_साधा();
    वायर्ड_नोंदणीस्थाने(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(लूप_संख्या_e7119cc7);
    वायर्ड_नोंदणीस्थाने(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(लूप_संख्या_e7119cc7);
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    वायर्ड_नोंदणीस्थाने(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    वायर्ड_नोंदणीस्थाने(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_MDF_CTRL) = 0;
    वायर्ड_नोंदणीस्थाने(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    मोबाइल_मूल्य->name[0] = 'e'; मोबाइल_मूल्य->name[1] = 'n'; मोबाइल_मूल्य->mtu = 1500;
    मोबाइल_मूल्य->hwaddr_len = 6; memcpy(मोबाइल_मूल्य->hwaddr, पत्ता, 6);
    मोबाइल_मूल्य->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    मोबाइल_मूल्य->output = etharp_output; मोबाइल_मूल्य->linkoutput = स्वतंत्रसंदेश_पाठवा;
    वायर्ड_मूल्य.तयार_करणे = 1;
    return ERR_OK;
}
void तपासा_वायर्ड_संचारजाळे(struct netif *मोबाइल_मूल्य) {
    if (!वायर्ड_मूल्य.तयार_करणे) return;
    uintptr_t आत्ता_मूल्य = बोर्ड_मिलिसेकंद();
    if (आत्ता_मूल्य >= वायर्ड_मूल्य.पुढील_आयटम_पडताळा) {
        वायर्ड_मूल्य.पुढील_आयटम_पडताळा = आत्ता_मूल्य + 500;
        भौतिक_वाचा(BRGPHY_MII_BMSR);
        int राज्य_मूल्य = भौतिक_वाचा(BRGPHY_MII_BMSR), सहायक_मूल्य = भौतिक_वाचा(BRGPHY_MII_AUXSTS);
        unsigned पद्धत_मोड = सहायक_मूल्य < 0 ? 0 : (सहायक_मूल्य & BRGPHY_AUXSTS_AN_RES) >> 8;
        int वेग_मूल्य = पद्धत_मोड == 7 ? 1000 : पद्धत_मोड == 5 ? 100 : पद्धत_मोड == 2 ? 10 : 0;
        वायर्ड_मूल्य.वेग_मूल्य = राज्य_मूल्य >= 0 && (राज्य_मूल्य & BRGPHY_BMSR_LINK) ? वेग_मूल्य : 0;
        if (वायर्ड_मूल्य.वेग_मूल्य) {
            uint32_t संयोजना = वायर्ड_नोंदणीस्थाने(GENET_EXT_RGMII_OOB_CTRL);
            संयोजना &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            वायर्ड_नोंदणीस्थाने(GENET_EXT_RGMII_OOB_CTRL) = संयोजना | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            संयोजना = वायर्ड_नोंदणीस्थाने(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            वायर्ड_नोंदणीस्थाने(GENET_UMAC_CMD) = संयोजना | (वेग_मूल्य == 1000 ? GENET_UMAC_CMD_SPEED_1000 : वेग_मूल्य == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(मोबाइल_मूल्य)) netif_set_link_up(मोबाइल_मूल्य);
        } else if (netif_is_link_up(मोबाइल_मूल्य)) netif_set_link_down(मोबाइल_मूल्य);
    }
    uint16_t निर्माणकरा_मूल्य = वायर्ड_नोंदणीस्थाने(GENET_RX_DMA_PROD_INDEX(लूप_संख्या_e7119cc7));
    unsigned बाकी_डेटा = (uint16_t)(निर्माणकरा_मूल्य - वायर्ड_मूल्य.वापरा_मूल्य);
    if (बाकी_डेटा > लूप_संख्या) { वायर्ड_मूल्य.सांख्यिकी_मूल्य[4]++; return; }
    for (unsigned लूप_क्रमांक = 0; लूप_क्रमांक < बाकी_डेटा && लूप_क्रमांक < 32; लूप_क्रमांक++) {
        unsigned स्थान_अनुक्रमणिका = वायर्ड_मूल्य.वापरा_मूल्य % लूप_संख्या;
        समन्वय_साधा();
        uint32_t राज्य_मूल्य = वायर्ड_नोंदणीस्थाने(GENET_RX_DESC_STATUS(स्थान_अनुक्रमणिका));
        unsigned लांबी_मूल्य = (राज्य_मूल्य & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t सीमा_मूल्य = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((राज्य_मूल्य & (सीमा_मूल्य | GENET_RX_DESC_STATUS_RX_ERROR)) != सीमा_मूल्य || लांबी_मूल्य < 16 || लांबी_मूल्य > 1538) वायर्ड_मूल्य.सांख्यिकी_मूल्य[4]++;
        else {
            सुबक_कॅशे(वायर्ड_मूल्य.स्वीकारा[स्थान_अनुक्रमणिका], लांबी_मूल्य, 1);
            struct pbuf *डेटा = pbuf_alloc(PBUF_RAW, लांबी_मूल्य - 2, PBUF_POOL);
            if (!डेटा) वायर्ड_मूल्य.सांख्यिकी_मूल्य[4]++;
            else if (pbuf_take(डेटा, वायर्ड_मूल्य.स्वीकारा[स्थान_अनुक्रमणिका] + 2, लांबी_मूल्य - 2) != ERR_OK || मोबाइल_मूल्य->input(डेटा, मोबाइल_मूल्य) != ERR_OK) {
                pbuf_free(डेटा); वायर्ड_मूल्य.सांख्यिकी_मूल्य[4]++;
            } else { वायर्ड_मूल्य.सांख्यिकी_मूल्य[0]++; वायर्ड_मूल्य.सांख्यिकी_मूल्य[1] += लांबी_मूल्य - 2; }
        }
        स्वीकारणे_पत्ता(स्थान_अनुक्रमणिका); समन्वय_साधा(); वायर्ड_मूल्य.वापरा_मूल्य++;
        वायर्ड_नोंदणीस्थाने(GENET_RX_DMA_CONS_INDEX(लूप_संख्या_e7119cc7)) = वायर्ड_मूल्य.वापरा_मूल्य;
    }
}
uint32_t वायर्ड_संचारजाळे_सांख्यिकी(unsigned प्रविष्टी_मूल्य) {
    return प्रविष्टी_मूल्य < 5 ? वायर्ड_मूल्य.सांख्यिकी_मूल्य[प्रविष्टी_मूल्य] : प्रविष्टी_मूल्य == 5 ? वायर्ड_मूल्य.वेग_मूल्य : प्रविष्टी_मूल्य == 6 ? वायर्ड_मूल्य.तयार_करणे : 0;
}
