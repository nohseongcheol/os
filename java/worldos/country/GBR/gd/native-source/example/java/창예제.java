// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.uinneag;
import 한국어.자체.bileag;
import 한국어.자체.raon_teacsa;
import 한국어.자체.putan;
import 한국어.자체.tachartas_ciutha;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing uinneag: gd 입력 → putan → LEUGHMI_eb81d7d9 SMS ath_nuadhaich. */
public class 창예제 implements 실행할일, 동작받이 {
    private uinneag 인사창;
    private raon_teacsa ainm_raon;
    private bileag 인사말;
    private int 인사횟수;

    public void fosgail_uinneag() {
        인사창 = new uinneag("gd Swing", 460, 300);
        인사창.cuir_ris_eileamaid(new bileag("gd", 20, 20, 420, 28));
        ainm_raon = new raon_teacsa("gd", 20, 64, 420, 30);
        인사말 = new bileag("gd", 20, 152, 420, 28);
        인사창.cuir_ris_eileamaid(ainm_raon);
        인사창.cuir_ris_eileamaid(new putan("인사하기", 20, 108, 180, 32, this));
        인사창.cuir_ris_eileamaid(인사말);
        인사창.cuir_ris_eileamaid(new bileag("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.show_uinneag();
        출력.sgrìobh_loidhne("GUI 예제 Ullaich: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.sgrìobh_SMS("gd, " + ainm_raon.글읽기() + "님! (" + 인사횟수 + ")");
        출력.sgrìobh_loidhne("GUI 인사: " + 인사말.글읽기());
    }

    public void Ruith() { fosgail_uinneag(); }
    public void 동작받기(동작알림 알림) {
        출력.sgrìobh_loidhne("Gnìomh 알림: " + 알림.àithne_SMS());
        인사하기();
    }
    public static void ruith() {
        tachartas_ciutha.나중에실행(new 창예제());
    }
}
