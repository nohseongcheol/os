// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 첫 네트워크 थर_मोल: 단일 कर्नेल_मोल 안의 IPv4/UDP 루프백 ट्रान्सफर_मोल.
 * 외부 IP는 ENETUNREACH. Ethernet/IP 패킷 드라이버를 대신한다고 표시하지 않는다.
 * सोपोवचें_पॉयंट 8개, 끝점당 전문 4개, 전문당 512바이트. 모든 호출은 비차단이다.
 */
public final class 되돌림망 {
    static int[] 사용 = new int[8];
    static int[] पोर्ट_मोल = new int[8];
    static int[] नामो = new int[8];
    static int[] 앞 = new int[8];
    static int[] आयटम_COUNT = new int[8];
    static int[] RECEIVED_पोर्ट = new int[8];
    static int[] लांबाय_मोल = new int[32];
    static int[] 보낸창구 = new int[32];
    static int[] डेटा = new int[32 * 512];
    static int[] फॉर्वर्ड_मोल = new int[512];
    static int 다음창구 = 49152;
    static int पुनर्तपासणी_करची(int INDEX) { return INDEX >= 32 && INDEX < 40 && 사용[INDEX - 32] != 0 ? INDEX - 32 : -1; }
    static boolean 겹침(int INDEX) {
        for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < 8; स्लॉट_प्रवेश++) if (사용[स्लॉट_प्रवेश] != 0 && पोर्ट_मोल[स्लॉट_प्रवेश] == INDEX) return true;
        return false;
    }
    static int 임시창구() {
        for (int 시도 = 0; 시도 < 16; 시도++) {
            int 후보 = 다음창구++;
            if (다음창구 > 65535) 다음창구 = 49152;
            if (!겹침(후보)) return 후보;
        }
        return -98;
    }
    public static int निर्माण_करचें_प्रवेश(int 영역, int 종류, int काम_मोल) {
        if (영역 != 2) return -97;
        if (종류 != 2 || (काम_मोल != 0 && काम_मोल != 17)) return -93;
        for (int स्लॉट_प्रवेश = 0; स्लॉट_प्रवेश < 8; स्लॉट_प्रवेश++) if (사용[स्लॉट_प्रवेश] == 0) {
            사용[स्लॉट_प्रवेश] = 1; पोर्ट_मोल[स्लॉट_प्रवेश] = 0; नामो[स्लॉट_प्रवेश] = 0; 앞[स्लॉट_प्रवेश] = 0; आयटम_COUNT[स्लॉट_प्रवेश] = 0; RECEIVED_पोर्ट[स्लॉट_प्रवेश] = 0;
            return स्लॉट_प्रवेश + 32;
        }
        return -24;
    }
    public static int 묶기(int INDEX, int नॅटवर्क_नामो, int 창구번호) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(INDEX);
        if (स्लॉट_प्रवेश < 0) return -9;
        if (नॅटवर्क_नामो != 0 && नॅटवर्क_नामो != 0x7f000001) return -99;
        if (पोर्ट_मोल[स्लॉट_प्रवेश] != 0 || 창구번호 < 0 || 창구번호 > 65535) return -22;
        if (창구번호 == 0) 창구번호 = 임시창구();
        if (창구번호 < 0) return 창구번호;
        if (겹침(창구번호)) return -98;
        पोर्ट_मोल[स्लॉट_प्रवेश] = 창구번호; नामो[स्लॉट_प्रवेश] = नॅटवर्क_नामो; return 0;
    }
    public static int 자료넣기(int INDEX, int मोल) {
        if (INDEX < 0 || INDEX >= 512) return -22;
        फॉर्वर्ड_मोल[INDEX] = मोल & 255; return 0;
    }
    public static int 자료읽기(int INDEX) { return INDEX >= 0 && INDEX < 512 ? फॉर्वर्ड_मोल[INDEX] : -22; }
    public static int धाडचें(int INDEX, int नॅटवर्क_नामो, int 창구번호, int आवाठ) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(INDEX);
        if (स्लॉट_प्रवेश < 0) return -9;
        if (नॅटवर्क_नामो != 0x7f000001) return -101;
        if (창구번호 < 1 || 창구번호 > 65535) return -22;
        if (आवाठ < 0 || आवाठ > 512) return -90;
        if (पोर्ट_मोल[स्लॉट_प्रवेश] == 0) {
            int मेजप = 묶기(INDEX, 0x7f000001, 0);
            if (मेजप < 0) return मेजप;
        }
        int नियुक्त_स्थान_मोल = -1;
        for (int 후보 = 0; 후보 < 8; 후보++) if (사용[후보] != 0 && पोर्ट_मोल[후보] == 창구번호) नियुक्त_स्थान_मोल = 후보;
        if (नियुक्त_स्थान_मोल < 0) return -111;
        if (आयटम_COUNT[नियुक्त_स्थान_मोल] == 4) return -11;
        int स्थिती_INDEX = नियुक्त_स्थान_मोल * 4 + (앞[नियुक्त_स्थान_मोल] + आयटम_COUNT[नियुक्त_स्थान_मोल]) % 4;
        for (int बायट_मोल = 0; बायट_मोल < आवाठ; बायट_मोल++) डेटा[स्थिती_INDEX * 512 + बायट_मोल] = फॉर्वर्ड_मोल[बायट_मोल];
        लांबाय_मोल[स्थिती_INDEX] = आवाठ; 보낸창구[स्थिती_INDEX] = पोर्ट_मोल[स्लॉट_प्रवेश]; आयटम_COUNT[नियुक्त_स्थान_मोल]++;
        return आवाठ;
    }
    public static int 받기(int INDEX, int 용량) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(INDEX);
        if (स्लॉट_प्रवेश < 0) return -9;
        if (용량 < 0 || 용량 > 512) return -22;
        if (आयटम_COUNT[स्लॉट_प्रवेश] == 0) return -11;
        int स्थिती_INDEX = स्लॉट_प्रवेश * 4 + 앞[स्लॉट_प्रवेश];
        int आवाठ = लांबाय_मोल[स्थिती_INDEX] < 용량 ? लांबाय_मोल[स्थिती_INDEX] : 용량;
        for (int बायट_मोल = 0; बायट_मोल < आवाठ; बायट_मोल++) फॉर्वर्ड_मोल[बायट_मोल] = डेटा[स्थिती_INDEX * 512 + बायट_मोल];
        RECEIVED_पोर्ट[स्लॉट_प्रवेश] = 보낸창구[स्थिती_INDEX]; 앞[स्लॉट_प्रवेश] = (앞[स्लॉट_प्रवेश] + 1) % 4; आयटम_COUNT[स्लॉट_प्रवेश]--;
        return आवाठ;
    }
    public static int 창구읽기(int INDEX) { int स्लॉट_प्रवेश = पुनर्तपासणी_करची(INDEX); return स्लॉट_प्रवेश < 0 ? -9 : पोर्ट_मोल[स्लॉट_प्रवेश]; }
    public static int 주소읽기(int INDEX) { int स्लॉट_प्रवेश = पुनर्तपासणी_करची(INDEX); return स्लॉट_प्रवेश < 0 ? -9 : नामो[स्लॉट_प्रवेश]; }
    public static int 보낸곳(int INDEX) { int स्लॉट_प्रवेश = पुनर्तपासणी_करची(INDEX); return स्लॉट_प्रवेश < 0 ? -9 : RECEIVED_पोर्ट[स्लॉट_प्रवेश]; }
    public static int शेवट(int INDEX) {
        int स्लॉट_प्रवेश = पुनर्तपासणी_करची(INDEX); if (स्लॉट_प्रवेश < 0) return -9;
        사용[स्लॉट_प्रवेश] = 0; आयटम_COUNT[स्लॉट_प्रवेश] = 0; पोर्ट_मोल[स्लॉट_प्रवेश] = 0; return 0;
    }
}
