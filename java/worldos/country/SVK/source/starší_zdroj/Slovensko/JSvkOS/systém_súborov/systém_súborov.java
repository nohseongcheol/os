// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.systém_súborov;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Čítanie 계층과 같은 Čítanie 전용 Súbor 저장소의 관리 모델이다. */
public final class systém_súborov {
    static final class 열린파일 {
        final byte[] údaje;
        int Pozícia;
        int zdroj_COUNT = 1;

        열린파일(byte[] údaje) {
            this.údaje = údaje;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Pripojiť_Súbor(String Názov, byte[] údaje) {
        파일들.put(kanonický_názov(Názov), Arrays.copyOf(údaje, údaje.length));
    }

    열린파일 Otvoriť(String Názov) {
        byte[] údaje = 파일들.get(kanonický_názov(Názov));
        if (údaje == null) {
            return null;
        }
        return new 열린파일(údaje);
    }

    public boolean 존재함(String Názov) {
        return 파일들.containsKey(kanonický_názov(Názov));
    }

    public Súbor_informácia Systémové_informácie(String Názov) {
        byte[] údaje = 파일들.get(kanonický_názov(Názov));
        if (údaje == null) {
            return null;
        }
        return new Súbor_informácia(údaje.length, 0100444);
    }

    private String kanonický_názov(String Názov) {
        if (Názov == null) {
            throw new NullPointerException("Súbor 이름이 없습니다.");
        }
        String KR = Názov.startsWith("/") ? Názov.substring(1) : Názov;
        return KR.toUpperCase(Locale.ROOT);
    }
}
