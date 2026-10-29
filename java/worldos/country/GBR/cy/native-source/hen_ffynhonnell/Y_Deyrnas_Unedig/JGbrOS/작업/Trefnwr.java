// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Y_Deyrnas_Unedig.JGbrOS.작업;

import java.util.ArrayDeque;
import java.util.HashMap;
import java.util.Map;
import java.util.Queue;
import Y_Deyrnas_Unedig.JGbrOS.기억공간.tudalen_rheolwr;
import Y_Deyrnas_Unedig.JGbrOS.system_ffeiliau.파일서술자표;

/** Proses_VALUE 식별자와 라운드로빈 Paratoi 대기열을 관리한다. */
public final class Trefnwr {
    private final tudalen_rheolwr 쪽관리;
    private final Map<Integer, Proses_VALUE> Rhestr_Prosesau = new HashMap<Integer, Proses_VALUE>();
    private final Queue<Proses_VALUE> 준비대기열 = new ArrayDeque<Proses_VALUE>();
    private int Nesaf_dynodwr = 1;

    public Trefnwr(tudalen_rheolwr 쪽관리) {
        this.쪽관리 = 쪽관리;
    }

    public Proses_VALUE 첫과정(파일서술자표 파일서술자) {
        Proses_VALUE 새과정 = new Proses_VALUE(dyrannu_dynodwr(), 0, 쪽관리.새주소공간(), 파일서술자);
        Rhestr_Prosesau.put(Integer.valueOf(새과정.dynodwr_VALUE()), 새과정);
        준비대기열.offer(새과정);
        return 새과정;
    }

    public Proses_VALUE 복제(Proses_VALUE 부모) {
        Proses_VALUE iselfen_VALUE = new Proses_VALUE(
                dyrannu_dynodwr(),
                부모.dynodwr_VALUE(),
                쪽관리.쓰기시복사복제(부모.ADDRESS_lle()),
                부모.파일서술자().복제());
        iselfen_VALUE.프로그램끝설정(부모.프로그램끝());
        Rhestr_Prosesau.put(Integer.valueOf(iselfen_VALUE.dynodwr_VALUE()), iselfen_VALUE);
        준비대기열.offer(iselfen_VALUE);
        return iselfen_VALUE;
    }

    public Proses_VALUE Nesaf_Proses() {
        int gwirio_COUNT = 준비대기열.size();
        for (int INDEX = 0; INDEX < gwirio_COUNT; INDEX++) {
            Proses_VALUE Nesaf_eitem = 준비대기열.poll();
            if (Nesaf_eitem != null && (Nesaf_eitem.cyflwr_VALUE() == Proses_cyflwr.Paratoi || Nesaf_eitem.cyflwr_VALUE() == Proses_cyflwr.Gweithredu_gorchymyn)) {
                Nesaf_eitem.set_cyflwr(Proses_cyflwr.Gweithredu_gorchymyn);
                준비대기열.offer(Nesaf_eitem);
                return Nesaf_eitem;
            }
        }
        return null;
    }

    public int 자식기다리기(Proses_VALUE 부모, int iselfen_dynodwr, boolean 기다리지않음) {
        for (Proses_VALUE 후보 : Rhestr_Prosesau.values()) {
            if (후보.부모식별자() != 부모.dynodwr_VALUE()) {
                continue;
            }
            if (iselfen_dynodwr > 0 && 후보.dynodwr_VALUE() != iselfen_dynodwr) {
                continue;
            }
            if (후보.cyflwr_VALUE() == Proses_cyflwr.gadael_Rhaglen) {
                int mesur = (후보.gadael_cod() & 0xff) << 8;
                Rhestr_Prosesau.remove(Integer.valueOf(후보.dynodwr_VALUE()));
                return mesur;
            }
            return 기다리지않음 ? 0 : -11;
        }
        return -10;
    }

    public Proses_VALUE FIND_Proses(int dynodwr_VALUE) {
        return Rhestr_Prosesau.get(Integer.valueOf(dynodwr_VALUE));
    }

    private int dyrannu_dynodwr() {
        return Nesaf_dynodwr++;
    }
}
