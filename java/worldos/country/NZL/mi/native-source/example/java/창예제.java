// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Reo_Māori.자체.matapihi;
import Reo_Māori.자체.tapanga;
import Reo_Māori.자체.āpure_kuputuhi;
import Reo_Māori.자체.pātene;
import Reo_Māori.자체.hui_tūtira;
import Reo_Māori.자체.출력;
import Reo_Māori.자체.실행할일;
import Reo_Māori.자체.동작받이;
import Reo_Māori.자체.동작알림;

/** 자체 커널의 Swing matapihi: mi 입력 → pātene → PĀNUIMAI_eb81d7d9 Ngā_kupu tāmata. */
public class 창예제 implements 실행할일, 동작받이 {
    private matapihi 인사창;
    private āpure_kuputuhi ingoa_āpure;
    private tapanga 인사말;
    private int 인사횟수;

    public void tiwhikete_matapihi() {
        인사창 = new matapihi("mi Swing", 460, 300);
        인사창.tāpiri_huānga(new tapanga("mi", 20, 20, 420, 28));
        ingoa_āpure = new āpure_kuputuhi("mi", 20, 64, 420, 30);
        인사말 = new tapanga("mi", 20, 152, 420, 28);
        인사창.tāpiri_huānga(ingoa_āpure);
        인사창.tāpiri_huānga(new pātene("인사하기", 20, 108, 180, 32, this));
        인사창.tāpiri_huānga(인사말);
        인사창.tāpiri_huānga(new tapanga("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.whakaatu_matapihi();
        출력.tuhi_hononga("GUI 예제 Whakarite: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.tuhi_TEXT("mi, " + ingoa_āpure.글읽기() + "님! (" + 인사횟수 + ")");
        출력.tuhi_hononga("GUI 인사: " + 인사말.글읽기());
    }

    public void kawe_tūmahi() { tiwhikete_matapihi(); }
    public void 동작받기(동작알림 알림) {
        출력.tuhi_hononga("hohenga 알림: " + 알림.tono_TEXT());
        인사하기();
    }
    public static void whakahaere() {
        hui_tūtira.나중에실행(new 창예제());
    }
}
