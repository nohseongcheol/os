// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Bẹ̀nẹ̀.JBenOS.Alásopọ̀_kójọ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Alásopọ̀_ìpele {
    @FunctionalInterface
    public interface 자료처리기 {
        void Ìlànà_iye_ìgbéwọlé(byte[] détà, int Rọ́ọ̀nù, int gígùn_iye);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void forúkọsílẹ̀_Ethernet(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void forúkọsílẹ̀_IP(int iṣẹ́_iye, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(iṣẹ́_iye & 0xff), 처리기);
    }

    public void forúkọsílẹ̀_aṣàmúlò_détà_ìkẹ́kọ̀ọ́(int ohun_èlò_alárídìmú_ojú, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(ohun_èlò_alárídìmú_ojú & 0xffff), 처리기);
    }

    public void forúkọsílẹ̀_ìfiránṣẹ́_ìdarí(int ohun_èlò_alárídìmú_ojú, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(ohun_èlò_alárídìmú_ojú & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] férèmù_wá_atọ̀ka_àkóónú) {
        if (!Alásopọ̀_Àwọn_irinṣẹ́.이더넷틀인가(férèmù_wá_atọ̀ka_àkóónú)) {
            return false;
        }
        int 종류 = Alásopọ̀_Àwọn_irinṣẹ́.이더넷상위규약(férèmù_wá_atọ̀ka_àkóónú);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Ìlànà_iye_ìgbéwọlé(férèmù_wá_atọ̀ka_àkóónú, 14, férèmù_wá_atọ̀ka_àkóónú.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(férèmù_wá_atọ̀ka_àkóónú, 14);
    }

    private boolean 상호통신망받기(byte[] détà, int Rọ́ọ̀nù) {
        if (!Alásopọ̀_Àwọn_irinṣẹ́.상호통신망규약사판인가(détà, Rọ́ọ̀nù)) {
            return false;
        }
        int àkọlé_gígùn = (détà[Rọ́ọ̀nù] & 0x0f) * 4;
        int 전체길이 = Alásopọ̀_Àwọn_irinṣẹ́.큰순서짧은정수(détà, Rọ́ọ̀nù + 2);
        if (전체길이 < àkọlé_gígùn || Rọ́ọ̀nù + 전체길이 > détà.length) {
            return false;
        }
        int iṣẹ́_iye = détà[Rọ́ọ̀nù + 9] & 0xff;
        int Àkóónú_bẹ̀rẹ̀ = Rọ́ọ̀nù + àkọlé_gígùn;
        int Àkóónú_gígùn = 전체길이 - àkọlé_gígùn;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(iṣẹ́_iye));
        if (직접처리기 != null) {
            직접처리기.Ìlànà_iye_ìgbéwọlé(détà, Àkóónú_bẹ̀rẹ̀, Àkóónú_gígùn);
            return true;
        }
        if (Àkóónú_gígùn < 4) {
            return false;
        }
        int 목적포트 = Alásopọ̀_Àwọn_irinṣẹ́.큰순서짧은정수(détà, Àkóónú_bẹ̀rẹ̀ + 2);
        Map<Integer, 자료처리기> ojú_atọ́ka = iṣẹ́_iye == 17 ? 사용자자료단위처리기 : iṣẹ́_iye == 6 ? 전송제어처리기 : null;
        if (ojú_atọ́ka == null) {
            return false;
        }
        자료처리기 포트처리기 = ojú_atọ́ka.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Ìlànà_iye_ìgbéwọlé(détà, Àkóónú_bẹ̀rẹ̀, Àkóónú_gígùn);
        return true;
    }
}

