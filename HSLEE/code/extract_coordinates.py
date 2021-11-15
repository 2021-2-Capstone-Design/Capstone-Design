import math
import numpy as np

file = open('./../file_to_extract/coordinate.txt', mode='rt', encoding='utf-8')

result = []

for line in file:
    temp_line = line
    ret = np.array([])
    count = 0

    parse_line = temp_line.split(' ')

    if(len(parse_line) != 99):
        # 관절 누락이 있다는 뜻
        print("There are missing joint coordinates")
    else:
        while True:
            for full_joint in range(len(parse_line)):
                if(full_joint / 3 == count):
                    temp_joint = np.array([parse_line[full_joint], parse_line[full_joint+1], parse_line[full_joint+2]], float)
                    ret = np.append(ret, temp_joint, axis = 0)
                    break
            count += 1
            if(count == 33):
                break


    # while True:
    #     if(temp_line is not None):
    #         if(len(temp_line.split(' ')) == 3):
    #             joint_x, joint_y, joint_z = temp_line.split(' ')
    #             temp_joint = np.array([joint_x, joint_y, joint_z], float)
    #             temp_line = ''
    #             ret = np.append(ret, temp_joint, axis=0)
    #             break
    #         elif(len(temp_line.split(' ')) == 4):
    #             joint_x, joint_y, joint_z, temp_line = temp_line.split(' ', maxsplit=3)
    #             temp_joint = np.array([joint_x, joint_y, joint_z], float)
    #             ret = np.append(ret, temp_joint, axis=0)
    #         else:
    #             break
    #     else:
    #         break

    result = np.append(result, ret, axis=0)

# 1차원 배열로 모든 관절 좌표 쭉! (99개씩 4프레임 예시로 텍스트 저장해둠)
print("\n*** Check result ***")
print(result)
print("\n")

# 프레임 수 계산
num_frame = result.shape[0]/(33*3)
print("*** Check result ***")
print(num_frame)
print("\n")

# frame 수,  tracking좌표 수, xyz
result = np.reshape(result,(int(num_frame),33,3))

# 프레임별로 numpy 배열 출력해보기
print("*** Check frame by frame ***")
for i in range(int(num_frame)):
    print("frame" + str(i))
    print(result[i])
    print("\n")

# 차원 확인 (numpy 배열 크기 확인)
print("*** Check result dimension ***")
print(result.shape)
print("\n")

