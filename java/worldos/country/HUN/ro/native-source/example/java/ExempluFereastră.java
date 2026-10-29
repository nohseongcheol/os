// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Română.propriu.Fereastră;
import Română.propriu.Etichetă;
import Română.propriu.câmp_text;
import Română.propriu.buton;
import Română.propriu.eveniment_coadă;
import Română.propriu.Rezultat;
import Română.propriu.실행할일;
import Română.propriu.동작받이;
import Română.propriu.Acțiune_înștiințare;

/** propriu 커널의 Swing Fereastră: ro 입력 → buton → 안내 SMS reîmprospăta. */
public class ExempluFereastră implements 실행할일, 동작받이 {
    private Fereastră 인사창;
    private câmp_text nume_câmp;
    private Etichetă 인사말;
    private int 인사횟수;

    public void crea_fereastră() {
        인사창 = new Fereastră("ro Swing", 460, 300);
        인사창.adăuga_element(new Etichetă("ro", 20, 20, 420, 28));
        nume_câmp = new câmp_text("ro", 20, 64, 420, 30);
        인사말 = new Etichetă("ro", 20, 152, 420, 28);
        인사창.adăuga_element(nume_câmp);
        인사창.adăuga_element(new buton("인사하기", 20, 108, 180, 32, this));
        인사창.adăuga_element(인사말);
        인사창.adăuga_element(new Etichetă("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.afișa_fereastră();
        Rezultat.scriere_linie("GUI 예제 Pregătiți: ExempluFereastră");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.scriere_SMS("ro, " + nume_câmp.글읽기() + "님! (" + 인사횟수 + ")");
        Rezultat.scriere_linie("GUI 인사: " + 인사말.글읽기());
    }

    public void Execută() { crea_fereastră(); }
    public void primi_Acțiune(Acțiune_înștiințare înștiințare) {
        Rezultat.scriere_linie("Acțiuni înștiințare: " + înștiințare.comandă_SMS());
        인사하기();
    }
    public static void Pornește() {
        eveniment_coadă.나중에실행(new ExempluFereastră());
    }
}
