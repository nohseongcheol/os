// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package मराठी.जावा;

import java.io.IOException;
import java.net.*;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.time.Duration;

public final class संचार {
    private संचार() {}
    /** आवाहकाला HTTP त्रुटिस्थितीही तपासता यावी म्हणून पूर्ण प्रतिसाद परत करते. */
    public static HttpResponse<String> घ्या_मूल्य(URI पत्ता, Duration वेळ_मर्यादा)
            throws IOException, InterruptedException {
        HttpClient जोडा = HttpClient.newBuilder().connectTimeout(वेळ_मर्यादा).build();
        return जोडा.send(HttpRequest.newBuilder(पत्ता).timeout(वेळ_मर्यादा).GET().build(),
                HttpResponse.BodyHandlers.ofString(StandardCharsets.UTF_8));
    }
    public static Socket कनेक्ट_संचारटोक(String पत्ता, int हार्डवेअर_पॉर्ट, int मर्यादा_मिलिसेकंद) throws IOException {
        Socket जोडा = new Socket();
        try {
            जोडा.connect(new InetSocketAddress(पत्ता, हार्डवेअर_पॉर्ट), मर्यादा_मिलिसेकंद);
            जोडा.setSoTimeout(मर्यादा_मिलिसेकंद);
            return जोडा;
        } catch (IOException त्रुटी) { जोडा.close(); throw त्रुटी; }
    }
}
