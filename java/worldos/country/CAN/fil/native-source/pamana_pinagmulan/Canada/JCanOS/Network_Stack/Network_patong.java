// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Canada.JCanOS.Network_Stack;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Network_patong {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proseso_VALUE_pagpasok(byte[] data, int run, int haba_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void magrehistro_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void magrehistro_IP(int kaso_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(kaso_VALUE & 0xff), 처리기);
    }

    public void magrehistro_gumagamit_data_aralin(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void magrehistro_pagpapadala_control(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] frame_INDEX) {
        if (!Network_Mga_Tool.information_technology_Ethernet_frame(frame_INDEX)) {
            return false;
        }
        int 종류 = Network_Mga_Tool.Ethernet_UPPER_protokol(frame_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proseso_VALUE_pagpasok(frame_INDEX, 14, frame_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(frame_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] data, int run) {
        if (!Network_Mga_Tool.상호통신망규약사판인가(data, run)) {
            return false;
        }
        int Header_haba = (data[run] & 0x0f) * 4;
        int 전체길이 = Network_Mga_Tool.큰순서짧은정수(data, run + 2);
        if (전체길이 < Header_haba || run + 전체길이 > data.length) {
            return false;
        }
        int kaso_VALUE = data[run + 9] & 0xff;
        int Nilalaman_Start = run + Header_haba;
        int Nilalaman_haba = 전체길이 - Header_haba;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(kaso_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proseso_VALUE_pagpasok(data, Nilalaman_Start, Nilalaman_haba);
            return true;
        }
        if (Nilalaman_haba < 4) {
            return false;
        }
        int patutunguhan_numero_ng_port = Network_Mga_Tool.큰순서짧은정수(data, Nilalaman_Start + 2);
        Map<Integer, 자료처리기> port_talahanayan = kaso_VALUE == 17 ? 사용자자료단위처리기 : kaso_VALUE == 6 ? 전송제어처리기 : null;
        if (port_talahanayan == null) {
            return false;
        }
        자료처리기 포트처리기 = port_talahanayan.get(Integer.valueOf(patutunguhan_numero_ng_port));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proseso_VALUE_pagpasok(data, Nilalaman_Start, Nilalaman_haba);
        return true;
    }
}

