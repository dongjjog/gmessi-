import re
import os

#모델파일 불러오기
with open("ex4.txt", "r") as f:
    lines = f.readlines()

# 
start = None
end = None

#node 
for i, line in enumerate(lines):
    if 'NBLOCK' in line:
        start = i + 2  
    elif start is not None and line.strip() == '':
        end = i
        break


with open('node.fei', 'w') as f:
    for line in lines[start:end]:
        data = line.split()
        if len(data) >= 6:  # 데이터 항목의 수 확인
            no = data[0]
            x = data[3]
            y = data[4]
            z = data[5]
            f.write(f'add node # {no} at ({x}*m, {y}*m, {z}*m) with 3 dofs;\n')
        else:
            print(f"Skipping line due to insufficient data: {line}")

#element
for i, line in enumerate(lines):
    if 'EBLOCK' in line:
        start = i + 2  
    elif start is not None and line.strip() == '':
        end = i
        break

with open('element.fei', 'w') as f:
    for line in lines[start:end]:
        data = line.split()
        if len(data) >= 19:
            g1 = data[0]
            e1 = data[10]
            p1 = data[11]  
            p2 = data[12]  
            p3 = data[13] 
            p4 = data[14] 
            p5 = data[15]
            p6 = data[16]
            p7 = data[17]
            p8 = data[18]

            
            f.write(f'add element #    {e1}  type 8NodeBrick using 2 Gauss points each direction with nodes( {p1}, {p2}, {p3}, {p4}, {p5}, {p6}, {p7}, {p8} ) use material #   {g1};\n')    
        else:
            print(f"Skipping line due to insufficient data: {line}")       


input_file_path = 'node.fei'
# Path to the output file to save the results
output_file_path = 'fix.fei'

# Open the input file and read lines
with open(input_file_path, 'r') as input_file:
    lines = input_file.readlines()

# Initialize the list to store the result lines
result_lines = []

# Process each line from the input file
for line in lines:
    # Split the line into parts to extract information
    parts = line.split()
    # Ensure the line is correctly formatted
    if len(parts) > 7 and parts[0] == 'add' and parts[1] == 'node':
        # Extract the node number directly without '#' character
        node_number = parts[3]  # Changed from parts[2] to correctly extract the node number without '#'
        coords = parts[5:10]  # Adjusted the indices to correctly extract coordinates
        xnodemax = parts[3]  # Changed from parts[2] to correctly extract the node number without '#'
        xcoords = parts[5:6] 
        ynodemax = parts[3]  # Changed from parts[2] to correctly extract the node number without '#'
        ycoords = parts[6:7] 
        #fix시킬 범위선택 x or y or z 좌요가 0일때
        if any('0.0000000000000e+00' in coord for coord in coords):
            # Adjusted to remove '#' in the output format
            result_lines.append(f"fix node No {node_number} dofs uz ;")
        #fix시킬 범위선택 x좌표max값   
        if any('1.0000000000000e+01' in coord for coord in xcoords):
            # Adjusted to remove '#' in the output format
            result_lines.append(f"fix node No {xnodemax} dofs uz ;")  
        #fix시킬 범위선택 y좌표max값           
        if any('1.0000000000000e+01' in coord for coord in ycoords):
            # Adjusted to remove '#' in the output format
            result_lines.append(f"fix node No {ynodemax} dofs uz ;") 
# Save the resulting strings to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write('\n'.join(result_lines)) 
