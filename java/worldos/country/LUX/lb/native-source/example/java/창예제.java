// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.Fënster;
import 한국어.자체.Numm_5ce2bd6f;
import 한국어.자체.Textfeld;
import 한국어.자체.Tast;
import 한국어.자체.Evenement_Schlaang;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing Fënster: lb 입력 → Tast → LIESMECH_eb81d7d9 SMS aktualiséieren. */
public class 창예제 implements 실행할일, 동작받이 {
    private Fënster 인사창;
    private Textfeld Numm_Feld;
    private Numm_5ce2bd6f 인사말;
    private int 인사횟수;

    public void ariichten_Fënster() {
        인사창 = new Fënster("lb Swing", 460, 300);
        인사창.derbäisetzen_Element(new Numm_5ce2bd6f("lb", 20, 20, 420, 28));
        Numm_Feld = new Textfeld("lb", 20, 64, 420, 30);
        인사말 = new Numm_5ce2bd6f("lb", 20, 152, 420, 28);
        인사창.derbäisetzen_Element(Numm_Feld);
        인사창.derbäisetzen_Element(new Tast("인사하기", 20, 108, 180, 32, this));
        인사창.derbäisetzen_Element(인사말);
        인사창.derbäisetzen_Element(new Numm_5ce2bd6f("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.Show_Fënster();
        출력.schreiwen_Zeil("GUI 예제 Préparéieren: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.schreiwen_SMS("lb, " + Numm_Feld.글읽기() + "님! (" + 인사횟수 + ")");
        출력.schreiwen_Zeil("GUI 인사: " + 인사말.글읽기());
    }

    public void Ausféieren() { ariichten_Fënster(); }
    public void 동작받기(동작알림 알림) {
        출력.schreiwen_Zeil("Aktioun 알림: " + 알림.Befeel_SMS());
        인사하기();
    }
    public static void Laf() {
        Evenement_Schlaang.나중에실행(new 창예제());
    }
}
