// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Oʻzbekiston.JUzbOS.fayllar_tizimi;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Oʻqish 계층과 같은 Oʻqish 전용 Fayl 저장소의 관리 모델이다. */
public final class fayllar_tizimi {
    static final class 열린파일 {
        final byte[] ma_lumotlar;
        int Holati;
        int Ma_lumotnomalar_COUNT = 1;

        열린파일(byte[] ma_lumotlar) {
            this.ma_lumotlar = ma_lumotlar;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Nomi, byte[] ma_lumotlar) {
        파일들.put(정규이름(Nomi), Arrays.copyOf(ma_lumotlar, ma_lumotlar.length));
    }

    열린파일 Ochish(String Nomi) {
        byte[] ma_lumotlar = 파일들.get(정규이름(Nomi));
        if (ma_lumotlar == null) {
            return null;
        }
        return new 열린파일(ma_lumotlar);
    }

    public boolean 존재함(String Nomi) {
        return 파일들.containsKey(정규이름(Nomi));
    }

    public fayl_ma_lumot msinfo32_exe(String Nomi) {
        byte[] ma_lumotlar = 파일들.get(정규이름(Nomi));
        if (ma_lumotlar == null) {
            return null;
        }
        return new fayl_ma_lumot(ma_lumotlar.length, 0100444);
    }

    private String 정규이름(String Nomi) {
        if (Nomi == null) {
            throw new NullPointerException("Fayl 이름이 없습니다.");
        }
        String o_lchov = Nomi.startsWith("/") ? Nomi.substring(1) : Nomi;
        return o_lchov.toUpperCase(Locale.ROOT);
    }
}
