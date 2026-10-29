// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.córas_comhad;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Léigh 계층과 같은 Léigh 전용 Comhad 저장소의 관리 모델이다. */
public final class córas_comhad {
    static final class 열린파일 {
        final byte[] sonraí;
        int suíomh;
        int Leabhair_thagartha_COUNT = 1;

        열린파일(byte[] sonraí) {
            this.sonraí = sonraí;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Ainm, byte[] sonraí) {
        파일들.put(정규이름(Ainm), Arrays.copyOf(sonraí, sonraí.length));
    }

    열린파일 Oscail(String Ainm) {
        byte[] sonraí = 파일들.get(정규이름(Ainm));
        if (sonraí == null) {
            return null;
        }
        return new 열린파일(sonraí);
    }

    public boolean 존재함(String Ainm) {
        return 파일들.containsKey(정규이름(Ainm));
    }

    public comhad_faisnéis msinfo32_exe(String Ainm) {
        byte[] sonraí = 파일들.get(정규이름(Ainm));
        if (sonraí == null) {
            return null;
        }
        return new comhad_faisnéis(sonraí.length, 0100444);
    }

    private String 정규이름(String Ainm) {
        if (Ainm == null) {
            throw new NullPointerException("Comhad 이름이 없습니다.");
        }
        String tomhas = Ainm.startsWith("/") ? Ainm.substring(1) : Ainm;
        return tomhas.toUpperCase(Locale.ROOT);
    }
}
