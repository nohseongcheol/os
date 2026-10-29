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
#include "പരസ്പരബന്ധിതമായ_നെറ്റ്_വർക്ക്.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int ബോർഡ്_മെഷീൻ_ഇമെയിൽ(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ഇമെയിൽ) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ഇമെയിൽ)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, ബഫറിന്_റെ_വലുപ്പം = 2048 };
static struct {
    unsigned char 받기[고리개수][ബഫറിന്_റെ_വലുപ്പം];
    unsigned char അയയ്ക്കുക[고리개수][ബഫറിന്_റെ_വലുപ്പം];
    uint16_t 소비, 생산;
    int 물리주소, തയ്യാറാക്കുക, 속도;
    uint32_t 집계[5];
    uintptr_t പരിശോധിക്കുക_അടുത്തത്_ഇനം;
} പരസ്പരബന്ധിതമായ_മൂല്യം __attribute__((aligned(64)));

static void സമന്വയിപ്പിക്കുക(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void ക്ലീൻ_കാഷെ(void *ഡാറ്റാ, unsigned ദൈര്_ഘ്യം_മൂല്യം, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ഡാറ്റാ + ദൈര്_ഘ്യം_മൂല്യം;
    for (uintptr_t ഇമെയിൽ = (uintptr_t)ഡാറ്റാ & ~(uintptr_t)63; ഇമെയിൽ < 끝; ഇമെയിൽ += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ഇമെയിൽ) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ഇമെയിൽ) : "memory");
    }
#else
    (void)ഡാറ്റാ; (void)ദൈര്_ഘ്യം_മൂല്യം; (void)받기;
#endif
    സമന്വയിപ്പിക്കുക();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ഇമെയിൽ, unsigned സൂചിക, int എഴുത്തു്, unsigned മൂല്യം) {
    uint32_t ആജ്ഞ = (എഴുത്തു് ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ഇമെയിൽ << GENET_MDIO_ADDR_SHIFT) | (സൂചിക << GENET_MDIO_REG_SHIFT) | (മൂല്യം & 65535);
    유선저장기(GENET_MDIO_CMD) = ആജ്ഞ;
    유선저장기(GENET_MDIO_CMD) = ആജ്ഞ | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t അവസ്ഥ_മൂല്യം = 유선저장기(GENET_MDIO_CMD);
        if (!(അവസ്ഥ_മൂല്യം & GENET_MDIO_START_BUSY))
            return അവസ്ഥ_മൂല്യം & GENET_MDIO_READ_FAILED ? -1 : (int)(അവസ്ഥ_മൂല്യം & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned സൂചിക) { return 물리전송(പരസ്പരബന്ധിതമായ_മൂല്യം.물리주소, സൂചിക, 0, 0); }
static int 물리쓰기(unsigned സൂചിക, unsigned മൂല്യം) { return 물리전송(പരസ്പരബന്ധിതമായ_മൂല്യം.물리주소, സൂചിക, 1, മൂല്യം); }
static int 물리준비(void) {
    പരസ്പരബന്ധിതമായ_മൂല്യം.물리주소 = -1;
    for (unsigned ഇമെയിൽ = 0; ഇമെയിൽ < 32; ഇമെയിൽ++) {
        int 식별 = 물리전송(ഇമെയിൽ, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { പരസ്പരബന്ധിതമായ_മൂല്യം.물리주소 = ഇമെയിൽ; break; }
    }
    if (പരസ്പരബന്ധിതമായ_മൂല്യം.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int മൂല്യം = 물리읽기(BRGPHY_MII_AUXCTL);
    if (മൂല്യം < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (മൂല്യം & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    മൂല്യം = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (മൂല്യം < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (മൂല്യം & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void തയ്യാറാക്കുക_ലൂപ്(unsigned నేపథ్యం_മൂല്യം) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ലൂപ്_മൂല്യം = నేపథ్యం_മൂല്യം + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned സ്ഥാനം = 0; സ്ഥാനം <= 0x30; സ്ഥാനം += 4) 유선저장기(ലൂപ്_മൂല്യം + സ്ഥാനം) = 0;
    유선저장기(ലൂപ്_മൂല്യം + 0x10) = (고리개수 << 16) | ബഫറിന്_റെ_വലുപ്പം;
    유선저장기(ലൂപ്_മൂല്യം + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (నేపథ్యం_മൂല്യം == GENET_RX_BASE) 유선저장기(ലൂപ്_മൂല്യം + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ലൂപ്_മൂല്യം + 0x24) = 1;
    유선저장기(నేపథ్యం_മൂല്യം + 0x104c) = 8;
    유선저장기(నేపథ్యం_മൂല്യം + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned പദവി_സൂചിക) {
    uintptr_t ഇമെയിൽ = (uintptr_t)പരസ്പരബന്ധിതമായ_മൂല്യം.받기[പദവി_സൂചിക];
    ക്ലീൻ_കാഷെ((void *)ഇമെയിൽ, ബഫറിന്_റെ_വലുപ്പം, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(പദവി_സൂചിക)) = (uint32_t)ഇമെയിൽ;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(പദവി_സൂചിക)) = (uint64_t)ഇമെയിൽ >> 32;
    유선저장기(GENET_RX_DESC_STATUS(പദവി_സൂചിക)) = ബഫറിന്_റെ_വലുപ്പം << 16;
}
static err_t 전문보내기(struct netif *മൊബൈൽ_മൂല്യം, struct pbuf *전문) {
    if (!പരസ്പരബന്ധിതമായ_മൂല്യം.തയ്യാറാക്കുക || !netif_is_link_up(മൊബൈൽ_മൂല്യം)) return ERR_RTE;
    unsigned വലിപ്പം = 전문->tot_len;
    if (!വലിപ്പം || വലിപ്പം > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(പരസ്പരബന്ധിതമായ_മൂല്യം.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned പദവി_സൂചിക = പരസ്പരബന്ധിതമായ_മൂല്യം.생산 % 고리개수, 송신길이 = വലിപ്പം < 60 ? 60 : വലിപ്പം;
    unsigned char *ഡാറ്റാ = പരസ്പരബന്ധിതമായ_മൂല്യം.അയയ്ക്കുക[പദവി_സൂചിക];
    memset(ഡാറ്റാ, 0, 송신길이);
    if (pbuf_copy_partial(전문, ഡാറ്റാ, വലിപ്പം, 0) != വലിപ്പം) return ERR_BUF;
    ക്ലീൻ_കാഷെ(ഡാറ്റാ, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(പദവി_സൂചിക)) = (uint32_t)(uintptr_t)ഡാറ്റാ;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(പദവി_സൂചിക)) = (uint64_t)(uintptr_t)ഡാറ്റാ >> 32;
    유선저장기(GENET_TX_DESC_STATUS(പദവി_സൂചിക)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    സമന്വയിപ്പിക്കുക();
    പരസ്പരബന്ധിതമായ_മൂല്യം.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = പരസ്പരബന്ധിതമായ_മൂല്യം.생산;
    പരസ്പരബന്ധിതമായ_മൂല്യം.집계[2]++; പരസ്പരബന്ധിതമായ_മൂല്യം.집계[3] += വലിപ്പം;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t തയ്യാറാക്കുക_പരസ്പരബന്ധിതമായ_നെറ്റ്_വർക്ക്(struct netif *മൊബൈൽ_മൂല്യം) {
    unsigned char ഇമെയിൽ[6];
    if (!유선장치있음() || !ബോർഡ്_മെഷീൻ_ഇമെയിൽ(ഇമെയിൽ) || (ഇമെയിൽ[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= ഇമെയിൽ[순번];
    if (!합) return ERR_IF;
    memset(&പരസ്പരബന്ധിതമായ_മൂല്യം, 0, sizeof(പരസ്പരബന്ധിതമായ_മൂല്യം));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ഇമെയിൽ[0] << 24 | (uint32_t)ഇമെയിൽ[1] << 16 | ഇമെയിൽ[2] << 8 | ഇമെയിൽ[3];
    유선저장기(GENET_UMAC_MAC1) = ഇമെയിൽ[4] << 8 | ഇമെയിൽ[5];
    തയ്യാറാക്കുക_ലൂപ്(GENET_TX_BASE); തയ്യാറാക്കുക_ലൂപ്(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    സമന്വയിപ്പിക്കുക();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    മൊബൈൽ_മൂല്യം->name[0] = 'e'; മൊബൈൽ_മൂല്യം->name[1] = 'n'; മൊബൈൽ_മൂല്യം->mtu = 1500;
    മൊബൈൽ_മൂല്യം->hwaddr_len = 6; memcpy(മൊബൈൽ_മൂല്യം->hwaddr, ഇമെയിൽ, 6);
    മൊബൈൽ_മൂല്യം->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    മൊബൈൽ_മൂല്യം->output = etharp_output; മൊബൈൽ_മൂല്യം->linkoutput = 전문보내기;
    പരസ്പരബന്ധിതമായ_മൂല്യം.തയ്യാറാക്കുക = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *മൊബൈൽ_മൂല്യം) {
    if (!പരസ്പരബന്ധിതമായ_മൂല്യം.തയ്യാറാക്കുക) return;
    uintptr_t ഇപ്പോൾ_മൂല്യം = 보드밀리초();
    if (ഇപ്പോൾ_മൂല്യം >= പരസ്പരബന്ധിതമായ_മൂല്യം.പരിശോധിക്കുക_അടുത്തത്_ഇനം) {
        പരസ്പരബന്ധിതമായ_മൂല്യം.പരിശോധിക്കുക_അടുത്തത്_ഇനം = ഇപ്പോൾ_മൂല്യം + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int അവസ്ഥ_മൂല്യം = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned విధానం_മോഡ് = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = విధానం_മോഡ് == 7 ? 1000 : విధానం_മോഡ് == 5 ? 100 : విధానం_മോഡ് == 2 ? 10 : 0;
        പരസ്പരബന്ധിതമായ_മൂല്യം.속도 = അവസ്ഥ_മൂല്യം >= 0 && (അവസ്ഥ_മൂല്യം & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (പരസ്പരബന്ധിതമായ_മൂല്യം.속도) {
            uint32_t സജ്ജീകരണം = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            സജ്ജീകരണം &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = സജ്ജീകരണം | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            സജ്ജീകരണം = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = സജ്ജീകരണം | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(മൊബൈൽ_മൂല്യം)) netif_set_link_up(മൊബൈൽ_മൂല്യം);
        } else if (netif_is_link_up(മൊബൈൽ_മൂല്യം)) netif_set_link_down(മൊബൈൽ_മൂല്യം);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - പരസ്പരബന്ധിതമായ_മൂല്യം.소비);
    if (남음 > 고리개수) { പരസ്പരബന്ധിതമായ_മൂല്യം.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned പദവി_സൂചിക = പരസ്പരബന്ധിതമായ_മൂല്യം.소비 % 고리개수;
        സമന്വയിപ്പിക്കുക();
        uint32_t അവസ്ഥ_മൂല്യം = 유선저장기(GENET_RX_DESC_STATUS(പദവി_സൂചിക));
        unsigned ദൈര്_ഘ്യം_മൂല്യം = (അവസ്ഥ_മൂല്യം & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((അവസ്ഥ_മൂല്യം & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || ദൈര്_ഘ്യം_മൂല്യം < 16 || ദൈര്_ഘ്യം_മൂല്യം > 1538) പരസ്പരബന്ധിതമായ_മൂല്യം.집계[4]++;
        else {
            ക്ലീൻ_കാഷെ(പരസ്പരബന്ധിതമായ_മൂല്യം.받기[പദവി_സൂചിക], ദൈര്_ഘ്യം_മൂല്യം, 1);
            struct pbuf *ഡാറ്റാ = pbuf_alloc(PBUF_RAW, ദൈര്_ഘ്യം_മൂല്യം - 2, PBUF_POOL);
            if (!ഡാറ്റാ) പരസ്പരബന്ധിതമായ_മൂല്യം.집계[4]++;
            else if (pbuf_take(ഡാറ്റാ, പരസ്പരബന്ധിതമായ_മൂല്യം.받기[പദവി_സൂചിക] + 2, ദൈര്_ഘ്യം_മൂല്യം - 2) != ERR_OK || മൊബൈൽ_മൂല്യം->input(ഡാറ്റാ, മൊബൈൽ_മൂല്യം) != ERR_OK) {
                pbuf_free(ഡാറ്റാ); പരസ്പരബന്ധിതമായ_മൂല്യം.집계[4]++;
            } else { പരസ്പരബന്ധിതമായ_മൂല്യം.집계[0]++; പരസ്പരബന്ധിതമായ_മൂല്യം.집계[1] += ദൈര്_ഘ്യം_മൂല്യം - 2; }
        }
        받는주소(പദവി_സൂചിക); സമന്വയിപ്പിക്കുക(); പരസ്പരബന്ധിതമായ_മൂല്യം.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = പരസ്പരബന്ധിതമായ_മൂല്യം.소비;
    }
}
uint32_t 유선망집계(unsigned എന്_ട്രി_മൂല്യം) {
    return എന്_ട്രി_മൂല്യം < 5 ? പരസ്പരബന്ധിതമായ_മൂല്യം.집계[എന്_ട്രി_മൂല്യം] : എന്_ട്രി_മൂല്യം == 5 ? പരസ്പരബന്ധിതമായ_മൂല്യം.속도 : എന്_ട്രി_മൂല്യം == 6 ? പരസ്പരബന്ധിതമായ_മൂല്യം.തയ്യാറാക്കുക : 0;
}
