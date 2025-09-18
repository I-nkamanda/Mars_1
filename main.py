import json

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
    sorted_lines = sorted(lines, reverse = True)
    print("시간 역순 객체 생성이 완료되었습니다.")
    print("생성된 객체를 출력합니다....")
    for ln in sorted_lines:
        parts = ln.split(",", 2)
        print("timestamp: ", parts[0])
        print("event: ", parts[1])
        print("message: ", parts[2])
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
    for ln in sorted_lines:
        ts, ev, msg = ln.split(",", 2)
        log_dict[ts] = {"event": ev, "message": msg}

    print(log_dict)
    with open("mission_computer_main.json", "w", encoding="utf-8") as f:
        json.dump(log_dict, f, ensure_ascii=False, indent=2)
        print("mission_computer_main.json 이름으로 딕셔너리 로그 저장 완료!")


if __name__ == "__main__":
    main()