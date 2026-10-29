// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Botswana.JBwaOS.setsamaisadifaele;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 faele 저장소의 관리 모델이다. */
public final class setsamaisadifaele {
    static final class 열린파일 {
        final byte[] tshedimosetso;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] tshedimosetso) {
            this.tshedimosetso = tshedimosetso;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String leina, byte[] tshedimosetso) {
        파일들.put(정규이름(leina), Arrays.copyOf(tshedimosetso, tshedimosetso.length));
    }

    열린파일 bula(String leina) {
        byte[] tshedimosetso = 파일들.get(정규이름(leina));
        if (tshedimosetso == null) {
            return null;
        }
        return new 열린파일(tshedimosetso);
    }

    public boolean 존재함(String leina) {
        return 파일들.containsKey(정규이름(leina));
    }

    public faele_tshedimosetso msinfo32_exe(String leina) {
        byte[] tshedimosetso = 파일들.get(정규이름(leina));
        if (tshedimosetso == null) {
            return null;
        }
        return new faele_tshedimosetso(tshedimosetso.length, 0100444);
    }

    private String 정규이름(String leina) {
        if (leina == null) {
            throw new NullPointerException("faele 이름이 없습니다.");
        }
        String 결과 = leina.startsWith("/") ? leina.substring(1) : leina;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
