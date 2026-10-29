// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bosna_i_Hercegovina.JBihOS.fajl_sistem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Čitaj 계층과 같은 Čitaj 전용 Fajl 저장소의 관리 모델이다. */
public final class fajl_sistem {
    static final class 열린파일 {
        final byte[] podaci;
        int Pozicija;
        int Reference_COUNT = 1;

        열린파일(byte[] podaci) {
            this.podaci = podaci;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Naziv, byte[] podaci) {
        파일들.put(정규이름(Naziv), Arrays.copyOf(podaci, podaci.length));
    }

    열린파일 Otvori(String Naziv) {
        byte[] podaci = 파일들.get(정규이름(Naziv));
        if (podaci == null) {
            return null;
        }
        return new 열린파일(podaci);
    }

    public boolean 존재함(String Naziv) {
        return 파일들.containsKey(정규이름(Naziv));
    }

    public fajl_informacija msinfo32_exe(String Naziv) {
        byte[] podaci = 파일들.get(정규이름(Naziv));
        if (podaci == null) {
            return null;
        }
        return new fajl_informacija(podaci.length, 0100444);
    }

    private String 정규이름(String Naziv) {
        if (Naziv == null) {
            throw new NullPointerException("Fajl 이름이 없습니다.");
        }
        String mjera = Naziv.startsWith("/") ? Naziv.substring(1) : Naziv;
        return mjera.toUpperCase(Locale.ROOT);
    }
}
