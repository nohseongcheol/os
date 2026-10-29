// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.fensetere;
import 한국어.자체.wijete;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    fensetere 화면;
    leibola MPUISE_eb81d7d9;
    SMS_lefelo 입력;
    public void diragatsa_Tiro() {
        검사.참인지(tiragalo_diletakgatiso.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new fensetere("한국어 laeborari fensetere", 400, 280);
        MPUISE_eb81d7d9 = wijete.theka_Boleng("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = wijete.SMS_lefelo("leina", 20, 65, 340, 30);
        화면.tsenya_tlhakakaelo(MPUISE_eb81d7d9);
        화면.tsenya_tlhakakaelo(입력);
        화면.tsenya_tlhakakaelo(wijete.konopo("인사하기", 20, 110, 180, 32, this));
        화면.bontsha_fensetere();
        출력.kwala_Mola("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 tiragalo) {
        검사.참인지(tiragalo_diletakgatiso.사건처리중인가(), "한국어 tiro 되부름");
        검사.참인지(tiragalo.tshupane() == 1001 && tiragalo.tiragalo_Motswedi() instanceof konopo, "한국어 tiragalo 객체와 출처");
        검사.참인지(!((Object)tiragalo.tiragalo_Motswedi() instanceof javax.swing.JButton), "표준 단추와 독립된 fometa_Boleng");
        검사.참인지(!((Object)tiragalo instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 fometa_Boleng");
        MPUISE_eb81d7d9.kwala_SMS("안녕하세요 " + 입력.글읽기());
        출력.kwala_Mola("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        tiragalo_diletakgatiso.나중에실행(new 한글창시험());
    }
}
