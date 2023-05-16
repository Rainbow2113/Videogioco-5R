import pygame   #Libreria necessarria per lo sviluppo di videogiochi su python
import random

pygame.init() #Funzione del modulo pygame che si occupa di inizializzare vari sottosistemi(grafica,input,audio)

white = (255, 255, 255) # definizioni colori   
green = (0, 255, 0)    
red= (255, 0, 0)    
black = (0,0,0)
yellow = (255, 255, 102)
blue = (50, 135, 213)

dis_width = 400 # dimensioni dello schermo
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('gioco dello snake')



snake_block = 15 # dimensioni e velocità del serpentello
snake_speed = 20

font_message = pygame.font.SysFont('arial', 20)
score_font = pygame.font.SysFont ('comicsums' , 30)

def Punteggio(score):
    value = score_font.render("punteggio: " , str(score), True, yellow) # stampa la variabile del punteggi
    dis.blit(value, [0 , 0])

def Serpentello(snake_block , snake_list):
    for x in snake_list:
       pygame.draw.rect(white, [x[0], x[1], snake_block , snake_block]) # stampa il serpentello
                        
def Messaggio(msg, color):
          mesg = font_message.render(msg, True, color) #stampa il messaggio
          dis.blit(mesg, [dis_width/15 , dis_height/5])
def Gioco():
          gioco_attivo = True
          game_over = False
          game_close = False
                   
          x1 = dis_width/2
          y1 = dis_height/2
                   
          x1_change = 0
          y1_change = 0
                   
          snake_list = []         
          lenght_of_snake = 1
                   
          foodx = round(random.randrange(0, dis_width - snake_block) /10.0) *10.0
          foody = round(random.randrange(0, dis_height - snake_block) /10.0) * 10.0
          

          while gioco_attivo:
              for x in snake_list[:-1]:
                  if  x == snake_Head:
                      game_close = True
                      Serpentello(snake_block, snake_list)
                      Punteggio(lenght_of_snake- 1)

              x1 += x1_change
              y1 += y1_change
              dis.fill(yellow)
              pygame.draw.rect(dis, green, (foodx, foody, snake_block, snake_block))
              snake_Head = []
              snake_Head.append(x1)
              snake_Head.append(y1)
              snake_list.append(snake_Head)
              if len(snake_list) > lenght_of_snake:
                     del snake_list[0]  
                     

              for event in pygame.event.get(): 
                      
                     if event.type == pygame.KEYDOWN:
                         
                        if event.key== pygame.K_c:
                            Gioco()

                        if event.key == pygame.K_LEFT:
                          x1_change = -snake_block
                          y1_change = 0            
                        elif event.key == pygame.K_RIGHT:
                          x1_change = snake_block
                          y1_change = 0
                        elif event.key == pygame.K_UP:
                          y1_change = -snake_block
                          x1_change = 0
                        elif event.key == pygame.K_DOWN:
                          y1_change = snake_block
                          x1_change = 0   
                   
              
              if x1  == foodx and y1 == foody:
                     foodx = round(random.randrange(0, dis_width - snake_block) /10.0) * 10.0
                     foody = round(random.randrange(0, dis_height - snake_block) /10.0) * 10.0
                     lenght_of_snake += 1
                   
              
              #if event.key == pygame.K_ESCAPE: 
              #             game_over = True
              #             game_class = False        
              if game_over == True:
                  dis.fill(blue)
                  Messaggio("Hai perso! Premi C Per continuare o Esc per uscire", red)
                  Punteggio = (lenght_of_snake - 1)
                                      
          pygame.display.update
                   
                  
             
          pygame.quit()
          quit()
         
         
Gioco()