// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ឯកសារនៃប្រព័ន្ធ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT អាន 계층과 같은 អាន 전용 ឯកសារ 저장소의 관리 모델이다. */
public final class ឯកសារនៃប្រព័ន្ធ {
    static final class 열린파일 {
        final byte[] ទិន្នន័យ;
        int កំណត់ទីតាំង;
        int 참조수 = 1;

        열린파일(byte[] ទិន្នន័យ) {
            this.ទិន្នន័យ = ទិន្នន័យ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ឈ្មោះ, byte[] ទិន្នន័យ) {
        파일들.put(정규이름(ឈ្មោះ), Arrays.copyOf(ទិន្នន័យ, ទិន្នន័យ.length));
    }

    열린파일 បើក(String ឈ្មោះ) {
        byte[] ទិន្នន័យ = 파일들.get(정규이름(ឈ្មោះ));
        if (ទិន្នន័យ == null) {
            return null;
        }
        return new 열린파일(ទិន្នន័យ);
    }

    public boolean 존재함(String ឈ្មោះ) {
        return 파일들.containsKey(정규이름(ឈ្មោះ));
    }

    public ឯកសារ_ព័ត៌មាន ប្រព័ន្ធព័ត៌មាន(String ឈ្មោះ) {
        byte[] ទិន្នន័យ = 파일들.get(정규이름(ឈ្មោះ));
        if (ទិន្នន័យ == null) {
            return null;
        }
        return new ឯកសារ_ព័ត៌មាន(ទិន្នន័យ.length, 0100444);
    }

    private String 정규이름(String ឈ្មោះ) {
        if (ឈ្មោះ == null) {
            throw new NullPointerException("ឯកសារ 이름이 없습니다.");
        }
        String ការវាស់វែង = ឈ្មោះ.startsWith("/") ? ឈ្មោះ.substring(1) : ឈ្មោះ;
        return ការវាស់វែង.toUpperCase(Locale.ROOT);
    }
}
