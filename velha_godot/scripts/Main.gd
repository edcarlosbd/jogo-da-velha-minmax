extends Node

# ─────────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────────
const HUMANO = "X"
const IA     = "O"
const VAZIO  = ""

# ─────────────────────────────────────────────
#  VARIÁVEIS DE ESTADO
# ─────────────────────────────────────────────
var board        = []   # tabuleiro 3x3
var turno_humano = true
var game_over    = false

# Referências aos nós da cena (preenchidas automaticamente ao carregar)
@onready var botoes        = $GridContainer.get_children()
@onready var label         = $LabelStatus
@onready var btn_reiniciar = $BotaoReiniciar


# ─────────────────────────────────────────────
#  INICIALIZAÇÃO
# ─────────────────────────────────────────────
func _ready():
	# _ready() é chamado automaticamente quando a cena carrega.
	# Equivale ao início do main() no pygame.
	criar_tabuleiro()
	conectar_botoes()
	label.text = "Sua vez!"


func criar_tabuleiro():
	board = []
	for l in range(3):
		board.append([VAZIO, VAZIO, VAZIO])


func conectar_botoes():
	# Conecta o clique de cada botão a uma função com o índice correto.
	# No pygame isso era feito manualmente no loop de eventos.
	for i in range(9):
		var idx = i
		botoes[i].pressed.connect(func(): clique_humano(idx))
	btn_reiniciar.pressed.connect(reiniciar)


# ─────────────────────────────────────────────
#  ESTADO DO TABULEIRO
# ─────────────────────────────────────────────
func tabuleiro_cheio() -> bool:
	for l in range(3):
		for c in range(3):
			if board[l][c] == VAZIO:
				return false
	return true


func verificar_vencedor() -> Array:
	# Retorna [vencedor, células_vencedoras]
	# vencedor é "X", "O" ou null

	# Linhas
	for i in range(3):
		if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != VAZIO:
			return [board[i][0], [[i,0],[i,1],[i,2]]]

	# Colunas
	for i in range(3):
		if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != VAZIO:
			return [board[0][i], [[0,i],[1,i],[2,i]]]

	# Diagonal principal
	if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != VAZIO:
		return [board[0][0], [[0,0],[1,1],[2,2]]]

	# Diagonal secundária
	if board[0][2] == board[1][1] and board[1][1] == board[2][0] and board[0][2] != VAZIO:
		return [board[0][2], [[0,2],[1,1],[2,0]]]

	return [null, []]


func movimentos_disponiveis() -> Array:
	var moves = []
	for l in range(3):
		for c in range(3):
			if board[l][c] == VAZIO:
				moves.append([l, c])
	return moves


# ─────────────────────────────────────────────
#  ALGORITMO MINMAX
# ─────────────────────────────────────────────
func minmax(profundidade: int, eh_maximizando: bool) -> int:
	# Avalia recursivamente todos os estados possíveis do jogo.
	#
	# Scores:
	#   +10 - profundidade  →  IA venceu  (vitórias mais rápidas valem mais)
	#   -10 + profundidade  →  Humano venceu
	#    0                  →  Empate

	var resultado = verificar_vencedor()
	var vencedor  = resultado[0]

	# Casos base
	if vencedor == IA:     return 10 - profundidade
	if vencedor == HUMANO: return profundidade - 10
	if tabuleiro_cheio():  return 0

	if eh_maximizando:
		# Turno da IA — quer maximizar o score
		var melhor = -1000
		for mov in movimentos_disponiveis():
			board[mov[0]][mov[1]] = IA
			var score = minmax(profundidade + 1, false)
			board[mov[0]][mov[1]] = VAZIO
			melhor = max(melhor, score)
		return melhor
	else:
		# Turno do humano — IA assume que humano joga otimamente (minimiza)
		var melhor = 1000
		for mov in movimentos_disponiveis():
			board[mov[0]][mov[1]] = HUMANO
			var score = minmax(profundidade + 1, true)
			board[mov[0]][mov[1]] = VAZIO
			melhor = min(melhor, score)
		return melhor


func melhor_jogada() -> Array:
	# Avalia todos os movimentos disponíveis e retorna o de maior score.
	var melhor_score = -1000
	var jogada       = []

	for mov in movimentos_disponiveis():
		board[mov[0]][mov[1]] = IA
		var score = minmax(0, false)
		board[mov[0]][mov[1]] = VAZIO

		if score > melhor_score:
			melhor_score = score
			jogada       = mov

	return jogada


# ─────────────────────────────────────────────
#  EVENTOS E RENDERIZAÇÃO
# ─────────────────────────────────────────────
func clique_humano(idx: int):
	# Chamado automaticamente pelo sinal do botão clicado.
	# Substitui o bloco MOUSEBUTTONDOWN do pygame.
	if game_over or not turno_humano:
		return

	var lin = idx / 3
	var col = idx % 3

	if board[lin][col] != VAZIO:
		return

	board[lin][col] = HUMANO
	atualizar_visual()
	turno_humano = false
	verificar_fim()

	if not game_over:
		await jogada_ia()


func jogada_ia():
	# await get_tree().process_frame garante que o label "IA pensando..."
	# apareça na tela antes de o cálculo bloquear o frame.
	label.text = "IA pensando..."
	await get_tree().process_frame

	var jogada = melhor_jogada()
	board[jogada[0]][jogada[1]] = IA
	atualizar_visual()
	turno_humano = true
	verificar_fim()

	if not game_over:
		label.text = "Sua vez!"


func atualizar_visual():
	# Atualiza o texto de cada botão conforme o estado do tabuleiro.
	# Substitui todo o desenhar_tabuleiro() do pygame.
	for i in range(9):
		var lin = i / 3
		var col = i % 3
		botoes[i].text = board[lin][col]


func verificar_fim():
	var resultado          = verificar_vencedor()
	var vencedor           = resultado[0]
	var celulas_vencedoras = resultado[1]

	if vencedor == HUMANO:
		label.text = "Você venceu! (isso não deveria acontecer...)"
		destacar_vencedor(celulas_vencedoras)
		game_over = true
	elif vencedor == IA:
		label.text = "IA venceu!"
		destacar_vencedor(celulas_vencedoras)
		game_over = true
	elif tabuleiro_cheio():
		label.text = "Empate!"
		game_over = true


func destacar_vencedor(celulas: Array):
	# Pinta os botões vencedores de verde.
	# No pygame isso era feito com pygame.draw.rect na cor VERDE.
	for cel in celulas:
		var idx = cel[0] * 3 + cel[1]
		botoes[idx].modulate = Color(0.2, 0.9, 0.4)


func reiniciar():
	criar_tabuleiro()
	game_over    = false
	turno_humano = true
	atualizar_visual()
	label.text = "Sua vez!"
	# Remove o destaque verde das células vencedoras
	for b in botoes:
		b.modulate = Color.WHITE
