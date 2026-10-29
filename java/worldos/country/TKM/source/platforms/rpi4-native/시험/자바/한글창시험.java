// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.penjire;
import 한국어.자체.wijet;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    penjire 화면;
    belgi README_eb81d7d9;
    tekst_meýdançasy 입력;
    public void ýerine_ýetir_tabşyryk() {
        검사.참인지(waka_nobat.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new penjire("한국어 Kitaphana penjire", 400, 280);
        README_eb81d7d9 = wijet.bellik_baha("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = wijet.tekst_meýdançasy("Ad", 20, 65, 340, 30);
        화면.goş_element(README_eb81d7d9);
        화면.goş_element(입력);
        화면.goş_element(wijet.düwme("인사하기", 20, 110, 180, 32, this));
        화면.görkez_penjire();
        출력.ýaz_setir("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 waka) {
        검사.참인지(waka_nobat.사건처리중인가(), "한국어 iş 되부름");
        검사.참인지(waka.indeks() == 1001 && waka.waka_gor() instanceof düwme, "한국어 waka 객체와 출처");
        검사.참인지(!((Object)waka.waka_gor() instanceof javax.swing.JButton), "표준 단추와 독립된 format_baha");
        검사.참인지(!((Object)waka instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_baha");
        README_eb81d7d9.ýaz_SMS("안녕하세요 " + 입력.글읽기());
        출력.ýaz_setir("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        waka_nobat.나중에실행(new 한글창시험());
    }
}
