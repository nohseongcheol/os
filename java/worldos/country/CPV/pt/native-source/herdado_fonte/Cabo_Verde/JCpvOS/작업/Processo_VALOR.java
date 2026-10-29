// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cabo_Verde.JCpvOS.작업;

import Cabo_Verde.JCpvOS.Memória_região.Gerenciador_de_Páginas;
import Cabo_Verde.JCpvOS.sistema_de_arquivos.Arquivo_descritor_tabela;

public final class Processo_VALOR {
    private final int identificador_VALOR;
    private final int pai_identificador;
    private final Gerenciador_de_Páginas.espaço_de_endereço espaço_de_endereço;
    private final Arquivo_descritor_tabela Arquivo_descritor;
    private Processo_Estado Estado_VALOR = Processo_Estado.Preparar;
    private int código_de_saída;
    private int app_intervalo = 0x06000000;
    private int execução_START_email;
    private String[] execução_argumento = new String[0];
    private String[] ambiente_VALOR = new String[0];

    Processo_VALOR(int identificador_VALOR, int pai_identificador, Gerenciador_de_Páginas.espaço_de_endereço espaço_de_endereço, Arquivo_descritor_tabela Arquivo_descritor) {
        this.identificador_VALOR = identificador_VALOR;
        this.pai_identificador = pai_identificador;
        this.espaço_de_endereço = espaço_de_endereço;
        this.Arquivo_descritor = Arquivo_descritor;
    }

    public int identificador_VALOR() {
        return identificador_VALOR;
    }

    public int pai_identificador() {
        return pai_identificador;
    }

    public Gerenciador_de_Páginas.espaço_de_endereço espaço_de_endereço() {
        return espaço_de_endereço;
    }

    public Arquivo_descritor_tabela Arquivo_descritor() {
        return Arquivo_descritor;
    }

    public Processo_Estado Estado_VALOR() {
        return Estado_VALOR;
    }

    public void set_Estado(Processo_Estado 새상태) {
        Estado_VALOR = 새상태;
    }

    public int código_de_saída() {
        return código_de_saída;
    }

    public void sair_app(int VALOR) {
        código_de_saída = VALOR & 0xff;
        Estado_VALOR = Processo_Estado.sair_app;
    }

    public int app_intervalo() {
        return app_intervalo;
    }

    public void set_app_intervalo(int 새끝) {
        if (새끝 < 0x06000000 || 새끝 > 0x07000000) {
            throw new IllegalArgumentException("app_f5044b9b 끝 범위를 벗어났습니다.");
        }
        app_intervalo = 새끝;
    }

    public void set_contexto(int START_email, String[] parâmetro_argumento, String[] ambiente) {
        execução_START_email = START_email;
        execução_argumento = parâmetro_argumento.clone();
        ambiente_VALOR = ambiente.clone();
    }

    public int execução_START_email() { return execução_START_email; }
    public String[] execução_argumento() { return execução_argumento.clone(); }
    public String[] ambiente_VALOR() { return ambiente_VALOR.clone(); }
}
