// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.skrárkerfi;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Lestur 계층과 같은 Lestur 전용 Skrá 저장소의 관리 모델이다. */
public final class skrárkerfi {
    static final class 열린파일 {
        final byte[] gögn;
        int Staðsetning;
        int tilvísun_COUNT = 1;

        열린파일(byte[] gögn) {
            this.gögn = gögn;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Heiti, byte[] gögn) {
        파일들.put(정규이름(Heiti), Arrays.copyOf(gögn, gögn.length));
    }

    열린파일 Opna(String Heiti) {
        byte[] gögn = 파일들.get(정규이름(Heiti));
        if (gögn == null) {
            return null;
        }
        return new 열린파일(gögn);
    }

    public boolean 존재함(String Heiti) {
        return 파일들.containsKey(정규이름(Heiti));
    }

    public skrá_uppl msinfo32_exe(String Heiti) {
        byte[] gögn = 파일들.get(정규이름(Heiti));
        if (gögn == null) {
            return null;
        }
        return new skrá_uppl(gögn.length, 0100444);
    }

    private String 정규이름(String Heiti) {
        if (Heiti == null) {
            throw new NullPointerException("Skrá 이름이 없습니다.");
        }
        String NIÐURSTAÐA = Heiti.startsWith("/") ? Heiti.substring(1) : Heiti;
        return NIÐURSTAÐA.toUpperCase(Locale.ROOT);
    }
}
