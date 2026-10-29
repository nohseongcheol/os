// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.स्वकीय;
/** स्वतंत्र केंद्रकाचे प्रमाणित निर्गत. UTF-16 प्रतिनिधी-जोड्या UART वरून UTF-8 मध्ये पाठवल्या जातात. */
public final class आउटपुट {
    private आउटपुट() {}
    public static void लेखन(String पाठ्य) { System.out.print(पाठ्य); }
    public static void ओळ_लिहा(String पाठ्य) { System.out.println(पाठ्य); }
    public static void संख्या_लिहा(int संख्या) { System.out.println(संख्या); }
}
