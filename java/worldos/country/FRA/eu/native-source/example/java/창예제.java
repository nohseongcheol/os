// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Euskara.자체.Leihoa;
import Euskara.자체.Etiketa;
import Euskara.자체.SMS_eremu;
import Euskara.자체.botoia;
import Euskara.자체.gertaera_ilara;
import Euskara.자체.Irteera;
import Euskara.자체.실행할일;
import Euskara.자체.동작받이;
import Euskara.자체.동작알림;

/** 자체 커널의 Swing Leihoa: eu 입력 → botoia → IRAKHAU_eb81d7d9 Testua freskatu. */
public class 창예제 implements 실행할일, 동작받이 {
    private Leihoa 인사창;
    private SMS_eremu izen_eremu;
    private Etiketa 인사말;
    private int 인사횟수;

    public void ireki_leiho() {
        인사창 = new Leihoa("eu Swing", 460, 300);
        인사창.gehitu_elementu(new Etiketa("eu", 20, 20, 420, 28));
        izen_eremu = new SMS_eremu("eu", 20, 64, 420, 30);
        인사말 = new Etiketa("eu", 20, 152, 420, 28);
        인사창.gehitu_elementu(izen_eremu);
        인사창.gehitu_elementu(new botoia("인사하기", 20, 108, 180, 32, this));
        인사창.gehitu_elementu(인사말);
        인사창.gehitu_elementu(new Etiketa("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.erakutsi_leiho();
        Irteera.idatzi_lerro("GUI 예제 준비: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.idatzi_SMS("eu, " + izen_eremu.글읽기() + "님! (" + 인사횟수 + ")");
        Irteera.idatzi_lerro("GUI 인사: " + 인사말.글읽기());
    }

    public void Exekutatu() { ireki_leiho(); }
    public void 동작받기(동작알림 알림) {
        Irteera.idatzi_lerro("Ekintza 알림: " + 알림.komando_SMS());
        인사하기();
    }
    public static void Exekutatu_2() {
        gertaera_ilara.나중에실행(new 창예제());
    }
}
