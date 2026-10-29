// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package افغانستان.JAfgOS.دوتنه_سېسټم;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT لوستل 계층과 같은 لوستل 전용 دوتنه 저장소의 관리 모델이다. */
public final class دوتنه_سېسټم {
    static final class 열린파일 {
        final byte[] اومتوک;
        int ځای;
        int 참조수 = 1;

        열린파일(byte[] اومتوک) {
            this.اومتوک = اومتوک;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String نوم, byte[] اومتوک) {
        파일들.put(정규이름(نوم), Arrays.copyOf(اومتوک, اومتوک.length));
    }

    열린파일 پرانيستل(String نوم) {
        byte[] اومتوک = 파일들.get(정규이름(نوم));
        if (اومتوک == null) {
            return null;
        }
        return new 열린파일(اومتوک);
    }

    public boolean 존재함(String نوم) {
        return 파일들.containsKey(정규이름(نوم));
    }

    public 파일정보 정보(String نوم) {
        byte[] اومتوک = 파일들.get(정규이름(نوم));
        if (اومتوک == null) {
            return null;
        }
        return new 파일정보(اومتوک.length, 0100444);
    }

    private String 정규이름(String نوم) {
        if (نوم == null) {
            throw new NullPointerException("دوتنه 이름이 없습니다.");
        }
        String 결과 = نوم.startsWith("/") ? نوم.substring(1) : نوم;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
