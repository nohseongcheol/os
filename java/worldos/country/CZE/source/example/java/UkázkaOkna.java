// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.vlastní.Okno;
import čeština.vlastní.Popisek;
import čeština.vlastní.textové_pole;
import čeština.vlastní.tlačítko;
import čeština.vlastní.událost_fronta;
import čeština.vlastní.výstupní_pozice;
import čeština.vlastní.실행할일;
import čeština.vlastní.동작받이;
import čeština.vlastní.Akce_povinnost_zvěřejnit;

/** vlastní 커널의 Swing Okno: čeština vstup_HODNOTA → tlačítko → 안내 text aktualizovat. */
public class UkázkaOkna implements 실행할일, 동작받이 {
    private Okno 인사창;
    private textové_pole název_pole;
    private Popisek 인사말;
    private int 인사횟수;

    public void otevřít_okno() {
        인사창 = new Okno("čeština Swing", 460, 300);
        인사창.Přidat_prvek(new Popisek("čeština", 20, 20, 420, 28));
        název_pole = new textové_pole("čeština", 20, 64, 420, 30);
        인사말 = new Popisek("čeština", 20, 152, 420, 28);
        인사창.Přidat_prvek(název_pole);
        인사창.Přidat_prvek(new tlačítko("인사하기", 20, 108, 180, 32, this));
        인사창.Přidat_prvek(인사말);
        인사창.Přidat_prvek(new Popisek("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.zobrazit_okno();
        výstupní_pozice.zápis_čára("GUI 예제 Připravit: UkázkaOkna");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.zápis_SMS("čeština, " + název_pole.글읽기() + "님! (" + 인사횟수 + ")");
        výstupní_pozice.zápis_čára("GUI 인사: " + 인사말.글읽기());
    }

    public void Spustit() { otevřít_okno(); }
    public void dostat_Akce(Akce_povinnost_zvěřejnit povinnost_zvěřejnit) {
        výstupní_pozice.zápis_čára("Akce povinnost_zvěřejnit: " + povinnost_zvěřejnit.příkaz_SMS());
        인사하기();
    }
    public static void Spustit_2() {
        událost_fronta.나중에실행(new UkázkaOkna());
    }
}
