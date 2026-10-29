// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Γερμανία.JDeuOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Κατάσταση_τιμή ενότητα_τιμή 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int φόντο_τιμή;
        private final int 한계;
        private final int πρόσβαση_τιμή;

        조각(int φόντο_τιμή, int 한계, int πρόσβαση_τιμή) {
            this.φόντο_τιμή = φόντο_τιμή;
            this.한계 = 한계;
            this.πρόσβαση_τιμή = πρόσβαση_τιμή;
        }

        public int φόντο_τιμή() { return φόντο_τιμή; }
        public int 한계() { return 한계; }
        public int πρόσβαση_τιμή() { return πρόσβαση_τιμή; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int προσαρτώ_καταχώρηση(int φόντο_τιμή, int 한계, int πρόσβαση_τιμή) {
        조각들.add(new 조각(φόντο_τιμή, 한계, πρόσβαση_τιμή));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void σύνολο_προεπιλεγμένη_τιμή() {
        조각들.clear();
        προσαρτώ_καταχώρηση(0, 0, 0);
        προσαρτώ_καταχώρηση(0, 0xfffff, 0x9a);
        προσαρτώ_καταχώρηση(0, 0xfffff, 0x92);
        προσαρτώ_καταχώρηση(0, 0xfffff, 0xfa);
        προσαρτώ_καταχώρηση(0, 0xfffff, 0xf2);
    }
}

