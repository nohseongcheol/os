// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.vlastné.Okno;
import Slovenský.vlastné.Nápis;
import Slovenský.vlastné.textové_pole;
import Slovenský.vlastné.Tlačidlo;
import Slovenský.vlastné.udalosť_front;
import Slovenský.vlastné.Výstup;
import Slovenský.vlastné.실행할일;
import Slovenský.vlastné.동작받이;
import Slovenský.vlastné.Akcia_upozornenie;

/** vlastné 커널의 Swing Okno: Slovenský vstup_VALUE → Tlačidlo → 안내 Spracovanie_textu obnoviť. */
public class UkážkaOkna implements 실행할일, 동작받이 {
    private Okno 인사창;
    private textové_pole názov_pole;
    private Nápis 인사말;
    private int 인사횟수;

    public void otvoriť_okno() {
        인사창 = new Okno("Slovenský Swing", 460, 300);
        인사창.Pridať_prvok(new Nápis("Slovenský", 20, 20, 420, 28));
        názov_pole = new textové_pole("Slovenský", 20, 64, 420, 30);
        인사말 = new Nápis("Slovenský", 20, 152, 420, 28);
        인사창.Pridať_prvok(názov_pole);
        인사창.Pridať_prvok(new Tlačidlo("인사하기", 20, 108, 180, 32, this));
        인사창.Pridať_prvok(인사말);
        인사창.Pridať_prvok(new Nápis("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.zobraziť_okno();
        Výstup.zapísať_linka("GUI 예제 Pripraviť: UkážkaOkna");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.zapísať_SMS("Slovenský, " + názov_pole.글읽기() + "님! (" + 인사횟수 + ")");
        Výstup.zapísať_linka("GUI 인사: " + 인사말.글읽기());
    }

    public void Spustiť() { otvoriť_okno(); }
    public void dostať_Akcia(Akcia_upozornenie upozornenie) {
        Výstup.zapísať_linka("Akcia upozornenie: " + upozornenie.príkaz_SMS());
        인사하기();
    }
    public static void Spustiť_2() {
        udalosť_front.나중에실행(new UkážkaOkna());
    }
}
