// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Cymraeg.자체.ffenestr;
import Cymraeg.자체.label;
import Cymraeg.자체.maes_testun;
import Cymraeg.자체.botwm;
import Cymraeg.자체.digwyddiad_ciw;
import Cymraeg.자체.Allbwn;
import Cymraeg.자체.실행할일;
import Cymraeg.자체.동작받이;
import Cymraeg.자체.동작알림;

/** 자체 커널의 Swing ffenestr: cy 입력 → botwm → GWYBODAETH_eb81d7d9 Testun adnewyddu. */
public class 창예제 implements 실행할일, 동작받이 {
    private ffenestr 인사창;
    private maes_testun enw_maes;
    private label 인사말;
    private int 인사횟수;

    public void agor_ffenestr() {
        인사창 = new ffenestr("cy Swing", 460, 300);
        인사창.ychwanegu_elfen(new label("cy", 20, 20, 420, 28));
        enw_maes = new maes_testun("cy", 20, 64, 420, 30);
        인사말 = new label("cy", 20, 152, 420, 28);
        인사창.ychwanegu_elfen(enw_maes);
        인사창.ychwanegu_elfen(new botwm("인사하기", 20, 108, 180, 32, this));
        인사창.ychwanegu_elfen(인사말);
        인사창.ychwanegu_elfen(new label("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.sioe_ffenestr();
        Allbwn.ysgrifennu_llinell("GUI 예제 Paratoi: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.ysgrifennu_SMS("cy, " + enw_maes.글읽기() + "님! (" + 인사횟수 + ")");
        Allbwn.ysgrifennu_llinell("GUI 인사: " + 인사말.글읽기());
    }

    public void Gweithredu() { agor_ffenestr(); }
    public void 동작받기(동작알림 알림) {
        Allbwn.ysgrifennu_llinell("Gweithrediad 알림: " + 알림.gorchymyn_SMS());
        인사하기();
    }
    public static void Gweithredu_2() {
        digwyddiad_ciw.나중에실행(new 창예제());
    }
}
