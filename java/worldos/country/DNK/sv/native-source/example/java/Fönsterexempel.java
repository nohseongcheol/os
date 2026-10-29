// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Svenska.eget.Fönster;
import Svenska.eget.Etikett;
import Svenska.eget.textfält;
import Svenska.eget.knapp;
import Svenska.eget.händelse_kö;
import Svenska.eget.utmatningsposition;
import Svenska.eget.실행할일;
import Svenska.eget.동작받이;
import Svenska.eget.동작알림;

/** eget 커널의 Swing Fönster: sv indata_värde → knapp → VIKTIGT_eb81d7d9 text uppdatera. */
public class Fönsterexempel implements 실행할일, 동작받이 {
    private Fönster 인사창;
    private textfält namn_fält;
    private Etikett 인사말;
    private int 인사횟수;

    public void skapa_fönster() {
        인사창 = new Fönster("sv Swing", 460, 300);
        인사창.Lägg_till_element(new Etikett("Hej", 20, 20, 420, 28));
        namn_fält = new textfält("sv", 20, 64, 420, 30);
        인사말 = new Etikett("Hej", 20, 152, 420, 28);
        인사창.Lägg_till_element(namn_fält);
        인사창.Lägg_till_element(new knapp("인사하기", 20, 108, 180, 32, this));
        인사창.Lägg_till_element(인사말);
        인사창.Lägg_till_element(new Etikett("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.visa_fönster();
        utmatningsposition.skriva_rad("GUI 예제 Förbereda: Fönsterexempel");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.skriva_SMS("Hej, " + namn_fält.läsa_SMS() + "님! (" + 인사횟수 + ")");
        utmatningsposition.skriva_rad("GUI 인사: " + 인사말.läsa_SMS());
    }

    public void Starta() { skapa_fönster(); }
    public void få_Action(동작알림 알림) {
        utmatningsposition.skriva_rad("Åtgärd 알림: " + 알림.kommando_SMS());
        인사하기();
    }
    public static void Kör() {
        händelse_kö.나중에실행(new Fönsterexempel());
    }
}
