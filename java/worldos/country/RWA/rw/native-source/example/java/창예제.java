// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Ikinyarwanda.자체.idirishya;
import Ikinyarwanda.자체.Akarango;
import Ikinyarwanda.자체.SMS_umwanya;
import Ikinyarwanda.자체.buto;
import Ikinyarwanda.자체.icyabaye_umurongo_utegererezwaho;
import Ikinyarwanda.자체.출력;
import Ikinyarwanda.자체.실행할일;
import Ikinyarwanda.자체.동작받이;
import Ikinyarwanda.자체.동작알림;

/** 자체 커널의 Swing idirishya: rw 입력 → buto → NSOMA_eb81d7d9 Umwandiko kugaruraho. */
public class 창예제 implements 실행할일, 동작받이 {
    private idirishya 인사창;
    private SMS_umwanya izina_umwanya;
    private Akarango 인사말;
    private int 인사횟수;

    public void kurema_idirishya() {
        인사창 = new idirishya("rw Swing", 460, 300);
        인사창.kongeraho_ikintu(new Akarango("rw", 20, 20, 420, 28));
        izina_umwanya = new SMS_umwanya("rw", 20, 64, 420, 30);
        인사말 = new Akarango("rw", 20, 152, 420, 28);
        인사창.kongeraho_ikintu(izina_umwanya);
        인사창.kongeraho_ikintu(new buto("인사하기", 20, 108, 180, 32, this));
        인사창.kongeraho_ikintu(인사말);
        인사창.kongeraho_ikintu(new Akarango("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.kugaragaza_idirishya();
        출력.kwandika_umurongo("GUI 예제 Gutegura: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.kwandika_SMS("rw, " + izina_umwanya.글읽기() + "님! (" + 인사횟수 + ")");
        출력.kwandika_umurongo("GUI 인사: " + 인사말.글읽기());
    }

    public void gukora_umukoro() { kurema_idirishya(); }
    public void 동작받기(동작알림 알림) {
        출력.kwandika_umurongo("Igikorwa 알림: " + 알림.ibwiriza_SMS());
        인사하기();
    }
    public static void ihuriro() {
        icyabaye_umurongo_utegererezwaho.나중에실행(new 창예제());
    }
}
