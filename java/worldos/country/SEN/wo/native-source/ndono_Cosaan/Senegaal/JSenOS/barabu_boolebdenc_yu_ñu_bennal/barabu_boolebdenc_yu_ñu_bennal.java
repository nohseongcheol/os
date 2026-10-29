// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Senegaal.JSenOS.barabu_boolebdenc_yu_ñu_bennal;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 bara_denc 저장소의 관리 모델이다. */
public final class barabu_boolebdenc_yu_ñu_bennal {
    static final class 열린파일 {
        final byte[] mbir;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] mbir) {
            this.mbir = mbir;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String tur_253d1510, byte[] mbir) {
        파일들.put(정규이름(tur_253d1510), Arrays.copyOf(mbir, mbir.length));
    }

    열린파일 sos(String tur_253d1510) {
        byte[] mbir = 파일들.get(정규이름(tur_253d1510));
        if (mbir == null) {
            return null;
        }
        return new 열린파일(mbir);
    }

    public boolean 존재함(String tur_253d1510) {
        return 파일들.containsKey(정규이름(tur_253d1510));
    }

    public bara_denc_yëglë msinfo32_exe(String tur_253d1510) {
        byte[] mbir = 파일들.get(정규이름(tur_253d1510));
        if (mbir == null) {
            return null;
        }
        return new bara_denc_yëglë(mbir.length, 0100444);
    }

    private String 정규이름(String tur_253d1510) {
        if (tur_253d1510 == null) {
            throw new NullPointerException("bara_denc 이름이 없습니다.");
        }
        String 결과 = tur_253d1510.startsWith("/") ? tur_253d1510.substring(1) : tur_253d1510;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
