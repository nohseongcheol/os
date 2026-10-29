// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package Россия.JRusOS.Саклагыч_мобиль;

import java.util.Arrays;

/** ATA 28비트 команда 계층과 같은 512바이트 논리 өлеш_VALUE 장치다. */
public final class 고급기술결합장치 {
    public static final int өлеш_үлчәмен_үзгәртү = 512;
    private final byte[] мәгълүмат;
    private final boolean укымалы_гына_VALUE;

    public 고급기술결합장치(int өлеш_COUNT, boolean укымалы_гына_VALUE) {
        if (өлеш_COUNT <= 0) {
            throw new IllegalArgumentException("өлеш_VALUE 수가 올바르지 않습니다.");
        }
        мәгълүмат = new byte[Math.multiplyExact(өлеш_COUNT, өлеш_үлчәмен_үзгәртү)];
        this.укымалы_гына_VALUE = укымалы_гына_VALUE;
    }

    public int өлеш_COUNT() {
        return мәгълүмат.length / өлеш_үлчәмен_үзгәртү;
    }

    public void 읽기(int өлеш_INDEX, byte[] 받을곳) {
        범위확인(өлеш_INDEX, 받을곳);
        System.arraycopy(мәгълүмат, өлеш_INDEX * өлеш_үлчәмен_үзгәртү, 받을곳, 0, өлеш_үлчәмен_үзгәртү);
    }

    public void язу(int өлеш_INDEX, byte[] 쓸자료) {
        if (укымалы_гына_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        범위확인(өлеш_INDEX, 쓸자료);
        System.arraycopy(쓸자료, 0, мәгълүмат, өлеш_INDEX * өлеш_үлчәмен_үзгәртү, өлеш_үлчәмен_үзгәртү);
    }

    public void 지우기() {
        if (укымалы_гына_VALUE) {
            throw new IllegalStateException("읽기 전용 장치입니다.");
        }
        Arrays.fill(мәгълүмат, (byte) 0);
    }

    private void 범위확인(int өлеш_INDEX, byte[] 임시공간) {
        if (өлеш_INDEX < 0 || өлеш_INDEX >= өлеш_COUNT() || 임시공간.length < өлеш_үлчәмен_үзгәртү) {
            throw new IllegalArgumentException("ATA өлеш_VALUE 범위가 올바르지 않습니다.");
        }
    }
}

