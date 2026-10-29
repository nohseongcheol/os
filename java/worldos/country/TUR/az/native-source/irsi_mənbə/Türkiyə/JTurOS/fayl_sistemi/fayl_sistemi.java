// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Türkiyə.JTurOS.fayl_sistemi;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Oxuma 계층과 같은 Oxuma 전용 FAYL 저장소의 관리 모델이다. */
public final class fayl_sistemi {
    static final class 열린파일 {
        final byte[] verilənlər;
        int yerinə_qoymaq;
        int İstinad_COUNT = 1;

        열린파일(byte[] verilənlər) {
            this.verilənlər = verilənlər;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Ad, byte[] verilənlər) {
        파일들.put(정규이름(Ad), Arrays.copyOf(verilənlər, verilənlər.length));
    }

    열린파일 Aç(String Ad) {
        byte[] verilənlər = 파일들.get(정규이름(Ad));
        if (verilənlər == null) {
            return null;
        }
        return new 열린파일(verilənlər);
    }

    public boolean 존재함(String Ad) {
        return 파일들.containsKey(정규이름(Ad));
    }

    public fayl_məlumat msinfo32_exe(String Ad) {
        byte[] verilənlər = 파일들.get(정규이름(Ad));
        if (verilənlər == null) {
            return null;
        }
        return new fayl_məlumat(verilənlər.length, 0100444);
    }

    private String 정규이름(String Ad) {
        if (Ad == null) {
            throw new NullPointerException("FAYL 이름이 없습니다.");
        }
        String ölçü = Ad.startsWith("/") ? Ad.substring(1) : Ad;
        return ölçü.toUpperCase(Locale.ROOT);
    }
}
