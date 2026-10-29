// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.Dritare;
import 한국어.자체.widget;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Dritare 화면;
    Etiketë LEXOMË_eb81d7d9;
    SMS_fushë 입력;
    public void Kryej() {
        검사.참인지(ngjarje_radhë.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new Dritare("한국어 bibliotekë Dritare", 400, 280);
        LEXOMË_eb81d7d9 = widget.shenjë_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = widget.SMS_fushë("Emër", 20, 65, 340, 30);
        화면.shto_element(LEXOMË_eb81d7d9);
        화면.shto_element(입력);
        화면.shto_element(widget.Buton("인사하기", 20, 110, 180, 32, this));
        화면.shfaq_dritare();
        출력.shkruaj_linjë("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 Ngjarje) {
        검사.참인지(ngjarje_radhë.사건처리중인가(), "한국어 Veprim 되부름");
        검사.참인지(Ngjarje.INDEX() == 1001 && Ngjarje.ngjarje_burim() instanceof Buton, "한국어 Ngjarje 객체와 출처");
        검사.참인지(!((Object)Ngjarje.ngjarje_burim() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)Ngjarje instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        LEXOMË_eb81d7d9.shkruaj_SMS("안녕하세요 " + 입력.글읽기());
        출력.shkruaj_linjë("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argumente) {
        ngjarje_radhë.나중에실행(new 한글창시험());
    }
}
