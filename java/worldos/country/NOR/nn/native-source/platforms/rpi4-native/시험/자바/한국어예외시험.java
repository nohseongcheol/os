// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import 한국어.자체.*;

public class 한국어예외시험 {
    static void standard_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 unntak");
    }
    public static void main(String[] Argument) throws I_U_unntak {
        try { throw new vent_TIMEOUT_unntak("vent_status 끝"); }
        catch (vent_TIMEOUT_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new ADDRESS_LOOKUP_unntak("ADDRESS feil_VALUE"); }
        catch (I_U_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 파일없음예외("Fil feil_VALUE"); }
        catch (java.io.IOException FEIL) { Utdata.skrive_line("표준 상위 unntak 호환"); }
        try { standard_TIMEOUT(); }
        catch (vent_TIMEOUT_unntak 잘못잡힘) { Utdata.skrive_line("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Utdata.skrive_line("한국어 예외의 독립된 TYPE_kategori"); }
        try { Fil.Les("없는한글파일"); }
        catch (파일없음예외 FEIL) { Utdata.skrive_line("Fil FEIL 한국어 CONVERT_VALUE"); }
        try { 문자.dele_opp_heiltal("숫자가아님"); }
        catch (숫자형식예외 FEIL) { Utdata.skrive_line("siffer_VALUE FEIL 한국어 CONVERT_VALUE"); }
        try { 검사.참인지(false, "검사 feil_VALUE"); }
        catch (ugyldig_argument_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 배열범위예외("klipp feil_VALUE"); }
        catch (범위예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new NULL_Oppslagsverk_unntak("빈 Oppslagsverk"); }
        catch (java.lang.RuntimeException FEIL) { Utdata.skrive_line("Utfør_kommando unntak 호환"); }
        try { throw new unntak("직접 정의한 설명"); }
        catch (unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new tråd_status_unntak("tråd_status_unntak"); }
        catch (tråd_status_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new vent_TIMEOUT_unntak("vent_TIMEOUT_unntak"); }
        catch (vent_TIMEOUT_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new ARRAY_Store_feil("ARRAY_Store_feil"); }
        catch (ARRAY_Store_feil FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new NULL_Oppslagsverk_unntak("NULL_Oppslagsverk_unntak"); }
        catch (NULL_Oppslagsverk_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new status_unntak("status_unntak"); }
        catch (status_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new unntak("unntak"); }
        catch (unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new I_U_unntak("I_U_unntak"); }
        catch (I_U_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new ugyldig_argument_unntak("ugyldig_argument_unntak"); }
        catch (ugyldig_argument_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new ADDRESS_LOOKUP_unntak("ADDRESS_LOOKUP_unntak"); }
        catch (ADDRESS_LOOKUP_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 FEIL) { Utdata.skrive_line(FEIL.설명()); }
        try { throw new TYPE_strøyme_unntak("TYPE_strøyme_unntak"); }
        catch (TYPE_strøyme_unntak FEIL) { Utdata.skrive_line(FEIL.설명()); }
        Utdata.skrive_line("한국어 unntak Prosess_VALUE_oppføring 완료");
    }
}
