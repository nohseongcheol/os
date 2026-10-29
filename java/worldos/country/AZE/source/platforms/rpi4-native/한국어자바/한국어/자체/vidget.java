// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자체;
/** 한국어 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class vidget {
    private vidget() {}
    public static void 나중에실행(실행할일 tapşırıq_aktiv) { hadisə_növbə.나중에실행(tapşırıq_aktiv); }
    public static Etiket teq_VALUE(String Mətn, int 가로, int Şaquli_yerinə_qoymaq, int 폭, int 높이) {
        return new Etiket(Mətn, 가로, Şaquli_yerinə_qoymaq, 폭, 높이);
    }
    public static düymə düymə(String Mətn, int 가로, int Şaquli_yerinə_qoymaq, int 폭, int 높이, 동작받이 받이) {
        return new düymə(Mətn, 가로, Şaquli_yerinə_qoymaq, 폭, 높이, 받이);
    }
    public static SMS_sahə SMS_sahə(String Mətn, int 가로, int Şaquli_yerinə_qoymaq, int 폭, int 높이) {
        return new SMS_sahə(Mətn, 가로, Şaquli_yerinə_qoymaq, 폭, 높이);
    }
}
