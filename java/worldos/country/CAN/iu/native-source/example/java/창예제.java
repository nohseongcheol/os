// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.igalaangujaq;
import 한국어.자체.nalunairli;
import 한국어.자체.titiqqaq_kisumuungavik;
import 한국어.자체.tikkuagaq;
import 한국어.자체.piniku_utaqqivik;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing igalaangujaq: iu 입력 → tikkuagaq → README_eb81d7d9 titiqqaq qittaijarli. */
public class 창예제 implements 실행할일, 동작받이 {
    private igalaangujaq 인사창;
    private titiqqaq_kisumuungavik atiq_kisumuungavik;
    private nalunairli 인사말;
    private int 인사횟수;

    public void matuirli_igalaangujaq() {
        인사창 = new igalaangujaq("iu Swing", 460, 300);
        인사창.ilali_ilanga(new nalunairli("iu", 20, 20, 420, 28));
        atiq_kisumuungavik = new titiqqaq_kisumuungavik("iu", 20, 64, 420, 30);
        인사말 = new nalunairli("iu", 20, 152, 420, 28);
        인사창.ilali_ilanga(atiq_kisumuungavik);
        인사창.ilali_ilanga(new tikkuagaq("인사하기", 20, 108, 180, 32, this));
        인사창.ilali_ilanga(인사말);
        인사창.ilali_ilanga(new nalunairli("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.saqqilli_igalaangujaq();
        출력.titiraq_titikutaak("GUI 예제 Parnalli: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.titiraq_titiqqaq("iu, " + atiq_kisumuungavik.글읽기() + "님! (" + 인사횟수 + ")");
        출력.titiraq_titikutaak("GUI 인사: " + 인사말.글읽기());
    }

    public void 실행하기() { matuirli_igalaangujaq(); }
    public void 동작받기(동작알림 알림) {
        출력.titiraq_titikutaak("sugiarut 알림: " + 알림.piqujijjut_titiqqaq());
        인사하기();
    }
    public static void 시작() {
        piniku_utaqqivik.나중에실행(new 창예제());
    }
}
