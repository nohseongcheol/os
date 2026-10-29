// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Türkçe.Öz.Pencere;
import Türkçe.Öz.Etiket;
import Türkçe.Öz.metin_alanı;
import Türkçe.Öz.düğme;
import Türkçe.Öz.olay_sıra;
import Türkçe.Öz.metinÇıktısı;
import Türkçe.Öz.실행할일;
import Türkçe.Öz.동작받이;
import Türkçe.Öz.Eylem_uyarı;

/** Öz 커널의 Swing Pencere: tr artış_değer → düğme → 안내 metin yenilemek. */
public class PencereÖrneği implements 실행할일, 동작받이 {
    private Pencere 인사창;
    private metin_alanı ad_Alan;
    private Etiket 인사말;
    private int 인사횟수;

    public void açık_pencere() {
        인사창 = new Pencere("tr Swing", 460, 300);
        인사창.Ekle_öğe(new Etiket("Merhaba", 20, 20, 420, 28));
        ad_Alan = new metin_alanı("tr", 20, 64, 420, 30);
        인사말 = new Etiket("Merhaba", 20, 152, 420, 28);
        인사창.Ekle_öğe(ad_Alan);
        인사창.Ekle_öğe(new düğme("인사하기", 20, 108, 180, 32, this));
        인사창.Ekle_öğe(인사말);
        인사창.Ekle_öğe(new Etiket("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.şov_pencere();
        metinÇıktısı.yazma_hat("GUI 예제 Hazırlan: PencereÖrneği");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.yazma_SMS("Merhaba, " + ad_Alan.글읽기() + "님! (" + 인사횟수 + ")");
        metinÇıktısı.yazma_hat("GUI 인사: " + 인사말.글읽기());
    }

    public void Çalıştır() { açık_pencere(); }
    public void almak_Eylem(Eylem_uyarı uyarı) {
        metinÇıktısı.yazma_hat("Eylem uyarı: " + uyarı.komut_SMS());
        인사하기();
    }
    public static void çalıştır() {
        olay_sıra.나중에실행(new PencereÖrneği());
    }
}
