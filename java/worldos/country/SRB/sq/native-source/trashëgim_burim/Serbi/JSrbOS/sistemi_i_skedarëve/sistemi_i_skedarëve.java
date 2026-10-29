// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Serbi.JSrbOS.sistemi_i_skedarëve;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Leximi 계층과 같은 Leximi 전용 Kartelë 저장소의 관리 모델이다. */
public final class sistemi_i_skedarëve {
    static final class 열린파일 {
        final byte[] të_dhëna;
        int Pozicioni;
        int Referencë_COUNT = 1;

        열린파일(byte[] të_dhëna) {
            this.të_dhëna = të_dhëna;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Emër, byte[] të_dhëna) {
        파일들.put(정규이름(Emër), Arrays.copyOf(të_dhëna, të_dhëna.length));
    }

    열린파일 Hap(String Emër) {
        byte[] të_dhëna = 파일들.get(정규이름(Emër));
        if (të_dhëna == null) {
            return null;
        }
        return new 열린파일(të_dhëna);
    }

    public boolean 존재함(String Emër) {
        return 파일들.containsKey(정규이름(Emër));
    }

    public skedar_informacion msinfo32_exe(String Emër) {
        byte[] të_dhëna = 파일들.get(정규이름(Emër));
        if (të_dhëna == null) {
            return null;
        }
        return new skedar_informacion(të_dhëna.length, 0100444);
    }

    private String 정규이름(String Emër) {
        if (Emër == null) {
            throw new NullPointerException("Kartelë 이름이 없습니다.");
        }
        String llogaritje = Emër.startsWith("/") ? Emër.substring(1) : Emër;
        return llogaritje.toUpperCase(Locale.ROOT);
    }
}
