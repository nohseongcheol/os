// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Svenska.eget.Fönster;
import Svenska.eget.skärmelement;
import Svenska.eget.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Fönster skärmbild;
    Etikett VIKTIGT_eb81d7d9;
    textfält indata_värde;
    public void Starta() {
        검사.참인지(händelse_kö.사건처리중인가(), "Svenska skärmbild 작업 큐");
        skärmbild = new Fönster("Svenska bibliotek Fönster", 400, 280);
        VIKTIGT_eb81d7d9 = skärmelement.tagg_värde("한글로 Java 코딩", 20, 20, 340, 30);
        indata_värde = skärmelement.textfält("Namn", 20, 65, 340, 30);
        skärmbild.Lägg_till_element(VIKTIGT_eb81d7d9);
        skärmbild.Lägg_till_element(indata_värde);
        skärmbild.Lägg_till_element(skärmelement.knapp("인사하기", 20, 110, 180, 32, this));
        skärmbild.visa_fönster();
        utmatningsposition.skriva_rad("KOREAN SWING READY");
    }
    public void få_Action(동작알림 Händelse) {
        검사.참인지(händelse_kö.사건처리중인가(), "Svenska Åtgärd 되부름");
        검사.참인지(Händelse.INDEX() == 1001 && Händelse.händelsekälla() instanceof knapp, "Svenska Händelse 객체와 origo_värde");
        검사.참인지(!((Object)Händelse.händelsekälla() instanceof javax.swing.JButton), "표준 단추와 독립된 format_värde");
        검사.참인지(!((Object)Händelse instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_värde");
        VIKTIGT_eb81d7d9.skriva_SMS("안녕하세요 " + indata_värde.läsa_SMS());
        utmatningsposition.skriva_rad("KOREAN SWING CLICK " + indata_värde.läsa_SMS());
    }
    public static void main(String[] argument) {
        händelse_kö.나중에실행(new 한글창시험());
    }
}
