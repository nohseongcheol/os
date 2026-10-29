// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package San_Marino.JSmrOS.descrittore_voce;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Stato_VALORE sezione_VALORE 설정값을 보관한다. */
public final class tabella_dei_descrittori_globali {
    public static final class blocco_VALORE_652d4b53 {
        private final int sfondo_VALORE;
        private final int 한계;
        private final int accesso_VALORE;

        blocco_VALORE_652d4b53(int sfondo_VALORE, int 한계, int accesso_VALORE) {
            this.sfondo_VALORE = sfondo_VALORE;
            this.한계 = 한계;
            this.accesso_VALORE = accesso_VALORE;
        }

        public int sfondo_VALORE() { return sfondo_VALORE; }
        public int 한계() { return 한계; }
        public int accesso_VALORE() { return accesso_VALORE; }
    }

    private final List<blocco_VALORE_652d4b53> 조각들 = new ArrayList<blocco_VALORE_652d4b53>();

    public int Aggiunta_voce(int sfondo_VALORE, int 한계, int accesso_VALORE) {
        조각들.add(new blocco_VALORE_652d4b53(sfondo_VALORE, 한계, accesso_VALORE));
        return (조각들.size() - 1) * 8;
    }

    public List<blocco_VALORE_652d4b53> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void set_valore_predefinito() {
        조각들.clear();
        Aggiunta_voce(0, 0, 0);
        Aggiunta_voce(0, 0xfffff, 0x9a);
        Aggiunta_voce(0, 0xfffff, 0x92);
        Aggiunta_voce(0, 0xfffff, 0xfa);
        Aggiunta_voce(0, 0xfffff, 0xf2);
    }
}

