// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package फ़िजी.JFjiOS.कर्नेल;

import फ़िजी.JFjiOS.मेमोरी_क्षेत्र.मेमोरी_प्रबंधक;
import फ़िजी.JFjiOS.मेमोरी_क्षेत्र.पेज_प्रबंधक;
import फ़िजी.JFjiOS.입력.입력관리자;
import फ़िजी.JFjiOS.작업.प्रक्रिया_मान;
import फ़िजी.JFjiOS.작업.शेड्यूलर;
import फ़िजी.JFjiOS.체계호출.체계호출;
import फ़िजी.JFjiOS.फ़ाइल_सिस्टम.파일서술자표;
import फ़िजी.JFjiOS.फ़ाइल_सिस्टम.फ़ाइल_सिस्टम;

/** Java 관리 커널의 조립과 시작을 담당한다. */
public final class कर्नेल {
    private final 하드웨어 उपकरण_मान;
    private final मेमोरी_प्रबंधक मेमोरी_क्षेत्र = new मेमोरी_प्रबंधक(32 * 1024 * 1024);
    private final पेज_प्रबंधक 쪽관리 = new पेज_प्रबंधक();
    private final फ़ाइल_सिस्टम फ़ाइल_सिस्टम = new फ़ाइल_सिस्टम();
    private final शेड्यूलर शेड्यूलर = new शेड्यूलर(쪽관리);
    private final 입력관리자 입력관리 = new 입력관리자(256);
    private final प्रक्रिया_मान 첫과정;
    private final 체계호출 체계호출;

    public कर्नेल(하드웨어 उपकरण_मान) {
        this.उपकरण_मान = उपकरण_मान;
        첫과정 = शेड्यूलर.첫과정(new 파일서술자표(फ़ाइल_सिस्टम));
        체계호출 = new 체계호출(फ़ाइल_सिस्टम, 쪽관리, शेड्यूलर, उपकरण_मान, 입력관리);
    }

    public void चलाएँ() {
        उपकरण_मान.직렬출력("=== JFjiOS 관리 कर्नेल_मान ===\n");
    }

    public void निष्पादित_करें_चरण() {
        उपकरण_मान.중앙처리장치멈춤();
    }

    public मेमोरी_प्रबंधक मेमोरी_क्षेत्र() {
        return मेमोरी_क्षेत्र;
    }

    public पेज_प्रबंधक 쪽관리() {
        return 쪽관리;
    }

    public फ़ाइल_सिस्टम फ़ाइल_सिस्टम() {
        return फ़ाइल_सिस्टम;
    }

    public शेड्यूलर शेड्यूलर() {
        return शेड्यूलर;
    }

    public 입력관리자 입력관리() {
        return 입력관리;
    }

    public प्रक्रिया_मान 첫과정() {
        return 첫과정;
    }

    public 체계호출 체계호출() {
        return 체계호출;
    }
}
