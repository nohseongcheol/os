// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Danmark.JDnkOS.filsystem;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Läs 계층과 같은 Läs 전용 filnamn 저장소의 관리 모델이다. */
public final class filsystem {
    static final class 열린파일 {
        final byte[] data;
        int position;
        int referens_ANTAL = 1;

        열린파일(byte[] data) {
            this.data = data;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void Lägga_till_fil(String Namn, byte[] data) {
        파일들.put(kanoniskt_namn(Namn), Arrays.copyOf(data, data.length));
    }

    열린파일 Öppna(String Namn) {
        byte[] data = 파일들.get(kanoniskt_namn(Namn));
        if (data == null) {
            return null;
        }
        return new 열린파일(data);
    }

    public boolean 존재함(String Namn) {
        return 파일들.containsKey(kanoniskt_namn(Namn));
    }

    public fil_info msinfo32_exe(String Namn) {
        byte[] data = 파일들.get(kanoniskt_namn(Namn));
        if (data == null) {
            return null;
        }
        return new fil_info(data.length, 0100444);
    }

    private String kanoniskt_namn(String Namn) {
        if (Namn == null) {
            throw new NullPointerException("filnamn 이름이 없습니다.");
        }
        String RESULTAT = Namn.startsWith("/") ? Namn.substring(1) : Namn;
        return RESULTAT.toUpperCase(Locale.ROOT);
    }
}
