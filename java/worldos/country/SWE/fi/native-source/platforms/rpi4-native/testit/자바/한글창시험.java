// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import suomi.oma.Ikkuna;
import suomi.oma.näyttöelementti;
import suomi.oma.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Ikkuna 화면;
    Nimike Lueminut_eb81d7d9;
    tekstikenttä syöte_ARVO;
    public void Suorita() {
        검사.참인지(tapahtuma_jono.사건처리중인가(), "suomi 화면 작업 큐");
        화면 = new Ikkuna("suomi kirjasto Ikkuna", 400, 280);
        Lueminut_eb81d7d9 = näyttöelementti.tunnus_ARVO("한글로 Java 코딩", 20, 20, 340, 30);
        syöte_ARVO = näyttöelementti.tekstikenttä("Nimi", 20, 65, 340, 30);
        화면.Lisää_elementti(Lueminut_eb81d7d9);
        화면.Lisää_elementti(syöte_ARVO);
        화면.Lisää_elementti(näyttöelementti.painike("인사하기", 20, 110, 180, 32, this));
        화면.näyttää_ikkuna();
        tulostuspaikka.kirjoitus_rivi("KOREAN SWING READY");
    }
    public void saada_toimi(동작알림 Tapahtuma) {
        검사.참인지(tapahtuma_jono.사건처리중인가(), "suomi Toiminto 되부름");
        검사.참인지(Tapahtuma.INDEKSI() == 1001 && Tapahtuma.tapahtumalähde() instanceof painike, "suomi Tapahtuma 객체와 origo_ARVO");
        검사.참인지(!((Object)Tapahtuma.tapahtumalähde() instanceof javax.swing.JButton), "표준 단추와 독립된 muoto_ARVO");
        검사.참인지(!((Object)Tapahtuma instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 muoto_ARVO");
        Lueminut_eb81d7d9.kirjoitus_SMS("안녕하세요 " + syöte_ARVO.lukea_SMS());
        tulostuspaikka.kirjoitus_rivi("KOREAN SWING CLICK " + syöte_ARVO.lukea_SMS());
    }
    public static void main(String[] argumentit) {
        tapahtuma_jono.나중에실행(new 한글창시험());
    }
}
