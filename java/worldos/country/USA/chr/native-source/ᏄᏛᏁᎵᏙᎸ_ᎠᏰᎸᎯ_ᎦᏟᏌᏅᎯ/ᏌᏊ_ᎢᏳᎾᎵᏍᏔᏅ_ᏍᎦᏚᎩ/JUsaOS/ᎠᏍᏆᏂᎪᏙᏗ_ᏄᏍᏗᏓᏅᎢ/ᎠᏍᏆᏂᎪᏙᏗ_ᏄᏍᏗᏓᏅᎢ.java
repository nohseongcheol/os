// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᏌᏊ_ᎢᏳᎾᎵᏍᏔᏅ_ᏍᎦᏚᎩ.JUsaOS.ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 ᎠᏍᏆᏂᎪᏙᏗ 저장소의 관리 모델이다. */
public final class ᎠᏍᏆᏂᎪᏙᏗ_ᏄᏍᏗᏓᏅᎢ {
    static final class 열린파일 {
        final byte[] ᎦᏟᏌᏅᎯ;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] ᎦᏟᏌᏅᎯ) {
            this.ᎦᏟᏌᏅᎯ = ᎦᏟᏌᏅᎯ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String ᏚᏙᎥᎢ, byte[] ᎦᏟᏌᏅᎯ) {
        파일들.put(정규이름(ᏚᏙᎥᎢ), Arrays.copyOf(ᎦᏟᏌᏅᎯ, ᎦᏟᏌᏅᎯ.length));
    }

    열린파일 ᎯᏍᏚᎢ(String ᏚᏙᎥᎢ) {
        byte[] ᎦᏟᏌᏅᎯ = 파일들.get(정규이름(ᏚᏙᎥᎢ));
        if (ᎦᏟᏌᏅᎯ == null) {
            return null;
        }
        return new 열린파일(ᎦᏟᏌᏅᎯ);
    }

    public boolean 존재함(String ᏚᏙᎥᎢ) {
        return 파일들.containsKey(정규이름(ᏚᏙᎥᎢ));
    }

    public ᎠᏍᏆᏂᎪᏙᏗ_ᎧᏃᎮᏢᎥᏍᎩ msinfo32_exe(String ᏚᏙᎥᎢ) {
        byte[] ᎦᏟᏌᏅᎯ = 파일들.get(정규이름(ᏚᏙᎥᎢ));
        if (ᎦᏟᏌᏅᎯ == null) {
            return null;
        }
        return new ᎠᏍᏆᏂᎪᏙᏗ_ᎧᏃᎮᏢᎥᏍᎩ(ᎦᏟᏌᏅᎯ.length, 0100444);
    }

    private String 정규이름(String ᏚᏙᎥᎢ) {
        if (ᏚᏙᎥᎢ == null) {
            throw new NullPointerException("ᎠᏍᏆᏂᎪᏙᏗ 이름이 없습니다.");
        }
        String 결과 = ᏚᏙᎥᎢ.startsWith("/") ? ᏚᏙᎥᎢ.substring(1) : ᏚᏙᎥᎢ;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
