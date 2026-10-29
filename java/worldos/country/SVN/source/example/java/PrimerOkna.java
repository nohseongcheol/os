// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import slovenščina.lastno.okno;
import slovenščina.lastno.Oznaka;
import slovenščina.lastno.SMS_polje;
import slovenščina.lastno.Gumb;
import slovenščina.lastno.dogodek_čakalna_vrsta;
import slovenščina.lastno.Izpis;
import slovenščina.lastno.실행할일;
import slovenščina.lastno.동작받이;
import slovenščina.lastno.akcija_obvestilo;

/** lastno 커널의 Swing okno: slovenščina 입력 → Gumb → 안내 Besedilo osvežiti. */
public class PrimerOkna implements 실행할일, 동작받이 {
    private okno 인사창;
    private SMS_polje ime_polje;
    private Oznaka 인사말;
    private int 인사횟수;

    public void odprto_okno() {
        인사창 = new okno("slovenščina Swing", 460, 300);
        인사창.Dodaj_element(new Oznaka("slovenščina", 20, 20, 420, 28));
        ime_polje = new SMS_polje("slovenščina", 20, 64, 420, 30);
        인사말 = new Oznaka("slovenščina", 20, 152, 420, 28);
        인사창.Dodaj_element(ime_polje);
        인사창.Dodaj_element(new Gumb("인사하기", 20, 108, 180, 32, this));
        인사창.Dodaj_element(인사말);
        인사창.Dodaj_element(new Oznaka("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.oddaja_okno();
        Izpis.pisati_linija("GUI 예제 Pripravi: PrimerOkna");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.pisati_SMS("slovenščina, " + ime_polje.글읽기() + "님! (" + 인사횟수 + ")");
        Izpis.pisati_linija("GUI 인사: " + 인사말.글읽기());
    }

    public void Izvedi() { odprto_okno(); }
    public void sprejeti_sprejemati_prejeti_prejemati_akcija(akcija_obvestilo obvestilo) {
        Izpis.pisati_linija("Dejanje obvestilo: " + obvestilo.ukaz_SMS());
        인사하기();
    }
    public static void Zaženi() {
        dogodek_čakalna_vrsta.나중에실행(new PrimerOkna());
    }
}
