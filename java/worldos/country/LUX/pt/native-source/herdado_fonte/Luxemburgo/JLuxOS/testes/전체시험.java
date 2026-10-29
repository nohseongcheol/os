// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Luxemburgo.JLuxOS.testes;

import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import Luxemburgo.JLuxOS.Memória_região.Memória_gerente;
import Luxemburgo.JLuxOS.Memória_região.Gerenciador_de_Páginas;
import Luxemburgo.JLuxOS.entrada_VALOR.entrada_Evento;
import Luxemburgo.JLuxOS.작업.Processo_VALOR;
import Luxemburgo.JLuxOS.chamada_ao_sistema.chamada_ao_sistema;
import Luxemburgo.JLuxOS.sistema_de_arquivos.executável_carregador;
import Luxemburgo.JLuxOS.Núcleo.Núcleo;
import Luxemburgo.JLuxOS.host.host_hardware;
import Luxemburgo.JLuxOS.IRQ.IRQ_gerente;
import Luxemburgo.JLuxOS.descritor_entrada.Global_descritor_tabela;
import Luxemburgo.JLuxOS.dispositivo_de_armazenamento.고급기술결합장치;
import Luxemburgo.JLuxOS.celular_VALOR.acessório_barramento_gerente;
import Luxemburgo.JLuxOS.rede_pilha.rede_Ferramentas;
import Luxemburgo.JLuxOS.rede_pilha.camada_de_rede;
import Luxemburgo.JLuxOS.celular_VALOR.Relógio;
import Luxemburgo.JLuxOS.descritor_entrada.Tarefa_Estado_segmento;
import Luxemburgo.JLuxOS.tela.caractere_visor;
import Luxemburgo.JLuxOS.sistema_de_arquivos.partição_primária_tabela;

public final class 전체시험 {
    private static int 통과수;

    private 전체시험() {
    }

    public static void main(String[] parâmetro_argumento) {
        host_hardware celular_VALOR = new host_hardware();
        Núcleo kernel_VALOR = new Núcleo(celular_VALOR);
        kernel_VALOR.iniciar();

        teste_Memória(kernel_VALOR);
        쪽관리시험(kernel_VALOR);
        파일과과정시험(kernel_VALOR);
        실행파일시험(kernel_VALOR);
        teste_entrada(kernel_VALOR);
        teste_hardware(celular_VALOR);
        개입중단과서술자시험();
        teste_Armazenamento_E_Rede();
        teste_tela_E_Relógio();

        System.out.println("JLuxOS testes 통과: " + 통과수);
    }

    private static void teste_Memória(Núcleo kernel_VALOR) {
        Memória_gerente gerente_VALOR = kernel_VALOR.Memória_região();
        int 첫주소 = gerente_VALOR.정렬할당(100, 64);
        verificar((첫주소 & 63) == 0, "alinhar_VALOR alocar_Armazenamento");
        gerente_VALOR.gravar_byte_VALOR(첫주소, (byte) 0x5a);
        verificar(gerente_VALOR.leitura_byte_VALOR(첫주소) == (byte) 0x5a, "물리 Memória_região 읽고 Escrita");
        int 사용전 = gerente_VALOR.사용크기();
        gerente_VALOR.lançar_Armazenamento(첫주소);
        verificar(gerente_VALOR.사용크기() < 사용전, "Memória_região lançar_Armazenamento");
    }

    private static void 쪽관리시험(Núcleo kernel_VALOR) {
        Gerenciador_de_Páginas gerente_VALOR = kernel_VALOR.쪽관리();
        Gerenciador_de_Páginas.espaço_de_endereço pai_ESPAÇO = gerente_VALOR.새주소공간();
        gerente_VALOR.MAP_página(pai_ESPAÇO, 0x1000, true);
        gerente_VALOR.gravar_byte_VALOR(pai_ESPAÇO, 0x1010, (byte) 7);
        Gerenciador_de_Páginas.espaço_de_endereço filho_ESPAÇO = gerente_VALOR.clone_COW(pai_ESPAÇO);
        gerente_VALOR.gravar_byte_VALOR(filho_ESPAÇO, 0x1010, (byte) 9);
        verificar(gerente_VALOR.leitura_byte_VALOR(pai_ESPAÇO, 0x1010) == 7, "Escrita 시 copiar_VALOR pai_VALOR 격리");
        verificar(gerente_VALOR.leitura_byte_VALOR(filho_ESPAÇO, 0x1010) == 9, "Escrita 시 copiar_VALOR filho_VALOR Escrita");
    }

    private static void 파일과과정시험(Núcleo kernel_VALOR) {
        byte[] Conteúdo_VALOR = "안녕하세요".getBytes(StandardCharsets.UTF_8);
        kernel_VALOR.sistema_de_arquivos().Acrescentar_Arquivo("testes", Conteúdo_VALOR);
        Processo_VALOR pai_VALOR = kernel_VALOR.첫과정();
        chamada_ao_sistema 호출 = kernel_VALOR.chamada_ao_sistema();
        int descritor_entrada = 호출.Abrir(pai_VALOR, "/testes", chamada_ao_sistema.somente_leitura_sinalizar);
        verificar(descritor_entrada >= 3, "ficheiro Abrir");

        byte[] receber_destino = new byte[Conteúdo_VALOR.length];
        verificar(호출.Leitura(pai_VALOR, descritor_entrada, receber_destino, receber_destino.length) == Conteúdo_VALOR.length, "ficheiro Leitura");
        verificar(Arrays.equals(Conteúdo_VALOR, receber_destino), "ficheiro Conteúdo_VALOR");
        verificar(호출.mover_cargo(pai_VALOR, descritor_entrada, 0, chamada_ao_sistema.busca_START) == 0, "ficheiro posição mover_VALOR");

        int 복제서술자 = 호출.Duplicar_descritor(pai_VALOR, descritor_entrada);
        verificar(복제서술자 >= 0, "descritor_entrada clone_VALOR");
        Processo_VALOR filho_VALOR = 호출.clone_Processo(pai_VALOR);
        verificar(filho_VALOR.identificador_VALOR() != pai_VALOR.identificador_VALOR(), "Processo_VALOR identificador_VALOR 분리");
        verificar(filho_VALOR.pai_identificador() == pai_VALOR.identificador_VALOR(), "pai_VALOR Processo_VALOR identificador_VALOR");
        verificar(호출.Fechar(filho_VALOR, descritor_entrada) == 0 && pai_VALOR.Arquivo_descritor().TI_abrir(descritor_entrada), "filho_VALOR Fechar 격리");

        int Anterior_encerrar = 호출.프로그램끝늘리기(pai_VALOR, 8192);
        verificar(Anterior_encerrar == 0x06000000, "app_f5044b9b 끝 늘리기");
        verificar(pai_VALOR.app_intervalo() == 0x06002000, "app_f5044b9b 끝 반영");
        verificar(filho_VALOR.app_intervalo() == 0x06000000, "과정별 app_f5044b9b 끝 격리");

        filho_VALOR.sair_app(7);
        verificar(호출.자식기다리기(pai_VALOR, filho_VALOR.identificador_VALOR(), false) == (7 << 8), "filho_VALOR sair_app 기다리기");
        verificar(호출.접근가능("testes", 1) == -13, "Executar_comando Permissão_VALOR rejeitar_VALOR");
        verificar(호출.UID() == 0 && 호출.GID() == 0, "사용자와 무리 identificador_VALOR");
        verificar("/".equals(호출.em_dia_Lista_de_Tarefas(2)) && 호출.mudar_Lista_de_Tarefas("/") == 0, "em_dia_item 작업 entrada_Lista_f07b3200");
        verificar(호출.TI_Terminal(pai_VALOR, 1), "표준 saídaTexto 단말");
        verificar("JLuxOS".equals(호출.Sistema_Detalhes().Sistema_nome()), "SO_VALOR msinfo32_exe");
    }

    private static void 실행파일시험(Núcleo kernel_VALOR) {
        byte[] dados = new byte[92];
        dados[0] = 0x7f;
        dados[1] = 'E';
        dados[2] = 'L';
        dados[3] = 'F';
        dados[4] = 1;
        dados[5] = 1;
        gravar_inteiro_VALOR(dados, 24, 0x04001000);
        gravar_inteiro_VALOR(dados, 32, 52);
        짧은정수쓰기(dados, 46, 40);
        짧은정수쓰기(dados, 48, 1);
        gravar_inteiro_VALOR(dados, 56, 8);
        gravar_inteiro_VALOR(dados, 60, 2);
        gravar_inteiro_VALOR(dados, 64, 0x04002000);
        gravar_inteiro_VALOR(dados, 72, 64);

        executável_carregador.foto foto_VALOR = new executável_carregador().검사(dados);
        verificar(foto_VALOR.START_email() == 0x04001000, "ELF iniciar Endereço");
        verificar(foto_VALOR.구역들().size() == 1 && foto_VALOR.구역들().get(0).Tipo_VALOR() == 8, "ELF 빈 dados seção_VALOR");
        int descritor_entrada = kernel_VALOR.chamada_ao_sistema().Abrir(kernel_VALOR.첫과정(), "testes", chamada_ao_sistema.somente_leitura_sinalizar);
        verificar(kernel_VALOR.chamada_ao_sistema().controlo_de_ficheiro(kernel_VALOR.첫과정(), descritor_entrada, 2, 1) == 0, "Executar_comando 시 Fechar Definições");
        verificar(kernel_VALOR.chamada_ao_sistema().Executar_comando(kernel_VALOR.첫과정(), dados, new String[] {"testes", "값"}, new String[] {"Idioma=Português"}) == 0, "ELF Executar_comando foto_VALOR 적재");
        verificar(kernel_VALOR.첫과정().execução_START_email() == 0x04001000, "Executar_comando iniciar Endereço 반영");
        verificar(kernel_VALOR.첫과정().execução_argumento().length == 2 && kernel_VALOR.첫과정().ambiente_VALOR().length == 1, "Executar_comando 인자와 ambiente");
        verificar(!kernel_VALOR.첫과정().Arquivo_descritor().TI_abrir(descritor_entrada), "Executar_comando 시 descritor_entrada Fechar");
        verificar(kernel_VALOR.쪽관리().leitura_byte_VALOR(kernel_VALOR.첫과정().espaço_de_endereço(), 0x04002000) == 0, "빈 dados seção_VALOR zero_operando inicializar");
    }

    private static void teste_entrada(Núcleo kernel_VALOR) {
        kernel_VALOR.입력관리().Chave_inoperante('가');
        kernel_VALOR.입력관리().쥐이동(3, -2);
        entrada_Evento 첫사건 = kernel_VALOR.입력관리().Avançar_Evento();
        entrada_Evento SEGUNDO_Evento = kernel_VALOR.입력관리().Avançar_Evento();
        verificar(첫사건.tipo_de_evento() == entrada_Evento.Tipo_VALOR.Chave_inoperante, "자판 Evento");
        verificar(SEGUNDO_Evento.첫째값() == 3 && SEGUNDO_Evento.SEGUNDO_VALOR() == -2, "쥐 mover_VALOR Evento");
    }

    private static void teste_hardware(host_hardware celular_VALOR) {
        celular_VALOR.gravar_porta_byte(0x3f8, 0xab);
        verificar(celular_VALOR.leitura_porta_byte(0x3f8) == 0xab, "hardware_porta E_S limite_VALOR");
        verificar(celular_VALOR.직렬기록().contains("JLuxOS"), "직렬 LOG_linha");
    }

    private static void 개입중단과서술자시험() {
        IRQ_gerente gerente_VALOR = new IRQ_gerente();
        gerente_VALOR.registro_entrada(0x21, Armazenamento_email -> Armazenamento_email + 4);
        gerente_VALOR.ligar();
        verificar(gerente_VALOR.distribuir_VALOR(0x21, 100) == 104, "IRQ distribuir_VALOR");
        gerente_VALOR.desativar();
        verificar(gerente_VALOR.distribuir_VALOR(0x21, 100) == 100, "IRQ desativar");

        Global_descritor_tabela descritor_tabela = new Global_descritor_tabela();
        descritor_tabela.set_valor_padrão();
        verificar(descritor_tabela.조각들().size() == 5, "전역 descritor_tabela");
        Tarefa_Estado_segmento Tarefa_Estado = new Tarefa_Estado_segmento();
        Tarefa_Estado.특권쌓임공간설정(0x10, 0x800000);
        verificar(Tarefa_Estado.pilha_zero_bloco() == 0x10 && Tarefa_Estado.pilha_zero_email() == 0x800000, "작업 Estado_VALOR seção_VALOR");
    }

    private static void teste_Armazenamento_E_Rede() {
        고급기술결합장치 dispositivo_de_armazenamento = new 고급기술결합장치(4, false);
        byte[] 쓸자료 = new byte[고급기술결합장치.seção_dimensionar];
        byte[] leitura_dados_VALOR = new byte[고급기술결합장치.seção_dimensionar];
        쓸자료[17] = 42;
        dispositivo_de_armazenamento.Escrita(2, 쓸자료);
        dispositivo_de_armazenamento.Leitura(2, leitura_dados_VALOR);
        verificar(leitura_dados_VALOR[17] == 42, "ATA seção_VALOR 읽고 Escrita");

        acessório_barramento_gerente acessório = new acessório_barramento_gerente();
        acessório.발견(new acessório_barramento_gerente.celular_VALOR(0x1022, 0x2000, 0xc000, 11));
        verificar(acessório.PROCURAR_entrada(0x1022, 0x2000) != null, "주변 celular_VALOR PROCURAR_entrada");

        byte[] Ethernet_quadro = new byte[34];
        Ethernet_quadro[12] = 0x08;
        Ethernet_quadro[13] = 0x00;
        Ethernet_quadro[14] = 0x45;
        verificar(rede_Ferramentas.Ethernet_MAIÚSCULA_protocolo(Ethernet_quadro) == 0x0800, "이더넷 상위 valor_do_contrato");
        verificar(rede_Ferramentas.TI_IPV_4_protocolo(Ethernet_quadro, 14), "상호통신망규약 4판");
        verificar(rede_Ferramentas.malha_soma_de_verificação(new byte[] {0, 0}, 0, 2) == 0xffff, "인터넷 soma_de_verificação");

        byte[] 첫구역 = new byte[512];
        첫구역[510] = 0x55;
        첫구역[511] = (byte) 0xaa;
        첫구역[450] = 0x0b;
        gravar_inteiro_VALOR(첫구역, 454, 63);
        gravar_inteiro_VALOR(첫구역, 458, 1024);
        verificar(new partição_primária_tabela().Leitura(첫구역).size() == 1, "valor_padrão 분할 영역표");

        camada_de_rede camada_VALOR = new camada_de_rede();
        int[] RECEBER_CONT_NÚM = new int[1];
        camada_VALOR.registro_usuário_dados_lição(7, (dados, iniciar, duração_VALOR) -> RECEBER_CONT_NÚM[0]++);
        byte[] quadro_ÍNDICE = new byte[14 + 20 + 8];
        quadro_ÍNDICE[12] = 0x08;
        quadro_ÍNDICE[13] = 0x00;
        quadro_ÍNDICE[14] = 0x45;
        quadro_ÍNDICE[16] = 0;
        quadro_ÍNDICE[17] = 28;
        quadro_ÍNDICE[23] = 17;
        quadro_ÍNDICE[36] = 0;
        quadro_ÍNDICE[37] = 7;
        verificar(camada_VALOR.receber_Ethernet(quadro_ÍNDICE) && RECEBER_CONT_NÚM[0] == 1, "espaço_do_utilizador dados lição_VALOR distribuir_VALOR");
    }

    private static void teste_tela_E_Relógio() {
        caractere_visor tela = new caractere_visor();
        tela.saídaTexto("가나\n다");
        verificar(tela.문자(0, 0) == '가' && tela.문자(0, 1) == '다', "문자 tela saídaTexto");
        Relógio Relógio = new Relógio(100);
        for (int ÍNDICE = 0; ÍNDICE < 10; ÍNDICE++) {
            Relógio.tique_VALOR();
        }
        verificar(Relógio.지난밀리초() == 100, "Relógio tique_VALOR CONVERTER_VALOR");
    }

    private static void gravar_inteiro_VALOR(byte[] dados, int posição, int VALOR) {
        dados[posição] = (byte) VALOR;
        dados[posição + 1] = (byte) (VALOR >>> 8);
        dados[posição + 2] = (byte) (VALOR >>> 16);
        dados[posição + 3] = (byte) (VALOR >>> 24);
    }

    private static void 짧은정수쓰기(byte[] dados, int posição, int VALOR) {
        dados[posição] = (byte) VALOR;
        dados[posição + 1] = (byte) (VALOR >>> 8);
    }

    private static void verificar(boolean doença, String Nome) {
        if (!doença) {
            throw new AssertionError("falha_VALOR: " + Nome);
        }
        통과수++;
        System.out.println("통과: " + Nome);
    }
}
