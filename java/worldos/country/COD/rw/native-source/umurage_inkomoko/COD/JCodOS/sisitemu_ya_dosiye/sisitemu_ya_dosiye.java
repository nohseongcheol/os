// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package COD.JCodOS.sisitemu_ya_dosiye;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT 읽기 계층과 같은 읽기 전용 Idosiye 저장소의 관리 모델이다. */
public final class sisitemu_ya_dosiye {
    static final class 열린파일 {
        final byte[] amakurushingiro;
        int 위치;
        int 참조수 = 1;

        열린파일(byte[] amakurushingiro) {
            this.amakurushingiro = amakurushingiro;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String Izina, byte[] amakurushingiro) {
        파일들.put(정규이름(Izina), Arrays.copyOf(amakurushingiro, amakurushingiro.length));
    }

    열린파일 Gufungura(String Izina) {
        byte[] amakurushingiro = 파일들.get(정규이름(Izina));
        if (amakurushingiro == null) {
            return null;
        }
        return new 열린파일(amakurushingiro);
    }

    public boolean 존재함(String Izina) {
        return 파일들.containsKey(정규이름(Izina));
    }

    public dosiye_amakuru msinfo32_exe(String Izina) {
        byte[] amakurushingiro = 파일들.get(정규이름(Izina));
        if (amakurushingiro == null) {
            return null;
        }
        return new dosiye_amakuru(amakurushingiro.length, 0100444);
    }

    private String 정규이름(String Izina) {
        if (Izina == null) {
            throw new NullPointerException("Idosiye 이름이 없습니다.");
        }
        String 결과 = Izina.startsWith("/") ? Izina.substring(1) : Izina;
        return 결과.toUpperCase(Locale.ROOT);
    }
}
