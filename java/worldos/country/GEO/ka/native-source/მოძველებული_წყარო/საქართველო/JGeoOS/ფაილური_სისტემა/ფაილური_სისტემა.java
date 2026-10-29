// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package საქართველო.JGeoOS.ფაილური_სისტემა;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT კითხვა 계층과 같은 კითხვა 전용 ფაილი 저장소의 관리 모델이다. */
public final class ფაილური_სისტემა {
    static final class 열린파일 {
        final byte[] მონაცემები;
        int პოზიცია;
        int 참조수 = 1;

        열린파일(byte[] მონაცემები) {
            this.მონაცემები = მონაცემები;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String სახელი, byte[] მონაცემები) {
        파일들.put(정규이름(სახელი), Arrays.copyOf(მონაცემები, მონაცემები.length));
    }

    열린파일 გახსნა(String სახელი) {
        byte[] მონაცემები = 파일들.get(정규이름(სახელი));
        if (მონაცემები == null) {
            return null;
        }
        return new 열린파일(მონაცემები);
    }

    public boolean 존재함(String სახელი) {
        return 파일들.containsKey(정규이름(სახელი));
    }

    public ფაილი_ინფო სისტემის_ინფორმაცია(String სახელი) {
        byte[] მონაცემები = 파일들.get(정규이름(სახელი));
        if (მონაცემები == null) {
            return null;
        }
        return new ფაილი_ინფო(მონაცემები.length, 0100444);
    }

    private String 정규이름(String სახელი) {
        if (სახელი == null) {
            throw new NullPointerException("ფაილი 이름이 없습니다.");
        }
        String გაზომვა = სახელი.startsWith("/") ? სახელი.substring(1) : სახელი;
        return გაზომვა.toUpperCase(Locale.ROOT);
    }
}
