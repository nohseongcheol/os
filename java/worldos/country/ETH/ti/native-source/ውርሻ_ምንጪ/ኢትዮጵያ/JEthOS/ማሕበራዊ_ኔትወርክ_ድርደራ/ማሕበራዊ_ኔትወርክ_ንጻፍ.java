// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ኢትዮጵያ.JEthOS.ማሕበራዊ_ኔትወርክ_ድርደራ;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ማሕበራዊ_ኔትወርክ_ንጻፍ {
    @FunctionalInterface
    public interface 자료처리기 {
        void መስርሕ_ዋጋ_ምእታው(byte[] ሓበሬታ, int ኣኺድ, int ንውሓት_ዋጋ);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void 이더넷등록(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void 상호통신망등록(int ዕዮ_ዋጋ_102996da, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(ዕዮ_ዋጋ_102996da & 0xff), 처리기);
    }

    public void 사용자자료단위등록(int ሃርድዌር_ወደብ, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(ሃርድዌር_ወደብ & 0xffff), 처리기);
    }

    public void 전송제어등록(int ሃርድዌር_ወደብ, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(ሃርድዌር_ወደብ & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ከፈፍ_መሐበሪ) {
        if (!ማሕበራዊ_ኔትወርክ_መሳርሒታት.이더넷틀인가(ከፈፍ_መሐበሪ)) {
            return false;
        }
        int 종류 = ማሕበራዊ_ኔትወርክ_መሳርሒታት.이더넷상위규약(ከፈፍ_መሐበሪ);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.መስርሕ_ዋጋ_ምእታው(ከፈፍ_መሐበሪ, 14, ከፈፍ_መሐበሪ.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ከፈፍ_መሐበሪ, 14);
    }

    private boolean 상호통신망받기(byte[] ሓበሬታ, int ኣኺድ) {
        if (!ማሕበራዊ_ኔትወርክ_መሳርሒታት.상호통신망규약사판인가(ሓበሬታ, ኣኺድ)) {
            return false;
        }
        int ርእሲ_ንውሓት = (ሓበሬታ[ኣኺድ] & 0x0f) * 4;
        int 전체길이 = ማሕበራዊ_ኔትወርክ_መሳርሒታት.큰순서짧은정수(ሓበሬታ, ኣኺድ + 2);
        if (전체길이 < ርእሲ_ንውሓት || ኣኺድ + 전체길이 > ሓበሬታ.length) {
            return false;
        }
        int ዕዮ_ዋጋ_102996da = ሓበሬታ[ኣኺድ + 9] & 0xff;
        int ትሕዝቶ_ጀምር = ኣኺድ + ርእሲ_ንውሓት;
        int ትሕዝቶ_ንውሓት = 전체길이 - ርእሲ_ንውሓት;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(ዕዮ_ዋጋ_102996da));
        if (직접처리기 != null) {
            직접처리기.መስርሕ_ዋጋ_ምእታው(ሓበሬታ, ትሕዝቶ_ጀምር, ትሕዝቶ_ንውሓት);
            return true;
        }
        if (ትሕዝቶ_ንውሓት < 4) {
            return false;
        }
        int 목적포트 = ማሕበራዊ_ኔትወርክ_መሳርሒታት.큰순서짧은정수(ሓበሬታ, ትሕዝቶ_ጀምር + 2);
        Map<Integer, 자료처리기> ወደብ_ሰሌዳ = ዕዮ_ዋጋ_102996da == 17 ? 사용자자료단위처리기 : ዕዮ_ዋጋ_102996da == 6 ? 전송제어처리기 : null;
        if (ወደብ_ሰሌዳ == null) {
            return false;
        }
        자료처리기 포트처리기 = ወደብ_ሰሌዳ.get(Integer.valueOf(목적포트));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.መስርሕ_ዋጋ_ምእታው(ሓበሬታ, ትሕዝቶ_ጀምር, ትሕዝቶ_ንውሓት);
        return true;
    }
}

