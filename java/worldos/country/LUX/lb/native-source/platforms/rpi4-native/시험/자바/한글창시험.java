// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.Fënster;
import 한국어.자체.Widget;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Fënster 화면;
    Numm_5ce2bd6f LIESMECH_eb81d7d9;
    Textfeld 입력;
    public void Ausféieren() {
        검사.참인지(Evenement_Schlaang.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new Fënster("한국어 Bibliothéik Fënster", 400, 280);
        LIESMECH_eb81d7d9 = Widget.Tag_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = Widget.Textfeld("Numm", 20, 65, 340, 30);
        화면.derbäisetzen_Element(LIESMECH_eb81d7d9);
        화면.derbäisetzen_Element(입력);
        화면.derbäisetzen_Element(Widget.Tast("인사하기", 20, 110, 180, 32, this));
        화면.Show_Fënster();
        출력.schreiwen_Zeil("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 Evenement) {
        검사.참인지(Evenement_Schlaang.사건처리중인가(), "한국어 Aktioun 되부름");
        검사.참인지(Evenement.INDEX() == 1001 && Evenement.Evenement_Quell() instanceof Tast, "한국어 Evenement 객체와 출처");
        검사.참인지(!((Object)Evenement.Evenement_Quell() instanceof javax.swing.JButton), "표준 단추와 독립된 Format_VALUE");
        검사.참인지(!((Object)Evenement instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 Format_VALUE");
        LIESMECH_eb81d7d9.schreiwen_SMS("안녕하세요 " + 입력.글읽기());
        출력.schreiwen_Zeil("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        Evenement_Schlaang.나중에실행(new 한글창시험());
    }
}
