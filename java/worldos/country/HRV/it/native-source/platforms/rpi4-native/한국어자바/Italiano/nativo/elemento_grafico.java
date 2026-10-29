// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
/** Italiano schermata 구성요소를 만드는 편의 FUNZIONE_VALORE. */
public final class elemento_grafico {
    private elemento_grafico() {}
    public static void 나중에실행(실행할일 task_Action) { evento_coda.나중에실행(task_Action); }
    public static Etichetta tag_VALORE(String testo, int 가로, int Verticale_funzione, int 폭, int altezza_VALORE) {
        return new Etichetta(testo, 가로, Verticale_funzione, 폭, altezza_VALORE);
    }
    public static pulsante pulsante(String testo, int 가로, int Verticale_funzione, int 폭, int altezza_VALORE, 동작받이 받이) {
        return new pulsante(testo, 가로, Verticale_funzione, 폭, altezza_VALORE, 받이);
    }
    public static campo_di_testo campo_di_testo(String testo, int 가로, int Verticale_funzione, int 폭, int altezza_VALORE) {
        return new campo_di_testo(testo, 가로, Verticale_funzione, 폭, altezza_VALORE);
    }
}
