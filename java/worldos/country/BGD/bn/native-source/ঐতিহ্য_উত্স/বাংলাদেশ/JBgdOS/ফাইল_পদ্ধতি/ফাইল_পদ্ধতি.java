// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package বাংলাদেশ.JBgdOS.ফাইল_পদ্ধতি;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT পড়া 계층과 같은 পড়া 전용 নথির_নাম 저장소의 관리 모델이다. */
public final class ফাইল_পদ্ধতি {
    static final class 열린파일 {
        final byte[] ডাটা;
        int অবস্থান;
        int 참조수 = 1;

        열린파일(byte[] ডাটা) {
            this.ডাটা = ডাটা;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String নাম, byte[] ডাটা) {
        파일들.put(정규이름(নাম), Arrays.copyOf(ডাটা, ডাটা.length));
    }

    열린파일 খুলুন(String নাম) {
        byte[] ডাটা = 파일들.get(정규이름(নাম));
        if (ডাটা == null) {
            return null;
        }
        return new 열린파일(ডাটা);
    }

    public boolean 존재함(String নাম) {
        return 파일들.containsKey(정규이름(নাম));
    }

    public ফাইল_তথ্য সিসটেম_তথ্য(String নাম) {
        byte[] ডাটা = 파일들.get(정규이름(নাম));
        if (ডাটা == null) {
            return null;
        }
        return new ফাইল_তথ্য(ডাটা.length, 0100444);
    }

    private String 정규이름(String নাম) {
        if (নাম == null) {
            throw new NullPointerException("নথির_নাম 이름이 없습니다.");
        }
        String পরিমাপ = নাম.startsWith("/") ? নাম.substring(1) : নাম;
        return পরিমাপ.toUpperCase(Locale.ROOT);
    }
}
