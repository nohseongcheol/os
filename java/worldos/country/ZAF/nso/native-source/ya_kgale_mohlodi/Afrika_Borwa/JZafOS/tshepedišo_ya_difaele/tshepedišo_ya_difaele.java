// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Borwa.JZafOS.tshepedišo_ya_difaele;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Bala 계층과 같은 Bala 전용 Faele 저장소의 관리 모델이다. */
public final class tshepedišo_ya_difaele {
    static final class 열린파일 {
        final byte[] data;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Leina, byte[] data) {
        파일들.put(정규이름(Leina), Arrays.copyOf(data, data.length));
    }

    열린파일 Bula(String Leina) {
        byte[] data = 파일들.get(정규이름(Leina));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Leina) {
        return 파일들.containsKey(정규이름(Leina));
    }

    public faele_tshedimošo msinfo32_exe(String Leina) {
        byte[] data = 파일들.get(정규이름(Leina));
        if (data == null) {
            return null;
        }
        return new faele_tshedimošo(data.length, 0100444);
    }

    private String 정규이름(String Leina) {
        if (Leina == null) {
            throw new NullPointerException("Faele 이름이 없습니다.");
        }
        String 결과 = Leina.startsWith("/") ? Leina.substring(1) : Leina;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
