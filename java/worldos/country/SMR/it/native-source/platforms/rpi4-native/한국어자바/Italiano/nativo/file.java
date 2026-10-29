// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Italiano.nativo;
import java.io.FileInputStream;
import java.io.FileOutputStream;
/** 파일은 기존 spazio_utente 용어를 보존한다. Regolari_articolo 저장소는 재부팅 시 사라지는 RAM 파일이다. */
public final class file {
    private file() {}
    public static byte[] 바이트읽기(String Nome) throws I_O_eccezione {
        try {
        FileInputStream Stream_VALORE = new FileInputStream(Nome);
        try {
            byte[] 임시 = new byte[16384]; int numero = 0, VALORE;
            while ((VALORE = Stream_VALORE.read()) != -1) { if (numero == 임시.length) throw new I_O_eccezione("file Dimensione 제한"); 임시[numero++] = (byte)VALORE; }
            byte[] risultato = new byte[numero]; System.arraycopy(임시, 0, risultato, 0, numero); return risultato;
        } finally { Stream_VALORE.close(); }
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static void scrivere_byte_VALORE(String Nome, byte[] Contenuto_VALORE) throws I_O_eccezione {
        try {
        FileOutputStream Stream_VALORE = new FileOutputStream(Nome);
        try { for (int Loop_INDICE = 0; Loop_INDICE < Contenuto_VALORE.length; Loop_INDICE++) Stream_VALORE.write(Contenuto_VALORE[Loop_INDICE] & 255); } finally { Stream_VALORE.close(); }
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static String Lettura(String Nome) throws I_O_eccezione {
        try { return 문자.decifrare_dati(바이트읽기(Nome));
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
    public static void Scrittura(String Nome, String Contenuto_VALORE) throws I_O_eccezione {
        try { scrivere_byte_VALORE(Nome, 문자.codificare(Contenuto_VALORE));
        } catch (java.io.IOException errore) { throw CONVERTI_eccezione.I_O(errore); }
        catch (RuntimeException errore) { throw CONVERTI_eccezione.Esegui_comando(errore); }
    }
}
