// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Română.propriu.*;

public class 한국어예외시험 {
    static void valoare_implicită_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 excepție");
    }
    public static void main(String[] Argumente) throws I_O_excepție {
        try { throw new 대기시간초과예외("stare_de_așteptare 끝"); }
        catch (대기시간초과예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new adresa_LOOKUP_excepție("adresa eroare_VALUE"); }
        catch (I_O_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 파일없음예외("Fișier eroare_VALUE"); }
        catch (java.io.IOException eroare) { Rezultat.scriere_linie("표준 상위 excepție 호환"); }
        try { valoare_implicită_TIMEOUT(); }
        catch (대기시간초과예외 잘못잡힘) { Rezultat.scriere_linie("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Rezultat.scriere_linie("Română 예외의 독립된 Tip_zonă"); }
        try { Fișier.Citire("없는한글파일"); }
        catch (파일없음예외 eroare) { Rezultat.scriere_linie("Fișier eroare Română CONVERT_VALUE"); }
        try { 문자.analiza_întreg("숫자가아님"); }
        catch (숫자형식예외 eroare) { Rezultat.scriere_linie("cifră_VALUE eroare Română CONVERT_VALUE"); }
        try { 검사.참인지(false, "검사 eroare_VALUE"); }
        catch (nul_argument_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 배열범위예외("clip eroare_VALUE"); }
        catch (범위예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new NUL_referință_excepție("빈 referință"); }
        catch (java.lang.RuntimeException eroare) { Rezultat.scriere_linie("executa_comandă excepție 호환"); }
        try { throw new excepție("직접 정의한 설명"); }
        catch (excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new fir_Stare_excepție("fir_Stare_excepție"); }
        catch (fir_Stare_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 대기시간초과예외("대기시간초과예외"); }
        catch (대기시간초과예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new ARRAY_Store_eroare("ARRAY_Store_eroare"); }
        catch (ARRAY_Store_eroare eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new NUL_referință_excepție("NUL_referință_excepție"); }
        catch (NUL_referință_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new Stare_excepție("Stare_excepție"); }
        catch (Stare_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new executare_excepție("executare_excepție"); }
        catch (executare_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new excepție("excepție"); }
        catch (excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new I_O_excepție("I_O_excepție"); }
        catch (I_O_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new nul_argument_excepție("nul_argument_excepție"); }
        catch (nul_argument_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new adresa_LOOKUP_excepție("adresa_LOOKUP_excepție"); }
        catch (adresa_LOOKUP_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 eroare) { Rezultat.scriere_linie(eroare.설명()); }
        try { throw new Tip_cast_excepție("Tip_cast_excepție"); }
        catch (Tip_cast_excepție eroare) { Rezultat.scriere_linie(eroare.설명()); }
        Rezultat.scriere_linie("Română excepție Proces_VALUE_intrare 완료");
    }
}
