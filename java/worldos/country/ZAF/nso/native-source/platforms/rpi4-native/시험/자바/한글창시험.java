// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.lefastere;
import 한국어.자체.witšete;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    lefastere 화면;
    leibole faele_ya_MPALE_eb81d7d9;
    SMS_lefelwana 입력;
    public void phethagatša_mošomo() {
        검사.참인지(tiragalo_lenaneotetelo.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new lefastere("한국어 Bokgobadata lefastere", 400, 280);
        faele_ya_MPALE_eb81d7d9 = witšete.leswao_boleng_a1435ed2("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = witšete.SMS_lefelwana("Leina", 20, 65, 340, 30);
        화면.oketša_elemente(faele_ya_MPALE_eb81d7d9);
        화면.oketša_elemente(입력);
        화면.oketša_elemente(witšete.konope("인사하기", 20, 110, 180, 32, this));
        화면.bontšha_lefastere();
        출력.ngwala_mothaladi("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 tiragalo) {
        검사.참인지(tiragalo_lenaneotetelo.사건처리중인가(), "한국어 Mogato 되부름");
        검사.참인지(tiragalo.lokela() == 1001 && tiragalo.tiragalo_mohlodi() instanceof konope, "한국어 tiragalo 객체와 출처");
        검사.참인지(!((Object)tiragalo.tiragalo_mohlodi() instanceof javax.swing.JButton), "표준 단추와 독립된 fomete_boleng");
        검사.참인지(!((Object)tiragalo instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 fomete_boleng");
        faele_ya_MPALE_eb81d7d9.ngwala_SMS("안녕하세요 " + 입력.글읽기());
        출력.ngwala_mothaladi("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        tiragalo_lenaneotetelo.나중에실행(new 한글창시험());
    }
}
