#librerie necessarie
import pygame as py
import random

#inizializzazione
py.init()


LUNGHEZZA_FINESTRA = 600
ALTEZZA_FINESTRA = 800
finestra = py.display.set_mode((LUNGHEZZA_FINESTRA, ALTEZZA_FINESTRA))
py.display.set_caption('Videogioco di salto')

#stato del gioco
run = True  
game_over = False

#definisco il frame rate in modo che gli elementi siano visibili (che non aggiorni la schermata troppo velocemente)
orologio = py.time.Clock()
FPS = 60

#variabili che conterranno i colori e font
BIANCO = (255, 255, 255)
NERO = (0,0,0)
ROSSO = (255, 10, 10)
font_piccolo = py.font.SysFont('Arial', 20)
font_grande = py.font.SysFont('Arial', 26)
font_gameover = py.font.SysFont('Arial', 80)

ZONA_SCORRIMENTO = 200  #valore che, se superato, innesca lo scorrimento
GRAVITA = 1  #velocità caduta
MAX_PIATTAFORME = 10  #piattafome massime creabili allo stesso momento
scrorre = 0
background_scorrimento = 0  #scorrimento del background
punteggio = 0
record = 0  #contiene il punteggio massimo fatto
dissolvenza = 0

#carico le immagini
img_background = py.transform.scale(py.image.load("bg.png"), (600, 800)).convert_alpha() #carico coi bordi trasparenti e ingrandisco
img_sole = py.transform.scale(py.image.load('sole.png'), (700,700)).convert_alpha()
img_personaggio = py.image.load('pannello1.png').convert_alpha()
img_piattaforma = py.image.load('nuvola.png').convert_alpha()



def stampa_testo(testo, font, colore, x, y): #stampa il testo
	img = font.render(testo, True, colore)
	finestra.blit(img, (x,y))

def mostra_punteggio():
	stampa_testo('PUNTEGGIO: ' + str(punteggio), font_piccolo, BIANCO, 10, 0)

def disegna_background(background_scorrimento): #continua a disegnare lo sfondo caricando quello precedente
	finestra.blit(img_background, (0, 0 + background_scorrimento))
	finestra.blit(img_background, (0, -800 + background_scorrimento))

	finestra.blit(img_sole, (300, -450 + scorrimento))


class Pannello():  #classe del pannello (personaggio che si muove)

	def __init__(self, x, y):  #inizializzazione della classe (costruttore)
		self.image = py.transform.scale(img_personaggio, (50, 50))
		self.lunghezza = 42
		self.altezza = 50
		self.rect = py.Rect(0, 0, self.lunghezza, self.altezza)
		self.rect.center = (x, y)
		self.gira = False  #variabile che specchia l'immagine
		self.vely = 0


	def muovi(self):  #movimento del pannello

		#inizializzazione variabili del movimento
		scorrimento = 0
		dx = 0
		dy = 0

		#controllo pressione dei tasti per il movimento
		key = py.key.get_pressed()
		if key[py.K_a]:
			dx = -10
			self.gira = False
		if key[py.K_d]:
			dx = 10
			self.gira = True

		#aumento di velocità in caduta
		self.vely += GRAVITA
		dy += self.vely

		#controllo che il presonaggio non esca dai bordi della finestra
		if self.rect.left + dx < 0 or self.rect.right + dx > LUNGHEZZA_FINESTRA:
			dx = 0

		#controlla collisioni con le piattaforme
		for piattaforma in gruppo_piattaforme:
			if piattaforma.rect.colliderect(self.rect.x, self.rect.y + dy, self.lunghezza, self.altezza):
				#se il personaggio è sopra la piattaforma
				if self.rect.bottom < piattaforma.rect.centery:
					if self.vely > 0:
						self.rect.bottom = piattaforma.rect.top
						dy = 0
						self.vely = -20

		#controlla salto verso il limite superiore della finestra
		if self.rect.top <= ZONA_SCORRIMENTO:
			if self.vely < 0: #se sta saltando
				scorrimento = -dy

		#aggiornamento posizione personaggio
		self.rect.x += dx
		self.rect.y += dy + scorrimento
		
		return scorrimento
		

	def disegna(self):  #disegno il pannello
		finestra.blit(py.transform.flip(self.image, self.gira, False), (self.rect.x - 5, self.rect.y - 5))
		#py.draw.rect(finestra, BIANCO, self.rect, 2)




class Piattaforma(py.sprite.Sprite):

	def __init__(self, x, y, lunghezza):  #costruttore
		py.sprite.Sprite.__init__(self)
		self.image = py.transform.scale(img_piattaforma, (lunghezza, 10))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


	def update(self, scorrimento):

		#aggiorna la posizione delle piattaforme facendole scorrere
		self.rect.y += scorrimento

		#controlla se le piattaforme sono andate sotto lo schermo
		if self.rect.top > ALTEZZA_FINESTRA:
			self.kill() #le elimino in modo che il numero di piattafome create sia inferiore di MAX_PIATTAFORME



#creo gli oggetti delle classi
personaggio = Pannello(LUNGHEZZA_FINESTRA // 2, ALTEZZA_FINESTRA - 150)
#creazione di Group (liste ottimizzate per lavorare con gli oggetti Sprite) che conterrà le piattforme sulle quali saltare)
gruppo_piattaforme = py.sprite.Group()
#creazione piattaforma iniziale
piattaforma = Piattaforma(LUNGHEZZA_FINESTRA // 2 - 45, ALTEZZA_FINESTRA - 50, 90)
gruppo_piattaforme.add(piattaforma)


#loop del gioco
while run:

	orologio.tick(FPS)

	if game_over == False: #se in game
		scorrimento = personaggio.muovi() 

		#disegna background
		background_scorrimento += scorrimento
		if background_scorrimento >= 800: #ricomincia a disegnare lo schermo dall'inizio
			background_scorrimento = 0
		disegna_background(background_scorrimento)

		#genera piattaforme fino al massimo valore di piattaforme creabili
		if len(gruppo_piattaforme) < MAX_PIATTAFORME:
			#randomizzo ogni piattaforma
			lunghezza_p = random.randint(60, 110)
			posizioneX_p = random.randint(0, LUNGHEZZA_FINESTRA - lunghezza_p)
			posizioneY_p = piattaforma.rect.y - random.randint(80, 120) #prendo la posizione della piattaforma precedente e aggiungo (tolgo perchè va in alto) un valore random

			piattaforma = Piattaforma(posizioneX_p, posizioneY_p, lunghezza_p)
			gruppo_piattaforme.add(piattaforma) #aggiungo la piattaforma al gruppo

		#aggiorna le piattaforme
		gruppo_piattaforme.update(scorrimento)

		#aggiorna punti
		if scorrimento > 0:
			punteggio += scorrimento
			if punteggio > record: #aggiorno record
				record = punteggio

		#disegna sprites
		gruppo_piattaforme.draw(finestra)
		personaggio.disegna()

		#disegna il punteggio
		mostra_punteggio()

		#controlla game_over
		if personaggio.rect.top > ALTEZZA_FINESTRA:
			game_over = True

	else: #GAME OVER
		if dissolvenza < ALTEZZA_FINESTRA:
			dissolvenza += 5
			py.draw.rect(finestra, NERO, (0, 0, dissolvenza, ALTEZZA_FINESTRA))
		else:
			stampa_testo('GAME OVER', font_gameover, ROSSO, 60, 200)
			stampa_testo('Punteggio: ' + str(punteggio), font_grande, BIANCO, 210, 300)
			stampa_testo('Record: ' + str(record), font_grande, BIANCO, 230, 350)
			stampa_testo('PREMI SPAZIO PER GIOCARE ANCORA', font_grande, BIANCO, 50, 500)

			key = py.key.get_pressed() #ricomincia
			if key[py.K_SPACE]:
				#resetto variabili
				dissolvenza = 0
				game_over = False
				punteggio = 0
				scorrimento = 0
				personaggio.rect.center = (LUNGHEZZA_FINESTRA // 2, ALTEZZA_FINESTRA - 150) #pannello in posizione iniziale
				gruppo_piattaforme.empty() #cancella tutte le piattaforme create
				#creo di nuovo la piattaforma iniziale
				piattaforma = Piattaforma(LUNGHEZZA_FINESTRA // 2 - 45, ALTEZZA_FINESTRA - 50, 90)
				gruppo_piattaforme.add(piattaforma)


	#quando chiudere il gioco
	for evento in py.event.get():
		if evento.type == py.QUIT:
			run = False

	py.display.update()  #aggiornare lo schermo


py.quit() #chiudi gioco
