// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Naịjịrịa.JNgaOS.Netwọọkụ_ikpo;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class Netwọọkụ_òkpùkpù {
    @FunctionalInterface
    public interface 자료처리기 {
        void ùsòrò_valuu_ndebà(byte[] datà, int Bido, int ogologo_valuu);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int ngō_valuu, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ngō_valuu & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int ngwaike_pọọt, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(ngwaike_pọọt & 0xffff), 처리기);
    }

    public void 전송제어등록(int ngwaike_pọọt, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(ngwaike_pọọt & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] okpokoro_indèks) {
        if (!Netwọọkụ_Ngwaọrụ.이더넷틀인가(okpokoro_indèks)) {
            return false;
        }
        int 종류 = Netwọọkụ_Ngwaọrụ.이더넷상위규약(okpokoro_indèks);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ùsòrò_valuu_ndebà(okpokoro_indèks, 14, okpokoro_indèks.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(okpokoro_indèks, 14);
    }

    private boolean 상호통신망받기(byte[] datà, int Bido) {
        if (!Netwọọkụ_Ngwaọrụ.상호통신망규약사판인가(datà, Bido)) {
            return false;
        }
        int isi_ogologo = (datà[Bido] & 0x0f) * 4;
        int 전체길이 = Netwọọkụ_Ngwaọrụ.큰순서짧은정수(datà, Bido + 2);
        if (전체길이 < isi_ogologo || Bido + 전체길이 > datà.length) {
            return false;
        }
        int ngō_valuu = datà[Bido + 9] & 0xff;
        int ndịnà_Mbido = Bido + isi_ogologo;
        int ndịnà_ogologo = 전체길이 - isi_ogologo;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ngō_valuu));
        if (직접처리기 != null) {
            직접처리기.ùsòrò_valuu_ndebà(datà, ndịnà_Mbido, ndịnà_ogologo);
            return true;
        }
        if (ndịnà_ogologo < 4) {
            return false;
        }
        int 목적포트 = Netwọọkụ_Ngwaọrụ.큰순서짧은정수(datà, ndịnà_Mbido + 2);
        Map<Integer, 자료처리기> pọọt_tebùl = ngō_valuu == 17 ? 사용자자료단위처리기 : ngō_valuu == 6 ? 전송제어처리기 : null;
        if (pọọt_tebùl == null) {
            return false;
        }
        자료처리기 포트처리기 = pọọt_tebùl.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ùsòrò_valuu_ndebà(datà, ndịnà_Mbido, ndịnà_ogologo);
        return true;
    }
}

