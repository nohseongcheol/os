// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.pəncərə;
import 한국어.자체.Etiket;
import 한국어.자체.SMS_sahə;
import 한국어.자체.düymə;
import 한국어.자체.hadisə_növbə;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing pəncərə: az 입력 → düymə → OXUMƏNİ_eb81d7d9 Mətn təzələmək. */
public class 창예제 implements 실행할일, 동작받이 {
    private pəncərə 인사창;
    private SMS_sahə ad_sahə;
    private Etiket 인사말;
    private int 인사횟수;

    public void açmaq_pəncərə() {
        인사창 = new pəncərə("az Swing", 460, 300);
        인사창.əlavə_etmək_element(new Etiket("az", 20, 20, 420, 28));
        ad_sahə = new SMS_sahə("az", 20, 64, 420, 30);
        인사말 = new Etiket("az", 20, 152, 420, 28);
        인사창.əlavə_etmək_element(ad_sahə);
        인사창.əlavə_etmək_element(new düymə("인사하기", 20, 108, 180, 32, this));
        인사창.əlavə_etmək_element(인사말);
        인사창.əlavə_etmək_element(new Etiket("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.göstərmək_pəncərə();
        출력.yazmaq_xətt("GUI 예제 Hazırla: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.yazmaq_SMS("az, " + ad_sahə.글읽기() + "님! (" + 인사횟수 + ")");
        출력.yazmaq_xətt("GUI 인사: " + 인사말.글읽기());
    }

    public void icra_etmək_tapşırıq() { açmaq_pəncərə(); }
    public void 동작받기(동작알림 알림) {
        출력.yazmaq_xətt("Gedişat 알림: " + 알림.əmr_SMS());
        인사하기();
    }
    public static void İcra_Et() {
        hadisə_növbə.나중에실행(new 창예제());
    }
}
