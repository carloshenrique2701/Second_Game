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
    imagem_tiro = pygame.transform.scale(pygame.image.load('imgs/missel.png'), (30, 30))
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

# Sistema de tiros melhorado
class Tiro_CLass:
    def __init__(self, x, y):
        self.ativo = True
        self.velocidade = 15
        self.rect = imagem_tiro.get_rect(center=(x, y))
    
    def update(self):
        if self.ativo:
            self.rect.y -= self.velocidade
            if self.rect.y < -30:
                self.ativo = False
    
    def draw(self):
        if self.ativo:
            janela.blit(imagem_tiro, self.rect)

# Lista para armazenar todos os tiros ativos
tiros_ativos = []
cooldown_tiro = 0  # Sistema de cooldown
COOLDOWN_MAX = 20  # Frames de espera entre tiros

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
    
    # Disparo - sistema melhorado
    if cooldown_tiro > 0:
        cooldown_tiro -= 1
    
    if teclas[pygame.K_SPACE] and cooldown_tiro == 0:
        tiros_ativos.append(Tiro_CLass(pos_x_player, pos_y_player - 40))  # Adiciona novo tiro
        cooldown_tiro = COOLDOWN_MAX  # Reseta o cooldown
    
    # Atualizações
    player_rect.center = (pos_x_player, pos_y_player)
    
    # Atualiza todos os tiros
    for tiro in tiros_ativos[:]:  # Usamos [:] para criar uma cópia da lista
        tiro.update()
        if not tiro.ativo:
            tiros_ativos.remove(tiro)
    
    # Atualiza inimigos e verifica colisões
    for inimigo in inimigos:
        inimigo.update()
        
        # Colisão com jogador
        if player_rect.colliderect(inimigo.rect):
            pontuacao -= 1
            inimigo.reset()
        
        # Colisão com tiros
        for tiro in tiros_ativos[:]:
            if tiro.ativo and tiro.rect.colliderect(inimigo.rect):
                pontuacao += 1
                tiro.ativo = False
                inimigo.reset()
                tiros_ativos.remove(tiro)
    
    # Renderização
    janela.blit(image_fundo, (0, 0))
    
    # Desenha todos os inimigos
    for inimigo in inimigos:
        inimigo.draw()
    
    # Desenha jogador
    janela.blit(nave_player, player_rect)
    
    # Desenha todos os tiros ativos
    for tiro in tiros_ativos:
        tiro.draw()
    
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