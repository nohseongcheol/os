// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package 한국어.자바;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class 통신 {
    private 통신() {}
    /** HTTP កំហុស 상태도 호출자가 판단할 수 있도록 ឆ្លើយតប 전체를 반환한다. */
    public static HttpResponse<String> 가져오기(URI អ៊ីម៉ែល, Duration ពេលវេលាកំណត់)
            throws IOException, InterruptedException {
        HttpClient ភ្ជាប់ = HttpClient.newBuilder().connectTimeout(ពេលវេលាកំណត់).build();
        return ភ្ជាប់.send(HttpRequest.newBuilder(អ៊ីម៉ែល).timeout(ពេលវេលាកំណត់).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket 연결하기(String អ៊ីម៉ែល, int 포트, int 제한밀리초) throws IOException {
        Socket ភ្ជាប់ = new Socket();
        try {
            ភ្ជាប់.connect(new InetSocketAddress(អ៊ីម៉ែល, 포트), 제한밀리초);
            ភ្ជាប់.setSoTimeout(제한밀리초);
            return ភ្ជាប់;
        } catch (IOException កំហុស) { ភ្ជាប់.close(); throw កំហុស; }
    }
}
