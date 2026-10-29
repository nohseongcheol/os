// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package An_Rìoghachd_Aonaichte.JGbrOS.lìonra_stac;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class lìonra_breath {
    @FunctionalInterface
    public interface 자료처리기 {
        void Pròiseas_VALUE_cur_a_steach(byte[] dàta, int ruith, int faid_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void clàraich_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void clàraich_IP(int cùis_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(cùis_VALUE & 0xff), 처리기);
    }

    public void clàraich_cleachdaiche_dàta_leasan(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] frèam_INDEX) {
        if (!lìonra_innealan.이더넷틀인가(frèam_INDEX)) {
            return false;
        }
        int 종류 = lìonra_innealan.Ethernet_UPPER_pròtacal(frèam_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Pròiseas_VALUE_cur_a_steach(frèam_INDEX, 14, frèam_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(frèam_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] dàta, int ruith) {
        if (!lìonra_innealan.상호통신망규약사판인가(dàta, ruith)) {
            return false;
        }
        int bann_cinn_faid = (dàta[ruith] & 0x0f) * 4;
        int 전체길이 = lìonra_innealan.큰순서짧은정수(dàta, ruith + 2);
        if (전체길이 < bann_cinn_faid || ruith + 전체길이 > dàta.length) {
            return false;
        }
        int cùis_VALUE = dàta[ruith + 9] & 0xff;
        int susbaint_Start = ruith + bann_cinn_faid;
        int susbaint_faid = 전체길이 - bann_cinn_faid;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(cùis_VALUE));
        if (직접처리기 != null) {
            직접처리기.Pròiseas_VALUE_cur_a_steach(dàta, susbaint_Start, susbaint_faid);
            return true;
        }
        if (susbaint_faid < 4) {
            return false;
        }
        int 목적포트 = lìonra_innealan.큰순서짧은정수(dàta, susbaint_Start + 2);
        Map<Integer, 자료처리기> port_clàr = cùis_VALUE == 17 ? 사용자자료단위처리기 : cùis_VALUE == 6 ? 전송제어처리기 : null;
        if (port_clàr == null) {
            return false;
        }
        자료처리기 포트처리기 = port_clàr.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Pròiseas_VALUE_cur_a_steach(dàta, susbaint_Start, susbaint_faid);
        return true;
    }
}

