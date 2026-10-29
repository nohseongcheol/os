// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Cymraeg.자체;
/** Cymraeg 화면 구성요소를 만드는 편의 SWYDDOGAETH_VALUE. */
public final class teclyn {
    private teclyn() {}
    public static void 나중에실행(실행할일 tasg_gweithred) { digwyddiad_ciw.나중에실행(tasg_gweithred); }
    public static label tag_VALUE(String Testun, int 가로, int Ar_i_fyny_safle, int 폭, int 높이) {
        return new label(Testun, 가로, Ar_i_fyny_safle, 폭, 높이);
    }
    public static botwm botwm(String Testun, int 가로, int Ar_i_fyny_safle, int 폭, int 높이, 동작받이 받이) {
        return new botwm(Testun, 가로, Ar_i_fyny_safle, 폭, 높이, 받이);
    }
    public static maes_testun maes_testun(String Testun, int 가로, int Ar_i_fyny_safle, int 폭, int 높이) {
        return new maes_testun(Testun, 가로, Ar_i_fyny_safle, 폭, 높이);
    }
}
