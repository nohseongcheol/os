// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package an_Ríocht_Aontaithe.JGbrOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import an_Ríocht_Aontaithe.JGbrOS.기억공간.leathanach_bainisteoir;
import an_Ríocht_Aontaithe.JGbrOS.córas_comhad.파일서술자표;

/** Próiseas_VALUE 식별자와 라운드로빈 Ullmhaigh 대기열을 관리한다. */
public final class Sceidealóir {
    private final leathanach_bainisteoir 쪽관리;
    private final Map<Integer, Próiseas_VALUE> Liosta_Próiseas = new HashMap<Integer, Próiseas_VALUE>();
    private final Queue<Próiseas_VALUE> 준비대기열 = new ArrayDeque<Próiseas_VALUE>();
    private int Ar_aghaidh_aitheantóir = 1;

    public Sceidealóir(leathanach_bainisteoir 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Próiseas_VALUE 첫과정(파일서술자표 파일서술자) {
        Próiseas_VALUE 새과정 = new Próiseas_VALUE(leithdháil_aitheantóir(), 0, 쪽관리.새주소공간(), 파일서술자);
        Liosta_Próiseas.put(Integer.valueOf(새과정.aitheantóir_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Próiseas_VALUE 복제(Próiseas_VALUE 부모) {
        Próiseas_VALUE leanbh_VALUE = new Próiseas_VALUE(
                leithdháil_aitheantóir(),
                부모.aitheantóir_VALUE(),
                쪽관리.쓰기시복사복제(부모.ADDRESS_spás()),
                부모.파일서술자().복제());
        leanbh_VALUE.프로그램끝설정(부모.프로그램끝());
        Liosta_Próiseas.put(Integer.valueOf(leanbh_VALUE.aitheantóir_VALUE()), leanbh_VALUE);
        준비대기열.offer(leanbh_VALUE);
        return leanbh_VALUE;
    }

    public Próiseas_VALUE Ar_aghaidh_Próiseas() {
        int seic_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < seic_COUNT; INDEX++) {
            Próiseas_VALUE Ar_aghaidh_mír = 준비대기열.poll();
            if (Ar_aghaidh_mír != null && (Ar_aghaidh_mír.staid_VALUE() == Próiseas_staid.Ullmhaigh || Ar_aghaidh_mír.staid_VALUE() == Próiseas_staid.Rith_ordú)) {
                Ar_aghaidh_mír.tacar_staid(Próiseas_staid.Rith_ordú);
                준비대기열.offer(Ar_aghaidh_mír);
                return Ar_aghaidh_mír;
            }
        }
        return null;
    }

    public int 자식기다리기(Próiseas_VALUE 부모, int leanbh_aitheantóir, boolean 기다리지않음) {
        for (Próiseas_VALUE 후보 : Liosta_Próiseas.values()) {
            if (후보.부모식별자() != 부모.aitheantóir_VALUE()) {
                continue;
            }
            if (leanbh_aitheantóir > 0 && 후보.aitheantóir_VALUE() != leanbh_aitheantóir) {
                continue;
            }
            if (후보.staid_VALUE() == Próiseas_staid.scoir_clár) {
                int tomhas = (후보.scoir_CODE() & 0xff) << 8;
                Liosta_Próiseas.remove(Integer.valueOf(후보.aitheantóir_VALUE()));
                return tomhas;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Próiseas_VALUE FIND_Próiseas(int aitheantóir_VALUE) {
        return Liosta_Próiseas.get(Integer.valueOf(aitheantóir_VALUE));
    }

    private int leithdháil_aitheantóir() {
        return Ar_aghaidh_aitheantóir++;
    }
}
