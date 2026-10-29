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
#include "קווי_רשת.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int לוח_כתובת_ממשית(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(למען) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (למען)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, מאגר_גודל = 2048 };
static struct {
    unsigned char לקבל[고리개수][מאגר_גודל];
    unsigned char שלח[고리개수][מאגר_גודל];
    uint16_t לצרוך_ערך, 생산;
    int 물리주소, להכין, 속도;
    uint32_t 집계[5];
    uintptr_t ודא_אמת_הבא_פריט;
} קווי_ערך __attribute__((aligned(64)));

static void סנכרן(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void נקי_מטמון(void *נתונים, unsigned 길이, int לקבל) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)נתונים + 길이;
    for (uintptr_t למען = (uintptr_t)נתונים & ~(uintptr_t)63; למען < 끝; למען += 64) {
        if (לקבל) __asm__ volatile("dc ivac, %0" :: "r"(למען) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(למען) : "memory");
    }
#else
    (void)נתונים; (void)길이; (void)לקבל;
#endif
    סנכרן();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned למען, unsigned מדד, int כתוב, unsigned ערך) {
    uint32_t פקודה = (כתוב ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (למען << GENET_MDIO_ADDR_SHIFT) | (מדד << GENET_MDIO_REG_SHIFT) | (ערך & 65535);
    유선저장기(GENET_MDIO_CMD) = פקודה;
    유선저장기(GENET_MDIO_CMD) = פקודה | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t מצב_ערך = 유선저장기(GENET_MDIO_CMD);
        if (!(מצב_ערך & GENET_MDIO_START_BUSY))
            return מצב_ערך & GENET_MDIO_READ_FAILED ? -1 : (int)(מצב_ערך & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned מדד) { return 물리전송(קווי_ערך.물리주소, מדד, 0, 0); }
static int 물리쓰기(unsigned מדד, unsigned ערך) { return 물리전송(קווי_ערך.물리주소, מדד, 1, ערך); }
static int 물리준비(void) {
    קווי_ערך.물리주소 = -1;
    for (unsigned למען = 0; למען < 32; למען++) {
        int 식별 = 물리전송(למען, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { קווי_ערך.물리주소 = למען; break; }
    }
    if (קווי_ערך.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ערך = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ערך < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ערך & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ערך = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ערך < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ערך & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void להכין_לולאה(unsigned טפט_ערך) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned לולאה_ערך = טפט_ערך + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned מיקום = 0; מיקום <= 0x30; מיקום += 4) 유선저장기(לולאה_ערך + מיקום) = 0;
    유선저장기(לולאה_ערך + 0x10) = (고리개수 << 16) | מאגר_גודל;
    유선저장기(לולאה_ערך + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (טפט_ערך == GENET_RX_BASE) 유선저장기(לולאה_ערך + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(לולאה_ערך + 0x24) = 1;
    유선저장기(טפט_ערך + 0x104c) = 8;
    유선저장기(טפט_ערך + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned עמדה_מדד) {
    uintptr_t למען = (uintptr_t)קווי_ערך.לקבל[עמדה_מדד];
    נקי_מטמון((void *)למען, מאגר_גודל, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(עמדה_מדד)) = (uint32_t)למען;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(עמדה_מדד)) = (uint64_t)למען >> 32;
    유선저장기(GENET_RX_DESC_STATUS(עמדה_מדד)) = מאגר_גודל << 16;
}
static err_t שלח_יחידת_נתונים(struct netif *התקן_ערך_e13f0cd9, struct pbuf *יחידת_נתונים) {
    if (!קווי_ערך.להכין || !netif_is_link_up(התקן_ערך_e13f0cd9)) return ERR_RTE;
    unsigned גודל = יחידת_נתונים->tot_len;
    if (!גודל || גודל > 1536) return ERR_BUF;
    uint16_t לצרוך_ערך = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(קווי_ערך.생산 - לצרוך_ערך) >= 고리개수 - 1) return ERR_MEM;
    unsigned עמדה_מדד = קווי_ערך.생산 % 고리개수, 송신길이 = גודל < 60 ? 60 : גודל;
    unsigned char *נתונים = קווי_ערך.שלח[עמדה_מדד];
    memset(נתונים, 0, 송신길이);
    if (pbuf_copy_partial(יחידת_נתונים, נתונים, גודל, 0) != גודל) return ERR_BUF;
    נקי_מטמון(נתונים, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(עמדה_מדד)) = (uint32_t)(uintptr_t)נתונים;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(עמדה_מדד)) = (uint64_t)(uintptr_t)נתונים >> 32;
    유선저장기(GENET_TX_DESC_STATUS(עמדה_מדד)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    סנכרן();
    קווי_ערך.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = קווי_ערך.생산;
    קווי_ערך.집계[2]++; קווי_ערך.집계[3] += גודל;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t להכין_קווי_רשת(struct netif *התקן_ערך_e13f0cd9) {
    unsigned char למען[6];
    if (!유선장치있음() || !לוח_כתובת_ממשית(למען) || (למען[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= למען[순번];
    if (!합) return ERR_IF;
    memset(&קווי_ערך, 0, sizeof(קווי_ערך));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t מצב_התחלתי = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = מצב_התחלתי | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = מצב_התחלתי & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)למען[0] << 24 | (uint32_t)למען[1] << 16 | למען[2] << 8 | למען[3];
    유선저장기(GENET_UMAC_MAC1) = למען[4] << 8 | למען[5];
    להכין_לולאה(GENET_TX_BASE); להכין_לולאה(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    סנכרן();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    התקן_ערך_e13f0cd9->name[0] = 'e'; התקן_ערך_e13f0cd9->name[1] = 'n'; התקן_ערך_e13f0cd9->mtu = 1500;
    התקן_ערך_e13f0cd9->hwaddr_len = 6; memcpy(התקן_ערך_e13f0cd9->hwaddr, למען, 6);
    התקן_ערך_e13f0cd9->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    התקן_ערך_e13f0cd9->output = etharp_output; התקן_ערך_e13f0cd9->linkoutput = שלח_יחידת_נתונים;
    קווי_ערך.להכין = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *התקן_ערך_e13f0cd9) {
    if (!קווי_ערך.להכין) return;
    uintptr_t עכשיו_ערך = 보드밀리초();
    if (עכשיו_ערך >= קווי_ערך.ודא_אמת_הבא_פריט) {
        קווי_ערך.ודא_אמת_הבא_פריט = עכשיו_ערך + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int מצב_ערך = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned פעולת_שירות_מצב = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = פעולת_שירות_מצב == 7 ? 1000 : פעולת_שירות_מצב == 5 ? 100 : פעולת_שירות_מצב == 2 ? 10 : 0;
        קווי_ערך.속도 = מצב_ערך >= 0 && (מצב_ערך & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (קווי_ערך.속도) {
            uint32_t הגדרות = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            הגדרות &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = הגדרות | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            הגדרות = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = הגדרות | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(התקן_ערך_e13f0cd9)) netif_set_link_up(התקן_ערך_e13f0cd9);
        } else if (netif_is_link_up(התקן_ערך_e13f0cd9)) netif_set_link_down(התקן_ערך_e13f0cd9);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - קווי_ערך.לצרוך_ערך);
    if (남음 > 고리개수) { קווי_ערך.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned עמדה_מדד = קווי_ערך.לצרוך_ערך % 고리개수;
        סנכרן();
        uint32_t מצב_ערך = 유선저장기(GENET_RX_DESC_STATUS(עמדה_מדד));
        unsigned 길이 = (מצב_ערך & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((מצב_ערך & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || 길이 < 16 || 길이 > 1538) קווי_ערך.집계[4]++;
        else {
            נקי_מטמון(קווי_ערך.לקבל[עמדה_מדד], 길이, 1);
            struct pbuf *נתונים = pbuf_alloc(PBUF_RAW, 길이 - 2, PBUF_POOL);
            if (!נתונים) קווי_ערך.집계[4]++;
            else if (pbuf_take(נתונים, קווי_ערך.לקבל[עמדה_מדד] + 2, 길이 - 2) != ERR_OK || התקן_ערך_e13f0cd9->input(נתונים, התקן_ערך_e13f0cd9) != ERR_OK) {
                pbuf_free(נתונים); קווי_ערך.집계[4]++;
            } else { קווי_ערך.집계[0]++; קווי_ערך.집계[1] += 길이 - 2; }
        }
        받는주소(עמדה_מדד); סנכרן(); קווי_ערך.לצרוך_ערך++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = קווי_ערך.לצרוך_ערך;
    }
}
uint32_t 유선망집계(unsigned ערך_ערך) {
    return ערך_ערך < 5 ? קווי_ערך.집계[ערך_ערך] : ערך_ערך == 5 ? קווי_ערך.속도 : ערך_ערך == 6 ? קווי_ערך.להכין : 0;
}
