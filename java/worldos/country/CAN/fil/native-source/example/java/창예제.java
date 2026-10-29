// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.window;
import 한국어.자체.label;
import 한국어.자체.SMS_field;
import 한국어.자체.button;
import 한국어.자체.kaganapan_pila;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing window: fil 입력 → button → BASAHINAKO_eb81d7d9 SMS i_refresh. */
public class 창예제 implements 실행할일, 동작받이 {
    private window 인사창;
    private SMS_field pangalan_field;
    private label 인사말;
    private int 인사횟수;

    public void buksan_window() {
        인사창 = new window("fil Swing", 460, 300);
        인사창.idagdag_elemento(new label("fil", 20, 20, 420, 28));
        pangalan_field = new SMS_field("fil", 20, 64, 420, 30);
        인사말 = new label("fil", 20, 152, 420, 28);
        인사창.idagdag_elemento(pangalan_field);
        인사창.idagdag_elemento(new button("인사하기", 20, 108, 180, 32, this));
        인사창.idagdag_elemento(인사말);
        인사창.idagdag_elemento(new label("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.ipakita_window();
        출력.sumulat_linya("GUI 예제 Ihanda: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.sumulat_SMS("fil, " + pangalan_field.글읽기() + "님! (" + 인사횟수 + ")");
        출력.sumulat_linya("GUI 인사: " + 인사말.글읽기());
    }

    public void Mag_execute_gawain() { buksan_window(); }
    public void 동작받기(동작알림 알림) {
        출력.sumulat_linya("aksyon 알림: " + 알림.utos_SMS());
        인사하기();
    }
    public static void run() {
        kaganapan_pila.나중에실행(new 창예제());
    }
}
