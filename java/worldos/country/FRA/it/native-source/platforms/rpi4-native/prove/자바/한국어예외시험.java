// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.nativo.*;

public class 한국어예외시험 {
    static void impostazione_predefinita_TIMEOUT() throws java.io.IOException {
        throw new java.net.SocketTimeoutException("원래 eccezione");
    }
    public static void main(String[] argomenti) throws I_O_eccezione {
        try { throw new aspetta_TIMEOUT_eccezione("stato_di_attesa 끝"); }
        catch (aspetta_TIMEOUT_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new e_mail_CERCA_eccezione("e_mail errore_VALORE"); }
        catch (I_O_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new 파일없음예외("file errore_VALORE"); }
        catch (java.io.IOException errore) { uscitaTesto.scrivere_riga("표준 상위 eccezione 호환"); }
        try { impostazione_predefinita_TIMEOUT(); }
        catch (aspetta_TIMEOUT_eccezione 잘못잡힘) { uscitaTesto.scrivere_riga("잘못된 alternativa_nome"); }
        catch (java.io.IOException 원래오류) { uscitaTesto.scrivere_riga("Italiano 예외의 독립된 TIPO_area"); }
        try { file.Lettura("없는한글파일"); }
        catch (파일없음예외 errore) { uscitaTesto.scrivere_riga("file errore Italiano CONVERTI_VALORE"); }
        try { 문자.analizzare_intero("숫자가아님"); }
        catch (numero_formato_errore errore) { uscitaTesto.scrivere_riga("cifra_VALORE errore Italiano CONVERTI_VALORE"); }
        try { 검사.참인지(false, "검사 errore_VALORE"); }
        catch (non_valida_argomento_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new 배열범위예외("ritagliare errore_VALORE"); }
        catch (범위예외 errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new riferimento_Null_eccezione("빈 fonti"); }
        catch (java.lang.RuntimeException errore) { uscitaTesto.scrivere_riga("Esegui_comando eccezione 호환"); }
        try { throw new eccezione("직접 정의한 설명"); }
        catch (eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new thread_Stato_eccezione("thread_Stato_eccezione"); }
        catch (thread_Stato_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new aspetta_TIMEOUT_eccezione("aspetta_TIMEOUT_eccezione"); }
        catch (aspetta_TIMEOUT_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new 대기중단예외("대기중단예외"); }
        catch (대기중단예외 errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new 문자열범위예외("문자열범위예외"); }
        catch (문자열범위예외 errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new 배열범위예외("배열범위예외"); }
        catch (배열범위예외 errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new array_Store_errore("array_Store_errore"); }
        catch (array_Store_errore errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new 범위예외("범위예외"); }
        catch (범위예외 errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new riferimento_Null_eccezione("riferimento_Null_eccezione"); }
        catch (riferimento_Null_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new aritmetico_errore("aritmetico_errore"); }
        catch (aritmetico_errore errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new Stato_eccezione("Stato_eccezione"); }
        catch (Stato_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new numero_formato_errore("numero_formato_errore"); }
        catch (numero_formato_errore errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new esecuzione_eccezione("esecuzione_eccezione"); }
        catch (esecuzione_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new eccezione("eccezione"); }
        catch (eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new negativo_array_ridimensionare_errore("negativo_array_ridimensionare_errore"); }
        catch (negativo_array_ridimensionare_errore errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new I_O_eccezione("I_O_eccezione"); }
        catch (I_O_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new non_valida_argomento_eccezione("non_valida_argomento_eccezione"); }
        catch (non_valida_argomento_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new e_mail_CERCA_eccezione("e_mail_CERCA_eccezione"); }
        catch (e_mail_CERCA_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new comunicazione_eccezione("comunicazione_eccezione"); }
        catch (comunicazione_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new 파일없음예외("파일없음예외"); }
        catch (파일없음예외 errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        try { throw new TIPO_cast_eccezione("TIPO_cast_eccezione"); }
        catch (TIPO_cast_eccezione errore) { uscitaTesto.scrivere_riga(errore.설명()); }
        uscitaTesto.scrivere_riga("Italiano eccezione Processi_VALORE_voce 완료");
    }
}
