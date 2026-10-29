// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.venster;
import 한국어.자체.etiket;
import 한국어.자체.SMS_veld;
import 한국어.자체.knoppie;
import 한국어.자체.gebeurtenis_tou;
import 한국어.자체.Afvoer;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing venster: af 입력 → knoppie → README_eb81d7d9 Teks verfris. */
public class 창예제 implements 실행할일, 동작받이 {
    private venster 인사창;
    private SMS_veld naam_veld;
    private etiket 인사말;
    private int 인사횟수;

    public void skep_venster() {
        인사창 = new venster("af Swing", 460, 300);
        인사창.byvoeg_element(new etiket("af", 20, 20, 420, 28));
        naam_veld = new SMS_veld("af", 20, 64, 420, 30);
        인사말 = new etiket("af", 20, 152, 420, 28);
        인사창.byvoeg_element(naam_veld);
        인사창.byvoeg_element(new knoppie("인사하기", 20, 108, 180, 32, this));
        인사창.byvoeg_element(인사말);
        인사창.byvoeg_element(new etiket("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.wys_venster();
        Afvoer.skryf_lyn("GUI 예제 Maak_gereed: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.skryf_SMS("af, " + naam_veld.글읽기() + "님! (" + 인사횟수 + ")");
        Afvoer.skryf_lyn("GUI 인사: " + 인사말.글읽기());
    }

    public void Voer_uit() { skep_venster(); }
    public void 동작받기(동작알림 알림) {
        Afvoer.skryf_lyn("Aksie 알림: " + 알림.bevel_SMS());
        인사하기();
    }
    public static void Loop() {
        gebeurtenis_tou.나중에실행(new 창예제());
    }
}
