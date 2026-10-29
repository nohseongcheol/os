// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Hollanda.JNldOS.dosya_sistemi;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Okuma 계층과 같은 Okuma 전용 dosya 저장소의 관리 모델이다. */
public final class dosya_sistemi {
    static final class 열린파일 {
        final byte[] veri;
        int konum;
        int Başvuru_BAĞ_DEĞ_SAY = 1;

        열린파일(byte[] veri) {
            this.veri = veri;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Ekleme_Dosya(String İsim, byte[] veri) {
        파일들.put(kurallı_ad(İsim), Arrays.copyOf(veri, veri.length));
    }

    열린파일 Aç(String İsim) {
        byte[] veri = 파일들.get(kurallı_ad(İsim));
        if (veri == null) {
            return null;
        }
        return new 열린파일(veri);
    }

    public boolean 존재함(String İsim) {
        return 파일들.containsKey(kurallı_ad(İsim));
    }

    public Dosya_bilgi msinfo32_exe(String İsim) {
        byte[] veri = 파일들.get(kurallı_ad(İsim));
        if (veri == null) {
            return null;
        }
        return new Dosya_bilgi(veri.length, 0100444);
    }

    private String kurallı_ad(String İsim) {
        if (İsim == null) {
            throw new NullPointerException("dosya 이름이 없습니다.");
        }
        String sonuç = İsim.startsWith("/") ? İsim.substring(1) : İsim;
        return sonuç.toUpperCase(Locale.ROOT);
    }
}
