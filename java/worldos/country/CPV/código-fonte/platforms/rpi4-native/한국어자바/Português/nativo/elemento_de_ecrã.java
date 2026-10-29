// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Português.nativo;
/** Português tela 구성요소를 만드는 편의 FUNÇÃO_VALOR. */
public final class elemento_de_ecrã {
    private elemento_de_ecrã() {}
    public static void 나중에실행(실행할일 Tarefa_Ação) { Evento_Fila.나중에실행(Tarefa_Ação); }
    public static Etiqueta tag_VALOR(String texto, int 가로, int Vertical_cargo, int 폭, int altura_VALOR) {
        return new Etiqueta(texto, 가로, Vertical_cargo, 폭, altura_VALOR);
    }
    public static botão botão(String texto, int 가로, int Vertical_cargo, int 폭, int altura_VALOR, 동작받이 받이) {
        return new botão(texto, 가로, Vertical_cargo, 폭, altura_VALOR, 받이);
    }
    public static campo_de_texto campo_de_texto(String texto, int 가로, int Vertical_cargo, int 폭, int altura_VALOR) {
        return new campo_de_texto(texto, 가로, Vertical_cargo, 폭, altura_VALOR);
    }
}
