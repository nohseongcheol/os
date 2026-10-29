// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Angola.JAgoOS.chamada_ao_sistema;

public final class Sistema_Detalhes {
    private final String Sistema_nome;
    private final String nó_nome;
    private final String edição_VALOR;
    private final String versão_VALOR;
    private final String computador;

    public Sistema_Detalhes(String Sistema_nome, String nó_nome, String edição_VALOR, String versão_VALOR, String computador) {
        this.Sistema_nome = Sistema_nome;
        this.nó_nome = nó_nome;
        this.edição_VALOR = edição_VALOR;
        this.versão_VALOR = versão_VALOR;
        this.computador = computador;
    }

    public String Sistema_nome() { return Sistema_nome; }
    public String nó_nome() { return nó_nome; }
    public String edição_VALOR() { return edição_VALOR; }
    public String versão_VALOR() { return versão_VALOR; }
    public String computador() { return computador; }
}
