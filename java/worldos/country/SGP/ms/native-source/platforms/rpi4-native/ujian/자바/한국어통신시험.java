// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Melayu.Asli.*;

/** 동일 바이트코드를 OpenJDK와 Asli JVM에서 실행하는 통신 계약 ujian. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws I_O_pengecualian {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        hubungan tetamu_VALUE = 연결통신.Buka("127.0.0.1", port_VALUE.nombor_port());
        hubungan 주인 = port_VALUE.받기();
        tetamu_VALUE.TIMEOUT(200); 주인.TIMEOUT(200);
        검사.참인지(tetamu_VALUE.연결됨() && !tetamu_VALUE.닫힘(), "Sambung status_VALUE");
        검사.참인지(주인.nombor_port() == tetamu_VALUE.setempat_nombor_port(), "rakan_VALUE nombor_port");
        검사.참인지(tetamu_VALUE.nombor_port() == 주인.setempat_nombor_port(), "setempat_Skop nombor_port");
        strim_input 입력 = 주인.입력(); strim_output 출력쪽 = tetamu_VALUE.출력();
        byte[] e_mel_8c783e64 = 문자.부호화("한글 strim_VALUE");
        출력쪽.Tulis(e_mel_8c783e64, 0, e_mel_8c783e64.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[e_mel_8c783e64.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Baca(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fail 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.nyahsulit_data(RECEIVED_SMS), "한글 strim_VALUE"), "부분 읽기와 Tulis");
        출력쪽.Tulis(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Baca(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Baca");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Baca();
        검사.참인지(두바이트[1] == 18, "나머지 Baca");
        주인.출력().Tulis(255);
        검사.참인지(tetamu_VALUE.입력().Baca() == 255, "pengekodan_VALUE 없는 한 bait_VALUE");
        출력쪽.Tutup();
        검사.참인지(tetamu_VALUE.닫힘() && 입력.Baca() == -1, "닫기와 Fail 끝");
        입력.Tutup(); 검사.참인지(주인.닫힘(), "입력 strim_VALUE Tutup");
        tetamu_VALUE.Tutup(); 주인.Tutup();
        port_VALUE.TIMEOUT(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (tunggu_TIMEOUT_pengecualian 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 TIMEOUT");
        port_VALUE.Tutup(); 검사.참인지(port_VALUE.닫힘(), "수신창구 Tutup");
        전문통로 받는곳 = 전문통로.Buka(0), 보내는곳 = 전문통로.Buka(0);
        받는곳.TIMEOUT(200);
        보내는곳.e_mel_9aee63bd("127.0.0.1", 받는곳.nombor_port(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Tutup(); 받는곳.Tutup();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Tutup");
        출력.tulis_baris("Melayu 통신 tentu_sahkan: Sambung 전문 strim_VALUE 시간제한 Tutup");
    }
}
