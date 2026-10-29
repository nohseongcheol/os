// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws 입출력예외 {
        수신창구 Port_VALUE = 연결통신.수신열기(0);
        Verbindung Gaascht_VALUE = 연결통신.ariichten("127.0.0.1", Port_VALUE.접속번호());
        Verbindung Besëtzer_Identifikateur = Port_VALUE.받기();
        Gaascht_VALUE.TIMEOUT(200); Besëtzer_Identifikateur.TIMEOUT(200);
        검사.참인지(Gaascht_VALUE.연결됨() && !Gaascht_VALUE.닫힘(), "Verbannen Status_VALUE");
        검사.참인지(Besëtzer_Identifikateur.접속번호() == Gaascht_VALUE.지역접속번호(), "Peer_VALUE 접속번호");
        검사.참인지(Gaascht_VALUE.접속번호() == Besëtzer_Identifikateur.지역접속번호(), "lokal_Beräich 접속번호");
        입력흐름 입력 = Besëtzer_Identifikateur.입력(); 출력흐름 출력쪽 = Gaascht_VALUE.출력();
        byte[] Noriicht = 문자.부호화("한글 Stream_VALUE");
        출력쪽.schreiwen(Noriicht, 0, Noriicht.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[Noriicht.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.읽기(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fichier 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.decryptéieren_Daten(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 schreiwen");
        출력쪽.schreiwen(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.읽기(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE 읽기");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.읽기();
        검사.참인지(두바이트[1] == 18, "나머지 읽기");
        Besëtzer_Identifikateur.출력().schreiwen(255);
        검사.참인지(Gaascht_VALUE.입력().읽기() == 255, "Codéierung_VALUE 없는 한 Byte_VALUE");
        출력쪽.Clôture();
        검사.참인지(Gaascht_VALUE.닫힘() && 입력.읽기() == -1, "닫기와 Fichier 끝");
        입력.Clôture(); 검사.참인지(Besëtzer_Identifikateur.닫힘(), "입력 Stream_VALUE Clôture");
        Gaascht_VALUE.Clôture(); Besëtzer_Identifikateur.Clôture();
        Port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { Port_VALUE.받기(); } catch (대기시간초과예외 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        Port_VALUE.Clôture(); 검사.참인지(Port_VALUE.닫힘(), "수신창구 Clôture");
        전문통로 받는곳 = 전문통로.ariichten(0), 보내는곳 = 전문통로.ariichten(0);
        받는곳.TIMEOUT(200);
        보내는곳.mailen("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Clôture(); 받는곳.Clôture();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Clôture");
        출력.schreiwen_Zeil("한국어 통신 verifizéieren: Verbannen 전문 Stream_VALUE 시간제한 Clôture");
    }
}
