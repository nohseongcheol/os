// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.eget.Vindu;
import norsk.eget.Etikett;
import norsk.eget.tekstfelt;
import norsk.eget.Knapp;
import norsk.eget.hendelse_kø;
import norsk.eget.Utgang;
import norsk.eget.실행할일;
import norsk.eget.동작받이;
import norsk.eget.Gjøremål_notice;

/** eget 커널의 Swing Vindu: Norwegian Bokmål inndata_VERDI → Knapp → Viktig_fil_eb81d7d9 Tekst oppdatere. */
public class Vinduseksempel implements 실행할일, 동작받이 {
    private Vindu 인사창;
    private tekstfelt navn_felt;
    private Etikett 인사말;
    private int 인사횟수;

    public void åpen_vindu() {
        인사창 = new Vindu("Norwegian Bokmål Swing", 460, 300);
        인사창.Legg_til_element(new Etikett("Hei", 20, 20, 420, 28));
        navn_felt = new tekstfelt("Norwegian Bokmål", 20, 64, 420, 30);
        인사말 = new Etikett("Hei", 20, 152, 420, 28);
        인사창.Legg_til_element(navn_felt);
        인사창.Legg_til_element(new Knapp("인사하기", 20, 108, 180, 32, this));
        인사창.Legg_til_element(인사말);
        인사창.Legg_til_element(new Etikett("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.vise_vindu();
        Utgang.skrive_linje("GUI 예제 Forbered: Vinduseksempel");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.skrive_SMS("Hei, " + navn_felt.글읽기() + "님! (" + 인사횟수 + ")");
        Utgang.skrive_linje("GUI 인사: " + 인사말.글읽기());
    }

    public void Kjør() { åpen_vindu(); }
    public void motta_Gjøremål(Gjøremål_notice notice) {
        Utgang.skrive_linje("Handling notice: " + notice.kommando_SMS());
        인사하기();
    }
    public static void Kjør_2() {
        hendelse_kø.나중에실행(new Vinduseksempel());
    }
}
