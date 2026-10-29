// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Cymraeg.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws I_O_eithriad {
        수신창구 porth_VALUE = 연결통신.수신열기(0);
        cyswllt gwestai_VALUE = 연결통신.Agor("127.0.0.1", porth_VALUE.rhif_porth());
        cyswllt perchennog_dynodwr = porth_VALUE.받기();
        gwestai_VALUE.TIMEOUT(200); perchennog_dynodwr.TIMEOUT(200);
        검사.참인지(gwestai_VALUE.연결됨() && !gwestai_VALUE.닫힘(), "Cysylltu cyflwr_VALUE");
        검사.참인지(perchennog_dynodwr.rhif_porth() == gwestai_VALUE.lleol_rhif_porth(), "cymar_VALUE rhif_porth");
        검사.참인지(gwestai_VALUE.rhif_porth() == perchennog_dynodwr.lleol_rhif_porth(), "lleol_cwmpas rhif_porth");
        입력흐름 입력 = perchennog_dynodwr.입력(); 출력흐름 출력쪽 = gwestai_VALUE.Allbwn();
        byte[] neges = 문자.부호화("한글 ffrwd_VALUE");
        출력쪽.Ysgrifennu(neges, 0, neges.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[neges.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Darllen(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Ffeil 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dadgryptio_data(RECEIVED_SMS), "한글 ffrwd_VALUE"), "부분 읽기와 Ysgrifennu");
        출력쪽.Ysgrifennu(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Darllen(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARAE_VALUE Darllen");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Darllen();
        검사.참인지(두바이트[1] == 18, "나머지 Darllen");
        perchennog_dynodwr.Allbwn().Ysgrifennu(255);
        검사.참인지(gwestai_VALUE.입력().Darllen() == 255, "amgodio_VALUE 없는 한 beit_VALUE");
        출력쪽.Cau();
        검사.참인지(gwestai_VALUE.닫힘() && 입력.Darllen() == -1, "닫기와 Ffeil 끝");
        입력.Cau(); 검사.참인지(perchennog_dynodwr.닫힘(), "입력 ffrwd_VALUE Cau");
        gwestai_VALUE.Cau(); perchennog_dynodwr.Cau();
        porth_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { porth_VALUE.받기(); } catch (aros_TIMEOUT_eithriad 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        porth_VALUE.Cau(); 검사.참인지(porth_VALUE.닫힘(), "수신창구 Cau");
        전문통로 받는곳 = 전문통로.Agor(0), 보내는곳 = 전문통로.Agor(0);
        받는곳.TIMEOUT(200);
        보내는곳.anfon("127.0.0.1", 받는곳.rhif_porth(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Cau(); 받는곳.Cau();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Cau");
        Allbwn.ysgrifennu_llinell("Cymraeg 통신 dilysu: Cysylltu 전문 ffrwd_VALUE 시간제한 Cau");
    }
}
