// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import norsk.eget.*;

public class 한국어예외시험 {
    static void standard_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 unntak");
    }
    public static void main(String[] Argumenter) throws I_U_unntak {
        try { throw new vent_TIMEOUT_unntak("ventende_tilstand 끝"); }
        catch (vent_TIMEOUT_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new e_post_Oppslag_unntak("e_post feil_VERDI"); }
        catch (I_U_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 파일없음예외("Fil feil_VERDI"); }
        catch (java.io.IOException feil) { Utgang.skrive_linje("표준 상위 unntak 호환"); }
        try { standard_TIMEOUT(); }
        catch (vent_TIMEOUT_unntak 잘못잡힘) { Utgang.skrive_linje("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Utgang.skrive_linje("norsk 예외의 독립된 Type_område"); }
        try { Fil.Les("없는한글파일"); }
        catch (파일없음예외 feil) { Utgang.skrive_linje("Fil feil norsk KONVERTER_VERDI"); }
        try { 문자.dele_opp_heltall("숫자가아님"); }
        catch (nummer_format_feil feil) { Utgang.skrive_linje("siffer_VERDI feil norsk KONVERTER_VERDI"); }
        try { 검사.참인지(false, "검사 feil_VERDI"); }
        catch (ugyldig_argument_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 배열범위예외("klippe feil_VERDI"); }
        catch (범위예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new NULL_referere_unntak("빈 referere"); }
        catch (java.lang.RuntimeException feil) { Utgang.skrive_linje("Utfør_kommando unntak 호환"); }
        try { throw new unntak("직접 정의한 설명"); }
        catch (unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new tråd_status_unntak("tråd_status_unntak"); }
        catch (tråd_status_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new vent_TIMEOUT_unntak("vent_TIMEOUT_unntak"); }
        catch (vent_TIMEOUT_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new MATRISE_Store_feil("MATRISE_Store_feil"); }
        catch (MATRISE_Store_feil feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new NULL_referere_unntak("NULL_referere_unntak"); }
        catch (NULL_referere_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new status_unntak("status_unntak"); }
        catch (status_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new nummer_format_feil("nummer_format_feil"); }
        catch (nummer_format_feil feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new kjøring_unntak("kjøring_unntak"); }
        catch (kjøring_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new unntak("unntak"); }
        catch (unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new I_U_unntak("I_U_unntak"); }
        catch (I_U_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new ugyldig_argument_unntak("ugyldig_argument_unntak"); }
        catch (ugyldig_argument_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new e_post_Oppslag_unntak("e_post_Oppslag_unntak"); }
        catch (e_post_Oppslag_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 feil) { Utgang.skrive_linje(feil.설명()); }
        try { throw new Type_strømme_unntak("Type_strømme_unntak"); }
        catch (Type_strømme_unntak feil) { Utgang.skrive_linje(feil.설명()); }
        Utgang.skrive_linje("norsk unntak Prosess_VERDI_oppføring 완료");
    }
}
