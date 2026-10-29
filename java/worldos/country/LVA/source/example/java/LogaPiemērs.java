// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Latviešu.savs.Logs;
import Latviešu.savs.Etiķete;
import Latviešu.savs.teksta_lauks;
import Latviešu.savs.Pogas;
import Latviešu.savs.notikums_rinda;
import Latviešu.savs.Izvade;
import Latviešu.savs.실행할일;
import Latviešu.savs.동작받이;
import Latviešu.savs.darbība_informēšana;

/** savs 커널의 Swing Logs: Latviešu 입력 → Pogas → fails_Lasi_mani_eb81d7d9 Teksts atsvaidzināt. */
public class LogaPiemērs implements 실행할일, 동작받이 {
    private Logs 인사창;
    private teksta_lauks nosaukums_lauks;
    private Etiķete 인사말;
    private int 인사횟수;

    public void atvērt_logs() {
        인사창 = new Logs("Latviešu Swing", 460, 300);
        인사창.Pievienot_elements(new Etiķete("Latviešu", 20, 20, 420, 28));
        nosaukums_lauks = new teksta_lauks("Latviešu", 20, 64, 420, 30);
        인사말 = new Etiķete("Latviešu", 20, 152, 420, 28);
        인사창.Pievienot_elements(nosaukums_lauks);
        인사창.Pievienot_elements(new Pogas("인사하기", 20, 108, 180, 32, this));
        인사창.Pievienot_elements(인사말);
        인사창.Pievienot_elements(new Etiķete("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.rādīt_logs();
        Izvade.rakstīšana_līnija("GUI 예제 Sagatavot: LogaPiemērs");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.rakstīšana_SMS("Latviešu, " + nosaukums_lauks.글읽기() + "님! (" + 인사횟수 + ")");
        Izvade.rakstīšana_līnija("GUI 인사: " + 인사말.글읽기());
    }

    public void Izpildīt() { atvērt_logs(); }
    public void saņemt_darbība(darbība_informēšana informēšana) {
        Izvade.rakstīšana_līnija("Darbība informēšana: " + informēšana.komanda_SMS());
        인사하기();
    }
    public static void Palaist() {
        notikums_rinda.나중에실행(new LogaPiemērs());
    }
}
