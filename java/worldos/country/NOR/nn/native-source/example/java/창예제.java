// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.vindauge;
import 한국어.자체.Etikett;
import 한국어.자체.SMS_felt;
import 한국어.자체.knapp;
import 한국어.자체.hending_kø;
import 한국어.자체.Utdata;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing vindauge: nn 입력 → knapp → Viktig_eb81d7d9 Tekst oppdatere. */
public class 창예제 implements 실행할일, 동작받이 {
    private vindauge 인사창;
    private SMS_felt namn_felt;
    private Etikett 인사말;
    private int 인사횟수;

    public void opne_vindauge() {
        인사창 = new vindauge("nn Swing", 460, 300);
        인사창.leggje_til_element(new Etikett("nn", 20, 20, 420, 28));
        namn_felt = new SMS_felt("nn", 20, 64, 420, 30);
        인사말 = new Etikett("nn", 20, 152, 420, 28);
        인사창.leggje_til_element(namn_felt);
        인사창.leggje_til_element(new knapp("인사하기", 20, 108, 180, 32, this));
        인사창.leggje_til_element(인사말);
        인사창.leggje_til_element(new Etikett("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.vise_vindauge();
        Utdata.skrive_line("GUI 예제 Klargjer: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.skrive_SMS("nn, " + namn_felt.글읽기() + "님! (" + 인사횟수 + ")");
        Utdata.skrive_line("GUI 인사: " + 인사말.글읽기());
    }

    public void Køyr() { opne_vindauge(); }
    public void 동작받기(동작알림 알림) {
        Utdata.skrive_line("Handling 알림: " + 알림.kommando_SMS());
        인사하기();
    }
    public static void Køyr_2() {
        hending_kø.나중에실행(new 창예제());
    }
}
