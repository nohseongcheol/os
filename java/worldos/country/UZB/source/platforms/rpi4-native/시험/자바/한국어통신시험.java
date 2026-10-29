// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws I_O_istisno {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        aloqa mehmon_VALUE = 연결통신.Ochish("127.0.0.1", port_VALUE.접속번호());
        aloqa egasi_identifikator = port_VALUE.받기();
        mehmon_VALUE.TANAFFUS(200); egasi_identifikator.TANAFFUS(200);
        검사.참인지(mehmon_VALUE.연결됨() && !mehmon_VALUE.닫힘(), "Ulanish holat_VALUE_e10195a1");
        검사.참인지(egasi_identifikator.접속번호() == mehmon_VALUE.지역접속번호(), "bir_rangli_VALUE 접속번호");
        검사.참인지(mehmon_VALUE.접속번호() == egasi_identifikator.지역접속번호(), "mahalliy_soha 접속번호");
        입력흐름 입력 = egasi_identifikator.입력(); 출력흐름 출력쪽 = mehmon_VALUE.출력();
        byte[] xabar = 문자.부호화("한글 oqim_VALUE");
        출력쪽.Yozish(xabar, 0, xabar.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[xabar.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Oʻqish(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fayl 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.shifrsizlantirish_ma_lumotlar(RECEIVED_SMS), "한글 oqim_VALUE"), "부분 읽기와 Yozish");
        출력쪽.Yozish(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Oʻqish(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Oʻqish");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Oʻqish();
        검사.참인지(두바이트[1] == 18, "나머지 Oʻqish");
        egasi_identifikator.출력().Yozish(255);
        검사.참인지(mehmon_VALUE.입력().Oʻqish() == 255, "kodlash_VALUE 없는 한 bayt_VALUE");
        출력쪽.Yopish();
        검사.참인지(mehmon_VALUE.닫힘() && 입력.Oʻqish() == -1, "닫기와 Fayl 끝");
        입력.Yopish(); 검사.참인지(egasi_identifikator.닫힘(), "입력 oqim_VALUE Yopish");
        mehmon_VALUE.Yopish(); egasi_identifikator.Yopish();
        port_VALUE.TANAFFUS(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (bir_daqiqa_TANAFFUS_istisno 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TANAFFUS");
        port_VALUE.Yopish(); 검사.참인지(port_VALUE.닫힘(), "수신창구 Yopish");
        전문통로 받는곳 = 전문통로.Ochish(0), 보내는곳 = 전문통로.Ochish(0);
        받는곳.TANAFFUS(200);
        보내는곳.yuborish("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Yopish(); 받는곳.Yopish();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Yopish");
        출력.yozmoq_satr("한국어 통신 tasdiqlamoq: Ulanish 전문 oqim_VALUE 시간제한 Yopish");
    }
}
