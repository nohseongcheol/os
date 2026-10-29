// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ລາວ.JLaoOS.ລະບົບຟາຍ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 ຟາຍ 저장소의 관리 모델이다. */
public final class ລະບົບຟາຍ {
    static final class 열린파일 {
        final byte[] ຂໍ້ມູນ;
        int ຈັດຕໍາແຫນ່ງ;
        int 참조수 = 1;

        열린파일(byte[] ຂໍ້ມູນ) {
            this.ຂໍ້ມູນ = ຂໍ້ມູນ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ຊື່, byte[] ຂໍ້ມູນ) {
        파일들.put(정규이름(ຊື່), Arrays.copyOf(ຂໍ້ມູນ, ຂໍ້ມູນ.length));
    }

    열린파일 ສ້າງ(String ຊື່) {
        byte[] ຂໍ້ມູນ = 파일들.get(정규이름(ຊື່));
        if (ຂໍ້ມູນ == null) {
            return null;
        }
        return new 열린파일(ຂໍ້ມູນ);
    }

    public boolean 존재함(String ຊື່) {
        return 파일들.containsKey(정규이름(ຊື່));
    }

    public ຟາຍ_ຂໍ້_ມູນ ລະບົບ_ຂໍ້_ມູນ(String ຊື່) {
        byte[] ຂໍ້ມູນ = 파일들.get(정규이름(ຊື່));
        if (ຂໍ້ມູນ == null) {
            return null;
        }
        return new ຟາຍ_ຂໍ້_ມູນ(ຂໍ້ມູນ.length, 0100444);
    }

    private String 정규이름(String ຊື່) {
        if (ຊື່ == null) {
            throw new NullPointerException("ຟາຍ 이름이 없습니다.");
        }
        String ມາດຕະການ = ຊື່.startsWith("/") ? ຊື່.substring(1) : ຊື່;
        return ມາດຕະການ.toUpperCase(Locale.ROOT);
    }
}
