// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.Dritare;
import 한국어.자체.Etiketë;
import 한국어.자체.SMS_fushë;
import 한국어.자체.Buton;
import 한국어.자체.ngjarje_radhë;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing Dritare: sq 입력 → Buton → LEXOMË_eb81d7d9 Teksti freskoj. */
public class 창예제 implements 실행할일, 동작받이 {
    private Dritare 인사창;
    private SMS_fushë emër_fushë;
    private Etiketë 인사말;
    private int 인사횟수;

    public void hap_dritare() {
        인사창 = new Dritare("sq Swing", 460, 300);
        인사창.shto_element(new Etiketë("sq", 20, 20, 420, 28));
        emër_fushë = new SMS_fushë("sq", 20, 64, 420, 30);
        인사말 = new Etiketë("sq", 20, 152, 420, 28);
        인사창.shto_element(emër_fushë);
        인사창.shto_element(new Buton("인사하기", 20, 108, 180, 32, this));
        인사창.shto_element(인사말);
        인사창.shto_element(new Etiketë("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.shfaq_dritare();
        출력.shkruaj_linjë("GUI 예제 Përgatit: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.shkruaj_SMS("sq, " + emër_fushë.글읽기() + "님! (" + 인사횟수 + ")");
        출력.shkruaj_linjë("GUI 인사: " + 인사말.글읽기());
    }

    public void Kryej() { hap_dritare(); }
    public void 동작받기(동작알림 알림) {
        출력.shkruaj_linjë("Veprim 알림: " + 알림.komandë_SMS());
        인사하기();
    }
    public static void Ekzekuto() {
        ngjarje_radhë.나중에실행(new 창예제());
    }
}
