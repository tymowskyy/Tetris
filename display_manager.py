import pygame
from settings import *


class DisplayManager:
    def __init__(self, win, bm):
        self.win = win
        self.bm = bm
        self.load_sprites()
        self.init_fonts()

    def init_fonts(self):
        pygame.font.init()
        self.font1 = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE, bold=True)
        self.font2 = pygame.font.SysFont(FONT_FAMILY, HIGH_SCORES_FONT_SIZE, bold=True)

    def load_sprites(self):
        sprite_sheet = pygame.image.load(TILES_PATH)
        self.tiles = []
        for i in range(15):
            self.tiles.append(self.get_sprite(sprite_sheet, i))
     
        sprite_sheet = pygame.image.load(BUTTONS_PATH)
        self.buttons = []
        for i in range(4):
            self.buttons.append(self.get_sprite(sprite_sheet, i))
            self.buttons[i] = pygame.transform.scale(self.buttons[i], BUTTONS_SIZE)

        self.background = pygame.image.load(BACKGROUND_PATH)

    def get_sprite(self, sheet, index):
        image = pygame.Surface((TILE_WIDTH, TILE_HEIGHT), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (index * TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT))
        return image

    def get_tile(self, index, projection):
        if projection:
            return self.tiles[index * 2 + 2]
        else:
            return self.tiles[index * 2 + 1]

    def draw_board(self):
        self.win.blit(self.background, (0, 0))
        self.draw_tiles()
        self.draw_block(self.bm.block_kind, [self.bm.block_pos[0], self.bm.block_proj], self.bm.block_rot, 1)
        self.draw_block(self.bm.block_kind, self.bm.block_pos, self.bm.block_rot, 0)
        self.draw_block_extra(self.bm.queue[0], SELF_NEXT_OFFSET, 0)
        if self.bm.holded != 0:
            self.draw_block_extra(self.bm.holded-1, SELF_HOLD_OFFSET, 0)
        self.draw_texts()
        self.draw_high_scores()

    def draw_tiles(self):
        for i in range(SIZE_X):
            for j in range(SIZE_Y):
                self.draw_tile((i*TILE_WIDTH + + BOARD_OFFSET[0], (SIZE_Y-j-1)*TILE_HEIGHT + + BOARD_OFFSET[1]), self.bm.board[j][i], 0)
    
    def draw_tile(self, pos, col, proj):
        if col==0:
            self.win.blit(self.tiles[0], pos)
        else:
            self.win.blit(self.get_tile(col-1, proj), pos)
    
    def draw_block(self, kind, pos, rot, proj):
        for i in range(4): # X
            for j in range(4): # Y
                if self.bm.blocks[kind][rot][j][i] and pos[1] - j < SIZE_Y:
                    self.draw_tile(((pos[0] + i) * TILE_WIDTH + BOARD_OFFSET[0], (SIZE_Y - pos[1] + j - 1) * TILE_HEIGHT + BOARD_OFFSET[1]), kind+1, proj)

    def draw_block_extra(self, kind, pos, rot):
        if kind == 0:
            new_pos = [pos[0], pos[1] - TILE_HEIGHT//2]
        elif kind == 1:
            new_pos = pos
        else:
            new_pos = [pos[0] + TILE_WIDTH//2, pos[1]]   
        for i in range(4): # X
            for j in range(4): # Y
                if self.bm.blocks[kind][rot][j][i]:
                    self.draw_tile((new_pos[0] + i*TILE_WIDTH, new_pos[1] + j*TILE_HEIGHT), kind+1, 0)
    
    def draw_text(self, text, offset, font):
        text_surface = font.render(str(text), True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(offset[0], offset[1]))
        self.win.blit(text_surface, text_rect)

    def draw_texts(self):
        self.draw_text(str(self.bm.score), SCORE_OFFSET, self.font1)
        self.draw_text(str(self.bm.level), LEVEL_OFFSET, self.font1)
        self.draw_text(str(self.bm.lines), LINES_OFFSET, self.font1)

    def draw_pause(self, hover):
        self.draw_board()
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_alpha(MENU_APLHA)
        surface.fill(MENU_COLOR)

        b1 = self.buttons[0]
        b2 = self.buttons[2]
        if hover == 1:
            b1 = self.buttons[1]
        elif hover == 2:
            b2 = self.buttons[3]

        self.win.blit(surface, (0, 0))
        self.win.blit(b1, RESUME_OFFSET)
        self.win.blit(b2, PLAY_AGAIN_OFFSET)
        pygame.display.flip()
    
    def draw_end_screen(self, name, hover):
        self.draw_board()
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.set_alpha(MENU_APLHA)
        surface.fill(MENU_COLOR)

        b = self.buttons[2]
        if hover:
            b = self.buttons[3]

        self.win.blit(surface, (0, 0))
        self.win.blit(b, PLAY_AGAIN_END_OFFSET)
        self.draw_text(name, END_SCREEN_NAME_OFFSET, self.font1)
        self.draw_text('GAME OVER! ENTER YOUR NAME:', END_SCREEN_TEXT_OFFSET, self.font1)
        pygame.display.flip()
    
    def draw_high_scores(self):
        for i, score in enumerate(self.bm.high_scores):
            self.draw_text(score[0] + ':', (HIGH_SCORES_OFFSET[0],
                HIGH_SCORES_OFFSET[1] + i*2*LINE_HEIGHT), self.font2)
            self.draw_text(score[1], (HIGH_SCORES_OFFSET[0],
                HIGH_SCORES_OFFSET[1] + (i*2+1)*LINE_HEIGHT), self.font2)