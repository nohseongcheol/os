// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Indonesia.JIdnOS.sistem_fail;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Baca 계층과 같은 Baca 전용 Fail 저장소의 관리 모델이다. */
public final class sistem_fail {
    static final class 열린파일 {
        final byte[] data;
        int Kedudukan;
        int Rujukan_COUNT = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Tambah_fail(String Nama, byte[] data) {
        파일들.put(정규이름(Nama), Arrays.copyOf(data, data.length));
    }

    열린파일 Buka(String Nama) {
        byte[] data = 파일들.get(정규이름(Nama));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Nama) {
        return 파일들.containsKey(정규이름(Nama));
    }

    public fail_info msinfo32_exe(String Nama) {
        byte[] data = 파일들.get(정규이름(Nama));
        if (data == null) {
            return null;
        }
        return new fail_info(data.length, 0100444);
    }

    private String 정규이름(String Nama) {
        if (Nama == null) {
            throw new NullPointerException("Fail 이름이 없습니다.");
        }
        String ukuran = Nama.startsWith("/") ? Nama.substring(1) : Nama;
        return ukuran.toUpperCase(Locale.ROOT);
    }
}
