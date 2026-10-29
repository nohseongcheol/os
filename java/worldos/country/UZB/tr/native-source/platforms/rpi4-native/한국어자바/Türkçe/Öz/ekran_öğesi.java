// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkçe.Öz;
/** Türkçe 화면 구성요소를 만드는 편의 işlev_değer. */
public final class ekran_öğesi {
    private ekran_öğesi() {}
    public static void 나중에실행(실행할일 Görev_Eylem) { olay_sıra.나중에실행(Görev_Eylem); }
    public static Etiket etiket_değer(String metin, int 가로, int Dikey_konum, int 폭, int 높이) {
        return new Etiket(metin, 가로, Dikey_konum, 폭, 높이);
    }
    public static düğme düğme(String metin, int 가로, int Dikey_konum, int 폭, int 높이, 동작받이 받이) {
        return new düğme(metin, 가로, Dikey_konum, 폭, 높이, 받이);
    }
    public static metin_alanı metin_alanı(String metin, int 가로, int Dikey_konum, int 폭, int 높이) {
        return new metin_alanı(metin, 가로, Dikey_konum, 폭, 높이);
    }
}
