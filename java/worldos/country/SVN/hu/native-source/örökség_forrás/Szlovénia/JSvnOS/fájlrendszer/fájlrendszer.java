// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Szlovénia.JSvnOS.fájlrendszer;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Olvasás 계층과 같은 Olvasás 전용 Fájl 저장소의 관리 모델이다. */
public final class fájlrendszer {
    static final class 열린파일 {
        final byte[] adat;
        int Pozíció;
        int hivatkozik_DARAB = 1;

        열린파일(byte[] adat) {
            this.adat = adat;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void hozzáfűz_Fájl(String Név, byte[] adat) {
        파일들.put(kanonikus_név(Név), Arrays.copyOf(adat, adat.length));
    }

    열린파일 Megnyitás(String Név) {
        byte[] adat = 파일들.get(kanonikus_név(Név));
        if (adat == null) {
            return null;
        }
        return new 열린파일(adat);
    }

    public boolean 존재함(String Név) {
        return 파일들.containsKey(kanonikus_név(Név));
    }

    public Fájl_infó msinfo32_exe(String Név) {
        byte[] adat = 파일들.get(kanonikus_név(Név));
        if (adat == null) {
            return null;
        }
        return new Fájl_infó(adat.length, 0100444);
    }

    private String kanonikus_név(String Név) {
        if (Név == null) {
            throw new NullPointerException("Fájl 이름이 없습니다.");
        }
        String KR = Név.startsWith("/") ? Név.substring(1) : Név;
        return KR.toUpperCase(Locale.ROOT);
    }
}
