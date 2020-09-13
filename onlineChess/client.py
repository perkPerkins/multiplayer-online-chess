import pygame
import colors
from network import Network
from board import Board
from text import Text
from button import Button
import initializer
from piece import Piece
from game import Game

WIDTH = 850
BOARD_WIDTH = 700
SQUARE_WIDTH = 87
BOARD_OFFSET = 75
ROWS = 8
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Cool chess game, dude")
icon = pygame.image.load('white_pawn.png')
pygame.display.set_icon(icon)


def new_name_screen(text):
    base_font = pygame.font.Font(None, 32)
    user_text = text
    center = screen.get_rect().center
    prompt = Text("Enter name here", center[0], center[1] - 25, 30)
    done_button = Button("Done", center[0] - 100, center[1] + 50, 200, 100, 30)
    done = False

    input_rect = pygame.Rect(center[0] - 100, center[1], 140, 32)
    color = pygame.Color("lightskyblue")

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    user_text = user_text.replace(",", "")
                    return user_text
                else:
                    user_text += event.unicode
            done = done_button.handle_event(event)
            if done:
                return user_text

        done_button.update()
        screen.fill(colors.BLACK)
        done_button.draw(screen)
        prompt.draw(screen)

        pygame.draw.rect(screen, color, input_rect, 5)

        text_surface = base_font.render(user_text, True, colors.WHITE)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        input_rect.w = max(200, text_surface.get_width() + 10)
        pygame.display.update()


def home_screen(name_button, game_button):
    new_game = False
    text = ""
    while not new_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            new_name = name_button.handle_event(event)
            if new_name:
                text = new_name_screen(text)
            new_game = game_button.handle_event(event)
            if new_game:
                break

        game_button.update()
        name_button.update()
        screen.fill(colors.BLACK)
        game_button.draw(screen)
        name_button.draw(screen)
        pygame.display.update()

    if text == "":
        return "Magnus#1632"
    return text


def image_at(rectangle, sheet, colorkey=None):
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
    image.blit(sheet, (0, 0), rect)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image


def load_piece_images():
    images = list()
    images.append(image_at((0, 0, 75, 76), pygame.image.load("white_pawn.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("white_rook.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("white_knight.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("white_bishop.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("white_queen.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("white_king.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("black_pawn.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("black_rook.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("black_knight.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("black_bishop.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("black_queen.png")))
    images.append(image_at((0, 0, 75, 76), pygame.image.load("black_king.png")))
    return images


def draw_square(screen, square):
    pygame.draw.line(screen, colors.RED, square, (square[0] + 87, square[1]), 5)
    pygame.draw.line(screen, colors.RED, (square[0] + 87, square[1]), (square[0] + 87, square[1] + 87), 5)
    pygame.draw.line(screen, colors.RED, (square[0] + 87, square[1] + 87), (square[0], square[1] + 87), 5)
    pygame.draw.line(screen, colors.RED, (square[0], square[1] + 87), square, 5)


def draw_screen(screen, grid, game, player, square):
    screen.fill(colors.LIGHT_GREY)

    for row in grid:
        for node in row:
            node.draw(screen)
    if square:
        draw_square(screen, square)
    if not game.ready:
        prompt = Text("Waiting for opponent....", WIDTH / 2, 30, 30, colors.RED, colors.LIGHT_GREY)
        prompt.draw(screen)
    else:
        if game.player_turn == player:
            prompt = Text("Your turn", WIDTH / 2, 30, 30, colors.RED, colors.LIGHT_GREY)
        else:
            if player == 0:
                opponent_name = game.player_two_name
            else:
                opponent_name = game.player_one_name
            prompt = Text(opponent_name + "'s Turn ", WIDTH / 2, 30, 30, colors.RED, colors.LIGHT_GREY)
        prompt.draw(screen)
    pygame.display.update()


def is_within_bounds(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


def generate_move(player_name, piece_position, row, col, checkmate=False):
    if checkmate:
        return player_name + ",mate"
    return player_name + "," + str(piece_position[0]) + "," + str(piece_position[1]) + "," + str(row) + "," + str(col)


    # LOS = Line Of Site (king's line of site)
def horizontal_vertical_LOS(king_pos, board, player_color, save_king=False):
    row = king_pos[0]
    col = king_pos[1] + 1
    while is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color == player_color:
                break
            else:
                piece_type = board[row][col].piece.type
                if save_king:
                    if piece_type == "pawn" and player_color != "white":
                        if abs(col - king_pos[1]) == 2 and not board[row][col].piece.has_moved:
                            return True, (row, col)
                        elif col - king_pos[1] == 1:
                            return True, (row, col)
                if piece_type == "queen" or piece_type == "rook":
                    return True, (row, col)
                else:
                    break
        col += 1

    row = king_pos[0] + 1
    col = king_pos[1]
    while is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color == player_color:
                break
            else:
                piece_type = board[row][col].piece.type
                if piece_type == "queen" or piece_type == "rook":
                    return True, (row, col)
                else:
                    break
        row += 1

    row = king_pos[0]
    col = king_pos[1] - 1
    while is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color == player_color:
                break
            else:
                piece_type = board[row][col].piece.type
                if save_king:
                    if piece_type == "pawn" and player_color != "black":
                        if abs(col - king_pos[1]) == 2 and not board[row][col].piece.has_moved:
                            return True, (row, col)
                        elif king_pos[1] - col == 1:
                            return True, (row, col)
                if piece_type == "queen" or piece_type == "rook":
                    return True, (row, col)
                else:
                    break
        col -= 1

    row = king_pos[0] - 1
    col = king_pos[1]
    while is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color == player_color:
                break
            else:
                piece_type = board[row][col].piece.type
                if piece_type == "queen" or piece_type == "rook":
                    return True, (row, col)
                else:
                    break
        row -= 1
    return False, None


def diagonal_LOS(king_pos, board, player_color, save_king=False):
    row = king_pos[0] + 1
    col = king_pos[1] + 1
    while is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color == player_color:
                break
            else:
                piece_type = board[row][col].piece.type
                if not save_king:
                    if piece_type == "pawn":
                        if abs(row - king_pos[0]) == 1 and abs(col - king_pos[1]) == 1:
                            return True, (row, col)
                if piece_type == "queen" or piece_type == "bishop":
                    return True, (row, col)
                else:
                    break
        col += 1
        row += 1

    row = king_pos[0] - 1
    col = king_pos[1] - 1
    while is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color == player_color:
                break
            else:
                piece_type = board[row][col].piece.type
                if not save_king:
                    if piece_type == "pawn":
                        if abs(row - king_pos[0]) == 1 and abs(col - king_pos[1]) == 1:
                            return True, (row, col)
                if piece_type == "queen" or piece_type == "bishop":
                    return True, (row, col)
                else:
                    break
        col -= 1
        row -= 1

    row = king_pos[0] + 1
    col = king_pos[1] - 1
    while is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color == player_color:
                break
            else:
                piece_type = board[row][col].piece.type
                if not save_king:
                    if piece_type == "pawn":
                        if abs(row - king_pos[0]) == 1 and abs(col - king_pos[1]) == 1:
                            return True, (row, col)
                if piece_type == "queen" or piece_type == "bishop":
                    return True, (row, col)
                else:
                    break
        col -= 1
        row += 1

    row = king_pos[0] - 1
    col = king_pos[1] + 1
    while is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color == player_color:
                break
            else:
                piece_type = board[row][col].piece.type
                if not save_king:
                    if piece_type == "pawn":
                        if abs(row - king_pos[0]) == 1 and abs(col - king_pos[1]) == 1:
                            return True, (row, col)
                if piece_type == "queen" or piece_type == "bishop":
                    return True, (row, col)
                else:
                    break
        col += 1
        row -= 1

    return False, None


def knight_check(king_pos, board, player_color):
    row = king_pos[0] - 1
    col = king_pos[1] - 2
    if is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color != player_color and board[row][col].piece.type == "knight":
                return True, (row, col)

    row = king_pos[0] - 2
    col = king_pos[1] - 1
    if is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color != player_color and board[row][col].piece.type == "knight":
                return True, (row, col)

    row = king_pos[0] - 2
    col = king_pos[1] + 1
    if is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color != player_color and board[row][col].piece.type == "knight":
                return True, (row, col)

    row = king_pos[0] - 1
    col = king_pos[1] + 2
    if is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color != player_color and board[row][col].piece.type == "knight":
                return True, (row, col)

    row = king_pos[0] + 1
    col = king_pos[1] + 2
    if is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color != player_color and board[row][col].piece.type == "knight":
                return True, (row, col)

    row = king_pos[0] + 2
    col = king_pos[1] + 1
    if is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color != player_color and board[row][col].piece.type == "knight":
                return True, (row, col)

    row = king_pos[0] + 2
    col = king_pos[1] - 1
    if is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color != player_color and board[row][col].piece.type == "knight":
                return True, (row, col)

    row = king_pos[0] + 1
    col = king_pos[1] - 2
    if is_within_bounds(row, col):
        if board[row][col].piece:
            if board[row][col].piece.color != player_color and board[row][col].piece.type == "knight":
                return True, (row, col)

    return False, None


def is_in_check(king_pos, board, player_color, save_king=False):
    in_check, checking_piece = diagonal_LOS(king_pos, board, player_color, save_king)
    if in_check:
        return True, checking_piece
    
    in_check, checking_piece = horizontal_vertical_LOS(king_pos, board, player_color, save_king)
    if in_check:
        return True, checking_piece

    in_check, checking_piece = knight_check(king_pos, board, player_color)
    if in_check:
        return True, checking_piece
    return False, None


def opponent_castle(board, old_pos, new_pos):
    if board.board[new_pos[0]][new_pos[1]].piece.type == "king" and abs(old_pos[0] - new_pos[0]) == 2:
        if new_pos[0] == 6:
            board.board[new_pos[0] - 1][new_pos[1]].piece = board.board[new_pos[0] + 1][new_pos[1]].piece
            board.board[new_pos[0] + 1][new_pos[1]].piece = None
        else:
            board.board[new_pos[0] + 1][new_pos[1]].piece = board.board[new_pos[0] - 2][new_pos[1]].piece
            board.board[new_pos[0] - 2][new_pos[1]].piece = None


def opponent_queen(board, new_pos, piece_list):
    if board.board[new_pos[0]][new_pos[1]].piece.type == "pawn" and (new_pos[1] == 0 or new_pos[1] == 7):
        if new_pos[1] == 7:
            board.board[new_pos[0]][new_pos[1]].piece = Piece(piece_list[10], "queen", "black")
        else:
            board.board[new_pos[0]][new_pos[1]].piece = Piece(piece_list[4], "queen", "white")


def update_opponent_move(player, opponent_move, board, game, piece_list):
    if player == 0:
        if opponent_move != game.player_two_move:
            old_pos = (int(game.player_two_move[0]), int(game.player_two_move[1]))
            new_pos = (int(game.player_two_move[2]), int(game.player_two_move[3]))
            board.board[new_pos[0]][new_pos[1]].piece = board.board[old_pos[0]][old_pos[1]].piece
            board.board[old_pos[0]][old_pos[1]].piece = None
            opponent_castle(board, old_pos, new_pos)
            opponent_queen(board, new_pos, piece_list)
            return game.player_two_move
    else:
        if opponent_move != game.player_one_move:
            old_pos = (int(game.player_one_move[0]), int(game.player_one_move[1]))
            new_pos = (int(game.player_one_move[2]), int(game.player_one_move[3]))
            board.board[new_pos[0]][new_pos[1]].piece = board.board[old_pos[0]][old_pos[1]].piece
            board.board[old_pos[0]][old_pos[1]].piece = None
            opponent_castle(board, old_pos, new_pos)
            opponent_queen(board, new_pos, piece_list)
            return game.player_one_move
    return opponent_move


def castle(board, piece_pos, row, column, king_pos, player_color):
    # if king is in check before or after castle
    in_check_before_castle, _ = is_in_check(king_pos, board.board, player_color)
    in_check_after_castle, _ = is_in_check((row, column), board.board, player_color)
    if in_check_before_castle or in_check_after_castle:
        return True, king_pos
    # king-side castle
    if row == 6:
        board.board[row][column].piece = board.board[piece_pos[0]][piece_pos[1]].piece
        board.board[piece_pos[0]][piece_pos[1]].piece = None
        board.board[row - 1][column].piece = board.board[row + 1][column].piece
        board.board[row + 1][column].piece = None
    # rook-side castle
    else:
        board.board[row][column].piece = board.board[piece_pos[0]][piece_pos[1]].piece
        board.board[piece_pos[0]][piece_pos[1]].piece = None
        board.board[row + 1][column].piece = board.board[row - 2][column].piece
        board.board[row - 2][column].piece = None

    board.board[row][column].piece.has_moved = True
    return False, (row, column)

# Yes this is messy as hell, but its the only way to do it while also keeping the computations as efficient as possible.
# Checkmate detection could be accomplished much more cleanly by keeping a list of all squares threatened by all pieces
# of the opposing color, but this is far more expensive. This way, we only check if the tiles surrounding the King are
# under attack
def king_is_trapped(king_pos, board, player_color):
    if is_within_bounds(king_pos[0] - 1, king_pos[1] - 1):
        if board[king_pos[0] - 1][king_pos[1] - 1].piece:
            if board[king_pos[0] - 1][king_pos[1] - 1].piece.color != player_color:
                in_check, _ = is_in_check((king_pos[0] - 1, king_pos[1] - 1), board, player_color)
                if not in_check:
                    return False
        else:
            in_check, _ = is_in_check((king_pos[0] - 1, king_pos[1] - 1), board, player_color)
            if not in_check:
                return False

    if is_within_bounds(king_pos[0] + 1, king_pos[1] + 1):
        if board[king_pos[0] + 1][king_pos[1] + 1].piece:
            if board[king_pos[0] + 1][king_pos[1] + 1].piece.color != player_color:
                in_check, _ = is_in_check((king_pos[0] + 1, king_pos[1] + 1), board, player_color)
                if not in_check:
                    return False
        else:
            in_check, _ = is_in_check((king_pos[0] + 1, king_pos[1] + 1), board, player_color)
            if not in_check:
                return False

    if is_within_bounds(king_pos[0] + 1, king_pos[1] - 1):
        if board[king_pos[0] + 1][king_pos[1] - 1].piece:
            if board[king_pos[0] + 1][king_pos[1] - 1].piece.color != player_color:
                in_check, _ = is_in_check((king_pos[0] + 1, king_pos[1] - 1), board, player_color)
                if not in_check:
                    return False
        else:
            in_check, _ = is_in_check((king_pos[0] + 1, king_pos[1] - 1), board, player_color)
            if not in_check:
                return False

    if is_within_bounds(king_pos[0] - 1, king_pos[1] + 1):
        if board[king_pos[0] - 1][king_pos[1] + 1].piece:
            if board[king_pos[0] - 1][king_pos[1] + 1].piece.color != player_color:
                in_check, _ = is_in_check((king_pos[0] - 1, king_pos[1] + 1), board, player_color)
                if not in_check:
                    return False
        else:
            in_check, _ = is_in_check((king_pos[0] - 1, king_pos[1] + 1), board, player_color)
            if not in_check:
                return False

    if is_within_bounds(king_pos[0] - 1, king_pos[1]):
        if board[king_pos[0] - 1][king_pos[1]].piece:
            if board[king_pos[0] - 1][king_pos[1]].piece.color != player_color:
                in_check, _ = is_in_check((king_pos[0] - 1, king_pos[1]), board, player_color)
                if not in_check:
                    return False
        else:
            in_check, _ = is_in_check((king_pos[0] - 1, king_pos[1]), board, player_color)
            if not in_check:
                return False

    if is_within_bounds(king_pos[0], king_pos[1] - 1):
        if board[king_pos[0]][king_pos[1] - 1].piece:
            if board[king_pos[0]][king_pos[1] - 1].piece.color != player_color:
                in_check, _ = is_in_check((king_pos[0], king_pos[1] - 1), board, player_color)
                if not in_check:
                    return False
        else:
            in_check, _ = is_in_check((king_pos[0], king_pos[1] - 1), board, player_color)
            if not in_check:
                return False

    if is_within_bounds(king_pos[0] + 1, king_pos[1]):
        if board[king_pos[0] + 1][king_pos[1]].piece:
            if board[king_pos[0] + 1][king_pos[1]].piece.color != player_color:
                in_check, _ = is_in_check((king_pos[0] + 1, king_pos[1]), board, player_color)
                if not in_check:
                    return False
        else:
            in_check, _ = is_in_check((king_pos[0] + 1, king_pos[1]), board, player_color)
            if not in_check:
                return False

    if is_within_bounds(king_pos[0], king_pos[1] + 1):
        if board[king_pos[0]][king_pos[1] + 1].piece:
            if board[king_pos[0]][king_pos[1] + 1].piece.color != player_color:
                in_check, _ = is_in_check((king_pos[0], king_pos[1] + 1), board, player_color)
                if not in_check:
                    return False
        else:
            in_check, _ = is_in_check((king_pos[0], king_pos[1] + 1), board, player_color)
            if not in_check:
                return False
    return True


def can_save_king(board, king_pos, threat_piece, player_color):
    # change player color to opponent's color, as we will be looking to see if the checking piece
    # can be taken
    player_color = "white" if player_color == "black" else "black"
    piece_type = board[threat_piece[0]][threat_piece[1]].piece.type

    # is_in_check will be used to determine if the checking piece is threatened, bc that's all that
    # function really does
    if piece_type == "pawn" or piece_type == "knight":
        return is_in_check(threat_piece, board, player_color), threat_piece
    else:
        # vertical
        if king_pos[0] == threat_piece[0]:
            high = max(king_pos[1], threat_piece[1]) + 1
            low = min(king_pos[1], threat_piece[1])
            for i in range(low, high):
                if board[threat_piece[0]][i].piece:
                    if board[threat_piece[0]][i].piece.type == "king":
                        continue
                # if current board location is threat piece, check if piece can be taken
                if i == threat_piece[1]:
                    in_check, saving_piece = is_in_check(threat_piece, board, player_color)
                    if in_check:
                        return True, saving_piece, threat_piece
                else:
                    in_check, saving_piece = is_in_check((threat_piece[0], i), board, player_color, True)
                    if in_check:
                        return True, saving_piece, (threat_piece[0], i)
        # horizontal
        elif king_pos[1] == threat_piece[1]:
            high = max(king_pos[0], threat_piece[0]) + 1
            low = min(king_pos[0], threat_piece[0])
            for i in range(low, high):
                if board[i][threat_piece[1]].piece:
                    if board[i][threat_piece[1]].piece.type == "king":
                        continue
                if i == threat_piece[0]:
                    in_check, saving_piece = is_in_check(threat_piece, board, player_color)
                    if in_check:
                        return True, saving_piece,
                else:
                    in_check, saving_piece = is_in_check((i, threat_piece[1]), board, player_color, True)
                    if in_check:
                        return True, saving_piece, (i, threat_piece[1])
        # diagonal (top left)
        elif threat_piece[0] < king_pos[0] and threat_piece[1] < king_pos[1]:
            i = threat_piece[0]
            j = threat_piece[1]
            for _ in range(abs(threat_piece[0] - king_pos[0])):
                if board[i][j].piece:
                    if board[i][j].piece.type == "king":
                        continue
                if i == threat_piece[0]:
                    in_check, saving_piece = is_in_check(threat_piece, board, player_color)
                    if in_check:
                        return True, saving_piece, threat_piece
                else:
                    in_check, saving_piece = is_in_check((i, j), board, player_color, True)
                    if in_check:
                        return True, saving_piece, (i, j)
                i += 1
                j += 1
        # diagonal bottom right
        elif threat_piece[0] > king_pos[0] and threat_piece[1] > king_pos[1]:
            i = threat_piece[0]
            j = threat_piece[1]
            for _ in range(abs(threat_piece[0] - king_pos[0])):
                if board[i][j].piece:
                    if board[i][j].piece.type == "king":
                        continue
                if i == threat_piece[0]:
                    in_check, saving_piece = is_in_check(threat_piece, board, player_color)
                    if in_check:
                        return True, saving_piece, threat_piece
                else:
                    in_check, saving_piece = is_in_check((i, j), board, player_color, True)
                    if in_check:
                        return True, saving_piece, (i, j)
                i -= 1
                j -= 1
        # diagonal bottom left
        elif threat_piece[0] < king_pos[0] and threat_piece[1] > king_pos[1]:
            i = threat_piece[0]
            j = threat_piece[1]
            for _ in range(abs(threat_piece[0] - king_pos[0])):
                if board[i][j].piece:
                    if board[i][j].piece.type == "king":
                        continue
                if i == threat_piece[0]:
                    in_check, saving_piece = is_in_check(threat_piece, board, player_color)
                    if in_check:
                        return True, saving_piece, threat_piece
                else:
                    in_check, saving_piece = is_in_check((i, j), board, player_color, True)
                    if in_check:
                        return True, saving_piece, (i, j)
                i += 1
                j -= 1
        else:   # threat_piece[0] > king_pos[0] and threat_piece[1] < king_pos[1]
            i = threat_piece[0]
            j = threat_piece[1]
            for _ in range(abs(threat_piece[0] - king_pos[0])):
                if board[i][j].piece:
                    if board[i][j].piece.type == "king":
                        continue
                if i == threat_piece[0]:
                    in_check, saving_piece = is_in_check(threat_piece, board, player_color)
                    if in_check:
                        return True, saving_piece, threat_piece
                else:
                    in_check, saving_piece = is_in_check((i, j), board, player_color, True)
                    if in_check:
                        return True, saving_piece, (i, j)
                i -= 1
                j += 1

        return False, None, None


def checkmate(game, opponent, screen, player):
    if game.loser is player:
        prompt = Text("You've been mated :(    " + opponent + " wins!", WIDTH / 2, 30, 30, colors.RED, colors.LIGHT_GREY)
    else:
        prompt = Text("You mated " + opponent + "!", WIDTH / 2, 30, 30, colors.RED, colors.LIGHT_GREY)

    prompt.draw(screen)
    pygame.display.update()

    # play again button


def update_board(board, piece_pos, row, column, king_pos, player_color, piece_list):
    piece = board.board[piece_pos[0]][piece_pos[1]].piece
    if piece.type == "king" and abs(piece_pos[0] - row) == 2:
        return castle(board, piece_pos, row, column, king_pos, player_color)

    board.board[piece_pos[0]][piece_pos[1]].piece = None
    board.board[row][column].piece = piece
    temp_king_pos = (row, column) if board.board[row][column].piece.type == "king" else king_pos
    in_check, _ = is_in_check(temp_king_pos, board.board, player_color)
    # if king still in check after move, the move is invalid
    if in_check:
        piece = board.board[row][column].piece
        board.board[row][column].piece = None
        board.board[piece_pos[0]][piece_pos[1]].piece = piece
    else:
        if piece.type == "pawn" and (column == 7 or column == 0):
            if column == 7:
                board.board[row][column].piece = Piece(piece_list[10], "queen", "black")
            else:
                board.board[row][column].piece = Piece(piece_list[4], "queen", "white")
        king_pos = temp_king_pos
        board.board[row][column].piece.has_moved = True
    return in_check, king_pos


def main():
    run = True
    piece_selected = False
    in_check = False
    piece_pos = ()
    pygame.init()
    center = screen.get_rect().center
    name_button = Button("Choose Name", center[0] - 200, center[1] - 200, 400, 200, 40)
    play_now_button = Button("Play Now", center[0] - 200, center[1] + 50, 400, 200, 40, colors.GREEN, colors.LIGHT_GREEN)
    player_name = home_screen(name_button, play_now_button)

    board = Board()
    board.board, piece_list = initializer.initialize_board(board.board, load_piece_images())
    n = Network()
    player = int(n.player_number)
    player_color = "white" if player == 0 else "black"
    king_position = (4, 7) if player_color == "white" else (4, 0)
    opponent_move = ""
    square = None
    print("You are player: ", player)

    while run:
        try:
            message = player_name + ",get"
            game = n.send(message)
            if game.loser != -1:
                if player == 0:
                    checkmate(game, game.player_two_name, screen, player)
                else:
                    checkmate(game, game.player_one_name, screen, player)
        except:
            run = False
            print("couldn't get game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if game.player_turn == player and game.ready:
                opponent_move = update_opponent_move(player, opponent_move, board, game, piece_list)
                in_check, threat_piece = is_in_check(king_position, board.board, player_color)
                if in_check:
                    if king_is_trapped(king_position, board.board, player_color):
                        can_be_saved, savior, block = can_save_king(board.board, king_position, threat_piece, player_color)
                        if can_be_saved:
                            board.board[block[0]][block[1]].piece = board.board[savior[0]][savior[1]].piece
                            board.board[savior[0]][savior[1]].piece = None
                            in_check, _ = is_in_check(king_position, board.board, player_color)
                            if in_check:
                                print("CHECKMATE")
                                if player == 0:
                                    checkmate(game, game.player_two_name, screen, player)
                                else:
                                    checkmate(game, game.player_one_name, screen, player)
                                n.send(generate_move(player_name, piece_pos, -1, -1, True))

                            board.board[savior[0]][savior[1]].piece = board.board[block[0]][block[1]].piece
                            board.board[block[0]][block[1]].piece = None
                        else:
                            print("CHECKMATE")
                            if player == 0:
                                checkmate(game, game.player_two_name, screen, player)
                            else:
                                checkmate(game, game.player_one_name, screen, player)
                            n.send(generate_move(player_name, piece_pos, -1, -1, True))

                    else:
                        print("NOT CHECKMATE")

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if not piece_selected:
                        row = (pos[0] - BOARD_OFFSET) // (BOARD_WIDTH // 8)
                        column = (pos[1] - BOARD_OFFSET) // (BOARD_WIDTH // 8)
                        if is_within_bounds(row, column):
                            if board.board[row][column].piece:
                                if board.board[row][column].piece.color == player_color:
                                    square = (BOARD_OFFSET + (SQUARE_WIDTH * row), (BOARD_OFFSET + (SQUARE_WIDTH * column)))
                                    piece_pos = (row, column)
                                    piece_selected = True
                    else:
                        row = (pos[0] - BOARD_OFFSET) // (BOARD_WIDTH // 8)
                        column = (pos[1] - BOARD_OFFSET) // (BOARD_WIDTH // 8)

                        if board.is_valid_move(piece_pos[0], piece_pos[1], row, column, player_color):
                            in_check, king_position = update_board(board, piece_pos, row, column, king_position, player_color, piece_list)
                            if not in_check:
                                n.send(generate_move(player_name, piece_pos, row, column))
                        square = None
                        piece_selected = False

        draw_screen(screen, board.board, game, player, square)


main()
