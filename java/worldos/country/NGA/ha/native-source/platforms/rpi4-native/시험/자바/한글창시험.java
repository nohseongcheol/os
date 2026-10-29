// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.taga;
import 한국어.자체.wijet;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    taga 화면;
    alama README_eb81d7d9;
    SMS_Fili 입력;
    public void gudanar_aiki() {
        검사.참인지(Faruwa_Jerin_ayyukan_da_za_a_yi.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new taga("한국어 laburare taga", 400, 280);
        README_eb81d7d9 = wijet.tambari_Daraja("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = wijet.SMS_Fili("Suna", 20, 65, 340, 30);
        화면.ƙara_Dan_gutsuren_bayani(README_eb81d7d9);
        화면.ƙara_Dan_gutsuren_bayani(입력);
        화면.ƙara_Dan_gutsuren_bayani(wijet.maɓali("인사하기", 20, 110, 180, 32, this));
        화면.Nuna_taga();
        출력.Rubuta_Layi("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 Faruwa) {
        검사.참인지(Faruwa_Jerin_ayyukan_da_za_a_yi.사건처리중인가(), "한국어 Aiki 되부름");
        검사.참인지(Faruwa.Indes() == 1001 && Faruwa.Faruwa_tushe() instanceof maɓali, "한국어 Faruwa 객체와 출처");
        검사.참인지(!((Object)Faruwa.Faruwa_tushe() instanceof javax.swing.JButton), "표준 단추와 독립된 zubi_Daraja");
        검사.참인지(!((Object)Faruwa instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 zubi_Daraja");
        README_eb81d7d9.Rubuta_SMS("안녕하세요 " + 입력.글읽기());
        출력.Rubuta_Layi("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        Faruwa_Jerin_ayyukan_da_za_a_yi.나중에실행(new 한글창시험());
    }
}
