// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Melayu.Asli;
/** Melayu 화면 구성요소를 만드는 편의 fungsi_VALUE. */
public final class unsur_skrin {
    private unsur_skrin() {}
    public static void 나중에실행(실행할일 tugas_cadangan) { acara_baris.나중에실행(tugas_cadangan); }
    public static label tag_VALUE(String Teks, int 가로, int Menegak_jawatan, int 폭, int 높이) {
        return new label(Teks, 가로, Menegak_jawatan, 폭, 높이);
    }
    public static Butang Butang(String Teks, int 가로, int Menegak_jawatan, int 폭, int 높이, 동작받이 받이) {
        return new Butang(Teks, 가로, Menegak_jawatan, 폭, 높이, 받이);
    }
    public static medan_teks medan_teks(String Teks, int 가로, int Menegak_jawatan, int 폭, int 높이) {
        return new medan_teks(Teks, 가로, Menegak_jawatan, 폭, 높이);
    }
}
