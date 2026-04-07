# Jogo da Velha — MinMax com Godot 4

Implementação do algoritmo MinMax aplicado ao Jogo da Velha,
desenvolvida em GDScript com a engine Godot 4.

## Como rodar

### 1. Instalar o Godot 4
- Acesse: https://godotengine.org/download
- Baixe a versão **Godot Engine 4.x — Standard** para o seu sistema
- Extraia o `.zip` e execute o `Godot_v4.x.exe` (não precisa de instalador)

### 2. Abrir o projeto
1. Na tela do **Gerenciador de Projetos**, clique em **Importar**
2. Navegue até a pasta `velha_godot/`
3. Selecione o arquivo `project.godot`
4. Clique em **Importar e Editar**

### 3. Rodar o jogo
- Pressione **F5** ou clique no botão ▶ no canto superior direito

## Como jogar

| Ação | O que faz |
|------|-----------|
| Clique numa célula | Faz sua jogada como X |
| Botão Reiniciar | Reinicia o jogo |

## Estrutura do projeto

```
velha_godot/
├── project.godot        # configurações da engine
├── scenes/
│   └── Main.tscn        # cena principal (layout visual)
└── scripts/
    └── Main.gd          # lógica do jogo + algoritmo MinMax
```

## Sobre o algoritmo MinMax

O MinMax é um algoritmo de busca para jogos de dois jogadores adversariais.
Ele explora toda a árvore de decisões possíveis e assume que o oponente
sempre joga de forma ótima.

- **+10** → IA venceu
- **-10** → Humano venceu
- **0**   → Empate

A IA é matematicamente imbatível — o melhor resultado possível para o
humano é o empate.

## Diferenças em relação à versão pygame (Python)

| Aspecto            | pygame (Python)              | Godot (GDScript)                  |
|--------------------|------------------------------|-----------------------------------|
| Loop principal     | `while True` manual          | Gerenciado pela engine            |
| Eventos de clique  | `pygame.event.get()` manual  | Sinais (`pressed.connect`)        |
| Renderização       | `pygame.draw.rect` manual    | Nós `Button` nativos              |
| Texto de status    | `pygame.font.render` manual  | Nó `Label` nativo                 |
| O algoritmo MinMax | Idêntico                     | Idêntico (só sintaxe diferente)   |
