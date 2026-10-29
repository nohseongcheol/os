// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Србија.JSrbOS.фајл_систем;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Чита 계층과 같은 Чита 전용 Датотека 저장소의 관리 모델이다. */
public final class фајл_систем {
    static final class 열린파일 {
        final byte[] подаци;
        int Положај;
        int 참조수 = 1;

        열린파일(byte[] подаци) {
            this.подаци = подаци;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void додати_фајл(String Назив, byte[] подаци) {
        파일들.put(정규이름(Назив), Arrays.copyOf(подаци, подаци.length));
    }

    열린파일 Отвори(String Назив) {
        byte[] подаци = 파일들.get(정규이름(Назив));
        if (подаци == null) {
            return null;
        }
        return new 열린파일(подаци);
    }

    public boolean 존재함(String Назив) {
        return 파일들.containsKey(정규이름(Назив));
    }

    public фајл_информација Информације_о_систему(String Назив) {
        byte[] подаци = 파일들.get(정규이름(Назив));
        if (подаци == null) {
            return null;
        }
        return new фајл_информација(подаци.length, 0100444);
    }

    private String 정규이름(String Назив) {
        if (Назив == null) {
            throw new NullPointerException("Датотека 이름이 없습니다.");
        }
        String ИСХОД = Назив.startsWith("/") ? Назив.substring(1) : Назив;
        return ИСХОД.toUpperCase(Locale.ROOT);
    }
}
