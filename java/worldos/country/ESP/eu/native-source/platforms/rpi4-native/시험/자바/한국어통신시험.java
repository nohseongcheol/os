// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Euskara.자체.*;

/** 동일 바이트코드를 OpenJDK와 자체 JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumentuak) throws S_I_salbuespen {
        수신창구 ataka_balio = 연결통신.수신열기(0);
        konexio gonbidatu_balio = 연결통신.Ireki("127.0.0.1", ataka_balio.ataka_zenbaki());
        konexio jabe_identifikatzaile = ataka_balio.받기();
        gonbidatu_balio.DENBORA_MUGA(200); jabe_identifikatzaile.DENBORA_MUGA(200);
        검사.참인지(gonbidatu_balio.연결됨() && !gonbidatu_balio.닫힘(), "Konektatu Egoera_balio");
        검사.참인지(jabe_identifikatzaile.ataka_zenbaki() == gonbidatu_balio.lokal_ataka_zenbaki(), "pareko_balio ataka_zenbaki");
        검사.참인지(gonbidatu_balio.ataka_zenbaki() == jabe_identifikatzaile.lokal_ataka_zenbaki(), "lokal_esparru ataka_zenbaki");
        입력흐름 입력 = jabe_identifikatzaile.입력(); 출력흐름 출력쪽 = gonbidatu_balio.Irteera();
        byte[] mezu = 문자.부호화("한글 Stream_balio");
        출력쪽.Idatzi(mezu, 0, mezu.length); 출력쪽.내보내기();
        byte[] RECEIVED_SMS = new byte[mezu.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Irakurri(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fitxategia 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.desenkriptatu_datuak(RECEIVED_SMS), "한글 Stream_balio"), "부분 읽기와 Idatzi");
        출력쪽.Idatzi(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Irakurri(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "matrize_balio Irakurri");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Irakurri();
        검사.참인지(두바이트[1] == 18, "나머지 Irakurri");
        jabe_identifikatzaile.Irteera().Idatzi(255);
        검사.참인지(gonbidatu_balio.입력().Irakurri() == 255, "kodeketa_balio 없는 한 byte_balio");
        출력쪽.Itxi();
        검사.참인지(gonbidatu_balio.닫힘() && 입력.Irakurri() == -1, "닫기와 Fitxategia 끝");
        입력.Itxi(); 검사.참인지(jabe_identifikatzaile.닫힘(), "입력 Stream_balio Itxi");
        gonbidatu_balio.Itxi(); jabe_identifikatzaile.Itxi();
        ataka_balio.DENBORA_MUGA(15);
        boolean 시간제한 = false;
        try { ataka_balio.받기(); } catch (itxaron_DENBORA_MUGA_salbuespen 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "수신 DENBORA_MUGA");
        ataka_balio.Itxi(); 검사.참인지(ataka_balio.닫힘(), "수신창구 Itxi");
        전문통로 받는곳 = 전문통로.Ireki(0), 보내는곳 = 전문통로.Ireki(0);
        받는곳.DENBORA_MUGA(200);
        보내는곳.bidali("127.0.0.1", 받는곳.ataka_zenbaki(), "전문 한글");
        검사.참인지(문자.같음(받는곳.받기(), "전문 한글"), "전문 송수신");
        보내는곳.Itxi(); 받는곳.Itxi();
        검사.참인지(보내는곳.닫힘() && 받는곳.닫힘(), "전문 Itxi");
        Irteera.idatzi_lerro("Euskara 통신 egiaztatu: Konektatu 전문 Stream_balio 시간제한 Itxi");
    }
}
