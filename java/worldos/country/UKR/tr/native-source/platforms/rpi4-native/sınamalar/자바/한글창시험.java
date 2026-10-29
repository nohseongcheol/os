// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Türkçe.Öz.Pencere;
import Türkçe.Öz.ekran_öğesi;
import Türkçe.Öz.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Pencere 화면;
    Etiket 안내;
    metin_alanı artış_değer;
    public void Çalıştır() {
        검사.참인지(olay_sıra.사건처리중인가(), "Türkçe 화면 작업 큐");
        화면 = new Pencere("Türkçe kitaplık Pencere", 400, 280);
        안내 = ekran_öğesi.etiket_değer("한글로 Java 코딩", 20, 20, 340, 30);
        artış_değer = ekran_öğesi.metin_alanı("İsim", 20, 65, 340, 30);
        화면.Ekle_öğe(안내);
        화면.Ekle_öğe(artış_değer);
        화면.Ekle_öğe(ekran_öğesi.düğme("인사하기", 20, 110, 180, 32, this));
        화면.şov_pencere();
        metinÇıktısı.yazma_hat("KOREAN SWING READY");
    }
    public void almak_Eylem(Eylem_uyarı Olay) {
        검사.참인지(olay_sıra.사건처리중인가(), "Türkçe Eylem 되부름");
        검사.참인지(Olay.Dizin() == 1001 && Olay.olay_kaynağı() instanceof düğme, "Türkçe Olay 객체와 origin_değer");
        검사.참인지(!((Object)Olay.olay_kaynağı() instanceof javax.swing.JButton), "표준 단추와 독립된 biçim_değer");
        검사.참인지(!((Object)Olay instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 biçim_değer");
        안내.yazma_SMS("안녕하세요 " + artış_değer.글읽기());
        metinÇıktısı.yazma_hat("KOREAN SWING CLICK " + artış_değer.글읽기());
    }
    public static void main(String[] bağımsız_değişkenler) {
        olay_sıra.나중에실행(new 한글창시험());
    }
}
