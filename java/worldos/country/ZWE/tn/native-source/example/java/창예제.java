// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.fensetere;
import 한국어.자체.leibola;
import 한국어.자체.SMS_lefelo;
import 한국어.자체.konopo;
import 한국어.자체.tiragalo_diletakgatiso;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing fensetere: tn 입력 → konopo → MPUISE_eb81d7d9 SMS Tsosolosa. */
public class 창예제 implements 실행할일, 동작받이 {
    private fensetere 인사창;
    private SMS_lefelo leina_lefelo;
    private leibola 인사말;
    private int 인사횟수;

    public void bula_fensetere() {
        인사창 = new fensetere("tn Swing", 460, 300);
        인사창.tsenya_tlhakakaelo(new leibola("tn", 20, 20, 420, 28));
        leina_lefelo = new SMS_lefelo("tn", 20, 64, 420, 30);
        인사말 = new leibola("tn", 20, 152, 420, 28);
        인사창.tsenya_tlhakakaelo(leina_lefelo);
        인사창.tsenya_tlhakakaelo(new konopo("인사하기", 20, 108, 180, 32, this));
        인사창.tsenya_tlhakakaelo(인사말);
        인사창.tsenya_tlhakakaelo(new leibola("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.bontsha_fensetere();
        출력.kwala_Mola("GUI 예제 Baakanya: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.kwala_SMS("tn, " + leina_lefelo.글읽기() + "님! (" + 인사횟수 + ")");
        출력.kwala_Mola("GUI 인사: " + 인사말.글읽기());
    }

    public void diragatsa_Tiro() { bula_fensetere(); }
    public void 동작받기(동작알림 알림) {
        출력.kwala_Mola("tiro 알림: " + 알림.Taelo_SMS());
        인사하기();
    }
    public static void dirisa() {
        tiragalo_diletakgatiso.나중에실행(new 창예제());
    }
}
