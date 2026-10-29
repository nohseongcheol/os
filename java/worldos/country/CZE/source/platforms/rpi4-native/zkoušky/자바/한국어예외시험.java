// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import čeština.vlastní.*;

public class 한국어예외시험 {
    static void výchozí_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 výjimka");
    }
    public static void main(String[] argumenty) throws vstup_a_výstup_výjimka {
        try { throw new počkej_TIMEOUT_výjimka("čekací_stav 끝"); }
        catch (počkej_TIMEOUT_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new ODKAZ_VYHLEDAT_výjimka("Adresa selhání_HODNOTA"); }
        catch (vstup_a_výstup_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 파일없음예외("název_souboru selhání_HODNOTA"); }
        catch (java.io.IOException chyba) { výstupní_pozice.zápis_čára("표준 상위 výjimka 호환"); }
        try { výchozí_TIMEOUT(); }
        catch (počkej_TIMEOUT_výjimka 잘못잡힘) { výstupní_pozice.zápis_čára("잘못된 별칭"); }
        catch (java.io.IOException 원래오류) { výstupní_pozice.zápis_čára("čeština 예외의 독립된 TYP_oblast"); }
        try { název_souboru.Čtení("없는한글파일"); }
        catch (파일없음예외 chyba) { výstupní_pozice.zápis_čára("název_souboru chyba čeština CONVERT_HODNOTA"); }
        try { 문자.parsovat_integer("숫자가아님"); }
        catch (číslo_formát_selhání chyba) { výstupní_pozice.zápis_čára("číslice_HODNOTA chyba čeština CONVERT_HODNOTA"); }
        try { 검사.참인지(false, "검사 selhání_HODNOTA"); }
        catch (neplatný_argument_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 배열범위예외("oříznout selhání_HODNOTA"); }
        catch (범위예외 chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new nulový_odkaz_výjimka("빈 odkaz"); }
        catch (java.lang.RuntimeException chyba) { výstupní_pozice.zápis_čára("Provést_příkaz výjimka 호환"); }
        try { throw new výjimka("직접 정의한 설명"); }
        catch (výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new vlákno_Stav_výjimka("vlákno_Stav_výjimka"); }
        catch (vlákno_Stav_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new počkej_TIMEOUT_výjimka("počkej_TIMEOUT_výjimka"); }
        catch (počkej_TIMEOUT_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new pole_Store_selhání("pole_Store_selhání"); }
        catch (pole_Store_selhání chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new nulový_odkaz_výjimka("nulový_odkaz_výjimka"); }
        catch (nulový_odkaz_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 산술예외("산술예외"); }
        catch (산술예외 chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new Stav_výjimka("Stav_výjimka"); }
        catch (Stav_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new číslo_formát_selhání("číslo_formát_selhání"); }
        catch (číslo_formát_selhání chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new spuštění_výjimka("spuštění_výjimka"); }
        catch (spuštění_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new výjimka("výjimka"); }
        catch (výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 음수배열크기예외("음수배열크기예외"); }
        catch (음수배열크기예외 chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new vstup_a_výstup_výjimka("vstup_a_výstup_výjimka"); }
        catch (vstup_a_výstup_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new neplatný_argument_výjimka("neplatný_argument_výjimka"); }
        catch (neplatný_argument_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new ODKAZ_VYHLEDAT_výjimka("ODKAZ_VYHLEDAT_výjimka"); }
        catch (ODKAZ_VYHLEDAT_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new komunikace_výjimka("komunikace_výjimka"); }
        catch (komunikace_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        try { throw new TYP_převod_výjimka("TYP_převod_výjimka"); }
        catch (TYP_převod_výjimka chyba) { výstupní_pozice.zápis_čára(chyba.설명()); }
        výstupní_pozice.zápis_čára("čeština výjimka Proces_HODNOTA_položka 완료");
    }
}
