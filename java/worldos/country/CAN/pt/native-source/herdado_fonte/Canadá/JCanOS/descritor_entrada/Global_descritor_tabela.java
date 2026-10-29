// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canadá.JCanOS.descritor_entrada;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** x86 전역 서술자표와 작업 Estado_VALOR seção_VALOR 설정값을 보관한다. */
public final class Global_descritor_tabela {
    public static final class fragmento_VALOR {
        private final int Tela_de_fundo_VALOR;
        private final int 한계;
        private final int acesso_VALOR;

        fragmento_VALOR(int Tela_de_fundo_VALOR, int 한계, int acesso_VALOR) {
            this.Tela_de_fundo_VALOR = Tela_de_fundo_VALOR;
            this.한계 = 한계;
            this.acesso_VALOR = acesso_VALOR;
        }

        public int Tela_de_fundo_VALOR() { return Tela_de_fundo_VALOR; }
        public int 한계() { return 한계; }
        public int acesso_VALOR() { return acesso_VALOR; }
    }

    private final List<fragmento_VALOR> 조각들 = new ArrayList<fragmento_VALOR>();

    public int Acrescentar_entrada(int Tela_de_fundo_VALOR, int 한계, int acesso_VALOR) {
        조각들.add(new fragmento_VALOR(Tela_de_fundo_VALOR, 한계, acesso_VALOR));
        return (조각들.size() - 1) * 8;
    }

    public List<fragmento_VALOR> 조각들() {
        return Collections.unmodifiableList(조각들);
    }

    public void set_valor_padrão() {
        조각들.clear();
        Acrescentar_entrada(0, 0, 0);
        Acrescentar_entrada(0, 0xfffff, 0x9a);
        Acrescentar_entrada(0, 0xfffff, 0x92);
        Acrescentar_entrada(0, 0xfffff, 0xfa);
        Acrescentar_entrada(0, 0xfffff, 0xf2);
    }
}

