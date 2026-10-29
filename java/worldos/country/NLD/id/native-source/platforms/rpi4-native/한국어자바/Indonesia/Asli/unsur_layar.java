// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.Asli;
/** Indonesia 화면 구성요소를 만드는 편의 fungsi_VALUE. */
public final class unsur_layar {
    private unsur_layar() {}
    public static void 나중에실행(실행할일 tugas_Tugas) { acara_antrean.나중에실행(tugas_Tugas); }
    public static Nama tag_VALUE(String teks, int 가로, int Vertikal_posisi, int 폭, int 높이) {
        return new Nama(teks, 가로, Vertikal_posisi, 폭, 높이);
    }
    public static tombol tombol(String teks, int 가로, int Vertikal_posisi, int 폭, int 높이, 동작받이 받이) {
        return new tombol(teks, 가로, Vertikal_posisi, 폭, 높이, 받이);
    }
    public static bidang_teks bidang_teks(String teks, int 가로, int Vertikal_posisi, int 폭, int 높이) {
        return new bidang_teks(teks, 가로, Vertikal_posisi, 폭, 높이);
    }
}
