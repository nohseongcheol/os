// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.siostam_fhaidhlichean;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 faidhle 저장소의 관리 모델이다. */
public final class siostam_fhaidhlichean {
    static final class 열린파일 {
        final byte[] dàta;
        int suidhich;
        int fiosrachadh_COUNT = 1;

        열린파일(byte[] dàta) {
            this.dàta = dàta;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Ainm, byte[] dàta) {
        파일들.put(정규이름(Ainm), Arrays.copyOf(dàta, dàta.length));
    }

    열린파일 fosgail(String Ainm) {
        byte[] dàta = 파일들.get(정규이름(Ainm));
        if (dàta == null) {
            return null;
        }
        return new 열린파일(dàta);
    }

    public boolean 존재함(String Ainm) {
        return 파일들.containsKey(정규이름(Ainm));
    }

    public faidhle_fios msinfo32_exe(String Ainm) {
        byte[] dàta = 파일들.get(정규이름(Ainm));
        if (dàta == null) {
            return null;
        }
        return new faidhle_fios(dàta.length, 0100444);
    }

    private String 정규이름(String Ainm) {
        if (Ainm == null) {
            throw new NullPointerException("faidhle 이름이 없습니다.");
        }
        String tomhas = Ainm.startsWith("/") ? Ainm.substring(1) : Ainm;
        return tomhas.toUpperCase(Locale.ROOT);
    }
}
