// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.dirisha;
import 한국어.자체.wijeti;
import 한국어.자체.*;

public class 한글창시험 implements 실행할일, 동작받이 {
    dirisha 화면;
    lebo NISOME_eb81d7d9;
    SMS_uga 입력;
    public void tekeleza_kazi() {
        검사.참인지(tukio_foleni.사건처리중인가(), "한국어 화면 작업 큐");
        화면 = new dirisha("한국어 maktaba dirisha", 400, 280);
        NISOME_eb81d7d9 = wijeti.lebo_thamani("한글로 Java 코딩", 20, 20, 340, 30);
        입력 = wijeti.SMS_uga("Jina", 20, 65, 340, 30);
        화면.jumlisha_elementi(NISOME_eb81d7d9);
        화면.jumlisha_elementi(입력);
        화면.jumlisha_elementi(wijeti.kitufe("인사하기", 20, 110, 180, 32, this));
        화면.onyesha_dirisha();
        출력.andika_laini("KOREAN SWING READY");
    }
    public void 동작받기(동작알림 tukio) {
        검사.참인지(tukio_foleni.사건처리중인가(), "한국어 Kitendo 되부름");
        검사.참인지(tukio.kielezo() == 1001 && tukio.tukio_chanzo() instanceof kitufe, "한국어 tukio 객체와 출처");
        검사.참인지(!((Object)tukio.tukio_chanzo() instanceof javax.swing.JButton), "표준 단추와 독립된 umbiza_thamani");
        검사.참인지(!((Object)tukio instanceof java.awt.event.ActionEvent), "표준 사건과 독립된 umbiza_thamani");
        NISOME_eb81d7d9.andika_SMS("안녕하세요 " + 입력.글읽기());
        출력.andika_laini("KOREAN SWING CLICK " + 입력.글읽기());
    }
    public static void main(String[] 인수) {
        tukio_foleni.나중에실행(new 한글창시험());
    }
}
