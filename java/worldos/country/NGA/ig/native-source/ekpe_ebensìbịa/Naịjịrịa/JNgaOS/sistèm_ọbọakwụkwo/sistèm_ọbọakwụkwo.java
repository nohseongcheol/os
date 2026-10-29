// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.sistèm_ọbọakwụkwo;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Wepụta_ọzi 계층과 같은 Wepụta_ọzi 전용 Faịlụ 저장소의 관리 모델이다. */
public final class sistèm_ọbọakwụkwo {
    static final class 열린파일 {
        final byte[] datà;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] datà) {
            this.datà = datà;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Aha, byte[] datà) {
        파일들.put(정규이름(Aha), Arrays.copyOf(datà, datà.length));
    }

    열린파일 Mepee(String Aha) {
        byte[] datà = 파일들.get(정규이름(Aha));
        if (datà == null) {
            return null;
        }
        return new 열린파일(datà);
    }

    public boolean 존재함(String Aha) {
        return 파일들.containsKey(정규이름(Aha));
    }

    public ọbọakwụkwọ_ozi Ozi_Sistèm(String Aha) {
        byte[] datà = 파일들.get(정규이름(Aha));
        if (datà == null) {
            return null;
        }
        return new ọbọakwụkwọ_ozi(datà.length, 0100444);
    }

    private String 정규이름(String Aha) {
        if (Aha == null) {
            throw new NullPointerException("Faịlụ 이름이 없습니다.");
        }
        String 결과 = Aha.startsWith("/") ? Aha.substring(1) : Aha;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
