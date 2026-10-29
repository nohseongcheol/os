// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws I_O_uitsondering {
        수신창구 ombou_VALUE = 연결통신.수신열기(0);
        verbinding gas_VALUE = 연결통신.skep("127.0.0.1", ombou_VALUE.접속번호());
        verbinding eienaar_waarde = ombou_VALUE.받기();
        gas_VALUE.UITTELLING(200); eienaar_waarde.UITTELLING(200);
        검사.참인지(gas_VALUE.연결됨() && !gas_VALUE.닫힘(), "Koppel stand_VALUE");
        검사.참인지(eienaar_waarde.접속번호() == gas_VALUE.지역접속번호(), "portuur_VALUE 접속번호");
        검사.참인지(gas_VALUE.접속번호() == eienaar_waarde.지역접속번호(), "lokaal_bestek 접속번호");
        입력흐름 입력 = eienaar_waarde.입력(); 출력흐름 출력쪽 = gas_VALUE.Afvoer();
        byte[] e_pos_8c783e64 = 문자.부호화("한글 Stream_VALUE");
        출력쪽.Skryf(e_pos_8c783e64, 0, e_pos_8c783e64.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[e_pos_8c783e64.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Lees(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Lêer 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dekripteer_data(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 Skryf");
        출력쪽.Skryf(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Lees(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Lees");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Lees();
        검사.참인지(두바이트[1] == 18, "나머지 Lees");
        eienaar_waarde.Afvoer().Skryf(255);
        검사.참인지(gas_VALUE.입력().Lees() == 255, "enkodering_VALUE 없는 한 greep_VALUE");
        출력쪽.Sluit();
        검사.참인지(gas_VALUE.닫힘() && 입력.Lees() == -1, "닫기와 Lêer 끝");
        입력.Sluit(); 검사.참인지(eienaar_waarde.닫힘(), "입력 Stream_VALUE Sluit");
        gas_VALUE.Sluit(); eienaar_waarde.Sluit();
        ombou_VALUE.UITTELLING(15);
        boolean 시간제한 = false;
        try { ombou_VALUE.받기(); } catch (wag_UITTELLING_uitsondering 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 UITTELLING");
        ombou_VALUE.Sluit(); 검사.참인지(ombou_VALUE.닫힘(), "수신창구 Sluit");
        전문통로 받는곳 = 전문통로.skep(0), 보내는곳 = 전문통로.skep(0);
        받는곳.UITTELLING(200);
        보내는곳.e_pos("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Sluit(); 받는곳.Sluit();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Sluit");
        Afvoer.skryf_lyn("한국어 통신 verifieer: Koppel 전문 Stream_VALUE 시간제한 Sluit");
    }
}
