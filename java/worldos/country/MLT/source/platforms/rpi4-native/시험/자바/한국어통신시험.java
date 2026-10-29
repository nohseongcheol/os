// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Malti.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        konnessjoni mistieden_VALUE = 연결통신.fetaħ("127.0.0.1", port_VALUE.접속번호());
        konnessjoni propjetarju_identifikatur = port_VALUE.받기();
        mistieden_VALUE.TIMEOUT(200); propjetarju_identifikatur.TIMEOUT(200);
        검사.참인지(mistieden_VALUE.연결됨() && !mistieden_VALUE.닫힘(), "AQBAD stat_VALUE");
        검사.참인지(propjetarju_identifikatur.접속번호() == mistieden_VALUE.지역접속번호(), "peer_VALUE 접속번호");
        검사.참인지(mistieden_VALUE.접속번호() == propjetarju_identifikatur.지역접속번호(), "lokali_ambitu 접속번호");
        입력흐름 입력 = propjetarju_identifikatur.입력(); 출력흐름 출력쪽 = mistieden_VALUE.출력();
        byte[] messaġġ = 문자.부호화("한글 Stream_VALUE");
        출력쪽.kiteb(messaġġ, 0, messaġġ.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[messaġġ.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.읽기(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 fajl 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.ddeċifra_data(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 kiteb");
        출력쪽.kiteb(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        propjetarju_identifikatur.출력().kiteb(255);
        검사.참인지(mistieden_VALUE.입력().읽기() == 255, "kodifikar_VALUE 없는 한 byte_VALUE");
        출력쪽.agħlaq();
        검사.참인지(mistieden_VALUE.닫힘() && 입력.읽기() == -1, "닫기와 fajl 끝");
        입력.agħlaq(); 검사.참인지(propjetarju_identifikatur.닫힘(), "입력 Stream_VALUE agħlaq");
        mistieden_VALUE.agħlaq(); propjetarju_identifikatur.agħlaq();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        port_VALUE.agħlaq(); 검사.참인지(port_VALUE.닫힘(), "수신창구 agħlaq");
        전문통로 받는곳 = 전문통로.fetaħ(0), 보내는곳 = 전문통로.fetaħ(0);
        받는곳.TIMEOUT(200);
        보내는곳.bagħat("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.agħlaq(); 받는곳.agħlaq();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 agħlaq");
        출력.kiteb_linja("Malti 통신 vverifika: AQBAD 전문 Stream_VALUE 시간제한 agħlaq");
    }
}
