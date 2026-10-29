// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Nederlands.Eigen.Venster;
import Nederlands.Eigen.Etiket;
import Nederlands.Eigen.tekstveld;
import Nederlands.Eigen.knop;
import Nederlands.Eigen.gebeurtenis_wachtrij;
import Nederlands.Eigen.tekstuitvoer;
import Nederlands.Eigen.실행할일;
import Nederlands.Eigen.동작받이;
import Nederlands.Eigen.Actie_kennisgeving;

/** Eigen 커널의 Swing Venster: Nederlands invoer_WAARDE → knop → LEESMIJ_eb81d7d9 tekst vernieuwen. */
public class Venstervoorbeeld implements 실행할일, 동작받이 {
    private Venster 인사창;
    private tekstveld naam_veld;
    private Etiket 인사말;
    private int 인사횟수;

    public void open_venster() {
        인사창 = new Venster("Nederlands Swing", 460, 300);
        인사창.Toevoegen_element(new Etiket("Hallo", 20, 20, 420, 28));
        naam_veld = new tekstveld("Nederlands", 20, 64, 420, 30);
        인사말 = new Etiket("Hallo", 20, 152, 420, 28);
        인사창.Toevoegen_element(naam_veld);
        인사창.Toevoegen_element(new knop("인사하기", 20, 108, 180, 32, this));
        인사창.Toevoegen_element(인사말);
        인사창.Toevoegen_element(new Etiket("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.weergeven_venster();
        tekstuitvoer.schrijven_lijn("GUI 예제 Bereid_voor: Venstervoorbeeld");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.schrijven_sms("Hallo, " + naam_veld.글읽기() + "님! (" + 인사횟수 + ")");
        tekstuitvoer.schrijven_lijn("GUI 인사: " + 인사말.글읽기());
    }

    public void Uitvoeren() { open_venster(); }
    public void ontvangen_Actie(Actie_kennisgeving kennisgeving) {
        tekstuitvoer.schrijven_lijn("Actie kennisgeving: " + kennisgeving.opdracht_sms());
        인사하기();
    }
    public static void starten() {
        gebeurtenis_wachtrij.나중에실행(new Venstervoorbeeld());
    }
}
