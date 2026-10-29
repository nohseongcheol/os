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
#include "แบบผ่านสาย_เครือข่าย.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int บอร์ด_เลขที่อยู่จริง(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(อีเมล) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (อีเมล)))
#endif
enum { วน_หมายเลข = 16, 고리개수 = 256, ขนาดบัฟเฟอร์ = 2048 };
static struct {
    unsigned char รับ[고리개수][ขนาดบัฟเฟอร์];
    unsigned char ส่ง[고리개수][ขนาดบัฟเฟอร์];
    uint16_t ใช้_ค่า_84aa75c8, 생산;
    int 물리주소, จัดเตรียม, 속도;
    uint32_t 집계[5];
    uintptr_t ยืนยัน_ถัดไป_รายการ;
} แบบผ่านสาย_ค่า __attribute__((aligned(64)));

static void ซิงค์(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void สะอาดตา_แคช(void *ข้อมูล, unsigned 길이, int รับ) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ข้อมูล + 길이;
    for (uintptr_t อีเมล = (uintptr_t)ข้อมูล & ~(uintptr_t)63; อีเมล < 끝; อีเมล += 64) {
        if (รับ) __asm__ volatile("dc ivac, %0" :: "r"(อีเมล) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(อีเมล) : "memory");
    }
#else
    (void)ข้อมูล; (void)길이; (void)รับ;
#endif
    ซิงค์();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned อีเมล, unsigned ดัชนี, int เขียน, unsigned ค่า) {
    uint32_t คําสั่ง = (เขียน ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (อีเมล << GENET_MDIO_ADDR_SHIFT) | (ดัชนี << GENET_MDIO_REG_SHIFT) | (ค่า & 65535);
    유선저장기(GENET_MDIO_CMD) = คําสั่ง;
    유선저장기(GENET_MDIO_CMD) = คําสั่ง | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t สถานะ_ค่า = 유선저장기(GENET_MDIO_CMD);
        if (!(สถานะ_ค่า & GENET_MDIO_START_BUSY))
            return สถานะ_ค่า & GENET_MDIO_READ_FAILED ? -1 : (int)(สถานะ_ค่า & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ดัชนี) { return 물리전송(แบบผ่านสาย_ค่า.물리주소, ดัชนี, 0, 0); }
static int 물리쓰기(unsigned ดัชนี, unsigned ค่า) { return 물리전송(แบบผ่านสาย_ค่า.물리주소, ดัชนี, 1, ค่า); }
static int 물리준비(void) {
    แบบผ่านสาย_ค่า.물리주소 = -1;
    for (unsigned อีเมล = 0; อีเมล < 32; อีเมล++) {
        int 식별 = 물리전송(อีเมล, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { แบบผ่านสาย_ค่า.물리주소 = อีเมล; break; }
    }
    if (แบบผ่านสาย_ค่า.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ค่า = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ค่า < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ค่า & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ค่า = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ค่า < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ค่า & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void จัดเตรียม_วน(unsigned พื้นหลัง_ค่า) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned วน_ค่า = พื้นหลัง_ค่า + 0xc00 + GENET_DMA_RING_SIZE * วน_หมายเลข;
    for (unsigned ตําแหน่ง = 0; ตําแหน่ง <= 0x30; ตําแหน่ง += 4) 유선저장기(วน_ค่า + ตําแหน่ง) = 0;
    유선저장기(วน_ค่า + 0x10) = (고리개수 << 16) | ขนาดบัฟเฟอร์;
    유선저장기(วน_ค่า + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (พื้นหลัง_ค่า == GENET_RX_BASE) 유선저장기(วน_ค่า + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(วน_ค่า + 0x24) = 1;
    유선저장기(พื้นหลัง_ค่า + 0x104c) = 8;
    유선저장기(พื้นหลัง_ค่า + 0x1040) = __BIT(วน_หมายเลข);
}
static void 받는주소(unsigned ดัชนีชี้ตําแหน่ง) {
    uintptr_t อีเมล = (uintptr_t)แบบผ่านสาย_ค่า.รับ[ดัชนีชี้ตําแหน่ง];
    สะอาดตา_แคช((void *)อีเมล, ขนาดบัฟเฟอร์, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(ดัชนีชี้ตําแหน่ง)) = (uint32_t)อีเมล;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(ดัชนีชี้ตําแหน่ง)) = (uint64_t)อีเมล >> 32;
    유선저장기(GENET_RX_DESC_STATUS(ดัชนีชี้ตําแหน่ง)) = ขนาดบัฟเฟอร์ << 16;
}
static err_t ส่ง_เดตาแกรม(struct netif *อุปกรณ์_ค่า, struct pbuf *เดตาแกรม) {
    if (!แบบผ่านสาย_ค่า.จัดเตรียม || !netif_is_link_up(อุปกรณ์_ค่า)) return ERR_RTE;
    unsigned ขนาด = เดตาแกรม->tot_len;
    if (!ขนาด || ขนาด > 1536) return ERR_BUF;
    uint16_t ใช้_ค่า_84aa75c8 = 유선저장기(GENET_TX_DMA_CONS_INDEX(วน_หมายเลข));
    if ((uint16_t)(แบบผ่านสาย_ค่า.생산 - ใช้_ค่า_84aa75c8) >= 고리개수 - 1) return ERR_MEM;
    unsigned ดัชนีชี้ตําแหน่ง = แบบผ่านสาย_ค่า.생산 % 고리개수, 송신길이 = ขนาด < 60 ? 60 : ขนาด;
    unsigned char *ข้อมูล = แบบผ่านสาย_ค่า.ส่ง[ดัชนีชี้ตําแหน่ง];
    memset(ข้อมูล, 0, 송신길이);
    if (pbuf_copy_partial(เดตาแกรม, ข้อมูล, ขนาด, 0) != ขนาด) return ERR_BUF;
    สะอาดตา_แคช(ข้อมูล, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(ดัชนีชี้ตําแหน่ง)) = (uint32_t)(uintptr_t)ข้อมูล;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(ดัชนีชี้ตําแหน่ง)) = (uint64_t)(uintptr_t)ข้อมูล >> 32;
    유선저장기(GENET_TX_DESC_STATUS(ดัชนีชี้ตําแหน่ง)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    ซิงค์();
    แบบผ่านสาย_ค่า.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(วน_หมายเลข)) = แบบผ่านสาย_ค่า.생산;
    แบบผ่านสาย_ค่า.집계[2]++; แบบผ่านสาย_ค่า.집계[3] += ขนาด;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t จัดเตรียม_แบบผ่านสาย_เครือข่าย(struct netif *อุปกรณ์_ค่า) {
    unsigned char อีเมล[6];
    if (!유선장치있음() || !บอร์ด_เลขที่อยู่จริง(อีเมล) || (อีเมล[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= อีเมล[순번];
    if (!합) return ERR_IF;
    memset(&แบบผ่านสาย_ค่า, 0, sizeof(แบบผ่านสาย_ค่า));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t สภาวะเริ่มต้น = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = สภาวะเริ่มต้น | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = สภาวะเริ่มต้น & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)อีเมล[0] << 24 | (uint32_t)อีเมล[1] << 16 | อีเมล[2] << 8 | อีเมล[3];
    유선저장기(GENET_UMAC_MAC1) = อีเมล[4] << 8 | อีเมล[5];
    จัดเตรียม_วน(GENET_TX_BASE); จัดเตรียม_วน(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    ซิงค์();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(วน_หมายเลข);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(วน_หมายเลข);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    อุปกรณ์_ค่า->name[0] = 'e'; อุปกรณ์_ค่า->name[1] = 'n'; อุปกรณ์_ค่า->mtu = 1500;
    อุปกรณ์_ค่า->hwaddr_len = 6; memcpy(อุปกรณ์_ค่า->hwaddr, อีเมล, 6);
    อุปกรณ์_ค่า->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    อุปกรณ์_ค่า->output = etharp_output; อุปกรณ์_ค่า->linkoutput = ส่ง_เดตาแกรม;
    แบบผ่านสาย_ค่า.จัดเตรียม = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *อุปกรณ์_ค่า) {
    if (!แบบผ่านสาย_ค่า.จัดเตรียม) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= แบบผ่านสาย_ค่า.ยืนยัน_ถัดไป_รายการ) {
        แบบผ่านสาย_ค่า.ยืนยัน_ถัดไป_รายการ = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int สถานะ_ค่า = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned เมธอด_โหมด = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = เมธอด_โหมด == 7 ? 1000 : เมธอด_โหมด == 5 ? 100 : เมธอด_โหมด == 2 ? 10 : 0;
        แบบผ่านสาย_ค่า.속도 = สถานะ_ค่า >= 0 && (สถานะ_ค่า & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (แบบผ่านสาย_ค่า.속도) {
            uint32_t ตั้งค่า = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            ตั้งค่า &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = ตั้งค่า | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ตั้งค่า = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = ตั้งค่า | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(อุปกรณ์_ค่า)) netif_set_link_up(อุปกรณ์_ค่า);
        } else if (netif_is_link_up(อุปกรณ์_ค่า)) netif_set_link_down(อุปกรณ์_ค่า);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(วน_หมายเลข));
    unsigned 남음 = (uint16_t)(생산 - แบบผ่านสาย_ค่า.ใช้_ค่า_84aa75c8);
    if (남음 > 고리개수) { แบบผ่านสาย_ค่า.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned ดัชนีชี้ตําแหน่ง = แบบผ่านสาย_ค่า.ใช้_ค่า_84aa75c8 % 고리개수;
        ซิงค์();
        uint32_t สถานะ_ค่า = 유선저장기(GENET_RX_DESC_STATUS(ดัชนีชี้ตําแหน่ง));
        unsigned 길이 = (สถานะ_ค่า & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((สถานะ_ค่า & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || 길이 < 16 || 길이 > 1538) แบบผ่านสาย_ค่า.집계[4]++;
        else {
            สะอาดตา_แคช(แบบผ่านสาย_ค่า.รับ[ดัชนีชี้ตําแหน่ง], 길이, 1);
            struct pbuf *ข้อมูล = pbuf_alloc(PBUF_RAW, 길이 - 2, PBUF_POOL);
            if (!ข้อมูล) แบบผ่านสาย_ค่า.집계[4]++;
            else if (pbuf_take(ข้อมูล, แบบผ่านสาย_ค่า.รับ[ดัชนีชี้ตําแหน่ง] + 2, 길이 - 2) != ERR_OK || อุปกรณ์_ค่า->input(ข้อมูล, อุปกรณ์_ค่า) != ERR_OK) {
                pbuf_free(ข้อมูล); แบบผ่านสาย_ค่า.집계[4]++;
            } else { แบบผ่านสาย_ค่า.집계[0]++; แบบผ่านสาย_ค่า.집계[1] += 길이 - 2; }
        }
        받는주소(ดัชนีชี้ตําแหน่ง); ซิงค์(); แบบผ่านสาย_ค่า.ใช้_ค่า_84aa75c8++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(วน_หมายเลข)) = แบบผ่านสาย_ค่า.ใช้_ค่า_84aa75c8;
    }
}
uint32_t 유선망집계(unsigned รายการ_ค่า) {
    return รายการ_ค่า < 5 ? แบบผ่านสาย_ค่า.집계[รายการ_ค่า] : รายการ_ค่า == 5 ? แบบผ่านสาย_ค่า.속도 : รายการ_ค่า == 6 ? แบบผ่านสาย_ค่า.จัดเตรียม : 0;
}
