// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package மொரிசியஸ்.JMusOS.பிணையம்_அடுக்கு_49fba3da;

/** Ethernet/ARP/IPv4/ICMP/UDP 계층이 공유하는 பைட்_மதிப்பு 순서와 சொதனைக்_கணக்கு 도구다. */
public final class பிணையம்_கருவிகள் {
    private பிணையம்_கருவிகள்() {
    }

    public static int 큰순서짧은정수(byte[] தரவு, int இடம்) {
        범위확인(தரவு, இடம், 2);
        return ((தரவு[இடம்] & 0xff) << 8) | (தரவு[இடம் + 1] & 0xff);
    }

    public static long 큰순서정수(byte[] தரவு, int இடம்) {
        범위확인(தரவு, இடம், 4);
        return ((long) (தரவு[இடம்] & 0xff) << 24)
                | ((long) (தரவு[இடம் + 1] & 0xff) << 16)
                | ((long) (தரவு[இடம் + 2] & 0xff) << 8)
                | (தரவு[இடம் + 3] & 0xffL);
    }

    public static int இணையம்_சொதனைக்_கணக்கு(byte[] தரவு, int செயல்படுத்துக, int நீளம்_மதிப்பு) {
        범위확인(தரவு, செயல்படுத்துக, நீளம்_மதிப்பு);
        long 합 = 0;
        int 끝 = செயல்படுத்துக + நீளம்_மதிப்பு;
        int இடம் = செயல்படுத்துக;
        while (இடம் + 1 < 끝) {
            합 += 큰순서짧은정수(தரவு, இடம்);
            இடம் += 2;
        }
        if (இடம் < 끝) {
            합 += (தரவு[இடம்] & 0xff) << 8;
        }
        while ((합 >>> 16) != 0) {
            합 = (합 & 0xffff) + (합 >>> 16);
        }
        return (int) (~합) & 0xffff;
    }

    public static boolean தகவல்_தொழில்நுட்பம்_ஈத்தர்நெட்_ஃபிரேம்(byte[] தரவு) {
        return தரவு != null && தரவு.length >= 14;
    }

    public static int 이더넷상위규약(byte[] தரவு) {
        if (!தகவல்_தொழில்நுட்பம்_ஈத்தர்நெட்_ஃபிரேம்(தரவு)) {
            throw new IllegalArgumentException("이더넷 틀이 너무 짧습니다.");
        }
        return 큰순서짧은정수(தரவு, 12);
    }

    public static boolean 상호통신망규약사판인가(byte[] தரவு, int இடம்) {
        if (தரவு == null || இடம் < 0 || தரவு.length - இடம் < 20) {
            return false;
        }
        int பதிப்பு_மதிப்பு = (தரவு[இடம்] >>> 4) & 0xf;
        int மேற்குறிப்பு_நீளம் = (தரவு[இடம்] & 0xf) * 4;
        return பதிப்பு_மதிப்பு == 4 && மேற்குறிப்பு_நீளம் >= 20 && தரவு.length - இடம் >= மேற்குறிப்பு_நீளம்;
    }

    private static void 범위확인(byte[] தரவு, int செயல்படுத்துக, int நீளம்_மதிப்பு) {
        if (தரவு == null || செயல்படுத்துக < 0 || நீளம்_மதிப்பு < 0 || செயல்படுத்துக > தரவு.length - நீளம்_மதிப்பு) {
            throw new IllegalArgumentException("பிணையம்_அடுக்கு_49fba3da தரவு 범위를 벗어났습니다.");
        }
    }
}

