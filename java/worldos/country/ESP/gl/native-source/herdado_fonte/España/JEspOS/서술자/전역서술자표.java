// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.서술자;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Estado_VALOR sección_VALOR 설정값을 보관한다. */
public final class 전역서술자표 {
    public static final class 조각 {
        private final int Fondo_VALOR;
        private final int 한계;
        private final int acceso_VALOR;

        조각(int Fondo_VALOR, int 한계, int acceso_VALOR) {
            this.Fondo_VALOR = Fondo_VALOR;
            this.한계 = 한계;
            this.acceso_VALOR = acceso_VALOR;
        }

        public int Fondo_VALOR() { return Fondo_VALOR; }
        public int 한계() { return 한계; }
        public int acceso_VALOR() { return acceso_VALOR; }
    }

    private final List<조각> 조각들 = new ArrayList<조각>();

    public int Anexar_introdución(int Fondo_VALOR, int 한계, int acceso_VALOR) {
        조각들.add(new 조각(Fondo_VALOR, 한계, acceso_VALOR));
        return (조각들.size() - 1) * 8;
    }

    public List<조각> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void conxunto_valor_predefinido() {
        조각들.clear();
        Anexar_introdución(0, 0, 0);
        Anexar_introdución(0, 0xfffff, 0x9a);
        Anexar_introdución(0, 0xfffff, 0x92);
        Anexar_introdución(0, 0xfffff, 0xfa);
        Anexar_introdución(0, 0xfffff, 0xf2);
    }
}

