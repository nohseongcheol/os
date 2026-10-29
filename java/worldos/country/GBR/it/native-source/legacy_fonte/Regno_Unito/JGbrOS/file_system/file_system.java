// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Regno_Unito.JGbrOS.file_system;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Lettura 계층과 같은 Lettura 전용 file 저장소의 관리 모델이다. */
public final class file_system {
    static final class 열린파일 {
        final byte[] dati;
        int posizione;
        int fonti_CONTA_NUMERI = 1;

        열린파일(byte[] dati) {
            this.dati = dati;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Aggiunta_File(String Nome, byte[] dati) {
        파일들.put(nome_canonico(Nome), Arrays.copyOf(dati, dati.length));
    }

    열린파일 Apri(String Nome) {
        byte[] dati = 파일들.get(nome_canonico(Nome));
        if (dati == null) {
            return null;
        }
        return new 열린파일(dati);
    }

    public boolean 존재함(String Nome) {
        return 파일들.containsKey(nome_canonico(Nome));
    }

    public File_info msinfo32_exe(String Nome) {
        byte[] dati = 파일들.get(nome_canonico(Nome));
        if (dati == null) {
            return null;
        }
        return new File_info(dati.length, 0100444);
    }

    private String nome_canonico(String Nome) {
        if (Nome == null) {
            throw new NullPointerException("file 이름이 없습니다.");
        }
        String risultato = Nome.startsWith("/") ? Nome.substring(1) : Nome;
        return risultato.toUpperCase(Locale.ROOT);
    }
}
