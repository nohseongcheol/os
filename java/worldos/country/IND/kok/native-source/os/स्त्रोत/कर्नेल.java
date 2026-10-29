// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** प्रत्यक्ष_डेटा 부팅 후 호출되는 Java प्रवेश_पॉयंट. JVM과 येजमान 운영체제에 의존하지 않는다. */
public final class कर्नेल {
    static int 합계(int 끝) {
        int SUM_मोल = 0;
        for (int INDEX = 1; INDEX <= 끝; INDEX++) SUM_मोल += INDEX;
        return SUM_मोल;
    }

    static boolean 시험() {
        int[] 값들 = new int[4];
        값들[2] = 합계(10);
        int 음수 = -7;
        int 최소 = 0x80000000;
        int भागाकार_मेजप = -1;
        int INDEX = 기억공간.नेमून_दिवचें_सांठवण();
        boolean पास_मोल = 값들[0] == 0 && 값들[2] == 55 && 값들.length == 4
            && 음수 / 3 == -2 && 음수 % 3 == -1 && 최소 / भागाकार_मेजप == 최소
            && 최소 % भागाकार_मेजप == 0 && "한글".length() == 2 && "한글".charAt(1) == '글'
            && INDEX >= 0 && 기억공간.return_मेजप(INDEX) && !기억공간.return_मेजप(INDEX);
        SMS_टर्मिनल.बरोवचें(पास_मोल ? "JAVA SELFTEST PASS\n" : "JAVA SELFTEST FAIL\n");
        return पास_मोल;
    }

    public static void चलोवप() {
        SMS_टर्मिनल.तयार_करचें_9ce364fc();
        SMS_टर्मिनल.बरोवचें("JKOROS NATIVE JAVA\n");
        SMS_टर्मिनल.बरोवचें("자바 기계어 कर्नेल_मोल चलोवप\n");
        if (मोबायल_मोल.부팅표식() != 0x2badb002) {
            SMS_टर्मिनल.बरोवचें("BAD MULTIBOOT MAGIC\n");
            मोबायल_मोल.정지();
        }
        if (!시험()) मोबायल_मोल.정지();
        if (기억공간.UPPER_मेमरी_आवाठ() < 15360) {
            SMS_टर्मिनल.बरोवचें("At least 16 MiB RAM required\n");
            मोबायल_मोल.정지();
        }
        मोबायल_मोल.तयार_करचें_उपेगकर्तो_एप्लिकेशन();
        SMS_टर्मिनल.बरोवचें("USER ELF: ring 3 / paging / int 0x80\n");
        नॅटवर्क_ड्रायव्हर.तयार_करचें_9ce364fc();
        नॅटवर्क_स्टॅक.नितळ_प्रक्रिया();
        मेमरी_फायल_प्रणाली.तयार_करचें_9ce364fc();
        파일보존.तयार_करचें_9ce364fc();
        명령해석기.चलोवप();
    }
}
