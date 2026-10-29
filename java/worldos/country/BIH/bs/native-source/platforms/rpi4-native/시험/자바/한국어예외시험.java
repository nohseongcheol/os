// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

public class 한국어예외시험 {
    static void zadano_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 izuzetak");
    }
    public static void main(String[] Argumenti) throws U_I_izuzetak {
        try { throw new čekaj_TIMEOUT_izuzetak("čekaj_stanje 끝"); }
        catch (čekaj_TIMEOUT_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new adresa_LOOKUP_izuzetak("adresa neuspjeh_VALUE"); }
        catch (U_I_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 파일없음예외("Fajl neuspjeh_VALUE"); }
        catch (java.io.IOException GRESKA) { Ispis.pisati_redak("표준 상위 izuzetak 호환"); }
        try { zadano_TIMEOUT(); }
        catch (čekaj_TIMEOUT_izuzetak 잘못잡힘) { Ispis.pisati_redak("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Ispis.pisati_redak("한국어 예외의 독립된 TYPE_oblast"); }
        try { Fajl.Čitaj("없는한글파일"); }
        catch (파일없음예외 GRESKA) { Ispis.pisati_redak("Fajl GRESKA 한국어 CONVERT_VALUE"); }
        try { 문자.raščlanjivati_cijeli_broj("숫자가아님"); }
        catch (숫자형식예외 GRESKA) { Ispis.pisati_redak("cifra_VALUE GRESKA 한국어 CONVERT_VALUE"); }
        try { 검사.참인지(false, "검사 neuspjeh_VALUE"); }
        catch (nevažeće_argument_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 배열범위예외("isječak neuspjeh_VALUE"); }
        catch (범위예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new NULL_Reference_izuzetak("빈 Reference"); }
        catch (java.lang.RuntimeException GRESKA) { Ispis.pisati_redak("Izvrši_komanda izuzetak 호환"); }
        try { throw new izuzetak("직접 정의한 설명"); }
        catch (izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new nit_stanje_izuzetak("nit_stanje_izuzetak"); }
        catch (nit_stanje_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new čekaj_TIMEOUT_izuzetak("čekaj_TIMEOUT_izuzetak"); }
        catch (čekaj_TIMEOUT_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new niz_Store_neuspjeh("niz_Store_neuspjeh"); }
        catch (niz_Store_neuspjeh GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new NULL_Reference_izuzetak("NULL_Reference_izuzetak"); }
        catch (NULL_Reference_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new stanje_izuzetak("stanje_izuzetak"); }
        catch (stanje_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new izuzetak("izuzetak"); }
        catch (izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new U_I_izuzetak("U_I_izuzetak"); }
        catch (U_I_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new nevažeće_argument_izuzetak("nevažeće_argument_izuzetak"); }
        catch (nevažeće_argument_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new adresa_LOOKUP_izuzetak("adresa_LOOKUP_izuzetak"); }
        catch (adresa_LOOKUP_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        try { throw new TYPE_Emitiranje_izuzetak("TYPE_Emitiranje_izuzetak"); }
        catch (TYPE_Emitiranje_izuzetak GRESKA) { Ispis.pisati_redak(GRESKA.설명()); }
        Ispis.pisati_redak("한국어 izuzetak proces_VALUE_unos 완료");
    }
}
