// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Slovensko.JSvkOS.systém_souborů;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Čtení 계층과 같은 Čtení 전용 název_souboru 저장소의 관리 모델이다. */
public final class systém_souborů {
    static final class 열린파일 {
        final byte[] data;
        int pozice;
        int odkaz_POČET = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Připojit_Soubor(String Název, byte[] data) {
        파일들.put(název_v_kanonickém_tvaru(Název), Arrays.copyOf(data, data.length));
    }

    열린파일 Otevřít(String Název) {
        byte[] data = 파일들.get(název_v_kanonickém_tvaru(Název));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Název) {
        return 파일들.containsKey(název_v_kanonickém_tvaru(Název));
    }

    public Soubor_informace Informace_o_systému(String Název) {
        byte[] data = 파일들.get(název_v_kanonickém_tvaru(Název));
        if (data == null) {
            return null;
        }
        return new Soubor_informace(data.length, 0100444);
    }

    private String název_v_kanonickém_tvaru(String Název) {
        if (Název == null) {
            throw new NullPointerException("název_souboru 이름이 없습니다.");
        }
        String VÝSLEDEK = Název.startsWith("/") ? Název.substring(1) : Název;
        return VÝSLEDEK.toUpperCase(Locale.ROOT);
    }
}
