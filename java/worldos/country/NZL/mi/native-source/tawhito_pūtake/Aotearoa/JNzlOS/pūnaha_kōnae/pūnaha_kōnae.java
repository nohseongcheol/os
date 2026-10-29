// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Aotearoa.JNzlOS.pūnaha_kōnae;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Pānuitia 계층과 같은 Pānuitia 전용 Kōnae 저장소의 관리 모델이다. */
public final class pūnaha_kōnae {
    static final class 열린파일 {
        final byte[] raraunga;
        int tūranga;
        int Pūranga_kōrero_COUNT = 1;

        열린파일(byte[] raraunga) {
            this.raraunga = raraunga;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Ingoa, byte[] raraunga) {
        파일들.put(정규이름(Ingoa), Arrays.copyOf(raraunga, raraunga.length));
    }

    열린파일 Huaki(String Ingoa) {
        byte[] raraunga = 파일들.get(정규이름(Ingoa));
        if (raraunga == null) {
            return null;
        }
        return new 열린파일(raraunga);
    }

    public boolean 존재함(String Ingoa) {
        return 파일들.containsKey(정규이름(Ingoa));
    }

    public kōnae_mōhiohio msinfo32_exe(String Ingoa) {
        byte[] raraunga = 파일들.get(정규이름(Ingoa));
        if (raraunga == null) {
            return null;
        }
        return new kōnae_mōhiohio(raraunga.length, 0100444);
    }

    private String 정규이름(String Ingoa) {
        if (Ingoa == null) {
            throw new NullPointerException("Kōnae 이름이 없습니다.");
        }
        String mēhua = Ingoa.startsWith("/") ? Ingoa.substring(1) : Ingoa;
        return mēhua.toUpperCase(Locale.ROOT);
    }
}
