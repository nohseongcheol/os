// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.जावा;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class पारपाडा_कार्य {
    private पारपाडा_कार्य() {}
    public static Thread सुरू_करा(String नाव, Runnable कृती) {
        Thread कार्यसूत्र_मूल्य_5b72a632 = new Thread(कृती, नाव);
        कार्यसूत्र_मूल्य_5b72a632.start();
        return कार्यसूत्र_मूल्य_5b72a632;
    }
    public static void प्रतीक्षाकरा(Thread कार्यसूत्र_मूल्य_5b72a632) throws InterruptedException { कार्यसूत्र_मूल्य_5b72a632.join(); }
    public static void उर्वरित_क्षणभर(long मिलिसेकंद) throws InterruptedException { Thread.sleep(मिलिसेकंद); }
    /** आवाहकाने shutdown() वापरून संसाधने परत करावीत. */
    public static ExecutorService कार्यपीठ_मूल्य(int कार्यसूत्र_संख्या) { return Executors.newFixedThreadPool(कार्यसूत्र_संख्या); }
}
