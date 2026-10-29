// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

public class 한국어예외시험 {
    static void podrazumevana_vrednost_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 izuzetak");
    }
    public static void main(String[] 인수) throws U_I_izuzetak {
        try { throw new čekaj_TIMEOUT_izuzetak("stanje_čekanja 끝"); }
        catch (čekaj_TIMEOUT_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new adresa_LOOKUP_izuzetak("adresa otkazivanje_VALUE"); }
        catch (U_I_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 파일없음예외("Datoteka otkazivanje_VALUE"); }
        catch (java.io.IOException greška) { 출력.줄쓰기("표준 상위 izuzetak 호환"); }
        try { podrazumevana_vrednost_TIMEOUT(); }
        catch (čekaj_TIMEOUT_izuzetak 잘못잡힘) { 출력.줄쓰기("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { 출력.줄쓰기("한국어 예외의 독립된 tip_oblast"); }
        try { Datoteka.읽기("없는한글파일"); }
        catch (파일없음예외 greška) { 출력.줄쓰기("Datoteka greška 한국어 CONVERT_VALUE"); }
        try { 문자.raščlaniti_ceo_broj("숫자가아님"); }
        catch (숫자형식예외 greška) { 출력.줄쓰기("cifra_VALUE greška 한국어 CONVERT_VALUE"); }
        try { 검사.참인지(false, "검사 otkazivanje_VALUE"); }
        catch (nevažeći_argument_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 배열범위예외("klip otkazivanje_VALUE"); }
        catch (범위예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new NULL_referenca_izuzetak("빈 referenca"); }
        catch (java.lang.RuntimeException greška) { 출력.줄쓰기("Izvrši_komanda izuzetak 호환"); }
        try { throw new izuzetak("직접 정의한 설명"); }
        catch (izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new nit_Status_izuzetak("nit_Status_izuzetak"); }
        catch (nit_Status_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new čekaj_TIMEOUT_izuzetak("čekaj_TIMEOUT_izuzetak"); }
        catch (čekaj_TIMEOUT_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new niz_Store_otkazivanje("niz_Store_otkazivanje"); }
        catch (niz_Store_otkazivanje greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new NULL_referenca_izuzetak("NULL_referenca_izuzetak"); }
        catch (NULL_referenca_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new Status_izuzetak("Status_izuzetak"); }
        catch (Status_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new izuzetak("izuzetak"); }
        catch (izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new U_I_izuzetak("U_I_izuzetak"); }
        catch (U_I_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new nevažeći_argument_izuzetak("nevažeći_argument_izuzetak"); }
        catch (nevažeći_argument_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new adresa_LOOKUP_izuzetak("adresa_LOOKUP_izuzetak"); }
        catch (adresa_LOOKUP_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 greška) { 출력.줄쓰기(greška.설명()); }
        try { throw new tip_Emitovanje_izuzetak("tip_Emitovanje_izuzetak"); }
        catch (tip_Emitovanje_izuzetak greška) { 출력.줄쓰기(greška.설명()); }
        출력.줄쓰기("한국어 izuzetak Proces_VALUE_stavka 완료");
    }
}
