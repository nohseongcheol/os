// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Íslenska.eigin.Gluggi;
import Íslenska.eigin.græja;
import Íslenska.eigin.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Gluggi 화면;
    Skýring LESTUMIG_eb81d7d9;
    SMS_reitur 입력;
    public void Keyra() {
        검사.참인지(atvik_biðröð.사건처리중인가(), "Íslenska 화면 작업 큐");
        화면 = new Gluggi("Íslenska safn Gluggi", 400, 280);
        LESTUMIG_eb81d7d9 = græja.merki_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = græja.SMS_reitur("Heiti", 20, 65, 340, 30);
        화면.bæta_við_eining(LESTUMIG_eb81d7d9);
        화면.bæta_við_eining(입력);
        화면.bæta_við_eining(græja.hnappur("인사하기", 20, 110, 180, 32, this));
        화면.sýna_gluggi();
        úttak.skrifa_lína("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 atvik) {
        검사.참인지(atvik_biðröð.사건처리중인가(), "Íslenska Aðgerð 되부름");
        검사.참인지(atvik.INDEX() == 1001 && atvik.atvik_uppruni() instanceof hnappur, "Íslenska atvik 객체와 출처");
        검사.참인지(!((Object)atvik.atvik_uppruni() instanceof javax.swing.JButton), "표준 단추와 독립된 snið_VALUE");
        검사.참인지(!((Object)atvik instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 snið_VALUE");
        LESTUMIG_eb81d7d9.skrifa_SMS("안녕하세요 " + 입력.글읽기());
        úttak.skrifa_lína("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Viðföng) {
        atvik_biðröð.나중에실행(new 한글창시험());
    }
}
