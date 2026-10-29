// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.oyna;
import 한국어.자체.vidjet;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    oyna 화면;
    Yorliq ma_lumot_fayli_eb81d7d9;
    SMS_ma_lumotlar_maydoni 입력;
    public void Ishga_tushirish() {
        검사.참인지(hodisa_navbat.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new oyna("한국어 kutubxona oyna", 400, 280);
        ma_lumot_fayli_eb81d7d9 = vidjet.teg_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = vidjet.SMS_ma_lumotlar_maydoni("Nomi", 20, 65, 340, 30);
        화면.qo_shmoq_element(ma_lumot_fayli_eb81d7d9);
        화면.qo_shmoq_element(입력);
        화면.qo_shmoq_element(vidjet.tugma("인사하기", 20, 110, 180, 32, this));
        화면.ko_rsatmoq_oyna();
        출력.yozmoq_satr("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 hodisa) {
        검사.참인지(hodisa_navbat.사건처리중인가(), "한국어 Amal 되부름");
        검사.참인지(hodisa.INDEX() == 1001 && hodisa.hodisa_manba() instanceof tugma, "한국어 hodisa 객체와 출처");
        검사.참인지(!((Object)hodisa.hodisa_manba() instanceof javax.swing.JButton), "표준 단추와 독립된 format_VALUE");
        검사.참인지(!((Object)hodisa instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 format_VALUE");
        ma_lumot_fayli_eb81d7d9.yozmoq_SMS("안녕하세요 " + 입력.글읽기());
        출력.yozmoq_satr("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        hodisa_navbat.나중에실행(new 한글창시험());
    }
}
