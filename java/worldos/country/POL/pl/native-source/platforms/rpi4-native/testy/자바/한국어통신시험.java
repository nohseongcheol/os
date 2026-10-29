// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import polski.własny.*;

/** 동일 바이트코드를 OpenJDK와 własny JVM에서 실행하는 komunikacja 계약 testy. */
public class 한국어통신시험 {
    public static void main(String[] argumenty) throws We_Wy_wyjątek {
        odbierać_port port_WARTOŚĆ = połączenie_transport.수신열기(0);
        połączenie gość_WARTOŚĆ = połączenie_transport.Otwórz("127.0.0.1", port_WARTOŚĆ.numer_portu());
        połączenie właściciel_identyfikator = port_WARTOŚĆ.odbierać();
        gość_WARTOŚĆ.TIMEOUT(200); właściciel_identyfikator.TIMEOUT(200);
        검사.참인지(gość_WARTOŚĆ.연결됨() && !gość_WARTOŚĆ.systemy_informacyjne_zamknięta(), "Połącz Stan_WARTOŚĆ");
        검사.참인지(właściciel_identyfikator.numer_portu() == gość_WARTOŚĆ.lokalny_numer_portu(), "węzeł_równorzędny_WARTOŚĆ numer_portu");
        검사.참인지(gość_WARTOŚĆ.numer_portu() == właściciel_identyfikator.lokalny_numer_portu(), "lokalny_Scope numer_portu");
        strumień_wejściowy wejście_WARTOŚĆ = właściciel_identyfikator.wejście_WARTOŚĆ(); strumień_wyjściowy produkt_wyjściowy_strona = gość_WARTOŚĆ.pozycja_wyjścia();
        byte[] e_mail = 문자.kodować("한글 Stream_WARTOŚĆ");
        produkt_wyjściowy_strona.Zapis(e_mail, 0, e_mail.length); produkt_wyjściowy_strona.내보내기();
        byte[] KWOTA_WYKUP_SMS = new byte[e_mail.length];
        int 읽은수 = 0;
        while (읽은수 < KWOTA_WYKUP_SMS.length) {
            int 더읽음 = wejście_WARTOŚĆ.Odczyt(KWOTA_WYKUP_SMS, 읽은수, KWOTA_WYKUP_SMS.length - 읽은수);
            검사.참인지(더읽음 > 0, "예상하지 않은 nazwa_pliku 끝"); 읽은수 += 더읽음;
        }
        검사.참인지(문자.같음(문자.odszyfrować_dane(KWOTA_WYKUP_SMS), "한글 Stream_WARTOŚĆ"), "부분 읽기와 Zapis");
        produkt_wyjściowy_strona.Zapis(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = wejście_WARTOŚĆ.Odczyt(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "TABLICA_WARTOŚĆ Odczyt");
        if (첫읽기 == 1) 두바이트[1] = (byte)wejście_WARTOŚĆ.Odczyt();
        검사.참인지(두바이트[1] == 18, "나머지 Odczyt");
        właściciel_identyfikator.pozycja_wyjścia().Zapis(255);
        검사.참인지(gość_WARTOŚĆ.wejście_WARTOŚĆ().Odczyt() == 255, "Encoding_WARTOŚĆ 없는 한 bajt_WARTOŚĆ");
        produkt_wyjściowy_strona.Zamknięte();
        검사.참인지(gość_WARTOŚĆ.systemy_informacyjne_zamknięta() && wejście_WARTOŚĆ.Odczyt() == -1, "닫기와 nazwa_pliku 끝");
        wejście_WARTOŚĆ.Zamknięte(); 검사.참인지(właściciel_identyfikator.systemy_informacyjne_zamknięta(), "wejście_WARTOŚĆ Stream_WARTOŚĆ Zamknięte");
        gość_WARTOŚĆ.Zamknięte(); właściciel_identyfikator.Zamknięte();
        port_WARTOŚĆ.TIMEOUT(15);
        boolean wykonanie_TIMEOUT = false;
        try { port_WARTOŚĆ.odbierać(); } catch (chwileczkę_TIMEOUT_wyjątek 예상한오류) { wykonanie_TIMEOUT = true; }
        검사.참인지(wykonanie_TIMEOUT, "odbierać_WARTOŚĆ TIMEOUT");
        port_WARTOŚĆ.Zamknięte(); 검사.참인지(port_WARTOŚĆ.systemy_informacyjne_zamknięta(), "odbierać_port Zamknięte");
        datagram_Kanał 받는곳 = datagram_Kanał.Otwórz(0), 보내는곳 = datagram_Kanał.Otwórz(0);
        받는곳.TIMEOUT(200);
        보내는곳.wysłać("127.0.0.1", 받는곳.numer_portu(), "datagram 한글");
        검사.참인지(문자.같음(받는곳.odbierać(), "datagram 한글"), "datagram 송수신");
        보내는곳.Zamknięte(); 받는곳.Zamknięte();
        검사.참인지(보내는곳.systemy_informacyjne_zamknięta() && 받는곳.systemy_informacyjne_zamknięta(), "datagram Zamknięte");
        pozycja_wyjścia.zapis_linia("polski komunikacja 확인: Połącz datagram Stream_WARTOŚĆ wykonanie_TIMEOUT Zamknięte");
    }
}
