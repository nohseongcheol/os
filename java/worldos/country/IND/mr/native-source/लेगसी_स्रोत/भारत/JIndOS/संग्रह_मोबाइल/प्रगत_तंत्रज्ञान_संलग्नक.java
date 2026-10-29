// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.संग्रह_मोबाइल;

import java.util.Arrays;

/** ATA 28-बिट आज्ञास्तराशी जुळणारे 512 बाइट तार्किक क्षेत्राचे साधन. */
public final class प्रगत_तंत्रज्ञान_संलग्नक {
    public static final int विभाग_आकारा = 512;
    private final byte[] डेटा;
    private final boolean केवळ_मूल्य_वाचा;

    public प्रगत_तंत्रज्ञान_संलग्नक(int विभाग_संख्या, boolean केवळ_मूल्य_वाचा) {
        if (विभाग_संख्या <= 0) {
            throw new IllegalArgumentException("विभाग_मूल्य 수가 올바르지 않습니다.");
        }
        डेटा = new byte[Math.multiplyExact(विभाग_संख्या, विभाग_आकारा)];
        this.केवळ_मूल्य_वाचा = केवळ_मूल्य_वाचा;
    }

    public int विभाग_संख्या() {
        return डेटा.length / विभाग_आकारा;
    }

    public void वाचन(int विभाग_अनुक्रमणिका, byte[] गंतव्यस्थान_स्वीकारा) {
        व्याप्ती_तपासा(विभाग_अनुक्रमणिका, गंतव्यस्थान_स्वीकारा);
        System.arraycopy(डेटा, विभाग_अनुक्रमणिका * विभाग_आकारा, गंतव्यस्थान_स्वीकारा, 0, विभाग_आकारा);
    }

    public void लेखन(int विभाग_अनुक्रमणिका, byte[] डेटा_कडे_लिहा) {
        if (केवळ_मूल्य_वाचा) {
            throw new IllegalStateException("वाचन 전용 장치입니다.");
        }
        व्याप्ती_तपासा(विभाग_अनुक्रमणिका, डेटा_कडे_लिहा);
        System.arraycopy(डेटा_कडे_लिहा, 0, डेटा, विभाग_अनुक्रमणिका * विभाग_आकारा, विभाग_आकारा);
    }

    public void पुसा_प्रविष्टी() {
        if (केवळ_मूल्य_वाचा) {
            throw new IllegalStateException("वाचन 전용 장치입니다.");
        }
        Arrays.fill(डेटा, (byte) 0);
    }

    private void व्याप्ती_तपासा(int विभाग_अनुक्रमणिका, byte[] तात्पुरते_जागा) {
        if (विभाग_अनुक्रमणिका < 0 || विभाग_अनुक्रमणिका >= विभाग_संख्या() || तात्पुरते_जागा.length < विभाग_आकारा) {
            throw new IllegalArgumentException("ATA विभाग_मूल्य 범위가 올바르지 않습니다.");
        }
    }
}

