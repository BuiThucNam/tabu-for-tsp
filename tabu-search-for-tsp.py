import math
import random
import numpy as np

def init_solution(n): # hàm khởi tạo giải pháp ngẫu nhiên ban đầu
    route = list(range(n))
    random.shuffle(route)
    
    return route

def read_node_coords(file_path): # hàm đọc file TSP
    with open(file_path, 'r') as f:
        lines = f.readlines()
    node_coords = []
    for line in lines:
        if line.strip() == 'NODE_COORD_SECTION':
            continue
        elif line.strip() == 'EOF':
            break
        else:
            node_id, x, y = line.strip().split()[0:3]
            node_coords.append((int(node_id), float(x), float(y)))

    return node_coords # trả về danh sách các tọa độ

def get_neighborhood(route): # hàm trả về danh sách các tuyến đường lân cận
    n = len(route)
    neighborhood = []
    for i in range(1, n-1):
        for j in range(i+1, n-1):
            new_route = route.copy()
            new_route[i], new_route[j] = new_route[j], new_route[i]
            neighborhood.append(new_route)
    
    return neighborhood

# def read_matrix_from_file(filename): # hàm đọc file ATSP và trả về một ma trận 
#     dist_matrix = []
#     with open(filename, 'r') as file:
#         start_parsing = False
#         for line in file:
#             if line.strip() == "EDGE_WEIGHT_SECTION":
#                 start_parsing = True
#                 continue
#             if line.strip() == "EOF":
#                 break
#             if start_parsing:
#                 row = list(map(int, line.split()))
#                 dist_matrix.append(row)
    
#     return dist_matrix

def distance_matrix(node_coords): # hàm tính ma trận khoảng cách giữa các thành phố
    n = len(node_coords)
    dist_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            x1, y1 = node_coords[i][0], node_coords[i][1]
            x2, y2 = node_coords[j][0], node_coords[j][1]
            dist = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            dist_matrix[i][j] = dist_matrix[j][i] = dist
               
    return dist_matrix

def fitness(route, dist_matrix): # hàm tính tổng khoảng cách của một tuyến đường
    total_dist = 0
    n = len(route)
    for i in range(n-1):
        total_dist += dist_matrix[route[i]][route[i+1]]
    total_dist += dist_matrix[route[n-1]][route[0]]
    
    return total_dist

# hàm thuật toán tìm kiếm tabu 
def tabu_search(dist_matrix, tabu_list_size=20, max_iterations=15000, remove_tabu_after=30):
    n = len(dist_matrix)
    best_route = init_solution(n)
    best_fitness = fitness(best_route, dist_matrix)
    tabu_list = []
    tabu_count = 0

    for i in range(max_iterations):
        candidate_routes = get_neighborhood(best_route)
        best_candidate = None
        best_candidate_fitness = float('inf')
        
        # Tìm lời giải tốt nhất trong các lời giải láng giềng
        for candidate in candidate_routes:
            candidate_fitness = fitness(candidate, dist_matrix)
            
            # Kiểm tra điều kiện nguyện vọng (aspiration conditions)
            if candidate in tabu_list:
                if candidate_fitness < best_candidate_fitness:
                    tabu_list.remove(candidate)
                    best_candidate = candidate
                    best_candidate_fitness = candidate_fitness
                    tabu_list = []
                    tabu_count = 0
            else:
                if candidate_fitness < best_candidate_fitness:
                    best_candidate = candidate
                    best_candidate_fitness = candidate_fitness
                
        # Cập nhật lời giải tốt nhất nếu tìm được lời giải tốt hơn
        if best_candidate is not None:
            best_route = best_candidate
            best_fitness = best_candidate_fitness
        
        if len(tabu_list) > tabu_list_size:
            tabu_list.pop(0)
            
        # Thêm lời giải tốt nhất vào danh sách tabu
        tabu_list.append(best_route)
        tabu_count += 1
        
        # Xóa các lời giải trong danh sách tabu nếu đã đủ số lượng lời giải tối đa
        if tabu_count == remove_tabu_after:
            tabu_list = []
            tabu_count = 0
            
    # Trả về tuyến đường và chi phí tốt nhất tìm được
    return best_route, best_fitness

filepath = "bays29(TSP).txt"
# filename = "ftv33(ATSP).txt"
node_coords = read_node_coords(filepath)
dist_matrix = distance_matrix(node_coords)
# dist_matrix = read_matrix_from_file(filename)
print(tabu_search(dist_matrix))
