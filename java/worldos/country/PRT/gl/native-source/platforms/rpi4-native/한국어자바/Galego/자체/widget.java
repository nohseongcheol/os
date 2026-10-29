// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Galego.자체;
/** Galego 화면 구성요소를 만드는 편의 FUNCIÓN_VALOR. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 tarefa_acción) { evento_cola.나중에실행(tarefa_acción); }
    public static Etiqueta etiqueta_VALOR(String Texto, int 가로, int Vertical_cargo, int 폭, int 높이) {
        return new Etiqueta(Texto, 가로, Vertical_cargo, 폭, 높이);
    }
    public static botón botón(String Texto, int 가로, int Vertical_cargo, int 폭, int 높이, 동작받이 받이) {
        return new botón(Texto, 가로, Vertical_cargo, 폭, 높이, 받이);
    }
    public static SMS_campo SMS_campo(String Texto, int 가로, int Vertical_cargo, int 폭, int 높이) {
        return new SMS_campo(Texto, 가로, Vertical_cargo, 폭, 높이);
    }
}
