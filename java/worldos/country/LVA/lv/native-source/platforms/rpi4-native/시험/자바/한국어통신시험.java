// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Latviešu.savs.*;

/** 동일 바이트코드를 OpenJDK와 savs JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Parametri) throws ievadizvade_izņēmums {
        saņemt_ports ports_VALUE = paziņa_transportēšana.수신열기(0);
        paziņa viesis_VALUE = paziņa_transportēšana.Atvērt("127.0.0.1", ports_VALUE.porta_numurs());
        paziņa īpašnieks_identifikators = ports_VALUE.saņemt();
        viesis_VALUE.NOILGUMS(200); īpašnieks_identifikators.NOILGUMS(200);
        검사.참인지(viesis_VALUE.연결됨() && !viesis_VALUE.informācijas_tehnoloģija_slēgts(), "Savienoties Statuss_VALUE");
        검사.참인지(īpašnieks_identifikators.porta_numurs() == viesis_VALUE.vietējs_porta_numurs(), "vienranga_VALUE porta_numurs");
        검사.참인지(viesis_VALUE.porta_numurs() == īpašnieks_identifikators.vietējs_porta_numurs(), "vietējs_Tvērums porta_numurs");
        ievades_straume 입력 = īpašnieks_identifikators.입력(); ražojums_Stream ražojums_lapa = viesis_VALUE.Izvade();
        byte[] ziņa = 문자.kodēt("한글 Stream_VALUE");
        ražojums_lapa.Rakstīt(ziņa, 0, ziņa.length); ražojums_lapa.내보내기();
        byte[] RECEIVED_SMS = new byte[ziņa.length];
        int 읽은수 = 0;
        while (읽은수 < RECEIVED_SMS.length) {
            int 더읽음 = 입력.Lasīt(RECEIVED_SMS, 읽은수, RECEIVED_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fails 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.atšifrēt_dati(RECEIVED_SMS), "한글 Stream_VALUE"), "부분 읽기와 Rakstīt");
        ražojums_lapa.Rakstīt(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = 입력.Lasīt(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "ARRAY_VALUE Lasīt");
        if (첫읽기 == 1) 두바이트[1] = (byte)입력.Lasīt();
        검사.참인지(두바이트[1] == 18, "나머지 Lasīt");
        īpašnieks_identifikators.Izvade().Rakstīt(255);
        검사.참인지(viesis_VALUE.입력().Lasīt() == 255, "kodēšana_VALUE 없는 한 byte_VALUE");
        ražojums_lapa.Aizvērt();
        검사.참인지(viesis_VALUE.informācijas_tehnoloģija_slēgts() && 입력.Lasīt() == -1, "닫기와 Fails 끝");
        입력.Aizvērt(); 검사.참인지(īpašnieks_identifikators.informācijas_tehnoloģija_slēgts(), "입력 Stream_VALUE Aizvērt");
        viesis_VALUE.Aizvērt(); īpašnieks_identifikators.Aizvērt();
        ports_VALUE.NOILGUMS(15);
        boolean 시간제한 = false;
        try { ports_VALUE.saņemt(); } catch (pagaidi_NOILGUMS_izņēmums 예상한오류) { 시간제한 = true; }
        검사.참인지(시간제한, "saņemt_VALUE NOILGUMS");
        ports_VALUE.Aizvērt(); 검사.참인지(ports_VALUE.informācijas_tehnoloģija_slēgts(), "saņemt_ports Aizvērt");
        datogramma_Kanāls 받는곳 = datogramma_Kanāls.Atvērt(0), 보내는곳 = datogramma_Kanāls.Atvērt(0);
        받는곳.NOILGUMS(200);
        보내는곳.sūtīt("127.0.0.1", 받는곳.porta_numurs(), "datogramma 한글");
        검사.참인지(문자.같음(받는곳.saņemt(), "datogramma 한글"), "datogramma 송수신");
        보내는곳.Aizvērt(); 받는곳.Aizvērt();
        검사.참인지(보내는곳.informācijas_tehnoloģija_slēgts() && 받는곳.informācijas_tehnoloģija_slēgts(), "datogramma Aizvērt");
        Izvade.rakstīšana_līnija("Latviešu 통신 verificēt: Savienoties datogramma Stream_VALUE 시간제한 Aizvērt");
    }
}
