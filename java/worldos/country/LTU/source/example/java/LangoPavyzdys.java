// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Lietuvių.savas.Langas;
import Lietuvių.savas.Pavadinimas;
import Lietuvių.savas.teksto_laukas;
import Lietuvių.savas.mygtukas;
import Lietuvių.savas.įvykis_eilė;
import Lietuvių.savas.Išvestis;
import Lietuvių.savas.실행할일;
import Lietuvių.savas.동작받이;
import Lietuvių.savas.gavinys_pranešimas;

/** savas 커널의 Swing Langas: Lietuvių 입력 → mygtukas → 안내 Tekstas atnaujinti. */
public class LangoPavyzdys implements 실행할일, 동작받이 {
    private Langas 인사창;
    private teksto_laukas pavadinimas_laukas;
    private Pavadinimas 인사말;
    private int 인사횟수;

    public void kurti_langas() {
        인사창 = new Langas("Lietuvių Swing", 460, 300);
        인사창.Įtraukti_elementas(new Pavadinimas("Lietuvių", 20, 20, 420, 28));
        pavadinimas_laukas = new teksto_laukas("Lietuvių", 20, 64, 420, 30);
        인사말 = new Pavadinimas("Lietuvių", 20, 152, 420, 28);
        인사창.Įtraukti_elementas(pavadinimas_laukas);
        인사창.Įtraukti_elementas(new mygtukas("인사하기", 20, 108, 180, 32, this));
        인사창.Įtraukti_elementas(인사말);
        인사창.Įtraukti_elementas(new Pavadinimas("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.laida_langas();
        Išvestis.rašymas_eilutė("GUI 예제 Parengti: LangoPavyzdys");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.rašymas_SMS("Lietuvių, " + pavadinimas_laukas.글읽기() + "님! (" + 인사횟수 + ")");
        Išvestis.rašymas_eilutė("GUI 인사: " + 인사말.글읽기());
    }

    public void Vykdyti() { kurti_langas(); }
    public void gauti_gavinys(gavinys_pranešimas pranešimas) {
        Išvestis.rašymas_eilutė("Veiksmas pranešimas: " + pranešimas.komanda_SMS());
        인사하기();
    }
    public static void Paleisti() {
        įvykis_eilė.나중에실행(new LangoPavyzdys());
    }
}
