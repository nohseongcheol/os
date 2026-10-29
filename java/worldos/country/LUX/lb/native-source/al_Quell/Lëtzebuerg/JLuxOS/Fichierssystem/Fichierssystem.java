// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Fichierssystem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 Fichier 저장소의 관리 모델이다. */
public final class Fichierssystem {
    static final class 열린파일 {
        final byte[] Daten;
        int positionéieren;
        int Referenzen_COUNT = 1;

        열린파일(byte[] Daten) {
            this.Daten = Daten;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Numm, byte[] Daten) {
        파일들.put(정규이름(Numm), Arrays.copyOf(Daten, Daten.length));
    }

    열린파일 ariichten(String Numm) {
        byte[] Daten = 파일들.get(정규이름(Numm));
        if (Daten == null) {
            return null;
        }
        return new 열린파일(Daten);
    }

    public boolean 존재함(String Numm) {
        return 파일들.containsKey(정규이름(Numm));
    }

    public Fichier_Info msinfo32_exe(String Numm) {
        byte[] Daten = 파일들.get(정규이름(Numm));
        if (Daten == null) {
            return null;
        }
        return new Fichier_Info(Daten.length, 0100444);
    }

    private String 정규이름(String Numm) {
        if (Numm == null) {
            throw new NullPointerException("Fichier 이름이 없습니다.");
        }
        String Mooss = Numm.startsWith("/") ? Numm.substring(1) : Numm;
        return Mooss.toUpperCase(Locale.ROOT);
    }
}
