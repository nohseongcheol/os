// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Svenska.eget.*;

/** 동일 바이트코드를 OpenJDK와 eget JVM에서 실행하는 kommunikation 계약 tester. */
public class 한국어통신시험 {
    public static void main(String[] argument) throws indata_utleverans_fel {
        få_port port_värde = kontakt_transport.수신열기(0);
        kontakt gäst_värde = kontakt_transport.Öppna("127.0.0.1", port_värde.portnummer());
        kontakt ägare_identifierare = port_värde.få();
        gäst_värde.TIMEOUT(200); ägare_identifierare.TIMEOUT(200);
        검사.참인지(gäst_värde.연결됨() && !gäst_värde.informationsteknik_stängd(), "Anslut status_värde");
        검사.참인지(ägare_identifierare.portnummer() == gäst_värde.lokal_portnummer(), "peer_värde portnummer");
        검사.참인지(gäst_värde.portnummer() == ägare_identifierare.lokal_portnummer(), "lokal_scope portnummer");
        indataström indata_värde = ägare_identifierare.indata_värde(); utdataström utleverans_page = gäst_värde.utmatningsposition();
        byte[] dokument = 문자.koda("한글 flöde_värde");
        utleverans_page.Skriv(dokument, 0, dokument.length); utleverans_page.내보내기();
        byte[] BELOPP_SMS = new byte[dokument.length];
        int läsa_ANTAL = 0;
        while (läsa_ANTAL < BELOPP_SMS.length) {
            int 더읽음 = indata_värde.Läs(BELOPP_SMS, läsa_ANTAL, BELOPP_SMS.length - läsa_ANTAL);
            검사.참인지(더읽음 > 0, "예상하지 않은 filnamn 끝"); läsa_ANTAL += 더읽음;
        }
        검사.참인지(문자.같음(문자.avkryptera_data(BELOPP_SMS), "한글 flöde_värde"), "부분 읽기와 Skriv");
        utleverans_page.Skriv(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = indata_värde.Läs(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MATRIS_värde Läs");
        if (첫읽기 == 1) 두바이트[1] = (byte)indata_värde.Läs();
        검사.참인지(두바이트[1] == 18, "나머지 Läs");
        ägare_identifierare.utmatningsposition().Skriv(255);
        검사.참인지(gäst_värde.indata_värde().Läs() == 255, "kodning_värde 없는 한 byte_värde");
        utleverans_page.Stäng();
        검사.참인지(gäst_värde.informationsteknik_stängd() && indata_värde.Läs() == -1, "닫기와 filnamn 끝");
        indata_värde.Stäng(); 검사.참인지(ägare_identifierare.informationsteknik_stängd(), "indata_värde flöde_värde Stäng");
        gäst_värde.Stäng(); ägare_identifierare.Stäng();
        port_värde.TIMEOUT(15);
        boolean körning_TIMEOUT = false;
        try { port_värde.få(); } catch (vänta_TIMEOUT_fel 예상한오류) { körning_TIMEOUT = true; }
        검사.참인지(körning_TIMEOUT, "få_värde TIMEOUT");
        port_värde.Stäng(); 검사.참인지(port_värde.informationsteknik_stängd(), "få_port Stäng");
        datagram_Kanal 받는곳 = datagram_Kanal.Öppna(0), 보내는곳 = datagram_Kanal.Öppna(0);
        받는곳.TIMEOUT(200);
        보내는곳.skicka("127.0.0.1", 받는곳.portnummer(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.få(), "datagram 한글"), "datagram 송수신");
        보내는곳.Stäng(); 받는곳.Stäng();
        검사.참인지(보내는곳.informationsteknik_stängd() && 받는곳.informationsteknik_stängd(), "datagram Stäng");
        utmatningsposition.skriva_rad("Svenska kommunikation verifiera: Anslut datagram flöde_värde körning_TIMEOUT Stäng");
    }
}
