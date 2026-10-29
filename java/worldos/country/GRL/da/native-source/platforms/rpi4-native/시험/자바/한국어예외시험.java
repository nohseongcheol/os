// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Dansk.eget.*;

public class 한국어예외시험 {
    static void standard_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 undtagelse");
    }
    public static void main(String[] Argumenter) throws I_O_undtagelse {
        try { throw new vent_TIMEOUT_undtagelse("ventetilstand 끝"); }
        catch (vent_TIMEOUT_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new mail_Opslag_undtagelse("mail fejl_VÆRDI"); }
        catch (I_O_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 파일없음예외("Fil fejl_VÆRDI"); }
        catch (java.io.IOException fejl) { Udgang.skrive_linje("표준 상위 undtagelse 호환"); }
        try { standard_TIMEOUT(); }
        catch (vent_TIMEOUT_undtagelse 잘못잡힘) { Udgang.skrive_linje("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Udgang.skrive_linje("Dansk 예외의 독립된 Type_område"); }
        try { Fil.Læse("없는한글파일"); }
        catch (파일없음예외 fejl) { Udgang.skrive_linje("Fil fejl Dansk KONVERTER_VÆRDI"); }
        try { 문자.opdele_tekst_heltal("숫자가아님"); }
        catch (tal_format_fejl fejl) { Udgang.skrive_linje("ciffer_VÆRDI fejl Dansk KONVERTER_VÆRDI"); }
        try { 검사.참인지(false, "검사 fejl_VÆRDI"); }
        catch (ugyldig_argument_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 배열범위예외("klippe fejl_VÆRDI"); }
        catch (범위예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new NULL_referere_undtagelse("빈 referere"); }
        catch (java.lang.RuntimeException fejl) { Udgang.skrive_linje("Udfør_kommando undtagelse 호환"); }
        try { throw new undtagelse("직접 정의한 설명"); }
        catch (undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new tråd_status_undtagelse("tråd_status_undtagelse"); }
        catch (tråd_status_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new vent_TIMEOUT_undtagelse("vent_TIMEOUT_undtagelse"); }
        catch (vent_TIMEOUT_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new MATRIX_Store_fejl("MATRIX_Store_fejl"); }
        catch (MATRIX_Store_fejl fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new NULL_referere_undtagelse("NULL_referere_undtagelse"); }
        catch (NULL_referere_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new status_undtagelse("status_undtagelse"); }
        catch (status_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new tal_format_fejl("tal_format_fejl"); }
        catch (tal_format_fejl fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new udførelse_undtagelse("udførelse_undtagelse"); }
        catch (udførelse_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new undtagelse("undtagelse"); }
        catch (undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new I_O_undtagelse("I_O_undtagelse"); }
        catch (I_O_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new ugyldig_argument_undtagelse("ugyldig_argument_undtagelse"); }
        catch (ugyldig_argument_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new mail_Opslag_undtagelse("mail_Opslag_undtagelse"); }
        catch (mail_Opslag_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 fejl) { Udgang.skrive_linje(fejl.설명()); }
        try { throw new Type_Cast_undtagelse("Type_Cast_undtagelse"); }
        catch (Type_Cast_undtagelse fejl) { Udgang.skrive_linje(fejl.설명()); }
        Udgang.skrive_linje("Dansk undtagelse Proces_VÆRDI_post 완료");
    }
}
