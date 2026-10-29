// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.oyna;
import 한국어.자체.Yorliq;
import 한국어.자체.SMS_ma_lumotlar_maydoni;
import 한국어.자체.tugma;
import 한국어.자체.hodisa_navbat;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing oyna: Uzbek 입력 → tugma → ma_lumot_fayli_eb81d7d9 Matn yangilamoq. */
public class 창예제 implements 실행할일, 동작받이 {
    private oyna 인사창;
    private SMS_ma_lumotlar_maydoni nom_ma_lumotlar_maydoni;
    private Yorliq 인사말;
    private int 인사횟수;

    public void ochmoq_oyna() {
        인사창 = new oyna("Uzbek Swing", 460, 300);
        인사창.qo_shmoq_element(new Yorliq("Uzbek", 20, 20, 420, 28));
        nom_ma_lumotlar_maydoni = new SMS_ma_lumotlar_maydoni("Uzbek", 20, 64, 420, 30);
        인사말 = new Yorliq("Uzbek", 20, 152, 420, 28);
        인사창.qo_shmoq_element(nom_ma_lumotlar_maydoni);
        인사창.qo_shmoq_element(new tugma("인사하기", 20, 108, 180, 32, this));
        인사창.qo_shmoq_element(인사말);
        인사창.qo_shmoq_element(new Yorliq("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.ko_rsatmoq_oyna();
        출력.yozmoq_satr("GUI 예제 Tayyorlamoq: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.yozmoq_SMS("Uzbek, " + nom_ma_lumotlar_maydoni.글읽기() + "님! (" + 인사횟수 + ")");
        출력.yozmoq_satr("GUI 인사: " + 인사말.글읽기());
    }

    public void Ishga_tushirish() { ochmoq_oyna(); }
    public void 동작받기(동작알림 알림) {
        출력.yozmoq_satr("Amal 알림: " + 알림.buyruq_SMS());
        인사하기();
    }
    public static void Bajarish() {
        hodisa_navbat.나중에실행(new 창예제());
    }
}
