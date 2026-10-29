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
#include "com_fio_rede.h"
#include "string.h"
#include "lwip/etharp.h"
#define __BIT(고리순번) (UINT32_C(1) << (고리순번))
#include "../vendor/freebsd-genet/if_genetreg.h"
#include "../vendor/freebsd-genet/brgphyreg.h"

extern uintptr_t 보드밀리초(void);
extern int 보드실물(void);
extern int Quadro_endereço_real(unsigned char *);
#ifndef 유선저장기
#define 유선저장기(Endereço) (*(volatile uint32_t *)(uintptr_t)(0xfd580000ul + (Endereço)))
#endif
enum { Loop_número = 16, Loop_CONT_NÚM = 256, tamanho_do_buffer = 2048 };
static struct {
    unsigned char receber[Loop_CONT_NÚM][tamanho_do_buffer];
    unsigned char enviar[Loop_CONT_NÚM][tamanho_do_buffer];
    uint16_t consumir_VALOR, 생산;
    int 물리주소, Preparar, 속도;
    uint32_t Estatísticas_VALOR[5];
    uintptr_t verificar_Avançar_item;
} com_fio_VALOR __attribute__((aligned(64)));

static void sincronizar(void) {
#ifndef JKOROS_GENET_TEST
    __asm__ volatile("dsb sy" ::: "memory");
#endif
}
static void TIRAR_cache(void *dados, unsigned duração_VALOR, int receber) {
#ifndef JKOROS_GENET_TEST
    uintptr_t 끝 = (uintptr_t)dados + duração_VALOR;
    for (uintptr_t Endereço = (uintptr_t)dados & ~(uintptr_t)63; Endereço < 끝; Endereço += 64) {
        if (receber) __asm__ volatile("dc ivac, %0" :: "r"(Endereço) : "memory");
        else __asm__ volatile("dc cvac, %0" :: "r"(Endereço) : "memory");
    }
#else
    (void)dados; (void)duração_VALOR; (void)receber;
#endif
    sincronizar();
}
static void 잠깐(void) {
    uintptr_t 끝 = 보드밀리초() + 1;
    while (보드밀리초() < 끝) {}
}
static int 물리전송(unsigned Endereço, unsigned ÍNDICE, int Escrita, unsigned VALOR) {
    uint32_t comando = (Escrita ? GENET_MDIO_WRITE : GENET_MDIO_READ) |
        (Endereço << GENET_MDIO_ADDR_SHIFT) | (ÍNDICE << GENET_MDIO_REG_SHIFT) | (VALOR & 65535);
    유선저장기(GENET_MDIO_CMD) = comando;
    유선저장기(GENET_MDIO_CMD) = comando | GENET_MDIO_START_BUSY;
    uintptr_t 끝 = 보드밀리초() + 20;
    for (;;) {
        uint32_t Estado_VALOR = 유선저장기(GENET_MDIO_CMD);
        if (!(Estado_VALOR & GENET_MDIO_START_BUSY))
            return Estado_VALOR & GENET_MDIO_READ_FAILED ? -1 : (int)(Estado_VALOR & 65535);
        if (보드밀리초() >= 끝) return -1;
    }
}
static int 물리읽기(unsigned ÍNDICE) { return 물리전송(com_fio_VALOR.물리주소, ÍNDICE, 0, 0); }
static int 물리쓰기(unsigned ÍNDICE, unsigned VALOR) { return 물리전송(com_fio_VALOR.물리주소, ÍNDICE, 1, VALOR); }
static int 물리준비(void) {
    com_fio_VALOR.물리주소 = -1;
    for (unsigned Endereço = 0; Endereço < 32; Endereço++) {
        int 식별 = 물리전송(Endereço, 2, 0, 0);
        if (식별 > 0 && 식별 != 65535) { com_fio_VALOR.물리주소 = Endereço; break; }
    }
    if (com_fio_VALOR.물리주소 < 0) return -1;
    /* FreeBSD brgphy_bcm54xx_clock_delay: Pi4 uses RGMII-RXID. */
    if (물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_SHADOW_MISC |
        BRGPHY_AUXCTL_SHADOW_MISC << BRGPHY_AUXCTL_MISC_READ_SHIFT) < 0) return -1;
    int VALOR = 물리읽기(BRGPHY_MII_AUXCTL);
    if (VALOR < 0 || 물리쓰기(BRGPHY_MII_AUXCTL, BRGPHY_AUXCTL_MISC_WRITE_EN |
        BRGPHY_AUXCTL_SHADOW_MISC | (VALOR & BRGPHY_AUXCTL_MISC_DATA_MASK) |
        BRGPHY_AUXCTL_MISC_RGMII_SKEW_EN) < 0) return -1;
    if (물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_CLK_CTRL) < 0) return -1;
    VALOR = 물리읽기(BRGPHY_MII_SHADOW_1C);
    if (VALOR < 0 || 물리쓰기(BRGPHY_MII_SHADOW_1C, BRGPHY_SHADOW_1C_WRITE_EN |
        BRGPHY_SHADOW_1C_CLK_CTRL | (VALOR & BRGPHY_SHADOW_1C_DATA_MASK & ~BRGPHY_SHADOW_1C_GTXCLK_EN)) < 0) return -1;
    /* IEEE 802.3 autonegotiation: advertise full duplex 10/100/1000. */
    if (물리쓰기(4, 0x0141) < 0 || 물리쓰기(9, 0x0200) < 0) return -1;
    return 물리쓰기(BRGPHY_MII_BMCR, BRGPHY_BMCR_AUTOEN | BRGPHY_BMCR_STARTNEG);
}
static void Preparar_Loop(unsigned Tela_de_fundo_VALOR) {
    /* Default queue layout from FreeBSD gen_init_{rx,tx}ring. */
    unsigned Loop_VALOR = Tela_de_fundo_VALOR + 0xc00 + GENET_DMA_RING_SIZE * Loop_número;
    for (unsigned posição = 0; posição <= 0x30; posição += 4) 유선저장기(Loop_VALOR + posição) = 0;
    유선저장기(Loop_VALOR + 0x10) = (Loop_CONT_NÚM << 16) | tamanho_do_buffer;
    유선저장기(Loop_VALOR + 0x1c) = Loop_CONT_NÚM * GENET_DMA_DESC_SIZE / 4 - 1;
    if (Tela_de_fundo_VALOR == GENET_RX_BASE) 유선저장기(Loop_VALOR + 0x28) = (5 << 16) | (Loop_CONT_NÚM >> 4);
    else 유선저장기(Loop_VALOR + 0x24) = 1;
    유선저장기(Tela_de_fundo_VALOR + 0x104c) = 8;
    유선저장기(Tela_de_fundo_VALOR + 0x1040) = __BIT(Loop_número);
}
static void 받는주소(unsigned cargo_ÍNDICE) {
    uintptr_t Endereço = (uintptr_t)com_fio_VALOR.receber[cargo_ÍNDICE];
    TIRAR_cache((void *)Endereço, tamanho_do_buffer, 0);
    유선저장기(GENET_RX_DESC_ADDRESS_LO(cargo_ÍNDICE)) = (uint32_t)Endereço;
    유선저장기(GENET_RX_DESC_ADDRESS_HI(cargo_ÍNDICE)) = (uint64_t)Endereço >> 32;
    유선저장기(GENET_RX_DESC_STATUS(cargo_ÍNDICE)) = tamanho_do_buffer << 16;
}
static err_t enviar_datagrama(struct netif *celular_VALOR, struct pbuf *datagrama) {
    if (!com_fio_VALOR.Preparar || !netif_is_link_up(celular_VALOR)) return ERR_RTE;
    unsigned Tamanho = datagrama->tot_len;
    if (!Tamanho || Tamanho > 1536) return ERR_BUF;
    uint16_t consumir_VALOR = 유선저장기(GENET_TX_DMA_CONS_INDEX(Loop_número));
    if ((uint16_t)(com_fio_VALOR.생산 - consumir_VALOR) >= Loop_CONT_NÚM - 1) return ERR_MEM;
    unsigned cargo_ÍNDICE = com_fio_VALOR.생산 % Loop_CONT_NÚM, 송신길이 = Tamanho < 60 ? 60 : Tamanho;
    unsigned char *dados = com_fio_VALOR.enviar[cargo_ÍNDICE];
    memset(dados, 0, 송신길이);
    if (pbuf_copy_partial(datagrama, dados, Tamanho, 0) != Tamanho) return ERR_BUF;
    TIRAR_cache(dados, 송신길이, 0);
    유선저장기(GENET_TX_DESC_ADDRESS_LO(cargo_ÍNDICE)) = (uint32_t)(uintptr_t)dados;
    유선저장기(GENET_TX_DESC_ADDRESS_HI(cargo_ÍNDICE)) = (uint64_t)(uintptr_t)dados >> 32;
    유선저장기(GENET_TX_DESC_STATUS(cargo_ÍNDICE)) = (송신길이 << 16) |
        GENET_TX_DESC_STATUS_SOP | GENET_TX_DESC_STATUS_EOP |
        GENET_TX_DESC_STATUS_CRC | GENET_TX_DESC_STATUS_QTAG_MASK;
    sincronizar();
    com_fio_VALOR.생산++;
    유선저장기(GENET_TX_DMA_PROD_INDEX(Loop_número)) = com_fio_VALOR.생산;
    com_fio_VALOR.Estatísticas_VALOR[2]++; com_fio_VALOR.Estatísticas_VALOR[3] += Tamanho;
    return ERR_OK;
}
int 유선장치있음(void) {
    return 보드실물() && ((유선저장기(GENET_SYS_REV_CTRL) & REV_MAJOR) >> REV_MAJOR_SHIFT) == REV_MAJOR_V5;
}
err_t Preparar_com_fio_rede(struct netif *celular_VALOR) {
    unsigned char Endereço[6];
    if (!유선장치있음() || !Quadro_endereço_real(Endereço) || (Endereço[0] & 1)) return ERR_IF;
    unsigned SUM_VALOR = 0; for (unsigned 순번 = 0; 순번 < 6; 순번++) SUM_VALOR |= Endereço[순번];
    if (!SUM_VALOR) return ERR_IF;
    memset(&com_fio_VALOR, 0, sizeof(com_fio_VALOR));
    유선저장기(GENET_INTRL2_CPU_SET_MASK) = UINT32_MAX;
    유선저장기(GENET_RX_DMA_CTRL) = 유선저장기(GENET_TX_DMA_CTRL) = 0;
    uint32_t estado_inicial = 유선저장기(GENET_SYS_RBUF_FLUSH_CTRL);
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = estado_inicial | GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = estado_inicial & ~GENET_SYS_RBUF_FLUSH_RESET; 잠깐();
    유선저장기(GENET_SYS_RBUF_FLUSH_CTRL) = 0; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_LCL_LOOP_EN | GENET_UMAC_CMD_SW_RESET; 잠깐();
    유선저장기(GENET_UMAC_CMD) = 0;
    유선저장기(GENET_UMAC_MIB_CTRL) = 7;
    유선저장기(GENET_UMAC_MIB_CTRL) = 0;
    유선저장기(GENET_SYS_PORT_CTRL) = GENET_SYS_PORT_MODE_EXT_GPHY;
    if (물리준비() < 0) return ERR_IF;
    유선저장기(GENET_UMAC_MAC0) = (uint32_t)Endereço[0] << 24 | (uint32_t)Endereço[1] << 16 | Endereço[2] << 8 | Endereço[3];
    유선저장기(GENET_UMAC_MAC1) = Endereço[4] << 8 | Endereço[5];
    Preparar_Loop(GENET_TX_BASE); Preparar_Loop(GENET_RX_BASE);
    for (unsigned 순번 = 0; 순번 < Loop_CONT_NÚM; 순번++) 받는주소(순번);
    sincronizar();
    유선저장기(GENET_TX_DMA_CTRL) = GENET_TX_DMA_CTRL_EN | GENET_TX_DMA_CTRL_RBUF_EN(Loop_número);
    유선저장기(GENET_RX_DMA_CTRL) = GENET_RX_DMA_CTRL_EN | GENET_RX_DMA_CTRL_RBUF_EN(Loop_número);
    유선저장기(GENET_UMAC_MAX_FRAME_LEN) = 1536;
    유선저장기(GENET_RBUF_CTRL) = GENET_RBUF_ALIGN_2B;
    유선저장기(GENET_RBUF_TBUF_SIZE_CTRL) = 1;
    유선저장기(GENET_UMAC_MDF_CTRL) = 0;
    유선저장기(GENET_UMAC_CMD) = GENET_UMAC_CMD_TXEN | GENET_UMAC_CMD_RXEN | GENET_UMAC_CMD_PROMISC;
    celular_VALOR->name[0] = 'e'; celular_VALOR->name[1] = 'n'; celular_VALOR->mtu = 1500;
    celular_VALOR->hwaddr_len = 6; memcpy(celular_VALOR->hwaddr, Endereço, 6);
    celular_VALOR->flags = NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | NETIF_FLAG_ETHERNET;
    celular_VALOR->output = etharp_output; celular_VALOR->linkoutput = enviar_datagrama;
    com_fio_VALOR.Preparar = 1;
    return ERR_OK;
}
void 유선망살피기(struct netif *celular_VALOR) {
    if (!com_fio_VALOR.Preparar) return;
    uintptr_t AGORA_VALOR = 보드밀리초();
    if (AGORA_VALOR >= com_fio_VALOR.verificar_Avançar_item) {
        com_fio_VALOR.verificar_Avançar_item = AGORA_VALOR + 500;
        물리읽기(BRGPHY_MII_BMSR);
        int Estado_VALOR = 물리읽기(BRGPHY_MII_BMSR), 보조 = 물리읽기(BRGPHY_MII_AUXSTS);
        unsigned método_MODO = 보조 < 0 ? 0 : (보조 & BRGPHY_AUXSTS_AN_RES) >> 8;
        int 속도 = método_MODO == 7 ? 1000 : método_MODO == 5 ? 100 : método_MODO == 2 ? 10 : 0;
        com_fio_VALOR.속도 = Estado_VALOR >= 0 && (Estado_VALOR & BRGPHY_BMSR_LINK) ? 속도 : 0;
        if (com_fio_VALOR.속도) {
            uint32_t Definições = 유선저장기(GENET_EXT_RGMII_OOB_CTRL);
            Definições &= ~(GENET_EXT_RGMII_OOB_OOB_DISABLE | GENET_EXT_RGMII_OOB_ID_MODE_DISABLE);
            유선저장기(GENET_EXT_RGMII_OOB_CTRL) = Definições | GENET_EXT_RGMII_OOB_RGMII_LINK | GENET_EXT_RGMII_OOB_RGMII_MODE_EN;
            Definições = 유선저장기(GENET_UMAC_CMD) & ~GENET_UMAC_CMD_SPEED;
            유선저장기(GENET_UMAC_CMD) = Definições | (속도 == 1000 ? GENET_UMAC_CMD_SPEED_1000 : 속도 == 100 ? GENET_UMAC_CMD_SPEED_100 : 0);
            if (!netif_is_link_up(celular_VALOR)) netif_set_link_up(celular_VALOR);
        } else if (netif_is_link_up(celular_VALOR)) netif_set_link_down(celular_VALOR);
    }
    uint16_t 생산 = 유선저장기(GENET_RX_DMA_PROD_INDEX(Loop_número));
    unsigned 남음 = (uint16_t)(생산 - com_fio_VALOR.consumir_VALOR);
    if (남음 > Loop_CONT_NÚM) { com_fio_VALOR.Estatísticas_VALOR[4]++; return; }
    for (unsigned 고리순번 = 0; 고리순번 < 남음 && 고리순번 < 32; 고리순번++) {
        unsigned cargo_ÍNDICE = com_fio_VALOR.consumir_VALOR % Loop_CONT_NÚM;
        sincronizar();
        uint32_t Estado_VALOR = 유선저장기(GENET_RX_DESC_STATUS(cargo_ÍNDICE));
        unsigned duração_VALOR = (Estado_VALOR & GENET_RX_DESC_STATUS_BUFLEN_MASK) >> GENET_RX_DESC_STATUS_BUFLEN_SHIFT;
        uint32_t limite_VALOR = GENET_RX_DESC_STATUS_SOP | GENET_RX_DESC_STATUS_EOP;
        if ((Estado_VALOR & (limite_VALOR | GENET_RX_DESC_STATUS_RX_ERROR)) != limite_VALOR || duração_VALOR < 16 || duração_VALOR > 1538) com_fio_VALOR.Estatísticas_VALOR[4]++;
        else {
            TIRAR_cache(com_fio_VALOR.receber[cargo_ÍNDICE], duração_VALOR, 1);
            struct pbuf *dados = pbuf_alloc(PBUF_RAW, duração_VALOR - 2, PBUF_POOL);
            if (!dados) com_fio_VALOR.Estatísticas_VALOR[4]++;
            else if (pbuf_take(dados, com_fio_VALOR.receber[cargo_ÍNDICE] + 2, duração_VALOR - 2) != ERR_OK || celular_VALOR->input(dados, celular_VALOR) != ERR_OK) {
                pbuf_free(dados); com_fio_VALOR.Estatísticas_VALOR[4]++;
            } else { com_fio_VALOR.Estatísticas_VALOR[0]++; com_fio_VALOR.Estatísticas_VALOR[1] += duração_VALOR - 2; }
        }
        받는주소(cargo_ÍNDICE); sincronizar(); com_fio_VALOR.consumir_VALOR++;
        유선저장기(GENET_RX_DMA_CONS_INDEX(Loop_número)) = com_fio_VALOR.consumir_VALOR;
    }
}
uint32_t com_fio_rede_Estatísticas(unsigned entrada_VALOR_962f286b) {
    return entrada_VALOR_962f286b < 5 ? com_fio_VALOR.Estatísticas_VALOR[entrada_VALOR_962f286b] : entrada_VALOR_962f286b == 5 ? com_fio_VALOR.속도 : entrada_VALOR_962f286b == 6 ? com_fio_VALOR.Preparar : 0;
}
