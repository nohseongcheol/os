// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argument) throws I_U_unntak {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        kontakt gjest_VALUE = 연결통신.Opna("127.0.0.1", port_VALUE.portnummer());
        kontakt eigar_identifikator = port_VALUE.받기();
        gjest_VALUE.TIMEOUT(200); eigar_identifikator.TIMEOUT(200);
        검사.참인지(gjest_VALUE.연결됨() && !gjest_VALUE.닫힘(), "Kopla_til status_VALUE");
        검사.참인지(eigar_identifikator.portnummer() == gjest_VALUE.lokal_portnummer(), "node_VALUE_6a3b6fa7 portnummer");
        검사.참인지(gjest_VALUE.portnummer() == eigar_identifikator.lokal_portnummer(), "lokal_område portnummer");
        입력흐름 입력 = eigar_identifikator.입력(); 출력흐름 출력쪽 = gjest_VALUE.Utdata();
        byte[] melding = 문자.부호화("한글 Stream_VALUE");
        출력쪽.Skriv(melding, 0, melding.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[melding.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Les(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fil 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dekryptere_data(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 Skriv");
        출력쪽.Skriv(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Les(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Les");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Les();
        검사.참인지(두바이트[1] == 18, "나머지 Les");
        eigar_identifikator.Utdata().Skriv(255);
        검사.참인지(gjest_VALUE.입력().Les() == 255, "koding_VALUE 없는 한 byte_VALUE");
        출력쪽.Lukk();
        검사.참인지(gjest_VALUE.닫힘() && 입력.Les() == -1, "닫기와 Fil 끝");
        입력.Lukk(); 검사.참인지(eigar_identifikator.닫힘(), "입력 Stream_VALUE Lukk");
        gjest_VALUE.Lukk(); eigar_identifikator.Lukk();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (vent_TIMEOUT_unntak 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        port_VALUE.Lukk(); 검사.참인지(port_VALUE.닫힘(), "수신창구 Lukk");
        전문통로 받는곳 = 전문통로.Opna(0), 보내는곳 = 전문통로.Opna(0);
        받는곳.TIMEOUT(200);
        보내는곳.sende("127.0.0.1", 받는곳.portnummer(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Lukk(); 받는곳.Lukk();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Lukk");
        Utdata.skrive_line("한국어 통신 stadfeste: Kopla_til 전문 Stream_VALUE 시간제한 Lukk");
    }
}
