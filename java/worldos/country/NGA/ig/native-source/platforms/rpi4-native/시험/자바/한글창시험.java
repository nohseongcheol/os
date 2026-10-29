// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.windò;
import 한국어.자체.ngwa_nkepụta;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    windò 화면;
    nnyeahà GỤ̀ỌM_eb81d7d9;
    SMS_fild 입력;
    public void mee_ọrụ() {
        검사.참인지(mmèrème_ọgbàrànchere.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new windò("한국어 ọbaakwụkwọ windò", 400, 280);
        GỤ̀ỌM_eb81d7d9 = ngwa_nkepụta.hụbaamā_valuu("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = ngwa_nkepụta.SMS_fild("Aha", 20, 65, 340, 30);
        화면.gbakwụnye_njìmebe(GỤ̀ỌM_eb81d7d9);
        화면.gbakwụnye_njìmebe(입력);
        화면.gbakwụnye_njìmebe(ngwa_nkepụta.ọdụmbi("인사하기", 20, 110, 180, 32, this));
        화면.gòsi_windò();
        출력.dee_ahịrī("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 mmèrème) {
        검사.참인지(mmèrème_ọgbàrànchere.사건처리중인가(), "한국어 mmèm 되부름");
        검사.참인지(mmèrème.indèks() == 1001 && mmèrème.mmèrème_ebensìbịa() instanceof ọdụmbi, "한국어 mmèrème 객체와 출처");
        검사.참인지(!((Object)mmèrème.mmèrème_ebensìbịa() instanceof javax.swing.JButton), "표준 단추와 독립된 hàzie_valuu");
        검사.참인지(!((Object)mmèrème instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 hàzie_valuu");
        GỤ̀ỌM_eb81d7d9.dee_SMS("안녕하세요 " + 입력.글읽기());
        출력.dee_ahịrī("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        mmèrème_ọgbàrànchere.나중에실행(new 한글창시험());
    }
}
