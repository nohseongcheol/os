// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP ত্ৰুটি 상태도 호출자가 판단할 수 있도록 প্ৰত্যুত্তৰ_দিয়ক 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI ঠিকনা, Duration সময়_সীমা)
            throws IOException, InterruptedException {
        HttpClient সংযোগ_স্থাপনা = HttpClient.newBuilder().connectTimeout(সময়_সীমা).build();
        return সংযোগ_স্থাপনা.send(HttpRequest.newBuilder(ঠিকনা).timeout(সময়_সীমা).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String ঠিকনা, int 포트, int 제한밀리초) throws IOException {
        Socket সংযোগ_স্থাপনা = new Socket();
        try {
            সংযোগ_স্থাপনা.connect(new InetSocketAddress(ঠিকনা, 포트), 제한밀리초);
            সংযোগ_স্থাপনা.setSoTimeout(제한밀리초);
            return সংযোগ_স্থাপনা;
        } catch (IOException ত্ৰুটি) { সংযোগ_স্থাপনা.close(); throw ত্ৰুটি; }
    }
}
