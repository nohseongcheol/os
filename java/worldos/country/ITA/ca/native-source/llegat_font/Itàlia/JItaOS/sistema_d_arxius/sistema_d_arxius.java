// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Itàlia.JItaOS.sistema_d_arxius;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Lectura 계층과 같은 Lectura 전용 Fitxer 저장소의 관리 모델이다. */
public final class sistema_d_arxius {
    static final class 열린파일 {
        final byte[] dades;
        int Posició;
        int Referència_COMPT = 1;

        열린파일(byte[] dades) {
            this.dades = dades;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Annexa_arxiu(String Nom, byte[] dades) {
        파일들.put(정규이름(Nom), Arrays.copyOf(dades, dades.length));
    }

    열린파일 Obre(String Nom) {
        byte[] dades = 파일들.get(정규이름(Nom));
        if (dades == null) {
            return null;
        }
        return new 열린파일(dades);
    }

    public boolean 존재함(String Nom) {
        return 파일들.containsKey(정규이름(Nom));
    }

    public arxiu_informació msinfo32_exe(String Nom) {
        byte[] dades = 파일들.get(정규이름(Nom));
        if (dades == null) {
            return null;
        }
        return new arxiu_informació(dades.length, 0100444);
    }

    private String 정규이름(String Nom) {
        if (Nom == null) {
            throw new NullPointerException("Fitxer 이름이 없습니다.");
        }
        String RESULTAT = Nom.startsWith("/") ? Nom.substring(1) : Nom;
        return RESULTAT.toUpperCase(Locale.ROOT);
    }
}
