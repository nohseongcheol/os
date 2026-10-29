// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Nederlands.Eigen.*;

/** 동일 바이트코드를 OpenJDK와 Eigen JVM에서 실행하는 communicatie 계약 tests. */
public class 한국어통신시험 {
    public static void main(String[] argumenten) throws I_O_uitzondering {
        ontvangen_poort poort_WAARDE = verbinding_transport.수신열기(0);
        verbinding gast_WAARDE = verbinding_transport.Openen("127.0.0.1", poort_WAARDE.poortnummer());
        verbinding eigenaar_id = poort_WAARDE.ontvangen();
        gast_WAARDE.TIMEOUT(200); eigenaar_id.TIMEOUT(200);
        검사.참인지(gast_WAARDE.연결됨() && !gast_WAARDE.informatie_afgesloten(), "Verbinden Status_WAARDE");
        검사.참인지(eigenaar_id.poortnummer() == gast_WAARDE.lokaal_poortnummer(), "peer_WAARDE poortnummer");
        검사.참인지(gast_WAARDE.poortnummer() == eigenaar_id.lokaal_poortnummer(), "lokaal_scope poortnummer");
        invoerstroom invoer_WAARDE = eigenaar_id.invoer_WAARDE(); uitvoerstroom uitvoer_page = gast_WAARDE.tekstuitvoer();
        byte[] e_mail = 문자.coderen("한글 Stream_WAARDE");
        uitvoer_page.Schrijven(e_mail, 0, e_mail.length); uitvoer_page.내보내기();
        byte[] OPBRENGST_sms = new byte[e_mail.length];
        int 읽은수 = 0;
        while (읽은수 < OPBRENGST_sms.length) {
            int 더읽음 = invoer_WAARDE.Lezen(OPBRENGST_sms, 읽은수, OPBRENGST_sms.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 bestand 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.ontsleutelen_gegevens(OPBRENGST_sms), "한글 Stream_WAARDE"), "부분 읽기와 Schrijven");
        uitvoer_page.Schrijven(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = invoer_WAARDE.Lezen(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MATRIX_WAARDE Lezen");
        if (첫읽기 == 1) 두바이트[1] = (byte)invoer_WAARDE.Lezen();
        검사.참인지(두바이트[1] == 18, "나머지 Lezen");
        eigenaar_id.tekstuitvoer().Schrijven(255);
        검사.참인지(gast_WAARDE.invoer_WAARDE().Lezen() == 255, "Encoding_WAARDE 없는 한 byte_WAARDE");
        uitvoer_page.Sluiten();
        검사.참인지(gast_WAARDE.informatie_afgesloten() && invoer_WAARDE.Lezen() == -1, "닫기와 bestand 끝");
        invoer_WAARDE.Sluiten(); 검사.참인지(eigenaar_id.informatie_afgesloten(), "invoer_WAARDE Stream_WAARDE Sluiten");
        gast_WAARDE.Sluiten(); eigenaar_id.Sluiten();
        poort_WAARDE.TIMEOUT(15);
        boolean uitvoerbewerking_TIMEOUT = false;
        try { poort_WAARDE.ontvangen(); } catch (wachten_TIMEOUT_uitzondering 예상한오류) { uitvoerbewerking_TIMEOUT = true; }
        검사.참인지(uitvoerbewerking_TIMEOUT, "ontvangen_WAARDE TIMEOUT");
        poort_WAARDE.Sluiten(); 검사.참인지(poort_WAARDE.informatie_afgesloten(), "ontvangen_poort Sluiten");
        datagram_Kanaal 받는곳 = datagram_Kanaal.Openen(0), 보내는곳 = datagram_Kanaal.Openen(0);
        받는곳.TIMEOUT(200);
        보내는곳.e_mailen("127.0.0.1", 받는곳.poortnummer(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.ontvangen(), "datagram 한글"), "datagram 송수신");
        보내는곳.Sluiten(); 받는곳.Sluiten();
        검사.참인지(보내는곳.informatie_afgesloten() && 받는곳.informatie_afgesloten(), "datagram Sluiten");
        tekstuitvoer.schrijven_lijn("Nederlands communicatie bevestigen: Verbinden datagram Stream_WAARDE uitvoerbewerking_TIMEOUT Sluiten");
    }
}
