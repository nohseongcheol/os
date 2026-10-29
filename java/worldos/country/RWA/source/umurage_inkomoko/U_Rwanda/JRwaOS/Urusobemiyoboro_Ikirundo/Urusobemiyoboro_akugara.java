// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package U_Rwanda.JRwaOS.Urusobemiyoboro_Ikirundo;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Urusobemiyoboro_akugara {
    @FunctionalInterface
    public interface 자료처리기 {
        void Inzira_agaciro_icyinjizwa(byte[] amakurushingiro, int ihuriro, int uburebure_agaciro);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int ikibazo_agaciro, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ikibazo_agaciro & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ikadiri_umugerekashakiro) {
        if (!Urusobemiyoboro_Ibikoresho.이더넷틀인가(ikadiri_umugerekashakiro)) {
            return false;
        }
        int 종류 = Urusobemiyoboro_Ibikoresho.이더넷상위규약(ikadiri_umugerekashakiro);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Inzira_agaciro_icyinjizwa(ikadiri_umugerekashakiro, 14, ikadiri_umugerekashakiro.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ikadiri_umugerekashakiro, 14);
    }

    private boolean 상호통신망받기(byte[] amakurushingiro, int ihuriro) {
        if (!Urusobemiyoboro_Ibikoresho.상호통신망규약사판인가(amakurushingiro, ihuriro)) {
            return false;
        }
        int Umutwengaruka_uburebure = (amakurushingiro[ihuriro] & 0x0f) * 4;
        int 전체길이 = Urusobemiyoboro_Ibikoresho.큰순서짧은정수(amakurushingiro, ihuriro + 2);
        if (전체길이 < Umutwengaruka_uburebure || ihuriro + 전체길이 > amakurushingiro.length) {
            return false;
        }
        int ikibazo_agaciro = amakurushingiro[ihuriro + 9] & 0xff;
        int Ibirimo_Itangira = ihuriro + Umutwengaruka_uburebure;
        int Ibirimo_uburebure = 전체길이 - Umutwengaruka_uburebure;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ikibazo_agaciro));
        if (직접처리기 != null) {
            직접처리기.Inzira_agaciro_icyinjizwa(amakurushingiro, Ibirimo_Itangira, Ibirimo_uburebure);
            return true;
        }
        if (Ibirimo_uburebure < 4) {
            return false;
        }
        int 목적포트 = Urusobemiyoboro_Ibikoresho.큰순서짧은정수(amakurushingiro, Ibirimo_Itangira + 2);
        Map<Integer, 자료처리기> poti_imbonerahamwe = ikibazo_agaciro == 17 ? 사용자자료단위처리기 : ikibazo_agaciro == 6 ? 전송제어처리기 : null;
        if (poti_imbonerahamwe == null) {
            return false;
        }
        자료처리기 포트처리기 = poti_imbonerahamwe.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Inzira_agaciro_icyinjizwa(amakurushingiro, Ibirimo_Itangira, Ibirimo_uburebure);
        return true;
    }
}

