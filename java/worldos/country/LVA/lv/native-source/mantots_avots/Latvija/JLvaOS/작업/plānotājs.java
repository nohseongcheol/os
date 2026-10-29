// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Latvija.JLvaOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Latvija.JLvaOS.atmiņa_reģions.쪽관리자;
import Latvija.JLvaOS.failu_sistēma.파일서술자표;

/** Process_VALUE 식별자와 라운드로빈 Sagatavot 대기열을 관리한다. */
public final class plānotājs {
    private final 쪽관리자 쪽관리;
    private final Map<Integer, Process_VALUE> Procesu_saraksts = new HashMap<Integer, Process_VALUE>();
    private final Queue<Process_VALUE> 준비대기열 = new ArrayDeque<Process_VALUE>();
    private int Tālāk_identifikators = 1;

    public plānotājs(쪽관리자 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Process_VALUE 첫과정(파일서술자표 파일서술자) {
        Process_VALUE 새과정 = new Process_VALUE(piešķirt_identifikators(), 0, 쪽관리.새주소공간(), 파일서술자);
        Procesu_saraksts.put(Integer.valueOf(새과정.identifikators_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Process_VALUE klons_VALUE(Process_VALUE vecākobjekts_VALUE) {
        Process_VALUE bērns_VALUE = new Process_VALUE(
                piešķirt_identifikators(),
                vecākobjekts_VALUE.identifikators_VALUE(),
                쪽관리.쓰기시복사복제(vecākobjekts_VALUE.adrese_telpa()),
                vecākobjekts_VALUE.파일서술자().klons_VALUE());
        bērns_VALUE.kopa_programma_pārtraukt(vecākobjekts_VALUE.programma_pārtraukt());
        Procesu_saraksts.put(Integer.valueOf(bērns_VALUE.identifikators_VALUE()), bērns_VALUE);
        준비대기열.offer(bērns_VALUE);
        return bērns_VALUE;
    }

    public Process_VALUE Tālāk_Process() {
        int čeks_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < čeks_COUNT; INDEX++) {
            Process_VALUE Tālāk_krājums = 준비대기열.poll();
            if (Tālāk_krājums != null && (Tālāk_krājums.Statuss_VALUE() == Process_Statuss.Sagatavot || Tālāk_krājums.Statuss_VALUE() == Process_Statuss.Izpildīt_komanda)) {
                Tālāk_krājums.kopa_Statuss(Process_Statuss.Izpildīt_komanda);
                준비대기열.offer(Tālāk_krājums);
                return Tālāk_krājums;
            }
        }
        return null;
    }

    public int 자식기다리기(Process_VALUE vecākobjekts_VALUE, int bērns_identifikators, boolean 기다리지않음) {
        for (Process_VALUE 후보 : Procesu_saraksts.values()) {
            if (후보.vecākobjekts_identifikators() != vecākobjekts_VALUE.identifikators_VALUE()) {
                continue;
            }
            if (bērns_identifikators > 0 && 후보.identifikators_VALUE() != bērns_identifikators) {
                continue;
            }
            if (후보.Statuss_VALUE() == Process_Statuss.Iziet_programma) {
                int mērs = (후보.Iziet_CODE() & 0xff) << 8;
                Procesu_saraksts.remove(Integer.valueOf(후보.identifikators_VALUE()));
                return mērs;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Process_VALUE FIND_Process(int identifikators_VALUE) {
        return Procesu_saraksts.get(Integer.valueOf(identifikators_VALUE));
    }

    private int piešķirt_identifikators() {
        return Tālāk_identifikators++;
    }
}
