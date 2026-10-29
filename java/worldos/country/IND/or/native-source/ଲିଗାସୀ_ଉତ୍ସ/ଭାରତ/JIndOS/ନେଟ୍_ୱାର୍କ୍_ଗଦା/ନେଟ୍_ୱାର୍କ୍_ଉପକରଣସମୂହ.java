// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package ଭାରତ.JIndOS.ନେଟ୍_ୱାର୍କ୍_ଗଦା;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 ବାଇଟ୍_ମୂଲ୍ୟ 순서와 ଚେକସୁମ୍ 도구다. */
public final class ନେଟ୍_ୱାର୍କ୍_ଉପକରଣସମୂହ {
    private ନେଟ୍_ୱାର୍କ୍_ଉପକରଣସମୂହ() {
    }

    public static int 큰순서짧은정수(byte[] ଡାଟା, int ଅବସ୍ଥାନ) {
        범위확인(ଡାଟା, ଅବସ୍ଥାନ, 2);
        return ((ଡାଟା[ଅବସ୍ଥାନ] & 0xff) << 8) | (ଡାଟା[ଅବସ୍ଥାନ + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] ଡାଟା, int ଅବସ୍ଥାନ) {
        범위확인(ଡାଟା, ଅବସ୍ଥାନ, 4);
        return ((long) (ଡାଟା[ଅବସ୍ଥାନ] & 0xff) << 24)
                | ((long) (ଡାଟା[ଅବସ୍ଥାନ + 1] & 0xff) << 16)
                | ((long) (ଡାଟା[ଅବସ୍ଥାନ + 2] & 0xff) << 8)
                | (ଡାଟା[ଅବସ୍ଥାନ + 3] & 0xffL);
    }

    public static int କ୍ଲାଉଡ୍_ଚେକସୁମ୍(byte[] ଡାଟା, int ଚଳାନ୍ତୁ, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
        범위확인(ଡାଟା, ଚଳାନ୍ତୁ, ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ);
        long 합 = 0;
        int 끝 = ଚଳାନ୍ତୁ + ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ;
        int ଅବସ୍ଥାନ = ଚଳାନ୍ତୁ;
        while (ଅବସ୍ଥାନ + 1 < 끝) {
            합 += 큰순서짧은정수(ଡାଟା, ଅବସ୍ଥାନ);
            ଅବସ୍ଥାନ += 2;
        }
        if (ଅବସ୍ଥାନ < 끝) {
            합 += (ଡାଟା[ଅବସ୍ଥାନ] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଇଥରନେଟ୍_ଫ୍ରେମ୍(byte[] ଡାଟା) {
        return ଡାଟା != null && ଡାଟା.length >= 14;
    }

    public static int 이더넷상위규약(byte[] ଡାଟା) {
        if (!ସୂଚନା_ପ୍ରଯୁକ୍ତିବିଦ୍ୟା_ଇଥରନେଟ୍_ଫ୍ରେମ୍(ଡାଟା)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(ଡାଟା, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] ଡାଟା, int ଅବସ୍ଥାନ) {
        if (ଡାଟା == null || ଅବସ୍ଥାନ < 0 || ଡାଟା.length - ଅବସ୍ଥାନ < 20) {
            return false;
        }
        int ସଂସ୍କରଣ_ମୂଲ୍ୟ = (ଡାଟା[ଅବସ୍ଥାନ] >>> 4) & 0xf;
        int ଶୀର୍ଷକ_ଦୈର୍ଘ୍ୟ = (ଡାଟା[ଅବସ୍ଥାନ] & 0xf) * 4;
        return ସଂସ୍କରଣ_ମୂଲ୍ୟ == 4 && ଶୀର୍ଷକ_ଦୈର୍ଘ୍ୟ >= 20 && ଡାଟା.length - ଅବସ୍ଥାନ >= ଶୀର୍ଷକ_ଦୈର୍ଘ୍ୟ;
    }

    private static void 범위확인(byte[] ଡାଟା, int ଚଳାନ୍ତୁ, int ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
        if (ଡାଟା == null || ଚଳାନ୍ତୁ < 0 || ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ < 0 || ଚଳାନ୍ତୁ > ଡାଟା.length - ଦୈର୍ଘ୍ୟ_ମୂଲ୍ୟ) {
            throw new IllegalArgumentException("ନେଟ୍_ୱାର୍କ୍_ଗଦା ଡାଟା 범위를 벗어났습니다.");
        }
    }
}

