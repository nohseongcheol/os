// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Guiné_Equatorial.JGnqOS.chamada_ao_sistema;

import Guiné_Equatorial.JGnqOS.Memória_região.Gerenciador_de_Páginas;
import Guiné_Equatorial.JGnqOS.작업.Processo_VALOR;
import Guiné_Equatorial.JGnqOS.작업.Agendador;
import Guiné_Equatorial.JGnqOS.sistema_de_arquivos.executável_carregador;
import Guiné_Equatorial.JGnqOS.sistema_de_arquivos.sistema_de_arquivos;
import Guiné_Equatorial.JGnqOS.sistema_de_arquivos.Arquivo_informações;
import Guiné_Equatorial.JGnqOS.Núcleo.hardware_VALOR;
import Guiné_Equatorial.JGnqOS.entrada_VALOR.entrada_gerente;
import Guiné_Equatorial.JGnqOS.entrada_VALOR.entrada_Evento;

/** engos POSIX 1단계 호출의 Java 관리 계층이다. */
public final class chamada_ao_sistema {
    public static final int somente_leitura_sinalizar = 0;
    public static final int busca_START = 0;
    public static final int busca_em_dia = 1;
    public static final int PROCURAR_entrada_encerrar = 2;

    private final sistema_de_arquivos sistema_de_arquivos;
    private final Gerenciador_de_Páginas 쪽관리;
    private final Agendador Agendador;
    private final executável_carregador carregador = new executável_carregador();
    private final hardware_VALOR celular_VALOR;
    private final entrada_gerente 입력관리;

    public chamada_ao_sistema(sistema_de_arquivos sistema_de_arquivos, Gerenciador_de_Páginas 쪽관리, Agendador Agendador, hardware_VALOR celular_VALOR, entrada_gerente 입력관리) {
        this.sistema_de_arquivos = sistema_de_arquivos;
        this.쪽관리 = 쪽관리;
        this.Agendador = Agendador;
        this.celular_VALOR = celular_VALOR;
        this.입력관리 = 입력관리;
    }

    public int Processo_identificador(Processo_VALOR em_dia_Processo) {
        return em_dia_Processo.identificador_VALOR();
    }

    public int pai_Processo_identificador(Processo_VALOR em_dia_Processo) {
        return em_dia_Processo.pai_identificador();
    }

    public int Abrir(Processo_VALOR em_dia_Processo, String Nome, int sinalizar_VALOR) {
        if (sinalizar_VALOR != somente_leitura_sinalizar) {
            return -30;
        }
        return em_dia_Processo.Arquivo_descritor().Abrir(Nome);
    }

    public int Leitura(Processo_VALOR em_dia_Processo, int descritor_entrada, byte[] receber_destino, int Tamanho) {
        if (descritor_entrada == 0) {
            if (Tamanho <= 0 || receber_destino.length == 0) {
                return 0;
            }
            entrada_Evento Evento = 입력관리.Avançar_Evento();
            if (Evento == null || Evento.tipo_de_evento() != entrada_Evento.Tipo_VALOR.Chave_inoperante) {
                return -11;
            }
            receber_destino[0] = (byte) Evento.첫째값();
            return 1;
        }
        return em_dia_Processo.Arquivo_descritor().Leitura(descritor_entrada, receber_destino, Tamanho);
    }

    public int Escrita(Processo_VALOR em_dia_Processo, int descritor_entrada, byte[] dados, int Tamanho) {
        if (descritor_entrada != 1 && descritor_entrada != 2) {
            return em_dia_Processo.Arquivo_descritor().TI_abrir(descritor_entrada) ? -30 : -9;
        }
        if (Tamanho < 0 || Tamanho > dados.length) {
            return -22;
        }
        celular_VALOR.직렬출력(new String(dados, 0, Tamanho, java.nio.charset.StandardCharsets.UTF_8));
        return Tamanho;
    }

    public int Fechar(Processo_VALOR em_dia_Processo, int descritor_entrada) {
        return em_dia_Processo.Arquivo_descritor().Fechar(descritor_entrada);
    }

    public int mover_cargo(Processo_VALOR em_dia_Processo, int descritor_entrada, int 거리, int ação_raiz) {
        return em_dia_Processo.Arquivo_descritor().mover_cargo(descritor_entrada, 거리, ação_raiz);
    }

    public int Duplicar_descritor(Processo_VALOR em_dia_Processo, int descritor_entrada) {
        return em_dia_Processo.Arquivo_descritor().복제서술자(descritor_entrada, 0);
    }

    public int 지정서술자복제(Processo_VALOR em_dia_Processo, int descritor_entrada, int 새서술자) {
        return em_dia_Processo.Arquivo_descritor().지정복제(descritor_entrada, 새서술자);
    }

    public int 접근가능(String Nome, int método_MODO) {
        Arquivo_informações msinfo32_exe = sistema_de_arquivos.msinfo32_exe(Nome);
        if (msinfo32_exe == null) {
            return -2;
        }
        if ((método_MODO & 1) != 0 && (msinfo32_exe.forma_Tipo() & 0111) == 0) {
            return -13;
        }
        if ((método_MODO & 2) != 0) {
            return -30;
        }
        return 0;
    }

    public int mudar_Lista_de_Tarefas(String Nome) {
        return "/".equals(Nome) ? 0 : -20;
    }

    public String em_dia_Lista_de_Tarefas(int receber_dimensionar) {
        return receber_dimensionar >= 2 ? "/" : null;
    }

    public int UID() { return 0; }
    public int efetivo_UID() { return 0; }
    public int GID() { return 0; }
    public int efetivo_GID() { return 0; }

    public int sincronizar_Arquivo(Processo_VALOR em_dia_Processo, int descritor_entrada) {
        return em_dia_Processo.Arquivo_descritor().msinfo32_exe(descritor_entrada) == null ? -9 : 0;
    }

    public void 모두동기화() {
        // em_dia_item 파일체계는 Leitura 전용이어서 밀어낼 자료가 없다.
    }

    public boolean TI_Terminal(Processo_VALOR em_dia_Processo, int descritor_entrada) {
        Arquivo_informações msinfo32_exe = em_dia_Processo.Arquivo_descritor().msinfo32_exe(descritor_entrada);
        return msinfo32_exe != null && (msinfo32_exe.forma_Tipo() & 0170000) == 0020000;
    }

    public int controlo_de_ficheiro(Processo_VALOR em_dia_Processo, int descritor_entrada, int comando, int parâmetro_argumento) {
        if (comando == 0) {
            return em_dia_Processo.Arquivo_descritor().복제서술자(descritor_entrada, parâmetro_argumento);
        }
        if (comando == 1) {
            return em_dia_Processo.Arquivo_descritor().실행시닫기값(descritor_entrada);
        }
        if (comando == 2) {
            return em_dia_Processo.Arquivo_descritor().실행시닫기설정(descritor_entrada, (parâmetro_argumento & 1) != 0);
        }
        if (comando == 3) {
            return em_dia_Processo.Arquivo_descritor().msinfo32_exe(descritor_entrada) == null ? -9 : somente_leitura_sinalizar;
        }
        if (comando == 4) {
            return parâmetro_argumento == somente_leitura_sinalizar ? 0 : -30;
        }
        return -22;
    }

    public int Criar_entrada(String Nome, int Permissão_VALOR) {
        return -30;
    }

    public Arquivo_informações descritor_informações(Processo_VALOR em_dia_Processo, int descritor_entrada) {
        return em_dia_Processo.Arquivo_descritor().msinfo32_exe(descritor_entrada);
    }

    public Sistema_Detalhes Sistema_Detalhes() {
        return new Sistema_Detalhes("JGnqOS", "JGnqOS", "0.1", "Java managed kernel", "i386");
    }

    public Arquivo_informações Arquivo_informações(String Nome) {
        return sistema_de_arquivos.msinfo32_exe(Nome);
    }

    public Processo_VALOR clone_Processo(Processo_VALOR pai_VALOR) {
        return Agendador.clone_VALOR(pai_VALOR);
    }

    public int 자식기다리기(Processo_VALOR pai_VALOR, int filho_identificador, boolean 기다리지않음) {
        return Agendador.자식기다리기(pai_VALOR, filho_identificador, 기다리지않음);
    }

    public int app_intervalo(Processo_VALOR em_dia_Processo, int 새끝) {
        int Anterior_encerrar = em_dia_Processo.app_intervalo();
        if (새끝 == 0) {
            return Anterior_encerrar;
        }
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            return -12;
        }
        int 첫쪽 = Anterior_encerrar / Gerenciador_de_Páginas.tamanho_da_página;
        int 끝쪽 = (새끝 + Gerenciador_de_Páginas.tamanho_da_página - 1) / Gerenciador_de_Páginas.tamanho_da_página;
        if (새끝 > Anterior_encerrar) {
            for (int ÍNDICE = 첫쪽; ÍNDICE < 끝쪽; ÍNDICE++) {
                int Endereço = ÍNDICE * Gerenciador_de_Páginas.tamanho_da_página;
                try {
                    쪽관리.leitura_byte_VALOR(em_dia_Processo.espaço_de_endereço(), Endereço);
                } catch (IllegalStateException erro) {
                    쪽관리.MAP_página(em_dia_Processo.espaço_de_endereço(), Endereço, true);
                }
            }
        }
        em_dia_Processo.set_app_intervalo(새끝);
        return 새끝;
    }

    public int 프로그램끝늘리기(Processo_VALOR em_dia_Processo, int incremento_valor) {
        int Anterior_encerrar = em_dia_Processo.app_intervalo();
        int resultado = app_intervalo(em_dia_Processo, Anterior_encerrar + incremento_valor);
        return resultado < 0 ? resultado : Anterior_encerrar;
    }

    public int Executar_comando(Processo_VALOR em_dia_Processo, byte[] executável) {
        return Executar_comando(em_dia_Processo, executável, new String[0], new String[0]);
    }

    public int Executar_comando(Processo_VALOR em_dia_Processo, byte[] executável, String[] parâmetro_argumento, String[] ambiente) {
        executável_carregador.foto foto_VALOR;
        try {
            foto_VALOR = carregador.검사(executável);
        } catch (IllegalArgumentException erro) {
            return -8;
        }
        if (parâmetro_argumento == null || ambiente == null || parâmetro_argumento.length > 16 || ambiente.length > 16) {
            return -7;
        }
        for (executável_carregador.seção_VALOR seção_VALOR : foto_VALOR.구역들()) {
            if ((seção_VALOR.sinalizar_VALOR() & 2) == 0 || seção_VALOR.Tamanho() == 0) {
                continue;
            }
            int 첫쪽 = seção_VALOR.Endereço() / Gerenciador_de_Páginas.tamanho_da_página;
            int 끝쪽 = (seção_VALOR.Endereço() + seção_VALOR.Tamanho() + Gerenciador_de_Páginas.tamanho_da_página - 1) / Gerenciador_de_Páginas.tamanho_da_página;
            for (int ÍNDICE = 첫쪽; ÍNDICE < 끝쪽; ÍNDICE++) {
                int Endereço = ÍNDICE * Gerenciador_de_Páginas.tamanho_da_página;
                try {
                    쪽관리.leitura_byte_VALOR(em_dia_Processo.espaço_de_endereço(), Endereço);
                    쪽관리.Bloqueado_alcance_gravar(em_dia_Processo.espaço_de_endereço(), Endereço, Gerenciador_de_Páginas.tamanho_da_página);
                } catch (IllegalStateException erro) {
                    쪽관리.MAP_página(em_dia_Processo.espaço_de_endereço(), Endereço, true);
                }
            }
            for (int ÍNDICE = 0; ÍNDICE < seção_VALOR.Tamanho(); ÍNDICE++) {
                byte VALOR = seção_VALOR.Tipo_VALOR() == 8 ? 0 : executável[seção_VALOR.Arquivo_cargo_2aa21a9a() + ÍNDICE];
                쪽관리.gravar_byte_VALOR(em_dia_Processo.espaço_de_endereço(), seção_VALOR.Endereço() + ÍNDICE, VALOR);
            }
        }
        em_dia_Processo.set_contexto(foto_VALOR.START_email(), parâmetro_argumento, ambiente);
        em_dia_Processo.Arquivo_descritor().실행시닫기();
        return 0;
    }

    public void encerrar_app(Processo_VALOR em_dia_Processo, int Estado_VALOR) {
        em_dia_Processo.sair_app(Estado_VALOR);
    }
}
