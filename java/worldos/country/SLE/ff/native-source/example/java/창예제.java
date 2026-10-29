// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.falanteere;
import 한국어.자체.tinndinoore;
import 한국어.자체.binndi_suudu;
import 한국어.자체.feɗoode;
import 한국어.자체.saɗteende_lappol;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing falanteere: ff 입력 → feɗoode → TARƊOO_eb81d7d9 binndi ɓamtude. */
public class 창예제 implements 실행할일, 동작받이 {
    private falanteere 인사창;
    private binndi_suudu innde_suudu;
    private tinndinoore 인사말;
    private int 인사횟수;

    public void udditde_falanteere() {
        인사창 = new falanteere("ff Swing", 460, 300);
        인사창.ɓeydude_geɗel(new tinndinoore("ff", 20, 20, 420, 28));
        innde_suudu = new binndi_suudu("ff", 20, 64, 420, 30);
        인사말 = new tinndinoore("ff", 20, 152, 420, 28);
        인사창.ɓeydude_geɗel(innde_suudu);
        인사창.ɓeydude_geɗel(new feɗoode("인사하기", 20, 108, 180, 32, this));
        인사창.ɓeydude_geɗel(인사말);
        인사창.ɓeydude_geɗel(new tinndinoore("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.hollirde_falanteere();
        출력.winndude_diidol("GUI 예제 Heblu: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.winndude_binndi("ff, " + innde_suudu.글읽기() + "님! (" + 인사횟수 + ")");
        출력.winndude_diidol("GUI 인사: " + 인사말.글읽기());
    }

    public void 실행하기() { udditde_falanteere(); }
    public void 동작받기(동작알림 알림) {
        출력.winndude_diidol("gollal 알림: " + 알림.ginol_binndi());
        인사하기();
    }
    public static void huutoraade() {
        saɗteende_lappol.나중에실행(new 창예제());
    }
}
