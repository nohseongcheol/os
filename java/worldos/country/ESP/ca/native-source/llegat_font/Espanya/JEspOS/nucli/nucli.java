// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Espanya.JEspOS.nucli;

import Espanya.JEspOS.기억공간.Memòria_administrador;
import Espanya.JEspOS.기억공간.pàgina_administrador;
import Espanya.JEspOS.입력.입력관리자;
import Espanya.JEspOS.작업.Procés_VALOR;
import Espanya.JEspOS.작업.Planificador;
import Espanya.JEspOS.체계호출.체계호출;
import Espanya.JEspOS.sistema_d_arxius.파일서술자표;
import Espanya.JEspOS.sistema_d_arxius.sistema_d_arxius;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class nucli {
    private final 하드웨어 dispositiu_VALOR;
    private final Memòria_administrador 기억공간 = new Memòria_administrador(32 * 1024 * 1024);
    private final pàgina_administrador 쪽관리 = new pàgina_administrador();
    private final sistema_d_arxius sistema_d_arxius = new sistema_d_arxius();
    private final Planificador Planificador = new Planificador(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Procés_VALOR 첫과정;
    private final 체계호출 체계호출;

    public nucli(하드웨어 dispositiu_VALOR) {
        this.dispositiu_VALOR = dispositiu_VALOR;
        첫과정 = Planificador.첫과정(new 파일서술자표(sistema_d_arxius));
        체계호출 = new 체계호출(sistema_d_arxius, 쪽관리, Planificador, dispositiu_VALOR, 입력관리);
    }

    public void Executa_2() {
        dispositiu_VALOR.직렬출력("=== JEspOS 관리 nucli_VALOR ===\n");
    }

    public void Executa_pas() {
        dispositiu_VALOR.중앙처리장치멈춤();
    }

    public Memòria_administrador 기억공간() {
        return 기억공간;
    }

    public pàgina_administrador 쪽관리() {
        return 쪽관리;
    }

    public sistema_d_arxius sistema_d_arxius() {
        return sistema_d_arxius;
    }

    public Planificador Planificador() {
        return Planificador;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Procés_VALOR 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
