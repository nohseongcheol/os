// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ନେଟ୍_ୱାର୍କ୍_ଗଦା;

import java.util.HashMap;
import java.util.Map;

/** Ethernet, ARP, IPv4, ICMP, UDP, TCP 수신 분배를 한곳에서 관리한다. */
public final class ନେଟ୍_ୱାର୍କ୍_ସ୍ତର {
    @FunctionalInterface
    public interface 자료처리기 {
        void ପ୍ରୋସେସ୍_ମୂଲ୍ୟ_ଏଣ୍ଟ୍ରି(byte[] ଡାଟା, int ଚଳାନ୍ତୁ, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
    }

    private final Map<Integer, 자료처리기> 이더넷처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 상호통신망처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 사용자자료단위처리기 = new HashMap<Integer, 자료처리기>();
    private final Map<Integer, 자료처리기> 전송제어처리기 = new HashMap<Integer, 자료처리기>();

    public void ପଞ୍ଜିକରଣ_କରନ୍ତୁ_ଇଥରନେଟ୍(int 종류, 자료처리기 처리기) {
        이더넷처리기.put(Integer.valueOf(종류 & 0xffff), 처리기);
    }

    public void ପଞ୍ଜିକରଣ_କରନ୍ତୁ_ଇଣ୍ଟର୍ନେଟ୍_ପ୍ରୋଟୋକଲ୍(int କର୍ମ_ମୂଲ୍ୟ, 자료처리기 처리기) {
        상호통신망처리기.put(Integer.valueOf(କର୍ମ_ମୂଲ୍ୟ & 0xff), 처리기);
    }

    public void ପଞ୍ଜିକରଣ_କରନ୍ତୁ_ଉପଭୋକ୍ତା_ଡାଟା_ଶିକ୍ଷା(int ହାର୍ଡୱେର୍_ପୋର୍ଟ, 자료처리기 처리기) {
        사용자자료단위처리기.put(Integer.valueOf(ହାର୍ଡୱେର୍_ପୋର୍ଟ & 0xffff), 처리기);
    }

    public void ପଞ୍ଜିକରଣ_କରନ୍ତୁ_ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ(int ହାର୍ଡୱେର୍_ପୋର୍ଟ, 자료처리기 처리기) {
        전송제어처리기.put(Integer.valueOf(ହାର୍ଡୱେର୍_ପୋର୍ଟ & 0xffff), 처리기);
    }

    public boolean 이더넷받기(byte[] ଫ୍ରେମ୍_ଅନୁକ୍ରମଣିକା) {
        if (!ନେଟ୍_ୱାର୍କ୍_ଉପକରଣସମୂହ.ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଇଥରନେଟ୍_ଫ୍ରେମ୍(ଫ୍ରେମ୍_ଅନୁକ୍ରମଣିକା)) {
            return false;
        }
        int 종류 = ନେଟ୍_ୱାର୍କ୍_ଉପକରଣସମୂହ.이더넷상위규약(ଫ୍ରେମ୍_ଅନୁକ୍ରମଣିକା);
        자료처리기 직접처리기 = 이더넷처리기.get(Integer.valueOf(종류));
        if (직접처리기 != null) {
            직접처리기.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ_ଏଣ୍ଟ୍ରି(ଫ୍ରେମ୍_ଅନୁକ୍ରମଣିକା, 14, ଫ୍ରେମ୍_ଅନୁକ୍ରମଣିକା.length - 14);
            return true;
        }
        return 종류 == 0x0800 && 상호통신망받기(ଫ୍ରେମ୍_ଅନୁକ୍ରମଣିକା, 14);
    }

    private boolean 상호통신망받기(byte[] ଡାଟା, int ଚଳାନ୍ତୁ) {
        if (!ନେଟ୍_ୱାର୍କ୍_ଉପକରଣସମୂହ.상호통신망규약사판인가(ଡାଟା, ଚଳାନ୍ତୁ)) {
            return false;
        }
        int ଶୀର୍ଷକ_ଦୈର୍ଘ୍ୟ = (ଡାଟା[ଚଳାନ୍ତୁ] & 0x0f) * 4;
        int 전체길이 = ନେଟ୍_ୱାର୍କ୍_ଉପକରଣସମୂହ.큰순서짧은정수(ଡାଟା, ଚଳାନ୍ତୁ + 2);
        if (전체길이 < ଶୀର୍ଷକ_ଦୈର୍ଘ୍ୟ || ଚଳାନ୍ତୁ + 전체길이 > ଡାଟା.length) {
            return false;
        }
        int କର୍ମ_ମୂଲ୍ୟ = ଡାଟା[ଚଳାନ୍ତୁ + 9] & 0xff;
        int ବିଷୟ_ଆରମ୍ଭ = ଚଳାନ୍ତୁ + ଶୀର୍ଷକ_ଦୈର୍ଘ୍ୟ;
        int ବିଷୟ_ଦୈର୍ଘ୍ୟ = 전체길이 - ଶୀର୍ଷକ_ଦୈର୍ଘ୍ୟ;
        자료처리기 직접처리기 = 상호통신망처리기.get(Integer.valueOf(କର୍ମ_ମୂଲ୍ୟ));
        if (직접처리기 != null) {
            직접처리기.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ_ଏଣ୍ଟ୍ରି(ଡାଟା, ବିଷୟ_ଆରମ୍ଭ, ବିଷୟ_ଦୈର୍ଘ୍ୟ);
            return true;
        }
        if (ବିଷୟ_ଦୈର୍ଘ୍ୟ < 4) {
            return false;
        }
        int ଲକ୍ଷସ୍ଥଳ_ପୋର୍ଟ୍_ନମ୍ଵର୍ = ନେଟ୍_ୱାର୍କ୍_ଉପକରଣସମୂହ.큰순서짧은정수(ଡାଟା, ବିଷୟ_ଆରମ୍ଭ + 2);
        Map<Integer, 자료처리기> ପୋର୍ଟ_ସାରଣୀ = କର୍ମ_ମୂଲ୍ୟ == 17 ? 사용자자료단위처리기 : କର୍ମ_ମୂଲ୍ୟ == 6 ? 전송제어처리기 : null;
        if (ପୋର୍ଟ_ସାରଣୀ == null) {
            return false;
        }
        자료처리기 포트처리기 = ପୋର୍ଟ_ସାରଣୀ.get(Integer.valueOf(ଲକ୍ଷସ୍ଥଳ_ପୋର୍ଟ୍_ନମ୍ଵର୍));
        if (포트처리기 == null) {
            return false;
        }
        포트처리기.ପ୍ରୋସେସ୍_ମୂଲ୍ୟ_ଏଣ୍ଟ୍ରି(ଡାଟା, ବିଷୟ_ଆରମ୍ଭ, ବିଷୟ_ଦୈର୍ଘ୍ୟ);
        return true;
    }
}

