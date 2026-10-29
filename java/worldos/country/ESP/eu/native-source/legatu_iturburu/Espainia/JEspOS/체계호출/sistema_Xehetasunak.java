// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espainia.JEspOS.체계호출;

public final class sistema_Xehetasunak {
    private final String sistema_izen;
    private final String nodo_izen;
    private final String 배포판;
    private final String bertsio_balio;
    private final String gailu;

    public sistema_Xehetasunak(String sistema_izen, String nodo_izen, String 배포판, String bertsio_balio, String gailu) {
        this.sistema_izen = sistema_izen;
        this.nodo_izen = nodo_izen;
        this.배포판 = 배포판;
        this.bertsio_balio = bertsio_balio;
        this.gailu = gailu;
    }

    public String sistema_izen() { return sistema_izen; }
    public String nodo_izen() { return nodo_izen; }
    public String 배포판() { return 배포판; }
    public String bertsio_balio() { return bertsio_balio; }
    public String gailu() { return gailu; }
}
