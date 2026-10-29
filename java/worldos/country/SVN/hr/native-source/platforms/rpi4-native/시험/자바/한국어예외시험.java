// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import hrvatski.vlastiti.*;

public class 한국어예외시험 {
    static void zadana_vrijednost_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 iznimka");
    }
    public static void main(String[] Argumenti) throws U_I_iznimka {
        try { throw new čekaj_TIMEOUT_iznimka("stanje_čekanja 끝"); }
        catch (čekaj_TIMEOUT_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new adresa_LOOKUP_iznimka("adresa kvar_VALUE"); }
        catch (U_I_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 파일없음예외("Datoteka kvar_VALUE"); }
        catch (java.io.IOException GREŠKA) { Izlaz.zapisivanje_red("표준 상위 iznimka 호환"); }
        try { zadana_vrijednost_TIMEOUT(); }
        catch (čekaj_TIMEOUT_iznimka 잘못잡힘) { Izlaz.zapisivanje_red("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Izlaz.zapisivanje_red("hrvatski 예외의 독립된 TYPE_područje"); }
        try { Datoteka.Čitaj("없는한글파일"); }
        catch (파일없음예외 GREŠKA) { Izlaz.zapisivanje_red("Datoteka GREŠKA hrvatski CONVERT_VALUE"); }
        try { 문자.rastavljati_cijeli_broj("숫자가아님"); }
        catch (숫자형식예외 GREŠKA) { Izlaz.zapisivanje_red("znamenka_VALUE GREŠKA hrvatski CONVERT_VALUE"); }
        try { 검사.참인지(false, "검사 kvar_VALUE"); }
        catch (nevaljan_argument_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 배열범위예외("isječak kvar_VALUE"); }
        catch (범위예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new NULL_Reference_iznimka("빈 Reference"); }
        catch (java.lang.RuntimeException GREŠKA) { Izlaz.zapisivanje_red("Izvrši_naredba iznimka 호환"); }
        try { throw new iznimka("직접 정의한 설명"); }
        catch (iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new nit_Stanje_iznimka("nit_Stanje_iznimka"); }
        catch (nit_Stanje_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new čekaj_TIMEOUT_iznimka("čekaj_TIMEOUT_iznimka"); }
        catch (čekaj_TIMEOUT_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new ARRAY_Store_kvar("ARRAY_Store_kvar"); }
        catch (ARRAY_Store_kvar GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new NULL_Reference_iznimka("NULL_Reference_iznimka"); }
        catch (NULL_Reference_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new Stanje_iznimka("Stanje_iznimka"); }
        catch (Stanje_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new iznimka("iznimka"); }
        catch (iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new U_I_iznimka("U_I_iznimka"); }
        catch (U_I_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new nevaljan_argument_iznimka("nevaljan_argument_iznimka"); }
        catch (nevaljan_argument_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new adresa_LOOKUP_iznimka("adresa_LOOKUP_iznimka"); }
        catch (adresa_LOOKUP_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        try { throw new TYPE_emitirati_iznimka("TYPE_emitirati_iznimka"); }
        catch (TYPE_emitirati_iznimka GREŠKA) { Izlaz.zapisivanje_red(GREŠKA.설명()); }
        Izlaz.zapisivanje_red("hrvatski iznimka Proces_VALUE_unos 완료");
    }
}
