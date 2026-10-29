// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package عێراق.JIrqOS.تۆڕ_ستاك;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class تۆڕ_چین {
    @FunctionalInterface
    public interface 자료처리기 {
        void پرۆسە_نرخ_تێنووسین(byte[] دەیتا, int ڕادان, int درێژی_نرخ);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int ئەرک_نرخ, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ئەرک_نرخ & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int 포트, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public void 전송제어등록(int 포트, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(포트 & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] فرەیم_پێرست) {
        if (!تۆڕ_ئامرازەکان.이더넷틀인가(فرەیم_پێرست)) {
            return false;
        }
        int 종류 = تۆڕ_ئامرازەکان.이더넷상위규약(فرەیم_پێرست);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.پرۆسە_نرخ_تێنووسین(فرەیم_پێرست, 14, فرەیم_پێرست.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(فرەیم_پێرست, 14);
    }

    private boolean 상호통신망받기(byte[] دەیتا, int ڕادان) {
        if (!تۆڕ_ئامرازەکان.상호통신망규약사판인가(دەیتا, ڕادان)) {
            return false;
        }
        int سەرپەڕ_درێژی = (دەیتا[ڕادان] & 0x0f) * 4;
        int 전체길이 = تۆڕ_ئامرازەکان.큰순서짧은정수(دەیتا, ڕادان + 2);
        if (전체길이 < سەرپەڕ_درێژی || ڕادان + 전체길이 > دەیتا.length) {
            return false;
        }
        int ئەرک_نرخ = دەیتا[ڕادان + 9] & 0xff;
        int ناوەرۆک_دەستپێك = ڕادان + سەرپەڕ_درێژی;
        int ناوەرۆک_درێژی = 전체길이 - سەرپەڕ_درێژی;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ئەرک_نرخ));
        if (직접처리기 != null) {
            직접처리기.پرۆسە_نرخ_تێنووسین(دەیتا, ناوەرۆک_دەستپێك, ناوەرۆک_درێژی);
            return true;
        }
        if (ناوەرۆک_درێژی < 4) {
            return false;
        }
        int 목적포트 = تۆڕ_ئامرازەکان.큰순서짧은정수(دەیتا, ناوەرۆک_دەستپێك + 2);
        Map<Integer, 자료처리기> دەرگا_خشتە = ئەرک_نرخ == 17 ? 사용자자료단위처리기 : ئەرک_نرخ == 6 ? 전송제어처리기 : null;
        if (دەرگا_خشتە == null) {
            return false;
        }
        자료처리기 포트처리기 = دەرگا_خشتە.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.پرۆسە_نرخ_تێنووسین(دەیتا, ناوەرۆک_دەستپێك, ناوەرۆک_درێژی);
        return true;
    }
}

