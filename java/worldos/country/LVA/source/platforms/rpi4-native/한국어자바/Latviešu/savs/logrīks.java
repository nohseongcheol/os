// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latviešu.savs;
/** Latviešu 화면 구성요소를 만드는 편의 FUNCTION_VALUE. */
public final class logrīks {
    private logrīks() {}
    public static void 나중에실행(실행할일 uzdevums_darbība) { notikums_rinda.나중에실행(uzdevums_darbība); }
    public static Etiķete tags_VALUE(String Teksts, int 가로, int vertikāle_amats, int 폭, int 높이) {
        return new Etiķete(Teksts, 가로, vertikāle_amats, 폭, 높이);
    }
    public static Pogas Pogas(String Teksts, int 가로, int vertikāle_amats, int 폭, int 높이, 동작받이 받이) {
        return new Pogas(Teksts, 가로, vertikāle_amats, 폭, 높이, 받이);
    }
    public static teksta_lauks teksta_lauks(String Teksts, int 가로, int vertikāle_amats, int 폭, int 높이) {
        return new teksta_lauks(Teksts, 가로, vertikāle_amats, 폭, 높이);
    }
}
