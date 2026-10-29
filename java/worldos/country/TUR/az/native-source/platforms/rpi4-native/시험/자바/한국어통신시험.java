// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] 인수) throws giriş_çıxış_istisna {
        수신창구 port_VALUE = 연결통신.수신열기(0);
        qoşulma qonaq_VALUE = 연결통신.Aç("127.0.0.1", port_VALUE.접속번호());
        qoşulma sahib_identifikator = port_VALUE.받기();
        qonaq_VALUE.FASİLƏ(200); sahib_identifikator.FASİLƏ(200);
        검사.참인지(qonaq_VALUE.연결됨() && !qonaq_VALUE.닫힘(), "Bağlan vəziyyət_VALUE");
        검사.참인지(sahib_identifikator.접속번호() == qonaq_VALUE.지역접속번호(), "eynisəviyyəli_VALUE 접속번호");
        검사.참인지(qonaq_VALUE.접속번호() == sahib_identifikator.지역접속번호(), "lokal_miqyas 접속번호");
        입력흐름 입력 = sahib_identifikator.입력(); 출력흐름 출력쪽 = qonaq_VALUE.출력();
        byte[] mesaj = 문자.부호화("한글 axın_VALUE");
        출력쪽.Yazma(mesaj, 0, mesaj.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[mesaj.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Oxuma(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 FAYL 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.şifr_açmaq_verilənlər(RECEIVED_SMS), "한글 axın_VALUE"), "부분 읽기와 Yazma");
        출력쪽.Yazma(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Oxuma(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Oxuma");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Oxuma();
        검사.참인지(두바이트[1] == 18, "나머지 Oxuma");
        sahib_identifikator.출력().Yazma(255);
        검사.참인지(qonaq_VALUE.입력().Oxuma() == 255, "kodlaşdırma_VALUE 없는 한 bayt_VALUE");
        출력쪽.Bağla();
        검사.참인지(qonaq_VALUE.닫힘() && 입력.Oxuma() == -1, "닫기와 FAYL 끝");
        입력.Bağla(); 검사.참인지(sahib_identifikator.닫힘(), "입력 axın_VALUE Bağla");
        qonaq_VALUE.Bağla(); sahib_identifikator.Bağla();
        port_VALUE.FASİLƏ(15);
        boolean 시간제한 = false;
        try { port_VALUE.받기(); } catch (gözlə_FASİLƏ_istisna 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 FASİLƏ");
        port_VALUE.Bağla(); 검사.참인지(port_VALUE.닫힘(), "수신창구 Bağla");
        전문통로 받는곳 = 전문통로.Aç(0), 보내는곳 = 전문통로.Aç(0);
        받는곳.FASİLƏ(200);
        보내는곳.göndərmək("127.0.0.1", 받는곳.접속번호(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Bağla(); 받는곳.Bağla();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Bağla");
        출력.yazmaq_xətt("한국어 통신 yoxlamaq: Bağlan 전문 axın_VALUE 시간제한 Bağla");
    }
}
