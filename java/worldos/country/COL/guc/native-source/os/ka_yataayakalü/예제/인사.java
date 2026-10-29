// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
public final class 인사 {
    public static int 시작() {
        ka_yataayakalü.ashajaa("Hello from a separate Java ELF!\n");
        ka_yataayakalü.ashajaa(ka_yataayakalü.실행권한() == 3 ? "USER MODE ring 3\n" : "WRONG PRIVILEGE\n");
        for (int ee_iyatialujuna = 0; ee_iyatialujuna < ka_yataayakalü.인수개수(); ee_iyatialujuna++) {
            ka_yataayakalü.ashajaa("arg: "); ka_yataayakalü.ashajaa(ka_yataayakalü.인수(ee_iyatialujuna)); ka_yataayakalü.ashajaa("\n");
        }
        return ka_yataayakalü.실행권한() == 3 ? 0 : 1;
    }
}
