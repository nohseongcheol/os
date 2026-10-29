// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Euskara.자체;
/** Euskara 화면 구성요소를 만드는 편의 FUNTZIOA_balio. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 ataza_ekintza) { gertaera_ilara.나중에실행(ataza_ekintza); }
    public static Etiketa etiketa_balio(String Testua, int 가로, int Bertikala_kargu, int 폭, int 높이) {
        return new Etiketa(Testua, 가로, Bertikala_kargu, 폭, 높이);
    }
    public static botoia botoia(String Testua, int 가로, int Bertikala_kargu, int 폭, int 높이, 동작받이 받이) {
        return new botoia(Testua, 가로, Bertikala_kargu, 폭, 높이, 받이);
    }
    public static SMS_eremu SMS_eremu(String Testua, int 가로, int Bertikala_kargu, int 폭, int 높이) {
        return new SMS_eremu(Testua, 가로, Bertikala_kargu, 폭, 높이);
    }
}
