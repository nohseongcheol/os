// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Монгол_Улс.JMngOS.файлын_систем;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Унших 계층과 같은 Унших 전용 Файл 저장소의 관리 모델이다. */
public final class файлын_систем {
    static final class 열린파일 {
        final byte[] өгөгдөл;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] өгөгдөл) {
            this.өгөгдөл = өгөгдөл;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Нэр, byte[] өгөгдөл) {
        파일들.put(정규이름(Нэр), Arrays.copyOf(өгөгдөл, өгөгдөл.length));
    }

    열린파일 Нээх(String Нэр) {
        byte[] өгөгдөл = 파일들.get(정규이름(Нэр));
        if (өгөгдөл == null) {
            return null;
        }
        return new 열린파일(өгөгдөл);
    }

    public boolean 존재함(String Нэр) {
        return 파일들.containsKey(정규이름(Нэр));
    }

    public файл_мэдээлэл системийн_мэдээлэл(String Нэр) {
        byte[] өгөгдөл = 파일들.get(정규이름(Нэр));
        if (өгөгдөл == null) {
            return null;
        }
        return new файл_мэдээлэл(өгөгдөл.length, 0100444);
    }

    private String 정규이름(String Нэр) {
        if (Нэр == null) {
            throw new NullPointerException("Файл 이름이 없습니다.");
        }
        String 결과 = Нэр.startsWith("/") ? Нэр.substring(1) : Нэр;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
