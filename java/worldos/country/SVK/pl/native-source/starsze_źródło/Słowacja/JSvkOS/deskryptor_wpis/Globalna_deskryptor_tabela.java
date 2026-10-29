// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Słowacja.JSvkOS.deskryptor_wpis;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Stan_WARTOŚĆ obszar_WARTOŚĆ_366e0bfa 설정값을 보관한다. */
public final class Globalna_deskryptor_tabela {
    public static final class fragment_WARTOŚĆ_652d4b53 {
        private final int Tło_WARTOŚĆ;
        private final int 한계;
        private final int dostęp_WARTOŚĆ;

        fragment_WARTOŚĆ_652d4b53(int Tło_WARTOŚĆ, int 한계, int dostęp_WARTOŚĆ) {
            this.Tło_WARTOŚĆ = Tło_WARTOŚĆ;
            this.한계 = 한계;
            this.dostęp_WARTOŚĆ = dostęp_WARTOŚĆ;
        }

        public int Tło_WARTOŚĆ() { return Tło_WARTOŚĆ; }
        public int 한계() { return 한계; }
        public int dostęp_WARTOŚĆ() { return dostęp_WARTOŚĆ; }
    }

    private final List<fragment_WARTOŚĆ_652d4b53> 조각들 = new ArrayList<fragment_WARTOŚĆ_652d4b53>();

    public int dołączać_wpis(int Tło_WARTOŚĆ, int 한계, int dostęp_WARTOŚĆ) {
        조각들.add(new fragment_WARTOŚĆ_652d4b53(Tło_WARTOŚĆ, 한계, dostęp_WARTOŚĆ));
        return (조각들.size() - 1) * 8;
    }

    public List<fragment_WARTOŚĆ_652d4b53> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void set_wartość_domyślna() {
        조각들.clear();
        dołączać_wpis(0, 0, 0);
        dołączać_wpis(0, 0xfffff, 0x9a);
        dołączać_wpis(0, 0xfffff, 0x92);
        dołączać_wpis(0, 0xfffff, 0xfa);
        dołączać_wpis(0, 0xfffff, 0xf2);
    }
}

