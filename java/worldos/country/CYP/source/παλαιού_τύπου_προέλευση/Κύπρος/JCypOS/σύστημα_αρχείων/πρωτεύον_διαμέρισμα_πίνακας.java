// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Κύπρος.JCypOS.σύστημα_αρχείων;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** DOS MBR의 네 προεπιλεγμένη_τιμή 분할 영역을 읽는다. */
public final class πρωτεύον_διαμέρισμα_πίνακας {
    public static final class διαμέρισμα_τιμή {
        private final int 종류;
        private final long αρχή_ενότητα;
        private final long 구역수;

        διαμέρισμα_τιμή(int 종류, long αρχή_ενότητα, long 구역수) {
            this.종류 = 종류;
            this.αρχή_ενότητα = αρχή_ενότητα;
            this.구역수 = 구역수;
        }

        public int 종류() { return 종류; }
        public long αρχή_ενότητα() { return αρχή_ενότητα; }
        public long 구역수() { return 구역수; }
    }

    public List<διαμέρισμα_τιμή> Ανάγνωση(byte[] 첫구역) {
        if (첫구역 == null || 첫구역.length < 512
                || (첫구역[510] & 0xff) != 0x55 || (첫구역[511] & 0xff) != 0xaa) {
            throw new IllegalArgumentException("올바른 MBR이 아닙니다.");
        }
        List<διαμέρισμα_τιμή> μέτρηση = new ArrayList<διαμέρισμα_τιμή>();
        for (int Ευρετήριο = 0; Ευρετήριο < 4; Ευρετήριο++) {
            int Θέση = 446 + Ευρετήριο * 16;
            int 종류 = 첫구역[Θέση + 4] & 0xff;
            long Εκτέλεση_2 = μικρό_endian_ακέραιος(첫구역, Θέση + 8);
            long Μέγεθος = μικρό_endian_ακέραιος(첫구역, Θέση + 12);
            if (종류 != 0 && Μέγεθος != 0) {
                μέτρηση.add(new διαμέρισμα_τιμή(종류, Εκτέλεση_2, Μέγεθος));
            }
        }
        return Collections.unmodifiableList(μέτρηση);
    }

    private long μικρό_endian_ακέραιος(byte[] δεδομένα, int Θέση) {
        return (δεδομένα[Θέση] & 0xffL)
                | ((δεδομένα[Θέση + 1] & 0xffL) << 8)
                | ((δεδομένα[Θέση + 2] & 0xffL) << 16)
                | ((δεδομένα[Θέση + 3] & 0xffL) << 24);
    }
}

