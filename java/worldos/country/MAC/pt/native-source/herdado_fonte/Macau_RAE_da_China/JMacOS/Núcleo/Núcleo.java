// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Macau_RAE_da_China.JMacOS.Núcleo;

import Macau_RAE_da_China.JMacOS.Memória_região.Memória_gerente;
import Macau_RAE_da_China.JMacOS.Memória_região.Gerenciador_de_Páginas;
import Macau_RAE_da_China.JMacOS.entrada_VALOR.entrada_gerente;
import Macau_RAE_da_China.JMacOS.작업.Processo_VALOR;
import Macau_RAE_da_China.JMacOS.작업.Agendador;
import Macau_RAE_da_China.JMacOS.chamada_ao_sistema.chamada_ao_sistema;
import Macau_RAE_da_China.JMacOS.sistema_de_arquivos.Arquivo_descritor_tabela;
import Macau_RAE_da_China.JMacOS.sistema_de_arquivos.sistema_de_arquivos;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class Núcleo {
    private final hardware_VALOR celular_VALOR;
    private final Memória_gerente Memória_região = new Memória_gerente(32 * 1024 * 1024);
    private final Gerenciador_de_Páginas 쪽관리 = new Gerenciador_de_Páginas();
    private final sistema_de_arquivos sistema_de_arquivos = new sistema_de_arquivos();
    private final Agendador Agendador = new Agendador(쪽관리);
    private final entrada_gerente 입력관리 = new entrada_gerente(256);
    private final Processo_VALOR 첫과정;
    private final chamada_ao_sistema chamada_ao_sistema;

    public Núcleo(hardware_VALOR celular_VALOR) {
        this.celular_VALOR = celular_VALOR;
        첫과정 = Agendador.첫과정(new Arquivo_descritor_tabela(sistema_de_arquivos));
        chamada_ao_sistema = new chamada_ao_sistema(sistema_de_arquivos, 쪽관리, Agendador, celular_VALOR, 입력관리);
    }

    public void iniciar() {
        celular_VALOR.직렬출력("=== JMacOS 관리 kernel_VALOR ===\n");
    }

    public void Executar_etapa() {
        celular_VALOR.중앙처리장치멈춤();
    }

    public Memória_gerente Memória_região() {
        return Memória_região;
    }

    public Gerenciador_de_Páginas 쪽관리() {
        return 쪽관리;
    }

    public sistema_de_arquivos sistema_de_arquivos() {
        return sistema_de_arquivos;
    }

    public Agendador Agendador() {
        return Agendador;
    }

    public entrada_gerente 입력관리() {
        return 입력관리;
    }

    public Processo_VALOR 첫과정() {
        return 첫과정;
    }

    public chamada_ao_sistema chamada_ao_sistema() {
        return chamada_ao_sistema;
    }
}
