// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package दक्षिण_अफ़्रीका.JZafOS.आयोजक;

import दक्षिण_अफ़्रीका.JZafOS.कर्नेल.कर्नेल;

public final class आयोजक_स्टार्टअप {
    private आयोजक_स्टार्टअप() {
    }

    public static void main(String[] पैरामीटर_तर्क) {
        कर्नेल कर्नेल_मान = new कर्नेल(new 호스트하드웨어());
        कर्नेल_मान.चलाएँ();
        कर्नेल_मान.निष्पादित_करें_चरण();
    }
}

