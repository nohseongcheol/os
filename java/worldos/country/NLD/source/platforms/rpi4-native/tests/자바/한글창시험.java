// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Nederlands.Eigen.Venster;
import Nederlands.Eigen.schermelement;
import Nederlands.Eigen.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Venster scherm;
    Etiket LEESMIJ_eb81d7d9;
    tekstveld invoer_WAARDE;
    public void Uitvoeren() {
        검사.참인지(gebeurtenis_wachtrij.사건처리중인가(), "Nederlands scherm 작업 큐");
        scherm = new Venster("Nederlands bibliotheek Venster", 400, 280);
        LEESMIJ_eb81d7d9 = schermelement.tag_WAARDE("한글로 Java 코딩", 20, 20, 340, 30);
        invoer_WAARDE = schermelement.tekstveld("Naam", 20, 65, 340, 30);
        scherm.Toevoegen_element(LEESMIJ_eb81d7d9);
        scherm.Toevoegen_element(invoer_WAARDE);
        scherm.Toevoegen_element(schermelement.knop("인사하기", 20, 110, 180, 32, this));
        scherm.weergeven_venster();
        tekstuitvoer.schrijven_lijn("KOREAN SWING READY");
    }
    public void ontvangen_Actie(Actie_kennisgeving Gebeurtenis) {
        검사.참인지(gebeurtenis_wachtrij.사건처리중인가(), "Nederlands Actie 되부름");
        검사.참인지(Gebeurtenis.INDEX() == 1001 && Gebeurtenis.gebeurtenisbron() instanceof knop, "Nederlands Gebeurtenis 객체와 oorsprong_WAARDE");
        검사.참인지(!((Object)Gebeurtenis.gebeurtenisbron() instanceof javax.swing.JButton), "표준 단추와 독립된 opmaak_WAARDE");
        검사.참인지(!((Object)Gebeurtenis instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 opmaak_WAARDE");
        LEESMIJ_eb81d7d9.schrijven_sms("안녕하세요 " + invoer_WAARDE.글읽기());
        tekstuitvoer.schrijven_lijn("KOREAN SWING CLICK " + invoer_WAARDE.글읽기());
    }
    public static void main(String[] argumenten) {
        gebeurtenis_wachtrij.나중에실행(new 한글창시험());
    }
}
