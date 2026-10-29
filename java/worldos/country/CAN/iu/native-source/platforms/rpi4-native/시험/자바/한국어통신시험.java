// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 kapputigaq_atuutilik = 연결통신.수신열기(0);
        kasuqsimaniq 손님 = 연결통신.matuirli("127.0.0.1", kapputigaq_atuutilik.접속번호());
        kasuqsimaniq 주인 = kapputigaq_atuutilik.받기();
        손님.대기시간(200); 주인.대기시간(200);
        검사.참인지(손님.연결됨() && !손님.닫힘(), "kasurli qanuilinganiq_atuutilik");
        검사.참인지(주인.접속번호() == 손님.지역접속번호(), "ilagijaujuq_atuutilik 접속번호");
        검사.참인지(손님.접속번호() == 주인.지역접속번호(), "tamaani_qinirvik 접속번호");
        입력흐름 입력 = 주인.입력(); 출력흐름 출력쪽 = 손님.출력();
        byte[] titiqqausiaq = 문자.부호화("한글 ingirrania_aulataup_atuutilik");
        출력쪽.titiraq(titiqqausiaq, 0, titiqqausiaq.length); 출력쪽.내보내기();
        byte[] 받은글 = new byte[titiqqausiaq.length];
        int 읽은수 = 0;
        while (읽은수 < 받은글.length) {
            int 더읽음 = 입력.읽기(받은글, 읽은수, 받은글.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 ini 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.suqquinarunniirlit_titiqqat(받은글), "한글 ingirrania_aulataup_atuutilik"), "부분 읽기와 titiraq");
        출력쪽.titiraq(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "array_atuutilik 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        주인.출력().titiraq(255);
        검사.참인지(손님.입력().읽기() == 255, "tukiniktiri_atuutilik 없는 한 byte_atuutilik");
        출력쪽.matuli();
        검사.참인지(손님.닫힘() && 입력.읽기() == -1, "닫기와 ini 끝");
        입력.matuli(); 검사.참인지(주인.닫힘(), "입력 ingirrania_aulataup_atuutilik matuli");
        손님.matuli(); 주인.matuli();
        kapputigaq_atuutilik.대기시간(15);
        boolean 시간제한 = false;
        try { kapputigaq_atuutilik.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 대기시간");
        kapputigaq_atuutilik.matuli(); 검사.참인지(kapputigaq_atuutilik.닫힘(), "수신창구 matuli");
        전문통로 받는곳 = 전문통로.matuirli(0), 보내는곳 = 전문통로.matuirli(0);
        받는곳.대기시간(200);
        보내는곳.nassiutili("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.matuli(); 받는곳.matuli();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 matuli");
        출력.titiraq_titikutaak("한국어 통신 nalunairli_1aacb54c: kasurli 전문 ingirrania_aulataup_atuutilik 시간제한 matuli");
    }
}
