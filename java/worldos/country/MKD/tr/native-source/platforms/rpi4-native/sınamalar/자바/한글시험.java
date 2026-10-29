// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Türkçe.Öz.문자;
import Türkçe.Öz.dosya;
import Türkçe.Öz.girdi_Liste;
import Türkçe.Öz.sözlük;
import Türkçe.Öz.metinÇıktısı;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String 인사 = "안녕하세요 · 日本語 · العربية · 😀";
        metinÇıktısı.yazma_hat(문자.şifre_çözmek_veri(문자.kodlamak(인사))); metinÇıktısı.수쓰기(문자.kod_öğesi_BAĞ_DEĞ_SAY("한글😀"));
        dosya.Yazma("한글자료.txt", 인사); metinÇıktısı.yazma_hat(dosya.Okuma("한글자료.txt"));
        girdi_Liste 이름들 = new girdi_Liste(); 이름들.더하기("가람"); 이름들.더하기("누리"); metinÇıktısı.yazma_hat(이름들.Okuma(1));
        sözlük 뜻 = new sözlük(); 뜻.넣기("가람", "강"); System.gc(); metinÇıktısı.yazma_hat(뜻.BUL_girdi("가람"));
        try { 문자.şifre_çözmek_veri(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { metinÇıktısı.yazma_hat("UTF-8 hata reddetmek_değer"); }
        metinÇıktısı.yazma_hat("Türkçe kitaplık 완료");
    }
}
