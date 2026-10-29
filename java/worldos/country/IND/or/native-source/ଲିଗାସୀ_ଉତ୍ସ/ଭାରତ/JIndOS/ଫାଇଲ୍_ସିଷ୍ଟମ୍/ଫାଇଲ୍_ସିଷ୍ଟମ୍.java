// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ଫାଇଲ୍_ସିଷ୍ଟମ୍;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT ପଢନ୍ତୁ 계층과 같은 ପଢନ୍ତୁ 전용 ଫାଇଲ 저장소의 관리 모델이다. */
public final class ଫାଇଲ୍_ସିଷ୍ଟମ୍ {
    static final class 열린파일 {
        final byte[] ଡାଟା;
        int ଅବସ୍ଥାନ;
        int 참조수 = 1;

        열린파일(byte[] ଡାଟା) {
            this.ଡାଟା = ଡାଟା;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ନାମ, byte[] ଡାଟା) {
        파일들.put(정규이름(ନାମ), Arrays.copyOf(ଡାଟା, ଡାଟା.length));
    }

    열린파일 ଖୋଲନ୍ତୁ(String ନାମ) {
        byte[] ଡାଟା = 파일들.get(정규이름(ନାମ));
        if (ଡାଟା == null) {
            return null;
        }
        return new 열린파일(ଡାଟା);
    }

    public boolean 존재함(String ନାମ) {
        return 파일들.containsKey(정규이름(ନାମ));
    }

    public ଫାଇଲ୍_ସୂଚନା ସିଷ୍ଟମ୍_ସୂଚନା(String ନାମ) {
        byte[] ଡାଟା = 파일들.get(정규이름(ନାମ));
        if (ଡାଟା == null) {
            return null;
        }
        return new ଫାଇଲ୍_ସୂଚନା(ଡାଟା.length, 0100444);
    }

    private String 정규이름(String ନାମ) {
        if (ନାମ == null) {
            throw new NullPointerException("ଫାଇଲ 이름이 없습니다.");
        }
        String ମାପ = ନାମ.startsWith("/") ? ନାମ.substring(1) : ନାମ;
        return ମାପ.toUpperCase(Locale.ROOT);
    }
}
