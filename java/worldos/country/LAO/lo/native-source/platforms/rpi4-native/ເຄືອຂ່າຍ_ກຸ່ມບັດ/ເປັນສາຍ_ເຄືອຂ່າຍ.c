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
#include "ເປັນສາຍ_ເຄືອຂ່າຍ.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int ກະດານ_ເຄື່ອງຈັກ_ອີເມວ(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(ອີເມວ) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (ອີເມວ)))
#endif
enum { 고리번호 = 16, 고리개수 = 256, ບ່ອນເກັບຊົ່ວຄາວ_ຂະ_ຫນາດ = 2048 };
static struct {
    unsigned char 받기[고리개수][ບ່ອນເກັບຊົ່ວຄາວ_ຂະ_ຫນາດ];
    unsigned char ສົ່ງ[고리개수][ບ່ອນເກັບຊົ່ວຄາວ_ຂະ_ຫນາດ];
    uint16_t 소비, 생산;
    int 물리주소, ກະ_ກຽມ, 속도;
    uint32_t 집계[5];
    uintptr_t 다음확인;
} ເປັນສາຍ_ຄ່າ __attribute__((aligned(64)));

static void ຊິງໂຄຣໄນ(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void ສະອາດ_ແຄຊ໌(void *ຂໍ້ມູນ, unsigned ຄວາມຍາວ_ຄ່າ, int 받기) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)ຂໍ້ມູນ + ຄວາມຍາວ_ຄ່າ;
    for (uintptr_t ອີເມວ = (uintptr_t)ຂໍ້ມູນ & ~(uintptr_t)63; ອີເມວ < 끝; ອີເມວ += 64) {
        if (받기) __asm__ volatile("dc ivac, %0" :: "r"(ອີເມວ) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(ອີເມວ) : "memory");
    }
#else
    (void)ຂໍ້ມູນ; (void)ຄວາມຍາວ_ຄ່າ; (void)받기;
#endif
    ຊິງໂຄຣໄນ();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned ອີເມວ, unsigned ດັດຊະນີ, int ຂຽນ, unsigned ຄ່າ) {
    uint32_t ຄໍາສັ່ງ_1f12b8e2 = (ຂຽນ ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (ອີເມວ << GENET_MDIO_ADDR_SHIFT) | (ດັດຊະນີ << GENET_MDIO_REG_SHIFT) | (ຄ່າ & 65535);
    유선저장기(GENET_MDIO_CMD) = ຄໍາສັ່ງ_1f12b8e2;
    유선저장기(GENET_MDIO_CMD) = ຄໍາສັ່ງ_1f12b8e2 | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t ສະຖານະ_ຄ່າ = 유선저장기(GENET_MDIO_CMD);
        if (!(ສະຖານະ_ຄ່າ & GENET_MDIO_START_BUSY))
            return ສະຖານະ_ຄ່າ & GENET_MDIO_READ_FAILED ? -1 : (int)(ສະຖານະ_ຄ່າ & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ດັດຊະນີ) { return 물리전송(ເປັນສາຍ_ຄ່າ.물리주소, ດັດຊະນີ, 0, 0); }
static int 물리쓰기(unsigned ດັດຊະນີ, unsigned ຄ່າ) { return 물리전송(ເປັນສາຍ_ຄ່າ.물리주소, ດັດຊະນີ, 1, ຄ່າ); }
static int 물리준비(void) {
    ເປັນສາຍ_ຄ່າ.물리주소 = -1;
    for (unsigned ອີເມວ = 0; ອີເມວ < 32; ອີເມວ++) {
        int 식별 = 물리전송(ອີເມວ, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { ເປັນສາຍ_ຄ່າ.물리주소 = ອີເມວ; break; }
    }
    if (ເປັນສາຍ_ຄ່າ.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int ຄ່າ = 물리읽기(BRGPHY_MII_AUXCTL);
    if (ຄ່າ < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (ຄ່າ & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    ຄ່າ = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (ຄ່າ < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (ຄ່າ & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void ກະ_ກຽມ_ຫ່ວງ(unsigned ພື້ນຫຼັງ_ຄ່າ) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned ຫ່ວງ_ຄ່າ = ພື້ນຫຼັງ_ຄ່າ + 0xc00 + GENET_DMA_RING_SIZE * 고리번호;
    for (unsigned ຈັດຕໍາແຫນ່ງ = 0; ຈັດຕໍາແຫນ່ງ <= 0x30; ຈັດຕໍາແຫນ່ງ += 4) 유선저장기(ຫ່ວງ_ຄ່າ + ຈັດຕໍາແຫນ່ງ) = 0;
    유선저장기(ຫ່ວງ_ຄ່າ + 0x10) = (고리개수 << 16) | ບ່ອນເກັບຊົ່ວຄາວ_ຂະ_ຫນາດ;
    유선저장기(ຫ່ວງ_ຄ່າ + 0x1c) = 고리개수 * GENET_DMA_DESC_SIZE / 4 - 1;
    if (ພື້ນຫຼັງ_ຄ່າ == GENET_RX_BASE) 유선저장기(ຫ່ວງ_ຄ່າ + 0x28) = (5 << 16) | (고리개수 >> 4);
    else 유선저장기(ຫ່ວງ_ຄ່າ + 0x24) = 1;
    유선저장기(ພື້ນຫຼັງ_ຄ່າ + 0x104c) = 8;
    유선저장기(ພື້ນຫຼັງ_ຄ່າ + 0x1040) = __BIT(고리번호);
}
static void 받는주소(unsigned ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ) {
    uintptr_t ອີເມວ = (uintptr_t)ເປັນສາຍ_ຄ່າ.받기[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ];
    ສະອາດ_ແຄຊ໌((void *)ອີເມວ, ບ່ອນເກັບຊົ່ວຄາວ_ຂະ_ຫນາດ, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ)) = (uint32_t)ອີເມວ;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ)) = (uint64_t)ອີເມວ >> 32;
    유선저장기(GENET_RX_DESC_STATUS(ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ)) = ບ່ອນເກັບຊົ່ວຄາວ_ຂະ_ຫນາດ << 16;
}
static err_t 전문보내기(struct netif *ມືຖື_ຄ່າ, struct pbuf *전문) {
    if (!ເປັນສາຍ_ຄ່າ.ກະ_ກຽມ || !netif_is_link_up(ມືຖື_ຄ່າ)) return ERR_RTE;
    unsigned ຂະ_ຫນາດ = 전문->tot_len;
    if (!ຂະ_ຫນາດ || ຂະ_ຫນາດ > 1536) return ERR_BUF;
    uint16_t 소비 = 유선저장기(GENET_TX_DMA_CONS_INDEX(고리번호));
    if ((uint16_t)(ເປັນສາຍ_ຄ່າ.생산 - 소비) >= 고리개수 - 1) return ERR_MEM;
    unsigned ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ = ເປັນສາຍ_ຄ່າ.생산 % 고리개수, 송신길이 = ຂະ_ຫນາດ < 60 ? 60 : ຂະ_ຫນາດ;
    unsigned char *ຂໍ້ມູນ = ເປັນສາຍ_ຄ່າ.ສົ່ງ[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ];
    memset(ຂໍ້ມູນ, 0, 송신길이);
    if (pbuf_copy_partial(전문, ຂໍ້ມູນ, ຂະ_ຫນາດ, 0) != ຂະ_ຫນາດ) return ERR_BUF;
    ສະອາດ_ແຄຊ໌(ຂໍ້ມູນ, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ)) = (uint32_t)(uintptr_t)ຂໍ້ມູນ;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ)) = (uint64_t)(uintptr_t)ຂໍ້ມູນ >> 32;
    유선저장기(GENET_TX_DESC_STATUS(ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    ຊິງໂຄຣໄນ();
    ເປັນສາຍ_ຄ່າ.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(고리번호)) = ເປັນສາຍ_ຄ່າ.생산;
    ເປັນສາຍ_ຄ່າ.집계[2]++; ເປັນສາຍ_ຄ່າ.집계[3] += ຂະ_ຫນາດ;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t ກະ_ກຽມ_ເປັນສາຍ_ເຄືອຂ່າຍ(struct netif *ມືຖື_ຄ່າ) {
    unsigned char ອີເມວ[6];
    if (!유선장치있음() || !ກະດານ_ເຄື່ອງຈັກ_ອີເມວ(ອີເມວ) || (ອີເມວ[0] & 1)) return ERR_IF;
    unsigned 합 = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) 합 |= ອີເມວ[순번];
    if (!합) return ERR_IF;
    memset(&ເປັນສາຍ_ຄ່າ, 0, sizeof(ເປັນສາຍ_ຄ່າ));
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
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)ອີເມວ[0] << 24 | (uint32_t)ອີເມວ[1] << 16 | ອີເມວ[2] << 8 | ອີເມວ[3];
    유선저장기(GENET_UMAC_MAC1) = ອີເມວ[4] << 8 | ອີເມວ[5];
    ກະ_ກຽມ_ຫ່ວງ(GENET_TX_BASE); ກະ_ກຽມ_ຫ່ວງ(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < 고리개수; 순번++) 받는주소(순번);
    ຊິງໂຄຣໄນ();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(고리번호);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    ມືຖື_ຄ່າ->name[0] = 'e'; ມືຖື_ຄ່າ->name[1] = 'n'; ມືຖື_ຄ່າ->mtu = 1500;
    ມືຖື_ຄ່າ->hwaddr_len = 6; memcpy(ມືຖື_ຄ່າ->hwaddr, ອີເມວ, 6);
    ມືຖື_ຄ່າ->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    ມືຖື_ຄ່າ->output = etharp_output; ມືຖື_ຄ່າ->linkoutput = 전문보내기;
    ເປັນສາຍ_ຄ່າ.ກະ_ກຽມ = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *ມືຖື_ຄ່າ) {
    if (!ເປັນສາຍ_ຄ່າ.ກະ_ກຽມ) return;
    uintptr_t 지금 = 보드밀리초();
    if (지금 >= ເປັນສາຍ_ຄ່າ.다음확인) {
        ເປັນສາຍ_ຄ່າ.다음확인 = 지금 + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int ສະຖານະ_ຄ່າ = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned ວິ_ທີ_ໂຫມດ = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = ວິ_ທີ_ໂຫມດ == 7 ? 1000 : ວິ_ທີ_ໂຫມດ == 5 ? 100 : ວິ_ທີ_ໂຫມດ == 2 ? 10 : 0;
        ເປັນສາຍ_ຄ່າ.속도 = ສະຖານະ_ຄ່າ >= 0 && (ສະຖານະ_ຄ່າ & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (ເປັນສາຍ_ຄ່າ.속도) {
            uint32_t ການຕັ້ງຄ່າ = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            ການຕັ້ງຄ່າ &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = ການຕັ້ງຄ່າ | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ການຕັ້ງຄ່າ = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = ການຕັ້ງຄ່າ | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(ມືຖື_ຄ່າ)) netif_set_link_up(ມືຖື_ຄ່າ);
        } else if (netif_is_link_up(ມືຖື_ຄ່າ)) netif_set_link_down(ມືຖື_ຄ່າ);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(고리번호));
    unsigned 남음 = (uint16_t)(생산 - ເປັນສາຍ_ຄ່າ.소비);
    if (남음 > 고리개수) { ເປັນສາຍ_ຄ່າ.집계[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ = ເປັນສາຍ_ຄ່າ.소비 % 고리개수;
        ຊິງໂຄຣໄນ();
        uint32_t ສະຖານະ_ຄ່າ = 유선저장기(GENET_RX_DESC_STATUS(ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ));
        unsigned ຄວາມຍາວ_ຄ່າ = (ສະຖານະ_ຄ່າ & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t 경계 = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((ສະຖານະ_ຄ່າ & (경계 | GENET_RX_DESC_STATUS_RX_ERROR)) != 경계 || ຄວາມຍາວ_ຄ່າ < 16 || ຄວາມຍາວ_ຄ່າ > 1538) ເປັນສາຍ_ຄ່າ.집계[4]++;
        else {
            ສະອາດ_ແຄຊ໌(ເປັນສາຍ_ຄ່າ.받기[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ], ຄວາມຍາວ_ຄ່າ, 1);
            struct pbuf *ຂໍ້ມູນ = pbuf_alloc(PBUF_RAW, ຄວາມຍາວ_ຄ່າ - 2, PBUF_POOL);
            if (!ຂໍ້ມູນ) ເປັນສາຍ_ຄ່າ.집계[4]++;
            else if (pbuf_take(ຂໍ້ມູນ, ເປັນສາຍ_ຄ່າ.받기[ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ] + 2, ຄວາມຍາວ_ຄ່າ - 2) != ERR_OK || ມືຖື_ຄ່າ->input(ຂໍ້ມູນ, ມືຖື_ຄ່າ) != ERR_OK) {
                pbuf_free(ຂໍ້ມູນ); ເປັນສາຍ_ຄ່າ.집계[4]++;
            } else { ເປັນສາຍ_ຄ່າ.집계[0]++; ເປັນສາຍ_ຄ່າ.집계[1] += ຄວາມຍາວ_ຄ່າ - 2; }
        }
        받는주소(ຈັດຕໍາແຫນ່ງ_ດັດຊະນີ); ຊິງໂຄຣໄນ(); ເປັນສາຍ_ຄ່າ.소비++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(고리번호)) = ເປັນສາຍ_ຄ່າ.소비;
    }
}
uint32_t 유선망집계(unsigned ເຂົ້າໃນ_ຄ່າ) {
    return ເຂົ້າໃນ_ຄ່າ < 5 ? ເປັນສາຍ_ຄ່າ.집계[ເຂົ້າໃນ_ຄ່າ] : ເຂົ້າໃນ_ຄ່າ == 5 ? ເປັນສາຍ_ຄ່າ.속도 : ເຂົ້າໃນ_ຄ່າ == 6 ? ເປັນສາຍ_ຄ່າ.ກະ_ກຽມ : 0;
}
