// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP चूक 상태도 호출자가 판단할 수 있도록 जाप_दिवप 전체를 반환한다. */
    public static HttpResponse<String> TAKE_मोल(URI नामो, Duration वेळ_मर्यादा)
            throws IOException, InterruptedException {
        HttpClient कनॅक्ट = HttpClient.newBuilder().connectTimeout(वेळ_मर्यादा).build();
        return कनॅक्ट.send(HttpRequest.newBuilder(नामो).timeout(वेळ_मर्यादा).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String नामो, int हार्डवॅर_पोर्ट, int 제한밀리초) throws IOException {
        Socket कनॅक्ट = new Socket();
        try {
            कनॅक्ट.connect(new InetSocketAddress(नामो, हार्डवॅर_पोर्ट), 제한밀리초);
            कनॅक्ट.setSoTimeout(제한밀리초);
            return कनॅक्ट;
        } catch (IOException चूक) { कनॅक्ट.close(); throw चूक; }
    }
}
