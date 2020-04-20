import pygame

pygame.init()
pygame.font.init()
tlarg = 660
talt = 660
grid_size = 10

win = pygame.display.set_mode((tlarg + 150, talt))
font = pygame.font.SysFont('constantia', 30)
big = pygame.font.SysFont('constantia', 60)


bg = (230, 230, 250)
black = (0, 0, 0)
block_color = (75, 0, 130)
finder_color = (220, 20, 60)
end_color = (255, 255, 0)
path_color = (0, 255, 127)
over_block_color = (60, 179, 113)
menu_color = (0, 0, 205)
menu_color2 = (255, 165, 0)

blocks = []
key = [[0, 0], [grid_size - 1, grid_size - 1]]
lock_find = False
lock_end = False
show_path = False
wall_breaks = 0


def distance(object1, object2):
    return ((object1[0] - object2[0]) ** 2 + (object1[1] - object2[1]) ** 2) ** 0.5


def draw_grid():
    for x in range(1, grid_size):
        pygame.draw.line(win, black, (x * talt / grid_size, 0), (x * talt / grid_size, talt))
        pygame.draw.line(win, black, (0, x * talt / grid_size), (talt, x * talt / grid_size))


def draw_blocks():
    for block in blocks:
        pygame.draw.rect(win, block_color, (block[0] * talt / grid_size, block[1] * talt / grid_size,
                                            talt / grid_size, talt / grid_size))


def draw_keys():
    pygame.draw.rect(win, finder_color, (key[0][0] * (talt / grid_size), key[0][1] * (talt / grid_size),
                                         talt / grid_size, talt / grid_size))
    pygame.draw.rect(win, end_color, (key[1][0] * (talt / grid_size), key[1][1] * (talt / grid_size),
                                      talt / grid_size, talt / grid_size))


def draw_menu():
    pygame.draw.line(win, black, (talt, 0), (talt, talt), 5)

    pygame.draw.circle(win, menu_color, (talt + 75, talt // 2), 50)
    pygame.draw.circle(win, black, (talt + 75, talt // 2), 50, 1)
    if show_path:
        win.blit(font.render('Hide', False, black), (talt + 75 - 30, talt // 2 - 30))
    else:
        win.blit(font.render('Find', False, black), (talt + 75 - 30, talt // 2 - 30))
    win.blit(font.render('Path', False, black), (talt + 75 - 30, talt // 2))

    pygame.draw.circle(win, menu_color, (talt + 75, talt // 4 - 25), 50)
    pygame.draw.circle(win, black, (talt + 75, talt // 4 - 25), 50, 1)
    win.blit(big.render(str(grid_size), False, black), (talt + 75 - 25, talt // 4 - 55))

    pygame.draw.circle(win, menu_color2, (talt + 75, talt // 8 - 25), 25)
    pygame.draw.circle(win, black, (talt + 75, talt // 8 - 25), 25, 1)
    win.blit(big.render('+', False, black), (talt + 75 - 15, talt // 8 - 55))

    pygame.draw.circle(win, menu_color2, (talt + 75, 3 * talt // 8 - 25), 25)
    pygame.draw.circle(win, black, (talt + 75, 3 * talt // 8 - 25), 25, 1)
    win.blit(big.render('-', False, black), (talt + 75 - 10, 3 * talt // 8 - 55))

    pygame.draw.circle(win, menu_color, (talt + 75, 3 * talt // 4 + 25), 50)
    pygame.draw.circle(win, black, (talt + 75, 3 * talt // 4 + 25), 50, 1)
    win.blit(big.render(str(wall_breaks), False, black), (talt + 75 - 10, 3 * talt // 4 - 8))

    pygame.draw.circle(win, menu_color2, (talt + 75, 7 * talt // 8 + 25), 25)
    pygame.draw.circle(win, black, (talt + 75, 7 * talt // 8 + 25), 25, 1)
    win.blit(big.render('+', False, black), (talt + 75 - 15, 7 * talt // 8 - 5))

    pygame.draw.circle(win, menu_color2, (talt + 75, 5 * talt // 8 + 25), 25)
    pygame.draw.circle(win, black, (talt + 75, 5 * talt // 8 + 25), 25, 1)
    win.blit(big.render('-', False, black), (talt + 75 - 10, 5 * talt // 8 - 5))


def pathfind(start, end):
    queue = [[[start[0], start[1], 0, wall_breaks]]]
    tries = 0
    while True:
        if tries > grid_size ** 2:
            return []
        tries += 1
        for q in queue:
            if q[-1][0] == end[0] and q[-1][1] == end[1]:
                return q
            to_remove = []
            adj = [[q[-1][0] + 1, q[-1][1], q[-1][2] + 1, q[-1][3]],
                   [q[-1][0] - 1, q[-1][1], q[-1][2] + 1, q[-1][3]],
                   [q[-1][0], q[-1][1] - 1, q[-1][2] + 1, q[-1][3]],
                   [q[-1][0], q[-1][1] + 1, q[-1][2] + 1, q[-1][3]]]
            for a in adj:
                if a[0] < 0 or a[1] < 0 or a[0] >= grid_size or a[1] >= grid_size:
                    to_remove.append(a)
                elif [a[0], a[1]] in blocks:
                    if a[3] > 0:
                        a[3] -= 1
                    else:
                        to_remove.append(a)
                for qi in queue:
                    if qi[-1][0] == a[0] and qi[-1][1] == a[1] and qi[-1][2] <= a[2]:
                        if qi[-1][3] >= a[3]:
                            to_remove.append(a)
                        else:
                            queue = [x for x in queue if not x[-1] == qi[-1]]
            for t in to_remove:
                if t in adj:
                    adj.remove(t)
            for a in adj:
                inter = q.copy()
                inter.append(a)
                queue.append(inter)


def draw_path(filtered_path):
    for tile in filtered_path:
        cor = path_color
        for block in blocks:
            if block[0] == tile[0] and block[1] == tile[1]:
                cor = over_block_color
        pygame.draw.rect(win, cor, (tile[0] * talt / grid_size, tile[1] * talt / grid_size,
                                           (talt / grid_size), (talt / grid_size)))


run = True
while run:
    win.fill(bg)
    draw_blocks()
    if show_path:
        draw_path(pathfind(key[0], key[1]))
    draw_keys()
    draw_menu()
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
            elif distance(pygame.mouse.get_pos(), (talt + 75, talt // 8 - 25)) < 25 and not show_path:
                grid_size += 1
            elif distance(pygame.mouse.get_pos(), (talt + 75, 3 * talt // 8 - 25)) < 25 and not show_path:
                if grid_size > 2:
                    grid_size -= 1
                    if key[1][0] == grid_size:
                        key[1][0] = grid_size - 1
                    if key[1][1] == grid_size:
                        key[1][1] = grid_size - 1
                    for block in blocks:
                        if block[0] == grid_size:
                            block[0] = grid_size - 1
                        if block[1] == grid_size:
                            block[1] = grid_size - 1
                        if blocks.count(block) > 1 or (block[0] == key[0][0] and block[1] == key[0][1]) or \
                                (block[0] == key[1][0] and block[1] == key[1][1]):
                            blocks = [x for x in blocks if not x == block]
            elif distance(pygame.mouse.get_pos(), (talt + 75, 7 * talt // 8 + 25)) < 25 and not show_path:
                wall_breaks += 1
            elif distance(pygame.mouse.get_pos(), (talt + 75, 5 * talt // 8 + 25)) < 25 and not show_path:
                if wall_breaks > 0:
                    wall_breaks -= 1

            if pygame.mouse.get_pos()[0] < talt:
                if pygame.mouse.get_pos()[0] // (talt / grid_size) == key[0][0] and\
                        pygame.mouse.get_pos()[1] // (talt / grid_size) == key[0][1]:
                    lock_find = True
                elif pygame.mouse.get_pos()[0] // (talt / grid_size) == key[1][0] and\
                        pygame.mouse.get_pos()[1] // (talt / grid_size) == key[1][1]:
                    lock_end = True
                elif lock_end:
                    key[1] = pygame.mouse.get_pos()[0] // (talt / grid_size),\
                             pygame.mouse.get_pos()[1] // (talt / grid_size)
                    lock_end = False
                elif lock_find:
                    key[0] = pygame.mouse.get_pos()[0] // (talt / grid_size),\
                             pygame.mouse.get_pos()[1] // (talt / grid_size)
                    lock_find = False
                else:
                    if [pygame.mouse.get_pos()[0] // (talt / grid_size), pygame.mouse.get_pos()[1] //
                     (talt / grid_size)] in blocks:blocks.remove([pygame.mouse.get_pos()[0] // (talt / grid_size),
                                                                   pygame.mouse.get_pos()[1] // (talt / grid_size)])
                    else:
                        blocks.append([pygame.mouse.get_pos()[0] // (talt / grid_size),
                                       pygame.mouse.get_pos()[1] // (talt / grid_size)])
    pygame.display.update()
