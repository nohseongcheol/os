// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.taga;
import 한국어.자체.alama;
import 한국어.자체.SMS_Fili;
import 한국어.자체.maɓali;
import 한국어.자체.Faruwa_Jerin_ayyukan_da_za_a_yi;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing taga: ha 입력 → maɓali → README_eb81d7d9 SMS Wartsakewa. */
public class 창예제 implements 실행할일, 동작받이 {
    private taga 인사창;
    private SMS_Fili Suna_Fili;
    private alama 인사말;
    private int 인사횟수;

    public void buɗe_taga() {
        인사창 = new taga("ha Swing", 460, 300);
        인사창.ƙara_Dan_gutsuren_bayani(new alama("ha", 20, 20, 420, 28));
        Suna_Fili = new SMS_Fili("ha", 20, 64, 420, 30);
        인사말 = new alama("ha", 20, 152, 420, 28);
        인사창.ƙara_Dan_gutsuren_bayani(Suna_Fili);
        인사창.ƙara_Dan_gutsuren_bayani(new maɓali("인사하기", 20, 108, 180, 32, this));
        인사창.ƙara_Dan_gutsuren_bayani(인사말);
        인사창.ƙara_Dan_gutsuren_bayani(new alama("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.Nuna_taga();
        출력.Rubuta_Layi("GUI 예제 Shirya: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.Rubuta_SMS("ha, " + Suna_Fili.글읽기() + "님! (" + 인사횟수 + ")");
        출력.Rubuta_Layi("GUI 인사: " + 인사말.글읽기());
    }

    public void gudanar_aiki() { buɗe_taga(); }
    public void 동작받기(동작알림 알림) {
        출력.Rubuta_Layi("Aiki 알림: " + 알림.Umarni_SMS());
        인사하기();
    }
    public static void Tafiyar_da() {
        Faruwa_Jerin_ayyukan_da_za_a_yi.나중에실행(new 창예제());
    }
}
