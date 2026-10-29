// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.체계호출;

public final class sistema_Detalles {
    private final String sistema_nome;
    private final String nó_nome;
    private final String 배포판;
    private final String versión_VALOR;
    private final String máquina;

    public sistema_Detalles(String sistema_nome, String nó_nome, String 배포판, String versión_VALOR, String máquina) {
        this.sistema_nome = sistema_nome;
        this.nó_nome = nó_nome;
        this.배포판 = 배포판;
        this.versión_VALOR = versión_VALOR;
        this.máquina = máquina;
    }

    public String sistema_nome() { return sistema_nome; }
    public String nó_nome() { return nó_nome; }
    public String 배포판() { return 배포판; }
    public String versión_VALOR() { return versión_VALOR; }
    public String máquina() { return máquina; }
}
