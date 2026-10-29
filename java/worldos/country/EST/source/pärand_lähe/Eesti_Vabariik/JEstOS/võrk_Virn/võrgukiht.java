// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Eesti_Vabariik.JEstOS.võrk_Virn;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP saama_VALUE 분배를 한곳에서 관리한다. */
public final class võrgukiht {
    @FunctionalInterface
    public interface 자료처리기 {
        void Joonis_VALUE_kirje(byte[] andmed, int Käivita_2, int 길이);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void register_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void register_IP(int lepingu_väärtus, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(lepingu_väärtus & 0xff), 처리기);
    }

    public void register_kasutaja_andmed_ühik(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean saama_Ethernet(byte[] raam_INDEX) {
        if (!võrk_Tööriistad.infotehnoloogia_Ethernet_raam(raam_INDEX)) {
            return false;
        }
        int 종류 = võrk_Tööriistad.Ethernet_UPPER_protokoll(raam_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Joonis_VALUE_kirje(raam_INDEX, 14, raam_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && saama_pilv_pakett(raam_INDEX, 14);
    }

    private boolean saama_pilv_pakett(byte[] andmed, int Käivita_2) {
        if (!võrk_Tööriistad.infotehnoloogia_AHH_4_protokoll(andmed, Käivita_2)) {
            return false;
        }
        int 머리길이 = (andmed[Käivita_2] & 0x0f) * 4;
        int 전체길이 = võrk_Tööriistad.큰순서짧은정수(andmed, Käivita_2 + 2);
        if (전체길이 < 머리길이 || Käivita_2 + 전체길이 > andmed.length) {
            return false;
        }
        int lepingu_väärtus = andmed[Käivita_2 + 9] & 0xff;
        int Sisu_START = Käivita_2 + 머리길이;
        int 내용길이 = 전체길이 - 머리길이;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(lepingu_väärtus));
        if (직접처리기 != null) {
            직접처리기.Joonis_VALUE_kirje(andmed, Sisu_START, 내용길이);
            return true;
        }
        if (내용길이 < 4) {
            return false;
        }
        int sihtkoht_pordinumber = võrk_Tööriistad.큰순서짧은정수(andmed, Sisu_START + 2);
        Map<Integer, 자료처리기> port_tabel = lepingu_väärtus == 17 ? 사용자자료단위처리기 : lepingu_väärtus == 6 ? 전송제어처리기 : null;
        if (port_tabel == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabel.get(Integer.valueOf(sihtkoht_pordinumber));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Joonis_VALUE_kirje(andmed, Sisu_START, 내용길이);
        return true;
    }
}

