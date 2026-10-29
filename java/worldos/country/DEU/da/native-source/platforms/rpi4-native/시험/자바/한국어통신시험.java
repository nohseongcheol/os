// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Dansk.eget.*;

/** 동일 바이트코드를 OpenJDK와 eget JVM에서 실행하는 통신 계약 시험. */
public class 한국어통신시험 {
    public static void main(String[] Argumenter) throws I_O_undtagelse {
        modtage_port port_VÆRDI = forbindelse_transport.수신열기(0);
        forbindelse gæst_VÆRDI = forbindelse_transport.Åbn("127.0.0.1", port_VÆRDI.portnummer());
        forbindelse ejer_identifikator = port_VÆRDI.modtage();
        gæst_VÆRDI.TIMEOUT(200); ejer_identifikator.TIMEOUT(200);
        검사.참인지(gæst_VÆRDI.연결됨() && !gæst_VÆRDI.it_lukket(), "Tilslut status_VÆRDI");
        검사.참인지(ejer_identifikator.portnummer() == gæst_VÆRDI.lokal_portnummer(), "peer_VÆRDI portnummer");
        검사.참인지(gæst_VÆRDI.portnummer() == ejer_identifikator.lokal_portnummer(), "lokal_Omfang portnummer");
        inputstream input_VÆRDI = ejer_identifikator.input_VÆRDI(); outputstream produktoutput_side = gæst_VÆRDI.Udgang();
        byte[] mail_8c783e64 = 문자.kode("한글 strøm_VÆRDI");
        produktoutput_side.Skrive(mail_8c783e64, 0, mail_8c783e64.length); produktoutput_side.내보내기();
        byte[] MODTAGET_VED_UDLØB_sms = new byte[mail_8c783e64.length];
        int 읽은수 = 0;
        while (읽은수 < MODTAGET_VED_UDLØB_sms.length) {
            int 더읽음 = input_VÆRDI.Læse(MODTAGET_VED_UDLØB_sms, 읽은수, MODTAGET_VED_UDLØB_sms.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 Fil 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.dekryptere_data(MODTAGET_VED_UDLØB_sms), "한글 strøm_VÆRDI"), "부분 읽기와 Skrive");
        produktoutput_side.Skrive(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = input_VÆRDI.Læse(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MATRIX_VÆRDI Læse");
        if (첫읽기 == 1) 두바이트[1] = (byte)input_VÆRDI.Læse();
        검사.참인지(두바이트[1] == 18, "나머지 Læse");
        ejer_identifikator.Udgang().Skrive(255);
        검사.참인지(gæst_VÆRDI.input_VÆRDI().Læse() == 255, "kodning_VÆRDI 없는 한 byte_VÆRDI");
        produktoutput_side.Luk();
        검사.참인지(gæst_VÆRDI.it_lukket() && input_VÆRDI.Læse() == -1, "닫기와 Fil 끝");
        input_VÆRDI.Luk(); 검사.참인지(ejer_identifikator.it_lukket(), "input_VÆRDI strøm_VÆRDI Luk");
        gæst_VÆRDI.Luk(); ejer_identifikator.Luk();
        port_VÆRDI.TIMEOUT(15);
        boolean udførelse_TIMEOUT = false;
        try { port_VÆRDI.modtage(); } catch (vent_TIMEOUT_undtagelse 예상한오류) { udførelse_TIMEOUT = true; }
        검사.참인지(udførelse_TIMEOUT, "modtage_VÆRDI TIMEOUT");
        port_VÆRDI.Luk(); 검사.참인지(port_VÆRDI.it_lukket(), "modtage_port Luk");
        datagram_Kanal 받는곳 = datagram_Kanal.Åbn(0), 보내는곳 = datagram_Kanal.Åbn(0);
        받는곳.TIMEOUT(200);
        보내는곳.maile("127.0.0.1", 받는곳.portnummer(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.modtage(), "datagram 한글"), "datagram 송수신");
        보내는곳.Luk(); 받는곳.Luk();
        검사.참인지(보내는곳.it_lukket() && 받는곳.it_lukket(), "datagram Luk");
        Udgang.skrive_linje("Dansk 통신 bekræfte: Tilslut datagram strøm_VÆRDI udførelse_TIMEOUT Luk");
    }
}
