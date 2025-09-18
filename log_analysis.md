# 사고 원인 분석 보고서

## 1. 요   약
- **사건 ID**: [MC-2023-08-27-001]
- **사건 발생 일시**: [2023-08-27 11:35–11:40]
- **상태**: [post-landing incident detected]
- **한 줄 요약**: [착륙 후 산소 탱크 불안정 → 폭발]

## 2. 타 임 라 인 (미션 컴퓨터 log 발췌)
- 10:30 — Liftoff
- 11:05 — Satellite deployment successful
- 11:28 — Touchdown confirmed
- 11:30 — Mission completed
- **11:35 — Oxygen tank unstable** ->  이상 징후 시작
- **11:40 — Oxygen tank explosion** -> 사건
- 12:00 — Systems powered down

> 출처: `mission_computer_main.log` (행 번호/타임스탬프로 근거 표시)

## 3. 이상 요인 상세
- **주요 요인**: 산소 탱크 압력/온도 불안정
- **언제**:  임무 완료 선언(11:30) 이후, 회수 단계 중
- **어디서**: 착륙지점 근방 (추정)

## 4. 사고 발생 이유 추정
| 가설 | 근거 (로그 내 라인) | 확보하지 못한 정보 | 가능성 |
|---|---|---|---|
| [탱크 잔류 압력 관리 실패] | [11:35 “unstable” 등] | [센서 데이터 없음] | **[Low]** |
| [열원 근접/충격] | [성공적 착륙, 미션 성공 선언 후 내 발생] | [열로그/취급기록 부재] | **[High]** |


## 5. Contributing Factors
- 착륙 후 잔류 산소량
- 화성의 강력한 모래바람