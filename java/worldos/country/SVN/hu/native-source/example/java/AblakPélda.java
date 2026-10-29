// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import magyar.saját.Ablak;
import magyar.saját.Címke;
import magyar.saját.szövegmező;
import magyar.saját.gomb;
import magyar.saját.esemény_várólista;
import magyar.saját.Kimenet;
import magyar.saját.실행할일;
import magyar.saját.동작받이;
import magyar.saját.Action_alapelv;

/** saját 커널의 Swing Ablak: hu bevitel_ÉRTÉK → gomb → fontos_fájl_eb81d7d9 Szöveg frissít. */
public class AblakPélda implements 실행할일, 동작받이 {
    private Ablak 인사창;
    private szövegmező név_mező;
    private Címke 인사말;
    private int 인사횟수;

    public void készít_ablak() {
        인사창 = new Ablak("hu Swing", 460, 300);
        인사창.hozzáad_elem(new Címke("hu", 20, 20, 420, 28));
        név_mező = new szövegmező("hu", 20, 64, 420, 30);
        인사말 = new Címke("hu", 20, 152, 420, 28);
        인사창.hozzáad_elem(név_mező);
        인사창.hozzáad_elem(new gomb("인사하기", 20, 108, 180, 32, this));
        인사창.hozzáad_elem(인사말);
        인사창.hozzáad_elem(new Címke("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.bemutató_ablak();
        Kimenet.ír_sor("GUI 예제 Előkészítés: AblakPélda");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.ír_SMS("hu, " + név_mező.글읽기() + "님! (" + 인사횟수 + ")");
        Kimenet.ír_sor("GUI 인사: " + 인사말.글읽기());
    }

    public void Végrehajtás() { készít_ablak(); }
    public void fogad_Action(Action_alapelv alapelv) {
        Kimenet.ír_sor("Művelet alapelv: " + alapelv.parancs_SMS());
        인사하기();
    }
    public static void Futtatás() {
        esemény_várólista.나중에실행(new AblakPélda());
    }
}
