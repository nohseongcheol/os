// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import isiXhosa.자체.i_window;
import isiXhosa.자체.Ilebhile;
import isiXhosa.자체.I_SMS_ifildi;
import isiXhosa.자체.iqhosha;
import isiXhosa.자체.umcimbi_ityhu;
import isiXhosa.자체.출력;
import isiXhosa.자체.실행할일;
import isiXhosa.자체.동작받이;
import isiXhosa.자체.동작알림;

/** 자체 커널의 Swing i_window: xh 입력 → iqhosha → i_README_eb81d7d9 Umbhalo qalela_ngokutsha. */
public class 창예제 implements 실행할일, 동작받이 {
    private i_window 인사창;
    private I_SMS_ifildi igama_ifildi;
    private Ilebhile 인사말;
    private int 인사횟수;

    public void vula_i_window() {
        인사창 = new i_window("xh Swing", 460, 300);
        인사창.yongeza_ielement(new Ilebhile("xh", 20, 20, 420, 28));
        igama_ifildi = new I_SMS_ifildi("xh", 20, 64, 420, 30);
        인사말 = new Ilebhile("xh", 20, 152, 420, 28);
        인사창.yongeza_ielement(igama_ifildi);
        인사창.yongeza_ielement(new iqhosha("인사하기", 20, 108, 180, 32, this));
        인사창.yongeza_ielement(인사말);
        인사창.yongeza_ielement(new Ilebhile("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.bonisa_i_window();
        출력.bhala_umgca("GUI 예제 lungisa: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.bhala_I_SMS("xh, " + igama_ifildi.글읽기() + "님! (" + 인사횟수 + ")");
        출력.bhala_umgca("GUI 인사: " + 인사말.글읽기());
    }

    public void ukwenza_umsebenzi() { vula_i_window(); }
    public void 동작받기(동작알림 알림) {
        출력.bhala_umgca("Intshukumo 알림: " + 알림.umyalelo_I_SMS());
        인사하기();
    }
    public static void Phumeza() {
        umcimbi_ityhu.나중에실행(new 창예제());
    }
}
