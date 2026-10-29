// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.eget.*;

/** 동일 바이트코드를 OpenJDK와 eget JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumenter) throws I_U_unntak {
        motta_port port_VERDI = kontakt_transport.수신열기(0);
        kontakt gjest_VERDI = kontakt_transport.Åpne("127.0.0.1", port_VERDI.portnummer());
        kontakt eier_identifikator = port_VERDI.motta();
        gjest_VERDI.TIMEOUT(200); eier_identifikator.TIMEOUT(200);
        검사.참인지(gjest_VERDI.연결됨() && !gjest_VERDI.informasjonssystemer_lukket(), "Koble_til status_VERDI");
        검사.참인지(eier_identifikator.portnummer() == gjest_VERDI.lokal_portnummer(), "node_VERDI_6a3b6fa7 portnummer");
        검사.참인지(gjest_VERDI.portnummer() == eier_identifikator.lokal_portnummer(), "lokal_Omfang portnummer");
        inndataflyt inndata_VERDI = eier_identifikator.inndata_VERDI(); utdataflyt produksjon_page = gjest_VERDI.Utgang();
        byte[] e_post_8c783e64 = 문자.부호화("한글 strøm_VERDI");
        produksjon_page.Skriv(e_post_8c783e64, 0, e_post_8c783e64.length); produksjon_page.내보내기();
        byte[] MOTTATT_AVKAST_SMS = new byte[e_post_8c783e64.length];
        int 읽은수 = 0;
        while (읽은수 < MOTTATT_AVKAST_SMS.length) {
            int 더읽음 = inndata_VERDI.Les(MOTTATT_AVKAST_SMS, 읽은수, MOTTATT_AVKAST_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fil 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dekryptere_data(MOTTATT_AVKAST_SMS), "한글 strøm_VERDI"), "부분 읽기와 Skriv");
        produksjon_page.Skriv(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = inndata_VERDI.Les(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MATRISE_VERDI Les");
        if (첫읽기 == 1) 두바이트[1] = (byte)inndata_VERDI.Les();
        검사.참인지(두바이트[1] == 18, "나머지 Les");
        eier_identifikator.Utgang().Skriv(255);
        검사.참인지(gjest_VERDI.inndata_VERDI().Les() == 255, "koding_VERDI 없는 한 byte_VERDI");
        produksjon_page.Lukk();
        검사.참인지(gjest_VERDI.informasjonssystemer_lukket() && inndata_VERDI.Les() == -1, "닫기와 Fil 끝");
        inndata_VERDI.Lukk(); 검사.참인지(eier_identifikator.informasjonssystemer_lukket(), "inndata_VERDI strøm_VERDI Lukk");
        gjest_VERDI.Lukk(); eier_identifikator.Lukk();
        port_VERDI.TIMEOUT(15);
        boolean kjøring_TIMEOUT = false;
        try { port_VERDI.motta(); } catch (vent_TIMEOUT_unntak 예상한오류) { kjøring_TIMEOUT = true; }
        검사.참인지(kjøring_TIMEOUT, "motta_VERDI TIMEOUT");
        port_VERDI.Lukk(); 검사.참인지(port_VERDI.informasjonssystemer_lukket(), "motta_port Lukk");
        datagram_Kanal 받는곳 = datagram_Kanal.Åpne(0), 보내는곳 = datagram_Kanal.Åpne(0);
        받는곳.TIMEOUT(200);
        보내는곳.sende("127.0.0.1", 받는곳.portnummer(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.motta(), "datagram 한글"), "datagram 송수신");
        보내는곳.Lukk(); 받는곳.Lukk();
        검사.참인지(보내는곳.informasjonssystemer_lukket() && 받는곳.informasjonssystemer_lukket(), "datagram Lukk");
        Utgang.skrive_linje("norsk 통신 bekrefte: Koble_til datagram strøm_VERDI kjøring_TIMEOUT Lukk");
    }
}
