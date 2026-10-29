// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package नेपाली.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP त्रुटि 상태도 호출자가 판단할 수 있도록 जवाफ_दिनुहोस् 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ठेगाना, Duration समय_सीमा)
            throws IOException, InterruptedException {
        HttpClient जडान = HttpClient.newBuilder().connectTimeout(समय_सीमा).build();
        return जडान.send(HttpRequest.newBuilder(ठेगाना).timeout(समय_सीमा).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ठेगाना, int हार्डवेयर_पोर्ट, int 제한밀리초) throws IOException {
        Socket जडान = new Socket();
        try {
            जडान.connect(new InetSocketAddress(ठेगाना, हार्डवेयर_पोर्ट), 제한밀리초);
            जडान.setSoTimeout(제한밀리초);
            return जडान;
        } catch (IOException त्रुटि) { जडान.close(); throw त्रुटि; }
    }
}
