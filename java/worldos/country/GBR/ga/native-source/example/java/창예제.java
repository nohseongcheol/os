// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Gaeilge.자체.fuinneog;
import Gaeilge.자체.Lipéad;
import Gaeilge.자체.réimse_téacs;
import Gaeilge.자체.cnaipe;
import Gaeilge.자체.ócáid_scuaine;
import Gaeilge.자체.Aschur;
import Gaeilge.자체.실행할일;
import Gaeilge.자체.동작받이;
import Gaeilge.자체.동작알림;

/** 자체 커널의 Swing fuinneog: ga 입력 → cnaipe → LÉIGHMÉ_eb81d7d9 Téacs athnuaigh. */
public class 창예제 implements 실행할일, 동작받이 {
    private fuinneog 인사창;
    private réimse_téacs ainm_réimse;
    private Lipéad 인사말;
    private int 인사횟수;

    public void oscail_fuinneog() {
        인사창 = new fuinneog("ga Swing", 460, 300);
        인사창.cuir_le_eilimint(new Lipéad("ga", 20, 20, 420, 28));
        ainm_réimse = new réimse_téacs("ga", 20, 64, 420, 30);
        인사말 = new Lipéad("ga", 20, 152, 420, 28);
        인사창.cuir_le_eilimint(ainm_réimse);
        인사창.cuir_le_eilimint(new cnaipe("인사하기", 20, 108, 180, 32, this));
        인사창.cuir_le_eilimint(인사말);
        인사창.cuir_le_eilimint(new Lipéad("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.seó_fuinneog();
        Aschur.scríobh_líne("GUI 예제 Ullmhaigh: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.scríobh_SMS("ga, " + ainm_réimse.글읽기() + "님! (" + 인사횟수 + ")");
        Aschur.scríobh_líne("GUI 인사: " + 인사말.글읽기());
    }

    public void Rith() { oscail_fuinneog(); }
    public void 동작받기(동작알림 알림) {
        Aschur.scríobh_líne("Gníomh 알림: " + 알림.ordú_SMS());
        인사하기();
    }
    public static void Rith_2() {
        ócáid_scuaine.나중에실행(new 창예제());
    }
}
