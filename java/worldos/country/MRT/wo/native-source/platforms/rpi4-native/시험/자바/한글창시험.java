// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.palanteer;
import 한국어.자체.kifin;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    palanteer 화면;
    tur JANG_MA_eb81d7d9;
    SMS_barabu_denc_ab_joxe 입력;
    public void def_ligeey() {
        검사.참인지(xewxew_Topplante_xaarandi.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new palanteer("한국어 daaray_téere palanteer", 400, 280);
        JANG_MA_eb81d7d9 = kifin.xàmme_xëyma("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = kifin.SMS_barabu_denc_ab_joxe("tur_253d1510", 20, 65, 340, 30);
        화면.mottal_cër(JANG_MA_eb81d7d9);
        화면.mottal_cër(입력);
        화면.mottal_cër(kifin.butoñ("인사하기", 20, 110, 180, 32, this));
        화면.féeñal_palanteer();
        출력.biir_buum("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 xewxew) {
        검사.참인지(xewxew_Topplante_xaarandi.사건처리중인가(), "한국어 jëf 되부름");
        검사.참인지(xewxew.àlluwa_tur() == 1001 && xewxew.xewxew_Cosaan() instanceof butoñ, "한국어 xewxew 객체와 출처");
        검사.참인지(!((Object)xewxew.xewxew_Cosaan() instanceof javax.swing.JButton), "표준 단추와 독립된 dayo_xëyma");
        검사.참인지(!((Object)xewxew instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 dayo_xëyma");
        JANG_MA_eb81d7d9.biir_SMS("안녕하세요 " + 입력.글읽기());
        출력.biir_buum("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        xewxew_Topplante_xaarandi.나중에실행(new 한글창시험());
    }
}
