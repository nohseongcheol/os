// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.eget.Vindu;
import norsk.eget.miniprogram;
import norsk.eget.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Vindu skjermbilde;
    Etikett Viktig_fil_eb81d7d9;
    tekstfelt inndata_VERDI;
    public void Kjør() {
        검사.참인지(hendelse_kø.사건처리중인가(), "norsk skjermbilde 작업 큐");
        skjermbilde = new Vindu("norsk bibliotek Vindu", 400, 280);
        Viktig_fil_eb81d7d9 = miniprogram.kode_VERDI("한글로 Java 코딩", 20, 20, 340, 30);
        inndata_VERDI = miniprogram.tekstfelt("Navn", 20, 65, 340, 30);
        skjermbilde.Legg_til_element(Viktig_fil_eb81d7d9);
        skjermbilde.Legg_til_element(inndata_VERDI);
        skjermbilde.Legg_til_element(miniprogram.Knapp("인사하기", 20, 110, 180, 32, this));
        skjermbilde.vise_vindu();
        Utgang.skrive_linje("KOREAN SWING READY");
    }
    public void motta_Gjøremål(Gjøremål_notice Hendelse) {
        검사.참인지(hendelse_kø.사건처리중인가(), "norsk Handling 되부름");
        검사.참인지(Hendelse.INDEKS() == 1001 && Hendelse.hendelseskilde() instanceof Knapp, "norsk Hendelse 객체와 origo_VERDI");
        검사.참인지(!((Object)Hendelse.hendelseskilde() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VERDI");
        검사.참인지(!((Object)Hendelse instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VERDI");
        Viktig_fil_eb81d7d9.skrive_SMS("안녕하세요 " + inndata_VERDI.글읽기());
        Utgang.skrive_linje("KOREAN SWING CLICK " + inndata_VERDI.글읽기());
    }
    public static void main(String[] Argumenter) {
        hendelse_kø.나중에실행(new 한글창시험());
    }
}
