def process_element_data(element_number, nodes, elset, elset_material_map):
 
    material_number = elset_material_map.get(elset, 0)  # Default to 0 if not found
    return f'add element # {element_number} type 8NodeBrick using 2 Gauss points each direction with nodes({", ".join(nodes)}) use material # {material_number};\n'

# Initialize a dictionary to map ELSET to material numbers
elset_material_map = {}
current_material_number = 0

lines = []  # Initialize lines list

# Ensure to read your file content here
with open("r.txt", "r") as f:
    lines = f.readlines()

# element 번호 및 그룹번호 지정
for line in lines:
    if '*ELEMENT,TYPE=' in line and 'ELSET=' in line:
        elset = line.split('ELSET=')[1].strip()
        if elset not in elset_material_map:
            current_material_number += 1  # element 번호
            elset_material_map[elset] = current_material_number

# Initialize parsing flag
parsing = False

# Extracting node information
with open('node.fei', 'w') as f:
    for line in lines:
        if '*NODE' in line: #node파트 읽기
            parsing = True
        elif '*ELEMENT' in line: #element파트 읽기 취소
            parsing = False
        if parsing:
            data = line.replace(',', ' ').split() #빈칸과 ','부분을 넘기기
            if len(data) == 4:  # Ensure exactly four parts for a node line
                no, x, y, z = data
                f.write(f'add node # {no} at ({x}*m, {y}*m, {z}*m) with 3 dofs;\n')

# Reset parsing flag and ELSET for each element section
parsing = False
elset = None

# Extracting and processing element information
with open('element.fei', 'w') as f:
    for line in lines:
        if '*ELEMENT,TYPE=' in line:
            data = line.split(',')
            elset = data[-1].split('=')[1].strip()  # ELSET=G10001 를 인식한다
            parsing = True
        elif elset and ',' in line and parsing:  # 
            data = line.strip().split(',')
            element_number = data[0] #element번호 
            nodes = data[1:] #node번호
            output_line = process_element_data(element_number, nodes, elset, elset_material_map)
            if output_line:  # Write output if it's not an empty string
                f.write(output_line)

# Path to the input file containing node information
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
        node_number2 = parts[3]  # Changed from parts[2] to correctly extract the node number without '#'
        coords2 = parts[5:9] 
        #fix시킬 범위선택 0
        if any('0.00000000000000e+00' in coord for coord in coords):
            # Adjusted to remove '#' in the output format
            result_lines.append(f"fix node No {node_number} dofs uz ;")
        #fix시킬 범위 10    
        if any('1.00000000000000e+00' in coord for coord in coords2):
            # Adjusted to remove '#' in the output format
            result_lines.append(f"fix node No {node_number2} dofs uz ;")        
# Save the resulting strings to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write('\n'.join(result_lines))


