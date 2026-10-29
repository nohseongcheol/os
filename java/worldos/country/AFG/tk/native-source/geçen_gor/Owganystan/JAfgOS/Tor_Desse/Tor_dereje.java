// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Owganystan.JAfgOS.Tor_Desse;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Tor_dereje {
    @FunctionalInterface
    public interface 자료처리기 {
        void Proses_baha_girizmeklik(byte[] maglumat, int Bitir, int dowamlylyk_baha);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int ýumuş_baha_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ýumuş_baha_102996da & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] kadr_indeks) {
        if (!Tor_Gurallar.이더넷틀인가(kadr_indeks)) {
            return false;
        }
        int 종류 = Tor_Gurallar.이더넷상위규약(kadr_indeks);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Proses_baha_girizmeklik(kadr_indeks, 14, kadr_indeks.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(kadr_indeks, 14);
    }

    private boolean 상호통신망받기(byte[] maglumat, int Bitir) {
        if (!Tor_Gurallar.상호통신망규약사판인가(maglumat, Bitir)) {
            return false;
        }
        int At_dowamlylyk = (maglumat[Bitir] & 0x0f) * 4;
        int 전체길이 = Tor_Gurallar.큰순서짧은정수(maglumat, Bitir + 2);
        if (전체길이 < At_dowamlylyk || Bitir + 전체길이 > maglumat.length) {
            return false;
        }
        int ýumuş_baha_102996da = maglumat[Bitir + 9] & 0xff;
        int Mazmun_başlat = Bitir + At_dowamlylyk;
        int Mazmun_dowamlylyk = 전체길이 - At_dowamlylyk;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ýumuş_baha_102996da));
        if (직접처리기 != null) {
            직접처리기.Proses_baha_girizmeklik(maglumat, Mazmun_başlat, Mazmun_dowamlylyk);
            return true;
        }
        if (Mazmun_dowamlylyk < 4) {
            return false;
        }
        int 목적포트 = Tor_Gurallar.큰순서짧은정수(maglumat, Mazmun_başlat + 2);
        Map<Integer, 자료처리기> port_tablisa = ýumuş_baha_102996da == 17 ? 사용자자료단위처리기 : ýumuş_baha_102996da == 6 ? 전송제어처리기 : null;
        if (port_tablisa == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tablisa.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Proses_baha_girizmeklik(maglumat, Mazmun_başlat, Mazmun_dowamlylyk);
        return true;
    }
}

