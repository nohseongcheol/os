// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.venster;
import 한국어.자체.legstuk;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    venster 화면;
    etiket README_eb81d7d9;
    SMS_veld 입력;
    public void Voer_uit() {
        검사.참인지(gebeurtenis_tou.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new venster("한국어 biblioteek venster", 400, 280);
        README_eb81d7d9 = legstuk.merk_VALUE("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = legstuk.SMS_veld("Naam", 20, 65, 340, 30);
        화면.byvoeg_element(README_eb81d7d9);
        화면.byvoeg_element(입력);
        화면.byvoeg_element(legstuk.knoppie("인사하기", 20, 110, 180, 32, this));
        화면.wys_venster();
        Afvoer.skryf_lyn("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 gebeurtenis) {
        검사.참인지(gebeurtenis_tou.사건처리중인가(), "한국어 Aksie 되부름");
        검사.참인지(gebeurtenis.INDEX() == 1001 && gebeurtenis.gebeurtenis_bron() instanceof knoppie, "한국어 gebeurtenis 객체와 출처");
        검사.참인지(!((Object)gebeurtenis.gebeurtenis_bron() instanceof javax.swing.JButton), "표준 단추와 독립된 formaat_VALUE");
        검사.참인지(!((Object)gebeurtenis instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 formaat_VALUE");
        README_eb81d7d9.skryf_SMS("안녕하세요 " + 입력.글읽기());
        Afvoer.skryf_lyn("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        gebeurtenis_tou.나중에실행(new 한글창시험());
    }
}
