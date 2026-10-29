// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package እስራኤል.JIsrOS.ናይ_ፋይል_ስርዓት;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 ፋይል 저장소의 관리 모델이다. */
public final class ናይ_ፋይል_ስርዓት {
    static final class 열린파일 {
        final byte[] ሓበሬታ;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] ሓበሬታ) {
            this.ሓበሬታ = ሓበሬታ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ሽም, byte[] ሓበሬታ) {
        파일들.put(정규이름(ሽም), Arrays.copyOf(ሓበሬታ, ሓበሬታ.length));
    }

    열린파일 ክፈት(String ሽም) {
        byte[] ሓበሬታ = 파일들.get(정규이름(ሽም));
        if (ሓበሬታ == null) {
            return null;
        }
        return new 열린파일(ሓበሬታ);
    }

    public boolean 존재함(String ሽም) {
        return 파일들.containsKey(정규이름(ሽም));
    }

    public ፋይል_ሓበሬታ ናይ_ስርዓት_ሓበሬታ(String ሽም) {
        byte[] ሓበሬታ = 파일들.get(정규이름(ሽም));
        if (ሓበሬታ == null) {
            return null;
        }
        return new ፋይል_ሓበሬታ(ሓበሬታ.length, 0100444);
    }

    private String 정규이름(String ሽም) {
        if (ሽም == null) {
            throw new NullPointerException("ፋይል 이름이 없습니다.");
        }
        String 결과 = ሽም.startsWith("/") ? ሽም.substring(1) : ሽም;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
