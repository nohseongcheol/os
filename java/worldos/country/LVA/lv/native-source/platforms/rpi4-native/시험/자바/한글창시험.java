// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Latviešu.savs.Logs;
import Latviešu.savs.logrīks;
import Latviešu.savs.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    Logs 화면;
    Etiķete fails_Lasi_mani_eb81d7d9;
    teksta_lauks 입력;
    public void Izpildīt() {
        검사.참인지(notikums_rinda.사건처리중인가(), "Latviešu 화면 작업 큐");
        화면 = new Logs("Latviešu bibliotēka Logs", 400, 280);
        fails_Lasi_mani_eb81d7d9 = logrīks.tags_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = logrīks.teksta_lauks("Nosaukums", 20, 65, 340, 30);
        화면.Pievienot_elements(fails_Lasi_mani_eb81d7d9);
        화면.Pievienot_elements(입력);
        화면.Pievienot_elements(logrīks.Pogas("인사하기", 20, 110, 180, 32, this));
        화면.rādīt_logs();
        Izvade.rakstīšana_līnija("KOREAN SWING READY");
    }
    public void saņemt_darbība(darbība_informēšana Notikums) {
        검사.참인지(notikums_rinda.사건처리중인가(), "Latviešu Darbība 되부름");
        검사.참인지(Notikums.INDEX() == 1001 && Notikums.notikuma_avots() instanceof Pogas, "Latviešu Notikums 객체와 출처");
        검사.참인지(!((Object)Notikums.notikuma_avots() instanceof javax.swing.JButton), "표준 단추와 독립된 formāts_VALUE");
        검사.참인지(!((Object)Notikums instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formāts_VALUE");
        fails_Lasi_mani_eb81d7d9.rakstīšana_SMS("안녕하세요 " + 입력.글읽기());
        Izvade.rakstīšana_līnija("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Parametri) {
        notikums_rinda.나중에실행(new 한글창시험());
    }
}
