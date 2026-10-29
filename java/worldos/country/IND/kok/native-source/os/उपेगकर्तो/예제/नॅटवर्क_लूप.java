// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 최대 आवाठ/홀수 लांबाय_मोल 데이터그램으로 प्रत्यक्ष_डेटा RTL8139 수신 लूप_मोल 순환을 시험한다. */
public final class नॅटवर्क_लूप {
    public static int चलोवप() {
        if (उपेगकर्तो.인수개수() != 1) { उपेगकर्तो.बरोवचें("Usage: run stress PORT\n"); return 2; }
        String SMS = उपेगकर्तो.인수(0);
        int पोर्ट_मोल = 0;
        for (int INDEX = 0; INDEX < SMS.length(); INDEX++) {
            if (SMS.charAt(INDEX) < '0' || SMS.charAt(INDEX) > '9' || पोर्ट_मोल > 6553) return 2;
            पोर्ट_मोल = पोर्ट_मोल * 10 + SMS.charAt(INDEX) - '0';
        }
        if (पोर्ट_मोल < 1 || पोर्ट_मोल > 65535) return 2;
        int हँडल_मोल = उपेगकर्तो.उगडचें_नॅटवर्क(0);
        if (हँडल_मोल < 0) return 3;
        int[] डेटा = new int[1024];
        for (int 회차 = 0; 회차 < 24; 회차++) {
            int लांबाय_मोल = 1024 - (회차 & 1);
            for (int INDEX = 0; INDEX < लांबाय_मोल; INDEX++) डेटा[INDEX] = (INDEX + 회차) & 255;
            if (उपेगकर्तो.धाडचें_डेटा(हँडल_मोल, 0x0a000202, पोर्ट_मोल, डेटा, लांबाय_मोल) != लांबाय_मोल) return 4;
            if (उपेगकर्तो.자료받기(हँडल_मोल, डेटा, 300) != लांबाय_मोल) return 5;
            for (int INDEX = 0; INDEX < लांबाय_मोल; INDEX++) if (डेटा[INDEX] != ((INDEX + 회차) & 255)) return 6;
        }
        उपेगकर्तो.शेवट_नॅटवर्क(हँडल_मोल);
        उपेगकर्तो.बरोवचें("UDP STRESS PASS: 24 full/odd datagrams\n");
        return 0;
    }
}
