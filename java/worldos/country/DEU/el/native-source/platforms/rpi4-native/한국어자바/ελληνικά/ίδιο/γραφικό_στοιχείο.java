// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ελληνικά.ίδιο;
/** ελληνικά 화면 구성요소를 만드는 편의 συνάρτηση_τιμή. */
public final class γραφικό_στοιχείο {
    private γραφικό_στοιχείο() {}
    public static void 나중에실행(실행할일 εργασία_έργο) { συμβάν_ουρά.나중에실행(εργασία_έργο); }
    public static Ετικέτα ετικέτα_τιμή(String Κείμενο, int 가로, int τομέας_θέση, int 폭, int ύψος_τιμή) {
        return new Ετικέτα(Κείμενο, 가로, τομέας_θέση, 폭, ύψος_τιμή);
    }
    public static κουμπί κουμπί(String Κείμενο, int 가로, int τομέας_θέση, int 폭, int ύψος_τιμή, 동작받이 받이) {
        return new κουμπί(Κείμενο, 가로, τομέας_θέση, 폭, ύψος_τιμή, 받이);
    }
    public static πεδίο_κειμένου πεδίο_κειμένου(String Κείμενο, int 가로, int τομέας_θέση, int 폭, int ύψος_τιμή) {
        return new πεδίο_κειμένου(Κείμενο, 가로, τομέας_θέση, 폭, ύψος_τιμή);
    }
}
