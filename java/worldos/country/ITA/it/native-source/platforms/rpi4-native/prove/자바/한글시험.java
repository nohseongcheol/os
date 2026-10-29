// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
import Italiano.nativo.문자;
import Italiano.nativo.file;
import Italiano.nativo.voce_elenco;
import Italiano.nativo.dizionario;
import Italiano.nativo.uscitaTesto;
public class 한글시험 {
    public static void main(String[] a) throws Exception {
        String messaggio_di_saluto_ae353e94 = "안녕하세요 · 日本語 · العربية · 😀";
        uscitaTesto.scrivere_riga(문자.decifrare_dati(문자.codificare(messaggio_di_saluto_ae353e94))); uscitaTesto.scrivere_numero(문자.punto_di_codice_CONTA_NUMERI("한글😀"));
        file.Scrittura("한글자료.txt", messaggio_di_saluto_ae353e94); uscitaTesto.scrivere_riga(file.Lettura("한글자료.txt"));
        voce_elenco 이름들 = new voce_elenco(); 이름들.더하기("가람"); 이름들.더하기("누리"); uscitaTesto.scrivere_riga(이름들.Lettura(1));
        dizionario 뜻 = new dizionario(); 뜻.넣기("가람", "강"); System.gc(); uscitaTesto.scrivere_riga(뜻.TROVA_voce("가람"));
        try { 문자.decifrare_dati(new byte[] {(byte)0xc0, (byte)0xaf}); } catch (IllegalArgumentException e) { uscitaTesto.scrivere_riga("UTF-8 errore rifiutare_VALORE"); }
        uscitaTesto.scrivere_riga("Italiano Catalogo 완료");
    }
}
