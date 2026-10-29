// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.window;
import 한국어.자체.widget;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    window 화면;
    label BASAHINAKO_eb81d7d9;
    SMS_field 입력;
    public void Mag_execute_gawain() {
        검사.참인지(kaganapan_pila.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new window("한국어 library window", 400, 280);
        BASAHINAKO_eb81d7d9 = widget.tag_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = widget.SMS_field("pangalan", 20, 65, 340, 30);
        화면.idagdag_elemento(BASAHINAKO_eb81d7d9);
        화면.idagdag_elemento(입력);
        화면.idagdag_elemento(widget.button("인사하기", 20, 110, 180, 32, this));
        화면.ipakita_window();
        출력.sumulat_linya("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 kaganapan) {
        검사.참인지(kaganapan_pila.사건처리중인가(), "한국어 aksyon 되부름");
        검사.참인지(kaganapan.INDEX() == 1001 && kaganapan.kaganapan_pinagmulan() instanceof button, "한국어 kaganapan 객체와 출처");
        검사.참인지(!((Object)kaganapan.kaganapan_pinagmulan() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)kaganapan instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        BASAHINAKO_eb81d7d9.sumulat_SMS("안녕하세요 " + 입력.글읽기());
        출력.sumulat_linya("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        kaganapan_pila.나중에실행(new 한글창시험());
    }
}
