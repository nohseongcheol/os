// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Ísland.JIslOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Ísland.JIslOS.기억공간.síða_stjórnandi;
import Ísland.JIslOS.skrárkerfi.파일서술자표;

/** Ferli_VALUE 식별자와 라운드로빈 Undirbúa 대기열을 관리한다. */
public final class Verkraðari {
    private final síða_stjórnandi 쪽관리;
    private final Map<Integer, Ferli_VALUE> Ferlislisti = new HashMap<Integer, Ferli_VALUE>();
    private final Queue<Ferli_VALUE> 준비대기열 = new ArrayDeque<Ferli_VALUE>();
    private int Áfram_auðkenni = 1;

    public Verkraðari(síða_stjórnandi 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Ferli_VALUE 첫과정(파일서술자표 파일서술자) {
        Ferli_VALUE 새과정 = new Ferli_VALUE(úthluta_auðkenni(), 0, 쪽관리.새주소공간(), 파일서술자);
        Ferlislisti.put(Integer.valueOf(새과정.auðkenni_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Ferli_VALUE 복제(Ferli_VALUE yfireining_VALUE) {
        Ferli_VALUE barn_VALUE = new Ferli_VALUE(
                úthluta_auðkenni(),
                yfireining_VALUE.auðkenni_VALUE(),
                쪽관리.쓰기시복사복제(yfireining_VALUE.slóð_svæði()),
                yfireining_VALUE.파일서술자().복제());
        barn_VALUE.sett_forrit_hlé(yfireining_VALUE.forrit_hlé());
        Ferlislisti.put(Integer.valueOf(barn_VALUE.auðkenni_VALUE()), barn_VALUE);
        준비대기열.offer(barn_VALUE);
        return barn_VALUE;
    }

    public Ferli_VALUE Áfram_Ferli() {
        int athuga_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < athuga_COUNT; INDEX++) {
            Ferli_VALUE Áfram_vara = 준비대기열.poll();
            if (Áfram_vara != null && (Áfram_vara.staða_VALUE_e10195a1() == Ferli_staða.Undirbúa || Áfram_vara.staða_VALUE_e10195a1() == Ferli_staða.keyra_skipun)) {
                Áfram_vara.sett_staða(Ferli_staða.keyra_skipun);
                준비대기열.offer(Áfram_vara);
                return Áfram_vara;
            }
        }
        return null;
    }

    public int 자식기다리기(Ferli_VALUE yfireining_VALUE, int barn_auðkenni, boolean 기다리지않음) {
        for (Ferli_VALUE 후보 : Ferlislisti.values()) {
            if (후보.yfireining_auðkenni() != yfireining_VALUE.auðkenni_VALUE()) {
                continue;
            }
            if (barn_auðkenni > 0 && 후보.auðkenni_VALUE() != barn_auðkenni) {
                continue;
            }
            if (후보.staða_VALUE_e10195a1() == Ferli_staða.loka_forrit) {
                int NIÐURSTAÐA = (후보.loka_CODE() & 0xff) << 8;
                Ferlislisti.remove(Integer.valueOf(후보.auðkenni_VALUE()));
                return NIÐURSTAÐA;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Ferli_VALUE FIND_Ferli(int auðkenni_VALUE) {
        return Ferlislisti.get(Integer.valueOf(auðkenni_VALUE));
    }

    private int úthluta_auðkenni() {
        return Áfram_auðkenni++;
    }
}
