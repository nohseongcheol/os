// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Azərbaycan.JAzeOS.Şəbəkə_Yığın;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Şəbəkə_lay {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proses_VALUE_daxiletmə(byte[] verilənlər, int İcra_Et, int uzunluq_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void qeydiyyatdan_keçmək_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void qeydiyyatdan_keçmək_IP(int müqavilə_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(müqavilə_VALUE & 0xff), 처리기);
    }

    public void qeydiyyatdan_keçmək_istifadəçi_verilənlər_dərs(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void qeydiyyatdan_keçmək_ötürülmə_nəzarət(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] kadr_INDEX) {
        if (!Şəbəkə_Alətlər.이더넷틀인가(kadr_INDEX)) {
            return false;
        }
        int 종류 = Şəbəkə_Alətlər.Ethernet_UPPER_protokol(kadr_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_daxiletmə(kadr_INDEX, 14, kadr_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(kadr_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] verilənlər, int İcra_Et) {
        if (!Şəbəkə_Alətlər.상호통신망규약사판인가(verilənlər, İcra_Et)) {
            return false;
        }
        int Başlıq_uzunluq = (verilənlər[İcra_Et] & 0x0f) * 4;
        int 전체길이 = Şəbəkə_Alətlər.큰순서짧은정수(verilənlər, İcra_Et + 2);
        if (전체길이 < Başlıq_uzunluq || İcra_Et + 전체길이 > verilənlər.length) {
            return false;
        }
        int müqavilə_VALUE = verilənlər[İcra_Et + 9] & 0xff;
        int Məzmun_Başla = İcra_Et + Başlıq_uzunluq;
        int Məzmun_uzunluq = 전체길이 - Başlıq_uzunluq;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(müqavilə_VALUE));
        if (직접처리기 != null) {
            직접처리기.Proses_VALUE_daxiletmə(verilənlər, Məzmun_Başla, Məzmun_uzunluq);
            return true;
        }
        if (Məzmun_uzunluq < 4) {
            return false;
        }
        int 목적포트 = Şəbəkə_Alətlər.큰순서짧은정수(verilənlər, Məzmun_Başla + 2);
        Map<Integer, 자료처리기> port_cədvəl = müqavilə_VALUE == 17 ? 사용자자료단위처리기 : müqavilə_VALUE == 6 ? 전송제어처리기 : null;
        if (port_cədvəl == null) {
            return false;
        }
        자료처리기 포트처리기 = port_cədvəl.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proses_VALUE_daxiletmə(verilənlər, Məzmun_Başla, Məzmun_uzunluq);
        return true;
    }
}

