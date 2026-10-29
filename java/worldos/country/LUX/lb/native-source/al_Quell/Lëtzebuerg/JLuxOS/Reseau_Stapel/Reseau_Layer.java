// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Lëtzebuerg.JLuxOS.Reseau_Stapel;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Reseau_Layer {
    @FunctionalInterface
    public interface 자료처리기 {
        void Prozess_VALUE_Agab(byte[] Daten, int Laf, int Längt_VALUE);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void registréieren_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void registréieren_IP(int Job_VALUE, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(Job_VALUE & 0xff), 처리기);
    }

    public void registréieren_Benotzer_Daten_Lektioun(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void registréieren_Transmissioun_Kontroll(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] Rumm_INDEX) {
        if (!Reseau_Tools.이더넷틀인가(Rumm_INDEX)) {
            return false;
        }
        int 종류 = Reseau_Tools.Ethernet_UPPER_Protokoll(Rumm_INDEX);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Prozess_VALUE_Agab(Rumm_INDEX, 14, Rumm_INDEX.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(Rumm_INDEX, 14);
    }

    private boolean 상호통신망받기(byte[] Daten, int Laf) {
        if (!Reseau_Tools.상호통신망규약사판인가(Daten, Laf)) {
            return false;
        }
        int En_tête_Längt = (Daten[Laf] & 0x0f) * 4;
        int 전체길이 = Reseau_Tools.큰순서짧은정수(Daten, Laf + 2);
        if (전체길이 < En_tête_Längt || Laf + 전체길이 > Daten.length) {
            return false;
        }
        int Job_VALUE = Daten[Laf + 9] & 0xff;
        int Inhalt_Start = Laf + En_tête_Längt;
        int Inhalt_Längt = 전체길이 - En_tête_Längt;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(Job_VALUE));
        if (직접처리기 != null) {
            직접처리기.Prozess_VALUE_Agab(Daten, Inhalt_Start, Inhalt_Längt);
            return true;
        }
        if (Inhalt_Längt < 4) {
            return false;
        }
        int 목적포트 = Reseau_Tools.큰순서짧은정수(Daten, Inhalt_Start + 2);
        Map<Integer, 자료처리기> Port_Tabell = Job_VALUE == 17 ? 사용자자료단위처리기 : Job_VALUE == 6 ? 전송제어처리기 : null;
        if (Port_Tabell == null) {
            return false;
        }
        자료처리기 포트처리기 = Port_Tabell.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Prozess_VALUE_Agab(Daten, Inhalt_Start, Inhalt_Längt);
        return true;
    }
}

