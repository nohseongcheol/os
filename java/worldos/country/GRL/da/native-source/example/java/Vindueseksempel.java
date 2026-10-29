// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Dansk.eget.Vindue;
import Dansk.eget.Etiket;
import Dansk.eget.tekstfelt;
import Dansk.eget.knap;
import Dansk.eget.hændelse_kø;
import Dansk.eget.Udgang;
import Dansk.eget.실행할일;
import Dansk.eget.동작받이;
import Dansk.eget.동작알림;

/** eget 커널의 Swing Vindue: da input_VÆRDI → knap → Vigtigt_eb81d7d9 Tekst opdatere. */
public class Vindueseksempel implements 실행할일, 동작받이 {
    private Vindue 인사창;
    private tekstfelt navn_felt;
    private Etiket 인사말;
    private int 인사횟수;

    public void åben_vindue() {
        인사창 = new Vindue("da Swing", 460, 300);
        인사창.Tilføj_element(new Etiket("Hej", 20, 20, 420, 28));
        navn_felt = new tekstfelt("da", 20, 64, 420, 30);
        인사말 = new Etiket("Hej", 20, 152, 420, 28);
        인사창.Tilføj_element(navn_felt);
        인사창.Tilføj_element(new knap("인사하기", 20, 108, 180, 32, this));
        인사창.Tilføj_element(인사말);
        인사창.Tilføj_element(new Etiket("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.vise_vindue();
        Udgang.skrive_linje("GUI 예제 Tilrettelæg: Vindueseksempel");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.skrive_sms("Hej, " + navn_felt.글읽기() + "님! (" + 인사횟수 + ")");
        Udgang.skrive_linje("GUI 인사: " + 인사말.글읽기());
    }

    public void Kør() { åben_vindue(); }
    public void modtage_To_do(동작알림 알림) {
        Udgang.skrive_linje("Handling 알림: " + 알림.kommando_sms());
        인사하기();
    }
    public static void Kør_2() {
        hændelse_kø.나중에실행(new Vindueseksempel());
    }
}
