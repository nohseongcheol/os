// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Қазақстан.JKazOS.желі_Бума;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class желілік_деңгей {
    @FunctionalInterface
    public interface 자료처리기 {
        void Процесс_мән_енгізу(byte[] деректер, int Орындау_2, int ұзындық_мән);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void тіркеу_IP_протоколы(int іс_мән, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(іс_мән & 0xff), 처리기);
    }

    public void тіркеу_пайдаланушы_деректер_сабақ(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void тіркеу_берілім_Басқару(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] кадр_индекс) {
        if (!желі_Құралдар.이더넷틀인가(кадр_индекс)) {
            return false;
        }
        int 종류 = желі_Құралдар.이더넷상위규약(кадр_индекс);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Процесс_мән_енгізу(кадр_индекс, 14, кадр_индекс.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(кадр_индекс, 14);
    }

    private boolean 상호통신망받기(byte[] деректер, int Орындау_2) {
        if (!желі_Құралдар.상호통신망규약사판인가(деректер, Орындау_2)) {
            return false;
        }
        int Тақырып_ұзындық = (деректер[Орындау_2] & 0x0f) * 4;
        int 전체길이 = желі_Құралдар.큰순서짧은정수(деректер, Орындау_2 + 2);
        if (전체길이 < Тақырып_ұзындық || Орындау_2 + 전체길이 > деректер.length) {
            return false;
        }
        int іс_мән = деректер[Орындау_2 + 9] & 0xff;
        int мазмұн_басы = Орындау_2 + Тақырып_ұзындық;
        int мазмұн_ұзындық = 전체길이 - Тақырып_ұзындық;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(іс_мән));
        if (직접처리기 != null) {
            직접처리기.Процесс_мән_енгізу(деректер, мазмұн_басы, мазмұн_ұзындық);
            return true;
        }
        if (мазмұн_ұзындық < 4) {
            return false;
        }
        int тағайындау_порт_нөмірі = желі_Құралдар.큰순서짧은정수(деректер, мазмұн_басы + 2);
        Map<Integer, 자료처리기> порт_кесте = іс_мән == 17 ? 사용자자료단위처리기 : іс_мән == 6 ? 전송제어처리기 : null;
        if (порт_кесте == null) {
            return false;
        }
        자료처리기 포트처리기 = порт_кесте.get(Integer.valueOf(тағайындау_порт_нөмірі));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Процесс_мән_енгізу(деректер, мазмұн_басы, мазмұн_ұзындық);
        return true;
    }
}

