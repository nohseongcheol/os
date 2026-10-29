// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import hrvatski.vlastiti.Prozor;
import hrvatski.vlastiti.Natpis;
import hrvatski.vlastiti.tekstno_polje;
import hrvatski.vlastiti.gumb;
import hrvatski.vlastiti.događaj_red_čekanja;
import hrvatski.vlastiti.Izlaz;
import hrvatski.vlastiti.실행할일;
import hrvatski.vlastiti.동작받이;
import hrvatski.vlastiti.akcija_obavijest;

/** vlastiti 커널의 Swing Prozor: hrvatski 입력 → gumb → 안내 Tekst osvježiti. */
public class PrimjerProzora implements 실행할일, 동작받이 {
    private Prozor 인사창;
    private tekstno_polje naziv_polje;
    private Natpis 인사말;
    private int 인사횟수;

    public void otvoreno_prozor() {
        인사창 = new Prozor("hrvatski Swing", 460, 300);
        인사창.Dodaj_element(new Natpis("hrvatski", 20, 20, 420, 28));
        naziv_polje = new tekstno_polje("hrvatski", 20, 64, 420, 30);
        인사말 = new Natpis("hrvatski", 20, 152, 420, 28);
        인사창.Dodaj_element(naziv_polje);
        인사창.Dodaj_element(new gumb("인사하기", 20, 108, 180, 32, this));
        인사창.Dodaj_element(인사말);
        인사창.Dodaj_element(new Natpis("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.emisija_prozor();
        Izlaz.zapisivanje_red("GUI 예제 Pripremi: PrimjerProzora");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.zapisivanje_SMS("hrvatski, " + naziv_polje.글읽기() + "님! (" + 인사횟수 + ")");
        Izlaz.zapisivanje_red("GUI 인사: " + 인사말.글읽기());
    }

    public void Izvrši() { otvoreno_prozor(); }
    public void primiti_akcija(akcija_obavijest obavijest) {
        Izlaz.zapisivanje_red("Aktivnost obavijest: " + obavijest.naredba_SMS());
        인사하기();
    }
    public static void Pokreni() {
        događaj_red_čekanja.나중에실행(new PrimjerProzora());
    }
}
