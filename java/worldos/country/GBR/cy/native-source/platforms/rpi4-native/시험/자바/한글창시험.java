// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Cymraeg.자체.ffenestr;
import Cymraeg.자체.teclyn;
import Cymraeg.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    ffenestr 화면;
    label GWYBODAETH_eb81d7d9;
    maes_testun 입력;
    public void Gweithredu() {
        검사.참인지(digwyddiad_ciw.사건처리중인가(), "Cymraeg 화면 작업 큐");
        화면 = new ffenestr("Cymraeg llyfrgell ffenestr", 400, 280);
        GWYBODAETH_eb81d7d9 = teclyn.tag_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = teclyn.maes_testun("Enw", 20, 65, 340, 30);
        화면.ychwanegu_elfen(GWYBODAETH_eb81d7d9);
        화면.ychwanegu_elfen(입력);
        화면.ychwanegu_elfen(teclyn.botwm("인사하기", 20, 110, 180, 32, this));
        화면.sioe_ffenestr();
        Allbwn.ysgrifennu_llinell("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 digwyddiad) {
        검사.참인지(digwyddiad_ciw.사건처리중인가(), "Cymraeg Gweithrediad 되부름");
        검사.참인지(digwyddiad.INDEX() == 1001 && digwyddiad.digwyddiad_ffynhonnell() instanceof botwm, "Cymraeg digwyddiad 객체와 출처");
        검사.참인지(!((Object)digwyddiad.digwyddiad_ffynhonnell() instanceof javax.swing.JButton), "표준 단추와 독립된 fformat_VALUE");
        검사.참인지(!((Object)digwyddiad instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 fformat_VALUE");
        GWYBODAETH_eb81d7d9.ysgrifennu_SMS("안녕하세요 " + 입력.글읽기());
        Allbwn.ysgrifennu_llinell("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        digwyddiad_ciw.나중에실행(new 한글창시험());
    }
}
