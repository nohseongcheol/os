// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ബഹ്റിൻ.JBhrOS.ഫയല്_സിസ്റ്റം;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT വായന 계층과 같은 വായന 전용 ഫയല് 저장소의 관리 모델이다. */
public final class ഫയല്_സിസ്റ്റം {
    static final class 열린파일 {
        final byte[] ഡാറ്റാ;
        int സ്ഥാനം;
        int 참조수 = 1;

        열린파일(byte[] ഡാറ്റാ) {
            this.ഡാറ്റാ = ഡാറ്റാ;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void 파일추가(String പേരു്, byte[] ഡാറ്റാ) {
        파일들.put(정규이름(പേരു്), Arrays.copyOf(ഡാറ്റാ, ഡാറ്റാ.length));
    }

    열린파일 തുറക്കുക(String പേരു്) {
        byte[] ഡാറ്റാ = 파일들.get(정규이름(പേരു്));
        if (ഡാറ്റാ == null) {
            return null;
        }
        return new 열린파일(ഡാറ്റാ);
    }

    public boolean 존재함(String പേരു്) {
        return 파일들.containsKey(정규이름(പേരു്));
    }

    public ഫയല്_വിവരം സിസ്റ്റം_വിവരങ്ങള്(String പേരു്) {
        byte[] ഡാറ്റാ = 파일들.get(정규이름(പേരു്));
        if (ഡാറ്റാ == null) {
            return null;
        }
        return new ഫയല്_വിവരം(ഡാറ്റാ.length, 0100444);
    }

    private String 정규이름(String പേരു്) {
        if (പേരു് == null) {
            throw new NullPointerException("ഫയല് 이름이 없습니다.");
        }
        String അളവ് = പേരു്.startsWith("/") ? പേരു്.substring(1) : പേരു്;
        return അളവ്.toUpperCase(Locale.ROOT);
    }
}
