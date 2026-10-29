// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import isiXhosa.자체.i_window;
import isiXhosa.자체.iwijethi;
import isiXhosa.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    i_window 화면;
    Ilebhile i_README_eb81d7d9;
    I_SMS_ifildi 입력;
    public void ukwenza_umsebenzi() {
        검사.참인지(umcimbi_ityhu.사건처리중인가(), "isiXhosa 화면 작업 큐");
        화면 = new i_window("isiXhosa ilayibhrari i_window", 400, 280);
        i_README_eb81d7d9 = iwijethi.thega_ixabiso("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = iwijethi.I_SMS_ifildi("Igama", 20, 65, 340, 30);
        화면.yongeza_ielement(i_README_eb81d7d9);
        화면.yongeza_ielement(입력);
        화면.yongeza_ielement(iwijethi.iqhosha("인사하기", 20, 110, 180, 32, this));
        화면.bonisa_i_window();
        출력.bhala_umgca("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 umcimbi) {
        검사.참인지(umcimbi_ityhu.사건처리중인가(), "isiXhosa Intshukumo 되부름");
        검사.참인지(umcimbi.indeksa() == 1001 && umcimbi.umcimbi_umthombo() instanceof iqhosha, "isiXhosa umcimbi 객체와 출처");
        검사.참인지(!((Object)umcimbi.umcimbi_umthombo() instanceof javax.swing.JButton), "표준 단추와 독립된 fomatha_ixabiso");
        검사.참인지(!((Object)umcimbi instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 fomatha_ixabiso");
        i_README_eb81d7d9.bhala_I_SMS("안녕하세요 " + 입력.글읽기());
        출력.bhala_umgca("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        umcimbi_ityhu.나중에실행(new 한글창시험());
    }
}
