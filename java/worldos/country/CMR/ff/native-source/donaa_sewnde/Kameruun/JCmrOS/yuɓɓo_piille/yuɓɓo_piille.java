// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Kameruun.JCmrOS.yuɓɓo_piille;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 fiilde 저장소의 관리 모델이다. */
public final class yuɓɓo_piille {
    static final class 열린파일 {
        final byte[] keɓe;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] keɓe) {
            this.keɓe = keɓe;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String innde, byte[] keɓe) {
        파일들.put(정규이름(innde), Arrays.copyOf(keɓe, keɓe.length));
    }

    열린파일 udditde(String innde) {
        byte[] keɓe = 파일들.get(정규이름(innde));
        if (keɓe == null) {
            return null;
        }
        return new 열린파일(keɓe);
    }

    public boolean 존재함(String innde) {
        return 파일들.containsKey(정규이름(innde));
    }

    public fiilde_kumpital msinfo32_exe(String innde) {
        byte[] keɓe = 파일들.get(정규이름(innde));
        if (keɓe == null) {
            return null;
        }
        return new fiilde_kumpital(keɓe.length, 0100444);
    }

    private String 정규이름(String innde) {
        if (innde == null) {
            throw new NullPointerException("fiilde 이름이 없습니다.");
        }
        String 결과 = innde.startsWith("/") ? innde.substring(1) : innde;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
