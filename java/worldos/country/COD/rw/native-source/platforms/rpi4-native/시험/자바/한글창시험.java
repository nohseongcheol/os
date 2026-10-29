// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Ikinyarwanda.자체.idirishya;
import Ikinyarwanda.자체.wijeti;
import Ikinyarwanda.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    idirishya 화면;
    Akarango NSOMA_eb81d7d9;
    SMS_umwanya 입력;
    public void gukora_umukoro() {
        검사.참인지(icyabaye_umurongo_utegererezwaho.사건처리중인가(), "Ikinyarwanda 화면 작업 큐");
        화면 = new idirishya("Ikinyarwanda isomero idirishya", 400, 280);
        NSOMA_eb81d7d9 = wijeti.Akarango_agaciro("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = wijeti.SMS_umwanya("Izina", 20, 65, 340, 30);
        화면.kongeraho_ikintu(NSOMA_eb81d7d9);
        화면.kongeraho_ikintu(입력);
        화면.kongeraho_ikintu(wijeti.buto("인사하기", 20, 110, 180, 32, this));
        화면.kugaragaza_idirishya();
        출력.kwandika_umurongo("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 icyabaye) {
        검사.참인지(icyabaye_umurongo_utegererezwaho.사건처리중인가(), "Ikinyarwanda Igikorwa 되부름");
        검사.참인지(icyabaye.umugerekashakiro() == 1001 && icyabaye.icyabaye_inkomoko() instanceof buto, "Ikinyarwanda icyabaye 객체와 출처");
        검사.참인지(!((Object)icyabaye.icyabaye_inkomoko() instanceof javax.swing.JButton), "표준 단추와 독립된 imiterere_agaciro");
        검사.참인지(!((Object)icyabaye instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 imiterere_agaciro");
        NSOMA_eb81d7d9.kwandika_SMS("안녕하세요 " + 입력.글읽기());
        출력.kwandika_umurongo("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        icyabaye_umurongo_utegererezwaho.나중에실행(new 한글창시험());
    }
}
