// Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
/** 국가판 생성기는 이 대응표의 말과 도움말을 판별 언어로 교체한다. */
public final class 관리명령 {
    static String 완성어() { return "아이피설정 아이피 응답시험 경로표 통신현황 작업목록 작업현황 기억현황 저장현황 가동시간 전원끄기 도움말"; }
    static String 말(int 번호) {
        if (번호==0) return "아이피설정";
        if (번호==1) return "아이피";
        if (번호==2) return "응답시험";
        if (번호==3) return "경로표";
        if (번호==4) return "통신현황";
        if (번호==5) return "작업목록";
        if (번호==6) return "작업현황";
        if (번호==7) return "기억현황";
        if (번호==8) return "저장현황";
        if (번호==9) return "가동시간";
        if (번호==10) return "전원끄기";
        return "도움말";
    }
    static String 설명(int 번호) {
        if (번호<=1) return "IPv4 주소·가림·관문 조회 및 설정";
        if (번호==2) return "ICMP 응답과 왕복 시간 확인";
        if (번호==3) return "직접 연결망과 기본 관문 조회";
        if (번호==4) return "TCP·UDP 끝점과 송수신 통계";
        if (번호==5) return "커널 작업과 사용자 실행과정 목록";
        if (번호==6) return "작업·기억 현황 갱신, q 또는 Ctrl+C로 끝내기";
        if (번호==7) return "실제 커널 기억 공간과 사용자 매핑 사용량";
        if (번호==8) return "RAM 파일시스템 용량·파일 칸 사용량";
        if (번호==9) return "부팅 후 가동 시간";
        if (번호==10) return "운영체제 종료, RAM 자료는 보존되지 않음";
        return "명령어와 각 나라 언어의 명령 이름 안내";
    }
}
