// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Isi_Zulu.자체.ifasitela;
import Isi_Zulu.자체.iwijethi;
import Isi_Zulu.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    ifasitela 화면;
    uphawu NGIFUNDE_eb81d7d9;
    I_SMS_inkundla_indawana 입력;
    public void yenza_umsebenzi() {
        검사.참인지(isigameko_ujenge.사건처리중인가(), "Isi_Zulu 화면 작업 큐");
        화면 = new ifasitela("Isi_Zulu umtapo ifasitela", 400, 280);
        NGIFUNDE_eb81d7d9 = iwijethi.ithegi_inani("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = iwijethi.I_SMS_inkundla_indawana("Igama", 20, 65, 340, 30);
        화면.hlanganisa_ilungu(NGIFUNDE_eb81d7d9);
        화면.hlanganisa_ilungu(입력);
        화면.hlanganisa_ilungu(iwijethi.inkinobho("인사하기", 20, 110, 180, 32, this));
        화면.khombisa_ifasitela();
        출력.bhala_umugqa("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 isigameko) {
        검사.참인지(isigameko_ujenge.사건처리중인가(), "Isi_Zulu Isenzo 되부름");
        검사.참인지(isigameko.thola_inkomba() == 1001 && isigameko.isigameko_umthombo() instanceof inkinobho, "Isi_Zulu isigameko 객체와 출처");
        검사.참인지(!((Object)isigameko.isigameko_umthombo() instanceof javax.swing.JButton), "표준 단추와 독립된 misa_inani");
        검사.참인지(!((Object)isigameko instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 misa_inani");
        NGIFUNDE_eb81d7d9.bhala_I_SMS("안녕하세요 " + 입력.글읽기());
        출력.bhala_umugqa("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        isigameko_ujenge.나중에실행(new 한글창시험());
    }
}
