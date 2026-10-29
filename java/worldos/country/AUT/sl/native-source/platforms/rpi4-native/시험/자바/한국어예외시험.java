// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import slovenščina.lastno.*;

public class 한국어예외시험 {
    static void privzeto_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 izjema");
    }
    public static void main(String[] Argumenti) throws V_I_izjema {
        try { throw new počakaj_TIMEOUT_izjema("čakalno_stanje 끝"); }
        catch (počakaj_TIMEOUT_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new naslov_LOOKUP_izjema("naslov napaka_VALUE"); }
        catch (V_I_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 파일없음예외("Datoteka napaka_VALUE"); }
        catch (java.io.IOException NAPAKA) { Izpis.pisati_linija("표준 상위 izjema 호환"); }
        try { privzeto_TIMEOUT(); }
        catch (počakaj_TIMEOUT_izjema 잘못잡힘) { Izpis.pisati_linija("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Izpis.pisati_linija("slovenščina 예외의 독립된 Tip_območje"); }
        try { Datoteka.Branje("없는한글파일"); }
        catch (파일없음예외 NAPAKA) { Izpis.pisati_linija("Datoteka NAPAKA slovenščina CONVERT_VALUE"); }
        try { 문자.razčlenjevati_celo_število("숫자가아님"); }
        catch (숫자형식예외 NAPAKA) { Izpis.pisati_linija("številka_VALUE NAPAKA slovenščina CONVERT_VALUE"); }
        try { 검사.참인지(false, "검사 napaka_VALUE"); }
        catch (neveljaven_argument_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 배열범위예외("izrezek napaka_VALUE"); }
        catch (범위예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new NULL_Gradiva_izjema("빈 Gradiva"); }
        catch (java.lang.RuntimeException NAPAKA) { Izpis.pisati_linija("Izvedi_ukaz izjema 호환"); }
        try { throw new izjema("직접 정의한 설명"); }
        catch (izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new nit_stanje_izjema("nit_stanje_izjema"); }
        catch (nit_stanje_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new počakaj_TIMEOUT_izjema("počakaj_TIMEOUT_izjema"); }
        catch (počakaj_TIMEOUT_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new ARRAY_Store_napaka("ARRAY_Store_napaka"); }
        catch (ARRAY_Store_napaka NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new NULL_Gradiva_izjema("NULL_Gradiva_izjema"); }
        catch (NULL_Gradiva_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new stanje_izjema("stanje_izjema"); }
        catch (stanje_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new izjema("izjema"); }
        catch (izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new V_I_izjema("V_I_izjema"); }
        catch (V_I_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new neveljaven_argument_izjema("neveljaven_argument_izjema"); }
        catch (neveljaven_argument_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new naslov_LOOKUP_izjema("naslov_LOOKUP_izjema"); }
        catch (naslov_LOOKUP_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        try { throw new Tip_pretvorba_izjema("Tip_pretvorba_izjema"); }
        catch (Tip_pretvorba_izjema NAPAKA) { Izpis.pisati_linija(NAPAKA.설명()); }
        Izpis.pisati_linija("slovenščina izjema Proces_VALUE_vnos 완료");
    }
}
