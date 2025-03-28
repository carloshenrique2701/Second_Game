import pygame
from pygame import mixer
from random import randint

# Inicialização do Pygame
pygame.init()

# Configurações da janela
LARGURA, ALTURA = 1280, 720
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Space Invaders')

# Carregamento de imagens
try:
    # Fundo e sprites
    image_fundo = pygame.image.load('imgs/fundo.png').convert()
    nave_player = pygame.transform.scale(pygame.image.load('imgs/nave_aliada.png'), (80, 80))
    nave_inimiga = pygame.transform.scale(pygame.image.load('imgs/nave_inimiga.png'), (80, 80))
    tiro = pygame.transform.scale(pygame.image.load('imgs/missel.png'), (30, 30))
except pygame.error as e:
    print(f"Erro ao carregar imagens: {e}")
    pygame.quit()
    exit()

# Variáveis do jogador
pos_x_player, pos_y_player = LARGURA // 2, ALTURA - 100
vel_nave_player = 8
player_rect = nave_player.get_rect(center=(pos_x_player, pos_y_player))

# Sistema de inimigos
class Inimigo:
    def __init__(self):
        self.reset()
        self.velocidade = 3
        self.rect = nave_inimiga.get_rect(center=(self.x, self.y))
    
    def reset(self):
        self.x = randint(50, LARGURA - 50)
        self.y = randint(-100, -40)
    
    def update(self):
        self.y += self.velocidade
        self.rect.center = (self.x, self.y)
        if self.y > ALTURA + 50:
            self.reset()
    
    def draw(self):
        janela.blit(nave_inimiga, self.rect)

# Cria vários inimigos
inimigos = [Inimigo() for _ in range(5)]  # 5 inimigos

# Sistema de tiros
class Tiro:
    def __init__(self):
        self.ativo = False
        self.velocidade = 15
        self.rect = tiro.get_rect()
    
    def disparar(self, x, y):
        self.ativo = True
        self.rect.center = (x, y - 40)  # Posiciona acima da nave
    
    def update(self):
        if self.ativo:
            self.rect.y -= self.velocidade
            if self.rect.y < -30:
                self.ativo = False
    
    def draw(self):
        if self.ativo:
            janela.blit(tiro, self.rect)

tiro_player = Tiro()
cooldown_tiro = 0  # Sistema de cooldown

# Pontuação
pontuacao = 0
fonte = pygame.font.SysFont('Arial', 30)

# Clock para controle de FPS
clock = pygame.time.Clock()
FPS = 60

# Loop principal
running = True
while running:
    # Controle de FPS
    clock.tick(FPS)
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movimentação do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and pos_y_player > 20:
        pos_y_player -= vel_nave_player
    if teclas[pygame.K_DOWN] and pos_y_player < ALTURA - 80:
        pos_y_player += vel_nave_player
    if teclas[pygame.K_LEFT] and pos_x_player > 20:
        pos_x_player -= vel_nave_player
    if teclas[pygame.K_RIGHT] and pos_x_player < LARGURA - 80:
        pos_x_player += vel_nave_player
    
    # Disparo
    if cooldown_tiro > 0:
        cooldown_tiro -= 1
    
    if teclas[pygame.K_SPACE] and not tiro_player.ativo and cooldown_tiro == 0:
        tiro_player.disparar(pos_x_player, pos_y_player)
        cooldown_tiro = 15  # Cooldown de 15 frames
    
    # Atualizações
    player_rect.center = (pos_x_player, pos_y_player)
    tiro_player.update()
    
    # Atualiza inimigos e verifica colisões
    for inimigo in inimigos:
        inimigo.update()
        
        # Colisão com jogador
        if player_rect.colliderect(inimigo.rect):
            pontuacao -= 1
            inimigo.reset()
        
        # Colisão com tiro
        if tiro_player.ativo and tiro_player.rect.colliderect(inimigo.rect):
            pontuacao += 1
            tiro_player.ativo = False
            inimigo.reset()
    
    # Renderização
    janela.blit(image_fundo, (0, 0))
    
    # Desenha todos os inimigos
    for inimigo in inimigos:
        inimigo.draw()
    
    # Desenha jogador e tiro
    janela.blit(nave_player, player_rect)
    tiro_player.draw()
    
    # Mostra pontuação
    texto_pontuacao = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
    janela.blit(texto_pontuacao, (20, 20))
    
    pygame.display.update()

# Fim do jogo
pygame.quit()
if pontuacao < 0:
    print('Você perdeu o Jogo! GAME OVER!')
else:
    print('Você ganhou o Jogo! PARABÉNS!')
print('-=' * 20)
