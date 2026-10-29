// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Malti.자체.tieqa;
import Malti.자체.tikketta;
import Malti.자체.qasam_ta_test;
import Malti.자체.buttuna;
import Malti.자체.avveniment_kju;
import Malti.자체.출력;
import Malti.자체.실행할일;
import Malti.자체.동작받이;
import Malti.자체.동작알림;

/** 자체 커널의 Swing tieqa: Malti 입력 → buttuna → AQRANI_eb81d7d9 SMS aġġorna. */
public class 창예제 implements 실행할일, 동작받이 {
    private tieqa 인사창;
    private qasam_ta_test isem_qasam;
    private tikketta 인사말;
    private int 인사횟수;

    public void fetaħ_tieqa() {
        인사창 = new tieqa("Malti Swing", 460, 300);
        인사창.żied_element(new tikketta("Malti", 20, 20, 420, 28));
        isem_qasam = new qasam_ta_test("Malti", 20, 64, 420, 30);
        인사말 = new tikketta("Malti", 20, 152, 420, 28);
        인사창.żied_element(isem_qasam);
        인사창.żied_element(new buttuna("인사하기", 20, 108, 180, 32, this));
        인사창.żied_element(인사말);
        인사창.żied_element(new tikketta("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.wera_tieqa();
        출력.kiteb_linja("GUI 예제 Ħejji: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.kiteb_SMS("Malti, " + isem_qasam.글읽기() + "님! (" + 인사횟수 + ")");
        출력.kiteb_linja("GUI 인사: " + 인사말.글읽기());
    }

    public void eżegwixxa_attività() { fetaħ_tieqa(); }
    public void 동작받기(동작알림 알림) {
        출력.kiteb_linja("azzjoni 알림: " + 알림.kmand_SMS());
        인사하기();
    }
    public static void serje() {
        avveniment_kju.나중에실행(new 창예제());
    }
}
