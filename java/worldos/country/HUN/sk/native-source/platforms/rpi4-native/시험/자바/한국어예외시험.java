// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Slovenský.vlastné.*;

public class 한국어예외시험 {
    static void predvolený_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 výnimka");
    }
    public static void main(String[] Argumenty) throws vstup_a_výstup_výnimka {
        try { throw new počkaj_TIMEOUT_výnimka("stav_čakania 끝"); }
        catch (počkaj_TIMEOUT_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new adresa_LOOKUP_výnimka("adresa zlyhanie_VALUE"); }
        catch (vstup_a_výstup_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 파일없음예외("Súbor zlyhanie_VALUE"); }
        catch (java.io.IOException chyba) { Výstup.zapísať_linka("표준 상위 výnimka 호환"); }
        try { predvolený_TIMEOUT(); }
        catch (počkaj_TIMEOUT_výnimka 잘못잡힘) { Výstup.zapísať_linka("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Výstup.zapísať_linka("Slovenský 예외의 독립된 Typ_oblasť"); }
        try { Súbor.Čítanie("없는한글파일"); }
        catch (파일없음예외 chyba) { Výstup.zapísať_linka("Súbor chyba Slovenský CONVERT_VALUE"); }
        try { 문자.analyzovať_celé_číslo("숫자가아님"); }
        catch (숫자형식예외 chyba) { Výstup.zapísať_linka("číslica_VALUE chyba Slovenský CONVERT_VALUE"); }
        try { 검사.참인지(false, "검사 zlyhanie_VALUE"); }
        catch (neplatné_argument_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 배열범위예외("klip zlyhanie_VALUE"); }
        catch (범위예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new NEPLATNÝ_zdroj_výnimka("빈 zdroj"); }
        catch (java.lang.RuntimeException chyba) { Výstup.zapísať_linka("Vykonať_príkaz výnimka 호환"); }
        try { throw new výnimka("직접 정의한 설명"); }
        catch (výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new vlákno_Stav_výnimka("vlákno_Stav_výnimka"); }
        catch (vlákno_Stav_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new počkaj_TIMEOUT_výnimka("počkaj_TIMEOUT_výnimka"); }
        catch (počkaj_TIMEOUT_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new pole_Store_zlyhanie("pole_Store_zlyhanie"); }
        catch (pole_Store_zlyhanie chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new NEPLATNÝ_zdroj_výnimka("NEPLATNÝ_zdroj_výnimka"); }
        catch (NEPLATNÝ_zdroj_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new Stav_výnimka("Stav_výnimka"); }
        catch (Stav_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new výnimka("výnimka"); }
        catch (výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new vstup_a_výstup_výnimka("vstup_a_výstup_výnimka"); }
        catch (vstup_a_výstup_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new neplatné_argument_výnimka("neplatné_argument_výnimka"); }
        catch (neplatné_argument_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new adresa_LOOKUP_výnimka("adresa_LOOKUP_výnimka"); }
        catch (adresa_LOOKUP_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 chyba) { Výstup.zapísať_linka(chyba.설명()); }
        try { throw new Typ_vysielať_výnimka("Typ_vysielať_výnimka"); }
        catch (Typ_vysielať_výnimka chyba) { Výstup.zapísať_linka(chyba.설명()); }
        Výstup.zapísať_linka("Slovenský výnimka Proces_VALUE_položka 완료");
    }
}
