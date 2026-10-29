// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Luxemburgo.JLuxOS.rede_pilha;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP receber_VALOR 분배를 한곳에서 관리한다. */
public final class camada_de_rede {
    @FunctionalInterface
    public interface dados_manipulador {
        void Processo_VALOR_entrada(byte[] dados, int iniciar, int duração_VALOR);
    }

    private final Map<Integer, dados_manipulador> Ethernet_manipulador = new HashMap<Integer, dados_manipulador>();
    private final Map<Integer, dados_manipulador> IP_manipulador = new HashMap<Integer, dados_manipulador>();
    private final Map<Integer, dados_manipulador> usuário_dados_lição_manipulador = new HashMap<Integer, dados_manipulador>();
    private final Map<Integer, dados_manipulador> transmissão_visual_manipulador = new HashMap<Integer, dados_manipulador>();

    public void registro_Ethernet(int Tipo_VALOR, dados_manipulador manipulador) {
        Ethernet_manipulador.put(Integer.valueOf(Tipo_VALOR & 0xffff), manipulador);
    }

    public void registro_IP(int valor_do_contrato, dados_manipulador manipulador) {
        IP_manipulador.put(Integer.valueOf(valor_do_contrato & 0xff), manipulador);
    }

    public void registro_usuário_dados_lição(int hardware_porta, dados_manipulador manipulador) {
        usuário_dados_lição_manipulador.put(Integer.valueOf(hardware_porta & 0xffff), manipulador);
    }

    public void registro_transmissão_visual(int hardware_porta, dados_manipulador manipulador) {
        transmissão_visual_manipulador.put(Integer.valueOf(hardware_porta & 0xffff), manipulador);
    }

    public boolean receber_Ethernet(byte[] quadro_ÍNDICE) {
        if (!rede_Ferramentas.TI_Ethernet_quadro(quadro_ÍNDICE)) {
            return false;
        }
        int Tipo_VALOR = rede_Ferramentas.Ethernet_MAIÚSCULA_protocolo(quadro_ÍNDICE);
        dados_manipulador 직접처리기 = Ethernet_manipulador.get(Integer.valueOf(Tipo_VALOR));
        if (직접처리기 != null) {
            직접처리기.Processo_VALOR_entrada(quadro_ÍNDICE, 14, quadro_ÍNDICE.length - 14);
            return true;
        }
        return Tipo_VALOR == 0x0800 && receber_malha_pacote(quadro_ÍNDICE, 14);
    }

    private boolean receber_malha_pacote(byte[] dados, int iniciar) {
        if (!rede_Ferramentas.TI_IPV_4_protocolo(dados, iniciar)) {
            return false;
        }
        int Cabeçalho_duração = (dados[iniciar] & 0x0f) * 4;
        int total_duração = rede_Ferramentas.큰순서짧은정수(dados, iniciar + 2);
        if (total_duração < Cabeçalho_duração || iniciar + total_duração > dados.length) {
            return false;
        }
        int valor_do_contrato = dados[iniciar + 9] & 0xff;
        int Conteúdo_START = iniciar + Cabeçalho_duração;
        int Conteúdo_duração = total_duração - Cabeçalho_duração;
        dados_manipulador 직접처리기 = IP_manipulador.get(Integer.valueOf(valor_do_contrato));
        if (직접처리기 != null) {
            직접처리기.Processo_VALOR_entrada(dados, Conteúdo_START, Conteúdo_duração);
            return true;
        }
        if (Conteúdo_duração < 4) {
            return false;
        }
        int destino_número_da_porta = rede_Ferramentas.큰순서짧은정수(dados, Conteúdo_START + 2);
        Map<Integer, dados_manipulador> porta_tabela = valor_do_contrato == 17 ? usuário_dados_lição_manipulador : valor_do_contrato == 6 ? transmissão_visual_manipulador : null;
        if (porta_tabela == null) {
            return false;
        }
        dados_manipulador porta_manipulador = porta_tabela.get(Integer.valueOf(destino_número_da_porta));
        if (porta_manipulador == null) {
            return false;
        }
        porta_manipulador.Processo_VALOR_entrada(dados, Conteúdo_START, Conteúdo_duração);
        return true;
    }
}

