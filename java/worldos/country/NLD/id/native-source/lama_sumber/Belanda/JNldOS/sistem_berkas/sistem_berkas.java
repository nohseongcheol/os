// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Belanda.JNldOS.sistem_berkas;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Baca 계층과 같은 Baca 전용 berkas 저장소의 관리 모델이다. */
public final class sistem_berkas {
    static final class 열린파일 {
        final byte[] data;
        int posisi;
        int Referensi_COUNT = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void tambah_file(String Nama_2, byte[] data) {
        파일들.put(정규이름(Nama_2), Arrays.copyOf(data, data.length));
    }

    열린파일 Buka(String Nama_2) {
        byte[] data = 파일들.get(정규이름(Nama_2));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Nama_2) {
        return 파일들.containsKey(정규이름(Nama_2));
    }

    public file_info msinfo32_exe(String Nama_2) {
        byte[] data = 파일들.get(정규이름(Nama_2));
        if (data == null) {
            return null;
        }
        return new file_info(data.length, 0100444);
    }

    private String 정규이름(String Nama_2) {
        if (Nama_2 == null) {
            throw new NullPointerException("berkas 이름이 없습니다.");
        }
        String hasil = Nama_2.startsWith("/") ? Nama_2.substring(1) : Nama_2;
        return hasil.toUpperCase(Locale.ROOT);
    }
}
