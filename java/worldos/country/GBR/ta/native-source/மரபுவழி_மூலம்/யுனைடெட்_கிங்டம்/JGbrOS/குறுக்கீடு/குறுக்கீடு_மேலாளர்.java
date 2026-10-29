// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package யுனைடெட்_கிங்டம்.JGbrOS.குறுக்கீடு;

import java.util.Arrays;

/** IDT의 Java 관리 측 처리기 등록과 분배를 담당한다. */
public final class குறுக்கீடு_மேலாளர் {
    private final 개입중단처리기[] 처리기들 = new 개입중단처리기[256];
    private boolean இயக்க;

    public void பதிவு_செய்_உள்ளீடு(int அடைவு, 개입중단처리기 처리기) {
        번호확인(அடைவு);
        처리기들[அடைவு] = 처리기;
    }

    public void அனுப்பு_சேமிப்பகம்(int அடைவு) {
        번호확인(அடைவு);
        처리기들[அடைவு] = null;
    }

    public int விநியோகி_மதிப்பு(int அடைவு, int 저장된쌓임주소) {
        번호확인(அடைவு);
        if (!இயக்க) {
            return 저장된쌓임주소;
        }
        개입중단처리기 처리기 = 처리기들[அடைவு];
        return 처리기 == null ? 저장된쌓임주소 : 처리기.செயலகம்_மதிப்பு_உள்ளீடு(저장된쌓임주소);
    }

    public void இயக்கு_0b9ce0d7() {
        இயக்க = true;
    }

    public void செயலிழக்கச்_செய்() {
        இயக்க = false;
    }

    public boolean தகவல்_தொழில்நுட்பம்_இயக்க() {
        return இயக்க;
    }

    public void 모두해제() {
        Arrays.fill(처리기들, null);
    }

    private void 번호확인(int அடைவு) {
        if (அடைவு < 0 || அடைவு >= 처리기들.length) {
            throw new IllegalArgumentException("குறுக்கீடு 번호가 올바르지 않습니다.");
        }
    }
}

