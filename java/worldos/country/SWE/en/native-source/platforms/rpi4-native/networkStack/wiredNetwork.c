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

#include "../naming/machineLinkNames.h"
#include "wiredNetwork.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(loopOrdinal) (UINT32_C(1) << (loopOrdinal))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t boardMillis(void);
extern int boardPhysicalHardware(void);
extern int boardMachineAddress(unsigned char *);
#ifndef wiredRegisters
#define wiredRegisters(address) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (address)))
#endif
enum { loopNumber = 16, loopCount = 256, bufferSize = 2048 };
static struct {
    unsigned char receive[loopCount][bufferSize];
    unsigned char send[loopCount][bufferSize];
    uint16_t consumeValue, produceValue;
    int physicalAddress, prepare, speedValue;
    uint32_t statisticsValue[5];
    uintptr_t verifyNextItem;
} wiredValue __attribute__((aligned(64)));

static void synchronize(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void cleanCache(void *data, unsigned lengthValue, int receive) {
#ifndef JKOROS_GENET_TEST
    uintptr_t ending = (uintptr_t)data + lengthValue;
    for (uintptr_t address = (uintptr_t)data & ~(uintptr_t)63; address < ending; address += 64) {
        if (receive) __asm__ volatile("dc ivac, %0" :: "r"(address) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(address) : "memory");
    }
#else
    (void)data; (void)lengthValue; (void)receive;
#endif
    synchronize();
}
static void briefDelay(void) {
    uintptr_t ending = boardMillis() + 1;
    while (boardMillis() < ending) {}
}
static int physicalTransfer(unsigned address, unsigned index, int write, unsigned value) {
    uint32_t command = (write ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (address << GENET_MDIO_ADDR_SHIFT) | (index << GENET_MDIO_REG_SHIFT) | (value & 65535);
    wiredRegisters(GENET_MDIO_CMD) = command;
    wiredRegisters(GENET_MDIO_CMD) = command | GENET_MDIO_START_BUSY;
    uintptr_t ending = boardMillis() + 20;
    for (;;) {
        uint32_t stateValue = wiredRegisters(GENET_MDIO_CMD);
        if (!(stateValue & GENET_MDIO_START_BUSY))
            return stateValue & GENET_MDIO_READ_FAILED ? -1 : (int)(stateValue & 65535);
        if (boardMillis() >= ending) return -1;
    }
}
static int readPhysical(unsigned index) { return physicalTransfer(wiredValue.physicalAddress, index, 0, 0); }
static int writePhysical(unsigned index, unsigned value) { return physicalTransfer(wiredValue.physicalAddress, index, 1, value); }
static int preparePhysical(void) {
    wiredValue.physicalAddress = -1;
    for (unsigned address = 0; address < 32; address++) {
        int identifyValue = physicalTransfer(address, 2, 0, 0);
        if (identifyValue > 0 && identifyValue != 65535) { wiredValue.physicalAddress = address; break; }
    }
    if (wiredValue.physicalAddress < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (writePhysical(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int value = readPhysical(BRGPHY_MII_AUXCTL);
    if (value < 0 || writePhysical(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (value & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (writePhysical(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    value = readPhysical(BRGPHY_MII_SHADOW_1C);
    if (value < 0 || writePhysical(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (value & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (writePhysical(4, 0x0141) < 0 || writePhysical(9, 0x0200) < 0) return -1;
    return writePhysical(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void prepareLoop(unsigned backgroundValue) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned loopValue = backgroundValue + 0xc00 + GENET_DMA_RING_SIZE * loopNumber;
    for (unsigned position = 0; position <= 0x30; position += 4) wiredRegisters(loopValue + position) = 0;
    wiredRegisters(loopValue + 0x10) = (loopCount << 16) | bufferSize;
    wiredRegisters(loopValue + 0x1c) = loopCount * GENET_DMA_DESC_SIZE / 4 - 1;
    if (backgroundValue == GENET_RX_BASE) wiredRegisters(loopValue + 0x28) = (5 << 16) | (loopCount >> 4);
    else wiredRegisters(loopValue + 0x24) = 1;
    wiredRegisters(backgroundValue + 0x104c) = 8;
    wiredRegisters(backgroundValue + 0x1040) = __BIT(loopNumber);
}
static void receivingAddress(unsigned positionIndex) {
    uintptr_t address = (uintptr_t)wiredValue.receive[positionIndex];
    cleanCache((void *)address, bufferSize, 0);
    wiredRegisters(GENET_RX_DESC_ADDRESS_LO(positionIndex)) = (uint32_t)address;
    wiredRegisters(GENET_RX_DESC_ADDRESS_HI(positionIndex)) = (uint64_t)address >> 32;
    wiredRegisters(GENET_RX_DESC_STATUS(positionIndex)) = bufferSize << 16;
}
static err_t sendDatagram(struct netif *deviceValue, struct pbuf *datagram) {
    if (!wiredValue.prepare || !netif_is_link_up(deviceValue)) return ERR_RTE;
    unsigned size = datagram->tot_len;
    if (!size || size > 1536) return ERR_BUF;
    uint16_t consumeValue = wiredRegisters(GENET_TX_DMA_CONS_INDEX(loopNumber));
    if ((uint16_t)(wiredValue.produceValue - consumeValue) >= loopCount - 1) return ERR_MEM;
    unsigned positionIndex = wiredValue.produceValue % loopCount, transmitLength = size < 60 ? 60 : size;
    unsigned char *data = wiredValue.send[positionIndex];
    memset(data, 0, transmitLength);
    if (pbuf_copy_partial(datagram, data, size, 0) != size) return ERR_BUF;
    cleanCache(data, transmitLength, 0);
    wiredRegisters(GENET_TX_DESC_ADDRESS_LO(positionIndex)) = (uint32_t)(uintptr_t)data;
    wiredRegisters(GENET_TX_DESC_ADDRESS_HI(positionIndex)) = (uint64_t)(uintptr_t)data >> 32;
    wiredRegisters(GENET_TX_DESC_STATUS(positionIndex)) = (transmitLength << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    synchronize();
    wiredValue.produceValue++;
    wiredRegisters(GENET_TX_DMA_PROD_INDEX(loopNumber)) = wiredValue.produceValue;
    wiredValue.statisticsValue[2]++; wiredValue.statisticsValue[3] += size;
    return ERR_OK;
}
int hasWiredDevice(void) {
    return boardPhysicalHardware() && ((wiredRegisters(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t prepareWiredNetwork(struct netif *deviceValue) {
    unsigned char address[6];
    if (!hasWiredDevice() || !boardMachineAddress(address) || (address[0] & 1)) return ERR_IF;
    unsigned sumValue = 0; for (unsigned ordinalIndex = 0; ordinalIndex < 6; ordinalIndex++) sumValue |= address[ordinalIndex];
    if (!sumValue) return ERR_IF;
    memset(&wiredValue, 0, sizeof(wiredValue));
    wiredRegisters(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    wiredRegisters(GENET_RX_DMA_CTRL) = wiredRegisters(GENET_TX_DMA_CTRL) = 0;
    uint32_t initialState = wiredRegisters(GENET_SYS_RBUF_FLUSH_CTRL);
    wiredRegisters(GENET_SYS_RBUF_FLUSH_CTRL) = initialState | GENET_SYS_RBUF_FLUSH_RESET; briefDelay();
    wiredRegisters(GENET_SYS_RBUF_FLUSH_CTRL) = initialState & ~GENET_SYS_RBUF_FLUSH_RESET; briefDelay();
    wiredRegisters(GENET_SYS_RBUF_FLUSH_CTRL) = 0; briefDelay();
    wiredRegisters(GENET_UMAC_CMD) = 0;
    wiredRegisters(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; briefDelay();
    wiredRegisters(GENET_UMAC_CMD) = 0;
    wiredRegisters(GENET_UMAC_MIB_CTRL) = 7;
    wiredRegisters(GENET_UMAC_MIB_CTRL) = 0;
    wiredRegisters(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (preparePhysical() < 0) return ERR_IF;
    wiredRegisters(GENET_UMAC_MAC0) = (uint32_t)address[0] << 24 | (uint32_t)address[1] << 16 | address[2] << 8 | address[3];
    wiredRegisters(GENET_UMAC_MAC1) = address[4] << 8 | address[5];
    prepareLoop(GENET_TX_BASE); prepareLoop(GENET_RX_BASE);
    for (unsigned ordinalIndex = 0; ordinalIndex < loopCount; ordinalIndex++) receivingAddress(ordinalIndex);
    synchronize();
    wiredRegisters(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(loopNumber);
    wiredRegisters(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(loopNumber);
    wiredRegisters(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    wiredRegisters(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    wiredRegisters(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    wiredRegisters(GENET_UMAC_MDF_CTRL) = 0;
    wiredRegisters(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    deviceValue->name[0] = 'e'; deviceValue->name[1] = 'n'; deviceValue->mtu = 1500;
    deviceValue->hwaddr_len = 6; memcpy(deviceValue->hwaddr, address, 6);
    deviceValue->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    deviceValue->output = etharp_output; deviceValue->linkoutput = sendDatagram;
    wiredValue.prepare = 1;
    return ERR_OK;
}
void inspectWiredNetwork(struct netif *deviceValue) {
    if (!wiredValue.prepare) return;
    uintptr_t nowValue = boardMillis();
    if (nowValue >= wiredValue.verifyNextItem) {
        wiredValue.verifyNextItem = nowValue + 500;
        readPhysical(BRGPHY_MII_BMSR);
        int stateValue = readPhysical(BRGPHY_MII_BMSR), auxiliaryValue = readPhysical(BRGPHY_MII_AUXSTS);
        unsigned methodMode = auxiliaryValue < 0 ? 0 : (auxiliaryValue & BRGPHY_AUXSTS_AN_RES) >> 8;
        int speedValue = methodMode == 7 ? 1000 : methodMode == 5 ? 100 : methodMode == 2 ? 10 : 0;
        wiredValue.speedValue = stateValue >= 0 && (stateValue & BRGPHY_BMSR_LINK) ? speedValue : 0;
        if (wiredValue.speedValue) {
            uint32_t settings = wiredRegisters(GENET_EXT_RGMII_OOB_CTRL);
            settings &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            wiredRegisters(GENET_EXT_RGMII_OOB_CTRL) = settings | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            settings = wiredRegisters(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            wiredRegisters(GENET_UMAC_CMD) = settings | (speedValue == 1000 ? GENET_UMAC_CMD_SPEED_1000 : speedValue == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(deviceValue)) netif_set_link_up(deviceValue);
        } else if (netif_is_link_up(deviceValue)) netif_set_link_down(deviceValue);
    }
    uint16_t produceValue = wiredRegisters(GENET_RX_DMA_PROD_INDEX(loopNumber));
    unsigned remainderData = (uint16_t)(produceValue - wiredValue.consumeValue);
    if (remainderData > loopCount) { wiredValue.statisticsValue[4]++; return; }
    for (unsigned loopOrdinal = 0; loopOrdinal < remainderData && loopOrdinal < 32; loopOrdinal++) {
        unsigned positionIndex = wiredValue.consumeValue % loopCount;
        synchronize();
        uint32_t stateValue = wiredRegisters(GENET_RX_DESC_STATUS(positionIndex));
        unsigned lengthValue = (stateValue & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t boundaryValue = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((stateValue & (boundaryValue | GENET_RX_DESC_STATUS_RX_ERROR)) != boundaryValue || lengthValue < 16 || lengthValue > 1538) wiredValue.statisticsValue[4]++;
        else {
            cleanCache(wiredValue.receive[positionIndex], lengthValue, 1);
            struct pbuf *data = pbuf_alloc(PBUF_RAW, lengthValue - 2, PBUF_POOL);
            if (!data) wiredValue.statisticsValue[4]++;
            else if (pbuf_take(data, wiredValue.receive[positionIndex] + 2, lengthValue - 2) != ERR_OK || deviceValue->input(data, deviceValue) != ERR_OK) {
                pbuf_free(data); wiredValue.statisticsValue[4]++;
            } else { wiredValue.statisticsValue[0]++; wiredValue.statisticsValue[1] += lengthValue - 2; }
        }
        receivingAddress(positionIndex); synchronize(); wiredValue.consumeValue++;
        wiredRegisters(GENET_RX_DMA_CONS_INDEX(loopNumber)) = wiredValue.consumeValue;
    }
}
uint32_t wiredNetworkStatistics(unsigned entryValue) {
    return entryValue < 5 ? wiredValue.statisticsValue[entryValue] : entryValue == 5 ? wiredValue.speedValue : entryValue == 6 ? wiredValue.prepare : 0;
}
