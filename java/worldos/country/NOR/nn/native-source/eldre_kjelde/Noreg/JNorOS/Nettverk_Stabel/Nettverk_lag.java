// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Noreg.JNorOS.Nettverk_Stabel;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Nettverk_lag {
    @FunctionalInterface
    public interface 자료처리기 {
        void Prosess_VALUE_oppføring(byte[] data, int Køyr_2, int lengd_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registrere_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registrere_IP(int sak_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(sak_VALUE & 0xff), 처리기);
    }

    public void registrere_brukar_data_leksjon(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void registrere_overføring_styring(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] rute_INDEX) {
        if (!Nettverk_Verktøy.informasjonsteknologi_Ethernet_rute(rute_INDEX)) {
            return false;
        }
        int 종류 = Nettverk_Verktøy.Ethernet_UPPER_protokoll(rute_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Prosess_VALUE_oppføring(rute_INDEX, 14, rute_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(rute_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] data, int Køyr_2) {
        if (!Nettverk_Verktøy.상호통신망규약사판인가(data, Køyr_2)) {
            return false;
        }
        int hode_lengd = (data[Køyr_2] & 0x0f) * 4;
        int 전체길이 = Nettverk_Verktøy.큰순서짧은정수(data, Køyr_2 + 2);
        if (전체길이 < hode_lengd || Køyr_2 + 전체길이 > data.length) {
            return false;
        }
        int sak_VALUE = data[Køyr_2 + 9] & 0xff;
        int Innhald_START = Køyr_2 + hode_lengd;
        int Innhald_lengd = 전체길이 - hode_lengd;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(sak_VALUE));
        if (직접처리기 != null) {
            직접처리기.Prosess_VALUE_oppføring(data, Innhald_START, Innhald_lengd);
            return true;
        }
        if (Innhald_lengd < 4) {
            return false;
        }
        int mål_portnummer = Nettverk_Verktøy.큰순서짧은정수(data, Innhald_START + 2);
        Map<Integer, 자료처리기> port_tabell = sak_VALUE == 17 ? 사용자자료단위처리기 : sak_VALUE == 6 ? 전송제어처리기 : null;
        if (port_tabell == null) {
            return false;
        }
        자료처리기 포트처리기 = port_tabell.get(Integer.valueOf(mål_portnummer));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Prosess_VALUE_oppføring(data, Innhald_START, Innhald_lengd);
        return true;
    }
}

