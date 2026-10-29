// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumente) throws I_O_përjashtim {
        수신창구 portë_VALUE = 연결통신.수신열기(0);
        lidhje i_ftuar_VALUE = 연결통신.Hap("127.0.0.1", portë_VALUE.numri_i_portës());
        lidhje pronari_identifikues = portë_VALUE.받기();
        i_ftuar_VALUE.TIMEOUT(200); pronari_identifikues.TIMEOUT(200);
        검사.참인지(i_ftuar_VALUE.연결됨() && !i_ftuar_VALUE.닫힘(), "Lidhu status_VALUE");
        검사.참인지(pronari_identifikues.numri_i_portës() == i_ftuar_VALUE.lokal_numri_i_portës(), "homolog_VALUE numri_i_portës");
        검사.참인지(i_ftuar_VALUE.numri_i_portës() == pronari_identifikues.lokal_numri_i_portës(), "lokal_fushë numri_i_portës");
        입력흐름 입력 = pronari_identifikues.입력(); 출력흐름 출력쪽 = i_ftuar_VALUE.출력();
        byte[] email_8c783e64 = 문자.부호화("한글 Stream_VALUE");
        출력쪽.Shkrimi(email_8c783e64, 0, email_8c783e64.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[email_8c783e64.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Leximi(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Kartelë 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dekriptoj_të_dhëna(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 Shkrimi");
        출력쪽.Shkrimi(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Leximi(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Leximi");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Leximi();
        검사.참인지(두바이트[1] == 18, "나머지 Leximi");
        pronari_identifikues.출력().Shkrimi(255);
        검사.참인지(i_ftuar_VALUE.입력().Leximi() == 255, "enkodim_VALUE 없는 한 bajt_VALUE");
        출력쪽.Mbyll();
        검사.참인지(i_ftuar_VALUE.닫힘() && 입력.Leximi() == -1, "닫기와 Kartelë 끝");
        입력.Mbyll(); 검사.참인지(pronari_identifikues.닫힘(), "입력 Stream_VALUE Mbyll");
        i_ftuar_VALUE.Mbyll(); pronari_identifikues.Mbyll();
        portë_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { portë_VALUE.받기(); } catch (Prit_TIMEOUT_përjashtim 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        portë_VALUE.Mbyll(); 검사.참인지(portë_VALUE.닫힘(), "수신창구 Mbyll");
        전문통로 받는곳 = 전문통로.Hap(0), 보내는곳 = 전문통로.Hap(0);
        받는곳.TIMEOUT(200);
        보내는곳.dërgoj("127.0.0.1", 받는곳.numri_i_portës(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Mbyll(); 받는곳.Mbyll();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Mbyll");
        출력.shkruaj_linjë("한국어 통신 verifikoj: Lidhu 전문 Stream_VALUE 시간제한 Mbyll");
    }
}
