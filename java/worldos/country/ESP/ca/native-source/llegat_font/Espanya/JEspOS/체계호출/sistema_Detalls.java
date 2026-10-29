// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.체계호출;

public final class sistema_Detalls {
    private final String sistema_nom;
    private final String node_nom;
    private final String 배포판;
    private final String versió_VALOR;
    private final String màquina;

    public sistema_Detalls(String sistema_nom, String node_nom, String 배포판, String versió_VALOR, String màquina) {
        this.sistema_nom = sistema_nom;
        this.node_nom = node_nom;
        this.배포판 = 배포판;
        this.versió_VALOR = versió_VALOR;
        this.màquina = màquina;
    }

    public String sistema_nom() { return sistema_nom; }
    public String node_nom() { return node_nom; }
    public String 배포판() { return 배포판; }
    public String versió_VALOR() { return versió_VALOR; }
    public String màquina() { return màquina; }
}
