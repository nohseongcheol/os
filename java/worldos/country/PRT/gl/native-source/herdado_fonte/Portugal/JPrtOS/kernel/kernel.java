// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Portugal.JPrtOS.kernel;

import Portugal.JPrtOS.기억공간.Memoria_xefe;
import Portugal.JPrtOS.기억공간.páxina_xefe;
import Portugal.JPrtOS.입력.입력관리자;
import Portugal.JPrtOS.작업.Proceso_VALOR;
import Portugal.JPrtOS.작업.Programador;
import Portugal.JPrtOS.체계호출.체계호출;
import Portugal.JPrtOS.sistema_de_ficheiros.파일서술자표;
import Portugal.JPrtOS.sistema_de_ficheiros.sistema_de_ficheiros;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class kernel {
    private final 하드웨어 dispositivo_VALOR;
    private final Memoria_xefe 기억공간 = new Memoria_xefe(32 * 1024 * 1024);
    private final páxina_xefe 쪽관리 = new páxina_xefe();
    private final sistema_de_ficheiros sistema_de_ficheiros = new sistema_de_ficheiros();
    private final Programador Programador = new Programador(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final Proceso_VALOR 첫과정;
    private final 체계호출 체계호출;

    public kernel(하드웨어 dispositivo_VALOR) {
        this.dispositivo_VALOR = dispositivo_VALOR;
        첫과정 = Programador.첫과정(new 파일서술자표(sistema_de_ficheiros));
        체계호출 = new 체계호출(sistema_de_ficheiros, 쪽관리, Programador, dispositivo_VALOR, 입력관리);
    }

    public void Executar_2() {
        dispositivo_VALOR.직렬출력("=== JPrtOS 관리 kernel_VALOR ===\n");
    }

    public void executar_paso() {
        dispositivo_VALOR.중앙처리장치멈춤();
    }

    public Memoria_xefe 기억공간() {
        return 기억공간;
    }

    public páxina_xefe 쪽관리() {
        return 쪽관리;
    }

    public sistema_de_ficheiros sistema_de_ficheiros() {
        return sistema_de_ficheiros;
    }

    public Programador Programador() {
        return Programador;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public Proceso_VALOR 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
