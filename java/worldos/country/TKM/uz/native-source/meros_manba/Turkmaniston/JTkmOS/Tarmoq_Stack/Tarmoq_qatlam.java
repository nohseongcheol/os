// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Turkmaniston.JTkmOS.Tarmoq_Stack;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Tarmoq_qatlam {
    @FunctionalInterface
    public interface 자료처리기 {
        void Jarayon_VALUE_kiritish(byte[] ma_lumotlar, int Bajarish, int uzunlik_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int murojaat_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(murojaat_VALUE & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] kadr_INDEX) {
        if (!Tarmoq_Vositalar.이더넷틀인가(kadr_INDEX)) {
            return false;
        }
        int 종류 = Tarmoq_Vositalar.Ethernet_UPPER_bayonnoma(kadr_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Jarayon_VALUE_kiritish(kadr_INDEX, 14, kadr_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(kadr_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] ma_lumotlar, int Bajarish) {
        if (!Tarmoq_Vositalar.상호통신망규약사판인가(ma_lumotlar, Bajarish)) {
            return false;
        }
        int Sarlavha_uzunlik = (ma_lumotlar[Bajarish] & 0x0f) * 4;
        int 전체길이 = Tarmoq_Vositalar.큰순서짧은정수(ma_lumotlar, Bajarish + 2);
        if (전체길이 < Sarlavha_uzunlik || Bajarish + 전체길이 > ma_lumotlar.length) {
            return false;
        }
        int murojaat_VALUE = ma_lumotlar[Bajarish + 9] & 0xff;
        int tarkib_Start = Bajarish + Sarlavha_uzunlik;
        int tarkib_uzunlik = 전체길이 - Sarlavha_uzunlik;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(murojaat_VALUE));
        if (직접처리기 != null) {
            직접처리기.Jarayon_VALUE_kiritish(ma_lumotlar, tarkib_Start, tarkib_uzunlik);
            return true;
        }
        if (tarkib_uzunlik < 4) {
            return false;
        }
        int 목적포트 = Tarmoq_Vositalar.큰순서짧은정수(ma_lumotlar, tarkib_Start + 2);
        Map<Integer, 자료처리기> port_jadval = murojaat_VALUE == 17 ? 사용자자료단위처리기 : murojaat_VALUE == 6 ? 전송제어처리기 : null;
        if (port_jadval == null) {
            return false;
        }
        자료처리기 포트처리기 = port_jadval.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Jarayon_VALUE_kiritish(ma_lumotlar, tarkib_Start, tarkib_uzunlik);
        return true;
    }
}

