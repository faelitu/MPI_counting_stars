def flood_star(i, j, tile):
    tile[i][j] = 128
    if tile[i][j+1] and tile[i][j+1] == 255: # pixel right
        flood_star(i, j+1, tile)
    if tile[i+1][j] and tile[i+1][j] == 255: # pixel below
        flood_star(i+1, j, tile)
    if tile[i][j-1] and tile[i][j-1] == 255: # pixel left
        flood_star(i, j-1, tile)

def show_tile(tile):
    for i in range(0, len(tile)):
        print(tile[i], '\n')

number_of_stars = 0

tile = [[0  ,0  ,0  ,0,  0,  0,  0,  0,0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0  ,0  ,0  ,0,  0,  0,  0,  0,255,255,0,  0,  0,  0,  0,  0,  0,255,255,  0,  0,  0],
        [0  ,0  ,0  ,0,  0,  0,  0,255,255,255,255,0,  0,  0,  0,  0,  0,255,255,  0,  0,  0],
        [0  ,0  ,0  ,0,  0,  0,  0,255,255,255,255,0,  0,  0,  0,  0,  0,  0,255,  0,  0,  0],
        [0  ,0  ,0  ,0,  0,  0,  0,  0,255,  0,  0,0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
        [0  ,0  ,0  ,0,  0,  0,  0,  0,0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0]]

for i in range(0, len(tile)):
    for j in range(0, len(tile[0])):
        if tile[i][j] == 255:
            flood_star(i, j, tile)
            number_of_stars += 1

show_tile(tile)
print()
            
print(number_of_stars)
