// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.windò;
import 한국어.자체.nnyeahà;
import 한국어.자체.SMS_fild;
import 한국어.자체.ọdụmbi;
import 한국어.자체.mmèrème_ọgbàrànchere;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing windò: ig 입력 → ọdụmbi → GỤ̀ỌM_eb81d7d9 SMS mèkwa_ọhụrụ. */
public class 창예제 implements 실행할일, 동작받이 {
    private windò 인사창;
    private SMS_fild akara_ahà_fild;
    private nnyeahà 인사말;
    private int 인사횟수;

    public void mepee_windò() {
        인사창 = new windò("ig Swing", 460, 300);
        인사창.gbakwụnye_njìmebe(new nnyeahà("ig", 20, 20, 420, 28));
        akara_ahà_fild = new SMS_fild("ig", 20, 64, 420, 30);
        인사말 = new nnyeahà("ig", 20, 152, 420, 28);
        인사창.gbakwụnye_njìmebe(akara_ahà_fild);
        인사창.gbakwụnye_njìmebe(new ọdụmbi("인사하기", 20, 108, 180, 32, this));
        인사창.gbakwụnye_njìmebe(인사말);
        인사창.gbakwụnye_njìmebe(new nnyeahà("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.gòsi_windò();
        출력.dee_ahịrī("GUI 예제 Kwado: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.dee_SMS("ig, " + akara_ahà_fild.글읽기() + "님! (" + 인사횟수 + ")");
        출력.dee_ahịrī("GUI 인사: " + 인사말.글읽기());
    }

    public void mee_ọrụ() { mepee_windò(); }
    public void 동작받기(동작알림 알림) {
        출력.dee_ahịrī("mmèm 알림: " + 알림.nnyemiwu_SMS());
        인사하기();
    }
    public static void Bido() {
        mmèrème_ọgbàrànchere.나중에실행(new 창예제());
    }
}
