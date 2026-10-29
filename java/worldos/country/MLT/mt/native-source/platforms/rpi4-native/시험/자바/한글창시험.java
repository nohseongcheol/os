// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Malti.자체.tieqa;
import Malti.자체.widget;
import Malti.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    tieqa 화면;
    tikketta AQRANI_eb81d7d9;
    qasam_ta_test 입력;
    public void eżegwixxa_attività() {
        검사.참인지(avveniment_kju.사건처리중인가(), "Malti 화면 작업 큐");
        화면 = new tieqa("Malti librerija tieqa", 400, 280);
        AQRANI_eb81d7d9 = widget.tag_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = widget.qasam_ta_test("isem", 20, 65, 340, 30);
        화면.żied_element(AQRANI_eb81d7d9);
        화면.żied_element(입력);
        화면.żied_element(widget.buttuna("인사하기", 20, 110, 180, 32, this));
        화면.wera_tieqa();
        출력.kiteb_linja("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 avveniment) {
        검사.참인지(avveniment_kju.사건처리중인가(), "Malti azzjoni 되부름");
        검사.참인지(avveniment.INDEX() == 1001 && avveniment.avveniment_sors() instanceof buttuna, "Malti avveniment 객체와 출처");
        검사.참인지(!((Object)avveniment.avveniment_sors() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)avveniment instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        AQRANI_eb81d7d9.kiteb_SMS("안녕하세요 " + 입력.글읽기());
        출력.kiteb_linja("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        avveniment_kju.나중에실행(new 한글창시험());
    }
}
