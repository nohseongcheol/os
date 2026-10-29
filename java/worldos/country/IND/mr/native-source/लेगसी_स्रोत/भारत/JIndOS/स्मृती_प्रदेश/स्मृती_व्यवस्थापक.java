// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
package भारत.JIndOS.स्मृती_प्रदेश;

import java.util.Arrays;
import java.util.Map;
import java.util.TreeMap;

/** भौतिक स्मृतीचे संरेखित वाटप, मुक्तता आणि एकत्रीकरण करते. */
public final class स्मृती_व्यवस्थापक {
    private final byte[] स्मृती_प्रदेश;
    private final TreeMap<Integer, Integer> रिक्त_प्रदेश = new TreeMap<Integer, Integer>();
    private final TreeMap<Integer, Integer> वापरलेले_प्रदेश = new TreeMap<Integer, Integer>();

    public स्मृती_व्यवस्थापक(int एकूण_आकारा) {
        if (एकूण_आकारा < 8192) {
            throw new IllegalArgumentException("기억공간이 너무 작습니다.");
        }
        स्मृती_प्रदेश = new byte[एकूण_आकारा];
        रिक्त_प्रदेश.put(Integer.valueOf(4096), Integer.valueOf(एकूण_आकारा - 4096));
    }

    public synchronized int संग्रह_वाटप_करा(int आकार) {
        return संरेखित_वाटप_करा(आकार, 1);
    }

    public synchronized int संरेखित_वाटप_करा(int आकार, int संरेखन_करावे_मूल्य) {
        if (आकार <= 0 || संरेखन_करावे_मूल्य <= 0 || (संरेखन_करावे_मूल्य & (संरेखन_करावे_मूल्य - 1)) != 0) {
            throw new IllegalArgumentException("크기와 정렬이 올바르지 않습니다.");
        }
        for (Map.Entry<Integer, Integer> प्रविष्टी_मूल्य : रिक्त_प्रदेश.entrySet()) {
            int सुरू_करा = प्रविष्टी_मूल्य.getKey().intValue();
            int प्रदेश_आकारा = प्रविष्टी_मूल्य.getValue().intValue();
            int संरेखित_प्रारंभ = (सुरू_करा + संरेखन_करावे_मूल्य - 1) & -संरेखन_करावे_मूल्य;
            int पुढील_मूल्य_आकारा = संरेखित_प्रारंभ - सुरू_करा;
            int अंतिम_आकारा = प्रदेश_आकारा - पुढील_मूल्य_आकारा - आकार;
            if (अंतिम_आकारा < 0) {
                continue;
            }
            रिक्त_प्रदेश.remove(Integer.valueOf(सुरू_करा));
            if (पुढील_मूल्य_आकारा > 0) {
                रिक्त_प्रदेश.put(Integer.valueOf(सुरू_करा), Integer.valueOf(पुढील_मूल्य_आकारा));
            }
            if (अंतिम_आकारा > 0) {
                रिक्त_प्रदेश.put(Integer.valueOf(संरेखित_प्रारंभ + आकार), Integer.valueOf(अंतिम_आकारा));
            }
            वापरलेले_प्रदेश.put(Integer.valueOf(संरेखित_प्रारंभ), Integer.valueOf(आकार));
            Arrays.fill(स्मृती_प्रदेश, संरेखित_प्रारंभ, संरेखित_प्रारंभ + आकार, (byte) 0);
            return संरेखित_प्रारंभ;
        }
        throw new OutOfMemoryError("물리 기억공간이 부족합니다.");
    }

    public synchronized void संग्रह_रिलीज(int पत्ता) {
        Integer आकारा_ऑब्जेक्ट = वापरलेले_प्रदेश.remove(Integer.valueOf(पत्ता));
        if (आकारा_ऑब्जेक्ट == null) {
            throw new IllegalArgumentException("할당되지 않은 주소입니다.");
        }
        int सुरू_करा = पत्ता;
        int आकार = आकारा_ऑब्जेक्ट.intValue();
        Map.Entry<Integer, Integer> पुढील_मूल्य = रिक्त_प्रदेश.lowerEntry(Integer.valueOf(सुरू_करा));
        if (पुढील_मूल्य != null && पुढील_मूल्य.getKey().intValue() + पुढील_मूल्य.getValue().intValue() == सुरू_करा) {
            सुरू_करा = पुढील_मूल्य.getKey().intValue();
            आकार += पुढील_मूल्य.getValue().intValue();
            रिक्त_प्रदेश.remove(पुढील_मूल्य.getKey());
        }
        Map.Entry<Integer, Integer> मागे_मूल्य = रिक्त_प्रदेश.ceilingEntry(Integer.valueOf(सुरू_करा));
        if (मागे_मूल्य != null && सुरू_करा + आकार == मागे_मूल्य.getKey().intValue()) {
            आकार += मागे_मूल्य.getValue().intValue();
            रिक्त_प्रदेश.remove(मागे_मूल्य.getKey());
        }
        रिक्त_प्रदेश.put(Integer.valueOf(सुरू_करा), Integer.valueOf(आकार));
    }

    public synchronized byte बाइट_मूल्य_वाचा(int पत्ता) {
        व्याप्ती_तपासा(पत्ता, 1);
        return स्मृती_प्रदेश[पत्ता];
    }

    public synchronized void बाइट_मूल्य_लिहा(int पत्ता, byte मूल्य) {
        व्याप्ती_तपासा(पत्ता, 1);
        स्मृती_प्रदेश[पत्ता] = मूल्य;
    }

    public synchronized int एकूण_आकारा() {
        return स्मृती_प्रदेश.length;
    }

    public synchronized int वापरलेले_आकारा() {
        int एकूण_मूल्य = 0;
        for (Integer आकार : वापरलेले_प्रदेश.values()) {
            एकूण_मूल्य += आकार.intValue();
        }
        return एकूण_मूल्य;
    }

    private void व्याप्ती_तपासा(int पत्ता, int आकार) {
        if (पत्ता < 0 || आकार < 0 || पत्ता > स्मृती_प्रदेश.length - आकार) {
            throw new IndexOutOfBoundsException("स्मृती_प्रदेश 범위를 벗어났습니다.");
        }
    }
}

