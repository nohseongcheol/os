// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ᑲᓇᑕᒥ.JCanOS.통신망;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Kasuqatigiitsimajut_qaliriit {
    @FunctionalInterface
    public interface 자료처리기 {
        void Pivallianiq_atuutilik_Iliniku(byte[] titiqqat, int 시작, int takininga_atuutilik);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int pijatsaq_atuutilik, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(pijatsaq_atuutilik & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] avalu_nalunaiqsimavik) {
        if (!통신망도구.이더넷틀인가(avalu_nalunaiqsimavik)) {
            return false;
        }
        int 종류 = 통신망도구.이더넷상위규약(avalu_nalunaiqsimavik);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.Pivallianiq_atuutilik_Iliniku(avalu_nalunaiqsimavik, 14, avalu_nalunaiqsimavik.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(avalu_nalunaiqsimavik, 14);
    }

    private boolean 상호통신망받기(byte[] titiqqat, int 시작) {
        if (!통신망도구.상호통신망규약사판인가(titiqqat, 시작)) {
            return false;
        }
        int Taijaugusinga_takininga = (titiqqat[시작] & 0x0f) * 4;
        int 전체길이 = 통신망도구.큰순서짧은정수(titiqqat, 시작 + 2);
        if (전체길이 < Taijaugusinga_takininga || 시작 + 전체길이 > titiqqat.length) {
            return false;
        }
        int pijatsaq_atuutilik = titiqqat[시작 + 9] & 0xff;
        int Ilulingit_pigiarli = 시작 + Taijaugusinga_takininga;
        int Ilulingit_takininga = 전체길이 - Taijaugusinga_takininga;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(pijatsaq_atuutilik));
        if (직접처리기 != null) {
            직접처리기.Pivallianiq_atuutilik_Iliniku(titiqqat, Ilulingit_pigiarli, Ilulingit_takininga);
            return true;
        }
        if (Ilulingit_takininga < 4) {
            return false;
        }
        int 목적포트 = 통신망도구.큰순서짧은정수(titiqqat, Ilulingit_pigiarli + 2);
        Map<Integer, 자료처리기> kapputigaq_kipu = pijatsaq_atuutilik == 17 ? 사용자자료단위처리기 : pijatsaq_atuutilik == 6 ? 전송제어처리기 : null;
        if (kapputigaq_kipu == null) {
            return false;
        }
        자료처리기 포트처리기 = kapputigaq_kipu.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.Pivallianiq_atuutilik_Iliniku(titiqqat, Ilulingit_pigiarli, Ilulingit_takininga);
        return true;
    }
}

