import pygame
import sys

# --- Configurações ---
LARGURA  = 600
ALTURA   = 700  # espaço extra embaixo para status
LINHAS   = 3
COLS     = 3

pygame.init()
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Velha — IA MinMax")

# --- Cores ---
BRANCO   = (255, 255, 255)
PRETO    = (0,   0,   0)
CINZA    = (200, 200, 200)
AZUL     = (70,  130, 220)   # jogador humano (X)
VERMELHO = (220, 70,  70)    # IA (O)
VERDE    = (50,  180, 100)   # linha vencedora
FUNDO    = (245, 245, 245)

# --- Fontes ---
FONTE_GRANDE  = pygame.font.SysFont("Arial", 120, bold=True)
FONTE_MEDIA   = pygame.font.SysFont("Arial", 36)
FONTE_PEQUENA = pygame.font.SysFont("Arial", 24)

# --- Constantes do jogo ---
HUMANO = "X"
IA     = "O"
VAZIO  = ""

# --- Tamanho de cada célula ---
TAM_CELULA = LARGURA // COLS  # 200px por célula


# ─────────────────────────────────────────────
#  ESTADO DO TABULEIRO
# ─────────────────────────────────────────────

def criar_tabuleiro():
    return [[VAZIO] * COLS for _ in range(LINHAS)]


def tabuleiro_cheio(board):
    return all(board[l][c] != VAZIO for l in range(3) for c in range(3))


def verificar_vencedor(board):
    """
    Retorna (vencedor, células_vencedoras).
    vencedor é 'X', 'O' ou None.
    """
    # Linhas e colunas
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != VAZIO:
            return board[i][0], [(i, 0), (i, 1), (i, 2)]
        if board[0][i] == board[1][i] == board[2][i] != VAZIO:
            return board[0][i], [(0, i), (1, i), (2, i)]

    # Diagonais
    if board[0][0] == board[1][1] == board[2][2] != VAZIO:
        return board[0][0], [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] != VAZIO:
        return board[0][2], [(0, 2), (1, 1), (2, 0)]

    return None, []


def movimentos_disponiveis(board):
    return [(l, c) for l in range(3) for c in range(3) if board[l][c] == VAZIO]


# ─────────────────────────────────────────────
#  ALGORITMO MINMAX
# ─────────────────────────────────────────────

def minmax(board, profundidade, eh_maximizando):

    vencedor, _ = verificar_vencedor(board)

    # Casos base
    if vencedor == IA:
        return 10 - profundidade
    if vencedor == HUMANO:
        return profundidade - 10
    if tabuleiro_cheio(board):
        return 0

    if eh_maximizando:
        # Turno da IA — quer maximizar o score
        melhor = -1000
        for (l, c) in movimentos_disponiveis(board):
            board[l][c] = IA
            score = minmax(board, profundidade + 1, False)
            board[l][c] = VAZIO
            melhor = max(melhor, score)
        return melhor

    else:
        # Turno do humano — IA assume que humano joga otimamente (minimiza)
        melhor = 1000
        for (l, c) in movimentos_disponiveis(board):
            board[l][c] = HUMANO
            score = minmax(board, profundidade + 1, True)
            board[l][c] = VAZIO
            melhor = min(melhor, score)
        return melhor


def melhor_jogada(board):
    """Avalia todos os movimentos disponíveis e retorna o de maior score."""
    melhor_score = -1000
    jogada = None

    for (l, c) in movimentos_disponiveis(board):
        board[l][c] = IA
        score = minmax(board, 0, False)
        board[l][c] = VAZIO

        if score > melhor_score:
            melhor_score = score
            jogada = (l, c)

    return jogada


# ─────────────────────────────────────────────
#  RENDERIZAÇÃO
# ─────────────────────────────────────────────

def desenhar_tabuleiro(board, celulas_vencedoras=[]):
    JANELA.fill(FUNDO)

    # Destaca células vencedoras
    for (l, c) in celulas_vencedoras:
        pygame.draw.rect(
            JANELA, VERDE,
            (c * TAM_CELULA + 4, l * TAM_CELULA + 4,
             TAM_CELULA - 8, TAM_CELULA - 8),
            border_radius=12
        )

    # Linhas do grid
    for i in range(1, 3):
        pygame.draw.line(JANELA, CINZA,
                         (i * TAM_CELULA, 0), (i * TAM_CELULA, LARGURA), 4)
        pygame.draw.line(JANELA, CINZA,
                         (0, i * TAM_CELULA), (LARGURA, i * TAM_CELULA), 4)

    # Peças X e O
    for l in range(3):
        for c in range(3):
            valor = board[l][c]
            if valor == VAZIO:
                continue
            cor   = AZUL if valor == HUMANO else VERMELHO
            texto = FONTE_GRANDE.render(valor, True, cor)
            rect  = texto.get_rect(
                center=(c * TAM_CELULA + TAM_CELULA // 2,
                        l * TAM_CELULA + TAM_CELULA // 2)
            )
            JANELA.blit(texto, rect)


def desenhar_status(mensagem, cor=PRETO):
    """Faixa de status abaixo do tabuleiro."""
    pygame.draw.rect(JANELA, BRANCO, (0, LARGURA, LARGURA, ALTURA - LARGURA))

    texto = FONTE_MEDIA.render(mensagem, True, cor)
    rect  = texto.get_rect(center=(LARGURA // 2, LARGURA + 45))
    JANELA.blit(texto, rect)

    dica = FONTE_PEQUENA.render("R = reiniciar", True, CINZA)
    JANELA.blit(dica, (20, LARGURA + 75))

    pygame.display.update()


# ─────────────────────────────────────────────
#  LOOP PRINCIPAL
# ─────────────────────────────────────────────

def main():
    board              = criar_tabuleiro()
    turno_humano       = True   # humano (X) sempre começa
    game_over          = False
    celulas_vencedoras = []

    while True:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Reinicia com R
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    board              = criar_tabuleiro()
                    turno_humano       = True
                    game_over          = False
                    celulas_vencedoras = []

            # Clique do humano
            if evento.type == pygame.MOUSEBUTTONDOWN and turno_humano and not game_over:
                x, y = pygame.mouse.get_pos()
                if y < LARGURA:   # clicou no tabuleiro, não na faixa de status
                    col = x // TAM_CELULA
                    lin = y // TAM_CELULA
                    if board[lin][col] == VAZIO:
                        board[lin][col] = HUMANO
                        turno_humano    = False

        # --- Renderização ---
        desenhar_tabuleiro(board, celulas_vencedoras)

        # --- Verifica estado do jogo ---
        vencedor, celulas_vencedoras = verificar_vencedor(board)

        if vencedor == HUMANO:
            desenhar_status("Você venceu! (isso não deveria acontecer...)", AZUL)
            game_over = True

        elif vencedor == IA:
            desenhar_status("IA venceu!", VERMELHO)
            game_over = True

        elif tabuleiro_cheio(board):
            desenhar_status("Empate!", CINZA)
            game_over = True

        elif not turno_humano and not game_over:
            # Vez da IA
            desenhar_status("IA pensando...", VERMELHO)
            pygame.display.update()
            pygame.time.delay(400)   # pausa para visualizar o "raciocínio"

            lin, col         = melhor_jogada(board)
            board[lin][col]  = IA
            turno_humano     = True

        else:
            desenhar_status("Sua vez! Clique em uma célula.", AZUL)

        pygame.display.update()


if __name__ == "__main__":
    main()
