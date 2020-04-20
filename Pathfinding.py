import pygame

pygame.init()
pygame.font.init()
tlarg = 660
talt = 660

win = pygame.display.set_mode((tlarg + 150, talt))
font = pygame.font.SysFont('constantia', 30)

bg = (230, 230, 250)
black = (0, 0, 0)
block_color = (75, 0, 130)
finder_color = (220, 20, 60)
end_color = (255, 255, 0)
path_color = (0, 255, 127)
menu_color = (0, 0, 205)

blocks = []
key = [[0, 0], [14, 14]]
lock_find = False
lock_end = False
show_path = False


def distance(object1, object2):
    return ((object1[0] - object2[0]) ** 2 + (object1[1] - object2[1]) ** 2) ** 0.5


def draw_grid():
    for x in range(1, talt // 44 + 1):
        pygame.draw.line(win, black, (x * talt // 15, 0), (x * talt // 15, talt))
        pygame.draw.line(win, black, (0, x * talt // 15), (talt, x * talt // 15))


def draw_blocks():
    for block in blocks:
        pygame.draw.rect(win, block_color, (block[0] * talt // 15, block[1] * talt // 15, talt // 15, talt // 15))


def draw_keys():
    pygame.draw.rect(win, finder_color, (key[0][0] * (talt // 15), key[0][1] * (talt // 15), talt // 15, talt // 15))
    pygame.draw.rect(win, end_color, (key[1][0] * (talt // 15), key[1][1] * (talt // 15), talt // 15, talt // 15))


def draw_menu():
    pygame.draw.line(win, black, (talt, 0), (talt, talt), 5)
    pygame.draw.circle(win, menu_color, (talt + 75, talt // 2), 50)
    pygame.draw.circle(win, black, (talt + 75, talt // 2), 50, 1)
    if show_path:
        win.blit(font.render('Hide', False, black), (talt + 75 - 30, talt // 2 - 30))
    else:
        win.blit(font.render('Find', False, black), (talt + 75 - 30, talt // 2 - 30))
    win.blit(font.render('Path', False, black), (talt + 75 - 30, talt // 2))


def pathfind(start, end):
    queue = [[start[0], start[1], 0]]
    while True:
        for q in queue:
            if q[0] == end[0] and q[1] == end[1]:
                return queue
            to_remove = []
            adj = [[q[0] + 1, q[1], q[2] + 1],
                   [q[0] - 1, q[1], q[2] + 1],
                   [q[0], q[1] - 1, q[2] + 1],
                   [q[0], q[1] + 1, q[2] + 1]]
            for a in adj:
                if a[0] < 0 or a[1] < 0 or a[0] > 14 or a[1] > 14:
                    to_remove.append(a)
                elif [a[0], a[1]] in blocks:
                    to_remove.append(a)
                for qi in queue:
                    if qi[0] == a[0] and qi[1] == a[1] and qi[2] <= a[2]:
                        to_remove.append(a)
            for t in to_remove:
                if t in adj:
                    adj.remove(t)
            for a in adj:
                queue.append(a)


def filter_path(path):
    filtered = []
    for p in path:
        if p[0] == key[1][0] and p[1] == key[1][1]:
            filtered = [p]
    while len(filtered) < filtered[0][2]:
        candidates = []
        for p in path:
            if (p[0] == filtered[-1][0] and (p[1] == filtered[-1][1] - 1 or p[1] == filtered[-1][1] + 1)) or\
             (p[1] == filtered[-1][1] and (p[0] == filtered[-1][0] - 1 or p[0] == filtered[-1][0] + 1)):
                candidates.append(p)
        choosen = candidates[0]
        for candidate in candidates:
            if candidate[2] < choosen[2] and [candidate[0][1]] not in blocks:
                choosen = candidate
        filtered.append(choosen)
    return filtered


def draw_path(filtered_path):
    for tile in filtered_path:
        pygame.draw.rect(win, path_color, (tile[0] * talt // 15, tile[1] * talt // 15, (talt // 15), (talt // 15)))


run = True
while run:
    win.fill(bg)
    if show_path:
        draw_path(filter_path(pathfind(key[0], key[1])))
    draw_menu()
    draw_keys()
    draw_blocks()
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if distance(pygame.mouse.get_pos(), (tlarg + 75, talt // 2)) < 50:
                if show_path:
                    show_path = False
                else:
                    show_path = True
            if pygame.mouse.get_pos()[0] < talt:
                if pygame.mouse.get_pos()[0] // (talt // 15) == key[0][0] and\
                        pygame.mouse.get_pos()[1] // (talt // 15) == key[0][1]:
                    lock_find = True
                elif pygame.mouse.get_pos()[0] // (talt // 15) == key[1][0] and\
                        pygame.mouse.get_pos()[1] // (talt // 15) == key[1][1]:
                    lock_end = True
                elif lock_end:
                    key[1] = pygame.mouse.get_pos()[0] // (talt // 15), pygame.mouse.get_pos()[1] // (talt // 15)
                    lock_end = False
                elif lock_find:
                    key[0] = pygame.mouse.get_pos()[0] // (talt // 15), pygame.mouse.get_pos()[1] // (talt // 15)
                    lock_find = False
                else:
                    if [pygame.mouse.get_pos()[0] // (talt // 15), pygame.mouse.get_pos()[1] // (talt // 15)] in blocks:
                        blocks.remove([pygame.mouse.get_pos()[0] // (talt // 15),
                                       pygame.mouse.get_pos()[1] // (talt // 15)])
                    else:
                        blocks.append([pygame.mouse.get_pos()[0] // (talt // 15),
                                       pygame.mouse.get_pos()[1] // (talt // 15)])
    pygame.display.update()
