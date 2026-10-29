// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Αίγυπτος.JEgyOS.σύστημα_αρχείων;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

/** engos FAT Ανάγνωση 계층과 같은 Ανάγνωση 전용 Αρχείο 저장소의 관리 모델이다. */
public final class σύστημα_αρχείων {
    static final class 열린파일 {
        final byte[] δεδομένα;
        int Θέση;
        int 참조수 = 1;

        열린파일(byte[] δεδομένα) {
            this.δεδομένα = δεδομένα;
        }
    }

    private final Map<String, byte[]> 파일들 = new LinkedHashMap<String, byte[]>();

    public void προσαρτώ_Αρχείο(String Όνομα, byte[] δεδομένα) {
        파일들.put(κανονικό_όνομα(Όνομα), Arrays.copyOf(δεδομένα, δεδομένα.length));
    }

    열린파일 Άνοιγμα(String Όνομα) {
        byte[] δεδομένα = 파일들.get(κανονικό_όνομα(Όνομα));
        if (δεδομένα == null) {
            return null;
        }
        return new 열린파일(δεδομένα);
    }

    public boolean 존재함(String Όνομα) {
        return 파일들.containsKey(κανονικό_όνομα(Όνομα));
    }

    public Αρχείο_πληροφορία Πληροφορίες_συστήματος(String Όνομα) {
        byte[] δεδομένα = 파일들.get(κανονικό_όνομα(Όνομα));
        if (δεδομένα == null) {
            return null;
        }
        return new Αρχείο_πληροφορία(δεδομένα.length, 0100444);
    }

    private String κανονικό_όνομα(String Όνομα) {
        if (Όνομα == null) {
            throw new NullPointerException("Αρχείο 이름이 없습니다.");
        }
        String μέτρηση = Όνομα.startsWith("/") ? Όνομα.substring(1) : Όνομα;
        return μέτρηση.toUpperCase(Locale.ROOT);
    }
}
