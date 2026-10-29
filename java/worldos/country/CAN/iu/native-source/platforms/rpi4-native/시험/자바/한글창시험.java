// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.igalaangujaq;
import 한국어.자체.화면요소;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    igalaangujaq 화면;
    nalunairli README_eb81d7d9;
    titiqqaq_kisumuungavik 입력;
    public void 실행하기() {
        검사.참인지(piniku_utaqqivik.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new igalaangujaq("한국어 tukisiurvik igalaangujaq", 400, 280);
        README_eb81d7d9 = 화면요소.nalunaikkutaq_atuutilik("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = 화면요소.titiqqaq_kisumuungavik("atiq", 20, 65, 340, 30);
        화면.ilali_ilanga(README_eb81d7d9);
        화면.ilali_ilanga(입력);
        화면.ilali_ilanga(화면요소.tikkuagaq("인사하기", 20, 110, 180, 32, this));
        화면.saqqilli_igalaangujaq();
        출력.titiraq_titikutaak("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 piniku) {
        검사.참인지(piniku_utaqqivik.사건처리중인가(), "한국어 sugiarut 되부름");
        검사.참인지(piniku.nalunaiqsimavik() == 1001 && piniku.piniku_pivviujuq() instanceof tikkuagaq, "한국어 piniku 객체와 출처");
        검사.참인지(!((Object)piniku.piniku_pivviujuq() instanceof javax.swing.JButton), "표준 단추와 독립된 aaqqisurli_atuutilik");
        검사.참인지(!((Object)piniku instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 aaqqisurli_atuutilik");
        README_eb81d7d9.titiraq_titiqqaq("안녕하세요 " + 입력.글읽기());
        출력.titiraq_titikutaak("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        piniku_utaqqivik.나중에실행(new 한글창시험());
    }
}
