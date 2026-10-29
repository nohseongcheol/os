// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Gaeilge.자체.fuinneog;
import Gaeilge.자체.giuirléid;
import Gaeilge.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    fuinneog 화면;
    Lipéad LÉIGHMÉ_eb81d7d9;
    réimse_téacs 입력;
    public void Rith() {
        검사.참인지(ócáid_scuaine.사건처리중인가(), "Gaeilge 화면 작업 큐");
        화면 = new fuinneog("Gaeilge leabharlann fuinneog", 400, 280);
        LÉIGHMÉ_eb81d7d9 = giuirléid.clib_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = giuirléid.réimse_téacs("Ainm", 20, 65, 340, 30);
        화면.cuir_le_eilimint(LÉIGHMÉ_eb81d7d9);
        화면.cuir_le_eilimint(입력);
        화면.cuir_le_eilimint(giuirléid.cnaipe("인사하기", 20, 110, 180, 32, this));
        화면.seó_fuinneog();
        Aschur.scríobh_líne("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 ócáid) {
        검사.참인지(ócáid_scuaine.사건처리중인가(), "Gaeilge Gníomh 되부름");
        검사.참인지(ócáid.INDEX() == 1001 && ócáid.ócáid_foinse() instanceof cnaipe, "Gaeilge ócáid 객체와 출처");
        검사.참인지(!((Object)ócáid.ócáid_foinse() instanceof javax.swing.JButton), "표준 단추와 독립된 formáid_VALUE");
        검사.참인지(!((Object)ócáid instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formáid_VALUE");
        LÉIGHMÉ_eb81d7d9.scríobh_SMS("안녕하세요 " + 입력.글읽기());
        Aschur.scríobh_líne("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] Argóintí) {
        ócáid_scuaine.나중에실행(new 한글창시험());
    }
}
