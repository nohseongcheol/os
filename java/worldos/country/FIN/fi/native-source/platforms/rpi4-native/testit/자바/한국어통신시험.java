// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import suomi.oma.*;

/** 동일 바이트코드를 OpenJDK와 oma JVM에서 실행하는 통신 계약 testit. */
public class 한국어통신시험 {
    public static void main(String[] argumentit) throws I_O_poikkeus {
        saada_portti portti_ARVO = yhteys_välitys.수신열기(0);
        yhteys vieras_ARVO = yhteys_välitys.Avaa("127.0.0.1", portti_ARVO.portin_numero());
        yhteys omistaja_tunniste = portti_ARVO.saada();
        vieras_ARVO.AIKAKATKAISU(200); omistaja_tunniste.AIKAKATKAISU(200);
        검사.참인지(vieras_ARVO.연결됨() && !vieras_ARVO.tietojärjestelmät_suljettu(), "Yhdistä Tila_ARVO");
        검사.참인지(omistaja_tunniste.portin_numero() == vieras_ARVO.paikallinen_portin_numero(), "vertaissolmu_ARVO portin_numero");
        검사.참인지(vieras_ARVO.portin_numero() == omistaja_tunniste.paikallinen_portin_numero(), "paikallinen_laajuus portin_numero");
        syötevirta syöte_ARVO = omistaja_tunniste.syöte_ARVO(); tietovirta tulos_page = vieras_ARVO.tulostuspaikka();
        byte[] sanoma = 문자.koodata("한글 virta_ARVO");
        tulos_page.Kirjoitus(sanoma, 0, sanoma.length); tulos_page.내보내기();
        byte[] SAATU_HINTA_SMS = new byte[sanoma.length];
        int lukea_LASKE = 0;
        while (lukea_LASKE < SAATU_HINTA_SMS.length) {
            int 더읽음 = syöte_ARVO.Luku(SAATU_HINTA_SMS, lukea_LASKE, SAATU_HINTA_SMS.length - lukea_LASKE);
            검사.참인지(더읽음 > 0, "예상하지 않은 tiedoston_nimi 끝"); lukea_LASKE += 더읽음;
        }
        검사.참인지(문자.같음(문자.pura_salaus_data(SAATU_HINTA_SMS), "한글 virta_ARVO"), "부분 읽기와 Kirjoitus");
        tulos_page.Kirjoitus(new byte[] {17, 18});
        byte[] 두바이트 = new byte[2];
        int 첫읽기 = syöte_ARVO.Luku(두바이트);
        검사.참인지(첫읽기 > 0 && 두바이트[0] == 17, "MATRIISI_ARVO Luku");
        if (첫읽기 == 1) 두바이트[1] = (byte)syöte_ARVO.Luku();
        검사.참인지(두바이트[1] == 18, "나머지 Luku");
        omistaja_tunniste.tulostuspaikka().Kirjoitus(255);
        검사.참인지(vieras_ARVO.syöte_ARVO().Luku() == 255, "koodaus_ARVO 없는 한 tavu_ARVO");
        tulos_page.Sulje();
        검사.참인지(vieras_ARVO.tietojärjestelmät_suljettu() && syöte_ARVO.Luku() == -1, "닫기와 tiedoston_nimi 끝");
        syöte_ARVO.Sulje(); 검사.참인지(omistaja_tunniste.tietojärjestelmät_suljettu(), "syöte_ARVO virta_ARVO Sulje");
        vieras_ARVO.Sulje(); omistaja_tunniste.Sulje();
        portti_ARVO.AIKAKATKAISU(15);
        boolean suoritus_AIKAKATKAISU = false;
        try { portti_ARVO.saada(); } catch (odottaa_AIKAKATKAISU_poikkeus 예상한오류) { suoritus_AIKAKATKAISU = true; }
        검사.참인지(suoritus_AIKAKATKAISU, "saada_ARVO AIKAKATKAISU");
        portti_ARVO.Sulje(); 검사.참인지(portti_ARVO.tietojärjestelmät_suljettu(), "saada_portti Sulje");
        datagrammi_Media 받는곳 = datagrammi_Media.Avaa(0), 보내는곳 = datagrammi_Media.Avaa(0);
        받는곳.AIKAKATKAISU(200);
        보내는곳.lähettää("127.0.0.1", 받는곳.portin_numero(), "datagrammi 한글");
        검사.참인지(문자.같음(받는곳.saada(), "datagrammi 한글"), "datagrammi 송수신");
        보내는곳.Sulje(); 받는곳.Sulje();
        검사.참인지(보내는곳.tietojärjestelmät_suljettu() && 받는곳.tietojärjestelmät_suljettu(), "datagrammi Sulje");
        tulostuspaikka.kirjoitus_rivi("suomi 통신 tarkistaa: Yhdistä datagrammi virta_ARVO suoritus_AIKAKATKAISU Sulje");
    }
}
