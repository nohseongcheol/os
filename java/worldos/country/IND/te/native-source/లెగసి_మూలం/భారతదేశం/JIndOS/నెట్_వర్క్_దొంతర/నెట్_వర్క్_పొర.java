// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package భారతదేశం.JIndOS.నెట్_వర్క్_దొంతర;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class నెట్_వర్క్_పొర {
    @FunctionalInterface
    public interface 자료처리기 {
        void విధానం_మూల్యం_ప్రవేశం(byte[] డేటా, int నడుపుము, int పొడవు_మూల్యం);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void నమోదు_చేయి_ఇథర్నెట్(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void నమోదు_చేయి_ఇంటర్నెట్_ప్రోటోకాల్(int పని_మూల్యం_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(పని_మూల్యం_102996da & 0xff), 처리기);
    }

    public void నమోదు_చేయి_వినియోగదారు_డేటా_పాఠం(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void నమోదు_చేయి_ప్రసారం_నియంత్రణ(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] చట్రం_సూచీ) {
        if (!నెట్_వర్క్_ఉపకరణాలు.సమాచార_టెక్నాలజీ_ఇథర్నెట్_చట్రం(చట్రం_సూచీ)) {
            return false;
        }
        int 종류 = నెట్_వర్క్_ఉపకరణాలు.이더넷상위규약(చట్రం_సూచీ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.విధానం_మూల్యం_ప్రవేశం(చట్రం_సూచీ, 14, చట్రం_సూచీ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(చట్రం_సూచీ, 14);
    }

    private boolean 상호통신망받기(byte[] డేటా, int నడుపుము) {
        if (!నెట్_వర్క్_ఉపకరణాలు.상호통신망규약사판인가(డేటా, నడుపుము)) {
            return false;
        }
        int శీర్షిక_పొడవు = (డేటా[నడుపుము] & 0x0f) * 4;
        int 전체길이 = నెట్_వర్క్_ఉపకరణాలు.큰순서짧은정수(డేటా, నడుపుము + 2);
        if (전체길이 < శీర్షిక_పొడవు || నడుపుము + 전체길이 > డేటా.length) {
            return false;
        }
        int పని_మూల్యం_102996da = డేటా[నడుపుము + 9] & 0xff;
        int విషయం_ప్రారంభం = నడుపుము + శీర్షిక_పొడవు;
        int విషయం_పొడవు = 전체길이 - శీర్షిక_పొడవు;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(పని_మూల్యం_102996da));
        if (직접처리기 != null) {
            직접처리기.విధానం_మూల్యం_ప్రవేశం(డేటా, విషయం_ప్రారంభం, విషయం_పొడవు);
            return true;
        }
        if (విషయం_పొడవు < 4) {
            return false;
        }
        int గమ్యం_పోర్ట్_సంఖ్య = నెట్_వర్క్_ఉపకరణాలు.큰순서짧은정수(డేటా, విషయం_ప్రారంభం + 2);
        Map<Integer, 자료처리기> పోర్టు_పట్టిక = పని_మూల్యం_102996da == 17 ? 사용자자료단위처리기 : పని_మూల్యం_102996da == 6 ? 전송제어처리기 : null;
        if (పోర్టు_పట్టిక == null) {
            return false;
        }
        자료처리기 포트처리기 = పోర్టు_పట్టిక.get(Integer.valueOf(గమ్యం_పోర్ట్_సంఖ్య));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.విధానం_మూల్యం_ప్రవేశం(డేటా, విషయం_ప్రారంభం, విషయం_పొడవు);
        return true;
    }
}

