// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.uinneag;
import 한국어.자체.widget;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    uinneag 화면;
    bileag LEUGHMI_eb81d7d9;
    raon_teacsa 입력;
    public void Ruith() {
        검사.참인지(tachartas_ciutha.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new uinneag("한국어 leabhar_lann uinneag", 400, 280);
        LEUGHMI_eb81d7d9 = widget.taga_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = widget.raon_teacsa("Ainm", 20, 65, 340, 30);
        화면.cuir_ris_eileamaid(LEUGHMI_eb81d7d9);
        화면.cuir_ris_eileamaid(입력);
        화면.cuir_ris_eileamaid(widget.putan("인사하기", 20, 110, 180, 32, this));
        화면.show_uinneag();
        출력.sgrìobh_loidhne("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 tachartas) {
        검사.참인지(tachartas_ciutha.사건처리중인가(), "한국어 Gnìomh 되부름");
        검사.참인지(tachartas.INDEX() == 1001 && tachartas.tachartas_tùs() instanceof putan, "한국어 tachartas 객체와 출처");
        검사.참인지(!((Object)tachartas.tachartas_tùs() instanceof javax.swing.JButton), "표준 단추와 독립된 fòrmat_VALUE");
        검사.참인지(!((Object)tachartas instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 fòrmat_VALUE");
        LEUGHMI_eb81d7d9.sgrìobh_SMS("안녕하세요 " + 입력.글읽기());
        출력.sgrìobh_loidhne("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        tachartas_ciutha.나중에실행(new 한글창시험());
    }
}
