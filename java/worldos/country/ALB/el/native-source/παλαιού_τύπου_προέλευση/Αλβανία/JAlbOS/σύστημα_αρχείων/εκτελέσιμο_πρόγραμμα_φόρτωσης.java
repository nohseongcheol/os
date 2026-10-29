// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Αλβανία.JAlbOS.σύστημα_αρχείων;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** ELF32 little-endian εκτελώ_εντολή 파일의 머리부와 적재 구역을 검증한다. */
public final class εκτελέσιμο_πρόγραμμα_φόρτωσης {
    public static final class ενότητα_τιμή {
        private final int 종류;
        private final int σημαία_τιμή;
        private final int διεύθυνση;
        private final int Αρχείο_θέση;
        private final int Μέγεθος;

        ενότητα_τιμή(int 종류, int σημαία_τιμή, int διεύθυνση, int Αρχείο_θέση, int Μέγεθος) {
            this.종류 = 종류;
            this.σημαία_τιμή = σημαία_τιμή;
            this.διεύθυνση = διεύθυνση;
            this.Αρχείο_θέση = Αρχείο_θέση;
            this.Μέγεθος = Μέγεθος;
        }

        public int 종류() {
            return 종류;
        }

        public int σημαία_τιμή() {
            return σημαία_τιμή;
        }

        public int διεύθυνση() {
            return διεύθυνση;
        }

        public int Αρχείο_θέση() {
            return Αρχείο_θέση;
        }

        public int Μέγεθος() {
            return Μέγεθος;
        }
    }

    public static final class εικόνα {
        private final int αρχή_διεύθυνση;
        private final List<ενότητα_τιμή> 구역들;

        εικόνα(int αρχή_διεύθυνση, List<ενότητα_τιμή> 구역들) {
            this.αρχή_διεύθυνση = αρχή_διεύθυνση;
            this.구역들 = Collections.unmodifiableList(구역들);
        }

        public int αρχή_διεύθυνση() {
            return αρχή_διεύθυνση;
        }

        public List<ενότητα_τιμή> 구역들() {
            return 구역들;
        }
    }

    public εικόνα 검사(byte[] δεδομένα) {
        if (δεδομένα == null || δεδομένα.length < 52
                || δεδομένα[0] != 0x7f || δεδομένα[1] != 'E' || δεδομένα[2] != 'L' || δεδομένα[3] != 'F') {
            throw new IllegalArgumentException("ELF 마법값이 올바르지 않습니다.");
        }
        if (δεδομένα[4] != 1 || δεδομένα[5] != 1) {
            throw new IllegalArgumentException("ELF32 little-endian 형식이 아닙니다.");
        }
        int αρχή_διεύθυνση = ανάλυση_ακέραιος(δεδομένα, 24);
        int ενότητα_πίνακας_θέση = ανάλυση_ακέραιος(δεδομένα, 32);
        int ενότητα_καταχώρηση_αλλάζω_μέγεθος = 짧은정수읽기(δεδομένα, 46);
        int 구역수 = 짧은정수읽기(δεδομένα, 48);
        if (ενότητα_καταχώρηση_αλλάζω_μέγεθος < 40 || ενότητα_πίνακας_θέση < 0
                || (long) ενότητα_πίνακας_θέση + (long) ενότητα_καταχώρηση_αλλάζω_μέγεθος * 구역수 > δεδομένα.length) {
            throw new IllegalArgumentException("ELF 구역표 범위가 올바르지 않습니다.");
        }
        List<ενότητα_τιμή> 구역들 = new ArrayList<ενότητα_τιμή>();
        for (int Ευρετήριο = 0; Ευρετήριο < 구역수; Ευρετήριο++) {
            int Θέση = ενότητα_πίνακας_θέση + Ευρετήριο * ενότητα_καταχώρηση_αλλάζω_μέγεθος;
            int 종류 = ανάλυση_ακέραιος(δεδομένα, Θέση + 4);
            int σημαία_τιμή = ανάλυση_ακέραιος(δεδομένα, Θέση + 8);
            int διεύθυνση = ανάλυση_ακέραιος(δεδομένα, Θέση + 12);
            int Αρχείο_θέση = ανάλυση_ακέραιος(δεδομένα, Θέση + 16);
            int Μέγεθος = ανάλυση_ακέραιος(δεδομένα, Θέση + 20);
            if (Μέγεθος < 0 || (종류 != 8 && ((long) Αρχείο_θέση + Μέγεθος > δεδομένα.length || Αρχείο_θέση < 0))) {
                throw new IllegalArgumentException("ELF ενότητα_τιμή δεδομένα 범위가 올바르지 않습니다.");
            }
            구역들.add(new ενότητα_τιμή(종류, σημαία_τιμή, διεύθυνση, Αρχείο_θέση, Μέγεθος));
        }
        return new εικόνα(αρχή_διεύθυνση, 구역들);
    }

    private int ανάλυση_ακέραιος(byte[] δεδομένα, int Θέση) {
        if (Θέση < 0 || Θέση > δεδομένα.length - 4) {
            throw new IllegalArgumentException("ELF ακέραιος 범위를 벗어났습니다.");
        }
        return (δεδομένα[Θέση] & 0xff)
                | ((δεδομένα[Θέση + 1] & 0xff) << 8)
                | ((δεδομένα[Θέση + 2] & 0xff) << 16)
                | ((δεδομένα[Θέση + 3] & 0xff) << 24);
    }

    private int 짧은정수읽기(byte[] δεδομένα, int Θέση) {
        if (Θέση < 0 || Θέση > δεδομένα.length - 2) {
            throw new IllegalArgumentException("ELF 짧은 ακέραιος 범위를 벗어났습니다.");
        }
        return (δεδομένα[Θέση] & 0xff) | ((δεδομένα[Θέση + 1] & 0xff) << 8);
    }
}
