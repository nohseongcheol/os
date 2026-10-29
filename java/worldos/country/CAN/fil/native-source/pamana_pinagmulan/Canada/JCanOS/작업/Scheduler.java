// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Canada.JCanOS.기억공간.page_tagapamahala;
import Canada.JCanOS.sistema_ng_file.파일서술자표;

/** Proseso_VALUE 식별자와 라운드로빈 Ihanda 대기열을 관리한다. */
public final class Scheduler {
    private final page_tagapamahala 쪽관리;
    private final Map<Integer, Proseso_VALUE> Listahan_ng_Proseso = new HashMap<Integer, Proseso_VALUE>();
    private final Queue<Proseso_VALUE> 준비대기열 = new ArrayDeque<Proseso_VALUE>();
    private int Susunod_tagakilala = 1;

    public Scheduler(page_tagapamahala 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proseso_VALUE 첫과정(파일서술자표 파일서술자) {
        Proseso_VALUE 새과정 = new Proseso_VALUE(maglaan_tagakilala(), 0, 쪽관리.새주소공간(), 파일서술자);
        Listahan_ng_Proseso.put(Integer.valueOf(새과정.tagakilala_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proseso_VALUE 복제(Proseso_VALUE 부모) {
        Proseso_VALUE anak_VALUE = new Proseso_VALUE(
                maglaan_tagakilala(),
                부모.tagakilala_VALUE(),
                쪽관리.쓰기시복사복제(부모.email_SPACE()),
                부모.파일서술자().복제());
        anak_VALUE.set_app_break(부모.app_break());
        Listahan_ng_Proseso.put(Integer.valueOf(anak_VALUE.tagakilala_VALUE()), anak_VALUE);
        준비대기열.offer(anak_VALUE);
        return anak_VALUE;
    }

    public Proseso_VALUE Susunod_Proseso() {
        int tseke_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < tseke_COUNT; INDEX++) {
            Proseso_VALUE Susunod_item = 준비대기열.poll();
            if (Susunod_item != null && (Susunod_item.katayuan_VALUE() == Proseso_katayuan.Ihanda || Susunod_item.katayuan_VALUE() == Proseso_katayuan.Mag_execute_utos)) {
                Susunod_item.set_katayuan(Proseso_katayuan.Mag_execute_utos);
                준비대기열.offer(Susunod_item);
                return Susunod_item;
            }
        }
        return null;
    }

    public int 자식기다리기(Proseso_VALUE 부모, int anak_tagakilala, boolean 기다리지않음) {
        for (Proseso_VALUE 후보 : Listahan_ng_Proseso.values()) {
            if (후보.부모식별자() != 부모.tagakilala_VALUE()) {
                continue;
            }
            if (anak_tagakilala > 0 && 후보.tagakilala_VALUE() != anak_tagakilala) {
                continue;
            }
            if (후보.katayuan_VALUE() == Proseso_katayuan.Paglabas_app) {
                int sukat = (후보.Paglabas_CODE() & 0xff) << 8;
                Listahan_ng_Proseso.remove(Integer.valueOf(후보.tagakilala_VALUE()));
                return sukat;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proseso_VALUE FIND_Proseso(int tagakilala_VALUE) {
        return Listahan_ng_Proseso.get(Integer.valueOf(tagakilala_VALUE));
    }

    private int maglaan_tagakilala() {
        return Susunod_tagakilala++;
    }
}
