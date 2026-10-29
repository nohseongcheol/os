// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.wínńdò;
import 한국어.자체.àkọlé;
import 한국어.자체.SMS_àayè_wúnrẹ̀n;
import 한국어.자체.bọ́tìnnì;
import 한국어.자체.ìgbéṣẹ̀_ìtòléra;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing wínńdò: yo 입력 → bọ́tìnnì → KÀ_MÍ_eb81d7d9 SMS sọdọ̀tun. */
public class 창예제 implements 실행할일, 동작받이 {
    private wínńdò 인사창;
    private SMS_àayè_wúnrẹ̀n orúkọ_àayè_wúnrẹ̀n;
    private àkọlé 인사말;
    private int 인사횟수;

    public void ṣí_wínńdò() {
        인사창 = new wínńdò("yo Swing", 460, 300);
        인사창.ròmọ́_ìdá_ìpìlẹ̀(new àkọlé("yo", 20, 20, 420, 28));
        orúkọ_àayè_wúnrẹ̀n = new SMS_àayè_wúnrẹ̀n("yo", 20, 64, 420, 30);
        인사말 = new àkọlé("yo", 20, 152, 420, 28);
        인사창.ròmọ́_ìdá_ìpìlẹ̀(orúkọ_àayè_wúnrẹ̀n);
        인사창.ròmọ́_ìdá_ìpìlẹ̀(new bọ́tìnnì("인사하기", 20, 108, 180, 32, this));
        인사창.ròmọ́_ìdá_ìpìlẹ̀(인사말);
        인사창.ròmọ́_ìdá_ìpìlẹ̀(new àkọlé("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.ṣàfihàn_wínńdò();
        출력.kọ_ìlà("GUI 예제 gbaradì: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.kọ_SMS("yo, " + orúkọ_àayè_wúnrẹ̀n.글읽기() + "님! (" + 인사횟수 + ")");
        출력.kọ_ìlà("GUI 인사: " + 인사말.글읽기());
    }

    public void ṣiṣẹ́_iṣẹ́() { ṣí_wínńdò(); }
    public void 동작받기(동작알림 알림) {
        출력.kọ_ìlà("ìṣe 알림: " + 알림.àṣẹ_SMS());
        인사하기();
    }
    public static void Rọ́ọ̀nù() {
        ìgbéṣẹ̀_ìtòléra.나중에실행(new 창예제());
    }
}
