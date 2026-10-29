// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Finland.JFinOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Finland.JFinOS.Minne_område.Sidhanteraren;
import Finland.JFinOS.filsystem.파일서술자표;

/** Process_värde 식별자와 라운드로빈 Förbereda 대기열을 관리한다. */
public final class Scheduler {
    private final Sidhanteraren 쪽관리;
    private final Map<Integer, Process_värde> Processlista = new HashMap<Integer, Process_värde>();
    private final Queue<Process_värde> 준비대기열 = new ArrayDeque<Process_värde>();
    private int Nästa_identifierare = 1;

    public Scheduler(Sidhanteraren 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Process_värde 첫과정(파일서술자표 파일서술자) {
        Process_värde 새과정 = new Process_värde(allokera_identifierare(), 0, 쪽관리.새주소공간(), 파일서술자);
        Processlista.put(Integer.valueOf(새과정.identifierare_värde()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Process_värde klon_värde(Process_värde överordnad_värde) {
        Process_värde barn_värde = new Process_värde(
                allokera_identifierare(),
                överordnad_värde.identifierare_värde(),
                쪽관리.쓰기시복사복제(överordnad_värde.adressutrymme()),
                överordnad_värde.파일서술자().klon_värde());
        barn_värde.uppsättning_app_rast(överordnad_värde.app_rast());
        Processlista.put(Integer.valueOf(barn_värde.identifierare_värde()), barn_värde);
        준비대기열.offer(barn_värde);
        return barn_värde;
    }

    public Process_värde Nästa_Process() {
        int check_ANTAL = 준비대기열.size();
        for (int INDEX = 0; INDEX < check_ANTAL; INDEX++) {
            Process_värde Nästa_objekt = 준비대기열.poll();
            if (Nästa_objekt != null && (Nästa_objekt.status_värde() == Process_status.Förbereda || Nästa_objekt.status_värde() == Process_status.köra_kommando)) {
                Nästa_objekt.uppsättning_status(Process_status.köra_kommando);
                준비대기열.offer(Nästa_objekt);
                return Nästa_objekt;
            }
        }
        return null;
    }

    public int 자식기다리기(Process_värde överordnad_värde, int barn_identifierare, boolean 기다리지않음) {
        for (Process_värde kandidat : Processlista.values()) {
            if (kandidat.överordnad_identifierare() != överordnad_värde.identifierare_värde()) {
                continue;
            }
            if (barn_identifierare > 0 && kandidat.identifierare_värde() != barn_identifierare) {
                continue;
            }
            if (kandidat.status_värde() == Process_status.Utgång_app) {
                int RESULTAT = (kandidat.slutkod() & 0xff) << 8;
                Processlista.remove(Integer.valueOf(kandidat.identifierare_värde()));
                return RESULTAT;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Process_värde Sök_Process(int identifierare_värde) {
        return Processlista.get(Integer.valueOf(identifierare_värde));
    }

    private int allokera_identifierare() {
        return Nästa_identifierare++;
    }
}
