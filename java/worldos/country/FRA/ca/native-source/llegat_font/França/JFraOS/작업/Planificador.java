// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package França.JFraOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import França.JFraOS.기억공간.pàgina_administrador;
import França.JFraOS.sistema_d_arxius.파일서술자표;

/** Procés_VALOR 식별자와 라운드로빈 Prepara 대기열을 관리한다. */
public final class Planificador {
    private final pàgina_administrador 쪽관리;
    private final Map<Integer, Procés_VALOR> Procés_Llista = new HashMap<Integer, Procés_VALOR>();
    private final Queue<Procés_VALOR> 준비대기열 = new ArrayDeque<Procés_VALOR>();
    private int Següent_identificador = 1;

    public Planificador(pàgina_administrador 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Procés_VALOR 첫과정(파일서술자표 파일서술자) {
        Procés_VALOR 새과정 = new Procés_VALOR(assignar_identificador(), 0, 쪽관리.새주소공간(), 파일서술자);
        Procés_Llista.put(Integer.valueOf(새과정.identificador_VALOR()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Procés_VALOR clon_VALOR(Procés_VALOR 부모) {
        Procés_VALOR nen_VALOR = new Procés_VALOR(
                assignar_identificador(),
                부모.identificador_VALOR(),
                쪽관리.쓰기시복사복제(부모.ADREÇA_espai()),
                부모.파일서술자().clon_VALOR());
        nen_VALOR.conjunt_programa_pausa(부모.programa_pausa());
        Procés_Llista.put(Integer.valueOf(nen_VALOR.identificador_VALOR()), nen_VALOR);
        준비대기열.offer(nen_VALOR);
        return nen_VALOR;
    }

    public Procés_VALOR Següent_Procés() {
        int xec_COMPT = 준비대기열.size();
        for (int INDEX = 0; INDEX < xec_COMPT; INDEX++) {
            Procés_VALOR Següent_element = 준비대기열.poll();
            if (Següent_element != null && (Següent_element.Estat_VALOR() == Procés_Estat.Prepara || Següent_element.Estat_VALOR() == Procés_Estat.Executa_ordre)) {
                Següent_element.conjunt_Estat(Procés_Estat.Executa_ordre);
                준비대기열.offer(Següent_element);
                return Següent_element;
            }
        }
        return null;
    }

    public int 자식기다리기(Procés_VALOR 부모, int nen_identificador, boolean 기다리지않음) {
        for (Procés_VALOR 후보 : Procés_Llista.values()) {
            if (후보.부모식별자() != 부모.identificador_VALOR()) {
                continue;
            }
            if (nen_identificador > 0 && 후보.identificador_VALOR() != nen_identificador) {
                continue;
            }
            if (후보.Estat_VALOR() == Procés_Estat.Surt_programa) {
                int RESULTAT = (후보.Surt_CODI() & 0xff) << 8;
                Procés_Llista.remove(Integer.valueOf(후보.identificador_VALOR()));
                return RESULTAT;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Procés_VALOR BUSCA_Procés(int identificador_VALOR) {
        return Procés_Llista.get(Integer.valueOf(identificador_VALOR));
    }

    private int assignar_identificador() {
        return Següent_identificador++;
    }
}
