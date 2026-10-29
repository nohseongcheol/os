// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Malta.JMltOS.sistema_tal_fajls;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 fajl 저장소의 관리 모델이다. */
public final class sistema_tal_fajls {
    static final class 열린파일 {
        final byte[] data;
        int pożizzjoni;
        int Referenza_COUNT = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String isem, byte[] data) {
        파일들.put(정규이름(isem), Arrays.copyOf(data, data.length));
    }

    열린파일 fetaħ(String isem) {
        byte[] data = 파일들.get(정규이름(isem));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String isem) {
        return 파일들.containsKey(정규이름(isem));
    }

    public fajl_informazzjoni msinfo32_exe(String isem) {
        byte[] data = 파일들.get(정규이름(isem));
        if (data == null) {
            return null;
        }
        return new fajl_informazzjoni(data.length, 0100444);
    }

    private String 정규이름(String isem) {
        if (isem == null) {
            throw new NullPointerException("fajl 이름이 없습니다.");
        }
        String miżura = isem.startsWith("/") ? isem.substring(1) : isem;
        return miżura.toUpperCase(Locale.ROOT);
    }
}
