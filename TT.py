import time
import random


def draw_board(board):
    """
    보드의 상태를 보여준다.
    :param board: 현재 보드의 상태
    """
    for y in range(3):
        print("-" * 7)
        print("|", end='')
        print(board[y][0], end='')
        print("|", end='')
        print(board[y][1], end='')
        print("|", end='')
        print(board[y][2], end='')
        print("|")
    print("-" * 7)


def reset_board(board):
    """
    보드를 초기화한다.
    :param board: 현재 보드의 상태
    """
    for x in range(3):
        for y in range(3):
            board[x][y] = ' '


def restart():
    """
    게임을 다시 시작한다.
    :return: 다시 시작하면 True, 아니면 False를 반환
    """
    result = input("다시 시작하시겠습니까? Yes or No")
    result = result.strip()
    # if(result == "Y" or result == "Yes" or result == "y" or result == "yes" or result == "O" or result == "True"):
    if result in ["Y", "Yes", "y", "yes", "O", "True", ""]:
        return True
    else:
        return False


def player_turn(present):  # 사람 차례
    """
    사람 차례의 순서
    :param present: 현재 보드의 상태
    input : 돌을 놓을 곳의 좌표
    """
    while True:
        try:
            px, py = input("당신의 차례입니다. 좌표를 공백을 두고 입력해주세요").split()
        except ValueError:
            print("좌표를 2개입력해야 합니다.")
            return player_turn(present)
        # if (check(px, py)):
        if check(px, py):
            px = int(px)
            py = int(py)
            if present[px-1][py-1] == ' ':
                present[px-1][py-1] = 'O'
                break
            else:
                print("이곳에는 놓을 수 없습니다.")
        else:
            print("1에서 3까지의 정수만 입력할 수 있습니다.")


def computer_turn(present):
    """
    컴퓨터 차례의 순서
    :param present: 현재 보드의 상태
    done : 컴퓨터가 돌을 두었는지 여부
    """
    print("컴퓨터의 차례입니다. 잠시만 기다려주세요")
    done = "False"
    if computer_al_at_df(present, "X"):
        done = "True"  # 이길 수 있는 자리에 놓기
    elif computer_al_at_df(present, "O"):
        done = "True"  # 지지 않는 자리에 놓기
    elif present[1][1] == " ":
        present[1][1] = "X"
        done = "True"  # 중앙 자리잡기
    elif computer_medium_occupied(present):
        done = "True"  # 중앙이 차 있을 때 코너 먹기
    elif computer_al_attack_depth(present):
        done = "True"  # 최대한 나은 수 두기
    if done != "True":  # 정 안 되면 랜덤으로 두기 -> 공백인 좌표를 저장 후 랜덤으로 뽑는다.
        rand = []
        for i in range(3):
            for j in range(3):
                if present[i][j] == " ":
                    rand.append([i, j])
        anywhere = random.sample(rand, 1)
        present[anywhere[0][0]][anywhere[0][1]] = "X"
    time.sleep(1)


def computer_al_at_df(present, x):
    """
    기본적인 공격과 방어를 위한 코드이다.
    지금 턴에 컴퓨터가 놓으면 이길 수 있거나, 다음 턴에 플레이어가 놓으면 질 수 있는 곳에 돌을 놓는다.
    :param present:
    :param x: 공격시 X, 방어시 O가 입력된다.
    :return: 돌을 두었다면 True를 반환한다.
    """
    for i in range(3):
        cnt = 0
        for j in range(3):
            cnt = int(cnt)
            if present[i][j] == x:
                cnt += 1
            if cnt >= 2:
                for k in range(3):  # 어떤 줄에 동일한 돌이 2개 이상이면 그 줄에 공백이 있는지 확인 후 공백에 돌을 둔다.
                    if present[i][k] == " ":
                        present[i][k] = "X"
                        return True
    for j in range(3):
        cnt = 0
        for i in range(3):
            cnt = int(cnt)
            if present[i][j] == x:
                cnt += 1
            if cnt >= 2:
                for k in range(3):
                    if present[k][j] == " ":
                        present[k][j] = "X"
                        return True
    cnt = 0
    if present[0][2] == x:
        cnt += 1
    if present[1][1] == x:
        cnt += 1
    if present[2][0] == x:
        cnt += 1
    if cnt >= 2:
        if present[0][2] == " ":
            present[0][2] = "X"
            return True
        if present[1][1] == " ":
            present[1][1] = "X"
            return True
        if present[2][0] == " ":
            present[2][0] = "X"
            return True

    cnt = 0
    if present[0][0] == x:
        cnt += 1
    if present[1][1] == x:
        cnt += 1
    if present[2][2] == x:
        cnt += 1
    if cnt >= 2:
        if present[0][0] == " ":
            present[0][0] = "X"
            return True
        if present[1][1] == " ":
            present[1][1] = "X"
            return True
        if present[2][2] == " ":
            present[2][2] = "X"
            return True


def computer_al_attack_depth(present):
    """
    유리한 수를 두게 하는 코드(=막힌 수를 두게 하지 않는 코드)이다.
    예시) | |X|O 일 때 공백이 아닌 다른 곳에 돌을 둔다.
    :param present: 현재 보드의 상태
    :return: 돌을 두었다면 True를 반환한다.
    """

    """
    cntO = O의 개수
    cntX = X의 개수
    어떤 줄에 O이 없고 X가 한 개 이상 있다면 그 줄의 공백에 X를 둔다.
    """
    for j in range(3):
        cnto = 0
        cntx = 0
        for i in range(3):
            cnto = int(cnto)
            cntx = int(cntx)
            if present[i][j] == "X":
                cntx += 1
            if present[i][j] == "O":
                cnto += 1
            if cntx >= 1 and cnto == 0:
                for k in range(3):
                    if present[k][j] == " ":
                        present[k][j] = "X"
                        return True
    cntx = 0
    cnto = 0
    if present[0][2] == "X":
        cntx += 1
    if present[0][2] == "O":
        cnto += 1
    if present[1][1] == "X":
        cntx += 1
    if present[1][1] == "O":
        cnto += 1
    if present[2][0] == "X":
        cntx += 1
    if present[2][0] == "O":
        cnto += 1
    if cntx >= 1 and cnto == 0:
        if present[0][2] == " ":
            present[0][2] = "X"
            return True
        if present[1][1] == " ":
            present[1][1] = "X"
            return True
        if present[2][0] == " ":
            present[2][0] = "X"
            return True

    for i in range(3):
        cnto = 0
        cntx = 0
        for j in range(3):
            cnto = int(cnto)
            cntx = int(cntx)
            if present[i][j] == "X":
                cntx += 1
            if present[i][j] == "O":
                cnto += 1
            if cntx >= 1 and cnto == 0:
                for k in range(3):
                    if present[i][k] == " ":
                        present[i][k] = "X"
                        return True
    cntx = 0
    cnto = 0
    if present[0][0] == "X":
        cntx += 1
    if present[0][0] == "O":
        cnto += 1
    if present[1][1] == "X":
        cntx += 1
    if present[1][1] == "O":
        cnto += 1
    if present[2][2] == "X":
        cntx += 1
    if present[2][2] == "O":
        cnto += 1
    if cntx >= 1 and cnto == 0:
        if present[0][0] == " ":
            present[0][0] = "X"
            return True
        if present[1][1] == " ":
            present[1][1] = "X"
            return True
        if present[2][2] == " ":
            present[2][2] = "X"
            return True


def computer_medium_occupied(present):
    """
    처음에 가운데가 차 있는 경우, 코너에 두는 게 유리하다.
    :param present: 현재 보드의 상태
    :return: 코너에 두었을 경우 True를 반환한다.
    """
    if present[1][1] == "O":
        rand = [[0, 0], [0, 2], [2, 0], [2, 2]]     # 코너의 각 좌표들
        while True:
            anywhere = random.sample(rand, 1)   # 좌표들 중 하나를 뽑는다.
            if present[anywhere[0][0]][anywhere[0][1]] == " ":  # 그 좌표가 비어있다면 돌을 놓는다.
                present[anywhere[0][0]][anywhere[0][1]] = "X"
                return True


def check(px, py):
    """
    사용자가 제대로 된 좌표를 입력했는지 확인한다.
    정수가 맞는지 판별 후, 1부터 3이내의 수인지 확인한다.
    :return: 제대로 입력되었다면 True, 아니면 False를 반환한다.
    """
    if px.isdecimal():
        if py.isdecimal():  # px, py가 정수인지 판별
            px = int(px)
            py = int(py)
            if 1 <= px <= 3 and 1 <= py <= 3:   # px, py가 1~3 이내인지 판별
                return True
            else:
                return False


def select_check(px):
    """
    동전 던지기를 할 떄 0이나 1만 입력되는지 확인한다.
    :return: 0이나 1만 입력되었으면 True, 아니면 False를 반환한다.
    """
    if px.isdecimal():
        px = int(px)
        if 0 <= px <= 1:
            return True
        else:
            return False


def v_check(board):
    """
    승리여부를 판단한다.
    :param board: 현재 보드의 상태
    :return: 승리시 True, 아닐 시 False를 반환한다.
    """
    for i in range(3):  # 어떤 줄에 똑같은 돌이 3개 있다면 승리이다.
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            return True
        elif board[0][i] == board[1][i] == board[2][i] != ' ':
            return True
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    elif board[0][0] == board[1][1] == board[2][2] != ' ':
        return True
    else:
        return False


def draw_check(present):
    """
    무승부 여부를 판단한다.
    :param present: 현재 보드의 상태
    :return: 무승부라면 True, 아니라면 False를 반환한다.
    """
    cnt = 0
    for i in range(3):
        for j in range(3):
            if present[i][j] in "OX":
                cnt += 1    # 보드가 차 있다면 cnt에 1을 더한다.
    if cnt == 9:
        return True     # cnt가 9면 누구도 승리하지 않은 채로 보드가 꽉 차 있으므로 무승부이다.
    else:
        return False


def player_first(present):
    """
    사람 선공시 순서이다.
    플레이어 턴 -> 보드 상태 표시 -> 무승부 판별 -> 플레이어 승리 판별 ->
    컴퓨터 턴 -> 보드 상태 표시 -> 무승부 판별 -> 컴퓨터 승리 판별 순으로 이루어진다
    :param present: 현재 보드의 상태
    :return: 무승부시 0, 플레이어 승리시 1, 컴퓨터 승리시 2를 반환한다.
    """
    while True:
        player_turn(present)
        draw_board(present)
        if draw_check(present):
            print("무승부입니다.")
            return "0"
        if v_check(present):
            print("당신이 승리했습니다.")
            return "1"
        else:
            computer_turn(present)
            draw_board(present)
            if draw_check(present):
                print("무승부입니다.")
                return "0"
            if v_check(present):
                print("컴퓨터가 승리했습니다.")
                return "2"


def computer_first(present):
    """
    컴퓨터 선공시 순서이다.
    컴퓨터의 턴 -> 보드 상태 표시 -> 무승부 판별 -> ai승리 판별 ->
    플레이어 턴 -> 보드 상태 표시 -> 무승부 판별 -> 컴퓨터 승리 판별 순으로 이루어진다.
    :param present: 현재 보드의 상태
    :return: 무승부시 0, 플레이어 승리시 1, 컴퓨터 승리시 2를 반환한다.
    """
    while True:
        computer_turn(present)
        draw_board(present)
        if draw_check(present):
            print("무승부입니다.")
            return "0"
        if v_check(present):
            print("컴퓨터가 승리했습니다.")
            return "2"
        else:
            player_turn(present)
            draw_board(present)
            if draw_check(present):
                print("무승부입니다.")
                return "0"
            if v_check(present):
                print("당신이 승리했습니다.")
                return "1"


def sequence_select():
    """
    선후공을 결정하는 코드 - 플레이어가 동전을 던져, 맞추면 선공, 틀리면 후공이 된다.
    :return:  선공이면 True, 후공이면 False를 반환한다.
    """
    print("동전을 던져 순서를 정합니다. 앞면은 1, 뒷면은 0을 입력해주세요.")
    y = random.randrange(0, 2)
    x = input()
    x = x.strip()
    if select_check(x):
        x = int(x)
        if x == y:
            if y == 1:
                print("앞면이 나왔습니다. 당신이 선공입니다.")
                return True
            else:
                print("뒷면이 나왔습니다. 당신이 선공입니다.")
                return True
        else:
            if y == 1:
                print("앞면이 나왔습니다. 당신이 후공입니다.")
                return False
            else:
                print("뒷면이 나왔습니다. 당신이 후공입니다.")
                return False
    else:
        print("0 혹은 1만 입력해주세요.")
        return sequence_select()


def tt():
    """
    게임을 시작하고, 스코어를 저장하며, 경기의 재시작 여부를 결정한다.
    """
    present = [[" "] * 3, [" "] * 3, [" "] * 3]
    print("띡땍또 Ver 1.0_Released")
    time.sleep(1)
    i = 1
    v1 = v2 = 0
    while i:
        if sequence_select():
            time.sleep(1)
            result = player_first(present)
            if result == "1":
                v1 += 1
            elif result == "2":
                v2 += 1
        else:
            time.sleep(1)
            result = computer_first(present)
            if result == "1":
                v1 += 1
            elif result == "2":
                v2 += 1
        print("스코어\n%d : %d" % (v1, v2))
        if restart():
            i = 1
            present = [[" "] * 3, [" "] * 3, [" "] * 3]
        else:
            i = 0


tt()
