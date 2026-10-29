// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Română.propriu;
/** Română 화면 구성요소를 만드는 편의 funcție_VALUE. */
public final class widget {
    private widget() {}
    public static void 나중에실행(실행할일 sarcină_Acțiune) { eveniment_coadă.나중에실행(sarcină_Acțiune); }
    public static Etichetă eticheta_VALUE(String SMS, int 가로, int Verticală_poziție, int 폭, int 높이) {
        return new Etichetă(SMS, 가로, Verticală_poziție, 폭, 높이);
    }
    public static buton buton(String SMS, int 가로, int Verticală_poziție, int 폭, int 높이, 동작받이 받이) {
        return new buton(SMS, 가로, Verticală_poziție, 폭, 높이, 받이);
    }
    public static câmp_text câmp_text(String SMS, int 가로, int Verticală_poziție, int 폭, int 높이) {
        return new câmp_text(SMS, 가로, Verticală_poziție, 폭, 높이);
    }
}
