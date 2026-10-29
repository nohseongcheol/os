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

#include "../denominación/nombresEnlazarMáquina.h"
#include "redCableado.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(ordinalBucle) (UINT32_C(1) << (ordinalBucle))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t milisegundosTranscurridosPlaca(void);
extern int equipoFísicoFísicoPlaca(void);
extern int direcciónMáquinaPlaca(unsigned char *);
#ifndef registrosCableado
#define registrosCableado(dirección) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (dirección)))
#endif
enum { númeroBucle = 16, númeroElementosBucle = 256, tamañoBúfer = 2048 };
static struct {
    unsigned char recibir[númeroElementosBucle][tamañoBúfer];
    unsigned char enviar[númeroElementosBucle][tamañoBúfer];
    uint16_t consumirValor, valorProducir;
    int direcciónFísico, preparar, valorVelocidad;
    uint32_t valorEstadísticas[5];
    uintptr_t verificarElementoListaSiguiente;
} valorCableado __attribute__((aligned(64)));

static void sincronizar(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void cachéLimpiar(void *Datos, unsigned longitud, int recibir) {
#ifndef JKOROS_GENET_TEST
    uintptr_t terminación = (uintptr_t)Datos + longitud;
    for (uintptr_t dirección = (uintptr_t)Datos & ~(uintptr_t)63; dirección < terminación; dirección += 64) {
        if (recibir) __asm__ volatile("dc ivac, %0" :: "r"(dirección) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(dirección) : "memory");
    }
#else
    (void)Datos; (void)longitud; (void)recibir;
#endif
    sincronizar();
}
static void demoraBreve(void) {
    uintptr_t terminación = milisegundosTranscurridosPlaca() + 1;
    while (milisegundosTranscurridosPlaca() < terminación) {}
}
static int transferenciaFísico(unsigned dirección, unsigned número, int escribir, unsigned valor) {
    uint32_t comando = (escribir ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (dirección << GENET_MDIO_ADDR_SHIFT) | (número << GENET_MDIO_REG_SHIFT) | (valor & 65535);
    registrosCableado(GENET_MDIO_CMD) = comando;
    registrosCableado(GENET_MDIO_CMD) = comando | GENET_MDIO_START_BUSY;
    uintptr_t terminación = milisegundosTranscurridosPlaca() + 20;
    for (;;) {
        uint32_t valorEstadoValor = registrosCableado(GENET_MDIO_CMD);
        if (!(valorEstadoValor & GENET_MDIO_START_BUSY))
            return valorEstadoValor & GENET_MDIO_READ_FAILED ? -1 : (int)(valorEstadoValor & 65535);
        if (milisegundosTranscurridosPlaca() >= terminación) return -1;
    }
}
static int leerFísico(unsigned número) { return transferenciaFísico(valorCableado.direcciónFísico, número, 0, 0); }
static int escribirFísico(unsigned número, unsigned valor) { return transferenciaFísico(valorCableado.direcciónFísico, número, 1, valor); }
static int prepararFísico(void) {
    valorCableado.direcciónFísico = -1;
    for (unsigned dirección = 0; dirección < 32; dirección++) {
        int identificarValor = transferenciaFísico(dirección, 2, 0, 0);
        if (identificarValor > 0 && identificarValor != 65535) { valorCableado.direcciónFísico = dirección; break; }
    }
    if (valorCableado.direcciónFísico < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (escribirFísico(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int valor = leerFísico(BRGPHY_MII_AUXCTL);
    if (valor < 0 || escribirFísico(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (valor & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (escribirFísico(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    valor = leerFísico(BRGPHY_MII_SHADOW_1C);
    if (valor < 0 || escribirFísico(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (valor & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (escribirFísico(4, 0x0141) < 0 || escribirFísico(9, 0x0200) < 0) return -1;
    return escribirFísico(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void prepararBucle(unsigned valorFondo) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned valorBucle = valorFondo + 0xc00 + GENET_DMA_RING_SIZE * númeroBucle;
    for (unsigned posición = 0; posición <= 0x30; posición += 4) registrosCableado(valorBucle + posición) = 0;
    registrosCableado(valorBucle + 0x10) = (númeroElementosBucle << 16) | tamañoBúfer;
    registrosCableado(valorBucle + 0x1c) = númeroElementosBucle * GENET_DMA_DESC_SIZE / 4 - 1;
    if (valorFondo == GENET_RX_BASE) registrosCableado(valorBucle + 0x28) = (5 << 16) | (númeroElementosBucle >> 4);
    else registrosCableado(valorBucle + 0x24) = 1;
    registrosCableado(valorFondo + 0x104c) = 8;
    registrosCableado(valorFondo + 0x1040) = __BIT(númeroBucle);
}
static void direcciónRecepciónEnCurso(unsigned índicePosición) {
    uintptr_t dirección = (uintptr_t)valorCableado.recibir[índicePosición];
    cachéLimpiar((void *)dirección, tamañoBúfer, 0);
    registrosCableado(GENET_RX_DESC_ADDRESS_LO(índicePosición)) = (uint32_t)dirección;
    registrosCableado(GENET_RX_DESC_ADDRESS_HI(índicePosición)) = (uint64_t)dirección >> 32;
    registrosCableado(GENET_RX_DESC_STATUS(índicePosición)) = tamañoBúfer << 16;
}
static err_t enviarDatagrama(struct netif *Dispositivo, struct pbuf *datagrama) {
    if (!valorCableado.preparar || !netif_is_link_up(Dispositivo)) return ERR_RTE;
    unsigned tamaño = datagrama->tot_len;
    if (!tamaño || tamaño > 1536) return ERR_BUF;
    uint16_t consumirValor = registrosCableado(GENET_TX_DMA_CONS_INDEX(númeroBucle));
    if ((uint16_t)(valorCableado.valorProducir - consumirValor) >= númeroElementosBucle - 1) return ERR_MEM;
    unsigned índicePosición = valorCableado.valorProducir % númeroElementosBucle, longitudTransmitir = tamaño < 60 ? 60 : tamaño;
    unsigned char *Datos = valorCableado.enviar[índicePosición];
    memset(Datos, 0, longitudTransmitir);
    if (pbuf_copy_partial(datagrama, Datos, tamaño, 0) != tamaño) return ERR_BUF;
    cachéLimpiar(Datos, longitudTransmitir, 0);
    registrosCableado(GENET_TX_DESC_ADDRESS_LO(índicePosición)) = (uint32_t)(uintptr_t)Datos;
    registrosCableado(GENET_TX_DESC_ADDRESS_HI(índicePosición)) = (uint64_t)(uintptr_t)Datos >> 32;
    registrosCableado(GENET_TX_DESC_STATUS(índicePosición)) = (longitudTransmitir << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sincronizar();
    valorCableado.valorProducir++;
    registrosCableado(GENET_TX_DMA_PROD_INDEX(númeroBucle)) = valorCableado.valorProducir;
    valorCableado.valorEstadísticas[2]++; valorCableado.valorEstadísticas[3] += tamaño;
    return ERR_OK;
}
int tieneDispositivoCableado(void) {
    return equipoFísicoFísicoPlaca() && ((registrosCableado(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t prepararRedCableado(struct netif *Dispositivo) {
    unsigned char dirección[6];
    if (!tieneDispositivoCableado() || !direcciónMáquinaPlaca(dirección) || (dirección[0] & 1)) return ERR_IF;
    unsigned valorTotalSuma = 0; for (unsigned índiceOrdinal = 0; índiceOrdinal < 6; índiceOrdinal++) valorTotalSuma |= dirección[índiceOrdinal];
    if (!valorTotalSuma) return ERR_IF;
    memset(&valorCableado, 0, sizeof(valorCableado));
    registrosCableado(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    registrosCableado(GENET_RX_DMA_CTRL) = registrosCableado(GENET_TX_DMA_CTRL) = 0;
    uint32_t estadoValorInicialValor = registrosCableado(GENET_SYS_RBUF_FLUSH_CTRL);
    registrosCableado(GENET_SYS_RBUF_FLUSH_CTRL) = estadoValorInicialValor | GENET_SYS_RBUF_FLUSH_RESET; demoraBreve();
    registrosCableado(GENET_SYS_RBUF_FLUSH_CTRL) = estadoValorInicialValor & ~GENET_SYS_RBUF_FLUSH_RESET; demoraBreve();
    registrosCableado(GENET_SYS_RBUF_FLUSH_CTRL) = 0; demoraBreve();
    registrosCableado(GENET_UMAC_CMD) = 0;
    registrosCableado(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; demoraBreve();
    registrosCableado(GENET_UMAC_CMD) = 0;
    registrosCableado(GENET_UMAC_MIB_CTRL) = 7;
    registrosCableado(GENET_UMAC_MIB_CTRL) = 0;
    registrosCableado(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (prepararFísico() < 0) return ERR_IF;
    registrosCableado(GENET_UMAC_MAC0) = (uint32_t)dirección[0] << 24 | (uint32_t)dirección[1] << 16 | dirección[2] << 8 | dirección[3];
    registrosCableado(GENET_UMAC_MAC1) = dirección[4] << 8 | dirección[5];
    prepararBucle(GENET_TX_BASE); prepararBucle(GENET_RX_BASE);
    for (unsigned índiceOrdinal = 0; índiceOrdinal < númeroElementosBucle; índiceOrdinal++) direcciónRecepciónEnCurso(índiceOrdinal);
    sincronizar();
    registrosCableado(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(númeroBucle);
    registrosCableado(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(númeroBucle);
    registrosCableado(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    registrosCableado(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    registrosCableado(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    registrosCableado(GENET_UMAC_MDF_CTRL) = 0;
    registrosCableado(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    Dispositivo->name[0] = 'e'; Dispositivo->name[1] = 'n'; Dispositivo->mtu = 1500;
    Dispositivo->hwaddr_len = 6; memcpy(Dispositivo->hwaddr, dirección, 6);
    Dispositivo->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    Dispositivo->output = etharp_output; Dispositivo->linkoutput = enviarDatagrama;
    valorCableado.preparar = 1;
    return ERR_OK;
}
void inspeccionarRedCableado(struct netif *Dispositivo) {
    if (!valorCableado.preparar) return;
    uintptr_t valorAhora = milisegundosTranscurridosPlaca();
    if (valorAhora >= valorCableado.verificarElementoListaSiguiente) {
        valorCableado.verificarElementoListaSiguiente = valorAhora + 500;
        leerFísico(BRGPHY_MII_BMSR);
        int valorEstadoValor = leerFísico(BRGPHY_MII_BMSR), valorAuxiliar = leerFísico(BRGPHY_MII_AUXSTS);
        unsigned modoMétodo = valorAuxiliar < 0 ? 0 : (valorAuxiliar & BRGPHY_AUXSTS_AN_RES) >> 8;
        int valorVelocidad = modoMétodo == 7 ? 1000 : modoMétodo == 5 ? 100 : modoMétodo == 2 ? 10 : 0;
        valorCableado.valorVelocidad = valorEstadoValor >= 0 && (valorEstadoValor & BRGPHY_BMSR_LINK) ? valorVelocidad : 0;
        if (valorCableado.valorVelocidad) {
            uint32_t ajustes = registrosCableado(GENET_EXT_RGMII_OOB_CTRL);
            ajustes &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            registrosCableado(GENET_EXT_RGMII_OOB_CTRL) = ajustes | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            ajustes = registrosCableado(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            registrosCableado(GENET_UMAC_CMD) = ajustes | (valorVelocidad == 1000 ? GENET_UMAC_CMD_SPEED_1000 : valorVelocidad == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(Dispositivo)) netif_set_link_up(Dispositivo);
        } else if (netif_is_link_up(Dispositivo)) netif_set_link_down(Dispositivo);
    }
    uint16_t valorProducir = registrosCableado(GENET_RX_DMA_PROD_INDEX(númeroBucle));
    unsigned datosRestoDivisión = (uint16_t)(valorProducir - valorCableado.consumirValor);
    if (datosRestoDivisión > númeroElementosBucle) { valorCableado.valorEstadísticas[4]++; return; }
    for (unsigned ordinalBucle = 0; ordinalBucle < datosRestoDivisión && ordinalBucle < 32; ordinalBucle++) {
        unsigned índicePosición = valorCableado.consumirValor % númeroElementosBucle;
        sincronizar();
        uint32_t valorEstadoValor = registrosCableado(GENET_RX_DESC_STATUS(índicePosición));
        unsigned longitud = (valorEstadoValor & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t valorFrontera = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((valorEstadoValor & (valorFrontera | GENET_RX_DESC_STATUS_RX_ERROR)) != valorFrontera || longitud < 16 || longitud > 1538) valorCableado.valorEstadísticas[4]++;
        else {
            cachéLimpiar(valorCableado.recibir[índicePosición], longitud, 1);
            struct pbuf *Datos = pbuf_alloc(PBUF_RAW, longitud - 2, PBUF_POOL);
            if (!Datos) valorCableado.valorEstadísticas[4]++;
            else if (pbuf_take(Datos, valorCableado.recibir[índicePosición] + 2, longitud - 2) != ERR_OK || Dispositivo->input(Datos, Dispositivo) != ERR_OK) {
                pbuf_free(Datos); valorCableado.valorEstadísticas[4]++;
            } else { valorCableado.valorEstadísticas[0]++; valorCableado.valorEstadísticas[1] += longitud - 2; }
        }
        direcciónRecepciónEnCurso(índicePosición); sincronizar(); valorCableado.consumirValor++;
        registrosCableado(GENET_RX_DMA_CONS_INDEX(númeroBucle)) = valorCableado.consumirValor;
    }
}
uint32_t estadísticasRedCableado(unsigned valorEntradaElemento) {
    return valorEntradaElemento < 5 ? valorCableado.valorEstadísticas[valorEntradaElemento] : valorEntradaElemento == 5 ? valorCableado.valorVelocidad : valorEntradaElemento == 6 ? valorCableado.preparar : 0;
}
