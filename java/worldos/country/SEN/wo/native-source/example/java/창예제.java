// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.palanteer;
import 한국어.자체.tur;
import 한국어.자체.SMS_barabu_denc_ab_joxe;
import 한국어.자체.butoñ;
import 한국어.자체.xewxew_Topplante_xaarandi;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing palanteer: wo 입력 → butoñ → JANG_MA_eb81d7d9 Tekst Yeesal. */
public class 창예제 implements 실행할일, 동작받이 {
    private palanteer 인사창;
    private SMS_barabu_denc_ab_joxe tur_barabu_denc_ab_joxe;
    private tur 인사말;
    private int 인사횟수;

    public void sos_palanteer() {
        인사창 = new palanteer("wo Swing", 460, 300);
        인사창.mottal_cër(new tur("wo", 20, 20, 420, 28));
        tur_barabu_denc_ab_joxe = new SMS_barabu_denc_ab_joxe("wo", 20, 64, 420, 30);
        인사말 = new tur("wo", 20, 152, 420, 28);
        인사창.mottal_cër(tur_barabu_denc_ab_joxe);
        인사창.mottal_cër(new butoñ("인사하기", 20, 108, 180, 32, this));
        인사창.mottal_cër(인사말);
        인사창.mottal_cër(new tur("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.féeñal_palanteer();
        출력.biir_buum("GUI 예제 jël_matuwaay: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.biir_SMS("wo, " + tur_barabu_denc_ab_joxe.글읽기() + "님! (" + 인사횟수 + ")");
        출력.biir_buum("GUI 인사: " + 인사말.글읽기());
    }

    public void def_ligeey() { sos_palanteer(); }
    public void 동작받기(동작알림 알림) {
        출력.biir_buum("jëf 알림: " + 알림.ndigel_SMS());
        인사하기();
    }
    public static void daw() {
        xewxew_Topplante_xaarandi.나중에실행(new 창예제());
    }
}
