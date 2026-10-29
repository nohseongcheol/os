// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package កម្ពុជា.JKhmOS.ការផ្ទុក_ឧបករណ៍;

import java.util.Arrays;

/** ATA 28비트 ពាក្យ_បញ្ជា 계층과 같은 512바이트 논리 ផ្នែក_តំលៃ 장치다. */
public final class 고급기술결합장치 {
    public static final int ផ្នែក_ដាក់ទំហំ = 512;
    private final byte[] ទិន្នន័យ;
    private final boolean ដែលបានត្រឹមតែអាន_តំលៃ;

    public 고급기술결합장치(int 구역수, boolean ដែលបានត្រឹមតែអាន_តំលៃ) {
        if (구역수 <= 0) {
            throw new IllegalArgumentException("ផ្នែក_តំលៃ 수가 올바르지 않습니다.");
        }
        ទិន្នន័យ = new byte[Math.multiplyExact(구역수, ផ្នែក_ដាក់ទំហំ)];
        this.ដែលបានត្រឹមតែអាន_តំលៃ = ដែលបានត្រឹមតែអាន_តំលៃ;
    }

    public int 구역수() {
        return ទិន្នន័យ.length / ផ្នែក_ដាក់ទំហំ;
    }

    public void អាន(int ផ្នែក_សន្ទស្សន៏, byte[] 받을곳) {
        범위확인(ផ្នែក_សន្ទស្សន៏, 받을곳);
        System.arraycopy(ទិន្នន័យ, ផ្នែក_សន្ទស្សន៏ * ផ្នែក_ដាក់ទំហំ, 받을곳, 0, ផ្នែក_ដាក់ទំហំ);
    }

    public void សរសេរ(int ផ្នែក_សន្ទស្សន៏, byte[] 쓸자료) {
        if (ដែលបានត្រឹមតែអាន_តំលៃ) {
            throw new IllegalStateException("អាន 전용 장치입니다.");
        }
        범위확인(ផ្នែក_សន្ទស្សន៏, 쓸자료);
        System.arraycopy(쓸자료, 0, ទិន្នន័យ, ផ្នែក_សន្ទស្សន៏ * ផ្នែក_ដាក់ទំហំ, ផ្នែក_ដាក់ទំហំ);
    }

    public void លុប_ការបញ្ចូល() {
        if (ដែលបានត្រឹមតែអាន_តំលៃ) {
            throw new IllegalStateException("អាន 전용 장치입니다.");
        }
        Arrays.fill(ទិន្នន័យ, (byte) 0);
    }

    private void 범위확인(int ផ្នែក_សន្ទស្សន៏, byte[] 임시공간) {
        if (ផ្នែក_សន្ទស្សន៏ < 0 || ផ្នែក_សន្ទស្សន៏ >= 구역수() || 임시공간.length < ផ្នែក_ដាក់ទំហំ) {
            throw new IllegalArgumentException("ATA ផ្នែក_តំលៃ 범위가 올바르지 않습니다.");
        }
    }
}

