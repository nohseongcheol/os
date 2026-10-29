// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.dirisha;
import 한국어.자체.lebo;
import 한국어.자체.SMS_uga;
import 한국어.자체.kitufe;
import 한국어.자체.tukio_foleni;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing dirisha: sw 입력 → kitufe → NISOME_eb81d7d9 SMS onyesha_upya. */
public class 창예제 implements 실행할일, 동작받이 {
    private dirisha 인사창;
    private SMS_uga jina_uga;
    private lebo 인사말;
    private int 인사횟수;

    public void unda_dirisha() {
        인사창 = new dirisha("sw Swing", 460, 300);
        인사창.jumlisha_elementi(new lebo("sw", 20, 20, 420, 28));
        jina_uga = new SMS_uga("sw", 20, 64, 420, 30);
        인사말 = new lebo("sw", 20, 152, 420, 28);
        인사창.jumlisha_elementi(jina_uga);
        인사창.jumlisha_elementi(new kitufe("인사하기", 20, 108, 180, 32, this));
        인사창.jumlisha_elementi(인사말);
        인사창.jumlisha_elementi(new lebo("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.onyesha_dirisha();
        출력.andika_laini("GUI 예제 Andaa: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.andika_SMS("sw, " + jina_uga.글읽기() + "님! (" + 인사횟수 + ")");
        출력.andika_laini("GUI 인사: " + 인사말.글읽기());
    }

    public void tekeleza_kazi() { unda_dirisha(); }
    public void 동작받기(동작알림 알림) {
        출력.andika_laini("Kitendo 알림: " + 알림.amri_SMS());
        인사하기();
    }
    public static void endesha() {
        tukio_foleni.나중에실행(new 창예제());
    }
}
