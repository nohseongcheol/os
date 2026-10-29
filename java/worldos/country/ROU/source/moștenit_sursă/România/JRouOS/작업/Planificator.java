// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package România.JRouOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import România.JRouOS.Memorie_regiune.쪽관리자;
import România.JRouOS.sistem_de_fișiere.파일서술자표;

/** Proces_VALUE 식별자와 라운드로빈 Pregătiți 대기열을 관리한다. */
public final class Planificator {
    private final 쪽관리자 쪽관리;
    private final Map<Integer, Proces_VALUE> Listă_proces = new HashMap<Integer, Proces_VALUE>();
    private final Queue<Proces_VALUE> 준비대기열 = new ArrayDeque<Proces_VALUE>();
    private int Următorul_identificator = 1;

    public Planificator(쪽관리자 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proces_VALUE 첫과정(파일서술자표 파일서술자) {
        Proces_VALUE 새과정 = new Proces_VALUE(aloca_identificator(), 0, 쪽관리.새주소공간(), 파일서술자);
        Listă_proces.put(Integer.valueOf(새과정.identificator_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proces_VALUE clona_VALUE(Proces_VALUE părinte_VALUE) {
        Proces_VALUE copil_VALUE = new Proces_VALUE(
                aloca_identificator(),
                părinte_VALUE.identificator_VALUE(),
                쪽관리.쓰기시복사복제(părinte_VALUE.adresa_SPAȚIU()),
                părinte_VALUE.파일서술자().clona_VALUE());
        copil_VALUE.set_program_pauză(părinte_VALUE.program_pauză());
        Listă_proces.put(Integer.valueOf(copil_VALUE.identificator_VALUE()), copil_VALUE);
        준비대기열.offer(copil_VALUE);
        return copil_VALUE;
    }

    public Proces_VALUE Următorul_Proces() {
        int verifica_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < verifica_COUNT; INDEX++) {
            Proces_VALUE Următorul_element = 준비대기열.poll();
            if (Următorul_element != null && (Următorul_element.Stare_VALUE() == Proces_Stare.Pregătiți || Următorul_element.Stare_VALUE() == Proces_Stare.executa_comandă)) {
                Următorul_element.set_Stare(Proces_Stare.executa_comandă);
                준비대기열.offer(Următorul_element);
                return Următorul_element;
            }
        }
        return null;
    }

    public int 자식기다리기(Proces_VALUE părinte_VALUE, int copil_identificator, boolean 기다리지않음) {
        for (Proces_VALUE 후보 : Listă_proces.values()) {
            if (후보.părinte_identificator() != părinte_VALUE.identificator_VALUE()) {
                continue;
            }
            if (copil_identificator > 0 && 후보.identificator_VALUE() != copil_identificator) {
                continue;
            }
            if (후보.Stare_VALUE() == Proces_Stare.ieși_program) {
                int KR = (후보.ieși_cod() & 0xff) << 8;
                Listă_proces.remove(Integer.valueOf(후보.identificator_VALUE()));
                return KR;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proces_VALUE FIND_Proces(int identificator_VALUE) {
        return Listă_proces.get(Integer.valueOf(identificator_VALUE));
    }

    private int aloca_identificator() {
        return Următorul_identificator++;
    }
}
