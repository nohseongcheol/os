// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Isi_Zulu.자체.ifasitela;
import Isi_Zulu.자체.uphawu;
import Isi_Zulu.자체.I_SMS_inkundla_indawana;
import Isi_Zulu.자체.inkinobho;
import Isi_Zulu.자체.isigameko_ujenge;
import Isi_Zulu.자체.출력;
import Isi_Zulu.자체.실행할일;
import Isi_Zulu.자체.동작받이;
import Isi_Zulu.자체.동작알림;

/** 자체 커널의 Swing ifasitela: zu 입력 → inkinobho → NGIFUNDE_eb81d7d9 Itekisi vuselela. */
public class 창예제 implements 실행할일, 동작받이 {
    private ifasitela 인사창;
    private I_SMS_inkundla_indawana igama_inkundla_indawana;
    private uphawu 인사말;
    private int 인사횟수;

    public void vula_ifasitela() {
        인사창 = new ifasitela("zu Swing", 460, 300);
        인사창.hlanganisa_ilungu(new uphawu("zu", 20, 20, 420, 28));
        igama_inkundla_indawana = new I_SMS_inkundla_indawana("zu", 20, 64, 420, 30);
        인사말 = new uphawu("zu", 20, 152, 420, 28);
        인사창.hlanganisa_ilungu(igama_inkundla_indawana);
        인사창.hlanganisa_ilungu(new inkinobho("인사하기", 20, 108, 180, 32, this));
        인사창.hlanganisa_ilungu(인사말);
        인사창.hlanganisa_ilungu(new uphawu("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.khombisa_ifasitela();
        출력.bhala_umugqa("GUI 예제 Hlela: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.bhala_I_SMS("zu, " + igama_inkundla_indawana.글읽기() + "님! (" + 인사횟수 + ")");
        출력.bhala_umugqa("GUI 인사: " + 인사말.글읽기());
    }

    public void yenza_umsebenzi() { vula_ifasitela(); }
    public void 동작받기(동작알림 알림) {
        출력.bhala_umugqa("Isenzo 알림: " + 알림.umyalo_I_SMS());
        인사하기();
    }
    public static void Sebenzisa() {
        isigameko_ujenge.나중에실행(new 창예제());
    }
}
