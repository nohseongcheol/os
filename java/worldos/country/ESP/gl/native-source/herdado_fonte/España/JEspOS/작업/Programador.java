// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package España.JEspOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import España.JEspOS.기억공간.páxina_xefe;
import España.JEspOS.sistema_de_ficheiros.파일서술자표;

/** Proceso_VALOR 식별자와 라운드로빈 준비 대기열을 관리한다. */
public final class Programador {
    private final páxina_xefe 쪽관리;
    private final Map<Integer, Proceso_VALOR> Proceso_Lista = new HashMap<Integer, Proceso_VALOR>();
    private final Queue<Proceso_VALOR> 준비대기열 = new ArrayDeque<Proceso_VALOR>();
    private int 다음식별자 = 1;

    public Programador(páxina_xefe 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proceso_VALOR 첫과정(파일서술자표 파일서술자) {
        Proceso_VALOR 새과정 = new Proceso_VALOR(식별자할당(), 0, 쪽관리.새주소공간(), 파일서술자);
        Proceso_Lista.put(Integer.valueOf(새과정.식별자()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proceso_VALOR clon_VALOR(Proceso_VALOR 부모) {
        Proceso_VALOR neno_VALOR = new Proceso_VALOR(
                식별자할당(),
                부모.식별자(),
                쪽관리.쓰기시복사복제(부모.ENDEREZO_espazo()),
                부모.파일서술자().clon_VALOR());
        neno_VALOR.conxunto_apl_pausa(부모.apl_pausa());
        Proceso_Lista.put(Integer.valueOf(neno_VALOR.식별자()), neno_VALOR);
        준비대기열.offer(neno_VALOR);
        return neno_VALOR;
    }

    public Proceso_VALOR Seguinte_Proceso() {
        int cheque_CONTAR = 준비대기열.size();
        for (int ÍNDICE = 0; ÍNDICE < cheque_CONTAR; ÍNDICE++) {
            Proceso_VALOR Seguinte_elemento = 준비대기열.poll();
            if (Seguinte_elemento != null && (Seguinte_elemento.Estado_VALOR() == Proceso_Estado.준비 || Seguinte_elemento.Estado_VALOR() == Proceso_Estado.executar_comando)) {
                Seguinte_elemento.conxunto_Estado(Proceso_Estado.executar_comando);
                준비대기열.offer(Seguinte_elemento);
                return Seguinte_elemento;
            }
        }
        return null;
    }

    public int 자식기다리기(Proceso_VALOR 부모, int 자식식별자, boolean 기다리지않음) {
        for (Proceso_VALOR 후보 : Proceso_Lista.values()) {
            if (후보.부모식별자() != 부모.식별자()) {
                continue;
            }
            if (자식식별자 > 0 && 후보.식별자() != 자식식별자) {
                continue;
            }
            if (후보.Estado_VALOR() == Proceso_Estado.saír_apl) {
                int RESULTANTE = (후보.saír_CÓDIGO() & 0xff) << 8;
                Proceso_Lista.remove(Integer.valueOf(후보.식별자()));
                return RESULTANTE;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proceso_VALOR Busca_Proceso(int 식별자) {
        return Proceso_Lista.get(Integer.valueOf(식별자));
    }

    private int 식별자할당() {
        return 다음식별자++;
    }
}
