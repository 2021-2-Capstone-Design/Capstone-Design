if __name__ == "__main__":
    f = open("result.txt",'r')
    dance_video = f.readlines()

    dance_vector=[]
    for line in dance_video:
        line = line[:-1]
        dance_vector.append(line)
    
    dance =[] # 최종 dance practice의 좌표값을 배열로 저장한 것
    for line in dance_vector:
        temp = line.split(',')
        print(temp)
        temp = list(map(float,temp))
        dance.append(temp)
    print(dance)