// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Dansk.eget.Vindue;
import Dansk.eget.widget;
import Dansk.eget.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Vindue skærmbillede;
    Etiket Vigtigt_eb81d7d9;
    tekstfelt input_VÆRDI;
    public void Kør() {
        검사.참인지(hændelse_kø.사건처리중인가(), "Dansk skærmbillede 작업 큐");
        skærmbillede = new Vindue("Dansk bibliotek Vindue", 400, 280);
        Vigtigt_eb81d7d9 = widget.tag_VÆRDI("한글로 Java 코딩", 20, 20, 340, 30);
        input_VÆRDI = widget.tekstfelt("Navn", 20, 65, 340, 30);
        skærmbillede.Tilføj_element(Vigtigt_eb81d7d9);
        skærmbillede.Tilføj_element(input_VÆRDI);
        skærmbillede.Tilføj_element(widget.knap("인사하기", 20, 110, 180, 32, this));
        skærmbillede.vise_vindue();
        Udgang.skrive_linje("KOREAN SWING READY");
    }
    public void modtage_To_do(동작알림 hændelse) {
        검사.참인지(hændelse_kø.사건처리중인가(), "Dansk Handling 되부름");
        검사.참인지(hændelse.INDEKS() == 1001 && hændelse.hændelseskilde() instanceof knap, "Dansk hændelse 객체와 begyndelsespunkt_VÆRDI");
        검사.참인지(!((Object)hændelse.hændelseskilde() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VÆRDI");
        검사.참인지(!((Object)hændelse instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VÆRDI");
        Vigtigt_eb81d7d9.skrive_sms("안녕하세요 " + input_VÆRDI.글읽기());
        Udgang.skrive_linje("KOREAN SWING CLICK " + input_VÆRDI.글읽기());
    }
    public static void main(String[] Argumenter) {
        hændelse_kø.나중에실행(new 한글창시험());
    }
}
