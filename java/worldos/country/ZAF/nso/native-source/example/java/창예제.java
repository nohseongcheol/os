// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.lefastere;
import 한국어.자체.leibole;
import 한국어.자체.SMS_lefelwana;
import 한국어.자체.konope;
import 한국어.자체.tiragalo_lenaneotetelo;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing lefastere: nso 입력 → konope → faele_ya_MPALE_eb81d7d9 Sengwalwa mpshafatša. */
public class 창예제 implements 실행할일, 동작받이 {
    private lefastere 인사창;
    private SMS_lefelwana leina_lefelwana;
    private leibole 인사말;
    private int 인사횟수;

    public void bula_lefastere() {
        인사창 = new lefastere("nso Swing", 460, 300);
        인사창.oketša_elemente(new leibole("nso", 20, 20, 420, 28));
        leina_lefelwana = new SMS_lefelwana("nso", 20, 64, 420, 30);
        인사말 = new leibole("nso", 20, 152, 420, 28);
        인사창.oketša_elemente(leina_lefelwana);
        인사창.oketša_elemente(new konope("인사하기", 20, 108, 180, 32, this));
        인사창.oketša_elemente(인사말);
        인사창.oketša_elemente(new leibole("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.bontšha_lefastere();
        출력.ngwala_mothaladi("GUI 예제 Lokišetša: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.ngwala_SMS("nso, " + leina_lefelwana.글읽기() + "님! (" + 인사횟수 + ")");
        출력.ngwala_mothaladi("GUI 인사: " + 인사말.글읽기());
    }

    public void phethagatša_mošomo() { bula_lefastere(); }
    public void 동작받기(동작알림 알림) {
        출력.ngwala_mothaladi("Mogato 알림: " + 알림.taelo_SMS());
        인사하기();
    }
    public static void Diriša() {
        tiragalo_lenaneotetelo.나중에실행(new 창예제());
    }
}
