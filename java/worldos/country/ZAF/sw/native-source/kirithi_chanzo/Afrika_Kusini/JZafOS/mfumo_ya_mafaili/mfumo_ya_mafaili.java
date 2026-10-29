// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Afrika_Kusini.JZafOS.mfumo_ya_mafaili;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 faili 저장소의 관리 모델이다. */
public final class mfumo_ya_mafaili {
    static final class 열린파일 {
        final byte[] data;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Jina, byte[] data) {
        파일들.put(정규이름(Jina), Arrays.copyOf(data, data.length));
    }

    열린파일 unda(String Jina) {
        byte[] data = 파일들.get(정규이름(Jina));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Jina) {
        return 파일들.containsKey(정규이름(Jina));
    }

    public faili_maelezo msinfo32_exe(String Jina) {
        byte[] data = 파일들.get(정규이름(Jina));
        if (data == null) {
            return null;
        }
        return new faili_maelezo(data.length, 0100444);
    }

    private String 정규이름(String Jina) {
        if (Jina == null) {
            throw new NullPointerException("faili 이름이 없습니다.");
        }
        String 결과 = Jina.startsWith("/") ? Jina.substring(1) : Jina;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
