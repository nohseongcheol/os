// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Català.propi.*;

public class 한국어예외시험 {
    static void valor_per_defecte_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 excepció");
    }
    public static void main(String[] 인수) throws E_S_excepció {
        try { throw new Espera_TIMEOUT_excepció("Espera_Estat 끝"); }
        catch (Espera_TIMEOUT_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new ADREÇA_Cerca_excepció("Adreça error_VALOR"); }
        catch (E_S_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 파일없음예외("Fitxer error_VALOR"); }
        catch (java.io.IOException s_ha_produït_un_error) { Sortida.escriure_línia("표준 상위 excepció 호환"); }
        try { valor_per_defecte_TIMEOUT(); }
        catch (Espera_TIMEOUT_excepció 잘못잡힘) { Sortida.escriure_línia("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { Sortida.escriure_línia("Català 예외의 독립된 TIPUS_Categoria"); }
        try { Fitxer.Lectura("없는한글파일"); }
        catch (파일없음예외 s_ha_produït_un_error) { Sortida.escriure_línia("Fitxer s_ha_produït_un_error Català CONVERT_VALOR"); }
        try { 문자.정수읽기("숫자가아님"); }
        catch (숫자형식예외 s_ha_produït_un_error) { Sortida.escriure_línia("dígit_VALOR s_ha_produït_un_error Català CONVERT_VALOR"); }
        try { 검사.참인지(false, "검사 error_VALOR"); }
        catch (invàlid_arg_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 배열범위예외("clip error_VALOR"); }
        catch (범위예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new NUL_Referència_excepció("빈 Referència"); }
        catch (java.lang.RuntimeException s_ha_produït_un_error) { Sortida.escriure_línia("Executa_ordre excepció 호환"); }
        try { throw new excepció("직접 정의한 설명"); }
        catch (excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new fil_Estat_excepció("fil_Estat_excepció"); }
        catch (fil_Estat_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new Espera_TIMEOUT_excepció("Espera_TIMEOUT_excepció"); }
        catch (Espera_TIMEOUT_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new MATRIU_Store_error("MATRIU_Store_error"); }
        catch (MATRIU_Store_error s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new NUL_Referència_excepció("NUL_Referència_excepció"); }
        catch (NUL_Referència_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new Estat_excepció("Estat_excepció"); }
        catch (Estat_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 숫자형식예외("숫자형식예외"); }
        catch (숫자형식예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 실행예외("실행예외"); }
        catch (실행예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new excepció("excepció"); }
        catch (excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new E_S_excepció("E_S_excepció"); }
        catch (E_S_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new invàlid_arg_excepció("invàlid_arg_excepció"); }
        catch (invàlid_arg_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new ADREÇA_Cerca_excepció("ADREÇA_Cerca_excepció"); }
        catch (ADREÇA_Cerca_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 통신예외("통신예외"); }
        catch (통신예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        try { throw new TIPUS_conversió_excepció("TIPUS_conversió_excepció"); }
        catch (TIPUS_conversió_excepció s_ha_produït_un_error) { Sortida.escriure_línia(s_ha_produït_un_error.설명()); }
        Sortida.escriure_línia("Català excepció Procés_VALOR_introducció 완료");
    }
}
