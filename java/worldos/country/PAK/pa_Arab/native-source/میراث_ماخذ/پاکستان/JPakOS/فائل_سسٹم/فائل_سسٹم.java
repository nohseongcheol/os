// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package پاکستان.JPakOS.فائل_سسٹم;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 فائل 저장소의 관리 모델이다. */
public final class فائل_سسٹم {
    static final class 열린파일 {
        final byte[] کوائف;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] کوائف) {
            this.کوائف = کوائف;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ناں, byte[] کوائف) {
        파일들.put(정규이름(ناں), Arrays.copyOf(کوائف, کوائف.length));
    }

    열린파일 بنڑاؤ(String ناں) {
        byte[] کوائف = 파일들.get(정규이름(ناں));
        if (کوائف == null) {
            return null;
        }
        return new 열린파일(کوائف);
    }

    public boolean 존재함(String ناں) {
        return 파일들.containsKey(정규이름(ناں));
    }

    public فائل_معلومات سسٹم_دی_معلومات(String ناں) {
        byte[] کوائف = 파일들.get(정규이름(ناں));
        if (کوائف == null) {
            return null;
        }
        return new فائل_معلومات(کوائف.length, 0100444);
    }

    private String 정규이름(String ناں) {
        if (ناں == null) {
            throw new NullPointerException("فائل 이름이 없습니다.");
        }
        String 결과 = ناں.startsWith("/") ? ناں.substring(1) : ناں;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
