// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 phote_boleng = 연결통신.수신열기(0);
        kgokaganya moeng_boleng = 연결통신.Bula("127.0.0.1", phote_boleng.접속번호());
        kgokaganya mong_sešupi = phote_boleng.받기();
        moeng_boleng.대기시간(200); mong_sešupi.대기시간(200);
        검사.참인지(moeng_boleng.연결됨() && !moeng_boleng.닫힘(), "Ikgokaganye boemo_boleng");
        검사.참인지(mong_sešupi.접속번호() == moeng_boleng.지역접속번호(), "sedirišwa_sa_legoro_le_tee_boleng 접속번호");
        검사.참인지(moeng_boleng.접속번호() == mong_sešupi.지역접속번호(), "kgauswi_skoupo 접속번호");
        입력흐름 입력 = mong_sešupi.입력(); 출력흐름 출력쪽 = moeng_boleng.출력();
        byte[] molaetša = 문자.부호화("한글 Stream_boleng");
        출력쪽.Ngwala(molaetša, 0, molaetša.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[molaetša.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.Bala(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Faele 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.boetša_sekeng_data(받은글), "한글 Stream_boleng"), "부분 읽기와 Ngwala");
        출력쪽.Ngwala(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Bala(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "arei_boleng Bala");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Bala();
        검사.참인지(두바이트[1] == 18, "나머지 Bala");
        mong_sešupi.출력().Ngwala(255);
        검사.참인지(moeng_boleng.입력().Bala() == 255, "go_enkhouta_boleng 없는 한 paete_boleng");
        출력쪽.Tswalela();
        검사.참인지(moeng_boleng.닫힘() && 입력.Bala() == -1, "닫기와 Faele 끝");
        입력.Tswalela(); 검사.참인지(mong_sešupi.닫힘(), "입력 Stream_boleng Tswalela");
        moeng_boleng.Tswalela(); mong_sešupi.Tswalela();
        phote_boleng.대기시간(15);
        boolean 시간제한 = false;
        try { phote_boleng.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        phote_boleng.Tswalela(); 검사.참인지(phote_boleng.닫힘(), "수신창구 Tswalela");
        전문통로 받는곳 = 전문통로.Bula(0), 보내는곳 = 전문통로.Bula(0);
        받는곳.대기시간(200);
        보내는곳.Romela("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Tswalela(); 받는곳.Tswalela();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Tswalela");
        출력.ngwala_mothaladi("한국어 통신 kgonthiša: Ikgokaganye 전문 Stream_boleng 시간제한 Tswalela");
    }
}
