// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.penjire;
import 한국어.자체.belgi;
import 한국어.자체.tekst_meýdançasy;
import 한국어.자체.düwme;
import 한국어.자체.waka_nobat;
import 한국어.자체.출력;
import 한국어.자체.실행할일;
import 한국어.자체.동작받이;
import 한국어.자체.동작알림;

/** 자체 커널의 Swing penjire: tk 입력 → düwme → README_eb81d7d9 Metin täzelendir. */
public class 창예제 implements 실행할일, 동작받이 {
    private penjire 인사창;
    private tekst_meýdançasy at_meýdan;
    private belgi 인사말;
    private int 인사횟수;

    public void aç_penjire() {
        인사창 = new penjire("tk Swing", 460, 300);
        인사창.goş_element(new belgi("tk", 20, 20, 420, 28));
        at_meýdan = new tekst_meýdançasy("tk", 20, 64, 420, 30);
        인사말 = new belgi("tk", 20, 152, 420, 28);
        인사창.goş_element(at_meýdan);
        인사창.goş_element(new düwme("인사하기", 20, 108, 180, 32, this));
        인사창.goş_element(인사말);
        인사창.goş_element(new belgi("F9 / Shift+Space | X", 20, 204, 420, 28));
        인사창.görkez_penjire();
        출력.ýaz_setir("GUI 예제 Taýýarla: 창예제");
    }

    public void 인사하기() {
        인사횟수++;
        인사말.ýaz_SMS("tk, " + at_meýdan.글읽기() + "님! (" + 인사횟수 + ")");
        출력.ýaz_setir("GUI 인사: " + 인사말.글읽기());
    }

    public void ýerine_ýetir_tabşyryk() { aç_penjire(); }
    public void 동작받기(동작알림 알림) {
        출력.ýaz_setir("iş 알림: " + 알림.buýruk_SMS());
        인사하기();
    }
    public static void Bitir() {
        waka_nobat.나중에실행(new 창예제());
    }
}
