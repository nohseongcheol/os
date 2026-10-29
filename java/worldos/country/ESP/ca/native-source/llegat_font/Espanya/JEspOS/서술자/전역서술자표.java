// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Estat_VALOR secció_VALOR 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Fons_VALOR;
        private final int 한계;
        private final int accés_VALOR;

        조각(int Fons_VALOR, int 한계, int accés_VALOR) {
            this.Fons_VALOR = Fons_VALOR;
            this.한계 = 한계;
            this.accés_VALOR = accés_VALOR;
        }

        public int Fons_VALOR() { return Fons_VALOR; }
        public int 한계() { return 한계; }
        public int accés_VALOR() { return accés_VALOR; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Annexa_introducció(int Fons_VALOR, int 한계, int accés_VALOR) {
        조각들.add(new 조각(Fons_VALOR, 한계, accés_VALOR));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void conjunt_valor_per_defecte() {
        조각들.clear();
        Annexa_introducció(0, 0, 0);
        Annexa_introducció(0, 0xfffff, 0x9a);
        Annexa_introducció(0, 0xfffff, 0x92);
        Annexa_introducció(0, 0xfffff, 0xfa);
        Annexa_introducció(0, 0xfffff, 0xf2);
    }
}

