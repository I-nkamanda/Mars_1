import json

DANGER_KEYWORDS = ["explosion", "unstable", "oxygen", "failure", "malfunction"]

def read_log_lines(path="mission_computer_main.log"):
    lines = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        first = f.readline()
        if first and first.strip().lower().startswith("timestamp,event,message"):
            pass
        else:
            if first:
                lines.append(first.strip())
        for ln in f:
            lines.append(ln.strip())
    return lines

def print_sorted_desc(path="mission_computer_main.log"):
    lines = read_log_lines(path)
    for ln in sorted(lines, reverse=True):
        ts, ev, msg = ln.split(",", 2)
        print(f"{ts} | {ev} | {msg}")

def parse_line(ln: str):
    ts, ev, msg = ln.split(",", 2)
    return ts, ev, msg

def save_danger_logs(out_path="danger_logs.txt", log_path="mission_computer_main.log"):
    lines = read_log_lines(log_path)
    picked = []
    for ln in lines:
        ts, ev, msg = parse_line(ln)
        blob = f"{ts} {ev} {msg}".casefold()
        if any(kw.casefold() in blob for kw in DANGER_KEYWORDS):
            picked.append(ln)
    picked.sort(reverse = True)

    with open(out_path, "w", encoding="utf-8") as f:
        for ln in picked:
            f.write(ln+"\n")
    print(f"[OK] 위험 로그 {len(picked)}건 저장 -> {out_path}")

def search_in_json(json_path="mission_computer_main.json", query="oxygen"):
    # """JSON 로그에서 사용자가 입력한 문자열이 포함된 항목만 출력"""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)  # dict: {timestamp: {event, message}}
    except FileNotFoundError:
        print(f"[에러] JSON 파일이 없습니다: {json_path}")
        return
    except json.JSONDecodeError as e:
        print(f"[에러] JSON 파싱 실패: {e}")
        return
    if not query.strip():  # ✅ 빈 문자열 방지
        print("[에러] 검색어가 비어 있습니다. 검색을 취소합니다.")
        return
    
    q = query.casefold()
    results = []

    for ts, obj in data.items():
        ev = str(obj.get("event", ""))
        msg = str(obj.get("message", ""))
        blob = f"{ts} {ev} {msg}".casefold()
        if q in blob:
            results.append((ts, ev, msg))

    if not results:
        print(f"[결과 없음] '{query}' 를 포함하는 로그가 없습니다.")
        return

    # 시간 역순 출력
    results.sort(key=lambda x: x[0], reverse=True)
    print(f"🔍 '{query}' 검색 결과 ({len(results)}건):")
    for ts, ev, msg in results:
        print(f"{ts} | {ev} | {msg}")


def main():
    
    print("Trying to open readable files....")
    print("files found: (1), mission_computer_main.log")
    while True:
        pin = input("해당 파일을 읽어들입니까? (y / n)")
        if pin == "y":
            break
        elif pin == "n":
            return
        else:
            print ("잘못된 입력입니다. 다시 입력해 주세요")
            continue

    try:
        with open("mission_computer_main.log", "r")as f: #with 구문은 Context manager라고 부름. f라는 객체가 생김. 
            next(f)
            for line in f: #with 안쪽이 끝나면 f.close (파일 닫기)가 자동으로 호출됨 (파일 읽는 도중 오류가 나도 close 보장)
                print(line.strip()) # 개행을 제거하고 한줄씩 한줄씩 나오게 됨.
    except FileNotFoundError:
        print("File not found. Check your directory.")
        print("시스템을 종료합니다.")
        return
    except PermissionError:
        print("You do not have access to the file. Ask Bocal or higher.")
        print("시스템을 종료합니다.")
        return
    except UnicodeDecodeError:
        print("Cannot interpret the file encoding. Check your encoding.")
        print("시스템을 종료합니다.")
        return
    except Exception as e:
        print(f"Unknown error has occured: {e}")
        print("시스템을 종료합니다.")
        return

    print("미션 로그 파일을 line-by-line으로 출력 완료했습니다.")

    while True:
        pin = input("미션 로그를 분석 후, 시간 순서대로 보시겠습니까? (y / n)")
        if pin == "y":
            break
        elif pin == "n":
            return
        else:
            print ("잘못된 입력입니다. 다시 입력해 주세요")
            continue

    with open("mission_computer_main.log", "r")as f:
        next(f)
        lines = [line.strip() for line in f]
        for line in lines:
            parts = line.split(",")
            print("timestamp:", parts[0])
            print("event:", parts[1])
            print("message:", parts[2])

    print("카테고리별 정렬 및 객체 전환 완료되었습니다.")
    while True:
            pin = input("로그 분석을 위해 시간 역순으로 보시겠습니까? (y / n)")
            if pin == "y":
                break
            elif pin == "n":
                return
            else:
                print ("잘못된 입력입니다. 다시 입력해 주세요")
                continue

    # print(type(lines))
    # sorted_lines = sorted(lines, reverse = True)
    # print("시간 역순 객체 생성이 완료되었습니다.")
    # print("생성된 객체를 출력합니다....")
    # for ln in sorted_lines:
    #     parts = ln.split(",", 2)
    #     print("timestamp: ", parts[0])
    #     print("event: ", parts[1])
    #     print("message: ", parts[2])

    try:
        print_sorted_desc("mission_computer_main.log")
    except Exception as e:
        print(f"[에러] 역순 정렬 출력 중 문제 발생: {e}")

    print("시간 역순 객체 출력이 완료되었습니다.")

    while True:
            pin = input("이어서 자료를 딕셔너리화 진행 후 .json 파일로 저장합니다. 계속합니까? (y / n)")
            if pin == "y":
                break
            elif pin == "n":
                return
            else:
                print ("잘못된 입력입니다. 다시 입력해 주세요")
                continue

    log_dict = {}
    sorted_lines = sorted(lines, reverse = True)
    for ln in sorted_lines:
        ts, ev, msg = ln.split(",", 2)
        log_dict[ts] = {"event": ev, "message": msg}
    
    print(log_dict)
    with open("mission_computer_main.json", "w", encoding="utf-8") as f:
        json.dump(log_dict, f, ensure_ascii=False, indent=2)
        print("mission_computer_main.json 이름으로 딕셔너리 로그 저장 완료!")
    
    while True:
            pin = input("이어서 위험 키워드 포함 로그를 파일로 저장합니다. 계속합니까? (y / n)")
            if pin == "y":
                try:
                    save_danger_logs("danger_logs.txt", "mission_computer_main.log")
                except Exception as e:
                    print(f"[에러] 위험 로그 저장 실패: {e}")
                break    
            elif pin == "n":
                return
            else:
                print ("잘못된 입력입니다. 다시 입력해 주세요")
                continue

    while True:
        pin = input("JSON 파일에서 특정 문자열을 검색하시겠습니까? (y / n) ").strip().lower()
        if pin == "y":
                while True:
                    q = input("검색할 문자열을 입력하세요(n 입력시 종료):  ").strip()
                    if q == "n":
                        print("n 입력 감지. 검색을 종료합니다.")
                        break
                    else:
                        try:
                            search_in_json("mission_computer_main.json", q)
                        except Exception as e:
                            print(f"[에러] 검색 중 문제 발생: {e}")
                            break
        elif pin == "n":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 입력해 주세요")
            continue

if __name__ == "__main__":
    main()

    # TODO: 마지막 질문 부분 조금만 손보기 []
    # TODO: 쫙 처음부터 주석 달면서 코드 이해하기 [ ]