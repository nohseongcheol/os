// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import polski.własny.Okno;
import polski.własny.Etykieta;
import polski.własny.pole_tekstowe;
import polski.własny.przycisk;
import polski.własny.konkurs_kolejka;
import polski.własny.pozycja_wyjścia;
import polski.własny.실행할일;
import polski.własny.동작받이;
import polski.własny.akcja_powiadomienie;

/** własny 커널의 Swing Okno: polski wejście_WARTOŚĆ → przycisk → plik_README_eb81d7d9 tekst odświeżyć. */
public class PrzykładOkna implements 실행할일, 동작받이 {
    private Okno 인사창;
    private pole_tekstowe nazwa_pole;
    private Etykieta 인사말;
    private int 인사횟수;

    public void otwarty_okno() {
        인사창 = new Okno("polski Swing", 460, 300);
        인사창.Dodaj_element(new Etykieta("Witaj", 20, 20, 420, 28));
        nazwa_pole = new pole_tekstowe("polski", 20, 64, 420, 30);
        인사말 = new Etykieta("Witaj", 20, 152, 420, 28);
        인사창.Dodaj_element(nazwa_pole);
        인사창.Dodaj_element(new przycisk("인사하기", 20, 108, 180, 32, this));
        인사창.Dodaj_element(인사말);
        인사창.Dodaj_element(new Etykieta("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.program_okno();
        pozycja_wyjścia.zapis_linia("GUI 예제 Przygotuj: PrzykładOkna");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.zapis_SMS("Witaj, " + nazwa_pole.글읽기() + "님! (" + 인사횟수 + ")");
        pozycja_wyjścia.zapis_linia("GUI 인사: " + 인사말.글읽기());
    }

    public void Uruchom() { otwarty_okno(); }
    public void odbierać_akcja(akcja_powiadomienie powiadomienie) {
        pozycja_wyjścia.zapis_linia("Akcja powiadomienie: " + powiadomienie.polecenie_SMS());
        인사하기();
    }
    public static void Uruchom_2() {
        konkurs_kolejka.나중에실행(new PrzykładOkna());
    }
}
