// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.sistema_ng_file;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 file 저장소의 관리 모델이다. */
public final class sistema_ng_file {
    static final class 열린파일 {
        final byte[] data;
        int posisyon;
        int Sanggunian_COUNT = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String pangalan, byte[] data) {
        파일들.put(정규이름(pangalan), Arrays.copyOf(data, data.length));
    }

    열린파일 buksan(String pangalan) {
        byte[] data = 파일들.get(정규이름(pangalan));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String pangalan) {
        return 파일들.containsKey(정규이름(pangalan));
    }

    public file_impormasyon msinfo32_exe(String pangalan) {
        byte[] data = 파일들.get(정규이름(pangalan));
        if (data == null) {
            return null;
        }
        return new file_impormasyon(data.length, 0100444);
    }

    private String 정규이름(String pangalan) {
        if (pangalan == null) {
            throw new NullPointerException("file 이름이 없습니다.");
        }
        String sukat = pangalan.startsWith("/") ? pangalan.substring(1) : pangalan;
        return sukat.toUpperCase(Locale.ROOT);
    }
}
