// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package युगांडा.JUgaOS.फ़ाइल_सिस्टम;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT पढ़ें 계층과 같은 पढ़ें 전용 संचिका 저장소의 관리 모델이다. */
public final class फ़ाइल_सिस्टम {
    static final class 열린파일 {
        final byte[] आँकड़े;
        int स्थान;
        int 참조수 = 1;

        열린파일(byte[] आँकड़े) {
            this.आँकड़े = आँकड़े;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void जोड़ें_फ़ाइल(String नाम, byte[] आँकड़े) {
        파일들.put(कैनॉनिकल_नाम(नाम), Arrays.copyOf(आँकड़े, आँकड़े.length));
    }

    열린파일 खोलें(String नाम) {
        byte[] आँकड़े = 파일들.get(कैनॉनिकल_नाम(नाम));
        if (आँकड़े == null) {
            return null;
        }
        return new 열린파일(आँकड़े);
    }

    public boolean 존재함(String नाम) {
        return 파일들.containsKey(कैनॉनिकल_नाम(नाम));
    }

    public फ़ाइल_जानकारी सिस्टम_जानकारी(String नाम) {
        byte[] आँकड़े = 파일들.get(कैनॉनिकल_नाम(नाम));
        if (आँकड़े == null) {
            return null;
        }
        return new फ़ाइल_जानकारी(आँकड़े.length, 0100444);
    }

    private String कैनॉनिकल_नाम(String नाम) {
        if (नाम == null) {
            throw new NullPointerException("संचिका 이름이 없습니다.");
        }
        String परिणाम = नाम.startsWith("/") ? नाम.substring(1) : नाम;
        return परिणाम.toUpperCase(Locale.ROOT);
    }
}
